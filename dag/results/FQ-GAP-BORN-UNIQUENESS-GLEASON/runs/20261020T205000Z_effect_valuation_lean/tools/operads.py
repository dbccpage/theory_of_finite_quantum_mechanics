"""Collect scoped typed operation records from the kernel receipts of this run; every listed proof must have a receipt."""
from pathlib import Path
import json,sys
B=Path(__file__).resolve().parents[1]
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def save(p,v):Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
F='BornFable.';O=F+'OrderedQUnit.';M=F+'MatrixCarrier.';R=F+'RationalSphere.';D=F+'PsdDecomposition.'
RECORDS=[
 ('EV-01','Order helpers of an ordered rational unit','OrderedQUnit V with its four order axioms','Difference form of the order, closure under addition, scaling and negation',[O+n for n in ['le_iff_sub_nonneg','add_nonneg','smul_le_smul','neg_le_neg']]),
 ('EV-02','Elementary laws of an effect valuation','EffectValuation S; effects a, b with the stated order relations','v 0 = 0, difference effects, monotonicity, v ≤ 1, scaled effects',[F+n for n in ['val_zero','effect_sub','val_mono','val_le_one','effect_smul']]),
 ('EV-03','Rational homogeneity on effects (the first missing lemma of run 20261020T004525Z_fable51_born)','Effect a, natural k with k • a an effect, or rational q in [0,1]','v (k • a) = k v a and v (q • a) = q v a from additivity alone',[F+'val_nsmul',F+'val_rat_smul']),
 ('EV-04','Quantitative comparison','Effects a, b with -(ε • u) ≤ a - b ≤ ε • u','|v a - v b| ≤ ε',[F+'val_sub_le_of_le',F+'val_sandwich']),
 ('EV-05','Bounded elements and the midpoint effect','Element a with -(t • u) ≤ a ≤ t • u, t > 0','(1/(2t)) • (a + t • u) is an effect; bounds are monotone and additive',[O+n for n in ['bounded_mono','bounded_add','bounded_of_effect','midpoint_effect']]),
 ('EV-06','Extension value independent of the admissible bound','Valuation W; bounds s, t > 0 for a (and b)','extAt is additive on a common bound and constant across bounds',[O+n for n in ['extAt_add','extAt_mono','extAt_eq']]),
 ('EV-07','Unique positive unital ℚ-linear extension','Order unit (IsOrderUnit) and an effect valuation','ℚ-linear functional agreeing with W on effects, positive, unital, unique',[O+n for n in ['bound_pos','bounded_bound','extend_eq_extAt','extend_add','extend_effect','extend_nonneg','extend_u','extendₗ_apply','extendₗ_effect','extendₗ_nonneg','extendₗ_u','extend_unique','linear_extension']]),
 ('EV-08','Rational matrix carrier with the quadratic-form preorder','Rational n×n matrices (symmetry not required); unit = identity','OrderedQUnit instance; effects are 0 ≤ qf E x ≤ x ⬝ x; the order is a preorder only',[M+n for n in ['qf','qf_add','qf_sub','qf_neg','qf_smul','qf_zero','qf_one','qf_eq_sum_sum','dot_self_nonneg','dot_self_pos','dot_self_eq_sum_sq','PsdQ','space','space_le','space_u','effect_iff',"effect_iff'"]]),
 ('EV-09','Order-unit bound on rational matrices','Any rational matrix A','|qf A x| ≤ (∑|A i j|) (x ⬝ x); natural bound k with -(k • 1) ≤ A ≤ k • 1',[M+n for n in ['sq_le_dot','abs_mul_le_dot','abs_qf_le','order_unit']]),
 ('EV-10','Rank-one effects','Nonzero rational vector x','P x = (1/(x ⬝ x)) • x xᵀ is an effect (Cauchy–Schwarz over ℚ)',[M+n for n in ['cauchy_schwarz','P','qf_vecMulVec','qf_rankOne','rankOne_effect']]),
 ('EV-11','Trace representation of ℚ-linear functionals on matrices','ℚ-linear L on rational n×n matrices','L A = trace (repMatrix L * A); the representing matrix is unique; qf ρ x = trace (ρ * x xᵀ); skew matrices are null in the preorder',[M+n for n in ['repMatrix','repMatrix_apply','trace_mul_eq_sum','trace_rep','rep_unique','qf_eq_trace',"qf_eq_trace'",'qf_eq_zero_of_skew','skew_le_zero_and_ge']]),
 ('EV-12','Born representation theorem','Effect valuation W on rational n×n matrices','Unique ρ with W.v E = trace (ρ * E) on effects; ρ symmetric, PSD over ℚ, trace one; v (P x) = ⟨x, ρ x⟩ / ⟨x, x⟩',[M+n for n in ['space_isOrderUnit','ext_effect','ext_one','ext_nonneg','ext_eq_trace','density_effect','density_trace','density_psd','single_transpose_eq','ext_skew_zero','density_symm','traceWith_apply','density_unique','born_representation','density_is_state','born_rule']]),
 ('EV-13','Converse and nonvacuity','Matrix ρ positive on effects with trace one; the pure state e₀','E ↦ trace (ρ * E) is an effect valuation with density ρ; pureZero exists in every dimension n+1',[M+n for n in ['ofState_density','trace_single_zero_mul','apply_zero_zero_eq_qf','pureZero_apply','pureZero_density']]),
 ('EV-14','Parity frame function on rational rays of S²','Integer triples, not all even, with square norm; orthogonal triples','Exactly one odd coordinate per ray; odd positions differ across orthogonal rays; parity sums to 1 on every orthogonal triple; two-valued; invariant under odd scalings',[R+n for n in ['sq_emod_eight','ray_exactly_one_odd','mul_emod_two_eq_one','orthogonal_rays_odd_positions_differ','parity_frame_function','parity_two_valued','parity_odd_smul','ray_e1','ray_e2','ray_e3','ray_340','ray_034','ray_043']]),
 ('EV-15','No quadratic form reproduces the parity frame function','Six explicit rays','The six evaluation equations for a rational quadratic form are inconsistent',[R+'parity_not_quadratic']),
]
def collect(extra=()):
    by={e['name']:e for e in load(B/'verification/kernel_axioms.json')['printed_receipts']};records=[]
    for id_,name,inputs,result,proofs in list(RECORDS)+list(extra):
        missing=[p for p in proofs if p not in by]
        if missing:raise RuntimeError('No receipt for '+', '.join(missing))
        records.append({'id':id_,'name':name,'inputs':inputs,'output_or_relation':result,'status':'KERNEL_CHECKED_TYPED_OPERATION','admissible_substitution':'Substitute only matching carrier types and supply every displayed binder; the matrix order is a preorder, not a partial order.','proofs':[by[p] for p in proofs]})
    save(B/'operad_delta.json',{'schema_version':2,'namespace':'EV-EFFECT-VALUATION','records':records,'formal_operad_claim':'Scoped typed operations with kernel-checked relations and exact receipts; no complete higher-arity operad is claimed.','authority_effect':'None'})
    print(json.dumps({'records':len(records),'proofs':sum(len(r['proofs']) for r in records)}))
if __name__=='__main__':
    extra=json.loads((B/'tools/operad_extra.json').read_text(encoding='utf-8')) if (B/'tools/operad_extra.json').is_file() else []
    collect([tuple(e) for e in extra])
