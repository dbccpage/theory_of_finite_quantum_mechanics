# [TFQ-0555] wdp-bridge-ongoing-to-window

> **Stage**: `WDP` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `9bbf4493-1bac-5676-886a-9bd927e505f8`  
> **Parent Derivation**: [TFQ-0554](tfq_0554_wdp_genesis_bridges_ledger.md)

---

## 1. Abstract & Formal Statement

Narrowed in Lean 4 to the carrier {0, 1}. The directed slots are e(0,0), e(1,1), e(0,1) and e(1,0). The coboundary of vertex values (g0, g1) is (0, 0, g0 - g1, g1 - g0). The unbalanced mark (0, 1, 0) has diagnostic e(0,1) + e(1,0) + e(0,0). That diagnostic is 0 on every coboundary and is unchanged when a coboundary is added. If a nonzero integer b scales an integer slot difference onto a coboundary, the difference is already the integer coboundary of (0, -d01). The table (1, 0, 0, -1) has diagnostic 0 and is not a coboundary. The table (0, 1, 0, 0) has diagnostic 0 and is not a coboundary. The one-arc table (0, 0, 1, 0) has diagnostic 1. The two-way table (0, 0, 1, 1) has arc sum 2 and arc difference 0. A general carrier, an arbitrary marked family, the degree-1 window of TFQ-0004, a continuous norm, and carrier-changing term operations stay open.

### Governing Obligation
Treat the Genesis Ongoing cancellation, raising and marked-fill data (TFQ-0483, TFQ-0484 and TFQ-0485) as a fixed-carrier repair quotient only; feeding them into the declared degree-1 window is owed and needs the zero-loop and antisymmetry hypotheses, a d₁ with d₁d₀ = 0, and congruence proofs for term addition and identification. A general carrier, an arbitrary marked family, the degree-1 window of TFQ-0004, a continuous norm, and carrier-changing term operations stay open.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Fixed carrier and declared marked triples F from the chosen Genesis Ongoing source contexts (assumption)`

### Further Prerequisites
- [TFQ-0485](../02_genesis/tfq_0485_go_h3_twin_fills_holonomy.md) go-h3-twin-fills-holonomy

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Open. One two-vertex carrier is checked. The coboundary cancellation, the denominator reflection, the two kernel witnesses, the one-arc diagnostic, and the two-way sum are checked. A general carrier, an arbitrary marked family, the window of TFQ-0004, a continuous norm, and carrier-changing term operations stay open.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/CampaignPgwWdpBridgeOngoing.lean::cob_slots`](../../../lean4/CampaignPgwWdpBridgeOngoing.lean)
- [`lean4/CampaignPgwWdpBridgeOngoing.lean::compensated_loop_closed`](../../../lean4/CampaignPgwWdpBridgeOngoing.lean)
- [`lean4/CampaignPgwWdpBridgeOngoing.lean::compensated_loop_not_coboundary`](../../../lean4/CampaignPgwWdpBridgeOngoing.lean)
- [`lean4/CampaignPgwWdpBridgeOngoing.lean::denominator_clears`](../../../lean4/CampaignPgwWdpBridgeOngoing.lean)
- [`lean4/CampaignPgwWdpBridgeOngoing.lean::diag_after_repair`](../../../lean4/CampaignPgwWdpBridgeOngoing.lean)
- [`lean4/CampaignPgwWdpBridgeOngoing.lean::diag_on_coboundary`](../../../lean4/CampaignPgwWdpBridgeOngoing.lean)
- [`lean4/CampaignPgwWdpBridgeOngoing.lean::one_arc_diagnostic`](../../../lean4/CampaignPgwWdpBridgeOngoing.lean)
- [`lean4/CampaignPgwWdpBridgeOngoing.lean::silent_loop_closed`](../../../lean4/CampaignPgwWdpBridgeOngoing.lean)
- [`lean4/CampaignPgwWdpBridgeOngoing.lean::silent_loop_not_coboundary`](../../../lean4/CampaignPgwWdpBridgeOngoing.lean)
- [`lean4/CampaignPgwWdpBridgeOngoing.lean::two_way_difference`](../../../lean4/CampaignPgwWdpBridgeOngoing.lean)
- [`lean4/CampaignPgwWdpBridgeOngoing.lean::two_way_sum`](../../../lean4/CampaignPgwWdpBridgeOngoing.lean)
- [`lean4/Imported/WitnessedDifference/WitnessedDifference/RootGaugeNormalization.lean::normal_preserves_round_sums`](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/RootGaugeNormalization.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_wdp/src/genesis_ongoing_adapter.rs::GenesisOngoingAdapter`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine/crates_rs/omega_wdp/src/genesis_ongoing_adapter.rs)

### Python Oracles & Numerical Evaluators
- [`checks/independent/pgw-wdp-bridge-ongoing-to-window.py::main`](../../../checks/independent/pgw-wdp-bridge-ongoing-to-window.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_to_wdp_derivation_programme.md:147-170`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_ongoing_fixed_carrier_bridge.md:26-36`
  - `omega_engine_education/documentation/006_oewdp/levels/level_22_genesis_to_wdp_bridges.md:116-137`
  - `dag/derivations/independent/pgw-wdp-bridge-ongoing-to-window.md:5`
  - `dag/research/campaign_pgw-wdp-bridge-ongoing-to-window_lean_replay.json:6`
