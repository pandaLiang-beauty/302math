const assert = require('node:assert/strict');
const test = require('node:test');

const { createAttemptSaveQueue } = require('../frontend/attemptSaveQueue.js');

test('serializes rapid re-assessments for one math question', async () => {
  const calls = [];
  let releaseFirst;
  const firstWrite = new Promise((resolve) => { releaseFirst = resolve; });
  const queue = createAttemptSaveQueue({
    save: async (entry) => {
      calls.push(entry.payload.result);
      if (calls.length === 1) await firstWrite;
    },
  });

  void queue.enqueue({ questionId: 8, payload: { result: 'fuzzy' } });
  await Promise.resolve();
  void queue.enqueue({ questionId: 8, payload: { result: 'wrong', reason: 'idea' } });
  releaseFirst();

  assert.equal(await queue.flushAll(), true);
  assert.deepEqual(calls, ['fuzzy', 'wrong']);
  assert.equal(queue.hasPendingChanges(), false);
});

test('keeps a failed assessment for an explicit retry', async () => {
  let calls = 0;
  const errors = [];
  const queue = createAttemptSaveQueue({
    save: async () => {
      calls += 1;
      if (calls === 1) throw new Error('temporary network failure');
    },
    onError: (error) => errors.push(error.message),
  });

  assert.equal(await queue.enqueue({ questionId: 12, payload: { result: 'correct' } }), false);
  assert.equal(queue.hasPendingChanges(), true);
  assert.equal(await queue.retryQuestion(12), true);
  assert.equal(queue.hasPendingChanges(), false);
  assert.equal(calls, 2);
  assert.deepEqual(errors, ['temporary network failure']);
});
