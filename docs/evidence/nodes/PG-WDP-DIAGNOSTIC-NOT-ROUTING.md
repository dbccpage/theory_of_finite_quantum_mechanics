# PG-WDP-DIAGNOSTIC-NOT-ROUTING

Stage: [WDP](../stages/WDP.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Diagnostic class (ExactClass, ClosedResidual, ActiveClosureFailure) is a different axis from routing terminal (CheckPassed, RequiresLift, Repair, Refusal, NoRule, BudgetUnknown, Refused) and from authority; ExactClass is not ExactRepair, and a diagnostic value or certificate is not authority.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 35
- distinct cited Lean declarations covered by a current replay receipt: 35
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test)

## Flags

- `receipt_names_uncited_module`: a replay receipt names this node for lean4/WdpDiagnosticRouting.lean, but the node's lean, rust and source fields do not cite it. A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence).

## Imported structure

None recorded.

## Bottleneck

Separation is a definitional discipline that the source code does not follow at the tag level (run.rs 626-633; the Rust exact class is named ExactRepair; omega_mub maps the class to a CodaTerminal); WDP-CH04-O01 (diagnostics feed checked finite routing receipts under a declared terminal, lift and guarded-change policy) is CONDITIONAL and only partially ported.

## Source status

WDP-CH04-N01 NONCLAIM; GTLA rules 4 and 6

## Review

- PFP review: [dag/results/PG-WDP-DIAGNOSTIC-NOT-ROUTING/reviews/20261021_batch01b_audit/delivery_review_result.json](../../../dag/results/PG-WDP-DIAGNOSTIC-NOT-ROUTING/reviews/20261021_batch01b_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `caveat_added`; prior status `DEFINITION`; qualifies for E4: yes.
  - narrowest claim: Over hand-transcribed source tables, the diagnostic class, routing terminal, residual class and authority tag are different finite axes and nothing forces the partial class-to-terminal composite the source declares (the exact class is unrouted); a diagnostic value is at most a necessary eligibility gate for sealing a certificate, never authority. The source code itself names the exact class ExactRepair and tags ClosedResidual as StabilizedSurvivor, contrary to ledger N01.
  - does not support: That any policy from diagnostic classes to terminals is the correct one or is forced; WDP-CH04-O01, which stays conditional; any identification of terminal_status::ResidualClass (Exact, ClosedSurvivor, Open, Refused) with the diagnostic class (the unrelated omega_homology ResidualClass with values ExactRepair, StabilizedSurvivor, OpenObstruction has the three values of the diagnostic class and is not modelled); that the Rust class name ExactRepair and the ledger name ExactClass denote different things (the Lean exactRepairAllowed is the same predicate as certEligible, so the clause "ExactClass is not ExactRepair" has no anchor of its own); a route for the exact class (the source declares none); budget, rule or lift availability as routing inputs (none exist in the source routing code); evidence about the source from the leaves that are definitional in the model (authority counts, AuthTag); any physical or interpretive claim.
  - next test: Enumerate the 7 total extensions of the declared partial policy (the 7 choices of terminal for ExactClass) and decide for each whether it is compatible with (a) certificate eligibility being exact-class-only, (b) the 4-element image of terminal_from_fiber, (c) Certified requiring an authority-bearing terminal; then state the surviving extension(s) as the policy O01 must declare.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/Routing.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/Routing.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Routing.lean)
- sha256 (`bytes`): `4fa11b70e328f2c42e32c89548b8970033b8f2da996181f2526febe6dcfca324`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_wdp.json](../../../dag/research/lean_replay_campaign_wdp.json) (module `Imported.WitnessedDifference.WitnessedDifference.Routing`): recorded sha256 `4fa11b70e328f2c42e32c89548b8970033b8f2da996181f2526febe6dcfca324` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/Routing.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `outside_profile_ne_refuted` | yes | yes | yes | none | `#print axioms outside_profile_ne_refuted` |
| `route` | yes | yes | yes | none | `#print axioms route` |

- counts toward the grade: yes

### Lean: `lean4/WdpDiagnosticRouting.lean`

- file: [lean4/WdpDiagnosticRouting.lean](../../../lean4/WdpDiagnosticRouting.lean)
- sha256 (`bytes`): `36530ac192efceb10c24eb272573d98f8852d40e63d888897c24523fd75ecdf0`
- cited in: receipt dag/research/pfp_batch01_lean_replay.json (WdpDiagnosticRouting)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `WdpDiagnosticRouting`): recorded sha256 `36530ac192efceb10c24eb272573d98f8852d40e63d888897c24523fd75ecdf0` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build WdpDiagnosticRouting`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WdpDiagnosticRouting.authTag_factors_through_route` | yes | yes | yes | propext | `#print axioms WdpDiagnosticRouting.authTag_factors_through_route` |
| `WdpDiagnosticRouting.auth_not_determine_route` | yes | yes | yes | propext | `#print axioms WdpDiagnosticRouting.auth_not_determine_route` |
| `WdpDiagnosticRouting.card_axes` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpDiagnosticRouting.card_axes` |
| `WdpDiagnosticRouting.card_injective_policies` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpDiagnosticRouting.card_injective_policies` |
| `WdpDiagnosticRouting.card_policies` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpDiagnosticRouting.card_policies` |
| `WdpDiagnosticRouting.certEligible_iff` | yes | yes | yes | propext | `#print axioms WdpDiagnosticRouting.certEligible_iff` |
| `WdpDiagnosticRouting.certified_needs_witness` | yes | yes | yes | propext | `#print axioms WdpDiagnosticRouting.certified_needs_witness` |
| `WdpDiagnosticRouting.certified_only_for_authority_terminals` | yes | yes | yes | propext | `#print axioms WdpDiagnosticRouting.certified_only_for_authority_terminals` |
| `WdpDiagnosticRouting.closed_tension` | yes | yes | yes | propext | `#print axioms WdpDiagnosticRouting.closed_tension` |
| `WdpDiagnosticRouting.diagRoute_injective_where_defined` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpDiagnosticRouting.diagRoute_injective_where_defined` |
| `WdpDiagnosticRouting.diagRoute_values` | yes | yes | yes | none | `#print axioms WdpDiagnosticRouting.diagRoute_values` |
| `WdpDiagnosticRouting.diag_cannot_set_authority` | yes | yes | yes | propext | `#print axioms WdpDiagnosticRouting.diag_cannot_set_authority` |
| `WdpDiagnosticRouting.diag_cannot_set_terminal` | yes | yes | yes | none | `#print axioms WdpDiagnosticRouting.diag_cannot_set_terminal` |
| `WdpDiagnosticRouting.exactClass_not_authority` | yes | yes | yes | propext | `#print axioms WdpDiagnosticRouting.exactClass_not_authority` |
| `WdpDiagnosticRouting.fiber_never_lift_budget_refused` | yes | yes | yes | propext | `#print axioms WdpDiagnosticRouting.fiber_never_lift_budget_refused` |
| `WdpDiagnosticRouting.fiber_reaches_four` | yes | yes | yes | none | `#print axioms WdpDiagnosticRouting.fiber_reaches_four` |
| `WdpDiagnosticRouting.fiber_route_in` | yes | yes | yes | propext | `#print axioms WdpDiagnosticRouting.fiber_route_in` |
| `WdpDiagnosticRouting.no_injective_from_routing` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpDiagnosticRouting.no_injective_from_routing` |
| `WdpDiagnosticRouting.no_surjective_policy` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpDiagnosticRouting.no_surjective_policy` |
| `WdpDiagnosticRouting.no_value_forced` | yes | yes | yes | propext | `#print axioms WdpDiagnosticRouting.no_value_forced` |
| `WdpDiagnosticRouting.outside_profile_ne_refuted` | yes | yes | yes | none | `#print axioms WdpDiagnosticRouting.outside_profile_ne_refuted` |
| `WdpDiagnosticRouting.policy_values_independent` | yes | yes | yes | propext | `#print axioms WdpDiagnosticRouting.policy_values_independent` |
| `WdpDiagnosticRouting.refuted_requires_profile` | yes | yes | yes | propext | `#print axioms WdpDiagnosticRouting.refuted_requires_profile` |
| `WdpDiagnosticRouting.relRoute_outside` | yes | yes | yes | none | `#print axioms WdpDiagnosticRouting.relRoute_outside` |
| `WdpDiagnosticRouting.relRoute_surjective` | yes | yes | yes | none | `#print axioms WdpDiagnosticRouting.relRoute_surjective` |
| `WdpDiagnosticRouting.residual_not_determine_route` | yes | yes | yes | propext | `#print axioms WdpDiagnosticRouting.residual_not_determine_route` |
| `WdpDiagnosticRouting.routePfp_misses_repair_and_norule` | yes | yes | yes | propext | `#print axioms WdpDiagnosticRouting.routePfp_misses_repair_and_norule` |
| `WdpDiagnosticRouting.routePfp_not_surjective` | yes | yes | yes | propext | `#print axioms WdpDiagnosticRouting.routePfp_not_surjective` |
| `WdpDiagnosticRouting.routeStatus_surjective` | yes | yes | yes | none | `#print axioms WdpDiagnosticRouting.routeStatus_surjective` |
| `WdpDiagnosticRouting.route_not_determine_residual` | yes | yes | yes | propext | `#print axioms WdpDiagnosticRouting.route_not_determine_residual` |
| `WdpDiagnosticRouting.sealed_exact_with_witness` | yes | yes | yes | propext | `#print axioms WdpDiagnosticRouting.sealed_exact_with_witness` |
| `WdpDiagnosticRouting.sealed_needs_witness` | yes | yes | yes | propext | `#print axioms WdpDiagnosticRouting.sealed_needs_witness` |
| `WdpDiagnosticRouting.sealed_only_exact` | yes | yes | yes | propext | `#print axioms WdpDiagnosticRouting.sealed_only_exact` |

- counts toward the grade: yes

### Rust: `code/rust/src/wdp/authority_gap.rs`

- file: [code/rust/src/wdp/authority_gap.rs](../../../code/rust/src/wdp/authority_gap.rs)
- sha256 (`bytes`): `0868299c878fb62cb4b194ba0f63b96aae2c2c39de916fb698aa252cc4a5399c`
- cited in: record TFQ-0347
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/wdp_kernel_check.rs`

- file: [code/rust/src/wdp/wdp_kernel_check.rs](../../../code/rust/src/wdp/wdp_kernel_check.rs)
- sha256 (`bytes`): `ed19fff6227820f276fbe81f21c2338bccb3337e7ef165188a99923ae59b94ec`
- cited in: record TFQ-0347
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: yes

### Documents and data: `.claude/rules/authority/rl_gtla_rules_rubric.md`

- file: `.claude/rules/authority/rl_gtla_rules_rubric.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md)
- sha256 (`lf-normalised`): `1596c27b09af32aec26710dacafcbe1dcb5081bc06d35d094b4c0b0353932e64`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0347_keep_exactclass_closedresidual_and_activeclosurefailure_off_the_routing_terminal_and_leave.md`

- file: [dag/derivations/06_wdp/tfq_0347_keep_exactclass_closedresidual_and_activeclosurefailure_off_the_routing_terminal_and_leave.md](../../../dag/derivations/06_wdp/tfq_0347_keep_exactclass_closedresidual_and_activeclosurefailure_off_the_routing_terminal_and_leave.md)
- sha256 (`lf-normalised`): `d42abe6dda763f08a747bf1dc9bf835c2f28adecbe61cdf9e37dbad8e8255b1a`
- generated view: listed, not counted
- cited in: record TFQ-0347
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:37446bd8af70040d3412b4895efe73f28dc7662ab259bc00986debcc8660c765::RoutingTerminal`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche14_cross_stage_route_composition_and_sorkin_hierarchy_witness`
- `external:sha256:bcb9825eb7031147a89239c7c5c90a65f7eb70bd996338ebbd0f1900316af187::EvidenceCeiling`
- `external:sha256:d5bfe8d13dd272a247b6448dc6597b2683283e7245db0441e35009cd59637324::GuardEvidence`

## Routes

Incoming (1):

- `PG-R-DIAG-NOT-ROUTING` `CONDITIONAL_ON_IMPORT`: [PG-WDP-QUOTIENT-EXACT-SEQUENCE](PG-WDP-QUOTIENT-EXACT-SEQUENCE.md) (PROVED_LEAN)

Outgoing (0):

