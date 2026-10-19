"""Make actual work-unit hypotheses explicit without rewriting historical stages."""
from pathlib import Path
B=Path(r'C:\Users\a343o\.codex\worktrees\bell-joint-extension\theory_of_finite_quantum_mechanics\dag\results\batches\20261019T201403Z_prompts_72_91')
p=B/'tools/review.py';t=p.read_text()
needle="    for g in delta['add_or_refine_generators']:g['evidence_status']="
insert="    work_hypotheses=list(dict.fromkeys(h for g in delta['add_or_refine_generators'] for h in g['hypotheses']))\n    delta['scope_refinements']={'historical_source_assumptions_are_not_the_full_work_unit_contract':True,'work_unit_admitted_hypotheses':work_hypotheses,'boundary':'Finite carriers, declared operations/readouts and actual native bounds are supplied assumptions, even when the historical source assumption list is empty.'}\n"
if needle not in t:raise ValueError('Unexpected review tool')
t=t.replace(needle,insert+needle)
needle="    path.write_bytes(yaml.safe_dump(collection,sort_keys=False,allow_unicode=True,width=100).encode());"
insert="    ambient=collection['operad_slots'][s.prepare.SLOTS[0]]\n    ambient['historical_source_assumptions']=list(ambient.get('admitted_assumptions',[]))\n    ambient['work_unit_admitted_hypotheses']=work_hypotheses\n    ambient['admitted_assumptions']=list(dict.fromkeys(ambient['historical_source_assumptions']+work_hypotheses))\n"
t=t.replace(needle,insert+needle);p.write_bytes(t.encode());(B/'tools/refine_work_unit_assumptions.py').write_bytes(Path(__file__).read_bytes())
