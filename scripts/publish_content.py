"""Package reviewed content and import without touching learning records."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'backend'))
import db
from study import question_hash


def digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True).encode()).hexdigest()


def package(require_complete=False):
    data=ROOT/'backend/data/authoring'
    solutions={r['key']:r for p in sorted(data.glob('*-Q*.json')) for r in [json.loads(p.read_text())]}
    reviews={}
    for key,s in solutions.items():
        path=data/'audited'/(key+'.json')
        if not path.exists():continue
        review=json.loads(path.read_text())
        if review.get('draft_hash')!=digest(s):continue
        if review['verdict']!='pass':
            s.update({k:review[k] for k in ('answer','solution','issue')})
        if review['verdict']=='uncertain':s['source_verified']=False
        reviews[key]=review
        s['review_status']=review['verdict']
    manual_path=ROOT/'content/manual-solutions.json'
    if manual_path.exists():
        for key,s in json.loads(manual_path.read_text()).items():
            solutions[key]=s
            reviews[key]={'key':key,'verdict':'manual','findings':s['manual_review'],'content_hash':s['content_hash']}
    # Unreviewed authoring drafts never enter a publishable package.
    solutions={k:s for k,s in solutions.items() if k in reviews}
    source_input={s['id']:s for s in json.loads((data/'exam-input.json').read_text())}
    visual_reviews=[]
    for path in sorted((data/'relations-visual').glob('*.json')):
        review=json.loads(path.read_text())
        draft=json.loads((data/f"relations-{review['source_id']}.json").read_text())
        if digest(draft)==review['draft_hash']:visual_reviews.append(review)
    relations=[r for review in visual_reviews for r in review['relations']]
    sources=[{'id':review['source_id'],'source_hash':review['source_hash']} for review in visual_reviews]
    exam_solutions={s['question_id']:s for p in sorted((data/'exam-solutions').glob('*.json')) for s in [json.loads(p.read_text())]}
    if require_complete:
        from import_workbook import records
        if set(solutions)!={r['source_key'] for r in records()} or set(reviews)!=set(solutions):
            raise ValueError(f'Content incomplete: {len(solutions)} solutions, {len(reviews)} reviews; expected 929 each')
        if {s['id'] for s in sources}!=set(source_input):
            raise ValueError('Not every core exam question has a reviewed relation result')
        if set(exam_solutions)!={s['id'] for s in source_input.values() if not s['solution_html']}:
            raise ValueError('Missing core exam explanations')
    for filename,values in [('solutions.json',solutions),('relations.json',relations),('relation-sources.json',sources),('solution-reviews.json',reviews),('exam-solutions.json',exam_solutions),('relation-reviews.json',visual_reviews)]:
        (ROOT/'content'/filename).write_text(json.dumps(values,ensure_ascii=False,indent=2)+'\n')
    return solutions,relations,sources


def apply(solutions,relations,sources):
    conn=db.connect();db.init_db(conn)
    counts={'solutions':0,'exam_solutions':0,'relations':0,'reviewed_sources':0,'stale_solutions':[],'stale_relations':[]}
    by_source={s['id']:[] for s in sources}
    for r in relations:
        if r['source_id'] not in by_source:raise ValueError('Relation has no reviewed source manifest')
        if r['stage'] not in ('同法练习','变式检验'):raise ValueError('Invalid relation stage')
        by_source[r['source_id']].append(r)
    with conn:
        for s in json.loads((ROOT/'content/exam-solutions.json').read_text()).values():
            row=conn.execute('SELECT stem_html,options_json FROM questions WHERE id=?',(s['question_id'],)).fetchone()
            if not row or question_hash(row[0],row[1])!=s['content_hash']:
                counts['stale_solutions'].append(s['key']);continue
            solution=s['solution']
            if s.get('issue'):solution='> **核对说明：** '+s['issue']+'\n\n'+solution
            conn.execute('''INSERT INTO exam_explanations(question_id,content_hash,solution_markdown,solution_source,answer_checkable)
              VALUES(?,?,?,?,?) ON CONFLICT(question_id) DO UPDATE SET content_hash=excluded.content_hash,
              solution_markdown=excluded.solution_markdown,solution_source=excluded.solution_source,answer_checkable=excluded.answer_checkable''',
              (s['question_id'],s['content_hash'],solution,'根据本题条件整理的补充讲解；参考答案沿用已入库真题。',int(not bool(s.get('issue')))))
            counts['exam_solutions']+=1
        for key,s in solutions.items():
            row=conn.execute('SELECT question_id,content_hash FROM workbook_text WHERE source_key=?',(key,)).fetchone()
            if not row or row['content_hash']!=s['content_hash']:
                counts['stale_solutions'].append(key);continue
            solution=s['solution']
            if s.get('issue'):solution='> **核对说明：** '+s['issue']+'\n\n'+solution
            source=('参考《27版880参考答案》PDF第 '+ '、'.join(map(str,s['source_pages']))+' 页整理，含解题思路补充。') if s.get('source_verified') and s.get('source_pages') else '补充推导（未完全对应原书解析），请结合核对说明阅读。'
            conn.execute('UPDATE workbook_text SET solution_markdown=?,solution_source=? WHERE question_id=?',(solution,source,row['question_id']))
            answer=s.get('answer','') if s.get('source_verified') and not s.get('issue') else ''
            conn.execute('UPDATE questions SET answer=? WHERE id=?',(answer,row['question_id']))
            counts['solutions']+=1
        # Each reviewed source replaces its old set exactly, including an empty set.
        for manifest in sources:
            sid=manifest['id'];source=conn.execute('SELECT stem_html,options_json FROM questions WHERE id=?',(sid,)).fetchone()
            if not source or question_hash(source[0],source[1])!=manifest['source_hash']:
                counts['stale_relations'].append([sid,None]);continue
            rows=by_source[sid];stale=False
            for r in rows:
                target=conn.execute('SELECT content_hash FROM workbook_text WHERE question_id=?',(r['target_id'],)).fetchone()
                if r['source_hash']!=manifest['source_hash'] or not target or target[0]!=r['target_hash']:
                    counts['stale_relations'].append([sid,r['target_id']]);stale=True
            if stale:continue
            conn.execute('DELETE FROM math_relations WHERE source_id=?',(sid,))
            for r in rows:
                conn.execute('''INSERT INTO math_relations(source_id,target_id,skill,reason,stage,source_hash,target_hash)
                  VALUES(?,?,?,?,?,?,?)''',tuple(r[k] for k in ('source_id','target_id','skill','reason','stage','source_hash','target_hash')))
                counts['relations']+=1
            counts['reviewed_sources']+=1
    conn.close();return counts


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--package',action='store_true');p.add_argument('--apply',action='store_true');p.add_argument('--require-complete',action='store_true');args=p.parse_args()
    if args.package:s,r,sources=package(args.require_complete)
    else:
        s=json.loads((ROOT/'content/solutions.json').read_text());r=json.loads((ROOT/'content/relations.json').read_text());sources=json.loads((ROOT/'content/relation-sources.json').read_text())
    print(json.dumps(apply(s,r,sources) if args.apply else {'solutions':len(s),'audited':sum('review_status' in v for v in s.values()),'relations':len(r),'reviewed_sources':len(sources)},ensure_ascii=False))
