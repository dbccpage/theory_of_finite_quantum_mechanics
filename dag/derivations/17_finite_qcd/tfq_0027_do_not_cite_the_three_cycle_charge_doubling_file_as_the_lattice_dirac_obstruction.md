# [TFQ-0027] Do not cite the three-cycle charge-doubling file as the lattice Dirac obstruction

> **Stage**: `FINITE_QCD` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `10ab5fdb-fa38-5177-aed5-d92ace696890`  
> **Parent Derivation**: [TFQ-0026](tfq_0026_add_python_and_lean_replays_of_the_declared_doubling_count_or_leave.md)

---

## 1. Abstract & Formal Statement

wilson_species_count in the same file counts corners where the rational expression mass + 2*r*(number of pi components) is zero, with no trigonometric approximation. The header states that the Wilson term vanishes only at k=0 and anticommutes with no chirality matrix gamma_*. zero_mode_count is the kernel dimension s*N^d minus exact rank over Q(i) for a dense operator that must fit under MAX_CARRIER_DIMENSION. Even-N antiperiodic twists return zero species. IntegralRefinementC3C6.lean covers charge doubling on a three-cycle refined to six vertices. That file is not a stand-in for this lattice Dirac obstruction.

### Governing Obligation
Do not cite the three-cycle charge-doubling file as the lattice Dirac obstruction.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/IntegralRefinementC3C6.lean`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/lattice_dirac_doubling.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: wilson_species_count has no Python twin in finite_qm`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0028](tfq_0028_state_the_beta0_window_as_rational_arithmetic_and_repeat_the_map_s_withheld.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
