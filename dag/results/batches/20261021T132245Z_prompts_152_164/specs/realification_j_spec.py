"""Build specs/L1-WDP-REALIFICATION-J.json from the producer and the node's reviewed claims."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp/batch_tools'))
from spec_builder import build_spec, write_spec  # noqa: E402

_s = importlib.util.spec_from_file_location('producer', ROOT / 'code/python/src/qm/pfp_realification_j.py')
producer = importlib.util.module_from_spec(_s)
_s.loader.exec_module(producer)

NODE = 'L1-WDP-REALIFICATION-J'
H = ('Complex matrices are pairs (P, Q) of real matrices (A = P + iQ) over a commutative ring; R(A) = [[P,-Q],[Q,P]] with all real coordinates before all imaginary ones; '
     'J_n = [[0,-I],[I,0]] is DECLARED.')
DQ = 'lean4/DerivationDagQMClosure.lean'
EXT = 'the_symbol_game/omega_engine/crates_rs/omega_quantum_physics/src/complex_realification.rs'


def spec():
    boundary = {
        'supports': ('For every finite index types m, n, k and every commutative ring (kernel-checked, Matrix.fromBlocks), on the declared PAIR model of a complex matrix A = (P, Q) with the hand-written product (PS - QT, PT + QS): R is additive, ring-linear, multiplicative on composable matrices, sends the identity to the identity and is injective; J^2 = -1; '
                     'J_m R(A) = R(A) J_n for rectangular A; R(iA) = J_m R(A); R(A*) = R(A)^T so A is Hermitian iff R(A) is symmetric; Tr R(A) = 2 Tr P, i.e. twice the REAL part of the complex trace '
                     '(the instance A = 1 + i has complex trace 1 + i and real trace 2); Theorem 2: a matrix indexed by (m + m) x (n + n) is R(A) for exactly one A iff J_m M = M J_n; '
                     'conjugating J by an invertible P transports the commutant, and an explicit unimodular instance shows [[1,-1],[2,-1]] is a second integer square root of -I that does not commute with J (kernel instance). '
                     'Native (exact tables, not kernel theorems): 9 product cases up to 3 x 3 (square and rectangular, incl. A = 0, A = I, A = iI, a Hermitian A) with R(AB), R(A*) and the INTERLEAVED coordinate order (re_1, im_1, re_2, ...) which in general gives a different matrix from the block one (the two can coincide, e.g. for A = 0 or A = I); each product record states whether the interleaved matrix commutes with the block J_n, and no universal statement is made; '
                     '13 real matrices tested for membership in the image (positive cases, diag(1,0,0,0), diag(-1,1,1,1), diag(1,-1) and diag(I,-I) which anticommute with J, an odd-dimensional matrix, rectangular cases, a symmetric non-image matrix); '
                     '9 small matrices (8 Hermitian, 1 non-Hermitian refused) on which complex positive semidefiniteness and positive semidefiniteness of the real symmetric R(A) agree (instances of preservation and reflection, found by principal minors and by elimination; NOT a kernel theorem); '
                     'the J-structure flags of 8 integer 2 x 2 matrices; and a brute-force census of the integer square roots of -I in the boxes B = 1, 2, 3, 5, 7: 26 solutions in the box [-5,5], of which only +-J commute with J. '
                     'The census is a bounded enumeration, not a theorem; "only +-J commute with J" is shown by the census in those boxes only (the commutant of J in M_2(Z) is {aI + bJ}, but that argument is not in the module).'),
        'does_not_support': ('Any selection of J or of the complex field (J is a declaration; a second square root of -I exists in the kernel instance and the census exhibits many more); the identification of the pair model CMat with Mathlib complex matrices (no anchor shows CMat is an associative ring or equals Matrix m n Complex); '
                             'the block-ordering convention (all real coordinates before all imaginary ones) is part of the definition: the interleaved ordering gives a different J and a different matrix; '
                             'states sigma = R(rho)/2, positivity as a theorem (native instances only), effects, instruments / Kraus intertwining (Theorem 3), the balanced tensor lift, or any operational or physical reading; infinite dimensions; the claim that every real channel is a realified complex one (it is not).'),
        'narrowest_claim': ('Complex matrices here are the declared pair model (P, Q) with the hand-written product. R(A) = [[P,-Q],[Q,P]] is an injective ring-linear multiplicative embedding of these into real matrices with J_m R(A) = R(A) J_n and Tr R(A) = 2 Re Tr A, and its image is exactly the real matrices that intertwine the DECLARED J (block coordinate order); '
                            'the same J^2 = -1 identity holds for other matrices (kernel instance, bounded census), so the choice of J remains an input.'),
        'next_test': ('Prove in the kernel that R preserves and reflects positivity for Hermitian A, i.e. A is positive semidefinite iff the real quadratic form of R(A) is nonnegative, and that sigma = R(rho)/2 has real trace 1 exactly when Tr rho = 1; the native psd rows are the instances to match.')}
    gens = [
        {'id': 'realify', 'source_declarations': [DQ + '::ds_qm062_u1_selector_layers_and_ring_iso (line 685): FIXED INSTANCE by decide: the 2 x 2 integer matrices J = [[0,-1],[1,0]], S, K, Z1 = [[3,-4],[4,3]], Z2 = [[1,-2],[2,1]] and one product Z1 Z2; this is R on 1 x 1 Gaussian integers',
                                  'lean4/DerivationDagQMClosure.lean::ds_qm062_and_l1_u1_selector_frob_exclusions_and_gaussian_ring_injectivity (line 1503): GENERAL in (a1,b1,a2,b2) but only for 1 x 1: additivity and injectivity of (a,b) -> [[a,-b],[b,a]]',
                                  EXT + '::realify_operator_with_limits (line 42): external executable realification of rectangular BasicMatrix<GaussianRat> with resource limits'],
         'ordered_inputs': ['ComplexMatrix'], 'output': 'RealMatrix', 'semantic_predicate': 'R(A) = [[P,-Q],[Q,P]], real coordinates first.', 'hypotheses': [H]},
        {'id': 'complex_structure_J', 'source_declarations': [DQ + '::ds_qm062_u1_selector_layers_and_ring_iso (line 685): J is a let-bound 2 x 2 literal inside a theorem, not a definition',
                                                             'dag/derivations/08_l1_to_l2/tfq_0006_conditional_finite_hilbert_lift.md (paper pin): lists the complex structure as an import'],
         'ordered_inputs': ['Dimension'], 'output': 'RealMatrix', 'semantic_predicate': 'J_m = [[0,-I],[I,0]] with J^2 = -I; declared, not selected.', 'hypotheses': [H, 'J is an assumption (node declared_assumptions: complex structure J).']},
        {'id': 'complex_product', 'source_declarations': [DQ + '::Mat2Int.mul (line 184): definition, the 2 x 2 integer matrix product, used as the realified Gaussian product on fixed examples'],
         'ordered_inputs': ['ComplexMatrix', 'ComplexMatrix'], 'output': 'ComplexMatrix', 'semantic_predicate': '(P+iQ)(S+iT) = (PS - QT) + i (PT + QS).', 'hypotheses': [H]},
        {'id': 'real_trace', 'source_declarations': ['no source declaration; paper Theorem 1 states Tr R(A) = 2 Re Tr A with the qualification that A = 1 + i has real trace 2, not 2 + 2i'],
         'ordered_inputs': ['RealMatrix'], 'output': 'Scalar', 'semantic_predicate': 'Tr R(A) = 2 Tr P.', 'hypotheses': [H]},
        {'id': 'image_decision', 'source_declarations': ['no source declaration; paper Theorem 2 (exact image), proof by block equations W = -V, Z = U'],
         'ordered_inputs': ['RealMatrix'], 'output': 'ComplexMatrixOrRefusal', 'semantic_predicate': 'M = R(A) for exactly one A iff J_m M = M J_n; then A = U - iV from the top blocks.', 'hypotheses': [H]}]
    rels = [
        {'id': 'R_multiplicative', 'source_declarations': [DQ + '::ds_qm062_u1_selector_layers_and_ring_iso (line 685): fixed product Z1 Z2 = Zprod only (1 x 1 Gaussian integers, by decide)'],
         'equation_or_predicate': 'R(AB) = R(A)R(B), R(A+B) = R(A)+R(B), R(1) = 1, R injective', 'typing_conditions': 'ComplexMatrix m x n, n x k over a commutative ring', 'evidence_status': 'Kernel theorems R_mul, R_add, R_smul, R_one, R_injective; native tables', 'scope': 'all finite shapes'},
        {'id': 'J_squares_to_minus_one_and_intertwines', 'source_declarations': [DQ + '::ds_qm062_u1_selector_layers_and_ring_iso (line 685): fixed J*J = -I on 2 x 2 only'],
         'equation_or_predicate': 'J^2 = -1; J_m R(A) = R(A) J_n; R(iA) = J_m R(A)', 'typing_conditions': 'rectangular allowed', 'evidence_status': 'Kernel theorems J_sq, J_R_comm, R_imul; native flags', 'scope': 'all finite shapes'},
        {'id': 'star_is_transpose', 'source_declarations': ['no source declaration; paper Theorem 1 R(A*) = R(A)^T'],
         'equation_or_predicate': 'R(A*) = R(A)^T; A Hermitian iff R(A) symmetric', 'typing_conditions': 'square for the Hermitian statement', 'evidence_status': 'Kernel theorems R_star, hermitian_iff_symmetric; native flags', 'scope': 'all finite shapes'},
        {'id': 'trace_is_twice_real_part', 'source_declarations': [DQ + '::l1_observer_h1_h5_cochain_flatness_and_wdp_window_mass_realification (line 1121): excluded lead, an aggregate of unrelated numeral facts plus the trivial iff (b = -c and a = d) <-> (b + c = 0 and a - d = 0); no R, no trace'],
         'equation_or_predicate': 'Tr R(A) = 2 Tr P; not 2 Tr_C A unless Im Tr A = 0', 'typing_conditions': 'square', 'evidence_status': 'Kernel theorems trace_R, trace_not_twice_complex_trace; native trace columns', 'scope': 'all square shapes'},
        {'id': 'image_iff_commutes_with_J', 'source_declarations': ['no source declaration; the node bottleneck says "Lean for Thm 1/2 not looked for"'],
         'equation_or_predicate': 'M = R(A) for exactly one A iff J_m M = M J_n', 'typing_conditions': 'M indexed by (m+m) x (n+n); even real dimensions only', 'evidence_status': 'Kernel theorem image_iff; native membership decided independently by the block form', 'scope': 'all finite shapes'},
        {'id': 'J_is_declared', 'source_declarations': [DQ + '::ds_qm062_and_l1_u1_selector_frob_exclusions_and_gaussian_ring_injectivity (line 1503): fixed K = [[0,1],[1,0]] with K^2 = I (a square root of +I) and S, K not commuting; J is not singled out'],
         'equation_or_predicate': 'J^2 = -1 does not determine J: other square roots exist, conjugate to J, with a different commutant', 'typing_conditions': 'Fin 2 over Int (instance); conjugation transport general', 'evidence_status': 'Kernel theorems commutes_conj (general), other_square_root_instance, other_root_not_in_image (instances); native census', 'scope': 'general transport, 2 x 2 integer instance and census'}]
    comps = [
        {'outer_operation': 'real_trace', 'input_slot': 0, 'inner_operation': 'realify', 'colour_match': 'RealMatrix', 'hypothesis_match': H,
         'licensing_relations': ['trace_is_twice_real_part'], 'evidence_status': 'Kernel and native'},
        {'outer_operation': 'realify', 'input_slot': 0, 'inner_operation': 'complex_product', 'colour_match': 'ComplexMatrix', 'hypothesis_match': H,
         'licensing_relations': ['R_multiplicative'], 'evidence_status': 'Kernel and native'},
        {'outer_operation': 'image_decision', 'input_slot': 0, 'inner_operation': 'realify', 'colour_match': 'RealMatrix', 'hypothesis_match': 'The decision returns the unique preimage A.',
         'licensing_relations': ['image_iff_commutes_with_J', 'R_multiplicative'], 'evidence_status': 'Kernel and native'}]
    failed = [
        {'composition': 'image_decision o realify on an unrestricted real matrix', 'reason': 'diag(1,0,0,0), diag(-1,1,1,1) and diag(1,-1) are real, symmetric or orthogonal but do not commute with J, so image_decision refuses; the image of realify is a strict subset of the real matrices (kernel image_iff).'},
        {'composition': 'real_trace o realify read as twice the complex trace', 'reason': 'Tr R(A) = 2 Re Tr A drops Im Tr A; A = 1 + i gives 2, not 2 + 2i (kernel instance).'}]
    counter = [
        {'id': 'other_square_root_of_minus_one', 'statement': 'The integer matrix [[1,-1],[2,-1]] squares to -I, is conjugate to J by the unimodular [[1,0],[1,1]], and does not commute with J, so it is not R of a complex number.', 'scope': 'Instance; kernel other_square_root_instance.'},
        {'id': 'census_of_square_roots', 'statement': 'In the box [-7,7] there are 26 integer 2 x 2 matrices with X^2 = -I but only two (+-J) commute with J.', 'scope': 'Native census, bounded box; the general count is not claimed.'}]
    return build_spec(
        node=NODE, short='realification_j', lean='RealificationJ',
        anchors=['RealificationJ.R_add', 'RealificationJ.R_smul', 'RealificationJ.R_mul', 'RealificationJ.R_one', 'RealificationJ.R_injective',
                 'RealificationJ.J_sq', 'RealificationJ.J_R_comm', 'RealificationJ.R_imul', 'RealificationJ.R_star', 'RealificationJ.hermitian_iff_symmetric',
                 'RealificationJ.trace_R', 'RealificationJ.trace_not_twice_complex_trace', 'RealificationJ.image_iff', 'RealificationJ.commutes_conj',
                 'RealificationJ.other_square_root_instance', 'RealificationJ.other_root_not_in_image'],
        cases=[list(c) for c in producer.CASES], public_tsv=producer.public_tsv(), data=producer.certificate(),
        scope_review=('The node is a DEFINITION whose bottleneck says Lean for Theorems 1 and 2 was not looked for. The local source ds_qm062_u1_selector_layers_and_ring_iso is a fixed 2 x 2 integer instance (J, S, K, Z1, Z2 and one product), '
                      'ds_qm062_and_l1_u1_selector_frob_exclusions_and_gaussian_ring_injectivity is general in four integers but only for 1 x 1 Gaussian integers, and the paper anchor l1_observer_h1_h5_cochain_flatness_and_wdp_window_mass_realification '
                      'is an excluded aggregate (its only structural conjunct is the trivial iff (b = -c and a = d) <-> (b + c = 0 and a - d = 0)). The theorems are therefore proved afresh for general finite index types in Lean '
                      '(Theorem 1 pieces and Theorem 2), the trace qualification (A = 1 + i) is a kernel instance, and J is shown to be a declaration: a different square root of -I exists and carves out a different commutant.'),
        predicates=['Independent construction R = I2 (x) P + [[0,-1],[1,0]] (x) Q and J_m = [[0,-1],[1,0]] (x) I_m; the REAL product R(A)R(B) is computed first and compared with R of the complex product.',
                    'Image membership decided from the top blocks (R(U - iV) == M) independently of the commutation test J_m M = M J_n, and the two must agree on every tested real matrix; odd dimensions refused.',
                    'Trace identity Tr R(A) = 2 Re Tr A recomputed from the real matrix, with the complex-trace failure flag (A = 1 + i, A = iI); Hermitian <-> symmetric recomputed from A and from R(A).',
                    'J-structure flags by direct 2 x 2 multiplication, and the square-root-of-minus-one census by brute force over the whole integer box; only +-J commute with J.',
                    'Exact cross-language (Python/Rust) wire equality and literal Lean axiom reports.'],
        boundary=boundary, generators=gens, relations=rels, compositions=comps, failed_compositions=failed, counterexamples=counter,
        open_obligations=['Positivity preservation and reflection for Hermitian A and the state map sigma = R(rho)/2 with real trace 1 (native psd rows only); identification of the pair model with Mathlib complex matrices; a kernel proof that only +-J commute with J among the square roots of -I.', 'Instrument (Theorem 3) and channel composition statements.',
                          'Selection of J and of the complex field (owned by L1-U1-SELECTOR-OTHER-SEGMENT; not established here).', 'The balanced tensor lift of the doubled carrier.'],
        colour_meanings={'ComplexMatrix': 'Pair (P, Q) of real matrices, A = P + iQ', 'RealMatrix': 'Real matrix on the doubled carrier', 'Dimension': 'Finite index type',
                         'Scalar': 'Ring element', 'ComplexMatrixOrRefusal': 'The unique preimage A or a refusal'},
        depends_on_result=True,
        qualification=('The node is a DEFINITION with Lean for Theorems 1 and 2 not looked for; the new module proves them for general finite shapes on the pair model of complex matrices, and the statement "Tr R(A) = 2 Re Tr A" is exactly the real-part statement, not twice the complex trace. The selection of J remains an import; positivity and states sigma = R(rho)/2 have native instances only.'),
        challenge_plan='Coordinate mutants of every certificate leaf plus twelve semantic near misses: trace read as twice the complex trace, swapped block convention, unrestricted real matrix in the image, conjugation as complex-linear, rectangular treated as square, any square root of -I as J, J unique, symmetric implies image, odd dimension has a J, interleaved ordering read as the same J, conjugate transpose without the sign of Q, positivity asserted for an indefinite matrix.',
        composition_tree=['real_trace(realify(A))', 'realify(complex_product(A,B))', 'image_decision(realify(A))'],
        construction='Exact Gaussian-rational realification tables, image decisions on real matrices, and an integer census of square roots of -I; Lean proves the general block statements.',
        relation_evidence={'R_multiplicative': 'Kernel theorem for all finite shapes; native R(A)R(B) = R(AB) on 9 product cases.',
                           'image_iff_commutes_with_J': 'Kernel iff; native image decision agrees with the commutation test on 13 real matrices.',
                           'J_is_declared': 'Kernel general conjugation transport and a 2 x 2 instance; native BOUNDED census 2/10/10/26/26 square roots for B = 1,2,3,5,7, of which exactly 2 commute with J (enumeration, not a theorem).'})


if __name__ == '__main__':
    print(write_spec(HERE, NODE, spec()))
