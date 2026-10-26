# L1-WDP-REALIFICATION-J

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> R(A) = \[\[P,-Q\],\[Q,P\]\] is an injective real-linear multiplicative representation of complex matrices with J^2 = -I and Tr_R R(A) = 2 Re Tr_C A (Thm 1). A real matrix is in the image iff it commutes with J (Thm 2). States are sigma = R(rho)/2. J is declared.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 18
- distinct cited Lean declarations covered by a current replay receipt: 18
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

- `receipt_names_uncited_module`: a replay receipt names this node for lean4/RealificationJ.lean, but the node's lean, rust and source fields do not cite it. A replay receipt names this node for a Lean module that the node does not cite itself (a citation gap; the module is counted as evidence).

## Imported structure

- complex structure J: assumption

## Bottleneck

Selection of J not derived (see L1-U1-SELECTOR-OTHER-SEGMENT). Lean for Thm 1/2 now exists (RealificationJ.lean). Positivity, states sigma = R(rho)/2 and the pair-model vs Mathlib complex-matrix identification are unpaid.

## Source status

genesis_qm_realification_bridge: 'declarations of complex structure, not a theorem that an unstructured real carrier selects J'

## Review

- PFP review: [dag/results/L1-WDP-REALIFICATION-J/reviews/20261021_batch01a_audit/delivery_review_result.json](../../../dag/results/L1-WDP-REALIFICATION-J/reviews/20261021_batch01a_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `caveat_added`; prior status `DEFINITION`; qualifies for E4: yes.
  - narrowest claim: Complex matrices here are the declared pair model (P, Q) with the hand-written product. R(A) = \[\[P,-Q\],\[Q,P\]\] is an injective ring-linear multiplicative embedding of these into real matrices with J_m R(A) = R(A) J_n and Tr R(A) = 2 Re Tr A, and its image is exactly the real matrices that intertwine the DECLARED J (block coordinate order); the same J^2 = -1 identity holds for other matrices (kernel instance, bounded census), so the choice of J remains an input.
  - does not support: Any selection of J or of the complex field (J is a declaration; a second square root of -I exists in the kernel instance and the census exhibits many more); the identification of the pair model CMat with Mathlib complex matrices (no anchor shows CMat is an associative ring or equals Matrix m n Complex); the block-ordering convention (all real coordinates before all imaginary ones) is part of the definition: the interleaved ordering gives a different J and a different matrix; states sigma = R(rho)/2, positivity as a theorem (native instances only), effects, instruments / Kraus intertwining (Theorem 3), the balanced tensor lift, or any operational or physical reading; infinite dimensions; the claim that every real channel is a realified complex one (it is not).
  - next test: Prove in the kernel that R preserves and reflects positivity for Hermitian A, i.e. A is positive semidefinite iff the real quadratic form of R(A) is nonnegative, and that sigma = R(rho)/2 has real trace 1 exactly when Tr rho = 1; the native psd rows are the instances to match.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1002
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm062_u1_selector_layers_and_ring_iso` | yes | yes | yes | none | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm062_u1_selector_layers_and_ring_iso` |
| `QuantumMechanics.DerivationDagQMClosure.l1_observer_h1_h5_cochain_flatness_and_wdp_window_mass_realification` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_observer_h1_h5_cochain_flatness_and_wdp_window_mass_realification` |

- counts toward the grade: yes

### Lean: `lean4/RealificationJ.lean`

- file: [lean4/RealificationJ.lean](../../../lean4/RealificationJ.lean)
- sha256 (`bytes`): `9c4af34f323541434cab7cb2134f4c4c311f6e8e9653bf31603611cd0c52c336`
- cited in: receipt dag/research/pfp_batch01_lean_replay.json (RealificationJ)
- replay: `verified`
  - receipt [dag/research/pfp_batch01_lean_replay.json](../../../dag/research/pfp_batch01_lean_replay.json) (module `RealificationJ`): recorded sha256 `9c4af34f323541434cab7cb2134f4c4c311f6e8e9653bf31603611cd0c52c336` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build RealificationJ`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `RealificationJ.J_R_comm` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RealificationJ.J_R_comm` |
| `RealificationJ.J_sq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RealificationJ.J_sq` |
| `RealificationJ.R_add` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RealificationJ.R_add` |
| `RealificationJ.R_imul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RealificationJ.R_imul` |
| `RealificationJ.R_injective` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RealificationJ.R_injective` |
| `RealificationJ.R_mul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RealificationJ.R_mul` |
| `RealificationJ.R_one` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RealificationJ.R_one` |
| `RealificationJ.R_smul` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RealificationJ.R_smul` |
| `RealificationJ.R_star` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RealificationJ.R_star` |
| `RealificationJ.commutes_conj` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RealificationJ.commutes_conj` |
| `RealificationJ.hermitian_iff_symmetric` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RealificationJ.hermitian_iff_symmetric` |
| `RealificationJ.image_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RealificationJ.image_iff` |
| `RealificationJ.other_root_not_in_image` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RealificationJ.other_root_not_in_image` |
| `RealificationJ.other_square_root_instance` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RealificationJ.other_square_root_instance` |
| `RealificationJ.trace_R` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RealificationJ.trace_R` |
| `RealificationJ.trace_not_twice_complex_trace` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms RealificationJ.trace_not_twice_complex_trace` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/complex_realification.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/complex_realification.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1002
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1002
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_wdp/src/genesis_realification_adapter.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/genesis_realification_adapter.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1002
- counts toward the grade: no

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1002_l1_wdp_realification_j.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1002_l1_wdp_realification_j.md](../../../dag/derivations/08_l1_to_l2/tfq_1002_l1_wdp_realification_j.md)
- sha256 (`lf-normalised`): `211c7110913b4dc9a180ab3ab6cd050f5406095f5cec23b71514ea03d0190218`
- generated view: listed, not counted
- cited in: record TFQ-1002
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_qm_realification_bridge.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_qm_realification_bridge.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `L1-R-REALIFICATION-J` `DERIVED_LEAN`: [L1-IMP-COMPLEX-FIELD](L1-IMP-COMPLEX-FIELD.md) (CONDITIONAL)

Outgoing (1):

- `X-R-REALIFICATION-TO-ADAPTER` `COMPUTED`: [FQ-IMPL-REALIFICATION-ADAPTER](FQ-IMPL-REALIFICATION-ADAPTER.md) (COMPUTATIONALLY_CHECKED)
