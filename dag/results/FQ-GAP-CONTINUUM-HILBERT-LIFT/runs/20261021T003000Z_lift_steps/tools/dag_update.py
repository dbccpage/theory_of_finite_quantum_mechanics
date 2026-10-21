"""Split the DAG record: add the construction node (PROVED_LEAN, hypotheses named) with its route, and
rewrite FQ-GAP-CONTINUUM-HILBERT-LIFT to the selection question that remains (status CONDITIONAL)."""
from pathlib import Path
import json,sys
B=Path(__file__).resolve().parents[1]
ROOT=next(p for p in B.parents if (p/'lean4/lakefile.lean').is_file())
DAG=ROOT/'dag/derivation_dag.json'
RUN=B.relative_to(ROOT).as_posix()
PRIOR='dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261020T230000Z_completion'
GAP='FQ-GAP-CONTINUUM-HILBERT-LIFT';NEW='FQ-CONTINUUM-HILBERT-LIFT-CONSTRUCTION'
def dump(d,ascii_):return json.dumps(d,indent=2,ensure_ascii=ascii_)+'\n'
def main():
    raw=DAG.read_bytes();crlf=b'\r\n' in raw;text=raw.decode('utf-8').replace('\r\n','\n');d=json.loads(text)
    ascii_=None
    for candidate in (False,True):
        if dump(d,candidate)==text:ascii_=candidate
    if ascii_ is None:raise RuntimeError('DAG serialization does not round-trip; refusing to rewrite the file')
    if any(n['id']==NEW for n in d['nodes']):raise RuntimeError('construction node already present')
    gap=next(n for n in d['nodes'] if n['id']==GAP)
    new={
     'id':NEW,'stage':'FINITE_QM_CORE','status':'PROVED_LEAN',
     'source_status':'Kernel-checked (Lean 4.33.1, pinned Mathlib cache) in '+PRIOR+' (four modules, 112 receipts) and '+RUN+' (three further modules; 168 receipts including the re-replayed dependencies); exact replays in code/python/src/qm/hilbert_lift_completion.py (20 tests, certificate row in test_isolated_certificates.py) and code/rust/src/qm/hilbert_lift_completion.rs (18 inline tests)',
     'statement':'With the scalar field k in {R, C} and the l2 uniformity supplied as named hypotheses: the exact finite carriers Fin n -> Q form a tower under zero padding whose directed union N ->0 Q is exhausted by the finite stages; the Hausdorff completion of N ->0 k is a complete inner product space into which the exact carrier embeds inner-product-preservingly, injectively and padding-compatibly (lift, liftFin); a sequence of exact vectors is Cauchy in the lift exactly when it is rational-l2-Cauchy, and every such sequence converges; over R the exact carrier is dense, continuous maps out of the lift are determined on exact vectors, and the lift is strictly larger than the carrier; over C the Gaussian-rational pairs a + ib are dense with the exact inner-product identity; the completion of the exact carrier under its intrinsic rational uniformity (the infimum of the rational sqdist-ball filters) is uniformly isomorphic to the real lift; the lift is linearly isometric to l2(N, k) with exact vectors as their coordinate sequences; every Q-linear map of the exact carrier with a rational quadratic bound C lifts uniquely to a continuous linear operator of norm at most sqrt(C) (the shift lifts to an isometry), and the Q-linear coordinate-sum functional admits no continuous extension.',
     'source':[PRIOR+'/README.md',PRIOR+'/review.md',RUN+'/README.md',RUN+'/review.md'],
     'lean':['lean4/HilbertLiftFiniteTower.lean::HilbertLift.exhaustion','lean4/HilbertLiftRationalUniformity.lean::HilbertLift.harmonic_separates_uniformities','lean4/HilbertLiftCompletion.lean::HilbertLift.controlled_completion','lean4/HilbertLiftComplexCarrier.lean::HilbertLift.controlled_completion_complex','lean4/HilbertLiftIntrinsicUniformity.lean::HilbertLift.uniformity_eq_iInf_sqdist','lean4/HilbertLiftIntrinsicUniformity.lean::HilbertLift.intrinsic_completion','lean4/HilbertLiftL2Model.lean::HilbertLift.l2_model_summary','lean4/HilbertLiftOperators.lean::HilbertLift.operator_lift_summary','lean4/HilbertLiftOperators.lean::HilbertLift.no_continuous_extension_coordSum'],
     'rust':['code/rust/src/qm/hilbert_lift_completion.rs::modulus_holds','code/rust/src/qm/hilbert_lift_completion.rs::shift_is_isometric','code/rust/src/qm/hilbert_lift_completion.rs::coord_sum_gap','code/rust/src/qm/hilbert_lift_completion.rs::certify'],
     'imported_structure':['scalar field R or C, i.e. the completion of Q or of Q(i) (assumption)','l2 uniformity on the exact carrier (assumption; harmonic_separates_uniformities shows that l1 is a different choice)'],
     'bottleneck':'Both hypotheses are supplied; their selection from finite-theory primitives is the content of '+GAP+'. Dynamics and generators are not lifted (FQ-GAP-STONE-CONTINUOUS-TIME); the bound C on an exact operator is a hypothesis.',
     'tags':['cross-ref:'+GAP+' construction half'],
     'see_also':[GAP,'GP-IMPORT-CONTINUUM-HILBERT']}
    idx=d['nodes'].index(gap);d['nodes'].insert(idx+1,new)
    gap['statement']=gap['statement']+' Construction half (split 2026-10-21): '+NEW+' records the completion once the scalar field and the l2 uniformity are supplied; this node keeps the selection of those two hypotheses, which no source derives.'
    gap['source_status']='Split on 2026-10-21: the construction (completion, embeddings, l2 model, intrinsic-uniformity completion, bounded operator lift) is recorded at '+NEW+' (PROVED_LEAN with named hypotheses) from '+PRIOR+' and '+RUN+'; this node keeps the selection question. Earlier record: '+gap['source_status']
    gap['bottleneck']='What remains at this node is the selection of the scalar field (R or C) and of the l2 uniformity from finite-theory primitives, which no source derives; the construction, the identification with l2(N, k), the intrinsic-uniformity completion and the lifting of bounded exact operators are recorded at '+NEW+'; dynamics and generators remain at FQ-GAP-STONE-CONTINUOUS-TIME. Z[i] non-field obstruction and discriminant-5 spectral exit from Q(i) remain mechanized.'
    if NEW not in gap['see_also']:gap['see_also'].append(NEW)
    for ref in ['lean4/HilbertLiftIntrinsicUniformity.lean::HilbertLift.intrinsic_completion','lean4/HilbertLiftL2Model.lean::HilbertLift.l2_model_summary','lean4/HilbertLiftOperators.lean::HilbertLift.operator_lift_summary']:
        if ref not in gap['lean']:gap['lean'].append(ref)
    routes=d['routes']
    if any(r['id']=='FQ-R-CONTINUUM-HILBERT-LIFT-CONSTRUCTION' for r in routes):raise RuntimeError('route already present')
    routes.append({'id':'FQ-R-CONTINUUM-HILBERT-LIFT-CONSTRUCTION','inputs':['FQ-CARRIER-CONTRACT-V2'],'output':NEW,'status':'CONDITIONAL_ON_IMPORT','source':[PRIOR+'/README.md',RUN+'/README.md','lean4/HilbertLiftCompletion.lean','lean4/HilbertLiftOperators.lean']})
    routes.append({'id':'FQ-R-GAP-CONTINUUM-FROM-CONSTRUCTION','inputs':[NEW],'output':GAP,'status':'GAP_NO_DERIVATION','mechanism':'Select the scalar field and the l2 uniformity from finite-theory primitives; the construction node supplies the completion once they are chosen.','source':[]})
    out=dump(d,ascii_)
    DAG.write_bytes((out.replace('\n','\r\n') if crlf else out).encode('utf-8'))
    print(json.dumps({'nodes':len(d['nodes']),'routes':len(routes),'new_node':NEW,'ensure_ascii':ascii_,'crlf':crlf}))
if __name__=='__main__':sys.exit(main())
