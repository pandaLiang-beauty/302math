'use strict';
const $ = (id) => document.getElementById(id);
const el = (t, c, h) => { const e = document.createElement(t); if (c) e.className = c; if (h != null) e.innerHTML = h; return e; };
const enc = encodeURIComponent;
const flow = window.MathStudyFlow;
const textEl = (tag, className, text) => { const node = el(tag, className); node.textContent = text; return node; };
function studyLink(label, href, className = 'btn') {
  const link = textEl('a', className, label); link.href = href; return link;
}
let choiceStorage;
try { choiceStorage = window.localStorage; } catch { /* In-memory selection still works. */ }
const savedChoices = flow.createChoiceStore(choiceStorage);

async function api(path, opts) {
  const r = await fetch('/api' + path, opts);
  if (!r.ok) { let d; try { d = (await r.json()).detail; } catch (e) {} throw new Error(d || ('HTTP ' + r.status)); }
  return r.json();
}
const WRONG_REASON_CN = { idea: '想不到', calculation: '算错', speed: '太慢' };
const KATEX_OPTS = {
  delimiters: [{ left: '$$', right: '$$', display: true }, { left: '\\[', right: '\\]', display: true },
  { left: '\\(', right: '\\)', display: false }, { left: '$', right: '$', display: false }],
  throwOnError: false
};
function renderMath(node) { if (window.renderMathInElement) try { renderMathInElement(node, KATEX_OPTS); } catch (e) {} }
const fmt = (s) => (s || '').replace(/\*\*(.+?)\*\*/g, '<b>$1</b>');

// ---------- 路由 ----------
function setNav(v) { document.querySelectorAll('nav a').forEach(a => a.classList.toggle('active', a.dataset.nav === v)); }
let disposeView = () => {};
async function route() {
  disposeView();
  disposeView = () => {};
  const current = flow.parseRoute(location.hash);
  const m = el('main', 'content-sheet'); m.id = 'main';
  $('main').replaceWith(m);
  m.textContent = '加载中…';
  const nav = ['practice', 'chapters'].includes(current.view) ? 'chapters'
    : ['type', 'lib'].includes(current.view) ? 'lib' : current.view === 'review' ? 'review' : 'papers';
  setNav(nav);
  setStudySidebar(null);
  try {
    if (current.view === 'paper') await viewPaper(current.year, current.questionId);
    else if (current.view === 'practice') await viewPractice(current);
    else if (current.view === 'chapters') await viewChapters();
    else if (current.view === 'type') await viewType(current.name);
    else if (current.view === 'review') await viewReview();
    else if (current.view === 'lib') await viewLib();
    else await viewHome();
  } catch (error) {
    if (!m.isConnected) return;
    m.replaceChildren(textEl('div', 'empty', '加载失败：' + error.message));
    const retry = textEl('button', 'btn', '重试'); retry.onclick = route;
    m.appendChild(retry);
    m.appendChild(studyLink('返回套卷', '#/home'));
  }
  if (m.isConnected) { renderMath(m); setSidebarActive(); }
}

// ---------- 题目卡(套卷 & 题型 复用) ----------
function problemCard(p, opts = {}) {
  const q = el('article', 'q'); q.dataset.qid = p.id;
  q.id = 'question-' + p.id;
  q.tabIndex = -1;
  if (opts.onFocus) {
    q.addEventListener('pointerdown', () => opts.onFocus(p.id));
    q.addEventListener('focusin', () => opts.onFocus(p.id));
  }
  const head = el('div', 'head');
  head.appendChild(textEl('span', 'src', opts.paper ? `第 ${p.number} 题` : p.src || `第 ${p.number} 题`));
  if (!opts.paper && p.level) head.appendChild(textEl('span', 'badge ' + p.level, p.level));
  if (!opts.paper && p.qtype_cn) head.appendChild(textEl('span', 'badge kind', p.qtype_cn));
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
      const selected = savedChoices.get(p.id) === option.key;
      choice.setAttribute('aria-checked', String(selected));
      choice.classList.toggle('selected', selected);
      choice.innerHTML = `<b class="choice-key">${option.key}</b><span class="choice-text">${option.text}</span>`;
      choice.onclick = () => {
        savedChoices.set(p.id, option.key);
        buttons.forEach(btn => {
          const selected = btn === choice;
          btn.classList.toggle('selected', selected);
          btn.setAttribute('aria-checked', String(selected));
        });
        opts.onSelect?.(p.id);
      };
      buttons.push(choice);
      choices.appendChild(choice);
    });
    q.appendChild(choices);
  }
  const acts = el('div', 'acts');
  const sol = el('div', 'sol');
  sol.id = 'solution-' + p.id;
  if (p.has_sol) {
    const bSol = textEl('button', 'text-action', '查看解析');
    bSol.type = 'button';
    bSol.setAttribute('aria-controls', sol.id);
    bSol.setAttribute('aria-expanded', 'false');
    bSol.onclick = async () => {
      if (sol.classList.contains('open')) {
        sol.classList.remove('open'); bSol.textContent = '查看解析';
        bSol.setAttribute('aria-expanded', 'false');
        return;
      }
      if (!sol.dataset.loaded) {
        bSol.textContent = '加载中…';
        bSol.disabled = true;
        try { const f = await api('/question?id=' + p.id); sol.innerHTML = (f.answer_html ? '<p><b>【答案】</b>' + f.answer_html + '</p>' : '') + (f.solution_html || '<i>暂无</i>'); sol.dataset.loaded = '1'; }
        catch (e) { sol.textContent = '加载失败：' + e.message; }
        finally { bSol.disabled = false; }
      }
      sol.classList.add('open'); bSol.textContent = '收起解析';
      bSol.setAttribute('aria-expanded', 'true');
      renderMath(sol);
    };
    acts.appendChild(bSol);
  }
  if (opts.practiceLink) {
    acts.appendChild(studyLink('880 补练 →', p.practice ? flow.practiceHash({ questionId: p.id }) : '#/chapters', 'text-action practice-link'));
  }
  if (p.answer_url) {
    const answer = studyLink('查看原版解析 ↗', p.answer_url, 'text-action book-link');
    answer.target = '_blank'; answer.rel = 'noopener';
    answer.title = '打开本章对应难度的答案，按题型与原书题号查阅';
    acts.appendChild(answer);
  }
  if (acts.children.length) q.appendChild(acts);
  if (p.has_sol) q.appendChild(sol);
  q.querySelectorAll('img').forEach(img => { img.loading = 'lazy'; });
  q.querySelectorAll('img.p880').forEach(img => {
    const zoom = studyLink('', img.src, 'question-image-zoom');
    zoom.target = '_blank'; zoom.rel = 'noopener';
    zoom.setAttribute('aria-label', '放大查看880题图');
    img.replaceWith(zoom);
    zoom.appendChild(img);
    zoom.appendChild(textEl('span', 'image-zoom-hint', '点击题图放大 ↗'));
  });
  return q;
}

// ---------- 视图:首页(套卷) ----------
async function viewHome() {
  const m = $('main');
  const papers = await api('/papers');
  if (!m.isConnected) return;
  m.replaceChildren();
  m.appendChild(textEl('h1', 'title', '2020—2026 · 数二真题套卷'));
  m.appendChild(textEl('p', 'lead', '按年份做套卷。遇到不会的题，进入对应知识点练880，练完返回原题继续。'));
  const first = flow.focusPapers(papers)[0];
  const start = el('div', 'paper-start');
  const intro = el('div');
  intro.appendChild(textEl('div', 'eyebrow', '从第一套开始'));
  intro.appendChild(textEl('h2', '', `${first.year} 年数学二`));
  intro.appendChild(textEl('p', '', first.available ? `${first.total} 道真题 · 选择题选项自动保留` : '这份套卷尚未入库。'));
  start.appendChild(intro);
  if (first.available) start.appendChild(studyLink('打开试卷 →', flow.paperHash(first.year), 'btn primary start-paper'));
  m.appendChild(start);
  const grid = el('div', 'grid priority-papers');
  flow.focusPapers(papers).forEach((paper, index) => grid.appendChild(yearCard(paper, index + 1)));
  m.appendChild(grid);
  const older = papers.filter(paper => !flow.YEARS.includes(paper.year));
  if (older.length) {
    const detail = el('details', 'older-papers');
    detail.appendChild(textEl('summary', '', `其他年份真题 · ${older.length}套`));
    const oldGrid = el('div', 'grid');
    older.forEach(paper => oldGrid.appendChild(yearCard({ ...paper, available: true })));
    detail.appendChild(oldGrid);
    m.appendChild(detail);
  }
  window.scrollTo(0, 0);
}

function yearCard(paper, order) {
  const card = paper.available ? studyLink('', flow.paperHash(paper.year), 'yearcard') : el('div', 'yearcard unavailable');
  if (order) card.appendChild(textEl('div', 'paper-order', `第 ${order} 套`));
  card.appendChild(textEl('div', 'y', paper.year));
  card.appendChild(textEl('div', 's', paper.available ? `${paper.total} 道真题` : '尚未入库'));
  if (paper.available) card.appendChild(textEl('span', 'year-action', '打开试卷 →'));
  return card;
}

// ---------- 视图:套卷(做题) ----------
async function viewPaper(year, focusId = null) {
  const m = $('main');
  const d = await api('/paper?year=' + year);
  if (!m.isConnected) return;
  m.replaceChildren();
  m.className = 'paper-sheet';
  m.appendChild(studyLink('← 真题套卷', '#/home', 'back-link'));
  const heading = el('div', 'paper-heading');
  heading.appendChild(textEl('p', 'paper-kicker', '全国硕士研究生招生考试'));
  heading.appendChild(textEl('h1', '', `${year} 年数学二真题`));
  const groups = [['choice', '一、选择题'], ['blank', '二、填空题'], ['subjective', '三、解答题']];
  heading.appendChild(textEl('p', 'paper-meta', groups.map(([kind, label]) =>
    `${label.slice(2)} ${d.problems.filter(p => p.qtype === kind).length} 题`).join('　·　')));
  m.appendChild(heading);

  const focusedQuestion = d.problems.find(p => p.id === focusId);
  let locatedScrollTop = null;
  const context = {
    kind: 'paper', data: d,
    activeId: focusedQuestion?.id || d.problems[0]?.id,
    locate: id => jumpTo(id),
  };
  const activate = id => {
    if (!m.isConnected) return;
    context.activeId = id;
    m.querySelectorAll('.q').forEach(node => node.classList.toggle('focus-question', Number(node.dataset.qid) === id));
    setSidebarActive();
  };
  const jumpTo = id => {
    const card = $('question-' + id);
    if (!card || !m.contains(card)) return;
    activate(id);
    history.replaceState(null, '', flow.paperHash(year, id));
    card.focus({ preventScroll: true });
    card.scrollIntoView({ block: 'start' });
    // The final questions may not have enough space below to reach the top.
    // Keep an explicit jump selected until the reader scrolls again.
    locatedScrollTop = window.scrollY;
  };
  groups.forEach(([kind, label]) => {
    const questions = d.problems.filter(p => p.qtype === kind);
    if (!questions.length) return;
    const section = el('section', 'paper-section');
    section.appendChild(textEl('h2', 'paper-section-title', label));
    questions.forEach(p => section.appendChild(problemCard(p, {
      paper: true, practiceLink: true, onFocus: activate, onSelect: activate,
    })));
    m.appendChild(section);
  });
  const footer = el('div', 'paper-next');
  footer.appendChild(textEl('span', '', `全卷 ${d.problems.length} 题`));
  if (d.next_year) footer.appendChild(studyLink(`下一套 · ${d.next_year} 年 →`, flow.paperHash(d.next_year), 'btn'));
  else footer.appendChild(studyLink('返回套卷列表 →', '#/home', 'btn'));
  m.appendChild(footer);

  setStudySidebar(context);
  activate(context.activeId);
  const cards = [...m.querySelectorAll('.q')];
  let scrollFrame = 0;
  const followScroll = () => {
    if (scrollFrame) return;
    scrollFrame = requestAnimationFrame(() => {
      scrollFrame = 0;
      if (!m.isConnected) return;
      if (locatedScrollTop === window.scrollY) return;
      locatedScrollTop = null;
      const top = document.querySelector('header').getBoundingClientRect().bottom + 100;
      let current = cards[0];
      for (const card of cards) {
        if (card.getBoundingClientRect().top > top) break;
        current = card;
      }
      const id = Number(current?.dataset.qid);
      if (id && context.activeId !== id) activate(id);
    });
  };
  window.addEventListener('scroll', followScroll, { passive: true });
  disposeView = () => {
    window.removeEventListener('scroll', followScroll);
    cancelAnimationFrame(scrollFrame);
  };
  if (focusedQuestion) requestAnimationFrame(() => { if (m.isConnected) jumpTo(focusId); });
  else window.scrollTo(0, 0);
}

// ---------- 视图:题型(讲解 + 分层题簇) ----------
async function viewType(name) {
  const m = $('main'); m.innerHTML = '加载中…';
  let d; try { d = await api('/type?name=' + enc(name)); } catch (e) { m.innerHTML = ''; m.appendChild(el('div', 'empty', '出错:' + e.message)); return; }
  if (!m.isConnected) return;
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
    m.appendChild(el('div', 'hint', '本章的880习题按基础、综合、拓展分组，可直接练习。'));
  } else {
    m.appendChild(el('div', 'hint', '这个题型的<b>通用解题方法</b>我还没写(正在按章补)。讲解是固定内容、不是现场生成的——下面可以先刷同类题。'));
  }

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
    const head = textEl('h2', 'tierhead', `${tier.label} · ${list.length} 道`);
    m.appendChild(head);
    const box = el('div', 'tierbox');
    const CAP = 3;
    list.forEach((p, i) => {
      const card = problemCard(p);
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

// ---------- 视图:历史错题 ----------
async function viewReview() {
  const m = $('main'); m.innerHTML = '加载中…';
  const d = await api('/review');
  if (!m.isConnected) return;
  m.innerHTML = '';
  m.appendChild(textEl('h1', 'title', '历史错题'));
  m.appendChild(textEl('p', 'lead', '以前标记的错题，可以回到对应题型查看讲解和练习。'));
  if (!d.wrong_types.length) { m.appendChild(textEl('div', 'empty', '暂无历史错题记录。')); return; }
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
  const a = el('a', 'trow' + (t.curated ? ' live' : ''));
  a.href = '#/type/' + enc(t.name);
  a.innerHTML = `<span class="tn">${t.curated ? '<i class="dot on"></i>' : '<i class="dot"></i>'}${t.name}</span>`
    + `<span class="tmeta"><span class="cnt">${t.n} 道</span>`
    + (t.curated ? '' : '<span class="tag">待归纳</span>') + '</span>';
  return a;
}

async function viewLib() {
  const m = $('main'); m.innerHTML = '加载中…';
  const tree = await api('/tree');
  if (!m.isConnected) return;
  m.innerHTML = '';
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
        + (c.ncurated ? ` · <b style="color:var(--accent)">讲解 ${c.ncurated}</b>` : '') + '</span>'));
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
if (window.ResizeObserver) {
  new ResizeObserver(entries => {
    document.documentElement.style.setProperty('--header-height', Math.ceil(entries[0].target.getBoundingClientRect().height) + 'px');
  }).observe(document.querySelector('header'));
}
if (document.readyState === 'loading') window.addEventListener('DOMContentLoaded', route, { once: true });
else void route();
