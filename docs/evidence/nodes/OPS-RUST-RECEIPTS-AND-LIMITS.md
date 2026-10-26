# OPS-RUST-RECEIPTS-AND-LIMITS

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> In Lean, maxGlobal is 2^20 and equals 1048576, and maxLp is 2^22 and equals 4194304. Then 2^64 \> maxGlobal, 2^21 = 2097152, and 2^21 \> maxGlobal. Also 10 * 2 = 20, 2^10 = 1024, 20 * 1024 = 20480, 2^10 \< maxGlobal, and 20 * 1024 \< maxLp. Not in this statement: a zero duality gap, a dual inequality, tamper or shape rejection, a rebuilt linear programme, a singleton census, and any Rust refusal.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 11
- cited Lean, Rust or Python symbols found in their in-repo files: 15
- distinct cited Lean declarations covered by a current replay receipt: 12
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 3
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (3 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The Lean statement is the narrowed ceiling arithmetic above. The Rust receipt replay, tamper rejection, shape check, zero-gap dual certificate, PR box, noisy boxes, and the functions verify_noncontextual_fraction and verify_l1_defect_receipt are not run here. The in-repo module uses omega_solvers, an external crate that is not a workspace member.

## Source status

Ledger rows L035-B15, L035-B16 and L035-B17, and the shape clause of L035-B9, stay outside this statement. The Rust tests that name them are not run in this repository. Narrowed to the ceiling counts G = 2^20 and L = 2^22, checked in Lean 4.35.0 with no axioms. Held at CONDITIONAL because those Rust tests are not run here.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CampaignOpsRustReceiptsAndLimits.lean`

- file: [lean4/CampaignOpsRustReceiptsAndLimits.lean](../../../lean4/CampaignOpsRustReceiptsAndLimits.lean)
- sha256 (`bytes`): `7201f9dd6fb95bf9a617fcd196c551ae680bd4b6a7f480cd159a50aad1059af0`
- cited in: node.lean, node.source, receipt dag/research/campaign_ops-rust-receipts-and-limits_lean_replay.json (CampaignOpsRustReceiptsAndLimits), receipt dag/research/foc035_observer_presheaf_lean_replay.json (CampaignOpsRustReceiptsAndLimits), receipt dag/research/pr_392_round2_replay.json (CampaignOpsRustReceiptsAndLimits), record TFQ-2519
- replay: `verified`
  - receipt [dag/research/campaign_ops-rust-receipts-and-limits_lean_replay.json](../../../dag/research/campaign_ops-rust-receipts-and-limits_lean_replay.json) (module `CampaignOpsRustReceiptsAndLimits`): recorded sha256 `7201f9dd6fb95bf9a617fcd196c551ae680bd4b6a7f480cd159a50aad1059af0` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/foc035_observer_presheaf_lean_replay.json](../../../dag/research/foc035_observer_presheaf_lean_replay.json) (module `CampaignOpsRustReceiptsAndLimits`): recorded sha256 `7201f9dd6fb95bf9a617fcd196c551ae680bd4b6a7f480cd159a50aad1059af0` matches the current file; exit code 0; Lean Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/pr_392_round2_replay.json](../../../dag/research/pr_392_round2_replay.json) (module `CampaignOpsRustReceiptsAndLimits`): recorded sha256 `7201f9dd6fb95bf9a617fcd196c551ae680bd4b6a7f480cd159a50aad1059af0` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build CampaignOpsRustReceiptsAndLimits`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `CampaignOpsRustReceiptsAndLimits.maxGlobal_eq_decimal` | yes | yes | yes | none | `#print axioms CampaignOpsRustReceiptsAndLimits.maxGlobal_eq_decimal` |
| `CampaignOpsRustReceiptsAndLimits.maxGlobal_eq_pow` | yes | yes | yes | none | `#print axioms CampaignOpsRustReceiptsAndLimits.maxGlobal_eq_pow` |
| `CampaignOpsRustReceiptsAndLimits.maxLp_eq_decimal` | yes | yes | yes | none | `#print axioms CampaignOpsRustReceiptsAndLimits.maxLp_eq_decimal` |
| `CampaignOpsRustReceiptsAndLimits.maxLp_eq_pow` | yes | yes | yes | none | `#print axioms CampaignOpsRustReceiptsAndLimits.maxLp_eq_pow` |
| `CampaignOpsRustReceiptsAndLimits.sixty_four_assignments_above` | yes | yes | yes | none | `#print axioms CampaignOpsRustReceiptsAndLimits.sixty_four_assignments_above` |
| `CampaignOpsRustReceiptsAndLimits.ten_assignments` | yes | yes | yes | none | `#print axioms CampaignOpsRustReceiptsAndLimits.ten_assignments` |
| `CampaignOpsRustReceiptsAndLimits.ten_assignments_inside` | yes | yes | yes | none | `#print axioms CampaignOpsRustReceiptsAndLimits.ten_assignments_inside` |
| `CampaignOpsRustReceiptsAndLimits.ten_entries` | yes | yes | yes | none | `#print axioms CampaignOpsRustReceiptsAndLimits.ten_entries` |
| `CampaignOpsRustReceiptsAndLimits.ten_entries_inside` | yes | yes | yes | none | `#print axioms CampaignOpsRustReceiptsAndLimits.ten_entries_inside` |
| `CampaignOpsRustReceiptsAndLimits.ten_rows` | yes | yes | yes | none | `#print axioms CampaignOpsRustReceiptsAndLimits.ten_rows` |
| `CampaignOpsRustReceiptsAndLimits.twenty_one_sections_above` | yes | yes | yes | none | `#print axioms CampaignOpsRustReceiptsAndLimits.twenty_one_sections_above` |
| `CampaignOpsRustReceiptsAndLimits.twenty_one_sections_eq` | yes | yes | yes | none | `#print axioms CampaignOpsRustReceiptsAndLimits.twenty_one_sections_eq` |

- counts toward the grade: yes

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

### Python: `checks/independent/ops-rust-receipts-and-limits.py`

- file: [checks/independent/ops-rust-receipts-and-limits.py](../../../checks/independent/ops-rust-receipts-and-limits.py)
- sha256 (`bytes`): `0cc51eaca111c9af151594f42dd889351c0faa7513bbdbf4fb83ad8844814f7e`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/35_foc035_observer_presheaf/tfq_2519_ops_rust_receipts_and_limits.md`

- file: [dag/derivations/35_foc035_observer_presheaf/tfq_2519_ops_rust_receipts_and_limits.md](../../../dag/derivations/35_foc035_observer_presheaf/tfq_2519_ops_rust_receipts_and_limits.md)
- sha256 (`lf-normalised`): `dbd7d50fa9672d292ca461e59401fb5826d39fb42dc7f2df058ebac24dc3928a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2519
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/ops-rust-receipts-and-limits.md`

- file: [dag/derivations/independent/ops-rust-receipts-and-limits.md](../../../dag/derivations/independent/ops-rust-receipts-and-limits.md)
- sha256 (`lf-normalised`): `1a80ece24abd6af2b799b2ed5ad3be87f8c1b9e136c43ea53ed9ba32de167405`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_ops-rust-receipts-and-limits_lean_replay.json`

- file: [dag/research/campaign_ops-rust-receipts-and-limits_lean_replay.json](../../../dag/research/campaign_ops-rust-receipts-and-limits_lean_replay.json)
- sha256 (`lf-normalised`): `6ed4d431e9220799b5396f69dc2dfc24fe0e80d43b51c6d7745f4b584f1a65c2`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/foc035_observer_presheaf_lean_replay.json`

- file: [dag/research/foc035_observer_presheaf_lean_replay.json](../../../dag/research/foc035_observer_presheaf_lean_replay.json)
- sha256 (`lf-normalised`): `5810e04e569b5ed7611d007c1497d7d4ee0dac3acec079a3509e4f1d2ad8944d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/pr_392_round2_replay.json`

- file: [dag/research/pr_392_round2_replay.json](../../../dag/research/pr_392_round2_replay.json)
- sha256 (`lf-normalised`): `1a4abfdd26445a36732843a3b1cb8696572f6663c2d6699e0d441fd2e8b8b25a`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/pr_392_scope_review.json`

- file: [dag/research/pr_392_scope_review.json](../../../dag/research/pr_392_scope_review.json)
- sha256 (`lf-normalised`): `ebc4b0e8dea5b73b2a0cd94665350070218664c205ada8a047e1425db9898372`
- cited in: node.source
- counts toward the grade: yes

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
