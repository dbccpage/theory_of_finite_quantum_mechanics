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
- `external:sha256:c324dc40d52818d23c350f65d7713acab9e81db6593ffcd6dd904086069807bd::PromptCochainEvaluator` (private upstream source, not in this repository)

### Python Oracles & Numerical Evaluators
- `external:sha256:669f33dced65b7f88d61dd17f9e7876f65c8ae044ba03c38020d04aa36f18a37::test_native_certificate_positive_and_decisive_mutations` (private upstream source, not in this repository)
- `external:sha256:a0e1b641bd377518bac80db7c24ee5c8850a369402bb5e6ca1c741fc5fcddae6::NativeCochainJudge` (private upstream source, not in this repository)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `external:sha256:bacfa8ca0bcf63778acf28f60ecb84985b20b7332d38eebb7212d9008b08246c:1-8`
  - `external:sha256:dbfd225f093e2e37d27cf508e9437092906353b692249f8e65ed1faac61c7516:84-93`
  - `external:sha256:3512168b69694d721f7878accd7b9fb9a72493e3219e36b231bff25c485f4cb9:174`
