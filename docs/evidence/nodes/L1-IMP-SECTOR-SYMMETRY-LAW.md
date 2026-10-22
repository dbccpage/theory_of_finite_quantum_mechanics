# L1-IMP-SECTOR-SYMMETRY-LAW

Stage: [L1_TO_L2](../stages/L1_TO_L2.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Transitive sector symmetry of the quadratic readout: relabelling sectors by any permutation in a set whose generated group acts transitively does not change the readout. This is the second law under which the inner product is selected up to scale; it is supplied, not derived from primitive difference, and sectors with distinguished labels would break it (then the diagonal is constant only on orbits).

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 6
- cited Lean, Rust or Python symbols found in their in-repo files: 10
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- transitive sector symmetry of the readout: assumption

## Bottleneck

No finite-theory primitive forces readout invariance under sector relabelling; H006 supplies the permutation envelope only. Deriving the law, or recording which sector labels are distinguished, is item 1 of the run next steps.

## Source status

Supplied law of the quadratic readout in dag/results/L1-IMP-HILBERT-INNER-PRODUCT/runs/20261021T013500Z_sector_form: the readout is invariant under a set of sector permutations whose generated group acts transitively on sectors (SectorFormUniqueness.Invariant, TransitiveOn, Generated; invariance is closed under products and inverses, invariant_of_generated). The finite theory supplies the permutation isometry envelope (H006PermutationUnitary.permutation_isometry), not the statement that the readout must be invariant under it.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/H006PermutationUnitary.lean`

- file: [lean4/H006PermutationUnitary.lean](../../../lean4/H006PermutationUnitary.lean)
- sha256 (`bytes`): `84c8c1b6a38f31091aeb711de1f63307e482cf77086ab2f0d23f2b9359519b6f`
- cited in: node.lean, node.source, record TFQ-1001
- replay: `none`
- check: `cd lean4 && lake build H006PermutationUnitary`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `FableHilbertWalk20260819.H006.permutation_isometry` | yes | yes | yes | - | `#print axioms FableHilbertWalk20260819.H006.permutation_isometry` |
- counts toward the grade: yes

### Lean: `lean4/SectorFormHermitian.lean`

- file: [lean4/SectorFormHermitian.lean](../../../lean4/SectorFormHermitian.lean)
- sha256 (`bytes`): `78ea0b521e573c51d4a1ced879454648a6ba2ca37d87f54f5383eaaccd551efc`
- cited in: node.lean, record TFQ-1001
- replay: `none`
- check: `cd lean4 && lake build SectorFormHermitian`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `InnerProductFable.HermitianSectorForm.Generated` | yes | yes | yes | - | `#print axioms InnerProductFable.HermitianSectorForm.Generated` |
| `InnerProductFable.HermitianSectorForm.Invariant` | yes | yes | yes | - | `#print axioms InnerProductFable.HermitianSectorForm.Invariant` |
- counts toward the grade: yes

### Lean: `lean4/SectorFormUniqueness.lean`

- file: [lean4/SectorFormUniqueness.lean](../../../lean4/SectorFormUniqueness.lean)
- sha256 (`bytes`): `2a08c38a779ba3b7cba8520f9134cfe8e9c8a5020d063c8d316c37e78aef79be`
- cited in: node.lean, record TFQ-1001
- replay: `none`
- check: `cd lean4 && lake build SectorFormUniqueness`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `InnerProductFable.SectorForm.Generated` | yes | yes | yes | - | `#print axioms InnerProductFable.SectorForm.Generated` |
| `InnerProductFable.SectorForm.Invariant` | yes | yes | yes | - | `#print axioms InnerProductFable.SectorForm.Invariant` |
| `InnerProductFable.SectorForm.TransitiveOn` | yes | yes | yes | - | `#print axioms InnerProductFable.SectorForm.TransitiveOn` |
| `InnerProductFable.SectorForm.diag_const_of_transitive` | yes | yes | yes | - | `#print axioms InnerProductFable.SectorForm.diag_const_of_transitive` |
| `InnerProductFable.SectorForm.invariant_of_generated` | yes | yes | yes | - | `#print axioms InnerProductFable.SectorForm.invariant_of_generated` |
- counts toward the grade: yes

### Rust: `code/rust/src/qm/inner_product_uniqueness.rs`

- file: [code/rust/src/qm/inner_product_uniqueness.rs](../../../code/rust/src/qm/inner_product_uniqueness.rs)
- sha256 (`bytes`): `3288c2617990e81fef8a9796a537a60c3f639a1eedc3c373d6860ae59a94fdd7`
- cited in: node.rust, record TFQ-1001

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `generated_transitivity_certificate` (rust_symbol) | yes | yes | yes | - | - |
| `invariance_certificate` (rust_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/08_l1_to_l2/tfq_1001_l1_imp_sector_symmetry_law.md`

- file: [dag/derivations/08_l1_to_l2/tfq_1001_l1_imp_sector_symmetry_law.md](../../../dag/derivations/08_l1_to_l2/tfq_1001_l1_imp_sector_symmetry_law.md)
- sha256 (`lf-normalised`): `0d3cdcd6acfc10d68f457153b473376e056fafe22b208761d40d666b464b312b`
- generated view: listed, not counted
- cited in: record TFQ-1001
- counts toward the grade: no

### Documents and data: `dag/results/L1-IMP-HILBERT-INNER-PRODUCT/runs/20261021T013500Z_sector_form/README.md`

- file: [dag/results/L1-IMP-HILBERT-INNER-PRODUCT/runs/20261021T013500Z_sector_form/README.md](../../../dag/results/L1-IMP-HILBERT-INNER-PRODUCT/runs/20261021T013500Z_sector_form/README.md)
- sha256 (`lf-normalised`): `f01c5d2da545bc6ad4951e385352cf309587c3540bbfd691fecf7192550beba4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/results/L1-IMP-HILBERT-INNER-PRODUCT/runs/20261021T013500Z_sector_form/review.md`

- file: [dag/results/L1-IMP-HILBERT-INNER-PRODUCT/runs/20261021T013500Z_sector_form/review.md](../../../dag/results/L1-IMP-HILBERT-INNER-PRODUCT/runs/20261021T013500Z_sector_form/review.md)
- sha256 (`lf-normalised`): `cc48bb4ba0e11dcfb32347c3e852fc453509ebda36518d3f8976b5bf808804bc`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (0):


Outgoing (1):

- `L1-R-INNER-PRODUCT-SECTOR-FORM` `CONDITIONAL_ON_IMPORT`: [L1-IMP-HILBERT-INNER-PRODUCT](L1-IMP-HILBERT-INNER-PRODUCT.md) (CONDITIONAL)

No incoming route.
