"""Capture and prove the exact migration relation, then install its strict checker."""
import difflib,hashlib,importlib.util,json,re,subprocess,sys,yaml
from pathlib import Path
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics');R=ROOT/'dag/results/custody/20261019T174819Z_filename_repair';SRC=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'dag/pfp'))
sp=importlib.util.spec_from_file_location('new_custody',SRC/'custody.py');c=importlib.util.module_from_spec(sp);sp.loader.exec_module(c)
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def blobs(ref,paths):
    paths=list(dict.fromkeys(paths));raw=subprocess.run(['git','cat-file','--batch'],cwd=ROOT,input=''.join(ref+':'+p+'\n' for p in paths).encode(),stdout=subprocess.PIPE,check=True).stdout;at=0;result={}
    for path in paths:
        end=raw.index(b'\n',at);parts=raw[at:end].split()
        if len(parts)!=3 or parts[1]!=b'blob':raise ValueError('Unavailable Git source '+path)
        size=int(parts[2]);result[path]=raw[end+1:end+1+size];at=end+size+2
    return result
def put(p,data):
    if p.exists():raise ValueError('Refuse overwrite '+str(p))
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
def save(p,x):put(p,(json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode())
if not (R/'baseline/protocol_receipt.json').exists():raise ValueError('Complete the actual failing baseline first')
selection=json.loads((R/'selection.json').read_bytes());old=selection['historical_commit'];base=selection['base_commit']
if git('rev-parse','HEAD').decode().strip()!=base:raise ValueError('Repair base changed')
index=json.loads((ROOT/'dag/operads/index.json').read_bytes());prior=json.loads(git('show',old+':dag/operads/index.json'))
if [n['node_id'] for n in index['nodes']]!=[n['node_id'] for n in prior['nodes']]:raise ValueError('Corpus changed')
audit=json.loads((ROOT/'dag/pfp/prompt_audit.json').read_bytes());audited={n['node_id']:n for n in audit['nodes']}
old_records=blobs(old,[n['operad_collection'] for n in prior['nodes']]);sources=[]
for n,pn in zip(index['nodes'],prior['nodes']):
    record=yaml.safe_load((ROOT/n['operad_collection']).read_bytes());pr=yaml.safe_load(old_records[pn['operad_collection']])
    sources.append(('prompt',n['prompt'],pn['prompt'],audited[n['node_id']]['after_sha256'],n['node_id']))
    pp=record['target'].get('paper_source_pins',[]);op=pr['target'].get('paper_source_pins',[])
    if len(pp)!=len(op):raise ValueError('Unreviewed paper source set change')
    for pin,before in zip(pp,op):
        if pin['sha256']!=before['sha256']:raise ValueError('Historical paper pin changed')
        if c.sha((ROOT/pin['path']).read_bytes())!=pin['sha256']:
            sources.append(('paper',pin['path'],before['path'],pin['sha256'],n['node_id']))
old_bytes=blobs(old,[s[2] for s in sources]);current_paths=set(git('ls-tree','-r','--name-only',base).decode().splitlines());old_paths=git('ls-tree','-r','--name-only',old).decode().splitlines();aliases={}
for path in old_paths:
    if not path.startswith(('dag/prompts/','dag/operads/','dag/derivations/')):continue
    p=Path(path)
    if p.suffix not in ('.md','.yaml'):continue
    newname=c.canonical_filename(p.name);newpath=(p.parent/newname).as_posix()
    if newname!=p.name and newpath in current_paths:
        if p.name in aliases and aliases[p.name]!=newname:raise ValueError('Ambiguous filename mapping')
        aliases[p.name]=newname
current_bytes=blobs(base,[s[1] for s in sources])
pattern=re.compile(rb'(?<![A-Za-z0-9_.-])(?:'+b'|'.join(re.escape(n.encode()) for n in sorted(aliases,key=len,reverse=True))+rb')(?!(?:[A-Za-z0-9_-]|\.[A-Za-z0-9_.-]))')
entries={};snapshots={};replacement_count=0
for kind,path,historical_path,expected,node in sources:
    before=old_bytes[historical_path];after=(ROOT/path).read_bytes()
    if after!=current_bytes[path]:raise ValueError('Current source differs from the reviewed base Git blob '+path)
    if c.sha(before)!=expected:raise ValueError('Historical bytes do not match the original pin '+historical_path)
    found=pattern.findall(before);renames={n.decode():aliases[n.decode()] for n in sorted(set(found))}
    line_endings='preserve' if c.rewrite(before,renames)==after else 'crlf_to_lf'
    if c.migrate(before,renames,line_endings)!=after:
        print('\n'.join(difflib.unified_diff(c.rewrite(before,renames).decode().splitlines(),after.decode().splitlines(),fromfile='expected_filename_only',tofile=path,n=1)))
        raise ValueError('Change beyond filename references: '+path)
    before_path=R/'snapshots/before'/historical_path;after_path=R/'snapshots/after'/path
    entry={'kind':kind,'path':path,'historical_path':historical_path,'historical_sha256':expected,'historical_git_blob':c.blob(before),'historical_snapshot':before_path.relative_to(ROOT).as_posix(),'current_sha256':c.sha(after),'current_git_blob':c.blob(after),'current_snapshot':after_path.relative_to(ROOT).as_posix(),'filename_renames':renames,'line_endings':line_endings,'uses':[]}
    key=(kind,path)
    if key in entries:
        if {k:v for k,v in entries[key].items() if k!='uses'}!={k:v for k,v in entry.items() if k!='uses'}:raise ValueError('Inconsistent source identity')
    else:
        entries[key]=entry;snapshots[before_path]=before;snapshots[after_path]=after;replacement_count+=len(found)
    if node not in entries[key]['uses']:entries[key]['uses'].append(node)
for entry in entries.values():entry['uses'].sort()
ledger={'schema_id':c.SCHEMA,'authority_effect':'None','historical_commit':old,'migration_commit':selection['migration_commit'],'reviewed_base_commit':base,'historical_audit_sha256':c.sha((ROOT/'dag/pfp/prompt_audit.json').read_bytes()),'snapshot_root':(R/'snapshots').relative_to(ROOT).as_posix(),'scope':'Exact current filename-reference successors of historical source pins. Does not replace the historical audit, source annotations, mathematical values, prompt text, canonical operads or any staged evidence.','artifacts':[entries[k] for k in sorted(entries)]}
# All transformations must be proved before installing any successor.
for path,data in snapshots.items():put(path,data)
put(ROOT/'dag/pfp/custody.py',(SRC/'custody.py').read_bytes());save(ROOT/'dag/pfp/filename_custody.json',ledger)
p=ROOT/'dag/pfp/validate_prompts.py';t=p.read_text()
t=t.replace('import yaml','import yaml\nfrom custody import Custody',1)
needle="    seen=set()"
t=t.replace(needle,"    try:\n        custody=Custody(ROOT)\n    except (ValueError,KeyError,TypeError,OSError) as error:\n        return {'prompts':len(files),'collections':len(indexed),'errors':['filename custody invalid: '+str(error)],'claim':'Custody failure; no mathematical acceptance.'}\n"+needle,1)
t=t.replace("            p=ROOT/pin['path']\n            if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=pin['sha256']:","            if not custody.matches('paper',pin['path'],pin['sha256'],node):")
t=t.replace("        if row.get('after_sha256')!=hashlib.sha256(path.read_bytes()).hexdigest(): errors.append(node+': audit hash mismatch')", "        if not custody.matches('prompt',path.relative_to(ROOT).as_posix(),row.get('after_sha256'),node): errors.append(node+': audit hash mismatch')")
t=t.replace("    workflow=yaml.safe_load", "    try:\n        custody.finish()\n    except ValueError as error:\n        errors.append(str(error))\n    workflow=yaml.safe_load",1)
p.write_bytes(t.encode())
p=ROOT/'dag/pfp/test_staged_prompts.py';t=p.read_text().replace("        bell=next(p for p in PROMPTS if 'FQ-BELL-RATIONAL-VIOLATION-14-5' in p.name)","        index=json.loads((ROOT/'dag/operads/index.json').read_bytes())\n        row=next(n for n in index['nodes'] if n['node_id']=='FQ-BELL-RATIONAL-VIOLATION-14-5')\n        bell=ROOT/row['prompt']").replace("        p=prepare.load(bell)\n        self.assertIn('14/5'", "        p=prepare.load(bell)\n        self.assertEqual(p['node_id'],row['node_id'])\n        self.assertIn('14/5'")
p.write_bytes(t.encode())
put(R/'tools/build.py',Path(__file__).read_bytes());save(R/'transform_review.json',{'changed_prompt_artifacts':sum(e['kind']=='prompt' for e in entries.values()),'changed_paper_artifacts':sum(e['kind']=='paper' for e in entries.values()),'paper_binding_uses':sum(len(e['uses']) for e in entries.values() if e['kind']=='paper'),'whole_filename_token_replacements':replacement_count,'explicit_CRLF_to_LF_artifacts':sum(e['line_endings']=='crlf_to_lf' for e in entries.values()),'review':'Every current byte equals the exact historical Git blob after whole canonical filename-token replacements and the recorded line-ending conversion only. No residual content difference was admitted. Historical digests, current digests and both Git blob IDs are retained and checked against their pinned commits.','scope':'A source-custody repair, not semantic mining completion, a new theorem or full operad coherence.','authority_effect':'None'})
print(json.dumps({'artifacts':len(entries),'snapshots':len(snapshots),'filename_token_replacements':replacement_count,'status':'installed exact custody successor; final tests required'}),flush=True)
