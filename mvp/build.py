#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""生成数二「题型体系」MVP 原型(自包含 index.html,真题真数据)。
- 按 scope_check 的数二白名单过滤真题
- 侧栏:真实的 科目→章→具体点 计数树
- 主体:深挖一个具体点「定积分的应用」→ 关键词拆成题型 → 每题型带讲解 + 同类题簇(题干 + 可展开的文字解析)
用法(在 math/mvp/ 下):python build.py  → 生成 index.html,浏览器打开即可
"""
import os, sys, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'backend'))
import survey  # noqa: E402

rows = survey.load_all()


def lv(r, i):
    """取第 i 级标签(0 科目 1 章 2 具体点),补齐缺失的科目层。同 scope_check。"""
    t = list(r['tags'])
    if t and t[0] not in ('高等数学', '线性代数', '概率论与数理统计'):
        t = [''] + t
    return t[i] if len(t) > i and t[i] else ''


# ---- 数二白名单过滤(数据驱动:以数二真题实际出现的具体点/章为准) ----
m2 = [r for r in rows if r['paper'] == 'math2']
white_pt = {lv(r, 2) for r in m2 if lv(r, 2)}
white_ch = {lv(r, 1) for r in m2 if lv(r, 1)}


def in_scope(r):
    if r['paper'] == 'math2':
        return True
    pt, ch = lv(r, 2), lv(r, 1)
    return (pt in white_pt) if pt else (ch in white_ch)


kept = [r for r in rows if in_scope(r)]

# ---- 侧栏树:科目 → 章 → 具体点(计数) ----
SUBJECT_ORDER = ['高等数学', '线性代数', '概率论与数理统计', '']
tree = {}
for r in kept:
    s, c, p = lv(r, 0) or '(未标科目)', lv(r, 1) or '(未标章)', lv(r, 2) or '(未细分)'
    tree.setdefault(s, {}).setdefault(c, {})
    tree[s][c][p] = tree[s][c].get(p, 0) + 1

tree_json = []
for s in sorted(tree, key=lambda x: (SUBJECT_ORDER.index(x) if x in SUBJECT_ORDER else 99, x)):
    chapters = []
    for c in sorted(tree[s], key=lambda x: -sum(tree[s][x].values())):
        pts = [{'name': p, 'n': n} for p, n in sorted(tree[s][c].items(), key=lambda kv: -kv[1])]
        chapters.append({'name': c, 'n': sum(tree[s][c].values()), 'points': pts})
    tree_json.append({'name': s, 'n': sum(sum(v.values()) for v in tree[s].values()), 'chapters': chapters})

# ---- 深挖:定积分的应用 → 题型 ----
DEMO_POINT = '定积分的应用'
demo_rows = [r for r in kept if lv(r, 2) == DEMO_POINT]


def strip(h):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', h or '')).strip()


def classify(r):
    s = strip(r['stem_html']) + ' ' + strip(r['solution_html']) + ' ' + strip(r['answer_html'])
    if re.search(r'弧长|曲线.{0,4}长', s):
        return '弧长'
    if re.search(r'旋转|体积|绕.{0,3}轴', s):
        return '旋转体体积'
    if re.search(r'面积|所围|围成|图形的?面积', s):
        return '平面图形面积'
    if re.search(r'形心|质心|做功|压力|引力|平均值|物理', s):
        return '物理/其他应用'
    return '其他/综合'


JIANGJIE = {
    '平面图形面积': {
        'trigger': '求两条曲线所围、或曲线与坐标轴围成的图形面积。',
        'steps': ['先画草图,找交点 → 定积分上下限', '竖着切用 ∫(上 − 下) dx;横着切用 ∫(右 − 左) dy', '哪个变量少分段、少绝对值就选哪个方向'],
        'pitfalls': ['谁在上/在下要按区间判,可能中途互换需分段', '交点必须解出来当积分限', '有对称性先用对称性减半'],
    },
    '旋转体体积': {
        'trigger': '平面图形绕 x 轴或 y 轴旋转,求旋转体体积。',
        'steps': ['绕谁转、被积区域在哪先想清', '圆盘/垫圈法:V = π∫(R² − r²) dx', '柱壳法:V = 2π∫ x·f(x) dx(绕 y 轴时常更省)'],
        'pitfalls': ['盘法 vs 壳法选错会算到崩,先判绕轴', '垫圈法别漏内圈 r²', '平方项别掉、积分限对应旋转区间'],
    },
    '弧长': {
        'trigger': "求曲线弧长,或参数/变限积分给出的曲线长度。",
        'steps': ['直角坐标:s = ∫√(1 + y′²) dx', '参数方程:s = ∫√(x′² + y′²) dt', '先定曲线定义域作为积分限'],
        'pitfalls': ['先求定义域(常被忽略)——它就是积分限', '被积函数是偶函数时用对称性 2∫₀ᵃ 减小计算量', '根号里别化错'],
    },
    '物理/其他应用': {
        'trigger': '形心/质心、变力做功、水压力、函数平均值等物理几何应用。',
        'steps': ['用元素法:取微元 → 写出微元贡献 dW/dF/… → 积分', '套对应公式(形心、做功 ∫F dx、压力 ∫ρg·h·dA)'],
        'pitfalls': ['建坐标系与微元方向要一致', '深度/力随位置变化,别当常量'],
    },
    '其他/综合': {
        'trigger': '定积分应用的综合题,常与前几类混合。',
        'steps': ['拆成上面几类的组合', '先识别每一步在求"面积/体积/弧长/物理量"中的哪个'],
        'pitfalls': ['综合题按小问逐个套打法,别想一步到位'],
    },
}
TYPE_ORDER = ['平面图形面积', '旋转体体积', '弧长', '物理/其他应用', '其他/综合']
QTYPE_CN = {'choice': '选择', 'blank': '填空', 'subjective': '解答'}
QTYPE_LEVEL = {'choice': '基础', 'blank': '基础', 'subjective': '综合'}

by_type = {}
for r in demo_rows:
    by_type.setdefault(classify(r), []).append(r)

demo_types = []
for tname in TYPE_ORDER:
    lst = by_type.get(tname, [])
    if not lst:
        continue
    lst.sort(key=lambda r: (r['qtype'] != 'choice', r['qtype'] != 'blank', -r['year']))
    probs = []
    for r in lst:
        sol = (('<p><b>【答案】</b>' + r['answer_html'] + '</p>') if r['answer_html'] else '') + (r['solution_html'] or '')
        probs.append({
            'src': '%s · %d年 · 第%d题' % ({'math1': '数一', 'math2': '数二', 'math3': '数三'}.get(r['paper'], r['paper']), r['year'], r['number']),
            'qtype': QTYPE_CN.get(r['qtype'], r['qtype']),
            'level': QTYPE_LEVEL.get(r['qtype'], '综合'),
            'stem': r['stem_html'],
            'sol': sol or '<i>(此题库中暂无文字解析,后续接李林880 扫描解析)</i>',
        })
    demo_types.append({'name': tname, 'jiangjie': JIANGJIE.get(tname, {}), 'count': len(probs), 'problems': probs})

DATA = {
    'point': DEMO_POINT,
    'total_kept': len(kept),
    'demo_total': len(demo_rows),
    'tree': tree_json,
    'types': demo_types,
}
data_js = json.dumps(DATA, ensure_ascii=False).replace('</', '<\\/')

HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>数二 · 题型体系 MVP</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<style>
:root{--bg:#f6f7f9;--card:#fff;--ink:#1f2328;--sub:#656d76;--line:#e5e8ec;--accent:#2f6feb;--accent-soft:#eaf1ff;--warn:#b25000}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;color:var(--ink);background:var(--bg);line-height:1.6}
header{position:sticky;top:0;z-index:5;background:#fff;border-bottom:1px solid var(--line);padding:12px 20px;display:flex;align-items:baseline;gap:14px}
header h1{font-size:16px;margin:0}
header .meta{font-size:12px;color:var(--sub)}
.layout{display:flex;align-items:flex-start}
aside{width:300px;flex:none;height:calc(100vh - 49px);overflow:auto;border-right:1px solid var(--line);background:#fbfcfd;padding:10px 6px}
main{flex:1;min-width:0;padding:22px 26px;max-width:900px}
.subj{font-size:12px;color:var(--sub);margin:12px 8px 4px;font-weight:600;letter-spacing:.03em}
.chap{margin:2px 4px}
.chap>summary{cursor:pointer;list-style:none;padding:6px 8px;border-radius:7px;font-size:13.5px;display:flex;justify-content:space-between;gap:8px}
.chap>summary:hover{background:#eef1f4}
.chap>summary::-webkit-details-marker{display:none}
.cnt{color:var(--sub);font-size:12px;font-variant-numeric:tabular-nums}
.pt{padding:5px 10px 5px 20px;margin:1px 4px;border-radius:6px;font-size:13px;display:flex;justify-content:space-between;gap:8px;color:var(--sub)}
.pt.live{color:var(--accent);cursor:pointer;font-weight:600}
.pt.live:hover{background:var(--accent-soft)}
.pt .tag{font-size:11px;color:#8a919a}
.hint{font-size:12px;color:var(--sub);background:#fff;border:1px dashed var(--line);border-radius:8px;padding:8px 10px;margin:8px}
.crumb{font-size:12.5px;color:var(--sub);margin-bottom:4px}
h2.point{margin:0 0 2px;font-size:22px}
.lead{color:var(--sub);font-size:13.5px;margin:0 0 18px}
.type{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:0 0 18px;box-shadow:0 1px 2px rgba(16,24,40,.04)}
.type h3{margin:0 0 2px;font-size:17px;display:flex;align-items:center;gap:8px}
.type h3 .n{font-size:12px;color:#fff;background:var(--accent);border-radius:20px;padding:1px 9px;font-weight:600}
.jj{background:#f8fafc;border:1px solid var(--line);border-radius:9px;padding:10px 14px;margin:10px 0 14px;font-size:13.5px}
.jj .row{margin:3px 0}
.jj b{color:var(--ink)}
.jj .k{display:inline-block;min-width:52px;color:var(--accent);font-weight:600}
.jj ul{margin:3px 0 3px 0;padding-left:20px}
.jj.pit .k{color:var(--warn)}
.cluster-h{font-size:12.5px;color:var(--sub);margin:4px 0 8px;font-weight:600}
.q{border-top:1px solid var(--line);padding:12px 0}
.q:first-of-type{border-top:none}
.q .head{display:flex;align-items:center;gap:8px;margin-bottom:6px}
.q .src{font-size:12px;color:var(--sub);font-variant-numeric:tabular-nums}
.badge{font-size:11px;border-radius:5px;padding:1px 7px;font-weight:600}
.badge.基础{background:#e7f6ec;color:#1a7f37}
.badge.综合{background:#fdf1e3;color:#b25000}
.badge.q{background:#eef1f4;color:#57606a}
.stem{font-size:15px}
.stem img,.sol img{max-width:100%}
.toggle{margin-top:8px;font-size:13px;color:var(--accent);background:var(--accent-soft);border:none;border-radius:7px;padding:5px 12px;cursor:pointer;font-weight:600}
.sol{margin-top:10px;padding:12px 14px;background:#fbfcfd;border:1px solid var(--line);border-radius:9px;font-size:14px;display:none}
.sol.open{display:block}
.katex{font-size:1.02em}
.foot{color:var(--sub);font-size:12px;margin-top:24px;border-top:1px solid var(--line);padding-top:12px}
</style>
</head>
<body>
<header>
  <h1>数二 · 题型体系 <span style="color:var(--accent)">MVP</span></h1>
  <span class="meta" id="meta"></span>
</header>
<div class="layout">
  <aside id="tree"></aside>
  <main id="main"></main>
</div>
<script>
const DATA = __DATA__;

function el(t,c,h){const e=document.createElement(t);if(c)e.className=c;if(h!=null)e.innerHTML=h;return e;}

document.getElementById('meta').textContent =
  `数二范围真题 ${DATA.total_kept} 道 · 样板具体点「${DATA.point}」${DATA.demo_total} 道`;

// ---- 侧栏 ----
const aside=document.getElementById('tree');
aside.appendChild(el('div','hint','左侧是真题按【科目→章→具体点】的真实计数。<b>「'+DATA.point+'」</b>是本 MVP 深挖的样板(蓝色可点),其余具体点的题型待我们一起归纳。'));
DATA.tree.forEach(s=>{
  aside.appendChild(el('div','subj',s.name+' · '+s.n));
  s.chapters.forEach(c=>{
    const d=el('details','chap');
    const sm=el('summary',null,`<span>${c.name}</span><span class="cnt">${c.n}</span>`);
    d.appendChild(sm);
    c.points.forEach(p=>{
      const live=p.name===DATA.point;
      const row=el('div','pt'+(live?' live':''),
        `<span>${p.name}${live?' ★':''}</span><span class="${live?'cnt':'tag'}">${p.n}${live?'':' · 待归纳'}</span>`);
      if(live) row.onclick=()=>renderDemo();
      d.appendChild(row);
    });
    aside.appendChild(d);
  });
});

// ---- 主体 ----
function renderDemo(){
  const m=document.getElementById('main');m.innerHTML='';
  m.appendChild(el('div','crumb','高等数学 › 一元函数积分学及其应用 › <b>'+DATA.point+'</b>'));
  m.appendChild(el('h2','point',DATA.point));
  m.appendChild(el('p','lead','做错任意一道 → 系统给这一类的<b>讲解</b> + 把<b>同型 / 变式</b>题尽量找齐,按 基础→综合 递进,刷到你说"够了"为止。下面每个卡片是一个<b>题型</b>。'));
  DATA.types.forEach(t=>{
    const card=el('div','type');
    card.appendChild(el('h3',null,`${t.name} <span class="n">${t.count} 道</span>`));
    const j=t.jiangjie||{};
    const jj=el('div','jj');
    if(j.trigger) jj.appendChild(el('div','row','<span class="k">识别</span> '+j.trigger));
    if(j.steps) jj.appendChild(el('div','row','<span class="k">打法</span><ul>'+j.steps.map(x=>'<li>'+x+'</li>').join('')+'</ul>'));
    card.appendChild(jj);
    if(j.pitfalls){const pit=el('div','jj pit');pit.appendChild(el('div','row','<span class="k">坑</span><ul>'+j.pitfalls.map(x=>'<li>'+x+'</li>').join('')+'</ul>'));card.appendChild(pit);}
    card.appendChild(el('div','cluster-h','── 同类题簇('+t.count+' 道 · 点开看解析)──'));
    t.problems.forEach(p=>{
      const q=el('div','q');
      const head=el('div','head');
      head.appendChild(el('span','src',p.src));
      head.appendChild(el('span','badge '+p.level,p.level));
      head.appendChild(el('span','badge q',p.qtype));
      q.appendChild(head);
      q.appendChild(el('div','stem',p.stem));
      const btn=el('button','toggle','看解析 ▾');
      const sol=el('div','sol',p.sol);
      btn.onclick=()=>{const o=sol.classList.toggle('open');btn.textContent=o?'收起解析 ▴':'看解析 ▾';};
      q.appendChild(btn);q.appendChild(sol);
      card.appendChild(q);
    });
    m.appendChild(card);
  });
  m.appendChild(el('div','foot','供给:真题(带文字解析)+ 李林880(880 题,解析为扫描图)。本 MVP 先用真题展示效果;880 与「变式」题簇、AI 讲解会在下一步接入。'));
  window.scrollTo(0,0);
}
renderDemo();
</script>
</body>
</html>
'''

out = HTML.replace('__DATA__', data_js)
open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(out)
print('生成 index.html  ·  数二保留 %d 道  ·  「%s」%d 道 → %d 个题型' % (
    len(kept), DEMO_POINT, len(demo_rows), len(demo_types)))
for t in demo_types:
    print('   %-12s %d 道' % (t['name'], t['count']))
