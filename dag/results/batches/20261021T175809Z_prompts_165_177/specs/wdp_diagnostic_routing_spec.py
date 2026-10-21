"""Build specs/PG-WDP-DIAGNOSTIC-NOT-ROUTING.json from the producer and the node's reviewed claims."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = next((p for p in HERE.parents if (p / 'dag/pfp/prepare_stage.py').is_file()),
            Path(r'C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.claude\worktrees\unified-dag\.claude\worktrees\pfp-batch-01'))
sys.path.insert(0, str(ROOT / 'dag/pfp/batch_tools'))
from spec_builder import build_spec, write_spec  # noqa: E402

_s = importlib.util.spec_from_file_location('producer', ROOT / 'code/python/src/qm/pfp_wdp_diagnostic_routing.py')
producer = importlib.util.module_from_spec(_s)
_s.loader.exec_module(producer)

NODE = 'PG-WDP-DIAGNOSTIC-NOT-ROUTING'
ROUTING_LEAN = 'external WitnessedDifference/Routing.lean'
RS = 'external omega_types/src/routing.rs'
TS = 'external omega_types/src/terminal_status.rs'
H = ('Finite enumerations and total maps transcribed from the_symbol_game; the diagnostic class is ObstructionDiagnosticClass (the exact class is `ExactRepair` in Rust, `ExactClass` in the ledger); '
     'ResidualClass is NOT identified with the diagnostic class; the only diagnostic-to-terminal code is the partial run.rs tag plus terminal_routing.json.')


def spec():
    boundary = {
        'supports': ('Over finite enumerations transcribed BY HAND from the pinned sources (checked against routing.rs, terminal_status.rs, run.rs, checked_packet.rs and terminal_routing.json by a one-off regex and a unit test that re-reads the pinned Rust text when the checkout is present; '
                     'Lean, producer and checker share the transcription): (1) as abstract maps between a 3-set and a 7-set, the diagnostic class and the routing terminal give 21 cells, no value is forced, any two classes take any two terminals '
                     'independently (343 policies), injective policies exist (210) and none is surjective; the source declares a partial map for 2 of the 3 classes; (2) run.rs 626-633 emits a status-tag string per class; composing it by string identity with '
                     'the PfpTerminal-to-RoutingTerminal map (routing.rs, terminal_routing.json; no source code performs this composition) gives a partial route: ClosedResidual to RequiresLift, ActiveClosureFailure to Refusal, and the exact class, whose tag is the '
                     'Rust name ExactRepair, has none (2 of the 21 cells declared, 1 class unrouted, 19 cells neither realised nor excluded); (3) in the TerminalStatus tables the residual class does not determine the routing terminal and vice versa (8 of 28 cells realised), '
                     'all 7 terminals are reachable from the 21 statuses, the PfpTerminal map is not surjective (Repair and NoRule are missing, kernel routePfp_misses_repair_and_norule; its image has 5 values, native), and terminal_from_fiber reaches only 4 terminals '
                     '(general over all counts in Lean, 640 inputs natively); (4) in the model the Certified predicate and the routing terminal are functions of (status, witness) only (by construction of the model); the only source code taking a diagnostic class towards '
                     'authority (checked_packet.rs:248) is a necessary eligibility gate (only the exact class can seal a checked-packet certificate, which retains AuthorityEffect::None), never sufficient (kernel sealed_only_exact, sealed_needs_witness); the tag-level type '
                     'AuthTag has no Certified value, so tag-level never-certified is true by construction of the modelled type; (5) the external Routing.lean `route` is a separate four-valued axis with Bool inputs (re-transcribed copy).'),
        'does_not_support': ('That any policy from diagnostic classes to terminals is the correct one or is forced; WDP-CH04-O01, which stays conditional; any identification of terminal_status::ResidualClass (Exact, ClosedSurvivor, Open, Refused) with the diagnostic class '
                             '(the unrelated omega_homology ResidualClass with values ExactRepair, StabilizedSurvivor, OpenObstruction has the three values of the diagnostic class and is not modelled); that the Rust class name ExactRepair and the ledger name ExactClass denote '
                             'different things (the Lean exactRepairAllowed is the same predicate as certEligible, so the clause "ExactClass is not ExactRepair" has no anchor of its own); a route for the exact class (the source declares none); budget, rule or lift availability '
                             'as routing inputs (none exist in the source routing code); evidence about the source from the leaves that are definitional in the model (authority counts, AuthTag); any physical or interpretive claim.'),
        'narrowest_claim': ('Over hand-transcribed source tables, the diagnostic class, routing terminal, residual class and authority tag are different finite axes and nothing forces the partial class-to-terminal composite the source declares (the exact class is unrouted); '
                            'a diagnostic value is at most a necessary eligibility gate for sealing a certificate, never authority. The source code itself names the exact class ExactRepair and tags ClosedResidual as StabilizedSurvivor, contrary to ledger N01.'),
        'next_test': ('Enumerate the 7 total extensions of the declared partial policy (the 7 choices of terminal for ExactClass) and decide for each whether it is compatible with (a) certificate eligibility being exact-class-only, (b) the 4-element image of terminal_from_fiber, '
                      '(c) Certified requiring an authority-bearing terminal; then state the surviving extension(s) as the policy O01 must declare.')}
    generators = [
        {'id': 'diagnostic_class', 'source_declarations': ['external omega_policy/src/trichotomy.rs::ObstructionDiagnosticClass (line 17): exact class named ExactRepair in Rust; classify_exact (line 65)'],
         'ordered_inputs': ['ExactPhi1Gamma2Evidence'], 'output': 'DiagClass',
         'semantic_predicate': 'SOURCE-ONLY (not recomputed here): ExactClass iff Phi1 = 0, ClosedResidual iff Phi1 > 0 and Gamma2 = 0, ActiveClosureFailure iff Gamma2 > 0.', 'hypotheses': [H]},
        {'id': 'routing_of_status', 'source_declarations': [RS + '::RoutingTerminal (line 15), From<TerminalStatus> (line 25): total map, 21 to 7'],
         'ordered_inputs': ['TerminalStatus'], 'output': 'RoutingTerminal',
         'semantic_predicate': 'The declared total map from the 21 statuses to the seven routing terminals.', 'hypotheses': [H]},
        {'id': 'routing_of_pfp_terminal', 'source_declarations': [RS + '::PfpTerminal (line 59), From<PfpTerminal> (line 87): total map, 10 to 7, equal to terminal_routing.json'],
         'ordered_inputs': ['PfpTerminal'], 'output': 'RoutingTerminal',
         'semantic_predicate': 'The declared total map from the 10 PfpTerminal values to the routing terminals; not surjective (Repair, NoRule missing).', 'hypotheses': [H]},
        {'id': 'terminal_from_fiber', 'source_declarations': [TS + '::terminal_from_fiber (line 166): total function with Err on inconsistent counts'],
         'ordered_inputs': ['FiberInput'], 'output': 'TerminalStatus',
         'semantic_predicate': 'Classifier of a candidate fiber; PARTIAL as modelled (an Err has no status); the diagnostic class is not an input.', 'hypotheses': [H]},
        {'id': 'residual_of_status', 'source_declarations': [TS + '::residual_class (line 119)'],
         'ordered_inputs': ['TerminalStatus'], 'output': 'ResidualClass',
         'semantic_predicate': 'Residual class Exact, ClosedSurvivor, Open or Refused (terminal_status::ResidualClass, not the homology enum of the same name).', 'hypotheses': [H]},
        {'id': 'authority_tag_of_status', 'source_declarations': [TS + '::authority_level (line 92), authority_terminal (line 157); test authority_level_never_returns_certified_from_tag_alone (line 322)'],
         'ordered_inputs': ['TerminalStatus'], 'output': 'AuthorityTag',
         'semantic_predicate': 'Tag-level authority Certifiable / Refused / Uncertified; the modelled type has no Certified value (by construction).', 'hypotheses': [H]},
        {'id': 'diagnostic_run_tag', 'source_declarations': ['external omega_id_run/src/run.rs lines 626-633: ExactRepair -> "ExactRepair", ClosedResidual -> "StabilizedSurvivor", ActiveClosureFailure -> "OpenObstruction" (a String)'],
         'ordered_inputs': ['DiagClass'], 'output': 'PfpTerminal',
         'semantic_predicate': 'Status-tag string per class read as a PfpTerminal by string identity (OUR identification; partial: "ExactRepair" is not a PfpTerminal).', 'hypotheses': [H]},
        {'id': 'certificate_seal_gate', 'source_declarations': ['external omega_certifiers/src/checked_packet.rs line 243-250: ExactRepair -> AuthorityTerminal::ExactRuleDerived, other classes -> NotAuthorityBearing error; witness bound to the replay hash also required'],
         'ordered_inputs': ['DiagClass'], 'output': 'EligibilityFlag',
         'semantic_predicate': 'Only the exact class can seal a checked-packet certificate (necessary, not sufficient; the certificate retains AuthorityEffect::None).', 'hypotheses': [H]},
        {'id': 'relative_status_route', 'source_declarations': [ROUTING_LEAN + '::RelativeStatus (line 12), route (line 19): four-valued, Bool inputs inProfile/contradicted/supported; re-transcribed copy'],
         'ordered_inputs': ['BoolTriple'], 'output': 'RelativeStatus',
         'semantic_predicate': 'A different axis: outside the profile is not refuted.', 'hypotheses': [H]}]
    relations = [
        {'id': 'policy_independence', 'source_declarations': ['no source declaration; new finite-type theorem about all maps DiagClass -> RoutingTerminal'],
         'equation_or_predicate': 'for classes d1 != d2 and terminals r1, r2 there is a policy with p d1 = r1 and p d2 = r2; no value forced; 343 policies, 210 injective, none surjective', 'typing_conditions': 'Finite types of sizes 3 and 7',
         'evidence_status': 'Kernel theorems policy_values_independent, no_value_forced, card_policies, no_surjective_policy, no_injective_from_routing, card_injective_policies; native enumeration of all 343', 'scope': 'Exact for these two finite types'},
        {'id': 'declared_policy_is_partial', 'source_declarations': ['external omega_id_run/src/run.rs lines 626-633 and omega_engine_pfp terminal_routing.json: ExactRepair tag has no key; no code composes the two'],
         'equation_or_predicate': 'our string-identity composite route: ClosedResidual to RequiresLift, ActiveClosureFailure to Refusal, ExactClass undefined', 'typing_conditions': 'DiagClass',
         'evidence_status': 'Kernel theorems diagRoute_values, diagRoute_injective_where_defined; native diag rows and diag_cells summary', 'scope': 'The transcribed source only'},
        {'id': 'status_tables_non_determination', 'source_declarations': [RS + ' (From<TerminalStatus>) and ' + TS + ' (residual_class, authority_level)'],
         'equation_or_predicate': 'residual does not determine route, route does not determine residual, authority tag does not determine route, but route determines the authority tag', 'typing_conditions': '21 statuses',
         'evidence_status': 'Kernel theorems residual_not_determine_route, route_not_determine_residual, auth_not_determine_route, authTag_factors_through_route; native determination matrix', 'scope': 'The 21 statuses'},
        {'id': 'image_sizes', 'source_declarations': [RS + ' From<PfpTerminal> equals terminal_routing.json (read, not parsed at run time)'],
         'equation_or_predicate': 'routing image of statuses is all 7, of PfpTerminal is 5 (no Repair, no NoRule), of terminal_from_fiber is 4 (no RequiresLift, BudgetUnknown, Refused)', 'typing_conditions': 'Finite',
         'evidence_status': 'Kernel theorems routeStatus_surjective, routePfp_not_surjective, routePfp_misses_repair_and_norule, fiber_route_in, fiber_never_lift_budget_refused (general over all counts), fiber_reaches_four; native 640-input enumeration', 'scope': 'General over counts for the fiber classifier'},
        {'id': 'authority_not_from_diagnostic', 'source_declarations': [TS + ' test authority_level_never_returns_certified_from_tag_alone (line 322); external checked_packet.rs lines 243-250'],
         'equation_or_predicate': 'certified s w = w and s authority-bearing (diagnostic absent by construction); sealed d w = w and d exact; tag type has no Certified value (by construction); ExactClass is eligible but not authority without witness', 'typing_conditions': 'TerminalStatus x Bool',
         'evidence_status': 'Kernel theorems certified_needs_witness, certified_only_for_authority_terminals, sealed_only_exact, sealed_needs_witness, sealed_exact_with_witness, exactClass_not_authority, certEligible_iff; diag_cannot_set_* hold by construction of the Situation model (rfl); the native authority leaves are computed from the modelled definition and are not evidence about the source function', 'scope': 'The class is a necessary eligibility gate (checked_packet.rs:248), never sufficient; independence from diag elsewhere is by construction of the model'},
        {'id': 'relative_status_separation', 'source_declarations': [ROUTING_LEAN + '::outside_profile_ne_refuted (line 26), route_outside_profile, refuted_route_requires_profile: general over Bool inputs; re-transcribed here as copies, not the external theorems'],
         'equation_or_predicate': 'outsideProfile != refuted; route false _ _ = outsideProfile; refuted implies inProfile', 'typing_conditions': 'Bool inputs',
         'evidence_status': 'Kernel theorems outside_profile_ne_refuted, relRoute_outside, refuted_requires_profile, relRoute_surjective; native 8 rows', 'scope': 'All Bool inputs (8 cases)'}]
    compositions = [
        {'outer_operation': 'routing_of_status', 'input_slot': 0, 'inner_operation': 'terminal_from_fiber', 'colour_match': 'TerminalStatus',
         'hypothesis_match': 'Err inputs (inconsistent counts) have no status and hence no route (partial composite).', 'licensing_relations': ['image_sizes'], 'evidence_status': 'Kernel and native'},
        {'outer_operation': 'routing_of_pfp_terminal', 'input_slot': 0, 'inner_operation': 'diagnostic_run_tag', 'colour_match': 'PfpTerminal',
         'hypothesis_match': 'Defined only when the tag is a PfpTerminal key; the exact class tag ExactRepair is not. No source code performs this composition.', 'licensing_relations': ['declared_policy_is_partial'], 'evidence_status': 'Kernel and native (partial composite by string identity)'},
        {'outer_operation': 'residual_of_status', 'input_slot': 0, 'inner_operation': 'terminal_from_fiber', 'colour_match': 'TerminalStatus',
         'hypothesis_match': H, 'licensing_relations': ['status_tables_non_determination'], 'evidence_status': 'Kernel and native'},
        {'outer_operation': 'authority_tag_of_status', 'input_slot': 0, 'inner_operation': 'terminal_from_fiber', 'colour_match': 'TerminalStatus',
         'hypothesis_match': H, 'licensing_relations': ['authority_not_from_diagnostic'], 'evidence_status': 'Kernel and native'}]
    failed = [
        {'composition': 'routing_of_pfp_terminal(diagnostic_run_tag(ExactClass))', 'reason': 'Fails: the tag "ExactRepair" is not a PfpTerminal, so terminal_routing.json gives the exact class no route; reading it as CheckPassed is a modelling choice not made here.'},
        {'composition': 'residual_class read as the diagnostic class', 'reason': 'ResidualClass has a fourth value Refused and Open covers statuses with no diagnostic at all (NoPacket, VerifierDisabled), so it is not the 3-valued diagnostic class.'},
        {'composition': 'certificate_eligibility as authority', 'reason': 'Eligibility is necessary only: certified needs a descent witness and an authority-bearing terminal, neither supplied by the class.'},
        {'composition': 'terminal_from_fiber into RequiresLift, BudgetUnknown or Refused', 'reason': 'None of the 640 inputs (and no input over any counts, by the kernel theorem) yields these three terminals.'}]
    counterexamples = [
        {'id': 'open_residual_four_routes', 'statement': 'The Open residual class routes to Repair, BudgetUnknown, RequiresLift and Refusal, so the residual class does not determine the terminal.', 'scope': 'Source tables for the 21 statuses'},
        {'id': 'refusal_two_residuals', 'statement': 'Refusal comes from ParseRefused (residual Refused) and NoPacket (residual Open), so the terminal does not determine the residual class.', 'scope': 'Source tables for the 21 statuses'},
        {'id': 'closed_class_two_routes', 'statement': 'If ClosedResidual is identified with ResidualClass.ClosedSurvivor (not asserted), run.rs routes it to RequiresLift while the TerminalStatus table routes ClosedSurvivor to NoRule: the two source tables disagree.', 'scope': 'Source reading under an explicit identification'}]
    return build_spec(
        node=NODE, short='wdp_diagnostic_routing', lean='WdpDiagnosticRouting',
        anchors=['WdpDiagnosticRouting.card_axes', 'WdpDiagnosticRouting.policy_values_independent', 'WdpDiagnosticRouting.no_value_forced',
                 'WdpDiagnosticRouting.card_policies', 'WdpDiagnosticRouting.no_surjective_policy', 'WdpDiagnosticRouting.no_injective_from_routing',
                 'WdpDiagnosticRouting.card_injective_policies', 'WdpDiagnosticRouting.diagRoute_values', 'WdpDiagnosticRouting.diagRoute_injective_where_defined',
                 'WdpDiagnosticRouting.routeStatus_surjective', 'WdpDiagnosticRouting.routePfp_not_surjective', 'WdpDiagnosticRouting.routePfp_misses_repair_and_norule', 'WdpDiagnosticRouting.residual_not_determine_route',
                 'WdpDiagnosticRouting.route_not_determine_residual', 'WdpDiagnosticRouting.auth_not_determine_route', 'WdpDiagnosticRouting.authTag_factors_through_route',
                 'WdpDiagnosticRouting.certified_needs_witness', 'WdpDiagnosticRouting.certified_only_for_authority_terminals', 'WdpDiagnosticRouting.diag_cannot_set_authority',
                 'WdpDiagnosticRouting.diag_cannot_set_terminal', 'WdpDiagnosticRouting.exactClass_not_authority', 'WdpDiagnosticRouting.certEligible_iff',
                 'WdpDiagnosticRouting.sealed_only_exact', 'WdpDiagnosticRouting.sealed_needs_witness', 'WdpDiagnosticRouting.sealed_exact_with_witness',
                 'WdpDiagnosticRouting.closed_tension', 'WdpDiagnosticRouting.fiber_route_in', 'WdpDiagnosticRouting.fiber_never_lift_budget_refused',
                 'WdpDiagnosticRouting.fiber_reaches_four', 'WdpDiagnosticRouting.outside_profile_ne_refuted', 'WdpDiagnosticRouting.relRoute_outside',
                 'WdpDiagnosticRouting.refuted_requires_profile', 'WdpDiagnosticRouting.relRoute_surjective'],
        cases=list(producer.CASES), public_tsv=producer.public_tsv(), data=producer.certificate(),
        scope_review=('The operad candidates `route` and `RelativeStatus` (external Routing.lean) are NOT the seven-valued routing terminal: they are a four-valued relative status with three Bool inputs; the real terminals are in omega_types routing.rs. '
                      'The diagnostic class lives in omega_policy trichotomy.rs, where its exact class is named ExactRepair (the ledger says ExactClass and states that ExactClass is not ExactRepair). The only class-to-status code (run.rs 626-633) maps '
                      'ClosedResidual to the tag StabilizedSurvivor although N01 says ClosedResidual is not StabilizedSurvivor, and the exact class to a tag that has no routing entry. The attached local witness '
                      'pg_to_sn_and_wdp_route_chain_composition is a conjunction of fixed small-number facts unrelated to routing. fda.rs GuardEvidence and ceiling.rs EvidenceCeiling are further separate axes (guards, capability chain) that '
                      'are read but not tabulated. All tables were transcribed by hand and cross-checked against the Rust sources by regex at authoring time (a unit test repeats this when the pinned checkout is present); the checker uses a separate grouped transcription but the transcription risk is shared. Source sha256 (the_symbol_game): omega_types/src/routing.rs 7dd9a3b1815434eb384c3a7837de2b16c6b560570f3b287ffb25439b987d596c; omega_types/src/terminal_status.rs fa4b67c847ea16cb8a3289ce3e18195f83175996a9d597158347db9fa0568160; omega_policy/src/trichotomy.rs 68cd397e43237e2ec7019907278849d54c56fc2b23efc7f8d28480d8d9898a5e; omega_id_run/src/run.rs cb4cf5ad9d464da7503200f80cf3e126c7f46483b395a5e5531702c1d1b80a74; omega_certifiers/src/checked_packet.rs 9e70b20ceb8c7b78b2997febaf715ea62b9d179ab5d184d09cf42723d834541e; omega_engine_pfp/infrastructure/yaml/stages/terminal_routing.json 18c4da98ec31e88e955f1d5f6a9184c06300fd66ec2ada35b9496c4c882f4df3; WitnessedDifference/Routing.lean cd9087a9ef86a63ad055c7be4310ef2fbdba6f3470243cf6e16161f8bfc35e13. No source code composes run.rs with terminal_routing.json (omega_id_run never references PfpTerminal): the composite is ours. Two Rust enums are named ResidualClass; only terminal_status::ResidualClass is modelled. No budget, rule-availability or lift-availability input exists in the source routing code, '
                      'so none is invented; all 343 abstract policies are enumerated instead.'),
        predicates=['Independent recomputation of every table row and summary from a separate grouped transcription of the source maps.',
                    'Fiber classifier rebuilt as valid-count test plus case split (producer uses early returns); all 640 inputs.',
                    'All 343 abstract policies enumerated: injective, surjective and per-pair value counts; determination matrix decided on fibres.',
                    'Theorem-level consistency: the exact class has route "-" (no declared route) and no status counts as certified without a witness.',
                    'Exact cross-language (Python/Rust) wire equality and literal Lean axiom reports.'],
        boundary=boundary, generators=generators, relations=relations, compositions=compositions, failed_compositions=failed, counterexamples=counterexamples,
        open_obligations=['WDP-CH04-O01 stays conditional on a declared terminal, lift and guarded-change policy.',
                          'No source route for the exact diagnostic class (the tag ExactRepair is not a PfpTerminal) and no source code composing the run.rs tag with terminal_routing.json.',
                          'Reconcile run.rs ClosedResidual -> StabilizedSurvivor with N01 "ClosedResidual is not StabilizedSurvivor".',
                          'fda.rs GuardEvidence and ceiling.rs EvidenceCeiling are not tabulated as axes.'],
        colour_meanings={'DiagClass': 'ExactClass / ClosedResidual / ActiveClosureFailure', 'RoutingTerminal': 'The seven routing terminals',
                         'TerminalStatus': 'The 21 TerminalStatus values', 'StatusTag': 'Status string emitted by run.rs', 'FiberInput': 'Arguments of terminal_from_fiber', 
                         'EligibilityFlag': 'Certificate eligibility', 'RelativeStatus': 'supported / refuted / outsideProfile / undetermined',
                         'ExactPhi1Gamma2Evidence': 'Exact Phi1 and Gamma2 values on the same residual', 'PfpTerminal': 'One of the 10 PfpTerminal values (tag read by string identity)',
                         'ResidualClass': 'terminal_status::ResidualClass', 'AuthorityTag': 'Certifiable / Refused / Uncertified', 'BoolTriple': 'Three Boolean inputs'},
        depends_on_result=True,
        qualification=('Over transcribed source tables the diagnostic class (3 values), routing terminal (7), residual class (4) and tag-level authority (3) are distinct finite types and nothing forces a map from the class to the terminal; '
                       'the source declares only a partial class-to-terminal composite (ExactClass unrouted; ClosedResidual tagged StabilizedSurvivor, which ledger N01 forbids; the Rust exact class is named ExactRepair), '
                       'tag-level authority is a function of the routing terminal, and a diagnostic value or certificate is not authority (the class is at most a necessary eligibility gate, checked_packet.rs:248).'),
        challenge_plan='Coordinate mutants of every record leaf plus fifteen semantic near misses: exact class routed, closed class borrowing the residual route, certification without witness, a unique policy, PfpTerminal surjective, fiber reaching RequiresLift, route determining residual, outside profile read as refuted, a surjective policy, no-rule certifiable, the tag ExactRepair identified with PfpTerminal::Exact, ClosedResidual certificate-eligible, residual determining route, exact class counted as routed, ParseRefused mistranscribed.',
        composition_tree=['routing_of_status(terminal_from_fiber(input)) (partial: Err)', 'routing_of_pfp_terminal(diagnostic_run_tag(class)) (partial, string identity)', 'residual_of_status(terminal_from_fiber(input))', 'authority_tag_of_status(terminal_from_fiber(input))'],
        construction='Exhaustive tables: 21 statuses, 10 PFP terminals, 3 classes, 8 relative-status inputs, 640 fiber inputs and 8 summaries (343 policies); Lean proves the finite-type statements and the general fiber-image theorem.',
        relation_evidence={'policy_independence': 'Kernel and native enumeration of all 343 policies.', 'declared_policy_is_partial': 'Source reading of run.rs lines 626-633 plus terminal_routing.json keys; kernel and native tables.',
                           'authority_not_from_diagnostic': 'Structural: the class is not an argument of certification; kernel theorems and native authority summary.'})


if __name__ == '__main__':
    print(write_spec(HERE, NODE, spec()))
