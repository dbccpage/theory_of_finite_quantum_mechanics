# [TFQ-0340] Refuse a symmetry-equivariant distinguished point on a finite set of size at

> **Stage**: `WDP` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `11bda918-752c-5965-a878-13ce78ab5ea7`  
> **Parent Derivation**: [TFQ-0339](TFQ-0339_preserve_a_protected_answer_exactly_on_report_fibers_and_do_not_derive.md)

---

## 1. Abstract & Formal Statement

WDP-CH03-P01 states that no Sym(X)-equivariant distinguished-point selection exists on an unstructured finite set with at least two elements. WDP-CH03-D01 defines the asymmetry-price frontier as the family of inclusion-minimal declared input sets whose removal restores a symmetry that moves the output. WDP-CH03-N01 says the symmetry obstruction does not make retention, dynamics, or observers unavailable, but their selection is not free. DAG node PG-WDP-PROTECTED-QUESTIONS records the same triple. Its bottleneck says WDP-CH03-P03, the declare-then-assert one-item separation claim, has no Lean port in the ledger.

### Governing Obligation
Refuse a symmetry-equivariant distinguished point on a finite set of size at least two, and leave WDP-CH03-P03 without a Lean port.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> WDP-CH03-P03 (no response of at most one item separates a from b in the declare-then-assert grammar) is stated with no Lean port in the ledger.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed`](../../code/lean4/)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/lean4/WitnessedDifference/Symmetry.lean::no_fully_invariant_point`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_wdp/src/observer.rs`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`PG-WDP-PROTECTED-QUESTIONS`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `PG-WDP-PROTECTED-QUESTIONS` (`WDP` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-WDP-PG-WDP-PROTECTED-QUESTIONS`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [630, -1260, 945]`, `chord_potential = 945`, `holonomy_gamma2 = 1260`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(PG-WDP-PROTECTED-QUESTIONS): 4*idx(63) + 3*stage_rank(4) + route_degree(2) == 266` ($\text{value} = 266$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(PG-WDP-PROTECTED-QUESTIONS): R_raw(146) - G_cob(71) - S_decoy(4) == 71 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 71$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 7dc69b01d4c56857c0b1f3b1378008b0bf6a42e28cae15f583ce4464d39be9b1`
