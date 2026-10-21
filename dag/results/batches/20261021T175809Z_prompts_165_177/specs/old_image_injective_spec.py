"""Build specs/PG-OLD-IMAGE-INJECTIVE.json from the producer and the node's reviewed claims."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp/batch_tools'))
from spec_builder import build_spec, write_spec  # noqa: E402

_s = importlib.util.spec_from_file_location('producer', ROOT / 'code/python/src/qm/pfp_old_image_injective.py')
producer = importlib.util.module_from_spec(_s)
_s.loader.exec_module(producer)

NODE = 'PG-OLD-IMAGE-INJECTIVE'
H = 'Types A, B, E (finite only for the counting relations), a lift u : A -> B and r : B -> A + E with r(u a) = inl a for every a; nothing is assumed off the image of u.'
P0 = 'omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Paper.lean'
P1 = 'omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean'


def spec():
    boundary = {
        'supports': ('Kernel-checked (types in Type): for arbitrary A, B, E the old-image law r(u a) = inl a implies u injective, hence |A| <= |B| when finite; for arbitrary A, B and E = Unit every injective lift has a law-satisfying recovery r : B -> A + Unit (injective_iff_exists_law; with E empty the converse fails when A is empty and B is not); for injective u the law can be extended by any single value x : A + E at all off-image points (law_freedom_off_image; the independent free value at each off-image point is the content of law_card), so for an off-image point and an old term a0 there are two law-satisfying recoveries, one refusing and one accepting it (off_image_not_implied_general); for any lift u and recovery r, with A nonempty and two distinct observation values, there are observations q, q2 with q2 after u different from q (observation_not_implied_general; the law hypothesis is not used), while q := q2 after u preserves observations on the same lift (observation_preserved_possible), so observation preservation is an extra condition the law neither implies nor excludes; the identity lift satisfies the law while leaving every predicate on the old terms unchanged (repair_not_implied_general, a persistence statement for the identity lift only); for finite A, B and injective u the number of law-satisfying recoveries into A + Unit is (|A|+1)^(|B|-|A|) (law_card). The three source negative boundaries are fixed Fin instances and are reproduced as such. '
                     'Native: exhaustive enumeration of all (u, r) pairs for eleven (|A|,|B|,|O|) cases with |A|,|B| <= 4: the number of law pairs, none with a non-injective lift, the number that refuse every off-image point (one per injective lift) and those that do not, observation pairs preserved, and obstruction pairs that persist or clear, all exact integers. Column definitions: persists = number of (law pair, oA, oB) with some a such that oA a and oB (u a); cleared = number with oA nonempty and no such a; these are counting conventions, not a repair notion. obs_preserved, persists and cleared are the law-pair count times a factor independent of r, so they carry no information about the law; the Lean statements carry that claim. The agreement of the producer enumeration with the checker closed forms is the independent evidence, not either alone.'),
        'does_not_support': ('Off-image rejection as a property of the S(n) retraction (that is PG-SN-OFF-IMAGE-REFUSAL, which needs an added soundness hypothesis on r); the pinned SnCarrier lift and retraction; any definition of obstruction repair beyond persistence of a Boolean predicate through a lift (the source repair_not_implied instance uses the constant-true predicate and defines no repair); sets with more than four elements in the native census (the Lean count law_card is general for finite types); infinite types for the count; any physical or categorical reading.'),
        'narrowest_claim': 'A recovery r : B -> A + Unit obeying r(u a) = inl a exists exactly when u is injective. For an injective lift it is determined only on the image: there are (|A|+1)^(|B|-|A|) of them, exactly one of which refuses every off-image point; when |A| >= 1 and |B| > |A| the others accept some off-image point as an old term, and for |B| = |A| or |A| = 0 the recovery is unique. The law fixes neither observations nor obstruction predicates (persistence through the identity lift only).',
        'next_test': 'Define repair of an obstruction for a lift (a witness-count or chain criterion on the lifted pair) and decide for the identity embedding and for a non-identity injective lift whether the old obstruction count strictly drops, replacing the constant-predicate instance of repair_not_implied by a statement with a stated repair criterion.'}
    generators = [
        {'id': 'lift', 'source_declarations': [P0 + '::old_image_injective (line 54) binder u : A -> B (function-valued premise, no definition)', P1 + '::old_image_injective (line 103) binder u : A -> B'],
         'ordered_inputs': ['OldTerm'], 'output': 'NewTerm', 'semantic_predicate': 'An arbitrary function u : A -> B; injectivity is a consequence of the law, not an assumption.', 'hypotheses': [H]},
        {'id': 'typed_recovery', 'source_declarations': [P0 + '::old_image_injective (line 54) binder r : B -> Sum A E', P1 + '::old_image_injective (line 103) binder r : B -> Sum A Unit'],
         'ordered_inputs': ['NewTerm'], 'output': 'OldTermOrRefusal', 'semantic_predicate': 'A function r : B -> A + E (E = Unit in Paper001); nothing is required of it off the image of u.', 'hypotheses': [H]},

        {'id': 'old_image', 'source_declarations': [P1 + '::off_image_not_implied (line 111) quantifies over b with forall a, u a != b (the complement of the image)'],
         'ordered_inputs': ['NewTerm'], 'output': 'ImageTest', 'semantic_predicate': 'Membership of b in the range of u.', 'hypotheses': [H]}]
    relations = [
        {'id': 'old_image_law_implies_injective', 'source_declarations': [P0 + '::old_image_injective (line 54): a general theorem over arbitrary types A B E', P1 + '::old_image_injective (line 103): the same with E = Unit'],
         'equation_or_predicate': 'r(u a) = inl a for all a implies u injective', 'typing_conditions': 'u : A -> B, r : B -> A + E', 'evidence_status': 'Kernel theorem old_image_injective; native: zero law pairs with a non-injective lift in every case', 'scope': 'All types'},
        {'id': 'old_image_law', 'source_declarations': [P0 + '::old_image_injective (line 54) hypothesis old : forall a, r (u a) = Sum.inl a', P1 + '::old_image_injective (line 103) hypothesis h'],
         'equation_or_predicate': 'r(u a) = inl a for all a (the hypothesis of the theorem)', 'typing_conditions': 'u : A -> B, r : B -> A + E', 'evidence_status': 'Definition OldImageLaw; native: tested on every (u, r) pair of the census', 'scope': 'All types'},
        {'id': 'injective_iff_recovery_exists', 'source_declarations': ['no source declaration; new converse'],
         'equation_or_predicate': 'u injective iff some r : B -> A + Unit satisfies the old-image law', 'typing_conditions': 'u : A -> B', 'evidence_status': 'Kernel theorem injective_iff_exists_law (E = Unit only); native: law_refusing = injective_u and law_noninjective = 0, i.e. exactly the injective lifts carry a law pair, one refusing pair each', 'scope': 'All types A, B with E = Unit'},
        {'id': 'off_image_not_implied', 'source_declarations': [P1 + '::off_image_not_implied (line 111): a fixed instance Fin 1 -> Fin 2, not a general statement'],
         'equation_or_predicate': 'for injective u and b0 off the image there are law-satisfying r (refusing b0) and r2 (accepting b0)', 'typing_conditions': 'u injective, b0 outside the range', 'evidence_status': 'Kernel theorems law_freedom_off_image, off_image_not_implied_general (all types) and off_image_not_implied_instance; native nonrefusing counts', 'scope': 'All types'},
        {'id': 'observation_not_implied', 'source_declarations': [P1 + '::observation_not_implied (line 128): a fixed instance on Fin 2'],
         'equation_or_predicate': 'the law does not imply q2 after u = q', 'typing_conditions': 'Nonempty A and two distinct observation values', 'evidence_status': 'Kernel theorem observation_not_implied_general and instance; native obs_preserved < obs_total', 'scope': 'All types'},
        {'id': 'repair_not_implied', 'source_declarations': [P1 + '::repair_not_implied (line 138): a fixed instance with the constant-true predicate; it defines no notion of repair'],
         'equation_or_predicate': 'the identity lift satisfies the law and leaves every predicate unchanged', 'typing_conditions': 'u = id', 'evidence_status': 'Kernel theorem repair_not_implied_general (weak: persistence only) and instance; native persists/cleared counts', 'scope': 'Persistence of a Boolean predicate through a lift; not a repair theorem'},
        {'id': 'law_count', 'source_declarations': ['no source declaration; new counting theorem'],
         'equation_or_predicate': 'for injective u between finite types the number of law-satisfying r : B -> A + Unit is (|A|+1)^(|B|-|A|)', 'typing_conditions': 'finite A, B', 'evidence_status': 'Kernel theorem law_card; native law counts for eleven cases', 'scope': 'All finite types'}]
    compositions = [
        {'outer_operation': 'typed_recovery', 'input_slot': 0, 'inner_operation': 'lift', 'colour_match': 'NewTerm', 'hypothesis_match': H,
         'licensing_relations': ['old_image_law', 'old_image_law_implies_injective', 'law_count'], 'evidence_status': 'Kernel and native'}]
    failed = [
        {'composition': 'lift o typed_recovery as a map B -> B', 'reason': 'Not a map: the refusal summand of A + E has no image under u (source paper, section 10); a partial composite exists only on the non-refused part.'},
        {'composition': 'old_image applied to typed_recovery to conclude refusal', 'reason': 'The law constrains r only on the image of u; off the image r is free, so refusal does not follow (kernel off_image_not_implied_general).'}]
    counterexamples = [
        {'id': 'off_image_accepts', 'statement': 'u : Fin 1 -> Fin 2 constant 0; r = (0 -> inl 0, 1 -> inr ()) and r2 = constant inl 0 both obey the law; r2 accepts the off-image point 1.', 'scope': 'Instance; kernel off_image_not_implied_instance.'},
        {'id': 'observations_unconstrained', 'statement': 'identity lift on Fin 2 with q = 0 and q2 = val: law holds, q2 after u != q.', 'scope': 'Instance; kernel observation_not_implied_instance.'},
        {'id': 'obstruction_persists', 'statement': 'identity lift on Fin 1 with the constant-true predicate: law holds, the obstruction persists at 0 and at u 0.', 'scope': 'Instance with a constant predicate; kernel repair_not_implied_instance.'}]
    return build_spec(
        node=NODE, short='old_image_injective', lean='OldImageInjective',
        anchors=['OldImageInjective.old_image_injective', 'OldImageInjective.injective_iff_exists_law', 'OldImageInjective.law_freedom_off_image',
                 'OldImageInjective.off_image_not_implied_general', 'OldImageInjective.off_image_not_implied_instance',
                 'OldImageInjective.observation_not_implied_general', 'OldImageInjective.observation_preserved_possible', 'OldImageInjective.observation_not_implied_instance',
                 'OldImageInjective.repair_not_implied_general', 'OldImageInjective.repair_not_implied_instance',
                 'OldImageInjective.law_card_le', 'OldImageInjective.law_card'],
        cases=[list(c) for c in producer.CASES], public_tsv=producer.public_tsv(), data=producer.certificate(),
        scope_review=('No operation candidate was recovered, so the declarations were mined by hand: Paper.lean line 54 (old_image_injective, a general theorem over arbitrary types A B E) and Paper001.lean lines 103 (E = Unit), 111, 128, 138. '
                      'The injectivity theorem is general and non-vacuous. The three negative-boundary theorems are fixed Fin instances (off_image_not_implied: u constant 0 and r constant inl 0 on Fin 1 -> Fin 2; observation_not_implied: identity on Fin 2; repair_not_implied: the constant-true predicate on Fin 1), and repair_not_implied states only that a constant-true predicate stays true, so it defines no repair. '
                      'This node proves the general forms of the first two boundaries, a converse and an exact count, keeps the repair statement at the weak persistence reading, and enumerates all (u, r) pairs for small finite sets to see that the claim could fail on them.'),
        predicates=['Closed-form counts (falling factorial times (a+1)^(b-a), 2^(b-a)(4^a-3^a)) with no enumeration of functions and no import of the producer.',
                    'Theorem-level consistency: no law pair with a non-injective lift, refusing plus non-refusing law pairs equal the law pairs, no recovery when |A| > |B|.',
                    'Exact cross-language (Python/Rust) wire equality and literal Lean axiom reports.'],
        boundary=boundary, generators=generators, relations=relations, compositions=compositions, failed_compositions=failed, counterexamples=counterexamples,
        open_obligations=['A definition of obstruction repair for a lift and a theorem deciding it.', 'Off-image refusal for the pinned S(n) retraction (PG-SN-OFF-IMAGE-REFUSAL).',
                          'Infinite sets: injectivity holds, but the count law_card is for finite types only.'],
        colour_meanings={'OldTerm': 'Element of the old set A', 'NewTerm': 'Element of the lifted set B', 'OldTermOrRefusal': 'Element of A + E (E = Unit is the refusal)', 'ImageTest': 'Membership in the range of u'},
        depends_on_result=True,
        qualification='The injectivity statement is general; off-image rejection and observation preservation are shown not to follow for all types, while the source repair_not_implied is a constant-predicate instance and does not define repair, so only persistence of a predicate through a lift is shown.',
        challenge_plan='Coordinate mutants of every certificate leaf plus eleven semantic near misses: law forces refusal, law without injectivity, law forces observation preservation, law repairs obstructions, recovery for a larger source, recovery unique per lift, every pair satisfies the law, law count ignoring the refusal summand, law forcing onto lifts, empty-source observation failure, non-refusing recovery of a bijective lift.',
        composition_tree=['typed_recovery(lift(a))'],
        construction='Exhaustive enumeration of all lifts and recoveries for eleven small cases; Lean proves the general statements and the count for finite types.',
        relation_evidence={'old_image_law_implies_injective': 'Kernel theorem; no law pair with a non-injective lift in any census record.',
                           'off_image_not_implied': 'Kernel theorems; native non-refusing law pairs are 72 of 96 at (3,4).',
                           'law_count': 'Kernel law_card equals the native law counts, e.g. 18 at (2,3) and 96 at (3,4).'})


if __name__ == '__main__':
    print(write_spec(HERE, NODE, spec()))
