# PGW-SN-E21-REPAIR-RANK

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_PROSE`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Example E21 takes vertices a, b, c, d and edges (ab, bc, ac, cd, da), so the 1-cycle space has dimension 5 − rank ∂₁ = 5 − 3 = 2, with z₁ = (1,1,−1,0,0) for triangle abc and z₂ = (0,0,1,1,1) for triangle acd. Adjoining two faces with boundaries z₁ and z₂ gives rank ∂₂ = 2, ∂₁∂₂ = 0 and H₁ = 0. Adjoining two free degree-two generators with the same boundary z₁ gives rank ∂₂ = 1 and dim H₁ = 1, so the receipt count is 2 while the repair rank is 1. Transport from orientation ca to the common basis edge ac needs e_ca = −e_ac, and a wrong sign gives ∂₁z ≠ 0.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

- `proved_prose_no_in_repo_document`: no in-repo non-generated document among the counted sources. PROVED_PROSE with no in-repo source document cited.

## Imported structure

None recorded.

## Bottleneck

The duplicate case is a chain-complex extension with two free generators, not two copies of one simplex; the page is a written finite example that grammar cases do not verify, and it does not establish 4D Regge gravity or a Bianchi identity.

## Source status

002_oesn levels/level_21 (E21 written finite example); curriculum.md Lesson 8

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0527_sn_e21_repair_rank.md`

- file: [dag/derivations/05_mssn_sn/tfq_0527_sn_e21_repair_rank.md](../../../dag/derivations/05_mssn_sn/tfq_0527_sn_e21_repair_rank.md)
- sha256 (`lf-normalised`): `7973ef9da15cc5a3c660defaedde18381d6dda52f14b51f73c260a296e2da027`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0527
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:07dcae5e71386c1a44b8b6d660e80887b4d30c4671ed0c2ac97df6d141e17905:42-47`
- `external:sha256:07dcae5e71386c1a44b8b6d660e80887b4d30c4671ed0c2ac97df6d141e17905:49-55`
- `external:sha256:a51ceb8d0d5703baac230c14caa4638cf25f3ae46fdc77013c7e09f27caaa1e9:163-166`

## Absences recorded by the TFQ records

- TFQ-0527 lean4: no Lean statement of E21 in the S(n) strand
- TFQ-0527 python: no Python check of E21 in the S(n) strand
- TFQ-0527 rust: no Rust check of E21 in the S(n) strand

## Routes

Incoming (1):

- `PGW-R-SN-E21-REPAIR-RANK` `DERIVED_PROSE`: [PGW-SN-E12-CIRCULATION-FUNCTIONAL](PGW-SN-E12-CIRCULATION-FUNCTIONAL.md) (PROVED_LEAN)

Outgoing (0):

