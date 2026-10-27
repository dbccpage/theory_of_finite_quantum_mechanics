from fractions import Fraction as Q
from pathlib import Path
import json,sys,yaml
root=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/'code'))
from residual_error_budget import advance_budget,waiting_window,product_defect_interval
folder=Path(__file__).parent
inputs=yaml.safe_load((folder/'input.yaml').read_text())
assert all(type(x) is str for x in inputs.values())
bounds={k:Q(x) for k,x in inputs.items()}
result={"scope":"exact arithmetic on supplied bounds; no physical enclosure certified","witnesses":[]}
for name in ["witness_valid.json","witness_near_miss.json"]:
 data=json.loads((folder/name).read_text())
 assert type(data['expected_within_budget']) is bool
 budget=advance_budget(bounds['error'],bounds['rate'],Q(data['duration']),bounds['integration_reserve'],bounds['jump_reserve'])
 accepted=budget<=bounds['target']
 assert accepted==data['expected_within_budget']
 result['witnesses'].append(dict(file=name,budget=str(budget),accepted=accepted))
result['waiting_window']=str(waiting_window(bounds['target'],bounds['error'],bounds['integration_reserve']+bounds['jump_reserve'],bounds['rate'],bounds['horizon']))
result['uncertainty_interval']=[str(x) for x in product_defect_interval(2,Q(1,50),Q(1,150))]
print(json.dumps(result,indent=2))
