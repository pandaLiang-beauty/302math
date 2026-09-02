"""数二·题型体系 后端:API + 托管前端。后端 127.0.0.1:8302。
前后端分离双端口:前端另起 scripts/local_frontend_proxy.py 在 5302(静态 + /api 反代),
对外只暴露 5302;下面 app.mount('/') 那份托管是本机直连后端时的备用入口。
路由:体系树 / 具体点 / 题型(讲解+题簇)/ 单题解析 / 记录作答 / 掌握标记 / 复习推荐 / 统计。
run: python server.py   （或 uvicorn server:app --reload）
"""
import os
import sys
import json
import re
import threading
import time
import urllib.request
import urllib.error
from collections import deque
from contextlib import asynccontextmanager
from typing import Literal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fastapi import FastAPI, HTTPException                # noqa: E402
from fastapi.staticfiles import StaticFiles               # noqa: E402
from pydantic import BaseModel                            # noqa: E402
import db                                                 # noqa: E402
from typedefs import PAPER_CN, QTYPE_CN                   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
FRONTEND = os.path.join(HERE, '..', 'frontend')
SUBJECT_ORDER = ['高等数学', '线性代数', '概率论与数理统计']


def _load_env():
    for name in ('.env.local', '.env'):
        p = os.path.join(HERE, name)
        if os.path.exists(p):
            for line in open(p, encoding='utf-8'):
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k.strip(), v.strip())


_load_env()
LLM_BASE = (os.environ.get('GRADE_BASE_URL') or 'https://vyceai.com/v1').rstrip('/')
LLM_KEY = os.environ.get('GRADE_API_KEY', '')
LLM_MODEL = os.environ.get('GRADE_MODEL') or 'gpt-5.6-luna'
AI_MAX_PER_HOUR = max(1, int(os.environ.get('STUDY_AI_MAX_PER_HOUR', '12')))
_ai_calls = deque()
_ai_lock = threading.Lock()


def q(sql, args=()):
    conn = db.connect()
    try:
        return [dict(r) for r in conn.execute(sql, args).fetchall()]
    finally:
        conn.close()


def one(sql, args=()):
    rs = q(sql, args)
    return rs[0] if rs else None


def write(sql, args=()):
    conn = db.connect()
    try:
        conn.execute(sql, args)
        conn.commit()
    finally:
        conn.close()


@asynccontextmanager
async def lifespan(app):
    conn = db.connect()
    db.init_db(conn)
    conn.close()
    yield


app = FastAPI(title='math-题型体系', lifespan=lifespan)


@app.exception_handler(HTTPException)
async def _exc(request, exc):
    from fastapi.responses import JSONResponse
    return JSONResponse({'detail': exc.detail}, status_code=exc.status_code)


@app.get('/api/health')
def health():
    return {'ok': True}


@app.get('/api/tree')
def tree():
    """题型库 = 章 → 题型。「具体点」不再是导航单位,只在拆出多个题型时当分组小标题。"""
    ts = q("""SELECT t.name, t.curated,
        (SELECT COUNT(*) FROM questions q WHERE q.type_name=t.name) n,
        (SELECT COUNT(*) FROM questions q WHERE q.type_name=t.name AND q.paper LIKE 'math%') nreal,
        (SELECT q.subject FROM questions q WHERE q.type_name=t.name AND q.paper LIKE 'math%'
            GROUP BY q.subject ORDER BY COUNT(*) DESC LIMIT 1) qsub,
        (SELECT q.chapter FROM questions q WHERE q.type_name=t.name AND q.paper LIKE 'math%'
            GROUP BY q.chapter ORDER BY COUNT(*) DESC LIMIT 1) qch,
        (SELECT q.point   FROM questions q WHERE q.type_name=t.name AND q.paper LIKE 'math%'
            GROUP BY q.point ORDER BY COUNT(*) DESC LIMIT 1) qpt,
        (SELECT COUNT(*) FROM questions q WHERE q.type_name=t.name
            AND EXISTS(SELECT 1 FROM attempts a WHERE a.question_id=q.id)) done,
        (SELECT COUNT(*) FROM questions q WHERE q.type_name=t.name AND 'wrong'=
            (SELECT result FROM attempts a WHERE a.question_id=q.id ORDER BY a.id DESC LIMIT 1)) wrong,
        (SELECT status FROM type_progress p WHERE p.type_name=t.name) status,
        t.subject tsub, t.chapter tch, t.point tpt
        FROM types t""")
    subs = {}
    for t in ts:
        if not t['n']:
            continue
        subject = t.pop('qsub') or t.pop('tsub') or '(未标科目)'
        chapter = t.pop('qch') or t.pop('tch') or '(未标章)'
        point = t.pop('qpt') or t.pop('tpt') or ''
        for k in ('tsub', 'tch', 'tpt'):
            t.pop(k, None)
        t['status'] = t['status'] or 'learning'
        t['pending'] = db.is_pending_880_type(t['name'])
        subs.setdefault(subject, {}).setdefault(chapter, {}).setdefault(point or chapter, []).append(t)

    def sub_key(s):
        return (SUBJECT_ORDER.index(s) if s in SUBJECT_ORDER else 99, s)

    out = []
    for s in sorted(subs, key=sub_key):
        chapters = []
        for c, gmap in subs[s].items():
            groups = []
            for pt, lst in gmap.items():
                lst.sort(key=lambda x: (-x['curated'], -x['n']))
                groups.append({'point': pt, 'split': len(lst) > 1, 'n': sum(x['n'] for x in lst),
                               'types': lst})
            groups.sort(key=lambda g: -g['n'])
            flat = [t for g in groups for t in g['types']]
            chapters.append({'chapter': c, 'n': sum(g['n'] for g in groups), 'groups': groups,
                             'ntypes': len(flat), 'ncurated': sum(1 for t in flat if t['curated']),
                             'nreal': sum(t['nreal'] for t in flat),
                             'mastered': sum(1 for t in flat if t['status'] == 'mastered')})
        chapters.sort(key=lambda ch: -ch['nreal'])
        out.append({'subject': s, 'n': sum(ch['n'] for ch in chapters),
                    'ntypes': sum(ch['ntypes'] for ch in chapters),
                    'ncurated': sum(ch['ncurated'] for ch in chapters),
                    'chapters': chapters})
    return out


def _progress(name):
    probs = q(
        "SELECT q.id,q.paper,q.year,q.number,q.qtype,q.level,q.stem_html,q.options_json,"
        "(q.solution_html<>'' OR q.answer_html<>'') has_sol,"
        "(SELECT result FROM attempts a WHERE a.question_id=q.id ORDER BY a.id DESC LIMIT 1) last "
        "FROM questions q WHERE q.type_name=? "
        "ORDER BY (q.qtype<>'choice'),(q.qtype<>'blank'),q.year DESC", (name,))
    for p in probs:
        p['options'] = json.loads(p.pop('options_json') or '[]')
        if p['paper'] == 'lilin880':
            p['src'] = '李林880 · ' + p['level']
        else:
            p['src'] = '%s · %d年 · 第%d题' % (PAPER_CN.get(p['paper'], p['paper']), p['year'], p['number'])
        p['qtype_cn'] = QTYPE_CN.get(p['qtype'], p['qtype'])
    done = sum(1 for p in probs if p['last'])
    correct = sum(1 for p in probs if p['last'] == 'correct')
    wrong = sum(1 for p in probs if p['last'] == 'wrong')
    st = one("SELECT status FROM type_progress WHERE type_name=?", (name,))
    return probs, {'status': st['status'] if st else 'learning',
                   'total': len(probs), 'done': done, 'correct': correct, 'wrong': wrong}


@app.get('/api/type')
def get_type(name: str):
    t = one("SELECT name,subject,chapter,point,intuition,example_src,example_qid,example_stem,"
            "example_steps_json,variants_json,figures_json,trigger,steps_json,pitfalls_json,curated "
            "FROM types WHERE name=?", (name,))
    if not t:
        raise HTTPException(404, '题型不存在')
    t['pending'] = db.is_pending_880_type(t['name'])
    t['steps'] = json.loads(t.pop('steps_json'))
    t['pitfalls'] = json.loads(t.pop('pitfalls_json'))
    t['example_steps'] = json.loads(t.pop('example_steps_json'))
    t['variants'] = json.loads(t.pop('variants_json'))
    t['figures'] = json.loads(t.pop('figures_json'))
    probs, prog = _progress(name)
    return {'type': t, 'problems': probs, 'progress': prog}


@app.get('/api/question')
def question(id: int):
    r = one("SELECT id,paper,year,number,qtype,options_json,answer,answer_html,solution_html,source_url "
            "FROM questions WHERE id=?", (id,))
    if not r:
        raise HTTPException(404, '题不存在')
    r['options'] = json.loads(r.pop('options_json') or '[]')
    return r


class Attempt(BaseModel):
    question_id: int
    result: Literal['correct', 'wrong', 'fuzzy']
    reason: Literal['', 'idea', 'calculation', 'speed'] = ''
    elapsed_seconds: int = 0


@app.post('/api/attempt')
def attempt(a: Attempt):
    if not one("SELECT 1 FROM questions WHERE id=?", (a.question_id,)):
        raise HTTPException(404, '题不存在')
    if a.reason and a.result != 'wrong':
        raise HTTPException(400, '错因只能记录在错题上')
    if not 0 <= a.elapsed_seconds <= 24 * 60 * 60:
        raise HTTPException(400, '作答用时非法')
    write("INSERT INTO attempts(question_id,result,reason,elapsed_seconds) VALUES(?,?,?,?)",
          (a.question_id, a.result, a.reason, a.elapsed_seconds))
    return {'ok': True}


class TypeStatus(BaseModel):
    name: str
    status: Literal['learning', 'mastered']


@app.post('/api/type_status')
def type_status(m: TypeStatus):
    if not one("SELECT 1 FROM types WHERE name=?", (m.name,)):
        raise HTTPException(404, '题型不存在')
    if db.is_pending_880_type(m.name):
        raise HTTPException(400, '待归纳题簇不能标记掌握')
    write("INSERT INTO type_progress(type_name,status,updated_at) VALUES(?,?,CURRENT_TIMESTAMP) "
          "ON CONFLICT(type_name) DO UPDATE SET status=excluded.status,updated_at=CURRENT_TIMESTAMP",
          (m.name, m.status))
    return {'ok': True}


@app.get('/api/review')
def review():
    wrong_types = q("""
      WITH latest AS (
        SELECT question_id, result, reason FROM attempts a
        WHERE a.id=(SELECT MAX(id) FROM attempts b WHERE b.question_id=a.question_id))
      SELECT q.type_name name, q.chapter,
             COUNT(*) wrong,
             COALESCE(SUM(latest.reason='idea'),0) idea,
             COALESCE(SUM(latest.reason='calculation'),0) calculation,
             COALESCE(SUM(latest.reason='speed'),0) speed,
             (SELECT COUNT(*) FROM questions qq WHERE qq.type_name=q.type_name) total,
             (SELECT curated FROM types t WHERE t.name=q.type_name) curated
      FROM questions q JOIN latest ON latest.question_id=q.id
      WHERE latest.result='wrong'
        AND q.type_name NOT IN (SELECT type_name FROM type_progress WHERE status='mastered')
      GROUP BY q.type_name ORDER BY wrong DESC""")
    recent = q("""SELECT a.question_id, a.reason, q.type_name, q.paper, q.year, q.number
      FROM attempts a JOIN questions q ON q.id=a.question_id
      WHERE a.result='wrong' ORDER BY a.id DESC LIMIT 20""")
    seen = set()
    uniq = []
    for r in recent:
        if r['question_id'] in seen:
            continue
        seen.add(r['question_id'])
        r['src'] = '%s · %d · 第%d题' % (PAPER_CN.get(r['paper'], r['paper']), r['year'], r['number'])
        uniq.append(r)
    return {'wrong_types': wrong_types, 'recent_wrong': uniq}


@app.get('/api/stats')
def stats():
    latest = ("SELECT question_id,result FROM attempts a "
              "WHERE a.id=(SELECT MAX(id) FROM attempts b WHERE b.question_id=a.question_id)")
    correct = one("SELECT COUNT(*) c FROM (%s) WHERE result='correct'" % latest)['c']
    wrong = one("SELECT COUNT(*) c FROM (%s) WHERE result='wrong'" % latest)['c']
    done = one("SELECT COUNT(DISTINCT question_id) c FROM attempts")['c']
    mastered = one("SELECT COUNT(*) c FROM type_progress WHERE status='mastered'")['c']
    return {'done': done, 'correct': correct, 'wrong': wrong, 'mastered': mastered,
            'questions': one("SELECT COUNT(*) c FROM questions")['c'],
            'types': one("SELECT COUNT(*) c FROM types")['c']}


@app.get('/api/papers')
def papers():
    """套卷入口:数二真题按年份,带完成进度。"""
    return q("""
      WITH latest AS (
        SELECT question_id, result FROM attempts a
        WHERE a.id=(SELECT MAX(id) FROM attempts b WHERE b.question_id=a.question_id))
      SELECT q.year,
             COUNT(*) total,
             COALESCE(SUM(latest.result IS NOT NULL),0) done,
             COALESCE(SUM(latest.result='correct'),0) correct,
             COALESCE(SUM(latest.result='wrong'),0) wrong
      FROM questions q LEFT JOIN latest ON latest.question_id=q.id
      WHERE q.paper='math2'
      GROUP BY q.year ORDER BY q.year DESC""")


@app.get('/api/paper')
def paper(year: int):
    """一份套卷的题目(按题号),每题带最近作答与所属题型(供"卡住→看讲解")。"""
    probs = q("""
      SELECT q.id,q.number,q.qtype,q.type_name,q.point,q.chapter,q.stem_html,
             q.options_json,
             (q.solution_html<>'' OR q.answer_html<>'') has_sol,
             (SELECT curated FROM types t WHERE t.name=q.type_name) type_curated,
             (SELECT result FROM attempts a WHERE a.question_id=q.id ORDER BY a.id DESC LIMIT 1) last
      FROM questions q WHERE q.paper='math2' AND q.year=? ORDER BY q.number""", (year,))
    for p in probs:
        p['options'] = json.loads(p.pop('options_json') or '[]')
        p['qtype_cn'] = QTYPE_CN.get(p['qtype'], p['qtype'])
    return {'year': year, 'problems': probs, 'count': len(probs)}


def _llm(prompt: str) -> str:
    body = json.dumps({'model': LLM_MODEL, 'temperature': 0.3,
                       'messages': [{'role': 'user', 'content': prompt}]}).encode()
    req = urllib.request.Request(LLM_BASE + '/chat/completions', data=body,
                                 headers={'Content-Type': 'application/json',
                                          'Authorization': 'Bearer ' + LLM_KEY,
                                          'Accept': 'application/json',
                                          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            d = json.loads(resp.read())
        return d['choices'][0]['message']['content'].strip()
    except urllib.error.HTTPError as ex:
        raise HTTPException(502, '大模型返回 %d:%s' % (ex.code, ex.read()[:200].decode('utf-8', 'ignore')))
    except Exception as ex:
        raise HTTPException(502, '调用大模型失败:' + str(ex))


class Explain(BaseModel):
    kind: Literal['type', 'question']
    name: str = ''
    question_id: int = 0
    force: bool = False


@app.get('/api/llm_status')
def llm_status():
    return {'configured': bool(LLM_KEY), 'model': LLM_MODEL, 'max_per_hour': AI_MAX_PER_HOUR}


def _reserve_ai_call() -> None:
    """Keep the optional temporary solver bounded even if an authenticated browser loops."""
    now = time.monotonic()
    with _ai_lock:
        while _ai_calls and _ai_calls[0] <= now - 3600:
            _ai_calls.popleft()
        if len(_ai_calls) >= AI_MAX_PER_HOUR:
            raise HTTPException(429, 'AI 临时试算已达到本小时上限，请稍后再试')
        _ai_calls.append(now)


@app.post('/api/explain')
def explain(e: Explain):
    ck = ('T:' + e.name) if e.kind == 'type' else ('Q:%d' % e.question_id)
    if not e.force:
        row = one("SELECT content FROM ai_explain WHERE cache_key=?", (ck,))
        if row:
            return {'content': row['content'], 'cached': True}
    if not LLM_KEY:
        raise HTTPException(400, '未配置大模型 key:请在 backend/.env.local 设置 GRADE_API_KEY 后重启')
    if e.kind == 'type':
        if not one("SELECT 1 FROM types WHERE name=?", (e.name,)):
            raise HTTPException(404, '题型不存在')
        probs = q("SELECT plain FROM questions WHERE type_name=? AND plain<>'' LIMIT 8", (e.name,))
        samples = '\n'.join('- ' + p['plain'][:200] for p in probs)
        prompt = ('你是考研数学(数二)辅导老师。下面是题型「%s」的若干同类题:\n%s\n\n'
                  '请用中文总结这一类题的【通用解题方法】,分三部分:\n'
                  '① 识别信号:什么样的题属于这一类;\n'
                  '② 通用步骤:拿到这类题怎么下手、标准套路(可编号);\n'
                  '③ 常见坑:容易错在哪。\n要具体、能照着做,不要空话套话。' % (e.name, samples))
    else:
        r = one("SELECT plain, solution_html, answer_html FROM questions WHERE id=?", (e.question_id,))
        if not r:
            raise HTTPException(404, '题不存在')
        sol = re.sub('<[^>]+>', '', (r['answer_html'] or '') + ' ' + (r['solution_html'] or '')).strip()
        prompt = ('你是考研数学(数二)辅导老师。请讲解这道题:\n%s\n\n%s'
                  '请给出:解题思路(为什么这样想)、关键步骤、最终答案。中文,简洁清楚。'
                  % (r['plain'], ('可参考的答案/解析:%s\n\n' % sol[:800]) if sol else ''))
    _reserve_ai_call()
    content = _llm(prompt)
    write("INSERT INTO ai_explain(cache_key,content) VALUES(?,?) "
          "ON CONFLICT(cache_key) DO UPDATE SET content=excluded.content,created_at=CURRENT_TIMESTAMP",
          (ck, content))
    return {'content': content, 'cached': False}


app.mount('/', StaticFiles(directory=FRONTEND, html=True), name='frontend')


if __name__ == '__main__':
    import uvicorn
    # 端口口径：前端 5+科目代码、后端 8+科目代码（302 → 5302/8302），子域能直接推出端口。
    # 前端由 scripts/local_frontend_proxy.py 独立起在 5302，Cloudflare Tunnel 只指前端。
    uvicorn.run(app, host='127.0.0.1', port=int(os.environ.get('STUDY_BACKEND_PORT', '8302')))
