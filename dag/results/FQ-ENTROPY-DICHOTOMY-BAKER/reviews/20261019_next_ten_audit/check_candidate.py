"""Reviewed successor of the retained original domain checker."""
import importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'dag/pfp/prepare_stage.py').is_file())
sys.path.insert(0,str(ROOT/'dag/pfp'))
from review_exact_json import audit_bound
config=json.loads((HERE/'config.json').read_bytes())
spec=importlib.util.spec_from_file_location('original_'+config['task_id'].replace('-','_'),ROOT/config['run']/'check_candidate.py')
original=importlib.util.module_from_spec(spec);spec.loader.exec_module(original)
def check(request,candidate):
    audit_bound(request,candidate,config['task_id'],HERE/'config.json')
    return original.check(request,candidate)
if __name__=='__main__':print(json.dumps(check(*sys.argv[1:]),indent=2))
