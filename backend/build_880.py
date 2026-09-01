#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""李林880(数二)做题本 → study.db。做题本文本层公式是散的,所以按题号坐标把每道题裁成图片。
- 输入:高数留白 + 线代留白 两个 PDF(同一套 880 题的科目切法)
- 结构:running header 给"章";内容里 基础题/综合题/拓展题 给"难度";一、选择题/… 给题型;(n) 是题
- 裁剪收到该题内容行的实际下边界(去掉留白版的手写空白)
- 图片存 frontend/880/*.png;积分章按关键词归「定积分的应用」题型
用法(在 backend/ 下):python build_880.py
"""
import os
import sys
import re
import glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fitz          # noqa: E402
import db            # noqa: E402
import typedefs as T  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
MATH_DIR = os.path.normpath(os.path.join(HERE, '..'))
IMG_DIR = os.path.join(HERE, '..', 'frontend', '880')

RE_PROB = re.compile(r'^\((\d+)\)')
RE_HDR = re.compile(r'880\s*[·•]\s*\d+\.?\s*(.+)')
DIFF = {'基础题': '基础', '综合题': '综合', '拓展题': '拓展'}
QT = {'选择题': 'choice', '填空题': 'blank', '解答题': 'subjective'}
CONTENT_TOP, CONTENT_BOTTOM = 40.0, 802.0
X_L, X_R = 52.0, 545.0


def find(*keys, exclude=()):
    for f in glob.glob(os.path.join(MATH_DIR, '*.pdf')):
        b = os.path.basename(f)
        if all(k in b for k in keys) and not any(e in b for e in exclude):
            return f


def is_wm(t):
    return '水印' in t or 'nocode' in t or '公众号' in t


def rows_of(page):
    out = []
    for b in page.get_text('dict')['blocks']:
        if b.get('type') != 0:
            continue
        for ln in b['lines']:
            t = ''.join(s['text'] for s in ln['spans']).strip()
            if t:
                out.append((ln['bbox'][1], ln['bbox'][3], ln['bbox'][0], t))  # y0,y1,x0,text
    out.sort()
    return out


def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    for old in glob.glob(os.path.join(IMG_DIR, '*.png')):
        os.remove(old)
    conn = db.connect()
    db.init_db(conn)
    conn.execute("DELETE FROM questions WHERE paper='lilin880'")

    gid = 0
    for path, subject in [(find('留白版', '高数', exclude=('基础',)), '高等数学'),
                          (find('留白版', '线代', exclude=('基础',)), '线性代数')]:
        doc = fitz.open(path)
        difficulty, qtype = '基础', 'choice'
        for pno in range(1, doc.page_count):
            page = doc[pno]
            rows = rows_of(page)
            chapter = ''
            for y0, y1, x, t in rows:
                if y0 < 32:
                    m = RE_HDR.search(t)
                    if m:
                        chapter = m.group(1).strip()
            probs, bounds = [], []
            for y0, y1, x, t in rows:
                if y0 < CONTENT_TOP or y0 > CONTENT_BOTTOM:
                    continue
                if t in DIFF:
                    difficulty = DIFF[t]; bounds.append(y0); continue
                mq = re.search(r'[一二三四五]、\s*(选择题|填空题|解答题)', t)
                if mq:
                    qtype = QT[mq.group(1)]; bounds.append(y0); continue
                if RE_PROB.match(t) and x < 95:
                    probs.append((y0, difficulty, qtype))
            starts = sorted([p[0] for p in probs])
            cuts = sorted(starts + bounds + [CONTENT_BOTTOM])
            for (y, diff, qt) in probs:
                seg_end = min([c for c in cuts if c > y + 3] or [CONTENT_BOTTOM])
                seg = sorted(r for r in rows if r[0] >= y - 2 and r[0] < seg_end and not is_wm(r[3]))
                if not seg:
                    continue
                kept = [seg[0]]                       # 从题首起按行走,遇到大空隙(下一题/留白)就断
                for r in seg[1:]:
                    if r[0] - kept[-1][1] > 40:
                        break
                    kept.append(r)
                bottom = min(max(r[1] for r in kept) + 6, CONTENT_BOTTOM)
                if bottom - y < 14:
                    continue
                txt = ' '.join(r[3] for r in kept)
                gid += 1
                pix = page.get_pixmap(clip=fitz.Rect(X_L, y - 6, X_R, bottom), matrix=fitz.Matrix(2, 2))
                pix.save(os.path.join(IMG_DIR, '%d.png' % gid))
                type_name = T.classify_880(chapter, txt, gid)
                point = ''
                if not type_name:
                    type_name = db.fallback_880_type(chapter)
                    point = '待归纳'
                conn.execute(
                    "INSERT INTO questions(paper,year,number,qtype,subject,chapter,point,type_name,level,"
                    "stem_html,answer,answer_html,solution_html,score,source_url,plain) "
                    "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    ('lilin880', 0, gid, qt, subject, chapter, point, type_name, diff,
                     '<img class="p880" src="/880/%d.png" alt="李林880题">' % gid,
                     '', '', '', 0, '李林880·' + subject, txt))
        doc.close()
    db.sync_880_fallback_types(conn)
    conn.commit()
    n = conn.execute("SELECT COUNT(*) c FROM questions WHERE paper='lilin880'").fetchone()['c']
    print('李林880 抽取完成:%d 道 → %s' % (n, IMG_DIR))
    print('  按难度:', {r['level']: r['c'] for r in conn.execute(
        "SELECT level,COUNT(*) c FROM questions WHERE paper='lilin880' GROUP BY level")})
    print('  已归入方法题型:', conn.execute(
        "SELECT COUNT(*) c FROM questions WHERE paper='lilin880' "
        "AND type_name NOT LIKE ?", (db.PENDING_880_PREFIX + '%' + db.PENDING_880_SUFFIX,)).fetchone()['c'], '道')
    conn.close()


if __name__ == '__main__':
    main()
