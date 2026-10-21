"""Build specs/L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED.json from the producer and the node's reviewed claims."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp/batch_tools'))
from spec_builder import build_spec, write_spec  # noqa: E402

_s = importlib.util.spec_from_file_location('producer', ROOT / 'code/python/src/qm/pfp_residual_sector_weights.py')
producer = importlib.util.module_from_spec(_s)
_s.loader.exec_module(producer)

NODE = 'L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED'
H = ('Edge cochains on the n-cycle with unweighted L1 form; the class of c in C^1/im d0 is its holonomy S = sum c; '
     'sectors are blocks of consecutive edges; sector weights are sums of |r_i| over a block.')
LEAN = 'lean4/ResidualSectorWeights.lean'
DQ = 'lean4/DerivationDagQMClosure.lean'


def jsonable(cases):
    return [list(c) for c in cases]


def spec():
    boundary = {
        'supports': ('On the n-cycle with the unweighted (equal edge mass) L1 form (kernel-checked for every n, every cochain c, over every commutative linearly ordered ring incl. Int and Rat): '
                     'the class of c in C^1/im d0 is determined by the holonomy S = sum c; Phi1(c) = min_h L1(c - d0 h) = |S| and is attained; the minimizers are exactly the cochains with sum S '
                     'all of whose entries have the sign of S (a scaled simplex); for n >= 2 and S != 0 two minimizers share Phi1 and the holonomy S but differ as residuals and in the weights of any bipartition into two nonempty sectors, '
                     'so the sector weights are NOT a function of (Phi1, Gamma2), where Gamma2 is MODELLED as the holonomy (class invariant) as in the TFQ-0354 M1 syndrome; the repo PUB-009 witness uses Gamma_2 = sum w_i^2, '
                     'and under that reading the minimizers do not even share Gamma2 (native: sum of squares ranges from sumsq_min to sumsq_max, e.g. 2 to 4 for the class (1,0,1,0)), but that reading is not a Lean anchor; '
                     'the weights of the two sectors always add up to Phi1; S = 0 forces the zero residual (total mass 0, refused by the node) and n = 1 has a unique minimizer; '
                     'the cyclically invariant minimizer exists and is unique over a field (constant S/n) and is integral iff n divides S, so it is a separate declared selector. '
                     'Native (exact enumeration, not kernel theorems): 16 unweighted cases incl. S = 0, S < 0, n = 1 and a single sector; 6 WEIGHTED cases with declared integer masses showing that the minimizer lives on the minimal-mass edges '
                     '(unique when the minimum is attained once, so the sector weights can then be determined by the declared masses, and determined-but-not-unique when all minimal edges share a sector); '
                     'and 4 two-disjoint-cycle cases (cycle rank 2) where one total holonomy does not determine Phi1.'),
        'does_not_support': ('Any derivation of declared sector weights from Phi1 and Gamma2 in the setting of the node source: the result is specific to EQUAL edge masses; for a weighted L1 form with a unique minimal-mass edge the minimizer, '
                             'hence the sector weights, are unique (native weighted rows), so non-derivability can fail in the weighted setting that the node source declares (the masses are then the declared input); '
                             'a Lean proof of the weighted statement or of the sum-of-squares reading of Gamma2; connected graphs of cycle rank > 1 (only two DISJOINT cycles are tabulated natively); the Hilbert lift, density matrices or any physical reading of the weights; '
                             'that the dihedral or cyclic symmetry is itself available (it is an extra declared input).'),
        'narrowest_claim': ('For the n-cycle with the unweighted L1 form, the set of minimizing residuals is the scaled simplex of sign-definite cochains with sum S (minimizer_iff); the sector weights are its block sums, which are not a function of (Phi1, Gamma2 = holonomy) '
                            'for n >= 2, S != 0 and at least two sectors (sector_weights_not_determined), because (Phi1, Gamma2) determine only the signed holonomy S (hence Phi1 = |S| and the sign pattern); any single choice, including the cyclically symmetric average S/n, is an extra declaration, '
                            'and with unequal declared masses the minimizer concentrates on the minimal-mass edges (native rows) so the masses themselves are the declared input.'),
        'next_test': ('Prove in the kernel that for the weighted form sum_i m_i |r_i| with declared positive edge masses the minimizers on the n-cycle are exactly the sign-definite cochains of holonomy S supported on the edges of minimal mass, so that the weights are unique iff the minimal mass is attained once.')}
    gens = [
        {'id': 'edge_residual_l1', 'source_declarations': [DQ + '::edgeResidualL1 (line 74): definition, the L1 sum of a List Nat of edge residuals; it is the L1 of a GIVEN nonnegative residual, not the minimum over a class'],
         'ordered_inputs': ['EdgeCochain'], 'output': 'Weight', 'semantic_predicate': 'l1 r = sum |r_i|.', 'hypotheses': [H]},
        {'id': 'class_holonomy', 'source_declarations': ['no source declaration; new definition ResidualSectorWeights.hol (the class invariant of C^1/im d0 on the n-cycle)'],
         'ordered_inputs': ['EdgeCochain'], 'output': 'SignedWeight', 'semantic_predicate': 'hol c = sum c; two cochains are in one class iff their holonomies agree (class_iff).', 'hypotheses': [H]},
        {'id': 'phi1_quotient_min', 'source_declarations': ['no source declaration for the minimum over the class; the source uses edgeResidualL1 of a fixed residual (line 74)'],
         'ordered_inputs': ['EdgeCochain'], 'output': 'Weight', 'semantic_predicate': 'Phi1 c = min over h of l1 (c - d0 h) = |hol c| (phi1_attained_and_lower_bound).', 'hypotheses': [H]},
        {'id': 'minimizer_set', 'source_declarations': [DQ + '::c4MinimizerOne (line 106), c4MinimizerTwo (line 112), even_cycle_sector_weights_require_selector (line 118): FIXED C4 INSTANCES proved by decide'],
         'ordered_inputs': ['EdgeCochain'], 'output': 'ResidualSet', 'semantic_predicate': 'All r in the class of c with l1 r = Phi1 c: sum = S, entries of the sign of S (minimizer_iff).', 'hypotheses': [H]},
        {'id': 'sector_weights', 'source_declarations': [DQ + '::sector_weights_sum_to_phi1 (line 98): general theorem, but only additivity of the list sum over append for List Nat'],
         'ordered_inputs': ['Residual', 'SectorSizes'], 'output': 'SectorWeightVector', 'semantic_predicate': 'Block sums of |r_i|; they add up to l1 r.', 'hypotheses': [H]},
        {'id': 'symmetric_average', 'source_declarations': [DQ + '::c4Rep1/c4Rep2/c4OrbitSum/c4Shift (lines 867-870), l1_even_cycle_symmetry_orbit_canonical_sector_weights (line 874): FIXED C4 INSTANCE by decide; the orbit SUM (1,1,1,1) has total 4 = 2 * Phi1',
                                 DQ + '::l1_qm020_c10_branch_pinching_and_residual_sector_orbit_closure (line 1428): second conjunct is the general arithmetic w0=w1=w2=w3 and total 4m imply w0=m'],
         'ordered_inputs': ['EdgeCochain'], 'output': 'Residual', 'semantic_predicate': 'The rotation-invariant minimizer, constant |S|/n (symmetric_selector); integral iff n divides S.', 'hypotheses': [H, 'The rotation symmetry is a declared extra input.']}]
    rels = [
        {'id': 'class_iff_holonomy', 'source_declarations': ['no source declaration; new general theorem class_iff / exists_d0_of_hol_zero'],
         'equation_or_predicate': 'r in class(c) iff hol r = hol c; im d0 = {hol = 0}', 'typing_conditions': 'EdgeCochain over a commutative linearly ordered ring', 'evidence_status': 'Kernel theorems class_iff, exists_d0_of_hol_zero; native enumeration sees one holonomy per class', 'scope': 'every n, every cochain'},
        {'id': 'phi1_equals_abs_holonomy', 'source_declarations': ['no source declaration; the source Phi1 is the L1 of a fixed residual (edgeResidualL1 line 74)'],
         'equation_or_predicate': 'min_h l1(c - d0 h) = |hol c|, attained', 'typing_conditions': 'EdgeCochain', 'evidence_status': 'Kernel theorem phi1_attained_and_lower_bound; native box minimum', 'scope': 'every n, every cochain'},
        {'id': 'minimizers_are_signed_simplex', 'source_declarations': [DQ + '::even_cycle_sector_weights_require_selector (line 118): fixed C4 instance, two single-edge residuals with sum 1'],
         'equation_or_predicate': 'IsMin c r iff hol r = hol c and all entries of r have the sign of hol c', 'typing_conditions': 'EdgeCochain', 'evidence_status': 'Kernel theorem minimizer_iff; native minimizer counts C(|S|+n-1, n-1)', 'scope': 'every n, every cochain'},
        {'id': 'sector_weights_not_determined', 'source_declarations': [DQ + '::l1_residual_sector_weights_minimizer_nonuniqueness_and_dihedral_selector (line 1648): fixed rA=(1,1,0,0), rB=(0,0,1,1) with sum 2, plus the conjunct (w0+w1>0 -> w0+w1 = w0+w1 and (w0>0 or w1>0)) which is trivially true and uses no minimizer'],
         'equation_or_predicate': 'n >= 2, hol c != 0, two nonempty sectors => exist minimizers with equal Phi1 and Gamma2 and different sector weights', 'typing_conditions': 'EdgeCochain, a bipartition of the edges', 'evidence_status': 'Kernel theorems minimizers_not_unique, sector_weights_not_determined; native sector-vector tables', 'scope': 'every n >= 2, every c with hol != 0'},
        {'id': 'sector_weights_add_to_phi1', 'source_declarations': [DQ + '::sector_weights_sum_to_phi1 (line 98): general theorem for List Nat append, no minimizer involved'],
         'equation_or_predicate': 'for a minimizer r and any bipartition, the two sector weights add up to Phi1', 'typing_conditions': 'Residual, Finset of edges', 'evidence_status': 'Kernel theorem sector_weights_sum_to_phi1; native sector vectors sum to phi1', 'scope': 'every minimizer'},
        {'id': 'zero_mass_and_single_edge_boundaries', 'source_declarations': [LEAN + '; BornRedundancy.lean::listSum_normalize (needs listSum w != 0), normalize (line 43)'],
         'equation_or_predicate': 'hol c = 0 implies the unique minimizer is 0 (M = 0); n = 1 implies a unique minimizer', 'typing_conditions': 'EdgeCochain', 'evidence_status': 'Kernel theorems minimizer_unique_of_hol_zero, minimizer_unique_of_one_edge; native records', 'scope': 'every c with hol = 0; every c on 1 edge'},
        {'id': 'symmetric_selector', 'source_declarations': [DQ + '::l1_even_cycle_symmetry_orbit_canonical_sector_weights (line 874): fixed C4 instance; BornRedundancy.lean::normalize (line 43) for the later normalization by M'],
         'equation_or_predicate': 'the rotation-invariant minimizer is unique and equals |S|/n on every edge; over Int it exists iff n divides S', 'typing_conditions': 'EdgeCochain over a field / Int', 'evidence_status': 'Kernel theorems symmetric_selector, symmetric_integral_iff, c4_orbit_sum_not_minimizer; native symmetric fractions', 'scope': 'every n >= 1, every c'}]
    comps = [
        {'outer_operation': 'sector_weights', 'input_slot': 0, 'inner_operation': 'minimizer_set', 'colour_match': 'ResidualSet element -> Residual', 'hypothesis_match': 'A minimizer is chosen explicitly; the choice is not an operation of the quotient.',
         'licensing_relations': ['sector_weights_add_to_phi1'], 'evidence_status': 'Kernel and native'},
        {'outer_operation': 'minimizer_set', 'input_slot': 0, 'inner_operation': 'phi1_quotient_min', 'colour_match': 'EdgeCochain -> Weight', 'hypothesis_match': 'The minimizing level is Phi1 c.',
         'licensing_relations': ['phi1_equals_abs_holonomy', 'minimizers_are_signed_simplex'], 'evidence_status': 'Kernel and native'}]
    failed = [
        {'composition': 'sector_weights o minimizer_set factored through (phi1_quotient_min, class_holonomy)', 'reason': 'No function of (Phi1, Gamma2) returns the sector weights when n >= 2, S != 0 and there are two nonempty sectors (kernel sector_weights_not_determined); it factors when S = 0 (zero residual, mass 0 refused) or for a single sector.'},
        {'composition': 'symmetric_average o minimizer_set over Int cochains', 'reason': 'The rotation-invariant minimizer exists over Int only when n divides S (kernel symmetric_integral_iff); the source orbit sum (1,1,1,1) is not a minimizer of the class of (1,0,1,0).'}]
    counter = [
        {'id': 'c4_two_minimizers', 'statement': 'On the 4-cycle the cochains (1,0,1,0) and (0,1,0,1) (holonomy 2) have the minimizers (2,0,0,0), (0,2,0,0), (1,1,0,0), ... : 10 in all, with 3 different (sector A, sector B) weight vectors for blocks {0,1},{2,3}.', 'scope': 'Instance of minimizers_not_unique; native records 1 and 2.'},
        {'id': 'c4_orbit_sum_not_minimizer', 'statement': 'The source orbit sum (1,1,1,1) of (1,0,1,0) and (0,1,0,1) has total 4 but Phi1 = 2; the canonical symmetric point is (1/2,1/2,1/2,1/2).', 'scope': 'Instance; kernel c4_orbit_sum_not_minimizer.'}]
    return build_spec(
        node=NODE, short='residual_sector_weights', lean='ResidualSectorWeights',
        anchors=['ResidualSectorWeights.hol_d0', 'ResidualSectorWeights.exists_d0_of_hol_zero', 'ResidualSectorWeights.class_iff',
                 'ResidualSectorWeights.phi1_attained_and_lower_bound', 'ResidualSectorWeights.minimizer_iff',
                 'ResidualSectorWeights.minimizers_not_unique', 'ResidualSectorWeights.sector_weights_sum_to_phi1',
                 'ResidualSectorWeights.sector_weights_not_determined', 'ResidualSectorWeights.minimizer_unique_of_hol_zero',
                 'ResidualSectorWeights.minimizer_unique_of_one_edge', 'ResidualSectorWeights.symmetric_integral_iff',
                 'ResidualSectorWeights.symmetric_selector', 'ResidualSectorWeights.c4_instance_two_minimizers',
                 'ResidualSectorWeights.c4_orbit_sum_not_minimizer'],
        cases=jsonable(producer.CASES), public_tsv=producer.public_tsv(), data=producer.certificate(),
        scope_review=('The source declarations are l1_residual_sector_weights_minimizer_nonuniqueness_and_dihedral_selector (fixed rA=(1,1,0,0), rB=(0,0,1,1), plus a conjunct that is true for any w0,w1 and uses neither), '
                      'even_cycle_sector_weights_require_selector (two fixed C4 vectors by decide), l1_even_cycle_symmetry_orbit_canonical_sector_weights (fixed vectors by decide; the orbit SUM has twice Phi1) and sector_weights_sum_to_phi1 (additivity of a list sum on append). '
                      'None of them defines the minimum over a class, so "Phi1" there is the L1 of a given residual. The general claim is therefore proved afresh: on the n-cycle the class is the holonomy, Phi1 = |S|, the minimizers are a signed simplex, '
                      'two minimizers with equal (Phi1, Gamma2) differ in sector weights, and the symmetric average is an extra declared selector (integral only when n divides S). Weighted L1 forms are not treated.'),
        predicates=['Independent brute-force enumeration of the class c - d0 h over a gauge-fixed integer box justified without the closed form (|h_i| <= 2 sum |c| unweighted; with masses |r_j| <= sum m|c| / m_min), reading off the (weighted) minimum, the full minimizer set, its lexicographic extremes, the sector-weight tuples and the extremes of the sum of squares; two-cycle classes enumerated per cycle.',
                    'Holonomy recomputed as the invariant of the whole enumerated class; minimizer entries checked to carry the sign of the holonomy.',
                    'Symmetric point |S|/n checked in exact rationals against the enumerated minimum; flags (determined, unique, integral, zero-mass refusal) recomputed from the enumeration, and non-determination is demanded exactly when n >= 2, Phi1 > 0 and at least two sectors.',
                    'Exact cross-language (Python/Rust) wire equality and literal Lean axiom reports.'],
        boundary=boundary, generators=gens, relations=rels, compositions=comps, failed_compositions=failed, counterexamples=counter,
        open_obligations=['Kernel proof for the weighted L1 form with declared positive edge masses (the form actually declared in the window definition); only native rows exist.', 'Connected graphs other than the n-cycle (general C^1/im d0 with cycle rank > 1).', 'Gamma2 read as the sum of squares of the weights (PUB-009) as a kernel statement.',
                          'Whether any non-symmetry principle selects a minimizer; the symmetry itself as a derived rather than declared input.', 'Hilbert lift and density-matrix reading of the weights.'],
        colour_meanings={'EdgeCochain': 'Integer or rational edge cochain on the n-cycle', 'Weight': 'Nonnegative L1 value', 'SignedWeight': 'Holonomy (signed total)',
                         'ResidualSet': 'Finite set of minimizing residuals', 'Residual': 'One minimizing residual cochain', 'SectorSizes': 'Block sizes of consecutive edges',
                         'SectorWeightVector': 'Vector of block sums of |r_i|'},
        depends_on_result=True,
        qualification=('The DAG label PROVED_LEAN for this node rests on fixed C4 instances and a list-sum additivity; the general non-derivability is established only for the unweighted equal-mass n-cycle model with Gamma2 modelled as the holonomy, and the weighted form declared in the window definition may select a unique weight vector (native rows only, not a kernel theorem).'),
        challenge_plan='Coordinate mutants of every certificate leaf plus fourteen semantic near misses: unique minimizer from one witness, orbit sum as symmetric point, rounded symmetric point, zero mass accepted, one-edge non-uniqueness, single-sector variation, raw L1 as Phi1, sign swap, absolute holonomy, minimizers counted by sector vectors, weighted read as unweighted, Gamma2 as constant sum of squares, rank-2 single holonomy, determined-but-not-unique read as free.',
        composition_tree=['sector_weights(minimizer_set(c), sizes)', 'minimizer_set(phi1_quotient_min(c))'],
        construction='Exact integer enumeration of the class of each cochain; Lean proves the general n-cycle statements.',
        relation_evidence={'sector_weights_not_determined': 'Kernel theorem for every n >= 2 and hol != 0; native tables show 3 to 10 sector vectors on the 4-cycle.',
                           'minimizers_are_signed_simplex': 'Kernel iff; native counts equal C(|S|+n-1, n-1) for every positive-mass case.'},
        max_coordinate_mutants=None)


if __name__ == '__main__':
    print(write_spec(HERE, NODE, spec()))
