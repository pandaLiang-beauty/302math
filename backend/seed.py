#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""解析真题 → study.db(数二范围),分配题型,写入讲解卡。
- 数二白名单过滤(数据驱动,同 scope_check)
- 「定积分的应用」→ 关键词细分 5 个题型(带讲解);其余具体点 → 直通题型(待归纳)
保留用户的 attempts / type_progress,只重灌题库与题型定义。
用法(在 backend/ 下):python seed.py
"""
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import survey            # noqa: E402
import db                # noqa: E402
import typedefs as T     # noqa: E402


def lv(r, i):
    t = list(r['tags'])
    if t and t[0] not in ('高等数学', '线性代数', '概率论与数理统计'):
        t = [''] + t
    return t[i] if len(t) > i and t[i] else ''


def main():
    rows = survey.load_all()
    m2 = [r for r in rows if r['paper'] == 'math2']
    white_pt = {lv(r, 2) for r in m2 if lv(r, 2)}
    white_ch = {lv(r, 1) for r in m2 if lv(r, 1)}

    def scope(r):
        if r['paper'] == 'math2':
            return True
        pt, ch = lv(r, 2), lv(r, 1)
        return (pt in white_pt) if pt else (ch in white_ch)

    kept = [r for r in rows if scope(r)]

    conn = db.connect()
    db.init_db(conn)
    conn.execute("DELETE FROM questions WHERE paper LIKE 'math%'")
    conn.execute('DELETE FROM types')

    types = {}   # name -> info
    dropped = 0
    for r in kept:
        subject = lv(r, 0) or '(未标科目)'
        chapter = lv(r, 1) or '(未标章)'
        point = lv(r, 2) or '(未细分)'
        plain = T._strip(r['stem_html'])
        if T.out_of_scope(chapter, plain):        # 数二不考:级数/概率/三重积分
            dropped += 1
            continue
        tn, point = T.classify_by_point(point, plain, T._strip(r.get('solution_html', '')),
                                        year=r['year'], number=r['number'])
        chapter = T.CANON_CHAPTER.get(point, chapter)
        if not tn:
            tn = point if point != '(未细分)' else chapter + '·未拆分'
        conn.execute(
            'INSERT INTO questions(paper,year,number,qtype,subject,chapter,point,type_name,level,'
            'stem_html,answer,answer_html,solution_html,score,source_url,plain) '
            'VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
            (r['paper'], r['year'], r['number'], r['qtype'], subject, chapter, point, tn,
             T.level_of(r['qtype']), r['stem_html'], r.get('answer', ''), r.get('answer_html', ''),
             r.get('solution_html', ''), r.get('score', 0), r.get('source_url', ''),
             plain))
        types.setdefault(tn, {'subject': subject, 'chapter': chapter,
                              'point': point if point != '(未细分)' else '',
                              'curated': 0, 'trigger': '', 'steps': [], 'pitfalls': []})

    # 讲解已写好、但真题里暂时没有的题型(如只出现在 880 的),也要建表项,否则 880 挂不上
    for tn, jj in T.ALL_JIANGJIE.items():
        types.setdefault(tn, {'subject': jj.get('subject', ''), 'chapter': jj.get('chapter', ''),
                              'point': jj.get('point', ''),
                              'curated': 1, 'trigger': '', 'steps': [], 'pitfalls': []})

    for tn, info in types.items():
        jj = T.ALL_JIANGJIE.get(tn) or {}
        conn.execute(
            'INSERT INTO types(name,subject,chapter,point,intuition,example_src,example_qid,example_stem,'
            'example_steps_json,variants_json,figures_json,trigger,steps_json,pitfalls_json,curated) '
            'VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
            (tn, info['subject'], info['chapter'], info['point'],
             jj.get('intuition', ''), jj.get('example_src', ''), jj.get('example_qid'),
             jj.get('example_stem', ''),
             json.dumps(jj.get('example_steps', []), ensure_ascii=False),
             json.dumps(jj.get('variants', []), ensure_ascii=False),
             json.dumps(jj.get('figures', []), ensure_ascii=False),
             jj.get('trigger', ''),
             json.dumps(jj.get('steps', []), ensure_ascii=False),
             json.dumps(jj.get('pitfalls', []), ensure_ascii=False),
             1 if jj else 0))

    conn.commit()
    nq = conn.execute('SELECT COUNT(*) c FROM questions').fetchone()['c']
    nt = conn.execute('SELECT COUNT(*) c FROM types').fetchone()['c']
    ntc = conn.execute('SELECT COUNT(*) c FROM types WHERE curated=1').fetchone()['c']
    print('题库 %d 题 · 题型 %d 个(带讲解 %d 个) → %s' % (nq, nt, ntc, db.DB_PATH))
    print('  数二越界已剔除:%d 道(级数/概率/三重积分)' % dropped)
    conn.close()


if __name__ == '__main__':
    main()
