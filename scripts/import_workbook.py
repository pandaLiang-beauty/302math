"""Validate and incrementally import the supplied Markdown; never reseed questions."""
import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))
import db

KINDS = {'选择题': 'choice', '填空题': 'blank', '解答题': 'subjective'}


def parse_book(path, book):
    records, current, chapter, section = [], None, '', ''
    chapter_number = 0 if book == 'calculus' else 6
    for line in path.read_text().splitlines():
        if line.startswith(('## ', '### ', '#### Q')) and current:
            records.append(current)
            current = None
        if line.startswith('## '):
            chapter = re.sub(r'^## 第[一二三四五六七八九十]+章', '', line).replace('、', '')
            chapter_number += 1
        elif line.startswith('### '):
            section = line[4:].split(' · ')
        elif line.startswith('#### Q'):
            match = re.fullmatch(r'#### (Q\d+)｜(.*?)｜PDF第([\d–]+)页', line)
            if not match:
                raise ValueError('Invalid question heading: ' + line)
            original = re.search(r'\((\d+)\)', match[2])
            current = dict(source_key=book + '-' + match[1], book=book, chapter=chapter,
                           chapter_number=chapter_number, level=section[0].removesuffix('题'),
                           qtype=KINDS[section[1]], original_number=int(original[1]) if original else None,
                           source_pages=match[3], body='')
        elif current:
            current['body'] += line + '\n'
    if current:
        records.append(current)
    for r in records:
        body = r.pop('body').strip()
        diagrams = re.findall(r'^【图示文字转写】[^\n]+', body, re.M)
        body = re.sub(r'^【图示文字转写】[^\n]+', '', body, flags=re.M).strip()
        r['options'] = []
        if r['qtype'] == 'choice':
            pieces = re.split(r'^([ABCD])[.．、]', body, flags=re.M)
            if pieces[1::2] != list('ABCD'):
                raise ValueError('Missing options: ' + r['source_key'])
            r['options'] = [{'key': k, 'text': text.strip()} for k, text in zip(pieces[1::2], pieces[2::2])]
            body = pieces[0].strip()
        if diagrams:
            body += '\n\n' + '\n\n'.join(diagrams)
        r['stem_markdown'] = body
        r['content_hash'] = hashlib.sha256(json.dumps([body, r['options']], ensure_ascii=False).encode()).hexdigest()
    return records


def records():
    incoming = parse_book(ROOT / 'content/workbooks/calculus.md', 'calculus') + parse_book(ROOT / 'content/workbooks/algebra.md', 'algebra')
    path=ROOT/'content/transcription-corrections.json'
    corrections=json.loads(path.read_text()) if path.exists() else {}
    for r in incoming:
        if r['source_key'] not in corrections:continue
        correction=corrections[r['source_key']]
        for before,after in correction['replacements']:
            if r['stem_markdown'].count(before)!=1:raise ValueError('Transcription correction no longer matches '+r['source_key'])
            r['stem_markdown']=r['stem_markdown'].replace(before,after)
        r['stem_markdown']+='\n\n> 校勘：'+correction['note']
        r['content_hash']=hashlib.sha256(json.dumps([r['stem_markdown'],r['options']],ensure_ascii=False).encode()).hexdigest()
    return incoming


def apply(conn, incoming):
    # Existing numbers 1..925 are kept. Four unnumbered questions are appended.
    legacy_number = 0
    for r in incoming:
        if r['original_number'] is not None:
            legacy_number += 1
        existing = conn.execute('SELECT question_id,content_hash FROM workbook_text WHERE source_key=?', (r['source_key'],)).fetchone()
        if existing:
            qid = existing[0]
            if existing['content_hash'] != r['content_hash']:
                conn.execute("UPDATE workbook_text SET solution_markdown='',solution_source='' WHERE question_id=?", (qid,))
                conn.execute("UPDATE questions SET answer='' WHERE id=?", (qid,))
        elif r['original_number'] is not None:
            old = conn.execute("SELECT * FROM questions WHERE paper='lilin880' AND number=?", (legacy_number,)).fetchone()
            if not old or (old['chapter'], old['level'], old['qtype']) != (r['chapter'], r['level'], r['qtype']):
                raise ValueError('Legacy metadata mismatch at ' + r['source_key'])
            qid = old['id']
        else:
            number = conn.execute("SELECT COALESCE(MAX(number),925)+1 FROM questions WHERE paper='lilin880'").fetchone()[0]
            cur = conn.execute("INSERT INTO questions(paper,year,number,qtype,subject,chapter,type_name,level) VALUES('lilin880',0,?,?,?,?,?,?)",
                (number, r['qtype'], '高等数学' if r['book'] == 'calculus' else '线性代数', r['chapter'], db.fallback_880_type(r['chapter']), r['level']))
            qid = cur.lastrowid
        conn.execute('''INSERT INTO workbook_text(question_id,source_key,book,chapter_number,original_number,source_pages,stem_markdown,options_markdown,content_hash)
          VALUES(?,?,?,?,?,?,?,?,?) ON CONFLICT(question_id) DO UPDATE SET source_pages=excluded.source_pages,
          stem_markdown=excluded.stem_markdown,options_markdown=excluded.options_markdown,content_hash=excluded.content_hash''',
          (qid,r['source_key'],r['book'],r['chapter_number'],r['original_number'],r['source_pages'],r['stem_markdown'],json.dumps(r['options'],ensure_ascii=False),r['content_hash']))
        conn.execute('UPDATE questions SET stem_html=?,options_json=?,plain=? WHERE id=?',
          ('<p>' + html.escape(r['stem_markdown']) + '</p>', json.dumps(r['options'],ensure_ascii=False),r['stem_markdown'],qid))
    db.sync_880_fallback_types(conn)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    incoming = records()
    assert len(incoming) == 929 and len({r['source_key'] for r in incoming}) == 929
    if args.apply:
        conn = db.connect()
        db.init_db(conn)
        with conn:
            apply(conn, incoming)
        conn.close()
    print(json.dumps({'questions': len(incoming), 'unnumbered': sum(r['original_number'] is None for r in incoming), 'applied': args.apply}))
