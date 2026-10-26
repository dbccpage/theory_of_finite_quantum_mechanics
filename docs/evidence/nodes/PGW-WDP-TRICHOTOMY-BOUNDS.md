# PGW-WDP-TRICHOTOMY-BOUNDS

Stage: [WDP](../stages/WDP.md). Status: `PROVED_PROSE`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> WDP-CH04-P04: in a window with d₁d₀ = 0 and a norm J meeting the norm hypothesis, every class \[h\] ∈ Q¹ has exactly one of ExactClass (\[h\] = 0), ClosedResidual (\[h\] ≠ 0 and Γ₂ = 0) or ActiveClosureFailure (Γ₂ \> 0); Φ₁ = 0 exactly on ExactClass, and every active class has Φ₁ \> 0. WDP-CH04-P05: Φ₁, Γ₂ ≥ 0, Γ₂ = 0 iff \[h\] ∈ H¹, Γ₂ ≤ ‖d₁‖_{J→1}Φ₁ (repair invariance of d₁h, then the infimum), no constant c \> 0 gives Γ₂ ≥ cΦ₁ when H¹ ≠ 0, and Γ₂ is a norm on Q¹/H¹. WDP-CH04-P06: if Φ₁ \> 0 then 0 ≤ R_cl ≤ ‖d₁‖_{J→1}, and the normalized ratio is undefined (0/0) when d₁ = 0. The norm hypothesis (ℝ, ℂ, or ℚ with J restricted from a norm on the real extension) is needed: J(x) = |x₀₁ + √2 x₁₂ + √3 x₀₂| is a norm on ℚ³, yet on the filled triangle with δ = (1, 1, 0) its repair values accumulate at 0, so Φ₁ = 0 while Γ₂ = 2.

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

- `proved_prose_no_in_repo_document`: no in-repo non-generated document among the counted sources. PROVED_PROSE with no in-repo source document cited.

## Imported structure

- Norm hypothesis: F = R or C, or F = Q with J the restriction of a norm on the real extension (assumption)

## Bottleneck

P04–P06 are written proofs; Lean covers item 4 of P05 (closure_charge_le_opnorm_mul_phi, with the greatest-lower-bound half of the infimum as hypothesis) and P06 for ℚ-valued costs only (closure_ratio_signature), and the exhaustive trichotomy test on three small complexes is a finite check.

## Source status

WDP monograph §4.8-§4.9 WDP-CH04-P04/P05/P06 written proofs; Lean narrower (item 4, Q-valued ratio)

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean)
- sha256 (`bytes`): `bef8623978d7c0735b4a02db686664b03b61e18bba0e5ef6bcce81ff4234dd0a`
- cited in: node.lean, record TFQ-0547
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_wdp.json](../../../dag/research/lean_replay_campaign_wdp.json) (module `Imported.WitnessedDifference.WitnessedDifference.Obstruction`): recorded sha256 `bef8623978d7c0735b4a02db686664b03b61e18bba0e5ef6bcce81ff4234dd0a` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `closure_charge_le_opnorm_mul_phi` | yes | yes | yes | module-level | `#print axioms closure_charge_le_opnorm_mul_phi` |
| `closure_ratio_signature` | yes | yes | yes | module-level | `#print axioms closure_ratio_signature` |

- counts toward the grade: yes

### Rust: `omega_engine/crates_rs/omega_wdp/src/primitive_axiomatics.rs`

- file: `omega_engine/crates_rs/omega_wdp/src/primitive_axiomatics.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/06_wdp/tfq_0547_wdp_trichotomy_bounds.md`

- file: [dag/derivations/06_wdp/tfq_0547_wdp_trichotomy_bounds.md](../../../dag/derivations/06_wdp/tfq_0547_wdp_trichotomy_bounds.md)
- sha256 (`lf-normalised`): `8ef860053168fef1c1fe63d45348649d14d146430a259b2dbc6942893fd15beb`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0547
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### Documents and data: `omega_engine_education/documentation/006_oewdp/levels/level_03_discrete_complex_cochains.md`

- file: `omega_engine_education/documentation/006_oewdp/levels/level_03_discrete_complex_cochains.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:upstream/omega_engine/crates_rs/omega_wdp/src/primitive_axiomatics.rs::TriadSignature`
- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/obstruction.py::classify_signature`
- `external:upstream/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/obstruction.py::obstruction_signature`

## Routes

Incoming (1):

- `PGW-R-WDP-TRICHOTOMY-BOUNDS` `DERIVED_PROSE`: [PGW-WDP-EXACT-SEQUENCE-H1-Q1](PGW-WDP-EXACT-SEQUENCE-H1-Q1.md) (PROVED_LEAN)

Outgoing (1):

- `PGW-R-WDP-SYNTHESIS-TRUNK-TIERS` `DERIVED_PROSE`: [PGW-WDP-SYNTHESIS-TRUNK-TIERS](PGW-WDP-SYNTHESIS-TRUNK-TIERS.md) (DEFINITION)
