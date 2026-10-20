# [TFQ-0197] Feed finite gravity only the rational Regge proxy, not the arccosine deficit

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `26c2b6da-9136-5b6b-b171-abf3a15f1ad3`  
> **Parent Derivation**: [TFQ-0166](tfq_0166_record_these_sibling_crates_as_controls_under_authorityeffect_none_not_as_completed.md)

---

## 1. Abstract & Formal Statement

The finite gravity shadow is the exact rational Regge face, not a full general-relativity derivation. src/lib.rs says the crate is not continuum GR. src/exact_regge/mod.rs evaluates squared lengths, Cayley-Menger volume squares, Barrett-Crane simplicity, SO(4, Q) transitions, hinge holonomy products, and the rational proxy of area-squared times kappa. It states that the deficit angle is an arccosine and is not an element of Q, so the classical Regge sum is not evaluated. The obligation is to admit only that proxy, and only the flat decision flat_einstein_hilbert, never a float cutoff.

### Governing Obligation
Feed finite gravity only the rational Regge proxy, not the arccosine deficit or a full Einstein derivation.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/FiniteQFTAndGravity.lean`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`code/rust/src/wdp/lib.rs`](../../code/rust/src/)
- [`code/rust/src/category_theory/monoidal/mod.rs`](../../code/rust/src/)
- [`code/rust/src/general_relativity/discrete_spacetime.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0198](tfq_0198_keep_discrete_spin_foam_amplitudes_cyclotomic_and_refuse_a_continuum_or.md)
- [TFQ-0199](tfq_0199_do_not_treat_the_gr_holonomy_scaffold_or_the_2d_regge_sum.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
