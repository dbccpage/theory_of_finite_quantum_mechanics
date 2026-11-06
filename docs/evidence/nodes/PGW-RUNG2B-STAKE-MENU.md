# PGW-RUNG2B-STAKE-MENU

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E2**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Rung two track two (pull request 135) answers Challenge 2, the stake read off the state, within a declared menu and rectangle and by finite computation only. The menu has nine rules E1 to E9 reading six observables (profile equality, profile emptiness, profile size, pair-orbit membership, class count, requirement pattern). On both readings, both measures, two items, arity two, four held data, fifteen rounds and guard 250 (847 reached regimes), six rules commute with every renaming over 1,345,706 cases, while E3, E4 and E6, which read pair orbits, are OPEN at transport replay. E4 alone generates demands of both kinds and its invariance is among the OPEN three, so no member is both checked invariant and two-kinded; all nine are retained.

## Grade

Evidence grade **E2** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 3
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: replay a cited Lean declaration and record a receipt whose sha256 matches the current file (see docs/evidence/README.md, Verify it yourself)

## Flags

- `proved_lean_below_e3`: grade E2; 3 Lean reference(s) cited, 3 in this checkout (replay: none 3). PROVED_LEAN below E3: no cited Lean declaration is covered by a current replay receipt.

## Imported structure

- Declared nine-rule stake menu over six observables, frozen before computation (assumption)

## Bottleneck

Within this menu and rectangle only, with no Lean; that no other rule qualifies is not claimed, and E3 and E4 invariance is answered later only in continuation attempt one's Lean mirror, whose orbit is not checked against the Python orbit the rules read (G-9).

## Source status

continuation.txt section 4 row 2 and section 6 rung two track two; run ledger SD-02b-1 to SD-02b-7; finite computation; mechanized in WitnessedDifference/WdpBatch9.lean

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch9.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch9.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch9.lean)
- sha256 (`bytes`): `84c1b281079874d4029bc2c5b304b50e4db594e0d013a5c053854f1790e03977`
- cited in: node.lean, record TFQ-0465
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch9.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch9.profile_equality_renaming_invariant` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch9.profile_equality_renaming_invariant` |
| `WitnessedDifference.WdpBatch9.rung2b_stake_menu_no_member_both_invariant_and_two_kinded` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch9.rung2b_stake_menu_no_member_both_invariant_and_two_kinded` |

- counts toward the grade: yes

### Lean: `atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch9Rep.lean`

- file: [atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch9Rep.lean](../../../atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch9Rep.lean)
- sha256 (`bytes`): `498be0c6a626beb7c40ce3bffb05f971be18f94e39b639deb19789cb1717cc54`
- cited in: node.lean, record TFQ-0465
- replay: `none`
- check: `cd lean4 && lake build   # the library that contains atlas/finite_obstruction_calculus/witnessed_difference_programme/lean4/WitnessedDifference/WdpBatch9Rep.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `WitnessedDifference.WdpBatch9Rep.rep_rung2b_stake_menu` | yes | yes | yes | - | `#print axioms WitnessedDifference.WdpBatch9Rep.rep_rung2b_stake_menu` |

- counts toward the grade: yes

### Documents and data: `atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt`

- file: [atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt](../../../atlas/finite_obstruction_calculus/genesis/docs/sources/continuation.txt)
- sha256 (`lf-normalised`): `7e774b9a5cd0b326f884716c49a18055df522968e659438910dceeaa332b73ad`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0465_rung2b_stake_menu.md`

- file: [dag/derivations/02_genesis/tfq_0465_rung2b_stake_menu.md](../../../dag/derivations/02_genesis/tfq_0465_rung2b_stake_menu.md)
- sha256 (`lf-normalised`): `ddcdecf31b0cc078af1aabc87a659cdecf41a901bc91703fc3b9928798ea270a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0465
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second/claim_ledger.md:149`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_stake/generation.py::invariance_record`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_stake/rules.py::label_of`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_stake/rules.py::rule_named`

## Absences recorded by the TFQ records

- TFQ-0465 rust: the second-derivation rung trees hold no Rust

## Routes

Incoming (1):

- `PGW-R-RUNG2B-STAKE-MENU` `DERIVED_LEAN`: [PGW-RUNG2A-STAKE-DECLARED-LABEL](PGW-RUNG2A-STAKE-DECLARED-LABEL.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-TYPED-REQUIREMENT-KINDS` `DERIVED_PROSE`: [PGW-TYPED-REQUIREMENT-KINDS](PGW-TYPED-REQUIREMENT-KINDS.md) (DEFINITION)
