# OPS-RUST-RECEIPTS-AND-LIMITS

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `CONDITIONAL`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> As the ledger states them for the Rust module empirical_presheaf. (B15) The l1 defect receipt has zero duality gap: \<phi*, e\> + y0 equals the defect, with the sup norm of phi* at most 1 and A^T phi* + y0 \<= 0, and replay rejects tampering and shape errors. (B17) verify_noncontextual_fraction and verify_l1_defect_receipt rebuild the linear programme, verify the embedded solution as its certificate, and bind primal, dual and value to the receipt's part, functional and fraction; the pivot trace is not bound. (B16) Every global and local section count is a checked fold against MAX_GLOBAL_ASSIGNMENTS = 2^20 returning EnumerationLimit, and dense allocations are bounded by MAX_LP_ENTRIES = 2^22 returning LpSizeLimit, with nothing of either size allocated or enumerated before the refusal: 64 binary singletons have 2^64 assignments and one context of 21 binary measurements has 2^21 sections, both above 2^20, while ten binary singletons give a 20 x 1024 incidence inside both ceilings. (B9, shape) The whole declared cochain is shape-checked before any incidence is read. Recomputed here: the ceiling arithmetic, and a zero-gap primal and dual pair for the PR box and the noisy boxes in the independent script's own solver, which does not test the Rust verifiers.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 3
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The computing tests are Rust tests of the source repository. The in-repo copy of the module (code/rust/src/sheaf_theory/empirical_presheaf) uses omega_solvers, an external crate that is not a member of the code/rust workspace (cargo metadata --no-deps lists no such package), and the source test file was not imported. These tests are not run here.

## Source status

Ledger rows L035-B15, L035-B16 and L035-B17 (and the shape clause of L035-B9): computed by the Rust tests convex_hull_distance_receipt_replays_and_rejects_shape_errors, tampered_receipts_are_rejected_by_replay, pr1080_embedded_lp_corruption_is_not_silently_accepted, pr1080_oversized_global_carrier_is_refused_without_overflow and pr1080_disconnected_cochain_shape_is_still_checked. Held at CONDITIONAL because those tests are not run in this repository.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Rust: `code/rust/src/sheaf_theory/empirical_presheaf/lp.rs`

- file: [code/rust/src/sheaf_theory/empirical_presheaf/lp.rs](../../../code/rust/src/sheaf_theory/empirical_presheaf/lp.rs)
- sha256 (`bytes`): `fd449b6519d292c1b407945bbed50069995223fe20caf9a062155e1a1a56d0bb`
- cited in: node.rust, record TFQ-2519

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `bound_dense` (rust_symbol) | yes | yes | yes | - | - |
| `verify_l1_defect_receipt` (rust_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Rust: `code/rust/src/sheaf_theory/empirical_presheaf/model.rs`

- file: [code/rust/src/sheaf_theory/empirical_presheaf/model.rs](../../../code/rust/src/sheaf_theory/empirical_presheaf/model.rs)
- sha256 (`bytes`): `e810daa27f63e26cebb273fc083bef80797858f842573ba2ea837ac75d4ed06e`
- cited in: node.rust, record TFQ-2519

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `verify_noncontextual_fraction` (rust_symbol) | yes | yes | yes | - | - |
- counts toward the grade: yes

### Python: `checks/independent/foc035_observer_presheaf.py`

- file: [checks/independent/foc035_observer_presheaf.py](../../../checks/independent/foc035_observer_presheaf.py)
- sha256 (`bytes`): `6c1962e9a7e6b987ed5ba1b47afca56f17065d81fbfd2522245711b3840967ef`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2519_ops_rust_receipts_and_limits.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2519_ops_rust_receipts_and_limits.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2519_ops_rust_receipts_and_limits.md)
- sha256 (`lf-normalised`): `0a0a29e1056f5a9d300e9ca15e4fee94e6c84f807c6c0e0eb365ddfecc246bda`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2519
- counts toward the grade: no

### Documents and data: `sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md`

- file: [sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md](../../../sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/claim_ledger.md)
- sha256 (`lf-normalised`): `da99779add73314574622d0db46ea4dfbc9b66c4938caf29ab98590033592ab4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md`

- file: [sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md](../../../sources/atlas/F004_papers/001_finite_obstruction_calculus/035_lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md)
- sha256 (`lf-normalised`): `649532625cf9e8ec085a420fd1bad9227fcc4dae9f06ba02be1eb19f497e3ec7`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `OPS-R-RUST-RECEIPTS-AND-LIMITS` `RECORD_PARENT`: [OPS-NOISY-PR-NCF](OPS-NOISY-PR-NCF.md) (COMPUTATIONALLY_CHECKED), [OPS-CECH-COBOUNDARY](OPS-CECH-COBOUNDARY.md) (PROVED_PROSE)

Outgoing (1):

- `OPS-R-REFUTED-EARLIER-RUST` `RECORD_PARENT`: [OPS-REFUTED-EARLIER-RUST](OPS-REFUTED-EARLIER-RUST.md) (REFUTED)
