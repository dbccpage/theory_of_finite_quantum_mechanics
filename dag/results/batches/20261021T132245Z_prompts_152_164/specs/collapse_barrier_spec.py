"""Build specs/PG-COLLAPSE-BARRIER.json from the producer and the node's reviewed claims."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp/batch_tools'))
from spec_builder import build_spec, write_spec  # noqa: E402

_s = importlib.util.spec_from_file_location('producer', ROOT / 'code/python/src/qm/pfp_collapse_barrier.py')
producer = importlib.util.module_from_spec(_s)
_s.loader.exec_module(producer)

NODE = 'PG-COLLAPSE-BARRIER'
EXT = 'omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean'
H = 'Carriers are arbitrary types in the Lean theorems and Fin n, Fin my, Fin mz in the native tables; no selection of the added tag.'


def spec():
    boundary = {
        'supports': ('Kernel-checked for arbitrary types in Type (universe 0): s factors through p only if s is constant on the fibres of p (collapsed_observation_barrier, re-proved as barrier); '
                     'the converse holds whenever the task codomain Z is inhabited and fails in the instance X empty, Y = Unit, Z empty; the exact criterion for every Z is fibre-constancy together with (Z inhabited or Y empty) (factors_iff_exact), and factoring through the image of p is unconditional (factorsImage_iff); '
                     'if s factors through a refined profile (p, t) then t separates every collapsed pair that s separates (tag_separates); for finite X, inhabited Z and a nonempty tag alphabet T, a tag with s factoring through (p, t) exists iff every profile fibre has at most card T distinct s values (tag_alphabet_iff; lower bound tag_card_lower_bound, existence tag_exists), '
                     'so the least nonempty alphabet is max(1, largest number of distinct s values in one fibre). Native: exhaustive tables for fifteen carrier-size triples (all profiles, all tasks, all factors g, and all tags t up to the first alphabet size that works; the tag test uses the fibre-constancy criterion, cross-checked against g-enumeration in the tests) with zero barrier exceptions and the exact histogram of least alphabet sizes. '
                     'In the histogram, key 0 means the empty alphabet works, which happens exactly for empty X (records (0,0,1) and (0,1,0)); record (2,0,2) has no profile at all and an empty histogram; for nonempty X the key is max(1, ...).'),
        'does_not_support': ('Which tag or instance is added (the node does not select one, and the paper only exhibits predicates under a supplied decoder); the barrier for the inscription strings of the Pre-Genesis paper; '
                             'infinite or non-function observation structures; universes above Type; any claim that an added tag exists in the physical or inscription regime; the source aggregate pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed, which is a bundle of fixed instances proved by rfl and decide.'),
        'narrowest_claim': ('For maps p : X -> Y and s : X -> Z, no function of p reproduces s as soon as one fibre of p contains two points with different s values; with Z inhabited this is the only obstruction, and for finite X a nonempty tag alphabet of size k recovers s through (p, t) exactly when every fibre has at most k distinct s values.'),
        'next_test': ('Confirm by exhaustive enumeration over the inscription strings <a>, <ab>, <aa> of the Pre-Genesis paper under the supplied decoder that the least tag alphabet equals the max-fibre value predicted by tag_alphabet_iff, and that the paper predicates "contains b" and "payload length > 1" achieve it.')}
    generators = [
        {'id': 'profile_map', 'source_declarations': [EXT + '::collapsed_observation_barrier (line 36; the report argument)', EXT + '::ReportImage (line 7; definition)'],
         'ordered_inputs': ['Datum'], 'output': 'Profile', 'semantic_predicate': 'A map p : X -> Y; two data are collapsed when p x = p y.', 'hypotheses': [H]},
        {'id': 'task_map', 'source_declarations': [EXT + '::collapsed_observation_barrier (line 36; the task argument)'],
         'ordered_inputs': ['Datum'], 'output': 'Answer', 'semantic_predicate': 'A map s : X -> Z, the protected answer required of each datum.', 'hypotheses': [H]},
        {'id': 'factor_through_profile', 'source_declarations': [EXT + '::collapsed_observation_barrier (line 36; the factor argument, a general theorem)', EXT + '::history_report_criterion (line 10; iff form on ReportImage, definition+theorem)'],
         'ordered_inputs': ['Profile'], 'output': 'Answer', 'semantic_predicate': 'g : Y -> Z with g (p x) = s x for all x.', 'hypotheses': [H]},
        {'id': 'refine_report', 'source_declarations': [EXT + '::refineReport (line 59; definition)', EXT + '::refine_preserves (line 61; rfl)', EXT + '::refine_separates (line 64; general theorem)'],
         'ordered_inputs': ['Profile', 'Tag'], 'output': 'Profile', 'semantic_predicate': '(p, t) : X -> Y x T; the first component is the old profile.', 'hypotheses': [H]},
        {'id': 'report_image', 'source_declarations': [EXT + '::ReportImage (line 7; definition)', EXT + '::history_factor_unique (line 26; uniqueness only on the image)'],
         'ordered_inputs': ['Profile'], 'output': 'ProfileImage', 'semantic_predicate': 'The subtype of Y hit by p; a factor is unique only there.', 'hypotheses': [H]}]
    relations = [
        {'id': 'collapsed_observation_barrier', 'source_declarations': [EXT + '::collapsed_observation_barrier (line 36; general theorem over arbitrary types)'],
         'equation_or_predicate': 'p x = p x\' and s x != s x\' imply no g with g . p = s', 'typing_conditions': 'Profile x Answer', 'evidence_status': 'Kernel theorem barrier (re-proved); native table has zero exceptions', 'scope': 'All types'},
        {'id': 'factoring_iff_fibre_constant', 'source_declarations': [EXT + '::history_report_criterion (line 10; stated on ReportImage, i.e. factoring through the image only; uses Classical.choice, axiom_report.txt line 2720)'],
         'equation_or_predicate': 'with Z inhabited: exists g with g . p = s iff s is constant on the fibres of p', 'typing_conditions': 'Nonempty Z; ImageFactor form unconditional',
         'evidence_status': 'Kernel theorems factors_iff_of_nonempty, factors_iff_exact, factorsImage_iff, factors_iff_fails_without_nonempty; native table', 'scope': 'All types in Type; boundary: empty Z'},
        {'id': 'tag_separates', 'source_declarations': [EXT + '::refine_separates (line 64; says only that a tag separating the pair separates the refined reports)'],
         'equation_or_predicate': 's factors through (p, t) implies t separates every collapsed pair that s separates', 'typing_conditions': 'Profile x Tag x Answer', 'evidence_status': 'Kernel theorem tag_separates (new, stronger direction)', 'scope': 'All types'},
        {'id': 'least_tag_alphabet', 'source_declarations': ['no source declaration; new general theorem'],
         'equation_or_predicate': 'exists t : X -> T with s factoring through (p, t) iff every fibre of p carries at most card T distinct s values (T inhabited)', 'typing_conditions': 'Finite X, T',
         'evidence_status': 'Kernel theorem tag_alphabet_iff (with tag_card_lower_bound, tag_exists); native histogram by tag enumeration', 'scope': 'Finite X, inhabited Z, nonempty T; empty X needs the empty alphabet in the native convention'},
        {'id': 'factor_unique_on_image_only', 'source_declarations': [EXT + '::history_factor_unique (line 26; uniqueness on ReportImage only, axiom_report.txt line 2719)'],
         'equation_or_predicate': 'number of (p, s, g) with g . p = s equals my^n * mz^my', 'typing_conditions': 'Fin n, Fin my, Fin mz', 'evidence_status': 'Native exact counts for fifteen triples; a factor is free off the image', 'scope': 'Listed triples'},
        {'id': 'aggregate_fixed_instances', 'source_declarations': ['lean4/DerivationDagQMClosure.lean::pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed (line 1157; a conjunction of rfl and decide instances: a constant f on Bool, 1 - x != x on Fin 2, three linear identities)'],
         'equation_or_predicate': 'fixed instances only; none is the barrier for arbitrary profile and task', 'typing_conditions': 'Fixed Nat and Int values', 'evidence_status': 'Source declaration, not used as support', 'scope': 'Fixed instance'}]
    compositions = [
        {'outer_operation': 'factor_through_profile', 'input_slot': 0, 'inner_operation': 'profile_map', 'colour_match': 'Profile', 'hypothesis_match': H,
         'licensing_relations': ['collapsed_observation_barrier', 'factoring_iff_fibre_constant'], 'evidence_status': 'Kernel and native'},
        {'outer_operation': 'factor_through_profile', 'input_slot': 0, 'inner_operation': 'refine_report', 'colour_match': 'Profile', 'hypothesis_match': 'The refined profile is itself a profile; the tag is chosen explicitly, never by the quotient.',
         'licensing_relations': ['tag_separates', 'least_tag_alphabet'], 'evidence_status': 'Kernel and native'}]
    failed = [{'composition': 'factor_through_profile of profile_map when one fibre holds two different task values', 'reason': 'No g exists (kernel barrier); native exceptions: 0.'},
              {'composition': 'factor_through_profile with empty X, one profile value and empty Z', 'reason': 'The fibre condition is vacuous but no g : Y -> Z exists, so "fibre-constant implies factors" needs Nonempty Z.'}]
    counterexamples = [{'id': 'collapsed_two_point', 'statement': 'p constant on Bool and s = id: no factor, and a one-valued tag cannot help; a two-valued tag does (two_point_no_factor, two_point_one_bit).', 'scope': 'Instance of barrier and tag_exists.'},
                       {'id': 'empty_task_codomain', 'statement': 'X empty, Y = Unit, Z empty: s is constant on fibres vacuously yet Factors fails (factors_iff_fails_without_nonempty).', 'scope': 'Boundary of factoring_iff_fibre_constant.'}]
    return build_spec(
        node=NODE, short='collapse_barrier', lean='CollapseBarrier',
        anchors=['CollapseBarrier.barrier', 'CollapseBarrier.factors_iff_of_nonempty', 'CollapseBarrier.factors_iff_exact', 'CollapseBarrier.factors_iff_fails_without_nonempty',
                 'CollapseBarrier.factorsImage_iff', 'CollapseBarrier.refine_separates', 'CollapseBarrier.tag_separates',
                 'CollapseBarrier.tag_card_lower_bound', 'CollapseBarrier.tag_exists', 'CollapseBarrier.tag_alphabet_iff', 'CollapseBarrier.two_point_one_bit', 'CollapseBarrier.two_point_no_factor'],
        cases=[list(c) for c in producer.CASES], public_tsv=producer.public_tsv(), data=producer.certificate(),
        scope_review=('The collection lists 0 operation candidates; mined by hand from 000_pre_genesis_to_mssn/lean4/Paper.lean (sha b0f6365df8): ReportImage (7), history_report_criterion (10), history_factor_unique (26), '
                      'collapsed_observation_barrier (36), refineReport (59), refine_preserves (61), refine_separates (64), and the local aggregate pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed (DerivationDagQMClosure.lean 1157). '
                      'collapsed_observation_barrier is a general, correct, nearly tautological theorem (s = g . p forces s constant on fibres of p). The aggregate local theorem is a conjunction of fixed instances, not the barrier. '
                      'The sharp content found: the converse holds when Z is inhabited and has the exact form fibre-constant and (Z inhabited or Y empty) (the source avoids this by factoring through ReportImage), the factor is unique only on the image, and for a nonempty tag alphabet the least size is the largest number of distinct task values in one fibre. '
                      'The node does not select the added tag; that stays open.'),
        predicates=['Independent closed-form counts: profiles with image size j are C(my,j)*Surj(n,j); tasks constant on fibres are mz^j each.',
                    'Triples (p, s, g) with g.p = s equal my^n * mz^my because every (p, g) fixes s.',
                    'Least tag alphabet size recomputed as 0 for empty X and otherwise the largest number of distinct task values in one fibre (at least 1), never by enumerating tags.',
                    'Barrier has zero exceptions and factoring never exceeds fibre-constancy; Z-empty boundary row has fibre-constant 1 and factoring 0.',
                    'Exact cross-language (Python/Rust) wire equality and literal Lean axiom reports.'],
        boundary=boundary, generators=generators, relations=relations, compositions=compositions, failed_compositions=failed, counterexamples=counterexamples,
        open_obligations=['Select or derive the added tag for a given regime (the node does not).', 'Apply the max-fibre formula to the inscription strings and decoder of the Pre-Genesis paper.',
                          'Infinite carriers and non-function observation structures.'],
        colour_meanings={'Datum': 'Element of the carrier X', 'Profile': 'Map p : X -> Y (the collapsed observation quotient)', 'Answer': 'Map s : X -> Z (the protected task)',
                         'Tag': 'Added map t : X -> T outside the quotient', 'ProfileImage': 'Subtype of Y hit by p'},
        depends_on_result=True,
        qualification='Equal profiles block every function of the quotient; the converse holds for an inhabited task codomain (exact form: fibre-constant and (Z inhabited or Y empty)); a tag alphabet of size k recovers the task iff every fibre has at most k distinct task values; the node does not choose the added tag, and the paper-level string predicates are not re-derived here; the DAG-cited aggregate theorem consists of fixed instances and is not the barrier.',
        challenge_plan='Coordinate mutants of every certificate leaf plus eleven semantic near misses: empty-codomain iff, barrier exception, one-bit-always-suffices, tag-never-helps, unique factorisation, swapped roles, injective profile collapsing, alphabet as global distinct count, alphabet as fibre size, off-by-one alphabet, empty-carrier convention.',
        composition_tree=['factor_through_profile(profile_map(x))', 'factor_through_profile(refine_report(profile_map, tag))'],
        construction='Exhaustive enumeration of all profiles, tasks, factors and tags on Fin n carriers; Lean proves the general statements.',
        relation_evidence={'collapsed_observation_barrier': 'Kernel theorem barrier; native zero exceptions on fifteen carrier triples.', 'least_tag_alphabet': 'Kernel tag_alphabet_iff; native histogram.'})


if __name__ == '__main__':
    print(write_spec(HERE, NODE, spec()))
