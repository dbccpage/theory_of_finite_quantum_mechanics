# PGW-MSSN-CIRCULATION-OBSTRUCTION

Stage: [MSSN_SN](../stages/MSSN_SN.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> MssnObstructionDetector.lean defines a Boolean active-obstruction predicate obstP on a passage state with witness pairs, protected pairs and an optional list of observation columns, and shows that it equals the conjunction of four gates: retained, protected, observation declared, and declared observation not separating the pair (obstP_factors, obst_of_gates). On the triangle a→b→c→a it shows that the cycle circulation vanishes on every integer coboundary d₀g (cycle_circulation_coboundary_vanishes), that x = (1,0,0) has circulation 1 (circulation_flux_obstruction), and that no integer potential g has d₀g = (1,0,0) (no_scalar_potential_for_unit_flux). candidateLiftCondition is a necessary condition on supplied metadata, not an implementation of the lift laws or an authorization decision.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 7
- distinct cited Lean declarations covered by a current replay receipt: 5
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 1
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (1 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Supplied observation columns in PState, not a checked partition or the full Genesis passage state (assumption)

## Bottleneck

The circulation results are relative to the displayed d₀ over ℤ; candidateLiftCondition consumes a supplied Boolean and verifies neither that an edit resolves an obstruction nor that it is authorized, and the Rust audit returns the circulation value without a potential search.

## Source status

003_oemssn lean4/MssnObstructionDetector.lean and lean4/README.md inventory row

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/MinimalSymbolSystems/MssnObstructionDetector.lean`

- file: [lean4/Imported/MinimalSymbolSystems/MssnObstructionDetector.lean](../../../lean4/Imported/MinimalSymbolSystems/MssnObstructionDetector.lean)
- sha256 (`bytes`): `4c4d0d2348ce89a0caa80aa4860c8fbcd3a038c8a4a2bbcc55a4e58bb609894a`
- cited in: node.lean, node.source, record TFQ-0534
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_genesis.json](../../../dag/research/lean_replay_campaign_genesis.json) (module `Imported.MinimalSymbolSystems.MssnObstructionDetector`): recorded sha256 `4c4d0d2348ce89a0caa80aa4860c8fbcd3a038c8a4a2bbcc55a4e58bb609894a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/MinimalSymbolSystems/MssnObstructionDetector.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `circulation_flux_obstruction` | yes | yes | yes | none | `#print axioms circulation_flux_obstruction` |
| `cycle_circulation_coboundary_vanishes` | yes | yes | yes | Quot.sound, propext | `#print axioms cycle_circulation_coboundary_vanishes` |
| `no_scalar_potential_for_unit_flux` | yes | yes | yes | Quot.sound, propext | `#print axioms no_scalar_potential_for_unit_flux` |
| `obstP_factors` | yes | yes | yes | Quot.sound, propext | `#print axioms obstP_factors` |
| `obst_of_gates` | yes | yes | yes | Quot.sound, propext | `#print axioms obst_of_gates` |

- counts toward the grade: yes

### Rust: `education/minimal_symbol_systems/code/rust/src/obstruction_detector.rs`

- file: [education/minimal_symbol_systems/code/rust/src/obstruction_detector.rs](../../../education/minimal_symbol_systems/code/rust/src/obstruction_detector.rs)
- sha256 (`bytes`): `439bafc4a90225a06b9e80fb2d9458ecd3718cd1908db47b734056ef8b6c3de2`
- cited in: node.rust

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `audit_layer_2_circulation_flux` (rust_symbol) | yes | yes | yes | - | - |
| `verify_four_gate_factorization` (rust_symbol) | yes | yes | yes | - | - |

- counts toward the grade: yes

### Documents and data: `dag/derivations/05_mssn_sn/tfq_0534_mssn_circulation_obstruction.md`

- file: [dag/derivations/05_mssn_sn/tfq_0534_mssn_circulation_obstruction.md](../../../dag/derivations/05_mssn_sn/tfq_0534_mssn_circulation_obstruction.md)
- sha256 (`lf-normalised`): `23f2b07c2c0d921cdc33192d804149edae630d4b813b86083206c5d5bb62d1da`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0534
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:1cd37babf20398c25a80ebbcad266a07807181d81f7502740c13b03d79822db7:11`
- `external:upstream/education/minimal_symbol_systems/code/rust/src/obstruction_detector.rs::audit_layer_2_circulation_flux`
- `external:upstream/education/minimal_symbol_systems/code/rust/src/obstruction_detector.rs::verify_four_gate_factorization`

## Absences recorded by the TFQ records

- TFQ-0534 python: no Python check of the four-gate detector or the triangle circulation in 003_oemssn

## Routes

Incoming (1):

- `PGW-R-MSSN-CIRCULATION-OBSTRUCTION` `DERIVED_LEAN`: [PGW-MSSN-ROWS-1-TO-6-SPECIFIED](PGW-MSSN-ROWS-1-TO-6-SPECIFIED.md) (DEFINITION), [PGW-SN-E12-CIRCULATION-FUNCTIONAL](PGW-SN-E12-CIRCULATION-FUNCTIONAL.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-MSSN-L1-CUTS-HODGE-ROWS` `DERIVED_PROSE`: [PGW-MSSN-L1-CUTS-HODGE-ROWS](PGW-MSSN-L1-CUTS-HODGE-ROWS.md) (DEFINITION)
