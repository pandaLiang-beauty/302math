'use strict';

let studySidebarContext = null;
let studyNavigationPromise = null;
let studySidebarRevision = 0;
let studySidebarCollapsed = false;
try { studySidebarCollapsed = localStorage.getItem('math302-sidebar-collapsed') === '1'; } catch { /* Use the default layout. */ }

function setStudySidebar(context) {
  studySidebarContext = context;
  void renderSidebar();
}

function sidebarSection(title) {
  const section = el('section', 'sidebar-section');
  section.appendChild(textEl('h3', 'sidebar-section-title', title));
  return section;
}

function updateSidebarCollapse() {
  document.querySelector('.layout').classList.toggle('sidebar-collapsed', studySidebarCollapsed);
  const body = $('sidebar-body');
  if (body) body.hidden = studySidebarCollapsed;
  const title = $('sidebar-title');
  if (title) title.hidden = studySidebarCollapsed;
  const button = $('sidebar-toggle');
  if (button) {
    button.textContent = studySidebarCollapsed ? '‹' : '›';
    button.title = studySidebarCollapsed ? '展开学习侧栏' : '收起学习侧栏';
    button.setAttribute('aria-label', button.title);
    button.setAttribute('aria-expanded', String(!studySidebarCollapsed));
  }
}

function renderQuestionPractice() {
  const target = $('sidebar-question-practice');
  if (!target || studySidebarContext?.kind !== 'paper') return;
  const question = studySidebarContext.data.problems.find(p => p.id === studySidebarContext.activeId);
  target.replaceChildren();
  if (!question) return;
  target.appendChild(textEl('h3', 'sidebar-section-title', `第 ${question.number} 题 · 880补练`));
  const topics = question.practice?.topics || [];
  if (topics.length) {
    topics.forEach(topic => {
      const link = studyLink('', flow.practiceHash({ questionId: question.id, topic: topic.id }), 'sidebar-practice-link');
      link.appendChild(textEl('span', '', topic.name));
      link.appendChild(textEl('small', '', `${topic.total} 道习题 →`));
      target.appendChild(link);
    });
  } else {
    target.appendChild(studyLink('进入对应章节练习 →', question.practice
      ? flow.practiceHash({ questionId: question.id }) : '#/chapters', 'sidebar-practice-link'));
  }
}

function setSidebarActive() {
  const current = flow.parseRoute(location.hash);
  const year = current.view === 'paper' ? current.year : $('main').dataset.originYear;
  const chapter = current.view === 'practice' ? ($('main').dataset.chapter || current.chapter) : '';
  $('tree').querySelectorAll('[data-year], [data-chapter]').forEach(link => {
    const active = link.dataset.year ? String(year) === link.dataset.year : chapter === link.dataset.chapter;
    link.classList.toggle('active', active);
    if (active) link.setAttribute('aria-current', 'page'); else link.removeAttribute('aria-current');
  });
  if (studySidebarContext?.kind !== 'paper') return;
  $('tree').querySelectorAll('[data-question-id]').forEach(button => {
    const id = Number(button.dataset.questionId);
    const current = id === studySidebarContext.activeId;
    button.classList.toggle('current', current);
    button.classList.toggle('answered', Boolean(savedChoices.get(id)));
    if (current) button.setAttribute('aria-current', 'true'); else button.removeAttribute('aria-current');
  });
  const selection = $('sidebar-selection');
  if (selection) {
    const choices = studySidebarContext.data.problems.filter(p => p.qtype === 'choice');
    selection.textContent = `选择题已选 ${choices.filter(p => savedChoices.get(p.id)).length} / ${choices.length}`;
  }
  renderQuestionPractice();
}

function renderPaperSidebar(body, papers, context) {
  const chooseYear = textEl('label', 'sidebar-label', '真题套卷');
  const select = el('select', 'sidebar-select');
  select.setAttribute('aria-label', '切换真题年份');
  const orderedPapers = [...flow.focusPapers(papers).filter(paper => paper.available),
    ...papers.filter(paper => !flow.YEARS.includes(paper.year))];
  orderedPapers.forEach(paper => {
    const option = textEl('option', '', `${paper.year} 年数学二`);
    option.value = paper.year;
    select.appendChild(option);
  });
  select.value = context.data.year;
  select.onchange = () => { location.hash = flow.paperHash(select.value); };
  chooseYear.appendChild(select);
  body.appendChild(chooseYear);
  const selection = textEl('p', 'sidebar-selection', '');
  selection.id = 'sidebar-selection';
  body.appendChild(selection);

  [['choice', '一、选择题'], ['blank', '二、填空题'], ['subjective', '三、解答题']].forEach(([kind, title]) => {
    const problems = context.data.problems.filter(p => p.qtype === kind);
    if (!problems.length) return;
    const section = sidebarSection(title);
    const grid = el('div', 'sidebar-question-grid');
    problems.forEach(problem => {
      const button = textEl('button', 'question-jump', problem.number);
      button.type = 'button';
      button.dataset.questionId = problem.id;
      button.setAttribute('aria-label', `定位第${problem.number}题`);
      button.onclick = () => context.locate(problem.id);
      grid.appendChild(button);
    });
    section.appendChild(grid);
    body.appendChild(section);
  });
  const practice = el('section', 'sidebar-section sidebar-current-practice');
  practice.id = 'sidebar-question-practice';
  body.appendChild(practice);
  body.appendChild(studyLink('全部880章节 →', '#/chapters', 'sidebar-footer-link'));
  body.appendChild(studyLink('返回套卷列表 →', '#/home', 'sidebar-footer-link'));
}

function renderPracticeSidebar(body, data) {
  if (data.origin) {
    body.appendChild(studyLink(`返回 ${data.origin.year} 年第 ${data.origin.number} 题 →`,
      flow.paperHash(data.origin.year, data.origin.id), 'btn primary sidebar-return'));
  }
  body.appendChild(textEl('p', 'sidebar-caption', data.chapter.name));
  const label = textEl('label', 'sidebar-label', '选择知识点');
  const select = el('select', 'sidebar-select topic-select');
  select.setAttribute('aria-label', '选择880知识点');
  const all = textEl('option', '', `本章全部 · ${data.chapter.total}题`);
  all.value = '';
  select.appendChild(all);
  data.chapter.topics.forEach(topic => {
    const option = textEl('option', '', `${topic.name} · ${topic.total}题`);
    option.value = topic.id;
    option.disabled = !topic.total;
    select.appendChild(option);
  });
  select.value = data.topic?.id || '';
  select.onchange = () => { location.hash = flow.practiceHash({ questionId: data.origin?.id, chapter: data.chapter.id, topic: select.value }); };
  label.appendChild(select);
  body.appendChild(label);
  if (data.suggested_topics.length > 1) {
    const related = sidebarSection('原题还涉及');
    data.suggested_topics.forEach(topic => {
      const link = studyLink(`${topic.name} · ${topic.total}题`,
        flow.practiceHash({ questionId: data.origin.id, topic: topic.id }),
        'sidebar-topic-link' + (topic.id === data.topic?.id ? ' active' : ''));
      if (topic.id === data.topic?.id) link.setAttribute('aria-current', 'page');
      related.appendChild(link);
    });
    body.appendChild(related);
  }
  if (data.books.length) {
    const books = sidebarSection('原版资料');
    data.books.forEach(book => {
      const link = studyLink(book.name + ' ↗', book.url, 'sidebar-topic-link');
      link.target = '_blank'; link.rel = 'noopener';
      books.appendChild(link);
    });
    body.appendChild(books);
  }
  body.appendChild(studyLink('全部880章节 →', '#/chapters', 'sidebar-footer-link'));
}

async function renderSidebar() {
  const revision = ++studySidebarRevision;
  const aside = $('tree');
  try {
    if (!studyNavigationPromise) studyNavigationPromise = Promise.all([api('/papers'), api('/chapters')]);
    const [papers, chapters] = await studyNavigationPromise;
    if (revision !== studySidebarRevision) return;
    const scrollTop = $('sidebar-body')?.scrollTop || 0;
    aside.replaceChildren();
    const head = el('div', 'study-sidebar-head');
    const title = textEl('strong', '', studySidebarContext?.kind === 'paper' ? '试卷目录' : studySidebarContext?.kind === 'practice' ? '880章节练习' : '学习导航');
    title.id = 'sidebar-title';
    head.appendChild(title);
    const toggle = textEl('button', 'sidebar-toggle', '›');
    toggle.id = 'sidebar-toggle'; toggle.type = 'button';
    toggle.setAttribute('aria-controls', 'sidebar-body');
    toggle.onclick = () => {
      studySidebarCollapsed = !studySidebarCollapsed;
      try { localStorage.setItem('math302-sidebar-collapsed', studySidebarCollapsed ? '1' : '0'); } catch { /* Keep this view usable. */ }
      updateSidebarCollapse();
    };
    head.appendChild(toggle);
    aside.appendChild(head);
    const body = el('div', 'study-sidebar-body');
    body.id = 'sidebar-body';
    aside.appendChild(body);

    if (studySidebarContext?.kind === 'paper') renderPaperSidebar(body, papers, studySidebarContext);
    else if (studySidebarContext?.kind === 'practice') renderPracticeSidebar(body, studySidebarContext.data);
    else {
      const years = sidebarSection('2020—2026 · 数二真题');
      const grid = el('div', 'sidebar-year-grid');
      flow.focusPapers(papers).forEach(paper => {
        const link = paper.available ? studyLink(`${paper.year}`, flow.paperHash(paper.year), 'sidebar-year') : textEl('span', 'sidebar-year unavailable', `${paper.year}`);
        link.dataset.year = paper.year;
        grid.appendChild(link);
      });
      years.appendChild(grid);
      body.appendChild(years);
      const chaptersSection = sidebarSection('章节练习 · 李林880');
      chapters.forEach(chapter => {
        const link = studyLink(chapter.name, flow.practiceHash({ chapter: chapter.id }), 'sidebar-topic-link');
        link.dataset.chapter = chapter.id;
        chaptersSection.appendChild(link);
      });
      body.appendChild(chaptersSection);
    }
    updateSidebarCollapse();
    body.scrollTop = scrollTop;
    setSidebarActive();
  } catch (error) {
    if (revision !== studySidebarRevision) return;
    studyNavigationPromise = null;
    aside.replaceChildren(textEl('p', 'hint', '侧栏加载失败'));
    const retry = textEl('button', 'btn', '重试'); retry.onclick = renderSidebar;
    aside.appendChild(retry);
  }
}
