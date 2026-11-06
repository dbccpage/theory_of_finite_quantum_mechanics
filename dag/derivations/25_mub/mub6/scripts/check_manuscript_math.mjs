import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL,fileURLToPath} from 'node:url';
const argumentsMap=new Map();
for(let i=2;i<process.argv.length;i+=2){
 const key=process.argv[i];
 if(!['--module-root','--papers-dir','--output-dir'].includes(key)||!process.argv[i+1])
  throw new Error('Expected --module-root, --papers-dir, or --output-dir followed by a path');
 argumentsMap.set(key,process.argv[i+1]);
}
const require=createRequire(import.meta.url);
const moduleRoot=argumentsMap.get('--module-root');
const resolveModule=(name,entry='index.js')=>moduleRoot?path.join(moduleRoot,name,entry):require.resolve(name);
const {micromark}=await import(pathToFileURL(resolveModule('micromark')).href);
const {math,mathHtml}=await import(pathToFileURL(resolveModule('micromark-extension-math')).href);
const katex=require(moduleRoot?path.join(moduleRoot,'katex'):'katex');
const katexPackage=path.dirname(require.resolve(moduleRoot?path.join(moduleRoot,'katex/package.json'):'katex/package.json'));
const papersDir=path.resolve(argumentsMap.get('--papers-dir')||fileURLToPath(new URL('..',import.meta.url)));
const targets=['mub6.md','mub6_claim_ledger.md','mub6_change_log.md','mub6_paper_update_and_frontier_synthesis_plan.md'];
const outdir=path.resolve(argumentsMap.get('--output-dir')||'scratch/mub6-render');
fs.mkdirSync(outdir,{recursive:true});
fs.cpSync(path.join(katexPackage,'dist/fonts'),path.join(outdir,'fonts'),{recursive:true});
const results=[];
for(const name of targets){
 const source=fs.readFileSync(path.join(papersDir,name),'utf8');
 if(/^(?:<<<<<<<|=======|>>>>>>>)/m.test(source))throw Error('Conflict marker: '+name);
 const html=micromark(source,{extensions:[math()],htmlExtensions:[mathHtml({throwOnError:true,strict:'error',trust:false})]});
 const count=(html.match(/class="math math-/g)||[]).length;
 const leftover=html.replace(/<pre[\s\S]*?<\/pre>/g,'').replace(/<code[\s\S]*?<\/code>/g,'').replace(/<annotation[\s\S]*?<\/annotation>/g,'');
 const prose=source.replace(/```[\s\S]*?```/g,'').replace(/`[^`]*`/g,'');
 const escapedCurrency=(prose.match(/\\\$/g)||[]).length;
 if((leftover.match(/\$/g)||[]).length!==escapedCurrency)throw Error('Unmatched dollar delimiter: '+name);
 fs.writeFileSync(path.join(outdir,name+'.html'),'<!doctype html><meta charset="utf-8"><title>'+name+'</title><style>'+fs.readFileSync(path.join(katexPackage,'dist/katex.min.css'),'utf8')+' body{max-width:900px;margin:3em auto;font-family:Georgia,serif;line-height:1.5}pre{white-space:pre-wrap}table{border-collapse:collapse}</style>'+html);
 results.push({file:name,math_expressions:count,render:'PASS'});
}
const result={renderer:'micromark + KaTeX',katex_version:katex.version,strict:'error',throwOnError:true,results};
fs.writeFileSync(path.join(outdir,'render-receipt.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
