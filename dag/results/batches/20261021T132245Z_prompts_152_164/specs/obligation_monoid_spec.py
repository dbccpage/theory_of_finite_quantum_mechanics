"""Build specs/PG-OBLIGATION-MONOID.json from the producer and the node's reviewed claims."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp/batch_tools'))
from spec_builder import build_spec, write_spec  # noqa: E402

_s = importlib.util.spec_from_file_location('producer', ROOT / 'code/python/src/qm/pfp_obligation_monoid.py')
producer = importlib.util.module_from_spec(_s)
_s.loader.exec_module(producer)

NODE = 'PG-OBLIGATION-MONOID'
LEAN = 'lean4/DerivationDagQMClosure.lean'
RS = 'omega_engine/crates_rs/omega_kernel/src/obligation.rs'
H = 'Counters are natural numbers (u64 with checked addition in the Rust source); the ledger model has the three ids A, B, C; Genesis events are the four declared events only.'


def spec():
    boundary = {
        'supports': ('Kernel-checked: counter vectors Fin k -> Nat under pointwise sum form a commutative cancellative monoid that is not a group (every nonzero vector lacks an inverse) and is the free commutative monoid on k ids (universal property, existence and uniqueness); '
                     'the bounded combine that refuses past a count bound is partially associative with equal definedness on both bracketings, and bounded generation returns none exactly when some coordinate would exceed the bound (genB_none_iff); '
                     'the re-declared copy (Ev, evOb, trace) of the source three-counter trace is a monoid homomorphism from lists of the four declared events; coordinate 0 counts declareTerm, coordinate 1 counts assertDiff, coordinate 2 counts removeDiff plus identifyTerms together, and the total equals the list length; the copy is order-blind and its event table is not injective; '
                     'one discharge step from a valid ledger yields a valid ledger and succeeds exactly when the request is at most the outstanding count, and, for the unbounded k-id model with generate and discharge operations, every successful run from the empty ledger ends valid (run_from_empty_valid). '
                     'Native: exact tables for 34 cases (laws on boxes up to 3 ids x 4, bounded and saturating sums, 13 event words, 12 ledger traces over three ids with u64 bound covering every error kind and a generation landing exactly on 2^64-1); the native ledger is a model of the Rust rule, not the Rust crate.'),
        'does_not_support': ('That Genesis events or S(n) maps are monoid morphisms into the obligation monoid (TFQ-0342, PG-GAP-EVENT-OBLIGATION): the event-to-vector table evOb is copied from the source, not derived, and only lists of the four declared events are covered; '
                             'any theorem tying Ev/evOb/trace to PrimGenEvent/eventObligation/traceObligation of DerivationDagQMClosure.lean (they are a re-declaration); any theorem connecting the Lean abstract-k unbounded ledger to the three-id u64 Python/Rust ledger; '
                             'the Rust crate itself (nothing in omega_kernel is executed); unbounded or string-keyed ids; any claim that the 3-counter vector equals the free monoid on the real obligation ids.'),
        'narrowest_claim': ('Obligation counters under pointwise sum are the free commutative monoid on the ids (cancellative, not a group); the re-declared copy of the source four-event three-counter trace is a homomorphism from event lists with total cost equal to length; in the abstract unbounded k-id model every successful generate/discharge run from the empty ledger keeps discharged within generated and a discharge succeeds exactly when it fits the outstanding count; Genesis events and S(n) maps being morphisms remains unproved.'),
        'next_test': ('Derive from the actual Genesis event and S(n)-map definitions (not the four-event table) that each step adds a fixed generated and discharged vector independent of context, i.e. that sequential composition maps to combine, or exhibit an event whose vector depends on the preceding trace.')}
    generators = [
        {'id': 'empty', 'source_declarations': [LEAN + '::ObligationMonoid.zero (line 19; definition)', RS + '::Obligations::empty (line 101; definition)'],
         'ordered_inputs': ['Unit'], 'output': 'ObligationVector', 'semantic_predicate': 'Nullary: the all-zero counter vector (empty multiset), taken from the one-point colour Unit.', 'hypotheses': [H]},
        {'id': 'single', 'source_declarations': [RS + '::Obligations::single (line 105) and of (line 109); definitions, a zero count gives the empty multiset'],
         'ordered_inputs': ['ObligationId'], 'output': 'ObligationVector', 'semantic_predicate': 'Basis vector of one id (count 1).', 'hypotheses': [H]},
        {'id': 'combine', 'source_declarations': [LEAN + '::ObligationMonoid.add (line 21; definition)', RS + '::Obligations::combine (line 118; definition with checked_add, returns CountOverflow)'],
         'ordered_inputs': ['ObligationVector', 'ObligationVector'], 'output': 'ObligationVector', 'semantic_predicate': 'Pointwise sum; partial when a count would exceed the bound.', 'hypotheses': [H]},
        {'id': 'event_obligation', 'source_declarations': [LEAN + '::eventObligation (line 29; definition, the table is data) over PrimGenEvent (line 6; inductive)'],
         'ordered_inputs': ['GenesisEvent'], 'output': 'ObligationVector', 'semantic_predicate': 'declare -> (1,0,0), assert -> (0,1,0), remove and identify -> (0,0,1).', 'hypotheses': [H]},
        {'id': 'trace_obligation', 'source_declarations': [LEAN + '::traceObligation (line 35; definition by recursion on the event list)'],
         'ordered_inputs': ['EventList'], 'output': 'ObligationVector', 'semantic_predicate': 'Sum of event vectors along the list.', 'hypotheses': [H]},
        {'id': 'discharge', 'source_declarations': [RS + '::ObligationLedger::discharge (line 189; definition) with ObligationError (line 85)'],
         'ordered_inputs': ['Ledger', 'ObligationId', 'Count'], 'output': 'LedgerOrError', 'semantic_predicate': 'Zero is a no-op; never-generated, then over-discharge, else add to discharged.', 'hypotheses': [H]}]
    relations = [
        {'id': 'monoid_laws', 'source_declarations': [RS + '::tests combine_is_commutative, combine_is_associative, empty_is_the_identity (lines 313-340; Rust unit tests on fixed multisets, not a proof)'],
         'equation_or_predicate': '(x+y)+z = x+(y+z); x+y = y+x; x+0 = x', 'typing_conditions': 'ObligationVector', 'evidence_status': 'Kernel theorems combine_assoc, combine_comm, combine_empty (general in k); native box tables', 'scope': 'All k'},
        {'id': 'cancellative_not_group', 'source_declarations': ['no source declaration; the source says only "commutative monoid"'],
         'equation_or_predicate': 'x+z = y+z implies x = y; x != 0 implies x+y != 0', 'typing_conditions': 'ObligationVector', 'evidence_status': 'Kernel theorems combine_cancel, no_inverse; native cancel_failures = 0, invertible_nonzero = 0', 'scope': 'All k'},
        {'id': 'free_commutative_monoid', 'source_declarations': [RS + '::Obligations (line 65; doc comment "an element of the free commutative monoid on obligation ids"; the claim is prose, no universal property is stated)'],
         'equation_or_predicate': 'every additive map from ObligationVector to a commutative monoid is determined by its values on single; lift exists', 'typing_conditions': 'Fin k ids, AddCommMonoid target', 'evidence_status': 'Kernel theorems lift_single, lift_unique', 'scope': 'All k, all commutative monoids'},
        {'id': 'trace_append', 'source_declarations': [LEAN + '::traceObligation_append (line 39; general theorem over lists of PrimGenEvent)'],
         'equation_or_predicate': 'trace(a ++ b) = trace(a) + trace(b); trace [] = 0', 'typing_conditions': 'EventList', 'evidence_status': 'Kernel theorem trace_append (re-proved with a different proof); native split_failures = 0', 'scope': 'Lists of the four declared events'},
        {'id': 'cost_is_length', 'source_declarations': [LEAN + '::declare_then_assert_cost_floor (line 52; hypothesis ValidFreshAssertionTrace at line 49 is a pure counter condition, so the theorem is the arithmetic fact termsAdded + assertionsAdded >= 2)'],
         'equation_or_predicate': 'sum of the three counters of trace l = length l; ValidFresh l implies length l >= 2', 'typing_conditions': 'EventList', 'evidence_status': 'Kernel theorems trace_total, trace_terms, cost_floor, valid_fresh_order_blind; native cost = length', 'scope': 'Lists of the four declared events'},
        {'id': 'order_and_identity_lost', 'source_declarations': ['no source declaration; new observation'],
         'equation_or_predicate': 'trace permutation-invariant; evOb removeDiff = evOb identifyTerms', 'typing_conditions': 'EventList, GenesisEvent', 'evidence_status': 'Kernel theorems trace_swap, event_table_not_injective; native perm_trace_failures = 0', 'scope': 'Four declared events'},
        {'id': 'bounded_partial_associativity', 'source_declarations': [RS + '::Obligations::combine (line 118; checked_add refusal) and tests (no overflow test for associativity)'],
         'equation_or_predicate': 'combineB M is associative with identical definedness: both bracketings are defined iff every coordinate sum x+y+z <= M', 'typing_conditions': 'ObligationVector, bound M', 'evidence_status': 'Kernel theorem combineB_assoc; native bounded tables', 'scope': 'All k, all M'},
        {'id': 'ledger_discharge_rule', 'source_declarations': [RS + '::ObligationLedger::discharge (line 189) and LedgerWire validation (line 242); doc: discharged never exceeds generated'],
         'equation_or_predicate': 'valid ledger and ok result imply valid ledger; ok iff c <= generated - discharged; never-generated iff generated = 0 and c > 0', 'typing_conditions': 'Ledger, Fin k, Nat', 'evidence_status': 'Kernel theorems discharge_valid, discharge_ok_iff, discharge_never_generated, over_discharge_needs_generated (one step), run_valid and run_from_empty_valid (whole traces, unbounded), genB_valid and genB_none_iff (bounded generation); native ledger traces', 'scope': 'All k in Lean (unbounded); three ids with the u64 bound natively'}]
    compositions = [
        {'outer_operation': 'combine', 'input_slot': 0, 'inner_operation': 'trace_obligation', 'colour_match': 'ObligationVector', 'hypothesis_match': H,
         'licensing_relations': ['trace_append', 'monoid_laws'], 'evidence_status': 'Kernel and native'},
        {'outer_operation': 'discharge', 'input_slot': 0, 'inner_operation': 'combine', 'colour_match': 'Ledger', 'hypothesis_match': 'Generation is combine on the generated vector; discharge reads the outstanding count.',
         'licensing_relations': ['ledger_discharge_rule', 'bounded_partial_associativity'], 'evidence_status': 'Kernel and native'}]
    failed = [{'composition': 'event_obligation as a monoid morphism from Genesis events and S(n) maps', 'reason': 'Only list append of the four declared events is shown to map to combine; events of the Genesis regime and S(n) maps are not defined here, and the table is copied data (TFQ-0342).'},
              {'composition': 'saturating total in place of checked combine', 'reason': 'Saturating addition is associative and commutative but not cancellative (native 20 failures at cap 3); the source refuses it, and the checked combine returns CountOverflow instead.'},
              {'composition': 'declare_then_assert_cost_floor read as ordering declare before assert', 'reason': 'ValidFreshAssertionTrace counts occurrences only; the trace [assertDiff, declareTerm] satisfies it.'}]
    counterexamples = [{'id': 'assert_before_declare', 'statement': 'trace A D has valid_fresh true and declare_then_assert false.', 'scope': 'Source theorem name versus hypothesis.'},
                       {'id': 'saturating_not_cancellative', 'statement': 'min(x+z, cap) = min(y+z, cap) with x != y occurs 20 times at cap 3.', 'scope': 'Alternative total operation.'},
                       {'id': 'remove_identify_share_vector', 'statement': 'evOb removeDiff = evOb identifyTerms = (0,0,1) although the events differ.', 'scope': 'Four declared events.'}]
    return build_spec(
        node=NODE, short='obligation_monoid', lean='ObligationMonoid',
        anchors=['ObligationMonoid.combine_assoc', 'ObligationMonoid.combine_comm', 'ObligationMonoid.combine_empty', 'ObligationMonoid.combine_cancel',
                 'ObligationMonoid.no_inverse', 'ObligationMonoid.lift_single', 'ObligationMonoid.lift_unique', 'ObligationMonoid.trace_append',
                 'ObligationMonoid.trace_total', 'ObligationMonoid.trace_terms', 'ObligationMonoid.trace_assertions', 'ObligationMonoid.trace_destructive', 'ObligationMonoid.cost_floor', 'ObligationMonoid.valid_fresh_order_blind',
                 'ObligationMonoid.trace_swap', 'ObligationMonoid.event_table_not_injective', 'ObligationMonoid.combineB_assoc',
                 'ObligationMonoid.discharge_valid', 'ObligationMonoid.discharge_ok_iff', 'ObligationMonoid.discharge_never_generated',
                 'ObligationMonoid.over_discharge_needs_generated', 'ObligationMonoid.run_valid', 'ObligationMonoid.run_from_empty_valid', 'ObligationMonoid.genB_valid', 'ObligationMonoid.genB_none_iff', 'ObligationMonoid.overdischarge_instance'],
        cases=[list(c) for c in producer.CASES], public_tsv=producer.public_tsv(), data=producer.certificate(),
        scope_review=('Read DerivationDagQMClosure.lean lines 6-56 (sha c9ad9c23a4) and obligation.rs (sha 172ab7d7cb, matches the pin). The source Lean ObligationMonoid is a Nat triple with componentwise add; traceObligation_append is a correct general list-append lemma. '
                      'declare_then_assert_cost_floor is the arithmetic fact that two counters >= 1 sum to >= 2: its hypothesis ValidFreshAssertionTrace does not order declare before assert. The Rust Obligations is described as the free commutative monoid in a doc comment only; no universal property is stated. '
                      'The node states that Genesis morphisms are meant to carry these vectors: this bundle proves the monoid facts, the free-monoid property, the declared-event trace homomorphism and the ledger rule, and does not prove the Genesis/S(n) morphism claim, as TFQ-0342 requires. '
                      'Found: the monoid is cancellative and not a group (not a failure of cancellation as one might fear), the saturating alternative fails cancellation, the event table loses order and identifies two events.'),
        predicates=['Counter-vector laws recomputed on positionally packed integers (vector sum = integer sum) rather than coordinate tuples.',
                    'Bounded combine counted by closed forms: a+b <= M has (M+1)(M+2)/2 solutions per coordinate, a+b+c <= M has C(M+3,3).',
                    'Saturating cancellation failures cap(cap+1)(cap+2)/3 against brute force with a clamp-form operator.',
                    'Event traces by str.count, ordering by regular expression D.*A, distinct permutations by the multinomial coefficient.',
                    'Ledger recomputed from generated and outstanding counts (producer tracks generated and discharged) with exact big integers and the 2^64-1 bound.',
                    'Exact cross-language (Python/Rust) wire equality and literal Lean axiom reports.'],
        boundary=boundary, generators=generators, relations=relations, compositions=compositions, failed_compositions=failed, counterexamples=counterexamples,
        open_obligations=['Derive Genesis events and S(n) maps as morphisms into the obligation monoid (PG-GAP-EVENT-OBLIGATION).', 'Relate the three-counter Lean monoid to the string-keyed Rust multiset.',
                          'Execute the real omega_kernel ledger on the replayed traces.'],
        colour_meanings={'Unit': 'One-point colour used for the nullary operation empty', 'ObligationId': 'Index i in Fin k', 'ObligationVector': 'Counter vector Fin k -> Nat (multiset)', 'Count': 'Natural number, u64 in the Rust source',
                         'GenesisEvent': 'One of declareTerm, assertDiff, removeDiff, identifyTerms', 'EventList': 'List of GenesisEvent', 'Ledger': 'Pair (generated, discharged) of vectors',
                         'LedgerOrError': 'Ledger, NeverGenerated, OverDischarge or CountOverflow'},
        depends_on_result=True,
        qualification='Mechanized for lists of the four declared events and counter vectors only; the declare_then_assert floor is a counter inequality that does not order the events, the Lean trace is a re-declared copy of the source table, and Genesis events and S(n) maps being monoid morphisms is not established (the original wording of the node should be read as an intent, with the morphism claim left open).',
        challenge_plan='Coordinate mutants of every certificate leaf plus fifteen semantic near misses: false cancellation failure, group claim, cancellative saturation, hidden overflow, bound ignored, ungenerated discharge accepted, zero discharge as error, swapped refusal kinds, order-blind floor read as ordered, removal counted as declaration, order-sensitive trace, non-associative bounded combine, non-associative saturation, discharge checked against generated, generation at the bound refused.',
        composition_tree=['combine(trace_obligation(a), trace_obligation(b))', 'discharge(combine(generated, v), id, c)'],
        construction='Exhaustive tables on counter boxes, bounded and saturating sums, event words and ledger traces; Lean proves the general statements for every k.',
        relation_evidence={'free_commutative_monoid': 'Kernel lift_unique; no native analogue beyond the box laws.', 'trace_append': 'Kernel trace_append; native split tables.',
                           'ledger_discharge_rule': 'Kernel discharge_ok_iff and run_valid; native traces with every error kind.'})


if __name__ == '__main__':
    print(write_spec(HERE, NODE, spec()))
