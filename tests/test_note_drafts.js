const assert = require('node:assert/strict');
const test = require('node:test');
const { createStore } = require('../frontend/noteDrafts.js');

function storage() {
  const data = new Map();
  return { getItem: key => data.get(key) || null, setItem: (key, value) => data.set(key, value), removeItem: key => data.delete(key) };
}

test('question drafts and edits survive reload without mixing questions or notes', () => {
  const disk = storage(), store = createStore(disk);
  store.set(10, null, { body: '真题草稿', client_id: 'exam' });
  store.set(20, null, { body: '880 草稿', client_id: 'book' });
  store.set(10, 3, { body: '修改已有笔记', revision: 2 });
  const reloaded = createStore(disk);
  assert.equal(reloaded.get(10).body, '真题草稿');
  assert.equal(reloaded.get(20).body, '880 草稿');
  assert.equal(reloaded.get(10, 3).revision, 2);
  reloaded.remove(10, 3);
  assert.equal(reloaded.get(10, 3), null);
  assert.equal(reloaded.get(10).body, '真题草稿');
});

test('a delayed save response cannot clear a newer draft', () => {
  const store = createStore(storage());
  store.set(10, null, { body: '正在提交' });
  store.set(10, null, { body: '继续补充' });
  store.remove(10, null, '正在提交');
  assert.equal(store.get(10).body, '继续补充');
  store.remove(10, null, '继续补充');
  assert.equal(store.get(10), null);
});

test('a full local store keeps the latest in-memory draft instead of restoring older text', () => {
  const disk = storage(), store = createStore(disk);
  store.set(10, null, { body: '旧草稿' });
  disk.setItem = () => { throw new Error('Quota exceeded'); };
  assert.equal(store.set(10, null, { body: '最新草稿' }), false);
  assert.equal(store.get(10).body, '最新草稿');
});

test('malformed or disabled browser storage does not prevent note editing', () => {
  for (const disk of [undefined, { getItem: () => '{broken', setItem: () => { throw new Error('blocked'); } }]) {
    const store = createStore(disk);
    assert.equal(store.get(1), null);
    store.set(1, null, { body: '继续编辑' });
    assert.equal(store.get(1).body, '继续编辑');
  }
});
