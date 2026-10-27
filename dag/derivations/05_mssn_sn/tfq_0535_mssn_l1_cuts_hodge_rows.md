# [TFQ-0535] mssn-l1-cuts-hodge-rows

> **Stage**: `MSSN_SN` | **Status**: `SOURCE_RECORD`  
> **UUID**: `19e9ef05-615d-5fa9-8aba-3ec3bd0d3c65`  
> **Parent Derivation**: [TFQ-0534](tfq_0534_mssn_circulation_obstruction.md)

---

## 1. Abstract & Formal Statement

Atlas row MSS-8 specifies exact primal-dual ℓ¹ cochain cuts over ℚ: the primal Φ₁(c) = min over g of ‖c − d₀g‖_{1,ω}, the dual max ⟨c, y⟩ subject to d₀ᵀy = 0 and |y_e| ≤ ω_e, certified when primal and dual masses agree, and a zero-gap string without dual feasibility is refused. Row MSS-18 specifies the rational ℓ² Hodge split c = d_{k−1}p + h + d_k* q with d_k* = M_k⁻¹ d_kᵀ M_{k+1} for symmetric positive-definite rational weights, unique in its three components while the potentials p and q need not be. Both rows are specified with lift status unlicensed, and their evaluators ConcentricDispatcher and HodgeProjector are proposed labels.

### Governing Obligation
Treat MSS-8 and MSS-18 as specified verifier obligations: replay primal-dual feasibility and equal masses for ℓ¹, and nilpotence, positive definiteness, reconstruction and orthogonality for the ℓ² split, without crediting either evaluator label.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `External MSS atlas row specifications MSS-8 and MSS-18 (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> An ℓ¹ cut is a minimal representative modulo exact cochains, not an ℓ² Hodge decomposition; MSS-18 implies no smooth Riemannian or de Rham-Hodge statement, the evaluator label is not an implementation receipt, and the worked triangle values are in TFQ-0524.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `missing obligation: no Lean statement of the MSS-8 or MSS-18 row obligations`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust ConcentricDispatcher or HodgeProjector implementation is linked from the rows`

### Python Oracles & Numerical Evaluators
- `missing obligation: no Python evaluator for the MSS-8 or MSS-18 packets`

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `external:sha256:2e8d3a73acde99fa958aebc35782e04482da4bd3e02496770588b9b28cdb9c73:63-67`
  - `external:sha256:584042f0b0371f95e96e81c58a5f4c3e24fe37dc20103464999b3bbde4e461f6:40`
  - `external:sha256:584042f0b0371f95e96e81c58a5f4c3e24fe37dc20103464999b3bbde4e461f6:77-78`
