# PGW-WDP-GENESIS-BRIDGES-LEDGER

Stage: [WDP](../stages/WDP.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> WDP Level 22 presents eleven proposed Genesis-to-WDP bridges drawn from register rows GEN-WDP-01 to GEN-WDP-10: the inertia boundary (01), apartness from R(a,b) with protected irreflexivity (02), report-fibre factorization of a protected decision (03), joint evaluation and permission reports (04), the replay append-fold law (05), history-loss countermodels (06), the fixed-carrier repair quotient of directed assertion tables (07), the marked-balance boundary (08), the doubled-real representation of a declared complex model (09) and the agent-count countermodel (10), plus finite parity, finite-list ℓ¹ attainment, flat-locus, odd-cycle anticorrelation and acyclic-succession checks. The register belongs to the enlarged first-principles programme and its IDs are separate from the 154 canonical WDP rows; its obligations GEN-WDP-O01 to O05 stay open (TFQ-0343). Bridge 1 also describes the S(n) stages as resolving W_n as a discrete Postnikov tower, but the derivation programme states that these are construction stages, not Postnikov truncations of a single space, and that reading is kept.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

A proposed-extension register, not part of the 154-row monograph ledger and not a derivation of WDP from \<\>; finite checks hold on their declared domains only, and the Postnikov framing of Bridge 1 is refused per S(n) (TFQ-0520).

## Source status

WDP Level 22 bridges and docs/genesis_bridge_register.md GEN-WDP-01..10 (proposed-extension register)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/FoundationalBridges.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/FoundationalBridges.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/FoundationalBridges.lean)
- sha256 (`bytes`): `b3f18641d80352faf0023d10748f222a135487fbd38e9186b5fca26ed363fcaf`
- cited in: node.lean, record TFQ-0554
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_wdp.json](../../../dag/research/lean_replay_campaign_wdp.json) (module `Imported.WitnessedDifference.WitnessedDifference.FoundationalBridges`): recorded sha256 `b3f18641d80352faf0023d10748f222a135487fbd38e9186b5fca26ed363fcaf` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: none; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/FoundationalBridges.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `triangle_parity_pairwise_distinct` | yes | yes | yes | none | `#print axioms triangle_parity_pairwise_distinct` |
- counts toward the grade: yes

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/rust/src/foundational_bridges.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/rust/src/foundational_bridges.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/06_wdp/tfq_0554_wdp_genesis_bridges_ledger.md`

- file: [dag/derivations/06_wdp/tfq_0554_wdp_genesis_bridges_ledger.md](../../../dag/derivations/06_wdp/tfq_0554_wdp_genesis_bridges_ledger.md)
- sha256 (`lf-normalised`): `103e4c74a5fa40654374ac47d4563c11b42f07c0f25bc16d940361435fa66d0d`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0554
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_bridge_register.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_bridge_register.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_to_wdp_derivation_programme.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_to_wdp_derivation_programme.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/006_oewdp/levels/level_22_genesis_to_wdp_bridges.md`

- file: `omega_engine_education/documentation/006_oewdp/levels/level_22_genesis_to_wdp_bridges.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/rust/src/foundational_bridges.rs::apartness_witness`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/foundational_bridges.py::apartness_witness`

## Routes

Incoming (1):

- `PGW-R-WDP-GENESIS-BRIDGES-LEDGER` `DERIVED_PROSE`: [PGW-WDP-OBSERVER-QUOTIENT-PASSIVITY](PGW-WDP-OBSERVER-QUOTIENT-PASSIVITY.md) (DEFINITION), [PG-WDP-GENESIS-BRIDGE-OBLIGATIONS](PG-WDP-GENESIS-BRIDGE-OBLIGATIONS.md) (OPEN), [PGW-SN-POSTNIKOV-REFUSAL](PGW-SN-POSTNIKOV-REFUSAL.md) (PROVED_PROSE)

Outgoing (2):

- `PGW-R-WDP-BRIDGE-ONGOING-TO-WINDOW` `GAP_NO_DERIVATION`: [PGW-WDP-BRIDGE-ONGOING-TO-WINDOW](PGW-WDP-BRIDGE-ONGOING-TO-WINDOW.md) (OPEN)
- `PGW-R-WDP-BRIDGE-REPORT-FIBER-OBSERVER` `CONDITIONAL_ON_IMPORT`: [PGW-WDP-BRIDGE-REPORT-FIBER-OBSERVER](PGW-WDP-BRIDGE-REPORT-FIBER-OBSERVER.md) (CONDITIONAL)
