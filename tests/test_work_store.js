const {test}=require('node:test');
const assert=require('node:assert/strict');
const {createStore}=require('../frontend/studyStore');
const item={session_id:1,question_id:2,answer:'',work:'',phase:'work',rating:'',reason:'',revision:0,mutation:''};
function storage(){const m=new Map();return {getItem:k=>m.get(k),setItem:(k,v)=>m.set(k,v),removeItem:k=>m.delete(k)};}
test('a slow first save cannot overwrite a later choice',async()=>{
  let finish;const calls=[];
  const store=createStore({storage:storage(),delay:1000,send:async(s,q,p)=>{calls.push(p);if(calls.length===1)await new Promise(r=>finish=r);return {...item,...p,revision:p.revision+1};}});
  const e=store.register(item);store.change(e,{answer:'A'});const saving=store.flush(e);
  store.change(e,{answer:'D'});finish();await saving;
  assert.deepEqual(calls.map(c=>[c.answer,c.revision]),[['A',0],['D',1]]);assert.equal(e.value.answer,'D');assert.equal(e.pending,null);
});
test('unsent text survives a new page and retries with the same mutation',async()=>{
  const local=storage();const first=createStore({storage:local,delay:1000,send:async()=>{throw Error('offline');}});
  const e=first.register(item);first.change(e,{answer:'C',work:'我的推导'});await first.flush(e);const mutation=e.pending.mutation;
  const next=createStore({storage:local,delay:1000,send:async(s,q,p)=>({...item,...p,revision:1})});
  const restored=next.register(item);assert.equal(restored.value.work,'我的推导');assert.equal(restored.pending.mutation,mutation);
  await next.flush(restored);assert.equal(restored.pending,null);
});
test('conflicting device writes require a choice and preserve both versions',async()=>{
  const remote={...item,answer:'B',revision:2};
  const store=createStore({storage:storage(),delay:1000,send:async()=>{const e=Error('conflict');e.current=remote;throw e;}});
  const e=store.register(item);store.change(e,{answer:'D'});await store.flush(e);
  assert.equal(e.value.answer,'D');assert.equal(e.conflict.answer,'B');store.resolve(e,false);
  assert.equal(e.value.answer,'B');assert.equal(e.pending,null);
});
