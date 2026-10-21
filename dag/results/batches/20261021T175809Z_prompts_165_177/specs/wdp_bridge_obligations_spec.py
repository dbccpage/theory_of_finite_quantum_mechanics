"""Build specs/PG-WDP-GENESIS-BRIDGE-OBLIGATIONS.json from the producer and the node's reviewed claims."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp/batch_tools'))
from spec_builder import build_spec, write_spec  # noqa: E402

_s = importlib.util.spec_from_file_location('producer', ROOT / 'code/python/src/qm/pfp_wdp_bridge_obligations.py')
producer = importlib.util.module_from_spec(_s)
_s.loader.exec_module(producer)

NODE = 'PG-WDP-GENESIS-BRIDGE-OBLIGATIONS'
DAG = 'lean4/DerivationDagQMClosure.lean'
H = ('Ledger model: five obligations O01..O05, statuses open / control-only / discharged; end-to-end is DEFINED as all five discharged; '
     'the programme order O01<..<O05 is our mapping of the derivation order of the programme document, not a stated prerequisite relation.')


def spec():
    boundary = {
        'supports': ("In a three-status ledger model (statuses open / control-only / discharged are this node's vocabulary; the register labels each obligation OPEN) with end-to-end DEFINED as all five discharged: "
                     'by definition the end-to-end claim holds iff every obligation is discharged, equivalently iff every obligation has a control and none is control-only (general over Fin n, instance n=5; Lean); because '
                     'ControlOnly and Discharged are distinct statuses, a ledger in which every obligation has a passing control and the end-to-end claim fails exists (the register sentence that scoped controls do not discharge '
                     'has no Lean declaration); one undischarged obligation blocks the claim; replacing position k of the all-Discharged vector by s gives an end-to-end ledger iff s = Discharged (update_sharp), and a monotone raise '
                     'of the one undischarged position of a ledger completes it (raise_completes); monotone updates never undo the claim; exactly 1 of the 3^5 = 243 vectors is end-to-end (enforced by the checker over the full '
                     'public input). Source declarations at general scope: the five-flag Boolean AND is the conjunction; the symmetrised adjacency adj u v || adj v u of a finite window is false iff adj u v and adj v u are both false, and '
                     'windows with opposite orientation have the same symmetrisation (n=2 countermodel), with no source-to-WDP transition map constructed (that is O02); for all naturals q>0 and p, p*p <> 2*q*q (the source witness '
                     'checks only q in 1..4, p in 1..6), the arithmetic core of GEN-WDP-68, not progress on O04. The columns upgrades, completing_upgrades, prefix_order and node_reading of the table are native definitions without Lean counterparts.'),
        'does_not_support': ('That any of O01..O05 is discharged, dischargeable or refutable; the truth of any end-to-end bridge claim; any independent semantics of "end-to-end" beyond the definitional conjunction; '
                             "that the register status of O01..O05 is control-only: the register labels each OPEN, and Open/ControlOnly/Discharged and the all-ControlOnly vector 11111 are this node's reading of the node statement "
                             '(scoped controls done, end-to-end not); that no_sq_eq_two_sq bears on O04; the programme order as a logical dependency; Hilbert, Born, scalar or governance choices; any physical or institutional interpretation.'),
        'narrowest_claim': ('In a three-status ledger model in which end-to-end is defined as all five discharged, scoped controls passing for all five obligations do not make the end-to-end claim hold, which holds exactly when all five are '
                            'discharged; the node reading (all five control-only) is therefore not end-to-end; ledger bookkeeping only, no obligation is discharged.'),
        'next_test': ('For O02, the only concrete candidate map in hand is the symmetrised adjacency of a finite window: choose an orientation-sensitive source transition system on FiniteGenesisWindow and prove or refute that '
                      'wdpPairDefect is a preservation-and-reflection morphism for it (pairDefect_forgets_orientation already refutes it for orientation-sensitive transitions); record the outcome as the first falsifier on the O02 row.')}
    generators = [
        {'id': 'obligation_status', 'source_declarations': ['genesis_bridge_register.md rows GEN-WDP-O01..O05 (lines 87-91) and programme_completion_audit.md enlarged derivation worklist: text, no Lean/Rust declaration'],
         'ordered_inputs': ['ObligationId'], 'output': 'Status',
         'semantic_predicate': 'Status of one obligation: open, control-only (scoped control passes) or discharged.', 'hypotheses': [H]},
        {'id': 'ledger_update', 'source_declarations': ['no source declaration; new definition (monotone single-position update)'],
         'ordered_inputs': ['Ledger', 'ObligationId', 'Status'], 'output': 'Ledger',
         'semantic_predicate': 'Raise one obligation to a status of at least its current rank.', 'hypotheses': [H]},
        {'id': 'end_to_end', 'source_declarations': ['genesis_bridge_register.md line 94-95 ("do not retag them as complete"); DAG ' + DAG + '::pg_wdp_genesis_bridge_o01_o05_observer_completion_and_diamond_curl (line 1633): Boolean AND of five flags'],
         'ordered_inputs': ['Ledger'], 'output': 'Verdict',
         'semantic_predicate': 'True iff all five obligations are discharged (definition).', 'hypotheses': [H]},
        {'id': 'pair_defect_bridge', 'source_declarations': [DAG + '::FiniteGenesisWindow (line 59), wdpPairDefect (line 65): definitions'],
         'ordered_inputs': ['FiniteGenesisWindow'], 'output': 'PairDefect',
         'semantic_predicate': 'Symmetrisation adj u v || adj v u of the adjacency relation of a finite window (false iff no edge in either direction); no WDP side is constructed.', 'hypotheses': ['Finite window over Fin n.']},
        {'id': 'trace_obligation_cost', 'source_declarations': [DAG + '::PrimGenEvent (6), ObligationMonoid (13), .zero (19), .add (21), .totalCost (26), eventObligation (29), traceObligation (35), ValidFreshAssertionTrace (49): definitions'],
         'ordered_inputs': ['EventTrace'], 'output': 'ObligationCost',
         'semantic_predicate': 'SOURCE-ONLY (no Lean definition, anchor or certificate record in this node): triple (terms, assertions, destructive ops) of a Genesis event trace; the O01 floor concerns this cost, not the ledger statuses.', 'hypotheses': ['Event traces over four primitive events.']}]
    relations = [
        {'id': 'end_to_end_iff_all_discharged', 'source_declarations': [DAG + '::pg_wdp_genesis_bridge_o01_o05_observer_completion_and_diamond_curl (line 1633): its Boolean-AND conjunct is the same equivalence for five free Bool flags, which are not tied to the obligation statuses'],
         'equation_or_predicate': 'EndToEnd v iff every v k is discharged iff discharged count = n', 'typing_conditions': 'Ledger over Fin n',
         'evidence_status': 'Kernel theorems endToEnd_iff_count, endToEnd_five, bool_and_iff (definitional); native table of 243 vectors', 'scope': 'Every n; instance n=5'},
        {'id': 'controls_do_not_discharge', 'source_declarations': ['genesis_bridge_register.md: "the five enlarged obligations remain open ... these additions do not retag them as complete"; no Lean declaration'],
         'equation_or_predicate': 'a ledger with every control passing and the end-to-end claim false exists; EndToEnd iff controls run and none control-only', 'typing_conditions': 'n >= 1',
         'evidence_status': 'Kernel theorems control_only_not_discharged, endToEnd_iff_controls_and_no_control; native: 32 control-passing vectors, 31 not end-to-end', 'scope': 'Every n >= 1'},
        {'id': 'leave_one_out_and_completion', 'source_declarations': [DAG + '::pg_wdp_genesis_bridge_o01_o05_observer_completion_and_diamond_curl (line 1633) and conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure (line 1311): the leave-one-out conjunct is decide on `decide (j ≠ k)`, a statement about that function, not about obligations'],
         'equation_or_predicate': 'one undischarged obligation blocks EndToEnd; the all-discharged-but-k ledger is EndToEnd iff k is discharged', 'typing_conditions': 'Ledger over Fin n',
         'evidence_status': 'Kernel theorems not_endToEnd_of_not_discharged, update_sharp, raise_completes; native update simulation', 'scope': 'Every n'},
        {'id': 'monotone_updates', 'source_declarations': ['no source declaration; new theorem'],
         'equation_or_predicate': 'v <= raise v k s, and EndToEnd is preserved by every pointwise-larger ledger', 'typing_conditions': 'Ledger over Fin n',
         'evidence_status': 'Kernel theorems le_raise, endToEnd_mono, raise_preserves_endToEnd; native single-update tables', 'scope': 'Every n'},
        {'id': 'symmetrisation_preserves_reflects_forgets_orientation', 'source_declarations': [DAG + '::genesis_to_wdp_bridge_preserves_and_reflects (line 68): general theorem over Fin n, a one-line Bool.or lemma'],
         'equation_or_predicate': 'adj u v || adj v u = false iff adj u v = false and adj v u = false; two windows with different adjacency can share the symmetrisation', 'typing_conditions': 'FiniteGenesisWindow n',
         'evidence_status': 'Kernel theorems pairDefect_preserves_and_reflects, pairDefect_forgets_orientation; Python cross-check', 'scope': 'Every n; countermodel at n=2'},
        {'id': 'sq_two_arithmetic_general', 'source_declarations': [DAG + '::pg_wdp_genesis_bridge_o01_o05_observer_completion_and_diamond_curl (line 1633): checks p*p != 2*q*q only for q in [1..4], p in [1..6] (bounded instance); arithmetic core of GEN-WDP-68, not O04'],
         'equation_or_predicate': 'for every q>0 and every p: p*p != 2*(q*q)', 'typing_conditions': 'Nat',
         'evidence_status': 'Kernel theorem no_sq_eq_two_sq (descent); Python brute force on q<200, p<300', 'scope': 'All naturals'}]
    compositions = [
        {'outer_operation': 'end_to_end', 'input_slot': 0, 'inner_operation': 'ledger_update', 'colour_match': 'Ledger',
         'hypothesis_match': H, 'licensing_relations': ['monotone_updates', 'leave_one_out_and_completion'], 'evidence_status': 'Kernel and native'}]
    failed = [
        {'composition': 'ledger_update(obligation_status(Ok), ...)', 'reason': 'Colour mismatch: ledger_update takes a Ledger but obligation_status outputs a Status; assembling five statuses into a Ledger is not an operation of this presentation.'},
        {'composition': 'end_to_end(ledger with every control passing)', 'reason': 'Fails: the source state (all five control-only) is not end-to-end; scoped controls do not compose into the end-to-end claim.'},
        {'composition': 'trace_obligation_cost into obligation_status', 'reason': 'No source map: the O01 cost floor (cost >= 2) is a statement about event traces and does not change any ledger status.'},
        {'composition': 'pair_defect_bridge as a faithful preservation map for O02', 'reason': 'The pair defect forgets orientation (kernel countermodel), so it is not a reflection of the source transition system beyond defect-freeness.'}]
    counterexamples = [
        {'id': 'all_controls_pass_not_discharged', 'statement': 'Ledger 11111: every obligation has a passing control and none is discharged, yet the end-to-end claim is false.', 'scope': 'Instance of control_only_not_discharged; the node reading of the register state (the register itself says OPEN)'},
        {'id': 'out_of_order_discharge', 'statement': 'Ledger 00002 discharges O05 only; it violates the programme order though no source says the order is a prerequisite.', 'scope': 'Modelling-choice order'},
        {'id': 'orientation_forgotten', 'statement': 'Windows with adjacency {0->1} and {1->0} have the same pair defect.', 'scope': 'n = 2 countermodel to faithfulness of the bridge map'}]
    return build_spec(
        node=NODE, short='wdp_bridge_obligations', lean='WdpBridgeObligations',
        anchors=['WdpBridgeObligations.endToEnd_iff_count', 'WdpBridgeObligations.endToEnd_five', 'WdpBridgeObligations.control_only_not_discharged',
                 'WdpBridgeObligations.endToEnd_iff_controls_and_no_control', 'WdpBridgeObligations.not_endToEnd_of_not_discharged',
                 'WdpBridgeObligations.update_sharp', 'WdpBridgeObligations.raise_completes', 'WdpBridgeObligations.endToEnd_mono', 'WdpBridgeObligations.le_raise',
                 'WdpBridgeObligations.raise_preserves_endToEnd', 'WdpBridgeObligations.prefixOrder_of_endToEnd', 'WdpBridgeObligations.prefixOrder_violation',
                 'WdpBridgeObligations.card_vectors', 'WdpBridgeObligations.endToEnd_unique', 'WdpBridgeObligations.bool_and_iff',
                 'WdpBridgeObligations.pairDefect_preserves_and_reflects', 'WdpBridgeObligations.pairDefect_forgets_orientation',
                 'WdpBridgeObligations.no_sq_eq_two_sq'],
        cases=list(producer.CASES), public_tsv=producer.public_tsv(), data=producer.certificate(),
        scope_review=('Read the 12 operation candidates and 5 relation candidates in DerivationDagQMClosure.lean and the real ledger text (genesis_bridge_register.md rows O01..O05, the '
                      'completion audit worklist, programme section 6). The source theorem pg_wdp_genesis_bridge_o01_o05_observer_completion_and_diamond_curl is mostly fixed-number arithmetic: its '
                      'Boolean AND of five free flags is the conjunction (vacuous with respect to the obligations), its leave-one-out conjunct is decide on `decide (j ≠ k)`, and its sqrt(2) check is bounded '
                      '(q<=4, p<=6). genesis_to_wdp_bridge_preserves_and_reflects is a general but one-line Bool.or lemma and the map forgets orientation. declare_then_assert_cost_floor is a general omega '
                      'lemma about event-trace costs and does not move any ledger status. The register labels each of O01..O05 literally OPEN (rows 87-91) and never says "control-only"; the ledger is modelled with statuses open / control-only / discharged, an invented vocabulary, the end-to-end predicate and the programme '
                      'order are modelling choices and are labelled as such. No obligation is discharged or dischargeable by this node.'),
        predicates=['Independent recomputation of every row: counts by filtering, programme order as a pairwise implication, update counts by simulating every strict single-position update (producer uses closed forms).',
                    'Theorem-level consistency: only the all-discharged vector is end-to-end; the source-reported vector has all controls and no discharge.',
                    'Exact cross-language (Python/Rust) wire equality and literal Lean axiom reports.'],
        boundary=boundary, generators=generators, relations=relations, compositions=compositions, failed_compositions=failed, counterexamples=counterexamples,
        open_obligations=['GEN-WDP-O01 carrier, signature, law and challenge-generation floor.', 'GEN-WDP-O02 preservation/reflection maps from each source transition and admission system.',
                          'GEN-WDP-O03 dynamic carrier transport and higher fillers.', 'GEN-WDP-O04 effect, probability, scalar and Hilbert choices.',
                          'GEN-WDP-O05 governance refinement (jurisdiction, appeal, enforcement maps).'],
        colour_meanings={'ObligationId': 'One of O01..O05', 'Status': 'open / control-only / discharged', 'Ledger': 'Function from the five obligations to statuses',
                         'Verdict': 'End-to-end holds or not', 'FiniteGenesisWindow': 'Finite window with an adjacency relation', 'PairDefect': 'Symmetric pair defect relation',
                         'EventTrace': 'List of primitive Genesis events', 'ObligationCost': 'Triple of natural-number costs'},
        depends_on_result=True, qualification='Lean establishes only finite ledger-bookkeeping lemmas about status vectors and small re-proved side facts; no bridge obligation O01-O05 is discharged, and the PROVED_LEAN label does not extend to the obligations.',
        challenge_plan='Coordinate mutants of every ledger leaf plus twelve semantic near misses: controls read as end-to-end, four of five enough, open counted as control, out-of-order discharge, hidden completing update, upgrade past discharged, node-reading marker moved to all-discharged or to 00000, two missing but one update completes, all-discharged not end-to-end, prefix flag reversed, no control passes.',
        composition_tree=['end_to_end(ledger_update(L, k, s))'],
        construction='All 3^5 status vectors with derived columns; Lean proves the ledger statements over Fin n and three source declarations at general scope.',
        relation_evidence={'controls_do_not_discharge': 'Kernel theorem; native: 32 vectors with all controls, 31 not end-to-end.',
                           'end_to_end_iff_all_discharged': 'Definitional; kernel and native agree that exactly one of 243 vectors is end-to-end.'})


if __name__ == '__main__':
    print(write_spec(HERE, NODE, spec()))
