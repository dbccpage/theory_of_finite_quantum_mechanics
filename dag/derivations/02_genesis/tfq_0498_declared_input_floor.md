# [TFQ-0498] declared-input-floor

> **Stage**: `GENESIS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `55d68a4f-522d-5581-9299-3ee49eebef8f`  
> **Parent Derivation**: [TFQ-0486](tfq_0486_genesis_freeze_endpoint_ledger.md)

---

## 1. Abstract & Formal Statement

Narrowed boundary, status left OPEN. The declared bound record is rounds 15, node guard 250, data ceiling 4, item bound 2, input count 2, engine count 4, and reading count 2. The input count equals the item bound. One is strictly below the input count. The guard is strictly above the round count. The engine count is not the reading count. The data counts strictly below 4, taken from the candidates 0, 1, 2, 3, and 4, are 0, 1, 2, and 3. There are 4 such counts. The ceiling itself is not strictly below 4.

### Governing Obligation
Keep this bound record separate from a floor. A floor for the declared-input count, or a reduction below two that holds past the bounds of attempt two, stays open.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> The seven numerals are a declared bound record. They are not a floor for the input count. They do not show that four engines carry the grammar forward, and they do not decide the other reading of the completion gate. Whether the four carry forward past the bounds stays open (H-1, SD-R-11). A reduction below two that holds past the bounds of attempt two stays open. The completion-gate clause was frozen as NOT_ESTABLISHED. Status stays OPEN.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/CampaignPgwDeclaredInputFloor.lean::pgwBounds_values`](../../../lean4/CampaignPgwDeclaredInputFloor.lean)
- [`lean4/CampaignPgwDeclaredInputFloor.lean::pgwCeiling_not_below`](../../../lean4/CampaignPgwDeclaredInputFloor.lean)
- [`lean4/CampaignPgwDeclaredInputFloor.lean::pgwEngines_ne_readings`](../../../lean4/CampaignPgwDeclaredInputFloor.lean)
- [`lean4/CampaignPgwDeclaredInputFloor.lean::pgwGuard_above_rounds`](../../../lean4/CampaignPgwDeclaredInputFloor.lean)
- [`lean4/CampaignPgwDeclaredInputFloor.lean::pgwInput_eq_items`](../../../lean4/CampaignPgwDeclaredInputFloor.lean)
- [`lean4/CampaignPgwDeclaredInputFloor.lean::pgwOne_below_input`](../../../lean4/CampaignPgwDeclaredInputFloor.lean)
- [`lean4/CampaignPgwDeclaredInputFloor.lean::pgwStrictlyBelow_length`](../../../lean4/CampaignPgwDeclaredInputFloor.lean)
- [`lean4/CampaignPgwDeclaredInputFloor.lean::pgwStrictlyBelow_list`](../../../lean4/CampaignPgwDeclaredInputFloor.lean)
- `missing obligation: no Lean statement of a declared-input floor`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust check of the input count`

### Python Oracles & Numerical Evaluators
- [`checks/independent/pgw-declared-input-floor.py::main`](../../../checks/independent/pgw-declared-input-floor.py)
- [`github:dbccpage/19L57G1@85a83ae7c/research/second_run/fwd_runs.py::carries_forward`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/second_run/fwd_runs.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt:386`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/continuation.txt:1064-1066`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt:333-336`
  - `dag/derivations/independent/pgw-declared-input-floor.md:5`
  - `dag/research/campaign_pgw-declared-input-floor_lean_replay.json:6`
