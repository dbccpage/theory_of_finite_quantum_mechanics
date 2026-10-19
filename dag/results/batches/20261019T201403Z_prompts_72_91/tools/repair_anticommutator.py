"""Fix the actual Rust sign bug, retaining both source versions and gate history."""
import hashlib,json
from pathlib import Path
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics');B=ROOT/'dag/results/batches/20261019T201403Z_prompts_72_91';source=ROOT/'code/rust/src/finite_probability/boundaries_exact.rs'
before=source.read_bytes();old=b'ma(&mm(&g, &h), &mm(&h, &g), -1),';new=b'ma(&mm(&g, &h), &mm(&h, &g), 1),'
if before.count(old)!=1:raise ValueError('Unexpected sign repair location')
after=before.replace(old,new)
def put(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():raise ValueError('refuse overwrite '+str(p))
    p.write_bytes(b)
sha=lambda b:hashlib.sha256(b).hexdigest()
for label,data in [('before',before),('after',after)]:put(B/'source_repair'/label/source.relative_to(ROOT),data)
source.write_bytes(after)
receipt={'source_path':source.relative_to(ROOT).as_posix(),'before_sha256':sha(before),'after_sha256':sha(after),'before_snapshot':(B/'source_repair/before'/source.relative_to(ROOT)).relative_to(ROOT).as_posix(),'after_snapshot':(B/'source_repair/after'/source.relative_to(ROOT)).relative_to(ROOT).as_posix(),'exact_replacement':{'before':old.decode(),'after':new.decode()},'failure':'Actual Majorana P2 Rust test failed and full cross-language output disagreed; AB-BA was implemented where AB+BA was required.','scope':'Only this Rust anticommutator sign changes. Python certificates and Lean statements remain unchanged. Earlier accepted kinds have separate immutable source versions; fresh final Rust replay is required for every run.'}
put(B/'source_repair/anticommutator.json',(json.dumps(receipt,indent=2)+'\n').encode())
# The generic proof-repair tool is copied for this actual node-specific defect.
t=(B/'tools/repair.py').read_text().replace("['nodes'][0]","['nodes'][13]")
a=t.index("finding='");b=t.index("\n",a)
t=t[:a]+"finding='Actual Majorana P2 exposed Rust subtraction of the reversed product in the anticommutator slot. Replace it with addition; retain the failed host result and unchanged numerical Python certificate. Final integration replays all runs against the repaired shared Rust source.'"+t[b:]
put(B/'tools/repair_majorana.py',t.encode())
# Historical receipts bind their historical source bytes. Only this explicit,
# one-token, versioned successor is permitted in place of current-source equality.
p=B/'verify_batch.py';t=p.read_text();needle='    total=0;records=0;anchors=set();failed=0'
insert='''    repair=load(BATCH/'source_repair/anticommutator.json')
    rb=(ROOT/repair['before_snapshot']).read_bytes();ra=(ROOT/repair['after_snapshot']).read_bytes()
    require(sha(ROOT/repair['before_snapshot'])==repair['before_sha256'] and sha(ROOT/repair['after_snapshot'])==repair['after_sha256'],'Rust source successor hashes')
    old=repair['exact_replacement']['before'].encode();new=repair['exact_replacement']['after'].encode()
    require(rb.count(old)==1 and rb.replace(old,new)==ra and (ROOT/repair['source_path']).read_bytes()==ra,'Rust successor is not the exact declared sign repair')
'''
t=t.replace(needle,insert+needle)
old_line="            for pin in r['source_pins']:require(sha(Path(pin['path']))==pin['sha256'],'accepted native working bytes drift')"
new_lines="""            for pin in r['source_pins']:
                live=Path(pin['path'])
                if live==(ROOT/repair['source_path']) and pin['sha256']==repair['before_sha256']:
                    require(sha(ROOT/repair['before_snapshot'])==pin['sha256'],'historical accepted Rust bytes drift')
                else:require(sha(live)==pin['sha256'],'accepted native working bytes drift')"""
if old_line not in t:raise ValueError('Unexpected historical receipt check')
t=t.replace(old_line,new_lines);p.write_bytes(t.encode())
p=B/'tools/integrate.py';t=p.read_text();needle='for optimized,label in [(False,'
pos=t.index(needle)
insert='''# Fresh full-output replay on the final Rust source, for every historical/current run.
replay_sources=sources+[s.ROOT/'code/rust/src/finite_probability/boundaries_exact.rs']
for i,row in enumerate(rows):
    run=s.ROOT/row['run'];acc=json.loads((run/'accepted.json').read_bytes());candidate=json.loads((run/acc['attempt']/'candidate.json').read_bytes());label='final_rust_replay_'+str(i)
    receipt=s.native.record(folder,label,[cargo,'run','--manifest-path','code/rust/Cargo.toml','-p','tfqm_finite_probability','--example','boundaries_exact_replay','--offline','--locked'],sources=replay_sources,stdin=(run/'public_input.tsv').read_bytes())
    wire_spec=importlib.util.spec_from_file_location('wire_'+str(i),run/'format_certificate.py');wire=importlib.util.module_from_spec(wire_spec);wire_spec.loader.exec_module(wire)
    if receipt['exit_code']!=0 or (folder/(label+'.stdout.log')).read_text().splitlines()!=wire.lines(candidate['data']):raise ValueError('Final Rust output mismatch '+row['node_id'])
    print(json.dumps({'gate':label,'exit_code':receipt['exit_code'],'full_output_match':True}),flush=True)
'''
t=t[:pos]+insert+t[pos:];p.write_bytes(t.encode())
p=B/'tools/finalize.py';t=p.read_text().replace('Actual contextual/code error tables, full Choi matrices, tomography effects and gamma/parity arrays replace route-index or provider-PASS proxies.','Actual contextual/code error tables, full Choi matrices, tomography effects and gamma/parity arrays replace route-index or provider-PASS proxies. The Majorana gate caught a real Rust commutator/anticommutator sign error; its failed checkpoint and before/after source versions remain in source_repair/. P3 corrects the sign without altering the Python numerical certificate. Every run is freshly replayed on the repaired final Rust source.');p.write_bytes(t.encode())
put(B/'tools/repair_anticommutator.py',Path(__file__).read_bytes())
