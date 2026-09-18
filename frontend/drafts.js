'use strict';

let activeDraftDialog = null;
const draftClientId = () => globalThis.crypto?.randomUUID?.() || 'draft-' + Date.now() + '-' + Math.random().toString(36).slice(2);
const draftRequest = (path, method, body) => api(path, {
  method, headers: { 'Content-Type': 'application/json' },
  ...(body ? { body: JSON.stringify(body) } : {}),
});

function updateDraftCount(questionId, count) {
  document.querySelectorAll('[data-draft-question="' + Number(questionId) + '"]').forEach(button => {
    button.textContent = count ? '草稿纸 ' + count : '草稿纸';
    button.classList.toggle('has-drafts', count > 0);
  });
}

function closeQuestionDrafts() {
  activeDraftDialog?.preview?.close();
  activeDraftDialog?.root.close();
}

function attachQuestionDrafts(card, question, tools) {
  const toggle = textEl('button', 'text-action question-draft-toggle', question.draft_count ? '草稿纸 ' + question.draft_count : '草稿纸');
  toggle.type = 'button'; toggle.dataset.draftQuestion = question.id;
  toggle.classList.toggle('has-drafts', question.draft_count > 0);
  toggle.setAttribute('aria-label', '第 ' + question.number + ' 题的草稿纸');
  toggle.setAttribute('aria-haspopup', 'dialog');
  toggle.onclick = () => openQuestionDrafts(question);
  tools.appendChild(toggle);
}

function draftPreview(images, start, parent) {
  const dialog = el('dialog', 'draft-preview');
  dialog.setAttribute('aria-label', '查看草稿纸');
  const heading = el('div', 'draft-dialog-heading');
  const title = textEl('strong', '', '');
  const previous = textEl('button', 'btn', '上一张'), next = textEl('button', 'btn', '下一张');
  const zoom = textEl('button', 'btn', '放大');
  const original = studyLink('原图 ↗', '', 'text-action'); original.target = '_blank'; original.rel = 'noopener';
  const close = textEl('button', 'draft-close', '×'); close.setAttribute('aria-label', '关闭图片预览');
  heading.append(title, previous, next, zoom, original, close);
  const canvas = el('div', 'draft-preview-canvas'), image = el('img');
  canvas.appendChild(image); dialog.append(heading, canvas);
  let index = start;
  const draw = () => {
    image.src = images[index].url; image.alt = '第 ' + (index + 1) + ' 张草稿纸';
    title.textContent = (index + 1) + ' / ' + images.length; original.href = images[index].url;
    previous.disabled = index === 0; next.disabled = index === images.length - 1;
    canvas.classList.remove('zoomed'); zoom.textContent = '放大'; canvas.scrollTo(0, 0);
  };
  previous.onclick = () => { if (index > 0) { index--; draw(); } };
  next.onclick = () => { if (index < images.length - 1) { index++; draw(); } };
  image.onclick = zoom.onclick = () => { zoom.textContent = canvas.classList.toggle('zoomed') ? '适应窗口' : '放大'; };
  close.onclick = () => dialog.close();
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') { event.preventDefault(); previous.click(); }
    if (event.key === 'ArrowRight') { event.preventDefault(); next.click(); }
  });
  dialog.addEventListener('close', () => { dialog.remove(); if (parent.preview === dialog) parent.preview = null; });
  document.body.appendChild(dialog); parent.preview = dialog; draw(); dialog.showModal();
}

function openQuestionDrafts(question) {
  closeQuestionDrafts();
  const root = el('dialog', 'draft-dialog');
  root.setAttribute('aria-labelledby', 'draft-dialog-title');
  const heading = el('div', 'draft-dialog-heading');
  const title = textEl('strong', '', '草稿纸'); title.id = 'draft-dialog-title';
  const close = textEl('button', 'draft-close', '×'); close.setAttribute('aria-label', '关闭草稿纸');
  heading.append(title, close);
  const source = textEl('p', 'draft-source', question.src || '第 ' + question.number + ' 题');
  const body = el('div', 'draft-dialog-body'), options = el('div', 'draft-upload-options');
  const choose = textEl('button', 'btn primary', '选图上传'), camera = textEl('button', 'btn draft-camera', '拍照');
  const files = el('input'), cameraFile = el('input');
  for (const input of [files, cameraFile]) {
    input.type = 'file'; input.accept = 'image/jpeg,image/png,image/webp,image/gif'; input.hidden = true;
  }
  files.multiple = true; cameraFile.setAttribute('capture', 'environment');
  files.setAttribute('aria-label', '选择草稿图片'); cameraFile.setAttribute('aria-label', '拍摄草稿纸');
  const formats = textEl('small', 'draft-formats', 'JPG、PNG、WebP、GIF · 单张 9 MB');
  const qrPanel = el('details', 'draft-qr-panel'); qrPanel.open = matchMedia('(min-width: 640px)').matches;
  const qrHeading = textEl('summary', '', '手机扫码上传');
  const qr = el('img', 'draft-qr'); qr.alt = '本题草稿上传二维码'; qr.hidden = true;
  const qrStatus = textEl('p', 'draft-qr-status', '');
  const issueButton = textEl('button', 'text-action', '重新生成');
  const phoneLink = studyLink('打开上传页 ↗', '', 'text-action draft-upload-link');
  phoneLink.target = '_blank'; phoneLink.rel = 'noopener noreferrer'; phoneLink.hidden = true;
  qrPanel.append(qrHeading, qr, qrStatus, issueButton, phoneLink);
  options.append(choose, camera, files, cameraFile, formats, qrPanel);
  const gallery = el('section', 'draft-gallery');
  const galleryHeading = el('div', 'draft-gallery-heading');
  const count = textEl('strong', '', '本题草稿');
  const refresh = textEl('button', 'text-action', '刷新');
  galleryHeading.append(count, refresh);
  const grid = el('div', 'draft-grid'); grid.appendChild(textEl('p', 'draft-empty', '加载中…'));
  gallery.append(galleryHeading, grid); body.append(options, gallery);
  const feedback = textEl('p', 'draft-feedback', ''); feedback.hidden = true;
  feedback.setAttribute('role', 'status'); feedback.setAttribute('aria-live', 'polite');
  const retry = textEl('button', 'btn', '重试上传'); retry.hidden = true;
  root.append(heading, source, body, feedback, retry);
  const ctx = { root, questionId: question.id, closed: false, busy: false, queue: [], images: [], loaded: false,
    version: 0, loadRequest: 0, tokenRequest: 0, expiresAt: 0, timer: null, preview: null };
  activeDraftDialog = ctx;
  const current = () => !ctx.closed && activeDraftDialog === ctx;
  const say = (message, error = false) => {
    if (!current()) return;
    feedback.textContent = message; feedback.hidden = !message; feedback.classList.toggle('error', error);
    feedback.setAttribute('role', error ? 'alert' : 'status');
  };
  const setBusy = busy => {
    ctx.busy = busy;
    for (const control of [choose, camera, files, cameraFile, retry, close]) control.disabled = busy;
    grid.querySelectorAll('.draft-delete').forEach(button => { button.disabled = busy; });
  };
  const updateExpiry = () => {
    if (ctx.expiresAt && Date.now() >= ctx.expiresAt * 1000) {
      qr.hidden = phoneLink.hidden = true; qrStatus.textContent = '二维码已过期'; ctx.expiresAt = 0;
    }
  };
  async function issue() {
    if (!current()) return;
    const request = ++ctx.tokenRequest;
    issueButton.disabled = true; qr.hidden = phoneLink.hidden = true; qrStatus.textContent = '生成二维码…';
    ctx.expiresAt = 0;
    try {
      const token = await draftRequest('/questions/' + ctx.questionId + '/draft-token', 'POST');
      const url = new URL(token.path, location.origin).href;
      const data = await window.MathDraftQR.toDataURL(url, { width: 400, margin: 2, errorCorrectionLevel: 'M' });
      if (!current() || request !== ctx.tokenRequest) return;
      qr.src = data; qr.hidden = false; phoneLink.href = url; phoneLink.hidden = false;
      ctx.expiresAt = token.expires_at; qrStatus.textContent = '10 分钟内有效';
    } catch (error) {
      if (current() && request === ctx.tokenRequest) qrStatus.textContent = '生成失败：' + error.message;
    } finally { if (current() && request === ctx.tokenRequest) issueButton.disabled = false; }
  }
  function renderImages() {
    if (!current()) return;
    updateDraftCount(ctx.questionId, ctx.images.length);
    count.textContent = '本题草稿 · ' + ctx.images.length + ' 张';
    const signature = ctx.images.map(image => image.id).join(',');
    if (ctx.loaded && grid.dataset.images === signature) return;
    grid.dataset.images = signature; grid.replaceChildren();
    if (!ctx.images.length) grid.appendChild(textEl('p', 'draft-empty', '还没有草稿纸'));
    ctx.images.forEach((image, index) => {
      const card = el('article', 'draft-image-card'); card.dataset.draftId = image.id;
      const thumbnail = el('button', 'draft-thumbnail'); thumbnail.type = 'button';
      thumbnail.setAttribute('aria-label', '放大第 ' + (index + 1) + ' 张草稿');
      const img = el('img'); img.src = image.url; img.alt = '草稿纸 ' + (index + 1); img.loading = 'lazy';
      thumbnail.appendChild(img); thumbnail.onclick = () => draftPreview([...ctx.images], index, ctx);
      const caption = el('div', 'draft-image-caption');
      const label = textEl('span', '', '第 ' + (index + 1) + ' 张');
      const remove = textEl('button', 'text-action draft-delete', '删除');
      remove.setAttribute('aria-label', '删除第 ' + (index + 1) + ' 张草稿'); remove.disabled = ctx.busy;
      remove.onclick = async () => {
        if (ctx.busy || !confirm('删除这张草稿纸？')) return;
        setBusy(true); ctx.version++;
        try {
          await draftRequest('/draft-images/' + image.id, 'DELETE');
          ctx.version++; ctx.images = ctx.images.filter(item => item.id !== image.id); renderImages();
          await load(); say('已删除');
        } catch (error) { say('删除失败：' + error.message, true); }
        finally { setBusy(false); }
      };
      caption.append(label, remove); card.append(thumbnail, caption); grid.appendChild(card);
    });
  }
  async function load(notify = false) {
    if (!current()) return;
    const request = ++ctx.loadRequest, version = ctx.version;
    try {
      const state = await api('/questions/' + ctx.questionId + '/drafts');
      if (!current() || version !== ctx.version || request !== ctx.loadRequest) return;
      const previous = new Set(ctx.images.map(image => image.id));
      const added = ctx.loaded ? state.drafts.filter(image => !previous.has(image.id)).length : 0;
      ctx.images = state.drafts; source.textContent = state.question.source;
      renderImages(); ctx.loaded = true;
      if (notify && added) { say('已追加 ' + added + ' 张草稿'); if (qrPanel.open) void issue(); }
    } catch (error) {
      if (current() && version === ctx.version && request === ctx.loadRequest) {
        if (!ctx.loaded) grid.replaceChildren(textEl('p', 'draft-empty', '暂时无法加载草稿'));
        say('加载失败：' + error.message, true);
      }
    }
  }
  async function poll() {
    if (!current()) return;
    updateExpiry();
    if (!document.hidden && !ctx.busy) await load(true);
    if (current()) ctx.timer = setTimeout(poll, 2500);
  }
  async function uploadQueue() {
    if (ctx.busy || !ctx.queue.length) return;
    setBusy(true); ctx.version++; retry.hidden = true;
    const total = ctx.queue.length;
    try {
      while (ctx.queue.length) {
        const item = ctx.queue[0];
        say('正在上传 ' + (total - ctx.queue.length + 1) + ' / ' + total + '…');
        const data = await new Promise((resolve, reject) => {
          const reader = new FileReader(); reader.onload = () => resolve(reader.result);
          reader.onerror = () => reject(new Error('图片读取失败')); reader.readAsDataURL(item.file);
        });
        // This question id and client id remain fixed across file reads, navigation and retries.
        const image = await draftRequest('/questions/' + ctx.questionId + '/drafts', 'POST',
          { image_base64: data, client_id: item.clientId });
        ctx.version++;
        if (!ctx.images.some(saved => saved.id === image.id)) ctx.images.push(image);
        ctx.queue.shift(); renderImages();
      }
      await load(); say('已上传 ' + total + ' 张草稿');
      if (current() && qrPanel.open) void issue();
    } catch (error) {
      say('上传失败：' + error.message + '。剩余 ' + ctx.queue.length + ' 张可重试。', true);
      retry.hidden = false;
    } finally { setBusy(false); }
  }
  function select(event) {
    const selected = [...(event.target.files || [])]; event.target.value = '';
    if (!selected.length || ctx.busy) return;
    for (const file of selected) {
      if (!file.size || file.size > 9000000) { say(file.name + '：图片为空或超过 9 MB', true); return; }
      if (file.type && !['image/jpeg', 'image/png', 'image/webp', 'image/gif'].includes(file.type)) {
        say(file.name + '：请选择 JPG、PNG、WebP 或 GIF 图片', true); return;
      }
    }
    ctx.queue.push(...selected.map(file => ({ file, clientId: draftClientId() })));
    void uploadQueue();
  }
  choose.onclick = () => files.click(); camera.onclick = () => cameraFile.click();
  files.onchange = cameraFile.onchange = select; retry.onclick = uploadQueue;
  issueButton.onclick = issue; refresh.onclick = () => { say(''); void load(); };
  qrPanel.addEventListener('toggle', () => { if (qrPanel.open && !ctx.expiresAt && !issueButton.disabled) void issue(); });
  close.onclick = () => root.close();
  root.addEventListener('cancel', event => { if (ctx.busy) event.preventDefault(); });
  const beforeUnload = event => { if (ctx.busy || ctx.queue.length) { event.preventDefault(); event.returnValue = ''; } };
  window.addEventListener('beforeunload', beforeUnload);
  root.addEventListener('close', () => {
    ctx.closed = true; clearTimeout(ctx.timer); ctx.preview?.close();
    window.removeEventListener('beforeunload', beforeUnload);
    if (activeDraftDialog === ctx) activeDraftDialog = null;
    root.remove();
  });
  document.body.appendChild(root); root.showModal();
  if (qrPanel.open) void issue();
  void poll();
}
