/* Browser acceptance always uses an isolated database and a dedicated loopback port. */
const {chromium,expect}=require('../frontend/node_modules/@playwright/test');
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {spawn,execFileSync}=require('node:child_process');
const root=path.resolve(__dirname,'..');
const python=process.env.MATH_PYTHON||path.join(root,'backend/.venv/bin/python');
const base='http://127.0.0.1:8304';
(async()=>{
  try{await fetch(base+'/api/health');throw Error('Test port 8304 is already in use');}catch(e){if(e.message.includes('already'))throw e;}
  const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'math-exam-test-'));
  const database=path.join(tmp,'study.db');
  execFileSync(python,['-c',`import sqlite3,sys
s=sqlite3.connect('file:'+sys.argv[1]+'?mode=ro',uri=True);d=sqlite3.connect(sys.argv[2]);s.backup(d)
for t in ('study_history','study_items','study_sessions','attempts'):d.execute('DELETE FROM '+t)
d.commit();d.close();s.close()`,path.join(root,'backend/data/study.db'),database]);
  const server=spawn(python,['backend/server.py'],{cwd:root,env:{...process.env,STUDY_DB_PATH:database,STUDY_BACKEND_PORT:'8304'},stdio:'ignore'});
  let browser;
  try{
    for(let i=0;i<60;i++){try{if((await fetch(base+'/api/health')).ok)break;}catch{}await new Promise(r=>setTimeout(r,200));}
    browser=await chromium.launch({executablePath:process.env.CHROME_PATH||'/opt/google/chrome/chrome',args:['--no-sandbox']});
    const a=await browser.newContext(),b=await browser.newContext();
    const errors=[];
    let pa=await a.newPage();pa.on('pageerror',e=>errors.push(e.message));
    await pa.goto(base+'/#/paper/2020');await pa.waitForSelector('.study-answer');
    const qid=await pa.locator('.q').first().getAttribute('data-qid');
    const card=page=>page.locator(`[data-qid="${qid}"]`);
    await card(pa).locator('.choice').nth(2).click();
    await expect(card(pa).locator('.study-save')).toHaveText('已保存到服务器');
    const pb=await b.newPage();pb.on('pageerror',e=>errors.push(e.message));
    await pb.goto(base+'/#/paper/2020');await pb.waitForSelector('.study-answer');
    await expect(card(pb).locator('.choice').nth(2)).toHaveAttribute('aria-checked','true');
    await card(pa).locator('.choice').nth(0).click();await expect(card(pa).locator('.study-save')).toHaveText('已保存到服务器');
    await card(pb).locator('.choice').nth(3).click();await expect(card(pb).locator('.study-save')).toHaveText('有版本冲突');
    await card(pb).getByRole('button',{name:'使用服务器版本',exact:true}).click();
    await expect(card(pb).locator('.choice').nth(0)).toHaveAttribute('aria-checked','true');
    await card(pa).locator('.study-thinking summary').click();
    await a.setOffline(true);await card(pa).getByRole('textbox',{name:'演算与思路',exact:true}).fill('断网保留的推导 $x^2$');
    await expect(card(pa).locator('.study-save')).toHaveText('尚未同步');
    await pa.close();await a.setOffline(false);pa=await a.newPage();pa.on('pageerror',e=>errors.push(e.message));
    await pa.goto(base+'/#/paper/2020');await pa.waitForSelector('.study-answer');
    await expect(card(pa).getByRole('textbox',{name:'演算与思路',exact:true})).toHaveValue('断网保留的推导 $x^2$');
    await expect(card(pa).locator('.study-save')).toHaveText('已保存到服务器');
    await card(pa).getByRole('button',{name:'核对答案',exact:true}).click();
    await expect(card(pa).locator('.study-solution')).toBeVisible();
    const answerData=await (await fetch(base+'/api/question?id='+qid)).json();
    if('solution_html' in answerData||'solution_markdown' in answerData)throw Error('Answer endpoint still exposes explanations');
    await expect(pa.getByRole('button',{name:/解析/})).toHaveCount(0);
    await expect(card(pa).locator('.study-solution')).not.toContainText('尚未收录');
    await card(pa).getByRole('button',{name:'不会／做错',exact:true}).click();
    await expect(card(pa).locator('.study-save')).toHaveText('已保存到服务器');
    await card(pa).getByRole('button',{name:'再做一次',exact:true}).click();
    await expect(card(pa).locator('.choice.selected')).toHaveCount(0);
    await card(pa).getByRole('button',{name:'历次作答',exact:true}).click();
    await expect(card(pa).locator('.study-history details')).toHaveCount(1);
    await pa.goto(base+`/#/practice?question_id=${qid}`);await pa.waitForSelector('.study-answer');
    await expect(pa.locator('.related-reason').first()).toBeVisible();
    await expect(pa.locator('img.p880')).toHaveCount(0);
    await expect(pa.locator('a[href*="books/880-answers"]')).toHaveCount(0);
    await pa.locator('.q').first().getByRole('button',{name:'核对答案',exact:true}).click();
    await expect(pa.locator('.study-solution').first()).toBeVisible();
    if((await pa.locator('.study-solution').first().textContent()).includes('尚未收录'))throw Error('Related question is missing its reference answer');
    await pa.setViewportSize({width:390,height:844});
    await pa.screenshot({path:path.join(tmp,'practice-mobile.png'),fullPage:false});
    const overflow=await pa.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+2);
    if(overflow)throw Error('Mobile page overflows horizontally');
    const legacy=await browser.newContext();await legacy.addInitScript(({qid})=>localStorage.setItem('math302-paper-choices-v1',JSON.stringify({[qid]:'D'})),{qid});
    const pl=await legacy.newPage();await pl.goto(base+'/#/home');await pl.waitForSelector('.priority-papers');
    await expect(pl.locator('.hint')).toContainText('未覆盖服务器');
    if(errors.length)throw Error(errors.join('\n'));
    console.log(JSON.stringify({passed:['cross-browser restore','version conflict','offline close and recovery','attempt history and redo','inline text and answers','exam-linked practice','mobile layout','legacy conflict protection'],artifacts:tmp}));
  }finally{if(browser)await browser.close();server.kill('SIGTERM');}
})().catch(e=>{console.error(e);process.exitCode=1});
