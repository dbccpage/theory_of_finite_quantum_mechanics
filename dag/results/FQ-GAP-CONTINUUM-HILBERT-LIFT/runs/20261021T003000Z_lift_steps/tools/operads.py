"""Collect scoped typed operation records from the kernel receipts of this run; every listed proof must have a receipt."""
from pathlib import Path
import json,sys
B=Path(__file__).resolve().parents[1]
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def save(p,v):Path(p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
H='HilbertLift.';O=H+'BoundedExactOperator.'
RECORDS=[
 ('HL-17','Intrinsic uniformity of the exact carrier','The exact carrier ℕ →₀ ℚ with the pullback uniformity along castSeq ℝ','the uniformity has the rational squared-distance balls as a basis and equals their infimum of principal filters; CauchySeq ↔ IsCauchyL2; castSeq ℝ and lift ℝ are uniform inducing; every rational ℓ²-Cauchy sequence converges in Completion Carrier',[H+n for n in ['isUniformInducing_castSeq_real','dist_castSeq_sq','uniformity_hasBasis_sqdist','uniformity_eq_iInf_sqdist','cauchySeq_iff_isCauchyL2','uniformContinuous_lift_real','isUniformInducing_lift_real','exists_limit_in_completion']]),
 ('HL-18','Completion of the exact carrier is the real Hilbert lift','Completion Carrier (intrinsic uniformity) and HilbertLiftSpace ℝ','completionToLift is uniform inducing, injective and surjective, giving the uniform isomorphism completionEquivLift that restricts to lift ℝ on exact vectors',[H+n for n in ['completionToLift_coe','isUniformInducing_completionToLift','completionToLift_injective','range_completionToLift','completionToLift_surjective','completionEquivLift_coe','completionEquivLift_symm_lift','intrinsic_completion']]),
 ('HL-19','Sequence model on the pre-Hilbert carrier','Finitely supported 𝕜-sequences and lp (fun _ => 𝕜) 2','the coordinate map is a linear isometry preserving the inner product, with dense range in ℓ²',[H+n for n in ['memℓp_coe','toL2_add','toL2_smul','inner_toL2','norm_toL2','denseRange_toL2']]),
 ('HL-20','The Hilbert lift is ℓ²(ℕ, 𝕜)','HilbertLiftSpace 𝕜','the extension of the coordinate map is a linear isometric equivalence onto ℓ² under which lift 𝕜 f is its own coordinate sequence',[H+n for n in ['liftToL2_coe','liftToL2_lift_apply','norm_liftToL2','liftToL2_add','liftToL2_smul','range_liftToL2','liftToL2_surjective','liftEquivL2_lift_apply','l2_model_summary']]),
 ('HL-21','Bounded exact operators lift to continuous linear operators','A ℚ-linear map A of the exact carrier with qinner (A f) (A f) ≤ C qinner f f','A is uniformly continuous, preserves rational ℓ²-Cauchy sequences, and extends uniquely to a continuous ℝ-linear operator on the real lift with ‖T x‖² ≤ C ‖x‖² and ‖T‖ ≤ √C',[O+n for n in ['sqdist_map_le','isCauchyL2_map','uniformContinuous_A','liftOp_lift','continuous_liftOp','liftOp_unique','norm_liftOp_sq_le','liftOp_add','liftOp_qsmul','liftOp_smul','toCLM_lift','norm_toCLM_le','opNorm_toCLM_le']]),
 ('HL-22','Stage projections and the unilateral shift','The exact projection onto report size n and the shift e_i ↦ e_{i+1}','both are bounded exact operators with bound 1; the projection lifts to liftFin ∘ trunc; the shift preserves qinner and lifts to an isometry of the real lift',[H+n for n in ['trunc_add','trunc_smul','proj_lift','qinner_shift','norm_shift_liftOp']]),
 ('HL-23','The coordinate-sum functional has no continuous extension','The ℚ-linear functional Σ_i f i and the harmonic witness','coordSum (harmonic 2n) − coordSum (harmonic n) ≥ 1/2 while qinner (harmonic N) (harmonic N) ≤ 2; no continuous real functional on the lift restricts to coordSum',[H+n for n in ['coordSum_add','coordSum_smul','coordSum_harmonic','coordSum_harmonic_gap','qinner_harmonic_le_two','no_continuous_extension_coordSum','operator_lift_summary']]),
]
def collect(extra=()):
    by={e['name']:e for e in load(B/'verification/kernel_axioms.json')['printed_receipts']};records=[]
    for id_,name,inputs,result,proofs in list(RECORDS)+list(extra):
        missing=[p for p in proofs if p not in by]
        if missing:raise RuntimeError('No receipt for '+', '.join(missing))
        records.append({'id':id_,'name':name,'inputs':inputs,'output_or_relation':result,'status':'KERNEL_CHECKED_TYPED_OPERATION','admissible_substitution':'Substitute only matching carrier types and supply every displayed binder; the scalar field 𝕜, the ℓ² uniformity and the operator bound C are hypotheses, not consequences of the exact carrier.','proofs':[by[p] for p in proofs]})
    save(B/'operad_delta.json',{'schema_version':2,'namespace':'HL-HILBERT-LIFT','records':records,'formal_operad_claim':'Scoped typed operations with kernel-checked relations and exact receipts; no complete higher-arity operad is claimed. Records HL-01 to HL-16 of runs/20261020T230000Z_completion are re-verified by the dependency receipts of this run but not re-listed.','authority_effect':'None'})
    print(json.dumps({'records':len(records),'proofs':sum(len(r['proofs']) for r in records)}))
if __name__=='__main__':
    extra=json.loads((B/'tools/operad_extra.json').read_text(encoding='utf-8')) if (B/'tools/operad_extra.json').is_file() else []
    collect([tuple(e) for e in extra])
