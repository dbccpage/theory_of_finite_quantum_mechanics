"""Build specs/PG-CHAIN-RETRACTION.json from the producer and the node's reviewed claims."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp/batch_tools'))
from spec_builder import build_spec, write_spec  # noqa: E402

_s = importlib.util.spec_from_file_location('producer', ROOT / 'code/python/src/qm/pfp_chain_retraction.py')
producer = importlib.util.module_from_spec(_s)
_s.loader.exec_module(producer)

NODE = 'PG-CHAIN-RETRACTION'
PRE = 'omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/'
SN = 'omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_sn_mssn/lean4/Paper001.lean'
H = 'Coefficients form a declared ring R (Lean: any ring; native: the rationals); chain complexes are free and finite in the native tables; r is a chain map with r . i = id.'


def spec():
    boundary = {
        'supports': ('Kernel-checked over any ring and any modules, degree by degree (so for complexes of any size): if linear maps rU, rM, rL commute with the boundary and differential and rM . iM = id on the middle module, a class that is not a boundary in C stays a non-boundary in D (cannot_kill), and the induced map on homology (cycles modulo boundaries, a Mathlib quotient) is injective (Hmap_injective, kernel_trivial). '
                     'The two named non-examples are built in Lean as concrete degree fragments over any ring (two isolated points in an edge, degree 0; a triangle boundary in the filled triangle, degree 1), the inclusion is proved to be a chain map, the killed class is exhibited as a nonzero element of Hom sent to zero by Hmap (nontrivial ring), and no linear rU, rM, rL satisfying the chain-map and section conditions exists (no_retraction_of_killed, TwoPoints.no_chain_retraction, Triangle.no_chain_retraction); other degrees of those complexes are not formalised in Lean and retractions are required to be linear there. '
                     'The converse fails over the integers in the labelled one-term instance x -> 2x (TimesTwo.converse_fails_over_int, stated through Hmap; not a subcomplex inclusion). '
                     'Native over Q: 13 finite free complexes (edges, triangles, tetrahedron skeleta) with exact Betti numbers, rank of the induced homology map, killed-class counts and the rank/augmented rank of the retraction system, with an explicit verified retraction wherever one exists; one refused non-subcomplex.'),
        'does_not_support': ('The bridge from declared inclusions to WDP-CH04-N02 (growth of the Genesis/WDP complexes does not repair an obstruction) for any actual Genesis/WDP complex pair; coefficient rings other than the declared one in the native tables; infinite or non-free complexes in the native tables; '
                             'non-linear retractions and the full-complex (all degrees at once) formalisation of the two named cases; an integral failure of the converse for a genuine subcomplex inclusion (the Z instance is a one-term map, not a subcomplex); the converse over Q as a Lean theorem (it is a standard fact over a field, only observed here on the listed complexes); any physical reading.'),
        'narrowest_claim': ('For chain maps i: C -> D and r: D -> C over a ring with r . i = id on the middle module and r commuting with the boundary, the induced map on homology is injective, so an extension admitting such an r cannot kill an old class; the two-points and triangle-with-face extensions kill a class (kernel, in the modelled degree fragment, and native) and admit no linear chain retraction (kernel, same fragment).'),
        'next_test': ('Take one actual Genesis/WDP growth inclusion named by WDP-CH04-N02, write it in the native complex encoding with its basis subset, and decide by the retraction system and the rank of H(i) whether the old obstruction class is killed or a chain retraction exists, so that the bridge from the general theorem to the WDP growth statement is tested on a real complex.')}
    generators = [
        {'id': 'chain_complex_fragment', 'source_declarations': [PRE + 'Paper.lean::ChainFragment (line 102; structure with explicit sub on the middle type)', PRE + 'Homology.lean::Complex (line 31; three groups, boundary, differential, square_zero)'],
         'ordered_inputs': ['Module', 'Module', 'Module'], 'output': 'Complex', 'semantic_predicate': 'U --bd--> M --d--> L with d . bd = 0 (one degree).', 'hypotheses': [H]},
        {'id': 'chain_map', 'source_declarations': [PRE + 'Paper.lean::ChainMap (line 112; definition)', PRE + 'Homology.lean::Morphism (line 158; definition)', 'omega_engine/crates_rs/omega_homology/src/chain_map.rs::CertifiedChainMap (line 35; checks commutation of given matrices)'],
         'ordered_inputs': ['Complex', 'Complex'], 'output': 'ChainMap', 'semantic_predicate': 'Linear maps in each degree commuting with bd and d.', 'hypotheses': [H]},
        {'id': 'homology_map', 'source_declarations': [PRE + 'Homology.lean::homologyMap (line 182; definition via a hand-built image quotient)'],
         'ordered_inputs': ['ChainMap'], 'output': 'HomologyMap', 'semantic_predicate': 'Cycles modulo boundaries, induced map.', 'hypotheses': [H]},
        {'id': 'retraction', 'source_declarations': [SN + '::ChainRetraction (line 453; structure with retractChain, sectionLaw)', PRE + 'Paper.lean::chain_retraction_cannot_kill (line 147; hypothesis fixes)'],
         'ordered_inputs': ['ChainMap', 'ChainMap'], 'output': 'Retraction', 'semantic_predicate': 'r . i = id on the middle module and r a chain map.', 'hypotheses': [H]},
        {'id': 'retraction_system', 'source_declarations': ['no source declaration; native linear system r|C = id, d r = r d solved over Q'],
         'ordered_inputs': ['Complex', 'Complex'], 'output': 'LinearSystem', 'semantic_predicate': 'Solvable iff a chain retraction onto C exists (rank equals augmented rank).', 'hypotheses': [H]}]
    relations = [
        {'id': 'cannot_kill', 'source_declarations': [PRE + 'Paper.lean::chain_retraction_cannot_kill (line 147; general theorem for fragments with an abstract sub)', PRE + 'Paper.lean::chain_retraction_reflects_boundaries (line 130)'],
         'equation_or_predicate': 'r . i = id and r commutes with bd imply: z not a boundary in C implies i z not a boundary in D', 'typing_conditions': 'Retraction', 'evidence_status': 'Kernel theorem cannot_kill over any ring and modules; native killed counts', 'scope': 'Any ring, any complex, degree by degree'},
        {'id': 'induced_homology_injective', 'source_declarations': [PRE + 'Homology.lean::induced_homology_injective (line 210; general over its own group-valued AddHom, Lean-core algebra)', SN + '::homology_kernel_trivial (line 460) and homology_injective_of_chain_retraction (line 468; concludes z is a boundary, with a vacuous cycleBoundary argument)'],
         'equation_or_predicate': 'retraction implies the induced map on cycles-mod-boundaries is injective', 'typing_conditions': 'HomologyMap, Retraction', 'evidence_status': 'Kernel theorems Hmap_injective, kernel_trivial (Mathlib quotient)', 'scope': 'Any ring and modules'},
        {'id': 'two_points_no_retraction', 'source_declarations': [SN + '::two_point_retraction_impossible (line 477; takes r0 (-1,1) = (-1,1) and r0 (-1,1) = (0,0) as hypotheses, i.e. the pointwise instances of the section law and the chain condition, and derives -1 = 0; it does not itself derive them from a chain retraction)'],
         'equation_or_predicate': 'No functions rU, rM with rM = id on the vertex chains and rM (bd e) = 0 (the point complex has no 1-chains)', 'typing_conditions': 'Edge over two points, nontrivial ring', 'evidence_status': 'Kernel theorems TwoPoints.cls_ne_zero, cls_killed, no_chain_retraction (concrete degree-0 fragment, chain-map hypotheses on r); native row two_isolated_points_in_edge', 'scope': 'Every nontrivial ring, linear rU, rM, rL in the modelled fragment'},
        {'id': 'triangle_no_retraction', 'source_declarations': [SN + '::triangle_retraction_impossible (line 491; takes hsec, hchain, hzero, the pointwise instances of the section law and chain condition, as hypotheses)'],
         'equation_or_predicate': 'No functions rU, rM with rM = id on the edge chains and rM (bd f) = 0 (the triangle boundary has no 2-chains)', 'typing_conditions': 'Filled triangle over its boundary, nontrivial ring', 'evidence_status': 'Kernel theorems Triangle.square_zero, cls_ne_zero, cls_killed, no_chain_retraction (concrete degree-1 fragment); native row triangle_boundary_in_filled_triangle', 'scope': 'Every nontrivial ring, linear rU, rM, rL in the modelled fragment'},
        {'id': 'converse_over_Q_observation', 'source_declarations': ['no source declaration; new native observation'],
         'equation_or_predicate': 'On free complexes over Q, a chain retraction exists iff H(i) is injective in every degree (exhaustive over 2448 subcomplexes of 3-term complexes with dims (2,2,1) in the test, and the 13 listed cases)', 'typing_conditions': 'Finite free complexes over Q', 'evidence_status': 'Native observation, not a Lean theorem here (a standard fact over a field); the converse is false over Z in the one-term instance (kernel TimesTwo.converse_fails_over_int)', 'scope': 'Listed finite complexes over Q only'},
        {'id': 'aggregate_chain_composition', 'source_declarations': ['lean4/DerivationDagQMClosure.lean::pg_to_sn_and_wdp_route_chain_composition (line 1257; a conjunction of fixed Nat/Fin 3 identities)'],
         'equation_or_predicate': 'fixed enumeration; not a chain-retraction theorem', 'typing_conditions': 'Fixed values', 'evidence_status': 'Source declaration, not used as support', 'scope': 'Fixed instance'}]
    compositions = [
        {'outer_operation': 'homology_map', 'input_slot': 0, 'inner_operation': 'chain_map', 'colour_match': 'ChainMap', 'hypothesis_match': H,
         'licensing_relations': ['induced_homology_injective'], 'evidence_status': 'Kernel and native'},
        {'outer_operation': 'retraction', 'input_slot': 0, 'inner_operation': 'chain_map', 'colour_match': 'ChainMap', 'hypothesis_match': 'The retraction is a chain map back into the old complex with r . i = id.',
         'licensing_relations': ['cannot_kill', 'two_points_no_retraction', 'triangle_no_retraction'], 'evidence_status': 'Kernel and native'}]
    failed = [{'composition': 'retraction onto the two isolated points from the edge joining them', 'reason': 'A chain retraction would fix both vertices and send the boundary of the edge (-1, 1) to 0; no such linear maps exist (kernel TwoPoints.no_chain_retraction in the degree-0 fragment, native inconsistent system).'},
              {'composition': 'retraction onto the triangle boundary from the filled triangle', 'reason': 'The cycle (1,1,1) is fixed by r yet is the boundary of the face, which r sends to 0 (kernel Triangle.no_chain_retraction in the degree-1 fragment, native inconsistent system).'},
              {'composition': 'inclusion of a non-closed vertex/edge set as a chain map', 'reason': 'An edge without its endpoint is not a subcomplex, so the inclusion is not a chain map and the section hypothesis is void (native is_subcomplex = 0).'},
              {'composition': 'converse over the integers', 'reason': 'Multiplication by 2 on Z (a one-term complex, not a subcomplex inclusion) is injective on homology but has no chain retraction (kernel TimesTwo.converse_fails_over_int).'}]
    counterexamples = [{'id': 'multiplication_by_two', 'statement': 'i = x -> 2x on Z: H(i) injective, no r with r . i = id.', 'scope': 'Over Z, one-term complex.'},
                       {'id': 'hollow_tetrahedron_in_solid', 'statement': 'The degree-2 class of the hollow tetrahedron dies in the solid tetrahedron.', 'scope': 'Native row, killed = 1.'}]
    return build_spec(
        node=NODE, short='chain_retraction', lean='ChainRetraction',
        anchors=['ChainRetraction.cannot_kill', 'ChainRetraction.Hmap_injective', 'ChainRetraction.kernel_trivial', 'ChainRetraction.no_retraction_of_killed',
                 'ChainRetraction.TwoPoints.cls_ne_zero', 'ChainRetraction.TwoPoints.cls_killed', 'ChainRetraction.TwoPoints.no_chain_retraction',
                 'ChainRetraction.Triangle.square_zero', 'ChainRetraction.Triangle.cls_ne_zero', 'ChainRetraction.Triangle.cls_killed',
                 'ChainRetraction.Triangle.no_chain_retraction', 'ChainRetraction.TimesTwo.converse_fails_over_int'],
        cases=[list(c) for c in producer.CASES], public_tsv=producer.public_tsv(), data=producer.certificate(),
        scope_review=('Read Paper.lean (sha b0f6365df8; fragments with explicit sub, chain_retraction_cannot_kill line 147), Homology.lean (sha 13d8de1400; hand-built image quotient over Lean-core Grind groups, induced_homology_injective line 210) and Paper001.lean (sha b90693440d; ChainRetraction 453, homology_kernel_trivial 460, homology_injective_of_chain_retraction 468, two_point_retraction_impossible 477, triangle_retraction_impossible 491). '
                      'The general theorems are correct. The two named non-example theorems take the pointwise instances of the section law and chain condition as hypotheses and derive -1 = 0 or 1 = 0; they are correct but do not themselves derive those facts from a chain retraction. '
                      'Mine: re-proved the injectivity for Mathlib modules over any ring (only r . i = id and bd-commutation used), modelled both named cases as concrete degree fragments with the killed class in Hom and derived non-existence of a linear chain retraction from the general theorem, and tabulated 13 complexes over Q. '
                      'The converse is false over Z (multiplication by 2); over Q it holds on every listed case and on 2448 enumerated subcomplexes, recorded as an observation only.'),
        predicates=['rank H_k(i) recomputed as b_k(C) - [rank d_{k+1}^D - rank(E_k) - rank d_{k+1}^C] (cycles of C that bound in D) using only matrix ranks, against the producer nullspace route.',
                    'Retraction system rebuilt at the matrix level with linear forms, solved by forward elimination and back substitution; rank and augmented rank compared; the canonical solution (free unknowns 0) compared entry by entry and verified by matrix products r.i = id and d^C r = r d^D.',
                    'A retraction exists only if H(i) is injective in every degree (the Lean theorem); on this family the converse is enforced as an observation.',
                    'Closedness of the basis subset under the boundary decides subcomplex status; a non-closed set is refused.',
                    'Exact cross-language (Python/Rust) wire equality and literal Lean axiom reports.'],
        boundary=boundary, generators=generators, relations=relations, compositions=compositions, failed_compositions=failed, counterexamples=counterexamples,
        open_obligations=['Integral coefficients and torsion: when does H(i) injective force a retraction over Z?', 'Bridge from declared inclusions to the WDP-CH04-N02 statement that growth does not repair an obstruction.',
                          'Infinite and non-free complexes in the native tables.'],
        colour_meanings={'Module': 'R-module in one degree', 'Complex': 'U --bd--> M --d--> L with d . bd = 0', 'ChainMap': 'Linear maps in the three degrees commuting with bd and d',
                         'HomologyMap': 'Induced map on cycles modulo boundaries', 'Retraction': 'Chain map r with r . i = id', 'LinearSystem': 'Equations on the unknown entries of r over Q'},
        depends_on_result=True,
        qualification='Injectivity of the induced homology map under a chain retraction is proved over any ring; the source instance theorems take the pointwise section and chain facts as hypotheses, and the versions here derive them from concrete degree-fragment chain complexes (linear retractions); the converse is not claimed (false over Z in a one-term instance, standard but unproved here over Q); the bridge to the WDP growth statement is open.',
        challenge_plan='Coordinate mutants of every certificate leaf plus nine semantic near misses: isolated points retract, triangle class survives the face, hollow tetrahedron class survives, converse denied over Q, non-subcomplex given homology, non-section retraction, skeleton inclusion retracts, an identity-on-vertices retraction claimed for the edge, injectivity read off degree 0 only.',
        composition_tree=['homology_map(chain_map(inclusion))', 'retraction(chain_map(inclusion))'],
        construction='Exact rational linear algebra on 13 finite free complexes; Lean proves injectivity over any ring and non-existence of a linear chain retraction for the two named inclusions in their modelled degree fragments.',
        relation_evidence={'cannot_kill': 'Kernel cannot_kill and Hmap_injective; native killed counts.', 'converse_over_Q_observation': 'Native only; Lean shows it false over Z in a one-term instance.'})


if __name__ == '__main__':
    print(write_spec(HERE, NODE, spec()))
