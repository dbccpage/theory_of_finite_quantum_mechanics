# FSP-BF-2GROUP-SIGN-CLAIM

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `OPEN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Claimed: in BF theory on finite cell complexes, the Postnikov class in H^3(G, A) governs cancellation of higher 2-group sign anomalies on knotted worldsheets; no BF model, linking computation or cancellation identity exists in this checkout.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 11
- distinct cited Lean declarations covered by a current replay receipt: 11
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

The result concerns the explicitly defined Z2 cochain model and normalized rephasings. It constructs no BF state sum, 2-group gauge dynamics, knotted-worldsheet amplitude or three-loop braiding observable. No general cancellation or sign-free theorem follows. Original target retained as an obligation: Claimed: in BF theory on finite cell complexes, the Postnikov class in H^3(G, A) governs cancellation of higher 2-group sign anomalies on knotted worldsheets; no BF model, linking computation or cancellation identity exists in this checkout. Prior boundary: Define the finite BF or 2-group gauge model, compute the 3-loop braiding phases and state exactly which weights become nonnegative; ledger GIN-C19 to GIN-C21 withdraw the fixture readings.

## Source status

papers/core/fsp/theory_of_finite_fsp.jsonl record FSP-DERIV-046 claims PROVED_LEAN; audited status OPEN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/BfCocycleObstruction.lean`

- file: [lean4/BfCocycleObstruction.lean](../../../lean4/BfCocycleObstruction.lean)
- sha256 (`bytes`): `0712dd42cc8b6cb9a67184f6759604bc93eed8d5d46a50a725cdb87a2a5e15b0`
- cited in: node.lean, receipt dag/research/campaign_fsp-bf-2group-sign-claim_lean_replay.json (BfCocycleObstruction), record TFQ-1210
- replay: `verified`
  - receipt [dag/research/campaign_fsp-bf-2group-sign-claim_lean_replay.json](../../../dag/research/campaign_fsp-bf-2group-sign-claim_lean_replay.json) (module `BfCocycleObstruction`): recorded sha256 `0712dd42cc8b6cb9a67184f6759604bc93eed8d5d46a50a725cdb87a2a5e15b0` matches the current file; exit code 0; Lean 4.35.0; Mathlib `-`; axiom audit passed: yes; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build BfCocycleObstruction`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `BfCocycleObstruction.Normalized` | yes | yes | yes | none | `#print axioms BfCocycleObstruction.Normalized` |
| `BfCocycleObstruction.coboundary` | yes | yes | yes | none | `#print axioms BfCocycleObstruction.coboundary` |
| `BfCocycleObstruction.cocycle` | yes | yes | yes | none | `#print axioms BfCocycleObstruction.cocycle` |
| `BfCocycleObstruction.cocycle_identity` | yes | yes | yes | none | `#print axioms BfCocycleObstruction.cocycle_identity` |
| `BfCocycleObstruction.generator_sign_survives_rephasing` | yes | yes | yes | propext | `#print axioms BfCocycleObstruction.generator_sign_survives_rephasing` |
| `BfCocycleObstruction.no_normalized_rephasing_makes_all_signs_positive` | yes | yes | yes | propext | `#print axioms BfCocycleObstruction.no_normalized_rephasing_makes_all_signs_positive` |
| `BfCocycleObstruction.normalized_coboundary_at_generator` | yes | yes | yes | propext | `#print axioms BfCocycleObstruction.normalized_coboundary_at_generator` |
| `BfCocycleObstruction.normalized_cocycle` | yes | yes | yes | none | `#print axioms BfCocycleObstruction.normalized_cocycle` |
| `BfCocycleObstruction.not_a_normalized_coboundary` | yes | yes | yes | propext | `#print axioms BfCocycleObstruction.not_a_normalized_coboundary` |
| `BfCocycleObstruction.rephase` | yes | yes | yes | none | `#print axioms BfCocycleObstruction.rephase` |
| `BfCocycleObstruction.sign` | yes | yes | yes | none | `#print axioms BfCocycleObstruction.sign` |

- counts toward the grade: yes

### Python: `checks/independent/fsp-bf-2group-sign-claim.py`

- file: [checks/independent/fsp-bf-2group-sign-claim.py](../../../checks/independent/fsp-bf-2group-sign-claim.py)
- sha256 (`bytes`): `9b1b7c5b3a3ba2735ff1e5bfa6bcd9e918f84c2281b0fa8d1c214e1fc1cf84dc`
- cited in: record TFQ-1210
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_1210_fsp_bf_2group_sign_claim.md`

- file: [dag/derivations/26_fsp/tfq_1210_fsp_bf_2group_sign_claim.md](../../../dag/derivations/26_fsp/tfq_1210_fsp_bf_2group_sign_claim.md)
- sha256 (`lf-normalised`): `7b04fa620b1e36295467311440d343c0c72abeeb84391b782012dc6870ddb9d3`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1210
- counts toward the grade: no

### Documents and data: `dag/derivations/independent/fsp-bf-2group-sign-claim.md`

- file: [dag/derivations/independent/fsp-bf-2group-sign-claim.md](../../../dag/derivations/independent/fsp-bf-2group-sign-claim.md)
- sha256 (`lf-normalised`): `a9965286126ad0ebb367fd9fa5cfad0ffdeca345c810c1ed38f4341b98caf880`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/research/campaign_fsp-bf-2group-sign-claim_lean_replay.json`

- file: [dag/research/campaign_fsp-bf-2group-sign-claim_lean_replay.json](../../../dag/research/campaign_fsp-bf-2group-sign-claim_lean_replay.json)
- sha256 (`lf-normalised`): `558f9650d8a80f2000e5bf6f26e9b5e63072b48f4f8d049b3a828b629d197ec2`
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

- `APP-R-FSP-BF-2GROUP-SIGN-CLAIM` `GAP_NO_DERIVATION`: [FSP-LAUGHLIN-EXCHANGE-PHASE](FSP-LAUGHLIN-EXCHANGE-PHASE.md) (IMPORTED_ASSUMPTION)

Outgoing (2):

- `APP-R-FSP-COBORDISM-INTRINSIC-SIGN` `GAP_NO_DERIVATION`: [FSP-COBORDISM-INTRINSIC-SIGN](FSP-COBORDISM-INTRINSIC-SIGN.md) (OPEN)
- `APP-R-FSP-XCUBE-FRACTON-MODEL` `CONDITIONAL_ON_IMPORT`: [FSP-XCUBE-FRACTON-MODEL](FSP-XCUBE-FRACTON-MODEL.md) (IMPORTED_ASSUMPTION)
