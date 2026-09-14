const assert = require('node:assert/strict');
const test = require('node:test');
const flow = require('../frontend/studyFlow.js');

test('starts with 2020 and moves to the first unfinished requested paper', () => {
  const papers = [2019, 2026, 2021, 2020, 2024, 2022, 2025, 2023, 2027]
    .map(year => ({ year, total: year === 2020 ? 23 : 22, done: 0 }));
  assert.deepEqual(flow.focusPapers(papers).map(p => p.year), [2020, 2021, 2022, 2023, 2024, 2025, 2026]);
  assert.equal(flow.nextPaper(papers).year, 2020);
  papers.find(p => p.year === 2020).done = 23;
  papers.find(p => p.year === 2022).done = 22;
  assert.equal(flow.nextPaper(papers).year, 2021);
  papers.forEach(p => { p.done = p.total; });
  assert.equal(flow.nextPaper(papers), null);
});

test('missing requested papers stay visible and cannot masquerade as completed', () => {
  const papers = [{ year: 2021, total: 22, done: 0 }];
  const next = flow.nextPaper(papers);
  assert.equal(next.year, 2020);
  assert.equal(next.available, false);
  assert.equal(flow.focusPapers(papers).length, 7);
});

test('practice routes preserve origin while changing topic or choosing the whole chapter', () => {
  const first = flow.parseRoute(flow.practiceHash({ questionId: 351, topic: 'double-order' }));
  assert.equal(first.questionId, 351);
  assert.equal(first.topic, 'double-order');
  const chapter = flow.parseRoute(flow.practiceHash({ questionId: first.questionId, chapter: 'double-integrals' }));
  assert.equal(chapter.questionId, first.questionId);
  assert.equal(chapter.topic, '');
  assert.deepEqual(flow.parseRoute(flow.paperHash(2020, first.questionId)), { view: 'paper', year: 2020, questionId: 351 });
  assert.equal(flow.parseRoute('#/practice?question_id=1oops').questionId, null);
  assert.equal(flow.parseRoute('#/type/%E0%A4%A').view, 'home');
});

test('selected options survive navigation and reload without affecting another question', () => {
  const data = new Map();
  const storage = { getItem: key => data.get(key) || null, setItem: (key, value) => data.set(key, value) };
  const store = flow.createChoiceStore(storage);
  store.set(123, 'C');
  store.set(124, 'B');
  assert.equal(flow.createChoiceStore(storage).get(123), 'C');
  assert.equal(store.get(124), 'B');
  store.set(123, 'A');
  assert.equal(flow.createChoiceStore(storage).get(123), 'A');
});

test('blocked or malformed storage does not stop selecting an answer', () => {
  for (const storage of [
    { getItem: () => '{broken', setItem: () => { throw new Error('full'); } },
    { getItem: () => { throw new Error('blocked'); }, setItem: () => { throw new Error('blocked'); } },
  ]) {
    const store = flow.createChoiceStore(storage);
    store.set(7, 'D');
    assert.equal(store.get(7), 'D');
  }
});

test('notebook return links locate a workbook question without confusing it with an exam origin', () => {
  const route = flow.parseRoute(flow.practiceHash({ chapter: 'limits', focusId: 8807 }));
  assert.equal(route.focusId, 8807);
  assert.equal(route.questionId, null);
  assert.equal(route.chapter, 'limits');
  assert.deepEqual(flow.parseRoute('#/notes?query=%E9%AB%98%E4%BA%AE&source=lilin880'), { view: 'notes', query: '高亮', source: 'lilin880' });
});
