"""Install final review/replay tooling; preserve all native stage submissions."""
from pathlib import Path
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics');SRC=Path(__file__).resolve().parent;B=ROOT/'dag/results/batches/20261019T201403Z_prompts_72_91';OLD=ROOT/'dag/results/batches/20261019T184100Z_prompts_52_71'
def put(p,b):
    if p.exists():raise ValueError('refuse overwrite '+str(p))
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
t=(OLD/'tools/review.py').read_text().replace('20261019_resources_audit','20261019_boundaries_audit')
a=t.index("    if kind=='witness':");b=t.index("    for g in delta",a);t=t[:a]+t[b:]
put(B/'tools/review.py',t.encode())
t=(OLD/'verify_batch.py').read_text().replace("before['nodes'][51:71]","before['nodes'][71:91]").replace('20261019_resources_audit','20261019_boundaries_audit')
t=t.replace("original=yaml.safe_load((run/'inputs/this_repository'/node['operad_collection']).read_bytes());collection=", "inventory=load(run/'p0/source_inventory.json')['source_records'];captured=next(p for p in inventory if p['repository']=='this_repository' and p['source_path']==node['operad_collection']);original=yaml.safe_load((ROOT/captured['snapshot']).read_bytes());collection=")
t=t.replace("    total=0;records=0;anchors=set();failed=0", "    successor=load(BATCH/'custody/majorana_source_successor.json')\n    for field,key in [('historical_snapshot','historical_sha256'),('current_snapshot','current_sha256')]:require(sha(ROOT/successor[field])==successor[key],'Majorana source successor bytes')\n    require((ROOT/successor['source_path']).read_bytes()==(ROOT/successor['current_snapshot']).read_bytes(),'Majorana current source drift')\n    total=0;records=0;anchors=set();failed=0")
put(B/'verify_batch.py',t.encode());put(B/'test_custody_guards.py',(OLD/'test_custody_guards.py').read_bytes())
t=(OLD/'tools/integrate.py').read_text().replace('test_resources_exact.py','test_boundaries_exact.py').replace('PromptResources','PromptBoundaries');t=t.replace("'20261019T164251Z_prompts_32_51']","'20261019T164251Z_prompts_32_51','20261019T184100Z_prompts_52_71']")
put(B/'tools/integrate.py',t.encode())
t=(OLD/'tools/finalize.py').read_text().replace('20261019_resources_audit','20261019_boundaries_audit').replace('PFP prompts 52 through 71','PFP prompts 72 through 91')
a=t.index("readme='# PFP");b=t.index("(B/'README.md')",a)
t=t[:a]+'''readme='# PFP prompts 72 through 91\\n\\nTwenty previously unrun prompts executed locally through P0/P1/P2/P4/P5, with P3 for actual failed native gates. Every stage retains operad deltas, exact input/source bindings and actual checker/native results. Original failed attempts and setup refusals remain preserved. No external provider was dispatched; active chat cost is unmeasured. One local Codex researcher performed the scope review.\\n\\n'+json.dumps(counts,sort_keys=True)+'\\n\\n'+json.dumps(integration,sort_keys=True)+'\\n\\nThe selected base includes upstream PR83. Its additive Majorana facade re-exports made one file-only source-lead pin stale; the initial P0 preparation refused it. Both source versions and the narrow public-export diff are retained in custody/, along with the original collection, initial request and failed resume. The successful successor uses a distinct snapshot path. No implementation or physical claim is promoted by that metadata repair.\\n\\nThe mathematical review separates declared registry/antecedent fields from real validation, a finite queue from a threshold theorem, repetition-code guarantees from arbitrary stabilizer/homology bounds, Q8 from quantum gravity, finite proxy separation from physical-import independence, and not-exponent-two from topological connectedness. The finite-map bundle receives a scoped Kellner-polynomial stage only; its other rows and physical integral/ansatz imports remain explicit. Actual contextual/code error tables, full Choi matrices, tomography effects and gamma/parity arrays replace route-index or provider-PASS proxies.\\n\\nNative arrays and literal finite/rational Lean statements have separate scopes. Full refined-carrier operad identity/substitution/symmetry/coherence, physical transport and original target closure remain open where stated. Cached pinned Mathlib is imported; no full Mathlib/transitive-dependency/whole-repository or hosted-CI claim is made. Counts are unique tests/theorems, not sums of repeated gates. Historical filename-custody paper pins remain explicit and unchanged. Prior results/prompts and unrelated operad collections are checked against their base Git blobs in review/preservation.json.\\n\\n| Prompt | Supported step | Remaining obligation |\\n|---|---|---|\\n'+'\\n'.join(table)+'\\n\\nRead-only replay:\\n\\n    py -3.9 -X utf8 verify_batch.py\\n    py -3.9 -X utf8 -O verify_batch.py\\n    py -3.9 -X utf8 test_custody_guards.py -v\\n\\nGitHub delivery state is independently verified after publication. AuthorityEffect: None.\\n'
''' +t[b:]
put(B/'tools/finalize.py',t.encode())
t=(OLD/'tools/git_prepare.py').read_text().replace('codex/pfp-prompts-52-through-71','codex/pfp-prompts-72-through-91')
a=t.index('for name in sorted(names):');b=t.index("subprocess.run(['git','diff'",a)
t=t[:a]+'''# One batch process retrieves exact blob bytes; avoid thousands of Git launches.
objects={}
for entry in git('ls-files','--stage','-z').split(b'\\0'):
    if not entry:continue
    meta,path=entry.split(b'\\t',1);name=path.decode()
    if name in names:objects[name]=meta.split()[1].decode()
ordered=sorted(names)
raw=git('cat-file','--batch',input=('\\n'.join(objects[n] for n in ordered)+'\\n').encode())
offset=0
for name in ordered:
    end=raw.index(b'\\n',offset);header=raw[offset:end].split();size=int(header[2]);start=end+1;sealed=raw[start:start+size];offset=start+size+1
    if header[1]!=b'blob' or raw[offset-1:offset]!=b'\\n' or sealed!=(ROOT/name).read_bytes():raise ValueError('Staged bytes differ '+name)
if offset!=len(raw):raise ValueError('Unexpected batch blob output')
''' +t[b:]
put(B/'tools/git_prepare.py',t.encode());put(B/'tools/install_workflow.py',Path(__file__).read_bytes())
