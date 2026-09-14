'use strict';

let noteStorage;
try { noteStorage = localStorage; } catch { /* Keep this session usable. */ }
const noteDrafts = window.MathNoteDrafts.createStore(noteStorage);
const noteClientId = () => globalThis.crypto?.randomUUID?.() || 'mathnote-' + Date.now() + '-' + Math.random().toString(36).slice(2);

function noteMarkdown(body) { return el('div', 'note-markdown', window.MathMarkdown.render(body)); }
function noteTime(note) { return (note.updated_at || note.created_at || '').replace('T', ' ').slice(0, 16); }
function noteRequest(path, method, body) {
  return api(path, { method, headers: { 'Content-Type': 'application/json' }, ...(body ? { body: JSON.stringify(body) } : {}) });
}
function updateNoteCount(questionId, count) {
  document.querySelectorAll(`[data-note-question="${Number(questionId)}"]`).forEach(button => {
    button.textContent = count ? `笔记 ${count}` : '笔记';
    button.classList.toggle('has-notes', count > 0);
  });
}
function noteQuestionHash(question) {
  if (question.paper === 'math2') return flow.paperHash(question.year, question.id);
  if (question.paper === 'lilin880' && question.practice_chapter) {
    return flow.practiceHash({ chapter: question.practice_chapter, focusId: question.id });
  }
  return '#/type/' + enc(question.type_name) + '?question=' + question.id;
}
function downloadNotes(groups) {
  const source = groups.map(group => `# ${group.question.source}\n\n` + group.notes
    .map(note => `${note.body}\n\n> ${noteTime(note)}`).join('\n\n---\n\n')).join('\n\n---\n\n');
  const url = URL.createObjectURL(new Blob([source], { type: 'text/markdown;charset=utf-8' }));
  const link = document.createElement('a');
  link.href = url; link.download = '数学笔记.md'; link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function createNotePanel(questionId, initial = null, onChange = () => {}) {
  const root = el('section', 'note-panel');
  root.setAttribute('aria-label', '本题笔记');
  const heading = el('div', 'note-panel-heading');
  const title = textEl('strong', '', '本题笔记');
  const refresh = textEl('button', 'text-action', '刷新笔记'); refresh.type = 'button';
  heading.append(title, refresh, studyLink('笔记本 →', '#/notes', 'text-action'));
  const feedback = textEl('p', 'note-feedback', ''); feedback.setAttribute('role', 'status'); feedback.hidden = true;
  const list = el('div', 'note-list');
  const compose = el('div', 'note-compose');
  root.append(heading, feedback, list, compose);
  let documentData = initial, loading = false, saving = false, loadVersion = 0;

  const say = (message, error = false) => {
    feedback.textContent = message; feedback.hidden = !message;
    feedback.classList.toggle('error', error);
    feedback.setAttribute('role', error ? 'alert' : 'status');
  };
  const changed = () => {
    const count = documentData?.notes.length || 0;
    updateNoteCount(questionId, count);
    onChange(documentData);
    title.textContent = `本题笔记 · ${count} 条`;
  };

  function editor(note = null) {
    const stored = noteDrafts.get(questionId, note?.id);
    const draft = stored || { body: note?.body || '', client_id: note?.client_id || noteClientId(), revision: note?.revision };
    const form = el('form', 'note-editor');
    const modes = el('div', 'note-editor-toolbar');
    const buttons = el('div', 'note-editor-modes');
    const edit = textEl('button', '', '编辑'), preview = textEl('button', '', '预览');
    edit.type = preview.type = 'button';
    buttons.append(edit, preview);
    modes.append(buttons, textEl('span', '', 'Markdown · ===高亮=== · $公式$'));
    const input = el('textarea', 'note-input');
    input.rows = 4; input.maxLength = 20000; input.value = draft.body;
    input.setAttribute('aria-label', note ? '编辑笔记' : '新增笔记');
    input.placeholder = '记录思路、易错点或解题步骤… 支持 Markdown 和 LaTeX 公式';
    const rendered = el('div', 'note-editor-preview'); rendered.hidden = true;
    const actions = el('div', 'note-editor-actions');
    const save = textEl('button', 'btn primary', note ? '保存修改' : '保存笔记'); save.type = 'submit';
    const cancel = textEl('button', 'btn', note ? '取消编辑' : '清空草稿'); cancel.type = 'button';
    const hint = textEl('small', 'note-draft-hint', '草稿会在此浏览器保留 · Ctrl / ⌘ + Enter 保存');
    actions.append(save, cancel);
    form.append(modes, input, rendered, actions, hint);
    const resize = () => { if (!input.hidden && input.isConnected) { input.style.height = 'auto'; input.style.height = Math.max(130, input.scrollHeight) + 'px'; } };
    const mode = showPreview => {
      input.hidden = showPreview; rendered.hidden = !showPreview;
      edit.setAttribute('aria-pressed', String(!showPreview)); preview.setAttribute('aria-pressed', String(showPreview));
      if (showPreview) rendered.replaceChildren(noteMarkdown(input.value || '暂无内容'));
      else { resize(); input.focus({ preventScroll: true }); }
    };
    edit.setAttribute('aria-pressed', 'true'); preview.setAttribute('aria-pressed', 'false');
    edit.onclick = () => mode(false); preview.onclick = () => mode(true);
    const persist = () => {
      draft.body = input.value;
      draft.revision = note?.revision;
      const ok = noteDrafts.set(questionId, note?.id, draft);
      hint.textContent = ok ? '草稿已保留 · Ctrl / ⌘ + Enter 保存' : '浏览器无法保留草稿，请保存笔记后再离开';
      save.disabled = !input.value.trim(); resize();
    };
    input.addEventListener('input', persist);
    input.addEventListener('keydown', event => {
      if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') { event.preventDefault(); form.requestSubmit(); }
    });
    save.disabled = !input.value.trim();
    cancel.onclick = () => {
      if (saving) return;
      noteDrafts.remove(questionId, note?.id);
      say(''); render();
    };
    form.onsubmit = async event => {
      event.preventDefault();
      if (saving || !input.value.trim()) return;
      const body = input.value;
      persist(); saving = true; refresh.disabled = true; input.disabled = save.disabled = cancel.disabled = true;
      save.textContent = '保存中…'; say('');
      try {
        const saved = note ? await noteRequest('/notes/' + note.id, 'PATCH', { body, revision: note.revision })
          : await noteRequest('/notes', 'POST', { body, question_id: questionId, client_id: draft.client_id });
        noteDrafts.remove(questionId, note?.id, body);
        const index = documentData.notes.findIndex(item => item.id === saved.id);
        if (index >= 0) documentData.notes[index] = saved; else documentData.notes.push(saved);
        changed();
        if (root.isConnected) { render(); say('已保存'); }
      } catch (error) {
        if (root.isConnected) say('保存失败：' + error.message + '。草稿仍在，可重试。', true);
      } finally {
        saving = false; refresh.disabled = false; input.disabled = cancel.disabled = false;
        save.disabled = !input.value.trim(); save.textContent = note ? '保存修改' : '保存笔记';
      }
    };
    requestAnimationFrame(resize);
    return form;
  }

  function render() {
    if (!documentData) return;
    const pending = noteDrafts.get(questionId);
    const accepted = pending && documentData.notes.find(note => note.client_id === pending.client_id);
    if (accepted) {
      if (accepted.body !== pending.body) noteDrafts.set(questionId, accepted.id, { ...pending, revision: accepted.revision });
      noteDrafts.remove(questionId, null, pending.body);
    }
    list.replaceChildren(); compose.replaceChildren();
    if (!documentData.notes.length) list.appendChild(textEl('p', 'note-empty', '还没有笔记，在下面记下这道题的思路。'));
    for (const note of documentData.notes) {
      const card = el('article', 'note-card'); card.dataset.noteId = note.id;
      const top = el('div', 'note-card-tools');
      top.appendChild(textEl('time', '', noteTime(note)));
      const edit = textEl('button', 'text-action', '编辑笔记'); edit.type = 'button';
      edit.onclick = () => {
        if (saving) return;
        noteDrafts.set(questionId, note.id, { body: note.body, client_id: note.client_id, revision: note.revision });
        render(); list.querySelector(`[data-note-id="${note.id}"] textarea`)?.focus({ preventScroll: true });
      };
      const download = textEl('button', 'text-action', '导出 Markdown'); download.type = 'button';
      download.onclick = () => downloadNotes([{ question: documentData.question, notes: [note] }]);
      const remove = textEl('button', 'text-action note-delete', '删除'); remove.type = 'button';
      remove.onclick = async () => {
        if (saving || !confirm('删除这条笔记？')) return;
        saving = true; remove.disabled = refresh.disabled = true; say('');
        try {
          await noteRequest('/notes/' + note.id + '?revision=' + note.revision, 'DELETE');
          noteDrafts.remove(questionId, note.id);
          documentData.notes = documentData.notes.filter(item => item.id !== note.id);
          changed(); if (root.isConnected) { render(); say('已删除'); }
        } catch (error) { if (root.isConnected) say('删除失败：' + error.message, true); }
        finally { saving = false; remove.disabled = refresh.disabled = false; }
      };
      top.append(edit, download, remove); card.appendChild(top);
      const draft = noteDrafts.get(questionId, note.id);
      if (draft) {
        edit.hidden = true;
        if (draft.revision !== note.revision) {
          const latest = el('details', 'note-latest');
          latest.append(textEl('summary', '', '其他页面已更新此笔记，展开核对已保存的内容'), noteMarkdown(note.body));
          card.appendChild(latest);
        }
        card.appendChild(editor(note));
      } else card.appendChild(noteMarkdown(note.body));
      list.appendChild(card);
    }
    compose.append(textEl('h4', '', '新增笔记'), editor());
    changed();
  }

  async function load() {
    if (saving || loading) return;
    const version = ++loadVersion;
    loading = true; refresh.disabled = true; say('正在读取笔记…');
    try {
      const data = await api('/notes?question_id=' + questionId);
      if (version !== loadVersion || !root.isConnected) return;
      documentData = data; render(); say('');
    } catch (error) { if (root.isConnected) say('笔记读取失败：' + error.message + '。请点击“刷新笔记”重试。', true); }
    finally { loading = false; refresh.disabled = false; }
  }
  refresh.onclick = load;
  if (initial) render();
  return { root, load };
}

function attachQuestionNotes(card, question, head) {
  const toggle = textEl('button', 'text-action question-note-toggle', question.note_count ? '笔记 ' + question.note_count : '笔记');
  toggle.type = 'button'; toggle.dataset.noteQuestion = question.id;
  toggle.classList.toggle('has-notes', question.note_count > 0);
  toggle.setAttribute('aria-label', `第 ${question.number} 题的笔记`);
  toggle.setAttribute('aria-expanded', 'false');
  const panel = createNotePanel(question.id);
  panel.root.id = 'notes-for-' + question.id; panel.root.hidden = true;
  toggle.setAttribute('aria-controls', panel.root.id);
  toggle.onclick = () => {
    const opening = panel.root.hidden;
    panel.root.hidden = !opening; toggle.setAttribute('aria-expanded', String(opening));
    if (opening) void panel.load();
  };
  head.appendChild(toggle); card.appendChild(panel.root);
}

async function viewNotes(query = '', source = '') {
  const main = $('main'); main.replaceChildren(); main.classList.add('notebook-sheet');
  main.append(textEl('h1', 'title', '数学笔记本'), textEl('p', 'lead', '真题和 880 的笔记按题目保存，可回到原题继续做题。'));
  const form = el('form', 'notebook-search');
  const search = el('input'); search.type = 'search'; search.value = query;
  search.placeholder = '搜索笔记内容或章节'; search.setAttribute('aria-label', '搜索数学笔记');
  const filter = el('select'); filter.setAttribute('aria-label', '笔记题目来源');
  for (const [value, name] of [['', '全部笔记'], ['exam', '真题笔记'], ['lilin880', '880 笔记']]) {
    const option = textEl('option', '', name); option.value = value; filter.appendChild(option);
  }
  filter.value = source;
  const submit = textEl('button', 'btn', '搜索'); submit.type = 'submit';
  form.append(search, filter, submit);
  form.onsubmit = event => {
    event.preventDefault();
    const hash = '#/notes?' + new URLSearchParams({ query: search.value.trim(), source: filter.value });
    if (location.hash === hash) void route(); else location.hash = hash;
  };
  main.appendChild(form);
  const groups = await api('/notebook?' + new URLSearchParams({ query, source }));
  if (!main.isConnected) return;
  const summary = el('div', 'notebook-summary');
  const total = textEl('span', '', '');
  const download = textEl('button', 'text-action', '导出当前笔记'); download.type = 'button';
  const updateSummary = () => {
    const count = groups.reduce((sum, group) => sum + group.notes.length, 0);
    total.textContent = `${groups.filter(group => group.notes.length).length} 道题 · ${count} 条笔记`;
    download.disabled = !count;
  };
  download.onclick = () => downloadNotes(groups.filter(group => group.notes.length));
  summary.append(total, download); main.appendChild(summary); updateSummary();
  if (!groups.length) main.appendChild(textEl('div', 'empty', query || source ? '没有符合条件的笔记。' : '还没有数学笔记。在真题或 880 题目旁点击“笔记”即可开始。'));
  groups.forEach(group => {
    const section = el('section', 'notebook-group');
    const heading = el('div', 'notebook-group-heading');
    heading.append(textEl('h2', '', group.question.source), studyLink('回到原题 →', noteQuestionHash(group.question), 'text-action practice-link'));
    const original = el('details', 'notebook-original');
    original.append(textEl('summary', '', '查看题目'), el('div', 'stem', group.question.stem_html));
    section.append(heading, original);
    const panel = createNotePanel(group.question.id, group, data => {
      if (data) group.notes = data.notes;
      updateSummary();
    });
    section.appendChild(panel.root); main.appendChild(section);
  });
  window.scrollTo(0, 0);
}
