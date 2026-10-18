# [TFQ-0008] Finite dynamics, instruments, and channels

> **Stage**: `FINITE_QM_DYNAMICS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `9a3ade1d-15a2-5016-a445-2b42ba90c577`  
> **Parent Derivation**: [TFQ-0007](../10_finite_qm_core/TFQ-0007_finite_quantum_mechanics_core_on_an_admitted_carrier.md)

---

## 1. Abstract & Formal Statement

After the finite carrier, the required dynamics are finite: an instrument or measurement update, a path sum on a finite graph, a unitary or Hamiltonian shadow on a finite matrix, and a channel that is either exact or explicitly imported. The derivation note leaves the step from stochastic kernels to completely positive maps as a gap. Python, Rust, and Lean 4 must each state the finite map and the hypothesis it uses. A numerical CPTP check at a fixed tolerance is a diagnostic. It does not authorize the exact channel.

### Governing Obligation
Separate finite instruments, path sums, and channels from any continuum generator.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Formalization
*Formalization active. Proof obligations tracked under zero-sorry regime.*

### Sovereign Rust Certifiers
*Computational witness tracked under `theory_of_finite_qm` crate.*

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0009](../14_finite_gauge/TFQ-0009_finite_gauge_cochain.md)
- [TFQ-0052](../14_finite_gauge/TFQ-0052_each_language_must_carry_on_a_declared_m_2_q_i_packet_d0_of_an.md)
- [TFQ-0084](../19_finite_qg/TFQ-0084_finite_quantum-gravity_shadow.md)
- [TFQ-0086](../19_finite_qg/TFQ-0086_fq-gap-continuum-hilbert-lift_stays_unpaid_no_continuum_hilbert_space_is_admitted_at_the_root.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/floor.yaml`
