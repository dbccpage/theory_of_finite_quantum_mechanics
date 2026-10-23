# PGW-WDP-FINITE-VALUATIONS

Stage: [WDP](../stages/WDP.md). Status: `DEFINITION`. Evidence grade: **E3**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> WDP-CH08-D01: finite families A and B are congruent relative to a comparison family K when a matching preserving K is exhibited, a bijective correspondence with no primitive number object that still presupposes the exhibited families, so plurality itself is not derived from one cut. With a declared mass m: W → ℝ≥0, μ(A) = Σ_{w∈A} m(w) is finitely additive by construction, and on a declared finite partition with μ(W) \> 0 the values p(A_i) = μ(A_i)/μ(W) are nonnegative and sum to 1 (WDP-CH08-P01). WDP-CH08-O01: a nonnegative additive valuation on a finite Boolean algebra has unique atom masses and pushforwards, and witness-level masses extending it are unique exactly when every nonsingleton atom has mass zero. WDP-CH08-C01 (conditional): an aggregator with a continuous associative composition law with identity 0, singleton values ct with c \> 0 and replica extensivity has composition x + y and value c Σ_e a_e. WDP-CH09-P01: |z_i|^q / Σ_j |z_j|^q is a probability vector for every q \> 0, and distinct exponents give distinct vectors when two nonzero magnitudes differ, so normalization does not select q = 2.

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

- Declared mass on a finite witness family and a declared finite partition with positive total mass (assumption)
- For C01: continuity, associativity and replica extensivity of the aggregation law (assumption)

## Bottleneck

A normalized finite valuation is not a frequency, propensity, degree of belief or countably additive measure; Lean Probability.sum_normalizedMultiplicity covers natural multiplicities only, and the monograph's C01 argument uses no Aczél representation theorem, superseding the education page's import reading.

## Source status

WDP monograph §8.1-§8.5 WDP-CH08-D01/P01/O01/C01 and §9.2 WDP-CH09-P01

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/Imported/WitnessedDifference/WitnessedDifference/Probability.lean`

- file: [lean4/Imported/WitnessedDifference/WitnessedDifference/Probability.lean](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Probability.lean)
- sha256 (`bytes`): `b1258e1ae67c5ff03ea365400ad78fb255e1342b550d28905d574297f7403936`
- cited in: node.lean, record TFQ-0552
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_wdp.json](../../../dag/research/lean_replay_campaign_wdp.json) (module `Imported.WitnessedDifference.WitnessedDifference.Probability`): recorded sha256 `b1258e1ae67c5ff03ea365400ad78fb255e1342b550d28905d574297f7403936` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Classical.choice, Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build   # the library that contains lean4/Imported/WitnessedDifference/WitnessedDifference/Probability.lean`

| Symbol | Counts | Found | Declaration form | Audited axioms | Check |
|---|---|---|---|---|---|
| `sum_normalizedMultiplicity` | yes | yes | yes | Classical.choice, Quot.sound, propext | `#print axioms sum_normalizedMultiplicity` |
- counts toward the grade: yes

### Rust: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/rust/src/foundational_bridges.rs`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/rust/src/foundational_bridges.rs`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.rust
- counts toward the grade: no

### Documents and data: `dag/derivations/06_wdp/tfq_0552_wdp_finite_valuations.md`

- file: [dag/derivations/06_wdp/tfq_0552_wdp_finite_valuations.md](../../../dag/derivations/06_wdp/tfq_0552_wdp_finite_valuations.md)
- sha256 (`lf-normalised`): `5efad9227df52e3ad6c798f77f87592e77d39042af507e3606d969e3071f3fb7`
- generated view: listed, not counted
- cited in: node.source, record TFQ-0552
- counts toward the grade: no

### Documents and data: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`

- file: `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md`
- resolution: `external_unresolved` (a path outside this repository; neither confirmed nor refuted here)
- cited in: node.source
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/rust/src/foundational_bridges.rs::MultiplicityDistribution`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/probability.py::disjoint_additivity`
- `external:the_symbol_game/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/probability.py::event_probability`

## Routes

Incoming (1):

- `PGW-R-WDP-FINITE-VALUATIONS` `DERIVED_PROSE`: [PGW-WDP-RETENTION-PACKET](PGW-WDP-RETENTION-PACKET.md) (DEFINITION)

Outgoing (1):

- `PGW-R-WDP-SYNTHESIS-TRUNK-TIERS` `DERIVED_PROSE`: [PGW-WDP-SYNTHESIS-TRUNK-TIERS](PGW-WDP-SYNTHESIS-TRUNK-TIERS.md) (DEFINITION)
