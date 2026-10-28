# MUB6-SZOLLOSI-GAUGED-666

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> At each admissible Szollosi parameter, quartet existence is equivalent to a solution of the 666-equation system (618 original, 24 column-gauge and 24 derived balance equations) in 440 coordinates, and to such a solution lying in one of six overlapping native candidate charts.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 7
- cited Lean, Rust or Python symbols found in their in-repo files: 5
- distinct cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

All six charts return UNRESOLVED_BOX in duplicate native runs; none is excluded.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-C20 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/SzollosiColumnGauge.lean`

- file: [lean4/SzollosiColumnGauge.lean](../../../lean4/SzollosiColumnGauge.lean)
- sha256 (`bytes`): `40d2a7a43eb4a6af119eacd842f05ee293e6a9f179260a526f8db5dd320933de`
- cited in: node.lean, record TFQ-1269
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `SzollosiColumnGauge`): recorded sha256 `40d2a7a43eb4a6af119eacd842f05ee293e6a9f179260a526f8db5dd320933de` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build SzollosiColumnGauge`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `exists_gauge_box_solution_with_parameters_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms exists_gauge_box_solution_with_parameters_iff` |

- counts toward the grade: yes

### Lean: `lean4/SzollosiGaugeBalance.lean`

- file: [lean4/SzollosiGaugeBalance.lean](../../../lean4/SzollosiGaugeBalance.lean)
- sha256 (`bytes`): `fb2b8eeda0f65497bb3320b0b221011ec333310c46ef654f0f68c9058ad5548b`
- cited in: node.lean, record TFQ-1269
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `SzollosiGaugeBalance`): recorded sha256 `fb2b8eeda0f65497bb3320b0b221011ec333310c46ef654f0f68c9058ad5548b` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build SzollosiGaugeBalance`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `solution_balance_equations` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms solution_balance_equations` |

- counts toward the grade: yes

### Lean: `lean4/SzollosiGaugedCover.lean`

- file: [lean4/SzollosiGaugedCover.lean](../../../lean4/SzollosiGaugedCover.lean)
- sha256 (`bytes`): `aeaa4546c8e28788a173348e6e79d0d366d5f1c097e85298f933ba5edb29d354`
- cited in: node.lean, record TFQ-1269
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `SzollosiGaugedCover`): recorded sha256 `aeaa4546c8e28788a173348e6e79d0d366d5f1c097e85298f933ba5edb29d354` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build SzollosiGaugedCover`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `augmented_solution_chart_cover` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms augmented_solution_chart_cover` |

- counts toward the grade: yes

### Lean: `lean4/SzollosiGaugedExecutable.lean`

- file: [lean4/SzollosiGaugedExecutable.lean](../../../lean4/SzollosiGaugedExecutable.lean)
- sha256 (`bytes`): `d87b81d16a62d67d2ed92d8df796dbd2d0a77241b5328c36074ff303dd46a19e`
- cited in: node.lean, record TFQ-1269
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `SzollosiGaugedExecutable`): recorded sha256 `d87b81d16a62d67d2ed92d8df796dbd2d0a77241b5328c36074ff303dd46a19e` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build SzollosiGaugedExecutable`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `augmented_exists_with_parameters_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms augmented_exists_with_parameters_iff` |

- counts toward the grade: yes

### Lean: `lean4/SzollosiGaugedReflection.lean`

- file: [lean4/SzollosiGaugedReflection.lean](../../../lean4/SzollosiGaugedReflection.lean)
- sha256 (`bytes`): `356eab2883d9d9494b06481f1ee41450a5f052a2bd157558657aca48da71c914`
- cited in: node.lean, record TFQ-1269
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `SzollosiGaugedReflection`): recorded sha256 `356eab2883d9d9494b06481f1ee41450a5f052a2bd157558657aca48da71c914` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build SzollosiGaugedReflection`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `native_chart_quartet_iff` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms native_chart_quartet_iff` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1269_mub6_szollosi_gauged_666.md`

- file: [dag/derivations/25_mub/tfq_1269_mub6_szollosi_gauged_666.md](../../../dag/derivations/25_mub/tfq_1269_mub6_szollosi_gauged_666.md)
- sha256 (`lf-normalised`): `f27d1ee57afbd0cdf4863c2aae8b3115c3ba33988ff57a0ff69e45d96b08ecb9`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1269
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `31ddd89d2594bb5ad401aadb99a3a91edb6ea8e33158386031a40b1dc36f7223`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `papers/core/mub6/mub6_claim_ledger.md`

- file: [papers/core/mub6/mub6_claim_ledger.md](../../../papers/core/mub6/mub6_claim_ledger.md)
- sha256 (`lf-normalised`): `6708883b9f1ed33cc93d794d2c7c50484f0f8e075e4576c2eaa74fadf6fbf842`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-SZOLLOSI-GAUGED-666` `DERIVED_LEAN`: [MUB6-SZOLLOSI-618-SYSTEM](MUB6-SZOLLOSI-618-SYSTEM.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-MUB6-SZOLLOSI-BOX-368-EXCLUSION` `DERIVED_LEAN`: [MUB6-SZOLLOSI-BOX-368-EXCLUSION](MUB6-SZOLLOSI-BOX-368-EXCLUSION.md) (PROVED_LEAN)
