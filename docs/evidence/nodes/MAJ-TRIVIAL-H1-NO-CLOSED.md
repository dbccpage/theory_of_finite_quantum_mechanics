# MAJ-TRIVIAL-H1-NO-CLOSED

Stage: [MAJORANA](../stages/MAJORANA.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> If every cocycle of a declared F2 cochain complex is exact, then no residual is ClosedResidual.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

None for the lemma; its use on the legacy carrier needs the legacy dim H1 = 0 measurement (MAJ-C13).

## Source status

papers/core/majorana/the_majorana_problem.md record MAJ-LEMMA-TRIVIAL-H1 claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `papers/core/majorana/lean4/MajoranaCore.lean`

- file: [papers/core/majorana/lean4/MajoranaCore.lean](../../../papers/core/majorana/lean4/MajoranaCore.lean)
- sha256 (`bytes`): `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071`
- cited in: node.lean, record TFQ-1153
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_majorana.json](../../../dag/research/lean_replay_campaign_majorana.json) (module `MajoranaCore`): recorded sha256 `10e0d2ffb73e63771564891d2ced8c72798f1c36c9adb82afdd574d86ad0d071` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains papers/core/majorana/lean4/MajoranaCore.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `legacy_carrier_obstruction` | yes | yes | yes | none | `#print axioms legacy_carrier_obstruction` |
- counts toward the grade: yes

### Rust: `code/rust/src/majorana/classify.rs`

- file: [code/rust/src/majorana/classify.rs](../../../code/rust/src/majorana/classify.rs)
- sha256 (`bytes`): `93bf9e0d978e50493ba85a1031c488f6537ee5f1e833db44606995b97e398b6b`
- cited in: node.rust, record TFQ-1153
- check: `cd code/rust && cargo test -p tfqm_majorana disk_never_yields_a_logical_class`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `disk_never_yields_a_logical_class` (rust_test) | yes | yes | yes | - | `cd code/rust && cargo test -p tfqm_majorana disk_never_yields_a_logical_class` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/28_majorana/tfq_1153_maj_trivial_h1_no_closed.md`

- file: [dag/derivations/28_majorana/tfq_1153_maj_trivial_h1_no_closed.md](../../../dag/derivations/28_majorana/tfq_1153_maj_trivial_h1_no_closed.md)
- sha256 (`lf-normalised`): `73d050c824b5b119a38c5b4541719cf4f2b189910cf9a8f815c13509b73d3375`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1153
- counts toward the grade: no

### Documents and data: `papers/core/majorana/the_majorana_problem.md`

- file: [papers/core/majorana/the_majorana_problem.md](../../../papers/core/majorana/the_majorana_problem.md)
- sha256 (`lf-normalised`): `e92416bb1739e51de20a8ad6a26d4b5f3d76b974d7556507b13149b29e8edb47`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MAJ-TRIVIAL-H1-NO-CLOSED` `DERIVED_LEAN`: [MAJ-TRICHOTOMY-PAIRWISE-EXCLUSION](MAJ-TRICHOTOMY-PAIRWISE-EXCLUSION.md) (PROVED_LEAN)

Outgoing (1):

- `APP-R-MAJ-LEGACY-CARRIER-RETRACTION` `CONDITIONAL_ON_IMPORT`: [MAJ-LEGACY-CARRIER-RETRACTION](MAJ-LEGACY-CARRIER-RETRACTION.md) (CONDITIONAL)
