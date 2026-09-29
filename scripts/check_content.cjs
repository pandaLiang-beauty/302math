const fs=require('node:fs'),path=require('node:path');
const katex=require('../frontend/node_modules/katex');
const root=path.resolve(__dirname,'..');
const input=['calculus','algebra'].flatMap(book=>fs.readFileSync(path.join(root,`content/workbooks/${book}.md`),'utf8').split(/^#### /m).slice(1).map(part=>({source_key:book+'-'+part.split('｜')[0],stem_markdown:part,options:[]})));
const answers=JSON.parse(fs.readFileSync(path.join(root,'content/reference-answers.json'),'utf8'));
const errors=[];let formulas=0;
function check(key,text){
  if(/[\x00-\x08\x0b\x0c\x0e-\x1f]/.test(text))errors.push({key,error:'control characters'});
  if((text.match(/(?<!\\)\$/g)||[]).length%2)errors.push({key,error:'unbalanced dollar delimiters'});
  for(const m of text.matchAll(/\$\$([\s\S]*?)\$\$|(?<!\\)\$([^$]*?)(?<!\\)\$|\\\[([\s\S]*?)\\\]|\\\(([\s\S]*?)\\\)/g)){
    formulas++;
    const formula=m[1]??m[2]??m[3]??m[4];
    if(/[\t\r]/.test(formula))errors.push({key,formula,error:'unexpected tab or carriage return inside formula'});
    try{katex.renderToString(formula,{displayMode:m[1]!=null||m[3]!=null,throwOnError:true,strict:'ignore',trust:false});}
    catch(e){errors.push({key,formula,error:e.message});}
  }
}
for(const r of input){check(r.source_key,r.stem_markdown);for(const o of r.options)check(r.source_key+':'+o.key,o.text);}
for(const [k,v] of Object.entries(answers))for(const field of ['answer','note'])check(k+':'+field,v[field]||'');
const relationPath=path.join(root,'content/relations.json');
if(fs.existsSync(relationPath))for(const r of JSON.parse(fs.readFileSync(relationPath,'utf8'))){check(`relation:${r.source_id}:${r.target_id}`,r.skill+'\n'+r.reason);}
const result={questions:input.length,answers:Object.keys(answers).length,formulas,errors};
fs.mkdirSync(path.join(root,'backend/data/authoring'),{recursive:true});fs.writeFileSync(path.join(root,'backend/data/authoring/render-check.json'),JSON.stringify(result,null,2));
console.log(JSON.stringify({...result,errors:errors.slice(0,12)}));
if(errors.length)process.exitCode=1;
