# MUB6-COMMUTATIVE-FLAT-REAL-POINT

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For a normalized real functional on polynomials whose degree-two coordinate moment matrix is positive semidefinite with rank equal to the degree-one matrix, there is a real point at which every quadratic-span polynomial p with L(p^2) = 0 vanishes.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

An extraction theorem; it says nothing about whether such a functional exists for the MUB(6) system.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-C35 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/CommutativeFlatMoments.lean`

- file: [lean4/CommutativeFlatMoments.lean](../../../lean4/CommutativeFlatMoments.lean)
- sha256 (`bytes`): `a093bd73ebaa1453cd2c08d014f9f5dbeca97f0b254c1e0a8f130deaa79677ea`
- cited in: node.lean, record TFQ-1280
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `CommutativeFlatMoments`): recorded sha256 `a093bd73ebaa1453cd2c08d014f9f5dbeca97f0b254c1e0a8f130deaa79677ea` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build CommutativeFlatMoments`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `operators_commute` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms operators_commute` |
| `real_point_of_positive_flat` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms real_point_of_positive_flat` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1280_mub6_commutative_flat_real_point.md`

- file: [dag/derivations/25_mub/tfq_1280_mub6_commutative_flat_real_point.md](../../../dag/derivations/25_mub/tfq_1280_mub6_commutative_flat_real_point.md)
- sha256 (`lf-normalised`): `7a6cbfc386d63ddd6a92c7b487858a15391de0da06c5a9f6389bc89a87ad3aba`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1280
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `edeb29b681854d6ff67bdf072e4d3163995e068973662ebb77220ba009345238`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/mub6_claim_ledger.md`

- file: [papers/core/mub6/mub6_claim_ledger.md](../../../papers/core/mub6/mub6_claim_ledger.md)
- sha256 (`lf-normalised`): `e21c9d2f20bd0e87979c8b003ab6e2c60422c19cfdd0117308db09ec10c47f7a`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-COMMUTATIVE-FLAT-REAL-POINT` `DERIVED_LEAN`: [MUB6-MOMENT-EVALUATION-FLAT](MUB6-MOMENT-EVALUATION-FLAT.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-MUB6-FOURTH-BASIS-FLAT-MOMENTS` `DERIVED_LEAN`: [MUB6-FOURTH-BASIS-FLAT-MOMENTS](MUB6-FOURTH-BASIS-FLAT-MOMENTS.md) (PROVED_LEAN)
