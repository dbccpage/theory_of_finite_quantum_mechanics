# [TFQ-0499] python-lean-carrier-bridge

> **Stage**: `GENESIS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `0306c224-964b-5b0d-ab75-f3f37014c49d`  
> **Parent Derivation**: [TFQ-0486](tfq_0486_genesis_freeze_endpoint_ledger.md)

---

## 1. Abstract & Formal Statement

Narrowed boundary, status left OPEN. The sealed reading-L history has length 7 and replays from genesis to regime R2L. The sealed reading-F history has length 8 and replays from genesis to regime R2F. R2L has data count 2 and requirement list (0, 1). R2F has data count 3 and requirement list (1, 2). Both regimes have empty form, instance, and rule lists. R2L is not R2F, and the two replay results are not equal.

### Governing Obligation
Keep these two replay results separate from a refinement. A refinement from each cited Python computation to its Lean statement stays open.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> These two replays are sealed Lean histories. They are not a refinement from a Python computation to a Lean statement. Token erasure, the license binding, rung-two track one, and the Python histories that stop before the requirement stay open. Status stays OPEN.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/CampaignPgwPythonLeanCarrierBridge.lean::pgwData_counts`](../../../lean4/CampaignPgwPythonLeanCarrierBridge.lean)
- [`lean4/CampaignPgwPythonLeanCarrierBridge.lean::pgwEmpty_carriers`](../../../lean4/CampaignPgwPythonLeanCarrierBridge.lean)
- [`lean4/CampaignPgwPythonLeanCarrierBridge.lean::pgwHistoryF_replays`](../../../lean4/CampaignPgwPythonLeanCarrierBridge.lean)
- [`lean4/CampaignPgwPythonLeanCarrierBridge.lean::pgwHistoryL_replays`](../../../lean4/CampaignPgwPythonLeanCarrierBridge.lean)
- [`lean4/CampaignPgwPythonLeanCarrierBridge.lean::pgwHistory_lengths`](../../../lean4/CampaignPgwPythonLeanCarrierBridge.lean)
- [`lean4/CampaignPgwPythonLeanCarrierBridge.lean::pgwR2L_ne_R2F`](../../../lean4/CampaignPgwPythonLeanCarrierBridge.lean)
- [`lean4/CampaignPgwPythonLeanCarrierBridge.lean::pgwReplay_ne`](../../../lean4/CampaignPgwPythonLeanCarrierBridge.lean)
- [`lean4/CampaignPgwPythonLeanCarrierBridge.lean::pgwReqs`](../../../lean4/CampaignPgwPythonLeanCarrierBridge.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/replay.rs::replay`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/replay.rs)

### Python Oracles & Numerical Evaluators
- [`checks/independent/pgw-python-lean-carrier-bridge.py::main`](../../../checks/independent/pgw-python-lean-carrier-bridge.py)
- [`omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/model.py::replay`](https://github.com/dbccpage/the_symbol_game/blob/7351ed452e518cb8cf2bf973d4c4881289084bce/omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/derivation/model.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt:37-43`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt:380`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt:1077-1080`
  - `dag/derivations/independent/pgw-python-lean-carrier-bridge.md:5`
  - `dag/research/campaign_pgw-python-lean-carrier-bridge_lean_replay.json:6`
