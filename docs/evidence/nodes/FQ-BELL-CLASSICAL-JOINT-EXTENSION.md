# FQ-BELL-CLASSICAL-JOINT-EXTENSION

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> If four binary response variables A0,A1,B0,B1 in {-1,+1} share one positive normalized joint law, every deterministic assignment has S in {-2,2} and |S| \<= 2 by convexity. The integer-scale separator/CHSH equivalence and the scaled facet bounds for Nat-weighted binary-assignment lists are formal, and finite exact native certificates cover the saved rational cases. The full formal rational Fine converse (a common joint law exists exactly when the CHSH family holds) remains open, and physical conclusions additionally need locality and setting independence.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- positive normalized joint law (assumption)
- locality and setting independence for physical reading (assumption)

## Bottleneck

Formalize the rational Fine converse: existence of a common positive joint law versus satisfaction of the CHSH family over the rationals.

## Source status

Deterministic CHSH {-2, 2} bound and inductive finite-convex-combination bound mechanized in DerivationDagQMClosure.lean

## Review

- PFP review: [dag/results/FQ-BELL-CLASSICAL-JOINT-EXTENSION/reviews/20261018_separator_audit/audit_results.json](../../../dag/results/FQ-BELL-CLASSICAL-JOINT-EXTENSION/reviews/20261018_separator_audit/audit_results.json); file present and sha256 matches the node's record: yes; verdict `separator_extension_reviewed_guards_repaired`; scope effect `statement_narrowed`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Integer separator theorem and finite exact native certificates; full formal rational Fine converse remains open.
  - does not support: The full formal rational Fine converse (common positive joint law versus the CHSH family over the rationals) remains open.
  - next test: Formalize the rational Fine converse and rerun the separator extension against it.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0259 (shared)
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.fq_bell_classical_joint_extension_convex_bound` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.fq_bell_classical_joint_extension_convex_bound` |

- counts toward the grade: yes

### Lean: `lean4/EverettForkingTree.lean`

- file: [lean4/EverettForkingTree.lean](../../../lean4/EverettForkingTree.lean)
- sha256 (`bytes`): `1dc256ecbad36c8d1a3cb128ba67fab5efc37880d9a58d58698dfc4765646b0e`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `EverettForkingTree`): recorded sha256 `1dc256ecbad36c8d1a3cb128ba67fab5efc37880d9a58d58698dfc4765646b0e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build EverettForkingTree`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `chsh_classical_bound` | yes | yes | yes | none | `#print axioms chsh_classical_bound` |

- counts toward the grade: yes

### Lean: `lean4/QuantumCorrelation.lean`

- file: [lean4/QuantumCorrelation.lean](../../../lean4/QuantumCorrelation.lean)
- sha256 (`bytes`): `1efde024ea6004e14e564be78cc1e9c5238919f28f2ddc1a1fbf6b58f6fa00bd`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_core.json](../../../dag/research/lean_replay_campaign_finite_qm_core.json) (module `QuantumCorrelation`): recorded sha256 `1efde024ea6004e14e564be78cc1e9c5238919f28f2ddc1a1fbf6b58f6fa00bd` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build QuantumCorrelation`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `classical_chsh_bound` | yes | yes | yes | none | `#print axioms classical_chsh_bound` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0259_finite_chsh_ceiling_on_one_global_joint_table.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0259_finite_chsh_ceiling_on_one_global_joint_table.md](../../../dag/derivations/12_finite_qm_structure/tfq_0259_finite_chsh_ceiling_on_one_global_joint_table.md)
- sha256 (`lf-normalised`): `b2177f05c11715d1dec037d5488c6c1e891d6c536e6fb4c875616087051c4c65`
- generated view: listed, not counted
- cited in: record TFQ-0259 (shared)
- counts toward the grade: no

### Documents and data: `sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md`

- file: [sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md](../../../sources/atlas/papers/finite_quantum_mechanics/finite_quantum_mechanics.md)
- sha256 (`lf-normalised`): `85ca7b22b1c1e360a4c17ad8a9e0bddae03433592585b01d23a74cd09c82929e`
- cited in: node.source
- counts toward the grade: yes

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:3aa68d6116ce374efc50eed1e23d148aaae1be854b3bf16be67d8d1ab42dceb4::JointAssignment`
- `external:sha256:436c024d77fc3479e5ac42ac8b0fc5e0884fa46295d995abb94d20d477c5c9cc::FiniteBellProblem`
- `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche2_row_sparsity_bell_torsion_and_structure_witness`

## Absences recorded by the TFQ records

- TFQ-0259 python: no local python twin located for sources/atlas/papers/finite_quantum_mechanics/python/finite_qm
- TFQ-0259 rust: no local rust twin located for external:sha256:3aa68d6116ce374efc50eed1e23d148aaae1be854b3bf16be67d8d1ab42dceb4

## Routes

Incoming (1):

- `FQ-R-BELL-CLASSICAL` `DERIVED_LEAN`: [FQ-POSITIVE-WEIGHTS-ADMITTED](FQ-POSITIVE-WEIGHTS-ADMITTED.md) (IMPORTED_ASSUMPTION)

Outgoing (1):

- `FQ-R-BELL-VIOLATION` `COMPUTED`: [FQ-BELL-RATIONAL-VIOLATION-14-5](FQ-BELL-RATIONAL-VIOLATION-14-5.md) (COMPUTATIONALLY_CHECKED)
