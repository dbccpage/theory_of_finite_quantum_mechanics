"""Build specs/PG-WDP-DEGREE1-WINDOW.json from the producer and the node's reviewed claims."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp/batch_tools'))
from spec_builder import build_spec, write_spec  # noqa: E402

_s = importlib.util.spec_from_file_location('producer', ROOT / 'code/python/src/qm/pfp_wdp_degree1_window.py')
producer = importlib.util.module_from_spec(_s)
_s.loader.exec_module(producer)

NODE = 'PG-WDP-DEGREE1-WINDOW'
OBS = 'external omega_engine_atlas/.../000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean'
H = ('Graph windows: d0 = coboundary of a directed multigraph (loop rows are zero), d1 an integer matrix over the edges, '
     'positive integer weights (J = weighted L1), integer 1-cochain h; the window itself is a declared datum.')


def spec():
    boundary = {
        'supports': ('Kernel-checked over a field (the integer graph windows are tensored with Q, so Q1, dim Q1 and dim H1 are Q-quantities): d1 descends to Q1 = C1/im d0 exactly when d1 o d0 = 0 '
                     '(an instance with d1 d0 != 0 has no kappa1 and two representatives of the zero class with different d1 values); H1 = ker kappa1 is the image of ker d1 in Q1 and a class is closed iff every '
                     'representative is. For the abstract defect IsPhi (attained minimum of a function J over h + im d0): it is repair invariant and unique; for nonnegative definite J it is nonnegative and zero exactly on the zero class. '
                     'BRIDGE (kernel): for the weighted-L1 graph cost, cost D w h x = wl1 w (h + negD D x), IsPhi (wl1 w) (negD D) is the attained minimum of cost (isPhi_graph_iff), wl1 is nonnegative and, for positive weights, definite, '
                     'so Phi1 = 0 iff the class is zero for EVERY graph window with positive weights (graph_phi_zero_iff). Weak duality and its certificate form isPhi_of_certificate (a primal potential x and a dual vector y with equal values '
                     'give the attained minimum); the filled triangle has Phi1 = Gamma2 = 2. Every (Phi1, Gamma2) pair lies in exactly one of ExactClass / ClosedResidual / ActiveClosureFailure; for Phi1 >= 0 the spellings phi != 0 and '
                     'phi > 0 agree (ne_zero_iff_pos). Native table over 17 graph windows (loop, disconnected, empty C2, d1 = 0, zero class, weights, a gauge-shifted pair, two windows with d1 d0 != 0 marked NotAWindow with a kappa witness): '
                     'every record carries a primal potential x and a dual vector y that the checker verifies exactly (cost(x) = y.h = Phi1, d0^T y = 0, |y_e| <= w_e), plus the dual-LP value recomputed independently of the producer; '
                     'the two gauge-shifted windows must carry equal Phi1, Gamma2, R_cl and class. For a non-window Phi1 (a class function of d0, J, h) is kept and Gamma2 is withheld, because the representative norm ||d1 h||_1 depends on the representative there.'),
        'does_not_support': ('Any derivation of the window from Genesis admission or Real_0 (it stays a declared datum); norms other than weighted L1; non-graph d0 beyond the module-level lemmas; existence of the attained minimum for the '
                             'weighted-L1 cost as a Lean theorem (attainment is part of IsPhi and is witnessed natively by x and y, but LP strong duality / minimiser existence is not formalised); complex coefficients; '
                             'any meaning of Gamma2 for a non-window (representative dependent); that R_cl = Gamma2/Phi1 mixes the weighted Phi1 with the unweighted Gamma2 and so depends on the weight scale; any physical reading of the three classes.'),
        'narrowest_claim': ('For modules over a field (the graph windows tensored with Q), kappa1 exists on Q1 = C1/im d0 exactly when d1 d0 = 0 (kernel); for graph windows with positive weights the weighted-L1 cost is the IsPhi defect of a '
                            'nonnegative definite J, so Phi1 = 0 iff the class is zero (kernel); on the 17 tabulated integer windows Phi1 is the weighted-L1 minimum over rational potentials with a verified primal potential and dual vector; '
                            'each (Phi1, Gamma2) pair has exactly one class: ExactClass iff Phi1 = 0, ClosedResidual iff Phi1 > 0 and Gamma2 = 0, ActiveClosureFailure iff both are positive (the Lean diag theorems state phi != 0, equivalent for Phi1 >= 0).'),
        'next_test': ('Prove in Lean that the weighted-L1 quotient defect of every graph window is attained (existence of a minimising potential, or strong duality for the pair of linear programs), so that the attainment clause of IsPhi '
                      'becomes a theorem for the windows instead of resting on the verified primal and dual witnesses tabulated here.')}
    generators = [
        {'id': 'repair_quotient_q1', 'source_declarations': [OBS + '::Q1 (line 42), Repair (line 37): definition on a bare Add type, no module structure'],
         'ordered_inputs': ['Window'], 'output': 'RepairQuotient', 'semantic_predicate': 'Q1 = C1 / im d0 as a module quotient; the class of h is h + im d0.', 'hypotheses': [H]},
        {'id': 'kappa1', 'source_declarations': [OBS + '::kappa (line 61), kappa_well_defined (line 51): general theorem on Add types given d1 additive and d1 d0 = 0'],
         'ordered_inputs': ['RepairQuotient'], 'output': 'ClosureCharge', 'semantic_predicate': 'kappa1([h]) = d1 h, defined iff d1 d0 = 0 (iff statement proved for modules over a field).', 'hypotheses': [H]},
        {'id': 'quotient_defect_phi1', 'source_declarations': ['code/rust/src/wdp/obstruction.rs::solve_exact_potential_weighted (line 142), DualWitnessCertificate (line 42): Rust algorithm, not executed here',
                                                                OBS + '::dual_certificate_lower_bound (weak duality, general theorem on lists)'],
         'ordered_inputs': ['RepairQuotient'], 'output': 'Phi1', 'semantic_predicate': 'Attained minimum over potentials x of sum_e w_e |h_e - (d0 x)_e|.', 'hypotheses': [H]},
        {'id': 'closure_gamma2', 'source_declarations': ['code/rust/src/wdp/primitive_axiomatics.rs::compute_triad_signature (line 207): Gamma2 computed from the primal residual; equals d1 h when d1 d0 = 0'],
         'ordered_inputs': ['ClosureCharge'], 'output': 'Gamma2', 'semantic_predicate': 'Unweighted L1 norm of d1 h.', 'hypotheses': [H]},
        {'id': 'diagnostic_class', 'source_declarations': ['external omega_policy/src/trichotomy.rs::ObstructionDiagnosticClass (line 17), classify_exact (line 65): the first variant is named ExactRepair there',
                                                          'code/rust/src/wdp/primitive_axiomatics.rs::TriadSignature::r_cl (line 159): returns Some(0) at Phi1 = 0 and Gamma2 = 0, an extension of the node statement'],
         'ordered_inputs': ['Phi1', 'Gamma2'], 'output': 'DiagnosticClass',
         'semantic_predicate': 'ExactClass iff Phi1 = 0; ClosedResidual iff Phi1 > 0 and Gamma2 = 0; ActiveClosureFailure iff Phi1 > 0 and Gamma2 > 0; NotAWindow (a refusal marker, not a class) when d1 d0 != 0.', 'hypotheses': [H]}]
    relations = [
        {'id': 'kappa_descends_iff_complex', 'source_declarations': [OBS + '::kappa_well_defined (line 51): one direction (d1 d0 = 0 gives invariance) as a general theorem; the converse is new'],
         'equation_or_predicate': 'exists kappa on Q1 with kappa o mk = d1  <->  d1 o d0 = 0', 'typing_conditions': 'Window', 'evidence_status': 'Kernel theorem kappa_descends_iff and instance kappa_not_defined_instance; native table of two refused windows', 'scope': 'Modules over a field'},
        {'id': 'h1_is_image_of_cycles', 'source_declarations': [OBS + '::kappa_exact_sequence (line 93): clause (iii), general theorem'],
         'equation_or_predicate': 'ker kappa1 = mk(ker d1); kappa1 q = 0 iff every representative has d1 = 0', 'typing_conditions': 'Window with d1 d0 = 0', 'evidence_status': 'Kernel theorems ker_kappa_eq_map, kappa_eq_zero_iff; native dim H1 = m - rank d1 - rank d0', 'scope': 'Modules over a field'},
        {'id': 'phi1_class_function', 'source_declarations': ['no source declaration (the source Lean takes the infimum characterisation as a hypothesis); new general theorem'],
         'equation_or_predicate': 'Phi_J(h + d0 y) = Phi_J(h); Phi_J(h) = 0 iff [h] = 0 for definite J', 'typing_conditions': 'Window with J nonnegative and definite', 'evidence_status': 'Kernel theorems isPhi_shift, isPhi_unique, isPhi_zero_iff', 'scope': 'Attained minimum; any norm J on C1'},
        {'id': 'diagnostic_trichotomy', 'source_declarations': ['external omega_policy/src/trichotomy.rs::classify_exact (line 65): fixed code with an if-chain, not a theorem'],
         'equation_or_predicate': 'exactly one of Phi1 = 0, (Phi1 > 0 and Gamma2 = 0), (Phi1 > 0 and Gamma2 > 0)', 'typing_conditions': 'Phi1, Gamma2 rational', 'evidence_status': 'Kernel theorem diag_unique, ratio_class; native table', 'scope': 'All rational pairs'},
        {'id': 'graph_cost_is_isphi', 'source_declarations': ['no source declaration; bridge between the Rust L1Seminorm residual and the module-form quotient defect'],
         'equation_or_predicate': 'cost D w h x = wl1 w (h + negD D x); IsPhi (wl1 w) (negD D) h p iff p is the attained minimum of cost; Phi1 = 0 iff [h] = 0 for positive weights', 'typing_conditions': 'Finite edge and vertex types over Q', 'evidence_status': 'Kernel theorems cost_eq, isPhi_graph_iff, wl1_definite, graph_phi_zero_iff', 'scope': 'Any matrix D, positive weights for the zero-class statement'},
        {'id': 'weak_duality_lower_bound', 'source_declarations': [OBS + '::dual_certificate_lower_bound (list version, general over lists of edges)'],
         'equation_or_predicate': 'd0^T y = 0, |y_e| <= w_e  implies  y . h <= sum_e w_e |h_e - (d0 x)_e| for every x', 'typing_conditions': 'Fin-indexed edges and vertices', 'evidence_status': 'Kernel theorems weak_duality, isPhi_of_certificate, instance tri_phi (Phi1 = 2); every table record carries x and y verified by the checker', 'scope': 'Weighted L1 over Q'}]
    compositions = [
        {'outer_operation': 'diagnostic_class', 'input_slot': 0, 'inner_operation': 'quotient_defect_phi1', 'colour_match': 'Phi1',
         'hypothesis_match': H, 'licensing_relations': ['diagnostic_trichotomy', 'phi1_class_function'], 'evidence_status': 'Kernel and native'},
        {'outer_operation': 'closure_gamma2', 'input_slot': 0, 'inner_operation': 'kappa1', 'colour_match': 'ClosureCharge',
         'hypothesis_match': 'Requires kappa1 defined, i.e. d1 d0 = 0; otherwise the composite is a refusal (NotAWindow).', 'licensing_relations': ['kappa_descends_iff_complex'], 'evidence_status': 'Kernel and native'}]
    failed = [{'composition': 'closure_gamma2 o kappa1 on a window with d1 d0 != 0', 'reason': 'kappa1 does not exist on Q1 (kappa_descends_iff); the table records NotAWindow with the witness d1 d0 e_v != 0 and withholds Gamma2.'},
              {'composition': 'diagnostic_class with R_cl at Phi1 = 0', 'reason': 'R_cl = Gamma2/Phi1 is undefined at Phi1 = 0; the Rust r_cl convention Some(0) is an extension, not the node statement.'}]
    counterexamples = [{'id': 'violates_d1d0_edge', 'statement': 'One edge 0->1 with d1 = (1): d1 d0 e_0 = -1, so the representatives 0 and d0 e_0 of the zero class have d1 values 0 and -1.', 'scope': 'Instance; general statement is kappa_descends_iff.'},
                      {'id': 'unrepaired_sum_is_not_phi1', 'statement': 'On K4 with h = (1,0,2,1,0,1) the unrepaired residual sum is 5 but Phi1 = 3.', 'scope': 'Instance; general bound is phi_le_unrepaired in the growth node.'}]
    return build_spec(
        node=NODE, short='wdp_degree1_window', lean='WdpDegree1Window',
        anchors=['WdpDegree1Window.kappa_descends_iff', 'WdpDegree1Window.ker_kappa_eq_map', 'WdpDegree1Window.kappa_eq_zero_iff',
                 'WdpDegree1Window.kappa_not_defined_instance', 'WdpDegree1Window.isPhi_shift', 'WdpDegree1Window.isPhi_zero_iff',
                 'WdpDegree1Window.isPhi_nonneg', 'WdpDegree1Window.diag_unique', 'WdpDegree1Window.ne_zero_iff_pos', 'WdpDegree1Window.ratio_class',
                 'WdpDegree1Window.weak_duality', 'WdpDegree1Window.isPhi_of_certificate', 'WdpDegree1Window.cost_eq', 'WdpDegree1Window.isPhi_graph_iff',
                 'WdpDegree1Window.wl1_definite', 'WdpDegree1Window.graph_phi_zero_iff', 'WdpDegree1Window.tri_phi', 'WdpDegree1Window.tri_gamma2'],
        cases=[dict(c) for c in producer.CASES], public_tsv=producer.public_tsv(), data=producer.certificate(),
        scope_review=('The node statement is a DEFINITION. Mined from Obstruction.lean (Repair, Q1, kappa, kappa_well_defined, H1, kappa_exact_sequence: general over Add types), '
                      'code/rust/src/wdp/obstruction.rs (Cochain1, the exact LP certificate) and primitive_axiomatics.rs (TriadSignature, compute_triad_signature) plus the external '
                      'omega_policy trichotomy. The source classes (Rust trichotomy.rs) are: exact iff Phi1 = 0, closed residual iff Phi1 > 0 and Gamma2 = 0, active closure failure iff Phi1 > 0 and Gamma2 > 0 '
                      '(first variant named ExactRepair in Rust, ExactClass in the node). The node statement defines R_cl only for Phi1 > 0; Rust returns Some(0) at Phi1 = 0, Gamma2 = 0. '
                      'The source operates on a bare Add type; here kappa is proved to exist iff d1 d0 = 0 over modules over a field. The ledger pin in dag/derivations/06_wdp/tfq_0344 is a CRLF-era hash: '
                      'the LF bytes in the tree hash differently (custody record in dag/pfp/filename_custody.json).'),
        predicates=['Phi1 from the dual LP (vertices of d0^T y = 0, |y_e| <= w_e), independent of the producer primal vertex enumeration over r = rank d0 zeroed residuals; plus exact verification of the carried primal potential x and dual vector y (cost(x) = y.h = Phi1, d0^T y = 0, |y_e| <= w_e).',
                    'Repair invariance in the certificate: windows with the same structure whose cochains differ by a coboundary carry equal Phi1, Gamma2, R_cl and class.',
                    'Ranks by fraction-free (Bareiss) elimination; d1 d0 expanded entrywise; dim H1 = m - rank d1 - rank d0 only when d1 d0 = 0.',
                    'Class by the source if-chain on (Phi1, Gamma2), NotAWindow exactly when d1 d0 != 0 (then Gamma2 is withheld); R_cl only when Phi1 > 0.',
                    'Theorem-level consistency: 0 <= Phi1 <= unrepaired residual sum; Phi1 = 0 implies Gamma2 = 0 on a complex; dim Q1 = dim H1 + rank d1.',
                    'Exact cross-language (Python/Rust) wire equality and literal Lean axiom reports.'],
        boundary=boundary, generators=generators, relations=relations, compositions=compositions, failed_compositions=failed, counterexamples=counterexamples,
        open_obligations=['Derivation of the window from Genesis admission (PG-GAP-GENESIS-TO-WINDOW).', 'Lean existence of the attained minimum (strong duality) for the weighted-L1 cost.',
                          'Norms other than weighted L1 and complex coefficients.'],
        colour_meanings={'Window': 'Graph window (nv, edges, weights, d1 rows, cochain h)', 'RepairQuotient': 'Q1 = C1 / im d0', 'ClosureCharge': 'd1 h in C2',
                         'Phi1': 'Exact rational quotient defect', 'Gamma2': 'Exact rational L1 norm of d1 h', 'DiagnosticClass': 'ExactClass | ClosedResidual | ActiveClosureFailure (NotAWindow marks a refusal)'},
        depends_on_result=False,
        challenge_plan='Coordinate mutants of every certificate leaf plus sixteen semantic near misses (kappa on a non-complex, closure ignored, closed read as exact, unrepaired sum as Phi1 and under a gauge shift, weights ignored or applied to Gamma2, H1 without quotient, dim Q1 swap, sign-ignored rank, ratio at Phi1 = 0, loop repaired, refusal hidden, representative Gamma2 for a non-window, non-optimal primal witness, dual vector beyond the weights) and one control.',
        composition_tree=['diagnostic_class(quotient_defect_phi1(q), closure_gamma2(kappa1(q)))'],
        construction='Exact table over 17 graph windows with primal and dual witnesses; Lean proves the module-level statements, the weak-duality certificate and the cost/IsPhi bridge.',
        relation_evidence={'kappa_descends_iff_complex': 'Kernel iff theorem plus two refused native windows.', 'diagnostic_trichotomy': 'Kernel partition theorem; native table has all three classes and a refusal.'})


if __name__ == '__main__':
    print(write_spec(HERE, NODE, spec()))
