#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""解析 data/raw/math{1,2,3}_YYYY.html（csgraduates 数学真题）→ 结构化题目 dict。

页面结构（已核实 2008–2026 一致）：
  <h5 id=N>N</h5>            题号，切题边界
  <div class="choice-container" data-answer=B data-tags=A,B,C>   选择题（无解析）
  <div class="answer-container" data-tags=A,B,C>                 填空/解答题
  <div class="solution-detail" style=display:none>
      <strong>【答案】</strong>…<strong>【解析】</strong>…       填空/解答题的答案与解析
  data-tags 是三层知识点：科目,章,具体点（逗号分隔，无引号）
"""
import re

RE_H5 = re.compile(r'<h5 id=(\d+)>')
RE_CHOICE = re.compile(r'<div class="choice-container[^"]*"([^>]*)>')
RE_ANSBOX = re.compile(r'<div class="answer-container[^"]*"([^>]*)>')
RE_SOL = re.compile(r'<div class="solution-detail[^"]*"[^>]*>')
RE_ANSWER = re.compile(r'data-answer=([^\s>]+)')
RE_TAGS = re.compile(r'data-tags=(?:"([^"]*)"|([^\s>]+))')
RE_SCORE = re.compile(r'本题满分\s*([0-9]+)\s*分')
RE_BLANK = re.compile(r'（填空题）|\(填空题\)')


def absolutize(s):
    return re.sub(r'(src|href)=("?)/(?!/)', r'\1=\2https://www.csgraduates.com/', s or '')


def clean(s):
    return absolutize(re.sub(r'\s+', ' ', re.sub(r'^\s*\d*\s*</h5>\s*', '', s or ''))).strip()


def strip_tail_divs(s):
    return re.sub(r'(\s*</div>)+\s*$', '', s).strip()


def parse_options(slice_html):
    options = []
    for m in re.finditer(r'<label class=choice-option[^>]*>(.*?)</label>', slice_html, re.S):
        block = m.group(1)
        mv = re.search(r'value=([A-Z])', block)
        if not mv:
            continue
        mt = re.search(r'<span class=choice-text>(.*)$', block, re.S)
        text = re.sub(r'</span>\s*$', '', mt.group(1).strip()) if mt else ''
        options.append({'key': mv.group(1), 'text': absolutize(text.strip())})
    return options


def parse_tags(attrs):
    m = RE_TAGS.search(attrs or '')
    raw = (m.group(1) or m.group(2) or '') if m else ''
    return [t.strip() for t in raw.split(',') if t.strip()]


def split_solution(sol_html):
    """把 solution-detail 内容拆成 (答案, 解析)。缺任一段时另一段留空。"""
    body = absolutize(re.sub(r'\s+', ' ', sol_html))
    ans, expl = '', ''
    ma = re.search(r'【答案】(.*?)(?=<strong>\s*【解析】|$)', body, re.S)
    if ma:
        ans = ma.group(1)
    me = re.search(r'【解析】(.*)$', body, re.S)
    if me:
        expl = me.group(1)
    if not ma and not me:
        expl = body
    tidy = lambda s: strip_tail_divs(re.sub(r'^\s*</strong>\s*', '', s).strip())
    return tidy(ans), tidy(expl)

def _solution_after(html, seg_start, seg_end):
    """题块内的 solution-detail（display:none 的那个），返回 (答案, 解析)。选择题没有，返回空。"""
    m = RE_SOL.search(html, seg_start, seg_end)
    if not m:
        return '', ''
    return split_solution(html[m.end():seg_end])


def parse_paper(paper, year, html):
    """解析一年一份卷子。返回题目 dict 列表。"""
    h5list = list(RE_H5.finditer(html))
    out = []
    for idx, m in enumerate(h5list):
        number = int(m.group(1))
        start, end = m.end(), (h5list[idx + 1].start() if idx + 1 < len(h5list) else len(html))
        mend = html.find('</main>', start, end)      # 末题会读到页脚/侧栏，截断
        if mend != -1:
            end = mend
        seg = html[start:end]
        base = {'paper': paper, 'year': year, 'number': number,
                'source_url': 'https://www.csgraduates.com/study_methods/math/%s/%d/' % (paper, year)}
        ch = RE_CHOICE.search(seg)
        if ch:
            options = parse_options(seg[ch.end():])
            ma = RE_ANSWER.search(ch.group(1))
            if not ma or len(options) < 2:
                continue
            ans_html, expl = _solution_after(html, start + ch.end(), end)
            base.update({'qtype': 'choice', 'stem_html': clean(seg[:ch.start()]),
                         'options': options, 'answer': ma.group(1).strip(),
                         'answer_html': ans_html, 'solution_html': expl,
                         'tags': parse_tags(ch.group(1)), 'score': 4 if year <= 2022 else 5})
            out.append(base)
            continue
        ab = RE_ANSBOX.search(seg)
        if not ab:
            continue
        stem = clean(seg[:ab.start()])
        if len(stem) < 8:
            continue
        ans_html, expl = _solution_after(html, start + ab.end(), end)
        ms = RE_SCORE.search(stem)
        if RE_BLANK.search(stem[:40]):
            qtype, score = 'blank', 4 if year <= 2022 else 5
        else:
            qtype, score = 'subjective', int(ms.group(1)) if ms else 10
        base.update({'qtype': qtype, 'stem_html': stem, 'options': [], 'answer': '',
                     'answer_html': ans_html, 'solution_html': expl,
                     'tags': parse_tags(ab.group(1)), 'score': score})
        out.append(base)
    return out

