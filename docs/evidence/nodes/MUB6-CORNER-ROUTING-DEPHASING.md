# MUB6-CORNER-ROUTING-DEPHASING

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Every 6x6 complex Hadamard matrix is Hadamard-equivalent to a dephased complex Hadamard matrix D, and D falls into the corner-determinant zero or nonzero case, each assigned a component label.

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

The labels carry no parameters or family realization; FullModuliClassification follows only from FiveBranchRealizationHypothesis, and the superseded notice withdraws reading this as routing to certified components.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-ATLAS-CORNER-ROUTING claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/MasterClassification.lean`

- file: [lean4/MasterClassification.lean](../../../lean4/MasterClassification.lean)
- sha256 (`bytes`): `cbfd11e4e0038f1a3deb5c51c8079d1c28f7e5fad3d189b3296239b50507ccc3`
- cited in: node.lean, record TFQ-1266
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `MasterClassification`): recorded sha256 `cbfd11e4e0038f1a3deb5c51c8079d1c28f7e5fad3d189b3296239b50507ccc3` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build MasterClassification`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `corner_routing_classification` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms corner_routing_classification` |
| `dephase_and_route_corner` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms dephase_and_route_corner` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1266_mub6_corner_routing_dephasing.md`

- file: [dag/derivations/25_mub/tfq_1266_mub6_corner_routing_dephasing.md](../../../dag/derivations/25_mub/tfq_1266_mub6_corner_routing_dephasing.md)
- sha256 (`lf-normalised`): `faafeae2c46fa4323b660adb1eeb9cde6e0b55db15047c9f2a94e31647b8c815`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1266
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6_global_proof_atlas.md`

- file: [papers/core/mub6/mub6_global_proof_atlas.md](../../../papers/core/mub6/mub6_global_proof_atlas.md)
- sha256 (`lf-normalised`): `94d599e65738f154ef0604e436b2e084b04c879c965f6015916781ef857a1209`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/research/superseded_notice.md`

- file: [papers/core/mub6/research/superseded_notice.md](../../../papers/core/mub6/research/superseded_notice.md)
- sha256 (`lf-normalised`): `c8db943e608d0b63ed08307fbb5af4f56f35ef216c5b5428a689118cfc2438c0`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-CORNER-ROUTING-DEPHASING` `DERIVED_LEAN`: [MUB6-QUARTET-RAW-HADAMARD-TRANSPORT](MUB6-QUARTET-RAW-HADAMARD-TRANSPORT.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-MUB6-FIVE-BRANCH-ROUTING-CLAIM` `GAP_NO_DERIVATION`: [MUB6-FIVE-BRANCH-ROUTING-CLAIM](MUB6-FIVE-BRANCH-ROUTING-CLAIM.md) (OPEN)
