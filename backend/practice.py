"""Read-only exam-to-workbook navigation; no reseeding or learning-data changes."""
import json
import re
from pathlib import Path

from fastapi import HTTPException

from practice_catalog import (
    CHAPTERS, CHAPTER_BY_KEY, TOPICS, TOPIC_BY_KEY, source_chapter, source_topics,
)
from typedefs import QTYPE_CN


ROOT = Path(__file__).resolve().parents[1]
BOOKS = {
    '880-answers': ROOT / '【PDF】27版880参考答案(1).pdf',
    '880-calculus': ROOT / '【A4留白版】李林880数二高数篇做题本.pdf',
    '880-algebra': ROOT / '【A4留白版】李林880数二线代篇做题本.pdf',
}
# PDF page numbers from the bundled 27th-edition answer book's own bookmarks.
ANSWER_PAGES = dict(zip(CHAPTER_BY_KEY, (
    (3, 9, 25), (29, 49, 70), (73, 95, 129), (134, 144, 158),
    (160, 172, 188), (193, 201, 219), (221, 225, 231), (233, 242, 249),
    (250, 255, 262), (264, 271, 282), (284, 296, 315), (317, 326, 347),
)))


def progress(problems):
    return {
        'total': len(problems),
        'done': sum(bool(p['last']) for p in problems),
        'correct': sum(p['last'] == 'correct' for p in problems),
        'wrong': sum(p['last'] == 'wrong' for p in problems),
        'fuzzy': sum(p['last'] == 'fuzzy' for p in problems),
    }


def catalog(conn):
    rows = [dict(row) for row in conn.execute("""
        SELECT q.number,q.chapter,
               (SELECT result FROM attempts a WHERE a.question_id=q.id ORDER BY a.id DESC LIMIT 1) last
        FROM questions q WHERE q.paper='lilin880' ORDER BY q.number
    """)]
    result = []
    for chapter in CHAPTERS:
        members = [row for row in rows if row['chapter'] == chapter.book_chapter]
        topics = []
        for topic in TOPICS:
            if topic.chapter != chapter.key:
                continue
            numbers = set(topic.numbers)
            topics.append({
                'id': topic.key, 'name': topic.name, 'chapter': chapter.key,
                **progress([row for row in members if row['number'] in numbers]),
            })
        result.append({
            'id': chapter.key, 'name': chapter.name, 'book_chapter': chapter.book_chapter,
            'subject': chapter.subject, 'topics': topics, **progress(members),
        })
    return result


def recommendation(question, chapters):
    chapter_id = source_chapter(question)
    if not chapter_id:
        return None
    chapters_by_id = {c['id']: c for c in chapters}
    topics_by_id = {t['id']: t for c in chapters for t in c['topics']}
    topics = [topics_by_id[t.key] for t in source_topics(question)]
    chapter = chapters_by_id[chapter_id]
    return {
        'chapter': chapter_id,
        'chapter_name': chapter['name'],
        'topic': topics[0]['id'] if topics else None,
        'name': topics[0]['name'] if topics else chapter['name'],
        'total': topics[0]['total'] if topics else chapter['total'],
        'topics': topics,
        'match': 'topic' if topics else 'chapter',
    }


def get_practice(conn, *, question_id=None, chapter='', topic=''):
    chapters = catalog(conn)
    origin = None
    suggested = None
    if question_id is not None:
        row = conn.execute(
            'SELECT id,paper,year,number,subject,chapter,point,type_name,stem_html,options_json '
            'FROM questions WHERE id=?', (question_id,),
        ).fetchone()
        if row is None:
            raise HTTPException(404, '真题不存在')
        origin = dict(row)
        origin['options'] = json.loads(origin.pop('options_json') or '[]')
        if origin['paper'] != 'math2':
            raise HTTPException(400, '请从数二真题进入对应练习')
        suggested = recommendation(origin, chapters)

    if topic:
        selected_topic = TOPIC_BY_KEY.get(topic)
        if not selected_topic:
            raise HTTPException(404, '知识点不存在')
        if chapter and chapter != selected_topic.chapter:
            raise HTTPException(400, '知识点不属于所选章节')
        chapter = selected_topic.chapter
    elif not chapter and suggested:
        chapter, topic = suggested['chapter'], suggested['topic'] or ''

    selected_chapter = CHAPTER_BY_KEY.get(chapter)
    if not selected_chapter:
        raise HTTPException(404, '暂未找到对应的880章节，请从章节练习选择')

    # Every practice query keeps the book restriction even for topic selections.
    sql = """
        SELECT q.id,q.paper,q.year,q.number,q.qtype,q.level,q.chapter,q.type_name,
               q.stem_html,q.options_json,q.plain,
               (q.solution_html<>'' OR q.answer_html<>'') has_sol,
               (SELECT COUNT(*) FROM notes n WHERE n.question_id=q.id) note_count,
               (SELECT result FROM attempts a WHERE a.question_id=q.id ORDER BY a.id DESC LIMIT 1) last
        FROM questions q WHERE q.paper='lilin880' AND q.chapter=?
    """
    args = [selected_chapter.book_chapter]
    if topic:
        numbers = TOPIC_BY_KEY[topic].numbers
        sql += ' AND q.number IN (' + ','.join('?' for _ in numbers) + ')'
        args.extend(numbers)
    sql += " ORDER BY CASE q.level WHEN '基础' THEN 0 WHEN '综合' THEN 1 ELSE 2 END,q.number,q.id"
    problems = [dict(row) for row in conn.execute(sql, args)]
    answers_available = BOOKS['880-answers'].is_file()
    for p in problems:
        p['options'] = json.loads(p.pop('options_json') or '[]')
        p['qtype_cn'] = QTYPE_CN.get(p['qtype'], p['qtype'])
        book_number = re.search(r'\((\d+)\)', p.pop('plain'))
        p['book_number'] = int(book_number.group(1)) if book_number else None
        p['src'] = '李林880 · %s · %s' % (p['chapter'], p['qtype_cn'])
        p['src'] += '（%d）' % p['book_number'] if p['book_number'] else ' · 题库编号 %d' % p['number']
        if answers_available:
            page = ANSWER_PAGES[chapter][{'基础': 0, '综合': 1, '拓展': 2}.get(p['level'], 0)]
            p['answer_url'] = '/api/books/880-answers#page=' + str(page)

    chapter_data = next(c for c in chapters if c['id'] == chapter)
    selected = next((t for t in chapter_data['topics'] if t['id'] == topic), None)
    workbook = '880-calculus' if selected_chapter.subject == '高等数学' else '880-algebra'
    books = [
        {'name': name, 'url': '/api/books/' + key}
        for key, name in (('880-answers', '880原版答案册'), (workbook, '880原版做题本'))
        if BOOKS[key].is_file()
    ]
    for book in books:
        if book['url'].endswith('880-answers'):
            book['url'] += '#page=' + str(ANSWER_PAGES[chapter][0])
    return {
        'chapter': chapter_data, 'topic': selected, 'origin': origin,
        'suggested_topics': suggested['topics'] if suggested else [],
        'match': 'topic' if selected else 'chapter',
        'problems': problems, 'progress': progress(problems), 'books': books,
    }
