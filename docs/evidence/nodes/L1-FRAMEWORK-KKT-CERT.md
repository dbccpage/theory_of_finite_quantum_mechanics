# L1-FRAMEWORK-KKT-CERT

Stage: [L1_EMERGENCE](../stages/L1_EMERGENCE.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> A finite primal-dual certificate (potential h, annihilating dual witness) certifies l1 optimality of the quotient residual. Lean covers integer-list instances; the real-vector statement is prose.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 1
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 2 Lean reference(s) cited, 1 in this checkout (replay: none 1). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Integer-list scope. The 3-step iterator in the same paper is REFUTED per its ledger.

## Source status

Thm 4.2 finite KKT certificate; Lean general_finite_certificate_optimality (integer lists)

## Review

- PFP review: [dag/results/L1-FRAMEWORK-KKT-CERT/reviews/20261019_l1_import_audit/delivery_review_result.json](../../../dag/results/L1-FRAMEWORK-KKT-CERT/reviews/20261019_l1_import_audit/delivery_review_result.json); file present and sha256 matches the node's record: yes; verdict `scoped_result_or_obstruction_reviewed`; scope effect `consistent`; prior status `PROVED_LEAN`; qualifies for E4: yes.
  - narrowest claim: Exact supplied primal/dual certificate predicates for a triangle, with accepted and capacity/divergence/gap failures; generic rational bound-to-optimality implication in Lean.
  - does not support: Prove representation refinement to the external arbitrary-list integer certificate and arbitrary real-vector attainment. A valid numeric triangle certificate does not establish unrestricted dual attainment.
  - next test: Prove representation refinement to the external arbitrary-list integer certificate and arbitrary real-vector attainment. A valid numeric triangle certificate does not establish unrestricted dual attainment.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DerivationDagQMClosure.lean`

- file: [lean4/DerivationDagQMClosure.lean](../../../lean4/DerivationDagQMClosure.lean)
- sha256 (`bytes`): `c9ad9c23a460d7a791d7a22180c2b552f066d11150b391e5241ef20687bd8154`
- cited in: node.lean
- replay: `none`
- check: `cd lean4 && lake build DerivationDagQMClosure`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed` | yes | yes | yes | - | `#print axioms QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed` |
- counts toward the grade: yes

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/003_l1_obstruction_framework/lean4/lp_general_certificate.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/003_l1_obstruction_framework/lean4/lp_general_certificate.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean, node.source
- counts toward the grade: no

### Rust: `code/rust/src/wdp/fenchel_duality.rs`

- file: [code/rust/src/wdp/fenchel_duality.rs](../../../code/rust/src/wdp/fenchel_duality.rs)
- sha256 (`bytes`): `ca7fe2172744dc3952b90c9367a64e649d4b0b46fc81b9471e5f79e6dde41df8`
- cited in: record TFQ-0351
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: yes

### Rust: `code/rust/src/wdp/obstruction.rs`

- file: [code/rust/src/wdp/obstruction.rs](../../../code/rust/src/wdp/obstruction.rs)
- sha256 (`bytes`): `d4a9514b3ee22c73ac47193206838c49cd5d908485d2c38dd026cd3bd9416cf8`
- cited in: record TFQ-0351
- note: no test is cited for this symbol; its crate is tfqm_wdp
- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`

- file: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_wdp/src/fenchel_duality.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/fenchel_duality.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_wdp/src/obstruction.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/obstruction.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/07_l1_emergence/tfq_0351_accept_an_integer_finite_list_certificate_only_inside_its_capacity_circulation_feasibility.md`

- file: [dag/derivations/07_l1_emergence/tfq_0351_accept_an_integer_finite_list_certificate_only_inside_its_capacity_circulation_feasibility.md](../../../dag/derivations/07_l1_emergence/tfq_0351_accept_an_integer_finite_list_certificate_only_inside_its_capacity_circulation_feasibility.md)
- sha256 (`lf-normalised`): `91d69f16d86f87bb85e3b6a77d66a336dc667a588b82d8215d405dec79f5cfe6`
- generated view: listed, not counted
- cited in: record TFQ-0351
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/003_l1_obstruction_framework/l1_obstruction_framework_claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/003_l1_obstruction_framework/l1_obstruction_framework_claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

## Routes

Incoming (1):

- `L1-R-KKT` `DERIVED_LEAN`: [L1-WDP-WINDOW-PHI1-GAMMA2](L1-WDP-WINDOW-PHI1-GAMMA2.md) (DEFINITION), [L1-CHAIN-D1D0-AXIOM](L1-CHAIN-D1D0-AXIOM.md) (ADMITTED_PRIMITIVE)

Outgoing (1):

- `L1-R-DENSITY-LIFT-PUB009` `DERIVED_LEAN`: [L1-DENSITY-LIFT-SIGNED-SQRT-PUB009](L1-DENSITY-LIFT-SIGNED-SQRT-PUB009.md) (PROVED_LEAN)
