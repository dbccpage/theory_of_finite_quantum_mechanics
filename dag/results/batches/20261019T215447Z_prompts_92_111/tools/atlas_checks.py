import importlib.util,json,sys
from pathlib import Path
B=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('stages',B/'target_stages.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
folder=B/'review/atlas_first';sources=[Path(__file__)]+[s.ROOT/p for p in ['scripts/verify_qm_atlas_loc.py','scripts/install_qm_atlas_hook.py','code/python/tests/test_qm_atlas_loc.py','code/python/src/qm/textbook_problems.py','code/rust/src/qm/textbook_problems.rs','lean4/FiniteQM.lean','docs/QM_PROBLEM_AND_PROOF_ATLAS.md','.agents/rules/qm_atlas_loc_sync.md','rules/rules.yaml']]
for label,argv in [('atlas',[sys.executable,'-X','utf8','scripts/verify_qm_atlas_loc.py']),('pytest',[sys.executable,'-X','utf8','-m','pytest','code/python/tests/test_qm_atlas_loc.py','-q'])]:
 r=s.native.record(folder,label,argv,sources=sources);print(json.dumps({'gate':label,'exit_code':r['exit_code']}),flush=True)
