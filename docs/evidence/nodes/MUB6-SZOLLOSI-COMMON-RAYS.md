# MUB6-SZOLLOSI-COMMON-RAYS

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a raw 6x6 complex Hadamard H, H completes to a raw quartet iff two bases of common rays of I and H are raw-unbiased to each other; in particular, if no two common rays z, w have |\<z,w\>|^2 = 6, then H has no raw quartet.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 2 Lean reference(s) cited, 2 in this checkout (replay: none 2). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

Exclusion needs the full set of common rays for each H; it is computed only at one special point (MUB6-C41).

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-C40 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/SzollosiCommonRays.lean`

- file: [lean4/SzollosiCommonRays.lean](../../../lean4/SzollosiCommonRays.lean)
- sha256 (`bytes`): `830f5016cbab23811de1d03fb02c7eef5846e5af3ae91ada2830ea2fdbf1298c`
- cited in: node.lean, record TFQ-1274
- replay: `none`
- check: `cd lean4 && lake build SzollosiCommonRays`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `no_quartet_of_no_unbiased_ray_pair` | yes | yes | yes | - | `#print axioms no_quartet_of_no_unbiased_ray_pair` |
| `quartet_iff_ray_bases` | yes | yes | yes | - | `#print axioms quartet_iff_ray_bases` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1274_mub6_szollosi_common_rays.md`

- file: [dag/derivations/25_mub/tfq_1274_mub6_szollosi_common_rays.md](../../../dag/derivations/25_mub/tfq_1274_mub6_szollosi_common_rays.md)
- sha256 (`lf-normalised`): `a19a138d674cd4971b3597062d6242e3fcad11a14e14e00bfd7b77c2578630c0`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1274
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6_claim_ledger.md`

- file: [papers/core/mub6/mub6_claim_ledger.md](../../../papers/core/mub6/mub6_claim_ledger.md)
- sha256 (`lf-normalised`): `e21c9d2f20bd0e87979c8b003ab6e2c60422c19cfdd0117308db09ec10c47f7a`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-SZOLLOSI-COMMON-RAYS` `DERIVED_LEAN`: [MUB6-QUARTET-RAW-HADAMARD-TRANSPORT](MUB6-QUARTET-RAW-HADAMARD-TRANSPORT.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-MUB6-SZOLLOSI-SPECIAL-POINT-PAIRS` `COMPUTED`: [MUB6-SZOLLOSI-SPECIAL-POINT-PAIRS](MUB6-SZOLLOSI-SPECIAL-POINT-PAIRS.md) (COMPUTATIONALLY_CHECKED)
