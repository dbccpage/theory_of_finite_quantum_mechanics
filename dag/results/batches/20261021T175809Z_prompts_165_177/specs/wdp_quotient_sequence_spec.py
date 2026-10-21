"""Build specs/PG-WDP-QUOTIENT-EXACT-SEQUENCE.json from the producer and the node's reviewed claims."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp/batch_tools'))
from spec_builder import build_spec, write_spec  # noqa: E402

_s = importlib.util.spec_from_file_location('producer', ROOT / 'code/python/src/qm/pfp_wdp_quotient_sequence.py')
producer = importlib.util.module_from_spec(_s)
_s.loader.exec_module(producer)

NODE = 'PG-WDP-QUOTIENT-EXACT-SEQUENCE'
OBS = 'external omega_engine_atlas/.../000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean'
DD = 'lean4/DerivationDagQMClosure.lean'
H = ('Graph windows: d0 = coboundary of a directed multigraph, d1 an integer matrix with d1 d0 = 0 (a window), non-negative integer weights '
     '(J = weighted L1; J is a norm only when every weight is positive), integer cochain h; the window is a declared datum.')


def spec():
    boundary = {
        'supports': ('Kernel-checked for modules over a field: with d1 d0 = 0 the sequence 0 -> H1 -> Q1 -> im d1 -> 0 is exact (injective, ker = range, onto) and, in finite dimension, dim Q1 = dim H1 + dim im d1 and '
                     'dim Q1 + dim im d0 = dim C1. When H1 and im d1 are both nontrivial NO section is invariant under the automorphisms 1 + incl f pi of the extension (these act simply transitively on the sections and are '
                     'automorphisms of the extension, not of the window and not isometries of J; INSTANCE model C1 = Q^2, d0 = 0, d1(a,b) = b); when H1 or im d1 is trivial (and pi is onto) there is exactly one section and it is invariant '
                     '(exists_unique_invariant_section_of_trivial). Exactly one diagnostic class holds for every (Phi1, Gamma2); for a definite J, Phi1 = 0 iff the class is zero (false for a seminorm, kernel instance with J = 0 on Q). '
                     'For d1 d0 = 0 and an attained minimum Phi1, ||d1 h||_1 <= c Phi1 whenever sum_r |d1_re| <= c w_e for all e (gamma_le_opnorm_phi, with gamma2_repair moving from the representative to the minimiser); at the minimiser '
                     'itself the bound needs no closure (gamma_at_minimiser_le). The operator bound ||d1 v||_1 <= c ||v||_J for all v is equivalent to these column inequalities (opbound_of_columns, columns_of_opbound), so the least c is '
                     'max_e column sum / w_e when all w_e > 0 (that max formula and its null-weight convention are the checker definition); a smaller constant fails (kernel instance with the largest entry as c). '
                     'Native table over 14 windows with a verified primal potential and dual vector each (cost(x) = y.h = Phi1, d0^T y = 0, |y_e| <= w_e), dim H1 recomputed in the checker from an explicit nullspace basis of d1 minus rank d0, '
                     'splitting freedom dim H1 * dim im d1, class, operator norm and inequality. One window has d1 d0 != 0: there kappa1 is undefined and the representative norm ||d1 h||_1 = 2 exceeds ||d1|| Phi1 = 0, but the source Gamma2 '
                     'at the minimal residual h* = 0 is 0 and the inequality holds, so Gamma2 is withheld for it. For a seminorm (a zero-weight edge) the label ExactClass means only Phi1 = 0: seminorm_zero_weight_filled has Phi1 = 0 and ||d1 h||_1 = 1.'),
        'does_not_support': ('Any derivation of the window; norms other than weighted L1 for the inequality; complex coefficients; a statement that the sequence has or lacks a section natural for automorphisms of the window '
                             '(graph automorphisms preserving d0, d1 and the weights); the converse "if there is an invariant section then dim H1 * dim im d1 = 0" is native by dimension (section_dim) with the trivial-factor halves in the kernel; '
                             'existence of minimisers for general norms; Phi1 >= 0 as a theorem for the weighted-L1 window (gamma2_nonneg is anchored, Phi1 >= 0 needs the cost bridge of the degree-1 window node); any physical reading of the classes.'),
        'narrowest_claim': ('For a window over a field with d1 d0 = 0 the sequence 0 -> H1 -> Q1 -> im d1 -> 0 is exact; no section is invariant under 1 + incl f pi when dim H1 > 0 and dim im d1 > 0 (kernel), and when dim H1 * dim im d1 = 0 '
                            'there is exactly one section and it is invariant (kernel); every class has exactly one diagnostic class; Phi1 = 0 iff the class is zero for a definite J; and ||d1 h||_1 <= c Phi1 for an attained minimum '
                            'and c at least the J-to-L1 column bound.'),
        'next_test': ('Decide the splitting claim for the finite group G of automorphisms of the K4 two-face window (graph automorphisms preserving the two faces, d0, d1 and the weights) by solving the linear fixed-point '
                      'equations of G on the affine section space over Hom(im d1, H1) = Q^2: either a G-fixed section exists or the fixed locus is empty.')}
    generators = [
        {'id': 'kappa1_on_q1', 'source_declarations': [OBS + '::kappa (line 61), kappa_well_defined (line 51): general over Add types with d1 additive and d1 d0 = 0'],
         'ordered_inputs': ['Window'], 'output': 'ClosureMap', 'semantic_predicate': 'kappa1: Q1 -> C2 with kappa1 o mk = d1, defined iff d1 d0 = 0.', 'hypotheses': [H]},
        {'id': 'h1_subspace', 'source_declarations': [OBS + '::H1 (line 82): subtype of Q1 on which kappa vanishes'],
         'ordered_inputs': ['ClosureMap'], 'output': 'H1', 'semantic_predicate': 'ker kappa1 inside Q1.', 'hypotheses': [H]},
        {'id': 'section_space', 'source_declarations': ['no source declaration; the source Lean never states non-splitting'],
         'ordered_inputs': ['ClosureMap'], 'output': 'SectionSpace', 'semantic_predicate': 'Linear sections of Q1 -> im d1: an affine space over Hom(im d1, H1) of dimension dim H1 * dim im d1.', 'hypotheses': [H]},
        {'id': 'operator_norm', 'source_declarations': [OBS + '::closure_charge_le_opnorm_mul_phi (line 153): takes the operator bound as a hypothesis (opbound), never computes ||d1||'],
         'ordered_inputs': ['Window'], 'output': 'OpNorm', 'semantic_predicate': 'Least c with ||d1 v||_1 <= c ||v||_J: max over edges of column L1 sum / weight; none for a null-weight edge with a nonzero column.', 'hypotheses': [H]},
        {'id': 'ratio_bound', 'source_declarations': [OBS + '::closure_ratio_le_opnorm (line 138), closure_ratio_nonneg (line 144), closure_ratio_signature (line 190): general over Q given the hypotheses'],
         'ordered_inputs': ['OpNorm', 'Phi1'], 'output': 'Gamma2Bound', 'semantic_predicate': 'Gamma2 <= ||d1|| Phi1.', 'hypotheses': [H]}]
    relations = [
        {'id': 'sequence_exact', 'source_declarations': [OBS + '::kappa_exact_sequence (line 93): general theorem on quotient types with four clauses (injective, ker, representatives, onto im d1)'],
         'equation_or_predicate': '0 -> H1 -> Q1 -> im d1 -> 0 exact; dim Q1 = dim H1 + dim im d1', 'typing_conditions': 'Window with d1 d0 = 0', 'evidence_status': 'Kernel theorems exact_sequence, finrank_sequence; native dimension table', 'scope': 'Modules over a field (finite dimension for the count)'},
        {'id': 'no_invariant_section', 'source_declarations': ['no source declaration; the Rust witness (verify_wdp_obligations_and_growth_witness, line 234-239) only adds 3 + 2 = 5'],
         'equation_or_predicate': 'H1, im d1 nontrivial implies no section s with (1 + incl f pi) s = s for all f; H1 = 0 or im d1 = 0 implies exactly one section, and it is invariant', 'typing_conditions': 'Exact sequence of vector spaces', 'evidence_status': 'Kernel theorems no_natural_section, section_unique_of_subsingleton, exists_unique_invariant_section_of_trivial, instance window_instance_no_natural_section; native section_dim', 'scope': 'Automorphisms 1 + incl f pi of the extension only (not of the window, not J-isometries)'},
        {'id': 'unique_class', 'source_declarations': ['external omega_policy/src/trichotomy.rs::classify_exact (line 65): if-chain'],
         'equation_or_predicate': 'exactly one of Phi1 = 0, (Phi1 > 0, Gamma2 = 0), (Phi1 > 0, Gamma2 > 0)', 'typing_conditions': 'Phi1, Gamma2 rational', 'evidence_status': 'Kernel theorem diag_unique; native classes_hit = 1 on all windows', 'scope': 'All rational pairs'},
        {'id': 'phi_zero_iff_zero_class', 'source_declarations': ['no source declaration; Rust defines ExactRepair as Phi1 = 0 (a definition, not a theorem)'],
         'equation_or_predicate': 'Phi1 = 0 iff [h] = 0 in Q1, for definite nonnegative J', 'typing_conditions': 'Window', 'evidence_status': 'Kernel theorem isPhi_zero_iff and seminorm_instance; native phi_zero_iff_class_zero', 'scope': 'Attained minimum'},
        {'id': 'gamma_le_opnorm_phi', 'source_declarations': [OBS + '::closure_charge_le_opnorm_mul_phi (line 153): general with the operator bound assumed'],
         'equation_or_predicate': 'sum_r |d1_re| <= c w_e for all e and d1 d0 = 0 imply Gamma2 <= c Phi1; the column bound is necessary for ||d1 v|| <= c ||v||_J', 'typing_conditions': 'Window, weighted L1', 'evidence_status': 'Kernel theorems gamma_le_opnorm_phi, gamma2_repair, gamma_at_minimiser_le, opbound_of_columns, columns_of_opbound, instance gamma_bound_fails_instance; native table', 'scope': 'Weighted L1 over Q, attained minimum, d1 d0 = 0 for the representative form'}]
    compositions = [
        {'outer_operation': 'ratio_bound', 'input_slot': 0, 'inner_operation': 'operator_norm', 'colour_match': 'OpNorm',
         'hypothesis_match': H, 'licensing_relations': ['gamma_le_opnorm_phi'], 'evidence_status': 'Kernel and native'},
        {'outer_operation': 'h1_subspace', 'input_slot': 0, 'inner_operation': 'kappa1_on_q1', 'colour_match': 'ClosureMap',
         'hypothesis_match': 'Requires d1 d0 = 0.', 'licensing_relations': ['sequence_exact'], 'evidence_status': 'Kernel and native'}]
    failed = [{'composition': 'section_space(kappa1_on_q1) invariant under 1 + incl f pi', 'reason': 'No invariant section when dim H1 > 0 and dim im d1 > 0 (kernel no_natural_section).'},
              {'composition': 'ratio_bound o operator_norm with the largest entry as ||d1||', 'reason': 'Column (1,1,1) has largest entry 1 but J-to-L1 norm 3; Gamma2 = 3 > 1 * Phi1 = 1 (kernel gamma_bound_fails_instance).'},
              {'composition': 'kappa1_on_q1 on a window with d1 d0 != 0', 'reason': 'Not defined; the table marks it NotAWindow and withholds Gamma2: the representative norm is 2 while the norm at the minimal residual h* = 0 is 0, so the failing inequality there is a convention artefact, not a counterexample to the source.'}]
    counterexamples = [{'id': 'canonical_splitting_for_trivial_h1', 'statement': 'For K4 with all faces H1 = 0, so the section is unique and canonical: the source phrase "no canonical splitting" is false there.', 'scope': 'Native table (section_dim 0) and kernel section_unique_of_subsingleton.'},
                       {'id': 'seminorm_exact_class', 'statement': 'Triangle with weights (0,1,1) and h = (1,0,0): Phi1 = 0 while the class of h is nonzero (kernel seminorm_instance).', 'scope': 'Instance.'},
                       {'id': 'source_vacuous_anchors', 'statement': 'The DAG lean anchors master_dag_177_node_10_stage_and_172_route_partition_conservation and master_operad_25_family_composition_and_end_to_end_chain_closure are fixed arithmetic identities (132+0+25+14+3+3 = 177, d0*1 = d0, ...) with no cochain content.', 'scope': 'Reading of lean4/DerivationDagQMClosure.lean lines 1320-1345.'}]
    return build_spec(
        node=NODE, short='wdp_quotient_sequence', lean='WdpQuotientSequence',
        anchors=['WdpQuotientSequence.exact_sequence', 'WdpQuotientSequence.finrank_sequence', 'WdpQuotientSequence.no_natural_section',
                 'WdpQuotientSequence.section_unique_of_subsingleton', 'WdpQuotientSequence.exists_unique_invariant_section_of_trivial',
                 'WdpQuotientSequence.window_instance_no_natural_section',
                 'WdpQuotientSequence.diag_unique', 'WdpQuotientSequence.isPhi_zero_iff', 'WdpQuotientSequence.seminorm_instance',
                 'WdpQuotientSequence.opbound_of_columns', 'WdpQuotientSequence.columns_of_opbound', 'WdpQuotientSequence.gamma2_repair',
                 'WdpQuotientSequence.gamma2_nonneg', 'WdpQuotientSequence.gamma_le_opnorm_phi', 'WdpQuotientSequence.gamma_at_minimiser_le',
                 'WdpQuotientSequence.gamma_bound_fails_instance'],
        cases=[dict(c) for c in producer.CASES], public_tsv=producer.public_tsv(), data=producer.certificate(),
        scope_review=('The source Obstruction.lean proves kappa_well_defined and kappa_exact_sequence in general (on Add types) but never states "no canonical splitting", and its ratio bound takes the operator bound as a hypothesis. '
                      'Mined: Q1, Repair, kappa, H1, kappa_exact_sequence, closure_charge_le_opnorm_mul_phi, closure_ratio_*; the two DerivationDagQMClosure anchors in the paper pin are fixed arithmetic. '
                      'Proved here over a field: exactness and the dimension count, the conditional non-splitting (invariance under 1 + incl f pi; false when H1 = 0 or d1 = 0), uniqueness of the class, Phi1 = 0 iff zero class for definite J '
                      '(false for a seminorm), and Gamma2 <= c Phi1 with the explicit column form of the operator-norm hypothesis and its necessity. External source hashes match the pins (Obstruction.lean, derivation_dag_witnesses.rs); '
                      'the paper pin tfq_0345 is a CRLF-era hash.'),
        predicates=['Phi1 from the dual LP (vertices of d0^T y = 0, |y_e| <= w_e), independent of the producer primal vertex enumeration; the carried primal potential x and dual vector y are verified exactly (cost(x) = y.h = Phi1, d0^T y = 0, |y_e| <= w_e).',
                    'Ranks by Bareiss elimination; dim H1 from an explicit nullspace basis of d1 (killed by d1, independent) minus rank d0; membership of h in im d0 by augmented rank; ||d1|| as the largest column-sum/weight ratio.',
                    'Splitting freedom dim H1 * dim im d1 from ranks; canonical iff zero.',
                    'Theorem-level: exactly one class; dimension count on every complex; Gamma2 <= ||d1|| Phi1 on every complex with a finite norm; Phi1 = 0 iff zero class when all weights are positive.',
                    'Exact cross-language (Python/Rust) wire equality and literal Lean axiom reports.'],
        boundary=boundary, generators=generators, relations=relations, compositions=compositions, failed_compositions=failed, counterexamples=counterexamples,
        open_obligations=['Splitting naturality for automorphisms of the window (graph automorphisms preserving d0, d1 and the weights).', 'Inequality for norms other than weighted L1 and for complex coefficients.', 'Phi1 >= 0 for the weighted-L1 window as a theorem of this module (see the degree-1 window node).',
                          'Derivation of the window from Genesis admission.'],
        colour_meanings={'Window': 'Graph window (nv, edges, weights, d1 rows, cochain h)', 'ClosureMap': 'kappa1 : Q1 -> C2', 'H1': 'ker kappa1', 'SectionSpace': 'Affine space of linear sections of Q1 -> im d1',
                         'OpNorm': 'Exact rational J-to-L1 operator norm of d1', 'Phi1': 'Exact rational quotient defect', 'Gamma2Bound': 'The inequality Gamma2 <= ||d1|| Phi1'},
        depends_on_result=True,
        qualification='"No canonical splitting" is proved only as: no section is invariant under the automorphisms 1 + incl f pi of the extension, and only when dim H1 > 0 and dim im d1 > 0 (otherwise the section is unique and invariant); it is not a statement about automorphisms of the window; "Phi1 = 0 exactly for ExactClass" needs J definite; Gamma2 <= ||d1|| Phi1 needs ||d1|| the J-to-L1 operator norm (largest column sum over weight), not the largest entry.',
        challenge_plan='Coordinate mutants of every certificate leaf plus fourteen semantic near misses (canonical splitting claimed, splitting denied for trivial H1, splitting claimed for d1 = 0, exactness without complex, largest-entry norm, representative and minimal-residual Gamma2 for a non-window, seminorm equivalence, seminorm label, two classes, H1 without quotient, weights ignored in the norm, nonzero class called zero, non-optimal primal witness) and one control.',
        composition_tree=['ratio_bound(operator_norm(W), phi1(W))', 'h1_subspace(kappa1_on_q1(W))'],
        construction='Exact table over 14 graph windows with verified primal and dual witnesses; Lean proves the module-level exactness, the non-splitting and its trivial-factor boundary, and the column-form inequality.',
        relation_evidence={'no_invariant_section': 'Kernel theorem plus native section_dim: 3 of 14 windows (two_triangles_mixed, k4_two_faces, parallel_bigon_active) have dim H1 * dim im d1 > 0 and canonical_split false; the others have a unique section.', 'gamma_le_opnorm_phi': 'Kernel theorem; native bound_holds on every complex window.'})


if __name__ == '__main__':
    print(write_spec(HERE, NODE, spec()))
