"""Concrete expected witnesses plus independent predicates over all reviewed cases."""
import importlib.util,json,sys,unittest
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'dag/pfp/prepare_stage.py').exists())
s=importlib.util.spec_from_file_location('born_producer',ROOT/'code/python/src/qm/born_boundary_exact.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
sys.path.insert(0,str(ROOT/'dag/pfp'));from born_boundary_checker import verify
B=ROOT/'dag/results/batches/20261020T000351Z_prompts_132_151'
sys.path.insert(0,str(B/'tools'));from specs import S
rows=json.loads((B/'tools/witness_cases.json').read_bytes())
class ExactControls(unittest.TestCase):pass
def _make_test(row):
 def run(self):
  y=m.evaluate(row['kind'],row['input']);i=row['start'];self.assertEqual(y[i:i+len(row['expected'])],row['expected']);verify(row['kind'],row['input'],y)
  for case in next(s for s in S if s['kind']==row['kind'])['cases']:verify(row['kind'],case,m.evaluate(row['kind'],case))
 return run
for row in rows:setattr(ExactControls,'test_'+row['kind'],_make_test(row))
if __name__=='__main__':unittest.main()
