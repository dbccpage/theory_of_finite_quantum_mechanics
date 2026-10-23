# [TFQ-0555] wdp-bridge-ongoing-to-window

> **Stage**: `WDP` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `9bbf4493-1bac-5676-886a-9bd927e505f8`  
> **Parent Derivation**: [TFQ-0554](tfq_0554_wdp_genesis_bridges_ledger.md)

---

## 1. Abstract & Formal Statement

GEN-WDP-07, a conditional theorem in the bridge register, fixes a carrier and marked triples F, keeps the full directed integer table e(x, y) = M_r(x, y) − M_s(x, y) including loops and independent reverse arcs, treats raising as e ↦ e + d₀g with (d₀g)(x, y) = g(x) − g(y), and uses the marked diagnostic D_F(e)(x, y, z) = e(x, y) + e(y, z) + e(z, x). Cancellation gives D_F d₀ = 0, so D_F(e + d₀g) = D_F e even for unbalanced triples, and rationalizing reflects integer repair equality. This is a repair quotient with descending reports, not automatically cohomology: C¹/im d₀ differs from ker D_F/im d₀, a filled mark may be unbalanced, triangle reports miss loops and two-way defects, and antisymmetric simplicial coordinates need e(x, x) = 0 and e(x, y) + e(y, x) = 0. Term addition and identification can fail to respect the quotient (source 23:D4), so carrier-changing operations need new congruence proofs.

### Governing Obligation
Treat the Genesis Ongoing cancellation, raising and marked-fill data (TFQ-0485) as a fixed-carrier repair quotient only; feeding them into the declared degree-1 window is owed and needs the zero-loop and antisymmetry hypotheses, a d₁ with d₁d₀ = 0, and congruence proofs for term addition and identification.

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
> Proposed, not derived: the bridge does not produce the window of TFQ-0004 from Genesis admission (TFQ-0344), integer change costs are not identified with a continuous norm, and dynamic carrier changes belong to GEN-WDP-O02 and O03.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/Imported/WitnessedDifference/WitnessedDifference/RootGaugeNormalization.lean::normal_preserves_round_sums`](../../../lean4/Imported/WitnessedDifference/WitnessedDifference/RootGaugeNormalization.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine/crates_rs/omega_wdp/src/genesis_ongoing_adapter.rs::GenesisOngoingAdapter`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine/crates_rs/omega_wdp/src/genesis_ongoing_adapter.rs)

### Python Oracles & Numerical Evaluators
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
