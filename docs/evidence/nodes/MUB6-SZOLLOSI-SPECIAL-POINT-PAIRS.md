# MUB6-SZOLLOSI-SPECIAL-POINT-PAIRS

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> At the Szollosi point (x,y,u,v) = (1,-1,1,i), the 120 real rays given by an exact rational parametrization of unit vectors unbiased to I and S are nonsingular and all 7,140 pairs satisfy ||\<z,w\>|^2 - 6| \> 47/100, so no two represented rays are unbiased.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `computational_no_runnable_test`: 2 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

None recorded.

## Bottleneck

Completeness of the represented ray set needs an independent bound on the number of complex solutions; the ledger records no replay on 2026-10-16 (python-flint and PARI/GP); one point does not cover the family.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-C41 claims COMPUTATIONALLY_CHECKED; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Python: `papers/core/mub6/research/five_derivations_20261015/replay_rur.py`

- file: [papers/core/mub6/research/five_derivations_20261015/replay_rur.py](../../../papers/core/mub6/research/five_derivations_20261015/replay_rur.py)
- sha256 (`bytes`): `cb9c8ac2bfa524dcb7667ba3cccb0edc1db8098b78e80882e5216150d6a53094`
- cited in: record TFQ-1275

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `check_pairs` (python_symbol) | yes | yes | yes | - | - |
| `check_parametrization` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1275_mub6_szollosi_special_point_pairs.md`

- file: [dag/derivations/25_mub/tfq_1275_mub6_szollosi_special_point_pairs.md](../../../dag/derivations/25_mub/tfq_1275_mub6_szollosi_special_point_pairs.md)
- sha256 (`lf-normalised`): `ba61a5766df1239a2f9e83ebe14159609a23313a4efbd4fd5c9ed6c3dbf9cdb0`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1275
- counts toward the grade: no

### Documents and data: `papers/core/mub6/artifacts/mub6_szollosi_t5_cover_receipt.json`

- file: [papers/core/mub6/artifacts/mub6_szollosi_t5_cover_receipt.json](../../../papers/core/mub6/artifacts/mub6_szollosi_t5_cover_receipt.json)
- sha256 (`lf-normalised`): `7ac57afc7fbd2c35c510223bb70ab91b2ee7f50cdae7ba798fdfebfcca0bf5fb`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/mub6_claim_ledger.md`

- file: [papers/core/mub6/mub6_claim_ledger.md](../../../papers/core/mub6/mub6_claim_ledger.md)
- sha256 (`lf-normalised`): `6708883b9f1ed33cc93d794d2c7c50484f0f8e075e4576c2eaa74fadf6fbf842`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/research/szollosi_vectors/README.md`

- file: [papers/core/mub6/research/szollosi_vectors/README.md](../../../papers/core/mub6/research/szollosi_vectors/README.md)
- sha256 (`lf-normalised`): `a9115bd04bd2e7e9101dc906441a29f1b2a3e53cc1bb077fc8679c443440d7e6`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-SZOLLOSI-SPECIAL-POINT-PAIRS` `COMPUTED`: [MUB6-SZOLLOSI-COMMON-RAYS](MUB6-SZOLLOSI-COMMON-RAYS.md) (PROVED_LEAN), [MUB6-SZOLLOSI-TWO-CIRCULANT](MUB6-SZOLLOSI-TWO-CIRCULANT.md) (PROVED_LEAN)

Outgoing (0):

