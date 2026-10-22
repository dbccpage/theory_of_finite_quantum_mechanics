# PGW-WDP-PHI-WELL-DEFINED-L1-DUALITY

Stage: [WDP](../stages/WDP.md). Status: `CONDITIONAL`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> WDP-CH04-P01: Φ_J(\[δ\]) = inf_f J(δ − d₀f) is independent of the representative, because δ' = δ + d₀g turns the infimum into one over h = f − g, a bijection of C⁰. WDP-CH04-P02 (conditional): when the repair space is finite-dimensional over ℝ or ℂ and J is a norm, the infimum is attained after quotienting ker d₀; the hypotheses cannot be dropped silently for seminorms or infinite carriers. WDP-CH04-C01 (conditional): with positive weights w, Φ_{1,w}(\[δ\]) = max{⟨y, δ⟩ : d₀*y = 0, |y_e| ≤ w_e}, an imported finite-dimensional convex-duality result (REF-MATH-005, Rockafellar, Convex Analysis) specialized to the declared weighted graph complex. In code, finite_quotient_l1 minimizes over an explicit candidate list, and exact_quotient_l1 solves the weighted ℓ¹ programme over Fraction and reports a value only after an independent certificate check.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

- Finite-dimensional convex (linear-programming) strong duality, REF-MATH-005 Rockafellar Convex Analysis, specialized to the declared weighted graph complex (assumption)
- Attainment hypothesis: repair space finite-dimensional over R or C and J a norm, not a seminorm (assumption)

## Bottleneck

Representative independence is unconditional; the weak direction of the duality is not imported (WDP-CH04-P07, TFQ-0348, Lean dual_certificate_lower_bound), and C01 is not shown for arbitrary coefficient spaces.

## Source status

WDP monograph §4.2-§4.3 WDP-CH04-P01, conditional P02 and C01 (imported LP duality)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.lean
- counts toward the grade: no

### Rust: `omega_engine/crates_rs/omega_wdp/src/fenchel_duality.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/fenchel_duality.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/06_wdp/tfq_0544_wdp_phi_well_defined_l1_duality.md`

- file: [dag/derivations/06_wdp/tfq_0544_wdp_phi_well_defined_l1_duality.md](../../../dag/derivations/06_wdp/tfq_0544_wdp_phi_well_defined_l1_duality.md)
- sha256 (`lf-normalised`): `a07f5297f73034c26ade86ee37723ca13b0222790a8a668e66c352e70760002c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0544
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine/crates_rs/omega_wdp/src/fenchel_duality.rs::FenchelDualityReceipt`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/cochains.py::finite_quotient_l1`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/obstruction.py::exact_quotient_l1`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Obstruction.lean::dual_certificate_lower_bound`

## Routes

Incoming (1):

- `PGW-R-WDP-PHI-WELL-DEFINED-L1-DUALITY` `CONDITIONAL_ON_IMPORT`: [PGW-WDP-GRAPH-COCHAIN-HOST](PGW-WDP-GRAPH-COCHAIN-HOST.md) (DEFINITION), [PGW-WDP-QUOTIENT-DEFECT-ROOT-P](PGW-WDP-QUOTIENT-DEFECT-ROOT-P.md) (DEFINITION), [PGW-SN-E08-WEIGHTED-L1-DUALITY](PGW-SN-E08-WEIGHTED-L1-DUALITY.md) (CONDITIONAL)

Outgoing (0):

