# [TFQ-0271] Show-the-packet protocol for a finite computation

> **Stage**: `FINITE_QM_INFORMATION` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `2a0ea7eb-3176-5160-9548-694a1eb958cc`  
> **Parent Derivation**: [TFQ-0270](tfq_0270_syndrome_distance_and_repair_capacity.md)

---

## 1. Abstract & Formal Statement

QM_103 is a public-protocol draft, companion to the projection-obstruction papers, asking that a physical quantum computation show its packet. The opened header does not contain a finished derivation of scalable computation. DS-QM103-SHOW-THE-PACKET-PROTOCOL is the derivation-graph id seen for the protocol. Read beside QM_101, the packet must name the code family, the noise hypothesis, the repair capacity, and the residual quotient that the threshold reading is supposed to shrink. A named file or a passing test does not replace that packet.

### Governing Obligation
Require a declared repair packet before a threshold reading is used, and leave the protocol's device claim open.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Rotated-surface-code packet is an illustrative placeholder (no measured numbers).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_and_fq_cptp_partial_transpose_born_lp_and_f64_diagnostic_firewall`](../../code/lean4/)
- [`lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.qm090_authority_firewall_zero_defect_iff`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_ds_qm_dynamics_structure_and_majorana_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`sources/atlas/papers/finite_quantum_mechanics/python/finite_qm`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`
- **Primary Source Paths**:
  - `external:git-tree:662d50fe40fdbf9e98bc3ae140d0355d3b3a45f5`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`DS-QM103-SHOW-THE-PACKET-PROTOCOL`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `DS-QM103-SHOW-THE-PACKET-PROTOCOL` (`FINITE_QM_STRUCTURE` / `DEFINITION`)
- **Mined Operad Family (`M2`)**: `OP-FINITE_QM_STRUCTURE-DS-QM103-SHOW-THE-PACKET-PROTOCOL`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [1690, -3380, 2535]`, `chord_potential = 2535`, `holonomy_gamma2 = 3380`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(DS-QM103-SHOW-THE-PACKET-PROTOCOL): 4*idx(169) + 3*stage_rank(8) + route_degree(2) == 702` ($\text{value} = 702$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(DS-QM103-SHOW-THE-PACKET-PROTOCOL): R_raw(378) - G_cob(185) - S_decoy(8) == 185 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 185$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `lean4/quantum_mechanics/DerivationDagQMClosure.lean::QuantumMechanics.DerivationDagQMClosure.ds_and_fq_cptp_partial_transpose_born_lp_and_f64_diagnostic_firewall`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche11_admitted_primitives_definitions_and_imported_assumptions_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = 540b20de1ba24d0ff4a34b72113513dedf2bbe7a537cc8bee98b088a051b7adc`
