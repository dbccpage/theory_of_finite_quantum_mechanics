"""Collect scoped typed operation records from the kernel receipts of this run; every listed proof must have a receipt."""
from pathlib import Path
import json
B=Path(__file__).resolve().parents[1]
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def save(p,v):Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
D='BornFable.DiscreteTime.'
RECORDS=[
 ('DT-01','Q-parameter group and discrete evolution','A group G, a step u, a rational time parameter','Discrete evolution is the Z-action k -> u^k (additive, unital, inverse at -k); a Q-parameter group restricts to the Z-action of its unit step and is determined on Z by it',[D+n for n in ['QParamGroup','discreteEvolution','discreteEvolution_add','discreteEvolution_zero','discreteEvolution_one','discreteEvolution_neg','QParamGroup.U_natMul','QParamGroup.U_neg','QParamGroup.U_int','QParamGroup.U_eq_discreteEvolution']]),
 ('DT-02','Roots of every order are necessary for continuous time','A Q-parameter group with unit step U(1); a positive natural m','U(1/m)^m = U(1): the unit step has an m-th root in the carrier for every m',[D+n for n in ['QParamGroup.U_inv_nat','QParamGroup.roots_of_all_orders']]),
 ('DT-03','Generator selection is a choice: half-steps come in pairs','A ring R with a Q-module structure; v with v*v = u and v nonzero','-v also squares to u and differs from v; instantiated on rational n x n matrices',[D+n for n in ['sq_root_neg','neg_ne_self_of_ne_zero','half_step_not_unique','matrix_half_step_not_unique']]),
 ('DT-04','The Pythagorean rotation as a reversible discrete evolution over Q','The rational 2 x 2 rotation R345 = [[3/5,-4/5],[4/5,3/5]]','Orthogonal, determinant one, and every natural power orthogonal',[D+n for n in ['R345','R345_transpose','R345_orthogonal','R345_det','R345_pow_orthogonal']]),
 ('DT-05','No rational half-step, hence no Q-parameter group through R345','Any rational 2 x 2 matrix V with V*V = R345; any Q-parameter group of invertible rational 2 x 2 matrices','V commutes with R345, so V = [[p,-r],[r,p]] with p^2 = 4/5, which is not a rational square (den 5); therefore no Q-parameter group has R345 as its unit step',[D+n for n in ['four_fifths_den','nat_mul_self_ne_five','four_fifths_not_rat_square','no_rational_half_step','no_qparam_group_through_R345']]),
]
def collect():
    by={e['name']:e for e in load(B/'verification/kernel_axioms.json')['printed_receipts']};records=[]
    for id_,name,inputs,result,proofs in RECORDS:
        missing=[p for p in proofs if p not in by]
        if missing:raise RuntimeError('No receipt for '+', '.join(missing))
        records.append({'id':id_,'name':name,'inputs':inputs,'output_or_relation':result,'status':'KERNEL_CHECKED_TYPED_OPERATION','admissible_substitution':'Substitute only matching group/ring/matrix types and supply every displayed binder; no topology or continuum completion is available on the carrier.','proofs':[by[p] for p in proofs]})
    save(B/'operad_delta.json',{'schema_version':2,'namespace':'DT-DISCRETE-TIME','records':records,'formal_operad_claim':'Scoped typed operations with kernel-checked relations and exact receipts; no complete higher-arity operad is claimed.','authority_effect':'None'})
    print(json.dumps({'records':len(records),'proofs':sum(len(r['proofs']) for r in records)}))
if __name__=='__main__':collect()
