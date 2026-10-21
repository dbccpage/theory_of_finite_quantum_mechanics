"""Build specs/PG-WDP-PROTECTED-QUESTIONS.json from the producer and the node's reviewed claims."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp/batch_tools'))
from spec_builder import build_spec, write_spec  # noqa: E402

_s = importlib.util.spec_from_file_location('producer', ROOT / 'code/python/src/qm/pfp_wdp_protected_questions.py')
producer = importlib.util.module_from_spec(_s)
_s.loader.exec_module(producer)

NODE = 'PG-WDP-PROTECTED-QUESTIONS'
SYM = 'external WitnessedDifference/Symmetry.lean'
H = ('Unstructured carrier with the full permutation action; a declared input set S is fixed pointwise (a modelling choice narrower than '
     'WDP-CH03-D01, which is relative to an implementation class and a dependency preorder that are not modelled).')


def spec():
    boundary = {
        'supports': ('Over an arbitrary type X (Lean, general; the cardinality statement frontier_card is informative only for finite X, frontierEquiv and minimalSelecting_iff_singleton carry the general content): '
                     'no point is fixed by every permutation when X has two distinct points (the bare-set form of "no Sym(X)-equivariant distinguished-point selection"); a point is invariant under the '
                     'pointwise stabiliser of a declared set S iff it lies in S or the complement of S is that single point; S selects some point iff S is nonempty or X has exactly one point; for X with two '
                     'distinct points the inclusion-minimal selecting sets are exactly the singletons, one per point (a consequence of the pointwise-stabiliser definition: a declared point is fixed because it is '
                     'declared); on a one-point carrier the empty declaration already selects and on an empty carrier nothing does. Replay bound (not part of the Lean claim): exact tables for every subset of every '
                     'carrier of size 0..6 (127 subsets), invariant points by enumerating all permutations fixing S, and the minimal selecting sets.'),
        'does_not_support': ('Retention, dynamics or observers being impossible or available (WDP-CH03-N01 is a nonclaim, not formalised); that Selecting / MinimalSelecting formalises WDP-CH03-D01 (D01 minimises declared '
                             'input sets whose removal restores a symmetry that moves the output, relative to an implementation class and dependency preorder; here the minimal declarations making some point invariant under the '
                             'pointwise stabiliser are computed, and the two agree on singletons only because the output is the declared point); a Lean notion of equivariant selection function (no_fully_invariant_point is its '
                             'bare-set specialisation); the price of selection on structured carriers (rigid, cyclic, graph) or under the setwise stabiliser; WDP-CH03-P03; infinite-carrier cardinality; any physical or interpretive claim.'),
        'narrowest_claim': ('On a bare set of at least two points no point is invariant under all permutations, and in the pointwise-stabiliser model the minimal selecting declarations are exactly the single declared points '
                            '(price one declared point; price zero on a one-point carrier; no selection on the empty carrier); symmetry-price bookkeeping only.'),
        'next_test': ('On structured carriers compute the same selecting and minimal tables with Sym(X) replaced by an explicit automorphism group G (n-cycle with rotations, K4 graph with its automorphisms, a rigid carrier with trivial G) '
                      'and test whether the frontier is still the singletons: a rigid carrier must give price 0 and the n-cycle with rotations price 1; any other value falsifies the claim that the singleton frontier is generic.')}
    generators = [
        {'id': 'fully_invariant_point', 'source_declarations': [SYM + '::FullyInvariantPoint (line 12): definition'],
         'ordered_inputs': ['Carrier'], 'output': 'PointPredicate',
         'semantic_predicate': 'x is fixed by every permutation of the carrier.', 'hypotheses': [H]},
        {'id': 'stabiliser_invariant_points', 'source_declarations': ['no source declaration; new definition modelling WDP-CH03-D01 (ledger text only, no Lean/Rust declaration)'],
         'ordered_inputs': ['Carrier', 'DeclaredSet'], 'output': 'PointSet',
         'semantic_predicate': 'Points fixed by every permutation that fixes the declared set pointwise.', 'hypotheses': [H]},
        {'id': 'selecting_test', 'source_declarations': ['no source declaration; new definition'],
         'ordered_inputs': ['PointSet'], 'output': 'Verdict',
         'semantic_predicate': 'The declared set selects iff its invariant-point set is nonempty.', 'hypotheses': [H]},
        {'id': 'asymmetry_price_frontier', 'source_declarations': ['ledger WDP-CH03-D01 (definition; no Lean/Rust declaration) - this node fixes the pointwise-stabiliser reading'],
         'ordered_inputs': ['Carrier', 'Verdict'], 'output': 'DeclaredSetFamily',
         'semantic_predicate': 'Inclusion-minimal declared sets that select.', 'hypotheses': [H]}]
    relations = [
        {'id': 'no_fully_invariant_point', 'source_declarations': [SYM + '::no_fully_invariant_point (line 25): general theorem, proved by a swap; reproved here'],
         'equation_or_predicate': 'two distinct points imply no x with sigma x = x for all sigma', 'typing_conditions': 'Carrier with DecidableEq and Nontrivial',
         'evidence_status': 'Kernel theorem no_fully_invariant_point, no_fully_invariant_point_card; native tables for n=2..6 at S empty', 'scope': 'Every type with two distinct points'},
        {'id': 'invariant_points_characterisation', 'source_declarations': ['no source declaration; new general theorem'],
         'equation_or_predicate': 'x invariant under Stab(S) iff x in S or every point outside S equals x', 'typing_conditions': 'Carrier with DecidableEq',
         'evidence_status': 'Kernel theorem invariantUnder_iff; native brute-force tables for n=0..6', 'scope': 'Every type'},
        {'id': 'selecting_iff_nonempty', 'source_declarations': ['no source declaration; new general theorem'],
         'equation_or_predicate': 'S selects iff S nonempty or the carrier has exactly one point; with two distinct points iff S nonempty', 'typing_conditions': 'Carrier with DecidableEq',
         'evidence_status': 'Kernel theorems selecting_iff, selecting_iff_nonempty; native tables', 'scope': 'Every type'},
        {'id': 'frontier_is_singletons', 'source_declarations': ['no source declaration; new general theorem'],
         'equation_or_predicate': 'with two distinct points the minimal selecting sets are exactly the singletons, so there are card X of them', 'typing_conditions': 'Nontrivial carrier',
         'evidence_status': 'Kernel theorems minimalSelecting_iff_singleton, frontierEquiv, frontier_card (finite carriers); native frontier tables n=2..6', 'scope': 'Every type with two distinct points'},
        {'id': 'small_carrier_boundary', 'source_declarations': ['no source declaration; new boundary theorems'],
         'equation_or_predicate': 'one point: the empty declaration selects (price 0); no points: nothing selects', 'typing_conditions': 'Subsingleton nonempty carrier; empty carrier',
         'evidence_status': 'Kernel theorems one_point_empty_selects, empty_carrier_no_selection; native rows n=0, n=1', 'scope': 'Every such type'},
        {'id': 'dag_witness_is_fixed_instance', 'source_declarations': ['lean4/DerivationDagQMClosure.lean::pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed (line 1157): fixed instance, partly vacuous'],
         'equation_or_predicate': 'its first conjunct g (f true) = g (f false) holds by rfl for a constant f; its second shows only that x -> 1 - x has no fixed point on Fin 2, one involution, not Sym(X)-invariance; the rest is unrelated cochain/KKT arithmetic',
         'typing_conditions': 'Nat/Int arithmetic on fixed numbers', 'evidence_status': 'Read, not reused as support; replaced by the general kernel theorems above', 'scope': 'Fixed instance only'}]
    compositions = [
        {'outer_operation': 'selecting_test', 'input_slot': 0, 'inner_operation': 'stabiliser_invariant_points', 'colour_match': 'PointSet',
         'hypothesis_match': H, 'licensing_relations': ['invariant_points_characterisation', 'selecting_iff_nonempty'], 'evidence_status': 'Kernel and native'},
        {'outer_operation': 'asymmetry_price_frontier', 'input_slot': 1, 'inner_operation': 'selecting_test', 'colour_match': 'Verdict',
         'hypothesis_match': 'At least two points for the singleton form of the frontier.', 'licensing_relations': ['frontier_is_singletons'], 'evidence_status': 'Kernel and native'}]
    failed = [
        {'composition': 'selecting_test(stabiliser_invariant_points(X, empty set)) at card X >= 2', 'reason': 'Fails by no_fully_invariant_point: the empty declaration has no invariant point, so selection is not free.'},
        {'composition': 'asymmetry_price_frontier at card X = 1 read as singletons', 'reason': 'On one point the empty set already selects, so the frontier is {empty set} at price 0, not the singleton.'}]
    counterexamples = [
        {'id': 'two_point_complement', 'statement': 'n=2, S={0}: the complement {1} is a single point, so both points are invariant; the pattern for n>=3 (only declared points are invariant) fails.', 'scope': 'Instance of the characterisation theorem'},
        {'id': 'dag_witness_not_equivariance', 'statement': 'The attached local Lean witness proves x -> 1 - x has no fixed point on Fin 2 and g (f true) = g (f false) for constant f; neither is Sym(X)-invariance.', 'scope': 'Source reading; not a counterexample to the general theorem'}]
    return build_spec(
        node=NODE, short='wdp_protected_questions', lean='WdpProtectedQuestions',
        anchors=['WdpProtectedQuestions.no_fully_invariant_point', 'WdpProtectedQuestions.no_fully_invariant_point_card',
                 'WdpProtectedQuestions.invariantUnder_iff', 'WdpProtectedQuestions.selecting_iff', 'WdpProtectedQuestions.selecting_iff_nonempty',
                 'WdpProtectedQuestions.minimalSelecting_iff_singleton', 'WdpProtectedQuestions.frontierEquiv', 'WdpProtectedQuestions.frontier_card',
                 'WdpProtectedQuestions.one_point_empty_selects', 'WdpProtectedQuestions.empty_carrier_no_selection', 'WdpProtectedQuestions.bool_instance'],
        cases=list(producer.CASES), public_tsv=producer.public_tsv(), data=producer.certificate(),
        scope_review=('Mined external Symmetry.lean (FullyInvariantPoint, no_fully_invariant_point: a general swap argument, not vacuous; no selection-function type or equivariance notion exists in it) and the local DAG witness '
                      'pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed, which is a fixed instance and partly vacuous (a constant function, the swap on Fin 2, unrelated KKT arithmetic). '
                      'The ledger D01 definition of the asymmetry-price frontier has no Lean/Rust declaration; it is modelled here by the pointwise stabiliser of a declared set, which is a modelling choice with a different quantifier pattern from D01 (minimal declarations producing invariance versus minimal input sets whose removal frees a symmetry). '
                      'The node proves the general theorem and the frontier characterisation in Lean and replays exact tables for carriers of size 0..6 with a brute-force permutation checker. '
                      'The bottleneck WDP-CH03-P03 (declare-then-assert one-item separation) stays unported.'),
        predicates=['Independent brute-force enumeration of all n! permutations fixing each declared subset pointwise (producer and Rust use different decompositions: closed form vs enumeration).',
                    'Minimality decided from the definition over all proper subsets.',
                    'Theorem-level consistency: for n>=2 the empty declaration never selects and the frontier is the singletons.',
                    'Exact cross-language (Python/Rust) wire equality and literal Lean axiom reports.'],
        boundary=boundary, generators=generators, relations=relations, compositions=compositions, failed_compositions=failed, counterexamples=counterexamples,
        open_obligations=['WDP-CH03-P03 declare-then-assert one-item separation has no Lean port.',
                          'Selecting/minimal tables on structured carriers (explicit automorphism groups) and under the setwise stabiliser.',
                          'Asymmetry-price frontier relative to an implementation class and dependency preorder (D01 full definition).',
                          'WDP-CH03-N01: whether retention, dynamics or observers exist is not decided by this obstruction.'],
        colour_meanings={'Carrier': 'Unstructured finite or arbitrary set with its full permutation group', 'DeclaredSet': 'Subset of the carrier fixed pointwise (declared input)',
                         'PointSet': 'Set of points invariant under the stabiliser of the declared set', 'Verdict': 'Selecting or not',
                         'DeclaredSetFamily': 'Family of inclusion-minimal selecting declared sets', 'PointPredicate': 'Predicate on points of the carrier'},
        depends_on_result=True, qualification='No fully invariant point on a bare set of at least two elements is kernel-checked (re-proved here); the asymmetry-price frontier is proved only in the pointwise-stabiliser modelling choice, not relative to an implementation class and dependency preorder.',
        challenge_plan='Coordinate mutants of every certificate leaf plus nine semantic near misses: empty declaration selects, complement singleton ignored, rigidification price, non-minimal marked minimal, one-point carrier pays a declaration, empty carrier selects, price zero at five points, setwise stabiliser table, rigid carrier price zero.',
        composition_tree=['selecting_test(stabiliser_invariant_points(X, S))', 'asymmetry_price_frontier(X, selecting_test(...))'],
        construction='Exact subset-mask tables for carriers of size 0..6; Lean proves the general statements over any type.',
        relation_evidence={'no_fully_invariant_point': 'Kernel theorem; native empty-declaration rows n=2..6 have no invariant point.',
                           'frontier_is_singletons': 'Kernel theorem; native frontier rows n=2..6.'})


if __name__ == '__main__':
    print(write_spec(HERE, NODE, spec()))
