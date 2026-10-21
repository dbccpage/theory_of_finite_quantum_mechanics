"""Build specsB/PG-SIX-OPERATIONS.json from the producer and the node's reviewed claims."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp/batch_tools'))
from spec_builder import build_spec, write_spec  # noqa: E402

_s = importlib.util.spec_from_file_location('producer', ROOT / 'code/python/src/qm/pfp_six_operations.py')
producer = importlib.util.module_from_spec(_s)
_s.loader.exec_module(producer)

NODE = 'PG-SIX-OPERATIONS'
SRC = 'lean4/DerivationDagQMClosure.lean'
H = ('Host state = (mentioned, supplied, designated, admitted, retained, outputs); one item per operation; Retain and Operate act only on admitted items. '
     'This is a declared definitional model, not the Genesis event semantics.')


def gen(name, line_note, semantics):
    return {'id': name, 'source_declarations': ['%s::PreGenOp.%s (lines 750-757, constructor of a six-valued enum acting on a COUNTER) %s' % (SRC, name, line_note)],
            'ordered_inputs': ['HostState', 'Item'], 'output': 'HostState', 'semantic_predicate': semantics, 'hypotheses': [H]}


def spec():
    boundary = {
        'supports': ('Kernel-checked for every item type with decidable equality, in a Finset state machine with the six operations: the other five operations leave the admitted component unchanged in every state (supply_keeps_admitted is the corresponding frame lemma in this model; the Genesis supply_no_op in Inertia.lean was read but is external and not bound or imported here); '
                     'one step changes the admitted set iff the operation is an Admit of an item not already admitted; for every finite trace the admitted set is the old set united with all admitted items of the trace and it changes iff the trace contains an Admit of a new item; '
                     'for every token, Readings L (supply t) and F (supply t, admit t) end in different admitted states in the six-operation machine and in the same admitted state in the machine in which Supply also admits (a two-machine comparison, not an iff over a family of machines). '
                     'By construction of the machine each operation writes its own state field and Retain and Operate are gated on admission, so that only Admit writes the admitted component and that the six operations are pairwise distinguishable are properties of this definition, not findings about a host. '
                     'INSTANCES (Nat items): at the probe state with item 0 admitted the six operations on item 0 give six pairwise different results; on the trace [admit 0, admit 1, designate 0, designate 1] the Designate-also-retains machine retains both items while the six-operation machine retains none, and the second designation overwrites the first; admitting item 0 twice gives a set of size 1 (the source counter would give 2). '
                     'Native exhaustive tables: all 22621 traces of length <= 4 over two items from each of four initial admitted sets (admitted state changes iff a new Admit occurs: 11510, 6516, 6516, 0 changing traces; the mismatch column is recomputed by the checker from flags carried through its programme); footprints of the six operations; '
                     '15 pair records (min_len = least length of a trace from the empty state after which some item gives different states under the two operations, over the two-item universe and lengths below 4; contexts = number of (trace of length <= 2, item) pairs at which they differ); 7 conflation counter-models with shortest witnesses (a conflation a_includes_b makes operation a first perform b on the same item); and Reading L / F records for the machines in which Supply also admits and in which Admit also supplies.'),
        'does_not_support': ('That these six operations or state fields match any host, the Genesis Python model or the Genesis event semantics (forms, instances, requirements); that the six operations are distinct beyond writing distinct fields of this machine (Retain and Operate are gated on admission by definition); '
                             'that conflating operations is the source of the Reading L / Reading F split of Genesis (a causal reading; only the model-level two-machine comparison is checked); more than two items or traces longer than 4 natively (the Lean statements are general, the Lean instances are Nat items); '
                             'the inert-inscription model of PG-INERT-DIAMOND (cross-referenced, not imported); any physical or interpretive reading.'),
        'narrowest_claim': 'By construction of its six state components, only Admit writes the admitted component of the six-operation state machine, and it changes it iff the item is new; the Reading L / Reading F pair has different admitted states in this machine and the same admitted state in the machine in which Supply also admits (a two-machine comparison for every token).',
        'next_test': ('Bridge this machine to the Genesis event model: define a simulation from the six operations to Derivation/Basic.lean stepE (supply a no-op, admitDatum an admission) and prove it preserves the admitted regime on the histories of the theorems historyL_replays and historyF_replays of Inertia.lean (external Genesis files, read but not bound and without a pinned sha256).')}
    generators = [
        gen('mention', '(applyPreGenOp: `| _ => admittedCount`, identity on the counter)', 'Add the item to the mentioned record; no other component changes.'),
        gen('supply', '(identity on the counter)', 'Add the item to the supplied record (payload delivered); admitted unchanged.'),
        gen('designate', '(identity on the counter)', 'Set the single designated item (overwrites the previous designation); admitted unchanged.'),
        gen('admit', '(applyPreGenOp: `| .admit => admittedCount + 1`, increments EVERY time, even for a repeated item)', 'Insert the item into the admitted set.'),
        gen('retain', '(identity on the counter)', 'If the item is admitted, add it to the retained set; otherwise refused (no change).'),
        gen('operate', '(identity on the counter)', 'If the item is admitted, add it to the outputs; otherwise refused. Outputs are not admitted.'),
        {'id': 'run_trace', 'source_declarations': ['no source declaration; Genesis Derivation/Basic.lean::replayE folds events (external, not bound here)'], 'ordered_inputs': ['HostState', 'Trace'], 'output': 'HostState',
         'semantic_predicate': 'Left fold of the step function over a list of operations.', 'hypotheses': [H]}]
    relations = [
        {'id': 'non_admit_ops_preserve_admitted', 'source_declarations': [SRC + '::pg_six_operations_and_primdiff_admission_gate (line 764), first conjunct: general in op and the counter n, but a counter, not an admitted set'],
         'equation_or_predicate': 'op is not an Admit implies admitted(step s op) = admitted(s)', 'typing_conditions': 'any state, any item type with decidable equality', 'evidence_status': 'Kernel theorem step_admitted_of_ne_admit; native footprints', 'scope': 'All states'},
        {'id': 'admit_changes_iff_new_item', 'source_declarations': [SRC + '::applyPreGenOp (line 759) increments the counter at every Admit; in the set model re-admission is a no-op'],
         'equation_or_predicate': 'admitted(step s op) != admitted(s) iff op = admit x with x not admitted', 'typing_conditions': 'any state', 'evidence_status': 'Kernel theorem step_changes_admitted_iff', 'scope': 'All states'},
        {'id': 'trace_admitted_union', 'source_declarations': ['no source declaration; new general lemma'], 'equation_or_predicate': 'admitted(run s tr) = admitted(s) union items admitted in tr; changes iff tr contains an Admit of a new item',
         'typing_conditions': 'any state, any finite trace', 'evidence_status': 'Kernel theorems run_admitted, run_changes_admitted_iff, run_without_admit; native 22621-trace tables', 'scope': 'All traces; native range length <= 4, two items'},
        {'id': 'six_results_pairwise_distinct', 'source_declarations': [SRC + '::pg_six_operations_and_primdiff_admission_gate (line 764) second conjunct is a Fin 4 tautology unrelated to operations; pg_root_coproduct_inert_diamond_and_six_operation_separation (line 1111) third part is a Fin 6 index coding (`op.val == 3`), vacuous as a statement about operations'],
         'equation_or_predicate': 'the six operations on one item have six pairwise different results at a probe state', 'typing_conditions': 'INSTANCE on Nat items (item 0 admitted at the probe); holds by construction, each operation writing its own field', 'evidence_status': 'Kernel instance six_results_pairwise_distinct; native pair records', 'scope': 'Instance'},
        {'id': 'supply_admit_conflation_collapses_readings', 'source_declarations': ['Genesis paper.md section 3 (Reading L supplied but unadmitted, Reading F also admits the token); external, read, not bound, no sha pinned'],
         'equation_or_predicate': 'a two-machine comparison: in the six-operation machine readingL t and readingF t end in different admitted states; in the machine in which Supply also admits they end in the same one', 'typing_conditions': 'any token t', 'evidence_status': 'Kernel theorems readings_separated_six_ops, readings_collapse_when_supply_admits (not an iff over a family of machines); native reading records (also the machine in which Admit also supplies, where the readings stay separated)', 'scope': 'Model-relative'},
        {'id': 'designate_retain_conflation', 'source_declarations': ['no source declaration; the node text names designation merged with retention'], 'equation_or_predicate': 'with Designate also retaining, two designations of admitted items retain both; with six operations only the last is designated and none retained',
         'typing_conditions': 'INSTANCE with items 0, 1', 'evidence_status': 'Kernel instances designate_retains_conflation_separates, designation_is_overwritten', 'scope': 'Instance'}]
    compositions = [
        {'outer_operation': 'retain', 'input_slot': 0, 'inner_operation': 'admit', 'colour_match': 'HostState', 'hypothesis_match': H,
         'licensing_relations': ['non_admit_ops_preserve_admitted', 'admit_changes_iff_new_item'], 'evidence_status': 'Kernel and native (retain after admit succeeds)'},
        ]
    failed = [
        {'composition': 'retain(supply(s, t), t)', 'reason': 'Retain acts only on admitted items; a supplied but unadmitted item is refused, so retention does not follow from supply (Reading L).'},
        {'composition': 'operate(designate(s, t), t)', 'reason': 'Designation does not admit; Operate on a merely designated item is refused.'}]
    counterexamples = [
        {'id': 'supply_is_admit_collapses_readings', 'statement': 'If Supply also admits, readings L and F reach the same admitted state; with six operations they differ by one Admit.', 'scope': 'Kernel theorems for every token (two-machine comparison); native reading records.'},
        {'id': 'counter_model_overcounts', 'statement': 'The source counter increments at every Admit; admitting the same item twice gives a set of size 1.', 'scope': 'Instance (repeated_admit_does_not_grow_set).'},
        {'id': 'designate_is_retain', 'statement': 'With Designate also retaining, two admitted designations leave both retained, while six operations leave none retained and one designated.', 'scope': 'Instance with items 0, 1.'}]
    return build_spec(
        node=NODE, short='six_operations', lean='SixOperations',
        anchors=['SixOperations.supply_keeps_admitted', 'SixOperations.step_admitted_of_ne_admit', 'SixOperations.step_changes_admitted_iff',
                 'SixOperations.run_admitted', 'SixOperations.run_changes_admitted_iff', 'SixOperations.run_without_admit',
                 'SixOperations.six_results_pairwise_distinct', 'SixOperations.readings_separated_six_ops',
                 'SixOperations.readings_collapse_when_supply_admits', 'SixOperations.supply_admits_conflation_separates',
                 'SixOperations.designate_retains_conflation_separates', 'SixOperations.designation_is_overwritten',
                 'SixOperations.repeated_admit_does_not_grow_set'],
        cases=[list(c) for c in producer.CASES], public_tsv=producer.public_tsv(), data=producer.certificate(),
        scope_review=('Mined PreGenOp (line 750), applyPreGenOp (line 759) and pg_six_operations_and_primdiff_admission_gate (line 764) of DerivationDagQMClosure.lean (sha256 c9ad9c23 matches the pin). '
                      'The first conjunct is a general statement but about a Nat COUNTER that every Admit increments; the second conjunct is a Fin 4 tautology that has nothing to do with the six operations; the theorem pg_root_coproduct_inert_diamond_and_six_operation_separation (line 1111) encodes Admit as Fin 6 index 3 by arithmetic and is vacuous as an operations statement. '
                      'The paper statement (Pre-Genesis paper.md section 3, TFQ-0363) states definitional separation only, and the prompt names an external Genesis theorem supply_no_op (Inertia.lean, read but neither bound nor pinned here) as the one theorem about supply. '
                      'This node replaces the counter by an admitted FINSET inside a six-component state, proves the frame/iff statements in general, and enumerates all traces natively. PG-INERT-DIAMOND is cross-referenced only.'),
        predicates=['State machine re-implemented with integer bitmasks instead of frozensets.',
                    'Trace counts and distinct final states from a dynamic programme over state multiplicities, cross-checked with the closed forms sum_k (6n)^k - (6n-j)^k (j = items not yet admitted).',
                    'Conflation witness counts from a dynamic programme over PAIRS (six-operation state, conflated state); first witness found by explicit lexicographic search.',
                    'Footprints and pairwise distinguishability recomputed from the independent step function; exact Python/Rust wire equality and literal Lean axiom reports.'],
        boundary=boundary, generators=generators, relations=relations, compositions=compositions, failed_compositions=failed, counterexamples=counterexamples,
        open_obligations=['Simulation of this machine into the Genesis event model (stepE / replayE) and the recorded histories.',
                          'Whether the six operations are exhaustive or minimal for any host; the model fixes them by definition.',
                          'The inert-inscription model (PG-INERT-DIAMOND) and its relation to Mention.'],
        colour_meanings={'HostState': '(mentioned, supplied, designated, admitted, retained, outputs)', 'Item': 'Element of a decidable-equality item type (0 or 1 natively)',
                         'Trace': 'Finite list of operations applied left to right'},
        depends_on_result=True,
        qualification='The DAG phrase that conflating operations "is the source of the Reading L / Reading F split" is narrowed to: in the six-operation state machine the two readings are separated by the admitted state exactly when Supply does not admit; causation in Genesis is not established.',
        challenge_plan='Coordinate mutants of every certificate leaf plus nine semantic near misses: supply writing admitted, readings collapsing without conflation, repeated admit counted as change, designate/retain conflation touching admitted, retain without admission, operate writing admitted, retain equal operate, mention equal supply, no trace changing admitted.',
        composition_tree=['retain(admit(s, x), x)'],
        construction='Exhaustive traces over two items with bitmask dynamic programmes; Lean proves the general frame and iff statements.',
        relation_evidence={'trace_admitted_union': 'Kernel theorems for every trace; native counts equal the closed forms 11510, 6516, 6516, 0.',
                           'supply_admit_conflation_collapses_readings': 'Kernel theorems for every token; native reading record.'})


if __name__ == '__main__':
    print(write_spec(HERE, NODE, spec()))
