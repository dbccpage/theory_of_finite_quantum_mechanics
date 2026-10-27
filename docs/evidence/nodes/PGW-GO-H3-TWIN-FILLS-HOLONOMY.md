# PGW-GO-H3-TWIN-FILLS-HOLONOMY

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Climbing round H3 is two fills on the H2 carrier. In the twenty-fourth derivation a fifth change fills one term, and a filled term x balances exactly when its loop excess e(x,x) is zero, the same in every state of a result and every writing (balances_iff); a result is told from the one asserting nothing exactly when some filled term's loop excess is non-zero (told_iff). In the twenty-fifth a filled triple (x,y,z) balances when the sum around e(x,y) + e(y,z) + e(z,x) is zero, which the sameness keeps; a result is told exactly when some filled triple does not balance (nothing_balanced, told_iff), with three terms it is blind exactly when the sum around 0,1,2 is zero and the two-way sums add up to zero (blind_three_iff), and with every loop and two-way sum zero the triples through one term decide (cone_decides). A scratch rank computation of the sums around filled triples modulo raising gives 2 of 7 dimensions at three terms, 7 of 13 at four and 16 of 21 at five, only the loops unseen from five terms.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 9
- cited Lean, Rust or Python symbols found in their in-repo files: 9
- distinct cited Lean declarations covered by a current replay receipt: 6
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 2
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (2 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- H2 sameness of the twenty-third derivation (Same3) as the carrier of both fills (assumption)

## Bottleneck

The ranks come from research/twentyfifth/scratch_rank.py, which labels itself scratch and not evidence; the general rank criterion C(n − 1, 2), the four-term blind converse and the counts are ledger row O2, proved in the paper and checked by computation up to five terms, with no Lean statement.

## Source status

genesis_ongoing paper/twentyfourth/claim_ledger.md D2 and D4, paper/twentyfifth/claim_ledger.md D4, D6 and D7; lean4_core/Twentyfourth and Twentyfifth

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/GenesisOngoingCore/Twentyfifth/Balance.lean`

- file: [lean4/Imported/GenesisOngoingCore/Twentyfifth/Balance.lean](../../../lean4/Imported/GenesisOngoingCore/Twentyfifth/Balance.lean)
- sha256 (`bytes`): `c4bd93383a93e0b9381dfab82eb0a9e7ad9328c2c296e44051f8276df92a6f82`
- cited in: node.lean, record TFQ-0485
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoingCore.Twentyfifth.Balance`): recorded sha256 `c4bd93383a93e0b9381dfab82eb0a9e7ad9328c2c296e44051f8276df92a6f82` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoingCore/Twentyfifth/Balance.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `nothing_balanced` | yes | yes | yes | Quot.sound, propext | `#print axioms nothing_balanced` |
| `told_iff` | yes | yes | yes | propext | `#print axioms told_iff` |

- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisOngoingCore/Twentyfifth/Blind.lean`

- file: [lean4/Imported/GenesisOngoingCore/Twentyfifth/Blind.lean](../../../lean4/Imported/GenesisOngoingCore/Twentyfifth/Blind.lean)
- sha256 (`bytes`): `38facb61dc83313ddcd31b2665db74fed134e8cceea69e882ef8a41e8110c1a4`
- cited in: node.lean, record TFQ-0485
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoingCore.Twentyfifth.Blind`): recorded sha256 `38facb61dc83313ddcd31b2665db74fed134e8cceea69e882ef8a41e8110c1a4` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoingCore/Twentyfifth/Blind.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `blind_three_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms blind_three_iff` |
| `cone_decides` | yes | yes | yes | Quot.sound, propext | `#print axioms cone_decides` |

- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisOngoingCore/Twentyfourth/Same.lean`

- file: [lean4/Imported/GenesisOngoingCore/Twentyfourth/Same.lean](../../../lean4/Imported/GenesisOngoingCore/Twentyfourth/Same.lean)
- sha256 (`bytes`): `e1facd662f66a886a471f22162488f804d7b0b0e4672bf69c63bbc65b04f4433`
- cited in: node.lean, record TFQ-0485
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoingCore.Twentyfourth.Same`): recorded sha256 `e1facd662f66a886a471f22162488f804d7b0b0e4672bf69c63bbc65b04f4433` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoingCore/Twentyfourth/Same.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `balances_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms balances_iff` |

- counts toward the grade: yes

### Lean: `lean4/Imported/GenesisOngoingCore/Twentyfourth/Tell.lean`

- file: [lean4/Imported/GenesisOngoingCore/Twentyfourth/Tell.lean](../../../lean4/Imported/GenesisOngoingCore/Twentyfourth/Tell.lean)
- sha256 (`bytes`): `61165fc36011772f1de9688c9ca19c32da623a5b3f130d2ce26f8403fc81cf69`
- cited in: node.lean, record TFQ-0485
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.GenesisOngoingCore.Twentyfourth.Tell`): recorded sha256 `61165fc36011772f1de9688c9ca19c32da623a5b3f130d2ce26f8403fc81cf69` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/GenesisOngoingCore/Twentyfourth/Tell.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `told_iff` | yes | yes | yes | Quot.sound, propext | `#print axioms told_iff` |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/twentyfifth/told.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/twentyfifth/told.py](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/twentyfifth/told.py)
- sha256 (`bytes`): `57117378b52d703d4e87e147f28bab3f674f1bee1bb441aecb01f5234a237ffb`
- cited in: record TFQ-0485

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `decides` (python_symbol) | yes | yes | yes | - | - |
| `rank` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/twentyfourth/state.py`

- file: [atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/twentyfourth/state.py](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/code/twentyfourth/state.py)
- sha256 (`bytes`): `fb475699dcb8105f7f31273322af46202f82907f93c1dc03d6cda217dabefdd3`
- cited in: record TFQ-0485

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `balances` (python_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/twentyfifth/claim_ledger.md`

- file: [atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/twentyfifth/claim_ledger.md](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/twentyfifth/claim_ledger.md)
- sha256 (`lf-normalised`): `0ad9844d2a72386cc8fe11716177f0e34739b8da51a628fc15c5f227a174de3d`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/twentyfourth/claim_ledger.md`

- file: [atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/twentyfourth/claim_ledger.md](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/paper/twentyfourth/claim_ledger.md)
- sha256 (`lf-normalised`): `944082e39e6e9a2434ed0be8206b9731233731ecf3ccdc908d222d0b997cfcfe`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/twentyfifth/reading_the_seed.md`

- file: [atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/twentyfifth/reading_the_seed.md](../../../atlas/papers/finite_obstruction_calculus/genesis_ongoing/research/twentyfifth/reading_the_seed.md)
- sha256 (`lf-normalised`): `01c934e8579575e2e090a55fc70d524efde43dd1286704bb9c90578c0bb51d95`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/02_genesis/tfq_0485_go_h3_twin_fills_holonomy.md`

- file: [dag/derivations/02_genesis/tfq_0485_go_h3_twin_fills_holonomy.md](../../../dag/derivations/02_genesis/tfq_0485_go_h3_twin_fills_holonomy.md)
- sha256 (`lf-normalised`): `d38769ea23510b025a408fd025967ecba6df2b58264cf30e50c2c6b9216b1fd5`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0485
- counts toward the grade: no

## Absences recorded by the TFQ records

- TFQ-0485 rust: the H3V7N5QF package holds no Rust

## Routes

Incoming (1):

- `PGW-R-GO-H3-TWIN-FILLS-HOLONOMY` `DERIVED_LEAN`: [PGW-GO-H2-STATE-RAISING-GAUGE](PGW-GO-H2-STATE-RAISING-GAUGE.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-BRIDGE-ONGOING-TO-WINDOW` `GAP_NO_DERIVATION`: [PGW-WDP-BRIDGE-ONGOING-TO-WINDOW](PGW-WDP-BRIDGE-ONGOING-TO-WINDOW.md) (OPEN)
