# PGW-RUNG2B-STAKE-MENU

Stage: [GENESIS](../stages/GENESIS.md). Status: `COMPUTATIONALLY_CHECKED`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Rung two track two (pull request 135) answers Challenge 2, the stake read off the state, within a declared menu and rectangle and by finite computation only. The menu has nine rules E1 to E9 reading six observables (profile equality, profile emptiness, profile size, pair-orbit membership, class count, requirement pattern). On both readings, both measures, two items, arity two, four held data, fifteen rounds and guard 250 (847 reached regimes), six rules commute with every renaming over 1,345,706 cases, while E3, E4 and E6, which read pair orbits, are OPEN at transport replay. E4 alone generates demands of both kinds and its invariance is among the OPEN three, so no member is both checked invariant and two-kinded; all nine are retained.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declaration references covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

- `computational_no_runnable_test`: 0 in-repo Rust or Python symbol(s) cited, none a test. COMPUTATIONALLY_CHECKED with no in-repo runnable Rust or Python test cited.

## Imported structure

- Declared nine-rule stake menu over six observables, frozen before computation (assumption)

## Bottleneck

Within this menu and rectangle only, with no Lean; that no other rule qualifies is not claimed, and E3 and E4 invariance is answered later only in continuation attempt one's Lean mirror, whose orbit is not checked against the Python orbit the rules read (G-9).

## Source status

continuation.txt section 4 row 2 and section 6 rung two track two; run ledger SD-02b-1 to SD-02b-7; finite computation

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/02_genesis/tfq_0465_rung2b_stake_menu.md`

- file: [dag/derivations/02_genesis/tfq_0465_rung2b_stake_menu.md](../../../dag/derivations/02_genesis/tfq_0465_rung2b_stake_menu.md)
- sha256 (`lf-normalised`): `1bc2615e560398a1038064f19038280fb2681cf8cdac74423b87815c4ebf63c6`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0465
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second/claim_ledger.md:149`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_stake/generation.py::invariance_record`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_stake/rules.py::label_of`
- `external:github.com/dbccpage/19L57G1@85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_stake/rules.py::rule_named`

## Absences recorded by the TFQ records

- TFQ-0465 lean4: rung two track two has no Lean package; its menu results are finite computation
- TFQ-0465 rust: the second-derivation rung trees hold no Rust

## Routes

Incoming (1):

- `PGW-R-RUNG2B-STAKE-MENU` `COMPUTED`: [PGW-RUNG2A-STAKE-DECLARED-LABEL](PGW-RUNG2A-STAKE-DECLARED-LABEL.md) (CONDITIONAL)

Outgoing (1):

- `PGW-R-TYPED-REQUIREMENT-KINDS` `DERIVED_PROSE`: [PGW-TYPED-REQUIREMENT-KINDS](PGW-TYPED-REQUIREMENT-KINDS.md) (DEFINITION)
