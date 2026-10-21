# [TFQ-0527] sn-e21-repair-rank

> **Stage**: `MSSN_SN` | **Status**: `SOURCE_RECORD`  
> **UUID**: `a43a422b-80f0-55ee-a4fc-724f91777783`  
> **Parent Derivation**: [TFQ-0523](tfq_0523_sn_e12_circulation_functional.md)

---

## 1. Abstract & Formal Statement

Example E21 takes vertices a, b, c, d and edges (ab, bc, ac, cd, da), so the 1-cycle space has dimension 5 − rank ∂₁ = 5 − 3 = 2, with z₁ = (1,1,−1,0,0) for triangle abc and z₂ = (0,0,1,1,1) for triangle acd. Adjoining two faces with boundaries z₁ and z₂ gives rank ∂₂ = 2, ∂₁∂₂ = 0 and H₁ = 0. Adjoining two free degree-two generators with the same boundary z₁ gives rank ∂₂ = 1 and dim H₁ = 1, so the receipt count is 2 while the repair rank is 1. Transport from orientation ca to the common basis edge ac needs e_ca = −e_ac, and a wrong sign gives ∂₁z ≠ 0.

### Governing Obligation
Compute rank ∂₂ for the submitted faces, verify ∂₁∂₂ = 0 and the remaining dim H₁, check orientation-sign transport, and count repair progress by boundary rank, not by receipt count.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The duplicate case is a chain-complex extension with two free generators, not two copies of one simplex; the page is a written finite example that grammar cases do not verify, and it does not establish 4D Regge gravity or a Bianchi identity.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `missing obligation: no Lean statement of E21 in the S(n) strand`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust check of E21 in the S(n) strand`

### Python Oracles & Numerical Evaluators
- `missing obligation: no Python check of E21 in the S(n) strand`

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_education/documentation/002_oesn/levels/level_21_discrete_4d_regge_curvature.md:42-47`
  - `omega_engine_education/documentation/002_oesn/levels/level_21_discrete_4d_regge_curvature.md:49-55`
  - `omega_engine_education/documentation/002_oesn/curriculum.md:163-166`
