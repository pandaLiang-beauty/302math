"""Build explicit exam ↔ workbook links; publish links only, transactionally."""
import argparse
import json
import re
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
import db
from study import question_hash
STAGES = ('同法练习', '变式检验', '基础衔接')
OUTPUT = ROOT / 'content/complete-relations.json'

def build():
    conn = db.connect()
    try:
        targets = {r['question_id']: dict(r) for r in conn.execute('SELECT * FROM workbook_text')}
        sources = {r['id']: question_hash(r['stem_html'], r['options_json']) for r in conn.execute("SELECT * FROM questions WHERE paper='math2'")}
        pairs = {(p['source_id'], p['target_id']): p for p in json.loads((ROOT / 'content/relations.json').read_text())}
        def label(match):
            target = targets.get(int(match[0]))
            return target['source_key'].replace('calculus-', '高数 ').replace('algebra-', '线代 ') if target else match[0]
        for line in (ROOT / 'content/coverage-links.tsv').read_text().splitlines():
            if not line or line.startswith('#'): continue
            sid, ids, stage, skill, reason = line.split('|')
            sid = int(sid)
            for tid in map(int, ids.split(',')):
                pair = dict(source_id=sid, target_id=tid, stage=stage, skill=skill,
                            reason=re.sub(r'\b\d{5}\b', label, reason), source_hash=sources[sid], target_hash=targets[tid]['content_hash'])
                pairs.setdefault((sid, tid), pair)
        rows = list(pairs.values())
        validate(conn, rows)
        OUTPUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
        return counts(conn, rows)
    finally: conn.close()

def validate(conn, rows):
    targets = {r['question_id']: r['content_hash'] for r in conn.execute('SELECT question_id,content_hash FROM workbook_text')}
    sources = {r['id']: question_hash(r['stem_html'], r['options_json']) for r in conn.execute("SELECT id,stem_html,options_json FROM questions WHERE paper='math2'")}
    core = {r[0] for r in conn.execute("SELECT id FROM questions WHERE paper='math2' AND year BETWEEN 2020 AND 2026")}
    seen = set()
    for p in rows:
        key = p['source_id'], p['target_id']
        if key in seen: raise ValueError(f'Duplicate pair {key}')
        seen.add(key)
        if p['stage'] not in STAGES or not p['reason'].strip() or not p['skill'].strip(): raise ValueError(f'Invalid relation {key}')
        if sources.get(key[0]) != p['source_hash']: raise ValueError(f'Stale source {key[0]}')
        if targets.get(key[1]) != p['target_hash']: raise ValueError(f'Stale target {key[1]}')
    missing_targets = set(targets) - {p['target_id'] for p in rows}
    missing_core = core - {p['source_id'] for p in rows}
    if missing_targets or missing_core: raise ValueError(f'Missing workbook {sorted(missing_targets)}, core exams {sorted(missing_core)}')

def counts(conn, rows):
    return dict(relations=len(rows), workbook_questions=len({p['target_id'] for p in rows}), exam_questions=len({p['source_id'] for p in rows}))

def apply():
    rows = json.loads(OUTPUT.read_text())
    conn = db.connect()
    try:
        with conn:
            conn.execute('BEGIN IMMEDIATE')
            validate(conn, rows)
            conn.execute('DELETE FROM math_relations')
            conn.executemany('INSERT INTO math_relations VALUES(?,?,?,?,?,?,?)', [tuple(p[k] for k in ('source_id','target_id','skill','reason','stage','source_hash','target_hash')) for p in rows])
        return counts(conn, rows)
    finally: conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--build', action='store_true')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    if args.build: print(json.dumps(build()))
    if args.apply: print(json.dumps(apply()))
