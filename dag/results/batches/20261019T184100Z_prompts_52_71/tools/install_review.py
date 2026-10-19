"""Install review tools without editing any recorded stage."""
from pathlib import Path
ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics');SRC=Path(__file__).resolve().parent
B=ROOT/'dag/results/batches/20261019T184100Z_prompts_52_71'
OLD=ROOT/'dag/results/batches/20261019T160201Z_prompts_22_31'
def put(p,b):
    if p.exists():raise ValueError('refuse overwrite '+str(p))
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
put(B/'tools/review.py',(SRC/'review.py').read_bytes())
t=(OLD/'verify_batch.py').read_text().replace("before['nodes'][21:31]","before['nodes'][51:71]").replace('ordered next-ten selection','ordered next-twenty selection').replace('20261019_structure_audit','20261019_resources_audit')
t=t.replace("    total=0;records=0;anchors=set();failed=0","    sys.path.insert(0,str(ROOT/'dag/pfp'))\n    from custody import Custody\n    custody=Custody(ROOT)\n    total=0;records=0;anchors=set();failed=0")
t=t.replace("            if source['available']:require(sha(ROOT/source['snapshot'])==source['actual_sha256'],'source custody')","            require(source['available'],'missing source')\n            require(sha(ROOT/source['snapshot'])==source['actual_sha256'],'source custody')\n            if source['recorded_sha256'] and source['recorded_sha256']!=source['actual_sha256']:\n                require(custody.matches('paper',source['source_path'],source['recorded_sha256'],task),'unresolved historical pin')\n                require(source.get('custody_ledger_sha256')==sha(ROOT/'dag/pfp/filename_custody.json'),'migration ledger custody')")
t=t.replace("            r=load(receipt);require(r['sources_unchanged'] and r['exit_code']==0,'accepted native receipt')","            r=load(receipt);require(r['sources_unchanged'] and r['exit_code']==0,'accepted native receipt')\n            for pin in r['source_pins']:require(sha(Path(pin['path']))==pin['sha256'],'accepted native working bytes drift')")
put(B/'verify_batch.py',t.encode())
put(B/'test_custody_guards.py',(ROOT/'dag/results/batches/20261019T164251Z_prompts_32_51/test_custody_guards.py').read_bytes())
put(B/'tools/execute_remaining.py',(ROOT/'dag/results/batches/20261019T164251Z_prompts_32_51/tools/execute_remaining.py').read_bytes())
put(B/'tools/install_review.py',Path(__file__).read_bytes())
