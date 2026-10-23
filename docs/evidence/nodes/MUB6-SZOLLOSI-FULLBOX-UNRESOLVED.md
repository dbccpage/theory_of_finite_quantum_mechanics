# MUB6-SZOLLOSI-FULLBOX-UNRESOLVED

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> On the full containing box of the 618-equation Szollosi system with zero centre and the recorded 28-entry preconditioner, the emitted Jacobian rows and images match the polynomial semantics, every solution is retained, the 144 raw coordinates of the additional bases are not narrowed, no coordinate separates, and every residual interval contains zero.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 5
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- cited Lean declarations covered by a current replay receipt: 7
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

None recorded.

## Bottleneck

Status CONTRACTED_UNRESOLVED_BOX and UNRESOLVED_FULL_BOX: no exclusion and no root; generic Rust and JSON decoding is not verified.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-C27 claims PROVED_LEAN; audited status COMPUTATIONALLY_CHECKED

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/SzollosiIntervalExclusion.lean`

- file: [lean4/SzollosiIntervalExclusion.lean](../../../lean4/SzollosiIntervalExclusion.lean)
- sha256 (`bytes`): `3e886199b605f2bb97cf672d9e0179e37598c3f26ae5e8ec417b1e2bd7ff4f9f`
- cited in: node.lean, record TFQ-1272
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `SzollosiIntervalExclusion`): recorded sha256 `3e886199b605f2bb97cf672d9e0179e37598c3f26ae5e8ec417b1e2bd7ff4f9f` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build SzollosiIntervalExclusion`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `full_box_check_unresolved` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms full_box_check_unresolved` |
| `phase_interior_excluded` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms phase_interior_excluded` |
- counts toward the grade: yes

### Lean: `lean4/SzollosiNativeReflection.lean`

- file: [lean4/SzollosiNativeReflection.lean](../../../lean4/SzollosiNativeReflection.lean)
- sha256 (`bytes`): `498061caf5fb238e3999c4d5c56943d6c9e1bfae931430e4674e8dca1f278029`
- cited in: node.lean, record TFQ-1272
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `SzollosiNativeReflection`): recorded sha256 `498061caf5fb238e3999c4d5c56943d6c9e1bfae931430e4674e8dca1f278029` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build SzollosiNativeReflection`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `native_full_box_unresolved` | yes | yes | yes | Quot.sound, propext | `#print axioms native_full_box_unresolved` |
- counts toward the grade: yes

### Lean: `lean4/SzollosiRectangularReflection.lean`

- file: [lean4/SzollosiRectangularReflection.lean](../../../lean4/SzollosiRectangularReflection.lean)
- sha256 (`bytes`): `9ac0b8f2710bfd04f9674804537e08efc77a67aafc3df34ba60e64a8ab837b40`
- cited in: node.lean, record TFQ-1272
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_mutually_unbiased_bases.json](../../../dag/research/lean_replay_campaign_mutually_unbiased_bases.json) (module `SzollosiRectangularReflection`): recorded sha256 `9ac0b8f2710bfd04f9674804537e08efc77a67aafc3df34ba60e64a8ab837b40` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build SzollosiRectangularReflection`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `native_additional_bases_unchanged` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms native_additional_bases_unchanged` |
| `native_images_have_no_separation` | yes | yes | yes | Quot.sound, propext | `#print axioms native_images_have_no_separation` |
| `native_jacobian_eq` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms native_jacobian_eq` |
| `solution_in_native_retained` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms solution_in_native_retained` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1272_mub6_szollosi_fullbox_unresolved.md`

- file: [dag/derivations/25_mub/tfq_1272_mub6_szollosi_fullbox_unresolved.md](../../../dag/derivations/25_mub/tfq_1272_mub6_szollosi_fullbox_unresolved.md)
- sha256 (`lf-normalised`): `7abca007cbccce4d534bab45cc6674950bcfdad137cb99797e1c07669fb9d542`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1272
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

- `APP-R-MUB6-SZOLLOSI-FULLBOX-UNRESOLVED` `COMPUTED`: [MUB6-RECTANGULAR-KRAWCZYK-SOUNDNESS](MUB6-RECTANGULAR-KRAWCZYK-SOUNDNESS.md) (PROVED_LEAN)

Outgoing (0):

