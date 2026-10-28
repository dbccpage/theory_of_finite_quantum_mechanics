# [TFQ-0176] Treat tfqm_mub as reconstruction bookkeeping, not as the owner of a completed

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `cb492133-3fa1-5cf8-ad31-ba3e2c0dc250`  
> **Parent Derivation**: [TFQ-0166](tfq_0166_record_these_sibling_crates_as_controls_under_authorityeffect_none_not_as_completed.md)

---

## 1. Abstract & Formal Statement

MUB reconstruction in tfqm_mub is not a completed existence derivation. src/lib.rs says nothing there mints authority and that the exact finite MUB constructions and the projector-algebra verifier live in quantum_physics::mub. src/native/mod.rs repeats that split: exact certificates, campaign corpora, and float cross-checks are separate modules, while the finite carriers are re-exported from the physics crate. The obligation is to cite this crate as reconstruction bookkeeping and stated-region checks. It does not settle how many mutually unbiased bases exist in dimension 6.

### Governing Obligation
Treat tfqm_mub as reconstruction bookkeeping, not as the owner of a completed MUB derivation.

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
- [`code/rust/src/wdp/lib.rs`](../../code/rust/src/)
- [`code/rust/src/category_theory/monoidal/mod.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`code/python/src/mub/mub_verify/a1_collar_swarm.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0177](tfq_0177_leave_the_existence_of_seven_mutually_unbiased_bases_in_dimension_6_open.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:sha256:3429888abb5e68b4f86f2bd9efe085b8dcdc981179166df315b7b6acf23de0b6`
