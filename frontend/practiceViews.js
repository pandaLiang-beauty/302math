'use strict';

async function viewChapters() {
  const m = $('main');
  m.textContent = '正在加载880章节…';
  const chapters = await api('/chapters');
  if (!m.isConnected) return;
  m.replaceChildren();
  m.appendChild(textEl('h1', 'title', '章节练习 · 李林880'));
  m.appendChild(textEl('p', 'lead', '选择知识点练习。做真题时，也可以从题目下方直接进入这里，练完回到原题。'));
  let subject = '';
  chapters.forEach((chapter, index) => {
    if (subject !== chapter.subject) {
      subject = chapter.subject;
      m.appendChild(textEl('h2', 'subj big', subject));
    }
    const detail = el('details', 'chapter-card');
    const summary = el('summary');
    summary.appendChild(textEl('span', 'chapter-name', `${index + 1}. ${chapter.name}`));
    summary.appendChild(textEl('span', 'cnt', `已做 ${chapter.done}/${chapter.total} 题`));
    detail.appendChild(summary);
    const content = el('div', 'chapter-content');
    content.appendChild(studyLink('练本章全部880 · ' + chapter.total + '题', flow.practiceHash({ chapter: chapter.id }), 'btn'));
    const topics = el('div', 'topic-list');
    chapter.topics.filter(topic => topic.total).forEach(topic => {
      const link = studyLink('', flow.practiceHash({ topic: topic.id }), 'topic-link');
      link.appendChild(textEl('span', '', topic.name));
      link.appendChild(textEl('span', 'cnt', `${topic.done}/${topic.total}`));
      topics.appendChild(link);
    });
    content.appendChild(topics);
    detail.appendChild(content);
    m.appendChild(detail);
  });
  window.scrollTo(0, 0);
}

async function viewPractice({ questionId, chapter, topic }) {
  const m = $('main');
  m.textContent = '正在加载对应的880练习…';
  const params = new URLSearchParams();
  if (questionId) params.set('question_id', questionId);
  if (chapter) params.set('chapter', chapter);
  if (topic) params.set('topic', topic);
  const data = await api('/practice?' + params.toString());
  if (!m.isConnected) return;
  m.replaceChildren();
  const origin = data.origin;
  m.dataset.chapter = data.chapter.id;
  if (origin) m.dataset.originYear = origin.year;
  const backHash = origin ? flow.paperHash(origin.year, origin.id) : '#/chapters';
  const backLabel = origin ? `返回 ${origin.year} 年第 ${origin.number} 题` : '返回章节列表';
  const context = el('div', 'practice-context');
  context.appendChild(textEl('span', '', origin ? `正在补练：${origin.year} 年数二 · 第 ${origin.number} 题` : '章节练习 · 李林880'));
  context.appendChild(studyLink(backLabel + ' →', backHash, 'btn primary'));
  m.appendChild(context);
  m.appendChild(textEl('div', 'crumb', `${data.chapter.subject} › ${data.chapter.name}`));
  m.appendChild(textEl('h1', 'title', data.topic ? data.topic.name : data.chapter.name));
  m.appendChild(textEl('p', 'lead', `李林880 · ${data.problems.length} 道${data.topic ? '对应习题' : '章节习题'}。按基础、综合、拓展练习，做完可查看原版解析。`));
  if (origin && !data.topic && !data.suggested_topics.length) {
    m.appendChild(textEl('div', 'hint', '这道真题暂未细分到知识点，先展示对应章节；你可以在下方选择要补练的知识点。'));
  }
  if (origin) {
    const original = el('details', 'source-question');
    original.appendChild(textEl('summary', '', `查看 ${origin.year} 年第 ${origin.number} 题`));
    original.appendChild(el('div', 'stem', origin.stem_html));
    (origin.options || []).forEach(option => {
      original.appendChild(el('div', 'source-option', `<b>${option.key}.</b> ${option.text}`));
    });
    m.appendChild(original);
  }
  if (data.suggested_topics.length > 1) {
    const related = el('div', 'related-topics');
    related.appendChild(textEl('span', 'filter-label', '这题还涉及'));
    data.suggested_topics.forEach(item => {
      const link = studyLink(`${item.name} · ${item.total}题`, flow.practiceHash({ questionId: origin.id, topic: item.id }),
        'topic-chip' + (data.topic?.id === item.id ? ' active' : ''));
      if (data.topic?.id === item.id) link.setAttribute('aria-current', 'page');
      related.appendChild(link);
    });
    m.appendChild(related);
  }
  const tools = el('div', 'practice-tools');
  const label = textEl('label', 'topic-select-label', '选择知识点');
  const select = el('select', 'topic-select');
  select.setAttribute('aria-label', '选择880知识点');
  const all = textEl('option', '', `本章全部880 · ${data.chapter.total}题`);
  all.value = '';
  select.appendChild(all);
  data.chapter.topics.forEach(item => {
    const option = textEl('option', '', `${item.name} · ${item.total}题`);
    option.value = item.id;
    option.disabled = !item.total;
    select.appendChild(option);
  });
  select.value = data.topic?.id || '';
  select.onchange = () => { location.hash = flow.practiceHash({ questionId: origin?.id, chapter: data.chapter.id, topic: select.value }); };
  label.appendChild(select);
  tools.appendChild(label);
  const books = el('div', 'book-links');
  data.books.forEach(book => {
    const link = studyLink(book.name + ' ↗', book.url, 'btn book-link');
    link.target = '_blank'; link.rel = 'noopener';
    books.appendChild(link);
  });
  tools.appendChild(books);
  m.appendChild(tools);

  data.problems.forEach(applyLocalAssessment);
  let bar = progressBar(computePg(data.problems));
  m.appendChild(bar);
  const tierCounters = [];
  const tiers = ['基础', '综合', '拓展'];
  tiers.forEach(level => {
    const list = data.problems.filter(problem => problem.level === level);
    if (!list.length) return;
    const section = el('section', 'practice-tier');
    const heading = textEl('h2', 'tierhead', `${level}练习 · ${list.length}题`);
    const counter = textEl('span', 'cnt', `已做 ${list.filter(p => p.last).length}/${list.length}`);
    heading.appendChild(counter);
    tierCounters.push({ list, counter });
    section.appendChild(heading);
    const box = el('div', 'tierbox');
    const cap = 6;
    list.forEach((problem, index) => {
      const card = problemCard(problem, { hideAI: true });
      if (index >= cap) card.classList.add('folded');
      box.appendChild(card);
    });
    section.appendChild(box);
    if (list.length > cap) {
      const more = textEl('button', 'btn more', `展开其余 ${list.length - cap} 道${level}题 ▾`);
      more.onclick = () => {
        const open = box.classList.toggle('open');
        more.textContent = open ? '收起 ▴' : `展开其余 ${list.length - cap} 道${level}题 ▾`;
      };
      section.appendChild(more);
    }
    m.appendChild(section);
  });
  refreshProgress = () => {
    const next = progressBar(computePg(data.problems));
    bar.replaceWith(next); bar = next;
    tierCounters.forEach(({ list, counter }) => { counter.textContent = `已做 ${list.filter(p => p.last).length}/${list.length}`; });
  };
  if (!data.problems.length) {
    m.appendChild(textEl('div', 'empty', '这个知识点的880习题暂未就绪，可以从上方切换到本章其他知识点。'));
  }
  if (origin) m.appendChild(studyLink(backLabel + '，继续套卷 →', backHash, 'btn primary practice-return'));
  renderMath(m);
  window.scrollTo(0, 0);
}
