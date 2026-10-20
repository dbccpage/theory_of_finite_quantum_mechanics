# [TFQ-0177] Leave the existence of seven mutually unbiased bases in dimension 6 open

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `e96070e1-5911-5764-9fab-3c39f39315c9`  
> **Parent Derivation**: [TFQ-0176](tfq_0176_treat_omega_mub_as_reconstruction_bookkeeping_not_as_the_owner_of_a_completed.md)

---

## 1. Abstract & Formal Statement

Seven mutually unbiased bases in dimension 6 stay open. The README titled MUB(6): exact reductions, conditional interfaces and open gaps says whether seven mutually unbiased bases exist in dimension six is open, that the deposit does not settle it, and that gap G1 is OPEN. The F004 register repeats that G1 is OPEN, that code/src/main.rs prints a banner and does not run a solver, and that R6 and R7 stay NOT_A_CERTIFICATE. The obligation is to leave MUB(6) existence unresolved. Checked reductions and conditional interfaces in that deposit are not a substitute for the missing global count.

### Governing Obligation
Leave the existence of seven mutually unbiased bases in dimension 6 open.

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
- [`code/rust/src/mub/src/omega_native/mub6_smale_sentry.rs`](../../code/rust/src/)
- [`absent: no local rust twin located for omega_engine_atlas/coda_atlas/F004_papers/010_mub6/rust/network_simplex.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`code/python/src/mub/mub_verify/a1_collar_swarm.py`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0178](tfq_0178_accept_a_mub_6_stated_region_bit_only_from_the_exact_certificate_never_from.md)
- [TFQ-0180](tfq_0180_keep_lean_mub_reconstructions_in_dimensions_3_and_4_from_being_cited.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
