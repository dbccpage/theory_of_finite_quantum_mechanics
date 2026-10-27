# [TFQ-0178] Accept a MUB(6) stated-region bit only from the exact certificate, never from

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `66dbd8c5-f415-58f9-a6ee-3dd2bfcf2b7a`  
> **Parent Derivation**: [TFQ-0177](tfq_0177_leave_the_existence_of_seven_mutually_unbiased_bases_in_dimension_6_open.md)

---

## 1. Abstract & Formal Statement

The MUB(6) claim firewall refuses a global solution bit even when a float is handed in. src/omega_native/mub6_firewall.rs stores the line stated region only; mints no authority, with AUTHORITY_EFFECT None. src/omega_native/mub6_claim_gate.rs builds a StatedRegionSeal whose mub6_equals_3, mub6_at_most_3, global_solution, and verified_certificate fields are documented as always false, and certificate_from_exact_only discards its f64 argument. The obligation is to accept only the exact EnclosedTriple certificate from that call.

### Governing Obligation
Accept a MUB(6) stated-region bit only from the exact certificate, never from a float or a global flag.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: not located`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/mub/src/omega_native/mub6_firewall.rs`](../../code/rust/src/)
- [`code/rust/src/mub/src/omega_native/mub6_claim_gate.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0179](tfq_0179_keep_omega_mub_float_cross_checks_from_authorizing_a_mub_6_existence_claim.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
