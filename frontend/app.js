'use strict';
const $ = (id) => document.getElementById(id);
const el = (t, c, h) => { const e = document.createElement(t); if (c) e.className = c; if (h != null) e.innerHTML = h; return e; };
const enc = encodeURIComponent;

async function api(path, opts) {
  const r = await fetch('/api' + path, opts);
  if (!r.ok) { let d; try { d = (await r.json()).detail; } catch (e) {} throw new Error(d || ('HTTP ' + r.status)); }
  return r.json();
}
const post = (path, body) => api(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });

const RESULT_CN = { correct: '上次:对', wrong: '上次:错', fuzzy: '上次:模糊' };
const WRONG_REASON_CN = { idea: '想不到', calculation: '算错', speed: '太慢' };
const attemptIndicators = new Map();
const attemptSaveErrors = new Map();

function showAttemptIndicator(questionId, text = '', kind = '', retry = null) {
  const indicator = attemptIndicators.get(Number(questionId));
  if (!indicator) return;
  indicator.textContent = text;
  indicator.className = 'save-state ' + kind;
  indicator.hidden = !text;
  indicator.onclick = retry || null;
  indicator.title = retry ? '点击重试保存' : '';
}

const attemptSaveQueue = window.MathAttemptSaveQueue.createAttemptSaveQueue({
  save: (entry) => post('/attempt', { question_id: entry.questionId, ...entry.payload }),
  onStateChange: ({ questionId, pending, active }) => {
    if (attemptSaveErrors.has(questionId)) return;
    showAttemptIndicator(questionId, pending || active ? '记录保存中…' : '', pending || active ? 'saving' : '');
  },
  onError: (error, entry) => {
    const message = error?.message || '记录保存失败';
    attemptSaveErrors.set(entry.questionId, message);
    showAttemptIndicator(entry.questionId, '记录未保存，点击重试', 'error', () => {
      attemptSaveErrors.delete(entry.questionId);
      showAttemptIndicator(entry.questionId, '正在重试保存…', 'saving');
      void attemptSaveQueue.retryQuestion(entry.questionId);
    });
  },
  onSuccess: (entry) => {
    attemptSaveErrors.delete(entry.questionId);
    void renderStats();
    void renderSidebar();
  },
});

window.addEventListener('beforeunload', (event) => {
  if (!attemptSaveQueue.hasPendingChanges()) return;
  event.preventDefault();
  event.returnValue = '';
});
const KATEX_OPTS = {
  delimiters: [{ left: '$$', right: '$$', display: true }, { left: '\\[', right: '\\]', display: true },
  { left: '\\(', right: '\\)', display: false }, { left: '$', right: '$', display: false }],
  throwOnError: false
};
function renderMath(node) { if (window.renderMathInElement) try { renderMathInElement(node, KATEX_OPTS); } catch (e) {} }
const fmt = (s) => (s || '').replace(/\*\*(.+?)\*\*/g, '<b>$1</b>');
let refreshProgress = () => {};   // 当前视图设置:重算并刷新进度条

// ---------- 侧栏:套卷(扶手) + 已写讲解的题型 ----------
async function renderSidebar() {
  const aside = $('tree'); aside.innerHTML = '';
  aside.appendChild(el('div', 'subj', '数二真题 · 套卷'));
  let papers = [];
  try { papers = await api('/papers'); } catch (e) {}
  papers.forEach(p => {
    const a = el('a', 'yr');
    a.href = '#/paper/' + p.year;
    a.innerHTML = `<span>${p.year} 年</span><span class="cnt">${p.done}/${p.total}${p.wrong ? ' · <b style="color:var(--bad)">错' + p.wrong + '</b>' : ''}</span>`;
    aside.appendChild(a);
  });
  aside.appendChild(el('div', 'hint', '从做一份真题开始。卡住/做错的题,点题下的「这类不会?」进题型:看讲解 + 刷同类。'));

  // 已写讲解的题型:目前只有这些能给到完整体验(直觉+母题图文演算+套路+变式+坑)
  try {
    const tree = await api('/tree');
    const rows = [];
    tree.forEach(s => s.chapters.forEach(c => c.groups.forEach(g => g.types.forEach(t => {
      if (t.curated) rows.push(Object.assign({ chapter: c.chapter }, t));
    }))));
    if (!rows.length) return;
    aside.appendChild(el('div', 'subj', `已写讲解的题型 · ${rows.length}`));
    let lastCh = null;
    rows.forEach(t => {
      if (t.chapter !== lastCh) { aside.appendChild(el('div', 'chlab', t.chapter)); lastCh = t.chapter; }
      const a = el('a', 'pt live' + (t.status === 'mastered' ? ' ok' : ''));
      a.href = '#/type/' + enc(t.name);
      a.innerHTML = `<span>${t.name}</span><span class="cnt">${t.status === 'mastered' ? '✓' : t.n}</span>`;
      aside.appendChild(a);
    });
  } catch (e) {}
}

async function renderStats() {
  try {
    const s = await api('/stats');
    $('stats').innerHTML = `题库 <b>${s.questions}</b> · 已做 <b>${s.done}</b> · 对 <b style="color:var(--ok)">${s.correct}</b> · 错 <b style="color:var(--bad)">${s.wrong}</b> · 掌握题型 <b>${s.mastered}</b>`;
  } catch (e) {}
}

// ---------- 路由 ----------
function setNav(v) { document.querySelectorAll('nav a').forEach(a => a.classList.toggle('active', a.dataset.nav === v)); }
function route() {
  refreshProgress = () => {};
  const h = location.hash || '#/home';
  if (h.startsWith('#/paper/')) { setNav('papers'); return viewPaper(parseInt(h.slice(8), 10)); }
  if (h.startsWith('#/type/')) { setNav('lib'); return viewType(decodeURIComponent(h.slice(7))); }
  if (h.startsWith('#/review')) { setNav('review'); return viewReview(); }
  if (h.startsWith('#/lib')) { setNav('lib'); return viewLib(); }
  setNav('papers'); return viewHome();
}

// ---------- 进度条 ----------
function computePg(problems) {
  return {
    total: problems.length,
    done: problems.filter(p => p.last).length,
    correct: problems.filter(p => p.last === 'correct').length,
    wrong: problems.filter(p => p.last === 'wrong').length,
  };
}
function progressBar(pg, opts = {}) {
  const wrap = el('div', 'prog');
  const cPct = pg.total ? pg.correct / pg.total * 100 : 0;
  const wPct = pg.total ? pg.wrong / pg.total * 100 : 0;
  wrap.appendChild(el('span', null, `已做 <b style="color:var(--ink)">${pg.done}</b>/${pg.total} · 对 ${pg.correct} · 错 ${pg.wrong}`));
  wrap.appendChild(el('div', 'bar', `<i class="c" style="width:${cPct}%"></i><i class="w" style="width:${wPct}%"></i>`));
  if (opts.masterName) {
    const mastered = opts.status === 'mastered';
    const btn = el('button', 'btn' + (mastered ? ' mastered' : ''), mastered ? '✓ 已掌握(点击撤销)' : '标记掌握(够了)');
    btn.onclick = async () => {
      const old = btn.textContent;
      btn.disabled = true; btn.textContent = '保存中…';
      try {
        await post('/type_status', { name: opts.masterName, status: mastered ? 'learning' : 'mastered' });
        await viewType(opts.masterName); await renderStats();
      } catch (e) {
        btn.textContent = '保存失败，重试';
        btn.title = e.message;
      } finally {
        btn.disabled = false;
        if (btn.isConnected && btn.textContent === '保存中…') btn.textContent = old;
      }
    };
    wrap.appendChild(btn);
  }
  return wrap;
}

// ---------- AI 讲解(题型级 / 单题级) ----------
function mdLite(s) {
  return (s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
    .replace(/^#{1,4}\s*(.+)$/gm, '<b>$1</b>');
}
async function explainInto(panel, btn, payload) {
  if (panel.classList.contains('open')) { panel.classList.remove('open'); return; }
  if (!panel.dataset.loaded) {
    const old = btn.textContent; btn.textContent = '🤖 AI 生成中…(约十几秒)'; btn.disabled = true;
    try { const r = await post('/explain', payload); panel.innerHTML = mdLite(r.content); renderMath(panel); panel.dataset.loaded = '1'; }
    catch (e) { panel.innerHTML = '<span style="color:var(--bad)">' + e.message + '</span>'; }
    btn.textContent = old; btn.disabled = false;
  }
  panel.classList.add('open');
}

// ---------- 题目卡(套卷 & 题型 复用) ----------
function problemCard(p, opts = {}) {
  const q = el('div', 'q'); q.dataset.qid = p.id;
  const head = el('div', 'head');
  head.appendChild(el('span', 'src', p.src || ('第 ' + p.number + ' 题')));
  if (p.level) head.appendChild(el('span', 'badge ' + p.level, p.level));
  head.appendChild(el('span', 'badge q', p.qtype_cn));
  const last = el('span', 'badge last ' + (p.last || ''), p.last ? RESULT_CN[p.last] : '');
  if (!p.last) last.style.display = 'none';
  head.appendChild(last);
  q.appendChild(head);
  q.appendChild(el('div', 'stem', p.stem_html));
  if (p.qtype === 'choice' && Array.isArray(p.options) && p.options.length) {
    const choices = el('div', 'choices');
    choices.setAttribute('role', 'radiogroup');
    choices.setAttribute('aria-label', '选择答案');
    const buttons = [];
    p.options.forEach(option => {
      const choice = el('button', 'choice');
      choice.type = 'button';
      choice.setAttribute('role', 'radio');
      choice.setAttribute('aria-checked', 'false');
      choice.innerHTML = `<b class="choice-key">${option.key}</b><span class="choice-text">${option.text}</span>`;
      choice.onclick = () => {
        buttons.forEach(btn => {
          const selected = btn === choice;
          btn.classList.toggle('selected', selected);
          btn.setAttribute('aria-checked', String(selected));
        });
      };
      buttons.push(choice);
      choices.appendChild(choice);
    });
    q.appendChild(choices);
  }

  const acts = el('div', 'acts');
  const saveState = el('span', 'save-state');
  saveState.hidden = true;
  saveState.setAttribute('aria-live', 'polite');
  attemptIndicators.set(Number(p.id), saveState);
  const mark = (result, reason = '') => {
    // Optimistic local state keeps a deliberate re-assessment visible while a
    // slow network write is serialized in the background.
    p.last = result; last.className = 'badge last ' + result; last.textContent = RESULT_CN[result]; last.style.display = '';
    attemptSaveErrors.delete(Number(p.id));
    showAttemptIndicator(p.id, '记录保存中…', 'saving');
    refreshProgress();
    void attemptSaveQueue.enqueue({ questionId: p.id, payload: { result, reason } });
  };
  const b = (txt, r) => { const x = el('button', 'btn', txt); x.onclick = () => mark(r); return x; };
  acts.appendChild(b('✓ 我会了', 'correct'));
  acts.appendChild(b('～ 模糊', 'fuzzy'));
  const wrong = el('button', 'btn', '✗ 不会/错了');
  const reasons = el('div', 'reason-picker');
  reasons.appendChild(el('span', 'reason-label', '主要卡在哪：'));
  [['idea', '想不到 → 看套路'], ['calculation', '算错 → 练计算'], ['speed', '太慢 → 限时刷']].forEach(([reason, label]) => {
    const button = el('button', 'btn reason', label);
    button.onclick = () => mark('wrong', reason);
    reasons.appendChild(button);
  });
  wrong.onclick = () => reasons.classList.toggle('open');
  acts.appendChild(wrong);
  acts.appendChild(el('span', 'sp'));
  if (opts.typeLink && p.type_name) {
    const tl = el('a', 'btn typelink', p.type_curated ? '这类不会?讲解+同类 →' : '刷同类题 →');
    tl.href = '#/type/' + enc(p.type_name);
    acts.appendChild(tl);
  }
  const sol = el('div', 'sol');
  if (p.has_sol) {
    const bSol = el('button', 'btn', '看解析 ▾');
    bSol.onclick = async () => {
      if (sol.classList.contains('open')) { sol.classList.remove('open'); bSol.textContent = '看解析 ▾'; return; }
      if (!sol.dataset.loaded) {
        bSol.textContent = '加载中…';
        try { const f = await api('/question?id=' + p.id); sol.innerHTML = (f.answer_html ? '<p><b>【答案】</b>' + f.answer_html + '</p>' : '') + (f.solution_html || '<i>暂无</i>'); sol.dataset.loaded = '1'; }
        catch (e) { sol.innerHTML = '出错:' + e.message; }
      }
      sol.classList.add('open'); bSol.textContent = '收起解析 ▴';
    };
    acts.appendChild(bSol);
  }
  const ai = el('div', 'sol ai');
  const bAI = el('button', 'btn ai', 'AI 试算(临时)');
  bAI.onclick = () => explainInto(ai, bAI, { kind: 'question', question_id: p.id });
  acts.appendChild(bAI);
  acts.appendChild(reasons);
  acts.appendChild(saveState);
  q.appendChild(acts); q.appendChild(sol); q.appendChild(ai);
  return q;
}

// ---------- 视图:首页(套卷) ----------
async function viewHome() {
  const m = $('main'); m.innerHTML = '';
  m.appendChild(el('h1', 'title', '从一份真题套卷开始'));
  m.appendChild(el('p', 'lead', '别翻大纲——直接做整份数二真题。做错、卡住的题,点题下的「这类不会?」进<b>题型</b>:看讲解(直觉→母题图文演算→套路→变式→坑)+ 把同类题刷透,自己觉得够了就点「标记掌握」。'));
  let papers = []; try { papers = await api('/papers'); } catch (e) {}
  const grid = el('div', 'grid');
  papers.forEach(p => {
    const c = el('a', 'yearcard'); c.href = '#/paper/' + p.year;
    const pct = p.total ? Math.round(p.done / p.total * 100) : 0;
    c.innerHTML = `<div class="y">${p.year}</div><div class="s">${p.done ? ('已做 ' + p.done + '/' + p.total + (p.wrong ? ' · 错 ' + p.wrong : '')) : (p.total + ' 题 · 未开始')}</div><div class="mini"><i style="width:${pct}%"></i></div>`;
    grid.appendChild(c);
  });
  m.appendChild(grid);
}

// ---------- 视图:套卷(做题) ----------
async function viewPaper(year) {
  const m = $('main'); m.innerHTML = '加载中…';
  let d; try { d = await api('/paper?year=' + year); } catch (e) { m.innerHTML = ''; m.appendChild(el('div', 'empty', '出错:' + e.message)); return; }
  m.innerHTML = '';
  m.appendChild(el('div', 'crumb', '套卷 › <b>' + year + ' 年数二真题</b>'));
  m.appendChild(el('h1', 'title', year + ' 年 · 数二真题'));
  m.appendChild(el('p', 'lead', '按题号做,自己判对错(选择题也自评)。做错的题点「这类不会?」进题型看讲解、刷同类;错题也会进「复习推荐」。'));
  let bar = progressBar(computePg(d.problems));
  m.appendChild(bar);
  refreshProgress = () => { const nb = progressBar(computePg(d.problems)); bar.replaceWith(nb); bar = nb; };
  d.problems.forEach(p => m.appendChild(problemCard(p, { typeLink: true })));
  window.scrollTo(0, 0);
}

// ---------- 视图:题型(讲解 + 分层题簇) ----------
async function viewType(name) {
  const m = $('main'); m.innerHTML = '加载中…';
  let d; try { d = await api('/type?name=' + enc(name)); } catch (e) { m.innerHTML = ''; m.appendChild(el('div', 'empty', '出错:' + e.message)); return; }
  m.innerHTML = '';
  const t = d.type;
  m.appendChild(el('div', 'crumb', `题型 › ${t.chapter || ''} › <b>${t.name}</b>`));
  m.appendChild(el('h1', 'title', t.name));
  if (t.curated) {
    const jw = el('div', 'jw');
    // 锚点条:五段一目了然,长页面可跳
    const secs = [['直觉', 'intu'], ['母题演算', 'ex'], ['套路', 'route'], ['变式', 'var'], ['坑', 'pit']];
    const nav = el('div', 'jnav');
    secs.forEach(([lb, id]) => { const a = el('a', null, lb); a.href = 'javascript:void(0)'; a.onclick = () => { const n = $('sec-' + id); if (n) n.scrollIntoView({ behavior: 'smooth', block: 'start' }); }; nav.appendChild(a); });
    jw.appendChild(nav);

    if (t.intuition) { const n = el('div', 'jj intu', '<span class="k">直觉</span>' + fmt(t.intuition)); n.id = 'sec-intu'; jw.appendChild(n); }
    if (t.example_stem) {
      const ex = el('div', 'example'); ex.id = 'sec-ex';
      ex.appendChild(el('div', 'exhead', '母题' + (t.example_src ? ' · ' + t.example_src : '')));
      ex.appendChild(el('div', 'exstem', fmt(t.example_stem)));
      const body = el('div', 'exbody');
      const steps = el('div', 'exsteps');
      t.example_steps.forEach((s, i) => steps.appendChild(el('div', 'exstep', '<i class="sn">' + (i + 1) + '</i>' + fmt(s))));
      body.appendChild(steps);
      if ((t.figures || []).length) {
        const figs = el('div', 'exfigs');
        t.figures.forEach(s => figs.appendChild(el('div', 'figslot', s)));
        body.appendChild(figs);
      }
      ex.appendChild(body);
      jw.appendChild(ex);
    }
    const j = el('div', 'jj'); j.id = 'sec-route';
    if (t.trigger) j.appendChild(el('div', 'row', '<span class="k">识别</span>' + fmt(t.trigger)));
    if (t.steps.length) j.appendChild(el('div', 'row', '<span class="k">套路</span><ol class="route">' + t.steps.map(x => '<li>' + fmt(x) + '</li>').join('') + '</ol>'));
    if (t.trigger || t.steps.length) jw.appendChild(j);
    if (t.variants.length) { const v = el('div', 'jj var'); v.id = 'sec-var'; v.appendChild(el('div', 'row', '<span class="k">变式</span><ul>' + t.variants.map(x => '<li>' + fmt(x) + '</li>').join('') + '</ul>')); jw.appendChild(v); }
    if (t.pitfalls.length) { const p = el('div', 'jj pit'); p.id = 'sec-pit'; p.appendChild(el('div', 'row', '<span class="k">坑</span><ul>' + t.pitfalls.map(x => '<li>' + fmt(x) + '</li>').join('') + '</ul>')); jw.appendChild(p); }
    m.appendChild(jw);
    renderMath(jw);
  } else if (t.pending) {
    m.appendChild(el('div', 'hint', '这是本章尚未逐题归纳的 <b>880 题簇</b>。可以先按基础/综合/拓展练题；它不是一个已经确认“同解法”的题型，因此不能标记掌握。'));
  } else {
    m.appendChild(el('div', 'hint', '这个题型的<b>通用解题方法</b>我还没写(正在按章补)。讲解是固定内容、不是现场生成的——下面可以先刷同类题。'));
  }

  const progressOpts = t.pending ? {} : { masterName: name, status: d.progress.status };
  let bar = progressBar(d.progress, progressOpts);
  m.appendChild(bar);
  refreshProgress = () => { const pg = computePg(d.problems); pg.status = d.progress.status; const nb = progressBar(pg, progressOpts); bar.replaceWith(nb); bar = nb; };

  const tiers = [
    { label: '真题(考过的)', test: p => p.paper !== 'lilin880' },
    { label: '李林880 · 基础', test: p => p.paper === 'lilin880' && p.level === '基础' },
    { label: '李林880 · 综合', test: p => p.paper === 'lilin880' && p.level === '综合' },
    { label: '李林880 · 拓展(变式)', test: p => p.paper === 'lilin880' && p.level === '拓展' },
  ];
  let shown = 0;
  tiers.forEach(tier => {
    const list = d.problems.filter(tier.test);
    if (!list.length) return;
    shown += list.length;
    const done = list.filter(p => p.last).length;
    const head = el('div', 'tierhead');
    head.innerHTML = `<span>${tier.label} · ${list.length} 道</span><span class="cnt">已做 ${done}/${list.length}</span>`;
    m.appendChild(head);
    const box = el('div', 'tierbox');
    const CAP = 3;
    list.forEach((p, i) => {
      const card = problemCard(p, { typeLink: false });
      if (i >= CAP) card.classList.add('folded');
      box.appendChild(card);
    });
    m.appendChild(box);
    if (list.length > CAP) {
      const more = el('button', 'btn more', `展开其余 ${list.length - CAP} 道 ▾`);
      more.onclick = () => {
        const on = box.classList.toggle('open');
        more.textContent = on ? '收起 ▴' : `展开其余 ${list.length - CAP} 道 ▾`;
      };
      m.appendChild(more);
    }
  });
  if (!shown) m.appendChild(el('div', 'empty', '此题型暂无题目。'));
  window.scrollTo(0, 0);
}

// ---------- 视图:复习推荐 ----------
async function viewReview() {
  const m = $('main'); m.innerHTML = '加载中…';
  const d = await api('/review'); m.innerHTML = '';
  m.appendChild(el('h1', 'title', '复习推荐'));
  m.appendChild(el('p', 'lead', '按你"最近一次做错"聚合。优先回到这些题型,把同类题刷到掌握。'));
  if (!d.wrong_types.length) { m.appendChild(el('div', 'empty', '还没有错题记录。去「套卷」做几道,做错的会出现在这里 →')); return; }
  m.appendChild(el('div', 'crumb', '── 建议再刷的题型 ──'));
  d.wrong_types.forEach(t => {
    const r = el('div', 'rec');
    const reasons = [['idea', '想不到：先看套路'], ['calculation', '算错：再练计算'], ['speed', '太慢：限时刷题']]
      .filter(([key]) => t[key]).map(([key, hint]) => `${WRONG_REASON_CN[key]} ${t[key]} · ${hint}`).join('　');
    r.appendChild(el('div', 'g', `<div class="t">${t.name}${t.curated ? ' ★' : ''}</div><div class="s">${t.chapter} · 待订正 <b style="color:var(--bad)">${t.wrong}</b> / 共 ${t.total} 道${reasons ? '<br><span class="reason-summary">' + reasons + '</span>' : ''}</div>`));
    const b = el('a', 'btn primary', '去刷 →'); b.href = '#/type/' + enc(t.name); r.appendChild(b);
    m.appendChild(r);
  });
}

// ---------- 视图:题型库(章 → 题型;具体点只当分组标签) ----------
function typeRow(t) {
  const a = el('a', 'trow' + (t.curated ? ' live' : '') + (t.status === 'mastered' ? ' done' : ''));
  a.href = '#/type/' + enc(t.name);
  const marks = [];
  if (t.status === 'mastered') marks.push('<span class="chip ok">✓ 已掌握</span>');
  if (t.wrong) marks.push(`<span class="chip bad">错 ${t.wrong}</span>`);
  if (t.done && t.status !== 'mastered') marks.push(`<span class="chip">已做 ${t.done}/${t.n}</span>`);
  a.innerHTML = `<span class="tn">${t.curated ? '<i class="dot on"></i>' : '<i class="dot"></i>'}${t.name}</span>`
    + `<span class="tmeta">${marks.join('')}<span class="cnt">${t.n} 道</span>`
    + (t.curated ? '' : '<span class="tag">待归纳</span>') + '</span>';
  return a;
}

async function viewLib() {
  const m = $('main'); m.innerHTML = '加载中…';
  const tree = await api('/tree'); m.innerHTML = '';
  m.appendChild(el('h1', 'title', '题型库'));
  const tt = tree.reduce((a, s) => a + s.ntypes, 0), tc = tree.reduce((a, s) => a + s.ncurated, 0);
  m.appendChild(el('p', 'lead',
    `按<b>解题方法</b>组织,不按知识点——一个题型就是一套能直接套用的打法。共 <b>${tt}</b> 个题型,`
    + `其中 <b style="color:var(--accent)">${tc}</b> 个已写讲解(蓝点)。章内按真题考频排序,越靠前越值得先啃。`));
  tree.forEach(s => {
    m.appendChild(el('div', 'subj big', `${s.subject} · ${s.ntypes} 个题型 · 讲解 ${s.ncurated}`));
    s.chapters.forEach(c => {
      const d = el('details', 'chap libchap');
      if (c.ncurated) d.open = true;
      d.appendChild(el('summary', null,
        `<span>${c.chapter}</span><span class="cnt">${c.ntypes} 型 · ${c.n} 道`
        + (c.ncurated ? ` · <b style="color:var(--accent)">讲解 ${c.ncurated}</b>` : '')
        + (c.mastered ? ` · <b style="color:var(--ok)">掌握 ${c.mastered}</b>` : '') + '</span>'));
      c.groups.forEach(g => {
        if (g.split) d.appendChild(el('div', 'gplabel', `${g.point} — 拆出 ${g.types.length} 个题型`));
        g.types.forEach(t => d.appendChild(typeRow(t)));
      });
      m.appendChild(d);
    });
  });
}
window.addEventListener('hashchange', route);

// ---------- 启动 ----------
(async () => { await renderSidebar(); await renderStats(); route(); })();
