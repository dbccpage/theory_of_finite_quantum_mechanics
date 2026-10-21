"""Build specs/PG-PREGEN-CONSTRUCTIVE-SUMMARY.json from the producer and the node's reviewed claims."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp/batch_tools'))
from spec_builder import build_spec, write_spec  # noqa: E402

_s = importlib.util.spec_from_file_location('producer', ROOT / 'code/python/src/qm/pfp_pregen_constructive.py')
producer = importlib.util.module_from_spec(_s)
_s.loader.exec_module(producer)

NODE = 'PG-PREGEN-CONSTRUCTIVE-SUMMARY'
H = ('A listing is any finite list of histories (repeats allowed); reports have decidable equality; the answer is a total function of the history; '
     'the criterion is relative to the listed histories only. Natively: histories {0..p-1}, reports {0..v-1}, answers {0..s-1}.')
LHS = 'omega_engine_education/documentation/000_oepregen/lean4/ListedHistorySummary.lean'  # external file named by the operad bindings; not part of the gated evidence
PAPER = 'omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean'
WIT = 'omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs'


def spec():
    boundary = {
        'supports': ('Own re-derivation (lean4/PregenConstructive.lean, structural recursion) over a list of histories with DecidableEq reports: first-match reconstruction recon returns every listed answer iff the answer is constant on report fibers among the listed histories; '
                     'recon is none exactly on unreported values; any f returning the listed answers agrees with recon on listed reports; a complete listing plus global fiber constancy gives the factor through the report image (the choice-free bridge to node 163); '
                     'with an unlisted history of a listed report and a different answer, recon returns the listed answer, which is then wrong. The kernel reports NO axioms at all for the seven general theorems recon_of_fiberConstant, fiberConstantOn_of_recon, listed_history_report_criterion, recon_eq_none_iff, recon_unique, recon_wrong_off_list and listed_factor_exists (relative to the supplied DecidableEq instance on reports); '
                     'the instance anchors report at most propext (instance_wrong_off_list and instance_not_fiberConstant: propext); the variant for a report type without decidable equality (instance from Classical.propDecidable) reports propext, Classical.choice, Quot.sound for that proof term. '
                     'The external ListedHistorySummary.lean is not in this repository and was not part of the gated evidence; all kernel claims are for the in-repo re-derivation PregenConstructive. '
                     'Exhaustive native check over ALL listings of length <= ell (repeats included), all reports and all answers for 11 non-degenerate tuples (p >= 1, v >= 1, s >= 1) and 4 degenerate boundary tuples (p = 0, or v = 0 or s = 0, where there is at most one triple): recon correct on every listed history iff listed fiber constant, zero mismatches; complete listings agree with the global criterion; '
                     'partial_false_positive = triples on a non-complete listing that are listed-fiber-constant but not globally fiber-constant; unlisted_refused/correct/wrong = quadruples (listing, report, answer, unlisted history) whose triple is listed-fiber-constant, classified by what recon returns for the unlisted history.'),
        'does_not_support': ('Report types without decidable equality (only the classical instance is covered, its proof term uses Classical.choice, and necessity of choice there is not shown); infinite or unlisted populations beyond the explicit complete-listing hypothesis; '
                             'the unconditional factorization for an arbitrary history type (node PG-HISTORY-REPORT-CRITERION); the external ListedHistorySummary.lean (not in this repository); any probability, measurement or physical reading of reports.'),
        'narrowest_claim': ('Over an explicit listing with decidable report equality, first-match reconstruction returns every listed answer iff the answer is constant on the listed report fibers, '
                            'with no axiom in the kernel for the seven general theorems (relative to the supplied DecidableEq instance on reports); off the listing it refuses unreported values and can be wrong on unlisted histories; verified exhaustively on 11 non-degenerate small tuples.'),
        'next_test': ('Decide whether the listed criterion survives a report type without decidable equality by a choice-free substitute for the first-match search, '
                      'or show that the Classical.propDecidable instance is unavoidable there (a choice-free model or an independence argument).')}
    generators = [
        {'id': 'listing', 'source_declarations': [LHS + '::hs : List H (explicit parameter of every theorem, e.g. line 37 recon, line 116 recon_of_fiberConstant)'],
         'ordered_inputs': ['HistoryType'], 'output': 'Listing', 'semantic_predicate': 'A finite list of histories; repeats and any order allowed.', 'hypotheses': [H]},
        {'id': 'first_match_recon', 'source_declarations': [LHS + '::recon (line 37, definition via List.find?)'],
         'ordered_inputs': ['Listing', 'ReportMap', 'QuestionMap', 'ReportValue'], 'output': 'OptionAnswer',
         'semantic_predicate': 'The answer of the first listed history reporting the given value, or none.', 'hypotheses': [H]},
        {'id': 'fiber_constant_on_listing', 'source_declarations': [LHS + '::FiberConstantOn (line 27, definition)'],
         'ordered_inputs': ['Listing', 'ReportMap', 'QuestionMap'], 'output': 'Verdict',
         'semantic_predicate': 'Equal reports imply equal answers on every pair of LISTED histories.', 'hypotheses': [H]},
        {'id': 'image_factor_from_listing', 'source_declarations': [LHS + '::listed_factor_exists (line 205, general theorem needing a complete listing)', PAPER + '::history_report_criterion (line 10; Classical.choose at line 22)'],
         'ordered_inputs': ['Listing', 'ReportMap', 'QuestionMap'], 'output': 'FactorMap',
         'semantic_predicate': 'The factor through the report image built from recon with Option.get, no choice.', 'hypotheses': [H, 'The listing is complete: every history is listed.']}]
    relations = [
        {'id': 'recon_of_fiber_constant', 'source_declarations': [LHS + '::recon_of_fiberConstant (line 116, general theorem)'],
         'equation_or_predicate': 'FiberConstantOn hs report answer => forall h in hs, recon hs report answer (report h) = some (answer h)', 'typing_conditions': 'Listing x ReportMap x QuestionMap',
         'evidence_status': 'Kernel theorem recon_of_fiberConstant (no axioms), own proof; native table', 'scope': 'Arbitrary types with DecidableEq reports'},
        {'id': 'fiber_constant_of_recon', 'source_declarations': [LHS + '::fiberConstant_of_recon (line 132, general theorem)'],
         'equation_or_predicate': 'recon returns every listed answer => FiberConstantOn hs report answer', 'typing_conditions': 'Listing x ReportMap x QuestionMap',
         'evidence_status': 'Kernel theorem fiberConstantOn_of_recon (no axioms), own proof; native table', 'scope': 'Arbitrary types with DecidableEq reports'},
        {'id': 'recon_refuses_unreported', 'source_declarations': [LHS + '::recon_eq_none_iff (line 152, general theorem)'],
         'equation_or_predicate': 'recon hs report answer x = none iff every listed history has a report other than x', 'typing_conditions': 'Listing x ReportValue',
         'evidence_status': 'Kernel theorem recon_eq_none_iff (no axioms); native refusal counts', 'scope': 'Arbitrary types with DecidableEq reports'},
        {'id': 'recon_unique_on_listed_reports', 'source_declarations': [LHS + '::recon_unique (line 188, general theorem)'],
         'equation_or_predicate': 'any f returning the listed answers agrees with recon on listed reports', 'typing_conditions': 'Listing x (ReportValue -> OptionAnswer)',
         'evidence_status': 'Kernel theorem recon_unique (no axioms); Python search test', 'scope': 'Arbitrary types with DecidableEq reports'},
        {'id': 'recon_wrong_off_listing', 'source_declarations': ['no source declaration; new boundary theorem (the source states the instance only as examples at lines 241-254 of ListedHistorySummary.lean)'],
         'equation_or_predicate': 'listed fiber constancy, an unlisted history with a listed report and a different answer => recon does not return that history\'s answer', 'typing_conditions': 'Listing x unlisted history',
         'evidence_status': 'Kernel theorem recon_wrong_off_list (no axioms); native unlisted_wrong counts', 'scope': 'Arbitrary types with DecidableEq reports'},
        {'id': 'classical_instance_axiom_bill', 'source_declarations': ['no source declaration; new axiom-bill record (Lean theorem listed_history_report_criterion_classical)'],
         'equation_or_predicate': 'the proof term of the criterion with the equality instance Classical.propDecidable uses propext, Classical.choice, Quot.sound; whether choice is necessary is open', 'typing_conditions': 'Listing x ReportMap x QuestionMap, no DecidableEq',
         'evidence_status': 'Kernel: axiom report of one proof term (propext, Classical.choice, Quot.sound); no necessity result', 'scope': 'Arbitrary types'}]
    compositions = [
        {'outer_operation': 'image_factor_from_listing', 'input_slot': 0, 'inner_operation': 'listing', 'colour_match': 'Listing',
         'hypothesis_match': 'A complete listing (every history listed) and global fiber constancy; the factor is then built from recon with Option.get inside the construction, not by plugging recon into the Listing slot.',
         'licensing_relations': ['recon_of_fiber_constant', 'recon_refuses_unreported'], 'evidence_status': 'Kernel (listed_factor_exists) and native (complete_triples, complete_mismatch)'},
        {'outer_operation': 'first_match_recon', 'input_slot': 0, 'inner_operation': 'listing', 'colour_match': 'Listing',
         'hypothesis_match': 'Any listing, including repeats allowed.',
         'licensing_relations': ['recon_unique_on_listed_reports'], 'evidence_status': 'Kernel (recon_unique) and native (exhaustive over all listings of length <= ell); the native checker additionally reduces a listing to its first-occurrence sequence, an algorithmic reduction checked only by agreement with the producer, not a Lean lemma'}]
    failed = [{'composition': 'image_factor_from_listing(first_match_recon(...)) as a graft', 'reason': 'Colour mismatch: the factor construction takes a Listing in its first slot and recon outputs OptionAnswer; recon is used inside the construction (listed_factor_exists), not as a grafted argument.'},
              {'composition': 'first_match_recon applied to an unlisted history', 'reason': 'Refused (none) when its report is unreported, and wrong when a listed history shares its report but not its answer (kernel recon_wrong_off_list; native unlisted_wrong counts).'},
              {'composition': 'first_match_recon without decidable equality of reports', 'reason': 'The search needs a Boolean test of report equality; the classical instance restores the statement but the kernel then reports Classical.choice.'}]
    counterexamples = [{'id': 'list_zero_only', 'statement': 'Histories 0,1,2 with report h mod 2, answer h, listing [0]: fiber constant on the listing, recon(report 2) = some 0, but answer 2 = 2.', 'scope': 'Instance of recon_wrong_off_list (Lean instance_wrong_off_list).'},
                       {'id': 'partial_false_positive', 'statement': 'A listing missing a history can be fiber constant while the answer is not globally fiber constant (native partial_false_positive counts, e.g. 840 of 2560 triples for p=3, ell=3, v=2, s=2).', 'scope': 'Native instances.'}]
    return build_spec(
        node=NODE, short='pregen_constructive', lean='PregenConstructive',
        anchors=['PregenConstructive.recon_of_fiberConstant', 'PregenConstructive.fiberConstantOn_of_recon', 'PregenConstructive.listed_history_report_criterion',
                 'PregenConstructive.recon_eq_none_iff', 'PregenConstructive.recon_unique', 'PregenConstructive.recon_wrong_off_list',
                 'PregenConstructive.listed_factor_exists', 'PregenConstructive.listed_history_report_criterion_classical',
                 'PregenConstructive.instance_reconstructs', 'PregenConstructive.instance_wrong_off_list'],
        cases=[list(c) for c in producer.CASES], public_tsv=producer.public_tsv(), data=producer.certificate(),
        scope_review=('The external source ListedHistorySummary.lean (named by the operad bindings, outside this repository; the line numbers cited from it are taken from that external file and are not verified by any gate) is general (arbitrary types, DecidableEq reports, explicit List); it calls itself a proposal. '
                      'The existing Rust witness verify_pregenesis_constructive_summary_witness checks one fixed four-pair listing and one split listing, an instance, not the general statement. '
                      'This node re-proves the criterion by structural recursion instead of List.find? lemmas, adds recon_wrong_off_list, a classical-instance variant that records where Classical.choice enters, and checks exhaustively all listings, reports and answers on 15 small tuples. '
                      'It is the constructive companion of PG-HISTORY-REPORT-CRITERION and does not repeat that node.'),
        predicates=['Enumeration of first-occurrence sequences weighted by Stirling numbers of the second kind (sum_k S2(k,t)), instead of enumerating all listings.',
                    'Reconstruction by a first-occurrence table per report; listed fiber constancy by pairwise equality on the listed set; both compared per triple.',
                    'Total listings equal sum_{k<=ell} p^k and total triples equal listings * v^p * s^p.',
                    'Exact cross-language (Python/Rust) wire equality and literal Lean axiom reports.'],
        boundary=boundary, generators=generators, relations=relations, compositions=compositions, failed_compositions=failed, counterexamples=counterexamples,
        open_obligations=['Report types without decidable equality (choice-free substitute or unavoidability).', 'Unconditional factorization for an arbitrary history type (node PG-HISTORY-REPORT-CRITERION).',
                          'Any probability, measurement or physical reading of reports.'],
        colour_meanings={'HistoryType': 'Type of histories', 'Listing': 'Finite list of histories, repeats allowed', 'ReportMap': 'Function from histories to reports', 'QuestionMap': 'Function from histories to answers',
                         'ReportValue': 'A value of the report type', 'OptionAnswer': 'Answer or none', 'Verdict': 'Proposition', 'FactorMap': 'Function from the report image to answers'},
        depends_on_result=False,
        challenge_plan='Coordinate mutants of every certificate leaf plus eight semantic near misses: first match always right, partial listing implies global, off-listing never wrong, repeats ignored, off-listing never refused, criterion failing on a triple, complete listing disagreeing with the global criterion, a listing of full length taken as complete.',
        composition_tree=['image_factor_from_listing(listing, report, answer)', 'first_match_recon(listing, report, answer, x)'],
        construction='Exhaustive enumeration of every listing, report and answer on 15 small tuples (11 non-degenerate); Lean proves the general listed criterion by structural recursion with no axiom in the kernel.',
        relation_evidence={'recon_of_fiber_constant': 'Kernel theorem (no axioms); native zero mismatch on all 15 tuples (11 non-degenerate).', 'recon_wrong_off_listing': 'Kernel theorem; native unlisted_wrong counts.'})


if __name__ == '__main__':
    print(write_spec(HERE, NODE, spec()))
