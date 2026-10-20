# [TFQ-0052] Each language must carry: on a declared M_2(Q(i)) packet, d0 of an

> **Stage**: `FINITE_GAUGE` | **Status**: `COMPUTATIONAL_CONTROL`  
> **UUID**: `c9c0b80a-06fb-5fd3-ac5b-1c713ed76b1b`  
> **Parent Derivation**: [TFQ-0008](../11_finite_qm_dynamics/tfq_0008_finite_dynamics_instruments_and_channels.md)

---

## 1. Abstract & Formal Statement

gauge_cochain_complex.rs builds a finite gauge complex on a declared packet in M_2(Q(i)). Degree zero is four real coordinates of an anti-Hermitian generator. Degree one holds one scalar Born defect per declared probability and one Hermitian defect per effect and per state. d0 sends the generator to commutators with those effects and states and writes zero in the Born slots. from_declaration_with_limits refuses a bad shape or a budget overrun and does not test positivity or complete positivity. The Born table remains caller-declared. Rust, Python and Lean 4 must each carry that shape refusal.

### Governing Obligation
Each language must carry: on a declared M_2(Q(i)) packet, d0 of an anti-Hermitian generator is the commutator residual in C^1, and a shape or budget failure is a refusal.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `M_2 packet with trace and unitary gauge (assumption)`
- **Admitted**: `declared unitary step (assumption)`
- **Admitted**: `generator branch selection for periodic sector (assumption)`
- **Admitted**: `presheaf functoriality / restriction system: assumption`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The dichotomy is instance-level; the price theorems are definitional.

> [!WARNING]
> Whether the Genesis / WDP fragments derive flatness is for those fragments to say.

> [!WARNING]
> Packet-specific; general n unaddressed.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`absent: not located`](../../lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`absent: no local rust twin located for omega_engine/crates_rs/omega_quantum_physics/src/gauge_cochain_complex.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`absent: not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0053](tfq_0053_each_language_must_carry_a_unit_gaussian_edge_connection_covariant_difference_vertex.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics`
  - `omega_engine_atlas/coda_atlas/F002_continuum/S000_continuum_descent`
