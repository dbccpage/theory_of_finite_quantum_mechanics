# FSP-DISCRETE-WDW-CONSTRAINT

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claimed: a discrete Wheeler-DeWitt operator H_perp on spatial triangulations is nonnegative and acts as a projection on diffeomorphism-invariant states; no such operator is constructed here, and the DeWitt supermetric of the continuum constraint is indefinite.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 10
- cited Lean declarations covered by a current replay receipt: 10
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Narrowed algebraic checks only. Rational residuals obey elementary norm bounds, and a zero-edge/sign-vertex witness has the displayed norm bound and objective equality. No incidence operator, transpose annihilation proposition, optimizer API, or general strong-duality theorem is constructed. A rank-one quadratic form, two supplied 2x2 projectors and a swap constraint have the stated identities. The thermal values 8 and 5 are second-order polynomial traces, not Gibbs exponential traces. The indefinite rational two-variable form is supplied and not derived from continuum DeWitt geometry; no physical Wheeler-DeWitt projector or fermion-sign mechanism follows. Status is unchanged. The original physical or operational bridge remains open.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-049 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignFspDiscreteWdwConstraint.lean`

- file: [lean4/CampaignFspDiscreteWdwConstraint.lean](../../../lean4/CampaignFspDiscreteWdwConstraint.lean)
- sha256 (`bytes`): `b9c0facb18d974145f514cc8e47133efd525444aee3830a67cedd19b989644e3`
- cited in: node.lean, record TFQ-1213
- replay: `verified`
  - receipt [dag/research/campaign_fsp-discrete-wdw-constraint_lean_replay.json](../../../dag/research/campaign_fsp-discrete-wdw-constraint_lean_replay.json) (module `CampaignFspDiscreteWdwConstraint`): recorded sha256 `b9c0facb18d974145f514cc8e47133efd525444aee3830a67cedd19b989644e3` matches the current file; exit code 0; Lean None; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignFspDiscreteWdwConstraint`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignFspDiscreteWdwConstraint.dJoint_linear_and_constant_kernel` | yes | yes | yes | module-level | `#print axioms CampaignFspDiscreteWdwConstraint.dJoint_linear_and_constant_kernel` |
| `CampaignFspDiscreteWdwConstraint.dewitt_supermetric_indefinite_signature_fence` | yes | yes | yes | module-level | `#print axioms CampaignFspDiscreteWdwConstraint.dewitt_supermetric_indefinite_signature_fence` |
| `CampaignFspDiscreteWdwConstraint.diffeomorphism_averaging_projector_and_constraint_complement` | yes | yes | yes | module-level | `#print axioms CampaignFspDiscreteWdwConstraint.diffeomorphism_averaging_projector_and_constraint_complement` |
| `CampaignFspDiscreteWdwConstraint.page_wootters_clock_system_conditioned_evolution` | yes | yes | yes | module-level | `#print axioms CampaignFspDiscreteWdwConstraint.page_wootters_clock_system_conditioned_evolution` |
| `CampaignFspDiscreteWdwConstraint.primal_l1_edge_and_vertex_residual_lower_bound` | yes | yes | yes | module-level | `#print axioms CampaignFspDiscreteWdwConstraint.primal_l1_edge_and_vertex_residual_lower_bound` |
| `CampaignFspDiscreteWdwConstraint.quadratic_constraint_psd_and_null_kernel_iff` | yes | yes | yes | module-level | `#print axioms CampaignFspDiscreteWdwConstraint.quadratic_constraint_psd_and_null_kernel_iff` |
| `CampaignFspDiscreteWdwConstraint.s4_seed_flat_vs_curved_wdw_defect_mass` | yes | yes | yes | module-level | `#print axioms CampaignFspDiscreteWdwConstraint.s4_seed_flat_vs_curved_wdw_defect_mass` |
| `CampaignFspDiscreteWdwConstraint.strong_duality_direct_sum_wdw_exact_coboundary` | yes | yes | yes | module-level | `#print axioms CampaignFspDiscreteWdwConstraint.strong_duality_direct_sum_wdw_exact_coboundary` |
| `CampaignFspDiscreteWdwConstraint.wdw_constraint_kernel_vs_thermal_gibbs_trace_fence` | yes | yes | yes | module-level | `#print axioms CampaignFspDiscreteWdwConstraint.wdw_constraint_kernel_vs_thermal_gibbs_trace_fence` |
| `CampaignFspDiscreteWdwConstraint.wdw_constraint_projection_preserves_fermion_sign_cancellation_fence` | yes | yes | yes | module-level | `#print axioms CampaignFspDiscreteWdwConstraint.wdw_constraint_projection_preserves_fermion_sign_cancellation_fence` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1213_fsp_discrete_wdw_constraint.md`

- file: [dag/derivations/26_fsp/tfq_1213_fsp_discrete_wdw_constraint.md](../../../dag/derivations/26_fsp/tfq_1213_fsp_discrete_wdw_constraint.md)
- sha256 (`lf-normalised`): `a00bd0f58128a75d088309c64a548d890f388d49e955cbe067de064bc912dfc2`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1213
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-discrete-wdw-constraint.md`

- file: [dag/derivations/independent/fsp-discrete-wdw-constraint.md](../../../dag/derivations/independent/fsp-discrete-wdw-constraint.md)
- sha256 (`lf-normalised`): `50b23b262263fafb0c2c97a43cb393213d5e0589d2a972f20058c01c6163f65c`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-discrete-wdw-constraint_independent.json`

- file: [dag/research/campaign_fsp-discrete-wdw-constraint_independent.json](../../../dag/research/campaign_fsp-discrete-wdw-constraint_independent.json)
- sha256 (`lf-normalised`): `c6ccf7aed95ab3e8072075fd9a90a71d07f3c9228987fe014d164e2ded94e6d7`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-discrete-wdw-constraint_lean_mutation.json`

- file: [dag/research/campaign_fsp-discrete-wdw-constraint_lean_mutation.json](../../../dag/research/campaign_fsp-discrete-wdw-constraint_lean_mutation.json)
- sha256 (`lf-normalised`): `a7f7cfdbe6d7b4be6cce4ad3087d21e064abd3c362b9a451b0dac95d60ce6fb8`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-discrete-wdw-constraint_lean_replay.json`

- file: [dag/research/campaign_fsp-discrete-wdw-constraint_lean_replay.json](../../../dag/research/campaign_fsp-discrete-wdw-constraint_lean_replay.json)
- sha256 (`lf-normalised`): `06b99289eab5a36365a99a5402160416ac71c99f1b4d52f1cb31243958ffa028`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign.md)
- sha256 (`lf-normalised`): `f894f295fb17dc831f4e961602bea56223bf79ae6b34c3350cfa6fe358789808`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `ad94021f09fb60b94e1a91553294c46ef5d3903f8093297b6289f124386e7178`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-DISCRETE-WDW-CONSTRAINT` `GAP_NO_DERIVATION`: [FSP-REGGE-DEFICIT-ACTION](FSP-REGGE-DEFICIT-ACTION.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `APP-R-FSP-CDT-FOLIATION-POSITIVITY` `GAP_NO_DERIVATION`: [FSP-CDT-FOLIATION-POSITIVITY](FSP-CDT-FOLIATION-POSITIVITY.md) (OPEN)
