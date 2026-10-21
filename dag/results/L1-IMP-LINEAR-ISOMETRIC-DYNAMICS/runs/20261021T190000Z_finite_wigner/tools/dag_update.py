"""Record this run on the DAG: rewrite the node L1-IMP-LINEAR-ISOMETRIC-DYNAMICS (IMPORTED_ASSUMPTION -> CONDITIONAL), add the imported node L1-IMP-TRANSITION-PROBABILITY-LAW for the operational hypothesis, and add the conditional route L1-R-DYNAMICS-FINITE-WIGNER beside the retained gap route; bytes are written with LF line endings. Run once on the pre-run DAG, then dag/sync_unified_dag.py, dag/sync_application_branches.py and dag/sync_pregenesis_to_wdp.py."""
from pathlib import Path
import json
B=Path(__file__).resolve().parents[1]
ROOT=next(p for p in B.parents if (p/'lean4/lakefile.lean').is_file())
DAG=ROOT/'dag/derivation_dag.json'
RUN='dag/results/L1-IMP-LINEAR-ISOMETRIC-DYNAMICS/runs/20261021T190000Z_finite_wigner'
K='lean4/FiniteWignerKernel.lean::WignerFable.Kernel.'
T='lean4/FiniteWignerTheorem.lean::WignerFable.Theorem.'
S='lean4/FiniteWignerSimilarity.lean::WignerFable.Similarity.'
A='lean4/GaussRatAutomorphisms.lean::WignerFable.GaussRatAut.'
RS='code/rust/src/qm/finite_wigner.rs::'
def add(lst,items):
    for x in items:
        if x not in lst:lst.append(x)
def main():
    raw=DAG.read_bytes();assert b'\r\n' not in raw,'DAG is expected to use LF line endings'
    d=json.loads(raw.decode('utf-8'));nodes={n['id']:n for n in d['nodes']};routes={r['id']:r for r in d['routes']}
    nd=nodes['L1-IMP-LINEAR-ISOMETRIC-DYNAMICS']
    assert nd['status']=='IMPORTED_ASSUMPTION' and 'L1-IMP-TRANSITION-PROBABILITY-LAW' not in nodes and 'L1-R-DYNAMICS-FINITE-WIGNER' not in routes,'already updated'
    # --- the dynamics node: linear (or conjugate-linear) similarity dynamics derived from transition-probability preservation
    nd['status']='CONDITIONAL'
    nd['source_status']=('Finite exact Wigner theorem kernel-checked in '+RUN+' (Lean 4.35.0): a map of the exact Born carrier Q(i)^n that sends nonzero vectors to nonzero vectors and preserves the transition probability tp x y = |<x,y>|^2/(|x|^2 |y|^2) (the normalised Born readout of rank-one effects, Kernel.tp_eq_born) is induced on rays by a Q(i)-linear similarity F^H F = d * 1 with a positive rational scale d, composed with the identity or with componentwise conjugation (Theorem.finite_wigner, finite_wigner_cases); the converse holds (tpPreserving_of_similarity) and the induced map is a bijection with inverse (1/d) F^H (similarity_bijective, Kernel.Similarity.inverse), so the dynamics is reversible and linear or antilinear, and no continuity hypothesis is used. The scale is removable (F = c * U with U unitary) iff d is a sum of two rational squares (Similarity.exists_unitary_iff); the countermodel F3 = [[1, -1+i], [1+i, 1]] with F3^H F3 = 3 * 1 preserves transition probabilities but is induced by no Q(i)-unitary and no Q(i)-antiunitary (F3_not_induced_by_unitary, F3_not_induced_by_antiunitary, three_not_sum_two_sq), so over the exact carrier the honest statement is similarity, not unitarity. The H006 permutation envelope is the unitary permMatrix (permMatrix_unitary). Aut Q(i) = {id, conjugation} (GaussRatAut.ringHom_eq_id_or_star). Exact replays: code/python/src/qm/finite_wigner.py (24 tests, see the run README) and code/rust/src/qm/finite_wigner.rs (29 tests). Earlier: '+nd['source_status'])
    nd['statement']=('Derived part ('+RUN+'): on the exact Born carrier Q(i)^n with the inner product fixed up to scale by the sector-form run, every ray map preserving Born transition probabilities between rays is induced by a Q(i)-linear similarity (F^H F = d * 1, d > 0) or by conjugation followed by one; the map is invertible, so the dynamics is reversible and linear or antilinear, isometric up to the positive scale d, with no continuity hypothesis. The scale is a unit choice only when d is a norm from Q(i): the scale-3 countermodel F3 preserves transition probabilities yet is no unitary nor antiunitary ray map, so the imported form "reversible linear isometries" is strictly stronger than what the finite carrier supports; the finite statement is "reversible linear or antilinear similarities". Imported part: that the dynamics acts on the rays of the lift and preserves the Born transition probabilities (node L1-IMP-TRANSITION-PROBABILITY-LAW); the carrier, the scalar field Q(i) and the quadratic readout. QM_122 H003 still shows that deterministic report dynamics do not by themselves give reversibility, and H006 supplies the permutation envelope, now a special (unitary) case.')
    nd['bottleneck']='Transition-probability preservation of the ray dynamics is supplied as an operational law (node L1-IMP-TRANSITION-PROBABILITY-LAW), not derived from primitive difference; the carrier, the scalar field and the quadratic readout remain imports; the similarity scale is a norm from Q(i) only under an extra arithmetic condition, and continuous time remains the Stone gap. The earlier Lean references under lean4/quantum_mechanics/ are retained as source annotations.'
    add(nd['lean'],[K+n for n in ['tp','tp_eq_born','eq_smul_of_normSq_ip_eq','Similarity','expansion']]+[T+n for n in ['TpPreserving','finite_wigner','finite_wigner_cases','tpPreserving_of_similarity','similarity_bijective','coord_rigidity','sgn_consistent']]+[S+n for n in ['exists_unitary_iff','three_not_sum_two_sq','F3_similarity','F3_tpPreserving','F3_not_induced_by_unitary','F3_not_induced_by_antiunitary','permMatrix_unitary','tpPreserving_iff_born']]+[A+'ringHom_eq_id_or_star'])
    add(nd.setdefault('rust',[]),[RS+'reconstruct',RS+'similarity_certificate',RS+'unitary_normalisation',RS+'f3'])
    nd['imported_structure']=['ray dynamics preserving Born transition probabilities: assumption (node L1-IMP-TRANSITION-PROBABILITY-LAW)','sector carrier, scalar field Q(i) and quadratic readout: assumption','unitarity (scale a norm from Q(i)): extra arithmetic condition, not derived (countermodel F3)']
    nd['tags']=[t for t in nd.get('tags',[]) if t not in ('gap','lean-ref-unverified')]+['conditional-on-readout-laws','finite-wigner']
    nd.setdefault('source',[]).append(RUN+'/README.md')
    # --- the operational law as a node of its own
    law={'id':'L1-IMP-TRANSITION-PROBABILITY-LAW','stage':'L1_TO_L2','status':'IMPORTED_ASSUMPTION',
     'source_status':'Supplied law of the ray dynamics in '+RUN+': the dynamics sends nonzero vectors of the exact carrier Q(i)^n to nonzero vectors and preserves the transition probability tp x y = |<x,y>|^2/(|x|^2|y|^2) between nonzero vectors (Theorem.TpPreserving), equivalently the normalised Born readout hf (P x) y / vnorm y of rank-one effects (Similarity.tpPreserving_iff_born, Kernel.tp_eq_born). Nothing in the finite theory forces a dynamics to preserve this readout; it is the operational hypothesis of the Wigner theorem.',
     'statement':'Transition-probability preservation of the ray dynamics: the evolution of rays of the lift preserves the Born probability of every rank-one effect in every state. Under this law the dynamics is a linear or conjugate-linear similarity (L1-IMP-LINEAR-ISOMETRIC-DYNAMICS); without it, any bijection of rays is admissible. Supplied, not derived from primitive difference.',
     'source':[RUN+'/README.md',RUN+'/review.md','lean4/FiniteWignerTheorem.lean'],
     'lean':[T+'TpPreserving',K+'tp',K+'tp_eq_born',S+'tpPreserving_iff_born',T+'tpPreserving_of_similarity'],
     'rust':[RS+'transition_probability',RS+'born_transition',RS+'verify_induced'],
     'imported_structure':['transition-probability (Born rank-one readout) preservation by the ray dynamics: assumption'],
     'bottleneck':'No finite-theory primitive forces the ray dynamics to preserve the Born readout of rank-one effects; deriving it (for instance from report relabelling invariance and the Born rule on the lift) is item 1 of the run next steps.',
     'tags':['gap','readout-law']}
    d['nodes'].insert(d['nodes'].index(nd)+1,law)
    # --- the conditional route beside the retained gap route L1-R-DYNAMICS-GAP
    new={'id':'L1-R-DYNAMICS-FINITE-WIGNER','inputs':['L1-IMP-HILBERT-INNER-PRODUCT','L1-IMP-TRANSITION-PROBABILITY-LAW'],'output':'L1-IMP-LINEAR-ISOMETRIC-DYNAMICS','status':'CONDITIONAL_ON_IMPORT','source':[RUN+'/README.md','lean4/FiniteWignerKernel.lean','lean4/FiniteWignerTheorem.lean','lean4/FiniteWignerSimilarity.lean'],'note':'Holds once the inner product is fixed up to scale (L1-IMP-HILBERT-INNER-PRODUCT, whose scale the transition probability does not see) and the ray dynamics preserves Born transition probabilities (L1-IMP-TRANSITION-PROBABILITY-LAW): the dynamics is then a reversible Q(i)-linear or conjugate-linear similarity with positive rational scale, unitary iff the scale is a sum of two rational squares (countermodel F3 with scale 3). No continuity is used.'}
    first_app=next((i for i,r in enumerate(d['routes']) if r['id'].startswith('APP-R-')),len(d['routes']))
    d['routes'].insert(first_app,new)  # application-branch routes stay last (dag/sync_application_branches.py)
    DAG.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode('utf-8'))
    print(json.dumps({'nodes':len(d['nodes']),'routes':len(d['routes']),'updated':['L1-IMP-LINEAR-ISOMETRIC-DYNAMICS'],'added_nodes':['L1-IMP-TRANSITION-PROBABILITY-LAW'],'added_routes':['L1-R-DYNAMICS-FINITE-WIGNER']}))
if __name__=='__main__':main()
