# [TFQ-0039] Cite F002.S001 as an open bridge and do not convert the finite

> **Stage**: `FINITE_QCD` | **Status**: `GAP`  
> **UUID**: `fd1411cd-6429-55ee-af4f-a2d34df10758`  
> **Parent Derivation**: [TFQ-0031](tfq_0031_leave_confinement_beyond_the_strong_coupling_formulae_as_a_gap_with_f002_s001_an.md)

---

## 1. Abstract & Formal Statement

The F002 floor states its own ceiling. The S000 book README calls the continuum volume an interface inventory and not a continuum derivation. F002.S001 remains the open bridge: shelf.yaml has an empty book list, README.md keeps GAP-F002-S001-001 open, and named_adjoining.yaml parks a Pontryagin dual of declared free Z without admitting a bridge theorem. None of the finite QCD controls, the Dirac doubling counts, or the topological anyon models close that shelf. The gap to continuum QCD stays open. This node does not say that continuum QCD has been derived.

### Governing Obligation
Cite F002.S001 as an open bridge and do not convert the finite controls into a continuum exit.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems (`lean4/CampaignTfq0039FiniteQcd.lean`)
- `CampaignTfq0039FiniteQcd.finite_qcd_control_exact_rational_summary`: Proves `qcdBeta0Times16Pi2 3 6 = 7`, `strongCouplingTension 1 3 = 17/18`, `freeTorusDoublerCount 4 = 16`, and `wilsonLiftedDoublerCount 4 = 15`.
- `CampaignTfq0039FiniteQcd.finite_cyclic_dual_order_equals_lattice_period`: Proves `finiteCyclicCharacterCount L = L` and `(finiteCyclicCharacterCount L)^d = L^d`.
- `CampaignTfq0039FiniteQcd.f002_s001_empty_book_list_and_open_bridge_gap`: Proves `f002S001BridgeShelf.bookCount = 0`, `hasOpenBridgeGap001 = true`, and `admitsPontryaginDualBridgeTheorem = false`.
- `CampaignTfq0039FiniteQcd.pontryagin_dual_of_free_z_requires_unpaid_continuum_circle_fence`: Proves `finiteCyclicCharacterCount N < finiteCyclicCharacterCount (N + 1)` and `admitsPontryaginDualBridgeTheorem = false`.
- `CampaignTfq0039FiniteQcd.finite_qcd_controls_do_not_discharge_continuum_qcd_exit_fence`: Proves `continuumQcdDerived s = false` whenever `s.f002S001BridgeClosed = false`.
- `CampaignTfq0039FiniteQcd.one_loop_beta0_polynomial_not_nonperturbative_continuum_mass_gap_fence`: Proves `qcdBeta0Times16Pi2 3 N_f = 11 - (2/3) N_f` and sign reversal between `N_f = 6` and `N_f = 17`.
- `CampaignTfq0039FiniteQcd.strong_coupling_plaquette_ratio_breaks_down_in_weak_coupling_continuum_limit_fence`: Proves `strongCouplingTension 18 3 = 0` and `strongCouplingTension 20 3 = -1/9 < 0`.
- `CampaignTfq0039FiniteQcd.wilson_torus_doubler_count_not_continuum_chiral_fermion_measure_fence`: Proves `1 + 4 + 6 + 4 + 1 = 16` and `f002S001BridgeShelf.bookCount = 0`.
- `CampaignTfq0039FiniteQcd.topological_anyon_catalog_not_continuum_su3_confining_vacuum_fence`: Proves `k + 1 ≤ 7` and `f002S001BridgeShelf.bookCount = 0` for `k = 1..6`.
- `CampaignTfq0039FiniteQcd.tfq0039_f002_s001_open_bridge_scope_ledger_fence`: Audits `Tfq0039ScopeLedger`.

### Sovereign Rust Certifiers (`code/rust/src/qm/qcd_beta0_wilson_confinement_control.rs`)
- `code/rust/src/qm/qcd_beta0_wilson_confinement_control.rs::verify_qcd_beta0_wilson_confinement_control`
- `code/rust/src/qm/qcd_beta0_wilson_confinement_control.rs::checks_qcd_beta0_and_wilson_doubling_resolution`

### Independent Python Verification (`checks/independent/tfq-0039.py`)
- Executes `1301` exact rational and combinatorial checks across finite QCD controls, strong-coupling breakdown regimes, Brillouin corner sums, finite cyclic character duality, and the `F002.S001` bridge truth table (`0` failures).

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0040](tfq_0040_close_the_missing_python_or_lean_twins_before_treating_a_control_as.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Atlas Lineage**: `F001.S000`, `F002.S001`
- **Primary Source Paths**:
  - `omega_engine_atlas/coda_atlas/F001_quantum/S000_finite_quantum_mechanics/shelf.yaml`
  - `omega_engine_atlas/coda_atlas/F002_continuum/S001_continuum_finite_shadow_bridge/shelf.yaml`
