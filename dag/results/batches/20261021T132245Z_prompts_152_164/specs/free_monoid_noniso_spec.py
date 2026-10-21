"""Build specs/PG-FREE-MONOID-NONISO.json from the producer and the node's reviewed claims."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp/batch_tools'))
from spec_builder import build_spec, write_spec  # noqa: E402

_s = importlib.util.spec_from_file_location('producer', ROOT / 'code/python/src/qm/pfp_free_monoid_noniso.py')
producer = importlib.util.module_from_spec(_s)
_s.loader.exec_module(producer)

NODE = 'PG-FREE-MONOID-NONISO'
H = ('Alphabets are arbitrary types in Lean and the finite sets {0..n-1} natively; the structure compared is the multiplication of the free monoid (words with concatenation); '
     'an isomorphism is a multiplicative bijection; a discrete category has only identity morphisms. Native homomorphism search is bounded by image length d <= 2 and word length 2.')
SRC = 'omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/'
PAPER = SRC + '000_pre_genesis_to_mssn/lean4/Paper.lean'
P001 = SRC + '001_sn_mssn/lean4/Paper001.lean'
CHECKS = SRC + '001_sn_mssn/code/sn_mssn_checks.py'


def spec():
    boundary = {
        'supports': ('For arbitrary alphabets (kernel-checked, lean4/FreeMonoidNoniso.lean, Mathlib FreeMonoid and CategoryTheory.Discrete): a monoid isomorphism FreeMonoid a ~ FreeMonoid b induces a bijection of the alphabets (the atoms are the one-letter words and an isomorphism permutes atoms), so unequal finite alphabets give non-isomorphic free monoids, and FreeMonoid a ~ FreeMonoid b iff a ~ b; '
                     'alphabetEquiv, no_free_monoid_iso, freeMonoid_iso_iff_equiv, set_bijection_exists and the discrete-category theorems use Classical.choice (kernel axiom reports: propext, Classical.choice, Quot.sound), as does the source for the same step; '
                     'an equivalence of discrete categories Discrete a ~ Discrete b (a genuine CategoryTheory.Equivalence) gives a bijection a ~ b, so Fin n and Fin m give equivalent discrete categories iff n = m; every source WordIso yields a MulEquiv (WordIso.toMulEquiv) and the source theorem is recovered through it; the converse MulEquiv -> WordIso is not stated; '
                     'the boundary is sharp: for n, m >= 1 the underlying SETS of FreeMonoid (Fin n) and FreeMonoid (Fin m) are in bijection (both countably infinite), so the content is multiplicativity, not cardinality; the free monoid on the empty alphabet is one point; words of length k over Fin n number n^k and atoms number n. '
                     'Exhaustive native checks on 15 alphabet pairs (sizes 0 to 4): all homomorphisms whose generator images have length <= 1 for the pairs (3,4), (4,3), (4,4) and length <= 2 for all other pairs; '
                     'the candidates injective on words of length <= 2 whose images contain every letter (a necessary-condition filter, not a proof of bijectivity) are exactly the n! letter permutations when n = m and none otherwise; the equivalences of discrete categories are exactly the bijections; '
                     'and the explicit shortlex bijection of the underlying sets is multiplicative on the first 30 words exactly when n = m (a prefix statement).'),
        'does_not_support': ('Any structure on numerals or alphabets other than the free-monoid multiplication or the discrete category (a numeral or alphabet re-presentation may still be a non-isomorphic map, a set bijection, or an isomorphism of some other structure; no other structure, such as free commutative monoids, is examined); '
                             'language restriction, partial recovery and total erasure (separate ledger row WDP-P001-009); infinite alphabets beyond the general Lean statement; the native homomorphism search covers short generator images only and is an instance, not the general theorem.'),
        'narrowest_claim': ('A monoid isomorphism between free monoids on any two alphabets induces a bijection of the alphabets, so free monoids on finite alphabets of different sizes are not isomorphic and discrete categories with different finite object counts are not equivalent; '
                            'a bare bijection of the underlying sets does exist for sizes at least one, so a numeral or alphabet re-presentation cannot be an isomorphism of the free-monoid (word concatenation) structure or of the discrete-category structure; other structures are not addressed.'),
        'next_test': ('Decide which numeral or alphabet re-presentations ARE structure-preserving: classify the monoid homomorphisms between free monoids on different alphabet sizes that are injective (codes) or onto (decoders), '
                      'and prove which of them preserve atoms, as the next step beyond the isomorphism obstruction proved here.')}
    generators = [
        {'id': 'free_monoid', 'source_declarations': [PAPER + '::WordIso (line 200, structure on List A: the free monoid presented as lists)', P001 + '::MonoidIso (line 193, structure on List alpha)'],
         'ordered_inputs': ['Alphabet'], 'output': 'FreeMonoid', 'semantic_predicate': 'Words over the alphabet with concatenation and the empty word.', 'hypotheses': [H]},
        {'id': 'atoms', 'source_declarations': [PAPER + '::unitAtom (line 177) and ::word_atom_iff_singleton (line 180, general theorem)', P001 + '::Indecomposable (line 147) and ::indecomposable_iff (line 175, general theorem)'],
         'ordered_inputs': ['FreeMonoid'], 'output': 'AtomSet', 'semantic_predicate': 'Nonidentity elements that are not a product of two nonidentity elements; exactly the one-letter words.', 'hypotheses': [H]},
        {'id': 'monoid_iso', 'source_declarations': [PAPER + '::WordIso (line 200, definition)', P001 + '::MonoidIso (line 193, definition)'],
         'ordered_inputs': ['FreeMonoid', 'FreeMonoid'], 'output': 'IsoSet', 'semantic_predicate': 'Multiplicative bijections with multiplicative inverse (a MulEquiv).', 'hypotheses': [H]},
        {'id': 'alphabet_bijection', 'source_declarations': [PAPER + '::word_iso_alphabet_bijection (line 238, general theorem using Classical.choice)', P001 + '::iso_letters (line 235) and ::no_free_monoid_iso (line 353, general theorem)'],
         'ordered_inputs': ['IsoSet'], 'output': 'AlphabetBijection', 'semantic_predicate': 'Restriction of an isomorphism to the atoms, read back as a bijection of alphabets.', 'hypotheses': [H]},
        {'id': 'discrete_category', 'source_declarations': [P001 + '::DiscreteEquiv (line 373, definition: a pair of mutually inverse maps of objects, i.e. a bijection, by definition)'],
         'ordered_inputs': ['Alphabet'], 'output': 'DiscreteCategory', 'semantic_predicate': 'A category whose only morphisms are identities.', 'hypotheses': [H]},
        {'id': 'discrete_equivalence_objects', 'source_declarations': [P001 + '::no_discrete_equivalence (line 379, general theorem about the DiscreteEquiv structure)'],
         'ordered_inputs': ['DiscreteCategory', 'DiscreteCategory'], 'output': 'AlphabetBijection', 'semantic_predicate': 'An equivalence matches isomorphism classes bijectively; classes of a discrete category are its objects.', 'hypotheses': [H]}]
    relations = [
        {'id': 'atoms_are_letters', 'source_declarations': [PAPER + '::word_atom_iff_singleton (line 180)', P001 + '::indecomposable_iff (line 175)'],
         'equation_or_predicate': 'x is an atom iff x = of a for a letter a', 'typing_conditions': 'FreeMonoid', 'evidence_status': 'Kernel theorem isAtom_iff; native atom counts', 'scope': 'Arbitrary alphabets'},
        {'id': 'iso_preserves_atoms', 'source_declarations': [PAPER + '::word_iso_preserves_atoms (line 214)', P001 + '::iso_preserves_indecomp (line 213)'],
         'equation_or_predicate': 'IsAtom (e x) iff IsAtom x for every monoid isomorphism e', 'typing_conditions': 'IsoSet x AtomSet', 'evidence_status': 'Kernel theorem isAtom_map_iff (any monoids); native bijective candidates are permutations', 'scope': 'Arbitrary monoids'},
        {'id': 'iso_gives_alphabet_bijection', 'source_declarations': [PAPER + '::word_iso_alphabet_bijection (line 238)', P001 + '::no_free_monoid_iso (line 353)'],
         'equation_or_predicate': 'FreeMonoid a ~ FreeMonoid b (as monoids) iff a ~ b (as sets); hence n != m implies no isomorphism', 'typing_conditions': 'IsoSet -> AlphabetBijection',
         'evidence_status': 'Kernel theorems alphabetEquiv, freeMonoid_iso_iff_equiv, no_free_monoid_iso (Classical.choice via Equiv.ofBijective); native exhaustive search', 'scope': 'Arbitrary alphabets'},
        {'id': 'discrete_equivalence_is_bijection', 'source_declarations': [P001 + '::no_discrete_equivalence (line 379; its DiscreteEquiv is a bijection by definition, so the source statement is the pigeonhole fact)', CHECKS + '::discrete_categories_inequivalent (returns left != right, a tautology)'],
         'equation_or_predicate': 'Discrete a ~ Discrete b (categorical equivalence) gives a ~ b; for Fin n, Fin m it holds iff n = m', 'typing_conditions': 'DiscreteCategory x DiscreteCategory',
         'evidence_status': 'Kernel theorems discrete_equivalence_card, discrete_equivalence_iff; native count of mutually inverse pairs', 'scope': 'Arbitrary types; finite counts for Fin'},
        {'id': 'set_bijection_but_not_iso', 'source_declarations': ['no source declaration; the paper (section 11.1) says decoders can map the strings onto the same natural numbers without making the monoids identical'],
         'equation_or_predicate': 'FreeMonoid (Fin n) and FreeMonoid (Fin m) are in set bijection for n, m >= 1, with n != m giving no multiplicative one', 'typing_conditions': 'FreeMonoid x FreeMonoid',
         'evidence_status': 'Kernel theorems set_bijection_exists, bijection_but_not_isomorphic; native shortlex bijection and violation counts', 'scope': 'n, m >= 1'},
        {'id': 'dag_local_theorem_is_vacuous', 'source_declarations': ['lean4/DerivationDagQMClosure.lean::pg_to_sn_and_wdp_route_chain_composition (line 1257, fixed arithmetic about 1+1=2, a Fin 3 injectivity and two list literals; mentions neither monoids nor alphabets, vacuous)'],
         'equation_or_predicate': 'none: no content about free monoids', 'typing_conditions': 'none', 'evidence_status': 'Reviewed as vacuous; no result is drawn from it', 'scope': 'Fixed arithmetic only'}]
    compositions = [
        {'outer_operation': 'alphabet_bijection', 'input_slot': 0, 'inner_operation': 'monoid_iso', 'colour_match': 'IsoSet',
         'hypothesis_match': 'The isomorphism restricts to the atoms of both sides; atoms are the letters.', 'licensing_relations': ['atoms_are_letters', 'iso_preserves_atoms'], 'evidence_status': 'Kernel and native'},
        {'outer_operation': 'discrete_equivalence_objects', 'input_slot': 0, 'inner_operation': 'discrete_category', 'colour_match': 'DiscreteCategory',
         'hypothesis_match': 'Isomorphism classes of a discrete category are its objects.', 'licensing_relations': ['discrete_equivalence_is_bijection'], 'evidence_status': 'Kernel and native'}]
    failed = [{'composition': 'monoid_iso(free_monoid(Fin n), free_monoid(Fin m)) for n != m', 'reason': 'Empty (kernel no_free_monoid_iso); no isomorphism exists although the underlying sets are in bijection for n, m >= 1.'},
              {'composition': 'a numeral or alphabet re-presentation read as an isomorphism of the free monoids', 'reason': 'Fails for different alphabet sizes; the shortlex re-presentation is a set bijection that fails multiplicativity on 841 of the 900 pairs of the first 30 words for sizes 2 and 3 (native homomorphism_violations; the 59 passing pairs involve the empty word).'}]
    counterexamples = [{'id': 'bijection_not_homomorphism', 'statement': 'For sizes 2 and 3 the shortlex-rank bijection of the underlying sets is a bijection on the first 30 words but fails multiplicativity on 841 of 900 pairs.', 'scope': 'Native instance; Lean bijection_but_not_isomorphic states the general fact.'},
                       {'id': 'collapsing_surjection', 'statement': 'Homomorphisms from three generators onto two letters (36 of them with images of length at most 2 are onto the letters) identify two generators and are never injective.', 'scope': 'Native instance (3,2,2).'}]
    return build_spec(
        node=NODE, short='free_monoid_noniso', lean='FreeMonoidNoniso',
        anchors=['FreeMonoidNoniso.isAtom_iff', 'FreeMonoidNoniso.isAtom_map_iff', 'FreeMonoidNoniso.alphabetEquiv', 'FreeMonoidNoniso.no_free_monoid_iso',
                 'FreeMonoidNoniso.freeMonoid_iso_iff_equiv', 'FreeMonoidNoniso.discrete_equivalence_card', 'FreeMonoidNoniso.no_discrete_equivalence',
                 'FreeMonoidNoniso.discrete_equivalence_iff', 'FreeMonoidNoniso.set_bijection_exists', 'FreeMonoidNoniso.bijection_but_not_isomorphic',
                 'FreeMonoidNoniso.free_monoid_zero_subsingleton', 'FreeMonoidNoniso.card_words_of_length', 'FreeMonoidNoniso.card_atoms',
                 'FreeMonoidNoniso.unequal_finite_alphabets_not_wordiso'],
        cases=[list(c) for c in producer.CASES], public_tsv=producer.public_tsv(), data=producer.certificate(),
        scope_review=('The sources are general: Paper.lean and Paper001.lean prove, over List A and List alpha with hand-rolled structures, that an isomorphism induces an alphabet bijection (Classical.choice is used for it, per Paper.lean header) and hence equal sizes. '
                      'Paper001.lean DiscreteEquiv is, by definition, a pair of mutually inverse maps on objects, so no_discrete_equivalence is the pigeonhole fact; the Python checks free_monoids_nonisomorphic and discrete_categories_inequivalent compare counts (the latter returns left != right). '
                      'The DAG-local Lean theorem pg_to_sn_and_wdp_route_chain_composition is fixed arithmetic and vacuous for this node. This node re-proves the statement with Mathlib FreeMonoid / MulEquiv and Discrete categories (genuine categorical equivalence), bridges the source WordIso to MulEquiv, adds the converse iff, '
                      'and records the sharp boundary: a set bijection exists, so the obstruction is multiplicativity; native: exact word counts, brute-force atoms, exhaustive homomorphism search with bounded image length, discrete equivalences, shortlex bijection.'),
        predicates=['Atoms recomputed as the complement of the set of products of two nonempty words, not by testing splits.',
                    'Number of homomorphisms (sum_{k<=d} m^k)^n and number onto the letters by inclusion-exclusion over missing letters.',
                    'Injectivity and bijective candidates recomputed with string-valued homomorphisms; candidates required to be exactly the letter permutations (n! if n = m, else none).',
                    'Discrete-category equivalences counted as bijective maps, shortlex bijection built by explicit enumeration with a dictionary rather than rank arithmetic.',
                    'Exact cross-language (Python/Rust) wire equality and literal Lean axiom reports.'],
        boundary=boundary, generators=generators, relations=relations, compositions=compositions, failed_compositions=failed, counterexamples=counterexamples,
        open_obligations=['Classification of structure-preserving re-presentations (injective and onto homomorphisms between free monoids on different alphabets).', 'Language restriction, partial recovery and total erasure (row WDP-P001-009).',
                          'Any structure other than the free-monoid multiplication and the discrete category.'],
        colour_meanings={'Alphabet': 'A type of letters', 'FreeMonoid': 'Words over an alphabet with concatenation', 'AtomSet': 'Indecomposable nonidentity words', 'IsoSet': 'Monoid isomorphisms between two free monoids',
                         'AlphabetBijection': 'Bijection of alphabets', 'DiscreteCategory': 'Category with only identity morphisms on a set of objects'},
        depends_on_result=True, qualification='Non-isomorphism is established for the free-monoid multiplication (monoid isomorphism) and for discrete-category equivalence; a bare set bijection between unequal infinite alphabets-of-words exists, so the node does not rule out re-presentations that ignore the multiplication.',
        challenge_plan='Coordinate mutants of every certificate leaf plus eight semantic near misses: set bijection read as isomorphism, cardinality as the invariant, collapsing surjection as bijection, longer atoms, discrete equivalence of unequal sizes, trivial monoid isomorphic to one generator, unique isomorphism, wrong word counts.',
        composition_tree=['alphabet_bijection(monoid_iso(free_monoid(a), free_monoid(b)))', 'discrete_equivalence_objects(discrete_category(a), discrete_category(b))'],
        construction='Exact word counts, brute-force atoms, exhaustive search of homomorphisms with bounded image length, counts of mutually inverse map pairs, explicit shortlex bijection; Lean proves the general statements.',
        relation_evidence={'iso_gives_alphabet_bijection': 'Kernel theorems; native: bijective candidates are exactly the permutations on 15 pairs.', 'set_bijection_but_not_iso': 'Kernel theorem; native violation counts 841 and 609.'})


if __name__ == '__main__':
    print(write_spec(HERE, NODE, spec()))
