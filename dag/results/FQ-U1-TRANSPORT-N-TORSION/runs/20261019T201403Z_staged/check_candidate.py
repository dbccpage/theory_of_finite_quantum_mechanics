import sys
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'dag/pfp/prepare_stage.py').is_file())
sys.path.insert(0,str(ROOT/'dag/pfp'))
from boundaries_checker import check as predicate
def check(request,candidate):return predicate(request,candidate,'FQ-U1-TRANSPORT-N-TORSION',Path(__file__).parent/'p1/review_contract.json',ROOT)
if __name__=='__main__':
 import json
 print(json.dumps(check(sys.argv[1],sys.argv[2])))
