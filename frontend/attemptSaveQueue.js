(function exposeAttemptSaveQueue(global) {
  'use strict';

  /**
   * Persist self-assessments in order for each question.
   *
   * Math records an assessment as an append-only attempt, rather than 408's
   * editable answer snapshot.  Rapidly changing one's self-assessment must
   * still arrive in click order; if a request fails, the newest assessment is
   * retained locally and can be retried without asking the learner to redo it.
   */
  function createAttemptSaveQueue({ save, onStateChange, onError, onSuccess } = {}) {
    const pending = new Map();
    const active = new Set();
    const chains = new Map();
    let revision = 0;

    function normalizeQuestionId(questionId) {
      const normalized = Number(questionId);
      return Number.isInteger(normalized) && normalized > 0 ? normalized : 0;
    }

    function notify(questionId) {
      const id = normalizeQuestionId(questionId);
      onStateChange?.({
        questionId: id,
        pending: pending.has(id),
        active: active.has(id),
        pendingCount: pending.size,
        activeCount: active.size,
      });
    }

    function appendDrain(questionId) {
      const previous = chains.get(questionId) || Promise.resolve(true);
      const next = previous.then(() => drain(questionId), () => drain(questionId));
      chains.set(questionId, next);
      void next.finally(() => {
        if (chains.get(questionId) === next) chains.delete(questionId);
        notify(questionId);
      });
      return next;
    }

    async function drain(questionId) {
      while (pending.has(questionId)) {
        const entry = pending.get(questionId);
        pending.delete(questionId);
        active.add(questionId);
        notify(questionId);
        try {
          await save(entry);
          onSuccess?.(entry);
        } catch (error) {
          // A more recent click may already be queued.  Never put this older
          // record back on top of it; only keep it when it remains the latest.
          const newer = pending.get(questionId);
          if (!newer || newer.revision <= entry.revision) pending.set(questionId, entry);
          onError?.(error, entry);
          return false;
        } finally {
          active.delete(questionId);
          notify(questionId);
        }
      }
      return true;
    }

    function enqueue({ questionId, payload }) {
      const id = normalizeQuestionId(questionId);
      if (!id) return Promise.resolve(false);
      pending.set(id, {
        questionId: id,
        payload: { ...payload },
        revision: ++revision,
      });
      notify(id);
      return appendDrain(id);
    }

    function retryQuestion(questionId) {
      const id = normalizeQuestionId(questionId);
      if (!id || !pending.has(id)) return Promise.resolve(!id ? false : true);
      return appendDrain(id);
    }

    async function flushAll() {
      await Promise.all([...chains.values()]);
      if (pending.size) {
        await Promise.all([...pending.keys()].map(retryQuestion));
        await Promise.all([...chains.values()]);
      }
      return pending.size === 0;
    }

    function hasPendingChanges() {
      return pending.size > 0 || active.size > 0 || chains.size > 0;
    }

    return { enqueue, retryQuestion, flushAll, hasPendingChanges };
  }

  const api = { createAttemptSaveQueue };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  global.MathAttemptSaveQueue = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
