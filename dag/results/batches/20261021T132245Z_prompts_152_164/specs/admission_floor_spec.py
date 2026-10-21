"""Build specs/PG-ADMISSION-FLOOR.json from the producer and the node's reviewed claims."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp/batch_tools'))
from spec_builder import build_spec, write_spec  # noqa: E402

_s = importlib.util.spec_from_file_location('producer', ROOT / 'code/python/src/qm/pfp_admission_floor.py')
producer = importlib.util.module_from_spec(_s)
_s.loader.exec_module(producer)

NODE = 'PG-ADMISSION-FLOOR'
WDP = 'omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/'
PAF = WDP + 'PrimitiveAdmissionFloor.lean'
PTR = WDP + 'PointedRelation.lean'
H = 'The cut law (irreflexivity of the relation) is supplied data, not selected from equality or derived from <> or Real_0; carriers are arbitrary types in Lean and Fin n in the native tables.'


def spec():
    boundary = {
        'supports': ('Kernel-checked for arbitrary carriers: an exhibited cut has distinct endpoints, a cut exists on V iff V has two distinct points, no cut exists on a subsingleton, a map carrying the relation into an irreflexive target separates the endpoints and (sharper) such a target exists iff the map separates every related pair; '
                     'instance-without-law and law-without-instance exist, and the three pointed-relation facts hold. Native: every relation on 0..4 points (65536 at n=4) tabulated by cut data, law, instance and the four related/equal quadrants, and every irreflexive relation, map and target on 1..3 points, all matching closed forms with zero exceptions.'),
        'does_not_support': ('Deriving the law (irreflexivity) from the primitive difference <> or from Real_0: the relation and its law remain supplied data; any selection of a preferred cut or orientation (two orientations exist on two points); '
                             'infinite carriers beyond the Lean statements; the arity-cost tie-breaker of the source (declared_arity_cost_selects is a decide on a priced toy, not used here); the aggregate local theorem pg_to_sn_and_wdp_route_chain_composition, which is a fixed enumeration.'),
        'narrowest_claim': ('A law-bearing cut (an irreflexive relation with an exhibited pair) exists exactly on carriers with two distinct points, its endpoints are apart, and a map separates the endpoints of every cut it carries into an irreflexive target; the pair of marks alone does not supply the relation or its law.'),
        'next_test': ('Replay the admission-floor model counts on 1..4 points with the declared Real_0 axiom list added as constraints and decide whether any declared axiom forces irreflexivity of the relation, i.e. whether the counts of relations with an exhibited pair but no law drop to zero.')}
    generators = [
        {'id': 'exhibited_cut', 'source_declarations': [PAF + '::ExhibitedCut (line 7; definition: relation, first, second, exhibited, protectedLaw)'],
         'ordered_inputs': ['Carrier', 'Relation', 'Endpoint', 'Endpoint'], 'output': 'Cut', 'semantic_predicate': 'R a b holds and forall x, not R x x holds; both supplied.', 'hypotheses': [H]},
        {'id': 'endpoint_apartness', 'source_declarations': [PAF + '::endpoints_apart (line 14; general theorem)'],
         'ordered_inputs': ['Cut'], 'output': 'Apartness', 'semantic_predicate': 'first != second.', 'hypotheses': [H]},
        {'id': 'quotient_map', 'source_declarations': [PAF + '::identification_breaks_law (line 23; general theorem, quantifies a map q and an irreflexive target)'],
         'ordered_inputs': ['Cut', 'Map', 'TargetRelation'], 'output': 'Apartness', 'semantic_predicate': 'q preserves R into an irreflexive target implies q first != q second.', 'hypotheses': [H]},
        {'id': 'pointed_relation', 'source_declarations': [PTR + '::pointed_relation_independence (line 84; general theorem over Type u)', PTR + '::self_loop_countermodel, empty_two_countermodel (lines 36, 44)'],
         'ordered_inputs': ['Carrier', 'Relation', 'Endpoint', 'Endpoint'], 'output': 'RelatednessDistinctness', 'semantic_predicate': 'The pair (R a b, a != b) as two independent booleans unless R is irreflexive.', 'hypotheses': [H]}]
    relations = [
        {'id': 'endpoints_apart', 'source_declarations': [PAF + '::endpoints_apart (line 14; general)'],
         'equation_or_predicate': 'R a b and forall x, not R x x imply a != b', 'typing_conditions': 'Cut', 'evidence_status': 'Kernel theorem endpoints_apart (re-proved); native irreflexive_related_equal = 0', 'scope': 'All types'},
        {'id': 'no_cut_on_subsingleton', 'source_declarations': [PAF + '::no_cut_on_subsingleton (line 20; general)'],
         'equation_or_predicate': 'Subsingleton V implies no cut on V; sharper: a cut exists iff V is nontrivial', 'typing_conditions': 'Carrier', 'evidence_status': 'Kernel theorems no_cut_on_subsingleton and cut_exists_iff_nontrivial; native cut counts 0 at n=0,1', 'scope': 'All types'},
        {'id': 'identification_breaks_law', 'source_declarations': [PAF + '::identification_breaks_law (line 23; general, one direction only)'],
         'equation_or_predicate': 'q carries R into an irreflexive target iff q separates every R-related pair', 'typing_conditions': 'Cut x Map', 'evidence_status': 'Kernel theorems identification_breaks_law (source direction) and exists_law_target_iff (converse, new); native identify tables', 'scope': 'All types; native n=1..3'},
        {'id': 'instance_law_independence', 'source_declarations': [PAF + '::instance_without_law_allows_singleton (line 33), law_without_instance_allows_singleton (line 37); both stated only on Unit'],
         'equation_or_predicate': 'On every carrier the total relation is an instance without law and the empty relation a law without instance', 'typing_conditions': 'Carrier', 'evidence_status': 'Kernel theorems instance_without_law, law_without_instance (generalised from Unit); native counts', 'scope': 'All types'},
        {'id': 'pointed_relation_independence', 'source_declarations': [PTR + '::pointed_relation_independence (line 84; general over Type u)'],
         'equation_or_predicate': 'related does not imply distinct; distinct does not imply related; irreflexive and related imply distinct', 'typing_conditions': 'Carrier x Relation x Endpoints', 'evidence_status': 'Kernel theorem pointed_relation_independence (Type 0 re-proof); native quadrant counts', 'scope': 'Type 0 in Lean'},
        {'id': 'law_not_derived_from_distinctness', 'source_declarations': ['no source declaration; new general theorem (the source states the node bottleneck in prose only)'],
         'equation_or_predicate': 'For a != b, a relation leaves a, b unrelated and law-bearing, and another relates them without the law', 'typing_conditions': 'Carrier with two distinct points', 'evidence_status': 'Kernel theorem law_not_derived_from_distinctness; native tables n>=2', 'scope': 'All types'},
        {'id': 'aggregate_fixed_enumeration', 'source_declarations': ['lean4/DerivationDagQMClosure.lean::pg_to_sn_and_wdp_route_chain_composition (line 1257; a conjunction of Nat identities and decide instances, including c0 < c1 < c2 implies c0 != c2)'],
         'equation_or_predicate': 'fixed finite enumeration; not the cut theorem', 'typing_conditions': 'Fixed Nat and Fin 3 values', 'evidence_status': 'Source declaration, not used as support', 'scope': 'Fixed instance'}]
    compositions = [
        {'outer_operation': 'endpoint_apartness', 'input_slot': 0, 'inner_operation': 'exhibited_cut', 'colour_match': 'Cut', 'hypothesis_match': H,
         'licensing_relations': ['endpoints_apart', 'no_cut_on_subsingleton'], 'evidence_status': 'Kernel and native'},
        {'outer_operation': 'quotient_map', 'input_slot': 0, 'inner_operation': 'exhibited_cut', 'colour_match': 'Cut', 'hypothesis_match': 'The map and its irreflexive target are supplied; the converse holds iff the map separates the related pairs.',
         'licensing_relations': ['identification_breaks_law'], 'evidence_status': 'Kernel and native'}]
    failed = [{'composition': 'exhibited_cut built from two marks and a pointed relation without the law', 'reason': 'Relatedness does not give distinctness (self-loop) and distinctness does not give relatedness (empty relation); the law field is not produced by pointed_relation (kernel pointed_relation_independence, native quadrants).'},
              {'composition': 'exhibited_cut on a subsingleton carrier', 'reason': 'Needs two distinct endpoints; none exist (kernel no_cut_on_subsingleton, native 0 cuts at n=0,1).'}]
    counterexamples = [{'id': 'self_loop_one_point', 'statement': 'The total relation on one point relates the point to itself, so relatedness does not imply distinctness and the instance has no law.', 'scope': 'n = 1, native related_equal = 1.'},
                       {'id': 'empty_relation_two_points', 'statement': 'The empty relation on two points leaves distinct points unrelated; it is a law without instance.', 'scope': 'n = 2.'}]
    return build_spec(
        node=NODE, short='admission_floor', lean='AdmissionFloor',
        anchors=['AdmissionFloor.endpoints_apart', 'AdmissionFloor.no_cut_on_subsingleton', 'AdmissionFloor.identification_breaks_law',
                 'AdmissionFloor.cut_exists_iff_nontrivial', 'AdmissionFloor.exists_law_target_iff', 'AdmissionFloor.instance_without_law',
                 'AdmissionFloor.law_without_instance', 'AdmissionFloor.law_not_derived_from_distinctness',
                 'AdmissionFloor.pointed_relation_independence', 'AdmissionFloor.two_point_cut_count', 'AdmissionFloor.one_point_cut_count'],
        cases=[list(c) for c in producer.CASES], public_tsv=producer.public_tsv(), data=producer.certificate(),
        scope_review=('Read PrimitiveAdmissionFloor.lean (sha df9d149bbd06, Core Lean, no Mathlib) and PointedRelation.lean (sha 2d36b5427b54): the cut theorems are general and correct (apartness, subsingleton refusal, identification) '
                      'but the instance/law singleton theorems are stated only on Unit, and pointed_relation_independence is over Type u with the third clause needing irreflexivity. The local aggregate (DerivationDagQMClosure.lean line 1257) is a fixed enumeration. '
                      'Re-proved all of them for arbitrary carriers and added: cut existence iff two distinct points, the exact converse of identification_breaks_law, and law-from-distinctness independence on every nontrivial carrier. '
                      'The law is supplied: the node (as the DAG bottleneck says) does not derive it from <> or Real_0 and neither does this bundle.'),
        predicates=['Independent closed forms: 2^(n^2) relations, 2^(n^2-n) law-bearing, exhibited cuts n(n-1)2^(n^2-n-1), quadrants n 2^(n^2-1) and n(n-1) 2^(n^2-1).',
                    'Targets carrying R along q counted as sum over q of 2^(n^2 - sum of squared fibre sizes of q) (subsets of separated pairs), not by enumerating targets.',
                    'Apartness (irreflexive_related_equal = 0), no cut at n<=1, identification overlap = 0 and the complementarity rq_with_target + rq_identifying = rq_pairs.',
                    'Exact cross-language (Python/Rust) wire equality and literal Lean axiom reports.'],
        boundary=boundary, generators=generators, relations=relations, compositions=compositions, failed_compositions=failed, counterexamples=counterexamples,
        open_obligations=['Derive (or refuse to derive) the law from the primitive difference <> and Real_0.', 'Select a preferred orientation among the two cuts on a two-point carrier.',
                          'Priced arity tie-breaker (declared_arity_cost_selects) is a declared toy, not covered.'],
        colour_meanings={'Carrier': 'Type V of marks', 'Relation': 'Binary relation R on V', 'Endpoint': 'Marked point of V', 'Cut': 'Relation, endpoints, R first second and irreflexivity law',
                         'Map': 'q : V -> W', 'TargetRelation': 'Binary relation on W', 'Apartness': 'Proposition first != second', 'RelatednessDistinctness': 'Pair of independent facts R a b and a != b'},
        depends_on_result=False,
        challenge_plan='Coordinate mutants of every certificate leaf plus seven semantic near misses: relatedness implies distinctness, distinctness implies relatedness, cut on a subsingleton, law requires instance, instance forces law, identification preserves the law, separation does not suffice.',
        composition_tree=['endpoint_apartness(exhibited_cut)', 'quotient_map(exhibited_cut, map, target)'],
        construction='Bitmask enumeration of every relation on 0..4 points and every (irreflexive relation, map, irreflexive target) on 1..3 points; Lean proves the general statements.',
        relation_evidence={'identification_breaks_law': 'Kernel both directions; native overlap 0 and complementarity on n=1..3.', 'pointed_relation_independence': 'Kernel; native quadrant counts for n<=4.'})


if __name__ == '__main__':
    print(write_spec(HERE, NODE, spec()))
