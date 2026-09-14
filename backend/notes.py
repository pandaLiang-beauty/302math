"""Question notes shared by exam papers, workbook practice and the notebook."""
from contextlib import contextmanager
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

import db
from practice_catalog import CHAPTER_BY_KEY
from typedefs import PAPER_CN

router = APIRouter(prefix='/api')


@contextmanager
def connection():
    conn = db.connect()
    try:
        with conn:
            yield conn
    finally:
        conn.close()


def question_info(conn, question_id):
    row = conn.execute(
        'SELECT id,paper,year,number,qtype,subject,chapter,type_name,stem_html '
        'FROM questions WHERE id=?', (question_id,),
    ).fetchone()
    if row is None:
        raise HTTPException(404, '题目不存在')
    question = dict(row)
    question['source'] = (f"李林880 · {row['chapter']} · 题库编号 {row['number']}" if row['paper'] == 'lilin880'
                          else f"{PAPER_CN.get(row['paper'], row['paper'])} · {row['year']} 年 · 第 {row['number']} 题")
    question['practice_chapter'] = next((key for key, chapter in CHAPTER_BY_KEY.items()
                                         if chapter.book_chapter == row['chapter']), '')
    return question


def get_record(conn, note_id):
    row = conn.execute('SELECT * FROM notes WHERE id=?', (note_id,)).fetchone()
    if row is None:
        raise HTTPException(404, '这条笔记已不存在，请刷新后重试')
    return dict(row)


def validate_body(body):
    if not body.strip():
        raise HTTPException(400, '请先填写笔记内容')
    return body


class CreateNote(BaseModel):
    question_id: int = Field(gt=0)
    body: str = Field(max_length=20000)
    client_id: str = Field(min_length=16, max_length=80, pattern=r'^[a-zA-Z0-9_-]+$')


class UpdateNote(BaseModel):
    body: str = Field(max_length=20000)
    revision: int = Field(gt=0)


@router.get('/notes')
def list_notes(question_id: int):
    with connection() as conn:
        question = question_info(conn, question_id)
        records = [dict(row) for row in conn.execute('SELECT * FROM notes WHERE question_id=? ORDER BY id', (question_id,))]
        return {'question': question, 'notes': records}


@router.post('/notes')
def create_note(payload: CreateNote):
    body = validate_body(payload.body)
    with connection() as conn:
        question_info(conn, payload.question_id)
        conn.execute('INSERT OR IGNORE INTO notes(question_id,body,client_id) VALUES(?,?,?)',
                     (payload.question_id, body, payload.client_id))
        record = dict(conn.execute('SELECT * FROM notes WHERE client_id=?', (payload.client_id,)).fetchone())
        if record['question_id'] != payload.question_id or record['body'] != body:
            raise HTTPException(409, '上一版笔记已经保存，请刷新笔记后核对；当前草稿仍会保留')
        return record


@router.patch('/notes/{note_id}')
def update_note(note_id: int, payload: UpdateNote):
    body = validate_body(payload.body)
    with connection() as conn:
        current = get_record(conn, note_id)
        if current['body'] == body:
            return current
        changed = conn.execute('UPDATE notes SET body=?,revision=revision+1,updated_at=CURRENT_TIMESTAMP '
                               'WHERE id=? AND revision=?', (body, note_id, payload.revision))
        if not changed.rowcount:
            raise HTTPException(409, '笔记已在其他页面更新，请刷新笔记后核对；当前草稿仍会保留')
        return get_record(conn, note_id)


@router.delete('/notes/{note_id}')
def delete_note(note_id: int, revision: int):
    with connection() as conn:
        get_record(conn, note_id)
        changed = conn.execute('DELETE FROM notes WHERE id=? AND revision=?', (note_id, revision))
        if not changed.rowcount:
            raise HTTPException(409, '笔记已在其他页面更新，请刷新后再删除')
        return {'ok': True}


@router.get('/notebook')
def notebook(query: str = '', source: Literal['', 'exam', 'lilin880'] = ''):
    query = query.strip()[:200]
    sql = ('SELECT DISTINCT q.id FROM questions q JOIN notes n ON n.question_id=q.id '
           "WHERE (?='' OR instr(lower(n.body),lower(?))>0 OR instr(lower(q.chapter),lower(?))>0) ")
    args = [query, query, query]
    if source == 'exam':
        sql += "AND q.paper LIKE 'math%' "
    elif source == 'lilin880':
        sql += "AND q.paper='lilin880' "
    sql += 'GROUP BY q.id ORDER BY MAX(n.updated_at) DESC,MAX(n.id) DESC'
    with connection() as conn:
        groups = []
        for row in conn.execute(sql, args).fetchall():
            records = [dict(note) for note in conn.execute('SELECT * FROM notes WHERE question_id=? ORDER BY id', (row['id'],))]
            groups.append({'question': question_info(conn, row['id']), 'notes': records})
        return groups
