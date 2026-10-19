# [TFQ-0359] Keep the Phi1 Banach-quotient reading on a finite-dimensional repair packet, and leave

> **Stage**: `L1_EMERGENCE` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `7a75c7af-1a3d-5cf5-b411-a61383a5988f`  
> **Parent Derivation**: [TFQ-0349](tfq_0349_compute_declared_phi1_and_gamma2_on_a_finite_window_and_do_not.md)

---

## 1. Abstract & Formal Statement

DAG node L1-QM002-O022A-PHI1-QUOTIENT says that for a finite-dimensional repair packet with c = d0, Phi1 of a class equals the Banach-quotient norm of the cofiber shadow. The node says the Lean statement named in the ledger is definitional, so the analytic identity is carried by the prose only, and that the unrestricted CODA-A bridge is refused and open. Route L1-R-PHI1-QUOTIENT takes the window node and the flatness axiom as inputs. This is still inside l1 emergence: it does not introduce a complex field, a circle action, or an inner product. AuthorityEffect is None.

### Governing Obligation
Keep the Phi1 Banach-quotient reading on a finite-dimensional repair packet, and leave the unrestricted CODA-A bridge open.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Banach quotient construction on finite-dim packet: lift`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Coboundary shift invariance (w + d0 g) - d0(f + g) = w - d0 f and L1 additivity are mechanized in DerivationDagQMClosure.lean.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.l1_gs001_replica_and_phi1_quotient_invariance`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_quantum_physics/src/cochain_repair_code.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/trace_distance_quotient.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche3_emergence_dynamics_heisenberg_and_qec_witness`](../../code/rust/src/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`L1-QM002-O022A-PHI1-QUOTIENT`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `L1-QM002-O022A-PHI1-QUOTIENT` (`L1_EMERGENCE` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-L1_EMERGENCE-L1-QM002-O022A-PHI1-QUOTIENT`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [750, -1500, 1125]`, `chord_potential = 1125`, `holonomy_gamma2 = 1500`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(L1-QM002-O022A-PHI1-QUOTIENT): 4*idx(75) + 3*stage_rank(5) + route_degree(3) == 318` ($\text{value} = 318$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(L1-QM002-O022A-PHI1-QUOTIENT): R_raw(175) - G_cob(85) - S_decoy(5) == 85 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 85$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.pg_collapse_barrier_protected_questions_and_l1_kkt_trace_embed`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4-flash` | `status = PASS` | `receipt_sha256 = 8e87d80a31ed7f0456ececad01e16135b6359e316414689d1afdcec79ea3bbbf`
