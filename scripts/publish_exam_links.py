"""Publish exam/workbook links and existing reference answers, without generating explanations."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
import db
from study import question_hash


def read(path):
    return json.loads(path.read_text())


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def package():
    data = ROOT / 'backend/data/authoring'
    original = {s['id']: s for s in read(data / 'exam-input.json')}
    conn = db.connect()
    targets = {r['question_id']: dict(r) for r in conn.execute('SELECT * FROM workbook_text')}
    conn.close()
    reviewed = {}
    for path in (data / 'relations-visual').glob('*.json'):
        review = read(path)
        if review['draft_hash'] == digest(read(data / f"relations-{review['source_id']}.json")):
            reviewed[review['source_id']] = review
    for sid, review in read(ROOT / 'content/manual-relations.json').items():
        reviewed[int(sid)] = {'source_id': int(sid), 'source_hash': original[int(sid)]['content_hash'], **review}
    if set(reviewed) != set(original):
        raise ValueError('Every core exam question must have a reviewed relation result')
    relations = []; manifests = []
    for sid, review in sorted(reviewed.items()):
        manifests.append({'id': sid, 'source_hash': review['source_hash']})
        unique = {}
        for pair in review['relations']:
            tid = pair['target_id']
            if tid not in targets: raise ValueError(f'Missing target {tid}')
            row = {k: pair[k] for k in ('source_id', 'target_id', 'skill', 'reason', 'stage')}
            row.update(source_hash=review['source_hash'], target_hash=pair.get('target_hash', targets[tid]['content_hash']))
            if tid in unique:
                if row['reason'] not in unique[tid]['reason']: unique[tid]['reason'] += ' ' + row['reason']
            else: unique[tid] = row
        relations.extend(unique.values())
    # Reuse completed checks only. Unreviewed drafts never become reference answers.
    answers = {}
    candidates = read(ROOT / 'content/solutions.json')
    for path in (data / 'audited').glob('*.json'):
        review = read(path); draft_path = data / path.name
        if not draft_path.exists(): continue
        draft = read(draft_path)
        if review.get('draft_hash') != digest(draft): continue
        if review['verdict'] != 'pass': draft.update({k: review[k] for k in ('answer', 'issue')})
        if review['verdict'] == 'uncertain': continue
        candidates[draft['key']] = draft
    candidates.update(read(ROOT / 'content/manual-solutions.json'))
    for key, value in candidates.items():
        if not value.get('answer'): continue
        answers[key] = {'answer': value['answer'], 'content_hash': value['content_hash'],
            'note': value.get('issue', ''), 'source_pages': value.get('source_pages', []),
            'checkable': bool(value.get('source_verified') and not value.get('issue'))}
    answers.update(read(ROOT / 'content/reference-answer-corrections.json'))
    for name, value in [('relations.json', relations), ('relation-sources.json', manifests), ('reference-answers.json', answers)]:
        (ROOT / 'content' / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    return {'relations': len(relations), 'reviewed_sources': len(manifests), 'answers': len(answers)}


def apply():
    relations = read(ROOT / 'content/relations.json')
    manifests = read(ROOT / 'content/relation-sources.json')
    answers = read(ROOT / 'content/reference-answers.json')
    conn = db.connect(); db.init_db(conn)
    counts = {'relations': 0, 'reviewed_sources': 0, 'answers': 0}
    try:
        with conn:
            for manifest in manifests:
                sid = manifest['id']
                row = conn.execute('SELECT stem_html,options_json FROM questions WHERE id=?', (sid,)).fetchone()
                if not row or question_hash(*row) != manifest['source_hash']: raise ValueError(f'Stale source {sid}')
            seen = set()
            for pair in relations:
                identity = (pair['source_id'], pair['target_id'])
                if identity in seen: raise ValueError(f'Duplicate pair {identity}')
                seen.add(identity)
                if pair['stage'] not in ('同法练习', '变式检验', '基础衔接') or not pair['reason'] or not pair['skill']: raise ValueError('Invalid relation')
                row = conn.execute('SELECT content_hash FROM workbook_text WHERE question_id=?', (pair['target_id'],)).fetchone()
                if not row or row[0] != pair['target_hash']: raise ValueError(f'Stale target {pair["target_id"]}')
                if not any(m['id']==pair['source_id'] and m['source_hash']==pair['source_hash'] for m in manifests): raise ValueError('Unreviewed source')
            for manifest in manifests:
                conn.execute('DELETE FROM math_relations WHERE source_id=?', (manifest['id'],))
            for pair in relations:
                conn.execute('INSERT INTO math_relations VALUES(?,?,?,?,?,?,?)', tuple(pair[k] for k in ('source_id','target_id','skill','reason','stage','source_hash','target_hash')))
            for key, answer in answers.items():
                row = conn.execute('SELECT question_id,content_hash FROM workbook_text WHERE source_key=?', (key,)).fetchone()
                if not row or row['content_hash'] != answer['content_hash']: raise ValueError(f'Stale answer {key}')
                conn.execute('''INSERT INTO reference_answers(question_id,content_hash,answer,note,source_pages,checkable)
                    VALUES(?,?,?,?,?,?) ON CONFLICT(question_id) DO UPDATE SET content_hash=excluded.content_hash,
                    answer=excluded.answer,note=excluded.note,source_pages=excluded.source_pages,checkable=excluded.checkable''',
                    (row['question_id'], answer['content_hash'], answer['answer'], answer['note'], json.dumps(answer['source_pages']), int(answer['checkable'])))
                conn.execute('UPDATE questions SET answer=? WHERE id=?', (answer['answer'] if answer['checkable'] else '', row['question_id']))
            counts.update(relations=len(relations), reviewed_sources=len(manifests), answers=len(answers))
    finally: conn.close()
    return counts


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--package', action='store_true'); parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    if args.package: print(json.dumps(package(), ensure_ascii=False))
    if args.apply: print(json.dumps(apply(), ensure_ascii=False))
