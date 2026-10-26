# PGW-GO-H3-TWIN-FILLS-HOLONOMY

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Climbing round H3 is two fills on the H2 carrier. In the twenty-fourth derivation a fifth change fills one term, and a filled term x balances exactly when its loop excess e(x,x) is zero, the same in every state of a result and every writing (balances_iff); a result is told from the one asserting nothing exactly when some filled term's loop excess is non-zero (told_iff). In the twenty-fifth a filled triple (x,y,z) balances when the sum around e(x,y) + e(y,z) + e(z,x) is zero, which the sameness keeps; a result is told exactly when some filled triple does not balance (nothing_balanced, told_iff), with three terms it is blind exactly when the sum around 0,1,2 is zero and the two-way sums add up to zero (blind_three_iff), and with every loop and two-way sum zero the triples through one term decide (cone_decides). A scratch rank computation of the sums around filled triples modulo raising gives 2 of 7 dimensions at three terms, 7 of 13 at four and 16 of 21 at five, only the loops unseen from five terms.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 4
- cited Lean, Rust or Python symbols found in their in-repo files: 6
- distinct cited Lean declarations covered by a current replay receipt: 6
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- H2 sameness of the twenty-third derivation (Same3) as the carrier of both fills (assumption)

## Bottleneck

The ranks come from research/twentyfifth/scratch_rank.py, which labels itself scratch and not evidence; the general rank criterion C(n − 1, 2), the four-term blind converse and the counts are ledger row O2, proved in the paper and checked by computation up to five terms, with no Lean statement.

## Source status

001_genesis_ongoing_h3v7n5qf paper/twentyfourth/claim_ledger.md D2 and D4, paper/twentyfifth/claim_ledger.md D4, D6 and D7; lean4_core/Twentyfourth and Twentyfifth

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisOngoingCore/Twentyfifth/Balance.lean`

- file: [lean4/Imported/GenesisOngoingCore/Twentyfifth/Balance.lean](../../../lean4/Imported/GenesisOngoingCore/Twentyfifth/Balance.lean)
- sha256 (`bytes`): `ff520a89ecde57a481175a77bc5cf5fcbf48902d9938e45c8c0f5f98b304fb0f`
- cited in: node.lean, record TFQ-0485
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoingCore.Twentyfifth.Balance`): recorded sha256 `ff520a89ecde57a481175a77bc5cf5fcbf48902d9938e45c8c0f5f98b304fb0f` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoingCore/Twentyfifth/Balance.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `nothing_balanced` | yes | yes | yes | Quot.sound, propext | `#print axioms nothing_balanced` |
| `told_iff` | yes | yes | yes | propext | `#print axioms told_iff` |

- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisOngoingCore/Twentyfifth/Blind.lean`

- file: [lean4/Imported/GenesisOngoingCore/Twentyfifth/Blind.lean](../../../lean4/Imported/GenesisOngoingCore/Twentyfifth/Blind.lean)
- sha256 (`bytes`): `422a67e3d2f99c062f21ad8133877151b5b016a496ea34dfa51dfca7547f8e46`
- cited in: node.lean, record TFQ-0485
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoingCore.Twentyfifth.Blind`): recorded sha256 `422a67e3d2f99c062f21ad8133877151b5b016a496ea34dfa51dfca7547f8e46` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoingCore/Twentyfifth/Blind.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `blind_three_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms blind_three_iff` |
| `cone_decides` | yes | yes | yes | Quot.sound, propext | `#print axioms cone_decides` |

- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisOngoingCore/Twentyfourth/Same.lean`

- file: [lean4/Imported/GenesisOngoingCore/Twentyfourth/Same.lean](../../../lean4/Imported/GenesisOngoingCore/Twentyfourth/Same.lean)
- sha256 (`bytes`): `b4a7d9411792a5fdd05eb220cb63619afca83622ac3de603008b1535c8954957`
- cited in: node.lean, record TFQ-0485
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoingCore.Twentyfourth.Same`): recorded sha256 `b4a7d9411792a5fdd05eb220cb63619afca83622ac3de603008b1535c8954957` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoingCore/Twentyfourth/Same.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `balances_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms balances_iff` |

- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisOngoingCore/Twentyfourth/Tell.lean`

- file: [lean4/Imported/GenesisOngoingCore/Twentyfourth/Tell.lean](../../../lean4/Imported/GenesisOngoingCore/Twentyfourth/Tell.lean)
- sha256 (`bytes`): `e7a56697a82bcbadd8c67c10cbef962771fe6dc1aae16be0ad5663b873ae66bd`
- cited in: node.lean, record TFQ-0485
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoingCore.Twentyfourth.Tell`): recorded sha256 `e7a56697a82bcbadd8c67c10cbef962771fe6dc1aae16be0ad5663b873ae66bd` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoingCore/Twentyfourth/Tell.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `told_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms told_iff` |

- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0485_go_h3_twin_fills_holonomy.md`

- file: [dag/derivations/02_genesis/tfq_0485_go_h3_twin_fills_holonomy.md](../../../dag/derivations/02_genesis/tfq_0485_go_h3_twin_fills_holonomy.md)
- sha256 (`lf-normalised`): `fbaefe33f36d5bd3b31ad8c933b0ad6b0563d223ef6b12c893c67e554095a7db`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0485
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/twentyfifth/claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/twentyfifth/claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/twentyfourth/claim_ledger.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/paper/twentyfourth/claim_ledger.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/research/twentyfifth/reading_the_seed.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/research/twentyfifth/reading_the_seed.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/twentyfifth/told.py::decides`
- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/twentyfifth/told.py::rank`
- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/001_genesis_ongoing_h3v7n5qf/code/twentyfourth/state.py::balances`

## Absences recorded by the TFQ records

- TFQ-0485 rust: the H3V7N5QF package holds no Rust

## Routes

Incoming (1):

- `PGW-R-GO-H3-TWIN-FILLS-HOLONOMY` `DERIVED_LEAN`: [PGW-GO-H2-STATE-RAISING-GAUGE](PGW-GO-H2-STATE-RAISING-GAUGE.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-BRIDGE-ONGOING-TO-WINDOW` `GAP_NO_DERIVATION`: [PGW-WDP-BRIDGE-ONGOING-TO-WINDOW](PGW-WDP-BRIDGE-ONGOING-TO-WINDOW.md) (OPEN)
