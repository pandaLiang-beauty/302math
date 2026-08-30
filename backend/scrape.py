#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""一次性抓取脚本：把 csgraduates 的数学真题年份页存到 data/raw/。
数学一/二/三 × 2008-2026 共 57 页。数一/数三只取数二考纲内的题（在 seed 阶段按标签过滤）。
用法（在 backend/ 下）：python scrape.py"""
import os
import time
import urllib.request

BASE = 'https://www.csgraduates.com/study_methods/math'
RAW_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'raw')
YEARS = range(2008, 2027)
PAPERS = ('math1', 'math2', 'math3')
# 站点对默认 Python-urllib UA 不友好，统一伪装浏览器
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/126.0 Safari/537.36')


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode('utf-8', 'replace')


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    todo = [(p, y) for p in PAPERS for y in YEARS]
    for i, (paper, year) in enumerate(todo, 1):
        out = os.path.join(RAW_DIR, '%s_%d.html' % (paper, year))
        if os.path.exists(out) and os.path.getsize(out) > 50000:
            print('[%2d/%d] skip %s' % (i, len(todo), os.path.basename(out)))
            continue
        url = '%s/%s/%d/' % (BASE, paper, year)
        try:
            html = fetch(url)
        except Exception as e:
            print('[%2d/%d] FAIL %s %s' % (i, len(todo), url, e))
            continue
        with open(out, 'w', encoding='utf-8') as f:
            f.write(html)
        print('[%2d/%d] ok   %s  %d KB' % (i, len(todo), os.path.basename(out), len(html) // 1024))
        time.sleep(0.5)


if __name__ == '__main__':
    main()
