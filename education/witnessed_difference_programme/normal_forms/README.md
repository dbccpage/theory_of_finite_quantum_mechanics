---
documentation_contract: education-documentation/v1
title: "Normal Forms — Witnessed Difference Programme (WDP)"
kind: normal-form-index
status: active
maturity: production
claim_status: source-grounded
authority_effect: "None"
canonical_source: omega_engine_education/documentation/014_normal_forms/contracts_normal_forms/
last_verified: 2026-09-29
---

# Normal Forms — Witnessed Difference Programme (WDP)

**AuthorityEffect:** None.\
**Canonical source:** [`omega_engine_education/documentation/014_normal_forms/contracts_normal_forms/`](../../014_normal_forms/contracts_normal_forms)

---

## Overview

This directory holds copies of twelve normal-form contracts from the
governance estate that are related to the WDP curriculum. Each file follows the
`smplx.nf.contract.v0` schema and is byte-identical to its canonical source.
Edit the canonical file, then re-copy; never edit the copy.

These contracts are governance artifacts, not part of the WDP monograph. None
of them is cited by the monograph or its ledger, and no WDP ledger row depends
on them. All twelve declare `contract_status: draft` and
`qualifies_as_true_normal_form: false`. Nine declare
`verification_status: executable` and three declare `absent`.

---

## Contracts in this directory

| ID | Name | Short | Verification | Related WDP level | How it relates |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `nf.wdp.wdnf` | Witnessed Difference Normal Form | WDNF | executable | [Level 0](../levels/level_00_admitted_cut.md) | Foundational WDP contract: eliminates ghost distinctions, requires support $|\Delta_{\mathrm{support}}| \ge 2$, irreflexivity, and explicit witness presence. |
| `nf.derivation.pdnf` | Primitive Difference Normal Form | PDNF | executable | [Level 0](../levels/level_00_admitted_cut.md) | Requires an asserted difference to be witnessed and irreflexive. WDP-CH01-P02 is the matching finite fact: irreflexivity is a declared ingredient, and with it a related pair forces distinctness. |
| `nf.derivation.obnf` | Obstruction Relativization Normal Form | OBNF | executable | [Level 3](../levels/level_03_discrete_complex_cochains.md) | Requires an obstruction to name the law it obstructs, as the degree-1 window names its repair map and norm before a residual is computed. |
| `nf.derivation.scnf` | Separation Cost Normal Form | SCNF | executable | [Level 3](../levels/level_03_discrete_complex_cochains.md) | Requires a cost claim to name its measure and say whether the minimizer is unique, as $\Phi_1$ is defined relative to a declared norm. |
| `nf.coda.tsnf` | Topological Simplex Normal Form | TSNF | executable | [Level 2](../levels/level_02_simplicial_sets_boundary_operators.md) | Enforces boundary nilpotence ($\partial^2 \equiv 0$) and quotient homology on oriented simplices under declared vertex total orders. |
| `nf.cochain.dhnf` | Discrete Hodge Normal Form | DHNF | executable | [Level 3](../levels/level_03_discrete_complex_cochains.md) | Enforces the orthogonal Hodge direct sum split $C^1 = \operatorname{im}(d_0) \oplus \mathcal{H}^1 \oplus \operatorname{im}(d_1^*)$; isolates harmonic loop obstructions. |
| `nf.fsp.bssnf` | Binary Sign-Switching Normal Form | BSS-NF | executable | [Demo 2](../demos/README.md) | FSP gauge transformation: diagonal signs $D_\alpha H D_\alpha$ eliminate negative weights iff cycle edge-bit holonomy $\sum s_e \equiv 0 \pmod 2$. |
| `nf.fsp.micnf` | Meron Involutive Cancellation NF | MIC-NF | executable | [Demo 2](../demos/README.md) | FSP meron involution: fixed-point free weight-preserving involution $\Xi$ pairing opposite-sign path configurations with non-negative survivor sector. |
| `nf.coda.eqnf` | Epistemic Quotient Normal Form | EQNF | executable | [Level 20](../levels/level_20_finite_adequacy_continuum_limits.md) | Requires every claim to carry its declared assumptions and a four-point audit, close to the four-part claim discipline used on every page. |
| `nf.epistemic.odnf` | Observer Distinguishability Normal Form | ODNF | absent | [Level 9](../levels/level_09_behavioral_quotients_finite_states.md), [Level 10](../levels/level_10_observation_measurement_calibration.md) | Excludes frame-free global sameness claims; WDP indexes every observation by a declared observer presentation. |
| `nf.epistemic.onf` | Orchestration Normal Form | ONF | absent | [Level 14](../levels/level_14_traceability_provenance_receipts.md) | Excludes agent laundering by requiring an action to declare its initiator, tool, and states. It concerns agent orchestration, not observation; its tie to WDP is the separation of authority from acceptance. |
| `nf.ontology.ainf` | Adjoint-Invariant Normal Form | AINF | absent | none direct | Concerns invariant leakage during structural lifts via an adjunction. The WDP monograph states no adjunction result; this contract is kept for cross-reference only. |
| `nf.ddc.hodge_canonical` | Hodge Canonical Normal Form | HCNF | executable | [Level 01](../levels/ddc/level_01_e_exact_repair.md) | Enforces orthogonal splitting $C^1 = \operatorname{im} d_0 \oplus \operatorname{im} d_1^\top \oplus \mathcal{H}^1$; prevents non-zero curl repair. |
| `nf.ddc.trace_merkle` | Trace Merkle Normal Form | TMNF | executable | [Level 04](../levels/ddc/level_04_i_integration.md) | Enforces SHA-256 Merkle chaining and deterministic replay for transitions. |
| `nf.ddc.context_boundary` | Context Boundary Normal Form | CBNF | executable | [Level 03](../levels/ddc/level_03_c_context_exposure.md) | Enforces disjoint edge partition $E(K') = E_{\mathrm{int}} \sqcup E_{\mathrm{bnd}}$ with non-decreasing defect mass. |
| `nf.ddc.loss_ledger` | Loss Ledger Normal Form | LLNF | executable | [Level 06](../levels/ddc/level_06_d_descent.md) | Enforces explicit `LossLedger` recording dropped tail coordinates and rational $\ell^1$ loss scalar. |
| `nf.ddc.refusal_receipt` | Refusal Receipt Normal Form | RRNF | executable | [Level 07](../levels/ddc/level_07_m_typed_refusal.md) | Enforces closed 7-member vocabulary, state preservation ($s' = s$), and $\{C, \Lambda, T\}$ routing. |
| `nf.ddc.terminal_partition` | Terminal Partition Normal Form | TPNF | executable | [Level 08](../levels/ddc/level_08_t_terminalization.md) | Enforces 9-way `CanContinue_n` halting and four-axis separation. |
| `nf.ddc.lift_ledger` | Lift Ledger Normal Form | LNLF | executable | [Level 05](../levels/ddc/level_05_lambda_structural_lift.md) | Enforces `FiniteLambdaLedger` chaining and $\ell^1$ norm preservation. |
| `nf.ddc.dual_witness` | Dual Witness Normal Form | DWNF | executable | [Level 02](../levels/ddc/level_02_r_residual_projection.md) | Enforces rational dual circulation flow certificate and $\Xi$ tie-break precondition equality. |

---

## Claim hygiene

1. **What these contracts support:** each names one anomaly it excludes and one
   invariant it preserves, under its own declared assumptions.
2. **What they do not support:** any WDP ledger row, any authorization, or any
   theorem beyond the contract's own scope. Draft status and
   `qualifies_as_true_normal_form: false` mean none of them is yet a normal
   form in the relational sense.
3. **Narrowest defensible claim:** nine of the twelve contracts carry an
   executable check of their excluded anomaly; the WDP pages use them only as
   cross-references.
4. **Next test needed:** a byte-identity check that keeps these copies in sync
   with `omega_engine_education/documentation/014_normal_forms/contracts_normal_forms/`. This is a
   suggested next step, not a ledger row.
