"""Fresh current checks plus exact preservation and pinned-Git provenance review."""
import copy,hashlib,importlib.util,json,os,re,subprocess,sys,time,yaml
from datetime import datetime,timezone
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1]
ROOT=next(p for p in R.parents if (p/'dag/pfp/prepare_stage.py').is_file())
sys.path.insert(0,str(ROOT/'dag/pfp'))
from custody import blob, sha


def require(ok,message):
    if not ok:raise ValueError(message)


def save(path,data):
    require(not path.exists(),'Refuse overwrite '+str(path));path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes((json.dumps(data,indent=2)+'\n').encode())


def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)


def export_extension(before,after):
    pattern=re.compile(rb'^pub use ([A-Za-z_][A-Za-z0-9_]*)::\{([^{}]*)\};\n',re.M)
    def entries(raw):
        exports,public=set(),set()
        for block in pattern.finditer(raw):
            for part in block[2].split(b','):
                if not part.strip():continue
                m=re.fullmatch(rb'\s*([A-Za-z_][A-Za-z0-9_]*)(?:\s+as\s+([A-Za-z_][A-Za-z0-9_]*))?\s*',part)
                require(m is not None,'Unsupported re-export syntax')
                name=m[2] or m[1];require(name not in public,'Public export collision');public.add(name)
                exports.add((block[1]+b'::'+m[1]+(b' as '+m[2] if m[2] else b'')).decode())
        return exports
    be,ae=entries(before),entries(after)
    require(pattern.sub(b'',before)==pattern.sub(b'',after),'Source body changed outside re-exports')
    require(be<ae,'Old re-exports removed, redirected or not strictly extended')
    return sorted(ae-be)


def preserve():
    selection=json.loads((R/'selection.json').read_bytes());base=selection['base_commit']
    listing=git('ls-tree','-r','-z',base,'--','dag/results','dag/operads','dag/prompts','dag/pfp/prompt_audit.json')
    changed_record='dag/operads/ds_qm212_majorana_problem.yaml';preserved=[]
    for row in listing.split(b'\0'):
        if not row:continue
        meta,name=row.split(b'\t',1);mode,kind,digest=meta.split();path=name.decode()
        require(kind==b'blob','Unexpected protected Git object')
        if path==changed_record:continue
        data=(ROOT/path).read_bytes();require(blob(data)==digest.decode(),'Protected bytes changed '+path)
        preserved.append({'path':path,'git_blob':digest.decode(),'sha256':sha(data)})
    review=json.loads((R/'review/majorana_source_successor.json').read_bytes())
    baseline=yaml.safe_load(git('show',base+':'+changed_record));current=yaml.safe_load((ROOT/changed_record).read_bytes())
    expected=copy.deepcopy(baseline);binding=next(b for b in expected['source_bindings'] if b['path']==review['source_path'])
    require(binding['sha256']==review['historical_sha256'] and binding['role']=='source_lead_only' and binding['declaration_status']=='file_only_no_symbol','Historical source-lead scope changed')
    binding['sha256']=review['current_sha256']
    expected['source_pin_successors']=[{'path':review['source_path'],'historical_sha256':review['historical_sha256'],'current_sha256':review['current_sha256'],'review':(R/'review/majorana_source_successor.json').relative_to(ROOT).as_posix(),'role':'source_lead_only','authority_effect':'None'}]
    require(current==expected,'Unrelated Majorana operad/source metadata edit')
    # All 177 presentations, including the sole changed source-lead record, remain exact.
    require(baseline['presentation']==current['presentation'],'Majorana operad changed')
    old_source=git('show',review['historical_commit']+':'+review['source_path']);new_source=git('show',base+':'+review['source_path'])
    require((ROOT/review['historical_snapshot']).read_bytes()==old_source and (ROOT/review['current_snapshot']).read_bytes()==new_source,'Source-successor snapshots differ from their commits')
    require((ROOT/review['source_path']).read_bytes()==new_source,'Live Rust source changed')
    require(export_extension(old_source,new_source)==review['added_public_exports'],'Re-export review differs')
    positive=b'pub mod a;\npub use a::{A};\nconst X: u8=1;\n'
    good=b'pub mod a;\npub use a::{A, B};\nconst X: u8=1;\n'
    require(export_extension(positive,good)==['a::B'],'Valid source review control rejected')
    rejected=0
    for bad in [good.replace(b'A, B',b'B'),good.replace(b'=1',b'=2'),good.replace(b'A, B',b'Q as A, B')]:
        try:export_extension(positive,bad)
        except ValueError:rejected+=1
        else:raise ValueError('Bad source review control accepted')
    ledger=json.loads((ROOT/'dag/pfp/filename_custody.json').read_bytes());refs=[];expected_oids=[]
    for entry in ledger['artifacts']:
        refs.extend([ledger['historical_commit']+':'+entry['historical_path'],base+':'+entry['path']])
        expected_oids.extend([entry['historical_git_blob'],entry['current_git_blob']])
    checked=subprocess.run(['git','cat-file','--batch-check=%(objectname) %(objecttype)'],cwd=ROOT,input=('\n'.join(refs)+'\n').encode(),stdout=subprocess.PIPE,check=True).stdout.decode().splitlines()
    require(checked==[oid+' blob' for oid in expected_oids],'Custody snapshots do not bind the declared Git commits')
    save(R/'review/preserved_existing_artifacts.json',{'base_commit':base,'files':preserved,'exception':{'path':changed_record,'allowed_edit':'Only the reviewed file-only source-lead pin and its explicit predecessor/current provenance. Presentation, target, stage history and other fields are unchanged.'}})
    save(R/'review/provenance_review.json',{'historical_and_current_git_blob_bindings_checked':len(refs),'preserved_existing_file_count':len(preserved),'canonical_operad_presentations_preserved':len(json.loads((ROOT/'dag/operads/index.json').read_bytes())['nodes']),'added_Majorana_public_exports':len(review['added_public_exports']),'source_review_negative_controls_rejected':rejected,'source_review_positive_control':'accepted','scope':'Literal byte/provenance and limited public-re-export checks. No numerical, mathematical, implementation or authority claim is promoted.','authority_effect':'None'})
    print(json.dumps({'preserved_existing_files':len(preserved),'Git_blob_bindings':len(refs),'source_review_negative_controls':rejected}),flush=True)


def main():
    preserve()
    sources=[ROOT/'dag/pfp'/p for p in ['custody.py','filename_custody.json','exact_json.py','validate_prompts.py','test_staged_prompts.py','test_custody.py','prompt_audit.json']]+[Path(__file__)]
    ledger=json.loads((ROOT/'dag/pfp/filename_custody.json').read_bytes())
    for entry in ledger['artifacts']:sources.extend(ROOT/entry[k] for k in ['path','historical_snapshot','current_snapshot'])
    sources.extend(ROOT/n['operad_collection'] for n in json.loads((ROOT/'dag/operads/index.json').read_bytes())['nodes'])
    sources=list(dict.fromkeys(sources))
    def record(name,args):
        path=R/'verification'/(name+'_receipt.json');require(not path.exists(),'Existing receipt '+name)
        pins={p.relative_to(ROOT).as_posix():sha(p.read_bytes()) for p in sources};start=time.perf_counter();stamp=datetime.now(timezone.utc).isoformat()
        p=subprocess.run(args,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        path.parent.mkdir(parents=True,exist_ok=True);(path.parent/(name+'.stdout.log')).write_bytes(p.stdout);(path.parent/(name+'.stderr.log')).write_bytes(p.stderr)
        same=all(sha((ROOT/f).read_bytes())==h for f,h in pins.items())
        save(path,{'argv':args,'started_utc':stamp,'seconds':round(time.perf_counter()-start,3),'exit_code':p.returncode,'source_pins':pins,'sources_unchanged':same})
        print(json.dumps({'gate':name,'exit_code':p.returncode,'seconds':round(time.perf_counter()-start,3)}),flush=True)
        require(same and p.returncode==0,'Failed verification retained: '+name)
    for opt,label in [(False,'normal'),(True,'optimized')]:
        prefix=[sys.executable,'-X','utf8']+(['-O'] if opt else [])
        record('custody_'+label,prefix+['dag/pfp/test_custody.py','-v'])
        record('validator_'+label,prefix+['dag/pfp/validate_prompts.py'])
        record('protocol_'+label,prefix+['dag/pfp/test_staged_prompts.py','-v'])
        record('sealed_twenty_replay_'+label,prefix+['dag/results/batches/20261019T164251Z_prompts_32_51/verify_batch.py'])
    for name in ['validator','sealed_twenty_replay']:
        require((R/'verification'/(name+'_normal.stdout.log')).read_bytes()==(R/'verification'/(name+'_optimized.stdout.log')).read_bytes(),'Optimization changed replay output')
    def tests(name):
        text=(R/'verification'/(name+'.stderr.log')).read_text();m=re.search(r'Ran (\d+) tests[\s\S]*\bOK\s*$',text);require(m is not None,'Missing measured test count');return int(m.group(1))
    before=json.loads((R/'baseline/validator.stdout.log').read_bytes());after=json.loads((R/'verification/validator_normal.stdout.log').read_bytes())
    replay=json.loads((R/'verification/sealed_twenty_replay_normal.stdout.log').read_text().splitlines()[-1])
    result={'before_custody_errors':len(before['errors']),'after_custody_errors':len(after['errors']),'validated_prompts':after['prompts'],'protocol_tests_per_mode':tests('protocol_normal'),'custody_tests_per_mode':tests('custody_normal'),'modes':['normal','Python -O'],'sealed_twenty_run_replay':replay,'review':json.loads((R/'review/provenance_review.json').read_bytes()),'scope':'Current corpus custody and protocol repair. Earlier failure receipts remain historical. Read-only replay checks retained exact certificates; no Rust/Lean compiler or mathematical campaign completion is claimed.','authority_effect':'None'}
    save(R/'verification/result.json',result);print(json.dumps(result),flush=True)


if __name__=='__main__':main()
