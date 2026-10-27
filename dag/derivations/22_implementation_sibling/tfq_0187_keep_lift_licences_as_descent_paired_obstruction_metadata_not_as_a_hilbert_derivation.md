# [TFQ-0187] Keep lift licences as descent-paired obstruction metadata, not as a Hilbert derivation

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `5b8f21a1-efaf-5b0c-98bd-06f08d308e60`  
> **Parent Derivation**: [TFQ-0166](tfq_0166_record_these_sibling_crates_as_controls_under_authorityeffect_none_not_as_completed.md)

---

## 1. Abstract & Formal Statement

Lift licences in omega_lifts are obstruction-calculus metadata, not a Hilbert derivation. src/lib.rs defines a lift as a map from Q_n to Q_{n+1} with a forgetful descent back, and says no lift is admissible without an explicit descent map. src/lift_license.rs labels LiftLicense as legacy metadata for that pair, not the maps themselves, and says the record is not used as proof that a lift is licensed. Candidate evaluations in candidate.rs carry Phi1 and Gamma2 as BigRational. The obligation is to keep a licence candidate from being read as an inner-product space, a Born rule, or a completed Hilbert lift.

### Governing Obligation
Keep lift licences as descent-paired obstruction metadata, not as a Hilbert derivation.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/PrimitiveLiftCertificate.lean`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/wdp/lib.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:b4c26ab4c15e52b2f236eee0c1d2cf80b6ebd4b31d89fe09ac901b60d2185a90`](../../code/rust/src/)
- [`absent: no local rust twin located for external:sha256:efc412f17bdf7ccea00fff86d63ddc4df7aff36766b2caa0256c36d31dd3fe4f`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0188](tfq_0188_refuse_the_f64_lift_scale_on_cycleliftspec_as_a_licence_for_an_exact.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:
  - `external:sha256:98533bbe8dde6cad1f5bbd9d2de0fb85196b2d44c74964cec5a96620ff69c94f`
