"""Build specs/PG-DEMAND-ACCOUNTING.json from the producer and the node's reviewed claims."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp/batch_tools'))
from spec_builder import build_spec, write_spec  # noqa: E402

_s = importlib.util.spec_from_file_location('producer', ROOT / 'code/python/src/qm/pfp_demand_accounting.py')
producer = importlib.util.module_from_spec(_s)
_s.loader.exec_module(producer)

NODE = 'PG-DEMAND-ACCOUNTING'
H = 'Finite registers; the next register is (W minus D) union B; D subset of W; births disjoint from W minus D (not from W or D).'
P1 = 'omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean'
P0 = 'omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean'
SNC = 'omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/SnCarrier.lean'


def spec():
    boundary = {
        'supports': ('Kernel-checked for Finsets of any type with decidable equality: D subset of W and (W minus D) disjoint from B imply |(W minus D) union B| = |W| - |D| + |B|; with no hypothesis |next| = |W| - |W cap D| + |B| - |(W minus D) cap B| (card_next_exact), so the integer identity holds if and only if |D minus W| = |(W minus D) cap B| (formula_iff); explicit counterexamples when D subset W is dropped and when disjointness is dropped, an explicit agreement with both dropped (exact cancellation), and an explicit case where the truncated natural-number identity holds although D is not inside W; every pair of counts (s, s2) is the count pair of an admissible step, and two admissible splits give the same counts, so a count sequence is not a law; the list-length reading of the source needs no disjointness, while for duplicate-free inputs the filter-based list register is duplicate-free exactly when the births avoid the survivors (list_register_nodup_iff). Exactly one violated hypothesis never permits the integer identity (single_violation_fails; its disjointness-alone half is the corollary of formula_iff with D inside W). The anchors fails_without_subset, fails_without_disjoint, holds_accidentally_without_hypotheses, nat_truncation_masks_subset_violation, split_not_determined and list_overlap_not_nodup are single instances, not universal statements. Axioms of the Finset theorems: propext, Classical.choice, Quot.sound (standard Mathlib); the list theorems use propext and Quot.sound or less. '
                     'Native: exhaustive classification of all 8^u triples (W, D, B) of subsets for u = 0..5 into the four hypothesis classes with, per class, the number of triples for which the integer and the truncated identity hold, four count sequences (including the source displayed sequence 0,1,1,1,0,1,1) with their exact number of admissible (|D|, |B|) splits per step, and two exhaustive list-register censuses (alphabet 2 with lists up to length 2, alphabet 3 up to length 3) showing the length identity holds for every triple and that duplicate-free inputs give a duplicate-free register exactly when the births avoid the survivors.'),
        'does_not_support': ('Which demands an engine actually carries; any claim that the displayed survivor sequence (0,1,1,1,0,1,1) is a native or universal law (the source itself calls it a chosen ledger example); the preservation.py demand_step frozenset reading and any Python or Rust wrapper over it; multiset or ordered-log registers as a state beyond the filter-based list register of Paper.lean (the erase-based removeAll register of Paper001.lean is not re-proved, and the Nodup conjunct of that List Nat statement is only matched by the filter-based list_register_nodup_iff and the native census); the identification of the active count s_n with the cumulative history |H_n|; universes of more than five elements; any physical or thermodynamic interpretation.'),
        'narrowest_claim': 'For finite sets, |(W minus D) union B| = |W| - |D| + |B| holds when D is inside W and the births avoid W minus D (births may coincide with discharged elements), it fails whenever exactly one of the two hypotheses is violated; when both are violated it holds if and only if |D minus W| = |(W minus D) cap B| (exact cancellation); and it imposes no constraint on a sequence of counts.',
        'next_test': 'Supply the missing count wrapper over preservation.demand_step of the opened preservation.py: show that the frozenset next-active set it returns equals the Finset (W minus D) union B of this model, carry the two hypotheses as typed fields of the wrapper, and replay the identity on the wrapper actual outputs.'}
    generators = [
        {'id': 'register_discharge', 'source_declarations': [P1 + '::removeAll (line 7) on List Nat, general erase-fold, a definition',
                                                               P0 + '::demand_accounting (line 82) uses active.filter (not discharged) on List A, general'],
         'ordered_inputs': ['ActiveRegister', 'DischargedSet'], 'output': 'SurvivorRegister', 'semantic_predicate': 'W minus D; the discharged set is a subset of W in the source theorems.', 'hypotheses': [H]},
        {'id': 'register_birth', 'source_declarations': [P1 + '::demand_accounting (line 86) uses (removeAll W D) ++ B on List Nat'],
         'ordered_inputs': ['SurvivorRegister', 'BirthSet'], 'output': 'ActiveRegister', 'semantic_predicate': 'Union of the survivors with the births; births are disjoint from the survivors only (hdisj ranges over removeAll W D).', 'hypotheses': [H]},
        {'id': 'register_count', 'source_declarations': [P1 + '::demand_accounting (line 86), List.length of the register; P0 Paper.lean line 82'],
         'ordered_inputs': ['ActiveRegister'], 'output': 'Count', 'semantic_predicate': 'Cardinality of a finite register.', 'hypotheses': [H]},
        {'id': 'count_step', 'source_declarations': [P1 + '::demand_accounting (line 86), right-hand side W.length - D.length + B.length (Nat subtraction, truncated)'],
         'ordered_inputs': ['Count', 'Count', 'Count'], 'output': 'Count', 'semantic_predicate': 's - d + b.', 'hypotheses': [H]}]
    relations = [
        {'id': 'demand_accounting_identity', 'source_declarations': [P1 + '::demand_accounting (line 86): a theorem on List Nat with hypotheses Nodup W, D, B, subset, disjointness; the length conjunct uses only W.Nodup, D.Nodup and the subset hypothesis',
                                                                        P0 + '::demand_accounting (line 82): a general theorem on List A with a Bool predicate, no disjointness'],
         'equation_or_predicate': 'D subset W and Disjoint (W minus D) B imply |(W minus D) union B| = |W| - |D| + |B|', 'typing_conditions': 'ActiveRegister x DischargedSet x BirthSet over a type with decidable equality',
         'evidence_status': 'Kernel theorem demand_accounting; native class hypotheses_hold: identity holds for all 5^u triples, u = 0..5', 'scope': 'All finite sets'},
        {'id': 'exact_next_cardinality', 'source_declarations': ['no source declaration; new general identity'],
         'equation_or_predicate': '|next| = |W| - |W cap D| + |B| - |(W minus D) cap B| with no hypothesis', 'typing_conditions': 'same', 'evidence_status': 'Kernel theorem card_next_exact', 'scope': 'All finite sets'},
        {'id': 'identity_iff_excess_equals_overlap', 'source_declarations': ['no source declaration; new exact characterisation'],
         'equation_or_predicate': '|next| = |W| - |D| + |B| (integers) iff |D minus W| = |(W minus D) cap B|', 'typing_conditions': 'same',
         'evidence_status': 'Kernel theorem formula_iff; native counts of the four classes', 'scope': 'All finite sets'},
        {'id': 'hypothesis_necessity', 'source_declarations': ['no source declaration; source text says the hypotheses are required but proves no failure'],
         'equation_or_predicate': 'dropping D subset W or disjointness yields a triple where the identity fails; the truncated natural-number identity can hold when D is strictly larger than W', 'typing_conditions': 'same',
         'evidence_status': 'Kernel theorems single_violation_fails (universal), fails_of_excess_without_overlap (universal), fails_without_subset and fails_without_disjoint (instances), nat_truncation_masks_subset_violation, holds_accidentally_without_hypotheses', 'scope': 'Instances plus the general integer statement for D not inside W without overlap'},
        {'id': 'list_length_vs_set_cardinality', 'source_declarations': [P0 + '::demand_accounting (line 82) and demand_register_nodup (line 89): length identity without disjointness, Nodup with it'],
         'equation_or_predicate': 'the list length of (active.filter not discharged) ++ births equals |active| - |discharged part| + |births| with no disjointness; the register is duplicate-free only under disjointness', 'typing_conditions': 'List A',
         'evidence_status': 'Kernel theorems list_length_no_disjointness, list_register_nodup_iff (universal) and list_overlap_not_nodup (instance); native listreg census', 'scope': 'All lists; the Nodup failure is an instance'},
        {'id': 'count_sequence_is_not_a_law', 'source_declarations': [SNC + '::activeObstructions (line 34), a table definition of the displayed sequence 0,1,1,1,0,1,1 (fixed values, no theorem)'],
         'equation_or_predicate': 'every pair (s, s2) of counts is realized by an admissible (W, D, B); the number of admissible (d, b) splits of a step is s + 1 - max(0, s - s2)', 'typing_conditions': 'Count x Count',
         'evidence_status': 'Kernel theorems every_step_is_an_accounting, split_not_determined; native sequence records', 'scope': 'All pairs of natural numbers'}]
    compositions = [
        {'outer_operation': 'register_count', 'input_slot': 0, 'inner_operation': 'register_birth', 'colour_match': 'ActiveRegister', 'hypothesis_match': H,
         'licensing_relations': ['demand_accounting_identity', 'exact_next_cardinality'], 'evidence_status': 'Kernel and native'},
        {'outer_operation': 'register_birth', 'input_slot': 0, 'inner_operation': 'register_discharge', 'colour_match': 'SurvivorRegister', 'hypothesis_match': H,
         'licensing_relations': ['demand_accounting_identity'], 'evidence_status': 'Kernel and native'}]
    failed = [
        {'composition': 'register_count o register_birth o register_discharge read as count_step(count W, count D, count B) without hypotheses',
         'reason': 'Equal only when |D minus W| = |(W minus D) cap B| (formula_iff); native counts show it fails for every triple violating exactly one hypothesis.'},
        {'composition': 'count_step inverted: recover (d, b) from a count sequence', 'reason': 'Not a function: a step s to s admits s + 1 splits when s2 = s (kernel split_not_determined; native decompositions).'}]
    counterexamples = [
        {'id': 'subset_violated', 'statement': 'W={0}, D={1}, B={}: |next|=1 but |W|-|D|+|B|=0.', 'scope': 'Instance; kernel fails_without_subset.'},
        {'id': 'overlap', 'statement': 'W={0,1}, D={0}, B={1}: |next|=1 but |W|-|D|+|B|=2.', 'scope': 'Instance; kernel fails_without_disjoint.'},
        {'id': 'natural_truncation', 'statement': 'W={0}, D={0,1}, B={}: truncated N identity gives 0 and |next|=0, though D is not inside W; the integer identity gives -1.', 'scope': 'Instance; kernel nat_truncation_masks_subset_violation.'},
        {'id': 'list_overlap', 'statement': 'Lists [0,1], discharge 0, births [1]: length identity holds (2=2-1+1) but the register [1,1] is not duplicate-free.', 'scope': 'Instance; kernel list_overlap_not_nodup.'}]
    return build_spec(
        node=NODE, short='demand_accounting', lean='DemandAccounting',
        anchors=['DemandAccounting.demand_accounting', 'DemandAccounting.card_next_exact', 'DemandAccounting.formula_iff',
                 'DemandAccounting.fails_without_subset', 'DemandAccounting.fails_without_disjoint',
                 'DemandAccounting.holds_accidentally_without_hypotheses', 'DemandAccounting.fails_of_excess_without_overlap', 'DemandAccounting.single_violation_fails', 'DemandAccounting.list_register_nodup_iff',
                 'DemandAccounting.nat_truncation_masks_subset_violation', 'DemandAccounting.every_step_is_an_accounting',
                 'DemandAccounting.split_not_determined', 'DemandAccounting.list_length_no_disjointness', 'DemandAccounting.list_overlap_not_nodup'],
        cases=[list(c) for c in producer.CASES], public_tsv=producer.public_tsv(), data=producer.certificate(),
        scope_review=('Read Paper.lean line 82 (a general List A theorem with a Bool predicate; no disjointness, the length identity is a filter partition), Paper001.lean line 86 (List Nat with Nodup, subset and disjointness; the disjointness hypothesis ranges over removeAll W D, i.e. births must avoid the survivors, not W or D, and only the Nodup conjunct uses it) and SnCarrier.activeObstructions (the displayed sequence is a table). '
                      'The source proofs are general but over lists; this node proves the Finset-cardinality statement, characterises exactly when it holds, and enumerates all triples over universes up to five elements. '
                      'The statement is not vacuous in the sources, but the DAG wording that both hypotheses are required is exact only for set cardinality and for the Nodup conjunct, not for the list length.'),
        predicates=['Independent dynamic program over universe elements tracking (|W|,|D|,|B|,|D minus W|,|(W minus D) cap B|), not the bitmask loops of the producer.',
                    'Class membership (hypotheses hold, one violated, both violated) recomputed from the excess and the overlap, with next cardinality |W| - |D| + excess + |B| - overlap.',
                    'Split counts by enumerating every D inside range(s) and every B outside the survivors (set enumeration, not the arithmetic of the producer); list-register counts by closed forms with falling factorials.',
                    'Theorem-level consistency: both hypotheses imply the identity (5^u triples, births may coincide with discharged elements), a single violation never satisfies the integer identity, class sizes sum to 8^u, list-register length identity universal and Nodup iff disjointness.',
                    'Exact cross-language (Python/Rust) wire equality and literal Lean axiom reports.'],
        boundary=boundary, generators=generators, relations=relations, compositions=compositions, failed_compositions=failed, counterexamples=counterexamples,
        open_obligations=['Count wrapper over preservation.demand_step (frozenset) with typed hypotheses.', 'Multiset and ordered-log registers.', 'Relation of s_n to the cumulative history |H_n|.',
                          'Any engine-specific survivor sequence.'],
        colour_meanings={'ActiveRegister': 'Finite set W of active demands', 'DischargedSet': 'Finite set D of discharged demands', 'BirthSet': 'Finite set B of births',
                         'SurvivorRegister': 'W minus D', 'Count': 'Natural number cardinality'},
        depends_on_result=True,
        qualification='The hypotheses are exact for set cardinality and for the Nodup conjunct; the list-length identity of the source needs no disjointness; the truncated natural-number identity can mask a violated subset hypothesis; the displayed survivor sequence is not constrained by the identity.',
        challenge_plan='Coordinate mutants of every certificate leaf plus nine semantic near misses: subset dropped, disjointness dropped, natural subtraction as violation detector, accidental agreement denied, births on discharged elements read as a violation, displayed sequence read as law, split forced by counts, list-register length identity needing disjointness, duplicate-free register without disjointness.',
        composition_tree=['register_count(register_birth(register_discharge(W, D), B))', 'count_step(register_count(W), register_count(D), register_count(B))'],
        construction='Exhaustive bitmask classification of all triples for u = 0..5, exact split counts for four count sequences and two list-register censuses; Lean proves the general Finset statements.',
        relation_evidence={'demand_accounting_identity': 'Kernel theorem; native class counts (5^u triples, all satisfying the identity).',
                           'identity_iff_excess_equals_overlap': 'Kernel theorem formula_iff; native counts of the four classes.',
                           'count_sequence_is_not_a_law': 'Kernel every_step_is_an_accounting; native split counts.'})


if __name__ == '__main__':
    print(write_spec(HERE, NODE, spec()))
