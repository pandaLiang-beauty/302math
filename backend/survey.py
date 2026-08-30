#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""一次性探测脚本：解析 data/raw/ 全部卷子，输出题量/题型/解析覆盖率/标签体系。
用来定「数二考纲过滤」的章节白名单。用法：python survey.py > survey.txt"""
import glob
import os
import re
from collections import Counter, defaultdict

import parse

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'raw')


def load_all():
    rows = []
    for path in sorted(glob.glob(os.path.join(RAW, 'math*_*.html'))):
        name = os.path.splitext(os.path.basename(path))[0]
        paper, year = name.rsplit('_', 1)
        html = open(path, 'rb').read().decode('utf-8', 'ignore')
        rows.extend(parse.parse_paper(paper, int(year), html))
    return rows


def main():
    rows = load_all()
    print('总题数 %d' % len(rows))
    print('\n== 按卷种/题型 ==')
    by = Counter((r['paper'], r['qtype']) for r in rows)
    for k in sorted(by):
        print('  %-7s %-11s %d' % (k[0], k[1], by[k]))
    print('\n== 每卷题数（paper x year）==')
    cnt = defaultdict(dict)
    for r in rows:
        cnt[r['year']][r['paper']] = cnt[r['year']].get(r['paper'], 0) + 1
    print('  year  math1 math2 math3')
    for y in sorted(cnt):
        c = cnt[y]
        print('  %d  %5s %5s %5s' % (y, c.get('math1', '-'), c.get('math2', '-'), c.get('math3', '-')))
    print('\n== 数据完整性 ==')
    for qt in ('choice', 'blank', 'subjective'):
        sub = [r for r in rows if r['qtype'] == qt]
        if not sub:
            continue
        print('  %-11s n=%-4d 有答案 %-4d 有解析 %-4d 有标签 %-4d 无标签 %d' % (
            qt, len(sub),
            sum(1 for r in sub if (r['answer'] or r['answer_html'])),
            sum(1 for r in sub if r['solution_html']),
            sum(1 for r in sub if r['tags']),
            sum(1 for r in sub if not r['tags'])))
    print('\n== 一级标签（科目层）==')
    for t, n in Counter(r['tags'][0] for r in rows if r['tags']).most_common():
        print('  %-14s %d' % (t, n))
    print('\n== 二级标签（章）× 卷种 ==  ← 用它定数二考纲过滤')
    ch = defaultdict(Counter)
    for r in rows:
        if len(r['tags']) >= 2:
            ch[r['tags'][1]][r['paper']] += 1
    print('  %-28s %5s %5s %5s' % ('章', 'math1', 'math2', 'math3'))
    for c in sorted(ch, key=lambda x: -sum(ch[x].values())):
        v = ch[c]
        print('  %-28s %5d %5d %5d' % (c, v['math1'], v['math2'], v['math3']))
    print('\n== 三级标签（具体点）共 %d 个 ==' % len({t for r in rows for t in r['tags'][2:]}))
    for t, n in Counter(t for r in rows for t in r['tags'][2:]).most_common(40):
        print('  %-30s %d' % (t, n))


if __name__ == '__main__':
    main()
