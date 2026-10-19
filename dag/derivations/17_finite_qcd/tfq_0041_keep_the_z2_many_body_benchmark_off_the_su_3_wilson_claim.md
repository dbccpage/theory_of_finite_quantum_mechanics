# [TFQ-0041] Keep the Z2 many-body benchmark off the SU(3) Wilson claim

> **Stage**: `FINITE_QCD` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `b711630a-3784-5508-afe0-0d439ed8cde2`  
> **Parent Derivation**: [TFQ-0023](tfq_0023_keep_the_3_by_3_betti_count_separate_from_a_link_ensemble.md)

---

## 1. Abstract & Formal Statement

lattice_gauge_manybody_benchmark.rs is a separate finite control. open_tfim builds an exact Rational matrix for an open Ising chain of 1 to 8 sites. Z2LatticeGauge reads an F2ChainComplex, counts physical X labels as 2 to the power of edges minus the rank of the edge boundary, and flips a plaquette only when that plaquette is itself a physical label. The module header says no thermodynamic or continuum limit is inferred. There is no SU(3) link, no Creutz ratio, and no f64 path in this file. A Z2 Gauss count cannot authorize the rational SU(3) channel factors or the algebraic Wilson comparison.

### Governing Obligation
Keep the Z2 many-body benchmark off the SU(3) Wilson claim.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: the Ising and F2 Gauss benchmark is not a FiniteQM QCD theorem`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/lattice_gauge_manybody_benchmark.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: no finite_qm use case wraps Z2LatticeGauge`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
