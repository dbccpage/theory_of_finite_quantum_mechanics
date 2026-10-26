# [TFQ-0552] wdp-finite-valuations

> **Stage**: `WDP` | **Status**: `DEFINITION`  
> **UUID**: `47087444-272c-50a6-b069-9cca348019d7`  
> **Parent Derivation**: [TFQ-0541](tfq_0541_wdp_retention_packet.md)

---

## 1. Abstract & Formal Statement

WDP-CH08-D01: finite families A and B are congruent relative to a comparison family K when a matching preserving K is exhibited, a bijective correspondence with no primitive number object that still presupposes the exhibited families, so plurality itself is not derived from one cut. With a declared mass m: W → ℝ≥0, μ(A) = Σ_{w∈A} m(w) is finitely additive by construction, and on a declared finite partition with μ(W) > 0 the values p(A_i) = μ(A_i)/μ(W) are nonnegative and sum to 1 (WDP-CH08-P01). WDP-CH08-O01: a nonnegative additive valuation on a finite Boolean algebra has unique atom masses and pushforwards, and witness-level masses extending it are unique exactly when every nonsingleton atom has mass zero. WDP-CH08-C01 (conditional): an aggregator with a continuous associative composition law with identity 0, singleton values ct with c > 0 and replica extensivity has composition x + y and value c Σ_e a_e. WDP-CH09-P01: |z_i|^q / Σ_j |z_j|^q is a probability vector for every q > 0, and distinct exponents give distinct vectors when two nonzero magnitudes differ, so normalization does not select q = 2.

### Governing Obligation
Exhibit the matching behind every congruence claim, normalize exact masses only on a declared partition with positive total, and select no Born exponent from normalization.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared mass on a finite witness family and a declared finite partition with positive total mass (assumption)`
- **Admitted**: `For C01: continuity, associativity and replica extensivity of the aggregation law (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> A normalized finite valuation is not a frequency, propensity, degree of belief or countably additive measure; Lean Probability.sum_normalizedMultiplicity covers natural multiplicities only, and the monograph's C01 argument uses no Aczél representation theorem, superseding the education page's import reading.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/WitnessedDifference/WitnessedDifference/Probability.lean::sum_normalizedMultiplicity`](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Probability.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/rust/src/foundational_bridges.rs::MultiplicityDistribution` (private upstream source, not in this repository)

### Python Oracles & Numerical Evaluators
- `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/probability.py::disjoint_additivity` (private upstream source, not in this repository)
- `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/code/witnessed_difference/probability.py::event_probability` (private upstream source, not in this repository)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md:3218-3257`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md:3334-3399`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/witnessed_difference_programme.md:3456-3467`
