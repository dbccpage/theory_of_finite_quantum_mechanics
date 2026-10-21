# [TFQ-0509] pfp-c4-certificate

> **Stage**: `AUTHORIZATION` | **Status**: `SOURCE_RECORD`  
> **UUID**: `95811873-a405-5a41-b167-ad4e056422c2`  
> **Parent Derivation**: [TFQ-0508](tfq_0508_pfp_stealth_cochain_phi1_gamma2.md)

---

## 1. Abstract & Formal Statement

On the supplied oriented 4-cycle with vertices 0 to 3, edges 01, 12, 23, 03 in that order, one declared face 01+12+23−03 and c = (2, −3, 5, 7), the potential a = (0, 2, −1, 4) gives d₀a = (2, −3, 5, 4) and residual r = (0, 0, 0, 3) with L1 norm 3, an upper bound. The dual w = (−1, −1, −1, 1) is feasible (max |wᵢ| = 1 and d₀ᵀw = 0 at all four vertices) with w·c = 3, so every potential leaves L1 cost at least 3 and φ₁ = 3. The face row d₁ = (1, 1, 1, −1) satisfies d₁d₀ = 0 and d₁c = −3, so γ₂ = 3. The fixture c4_public_input.json carries this complex, and test_native_certificate_positive_and_decisive_mutations checks the certificate through the native Rust checker, rejects a +1 change to each answer field and accepts a constant shift of the potential; it passed in the recorded receipt of 2026-10-19 (2 passed, 0 failed).

### Governing Obligation
Check the C4 certificate with exact rationals: primal residual norm, dual feasibility (|wᵢ| ≤ 1, d₀ᵀw = 0), matching objectives w·c = ‖r‖₁ = 3, and γ₂ = |d₁c| = 3.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Supplied oriented C4 complex, L1 edge norm and rational coefficients, as declared in c4_work_unit.json (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> A finite certificate for one supplied complex: φ₁ = γ₂ here does not hold on all complexes or norms, and neither the certificate nor a schema check supplies a Hilbert space, a Born rule or an authorization.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `missing obligation: no Lean statement of the C4 optimum`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_symbol_game_runtime/src/cochain.rs::PromptCochainEvaluator`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine/crates_rs/omega_symbol_game_runtime/src/cochain.rs)

### Python Oracles & Numerical Evaluators
- [`omega_engine_pfp/infrastructure/finite_qm_cochain_judge.py::NativeCochainJudge`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_pfp/infrastructure/finite_qm_cochain_judge.py)
- [`omega_engine_pfp/tests/finite_qm_workflow/test_finite_qm_reference_workflow.py::test_native_certificate_positive_and_decisive_mutations`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_pfp/tests/finite_qm_workflow/test_finite_qm_reference_workflow.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_pfp/fixtures/finite_qm_workflow/c4_public_input.json:1-8`
  - `omega_engine_education/documentation/004_oepfp/levels/level_finite_qm_certificate_walkthrough.md:84-93`
  - `omega_engine_product_planning_office/plans/review_remediation/evidence/batch_13/c4_native_actual.json:174`
