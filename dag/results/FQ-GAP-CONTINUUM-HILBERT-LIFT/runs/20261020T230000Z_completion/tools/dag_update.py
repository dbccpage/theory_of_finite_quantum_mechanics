"""Apply this run's record to the DAG node FQ-GAP-CONTINUUM-HILBERT-LIFT; status stays CONDITIONAL."""
from pathlib import Path
import json,sys
B=Path(__file__).resolve().parents[1]
ROOT=next(p for p in B.parents if (p/'lean4/lakefile.lean').is_file())
DAG=ROOT/'dag/derivation_dag.json'
RUN=B.relative_to(ROOT).as_posix()
NODE='FQ-GAP-CONTINUUM-HILBERT-LIFT'
def dump(d,ascii_):return json.dumps(d,indent=2,ensure_ascii=ascii_)+'\n'
def main():
    raw=DAG.read_bytes();crlf=b'\r\n' in raw;text=raw.decode('utf-8').replace('\r\n','\n');d=json.loads(text)
    ascii_=None
    for candidate in (False,True):
        if dump(d,candidate)==text:ascii_=candidate
    if ascii_ is None:raise RuntimeError('DAG serialization does not round-trip; refusing to rewrite the file')
    node=next(n for n in d['nodes'] if n['id']==NODE)
    node['source_status']=('Controlled completion kernel-checked in '+RUN+': the exact finite carriers Fin n -> Q form a tower under zero padding whose directed union N ->0 Q is exhausted by the finite stages (HilbertLiftFiniteTower: exhaustion, qinner_sq_le); the l2 Cauchy condition is stated with rational tolerances and the harmonic witness h_N = sum_{i<N} e_i/(i+1) is l2-Cauchy with the explicit modulus k -> k+1, is not l1-Cauchy, and converges to no exact vector (HilbertLiftRationalUniformity: harmonic_separates_uniformities); the Hausdorff completion of the pre-Hilbert carrier N ->0 k (k = R or C) is a complete inner product space into which the exact carrier embeds inner-product-preservingly, injectively and compatibly with padding, Cauchy-ness in the lift is exactly the rational l2 condition, every such sequence converges, and over R the exact carrier is dense, continuous maps out of the lift are determined on exact vectors, and the lift is strictly larger than the exact carrier (HilbertLiftCompletion: controlled_completion); over C the Gaussian-rational pairs a + ib are dense with the exact inner-product identity and the lift is strictly larger (HilbertLiftComplexCarrier: controlled_completion_complex). Exact replays: code/python/src/qm/hilbert_lift_completion.py (16 tests), code/rust/src/qm/hilbert_lift_completion.rs (14 inline tests). Earlier: Z[i] non-field obstruction (2*(a^2+b^2) != 1) and symmetric integer matrix M=[[2,1],[1,1]] characteristic discriminant 5 non-square obstruction in Q(i) mechanized in DerivationDagQMClosure.lean')
    new_lean=['lean4/HilbertLiftFiniteTower.lean::HilbertLift.exhaustion','lean4/HilbertLiftFiniteTower.lean::HilbertLift.qinner_sq_le','lean4/HilbertLiftRationalUniformity.lean::HilbertLift.harmonic_hasModulus','lean4/HilbertLiftRationalUniformity.lean::HilbertLift.harmonic_separates_uniformities','lean4/HilbertLiftCompletion.lean::HilbertLift.inner_lift','lean4/HilbertLiftCompletion.lean::HilbertLift.cauchySeq_lift_iff','lean4/HilbertLiftCompletion.lean::HilbertLift.exists_limit_of_isCauchyL2','lean4/HilbertLiftCompletion.lean::HilbertLift.denseRange_lift_real','lean4/HilbertLiftCompletion.lean::HilbertLift.lift_not_surjective','lean4/HilbertLiftCompletion.lean::HilbertLift.controlled_completion','lean4/HilbertLiftComplexCarrier.lean::HilbertLift.inner_liftPair','lean4/HilbertLiftComplexCarrier.lean::HilbertLift.denseRange_liftPair','lean4/HilbertLiftComplexCarrier.lean::HilbertLift.controlled_completion_complex']
    node['lean']=[r for r in node['lean'] if r not in new_lean]+new_lean
    new_rust=['code/rust/src/qm/hilbert_lift_completion.rs::harmonic_nonconvergence_bound_holds','code/rust/src/qm/hilbert_lift_completion.rs::modulus_holds','code/rust/src/qm/hilbert_lift_completion.rs::grid_approximation']
    node['rust']=[r for r in node['rust'] if r not in new_rust]+new_rust
    node['imported_structure']=['scalar field R or C, i.e. the completion of Q or of Q(i) (assumption; the lift is the Hausdorff completion of the finitely supported scalar sequences and nothing selects the field)','l2 uniformity on the exact carrier (assumption; harmonic_separates_uniformities shows that l1 is a different choice with a different Cauchy structure)','Cauchy convergence hypothesis: limits exist in the lift for rational-l2-Cauchy sequences of exact vectors and not on the exact carrier itself (harmonic_not_tendsTo)']
    node['bottleneck']=('The continuum Hilbert completion is now constructed with explicit embeddings (lift, liftFin, liftPair), explicit topology (rational l2 uniformity) and explicit convergence hypotheses (IsCauchyL2, HasModulusL2); what remains imported is the selection of the scalar field and of the l2 uniformity from finite-theory primitives, the lifting of operators and dynamics (FQ-GAP-STONE-CONTINUOUS-TIME), and the intrinsic identification Completion (N ->0 Q) with HilbertLiftSpace R (run next_steps.md). Z[i] non-field obstruction and discriminant-5 spectral exit from Q(i) remain mechanized.')
    out=dump(d,ascii_)
    DAG.write_bytes((out.replace('\n','\r\n') if crlf else out).encode('utf-8'))
    print(json.dumps({'node':NODE,'lean_refs':len(node['lean']),'rust_refs':len(node['rust']),'ensure_ascii':ascii_,'crlf':crlf}))
if __name__=='__main__':sys.exit(main())
