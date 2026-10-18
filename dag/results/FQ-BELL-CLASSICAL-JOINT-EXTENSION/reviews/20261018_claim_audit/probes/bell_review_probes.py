from pathlib import Path
import importlib.util
import json

root=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics')
run=root/'dag/results/FQ-BELL-CLASSICAL-JOINT-EXTENSION/runs/20261018T225117Z_operad_expectation'
here=Path(__file__).parent
spec=importlib.util.spec_from_file_location('original',run/'check_certificate.py')
checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
original=(run/'p1/candidate.json').read_text()
duplicate=original.replace('"chsh": "2"','"chsh": "999", "chsh": "2"',1)
assert duplicate!=original
dp=here/'bell_duplicate_probe.json';dp.write_bytes(duplicate.encode())
request=json.loads((run/'p1/request.json').read_bytes());candidate=json.loads(original)
request['public_context']['reviewed_work']['work_unit']['operad_slots']['slot_m1_layer0_ambient_carrier']['public_input']['required_anchors']=['missing.lean::made_up']
candidate['anchors']=['missing.lean::made_up']
rp=here/'bell_request_probe.json';cp=here/'bell_candidate_probe.json'
rp.write_bytes(json.dumps(request).encode());cp.write_bytes(json.dumps(candidate).encode())
print(json.dumps({'duplicate_field_accepted_by_old_checker':checker.check(run/'p1/request.json',dp),
 'mutated_context_and_missing_anchor_accepted_by_old_checker':checker.check(rp,cp)},indent=2))
