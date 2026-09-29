"""Structured workbook content; original database IDs survive text replacement."""
import hashlib
import json
from notes import connection


def fingerprint(row):
    return hashlib.sha256((row.get('stem_markdown') or row.get('stem_html', '')).encode()).hexdigest()


def enrich(problems):
    if not problems:
        return problems
    with connection() as conn:
        content = {r['question_id']: dict(r) for r in conn.execute('SELECT * FROM workbook_text')}
    for p in problems:
        if p['id'] not in content:
            continue
        row = content[p['id']]
        p.update({k: row[k] for k in ('stem_markdown', 'source_key', 'source_pages', 'original_number', 'book')})
        p['options'] = json.loads(row['options_markdown'])
        p['options_are_markdown'] = True
        if row['source_key'] in {'calculus-Q107','calculus-Q179','calculus-Q191','calculus-Q374','calculus-Q385','calculus-Q612'}:
            p['figure_url'] = '/figures/workbook/' + row['source_key'] + '.png'
        p['has_sol'] = bool(row['solution_markdown'])
        p['src'] = '李林880 · ' + ('高数' if row['book'] == 'calculus' else '线代') + f" · 第{row['chapter_number']}章 · {p.get('level', '')} · " + (f"原题({row['original_number']})" if row['original_number'] else '原书未编号题')
        p.pop('answer_url', None)
    return problems
