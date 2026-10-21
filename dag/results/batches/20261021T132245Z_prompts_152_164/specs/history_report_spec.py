"""Build specs/PG-HISTORY-REPORT-CRITERION.json from the producer and the node's reviewed claims."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp/batch_tools'))
from spec_builder import build_spec, write_spec  # noqa: E402

_s = importlib.util.spec_from_file_location('producer', ROOT / 'code/python/src/qm/pfp_history_report.py')
producer = importlib.util.module_from_spec(_s)
_s.loader.exec_module(producer)

NODE = 'PG-HISTORY-REPORT-CRITERION'
H = 'Histories, reports and answers are arbitrary types in Lean and the finite sets {0..h-1}, {0..v-1}, {0..s-1} natively; the answer is a total function of the history; the image is the actual image of the report (no extension to unused reports).'
SRC = 'omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/'
PAPER = SRC + '000_pre_genesis_to_mssn/lean4/Paper.lean'
BRIDGE = SRC + '000_witnessed_difference_programme/lean4/WitnessedDifference/ProposalAdmissionBridge.lean'
DESCENT = SRC + '000_witnessed_difference_programme/lean4/WitnessedDifference/Descent.lean'
P001 = SRC + '001_sn_mssn/lean4/Paper001.lean'


def spec():
    boundary = {
        'supports': ('For arbitrary types H, V, S (kernel-checked, lean4/HistoryReport.lean): factoring through the report image implies constancy on report fibers without any axiom; '
                     'constancy on fibers implies factoring when a selector of a history in every nonempty fiber is supplied as a hypothesis, again without any axiom, and for an arbitrary report the selector is obtained from Classical.choice '
                     '(the kernel reports Classical.choice for selector_exists and for the unconditional criterion, Quot.sound for uniqueness on the image via funext); the factor is unique on the image; two histories with one report and two answers refute factoring; '
                     'off the image the extension to all reports is not unique under the hypotheses of off_image_not_unique: DecidableEq of the report type, an off-image point v0, an extension f, and a value s different from f v0 (so at least two answers); for a surjective report the extension is unique. '
                     'Exhaustive native check over ALL report and question functions for 16 small (h,v,s) triples including empty and degenerate ones (including h=0, v=2, s=0 where the empty question factors through the empty image but has no extension): factoring equals fiber constancy pair by pair, '
                     'factoring counts equal sum_k C(v,k) k! S2(h,k) s^k (recomputed independently of the enumeration, with the fiber-constant count recomputed separately from set partitions), every factoring pair has exactly one factor on the image and s^(v-k) extensions. '
                     'The finite native check is combinatorial corroboration only and is insensitive to the choice question, since choice is provable on finite types.'),
        'does_not_support': ('Necessity of a selector or of Classical.choice for the direction constancy => factoring (this node proves no independence or unprovability result; the selector is a hypothesis, not a construction); '
                             'the constructive listed-history reconstruction (node PG-PREGEN-CONSTRUCTIVE-SUMMARY); any structure on H, V or S, probability, measurement or physical interpretation of reports.'),
        'narrowest_claim': ('For arbitrary types, an answer factors through the report image iff it is constant on report fibers, uniquely on the image; the direction constancy => factoring is proved from a selector of fiber representatives (a hypothesis, axiom-free) '
                            'and, for an arbitrary report, with Classical.choice; necessity of a selector or of choice is not shown; verified exhaustively on 16 small function-space triples.'),
        'next_test': ('Decide whether constancy on fibers => factoring through the image is provable without Classical.choice for an arbitrary history type (prove it, or give a choice-free model in which a fiber-constant question fails to factor), '
                      'beyond the selector hypothesis proved here and the listed-history version of node 166.')}
    generators = [
        {'id': 'report_image', 'source_declarations': [PAPER + '::ReportImage (line 7, definition)', BRIDGE + '::ReportImage (line 13, definition)'],
         'ordered_inputs': ['ReportMap'], 'output': 'ImageType', 'semantic_predicate': 'The subtype of the report type of values actually reported by some history.', 'hypotheses': [H]},
        {'id': 'fiber_constant', 'source_declarations': [DESCENT + '::FiberConstant (line 25, definition)', BRIDGE + '::FiberConstant (line 19, definition)'],
         'ordered_inputs': ['ReportMap', 'QuestionMap'], 'output': 'Verdict', 'semantic_predicate': 'Equal reports imply equal answers on every pair of histories.', 'hypotheses': [H]},
        {'id': 'factor_through_image', 'source_declarations': [BRIDGE + '::FactorsOnImage (line 23, definition)', DESCENT + '::FactorsThrough (line 31, definition; presentation map, not the image)'],
         'ordered_inputs': ['ReportMap', 'QuestionMap'], 'output': 'FactorMap', 'semantic_predicate': 'A map g from the image to the answers with g(report h) = answer h for every history.', 'hypotheses': [H]},
        {'id': 'fiber_selector', 'source_declarations': [PAPER + '::history_report_criterion (line 10; the Classical.choose at line 22 is the selector)', P001 + '::exists_descent_of_constant (line 531; Classical.choose at line 534)'],
         'ordered_inputs': ['ReportMap'], 'output': 'Selector', 'semantic_predicate': 'A history reporting each image point; the only place the choice axiom enters.', 'hypotheses': [H]},
        {'id': 'extend_off_image', 'source_declarations': ['no source declaration; the sources state factorization on the actual image only (ProposalAdmissionBridge.lean header lines 3-8)'],
         'ordered_inputs': ['FactorMap', 'ReportMap'], 'output': 'ExtensionSet', 'semantic_predicate': 'The maps f from all reports to answers with f(report h) = answer h; a torsor under free values at unreported points.', 'hypotheses': [H]}]
    relations = [
        {'id': 'factors_implies_fiber_constant', 'source_declarations': [PAPER + '::history_report_criterion (line 10, mp branch lines 16-19; general theorem)', BRIDGE + '::factorization_iff_fiber_constancy (line 27, general theorem)'],
         'equation_or_predicate': 'FactorsOnImage report answer => FiberConstant report answer', 'typing_conditions': 'ReportMap x QuestionMap', 'evidence_status': 'Kernel theorem fiberConstant_of_factors (no axioms); native table',
         'scope': 'Arbitrary types'},
        {'id': 'fiber_constant_implies_factors', 'source_declarations': [PAPER + '::history_report_criterion (line 10, mpr branch lines 20-24; general theorem using Classical.choose)'],
         'equation_or_predicate': 'FiberConstant report answer and a selector => FactorsOnImage report answer; without a hypothesis the selector is Classical.choice', 'typing_conditions': 'ReportMap x QuestionMap (x Selector)',
         'evidence_status': 'Kernel theorems factors_of_fiberConstant_of_selector (no axioms), selector_exists and history_report_criterion (Classical.choice); native table', 'scope': 'Arbitrary types'},
        {'id': 'factor_unique_on_image', 'source_declarations': [PAPER + '::history_factor_unique (line 26, general theorem)', P001 + '::descent_unique (line 545, general theorem)'],
         'equation_or_predicate': 'two factors through the image of the same question are equal', 'typing_conditions': 'FactorMap x FactorMap', 'evidence_status': 'Kernel theorem factor_unique_on_image (Quot.sound via funext); native max multiplicity 1',
         'scope': 'Arbitrary types'},
        {'id': 'split_refutes_factoring', 'source_declarations': [PAPER + '::collapsed_observation_barrier (line 36, general theorem)', BRIDGE + '::equal_report_opposite_decision_no_decoder (line 46, general theorem)'],
         'equation_or_predicate': 'report h = report h and answer h != answer h implies no factor', 'typing_conditions': 'ReportMap x QuestionMap', 'evidence_status': 'Kernel theorem not_factors_of_split (no axioms); native table',
         'scope': 'Arbitrary types'},
        {'id': 'off_image_extension_not_unique', 'source_declarations': ['no source declaration; new boundary theorem'],
         'equation_or_predicate': 'v0 not in the image, s != f v0 implies a second extension; surjective report implies a unique extension', 'typing_conditions': 'ExtensionSet; decidable equality of reports for the first half',
         'evidence_status': 'Kernel theorems off_image_not_unique (no axioms), extension_unique_of_surjective (Quot.sound); native extension counts', 'scope': 'Arbitrary types'}]
    compositions = [
        {'outer_operation': 'factor_through_image', 'input_slot': 0, 'inner_operation': 'fiber_selector', 'colour_match': 'Selector -> FactorMap',
         'hypothesis_match': 'The factor is built as g v = answer (selector v); fiber constancy transports the selector to every history.',
         'licensing_relations': ['fiber_constant_implies_factors'], 'evidence_status': 'Kernel and native'},
        {'outer_operation': 'extend_off_image', 'input_slot': 0, 'inner_operation': 'factor_through_image', 'colour_match': 'FactorMap -> ExtensionSet',
         'hypothesis_match': 'An extension needs a value at every unreported point; none is forced.',
         'licensing_relations': ['off_image_extension_not_unique', 'factor_unique_on_image'], 'evidence_status': 'Kernel and native'}]
    failed = [{'composition': 'fiber_selector for an arbitrary report without the choice axiom', 'reason': 'Not composable in this development: the selector is a hypothesis or Classical.choice. No unprovability result is proved here; whether a choice-free selector exists for an arbitrary history type is the next obligation.'},
              {'composition': 'extend_off_image with a unique result when the report is not surjective', 'reason': 'Fails whenever an unreported point exists and the answer type has two elements (kernel off_image_not_unique; native nonunique counts).'}]
    counterexamples = [{'id': 'h_mod_2_answer_h', 'statement': 'Three histories 0,1,2 with report h mod 2 and answer h: histories 0 and 2 share report 0 with answers 0 and 2, so the answer is not fiber constant and does not factor.', 'scope': 'Instance of not_factors_of_split (Lean instance_split).'},
                       {'id': 'two_extensions_same_factor', 'statement': 'h=1, v=2, s=2: the question 0 over one history reporting 0 factors uniquely through the image {0}, but has two extensions to V={0,1}.', 'scope': 'Instance of off_image_not_unique; native row 1 2 2 has nonunique count 4 of 4 factoring pairs.'}]
    return build_spec(
        node=NODE, short='history_report', lean='HistoryReport',
        anchors=['HistoryReport.fiberConstant_of_factors', 'HistoryReport.factors_of_fiberConstant_of_selector', 'HistoryReport.selector_exists',
                 'HistoryReport.history_report_criterion', 'HistoryReport.factor_unique_on_image', 'HistoryReport.not_factors_of_split',
                 'HistoryReport.off_image_not_unique', 'HistoryReport.extension_unique_of_surjective', 'HistoryReport.instance_split'],
        cases=[list(c) for c in producer.CASES], public_tsv=producer.public_tsv(), data=producer.certificate(),
        scope_review=('The source declares the criterion for arbitrary types (Paper.lean history_report_criterion, history_factor_unique) and its variants (ProposalAdmissionBridge, Descent with surjectivity, Paper001 descent). '
                      'The source statement is general and correct; its mpr direction uses Classical.choose exactly to select a representative of each fiber. This node re-derives the criterion, isolates the selector as a hypothesis (axiom-free) '
                      'and records the kernel axiom report of each direction, adds the off-image non-uniqueness and surjective uniqueness boundary, and checks all report/question function pairs on 16 finite triples. The constructive listed version is the sibling node 166. The Rust FactorizationCertificate (code/rust/src/category_theory/finite_report_query.rs line 151, flagged for re-review after upstream restoration) was re-read: on enumerated carriers it stores the realized image, a decoder and an explicit representative map (the selector as data) next to a Collision alternative, a finite certificate of the same dichotomy, not the general theorem.'),
        predicates=['Exact closed-form counts of reports with image size k (surjections via Stirling numbers of the second kind), recomputed without enumerating functions.',
                    'Fiber-constant count recomputed separately from set partitions (restricted growth strings) and compared with the factoring count; mismatch = difference of the two counts (every factoring pair is fiber constant).',
                    'Total extensions to V equal v^h s^v and a factoring pair is non-unique off the image exactly when s^(v-k) >= 2.',
                    'Exact cross-language (Python/Rust) wire equality and literal Lean axiom reports.'],
        boundary=boundary, generators=generators, relations=relations, compositions=compositions, failed_compositions=failed, counterexamples=counterexamples,
        open_obligations=['Choice-freedom (or independence) of constancy => factoring for an arbitrary history type.', 'Listed-history constructive version (node PG-PREGEN-CONSTRUCTIVE-SUMMARY).',
                          'Any structure on histories, reports or answers; probability, measurement or physical reading of reports.'],
        colour_meanings={'ReportMap': 'Function from histories to reports', 'QuestionMap': 'Function from histories to answers', 'ImageType': 'Subtype of reports actually reported',
                         'FactorMap': 'Function from the image to answers', 'Selector': 'Function choosing a history in each fiber of the image', 'Verdict': 'Proposition (constant on fibers or not)',
                         'ExtensionSet': 'Functions from all reports to answers agreeing with the question'},
        depends_on_result=True, qualification='The clause that a constructive listed-history version is not established is stale (node PG-PREGEN-CONSTRUCTIVE-SUMMARY proves a choice-free listed version); for an arbitrary history type the fiber-constant-to-factor direction is proved here using a selector of fiber representatives, with no independence from Classical.choice shown.',
        challenge_plan='Coordinate mutants of every certificate leaf plus ten semantic near misses: every question factors, injective reports only, unique extension off the image, surjective report with freedom, image confused with codomain, criterion failing on a pair, two factors on the image, empty histories refused, a coarser kernel than each report own kernel, empty answers extending uniquely.',
        composition_tree=['factor_through_image(fiber_selector(report))', 'extend_off_image(factor_through_image(report, answer), report)'],
        construction='Exhaustive enumeration of all reports H -> V and questions H -> S with direct search for factors on the image and extensions to V; Lean proves the general criterion and records axiom bills.',
        relation_evidence={'fiber_constant_implies_factors': 'Kernel: selector hypothesis no axioms; arbitrary report Classical.choice. Native: equality of counts on 16 triples.',
                           'off_image_extension_not_unique': 'Kernel theorem; native nonunique counts equal sum over k with s^(v-k)>=2.'})


if __name__ == '__main__':
    print(write_spec(HERE, NODE, spec()))
