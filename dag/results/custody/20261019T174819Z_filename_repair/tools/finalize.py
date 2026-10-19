"""Seal the measured custody repair and explicitly stage only its owned paths."""
import hashlib,json,re,subprocess,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1];ROOT=next(p for p in R.parents if (p/'dag/pfp/prepare_stage.py').is_file())
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,data):
    if p.exists():raise ValueError('Refuse overwrite '+str(p))
    p.write_bytes((json.dumps(data,indent=2)+'\n').encode())
selection=json.loads((R/'selection.json').read_bytes());result=json.loads((R/'verification/result.json').read_bytes());transforms=json.loads((R/'transform_review.json').read_bytes());classification=json.loads((R/'review/error_classification.json').read_bytes())
if result['after_custody_errors']!=0:raise ValueError('Custody remains failing')
protocol=(R/'baseline/protocol.stderr.log').read_text();match=re.search(r'FAILED \(failures=(\d+), errors=(\d+)\)',protocol)
if not match:raise ValueError('Missing actual baseline protocol failure count')
summary={'base_commit':selection['base_commit'],'status':'custody_and_protocol_repaired','measured':result,'migration_byte_review':transforms,'actual_baseline_classification':classification,'baseline_protocol_failures':int(match.group(1)),'baseline_protocol_errors':int(match.group(2)),'reviewer':'Same local Codex researcher, exact byte/source comparisons and independent host checks; no independent-author panel.','scope':'All 398 current custody errors and both protocol failures repaired. No source lead, old failed checkpoint or quantum target is promoted to a proved result.','authority_effect':'None'}
save(R/'summary.json',summary)
text='''# PFP custody and protocol repair

The current 177-prompt validator now has zero errors, and all 12 staged-protocol tests pass. The actual starting 398 errors were 177 stale prompt hashes, 220 stale paper bindings (144 distinct papers), and one stale file-only Majorana source pin. Both previous protocol issues are repaired: corpus custody is checked through exact predecessor/successor records, and the Bell target test resolves the semantic node ID through the index instead of relying on uppercase filenames.

The original prompt audit, all current prompt text and paper text, and every existing staged/review artifact remain byte-identical. All 177 canonical operad presentations, targets and stage histories are preserved. The only canonical operad edit advances one file-only source-lead hash and appends explicit predecessor/current provenance for an upstream additive public-re-export change. Its scope remains source_lead_only/file_only_no_symbol; this is not a Rust implementation or theorem validation.

The new custody ledger binds 177 prompts and 144 papers to exact historical and current snapshots. All 654 whole-filename-token replacements and 144 explicit CRLF-to-LF conversions reproduce the current bytes exactly; other content or numerical changes are rejected. Both versions are checked against their declared Git commits. Historical pins and the historical audit are retained, not silently rewritten or waived.

Adversarial tests reject changed values even with forged current hashes, forged predecessors that do not match the original pin, rollbacks, missing snapshots/entries, wrong tasks, incomplete use coverage, duplicate keys, floats, Boolean digests, arbitrary substitutions and path escapes. The re-export review separately rejects removed/redirected exports and changed source bodies. Earlier failed validator/protocol receipts and the two rejected constructor source versions remain retained; their diagnostics are not presented as passing checks.

Measured verification: '''+json.dumps(result,sort_keys=True)+'''.

Normal and optimized Python each run the full validator, 12 protocol tests, 18 custody tests and the sealed twenty-run replay. The replay checks exact saved certificates and compiler receipts; it does not recompile Rust or Lean. This repair changes no Rust/Lean implementation, numerical certificate, quantum theorem claim or full-operad coherence obligation. These historical limitations remain open.

Live checks from repository root:

    py -3.9 -X utf8 dag/pfp/validate_prompts.py
    py -3.9 -X utf8 dag/pfp/test_staged_prompts.py -v
    py -3.9 -X utf8 dag/pfp/test_custody.py -v
    py -3.9 -X utf8 -O dag/pfp/test_custody.py -v

The source/snapshot custody checker is portable and needs no live Git history. The retained construction/review tools additionally inspect historical Git objects and refuse to overwrite their receipts. AuthorityEffect: None.
'''
(R/'README.md').write_bytes(text.encode())
owned=[ROOT/'dag/pfp'/n for n in ['custody.py','filename_custody.json','test_custody.py','validate_prompts.py','test_staged_prompts.py']]+[ROOT/'dag/operads/ds_qm212_majorana_problem.yaml']
owned+=list(p for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
owned=sorted(set(owned));save(R/'manifest.json',{'scope':'All new repair evidence and live repair sources; this manifest excludes itself. All prior staged evidence is separately bound in preserved_existing_artifacts.json.','files':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in owned]});owned.append(R/'manifest.json')
if git('branch','--show-current').decode().strip()!='codex/repair-pfp-custody':raise ValueError('Wrong repair branch')
if git('rev-parse','HEAD').decode().strip()!=selection['base_commit']:raise ValueError('Base changed before explicit staging')
if git('diff','--cached','--name-only'):raise ValueError('Existing staged changes')
names=sorted(p.relative_to(ROOT).as_posix() for p in owned);changed=set(git('diff','--name-only').decode().splitlines())
if not changed<=set(names):raise ValueError('Unowned tracked modifications '+repr(changed-set(names)))
with tempfile.NamedTemporaryFile(delete=False) as f:
    f.write(b'\0'.join(n.encode() for n in names)+b'\0');plan=Path(f.name)
try:subprocess.run(['git','add','--force','--pathspec-from-file='+str(plan),'--pathspec-file-nul'],cwd=ROOT,check=True)
finally:plan.unlink()
data=subprocess.run(['git','cat-file','--batch'],cwd=ROOT,input=''.join(':'+n+'\n' for n in names).encode(),stdout=subprocess.PIPE,check=True).stdout;at=0
for name in names:
    end=data.index(b'\n',at);size=int(data[at:end].split()[-1]);content=data[end+1:end+1+size];at=end+size+2
    if hashlib.sha256(content).hexdigest()!=sha(ROOT/name):raise ValueError('Git index transformed owned bytes '+name)
subprocess.run(['git','diff','--cached','--check'],cwd=ROOT,check=True)
print(json.dumps({'owned_paths_verified_in_Git_index':len(names),'custody_errors_before':result['before_custody_errors'],'custody_errors_after':result['after_custody_errors'],'protocol_tests_per_mode':result['protocol_tests_per_mode'],'custody_tests_per_mode':result['custody_tests_per_mode'],'preserved_existing_files':result['review']['preserved_existing_file_count'],'operad_presentations_preserved':result['review']['canonical_operad_presentations_preserved']}),flush=True)
