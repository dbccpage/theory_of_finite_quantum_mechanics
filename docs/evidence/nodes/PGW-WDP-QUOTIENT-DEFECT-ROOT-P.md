# PGW-WDP-QUOTIENT-DEFECT-ROOT-P

Stage: [WDP](../stages/WDP.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Root P, the evaluation layer: with V a finite-dimensional real space of defects, A a finite-dimensional space of repairs, d: A → V a linear repair map, δ ∈ V an exhibited defect and J a declared seminorm or cost, the quotient defect is Φ_J(\[δ\]) = inf_{α ∈ A} J(δ − dα), where \[δ\] is the coset of δ modulo im d. The expression is not primitive: it imports a linear carrier, a repair map and a cost, each declared rather than derived. Root P presupposes Root W, the admitted cut with its witnessed irreflexive relation, as carrier and never substitutes for it. This infimum over repairs is the quantity WDP later writes Φ₁.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 2
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Declared defect space V, repair space A, linear repair map d and cost J (assumption)

## Bottleneck

A declared construction, not a theorem; it derives none of the carrier, repair map or cost from the admitted cut, and Φ_J(\[δ\]) equals J(δ) or ‖d₀δ‖₁ only where that value is shown to be the infimum.

## Source status

WDP monograph §2.1 Root P quotient defect (declared construction)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean)
- sha256 (`bytes`): `bef8623978d7c0735b4a02db686664b03b61e18bba0e5ef6bcce81ff4234dd0a`
- cited in: node.lean, record TFQ-0538
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_wdp.json](../../../dag/research/lean_replay_campaign_wdp.json) (module `Imported.WitnessedDifference.WitnessedDifference.Obstruction`): recorded sha256 `bef8623978d7c0735b4a02db686664b03b61e18bba0e5ef6bcce81ff4234dd0a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `Q1` | yes | yes | yes | none | `#print axioms Q1` |
| `Repair` | yes | yes | yes | none | `#print axioms Repair` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_wdp/src/obstruction.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/obstruction.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/06_wdp/tfq_0538_wdp_quotient_defect_root_p.md`

- file: [dag/derivations/06_wdp/tfq_0538_wdp_quotient_defect_root_p.md](../../../dag/derivations/06_wdp/tfq_0538_wdp_quotient_defect_root_p.md)
- sha256 (`lf-normalised`): `ac36eb5f52dc37dd1dcdbbd7c3a6593ee0fa5ffd5596fb4a2f9dc1955d88ccff`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0538
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/006_oewdp/levels/level_01_witness_function.md`

- file: `omega_engine_education/documentation/006_oewdp/levels/level_01_witness_function.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:upstream/omega_engine/crates_rs/omega_wdp/src/obstruction.rs::solve_exact_potential_weighted`
- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/obstruction.py::matrix_quotient_l1`

## Routes

Incoming (1):

- `PGW-R-WDP-QUOTIENT-DEFECT-ROOT-P` `DERIVED_PROSE`: [PGW-WDP-FAILED-SAMENESS](PGW-WDP-FAILED-SAMENESS.md) (PROVED_PROSE)

Outgoing (2):

- `PGW-R-WDP-PHI-WELL-DEFINED-L1-DUALITY` `CONDITIONAL_ON_IMPORT`: [PGW-WDP-PHI-WELL-DEFINED-L1-DUALITY](PGW-WDP-PHI-WELL-DEFINED-L1-DUALITY.md) (CONDITIONAL)
- `PGW-R-WDP-SEVEN-WITNESS-ROLES` `DERIVED_PROSE`: [PGW-WDP-SEVEN-WITNESS-ROLES](PGW-WDP-SEVEN-WITNESS-ROLES.md) (DEFINITION)
