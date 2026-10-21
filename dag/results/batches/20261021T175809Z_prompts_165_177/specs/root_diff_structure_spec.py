"""Build specsB/PG-ROOT-DIFF-STRUCTURE.json from the producer and the node's reviewed claims."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp/batch_tools'))
from spec_builder import build_spec, write_spec  # noqa: E402

_s = importlib.util.spec_from_file_location('producer', ROOT / 'code/python/src/qm/pfp_root_diff_structure.py')
producer = importlib.util.module_from_spec(_s)
_s.loader.exec_module(producer)

NODE = 'PG-ROOT-DIFF-STRUCTURE'
OB = 'lean4/OntologyBasic.lean'
H = ('Two channels with arbitrary payload types PD (difference) and S (structure); the coproduct has the two-constructor shape of OntologyBasic.Real0. '
     'Both channels are POSITED, not derived: this node proves only what the coproduct construction asserts and does not assert.')


def spec():
    boundary = {
        'supports': ('Kernel-checked for arbitrary types PD, S, with Real0 PD S given the two-constructor shape of OntologyBasic.Real0: both injections are injective, their ranges are disjoint and exhaustive, Real0 is equivalent to PD + S, '
                     'every pair of maps out of the channels has exactly one extension (universal property), and the number of maps out of the coproduct is the product of the numbers of maps out of the channels (|C|^(|PD|+|S|)). '
                     'A map out of the coproduct that is the identity on one channel (a retraction onto it) exists iff that channel is nonempty or the other channel is empty: a retraction onto the difference channel is impossible only when that channel is empty and the structure channel is not (and symmetrically); '
                     'whenever both channels are inhabited retractions in both directions exist (retractions_both_ways_of_nonempty), each one of |A|^|B| choices that the coproduct does not select. So bare function-existence is trivial for inhabited channels and does NOT formalise "no reduction of either channel to the other". '
                     'Real0 is nonempty iff a channel is, empty for two empty channels, and all four combinations of the two nonemptiness posits are realised, so neither posit follows from the construction or from the other. '
                     'Native exhaustive tables: 38 map counts (|A|,|B| <= 2 with |C| <= 3, plus (3,2,2) and (2,3,2)), 16 retraction tables for |A|,|B| <= 3, and the four-row posit table; the injection, disjointness and covering columns are set facts built from the tags, so the kernel theorems are the evidence for them.'),
        'does_not_support': ('Anything about the actual OntologyBasic.Real0 beyond its constructor shape (the file is not imported; its payloads are universe-polymorphic record types). The real Real0 has the record TYPES PrimitiveDifference and Structure as channels; both are inhabited, so by retracts_to_pd_iff and retracts_to_s_iff retractions in both directions exist for it: the emptiness cases of this file are not instances of the real node, and nothing here says either channel is irreducible to the other. '
                             'That either channel exists, is real or has an origin (admitted posits, ENC-1138 lineage withdrawn); the passage from the literal inscription (PG-INERT-DIAMOND, route marked GAP_NO_DERIVATION); the clauses "carrier-Structure precedes a primitive difference", "residual-Structure Q^1 = C^1/im d0 is what the difference produces" and "the ladder is a definability order"; any physical or interpretive reading.'),
        'narrowest_claim': ('The typed coproduct of two payload types (same two-constructor shape as OntologyBasic.Real0) is a categorical coproduct that supplies no map between the channels and no element of either channel: a map out of it that is the identity on one channel exists exactly when that channel is nonempty or the other is empty (so bare existence of such a map is not a reduction theorem for inhabited channels), and the two nonemptiness conditions are independent of the construction and of each other.'),
        'next_test': ('Formalise the clause "carrier-Structure precedes a primitive difference": define precedence as the statement that a PrimitiveDifference record can be built with no Structure value in scope (Source := PUnit) and a Structure record with no PrimitiveDifference, then decide whether Source must equal Structure.Carrier for the node text to be meant, by a finite model or a counterexample.')}
    generators = [
        {'id': 'inject_difference', 'source_declarations': [OB + '::Real0.primitiveDifference (line 27 inductive Real0, first constructor) - a constructor taking the PrimitiveDifference RECORD (line 12), not an element of a carrier'],
         'ordered_inputs': ['DifferencePayload'], 'output': 'Real0', 'semantic_predicate': 'Left injection of the coproduct; injective, range disjoint from the structure range.', 'hypotheses': [H]},
        {'id': 'inject_structure', 'source_declarations': [OB + '::Real0.structure (line 27 inductive Real0, second constructor) taking the Structure RECORD (line 19)'],
         'ordered_inputs': ['StructurePayload'], 'output': 'Real0', 'semantic_predicate': 'Right injection of the coproduct; injective, range disjoint from the difference range.', 'hypotheses': [H]},
        {'id': 'copair', 'source_declarations': ['no source declaration; Real0 has no eliminator named in OntologyBasic beyond Lean\'s recursor; universal property proved here'],
         'ordered_inputs': ['DifferenceMap', 'StructureMap'], 'output': 'Real0Map', 'semantic_predicate': 'The unique map out of the coproduct restricting to the two given maps.', 'hypotheses': [H]},
        {'id': 'retraction_candidate', 'source_declarations': ['no source declaration; the node text says "no reduction of either channel to the other"'],
         'ordered_inputs': ['Real0'], 'output': 'DifferencePayload', 'semantic_predicate': 'A map out of the coproduct that is the identity on the difference channel; exists only when the difference channel is nonempty or the structure channel is empty.', 'hypotheses': [H]}]
    relations = [
        {'id': 'injections_disjoint_and_injective', 'source_declarations': [OB + '::Real0 (line 27): an inductive type, so constructor injectivity and disjointness hold by the kernel; the source bridge theorem pg_root_coproduct_inert_diamond_and_six_operation_separation (DerivationDagQMClosure.lean line 1111) states `d + 0 = d` and `0 + s = s` on Int and (0:Nat) != 1, which are not coproduct statements'],
         'equation_or_predicate': 'inl, inr injective; inl d != inr s; every element is in one range', 'typing_conditions': 'any payload types', 'evidence_status': 'Kernel theorems pd_injective, st_injective, pd_ne_st, exhaustive; native tables', 'scope': 'All types'},
        {'id': 'universal_property', 'source_declarations': ['no source declaration'], 'equation_or_predicate': 'for f : PD -> C and g : S -> C there is exactly one h with h o inl = f and h o inr = g', 'typing_conditions': 'any types',
         'evidence_status': 'Kernel theorem universal; native unique_copairs column', 'scope': 'All types'},
        {'id': 'maps_out_count', 'source_declarations': ['no source declaration'], 'equation_or_predicate': '|Real0 -> C| = |PD -> C| * |S -> C| = |C|^(|PD|+|S|)', 'typing_conditions': 'finite types',
         'evidence_status': 'Kernel theorems card_maps_out, card_maps_out_pow; native 38-row table (|A|,|B| <= 2 with |C| <= 3, plus (3,2,2) and (2,3,2))', 'scope': 'All finite types'},
        {'id': 'retraction_iff_emptiness', 'source_declarations': ['no source declaration'], 'equation_or_predicate': 'retraction onto PD exists iff PD nonempty or S empty; symmetric for S', 'typing_conditions': 'any types',
         'evidence_status': 'Kernel theorems retracts_to_pd_iff, retracts_to_s_iff, no_reduction_to_pd, no_reduction_to_s, retractions_both_ways_of_nonempty; native 16-row table (counts |A|^|B|, |B|^|A|)', 'scope': 'All types'},
        {'id': 'posits_independent', 'source_declarations': ['Admitted imports of the node: "Primitive difference delta_0 (assumption)", "Structure carrier (assumption: declared, not derived)"'], 'equation_or_predicate': 'for every pair of truth values for (PD nonempty, S nonempty) some pair of channels realises it; Real0 nonempty iff a channel is',
         'typing_conditions': 'any types', 'evidence_status': 'Kernel theorems posits_independent, nonempty_real0_iff, real0_empty_of_both_empty; native posit table', 'scope': 'All types; does not turn either posit into a theorem'}]
    compositions = [
        {'outer_operation': 'retraction_candidate', 'input_slot': 0, 'inner_operation': 'inject_structure', 'colour_match': 'Real0', 'hypothesis_match': 'Applied to a structure item; defined only when a retraction exists.',
         'licensing_relations': ['retraction_iff_emptiness'], 'evidence_status': 'Kernel theorem retracts_to_pd_iff; conditional on nonemptiness'}]
    failed = [
        {'composition': 'retraction_candidate(inject_structure(s)) with an empty difference channel', 'reason': 'No map from a nonempty structure channel to an empty difference channel exists (kernel no_reduction_to_pd); the coproduct asserts no reduction.'},
        {'composition': 'inject_structure s identified with inject_difference d', 'reason': 'The ranges are disjoint (kernel pd_ne_st): no identification, so no reduction by equation.'}]
    counterexamples = [
        {'id': 'empty_difference_channel', 'statement': 'PD empty, S of size 1: Real0 has one element and no retraction onto PD exists; retractions onto S exist.', 'scope': 'Instance of retraction_iff_emptiness.'},
        {'id': 'two_empty_channels', 'statement': 'Both channels empty: Real0 is empty; the construction alone does not give a root element.', 'scope': 'Kernel theorem real0_empty_of_both_empty.'}]
    return build_spec(
        node=NODE, short='root_diff_structure', lean='RootDiffStructure',
        anchors=['RootDiffStructure.pd_injective', 'RootDiffStructure.st_injective', 'RootDiffStructure.pd_ne_st', 'RootDiffStructure.exhaustive',
                 'RootDiffStructure.no_identification', 'RootDiffStructure.universal', 'RootDiffStructure.card_real0', 'RootDiffStructure.card_maps_out',
                 'RootDiffStructure.card_maps_out_pow', 'RootDiffStructure.retracts_to_pd_iff', 'RootDiffStructure.retracts_to_s_iff',
                 'RootDiffStructure.no_reduction_to_pd', 'RootDiffStructure.no_reduction_to_s', 'RootDiffStructure.retractions_both_ways_of_nonempty', 'RootDiffStructure.nonempty_real0_iff',
                 'RootDiffStructure.real0_empty_of_both_empty', 'RootDiffStructure.posits_independent'],
        cases=[list(c) for c in producer.CASES], public_tsv=producer.public_tsv(), data=producer.certificate(),
        scope_review=('Mined OntologyBasic.lean (sha256 7ba6024a matches): PrimitiveDifference (line 12, a record Source/Target/delta), Structure (line 19, a record with Carrier and five Props) and Real0 (line 27, an inductive with one constructor per record type). '
                      'Real0 is a tagged union of the two record types; its coproduct properties are kernel facts about any such inductive and the file proves none of them. The bound bridge theorem pg_root_coproduct_inert_diamond_and_six_operation_separation (DerivationDagQMClosure.lean line 1111, sha256 c9ad9c23) is a conjunction of integer identities, (0:Nat) != 1 and a Fin 6 index coding: it contains no coproduct statement, so it is vacuous for this node. '
                      'The Rust omega_types primitive_difference.rs (external, sha256 matches) defines a zero-difference relation with factors_through, a different notion of primitive difference from OntologyBasic.PrimitiveDifference; neither contains the claims about precedence of the carrier or the definability ladder. '
                      'This node is an ADMITTED primitive: the Lean module proves the coproduct property for arbitrary payload types and the neutrality of the construction about the two posits, and does not turn either posit into a theorem.'),
        predicates=['Maps out of the coproduct counted by the closed form c^(a+b) = c^a * c^b; the producer enumerates every function.',
                    'Retractions counted as |A|^|B| (every g : B -> A gives exactly one copair(id, g)); the producer filters all functions on the coproduct.',
                    'Existence of a retraction decided by the emptiness criterion, not by search; non-reduction pinned for an empty channel facing a nonempty one.',
                    'Maps out of the coproduct are enumerated and grouped by their pair of restrictions in the checker (unique_copairs is a count, not a formula); injection, disjointness and covering flags are checked against sets the checker builds from the tags, so the kernel theorems, not the tables, are the evidence for them; exact Python/Rust wire equality and literal Lean axiom reports.'],
        boundary=boundary, generators=generators, relations=relations, compositions=compositions, failed_compositions=failed, counterexamples=counterexamples,
        open_obligations=['The clause "carrier-Structure precedes a primitive difference" (a dependency order) is not formalised or tested.',
                          'The clause that residual-Structure Q^1 = C^1/im d0 is what the difference produces, and that the ladder is a definability order that mints no authority.',
                          'The actual OntologyBasic.Real0 with its universe-polymorphic record payloads (not imported here).',
                          'Any derivation of either channel, or of the passage from the literal inscription (PG-INERT-DIAMOND).'],
        colour_meanings={'DifferencePayload': 'Payload of the primitive-difference channel', 'StructurePayload': 'Payload of the structure channel', 'Real0': 'Coproduct of the two channels',
                         'DifferenceMap': 'Map from the difference channel to a target', 'StructureMap': 'Map from the structure channel to a target', 'Real0Map': 'Map out of the coproduct'},
        depends_on_result=True,
        qualification='The coproduct statement "no reduction of either channel to the other and no origin of either" is supported only as neutrality of the typed coproduct construction; the precedence and definability clauses are not addressed and the posits remain admitted.',
        challenge_plan='Coordinate mutants of every certificate leaf plus nine semantic near misses: overlapping ranges, an always-existing reduction, a canonical reduction, maps-out count as a sum, a coproduct without posits, structure posit entailing difference, missing copair, swapped direction, coproduct size as a max.',
        composition_tree=['retraction_candidate(inject_structure(s))'],
        construction='Exhaustive map tables for channels of size at most 2 (two rows at 3) and codomains of size at most 3, retraction tables for channels of size at most 3; Lean proves the general coproduct and neutrality statements.',
        relation_evidence={'retraction_iff_emptiness': 'Kernel iff; native counts |A|^|B| agree with existence for all 16 size pairs.',
                           'posits_independent': 'Kernel theorem for every pair of truth values; native posit table covers the four size classes.'})


if __name__ == '__main__':
    print(write_spec(HERE, NODE, spec()))
