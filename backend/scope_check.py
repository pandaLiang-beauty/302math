#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""算「数二考纲过滤」能从数一/数三捞回多少题。
规则（数据驱动，不靠人工猜考纲）：以数二真题 431 道实际出现过的三级知识点集合为白名单，
数一/数三的题只要三级点落在白名单内即 in_scope。缺三级点的题退化为按二级章判定。"""
import survey
from collections import Counter

rows = survey.load_all()
m2 = [r for r in rows if r['paper'] == 'math2']


def lv(r, i):
    """取第 i 级标签（0 科目 1 章 2 点）。有的题缺科目层，按已知科目名归一。"""
    t = list(r['tags'])
    if t and t[0] not in ('高等数学', '线性代数', '概率论与数理统计'):
        t = [''] + t          # 补齐缺失的科目层
    return t[i] if len(t) > i and t[i] else ''


white_pt = {lv(r, 2) for r in m2 if lv(r, 2)}
white_ch = {lv(r, 1) for r in m2 if lv(r, 1)}
print('数二白名单：章 %d 个 / 具体点 %d 个' % (len(white_ch), len(white_pt)))

kept, dropped = [], []
for r in rows:
    if r['paper'] == 'math2':
        kept.append(r)
        continue
    pt, ch = lv(r, 2), lv(r, 1)
    ok = (pt in white_pt) if pt else (ch in white_ch)
    (kept if ok else dropped).append(r)

print('\n保留 %d 道（数二 %d + 数一/数三捞回 %d）  剔除 %d 道'
      % (len(kept), len(m2), len(kept) - len(m2), len(dropped)))
print('\n== 保留的按卷种/题型 ==')
c = Counter((r['paper'], r['qtype']) for r in kept)
for k in sorted(c):
    print('  %-7s %-11s %d' % (k[0], k[1], c[k]))
print('\n== 剔除的按章（前 20）==')
for ch, n in Counter(lv(r, 1) or '(无章)' for r in dropped).most_common(20):
    print('  %-26s %d' % (ch, n))
print('\n== 捞回的题里，有解析的比例 ==')
gain = [r for r in kept if r['paper'] != 'math2']
print('  捞回 %d 道，其中有解析 %d，选择题(无解析) %d'
      % (len(gain), sum(1 for r in gain if r['solution_html']),
         sum(1 for r in gain if r['qtype'] == 'choice')))
print('\n== 全库有解析的题（抽解题方法的燃料）==')
print('  %d 道' % sum(1 for r in kept if r['solution_html']))
