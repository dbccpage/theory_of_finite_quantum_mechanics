# PG-WDP-QUOTIENT-EXACT-SEQUENCE

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a window over a field with d1 d0 = 0, kappa1 is well defined on Q1 and 0 -\> H1 -\> Q1 -\> im d1 -\> 0 is exact with dim Q1 = dim H1 + dim im d1; when dim H1 \> 0 and dim im d1 \> 0 no section is invariant under the automorphisms 1 + incl f pi of the extension (which act freely on the sections and are not automorphisms of the window), and when either vanishes the section is unique and invariant; every pair (Phi1, Gamma2) lies in exactly one diagnostic class; for a definite J, Phi1 = 0 iff the class of h is zero (false for a seminorm); and for weighted L1 over Q with an attained minimum, ||d1 h||_1 \<= c Phi1 whenever c is at least the largest column-sum-to-weight ratio (equivalent to the operator bound). Naturality of the splitting for automorphisms of the window, other norms, complex coefficients and Phi1 \>= 0 are not covered.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 22
- cited Lean declarations covered by a current replay receipt: 22
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 3
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (3 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `receipt_names_uncited_module`: a replay receipt names this node for lean4/WdpQuotientSequence.lean, but the node's lean, rust and source fields do not cite it. A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence).

## Imported structure

- Norm hypothesis over R, C, or Q restricted from the real extension (assumption)

## Bottleneck

'No canonical splitting' is proved only for the unipotent automorphisms of the extension (a torsor statement) and is false for dim H1 = 0 or d1 = 0; Gamma2 is the representative norm (equal to the source value at the minimal residual when d1 d0 = 0); the norm hypothesis and an attained minimiser are assumed; naturality for window automorphisms is the node's next test.

## Source status

WDP-CH04-P03 FINITE_PROVED (P); P04/P05 FINITE_PROVED (P; C)

## Review

- PFP review: [dag/results/PG-WDP-QUOTIENT-EXACT-SEQUENCE/reviews/20261021_batch01b_audit/delivery_review_result.json](../../../dag/results/PG-WDP-QUOTIENT-EXACT-SEQUENCE/reviews/20261021_batch01b_audit/delivery_review_result.json); file present and sha256 matches the node's record: no; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: For a window over a field with d1 d0 = 0 the sequence 0 -\> H1 -\> Q1 -\> im d1 -\> 0 is exact; no section is invariant under 1 + incl f pi when dim H1 \> 0 and dim im d1 \> 0 (kernel), and when dim H1 * dim im d1 = 0 there is exactly one section and it is invariant (kernel); every class has exactly one diagnostic class; Phi1 = 0 iff the class is zero for a definite J; and \|\|d1 h\|\|_1 \<= c Phi1 for an attained minimum and c at least the J-to-L1 column bound.
  - does not support: Any derivation of the window; norms other than weighted L1 for the inequality; complex coefficients; a statement that the sequence has or lacks a section natural for automorphisms of the window (graph automorphisms preserving d0, d1 and the weights); the converse "if there is an invariant section then dim H1 * dim im d1 = 0" is native by dimension (section_dim) with the trivial-factor halves in the kernel; existence of minimisers for general norms; Phi1 \>= 0 as a theorem for the weighted-L1 window (gamma2_nonneg is anchored, Phi1 \>= 0 needs the cost bridge of the degree-1 window node); any physical reading of the classes.
  - next test: Decide the splitting claim for the finite group G of automorphisms of the K4 two-face window (graph automorphisms preserving the two faces, d0, d1 and the weights) by solving the linear fixed-point equations of G on the affine section space over Hom(im d1, H1) = Q^2: either a G-fixed section exists or the fixed locus is empty.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.master_dag_177_node_10_stage_and_172_route_partition_conservation` |
| `QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.master_operad_25_family_composition_and_end_to_end_chain_closure` |
- counts toward the grade: yes

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean)
- sha256 (`bytes`): `bef8623978d7c0735b4a02db686664b03b61e18bba0e5ef6bcce81ff4234dd0a`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_wdp.json](../../../dag/research/lean_replay_campaign_wdp.json) (module `Imported.WitnessedDifference.WitnessedDifference.Obstruction`): recorded sha256 `bef8623978d7c0735b4a02db686664b03b61e18bba0e5ef6bcce81ff4234dd0a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `closure_ratio_le_opnorm` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms closure_ratio_le_opnorm` |
| `closure_ratio_nonneg` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms closure_ratio_nonneg` |
| `kappa_exact_sequence` | yes | yes | yes | none | `#print axioms kappa_exact_sequence` |
| `kappa_well_defined` | yes | yes | yes | none | `#print axioms kappa_well_defined` |
- counts toward the grade: yes

### Lean: `lean4/WdpQuotientSequence.lean`

- file: [lean4/WdpQuotientSequence.lean](../../../lean4/WdpQuotientSequence.lean)
- sha256 (`bytes`): `2ee150c2744e6b60bf7d2db1c630bd44d1a62fd76aae37e510d24788a46db866`
- cited in: receipt dag/research/pfp_batch01_lean_replay.json (WdpQuotientSequence)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `WdpQuotientSequence`): recorded sha256 `2ee150c2744e6b60bf7d2db1c630bd44d1a62fd76aae37e510d24788a46db866` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build WdpQuotientSequence`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WdpQuotientSequence.columns_of_opbound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpQuotientSequence.columns_of_opbound` |
| `WdpQuotientSequence.diag_unique` | yes | yes | yes | Quot.sound, propext | `#print axioms WdpQuotientSequence.diag_unique` |
| `WdpQuotientSequence.exact_sequence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpQuotientSequence.exact_sequence` |
| `WdpQuotientSequence.exists_unique_invariant_section_of_trivial` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpQuotientSequence.exists_unique_invariant_section_of_trivial` |
| `WdpQuotientSequence.finrank_sequence` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpQuotientSequence.finrank_sequence` |
| `WdpQuotientSequence.gamma2_nonneg` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpQuotientSequence.gamma2_nonneg` |
| `WdpQuotientSequence.gamma2_repair` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpQuotientSequence.gamma2_repair` |
| `WdpQuotientSequence.gamma_at_minimiser_le` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpQuotientSequence.gamma_at_minimiser_le` |
| `WdpQuotientSequence.gamma_bound_fails_instance` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpQuotientSequence.gamma_bound_fails_instance` |
| `WdpQuotientSequence.gamma_le_opnorm_phi` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpQuotientSequence.gamma_le_opnorm_phi` |
| `WdpQuotientSequence.isPhi_zero_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpQuotientSequence.isPhi_zero_iff` |
| `WdpQuotientSequence.no_natural_section` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpQuotientSequence.no_natural_section` |
| `WdpQuotientSequence.opbound_of_columns` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpQuotientSequence.opbound_of_columns` |
| `WdpQuotientSequence.section_unique_of_subsingleton` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpQuotientSequence.section_unique_of_subsingleton` |
| `WdpQuotientSequence.seminorm_instance` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpQuotientSequence.seminorm_instance` |
| `WdpQuotientSequence.window_instance_no_natural_section` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpQuotientSequence.window_instance_no_natural_section` |
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/cochains.rs`

- file: [code/rust/src/wdp/cochains.rs](../../../code/rust/src/wdp/cochains.rs)
- sha256 (`bytes`): `56119171f22517ed69ba8b086b3001e8f23f46438bbbb8d07962252b58e524a5`
- cited in: record TFQ-0345
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/fenchel_duality.rs`

- file: [code/rust/src/wdp/fenchel_duality.rs](../../../code/rust/src/wdp/fenchel_duality.rs)
- sha256 (`bytes`): `ca7fe2172744dc3952b90c9367a64e649d4b0b46fc81b9471e5f79e6dde41df8`
- cited in: record TFQ-0348
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/obstruction.rs`

- file: [code/rust/src/wdp/obstruction.rs](../../../code/rust/src/wdp/obstruction.rs)
- sha256 (`bytes`): `d4a9514b3ee22c73ac47193206838c49cd5d908485d2c38dd026cd3bd9416cf8`
- cited in: record TFQ-0345, record TFQ-0348
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/06_wdp/tfq_0345_on_a_declared_window_with_d1_d0_0_compute_q1_kappa1.md`

- file: [dag/derivations/06_wdp/tfq_0345_on_a_declared_window_with_d1_d0_0_compute_q1_kappa1.md](../../../dag/derivations/06_wdp/tfq_0345_on_a_declared_window_with_d1_d0_0_compute_q1_kappa1.md)
- sha256 (`lf-normalised`): `809cc5302ac9487baa21af0cfa1a5de615d112d890408c1ca471d77c27773507`
- generated view: listed, not counted
- cited in: record TFQ-0345
- counts toward the grade: no

### Documents and data: `dag/derivations/06_wdp/tfq_0348_certify_a_rational_phi1_value_by_a_bounded_circulation_that_meets_a.md`

- file: [dag/derivations/06_wdp/tfq_0348_certify_a_rational_phi1_value_by_a_bounded_circulation_that_meets_a.md](../../../dag/derivations/06_wdp/tfq_0348_certify_a_rational_phi1_value_by_a_bounded_circulation_that_meets_a.md)
- sha256 (`lf-normalised`): `478378ffe76020913f8376bd706b37f2f09c292bf0d10965241a002bea1581c3`
- generated view: listed, not counted
- cited in: record TFQ-0348
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `PG-R-WINDOW-SEQUENCE` `DERIVED_LEAN`: [PG-WDP-DEGREE1-WINDOW](PG-WDP-DEGREE1-WINDOW.md) (DEFINITION)

Outgoing (5):

- `IMPL-R-FSP-NF002` `DERIVED_LEAN`: [IMPL-FSP-SWITCHING-NORMAL-FORM-NF002](IMPL-FSP-SWITCHING-NORMAL-FORM-NF002.md) (PROVED_LEAN)
- `PG-R-DIAG-NOT-ROUTING` `CONDITIONAL_ON_IMPORT`: [PG-WDP-DIAGNOSTIC-NOT-ROUTING](PG-WDP-DIAGNOSTIC-NOT-ROUTING.md) (DEFINITION)
- `PG-R-GROWTH` `DERIVED_LEAN`: [PG-WDP-GROWTH-NO-REPAIR](PG-WDP-GROWTH-NO-REPAIR.md) (PROVED_LEAN)
- `PGW-R-WDP-EXACT-SEQUENCE-H1-Q1` `DERIVED_LEAN`: [PGW-WDP-EXACT-SEQUENCE-H1-Q1](PGW-WDP-EXACT-SEQUENCE-H1-Q1.md) (PROVED_LEAN)
- `PGW-R-WDP-FILLED-TRIANGLE` `DERIVED_LEAN`: [PGW-WDP-FILLED-TRIANGLE](PGW-WDP-FILLED-TRIANGLE.md) (PROVED_LEAN)
