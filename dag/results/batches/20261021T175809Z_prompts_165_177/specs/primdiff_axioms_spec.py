"""Build specsB/PG-PRIMDIFF-AXIOMS.json from the producer and the node's reviewed claims."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp/batch_tools'))
from spec_builder import build_spec, write_spec  # noqa: E402

_s = importlib.util.spec_from_file_location('producer', ROOT / 'code/python/src/qm/pfp_primdiff_axioms.py')
producer = importlib.util.module_from_spec(_s)
_s.loader.exec_module(producer)

NODE = 'PG-PRIMDIFF-AXIOMS'
RS = 'code/rust/src/wdp/primitive_axiomatics.rs'
H = ('Finite carrier items 0..n-1 (n <= 3 natively); a structure is (D, E, F, alpha): admitted ordered pairs D, directed evaluation edges E, at most one face (0,1,2) F, authority flag alpha. '
     'The predicates are OUR transcription: the pinned Rust file gives ten axiom names and code for A1, A3, A5 and the triad classification only.')


def spec():
    boundary = {
        'supports': ('The pinned Rust source lists ten axiom NAMES with no predicate attached; the only enforcement is GenesisAdmissionKernel::admit_difference, which checks a != b (A1) and then carrier membership. '
                     'Kernel-checked for arbitrary name types: the transcribed kernel accepts a pair iff a != b and both are in the carrier, checks A1 first, never inspects the token (acceptance is token-independent) and keeps its admitted pairs irreflexive and inside the carrier (INSTANCES: duplicates and both orientations are accepted); '
                     'the reflexive-transitive closure is the least preorder containing a relation (A3); the face boundary of a coboundary vanishes for every potential iff the three boundary edges are all present or all absent (and the decidable form A5 of the instance section is equivalent to that nilpotence); '
                     'a coboundary descends to the quotient by im d0 iff d1 o d0 = 0, so A7 read as "d1 vanishes on im d0" (our reading of an unpinned gloss) is A5 again; any Nat-valued defect of the form inf over phi of N(h - d0 phi) is gauge invariant (A6; the rational-valued Phi1 of the source is not covered, and its gauge invariance is tested natively only for shifts in {-1,0,1}^n); '
                     'for the TRANSCRIBED rule rcl (none exactly when Phi = 0 and Gamma != 0, Gamma read as the coboundary) the exact-but-not-closed cell is empty iff d1 o d0 = 0 and nonempty otherwise. The source cannot reach its own None branch through compute_triad_signature: its complex constructor rejects d1 o d0 != 0 (gamma2.rs verify_chain_law), it refuses a face with a missing edge (test_triad_refuses_malformed_input) and its Gamma2 is evaluated on the Phi1 residual. '
                     'Native tables, in the PRODUCT model (D, E, F, alpha) on carriers of 1, 2, 3 points with at most one face (0,1,2), present only for n = 3: A1 reads the admitted relation D, A3/A4/A5/A7 read the evaluation relation E and the face flag F, and A10 is read from a free flag alpha with no further content, so independence of A1 and A10 from the other axioms is true by construction and the one computed interaction is A4 versus A5. '
                     'Order of violate_only is [A1, A3, A4, A5, A7, A10]: all-axiom models 1, 12, 2304; A1, A4 and A10 are each violable alone from one point (counts 1, 1, 1 at n=1; 36, 52, 12 at n=2; 16128, 38656, 2304 at n=3); A3 is never violated; A5 and A7 fail together (entries 4 and 5 of violate_only are structurally 0), jointly only from n=3 (1152 structures) because the encoding has a face only for n=3. '
                     'A5 without well-formedness (a floating face with no boundary edge present) holds in 65536 structures at n=3. In the product model the empty structure is always a model and each off-diagonal pair lies in exactly half the models; since A2 is not a state predicate this shows only that the encoding forces no admission. '
                     'The kernel facts are a transcription of admit_difference checked against a reading of the pinned source (the checker re-simulates it; no gate executes the real GenesisAdmissionKernel). Also native: closure counts 1, 4, 29 preorders and six named complexes with exact/closed/rupture counts, the transcribed rule rcl evaluated on (Phi1, coboundary L1 norm) per cochain, and gauge invariance of the unit-weight L1 distance.'),
        'does_not_support': ('A derivation of the axiom list (obligation GEN-WDP-O01 and paper pin tfq_0394 stay open: this is a transcription and a small-model study, not a justification); that the predicates for A2, A4 and A6-A9 are the intended ones (the pinned file has names only; the one-line glosses come from an external copy of the file whose bytes differ from the pin); '
                             'independence of A1 and A10 as a finding about the axioms (it holds by construction of the product model); A9: the relabelling check is an isomorphism (permuting vertex labels while keeping the cochain index-wise) and cannot fail, so it says nothing about observer-selected metrics; carriers of more than 3 points; real-valued Phi1, Gamma2 and R_cl values (here Phi1 is the unit-weight L1 distance to im d0 in integers and Gamma the L1 norm of d1 h); that the exact/closed classification equals classify_exact; any reachability of the source r_cl None branch; the Born, Hilbert or physical reading of any axiom.'),
        'narrowest_claim': ('In a small product model (carriers of at most three points, at most one triangular face, A10 a free flag), the transcribed axioms A1, A4, A5 and A10 are jointly satisfiable and A1, A4, A10 are each violable alone from one point and A5 (together with A7) from three points; A3 holds because a reflexive-transitive closure is a preorder; A7 is A5 under the reading of A7 as d1 vanishing on im d0; '
                            'the kernel enforces only A1 and carrier membership (the token is stored, never checked); and the transcribed R_cl rule refuses exactly on the exact-but-not-closed cell that d1 o d0 = 0 empties, a branch the source cannot reach because it rejects d1 o d0 != 0 at construction. This is evidence about a transcription of the list, not a derivation of it.'),
        'next_test': ('Obtain the definitions of A2, A4 and A6-A9 from the FOC-006 / FOC-000 sources (not bound here), replace the gloss-based predicates by them, and decide whether A9 is independent at all: test it with a weighted L1 norm whose weights are not permuted with the vertices (an observer-selected metric), since the present relabelling check is an isomorphism and cannot fail.')}
    generators = [
        {'id': 'admit_difference', 'source_declarations': ['%s::GenesisAdmissionKernel::admit_difference (line 53) - a definition with a fixed-instance test (line 258: alpha/beta admitted, alpha/alpha refused)' % RS],
         'ordered_inputs': ['Kernel', 'Name', 'Name', 'Token'], 'output': 'KernelResult', 'semantic_predicate': 'Refuse a == b (A1), then refuse names outside the carrier, else append (a, b, token); the token is never inspected.', 'hypotheses': [H]},
        {'id': 'evaluation_closure', 'source_declarations': ['%s::EvaluationPreorder::from_relation (line 75); the test at line 269 is one fixed three-element chain' % RS],
         'ordered_inputs': ['Relation'], 'output': 'Preorder', 'semantic_predicate': 'Reflexive-transitive closure of the base pairs (A3).', 'hypotheses': [H]},
        {'id': 'coboundary_d0', 'source_declarations': ['%s::EvaluationCarrier::carrier (line ~190) delegating to crate::cochains::named_graph_carrier (not bound, not read); nilpotence test at line 285 is one fixed potential on the filled triangle' % RS],
         'ordered_inputs': ['Potential'], 'output': 'EdgeCochain', 'semantic_predicate': 'd0 phi (u,v) = phi(v) - phi(u) on the edges present.', 'hypotheses': [H]},
        {'id': 'coboundary_d1', 'source_declarations': ['%s::EvaluationCarrier (line 176) carrier with faces; test_triad_refuses_malformed_input (line 338) refuses a face with a missing edge' % RS],
         'ordered_inputs': ['EdgeCochain'], 'output': 'FaceCochain', 'semantic_predicate': 'd1 psi (a,b,c) = psi(b,c) - psi(a,c) + psi(a,b), absent edges contributing nothing.', 'hypotheses': [H]},
        {'id': 'triad_class', 'source_declarations': ['%s::TriadSignature (line 135) and the test at line 294 (three fixed classifications on the triangle)' % RS],
         'ordered_inputs': ['EdgeCochain'], 'output': 'TriadClass', 'semantic_predicate': 'exact, closed-not-exact, rupture (not closed), or the fourth cell exact-not-closed.', 'hypotheses': [H]},
        {'id': 'r_cl', 'source_declarations': ['%s::TriadSignature::r_cl (line 159) - a definition: gamma/phi, 0 when both vanish, none otherwise' % RS],
         'ordered_inputs': ['Phi1', 'Gamma2'], 'output': 'MaybeRatio', 'semantic_predicate': 'The R_cl rule; refuses exactly when Phi1 = 0 and Gamma2 != 0.', 'hypotheses': [H]}]
    relations = [
        {'id': 'kernel_accepts_iff_distinct_in_carrier', 'source_declarations': ['%s::admit_difference (line 53); test at line 258 is a fixed instance' % RS],
         'equation_or_predicate': 'admit a b tok succeeds iff a != b and a, b in the carrier; a = b fails with A1 before any carrier check', 'typing_conditions': 'any name type with decidable equality',
         'evidence_status': 'Kernel theorems admit_error_a1, admit_ok_iff; native kernel probe tables', 'scope': 'All carriers'},
        {'id': 'token_stored_not_checked', 'source_declarations': ['%s::admit_difference (line 53): the token argument is only pushed onto the admitted list' % RS],
         'equation_or_predicate': 'acceptance does not depend on the token; the empty token is admitted', 'typing_conditions': 'any token type', 'evidence_status': 'Kernel theorem admit_token_irrelevant; native token_irrelevant column', 'scope': 'All carriers'},
        {'id': 'kernel_invariant_a1', 'source_declarations': ['%s::GenesisAdmissionKernel (line 38)' % RS], 'equation_or_predicate': 'every admitted pair is irreflexive and inside the carrier, and admit preserves this',
         'typing_conditions': 'any name type', 'evidence_status': 'Kernel theorem admit_preserves_inv; instances duplicates_stored, reverse_orientation_accepted', 'scope': 'All carriers'},
        {'id': 'closure_least_preorder', 'source_declarations': ['%s::EvaluationPreorder (line 69), test at line 269: one chain of three elements' % RS],
         'equation_or_predicate': 'reflexive-transitive closure is a preorder containing the relation and contained in every such preorder', 'typing_conditions': 'any relation', 'evidence_status': 'Kernel theorems rtc_preorder, rtc_least; native closure counts 1, 4, 29', 'scope': 'All types; native n <= 3'},
        {'id': 'face_nilpotent_iff', 'source_declarations': ['%s::test_nilpotence_d1_d0_is_zero (line 285): one fixed potential (1/2, 3/4, -1/3) on the filled triangle' % RS],
         'equation_or_predicate': 'd1E o d0 = 0 on a face iff its three boundary edges are all present or all absent; full presence gives 0 for every potential', 'typing_conditions': 'face with distinct vertices',
         'evidence_status': 'Kernel theorems d1_d0, face_nilpotent_iff; native A5 counts', 'scope': 'All potentials, every face'},
        {'id': 'descent_iff_nilpotent', 'source_declarations': ['no source declaration; A7 is named in the enum (line 31) without a predicate'], 'equation_or_predicate': 'd1 factors through the quotient by im d0 iff d1 o d0 = 0',
         'typing_conditions': 'additive groups', 'evidence_status': 'Kernel theorem descends_iff; native a5_equals_a7', 'scope': 'All abelian groups'},
        {'id': 'defect_gauge_invariant', 'source_declarations': ['no source declaration; A6 is named in the enum without a predicate'], 'equation_or_predicate': 'inf over gauge shifts of N(h - d0 phi) is unchanged by h -> h + d0 psi',
         'typing_conditions': 'any natural-valued N', 'evidence_status': 'Kernel theorem defect_gauge_invariant; native gauge_invariant on six complexes', 'scope': 'All'},
        {'id': 'exact_nonclosed_cell', 'source_declarations': ['%s::TriadSignature::r_cl (line 159) and the classification test at line 294' % RS],
         'equation_or_predicate': 'the cell (exact, not closed) is empty iff d1 o d0 = 0; r_cl refuses exactly on phi = 0, gamma != 0', 'typing_conditions': 'additive groups; phi, gamma rationals vanishing exactly on exact and closed cochains',
         'evidence_status': 'Kernel theorems exact_closed, exact_not_closed, trichotomy, rcl_eq_none_iff, rcl_defined_of_nilpotent; native triad refusals (6 of 9 on the half-attached face, 0 elsewhere)', 'scope': 'Hypotheses about Phi1 and Gamma2 are assumptions of the lemma'},
        {'id': 'small_model_independence', 'source_declarations': ['no source declaration'], 'equation_or_predicate': 'A1, A4, A5, A10 are jointly satisfiable and pairwise independent on carriers of 3 points (A5 not before)',
         'typing_conditions': 'carriers of 1..3 points', 'evidence_status': 'Kernel instance a1_a4_a5_independent_on_three_vertices, empty_structure_is_a_model; native models table', 'scope': 'Instance; not a derivation of the list'}]
    compositions = [
        {'outer_operation': 'coboundary_d1', 'input_slot': 0, 'inner_operation': 'coboundary_d0', 'colour_match': 'EdgeCochain', 'hypothesis_match': 'Every face has all three boundary edges present or none.',
         'licensing_relations': ['face_nilpotent_iff'], 'evidence_status': 'Kernel and native'}]
    failed = [
        {'composition': 'r_cl(triad_class(h))', 'reason': 'Colour mismatch: r_cl takes Phi1 and Gamma2, triad_class outputs a class; linking them needs the hypotheses that Phi1 vanishes exactly on exact and Gamma2 exactly on closed cochains (lemma rcl_defined_of_nilpotent assumes them).'},
        {'composition': 'coboundary_d1 o coboundary_d0 on a half-attached face', 'reason': 'With only some boundary edges present d1 o d0 != 0 (kernel face_nilpotent_iff); the source constructor rejects such a face.'},
        {'composition': 'r_cl(triad_class(h)) on an exact cochain with nonzero coboundary', 'reason': 'Phi1 = 0 and Gamma2 != 0 makes r_cl refuse; the cell is empty only when d1 o d0 = 0.'},
        {'composition': 'axiom list derived from the transcription', 'reason': 'No composition derives A1-A10: the list is the input to the study, and independence on three points is not a derivation (tfq_0394).'}]
    counterexamples = [
        {'id': 'token_not_required', 'statement': 'admit_difference with the empty token succeeds; the kernel does not require a token.', 'scope': 'Kernel theorem admit_token_irrelevant.'},
        {'id': 'half_attached_face', 'statement': 'Edges 0-1, 1-2 and the face 0-1-2 (edge 0-2 missing): d1 o d0 != 0, six of the nine {-1,0,1} cochains are exact and not closed, and the transcribed rule rcl would refuse on them; the source refuses to build such a complex.', 'scope': 'Native triad broken_face; kernel exact_not_closed.'},
        {'id': 'floating_face', 'statement': 'A face with no boundary edges present has d1 o d0 = 0 (A5 holds) although the face is not well formed.', 'scope': 'Kernel face_nilpotent_iff; native floating_face and a5_without_well_formed = 65536 on three points.'}]
    return build_spec(
        node=NODE, short='primdiff_axioms', lean='PrimdiffAxioms',
        anchors=['PrimdiffAxioms.admit_error_a1', 'PrimdiffAxioms.admit_ok_iff', 'PrimdiffAxioms.admit_token_irrelevant', 'PrimdiffAxioms.admit_preserves_inv',
                 'PrimdiffAxioms.duplicates_stored', 'PrimdiffAxioms.reverse_orientation_accepted', 'PrimdiffAxioms.rtc_preorder', 'PrimdiffAxioms.rtc_least',
                 'PrimdiffAxioms.d1_d0', 'PrimdiffAxioms.face_nilpotent_iff', 'PrimdiffAxioms.descends_iff', 'PrimdiffAxioms.defect_gauge_invariant',
                 'PrimdiffAxioms.exact_closed', 'PrimdiffAxioms.exact_not_closed', 'PrimdiffAxioms.trichotomy', 'PrimdiffAxioms.rcl_eq_none_iff',
                 'PrimdiffAxioms.rcl_defined_of_nilpotent', 'PrimdiffAxioms.rcl_refuses_zero_one', 'PrimdiffAxioms.a1_a4_a5_independent_on_three_vertices',
                 'PrimdiffAxioms.empty_structure_is_a_model'],
        cases=[list(c) for c in producer.CASES], public_tsv=producer.public_tsv(), data=producer.certificate(),
        scope_review=('Read primitive_axiomatics.rs (sha256 c1ae6edb matches the pin): the enum PrimitiveDifferenceAxiom (line 24) has ten names and no predicate; the kernel (line 38) enforces A1 and carrier membership and stores the token; EvaluationPreorder (line 69), the cochain tests (lines 285-350) and TriadSignature::r_cl (line 159) realise A3, A5 and the triad rule on fixed instances. '
                      'The other bound source, DerivationDagQMClosure.lean::pg_six_operations_and_primdiff_admission_gate (line 764, sha256 c9ad9c23), contains `(x != y and 0 < 2) iff x.val != y.val` on Fin 4, a tautology that is not about the kernel or the axioms; it is vacuous for this node. '
                      'The paper pin tfq_0394 records the list as underived and says the enum and test_primitive_difference.py were not opened. An external copy of the Rust file (different bytes, sha256 e39ae75e) carries one-line doc glosses for A1-A10; they were used only as readings for A4, A6, A7, A9 and are not pinned. '
                      'Result: a transcription of the checkable parts into decidable predicates with explicit statuses, general Lean theorems for the kernel and the cochain facts, and exhaustive native tables on carriers of up to three points.'),
        predicates=['Structures as bitmasks and A4 by mask transposition; A5 by the face rule (present boundary edges in {0, 3}); A7 by brute force over all potentials in {-1,0,1}^n (producer: edge lists, integer matrix product, unit potentials).',
                    'Closure record by the intersection of all preorders containing the relation and by boolean matrix power (producer: Warshall and depth-first reachability).',
                    'Triad tables by brute-force integer potentials in a box (producer: spanning-forest enumeration); gauge and relabelling invariance recomputed.',
                    'Kernel counts by closed forms 2n(n-1), 2(n+1), probes minus both; all-axiom model counts checked against D-factor 2^(n^2-n) times face-factor.',
                    'Exact Python/Rust wire equality and literal Lean axiom reports.'],
        boundary=boundary, generators=generators, relations=relations, compositions=compositions, failed_compositions=failed, counterexamples=counterexamples,
        open_obligations=['The definitions of A2, A4 and A6-A9 are not in the pinned source; the transcriptions here are readings, not the authors\' predicates.',
                          'A9 for general weighted L1 norms and for carriers beyond three points; real-valued Phi1, Gamma2 and the exact classify_exact outcome.',
                          'Whether the list can be justified rather than admitted (GEN-WDP-O01); B001_raw_distinction.lean and test_primitive_difference.py were not read.'],
        colour_meanings={'Kernel': 'Carrier set with the list of admitted (a, b, token) triples', 'Name': 'Carrier item name', 'Token': 'Opaque witness token (never inspected)',
                         'KernelResult': 'Updated kernel or the error a1 / carrier', 'Relation': 'Set of ordered pairs on the carrier', 'Preorder': 'Reflexive transitive relation',
                         'Potential': 'Integer function on vertices', 'EdgeCochain': 'Integer function on the present directed edges', 'FaceCochain': 'Integer function on faces',
                         'TriadClass': 'exact / closed-not-exact / rupture / exact-not-closed', 'Phi1': 'Non-negative quotient L1 distance', 'Gamma2': 'Non-negative closure defect', 'MaybeRatio': 'Rational or refusal'},
        depends_on_result=True,
        qualification='The DAG statement "implementation of the admitted floor, not a derivation" is confirmed and sharpened: the pinned enum carries ten names without predicates, the kernel enforces only A1 and carrier membership, the token is stored and never checked, and A7 is A5 again on every structure.',
        challenge_plan='Coordinate mutants of every certificate leaf plus twelve semantic near misses: the list read as derived (A2 as a predicate), A5 violable on two points, A7 independent of A5, a required token, refused duplicates, refused reverse orientation, swapped guard order, forced admission, R_cl defined on the open cell, closed non-exact cochains on a filled triangle, non-invariant gauge, wrong preorder count.',
        composition_tree=['coboundary_d1(coboundary_d0(phi))'],
        construction='Exhaustive structure counts on carriers of 1, 2, 3 points by block histograms; kernel probe tables; closure counts; six named complexes with integer L1 distances; Lean proves the general kernel and cochain statements.',
        relation_evidence={'face_nilpotent_iff': 'Kernel iff; native A5 counts 8, 512, 655360 of 8, 512, 1048576 structures and A7 counts equal them.',
                           'exact_nonclosed_cell': 'Kernel theorems about the transcribed rule; native triad: transcribed refusals only on the half-attached face (6 of 9); the source cannot reach its None branch.'})


if __name__ == '__main__':
    print(write_spec(HERE, NODE, spec()))
