# MAJ-IMPORT-ISING-ANYONS

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `IMPORTED_ASSUMPTION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The Ising model {1, sigma, psi} with sigma x sigma = 1 + psi, sigma x psi = sigma, psi x psi = 1 and the R, F data R = e^{-i pi/8} diag(1, i), F = (1/sqrt2)\[\[1,1\],\[1,-1\]\] on the four-sigma fusion space are imported; Ising braiding alone yields only Clifford operations, classically simulable by Gottesman-Knill, so magic-state inputs are required for a complete gate set.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Ising anyon fusion, F and R data (Nayak et al. 2008)
- Clifford-only braiding and Gottesman-Knill simulability

## Bottleneck

No claim of physical anyon braiding is made; the braid-matrix identities are the open check MAJ-ISING-BRAID-CHECK.

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-C7 claims DEFINITION; audited status IMPORTED_ASSUMPTION

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/majorana/lean4/MajoranaCore.lean`

- file: [papers/core/majorana/lean4/MajoranaCore.lean](../../../papers/core/majorana/lean4/MajoranaCore.lean)
- sha256 (`bytes`): `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071`
- cited in: node.lean, record TFQ-1170
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_majorana.json](../../../dag/research/lean_replay_campaign_majorana.json) (module `papers.core.majorana.lean4.MajoranaCore`): recorded sha256 `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `IsingAnyon` | yes | yes | yes | module-level | `#print axioms IsingAnyon` |
| `ising_quantum_dim_squared` | yes | yes | yes | module-level | `#print axioms ising_quantum_dim_squared` |
- counts toward the grade: yes

### Rust: `code/rust/src/fusion_categories/catalog.rs`

- file: [code/rust/src/fusion_categories/catalog.rs](../../../code/rust/src/fusion_categories/catalog.rs)
- sha256 (`bytes`): `0aa0caac8a1af06d892120b3f1b1b49a81620d76239768d205f2e79358ed687b`
- cited in: node.rust, record TFQ-1170

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ising` (rust_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1170_maj_import_ising_anyons.md`

- file: [dag/derivations/28_majorana/tfq_1170_maj_import_ising_anyons.md](../../../dag/derivations/28_majorana/tfq_1170_maj_import_ising_anyons.md)
- sha256 (`lf-normalised`): `e69908743cac38e5e45e957fdaf4d99dfea795613164d218909855508cbc5069`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1170
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `e92416bb1739e51de20a8ad6a26d4b5f3d76b974d7556507b13149b29e8edb47`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/majorana/the_majorana_problem_claim_ledger.md`

- file: [papers/core/majorana/the_majorana_problem_claim_ledger.md](../../../papers/core/majorana/the_majorana_problem_claim_ledger.md)
- sha256 (`lf-normalised`): `2d2b91881568780f56d7cdb53c97eec42bbfa09c21b2f1c6302665a79aad7565`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-IMPORT-ISING-ANYONS` `CONDITIONAL_ON_IMPORT`: [MAJ-HARDWARE-NARRATIVE-QUARANTINE](MAJ-HARDWARE-NARRATIVE-QUARANTINE.md) (DEFINITION), [TFQ-0043](TFQ-0043.md) (COMPUTATIONALLY_CHECKED)

Outgoing (2):

- `APP-R-MAJ-ISING-BRAID-EXACT-OPEN` `GAP_NO_DERIVATION`: [MAJ-ISING-BRAID-EXACT-OPEN](MAJ-ISING-BRAID-EXACT-OPEN.md) (OPEN)
- `APP-R-MAJ-MAJORANA-BRAID-YB-EXACT` `COMPUTED`: [MAJ-MAJORANA-BRAID-YB-EXACT](MAJ-MAJORANA-BRAID-YB-EXACT.md) (COMPUTATIONALLY_CHECKED)
