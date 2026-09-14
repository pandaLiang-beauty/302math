(function exposeNoteDrafts(global) {
  'use strict';
  function createStore(storage) {
    const memory = new Map();
    const unsaved = new Set();
    const key = (questionId, noteId) => `math302-note-draft:${questionId}:${noteId || 'new'}`;
    return {
      get(questionId, noteId) {
        const name = key(questionId, noteId);
        if (unsaved.has(name)) return memory.get(name) || null;
        try {
          const data = JSON.parse(storage?.getItem(name) || 'null');
          if (data && typeof data.body === 'string') memory.set(name, data);
          else memory.delete(name);
        } catch { /* Retain drafts in memory if storage is unavailable. */ }
        return memory.get(name) || null;
      },
      set(questionId, noteId, data) {
        const name = key(questionId, noteId);
        memory.set(name, { ...data });
        unsaved.add(name);
        try { if (!storage) return false; storage.setItem(name, JSON.stringify(data)); unsaved.delete(name); return true; }
        catch { return false; }
      },
      remove(questionId, noteId, expectedBody) {
        const current = this.get(questionId, noteId);
        if (expectedBody !== undefined && current?.body !== expectedBody) return;
        const name = key(questionId, noteId);
        memory.delete(name);
        unsaved.delete(name);
        try { storage?.removeItem(name); } catch { unsaved.add(name); }
      },
    };
  }
  const api = { createStore };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  global.MathNoteDrafts = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
