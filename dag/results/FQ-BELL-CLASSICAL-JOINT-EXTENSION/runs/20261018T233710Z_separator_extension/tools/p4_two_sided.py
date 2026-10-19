from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
RUN=ROOT/'dag/results/FQ-BELL-CLASSICAL-JOINT-EXTENSION/runs/20261018T233710Z_separator_extension'
request=json.loads((RUN/'p3/request.json').read_bytes());candidate=json.loads((RUN/'p3/candidate.json').read_bytes())
public=request['public_context']['reviewed_work']['work_unit']['operad_slots']['slot_m1_layer0_ambient_carrier']['public_input']['cases']
data={p['id']:p for p in public}
answer=next(a for a in candidate['cases'] if a['status']=='blocked' and abs(Q(a['facets'][4]))<=2)
s=importlib.util.spec_from_file_location('checker',RUN/'check_candidate.py');checker=importlib.util.module_from_spec(s);s.loader.exec_module(checker)
classification=checker.check_case(data[answer['id']],answer)
if classification!='blocked':raise ValueError('control is not a verified obstruction')
masks=[1,2,4,7,8,11,13,14]
result={'id':'two_sided_standard_chsh_is_insufficient','original_candidate_sha256':hashlib.sha256((RUN/'p3/candidate.json').read_bytes()).hexdigest(),
 'case':data[answer['id']],'answer':answer,'standard_CHSH_value':answer['facets'][4],
 'standard_two_sided_bound_satisfied':abs(Q(answer['facets'][4]))<=2,'violating_mask':answer['violating_mask'],
 'violated_facet_value':answer['facets'][masks.index(answer['violating_mask'])],
 'predicate_result':classification,'scope':'Compatible positive pair data pass |E00+E01+E10-E11|<=2, yet another signed facet exceeds 2.',
 'earlier_control_boundary':'The first P4 control passed the upper standard facet only; this supplemental control passes both signs.'}
p=RUN/'p4/two_sided_chsh_control.json'
with p.open('xb') as f:f.write((json.dumps(result,indent=2)+'\n').encode())
print('Two-sided control:',answer['id'],'standard S=',result['standard_CHSH_value'],'violated=',result['violated_facet_value'])
