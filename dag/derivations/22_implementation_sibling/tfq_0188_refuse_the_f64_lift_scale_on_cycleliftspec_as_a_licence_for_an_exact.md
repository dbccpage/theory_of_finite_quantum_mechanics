# [TFQ-0188] Refuse the f64 lift_scale on CycleLiftSpec as a licence for an exact

> **Stage**: `IMPLEMENTATION_SIBLING` | **Status**: `GAP`  
> **UUID**: `8872f729-8203-5290-891d-5a3032139b2f`  
> **Parent Derivation**: [TFQ-0187](tfq_0187_keep_lift_licences_as_descent_paired_obstruction_metadata_not_as_a_hilbert_derivation.md)

---

## 1. Abstract & Formal Statement

CycleLiftSpec breaks the exact-licence story by storing lift_scale as f64. src/cycle_lift_spec.rs declares cycle_node_indices as a vector of usize and lift_scale as f64, and its error NonFiniteLiftScale only rejects a non-finite float. That is not a BigRational descent witness. FQ-IMPL-F64-GATING counts three omega_lifts files in legacy_debt and says a float may propose but never authorize a result. The obligation is to refuse this f64 scale as a lift licence. PrimitiveLiftCertificate.lean is only a boolean checklist of propositions and does not supply the missing exact scale.

### Governing Obligation
Refuse the f64 lift_scale on CycleLiftSpec as a licence for an exact finite lift.

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
- [`lean4/quantum_mechanics/PrimitiveLiftCertificate.lean`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`external:sha256:2908042afeabf18585e04298b65ebe3d19f65c7d68d6e6761fce9a908e9a59d7`](../../code/rust/src/)
- [`external:sha256:c58c7a83c804699a86ad761d7e3f9456f56daa0c1ba50dcff68378049955b99c`](../../code/rust/src/)
- [`external:sha256:7cdc5e0bce6c29a1598347459d048b0b89de2fe7170e1892096c2f9e93c3db89`](../../code/rust/src/)
- [`external:sha256:8a8eb6cdf84a34d0de92f887c5efc2d394dbc6aed7be3b70394c09b72d36f078::DiagnosticBridgeError`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche5_full_dag_177_node_coverage_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`not located`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`
- **Primary Source Paths**:
  - `external:sha256:98533bbe8dde6cad1f5bbd9d2de0fb85196b2d44c74964cec5a96620ff69c94f`

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
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 8a80e51136e8fca160ef271621bb3bcde0e90531dcb8cc3516a7ce5e97a025fc`
