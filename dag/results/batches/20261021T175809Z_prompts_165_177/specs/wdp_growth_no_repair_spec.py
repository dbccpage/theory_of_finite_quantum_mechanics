"""Build specs/PG-WDP-GROWTH-NO-REPAIR.json from the producer and the node's reviewed claims."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp/batch_tools'))
from spec_builder import build_spec, write_spec  # noqa: E402

_s = importlib.util.spec_from_file_location('producer', ROOT / 'code/python/src/qm/pfp_wdp_growth_no_repair.py')
producer = importlib.util.module_from_spec(_s)
_s.loader.exec_module(producer)

NODE = 'PG-WDP-GROWTH-NO-REPAIR'
DD = 'lean4/DerivationDagQMClosure.lean'
H = ('Graph windows with weighted-L1 norm J (positive integer weights), integer d1 rows and cochain; restriction keeps a set of edges with their cochain values, '
     'weights not increased, and the 2-cells supported inside; attachment adds rows with d1 d0 = 0.')


def spec():
    boundary = {
        'supports': ('Kernel-checked over finite index types, for rational windows whose attained minima Phi1 exist (existence of minimisers is a hypothesis, IsPhi, not proved): if the sub-window d0 is the restriction of the big d0 (hcompat), '
                     'its cochain is the restriction and its weights are at most the restrictions of the big weights, then Phi1(sub) <= Phi1(big) (phi_restrict_le); hence growth with an extending cochain and weights not lowered never lowers Phi1 '
                     '(phi_growth_not_lower, which is the contrapositive of the source necessity wording: a decrease needs deleted cells, lowered weights, an incompatible d0 or changed cochain values); Phi1 <= the unrepaired residual sum; '
                     'attaching a 2-cell leaves (D0, w, h) and hence Phi1 untouched (definitional) and adds |row . h| to the representative norm ||d1 h||_1; this is the source Gamma2 (the norm at the minimal residual) only when d1 d0 = 0, '
                     'which gamma2_repair proves and which every valid row preserves (closed_attach, triangle_row_closed). Boundaries as kernel instances: incompatible d0, weights raised 2 -> 3 (Phi1 4 -> 6), and norm arithmetic only for '
                     'J(a,b) = |a+b| + |a-b|/4 with J(1,-1) = 1/2 < J(1,0) = 5/4 (for d0 = 0 the defect of h is J(h), so deleting a coordinate raises it; this consequence is not stated as a theorem about Phi1). '
                     'Native table of 82 pairs (9 named restrictions plus all 63 edge subsets of K4 for one cochain, 6 attachments incl. an invalid row, 4 edits) with a verified primal potential and dual vector for both windows of every pair and '
                     'Phi1 recomputed by the dual LP in the checker; the strict decreases from deleting cells (3 -> 0), lowering weights (6 -> 2) and changing the cochain (1 -> 0) are native rows, not kernel instances.'),
        'does_not_support': ('Monotonicity for arbitrary norms J or renormalised weights (the instances show it fails), or when the sub d0 is not the restriction of d0; existence of minimisers for weighted L1 as a Lean theorem; '
                             'that each of the three failing hypotheses is by itself sufficient to lower Phi1 in general (kernel instances exist for raised weights and a changed d0; the native rows cover deletion, a changed cochain and lowered weights); '
                             'equal-weight subdivision and filtration limit pages (clauses of WDP-CH04-P09 absent from the source Lean); the source Gamma2 at a minimal residual of a non-closed window (non-unique, withheld); complex coefficients; any physical reading.'),
        'narrowest_claim': ('For weighted-L1 graph windows with attained minima, restricting to a sub-window whose d0, cochain and weights are the restrictions (weights at most the restrictions of the big weights) never raises Phi1, '
                            'and attaching 2-cells with d1 d0 = 0 leaves Phi1 unchanged and cannot lower Gamma2; in the native table, deleting cells, lowering weights and changing the cochain strictly lowered Phi1 '
                            '(kernel instances exist only for raised weights and a changed d0).'),
        'next_test': ('Prove the equal-weight subdivision clause of WDP-CH04-P09 (subdividing an edge through a new degree-two vertex with equal weights leaves Phi1 unchanged) as a Lean theorem over IsPhi and check it by exact enumeration; '
                      'separately discharge the existence of minimisers (IsPhi attainment) for weighted L1 so that phi_restrict_le has no attained-minimum hypothesis.')}
    generators = [
        {'id': 'restrict_window', 'source_declarations': [DD + '::edgeResidualL1 (line 74), wdp_growth_subcomplex_monotone (line 78): list of naturals, appending to a list; not a window restriction'],
         'ordered_inputs': ['Window'], 'output': 'Window', 'semantic_predicate': 'Keep an edge subset with cochain values, weights and the 2-cells supported inside; vertices unchanged.', 'hypotheses': [H]},
        {'id': 'attach_two_cell', 'source_declarations': [DD + '::SimplicialComplex2D (line 86), attachTwoSimplex (line 90): record update that does not touch edgeResiduals'],
         'ordered_inputs': ['Window', 'Row'], 'output': 'Window', 'semantic_predicate': 'Append one row to d1; legal exactly when row . d0 = 0.', 'hypotheses': [H]},
        {'id': 'edit_cochain_or_weights', 'source_declarations': ['no source declaration; the paper clause of WDP-CH04-N02 names these routes in prose'],
         'ordered_inputs': ['Window', 'CochainOrWeights'], 'output': 'Window', 'semantic_predicate': 'Replace h or w on the same graph.', 'hypotheses': [H]},
        {'id': 'phi1', 'source_declarations': ['code/rust/src/wdp/obstruction.rs::solve_exact_potential_weighted (line 142): Rust LP; the source Lean has no definition of Phi1 for these theorems'],
         'ordered_inputs': ['Window'], 'output': 'Phi1', 'semantic_predicate': 'Attained minimum over potentials of the weighted L1 residual.', 'hypotheses': [H]},
        {'id': 'gamma2', 'source_declarations': ['code/rust/src/wdp/primitive_axiomatics.rs::compute_triad_signature (line 207)'],
         'ordered_inputs': ['Window'], 'output': 'Gamma2', 'semantic_predicate': 'L1 norm of d1 h.', 'hypotheses': [H]}]
    relations = [
        {'id': 'restriction_monotone', 'source_declarations': [DD + '::wdp_growth_subcomplex_monotone (line 78): general theorem, but about a sum of naturals appended to a list, i.e. an upper bound for Phi1, not Phi1'],
         'equation_or_predicate': 'hcompat, h restricts, w_sub <= w  implies  Phi1(sub) <= Phi1(big)', 'typing_conditions': 'Window, Window with an edge embedding', 'evidence_status': 'Kernel theorem phi_restrict_le, phi_growth_not_lower; native table and exhaustive subset test', 'scope': 'Finite index types over Q'},
        {'id': 'attachment_preserves_phi1', 'source_declarations': [DD + '::wdp_two_simplex_attachment_preserves_phi1 (line 93): proved by rfl because the record update leaves edgeResiduals alone (vacuous)'],
         'equation_or_predicate': 'Phi1(attach W row) = Phi1(W)', 'typing_conditions': 'Window, Row', 'evidence_status': 'Kernel theorem phi_attach_iff (definitional, labelled as such); native table', 'scope': 'Finite index types over Q'},
        {'id': 'attachment_raises_gamma2_only', 'source_declarations': ['no source declaration; new general theorem'],
         'equation_or_predicate': 'Gamma2(attach W row) = Gamma2(W) + |row . h| >= Gamma2(W)', 'typing_conditions': 'Window, Row', 'evidence_status': 'Kernel theorems gamma2_attach, gamma2_attach_ge, closed_attach; native table', 'scope': 'Finite index types over Q'},
        {'id': 'gamma2_at_minimal_residual', 'source_declarations': ['external omega_wdp run.rs lines 169-171 (not bound): Gamma2 is the norm of d1 at the SAME minimal residual; no Lean source'],
         'equation_or_predicate': 'd1 d0 = 0 implies ||d1 (h - d0 x)||_1 = ||d1 h||_1 for every potential x, in particular at a minimal residual', 'typing_conditions': 'Closed window', 'evidence_status': 'Kernel theorem gamma2_repair; native test over all pairs', 'scope': 'Finite index types over Q'},
        {'id': 'triangle_row_cocycle', 'source_declarations': ['no source declaration; new general theorem'],
         'equation_or_predicate': 'row(ab + bc - ac) . d0 = 0 for any graph window and any triangle a,b,c', 'typing_conditions': 'Graph window', 'evidence_status': 'Kernel theorem triangle_row_closed; native invalid-row pair', 'scope': 'Any edge type with endpoint maps'},
        {'id': 'unrepaired_sum_upper_bound', 'source_declarations': [DD + '::edgeResidualL1 (line 74)'],
         'equation_or_predicate': 'Phi1 <= sum_e w_e |h_e|', 'typing_conditions': 'Window', 'evidence_status': 'Kernel theorem phi_le_unrepaired; native K4 pair has Phi1 = 3 < 5', 'scope': 'Finite index types over Q'}]
    compositions = [
        {'outer_operation': 'phi1', 'input_slot': 0, 'inner_operation': 'attach_two_cell', 'colour_match': 'Window',
         'hypothesis_match': H, 'licensing_relations': ['attachment_preserves_phi1'], 'evidence_status': 'Kernel (definitional) and native'},
        {'outer_operation': 'phi1', 'input_slot': 0, 'inner_operation': 'restrict_window', 'colour_match': 'Window',
         'hypothesis_match': H, 'licensing_relations': ['restriction_monotone'], 'evidence_status': 'Kernel and native'}]
    failed = [{'composition': 'phi1 o restrict_window with weights raised', 'reason': 'Phi1 can go up (parallel edges, weights 2 -> 3, Phi1 4 -> 6): the inequality needs w_sub <= w.'},
              {'composition': 'phi1 o restrict_window for a norm J not monotone under coordinate deletion', 'reason': 'J(a,b) = |a+b| + |a-b|/4 with d0 = 0 gives 1/2 for h = (1,-1) and 5/4 for its restriction (kernel instance).'},
              {'composition': 'phi1 o restrict_window with a sub d0 that is not the restriction of d0', 'reason': 'One edge, d0 = (1) big and (0) small: Phi1 goes from 0 to 1 (kernel instance).'},
              {'composition': 'attach_two_cell with a row that is not a cocycle', 'reason': 'Row (1,0,0) on the triangle has d1 d0 != 0; the result is not a window (table verdict attach_not_a_window, class marker NotAWindow, Gamma2 withheld).'}]
    counterexamples = [{'id': 'parallel_restrict_rescaled_weights', 'statement': 'Three parallel edges 0->1, h = (1,-1,0), weights 2: Phi1 = 4; restricting to the first two edges with weights 3 gives Phi1 = 6.', 'scope': 'Instance (kernel rescaled_weights_instance and native pair).'},
                       {'id': 'nonmonotone_norm', 'statement': 'J(a,b) = |a+b| + |a-b|/4: J(1,-1) = 1/2 but J(1,0) = 5/4.', 'scope': 'Instance (kernel nonmonotone_norm_instance).'},
                       {'id': 'source_vacuity', 'statement': 'The source growth theorem is edgeResidualL1 base <= edgeResidualL1 (base ++ added) for Lists of Nat and the attachment theorem is rfl; neither mentions the minimum over potentials.', 'scope': 'Reading of lean4/DerivationDagQMClosure.lean lines 74-93.'},
                       {'id': 'source_rust_witness_constants', 'statement': 'verify_wdp_obligations_and_growth_witness compares the hard-coded constants 1 <= 1 for the C3/K4 growth claim and adds 3 + 2 = 5 for the exact sequence; it computes no Phi1.', 'scope': 'External omega_symbol_game/src/derivation_dag_witnesses.rs lines 227-239.'}]
    return build_spec(
        node=NODE, short='wdp_growth_no_repair', lean='WdpGrowthNoRepair',
        anchors=['WdpGrowthNoRepair.phi_restrict_le', 'WdpGrowthNoRepair.phi_growth_not_lower', 'WdpGrowthNoRepair.phi_le_unrepaired',
                 'WdpGrowthNoRepair.phi_attach_iff', 'WdpGrowthNoRepair.gamma2_attach', 'WdpGrowthNoRepair.gamma2_attach_ge',
                 'WdpGrowthNoRepair.closed_attach', 'WdpGrowthNoRepair.gamma2_repair', 'WdpGrowthNoRepair.triangle_row_closed', 'WdpGrowthNoRepair.incompatible_d0_instance',
                 'WdpGrowthNoRepair.rescaled_weights_instance', 'WdpGrowthNoRepair.nonmonotone_norm_instance'],
        cases=[dict(c) for c in producer.CASES], public_tsv=producer.public_tsv(), data=producer.certificate(),
        scope_review=('The source claims are PROVED_LEAN, but wdp_growth_subcomplex_monotone is the monotonicity of a List Nat sum under appending, and wdp_two_simplex_attachment_preserves_phi1 is rfl '
                      'because attachTwoSimplex updates only the triangle list; neither involves the minimum over potentials that defines Phi1. The Rust witness uses hard-coded constants. '
                      'The real content is proved here: restriction monotonicity of the attained weighted-L1 minimum under hypotheses the source does not state (d0 compatibility, h restricted, weights not raised, minima attained), '
                      'with kernel counterexamples when a hypothesis is dropped, the definitional invariance of Phi1 under attachment, the additive rise of the representative norm and gamma2_repair (equal to the source Gamma2 at the minimal residual when d1 d0 = 0). The necessity wording of the source (a decrease requires deleted cells, changed weights or changed values) is the contrapositive of phi_growth_not_lower for the modelled structure. Source external hashes match the pins '
                      '(Obstruction.lean, derivation_dag_witnesses.rs, DerivationDagQMClosure.lean); the paper pin tfq_0346 is a CRLF-era hash.'),
        predicates=['Phi1 of both windows from the dual LP (vertices of d0^T y = 0, |y_e| <= w_e), independent of the producer primal vertex enumeration; the carried primal potential x and dual vector y of both windows are verified exactly (cost(x) = y.h = Phi1, d0^T y = 0, |y_e| <= w_e).',
                    'Second window rebuilt from the operation by a different decomposition (row filter by support complement).',
                    'Theorem-level: restriction with weights not raised has Phi1(sub) <= Phi1(big); a valid attachment keeps Phi1 and does not lower Gamma2.',
                    'Verdict, class and complex flags are recomputed, not read from the candidate; public windows are validated (positive weights, endpoint range, integer data, closed base window) and the 82 declared pairs are fixed.',
                    'Exact cross-language (Python/Rust) wire equality and literal Lean axiom reports.'],
        boundary=boundary, generators=generators, relations=relations, compositions=compositions, failed_compositions=failed, counterexamples=counterexamples,
        open_obligations=['Equal-weight subdivision and filtration limit pages (WDP-CH04-P09).', 'Existence of minimisers (IsPhi attainment) for weighted L1 as a Lean theorem.',
                          'Norms other than weighted L1 and complex coefficients.'],
        colour_meanings={'Window': 'Graph window (nv, edges, weights, d1 rows, cochain h)', 'Row': 'Integer 2-cell boundary row over the edges', 'CochainOrWeights': 'Replacement integer vector',
                         'Phi1': 'Exact rational quotient defect', 'Gamma2': 'Exact rational L1 norm of d1 h'},
        depends_on_result=True,
        qualification='Restriction monotonicity of Phi1 holds for a weighted-L1 norm with the sub d0, cochain and weights the restrictions (weights not raised); the source Lean theorems prove only a List Nat sum bound and an rfl, and the statement fails for re-normalised weights or a norm not monotone under coordinate deletion.',
        challenge_plan='Coordinate mutants of every certificate leaf plus fifteen semantic near misses (rescaled weights called monotone, attachment lowers Phi1, Gamma2 kept, invalid row accepted, residual sum as Phi1, class unchanged, gauge shift as repair, weight change called invariant, face survives without edges, representative Gamma2 for a non-window, lowered weights called raising, deletion called neutral, routing name as class, subset restriction raised, non-optimal witness) and one control.',
        composition_tree=['phi1(attach_two_cell(W, row))', 'phi1(restrict_window(W, keep))'],
        construction='Exact table over 82 window pairs with verified primal and dual witnesses; Lean proves the general restriction and attachment statements, gamma2_repair and three boundary instances.',
        relation_evidence={'restriction_monotone': 'Kernel theorem plus the certificate itself: all 63 edge subsets of K4 for one cochain, each with primal and dual witnesses (the Python unit test also covers 243 cochains).', 'attachment_preserves_phi1': 'Definitional in Lean (the source one is rfl too); native rows show Phi1 equal and Gamma2 up.'})


if __name__ == '__main__':
    print(write_spec(HERE, NODE, spec()))
