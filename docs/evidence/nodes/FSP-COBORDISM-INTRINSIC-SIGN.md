# FSP-COBORDISM-INTRINSIC-SIGN

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claimed: a 4D boundary fermion theory with nontrivial invariant exp(2 pi i eta) in Omega_5^Spin(B Z2) has an unremovable sign problem curable only by a 5D bulk; no computation of the bordism group, eta invariant or sign obstruction exists in this checkout.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 12
- distinct cited Lean declarations covered by a current replay receipt: 12
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Only diagonal vertex-sign switching on one three-cycle is classified. No spin bordism group, eta invariant, fermion representation, bulk cancellation or obstruction over all representations is computed. The original cobordism-based intrinsic-sign claim remains open. Original target retained as an obligation: Claimed: a 4D boundary fermion theory with nontrivial invariant exp(2 pi i eta) in Omega_5^Spin(B Z2) has an unremovable sign problem curable only by a 5D bulk; no computation of the bordism group, eta invariant or sign obstruction exists in this checkout. Prior boundary: Relate the anomaly invariant to the sign of a declared finite representation and rule out every representation in a stated class; anomaly-based intrinsic sign results in the literature are class specific.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-047 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/SignedTriangleSwitching.lean`

- file: [lean4/SignedTriangleSwitching.lean](../../../lean4/SignedTriangleSwitching.lean)
- sha256 (`bytes`): `4ffc345ebf79bff4b3ad6ecc5ecbcecf84681f0373a6a95d8a86f1e81381beb8`
- cited in: node.lean, receipt dag/research/campaign_fsp-cobordism-intrinsic-sign_lean_replay.json (SignedTriangleSwitching), record TFQ-1211
- replay: `verified`
  - receipt [dag/research/campaign_fsp-cobordism-intrinsic-sign_lean_replay.json](../../../dag/research/campaign_fsp-cobordism-intrinsic-sign_lean_replay.json) (module `SignedTriangleSwitching`): recorded sha256 `4ffc345ebf79bff4b3ad6ecc5ecbcecf84681f0373a6a95d8a86f1e81381beb8` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build SignedTriangleSwitching`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `SignedTriangleSwitching.Signs` | yes | yes | yes | none | `#print axioms SignedTriangleSwitching.Signs` |
| `SignedTriangleSwitching.balanced_negative_edges_are_removable` | yes | yes | yes | none | `#print axioms SignedTriangleSwitching.balanced_negative_edges_are_removable` |
| `SignedTriangleSwitching.edge_product_is_cycle_sign` | yes | yes | yes | none | `#print axioms SignedTriangleSwitching.edge_product_is_cycle_sign` |
| `SignedTriangleSwitching.explicit_negative_cycle` | yes | yes | yes | none | `#print axioms SignedTriangleSwitching.explicit_negative_cycle` |
| `SignedTriangleSwitching.negative_cycle_obstruction` | yes | yes | yes | none | `#print axioms SignedTriangleSwitching.negative_cycle_obstruction` |
| `SignedTriangleSwitching.parity` | yes | yes | yes | none | `#print axioms SignedTriangleSwitching.parity` |
| `SignedTriangleSwitching.parity_invariant` | yes | yes | yes | none | `#print axioms SignedTriangleSwitching.parity_invariant` |
| `SignedTriangleSwitching.positive` | yes | yes | yes | none | `#print axioms SignedTriangleSwitching.positive` |
| `SignedTriangleSwitching.positive_switching_iff` | yes | yes | yes | none | `#print axioms SignedTriangleSwitching.positive_switching_iff` |
| `SignedTriangleSwitching.sign` | yes | yes | yes | none | `#print axioms SignedTriangleSwitching.sign` |
| `SignedTriangleSwitching.switched` | yes | yes | yes | none | `#print axioms SignedTriangleSwitching.switched` |
| `SignedTriangleSwitching.switching_normal_form` | yes | yes | yes | none | `#print axioms SignedTriangleSwitching.switching_normal_form` |

- counts toward the grade: yes

### Python: `checks/independent/fsp-cobordism-intrinsic-sign.py`

- file: [checks/independent/fsp-cobordism-intrinsic-sign.py](../../../checks/independent/fsp-cobordism-intrinsic-sign.py)
- sha256 (`bytes`): `f3b7bf730dfeca78e102054fbae9b6df8493110d91ebce7567f75db85535f078`
- cited in: record TFQ-1211
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1211_fsp_cobordism_intrinsic_sign.md`

- file: [dag/derivations/26_fsp/tfq_1211_fsp_cobordism_intrinsic_sign.md](../../../dag/derivations/26_fsp/tfq_1211_fsp_cobordism_intrinsic_sign.md)
- sha256 (`lf-normalised`): `8f1d8611a1c568dffabaf7a99913395b6369c2691f36ab04f15be541e6e43f4d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1211
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-cobordism-intrinsic-sign.md`

- file: [dag/derivations/independent/fsp-cobordism-intrinsic-sign.md](../../../dag/derivations/independent/fsp-cobordism-intrinsic-sign.md)
- sha256 (`lf-normalised`): `4663accaae381d3f99c27d47e1e28b7bc02bbcc037b53148e58598fcbb562303`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-cobordism-intrinsic-sign_lean_replay.json`

- file: [dag/research/campaign_fsp-cobordism-intrinsic-sign_lean_replay.json](../../../dag/research/campaign_fsp-cobordism-intrinsic-sign_lean_replay.json)
- sha256 (`lf-normalised`): `7e1a5f8db3cca1ab668bb4c88914d71f2f199cbf35be269cde266f749ee12fff`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign.md)
- sha256 (`lf-normalised`): `f894f295fb17dc831f4e961602bea56223bf79ae6b34c3350cfa6fe358789808`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md`

- file: [papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md](../../../papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md)
- sha256 (`lf-normalised`): `0a97b32d187a99450605943866d6d4285f0bfd73dcc021c2b69911243066f2f3`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/fsp/theory_of_finite_fsp.md`

- file: [papers/core/fsp/theory_of_finite_fsp.md](../../../papers/core/fsp/theory_of_finite_fsp.md)
- sha256 (`lf-normalised`): `5a72c2f6006ea18c3362f0a63e8525b65d41898e8f1bd437b7e4c2e368c7e102`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-COBORDISM-INTRINSIC-SIGN` `GAP_NO_DERIVATION`: [FSP-BF-2GROUP-SIGN-CLAIM](FSP-BF-2GROUP-SIGN-CLAIM.md) (OPEN)

Outgoing (2):

- `APP-R-FSP-MASTER-DICHOTOMY-REFUTED` `DERIVED_PROSE`: [FSP-MASTER-DICHOTOMY-REFUTED](FSP-MASTER-DICHOTOMY-REFUTED.md) (REFUTED)
- `APP-R-FSP-REGGE-DEFICIT-ACTION` `CONDITIONAL_ON_IMPORT`: [FSP-REGGE-DEFICIT-ACTION](FSP-REGGE-DEFICIT-ACTION.md) (IMPORTED_ASSUMPTION)
