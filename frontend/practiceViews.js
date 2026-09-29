'use strict';

async function viewChapters() {
  const m = $('main');
  m.textContent = '正在加载880章节…';
  const chapters = await api('/chapters');
  if (!m.isConnected) return;
  m.replaceChildren();
  m.appendChild(textEl('h1', 'title', '章节练习 · 李林880'));
  m.appendChild(textEl('p', 'lead', '按知识点练习880。做真题时，也可以从侧栏进入对应习题，练完返回原题。'));
  let subject = '';
  chapters.forEach((chapter, index) => {
    if (subject !== chapter.subject) {
      subject = chapter.subject;
      m.appendChild(textEl('h2', 'subj big', subject));
    }
    const detail = el('details', 'chapter-card');
    const summary = el('summary');
    summary.appendChild(textEl('span', 'chapter-name', `${index + 1}. ${chapter.name}`));
    summary.appendChild(textEl('span', 'cnt', `${chapter.total} 道习题`));
    detail.appendChild(summary);
    const content = el('div', 'chapter-content');
    content.appendChild(studyLink('练本章全部880 · ' + chapter.total + '题', flow.practiceHash({ chapter: chapter.id }), 'btn'));
    const topics = el('div', 'topic-list');
    chapter.topics.filter(topic => topic.total).forEach(topic => {
      const link = studyLink('', flow.practiceHash({ topic: topic.id }), 'topic-link');
      link.appendChild(textEl('span', '', topic.name));
      link.appendChild(textEl('span', 'cnt', `${topic.total} 题`));
      topics.appendChild(link);
    });
    content.appendChild(topics);
    detail.appendChild(content);
    m.appendChild(detail);
  });
  window.scrollTo(0, 0);
}

async function viewPractice({ questionId, chapter, topic, focusId }) {
  const m = $('main');
  m.textContent = '正在加载对应的880练习…';
  const params = new URLSearchParams();
  if (questionId) params.set('question_id', questionId);
  if (chapter) params.set('chapter', chapter);
  if (topic) params.set('topic', topic);
  const data = await api((questionId&&!chapter&&!topic?'/study/related?':'/practice?') + params.toString());
  if (!m.isConnected) return;
  await openStudy('practice:'+ (data.origin?.id||'chapter')+':'+(data.mode==='related'?'related':data.topic?.id||data.chapter.id),
    data.origin?`${data.origin.year} 年第 ${data.origin.number} 题的补练`:'880 · '+data.chapter.name,data.problems,data.origin?.id||null);
  if (!m.isConnected) return;
  m.replaceChildren();
  m.className = 'paper-sheet practice-sheet';
  const origin = data.origin;
  m.dataset.chapter = data.chapter.id;
  if (origin) m.dataset.originYear = origin.year;
  const backHash = origin ? flow.paperHash(origin.year, origin.id) : '#/chapters';
  const backLabel = origin ? `返回 ${origin.year} 年第 ${origin.number} 题` : '返回章节列表';
  m.appendChild(studyLink('← ' + backLabel, backHash, 'back-link'));
  m.appendChild(textEl('div', 'crumb', `${data.chapter.subject} › ${data.chapter.name}`));
  m.appendChild(textEl('h1', 'title', data.mode==='related'?`${origin.year} 年第 ${origin.number} 题 · 同类补练`:data.topic ? data.topic.name : data.chapter.name));
  m.appendChild(textEl('p', 'lead', data.mode==='related'?`围绕原题的关键解法，先练同法题，再检验变式。共 ${data.problems.length} 道，练完返回原题。`:`李林880 · ${data.problems.length} 道章节习题。答案、演算和复盘分别保存。`));
  if (origin && data.mode!=='related' && !data.topic && !data.suggested_topics.length) {
    m.appendChild(textEl('div', 'hint', '这道真题暂未细分到知识点，先展示对应章节；你可以在侧栏选择要补练的知识点。'));
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
  const tiers = data.mode==='related'?['同法练习','变式检验']:['基础', '综合', '拓展'];
  tiers.forEach(level => {
    const list = data.problems.filter(problem => (data.mode==='related'?problem.relation.stage:problem.level) === level);
    if (!list.length) return;
    const section = el('section', 'practice-tier');
    const heading = textEl('h2', 'tierhead', `${level} · ${list.length}题`);
    section.appendChild(heading);
    const box = el('div', 'tierbox');
    const cap = 6;
    list.forEach((problem, index) => {
      const card = problemCard(problem);
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
  if (!data.problems.length) {
    m.appendChild(textEl('div', 'empty', data.mode==='related'?'这道题暂未找到足够贴近的 880 练习。可以返回原题，或自主选择章节习题。':'这个知识点暂未收录习题。'));
  }
  if (origin) m.appendChild(studyLink(backLabel + '，继续套卷 →', backHash, 'btn primary practice-return'));
  setStudySidebar({ kind: 'practice', data });
  renderMath(m);
  if (focusId) requestAnimationFrame(() => {
    const card = $('question-' + focusId);
    if (!card || !m.isConnected) return;
    card.closest('.tierbox')?.classList.add('open');
    card.classList.add('focus-question'); card.scrollIntoView({ block: 'start' });
  });
  else window.scrollTo(0, 0);
}
