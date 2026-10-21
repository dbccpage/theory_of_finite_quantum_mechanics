"""Build specsB/PG-REFINE-SEPARATES.json from the producer and the node's reviewed claims."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp/batch_tools'))
from spec_builder import build_spec, write_spec  # noqa: E402

_s = importlib.util.spec_from_file_location('producer', ROOT / 'code/python/src/qm/pfp_refine_separates.py')
producer = importlib.util.module_from_spec(_s)
_s.loader.exec_module(producer)

NODE = 'PG-REFINE-SEPARATES'
SRC = 'the_symbol_game:omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/'
PAPER = SRC + '000_pre_genesis_to_mssn/lean4/Paper.lean'
PAPER1 = SRC + '001_sn_mssn/lean4/Paper001.lean'
H = 'A report q : A -> O, a supplied tag t : A -> T (an input, never chosen), and a conflict relation C on A given as data; finite A for the counting statements.'


def spec():
    boundary = {
        'supports': ('Kernel-checked and general over all types A, O, T: the refined report (q, t) keeps q as its first projection; a differing tag separates a pair (the source theorem refine_separates is this forward direction only); on a pair the old report collapses, the tag decides separation exactly (refine_separates_iff, new); refinement never merges what q separated. '
                     'For a conflict relation C contained in the collapse of q: a GIVEN tag resolves every conflict iff it is proper for C (resolves_iff_proper); SOME b-bit tag (Fin b -> Bool) resolves every conflict iff C has a proper 2^b-colouring (refine_separates_many, an existence statement over tags). '
                     'A Bool tag proper for C forbids any odd closed walk in C (so no triangle, no 5-cycle); this is the forward direction only, the converse (no odd closed walk implies a one-bit tag, Konig) is not in the kernel and is used natively (bipartite iff odd girth 0; one-bit tags 2^components when bipartite). '
                     'For a finite type A in which every pair of distinct elements conflicts (a collapsed fibre taken as its own type, or q constant) a b-bit tag separating all pairs exists iff |A| <= 2^b (fibre_bits_iff; one bit iff |A| <= 2, fibre_one_bit_iff); for the fibre {a // q a = x} of an arbitrary report q some b-bit tag on the whole type resolves all conflicts between distinct fibre elements iff the fibre has at most 2^b elements (fibre_report_bits_iff). '
                     'Native columns are counts over all (q, t) and ordered pairs (a, b), a = b allowed: quadruples = o^n t^n n^2; separated_by_tag = pairs with q a = q b and t a != t b; refined_equal = pairs with equal refined reports; old_separation_kept = pairs with q a != q b (all stay separated); iff_failures = pairs where equality of refined reports differs from equality of both components (0; the checker evaluates the refinement itself). '
                     'Exact native tables: 14 named conflict graphs (components, proper one-bit tag counts 2^c or 0, chromatic number, minimal bits, odd girth), all labelled graphs on 1..5 vertices (labelled bipartite counts 1,2,7,41,376; minimal-bit distributions), fibre tag counts for m=1..5 and bits for m=6,8,9,17, and refinement counts for five small (n,o,t).'),
        'does_not_support': ('Any algorithm, complexity or guarantee for FINDING a tag (the tables and the iff are existence statements, not search procedures); which tag a host should supply; the converse of the odd-closed-walk theorem in the kernel (Konig; native only); conflict graphs on more than 5 vertices beyond the 14 named ones; '
                             'infinite carriers; any measurement, physical or interpretive reading of tags.'),
        'narrowest_claim': ('For a report q and a conflict relation C inside its collapse, SOME b-bit tag resolves all conflicts iff C has a proper 2^b-colouring (refine_separates_many); a GIVEN tag resolves C iff it is proper (resolves_iff_proper). The source refine_separates is the forward direction for one pair; refine_separates_iff is the one-pair equivalence on collapsed pairs.'),
        'next_test': ('First prove in Lean the converse of no_one_bit_of_odd_cycle (a finite symmetric conflict relation with no odd closed walk has a proper Bool tag), then that breadth-first 2-colouring is sound and complete for deciding it, as the first algorithmic statement about finding a tag; the present node proves existence criteria only.')}
    generators = [
        {'id': 'refine_report', 'source_declarations': ['the_symbol_game Paper.lean::refineReport (line 59) - a definition (general in A O T)'], 'ordered_inputs': ['Report', 'Tag'], 'output': 'RefinedReport',
         'semantic_predicate': 'a |-> (q a, t a); the tag is an input argument, never searched.', 'hypotheses': [H]},
        {'id': 'project_old_report', 'source_declarations': ['the_symbol_game Paper.lean::refine_preserves (line 61) - general theorem, proved by rfl'], 'ordered_inputs': ['RefinedReport'], 'output': 'Report',
         'semantic_predicate': 'First projection; recovers the old report q from the refined report.', 'hypotheses': [H]},
        {'id': 'proper_tag_test', 'source_declarations': ['the_symbol_game Paper001.lean::supplied_tag_separates (line 96) - general in A O but the tag is Fin 2 and the statement concerns ONE pair; the conflict-graph reading is prose only (paper.md section 9)'],
         'ordered_inputs': ['ConflictRelation', 'Tag'], 'output': 'Verdict', 'semantic_predicate': 'Proper C t: every conflicting pair gets different tag values.', 'hypotheses': [H]},
        {'id': 'tag_pair', 'source_declarations': ['no source declaration; new general lemma proper_union'], 'ordered_inputs': ['Tag', 'Tag'], 'output': 'Tag',
         'semantic_predicate': 'Pair of tags (t1, t2): bit counts add; a proper t1 for C1 and a proper t2 for C2 give a proper pair for C1 or C2.', 'hypotheses': [H]},
        {'id': 'bits_needed', 'source_declarations': ['no source declaration; paper.md section 9 states prose "a three-clique needs three colors"; new general lemmas bits_iff_colours, fibre_bits_iff'],
         'ordered_inputs': ['ConflictRelation'], 'output': 'BitCount', 'semantic_predicate': 'Least b such that C has a proper 2^b-colouring (ceil log2 chi for a finite graph).', 'hypotheses': [H]}]
    relations = [
        {'id': 'refine_retains_old_report', 'source_declarations': ['the_symbol_game Paper.lean::refine_preserves (line 61): general'], 'equation_or_predicate': 'fst o refine q t = q',
         'typing_conditions': 'A O T arbitrary types', 'evidence_status': 'Kernel theorem refine_retains', 'scope': 'All types'},
        {'id': 'tag_difference_separates_pair', 'source_declarations': ['the_symbol_game Paper.lean::refine_separates (line 64), Paper001.lean::supplied_tag_separates (line 96): general / Fin 2 tag'],
         'equation_or_predicate': 't a != t b implies refine q t a != refine q t b', 'typing_conditions': 'any tag type T', 'evidence_status': 'Kernel theorem refine_separates', 'scope': 'All types, one pair'},
        {'id': 'collapsed_pair_separated_iff_tags_differ', 'source_declarations': ['no source declaration; the source proves only the forward direction'],
         'equation_or_predicate': 'q a = q b implies (refine q t a != refine q t b iff t a != t b)', 'typing_conditions': 'a b collapsed by q', 'evidence_status': 'Kernel theorem refine_separates_iff; native count table (iff_failures 0)', 'scope': 'All types'},
        {'id': 'many_conflicts_iff_proper_colouring', 'source_declarations': ['paper.md section 9 prose ("a tag assignment separating every edge is a proper coloring"), no Lean statement in the source'],
         'equation_or_predicate': 'C inside collapse(q) implies (some b-bit tag resolves C iff C has a proper 2^b-colouring)', 'typing_conditions': 'arbitrary relation C on A', 'evidence_status': 'Kernel theorems resolves_iff_proper, bits_iff_colours, refine_separates_many; native tables', 'scope': 'All types; existence only'},
        {'id': 'proper_union_of_tags', 'source_declarations': ['no source declaration'], 'equation_or_predicate': 'a proper t1 for C1 and a proper t2 for C2 give the proper pair tag (t1, t2) for C1 or C2',
         'typing_conditions': 'any relations and tag types', 'evidence_status': 'Kernel theorem proper_union', 'scope': 'All types'},
        {'id': 'odd_closed_walk_refuses_one_bit', 'source_declarations': ['the_symbol_game Paper.lean::triangle_not_two_colored (line 69): a FIXED instance (three Bool values), not the general statement'],
         'equation_or_predicate': 'odd closed walk in C implies no Bool tag is proper', 'typing_conditions': 'any C, any closed walk of odd length', 'evidence_status': 'Kernel theorems no_one_bit_of_odd_cycle, triangle_no_one_bit (forward direction only); the converse (no odd closed walk implies a proper Bool tag, Konig) is NOT in the kernel and is used natively: bipartite iff odd girth 0, one-bit tags 2^components', 'scope': 'All types'},
        {'id': 'fibre_bit_count', 'source_declarations': ['no source declaration'], 'equation_or_predicate': 'all pairs of a fibre of size m separated by a b-bit tag iff m <= 2^b', 'typing_conditions': 'finite fibre',
         'evidence_status': 'Kernel theorems fibre_bits_iff, fibre_one_bit_iff (complete conflict relation on a finite type), fibre_report_bits_iff (fibre of a report); native injective-tag counts', 'scope': 'All finite types'}]
    compositions = [
        {'outer_operation': 'project_old_report', 'input_slot': 0, 'inner_operation': 'refine_report', 'colour_match': 'RefinedReport', 'hypothesis_match': H,
         'licensing_relations': ['refine_retains_old_report'], 'evidence_status': 'Kernel and native (retained-old-report counts)'},
        {'outer_operation': 'proper_tag_test', 'input_slot': 1, 'inner_operation': 'tag_pair', 'colour_match': 'Tag', 'hypothesis_match': 'Union of the two conflict relations; tags are supplied.',
         'licensing_relations': ['proper_union_of_tags'], 'evidence_status': 'Kernel theorem proper_union'}]
    failed = [
        {'composition': 'proper_tag_test(triangle conflicts, Bool tag)', 'reason': 'No Bool tag is proper on a triangle or any odd closed walk (kernel no_one_bit_of_odd_cycle); two bits are needed.'},
        {'composition': 'refine_report(q, tag chosen by the operad)', 'reason': 'The operad has no generator producing a tag from (report, conflicts): the tag is an input, and no source or kernel statement derives it.'}]
    counterexamples = [
        {'id': 'triangle_needs_two_bits', 'statement': 'Three mutually conflicting collapsed elements: chi=3, min_bits=2, proper one-bit tags 0.', 'scope': 'Instance of the odd-cycle theorem.'},
        {'id': 'five_cycle_needs_two_bits', 'statement': 'A 5-cycle has no triangle yet no proper one-bit tag (odd girth 5, chi 3).', 'scope': 'Instance of the odd-cycle theorem; shows cliques are not the only obstruction.'},
        {'id': 'fibre_of_three_needs_two_bits', 'statement': 'A collapsed fibre of size 3: no one-bit injective tag; 24 injective tags with two bits.', 'scope': 'Instance of fibre_bits_iff.'}]
    return build_spec(
        node=NODE, short='refine_separates', lean='RefineSeparates',
        anchors=['RefineSeparates.refine_retains', 'RefineSeparates.refine_separates', 'RefineSeparates.refine_separates_iff',
                 'RefineSeparates.refine_keeps_old_separation', 'RefineSeparates.resolves_iff_proper', 'RefineSeparates.proper_union',
                 'RefineSeparates.bits_iff_colours', 'RefineSeparates.no_one_bit_of_odd_cycle', 'RefineSeparates.triangle_no_one_bit',
                 'RefineSeparates.fibre_bits_iff', 'RefineSeparates.fibre_one_bit_iff', 'RefineSeparates.fibre_report_bits_iff', 'RefineSeparates.refine_separates_many'],
        cases=[list(c) for c in producer.CASES], public_tsv=producer.public_tsv(), data=producer.certificate(),
        scope_review=('Mined the source declarations refineReport, refine_preserves, refine_separates (Paper.lean lines 59-66), supplied_tag_separates (Paper001.lean line 96, Fin 2 tag, one pair) and triangle_not_two_colored (Paper.lean line 69). '
                      'The single-pair theorem is general and non-vacuous; the triangle theorem is a fixed three-Bool instance; the many-conflict statement (conflict graph, proper colouring, a 3-clique needs three colours) exists only as prose in paper.md section 9. '
                      'This node proves the colouring characterisation, the odd-closed-walk obstruction and the fibre bit count in Lean for arbitrary relations/finite types, and tabulates all labelled graphs on up to 5 vertices natively. '
                      'The sha256 of the three bound source files matches their operad pins (Paper.lean b0f6365d, Paper001.lean b9034069, DerivationDagQMClosure.lean c9ad9c23); the DerivationDagQMClosure theorem pg_to_sn_and_wdp_route_chain_composition is a conjunction of fixed arithmetic facts and does not mention refinement, so it supplies nothing here.'),
        predicates=['Union-find components and breadth-first two-colouring replace the producer\'s depth-first components and exhaustive tag enumeration; proper one-bit tags counted as 2^components when bipartite.',
                    'Chromatic number by dynamic programming over vertex subsets (cover by independent sets), minimal bits as bit_length(chi-1); the producer uses backtracking colourings with 2^b colours.',
                    'Odd girth as the least odd k with nonzero trace of A^k; the producer uses breadth-first levels.',
                    'Enumeration identity: sum over bipartite G of 2^c(G) equals sum_k C(n,k) 2^(k(n-k)); labelled bipartite count equals graphs with at most one bit.',
                    'Injective tag counts as falling factorials (2^b)_m; refinement records recomputed by evaluating the refinement on every (q, t, a, b) in the checker and compared with the closed forms n(n-1) o^(n-1) t^(n-1) (t-1) and n(n-1) o^(n-1) (o-1) t^n; exact Python/Rust wire equality and literal Lean axiom reports.'],
        boundary=boundary, generators=generators, relations=relations, compositions=compositions, failed_compositions=failed, counterexamples=counterexamples,
        open_obligations=['Algorithmic or complexity statements about finding a tag; the node proves existence criteria only.',
                          'Conflict graphs beyond the 14 named graphs and the exhaustive range of 5 vertices.',
                          'Any host-level meaning of conflicts, tags or bits beyond the abstract report/tag model.'],
        colour_meanings={'Report': 'Function q from the carrier to observations', 'Tag': 'Supplied function t from the carrier to tag values (Bool, Fin b -> Bool, Fin k)',
                         'RefinedReport': 'Pair report a |-> (q a, t a)', 'ConflictRelation': 'Relation C on the carrier whose pairs must be separated',
                         'Verdict': 'Boolean: tag is proper for C', 'BitCount': 'Least number of tag bits resolving C'},
        depends_on_result=True,
        qualification='The DAG phrase "satisfying many conflicts at once ... unaddressed" is narrowed: existence of a satisfying b-bit tag for conflicts inside a collapse is exactly proper 2^b-colourability (kernel-checked); finding such a tag remains unaddressed.',
        challenge_plan='Coordinate mutants of every certificate leaf plus nine semantic near misses: triangle/odd cycle/fibre of three claimed one-bit, tag taken as unique, components ignored, refinement merging old reports, bits confused with colours, unlabelled counts for labelled graphs, degree bound read as colouring.',
        composition_tree=['project_old_report(refine_report(q, t))', 'proper_tag_test(C, tag_pair(t1, t2)) with C = C1 or C2'],
        construction='Exact integer tables for named conflict graphs, all labelled graphs on up to 5 vertices, fibres, and small refinement counts; Lean proves the general statements.',
        relation_evidence={'many_conflicts_iff_proper_colouring': 'Kernel theorem for arbitrary relations; native bipartite counts 1,2,7,41,376 agree with the colouring-pair identity.',
                           'odd_closed_walk_refuses_one_bit': 'Kernel theorem; every native graph with positive odd girth has zero one-bit tags.'})


if __name__ == '__main__':
    print(write_spec(HERE, NODE, spec()))
