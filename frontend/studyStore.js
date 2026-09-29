(function(global) {
  'use strict';
  const fields = ['answer', 'work', 'phase', 'rating', 'reason'];
  const pick = item => Object.fromEntries(fields.map(key => [key, item[key] || (key === 'phase' ? 'work' : '')]));
  function createStore({storage, send, notify = () => {}, delay = 350}) {
    const entries = new Map();
    const key = item => `${item.session_id}:${item.question_id}`;
    const storageKey = item => 'math302-work-v1:' + key(item);
    const uuid = () => global.crypto?.randomUUID?.() || 'math-' + Date.now() + '-' + Math.random().toString(36).slice(2);
    function persist(e) {
      try {
        if (e.pending) {
          if(!storage)throw Error('本机存储不可用');
          storage.setItem(storageKey(e.value), JSON.stringify(e.pending));
        } else { try{storage?.removeItem(storageKey(e.value));}catch{} }
        e.storageError = '';
      } catch { e.storageError = '浏览器无法保留待同步内容，请保持页面打开直到服务器保存完成。'; }
      notify(e);
    }
    function register(server) {
      const id = key(server);
      const existing = entries.get(id);
      if (existing?.active || existing?.pending) return existing;
      let pending = null;
      try { pending = JSON.parse(storage?.getItem(storageKey(server)) || 'null'); } catch {}
      const valid = pending && Number.isInteger(pending.revision) && pending.revision>=0 && typeof pending.mutation === 'string' && fields.every(k => typeof pending[k] === 'string') && ['work','review','done'].includes(pending.phase) && ['','correct','wrong','fuzzy'].includes(pending.rating) && ['','idea','calculation','speed'].includes(pending.reason);
      if (!valid || server.mutation === pending.mutation) pending = null;
      const e = {value: {...server, ...(pending ? pick(pending) : {})}, pending, active: false, timer: null, error: '', conflict: null, storageError: ''};
      entries.set(id, e);
      if (pending && pending.revision !== server.revision) e.conflict = server;
      persist(e);
      if (pending && !e.conflict) schedule(e);
      return e;
    }
    function schedule(e) { clearTimeout(e.timer); e.timer = setTimeout(() => void flush(e), delay); }
    function change(e, patch) {
      if (e.value.phase === 'done' || e.conflict) return;
      Object.assign(e.value, patch);
      e.pending = {...pick(e.value), revision: e.value.revision, mutation: uuid()};
      e.error = '';
      persist(e); schedule(e);
    }
    async function flush(e) {
      clearTimeout(e.timer);
      if (e.active) return e.running;
      if (!e.pending || e.conflict) return !e.pending;
      e.active = true; notify(e);
      e.running = (async () => {
        while (e.pending && !e.conflict) {
          const sending = {...e.pending};
          try {
            const saved = await send(e.value.session_id, e.value.question_id, sending);
            e.error = '';
            if (e.pending.mutation === sending.mutation) {
              e.pending = null; e.value = saved;
            } else {
              e.pending.revision = saved.revision;
              e.value = {...saved, ...pick(e.pending)};
            }
            persist(e);
          } catch (error) {
            e.error = error.message || '保存失败';
            e.conflict = error.current || null;
            persist(e);
            return false;
          }
        }
        return true;
      })();
      try { return await e.running; }
      finally { e.active = false; notify(e); }
    }
    function resolve(e, useLocal) {
      if (!e.conflict) return;
      const remote = e.conflict;
      if (useLocal && remote.phase === 'done') {
        e.error = '服务器上的本次作答已完成。请先下载本机内容，再使用服务器版本；需要修改时可再做一次。';
        notify(e); return;
      }
      e.conflict = null; e.error = '';
      if (useLocal) {
        e.value = {...remote, ...pick(e.value)};
        e.pending = {...pick(e.value), revision: remote.revision, mutation: uuid()};
      } else { e.value = remote; e.pending = null; }
      persist(e);
      if (useLocal) void flush(e);
    }
    function adopt(server) {
      const e = entries.get(key(server));
      if (e) { e.value = server; e.pending = null; e.conflict = null; e.error = ''; persist(e); return e; }
      return register(server);
    }
    return {register, change, flush, resolve, adopt,
      retry: () => Promise.all([...entries.values()].filter(e => e.pending).map(flush)),
      pending: () => [...entries.values()].some(e => e.pending || e.active),
      entries};
  }
  global.MathWorkStore = {createStore};
  if (typeof module !== 'undefined') module.exports = {createStore};
})(typeof globalThis !== 'undefined' ? globalThis : this);
