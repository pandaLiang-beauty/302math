"""Server-owned work in progress and immutable snapshots of each completed attempt."""
import json
import hashlib
from typing import Literal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from notes import connection

router = APIRouter(prefix='/api/study')


def question_hash(stem_html, options_json):
    return hashlib.sha256(json.dumps([stem_html, options_json], ensure_ascii=False).encode()).hexdigest()


def init(conn):
    conn.executescript('''
    CREATE TABLE IF NOT EXISTS study_sessions(
      id INTEGER PRIMARY KEY, scope TEXT NOT NULL UNIQUE, title TEXT NOT NULL,
      origin_id INTEGER REFERENCES questions(id), created_at TEXT DEFAULT CURRENT_TIMESTAMP);
    CREATE TABLE IF NOT EXISTS study_items(
      session_id INTEGER REFERENCES study_sessions(id), question_id INTEGER REFERENCES questions(id),
      answer TEXT NOT NULL DEFAULT '', work TEXT NOT NULL DEFAULT '', phase TEXT NOT NULL DEFAULT 'work',
      rating TEXT NOT NULL DEFAULT '', reason TEXT NOT NULL DEFAULT '', revision INTEGER NOT NULL DEFAULT 0,
      mutation TEXT NOT NULL DEFAULT '', updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY(session_id,question_id));
    CREATE TABLE IF NOT EXISTS study_history(
      id INTEGER PRIMARY KEY, session_id INTEGER REFERENCES study_sessions(id),
      question_id INTEGER REFERENCES questions(id), revision INTEGER NOT NULL,
      snapshot TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP,
      UNIQUE(session_id,question_id,revision));
    CREATE INDEX IF NOT EXISTS idx_study_history_question ON study_history(question_id,id);
    CREATE TABLE IF NOT EXISTS workbook_text(
      question_id INTEGER PRIMARY KEY REFERENCES questions(id), source_key TEXT NOT NULL UNIQUE,
      book TEXT NOT NULL, chapter_number INTEGER NOT NULL, original_number INTEGER,
      source_pages TEXT NOT NULL, stem_markdown TEXT NOT NULL, options_markdown TEXT NOT NULL,
      solution_markdown TEXT NOT NULL DEFAULT '', solution_source TEXT NOT NULL DEFAULT '',
      method_json TEXT NOT NULL DEFAULT '[]', content_hash TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS reference_answers(
      question_id INTEGER PRIMARY KEY REFERENCES questions(id), content_hash TEXT NOT NULL,
      answer TEXT NOT NULL, note TEXT NOT NULL DEFAULT '', source_pages TEXT NOT NULL DEFAULT '[]',
      checkable INTEGER NOT NULL DEFAULT 0);
    CREATE TABLE IF NOT EXISTS math_relations(
      source_id INTEGER REFERENCES questions(id), target_id INTEGER REFERENCES questions(id),
      skill TEXT NOT NULL, reason TEXT NOT NULL, stage TEXT NOT NULL DEFAULT '同法练习',
      source_hash TEXT NOT NULL, target_hash TEXT NOT NULL,
      PRIMARY KEY(source_id,target_id));
    CREATE TABLE IF NOT EXISTS exam_explanations(
      question_id INTEGER PRIMARY KEY REFERENCES questions(id), content_hash TEXT NOT NULL,
      solution_markdown TEXT NOT NULL, solution_source TEXT NOT NULL,
      answer_checkable INTEGER NOT NULL DEFAULT 1);
    ''')
    if 'answer_checkable' not in {r[1] for r in conn.execute('PRAGMA table_info(exam_explanations)')}:
        conn.execute('ALTER TABLE exam_explanations ADD COLUMN answer_checkable INTEGER NOT NULL DEFAULT 1')


class OpenSession(BaseModel):
    scope: str = Field(min_length=1, max_length=240)
    title: str = Field(min_length=1, max_length=160)
    question_ids: list[int] = Field(min_length=1, max_length=2000)
    origin_id: int | None = None


def item(conn, sid, qid):
    row = conn.execute('SELECT * FROM study_items WHERE session_id=? AND question_id=?', (sid, qid)).fetchone()
    if row is None:
        raise HTTPException(404, '这次练习中没有这道题')
    return dict(row)


@router.post('/sessions')
def open_session(body: OpenSession):
    ids = list(dict.fromkeys(body.question_ids))
    with connection() as conn:
        conn.execute('BEGIN IMMEDIATE')
        available = {r[0] for r in conn.execute('SELECT id FROM questions WHERE id IN (' + ','.join('?' for _ in ids) + ')', ids)}
        if set(ids) != available or (body.origin_id and not conn.execute('SELECT 1 FROM questions WHERE id=?', (body.origin_id,)).fetchone()):
            raise HTTPException(404, '题目不存在')
        conn.execute('INSERT OR IGNORE INTO study_sessions(scope,title,origin_id) VALUES(?,?,?)', (body.scope, body.title, body.origin_id))
        session = dict(conn.execute('SELECT * FROM study_sessions WHERE scope=?', (body.scope,)).fetchone())
        if session['origin_id'] != body.origin_id:
            raise HTTPException(409, '练习来源不一致，请刷新')
        conn.executemany('INSERT OR IGNORE INTO study_items(session_id,question_id) VALUES(?,?)', [(session['id'], qid) for qid in ids])
        session['items'] = {str(qid): item(conn, session['id'], qid) for qid in ids}
        return session


class EditItem(BaseModel):
    revision: int = Field(ge=0)
    mutation: str = Field(min_length=16, max_length=80, pattern=r'^[a-zA-Z0-9_-]+$')
    answer: str = Field(default='', max_length=20000)
    work: str = Field(default='', max_length=50000)
    phase: Literal['work', 'review', 'done'] = 'work'
    rating: Literal['', 'correct', 'wrong', 'fuzzy'] = ''
    reason: Literal['', 'idea', 'calculation', 'speed'] = ''


class LegacyChoices(BaseModel):
    choices: dict[str, str]


@router.post('/import-choices')
def import_choices(body: LegacyChoices):
    if len(body.choices) > 3000:
        raise HTTPException(400, '记录数量过多')
    imported, conflicts = [], []
    with connection() as conn:
        conn.execute('BEGIN IMMEDIATE')
        for raw_id, answer in body.choices.items():
            if not raw_id.isascii() or not raw_id.isdigit() or len(raw_id)>12 or answer not in ('A','B','C','D'):
                continue
            q = conn.execute("SELECT * FROM questions WHERE id=? AND paper='math2' AND qtype='choice'", (int(raw_id),)).fetchone()
            if not q or answer not in {o['key'] for o in json.loads(q['options_json'])}:
                continue
            scope = 'exam:' + str(q['year'])
            conn.execute('INSERT OR IGNORE INTO study_sessions(scope,title) VALUES(?,?)', (scope, str(q['year']) + ' 年数学二真题'))
            sid = conn.execute('SELECT id FROM study_sessions WHERE scope=?', (scope,)).fetchone()[0]
            conn.execute('INSERT OR IGNORE INTO study_items(session_id,question_id) VALUES(?,?)', (sid,q['id']))
            current = item(conn,sid,q['id'])
            if current['revision'] == 0:
                conn.execute('UPDATE study_items SET answer=?,revision=1,mutation=?,updated_at=CURRENT_TIMESTAMP WHERE session_id=? AND question_id=?',
                    (answer, 'legacy-choice-import-' + str(q['id']), sid,q['id']))
                imported.append(q['id'])
            elif current['answer'] != answer:
                conflicts.append(q['id'])
    return {'imported': imported, 'conflicts': conflicts}


@router.patch('/sessions/{sid}/items/{qid}')
def edit_item(sid: int, qid: int, body: EditItem):
    with connection() as conn:
        conn.execute('BEGIN IMMEDIATE')
        current = item(conn, sid, qid)
        if body.mutation == current['mutation']:
            return current
        if current['revision'] != body.revision:
            raise HTTPException(409, {'message': '其他页面已经更新此题，两份内容都已保留。', 'current': current})
        if current['phase'] == 'done':
            raise HTTPException(409, {'message': '这次作答已完成，请先点击再做一次。', 'current': current})
        if bool(body.rating) != (body.phase == 'done') or (body.reason and body.rating not in ('wrong', 'fuzzy')):
            raise HTTPException(400, '请先完成核对，再记录本次结果')
        q = conn.execute('SELECT qtype,options_json,answer FROM questions WHERE id=?', (qid,)).fetchone()
        if q['qtype'] == 'choice' and body.answer and body.answer not in {x['key'] for x in json.loads(q['options_json'])}:
            raise HTTPException(400, '请选择本题提供的选项')
        rating = body.rating
        uncertain = conn.execute('SELECT 1 FROM exam_explanations WHERE question_id=? AND answer_checkable=0',(qid,)).fetchone()
        if body.phase == 'done' and not uncertain and q['qtype'] == 'choice' and q['answer'] in ('A','B','C','D') and body.answer != q['answer']:
            rating = 'wrong'
        conn.execute('UPDATE study_items SET answer=?,work=?,phase=?,rating=?,reason=?,revision=revision+1,mutation=?,updated_at=CURRENT_TIMESTAMP WHERE session_id=? AND question_id=?',
                     (body.answer, body.work, body.phase, rating, body.reason, body.mutation, sid, qid))
        saved = item(conn, sid, qid)
        if body.phase == 'done':
            snapshot = {**saved, 'reference_answer': q['answer'], 'reference_checkable': not bool(uncertain), 'draft_images': [r[0] for r in conn.execute('SELECT id FROM draft_images WHERE question_id=? ORDER BY id', (qid,))]}
            conn.execute('INSERT INTO study_history(session_id,question_id,revision,snapshot) VALUES(?,?,?,?)',
                         (sid, qid, saved['revision'], json.dumps(snapshot, ensure_ascii=False)))
            conn.execute('INSERT INTO attempts(question_id,result,reason) VALUES(?,?,?)', (qid, rating, body.reason if rating == 'wrong' else ''))
        return saved


class Redo(BaseModel):
    revision: int = Field(ge=0)
    mutation: str = Field(min_length=16, max_length=80, pattern=r'^[a-zA-Z0-9_-]+$')


@router.post('/sessions/{sid}/items/{qid}/redo')
def redo(sid: int, qid: int, body: Redo):
    with connection() as conn:
        conn.execute('BEGIN IMMEDIATE')
        current = item(conn, sid, qid)
        if current['mutation'] == body.mutation:
            return current
        if current['revision'] != body.revision or current['phase'] != 'done':
            raise HTTPException(409, {'message': '记录已更新，请刷新后再试。', 'current': current})
        conn.execute("UPDATE study_items SET answer='',work='',phase='work',rating='',reason='',revision=revision+1,mutation=?,updated_at=CURRENT_TIMESTAMP WHERE session_id=? AND question_id=?", (body.mutation, sid, qid))
        return item(conn, sid, qid)


@router.get('/questions/{qid}/history')
def history(qid: int):
    with connection() as conn:
        return [{**dict(r), 'snapshot': json.loads(r['snapshot'])} for r in conn.execute(
            'SELECT h.*,s.title,s.origin_id FROM study_history h JOIN study_sessions s ON s.id=h.session_id WHERE h.question_id=? ORDER BY h.id DESC', (qid,))]


@router.get('/summary')
def summary():
    with connection() as conn:
        return [dict(r) for r in conn.execute('''SELECT s.*,count(i.question_id) total,
          sum(i.answer<>'' OR i.work<>'' OR i.phase<>'work') started,sum(i.phase='done') done,
          max(i.updated_at) updated_at FROM study_sessions s JOIN study_items i ON i.session_id=s.id
          GROUP BY s.id ORDER BY max(i.updated_at) DESC''')]


@router.get('/export')
def export_records():
    from fastapi.responses import JSONResponse
    with connection() as conn:
        data = {table: [dict(r) for r in conn.execute('SELECT * FROM ' + table)]
                for table in ('study_sessions', 'study_items', 'study_history', 'notes', 'draft_images')}
    return JSONResponse({'version': 1, **data}, headers={'Content-Disposition': 'attachment; filename="math-study.json"', 'Cache-Control': 'no-store'})


@router.get('/related')
def related(question_id: int):
    import practice
    import workbook
    with connection() as conn:
        origin = conn.execute("SELECT id,paper,year,number,chapter,point,type_name,stem_html,options_json FROM questions WHERE id=? AND paper='math2'", (question_id,)).fetchone()
        if not origin:
            raise HTTPException(404, '请从真题进入同类补练')
        origin = dict(origin)
        source_hash = question_hash(origin['stem_html'], origin['options_json'])
        origin['options'] = json.loads(origin.pop('options_json'))
        chapters = practice.catalog(conn)
        chapter_key = practice.source_chapter(origin)
        chapter = next((c for c in chapters if c['id'] == chapter_key), chapters[0])
        rows = conn.execute('''SELECT q.id,q.paper,q.year,q.number,q.qtype,q.chapter,q.level,q.stem_html,q.options_json,
          (SELECT count(*) FROM notes WHERE question_id=q.id) note_count,
          (SELECT count(*) FROM draft_images WHERE question_id=q.id) draft_count,
          r.skill,r.reason,r.stage,r.source_hash,r.target_hash,w.content_hash
          FROM math_relations r JOIN questions q ON q.id=r.target_id JOIN workbook_text w ON w.question_id=q.id
          WHERE r.source_id=? ORDER BY (r.stage<>'同法练习'),CASE q.level WHEN '基础' THEN 0 WHEN '综合' THEN 1 ELSE 2 END,q.number''', (question_id,)).fetchall()
        problems = []
        for row in rows:
            p = dict(row)
            if p.pop('source_hash') != source_hash or p.pop('target_hash') != p.pop('content_hash'):
                continue
            p['relation'] = {k:p.pop(k) for k in ('skill','reason','stage')}
            p['options'] = json.loads(p.pop('options_json'))
            problems.append(p)
    return {'origin':origin,'chapter':chapter,'topic':None,'mode':'related','suggested_topics':[],
            'problems':workbook.enrich(problems),'books':[]}
