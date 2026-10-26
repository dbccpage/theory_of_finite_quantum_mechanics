# [TFQ-0545] wdp-closure-needs-degree

> **Stage**: `WDP` | **Status**: `DEFINITION`  
> **UUID**: `c43a77a8-f287-5fa3-b382-23e210e37763`  
> **Parent Derivation**: [TFQ-0542](tfq_0542_wdp_graph_cochain_host.md)

---

## 1. Abstract & Formal Statement

Given d₁: C¹ → C² from a finite 2-cell structure, the closure diagnostic Γ(δ) = J₂(d₁δ) descends to Q¹ exactly when d₁d₀ = 0 on the admissible repairs if J₂ is a norm (for a seminorm, exactly when im(d₁d₀) ⊆ ker J₂): necessity by comparing a repair with the zero representative, sufficiency by linearity. Otherwise K = d₁d₀ is itself a typed curvature or composition defect, calling Q¹ cohomology while K ≠ 0 is an error, and none of the window results of §§4.8–4.11 applies. WDP-CH04-D01 makes the d₁d₀ = 0 certificate part of the degree-1 window: automatic on the simplicial nerve route, verified for any hand-declared pair; degree_one_window multiplies the exact matrices and refuses a nonzero product with CERTIFICATE_MISMATCH.

### Governing Obligation
Compute K = d₁d₀ exactly for every declared pair, report a nonzero K as a typed composition defect, and apply closure descent, H¹ and the signature only when K = 0.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Declared d₁ from a finite 2-cell structure and closure norm J₂ (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> A typing rule for the window; it does not select which d₁ to declare, and a zero K does not derive the window from Genesis admission (TFQ-0344).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean::kappa_well_defined`](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/Obstruction.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no omega_wdp Rust check of the window-level composition defect K = d1 d0; the Python degree_one_window carries it`

### Python Oracles & Numerical Evaluators
- [`atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py::degree_one_window`](../../../atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/code/witnessed_difference/obstruction.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md:1361-1380`
  - `atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md:1467-1476`
  - `omega_engine_education/documentation/006_oewdp/levels/level_03_discrete_complex_cochains.md:330-337`
