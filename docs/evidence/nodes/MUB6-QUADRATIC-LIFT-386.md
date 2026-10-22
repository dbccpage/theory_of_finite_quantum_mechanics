# MUB6-QUADRATIC-LIFT-386

Stage: [MUTUALLY_UNBIASED_BASES](../stages/MUTUALLY_UNBIASED_BASES.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Quartet existence in C^6 is equivalent to a common zero of the literal 648-row degree-two table in 386 coded coordinates within the coded box \[-1,1\]^170 x \[-3,3\]^216, and also within the narrowed box with transition coordinates in \[-10035/4096, 10035/4096\].

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

None recorded.

## Bottleneck

The native sweep on this box returns CONTRACTED_UNRESOLVED_BOX; infeasibility is open; JSON parsing and hashing of the exported table are outside the kernel.

## Source status

papers/core/mub6/theory_of_finite_mub6.jsonl record MUB6-PAPER-QUADRATIC-LIFT claims PROVED_LEAN; audited status PROVED_LEAN

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/MubQuadraticLiftNarrowBox.lean`

- file: [lean4/MubQuadraticLiftNarrowBox.lean](../../../lean4/MubQuadraticLiftNarrowBox.lean)
- sha256 (`bytes`): `0e3a98ed598a0b74eaf2b6c2c152cc41ea40a416766501734249920419c053ac`
- cited in: node.lean, record TFQ-1262
- replay: `none`
- check: `cd lean4 && lake build MubQuadraticLiftNarrowBox`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `exists_quartet_iff_narrow_table` | yes | yes | yes | - | `#print axioms exists_quartet_iff_narrow_table` |
- counts toward the grade: yes

### Lean: `lean4/MubQuadraticLiftTable.lean`

- file: [lean4/MubQuadraticLiftTable.lean](../../../lean4/MubQuadraticLiftTable.lean)
- sha256 (`bytes`): `a9b19face97bd0413c997ca484bab4866b89085cee4330d29e55b10c5389b4d8`
- cited in: node.lean, record TFQ-1262
- replay: `none`
- check: `cd lean4 && lake build MubQuadraticLiftTable`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `exists_quartet_iff_table` | yes | yes | yes | - | `#print axioms exists_quartet_iff_table` |
| `rows_match` | yes | yes | yes | - | `#print axioms rows_match` |
- counts toward the grade: yes

### Documents and data: `dag/derivations/25_mub/tfq_1262_mub6_quadratic_lift_386.md`

- file: [dag/derivations/25_mub/tfq_1262_mub6_quadratic_lift_386.md](../../../dag/derivations/25_mub/tfq_1262_mub6_quadratic_lift_386.md)
- sha256 (`lf-normalised`): `e2a4f7060056cb4b43c2672dc940a621a0419b65911aea493f3a57179ad3957a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-1262
- counts toward the grade: no

### Documents and data: `papers/core/mub6/mub6.md`

- file: [papers/core/mub6/mub6.md](../../../papers/core/mub6/mub6.md)
- sha256 (`lf-normalised`): `edeb29b681854d6ff67bdf072e4d3163995e068973662ebb77220ba009345238`
- cited in: node.source
- counts toward the grade: yes

## Routes

Incoming (1):

- `APP-R-MUB6-QUADRATIC-LIFT-386` `DERIVED_LEAN`: [MUB6-QUARTET-RAW-HADAMARD-TRANSPORT](MUB6-QUARTET-RAW-HADAMARD-TRANSPORT.md) (PROVED_LEAN)

Outgoing (2):

- `APP-R-MUB6-BALANCED-648-QUADRATIC` `DERIVED_LEAN`: [MUB6-BALANCED-648-QUADRATIC](MUB6-BALANCED-648-QUADRATIC.md) (PROVED_LEAN)
- `APP-R-MUB6-CLOSE-COLUMNS-EXCLUSION` `DERIVED_LEAN`: [MUB6-CLOSE-COLUMNS-EXCLUSION](MUB6-CLOSE-COLUMNS-EXCLUSION.md) (PROVED_LEAN)
