# [TFQ-0351] Accept an integer finite list certificate only inside its capacity, circulation, feasibility,

> **Stage**: `L1_EMERGENCE` | **Status**: `SOURCE_RECORD`  
> **UUID**: `e1a166e1-a51d-5dd5-964d-16e5c6551f62`  
> **Parent Derivation**: [TFQ-0350](TFQ-0350_assume_d1_d0_0_only_by_a_declared_certificate_or_the.md)

---

## 1. Abstract & Formal Statement

Package 002_l1_native_cohomology, version 6.5.2, says Lean mechanizes a finite matrix certificate and integer-complex lemmas, while the general real Lp discussion stays classical prose. Ledger row L1C-TG says a finite list certificate with capacity, circulation, primal feasibility, and zero gap certifies global optimality for the stated integer model, and that there is no certificate-existence theorem and no Python-correctness theorem. L1C-T3 is weak duality on the integer 3-cycle, not strong duality.

### Governing Obligation
Accept an integer finite list certificate only inside its capacity, circulation, feasibility, and zero-gap hypotheses, and do not extend it to a general real vector theorem.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Integer-list scope. The 3-step iterator in the same paper is REFUTED per its ledger.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/003_l1_obstruction_framework/lean4/lp_general_certificate.lean::general_finite_certificate_optimality`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/fenchel_duality.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/fenchel_duality.rs::FenchelDualityReceipt`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/obstruction.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/obstruction.rs::DualWitnessCertificate`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-FRAMEWORK-KKT-CERT`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-FRAMEWORK-KKT-CERT` (`L1_EMERGENCE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-L1_EMERGENCE-L1-FRAMEWORK-KKT-CERT`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [760, -1520, 1140]`, `chord_potential = 1140`, `holonomy_gamma2 = 1520`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(L1-FRAMEWORK-KKT-CERT): 4*idx(76) + 3*stage_rank(5) + route_degree(3) == 322` ($\text{value} = 322$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(L1-FRAMEWORK-KKT-CERT): R_raw(177) - G_cob(86) - S_decoy(5) == 86 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 86$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = da35df572608b49dd8ca39e61e94655da84dfde8e059805c94d0fab255a64a07`
