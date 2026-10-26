# MUB6-SZOLLOSI-618-SYSTEM

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> For the Szollosi two-circulant family with both additional bases arbitrary, quartet existence (at some and at each fixed admissible parameter) is equivalent to a real solution of 618 rational equations of degree at most two in 440 variables, and every solution lies in the box of radius 1 for phase and raw-basis coordinates and 3 for cross-product coordinates.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- distinct cited Lean declarations covered by a current replay receipt: 7
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Emptiness over all admissible parameters and all third bases (no_quartet_iff_all_varieties_empty) is open; the system covers quartets containing a family member only.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-C24 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/SzollosiQuadraticSystem.lean`

- file: [lean4/SzollosiQuadraticSystem.lean](../../../lean4/SzollosiQuadraticSystem.lean)
- sha256 (`bytes`): `1d985ffd763ed3de6618da8b90b591cbc48e18277729541056153dc0412eed25`
- cited in: node.lean, record TFQ-1268
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `SzollosiQuadraticSystem`): recorded sha256 `1d985ffd763ed3de6618da8b90b591cbc48e18277729541056153dc0412eed25` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build SzollosiQuadraticSystem`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `equation_degree` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms equation_degree` |
| `exists_bounded_solution_iff_quartet` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms exists_bounded_solution_iff_quartet` |
| `exists_solution_iff_quartet` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms exists_solution_iff_quartet` |
| `exists_solution_with_parameters_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms exists_solution_with_parameters_iff` |
| `solution_in_full_box` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms solution_in_full_box` |

- counts toward the grade: yes

### Lean: `lean4/SzollosiQuartetSystem.lean`

- file: [lean4/SzollosiQuartetSystem.lean](../../../lean4/SzollosiQuartetSystem.lean)
- sha256 (`bytes`): `6fa7c1b58f88056161fc9ea83fc5ed61a6421f17b0bd3e34c94662d65aa6ad3b`
- cited in: node.lean, record TFQ-1268
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `SzollosiQuartetSystem`): recorded sha256 `6fa7c1b58f88056161fc9ea83fc5ed61a6421f17b0bd3e34c94662d65aa6ad3b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build SzollosiQuartetSystem`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `mu_identity_coordinates_bounded` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms mu_identity_coordinates_bounded` |
| `quartet_iff_candidate_equations` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms quartet_iff_candidate_equations` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1268_mub6_szollosi_618_system.md`

- file: [dag/derivations/25_mub/tfq_1268_mub6_szollosi_618_system.md](../../../dag/derivations/25_mub/tfq_1268_mub6_szollosi_618_system.md)
- sha256 (`lf-normalised`): `9d8b6c96d0e7582140342730131140bcb1df76399853b0761e230f6c5cf0e1db`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1268
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `31ddd89d2594bb5ad401aadb99a3a91edb6ea8e33158386031a40b1dc36f7223`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/mub6_claim_ledger.md`

- file: [papers/core/mub6/mub6_claim_ledger.md](../../../papers/core/mub6/mub6_claim_ledger.md)
- sha256 (`lf-normalised`): `e21c9d2f20bd0e87979c8b003ab6e2c60422c19cfdd0117308db09ec10c47f7a`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-SZOLLOSI-618-SYSTEM` `DERIVED_LEAN`: [MUB6-SZOLLOSI-TWO-CIRCULANT](MUB6-SZOLLOSI-TWO-CIRCULANT.md) (PROVED_LEAN)

Outgoing (2):

- `APP-R-MUB6-RECTANGULAR-KRAWCZYK-SOUNDNESS` `DERIVED_LEAN`: [MUB6-RECTANGULAR-KRAWCZYK-SOUNDNESS](MUB6-RECTANGULAR-KRAWCZYK-SOUNDNESS.md) (PROVED_LEAN)
- `APP-R-MUB6-SZOLLOSI-GAUGED-666` `DERIVED_LEAN`: [MUB6-SZOLLOSI-GAUGED-666](MUB6-SZOLLOSI-GAUGED-666.md) (PROVED_LEAN)
