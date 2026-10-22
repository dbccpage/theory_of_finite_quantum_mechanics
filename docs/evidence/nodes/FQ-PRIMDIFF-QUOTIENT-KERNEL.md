# FQ-PRIMDIFF-QUOTIENT-KERNEL

Stage: [FINITE_QM_CORE](../stages/FINITE_QM_CORE.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a supplied difference delta : A x A -\> B with a supplied Zero predicate that is reflexive, symmetric and transitive on delta values, ZeroRel is an equivalence and the quotient ResidualQuotient exists; a finite presented carrier X -\> Q has same-report iff equal reports (sameReport_iff). The Zero predicate and the report map are inputs.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 4 Lean reference(s) cited, 4 in this checkout (replay: none 4). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- Zero predicate on difference values (assumption)
- finite report map X -\> Q (assumption)

## Bottleneck

Content is the quotient construction only; nothing here yields a field, norm or Hilbert structure.

## Source status

LEAN PROVED (RECEIPTED) per ledger; Lean header for the H000..H018 family says Candidate only

## Review

- PFP review: [dag/results/FQ-PRIMDIFF-QUOTIENT-KERNEL/reviews/20261019_structure_audit/review_result.json](../../../dag/results/FQ-PRIMDIFF-QUOTIENT-KERNEL/reviews/20261019_structure_audit/review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: The supplied ZeroRel is an equivalence and class equality iff ZeroRel is rechecked generally; finite report partitions and their full equality kernels are recomputed on the retained inputs.
  - does not support: Zero, difference laws and report map remain inputs. A quotient construction alone supplies no coefficient field, norm, Hilbert structure or preferred physical readout.
  - next test: Zero, difference laws and report map remain inputs. A quotient construction alone supplies no coefficient field, norm, Hilbert structure or preferred physical readout.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean, record TFQ-1007
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.l1_to_l2_and_cross_fragment_route_composition` |
- counts toward the grade: yes

### Lean: `lean4/H000FinitePresentedCarrier.lean`

- file: [lean4/H000FinitePresentedCarrier.lean](../../../lean4/H000FinitePresentedCarrier.lean)
- sha256 (`bytes`): `789978ed31d30571cffbfe7efa8e8f46f6340649ab09e876289896eb5ca1a5ce`
- cited in: node.lean, record TFQ-1007
- replay: `none`
- check: `cd lean4 && lake build H000FinitePresentedCarrier`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `presented_carrier_separates` | yes | yes | yes | - | `#print axioms presented_carrier_separates` |
| `sameReport_iff` | yes | yes | yes | - | `#print axioms sameReport_iff` |
- counts toward the grade: yes

### Lean: `lean4/PrimitiveDifference.lean`

- file: [lean4/PrimitiveDifference.lean](../../../lean4/PrimitiveDifference.lean)
- sha256 (`bytes`): `8748733821f0d959e698794f70d4db6595e8fe4a1a00581acd52961f751833a8`
- cited in: node.lean, record TFQ-1007
- replay: `none`
- check: `cd lean4 && lake build PrimitiveDifference`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `zeroRel_equivalence` | yes | yes | yes | - | `#print axioms zeroRel_equivalence` |
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust, record TFQ-1007
- counts toward the grade: no

### Documents and data: `dag/derivations/10_finite_qm_core/tfq_1007_fq_primdiff_quotient_kernel.md`

- file: [dag/derivations/10_finite_qm_core/tfq_1007_fq_primdiff_quotient_kernel.md](../../../dag/derivations/10_finite_qm_core/tfq_1007_fq_primdiff_quotient_kernel.md)
- sha256 (`lf-normalised`): `a000ec130c6228a98585902f11b2c79b75313eb1f1a175ebae03780a47ade160`
- generated view: listed, not counted
- cited in: record TFQ-1007
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/finite_quantum_mechanics.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/finite_quantum_mechanics_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/006_finite_qm/finite_quantum_mechanics_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `X-R-ROOT-TO-PRIMDIFF-KERNEL` `CONDITIONAL_ON_IMPORT`: [PG-ROOT-DIFF-STRUCTURE](PG-ROOT-DIFF-STRUCTURE.md) (ADMITTED_PRIMITIVE)

Outgoing (6):

- `FQ-R-CONTEXTUALITY` `DERIVED_LEAN`: [FQ-CONTEXTUALITY-CECH-F2](FQ-CONTEXTUALITY-CECH-F2.md) (PROVED_LEAN)
- `FQ-R-GAP-PRIM-TO-INTERFACE` `GAP_NO_DERIVATION`: [FQ-DECLARED-QUANTUM-INTERFACE](FQ-DECLARED-QUANTUM-INTERFACE.md) (IMPORTED_ASSUMPTION)
- `FQ-R-GAP-PRIM-TO-SELECTION` `CONDITIONAL_ON_IMPORT`: [FQ-PRIM-TO-QM-SELECTION-OPEN](FQ-PRIM-TO-QM-SELECTION-OPEN.md) (CONDITIONAL)
- `FQ-R-PHASE-FIBER` `CONDITIONAL_ON_IMPORT`: [FQ-PHASE-FIBER-QUOTIENT](FQ-PHASE-FIBER-QUOTIENT.md) (PROVED_LEAN)
- `FQ-R-REALIFICATION` `DERIVED_LEAN`: [FQ-IMPL-REALIFICATION-ADAPTER](FQ-IMPL-REALIFICATION-ADAPTER.md) (PROVED_LEAN)
- `FQ-R-TRACE-ZERO-DUAL` `COMPUTED`: [FQ-TRACE-ZERO-DUALITY-K23](FQ-TRACE-ZERO-DUALITY-K23.md) (COMPUTATIONALLY_CHECKED)
