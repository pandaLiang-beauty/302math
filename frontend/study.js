'use strict';
let activeStudy = null;
let studyOpenVersion = 0;
let workStorage;
try { workStorage = localStorage; } catch {}
const workStore = MathWorkStore.createStore({storage: workStorage,
  send: (sid, qid, body) => api(`/study/sessions/${sid}/items/${qid}`, {method:'PATCH', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body)}),
  notify: entry => window.dispatchEvent(new CustomEvent('math-work-change', {detail:entry})),
});
const legacyChoices = MathStudyFlow.createChoiceStore(workStorage);
let legacyMigration = null;
let legacyConflicts = [];
let legacyMigrationError = '';
function migrateChoices() {
  if(legacyMigration)return legacyMigration;
  legacyMigration=(async()=>{
    let choices;try{choices=JSON.parse(workStorage?.getItem('math302-paper-choices-v1')||'{}');}catch{return;}
    if(!choices||typeof choices!=='object'||Array.isArray(choices))return;
    choices=Object.fromEntries(Object.entries(choices).filter(([k,v])=>/^[0-9]{1,12}$/.test(k)&&typeof v==='string'&&/^[ABCD]$/.test(v)).slice(0,3000));
    if(!Object.keys(choices).length)return;
    const fingerprint=JSON.stringify(choices);
    try{const done=JSON.parse(workStorage?.getItem('math302-legacy-imported-v1')||'null');if(done?.fingerprint===fingerprint){legacyConflicts=done.conflicts||[];return;}}catch{}
    const result=await postStudy('/import-choices',{choices});legacyConflicts=result.conflicts;legacyMigrationError='';
    try{workStorage?.setItem('math302-legacy-imported-v1',JSON.stringify({fingerprint,conflicts:legacyConflicts}));}catch{}
  })().catch(err=>{legacyMigration=null;legacyMigrationError='旧浏览器记录尚未完成迁移：'+err.message+'。原始内容仍保留，请联网后刷新重试。';});
  return legacyMigration;
}
const savedChoices = {get: id => activeStudy?.entries.get(Number(id))?.value.answer || '',
  set: (id, answer) => { const e=activeStudy?.entries.get(Number(id)); if(e)workStore.change(e,{answer}); }};
function postStudy(path, body) { return api('/study'+path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}); }
function downloadStudyDrafts() {
  const data={};
  try { for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);if(k.startsWith('math302-'))data[k]=localStorage.getItem(k);} } catch {}
  for(const [k,e] of workStore.entries)if(e.pending)data['pending:'+k]=e.pending;
  const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));
  const a=document.createElement('a');a.href=url;a.download='数学本机记录备份.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
async function openStudy(scope,title,problems,originId=null) {
  const version=++studyOpenVersion;
  activeStudy=null;
  if(!problems.length)return;
  await migrateChoices();
  const session=await postStudy('/sessions',{scope,title,question_ids:problems.map(p=>p.id),origin_id:originId});
  if(version!==studyOpenVersion)return;
  const entries=new Map();
  for(const p of problems){
    const e=workStore.register(session.items[p.id]);entries.set(p.id,e);
    // Preserve the original local key as a backup. Never overwrite existing server work.
    const old=legacyChoices.get(p.id);
    if(old&&e.value.revision===0&&!e.pending&&(p.options||[]).some(o=>o.key===old))workStore.change(e,{answer:old});
  }
  activeStudy={session,entries};
}
function studyControls(card,p) {
  const e=activeStudy?.entries.get(p.id);if(!e)return;
  let referenceChoice='',referenceTrusted=true;
  const root=el('section','study-answer');root.setAttribute('aria-label','本题作答记录');
  const status=textEl('span','study-save','');status.setAttribute('role','status');
  const top=el('div','study-answer-top');top.append(textEl('strong','','我的作答'),status);root.append(top);
  let answerInput;
  if(p.qtype!=='choice'){
    answerInput=el('textarea','study-text');answerInput.rows=2;answerInput.maxLength=20000;
    answerInput.placeholder=p.qtype==='blank'?'写下结果，支持 $数学公式$':'写下最终结果或关键步骤，也可以上传纸上演算';
    answerInput.setAttribute('aria-label','我的答案');answerInput.value=e.value.answer;
    answerInput.oninput=()=>workStore.change(e,{answer:answerInput.value});root.append(answerInput);
  }
  const thinking=el('details','study-thinking');thinking.open=!!e.value.work;
  thinking.append(textEl('summary','','演算与思路'));
  const work=el('textarea','study-text');work.rows=4;work.maxLength=50000;work.value=e.value.work;
  work.placeholder='已知条件、想到的方法、卡住的步骤……自动保存';work.setAttribute('aria-label','演算与思路');
  work.oninput=()=>workStore.change(e,{work:work.value});thinking.append(work);root.append(thinking);
  const actions=el('div','study-actions');
  const review=textEl('button','btn','核对答案与解析');review.type='button';
  review.onclick=async()=>{
    if(e.value.phase==='work'){workStore.change(e,{phase:'review'});await workStore.flush(e);}
    if(!solution.childNodes.length){
      review.disabled=true;
      try{
        const data=await api('/question?id='+p.id);
        if(data.solution_markdown)solution.innerHTML=MathMarkdown.render(data.solution_markdown);
        else solution.innerHTML=(data.answer_html?'<p><b>参考答案</b> '+data.answer_html+'</p>':'')+(data.solution_html||'');
        if(!solution.childNodes.length)solution.append(textEl('p','','本题解析暂不可用，请先保留作答。'));
        if(data.solution_source)solution.prepend(textEl('p','solution-source',data.solution_source));
        if(p.qtype==='choice'&&/^[ABCD]$/.test(data.answer||'')){
          referenceChoice=data.answer;referenceTrusted=data.answer_checkable!==false;solution.prepend(textEl('p','study-choice-check',''));render();
        }
        renderMath(solution);
      }catch(err){status.textContent='解析加载失败：'+err.message;return;}
      finally{review.disabled=false;}
    }
    solution.hidden=!solution.hidden;
    if(e.value.phase==='review')solution.hidden=false;
  };
  const history=textEl('button','text-action','历次作答');history.type='button';
  const historyPanel=el('div','study-history');historyPanel.hidden=true;
  history.onclick=async()=>{
    if(!historyPanel.hidden){historyPanel.hidden=true;return;}
    history.disabled=true;
    try{
      const list=await api('/study/questions/'+p.id+'/history');historyPanel.replaceChildren();
      if(!list.length)historyPanel.append(textEl('p','','完成核对并记录结果后，会留下本次答案与演算。'));
      list.forEach(h=>{const d=el('details');const when=new Date(h.created_at.replace(' ','T')+'Z').toLocaleString('zh-CN');d.append(textEl('summary','',when+' · '+({correct:'做对',fuzzy:'生疏',wrong:'不会／做错'}[h.snapshot.rating])+' · '+h.title));
        const body=el('div','note-markdown');body.innerHTML=MathMarkdown.render('**当时的答案**\n\n'+(h.snapshot.answer||'未填写')+'\n\n**当时的演算**\n\n'+(h.snapshot.work||'未填写'));
        d.append(body);
        if(h.snapshot.reason)d.append(textEl('p','', '当时的主要卡点：'+({idea:'想不到方法',calculation:'计算出错',speed:'用时太久'}[h.snapshot.reason]||h.snapshot.reason)));
        if(h.snapshot.reference_answer){const reference=el('div','note-markdown');reference.innerHTML=MathMarkdown.render((h.snapshot.reference_checkable===false?'**当时题库答案（题面待核对）**':'**当时的参考答案**')+'\n\n'+h.snapshot.reference_answer);d.append(reference);}
        for(const id of h.snapshot.draft_images||[]){const a=studyLink('查看当时的草稿照片 ↗','/api/draft-images/'+id,'text-action');a.target='_blank';a.rel='noopener';d.append(a);}
        historyPanel.append(d);});historyPanel.hidden=false;
    }catch(err){status.textContent=err.message;}finally{history.disabled=false;}
  };
  actions.append(review,history);root.append(actions);
  const solution=el('div','study-solution');solution.hidden=true;root.append(solution);
  const ratings=el('div','study-rating');
  ratings.append(textEl('span','','核对后，记录这次完成情况：'));
  const reason=el('select');reason.setAttribute('aria-label','主要卡点');
  [['','主要卡点（可选）'],['idea','想不到方法'],['calculation','计算出错'],['speed','用时太久']].forEach(([v,t])=>{const o=textEl('option','',t);o.value=v;reason.append(o);});
  ratings.append(reason);
  [['correct','做对了'],['fuzzy','做对但生疏'],['wrong','不会／做错']].forEach(([rating,label])=>{
    const b=textEl('button','btn',label);b.type='button';b.onclick=async()=>{workStore.change(e,{phase:'done',rating,reason:rating==='correct'?'':reason.value});await workStore.flush(e);};ratings.append(b);
  });root.append(ratings);
  const completed=el('div','study-completed');const completion=textEl('span','','');
  const redo=textEl('button','btn','再做一次');redo.type='button';
  redo.onclick=async()=>{
    if(e.pending||e.active)return;
    redo.disabled=true;
    try{const saved=await postStudy(`/sessions/${e.value.session_id}/items/${p.id}/redo`,{revision:e.value.revision,mutation:crypto.randomUUID()});workStore.adopt(saved);solution.replaceChildren();solution.hidden=true;reason.value='';}
    catch(err){status.textContent=err.message;}finally{redo.disabled=false;}
  };
  completed.append(completion,redo);root.append(completed);
  const problems=el('div','study-sync-problem');problems.hidden=true;
  const issue=textEl('p','','');const retry=textEl('button','btn','重试保存');retry.onclick=()=>void workStore.flush(e);
  const local=textEl('button','btn','保留本机版本');local.onclick=()=>workStore.resolve(e,true);
  const remote=textEl('button','btn','使用服务器版本');remote.onclick=()=>workStore.resolve(e,false);
  const download=textEl('button','text-action','下载本机备份');download.onclick=downloadStudyDrafts;
  const compare=el('div','study-conflict-compare');
  problems.append(issue,compare,retry,local,remote,download);root.append(problems);
  card.append(root,historyPanel);
  function render(){
    const done=e.value.phase==='done';
    status.textContent=e.conflict?'有版本冲突':e.error?'尚未同步':e.pending||e.active?'正在保存…':'已保存到服务器';
    status.classList.toggle('error',!!(e.error||e.conflict));
    if(answerInput){answerInput.disabled=done||!!e.conflict;if(document.activeElement!==answerInput)answerInput.value=e.value.answer;}
    work.disabled=done||!!e.conflict;if(document.activeElement!==work)work.value=e.value.work;
    const check=solution.querySelector('.study-choice-check');
    if(check)check.textContent=referenceTrusted?`你的选择：${e.value.answer||'未选'} · 参考答案：${referenceChoice}${e.value.answer===referenceChoice?' · 选择正确':' · 本次尚未选对'}`:`你的选择：${e.value.answer||'未选'} · 题库原答案：${referenceChoice}（题面待核对，请阅读说明；本题不自动判正误）`;
    card.querySelectorAll('.choice').forEach(btn=>{const selected=btn.dataset.key===e.value.answer;btn.classList.toggle('selected',selected);btn.setAttribute('aria-checked',String(selected));btn.disabled=done||!!e.conflict;});
    ratings.hidden=e.value.phase!=='review';completed.hidden=!done;
    completion.textContent=({correct:'本次做对了',fuzzy:'本次做对但生疏',wrong:'本次不会／做错'}[e.value.rating]||'')+(e.pending?' · 等待保存':' · 已留下作答记录');
    redo.disabled=!!(e.pending||e.active||e.conflict);
    problems.hidden=!(e.error||e.conflict||e.storageError);issue.textContent=e.storageError||e.error||'另一页面保存了不同内容，请核对两份记录。';
    local.hidden=remote.hidden=!e.conflict;retry.hidden=!!e.conflict;
    compare.replaceChildren();
    if(e.conflict){for(const [label,v] of [['本机内容',e.value],['服务器内容',e.conflict]]){const d=el('details');d.append(textEl('summary','',label),textEl('pre','',v.answer+'\n'+v.work));compare.append(d);}}
    setSidebarActive();
  }
  card._studyRender=render;render();
}
window.addEventListener('math-work-change',event=>{
  document.querySelectorAll('.q').forEach(card=>{if(Number(card.dataset.qid)===event.detail.value.question_id)card._studyRender?.();});
});
window.addEventListener('beforeunload',event=>{if(workStore.pending()){event.preventDefault();event.returnValue='';}});
window.addEventListener('online',()=>void workStore.retry());
setInterval(()=>{if(navigator.onLine)void workStore.retry();},15000);
