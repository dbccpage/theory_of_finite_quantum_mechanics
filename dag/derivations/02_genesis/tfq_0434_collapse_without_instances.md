# [TFQ-0434] collapse-without-instances

> **Stage**: `GENESIS` | **Status**: `PROVED_LEAN`  
> **UUID**: `8ac0258b-1cb7-5e88-9498-93dfb3573eed`  
> **Parent Derivation**: [TFQ-0433](tfq_0433_contexts_plugging_profiles.md)

---

## 1. Abstract & Formal Statement

With no admitted instances, the derivability of a plugged context depends only on its form, so every pair of data is observationally collapsed (collapsed_of_no_insts). Uniform rules do not change this: a ruled form makes every plugging derivable alike. Retaining another datum alone therefore need not increase expressive power.

### Governing Obligation
Show that a regime whose instance list is empty collapses every pair of data, whatever its forms and uniform rules.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The statement covers instance-free regimes only; once an instance is admitted collapse is decided by the profiles, and a later uniform rule can again erase a separation (TFQ-0385).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean::collapsed_of_no_insts`](../../../lean4/Imported/Genesis19l57g1/Derivation/Inertia.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/profile.rs::coverage_is_constant_across_data_at_a_fixed_context` (private upstream source, not in this repository)

### Python Oracles & Numerical Evaluators
- `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/observe.py::collapsed_pairs` (private upstream source, not in this repository)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/paper.md:243-248`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:235-237`
