# PGW-WDP-FILLED-TRIANGLE

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> WDP-CH04-P08: on vertices {0, 1, 2}, edges (01, 12, 02) and one 2-simplex, with d₀f = (f₁ − f₀, f₂ − f₁, f₂ − f₀) and d₁x = x₀₁ + x₁₂ − x₀₂, the field δ = (1, 1, 0) over ℚ with unit weights has d₁d₀ = 0, Φ₁ = 2 attained at f = (0, 1, 0) (residual (0, 2, 0)) and certified by the circulation y = (1, 1, −1), Γ₂ = |1 + 1 − 0| = 2, ‖d₁‖_{1→1} = 1 and R_cl = 1, which saturates the closure-ratio bound; the class is ActiveClosureFailure. Without the 2-simplex, C² = 0 and the cyclic field (1, 1, 1) has Φ₁ = 3 (certificate y = (1, 1, 1)) and Γ₂ = 0, a ClosedResidual; filling the triangle converts that closed residual into closure charge without changing Φ₁. Orthogonal projection of δ onto ker d₁ subtracts (2/3, 2/3, −2/3) ∈ im d₁*, which meets im d₀ only in 0, so it is not a repair and Φ₁ of the original class stays 2.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 1
- cited Lean, Rust or Python symbols found in their in-repo files: 1
- distinct cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add an in-repo Rust or Python runnable test (0 in-repo Rust or Python file(s) cited, none a test) and a recorded statement-match review

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Unit weights on the declared filled triangle over Q (assumption)

## Bottleneck

Lean filled_triangle_signature covers the filled-triangle numbers over ℚ, including that 1 is the least operator constant; the hollow comparison and the projection remark are prose with Python checks, and the certificate fixes the value Φ₁ = 2, not one repair.

## Source status

WDP monograph §4.11 WDP-CH04-P08; Lean Obstruction.filled_triangle_signature (exact)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean)
- sha256 (`bytes`): `bef8623978d7c0735b4a02db686664b03b61e18bba0e5ef6bcce81ff4234dd0a`
- cited in: node.lean, node.source, record TFQ-0548
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_wdp.json](../../../dag/research/lean_replay_campaign_wdp.json) (module `Imported.WitnessedDifference.WitnessedDifference.Obstruction`): recorded sha256 `bef8623978d7c0735b4a02db686664b03b61e18bba0e5ef6bcce81ff4234dd0a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `filled_triangle_signature` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms filled_triangle_signature` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_wdp/src/obstruction.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/obstruction.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/06_wdp/tfq_0548_wdp_filled_triangle.md`

- file: [dag/derivations/06_wdp/tfq_0548_wdp_filled_triangle.md](../../../dag/derivations/06_wdp/tfq_0548_wdp_filled_triangle.md)
- sha256 (`lf-normalised`): `3c358f3d91f911caf0abd90a52ca68a38c5a276c126526c664cf118c7593fc6c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0548
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:upstream/omega_engine/crates_rs/omega_wdp/src/obstruction.rs::DualWitnessCertificate`
- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/unit_tests/test_obstruction.py::test_worked_filled_triangle_signature_and_certificate`

## Routes

Incoming (1):

- `PGW-R-WDP-FILLED-TRIANGLE` `DERIVED_LEAN`: [PG-WDP-QUOTIENT-EXACT-SEQUENCE](PG-WDP-QUOTIENT-EXACT-SEQUENCE.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-SYNTHESIS-TRUNK-TIERS` `DERIVED_PROSE`: [PGW-WDP-SYNTHESIS-TRUNK-TIERS](PGW-WDP-SYNTHESIS-TRUNK-TIERS.md) (DEFINITION)
