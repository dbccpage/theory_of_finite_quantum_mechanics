"""Concrete independent witness controls; full stage cases use the domain predicate."""
import importlib.util,json,sys,unittest
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'dag/pfp/prepare_stage.py').exists())
spec=importlib.util.spec_from_file_location('producer',ROOT/'code/python/src/qm/l1_import_exact.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
sys.path.insert(0,str(ROOT/'dag/pfp'));from l1_import_checker import verify
B=ROOT/'dag/results/batches/20261019T232430Z_prompts_112_131'
rows=json.loads((B/'tools/witness_cases.json').read_bytes())
class ExactControls(unittest.TestCase):pass
def test(row):
 def run(self):
  y=m.evaluate(row['kind'],row['input']);i=row['start'];self.assertEqual(y[i:i+len(row['expected'])],row['expected']);verify(row['kind'],row['input'],y)
 return run
for row in rows:setattr(ExactControls,'test_'+row['kind'],test(row))
if __name__=='__main__':unittest.main()
