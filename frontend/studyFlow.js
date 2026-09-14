(function exposeStudyFlow(global) {
  'use strict';

  const YEARS = Object.freeze([2020, 2021, 2022, 2023, 2024, 2025, 2026]);

  function focusPapers(papers) {
    return YEARS.map(year => {
      const paper = papers.find(item => item.year === year);
      return paper ? { ...paper, available: paper.total > 0 }
        : { year, total: 0, done: 0, correct: 0, wrong: 0, available: false };
    });
  }

  function nextPaper(papers) {
    // A missing year is shown explicitly, rather than silently starting later.
    return focusPapers(papers).find(paper => !paper.available || paper.done < paper.total) || null;
  }

  function positiveInt(value) {
    return /^\d+$/.test(String(value)) && Number.isSafeInteger(Number(value)) && Number(value) > 0
      ? Number(value) : null;
  }

  function paperHash(year, questionId) {
    return '#/paper/' + year + (positiveInt(questionId) ? '?question=' + questionId : '');
  }

  function practiceHash({ questionId, chapter, topic, focusId } = {}) {
    const params = new URLSearchParams();
    if (positiveInt(questionId)) params.set('question_id', questionId);
    if (chapter) params.set('chapter', chapter);
    if (topic) params.set('topic', topic);
    if (positiveInt(focusId)) params.set('focus', focusId);
    return '#/practice' + (params.size ? '?' + params.toString() : '');
  }

  function parseRoute(hash) {
    const [path, query = ''] = (hash || '#/home').split('?');
    const params = new URLSearchParams(query);
    const paper = path.match(/^#\/paper\/(\d+)$/);
    if (paper) return { view: 'paper', year: Number(paper[1]), questionId: positiveInt(params.get('question')) };
    if (path === '#/practice') {
      return { view: 'practice', questionId: positiveInt(params.get('question_id')),
        chapter: params.get('chapter') || '', topic: params.get('topic') || '', focusId: positiveInt(params.get('focus')) };
    }
    if (path === '#/chapters') return { view: 'chapters' };
    if (path === '#/review') return { view: 'review' };
    if (path === '#/notes') return { view: 'notes', query: params.get('query') || '', source: params.get('source') || '' };
    if (path === '#/lib') return { view: 'lib' };
    if (path.startsWith('#/type/')) {
      try { return { view: 'type', name: decodeURIComponent(path.slice(7)), questionId: positiveInt(params.get('question')) }; }
      catch { return { view: 'home' }; }
    }
    return { view: 'home' };
  }

  function createChoiceStore(storage) {
    const key = 'math302-paper-choices-v1';
    let choices = {};
    try {
      const saved = JSON.parse(storage?.getItem(key) || '{}');
      if (saved && typeof saved === 'object' && !Array.isArray(saved)) choices = saved;
    } catch { /* A disabled or full store must not stop a question from working. */ }
    return {
      get: id => typeof choices[id] === 'string' ? choices[id] : '',
      set(id, value) {
        if (!positiveInt(id) || typeof value !== 'string') return;
        choices[id] = value;
        try { storage?.setItem(key, JSON.stringify(choices)); } catch { /* Keep the in-memory selection. */ }
      },
    };
  }

  const api = { YEARS, focusPapers, nextPaper, positiveInt, paperHash, practiceHash, parseRoute, createChoiceStore };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  global.MathStudyFlow = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
