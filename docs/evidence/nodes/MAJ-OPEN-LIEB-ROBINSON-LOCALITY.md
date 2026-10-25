# MAJ-OPEN-LIEB-ROBINSON-LOCALITY

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Which distinctions a local system can detect, preserve or repair within a specified time may admit a Lieb-Robinson quantitative extension supporting conditional statements on quantum computing viability.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 12
- cited Lean declarations covered by a current replay receipt: 10
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Continuous-time Banach-algebra Lieb-Robinson bounds for microscopic superconducting Hamiltonians and general physical device viability verdicts remain open. Narrowed in lean4/CampaignMajOpenLiebRobinsonLocality.lean and checks/independent/maj-open-lieb-robinson-locality.py while keeping status OPEN to: (1) one-sided causal radius additivity R_LR(R_LR(r0, vLR, t1), vLR, t2) = R_LR(r0, vLR, t1 + t2) and two-sided 1D support diameter growth W_LR(w0, vLR, t) = w0 + 2 vLR t with strict step increase for vLR \> 0; (2) syndrome recovery viability within the Lieb-Robinson horizon (2 W_LR(w0, vLR, t) \< d implies every propagated error-pair difference satisfies wDiff \< d) and horizon monotonicity across tLo \< tHi with margin 4 vLR (tHi - tLo); (3) horizon overflow logical collision (when d \<= 2 W_LR(w0, vLR, t), a weight-d logical cycle partitions into w1 = floor(d/2) and w2 = d - floor(d/2) inside the propagated ball); and (4) discrete commutator tail suppression c0 g^t \< c0 mu^dist outside the light cone (t \< dist), classical syndrome-routing delay inequality 2 w0 vCl + 4 vLR L \< d vCl, and L=4 vs L=7 tetron torus viability window comparisons.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-OPEN-LOCALITY-VIABILITY claims OPEN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignMajOpenLiebRobinsonLocality.lean`

- file: [lean4/CampaignMajOpenLiebRobinsonLocality.lean](../../../lean4/CampaignMajOpenLiebRobinsonLocality.lean)
- sha256 (`bytes`): `b1661aed81b981c3429e2f704d52f074e3286c60159f0d9a0ae56ebe173c2013`
- cited in: node.lean, receipt dag/research/campaign_maj-open-lieb-robinson-locality_lean_replay.json (CampaignMajOpenLiebRobinsonLocality), record TFQ-1149
- replay: `verified`
  - receipt [dag/research/campaign_maj-open-lieb-robinson-locality_lean_replay.json](../../../dag/research/campaign_maj-open-lieb-robinson-locality_lean_replay.json) (module `CampaignMajOpenLiebRobinsonLocality`): recorded sha256 `b1661aed81b981c3429e2f704d52f074e3286c60159f0d9a0ae56ebe173c2013` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CampaignMajOpenLiebRobinsonLocality`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignMajOpenLiebRobinsonLocality.critical_repair_horizon_monotonicity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajOpenLiebRobinsonLocality.critical_repair_horizon_monotonicity` |
| `CampaignMajOpenLiebRobinsonLocality.discrete_commutator_tail_decay_recurrence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajOpenLiebRobinsonLocality.discrete_commutator_tail_decay_recurrence` |
| `CampaignMajOpenLiebRobinsonLocality.lieb_robinson_1d_support_diameter_growth` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajOpenLiebRobinsonLocality.lieb_robinson_1d_support_diameter_growth` |
| `CampaignMajOpenLiebRobinsonLocality.lieb_robinson_causal_radius_additive` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajOpenLiebRobinsonLocality.lieb_robinson_causal_radius_additive` |
| `CampaignMajOpenLiebRobinsonLocality.lieb_robinson_horizon_exceeded_logical_collision` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajOpenLiebRobinsonLocality.lieb_robinson_horizon_exceeded_logical_collision` |
| `CampaignMajOpenLiebRobinsonLocality.lieb_robinson_locality_open_scope_fence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajOpenLiebRobinsonLocality.lieb_robinson_locality_open_scope_fence` |
| `CampaignMajOpenLiebRobinsonLocality.lieb_robinson_pair_difference_weight_bound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajOpenLiebRobinsonLocality.lieb_robinson_pair_difference_weight_bound` |
| `CampaignMajOpenLiebRobinsonLocality.syndrome_measurement_communication_delay_bound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajOpenLiebRobinsonLocality.syndrome_measurement_communication_delay_bound` |
| `CampaignMajOpenLiebRobinsonLocality.syndrome_recovery_viability_within_lr_horizon` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajOpenLiebRobinsonLocality.syndrome_recovery_viability_within_lr_horizon` |
| `CampaignMajOpenLiebRobinsonLocality.torus_tetron_viability_window_witness` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms CampaignMajOpenLiebRobinsonLocality.torus_tetron_viability_window_witness` |
- counts toward the grade: yes

### Python: `checks/independent/maj-open-lieb-robinson-locality.py`

- file: [checks/independent/maj-open-lieb-robinson-locality.py](../../../checks/independent/maj-open-lieb-robinson-locality.py)
- sha256 (`bytes`): `4a5d2445af665608485c880298b396bb325578fe8c29b000542eb7c437795272`
- cited in: record TFQ-1149

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `lr_support_weight_1d` (python_symbol) | yes | yes | yes | - | - |
| `main` (python_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1149_maj_open_lieb_robinson_locality.md`

- file: [dag/derivations/28_majorana/tfq_1149_maj_open_lieb_robinson_locality.md](../../../dag/derivations/28_majorana/tfq_1149_maj_open_lieb_robinson_locality.md)
- sha256 (`lf-normalised`): `a5e706c7ce4dc31a266abe35532cf7e8163898f9c49b3cf8ad6c5ad909c9acba`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1149
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/maj-open-lieb-robinson-locality.md`

- file: [dag/derivations/independent/maj-open-lieb-robinson-locality.md](../../../dag/derivations/independent/maj-open-lieb-robinson-locality.md)
- sha256 (`lf-normalised`): `ee3d5a84eedffce98e5b56ae5ac64ba9008d477ac359d1bce7ba5eaad520aa53`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_maj-open-lieb-robinson-locality_independent.json`

- file: [dag/research/campaign_maj-open-lieb-robinson-locality_independent.json](../../../dag/research/campaign_maj-open-lieb-robinson-locality_independent.json)
- sha256 (`lf-normalised`): `add946add17d57473e564f9f75808e012e655802dd9f35c9e5534114171fe432`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_maj-open-lieb-robinson-locality_lean_mutation.json`

- file: [dag/research/campaign_maj-open-lieb-robinson-locality_lean_mutation.json](../../../dag/research/campaign_maj-open-lieb-robinson-locality_lean_mutation.json)
- sha256 (`lf-normalised`): `4b017ed1abd43b3dc30002ea857cc39534198a564ae8c3cffcec988dbd41f4f4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_maj-open-lieb-robinson-locality_lean_replay.json`

- file: [dag/research/campaign_maj-open-lieb-robinson-locality_lean_replay.json](../../../dag/research/campaign_maj-open-lieb-robinson-locality_lean_replay.json)
- sha256 (`lf-normalised`): `25d795436ea40d9ac748cf058137ea4de55aeedcbd36ec0fd6762727815b8a44`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `e92416bb1739e51de20a8ad6a26d4b5f3d76b974d7556507b13149b29e8edb47`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-OPEN-LIEB-ROBINSON-LOCALITY` `GAP_NO_DERIVATION`: [MAJ-SYNDROME-RECOVERY-CRITERION](MAJ-SYNDROME-RECOVERY-CRITERION.md) (PROVED_PROSE)

Outgoing (1):

- `APP-R-QCV-PHYSICAL-SATISFIABILITY-OPEN` `GAP_NO_DERIVATION`: [QCV-PHYSICAL-SATISFIABILITY-OPEN](QCV-PHYSICAL-SATISFIABILITY-OPEN.md) (OPEN)
