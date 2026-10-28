# OPS-RUST-RECEIPTS-AND-LIMITS

Stage: [OBSERVER_PRESHEAF](../stages/OBSERVER_PRESHEAF.md). Status: `CONDITIONAL`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> As the ledger states them for the Rust module empirical_presheaf. (B15) The l1 defect receipt has zero duality gap: \<phi*, e\> + y0 equals the defect, with the sup norm of phi* at most 1 and A^T phi* + y0 \<= 0, and replay rejects tampering and shape errors. (B17) verify_noncontextual_fraction and verify_l1_defect_receipt rebuild the linear programme, verify the embedded solution as its certificate, and bind primal, dual and value to the receipt's part, functional and fraction; the pivot trace is not bound. (B16) Every global and local section count is a checked fold against MAX_GLOBAL_ASSIGNMENTS = 2^20 returning EnumerationLimit, and dense allocations are bounded by MAX_LP_ENTRIES = 2^22 returning LpSizeLimit, with nothing of either size allocated or enumerated before the refusal: 64 binary singletons have 2^64 assignments and one context of 21 binary measurements has 2^21 sections, both above 2^20, while ten binary singletons give a 20 x 1024 incidence inside both ceilings. (B9, shape) The whole declared cochain is shape-checked before any incidence is read. Recomputed here: the ceiling arithmetic, and a zero-gap primal and dual pair for the PR box and the noisy boxes in the independent script's own solver, which does not test the Rust verifiers.

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

The Lean statement is the narrowed ceiling arithmetic above. The Rust receipt replay, tamper rejection, shape check, zero-gap dual certificate, PR box, noisy boxes, and the functions verify_noncontextual_fraction and verify_l1_defect_receipt are not run here. The in-repo module uses solvers, an external crate that is not a workspace member.

## Source status

Ledger rows L035-B15, L035-B16 and L035-B17, and the shape clause of L035-B9, stay outside this statement. The Rust tests that name them are not run in this repository. Narrowed to the ceiling counts G = 2^20 and L = 2^22, checked in Lean 4.35.0 with no axioms. Held at CONDITIONAL because those Rust tests are not run here.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/ObserverPresheafReceiptLimits.lean`

- file: [lean4/ObserverPresheafReceiptLimits.lean](../../../lean4/ObserverPresheafReceiptLimits.lean)
- sha256 (`bytes`): `e7f9d80c2edcf7fa3b94ae44f0a345c42ad37a37d91ad0c09c2b34a0c4b96514`
- cited in: node.lean, node.source, receipt dag/research/campaign_ops-rust-receipts-and-limits_lean_replay.json (ObserverPresheafReceiptLimits), receipt dag/research/foc035_observer_presheaf_lean_replay.json (ObserverPresheafReceiptLimits), receipt dag/research/pr_392_round2_replay.json (ObserverPresheafReceiptLimits), record TFQ-2519
- replay: `verified`
  - receipt [dag/research/campaign_ops-rust-receipts-and-limits_lean_replay.json](../../../dag/research/campaign_ops-rust-receipts-and-limits_lean_replay.json) (module `ObserverPresheafReceiptLimits`): recorded sha256 `e7f9d80c2edcf7fa3b94ae44f0a345c42ad37a37d91ad0c09c2b34a0c4b96514` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/foc035_observer_presheaf_lean_replay.json](../../../dag/research/foc035_observer_presheaf_lean_replay.json) (module `ObserverPresheafReceiptLimits`): recorded sha256 `e7f9d80c2edcf7fa3b94ae44f0a345c42ad37a37d91ad0c09c2b34a0c4b96514` matches the current file; exit code 0; Lean Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
  - receipt [dag/research/pr_392_round2_replay.json](../../../dag/research/pr_392_round2_replay.json) (module `ObserverPresheafReceiptLimits`): recorded sha256 `e7f9d80c2edcf7fa3b94ae44f0a345c42ad37a37d91ad0c09c2b34a0c4b96514` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build ObserverPresheafReceiptLimits`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `ObserverPresheafReceiptLimits.maxGlobal_eq_decimal` | yes | yes | yes | none | `#print axioms ObserverPresheafReceiptLimits.maxGlobal_eq_decimal` |
| `ObserverPresheafReceiptLimits.maxGlobal_eq_pow` | yes | yes | yes | none | `#print axioms ObserverPresheafReceiptLimits.maxGlobal_eq_pow` |
| `ObserverPresheafReceiptLimits.maxLp_eq_decimal` | yes | yes | yes | none | `#print axioms ObserverPresheafReceiptLimits.maxLp_eq_decimal` |
| `ObserverPresheafReceiptLimits.maxLp_eq_pow` | yes | yes | yes | none | `#print axioms ObserverPresheafReceiptLimits.maxLp_eq_pow` |
| `ObserverPresheafReceiptLimits.sixty_four_assignments_above` | yes | yes | yes | none | `#print axioms ObserverPresheafReceiptLimits.sixty_four_assignments_above` |
| `ObserverPresheafReceiptLimits.ten_assignments` | yes | yes | yes | none | `#print axioms ObserverPresheafReceiptLimits.ten_assignments` |
| `ObserverPresheafReceiptLimits.ten_assignments_inside` | yes | yes | yes | none | `#print axioms ObserverPresheafReceiptLimits.ten_assignments_inside` |
| `ObserverPresheafReceiptLimits.ten_entries` | yes | yes | yes | none | `#print axioms ObserverPresheafReceiptLimits.ten_entries` |
| `ObserverPresheafReceiptLimits.ten_entries_inside` | yes | yes | yes | none | `#print axioms ObserverPresheafReceiptLimits.ten_entries_inside` |
| `ObserverPresheafReceiptLimits.ten_rows` | yes | yes | yes | none | `#print axioms ObserverPresheafReceiptLimits.ten_rows` |
| `ObserverPresheafReceiptLimits.twenty_one_sections_above` | yes | yes | yes | none | `#print axioms ObserverPresheafReceiptLimits.twenty_one_sections_above` |
| `ObserverPresheafReceiptLimits.twenty_one_sections_eq` | yes | yes | yes | none | `#print axioms ObserverPresheafReceiptLimits.twenty_one_sections_eq` |

- counts toward the grade: yes

### Rust: `code/rust/src/sheaf_theory/empirical_presheaf/lp.rs`

- file: [code/rust/src/sheaf_theory/empirical_presheaf/lp.rs](../../../code/rust/src/sheaf_theory/empirical_presheaf/lp.rs)
- sha256 (`bytes`): `3c6157faba9f5aa5d5f60514decd4e2371163c701402487b7f3162320e398eec`
- cited in: node.rust, record TFQ-2519

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `bound_dense` (rust_symbol) | yes | yes | yes | - | - |
| `verify_l1_defect_receipt` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Rust: `code/rust/src/sheaf_theory/empirical_presheaf/model.rs`

- file: [code/rust/src/sheaf_theory/empirical_presheaf/model.rs](../../../code/rust/src/sheaf_theory/empirical_presheaf/model.rs)
- sha256 (`bytes`): `f3394e924037042349bc7593855651e9f470d5b57fd5512b82e7761a8e40765a`
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
- sha256 (`lf-normalised`): `81b9253321a4e6c04ffa6d18dfcda030f03f7ca005ecc42a30a68fb153c3408f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2519
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/ops-rust-receipts-and-limits.md`

- file: [dag/derivations/independent/ops-rust-receipts-and-limits.md](../../../dag/derivations/independent/ops-rust-receipts-and-limits.md)
- sha256 (`lf-normalised`): `0767b4dc5cbccc6b584e0a41bff90ca6c7d47a636f558af2b3d9e337b4c15d2f`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_ops-rust-receipts-and-limits_lean_replay.json`

- file: [dag/research/campaign_ops-rust-receipts-and-limits_lean_replay.json](../../../dag/research/campaign_ops-rust-receipts-and-limits_lean_replay.json)
- sha256 (`lf-normalised`): `52bc9ff117a8422d1255a7d7785595345dde3f353dc1e1798e9c09d203db33cb`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/foc035_observer_presheaf_lean_replay.json`

- file: [dag/research/foc035_observer_presheaf_lean_replay.json](../../../dag/research/foc035_observer_presheaf_lean_replay.json)
- sha256 (`lf-normalised`): `aa747939246b57696033aba8ac40835f9c0b8958a9d5b431634b1fc4c6952329`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/pr_392_round2_replay.json`

- file: [dag/research/pr_392_round2_replay.json](../../../dag/research/pr_392_round2_replay.json)
- sha256 (`lf-normalised`): `9297597ef300ae17134398da5ee4c86faf1552fe9f3ffb6ca6bea5ef27e559b6`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/pr_392_scope_review.json`

- file: [dag/research/pr_392_scope_review.json](../../../dag/research/pr_392_scope_review.json)
- sha256 (`lf-normalised`): `76c0b1fa74c09727bd542353a91676c73850f9962ff0201343e402d058bf4259`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/claim_ledger.md`

- file: [sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/claim_ledger.md](../../../sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/claim_ledger.md)
- sha256 (`lf-normalised`): `da99779add73314574622d0db46ea4dfbc9b66c4938caf29ab98590033592ab4`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md`

- file: [sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md](../../../sources/atlas/papers/finite_obstruction_calculus/lggr_quantum_observer_presheaf/lggr_and_the_quantum_observer_presheaf.md)
- sha256 (`lf-normalised`): `ae5564735bb6591e0f149868f83bd9f9793f297be0f8af3cc889c293ae4059cb`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `OPS-R-RUST-RECEIPTS-AND-LIMITS` `RECORD_PARENT`: [OPS-NOISY-PR-NCF](OPS-NOISY-PR-NCF.md) (COMPUTATIONALLY_CHECKED), [OPS-CECH-COBOUNDARY](OPS-CECH-COBOUNDARY.md) (PROVED_PROSE)

Outgoing (1):

- `OPS-R-REFUTED-EARLIER-RUST` `RECORD_PARENT`: [OPS-REFUTED-EARLIER-RUST](OPS-REFUTED-EARLIER-RUST.md) (REFUTED)
