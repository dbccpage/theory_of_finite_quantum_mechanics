# PGW-WDP-FILLED-TRIANGLE

Stage: [WDP](../stages/WDP.md). Status: `PROVED_LEAN`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> WDP-CH04-P08: on vertices {0, 1, 2}, edges (01, 12, 02) and one 2-simplex, with d₀f = (f₁ − f₀, f₂ − f₁, f₂ − f₀) and d₁x = x₀₁ + x₁₂ − x₀₂, the field δ = (1, 1, 0) over ℚ with unit weights has d₁d₀ = 0, Φ₁ = 2 attained at f = (0, 1, 0) (residual (0, 2, 0)) and certified by the circulation y = (1, 1, −1), Γ₂ = |1 + 1 − 0| = 2, ‖d₁‖_{1→1} = 1 and R_cl = 1, which saturates the closure-ratio bound; the class is ActiveClosureFailure. Without the 2-simplex, C² = 0 and the cyclic field (1, 1, 1) has Φ₁ = 3 (certificate y = (1, 1, 1)) and Γ₂ = 0, a ClosedResidual; filling the triangle converts that closed residual into closure charge without changing Φ₁. Orthogonal projection of δ onto ker d₁ subtracts (2/3, 2/3, −2/3) ∈ im d₁*, which meets im d₀ only in 0, so it is not a repair and Φ₁ of the original class stays 2.

## Grade

Evidence grade **E3** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 3
- cited Lean, Rust or Python symbols found in their in-repo files: 2
- distinct cited Lean declarations covered by a current replay receipt: 1
- counted in-repo runnable tests: 1
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: add a recorded statement-match review

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
- sha256 (`bytes`): `b5adb85d12297d203151348422a0400482d6cac0397e8fcc5381c9c8a54c9885`
- cited in: node.lean, node.source, record TFQ-0548
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_wdp.json](../../../dag/research/lean_replay_campaign_wdp.json) (module `Imported.WitnessedDifference.WitnessedDifference.Obstruction`): recorded sha256 `b5adb85d12297d203151348422a0400482d6cac0397e8fcc5381c9c8a54c9885` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `filled_triangle_signature` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms filled_triangle_signature` |

- counts toward the grade: yes

### Python: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_obstruction.py`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_obstruction.py](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_obstruction.py)
- sha256 (`bytes`): `5a88f14b6c7d3118868d35e112487ee944ca200ee690736a22a867f2c461ca9b`
- cited in: record TFQ-0548
- check: `python -m pytest atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_obstruction.py::test_worked_filled_triangle_signature_and_certificate`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `test_worked_filled_triangle_signature_and_certificate` (python_test) | yes | yes | yes | - | `python -m pytest atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/unit_tests/test_obstruction.py::test_worked_filled_triangle_signature_and_certificate` |

- counts toward the grade: yes

### Documents and data: `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md`

- file: [atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md)
- sha256 (`lf-normalised`): `753d1c99c799f84f9a71912b98082d590c89c531f980c112b62ee2a86ab2726b`
- cited in: node.source
- counts toward the grade: yes

### Documents and data: `dag/derivations/06_wdp/tfq_0548_wdp_filled_triangle.md`

- file: [dag/derivations/06_wdp/tfq_0548_wdp_filled_triangle.md](../../../dag/derivations/06_wdp/tfq_0548_wdp_filled_triangle.md)
- sha256 (`lf-normalised`): `7c6e2f1ef22c7bdd659a3c61207a3345f2df804f2b13f6c6060a489d5692f47a`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0548
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:sha256:67f95afb329218e2db037b98e7b7d632e0ee073156f58a6c3b03ff9a386b4702::DualWitnessCertificate`
- `external:upstream/external:sha256:67f95afb329218e2db037b98e7b7d632e0ee073156f58a6c3b03ff9a386b4702::DualWitnessCertificate`

## Routes

Incoming (1):

- `PGW-R-WDP-FILLED-TRIANGLE` `DERIVED_LEAN`: [PG-WDP-QUOTIENT-EXACT-SEQUENCE](PG-WDP-QUOTIENT-EXACT-SEQUENCE.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-SYNTHESIS-TRUNK-TIERS` `DERIVED_PROSE`: [PGW-WDP-SYNTHESIS-TRUNK-TIERS](PGW-WDP-SYNTHESIS-TRUNK-TIERS.md) (DEFINITION)
