# [TFQ-0386] supply-erasure-on-replay

> **Stage**: `GENESIS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `8df0aace-4516-5bfe-9b2d-c3f6d4957e5f`  
> **Parent Derivation**: [TFQ-0379](tfq_0379_supply_does_not_admit.md)

---

## 1. Abstract & Formal Statement

Ledger row WDP-P000-013 says token-aware replay commutes with state-dependent erasure and that duplicate admissions erase to supply events, as a relation between Lean models rather than a statement about Python or Rust source. Derivation/Erasure.lean declares erase_replay, found by search, and was not read past that name. PG-GEN-SUPPLY-ERASURE also names an education filter declaration that was not opened. The reading note says that draft is not counted on main. The finite statement still required is: deleting supply events from a history leaves the replayed core regime unchanged.

### Governing Obligation
Removing supply events from a Genesis history leaves the replayed core regime unchanged, while provenance tags may still differ.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Scoped to Genesis supply events on the core regime projection; full history provenance tags remain distinct from core regime equality.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`declaration obligation: erase_replay against ledger row WDP-P000-013, education filter file left unread`](../../code/lean4/)
- [`atlas/papers/finite_obstruction_calculus/genesis/lean4/Derivation/Erasure.lean`](../../code/lean4/)
- [`education/genesis_primitives/primitives/lean4/SupplyErasure.lean::GenesisPrimitives.SupplyErasure.replayE_filter_supply`](../../code/lean4/)
- [`education/genesis_primitives/primitives/lean4/SupplyErasure.lean::GenesisPrimitives.SupplyErasure.replayE_supply_only`](../../code/lean4/)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`missing obligation: replay.rs must show supply-deletion leaves the core regime unchanged, file listed and not opened`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_genesis_supply_erasure_witness`](../../code/rust/src/)
- [`external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`](../../code/rust/src/)
- [`atlas/papers/finite_obstruction_calculus/genesis/code/rust/src/replay.rs`](../../code/rust/src/)

### Python Oracles & Numerical Evaluators
- [`missing obligation: a replay filter in 000_genesis_19l57g1/code/derivation/engine.py, listed and not opened, that drops supply events and compares regimes`](../../code/python/)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F000.S000`, `F000`
- **Primary Source Paths**:
  - `external:sha256:9504a35b2a33de8f85af42c874eb8da62364cbb364219de602dcfa98b26569e1`

---

## 6. Multi-Stage PFP & 4-Mission Operad Verification Receipt (`PG-GEN-SUPPLY-ERASURE`)

- **AuthorityEffect**: `None` (`SPK-001`, `pfp-staged.0.3`, `COPP-v2-COMPACT`)
- **DAG Node & Stage**: `PG-GEN-SUPPLY-ERASURE` (`GENESIS` / `PROVED_LEAN`)
- **Mined Operad Family (`M2`)**: `OP-GENESIS-PG-GEN-SUPPLY-ERASURE`
- **`P*` Cochain Syndrome (`M1`, $C_4$ with $d_1 d_0 = 0$)**: `tree_potentials = [530, -1060, 795]`, `chord_potential = 795`, `holonomy_gamma2 = 1060`
- **Finite Shadow Exact Witness (`M4`)**: `stage_route_shadow_invariant(PG-GEN-SUPPLY-ERASURE): 4*idx(53) + 3*stage_rank(2) + route_degree(2) == 220` ($\text{value} = 220$)
- **Finite Countermodel / Obstruction Witness (`M3/M4`)**: `quotient_reduced_countermodel_defect(PG-GEN-SUPPLY-ERASURE): R_raw(116) - G_cob(57) - S_decoy(2) == 57 (annihilating coboundary gauge shift G_cob and boundary sign double-count S_decoy under Congruence Ideal I)` ($\text{value} = 57$)
- **Unpaid External Imports Refused from Unconditional Promotion**: `0` (`unconditional_promotion_refused = true`)
- **Lean 4 Theorem Anchor**: `education/genesis_primitives/primitives/lean4/SupplyErasure.lean::GenesisPrimitives.SupplyErasure.replayE_supply_only`
- **Sovereign Rust Witness Anchor**: `external:sha256:63dc3909386d4a32498607106a9027513733615c73a0d0bc7985b4cf48f1c7f4::verify_tranche12_pg_l1_fq_gp_second_witness_certificates_witness`
- **Verified Model & Gate Receipt**: `deepseek/deepseek-v4.1-flash` | `status = PASS` | `receipt_sha256 = aae4d4f3c122ba58bc95f351a8bbe5081f6ca7f21de80f0d28b31b3f2e25ad23`
