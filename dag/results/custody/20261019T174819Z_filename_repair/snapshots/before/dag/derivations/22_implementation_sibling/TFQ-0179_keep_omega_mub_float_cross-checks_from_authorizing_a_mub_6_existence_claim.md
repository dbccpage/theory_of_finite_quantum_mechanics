# [TFQ-0179] Keep omega_mub float cross-checks from authorizing a MUB(6) existence claim

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `GAP`  
> **UUID**: `79cdac0c-c928-52f2-8f96-d6c20c25aef5`  
> **Parent Derivation**: [TFQ-0178](TFQ-0178_accept_a_mub_6_stated-region_bit_only_from_the_exact_certificate_never_from.md)

---

## 1. Abstract & Formal Statement

Float cross-checks in omega_mub remain legacy debt beside the exact lane. src/omega_native/mod.rs separates float_check from exact. The source tree lists d6_sos_float_sdp.rs next to exact modules such as d6_exact_sos.rs; this pass did not read the float solver body. derivation_dag.json node FQ-IMPL-F64-GATING records twenty omega_mub files in legacy_debt and states that a float may propose but never authorize a result, with sealed use empty. The obligation is to keep those float files from authorizing a MUB(6) count. The open existence question is unchanged by a float prefilter.

### Governing Obligation
Keep omega_mub float cross-checks from authorizing a MUB(6) existence claim.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `floating point as diagnostic only (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Exact faces use BigRational/Q(i)/Q(zeta_n); f64 faces are legacy debt, not agreed use. Which quantum_physics results still route through f64 is not audited here.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_and_fq_cptp_partial_transpose_born_lp_and_f64_diagnostic_firewall`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.fq_impl_amplitude_realification_and_pairing_bridges`](../../code/lean4/)
- [`not located`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_mub/src/omega_native/d6_exact_sos.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_mub/src/omega_native/d6_sos_float_sdp.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_mub/src/omega_native/mod.rs`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_quantum_physics/src/engine_bridge.rs::DiagnosticBridgeError`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`](../../code/rust/src/)
- [`omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`FQ-IMPL-F64-GATING`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `FQ-IMPL-F64-GATING` (`IMPLEMENTATION` / `DEFINITION`)
- **Mined Operad Family (`M2`)**: `OP-IMPLEMENTATION-FQ-IMPL-F64-GATING`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1260, -2520, 1890]`, `chord_potential = 1890`, `holonomy_gamma2 = 2520`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(FQ-IMPL-F64-GATING): 4*idx(126) + 3*stage_rank(10) + route_degree(1) == 535` ($\text{value} = 535$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(FQ-IMPL-F64-GATING): R_raw(302) - G_cob(146) - S_decoy(10) == 146 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 146$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `1` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_and_fq_cptp_partial_transpose_born_lp_and_f64_diagnostic_firewall`
- **Sovereign Rust Witness Anchor**: `omega_engine/crates_rs/omega_symbol_game/src/derivation_dag_witnesses.rs::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 8a80e51136e8fca160ef271621bb3bcde0e90531dcb8cc3516a7ce5e97a025fc`
