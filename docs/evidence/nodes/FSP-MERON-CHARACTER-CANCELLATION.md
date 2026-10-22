# FSP-MERON-CHARACTER-CANCELLATION

Stage: [FERMION_SIGN](../stages/FERMION_SIGN.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> The finite flip-orbit sign sum is zero when at least one meron flag is true, and is 2^k when all k flags are false. Weighted partition and observable reductions require additional orbit hypotheses.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 3
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- supplied Boolean flip-orbit model; not derived from graph switching

## Bottleneck

Supply invariant weight magnitudes, valid flip action and compatible observables before using the sign identity as a model reduction.

## Source status

Source record or explicit branch obligation; status scoped to the statement.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/MeronCharacter.lean`

- file: [lean4/MeronCharacter.lean](../../../lean4/MeronCharacter.lean)
- sha256 (`bytes`): `bde7f9bade1d62d06e66a2671dfefdbac25c1f32011d32732169bc575e168c9d`
- cited in: node.lean, record TFQ-0407
- replay: `verified`
  - receipt [dag/research/tensor_measurement_validation.json](../../../dag/research/tensor_measurement_validation.json) (module `MeronCharacter`): recorded sha256 `bde7f9bade1d62d06e66a2671dfefdbac25c1f32011d32732169bc575e168c9d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build MeronCharacter`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `compression_preserves_partition` | yes | yes | yes | Quot.sound, propext | `#print axioms compression_preserves_partition` |
| `meron_orbit_cancels` | yes | yes | yes | Quot.sound, propext | `#print axioms meron_orbit_cancels` |
| `zero_meron_orbit_positive` | yes | yes | yes | Quot.sound, propext | `#print axioms zero_meron_orbit_positive` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/26_fsp/tfq_0407_fsp_meron_character_cancellation.md`

- file: [dag/derivations/26_fsp/tfq_0407_fsp_meron_character_cancellation.md](../../../dag/derivations/26_fsp/tfq_0407_fsp_meron_character_cancellation.md)
- sha256 (`lf-normalised`): `80a706cc9fc7a6dbb8e5ae6a555f4102705056dcaeee5fe087b42031d5578b26`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0407
- counts toward the grade: no

### Documents and data: `papers/core/fsp/README.md`

- file: [papers/core/fsp/README.md](../../../papers/core/fsp/README.md)
- sha256 (`lf-normalised`): `49bf9e23ec5b96cfd3fbd8bfff74f2a03d0151e20c497589d4233136dc24ca5b`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-FSP-MERON-CHARACTER-CANCELLATION` `DERIVED_LEAN`: [FSP-SWITCHING-NORMAL-FORM](FSP-SWITCHING-NORMAL-FORM.md) (PROVED_LEAN)

Outgoing (2):

- `APP-R-FSP-EFFICIENT-SAMPLING-OBLIGATIONS` `GAP_NO_DERIVATION`: [FSP-EFFICIENT-SAMPLING-OBLIGATIONS](FSP-EFFICIENT-SAMPLING-OBLIGATIONS.md) (OPEN)
- `APP-R-MAJ-GIN-INVOLUTION-PAIR-CANCEL` `DERIVED_LEAN`: [MAJ-GIN-INVOLUTION-PAIR-CANCEL](MAJ-GIN-INVOLUTION-PAIR-CANCEL.md) (PROVED_LEAN)
