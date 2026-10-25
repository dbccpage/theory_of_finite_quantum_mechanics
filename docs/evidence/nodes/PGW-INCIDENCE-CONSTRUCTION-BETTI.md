# PGW-INCIDENCE-CONSTRUCTION-BETTI

Stage: [GENESIS](../stages/GENESIS.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Starting from the literal supply of \<\>, the WDP construction records Supply(\<\>) without admitting it, then supplies and admits \<a\>, \<ab\> and \<c\>, forms of arities 1, 2 and 3, three unary vertex instances and the edges 01, 12 and 02. Under an explicitly chosen incidence interpretation (a datum's admission index is a vertex, an arity-k form carries (k−1)-dimensional simplices, an instance lists its increasing vertex indices, and every vertex and face needs its own instance) the cycle has rational Betti numbers (1, 1), and admitting the single instance 012 gives (1, 0, 0). The education Lean module establishes these Betti numbers from explicit integer kernels and images of the boundary matrices (cycle_rational_betti, filled_rational_betti) and that its incidence reading returns the cycle and filled simplex lists (cycle_incidence_eq, filled_incidence_eq). For a general face-closed family K, that the construction's interpretation is exactly K rests on a written argument.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 4
- distinct cited Lean declarations covered by a current replay receipt: 4
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared incidence interpretation of admitted forms and instances as simplices, incidence_construction.txt (assumption)

## Bottleneck

The interpretation is a construction choice, not extracted from the spelling of \<\>; the general construction result is a written argument, the Lean covers the worked three-vertex complex only, and no Lean refinement of the Rust implementation is claimed.

## Source status

paper.md section 11 and incidence_construction.txt (construction choice, written argument); 006_oewdp GenesisIncidence.lean Betti theorems

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/OeWdp/GenesisIncidence.lean`

- file: [lean4/Imported/OeWdp/GenesisIncidence.lean](../../../lean4/Imported/OeWdp/GenesisIncidence.lean)
- sha256 (`bytes`): `ea27798ed2765ce05c4ee2b822efd380aaf2948486db66fdc0d42b2ad63797c9`
- cited in: node.lean, record TFQ-0460
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.OeWdp.GenesisIncidence`): recorded sha256 `ea27798ed2765ce05c4ee2b822efd380aaf2948486db66fdc0d42b2ad63797c9` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/OeWdp/GenesisIncidence.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `cycle_incidence_eq` | yes | yes | yes | none | `#print axioms cycle_incidence_eq` |
| `cycle_rational_betti` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms cycle_rational_betti` |
| `filled_incidence_eq` | yes | yes | yes | none | `#print axioms filled_incidence_eq` |
| `filled_rational_betti` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms filled_rational_betti` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_wdp/src/genesis_construction.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/genesis_construction.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/02_genesis/tfq_0460_incidence_construction_betti.md`

- file: [dag/derivations/02_genesis/tfq_0460_incidence_construction_betti.md](../../../dag/derivations/02_genesis/tfq_0460_incidence_construction_betti.md)
- sha256 (`lf-normalised`): `7c82bc67c3c89e4d585d7c22b7909abc31818274b3290889847221305af780f1`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0460
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/incidence_construction.txt`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/incidence_construction.txt`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine/crates_rs/omega_wdp/src/genesis_construction.rs::cycle_construction`
- `external:the_symbol_game/omega_engine/crates_rs/omega_wdp/src/genesis_construction.rs::homology`

## Absences recorded by the TFQ records

- TFQ-0460 python: no Python implementation of the incidence reading or its homology

## Routes

Incoming (1):

- `PGW-R-INCIDENCE-CONSTRUCTION-BETTI` `DERIVED_LEAN`: [PGW-D2-INITIAL-POINTED](PGW-D2-INITIAL-POINTED.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-INCIDENCE-ORIENTATION-TRANSPORT` `GAP_NO_DERIVATION`: [PGW-WDP-INCIDENCE-ORIENTATION-TRANSPORT](PGW-WDP-INCIDENCE-ORIENTATION-TRANSPORT.md) (OPEN)
