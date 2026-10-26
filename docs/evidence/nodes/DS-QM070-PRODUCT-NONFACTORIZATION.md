# DS-QM070-PRODUCT-NONFACTORIZATION

Stage: [FINITE_QM_STRUCTURE](../stages/FINITE_QM_STRUCTURE.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a finite nonnegative joint table w on A x B with W\>0, the product defect Phi(w) vanishes iff w factors through its marginals. Phi is basis-relative and does not see entanglement (Bell state and the classical mixture share the (1/2,0,0,1/2) table).

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- bipartite product structure A x B on a joint table (assumption)

## Bottleneck

Lean states the 2x2 case only: a product table has determinant 0 and the identity table does not factor. The iff for general A x B is not in Lean.

## Source status

\[PROVEN\] mechanized Phi_zero_iff_factors, ENC-1123 (QM-070-C5, C6)

## Review

- PFP review: [dag/results/DS-QM070-PRODUCT-NONFACTORIZATION/reviews/20261019_resources_audit/review_result.json](../../../dag/results/DS-QM070-PRODUCT-NONFACTORIZATION/reviews/20261019_resources_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `status_lowered`; prior status `PROVED_LEAN`; qualifies for E4: no.
  - narrowest claim: Actual marginals, normalized product reconstruction, signed residuals and Phi are checked; residual and zero-defect polynomials are general over Q in Lean.
  - does not support: Formalize arbitrary finite table reconstruction and justify any tensor/basis/quantum coherence lift; a product defect of diagonals does not test entanglement.
  - next test: Formalize arbitrary finite table reconstruction and justify any tensor/basis/quantum coherence lift; a product defect of diagonals does not test entanglement.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-0256
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DerivationDagQMClosure`): recorded sha256 `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.ds_qm070_071_product_nonfactorization_and_entanglement_witness` | yes | yes | yes | Quot.sound, propext | `#print axioms QuantumMechanics.DerivationDagQMClosure.ds_qm070_071_product_nonfactorization_and_entanglement_witness` |

- counts toward the grade: yes

### Lean: `lean4/H014TensorCompositionBoundary.lean`

- file: [lean4/H014TensorCompositionBoundary.lean](../../../lean4/H014TensorCompositionBoundary.lean)
- sha256 (`bytes`): `0754fd419711de9caf9e47d901c467db8f95dd38bfd570fefb305d0e9ad9386a`
- cited in: node.lean
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `H014TensorCompositionBoundary`): recorded sha256 `0754fd419711de9caf9e47d901c467db8f95dd38bfd570fefb305d0e9ad9386a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build H014TensorCompositionBoundary`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `tensor_not_forced_open` | yes | yes | yes | none | `#print axioms tensor_not_forced_open` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_quantum_physics/src/entanglement.rs`

- file: `omega_engine/crates_rs/omega_quantum_physics/src/entanglement.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/12_finite_qm_structure/tfq_0256_product_defect_on_a_bipartite_weight_table.md`

- file: [dag/derivations/12_finite_qm_structure/tfq_0256_product_defect_on_a_bipartite_weight_table.md](../../../dag/derivations/12_finite_qm_structure/tfq_0256_product_defect_on_a_bipartite_weight_table.md)
- sha256 (`lf-normalised`): `a8b8186f85a093a61bdcc4104959393ada8fa99ca487b667229e7f3d35694789`
- generated view: listed, not counted
- cited in: record TFQ-0256
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/070_product_non_factorization_as_a_bipartite_obstruction/qm_070_product_non_factorization_as_a_bipartite_obstruction_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/003_quantum_foundations/070_product_non_factorization_as_a_bipartite_obstruction/qm_070_product_non_factorization_as_a_bipartite_obstruction_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0256 python: no local python twin located for omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/python/finite_qm
- TFQ-0256 rust: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/entanglement.rs

## Routes

Incoming (2):

- `DS-R-PRODUCT-DEFECT` `COMPUTED`: [FQ-CARRIER-CONTRACT-V2](FQ-CARRIER-CONTRACT-V2.md) (DEFINITION)
- `DS-R-PRODUCT-FROM-WEIGHTS` `COMPUTED`: [L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED](L1-RESIDUAL-SECTOR-WEIGHTS-DECLARED.md) (CONDITIONAL)

Outgoing (2):

- `DS-R-PRODUCT-TO-ENTANGLEMENT` `DERIVED_LEAN`: [DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS](DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS.md) (PROVED_LEAN)
- `DS-R-QUBIT` `GAP_NO_DERIVATION`: [DS-QM072-QUBIT-SUPERPOSITION-OBSTRUCTED](DS-QM072-QUBIT-SUPERPOSITION-OBSTRUCTED.md) (OPEN)
