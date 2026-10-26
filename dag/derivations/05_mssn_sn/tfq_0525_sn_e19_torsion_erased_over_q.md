# [TFQ-0525] sn-e19-torsion-erased-over-q

> **Stage**: `MSSN_SN` | **Status**: `SOURCE_RECORD`  
> **UUID**: `c1ea3d31-3a25-517e-b67e-35a7b1c35330`  
> **Parent Derivation**: [TFQ-0523](tfq_0523_sn_e12_circulation_functional.md)

---

## 1. Abstract & Formal Statement

Example E19 takes the free chain complex C₂ = ℤ → C₁ = ℤ → C₀ = ℤ with ∂₂(1) = 2 and ∂₁ = 0. The cycle z = 1 is nonzero in H₁ = ℤ/2 because no integer c has 2c = 1. After tensoring with ℚ, ∂₂(1/2) = 1, so H₁(C;ℚ) = 0, but the rational primitive 1/2 is not an integral repair witness. Adjoining one integer generator f with ∂₂f = 1 removes the class over ℤ at a cost of one new generator, against zero new generators for the coefficient change; replacing 2 by m ≥ 2 gives H₁ = ℤ/m over ℤ and 0 over ℚ.

### Governing Obligation
Verify non-exactness of z modulo m over ℤ, exhibit the rational primitive 1/m over ℚ, and keep a coefficient change apart from an integral boundary added in the source ring.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Erasing a class by changing coefficients supplies no integral repair, and a rational fraction 1/m offered as an integral repair receipt is refused; the page is a written finite example that grammar cases do not verify, and compute_integral_homology computes torsion factors for supplied integer matrices without a recorded run of this complex.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `missing obligation: no Lean statement of E19; MssnSmithNormalForm.lean checks supplied invariant-factor records only`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `omega_engine_education/documentation/003_oemssn/code/rust/src/smith_normal_form.rs::compute_integral_homology` (private upstream source, not in this repository)

### Python Oracles & Numerical Evaluators
- `missing obligation: no Python check of E19 in the S(n) strand`

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_education/documentation/002_oesn/levels/level_19_zeta_spectral_shadow.md:46-49`
  - `omega_engine_education/documentation/002_oesn/levels/level_19_zeta_spectral_shadow.md:51-54`
  - `omega_engine_education/documentation/002_oesn/curriculum.md:146-147`
