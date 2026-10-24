# [TFQ-0555] wdp-bridge-ongoing-to-window

> **Stage**: `WDP` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `9bbf4493-1bac-5676-886a-9bd927e505f8`  
> **Parent Derivation**: [TFQ-0554](tfq_0554_wdp_genesis_bridges_ledger.md)

---

## 1. Abstract & Formal Statement

For three positions labeled 0, 1, and 2, every integer triple (g0, g1, g2) has coboundary round sum (g0 - g1) + (g1 - g2) + (g2 - g0) = 0, and adding those differences leaves e01 + e12 + e20 unchanged, including the unbalanced mark 1 + 1 + 1 = 3, which stays 3 after the differences from (2, 5, 11). For every integer g the diagonal g - g is 0, so the loop value 4 is not a diagonal coboundary, while the oriented arcs 0, 0, 0 have diagnostic 0. The forward arc 3 with the other oriented arcs 0 has diagnostic 3, and the two-way values 3 and 5 sum to 8.

### Governing Obligation
The finite check on positions 0, 1, 2 records round-sum cancellation, invariance of e01 + e12 + e20, the unbalanced mark 3 after the shift from (2, 5, 11), the loop 4 with diagnostic 0, and the two-way sum 8. A repair quotient for a general marked family, and a transport into the degree-1 window, stay open.

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
> The cancellation is the three-term integer identity on one ordered triple of positions. It does not identify the repair quotient with cohomology, and it does not produce the window of TFQ-0004 from Genesis admission (TFQ-0344). Rational repair equality, term addition, identification, a continuous norm, and carrier changes GEN-WDP-O02 and O03 stay open. normal_preserves_round_sums is gauge normalization of a whole table. The loop 4 and the pair 3, 5 are witnesses on this triple.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/CampaignPgwWdpBridgeOngoingToWindow.lean::pgwBr_gradient_round`](../../../lean4/CampaignPgwWdpBridgeOngoingToWindow.lean)
- [`lean4/CampaignPgwWdpBridgeOngoingToWindow.lean::pgwBr_loop_not_coboundary`](../../../lean4/CampaignPgwWdpBridgeOngoingToWindow.lean)
- [`lean4/CampaignPgwWdpBridgeOngoingToWindow.lean::pgwBr_loop_report`](../../../lean4/CampaignPgwWdpBridgeOngoingToWindow.lean)
- [`lean4/CampaignPgwWdpBridgeOngoingToWindow.lean::pgwBr_shift_preserves`](../../../lean4/CampaignPgwWdpBridgeOngoingToWindow.lean)
- [`lean4/CampaignPgwWdpBridgeOngoingToWindow.lean::pgwBr_two_way`](../../../lean4/CampaignPgwWdpBridgeOngoingToWindow.lean)
- [`lean4/CampaignPgwWdpBridgeOngoingToWindow.lean::pgwBr_unbalanced`](../../../lean4/CampaignPgwWdpBridgeOngoingToWindow.lean)
- [`lean4/Imported/WitnessedDifference/WitnessedDifference/RootGaugeNormalization.lean::normal_preserves_round_sums`](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/RootGaugeNormalization.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_wdp/src/genesis_ongoing_adapter.rs::GenesisOngoingAdapter`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine/crates_rs/omega_wdp/src/genesis_ongoing_adapter.rs)

### Python Oracles & Numerical Evaluators
- [`checks/independent/pgw-wdp-bridge-ongoing-to-window.py::main`](../../../checks/independent/pgw-wdp-bridge-ongoing-to-window.py)
- `missing obligation: GEN-WDP-07 carries a written proof and the native omega_wdp adapter; no Python binding`

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_to_wdp_derivation_programme.md:147-170`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/genesis_ongoing_fixed_carrier_bridge.md:26-36`
  - `omega_engine_education/documentation/006_oewdp/levels/level_22_genesis_to_wdp_bridges.md:116-137`
  - `lean4/CampaignPgwWdpBridgeOngoingToWindow.lean:9-10`
  - `dag/derivations/independent/pgw-wdp-bridge-ongoing-to-window.md:1`
  - `dag/research/campaign_pgw-wdp-bridge-ongoing-to-window_lean_replay.json:2-4`
