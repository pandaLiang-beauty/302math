/* Offline visual references preserve pre-rendered exam fractions and exponents. */
const {chromium}=require('../frontend/node_modules/@playwright/test');
const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..'),data=path.join(root,'backend/data/authoring');
(async()=>{
 const input=JSON.parse(fs.readFileSync(path.join(data,'exam-input.json'),'utf8'));
 fs.mkdirSync(path.join(data,'exam-images'),{recursive:true});
 const browser=await chromium.launch({executablePath:'/opt/google/chrome/chrome',args:['--no-sandbox']});
 try{
 const page=await browser.newPage({viewport:{width:1100,height:1200},deviceScaleFactor:1.5});
 await page.goto('http://127.0.0.1:8303/');await page.waitForSelector('.priority-papers');
 await page.evaluate(()=>{document.body.replaceChildren();const d=document.createElement('div');d.id='capture';d.style.cssText='box-sizing:border-box;width:940px;padding:24px;background:white;color:#111;font-size:18px;line-height:1.8';document.body.append(d)});
 for(const q of input){
  const out=path.join(data,'exam-images',q.id+'.png');if(fs.existsSync(out))continue;
  await page.evaluate(q=>{const d=document.querySelector('#capture');d.innerHTML=`<b>${q.year} 年数学二 · 第 ${q.number} 题</b><div class="stem">${q.stem_html}</div>`;for(const o of JSON.parse(q.options_json)){const p=document.createElement('div');p.style.cssText='display:flex;gap:12px;margin:16px 0';p.innerHTML=`<b>${o.key}.</b><div>${o.text}</div>`;d.append(p)}},q);
  await page.evaluate(()=>document.fonts.ready);await page.locator('#capture').screenshot({path:out});
 }
 console.log('exam image references',input.length);
 }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exitCode=1});
