# PG-WDP-DEGREE1-WINDOW

Stage: [WDP](../stages/WDP.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A degree-1 window is (C0,C1,C2,d0,d1) of finite-dimensional spaces with a norm J; Q1 = C1/im d0; kappa1(\[h\]) = d1 h is defined exactly when d1 d0 = 0 (the window hypothesis; otherwise no kappa1 exists on Q1), H1 = ker kappa1, Phi1 = quotient defect Phi_J, Gamma2 = L1 norm of d1 h, R_cl = Gamma2/Phi1 only when Phi1 \> 0; the diagnostic classes ExactClass (Phi1 = 0), ClosedResidual (Phi1 \> 0, Gamma2 = 0), ActiveClosureFailure (Phi1 \> 0, Gamma2 \> 0) partition the (Phi1, Gamma2) pairs. \[Kernel-checked over a field for the algebra and for the abstract defect; for weighted-L1 cost on graph windows with positive weights the cost is proved to be the IsPhi defect of a definite J, so Phi1 = 0 iff the class is zero; Phi1 values on 17 integer windows are certified by verified primal/dual pairs; norms other than weighted L1 and attainment for general windows are not covered.\]

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 21
- cited Lean declarations covered by a current replay receipt: 21
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

- `receipt_names_uncited_module`: a replay receipt names this node for lean4/WdpDegree1Window.lean, but the node's lean, rust and source fields do not cite it. A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence).

## Imported structure

- Finite-dimensional real/complex vector space and norm J (assumption: declared)
- Complex/chain structure d1 d0 = 0 (assumption: window hypothesis)

## Bottleneck

The window is declared, not derived from \<\> or Real_0 (PG-GAP-GENESIS-TO-WINDOW). Existence of the attained minimum for every weighted-L1 window (strong duality) is not a Lean theorem; per-window attainment rests on verified primal/dual witnesses.

## Source status

WDP-CH04-D01/D02: degree-1 window (C0,C1,C2,d0,d1), Q1, kappa1, Phi1, Gamma2, R_cl, diagnostic classes

## Review

- PFP review: [dag/results/PG-WDP-DEGREE1-WINDOW/reviews/20261021_batch01b_audit/delivery_review_result.json](../../../dag/results/PG-WDP-DEGREE1-WINDOW/reviews/20261021_batch01b_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `statement_narrowed`; prior status `DEFINITION`; qualifies for E4: yes.
  - narrowest claim: For modules over a field (the graph windows tensored with Q), kappa1 exists on Q1 = C1/im d0 exactly when d1 d0 = 0 (kernel); for graph windows with positive weights the weighted-L1 cost is the IsPhi defect of a nonnegative definite J, so Phi1 = 0 iff the class is zero (kernel); on the 17 tabulated integer windows Phi1 is the weighted-L1 minimum over rational potentials with a verified primal potential and dual vector; each (Phi1, Gamma2) pair has exactly one class: ExactClass iff Phi1 = 0, ClosedResidual iff Phi1 \> 0 and Gamma2 = 0, ActiveClosureFailure iff both are positive (the Lean diag theorems state phi != 0, equivalent for Phi1 \>= 0).
  - does not support: Any derivation of the window from Genesis admission or Real_0 (it stays a declared datum); norms other than weighted L1; non-graph d0 beyond the module-level lemmas; existence of the attained minimum for the weighted-L1 cost as a Lean theorem (attainment is part of IsPhi and is witnessed natively by x and y, but LP strong duality / minimiser existence is not formalised); complex coefficients; any meaning of Gamma2 for a non-window (representative dependent); that R_cl = Gamma2/Phi1 mixes the weighted Phi1 with the unweighted Gamma2 and so depends on the weight scale; any physical reading of the three classes.
  - next test: Prove in Lean that the weighted-L1 quotient defect of every graph window is attained (existence of a minimising potential, or strong duality for the pair of linear programs), so that the attainment clause of IsPhi becomes a theorem for the windows instead of resting on the verified primal and dual witnesses tabulated here.

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
| `QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.conditional_route_bridges_pg_l1_fq_ds_sixteen_route_closure` |
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
| `Repair` | yes | yes | yes | none | `#print axioms Repair` |
| `kappa` | yes | yes | yes | none | `#print axioms kappa` |
- counts toward the grade: yes

### Lean: `lean4/WdpDegree1Window.lean`

- file: [lean4/WdpDegree1Window.lean](../../../lean4/WdpDegree1Window.lean)
- sha256 (`bytes`): `9da1d559e69e39b4235df28e9739536481b06944e90981b4b975683ddef5db42`
- cited in: receipt dag/research/pfp_batch01_lean_replay.json (WdpDegree1Window)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `WdpDegree1Window`): recorded sha256 `9da1d559e69e39b4235df28e9739536481b06944e90981b4b975683ddef5db42` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build WdpDegree1Window`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WdpDegree1Window.cost_eq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpDegree1Window.cost_eq` |
| `WdpDegree1Window.diag_unique` | yes | yes | yes | Quot.sound, propext | `#print axioms WdpDegree1Window.diag_unique` |
| `WdpDegree1Window.graph_phi_zero_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpDegree1Window.graph_phi_zero_iff` |
| `WdpDegree1Window.isPhi_graph_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpDegree1Window.isPhi_graph_iff` |
| `WdpDegree1Window.isPhi_nonneg` | yes | yes | yes | Quot.sound, propext | `#print axioms WdpDegree1Window.isPhi_nonneg` |
| `WdpDegree1Window.isPhi_of_certificate` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpDegree1Window.isPhi_of_certificate` |
| `WdpDegree1Window.isPhi_shift` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpDegree1Window.isPhi_shift` |
| `WdpDegree1Window.isPhi_zero_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpDegree1Window.isPhi_zero_iff` |
| `WdpDegree1Window.kappa_descends_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpDegree1Window.kappa_descends_iff` |
| `WdpDegree1Window.kappa_eq_zero_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpDegree1Window.kappa_eq_zero_iff` |
| `WdpDegree1Window.kappa_not_defined_instance` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpDegree1Window.kappa_not_defined_instance` |
| `WdpDegree1Window.ker_kappa_eq_map` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpDegree1Window.ker_kappa_eq_map` |
| `WdpDegree1Window.ne_zero_iff_pos` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpDegree1Window.ne_zero_iff_pos` |
| `WdpDegree1Window.ratio_class` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpDegree1Window.ratio_class` |
| `WdpDegree1Window.tri_gamma2` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpDegree1Window.tri_gamma2` |
| `WdpDegree1Window.tri_phi` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpDegree1Window.tri_phi` |
| `WdpDegree1Window.weak_duality` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpDegree1Window.weak_duality` |
| `WdpDegree1Window.wl1_definite` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms WdpDegree1Window.wl1_definite` |
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/obstruction.rs`

- file: [code/rust/src/wdp/obstruction.rs](../../../code/rust/src/wdp/obstruction.rs)
- sha256 (`bytes`): `d4a9514b3ee22c73ac47193206838c49cd5d908485d2c38dd026cd3bd9416cf8`
- cited in: record TFQ-0344 (shared), record TFQ-0349 (shared)
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: no

### Rust: `code/rust/src/wdp/phi1_coda_adapter.rs`

- file: [code/rust/src/wdp/phi1_coda_adapter.rs](../../../code/rust/src/wdp/phi1_coda_adapter.rs)
- sha256 (`bytes`): `a87803bfe55c4f16247dfe593bbb691570ee495b19d07c0a82ff096c5591c276`
- cited in: record TFQ-0349 (shared)
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: no

### Rust: `code/rust/src/wdp/primitive_axiomatics.rs`

- file: [code/rust/src/wdp/primitive_axiomatics.rs](../../../code/rust/src/wdp/primitive_axiomatics.rs)
- sha256 (`bytes`): `c1ae6edba4d807a8247b3a2726dd7d07f30d83dbb27611e036c09e5e6ef26efc`
- cited in: record TFQ-0344 (shared), record TFQ-0349 (shared)
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_wdp/src/obstruction.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/obstruction.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_wdp/src/primitive_axiomatics.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/primitive_axiomatics.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/06_wdp/tfq_0004_witnessed_difference_degree_1_window.md`

- file: [dag/derivations/06_wdp/tfq_0004_witnessed_difference_degree_1_window.md](../../../dag/derivations/06_wdp/tfq_0004_witnessed_difference_degree_1_window.md)
- sha256 (`lf-normalised`): `ff7df5416142771ec9a4d7edc2fe2b4150c3092d76bb90e30bc7926120b01570`
- generated view: listed, not counted
- cited in: record TFQ-0004
- counts toward the grade: no

### Documents and data: `dag/derivations/06_wdp/tfq_0344_do_not_derive_the_degree_1_window_c0_c1_c2_d0_d1_from.md`

- file: [dag/derivations/06_wdp/tfq_0344_do_not_derive_the_degree_1_window_c0_c1_c2_d0_d1_from.md](../../../dag/derivations/06_wdp/tfq_0344_do_not_derive_the_degree_1_window_c0_c1_c2_d0_d1_from.md)
- sha256 (`lf-normalised`): `c16aa4ea4b517bdc1a92a8369e95aeb46571eb4ab99577a59f4423c1aecdfdd9`
- generated view: listed, not counted
- cited in: record TFQ-0344 (shared)
- counts toward the grade: no

### Documents and data: `dag/derivations/07_l1_emergence/tfq_0349_compute_declared_phi1_and_gamma2_on_a_finite_window_and_do_not.md`

- file: [dag/derivations/07_l1_emergence/tfq_0349_compute_declared_phi1_and_gamma2_on_a_finite_window_and_do_not.md](../../../dag/derivations/07_l1_emergence/tfq_0349_compute_declared_phi1_and_gamma2_on_a_finite_window_and_do_not.md)
- sha256 (`lf-normalised`): `047105de6bc2cc440087151d00b36b8184df248cb1787f361bb411a256f3c1bf`
- generated view: listed, not counted
- cited in: record TFQ-0349 (shared)
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `PG-R-GAP-GENESIS-TO-WINDOW` `DERIVED_LEAN`: [PG-WDP-GENESIS-BRIDGE-OBLIGATIONS](PG-WDP-GENESIS-BRIDGE-OBLIGATIONS.md) (OPEN), [PG-PRIMDIFF-AXIOMS](PG-PRIMDIFF-AXIOMS.md) (DEFINITION)

Outgoing (6):

- `OPS-R-CECH-COBOUNDARY-2` `GAP_NO_DERIVATION`: [OPS-CECH-COBOUNDARY](OPS-CECH-COBOUNDARY.md) (PROVED_PROSE)
- `PG-R-WINDOW-SEQUENCE` `DERIVED_LEAN`: [PG-WDP-QUOTIENT-EXACT-SEQUENCE](PG-WDP-QUOTIENT-EXACT-SEQUENCE.md) (PROVED_LEAN)
- `PGW-R-WDP-DEGREE-K-TORSION-BALANCE` `DERIVED_PROSE`: [PGW-WDP-DEGREE-K-TORSION-BALANCE](PGW-WDP-DEGREE-K-TORSION-BALANCE.md) (PROVED_PROSE)
- `PGW-R-WDP-DURATION-EXACTNESS-PERIOD-WITNESS` `DERIVED_PROSE`: [PGW-WDP-DURATION-EXACTNESS-PERIOD-WITNESS](PGW-WDP-DURATION-EXACTNESS-PERIOD-WITNESS.md) (DEFINITION)
- `PGW-R-WDP-EXACT-SEQUENCE-H1-Q1` `DERIVED_LEAN`: [PGW-WDP-EXACT-SEQUENCE-H1-Q1](PGW-WDP-EXACT-SEQUENCE-H1-Q1.md) (PROVED_LEAN)
- `X-R-WDP-WINDOW-TO-L1-WINDOW` `DERIVED_LEAN`: [L1-WDP-WINDOW-PHI1-GAMMA2](L1-WDP-WINDOW-PHI1-GAMMA2.md) (DEFINITION)
