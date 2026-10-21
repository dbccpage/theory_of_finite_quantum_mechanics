"""Build specs/L1-U1-SELECTOR-OTHER-SEGMENT.json from the producer and the node's reviewed claims."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp/batch_tools'))
from spec_builder import build_spec, write_spec  # noqa: E402

_s = importlib.util.spec_from_file_location('producer', ROOT / 'code/python/src/qm/pfp_u1_selector_segment.py')
producer = importlib.util.module_from_spec(_s)
_s.loader.exec_module(producer)

NODE = 'L1-U1-SELECTOR-OTHER-SEGMENT'
H = 'Points of the unit circle x^2 + y^2 = 1 with rational coordinates (the unit Gaussian rationals) under complex multiplication; a phase group is a subgroup; finite means every element has finite order.'
H011 = 'lean4/H011U1SelectorBoundary.lean'
DQ = 'lean4/DerivationDagQMClosure.lean'


def spec():
    boundary = {
        'supports': ('For EVERY rational point z = (x, y) of the unit circle (kernel-checked): z has finite order iff z is one of (1,0), (-1,0), (0,1), (0,-1), i.e. the torsion of the unit Gaussian rationals is exactly mu_4; '
                     'if 2x is not an integer the point has infinite order (integer sequence W_n = c^n 2 Re z^n with W_{n+2} = a W_{n+1} - c^2 W_n is a^n modulo a prime p dividing c, while z^n = 1 would give 2 c^n); '
                     'x = +-1/2 is impossible (y^2 = 3/4 has no rational root), so there is no order-3 or order-6 phase and every finite phase group inside the Gaussian rationals has exponent dividing 4; '
                     'the Cayley map (m, n) -> ((n^2 - m^2)/(n^2 + m^2), 2mn/(n^2 + m^2)) lands on the circle (cayley_on_circle) and every point with x != -1 equals Cayley(m, n) for (m, n) = (y, 1 + x) (every_point_is_cayley); (-1, 0) is also reached, at n = 0 (cayley_reaches_south_pole), so the map is onto the circle; '
                     'the Cayley points include the four points of mu_4; the infinite-order rational points are exactly those with 2x not an integer, i.e. the circle minus mu_4; (3/5, 4/5) has infinite order (u345_infinite_order, the kernel instance). '
                     'Native (exact enumeration, not kernel theorems): the exhaustive list of the five cases 2x = -2..2 (two refused at x = +-1/2); 15 Cayley points with the smallest prime p dividing den(2x) and the valuation law v_p(2 Re z^k) = -k v_p(den 2x) for k = 1..6; '
                     'orders are searched up to 12, so order 0 means "no power equal to 1 up to 12" and infinite order itself rests on the kernel theorem; two census rows (B = 3 and 6: 16 and 48 distinct Cayley points, exactly 4 in mu_4, (-1,0) reached); '
                     'and a finite-field table: the unit circle over F_p has p-1 points for p = 1 mod 4, p+1 for p = 3 mod 4 and is cyclic, so phases of orders beyond 4 occur there (13 primes up to 43, brute force).'),
        'does_not_support': ('Any derivation of C or U(1) from finite carriers, or a proof that no such derivation exists: the node is a pointer to QM_028 / QM_062 owned by another segment and its selection is NOT established here; '
                             'finite carriers in the sense of finite fields or finite rings (the unit circle over F_p has order p -+ 1, native table only): the theorem is a no-go only for finite subgroups of the unit Gaussian rationals, and the identification of a finite phase carrier with such a subgroup is not argued; '
                             'larger finite phase groups in cyclotomic extensions (Q(zeta_8), Q(zeta_3), ...) which this result does not treat; completion, continuity, compactness or Haar measure of the circle; '
                             'that there are infinitely many infinite-order points as a kernel statement (only the instance u345_infinite_order and the native census); '
                             'the rival split-complex hyperbola x^2 - y^2 = 1 (the H011 flag rival_excluded); the H011 selector pack, whose selector_not_free is rfl on a record with a hand-set Boolean field; any physical reading of phases.'),
        'narrowest_claim': ('Inside the unit Gaussian rationals the only phases of finite order are the four elements of mu_4; the rational circle points outside mu_4 are exactly those with 2x not an integer and they have infinite order (kernel instance: (3/5, 4/5)), '
                            'so a finite phase group inside the Gaussian rationals has order dividing 4, whereas the unit circle over a finite field F_p is a different finite carrier with p -+ 1 elements (native table, not a kernel statement).'),
        'next_test': ('Determine the unit circle {x^2 + y^2 = 1} over F_p and over Z/n exactly: prove that it is cyclic of order p - (-1/p) and show which phase orders a finite scalar ring does and does not force, as the finite-carrier counterpart of the Gaussian-rational torsion result; the torsion over Q(i, sqrt 2) and Q(zeta_3) is a secondary item.')}
    gens = [
        {'id': 'cayley_point', 'source_declarations': [DQ + '::fq_u1_selector_split_real_zero_divisors_and_cayley_unit_circle (line 959): GENERAL in t : Int for the Pythagorean identity (1-t^2)^2 + (2t)^2 = (1+t^2)^2, plus fixed conjuncts (1*1-1*1 = 0, 1+1 = 2); this node extends to Rat parameters and surjectivity'],
         'ordered_inputs': ['CayleyParameter'], 'output': 'CirclePoint', 'semantic_predicate': '((n^2-m^2)/(n^2+m^2), 2mn/(n^2+m^2)) has norm 1; every point except (-1,0) arises.', 'hypotheses': [H]},
        {'id': 'circle_power', 'source_declarations': ['lean4/U1PowerMapInjectivity.lean::gaussPow34 (powers of 3+4i; a different module, not a source binding of this node, shown for lineage)'],
         'ordered_inputs': ['CirclePoint', 'Exponent'], 'output': 'CirclePoint', 'semantic_predicate': 'z^k by complex multiplication; Re z^(k+2) = 2x Re z^(k+1) - Re z^k.', 'hypotheses': [H]},
        {'id': 'torsion_order', 'source_declarations': [H011 + '::quarter_turn_outside_sign_subgroup (line 66): FIXED INSTANCE on Fin 4 by decide (quarter + quarter = half)',
                                                         'lean4/U1TorsionExclusion.lean::J_order_4 (fixed 2 x 2 integer matrix of order 4, not a source binding)'],
         'ordered_inputs': ['CirclePoint'], 'output': 'OrderOrInfinite', 'semantic_predicate': 'Smallest n > 0 with z^n = 1, or infinite.', 'hypotheses': [H]},
        {'id': 'padic_witness', 'source_declarations': ['no source declaration; new integer-sequence witness (Wseq) with a prime p dividing den(2x)'],
         'ordered_inputs': ['CirclePoint'], 'output': 'Prime', 'semantic_predicate': 'Smallest prime p | den(2x), with v_p(2 Re z^k) = -k v_p(den 2x).', 'hypotheses': [H]},
        {'id': 'selector_pack_discharge', 'source_declarations': [H011 + '::SelectorPack (line 16), SelectorDischarged (line 22), qm062Route (line 26), selector_not_free (line 32): a 4-Boolean record, its AND, one record with rival_excluded := false, and rfl; DEFINITION-LEVEL, vacuous as a derivation'],
         'ordered_inputs': ['SelectorPack'], 'output': 'Bool', 'semantic_predicate': 'AND of phase_composition_law, transport_functoriality, carrier_connectedness, rival_excluded.', 'hypotheses': ['Bookkeeping only; the flags are hand-set.']}]
    rels = [
        {'id': 'real_part_recurrence', 'source_declarations': ['no source declaration; new general theorem re_rec'],
         'equation_or_predicate': 'Re z^(k+2) = 2x Re z^(k+1) - Re z^k when x^2 + y^2 = 1', 'typing_conditions': 'CirclePoint, Exponent', 'evidence_status': 'Kernel theorem re_rec; native valuation columns use it', 'scope': 'all rational circle points'},
        {'id': 'torsion_is_mu4', 'source_declarations': [H011 + '::sign_units_closed (line 62), quarter_turn_outside_sign_subgroup (line 66): fixed Int/Fin 4 instances only'],
         'equation_or_predicate': 'z^n = 1 for some n > 0 iff z in {(1,0), (-1,0), (0,1), (0,-1)}', 'typing_conditions': 'CirclePoint over Q', 'evidence_status': 'Kernel theorems circle_torsion, circle_torsion_iff, torsion_exponent_divides_four; native orders', 'scope': 'all rational circle points'},
        {'id': 'infinite_order_when_twice_x_nonintegral', 'source_declarations': ['no source declaration; U1PowerMapInjectivity proves it for the single point 3+4i (not a binding)'],
         'equation_or_predicate': 'den(2x) != 1 implies z^n != 1 for all n > 0', 'typing_conditions': 'CirclePoint', 'evidence_status': 'Kernel theorem not_torsion_of_den, u345_infinite_order (instance); native valuation law', 'scope': 'all rational circle points'},
        {'id': 'no_half_integer_x_points', 'source_declarations': ['no source declaration'],
         'equation_or_predicate': 'x = +-1/2 forces y^2 = 3/4, which has no rational root; hence no order-3 or order-6 phase', 'typing_conditions': 'Rat', 'evidence_status': 'Kernel theorems no_point_with_x_half, cube_root_trivial; native half records', 'scope': 'all rational y'},
        {'id': 'cayley_covers_the_circle', 'source_declarations': [DQ + '::fq_u1_selector_split_real_zero_divisors_and_cayley_unit_circle (line 959): Int parameter, identity only'],
         'equation_or_predicate': 'cayley(m,n) is on the circle; every point with x != -1 is cayley(y, 1+x); (-1,0) = cayley(m, 0)', 'typing_conditions': 'Rat parameters', 'evidence_status': 'Kernel theorems cayley_on_circle, every_point_is_cayley', 'scope': 'all rational circle points'},
        {'id': 'selector_pack_is_bookkeeping', 'source_declarations': [H011 + '::selector_not_free (line 32): rfl on qm062Route with rival_excluded := false; ' + H011 + '::selector_requires_rival_exclusion (line 54): general over the record but only unfolds the Boolean AND'],
         'equation_or_predicate': 'SelectorDischarged S = false whenever one flag is false', 'typing_conditions': 'SelectorPack', 'evidence_status': 'Source theorems read, not re-proved; they carry no mathematical content about circles', 'scope': 'Boolean record'}]
    comps = [
        {'outer_operation': 'torsion_order', 'input_slot': 0, 'inner_operation': 'cayley_point', 'colour_match': 'CirclePoint', 'hypothesis_match': H,
         'licensing_relations': ['torsion_is_mu4', 'cayley_covers_the_circle'], 'evidence_status': 'Kernel and native'},
        {'outer_operation': 'padic_witness', 'input_slot': 0, 'inner_operation': 'cayley_point', 'colour_match': 'CirclePoint', 'hypothesis_match': H,
         'licensing_relations': ['infinite_order_when_twice_x_nonintegral', 'real_part_recurrence'], 'evidence_status': 'Kernel and native'}]
    failed = [
        {'composition': 'torsion_order o cayley_point onto a phase of order 3, 5, 6 or 8', 'reason': 'No rational circle point has such an order: torsion is mu_4 (kernel circle_torsion); x = +-1/2 would be needed for order 3 or 6 and y^2 = 3/4 has no rational root.'},
        {'composition': 'selector_pack_discharge from finite Gaussian-rational carriers', 'reason': 'No operation of this node produces the flag rival_excluded or the circle; the pack is a hand-set Boolean record, and the finite carriers inside the Gaussian rationals stop at mu_4.'}]
    counter = [
        {'id': 'pythagorean_point_infinite_order', 'statement': '(3/5, 4/5) is a rational phase of infinite order (den(2x) = 5; W_n = a^n mod 5 is never 0).', 'scope': 'Instance of not_torsion_of_den; kernel u345_infinite_order; native record (1,2).'},
        {'id': 'no_order_six_phase', 'statement': 'A primitive sixth root of unity would have x = 1/2 and y = sqrt(3)/2; y^2 = 3/4 is not a rational square.', 'scope': 'Kernel no_point_with_x_half; native half record k = 1.'}]
    return build_spec(
        node=NODE, short='u1_selector_segment', lean='U1SelectorSegment',
        anchors=['U1SelectorSegment.re_rec', 'U1SelectorSegment.Wseq_cast', 'U1SelectorSegment.Wseq_mod', 'U1SelectorSegment.not_torsion_of_den',
                 'U1SelectorSegment.no_point_with_x_half', 'U1SelectorSegment.circle_integral_case', 'U1SelectorSegment.circle_torsion',
                 'U1SelectorSegment.circle_torsion_iff', 'U1SelectorSegment.torsion_exponent_divides_four', 'U1SelectorSegment.cube_root_trivial',
                 'U1SelectorSegment.u345_infinite_order', 'U1SelectorSegment.cayley_on_circle', 'U1SelectorSegment.every_point_is_cayley',
                 'U1SelectorSegment.cayley_reaches_south_pole'],
        cases=[list(c) for c in producer.CASES], public_tsv=producer.public_tsv(), data=producer.certificate(),
        scope_review=('The node is a pointer ("Referenced only ... owned by another segment"), so it cannot be discharged here. The local sources are H011U1SelectorBoundary (a four-Boolean SelectorPack, its AND, a record with rival_excluded := false and rfl: bookkeeping), '
                      'quarter_turn_outside_sign_subgroup (Fin 4 by decide), ds_qm062_u1_selector_layers_and_ring_iso (fixed 2 x 2 integers), the Int Cayley identity in fq_u1_selector_split_real_zero_divisors_and_cayley_unit_circle (general in t but only an identity) '
                      'and ds_qm062_and_l1_u1_selector_frob_exclusions_and_gaussian_ring_injectivity (fixed plus 1 x 1 additivity/injectivity). The external complex_structure_selector.rs only checks the pairing factor sigma(u)u. '
                      'What a finite carrier can and cannot select is made exact in one place: the torsion of the unit Gaussian rationals is mu_4, proved for every rational circle point with an integer-sequence argument, with the Cayley map covering the whole circle. '
                      'This is a no-go for finite carriers inside Q(i), not a statement that C or U(1) cannot be selected by other means.'),
        predicates=['Independent Gaussian-integer powers A^k/d^k with d the lcm of the denominators of x and y; orders read off A^n == d^n.',
                    'p-adic valuations of 2 Re z^k computed as v_p(2 Re A^k) - k v_p(d) and compared with the predicted -k v_p(den 2x); points with den(2x) > 1 must have order 0 (infinite in the search bound), points with integral 2x must be in mu_4.',
                    'Rational y for the half-integer x values decided by the integer square test on P*Q (producer tests numerator and denominator separately); x = +-1/2 must be refused.',
                    'Census of all Cayley points in a box recomputed with exact Fractions: exactly the four mu_4 points have a power equal to 1 within the bound, every other point has 2x not an integer, and (-1,0) is reached.',
                    'Unit circle over F_p counted by plain enumeration of F_p^2 (producer uses the Euler criterion), element orders by repeated complex multiplication, cyclicity from an element of every divisor order.',
                    'Exact cross-language (Python/Rust) wire equality and literal Lean axiom reports.'],
        boundary=boundary, generators=gens, relations=rels, compositions=comps, failed_compositions=failed, counterexamples=counter,
        open_obligations=['Derivation or failure of the selection of C and U(1) (owned by the QM_028 / QM_062 segment).', 'Kernel proof of the unit circle over F_p and Z/n (finite carriers proper): cyclic of order p - (-1/p); torsion over Q(i, sqrt 2) and Q(zeta_3) (larger finite phase groups).',
                          'The split-complex rival hyperbola x^2 - y^2 = 1 (torsion {+-1}) and the H011 rival_excluded flag.', 'Completion, continuity and compactness of the phase group.'],
        colour_meanings={'CayleyParameter': 'Pair (m, n) of rationals, not both zero', 'CirclePoint': 'Pair (x, y) of rationals with x^2 + y^2 = 1', 'Exponent': 'Natural number k',
                         'OrderOrInfinite': 'Smallest n > 0 with z^n = 1, or infinite', 'Prime': 'Smallest prime dividing den(2x), 0 if 2x is an integer', 'SelectorPack': 'Four hand-set Boolean flags'},
        depends_on_result=True,
        qualification=('The node is a pointer, not a theorem. This result is only the torsion no-go for finite phase groups inside the unit Gaussian rationals (torsion = mu_4); it neither derives nor refutes the selection of C and U(1) from finite carriers.'),
        challenge_plan='Coordinate mutants of every certificate leaf plus twelve semantic near misses: a sixth root of unity, the 3-4-5 point as a quarter turn, valuation at a wrong prime or with a wrong exponent, i of infinite order, identity read as -1, search bound read as an order, a non-unit point flagged mu_4, integral 2x for a Cayley point, all Cayley points of infinite order, the Cayley map missing (-1,0), the finite-field circle read as having only mu_4.',
        composition_tree=['torsion_order(cayley_point(m,n))', 'padic_witness(cayley_point(m,n))'],
        construction='Exact orders and p-adic valuations of rational circle points from Cayley parameters, with the exhaustive half-integer list; Lean proves the torsion theorem for every rational point.',
        relation_evidence={'torsion_is_mu4': 'Kernel iff for every rational circle point; native orders: the 4 mu_4 points have orders 1, 2, 4, 4 and all 11 other Cayley points have order 0 within bound 12; census rows B = 3, 6.',
                           'infinite_order_when_twice_x_nonintegral': 'Kernel theorem; native valuation law on 11 points with den(2x) > 1.'})


if __name__ == '__main__':
    print(write_spec(HERE, NODE, spec()))
