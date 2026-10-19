# [TFQ-0169] Compare finite entropies as exact rational combinations of prime logarithms, not as

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `a2ba8c13-65da-5e52-a3cd-182e779c6b97`  
> **Parent Derivation**: [TFQ-0167](tfq_0167_admit_only_exact_nonnegative_rational_masses_that_sum_to_one_with_no.md)

---

## 1. Abstract & Formal Statement

Entropy in this crate is a LogForm, not a float and not a measurement-interval kind. src/log_form.rs stores Shannon, relative, Renyi, and mutual information as rational coefficients of logarithms of primes, using unique factorization so two forms match exactly when their coefficient maps match. Enclosure returns a rational interval around that form; the interval is a bound on the logarithm, not authority to replace the form by a float. The obligation is to authorize entropy comparisons from the exact coefficient map, and to keep those rational enclosures distinct from omega_measurement interval evidence.

### Governing Obligation
Compare finite entropies as exact rational combinations of prime logarithms, not as floats.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`not located`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_finite_probability/src/log_form.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F000_finite/floor.yaml`
