# [TFQ-0504] endogenous-demand-ob1

> **Stage**: `GENESIS` | **Status**: `OPEN_OBLIGATION`  
> **UUID**: `c259276b-e842-5fd2-b75a-6fa1c6e51b45`  
> **Parent Derivation**: [TFQ-0486](tfq_0486_genesis_freeze_endpoint_ledger.md)

---

## 1. Abstract & Formal Statement

No endogenous demand generator exists in the Alpha harness (AE-DEMAND-OPEN, OB-1, successor research S2): a demand is a target pair (i, j) with 0 ≤ i < j < n_data supplied by the host together with the measure and the declared bounds, nothing in the harness chooses a next demand, and the collapsed pairs left after an admission are returned as observations, not demands (leftover_as_demand refuses). The sealed derivation's pair-separation closure policy is declared metatheory, not a harness function, and the sealed result is that no object-language endogenous demand generator was derived.

### Governing Obligation
Derive an object-language rule that generates the next unresolved requirement from admitted structure without reading token glyphs, supplying a fresh datum, importing a new goal or assuming the continuation, or keep every demand host-supplied and recorded.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Further Prerequisites
- [TFQ-0487](tfq_0487_endogenous_demands_exogenous_payments.md) endogenous-demands-exogenous-payments

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> A declared policy and object-language SEEK extension now computes fresh targets from source contexts and records source impose events. This is a narrowed extension, not a derivation of the policy from frozen observations or a refinement of Alpha search/licensing. Requests do not satisfy demands; unbounded continuation remains open.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/CampaignGenesisDemandPolicy.lean::CampaignGenesisDemandPolicy.collapseTest_correct`](../../../lean4/CampaignGenesisDemandPolicy.lean)
- [`lean4/CampaignGenesisDemandPolicy.lean::CampaignGenesisDemandPolicy.fixed_data_saturates`](../../../lean4/CampaignGenesisDemandPolicy.lean)
- [`lean4/CampaignGenesisDemandPolicy.lean::CampaignGenesisDemandPolicy.instruction_records_demand`](../../../lean4/CampaignGenesisDemandPolicy.lean)
- [`lean4/CampaignGenesisDemandPolicy.lean::CampaignGenesisDemandPolicy.mem_agenda`](../../../lean4/CampaignGenesisDemandPolicy.lean)
- [`lean4/CampaignGenesisDemandPolicy.lean::CampaignGenesisDemandPolicy.mem_contexts`](../../../lean4/CampaignGenesisDemandPolicy.lean)
- [`lean4/CampaignGenesisDemandPolicy.lean::CampaignGenesisDemandPolicy.next_none_iff`](../../../lean4/CampaignGenesisDemandPolicy.lean)
- [`lean4/CampaignGenesisDemandPolicy.lean::CampaignGenesisDemandPolicy.next_sound`](../../../lean4/CampaignGenesisDemandPolicy.lean)
- [`lean4/CampaignGenesisDemandPolicy.lean::CampaignGenesisDemandPolicy.no_host_target_in_program`](../../../lean4/CampaignGenesisDemandPolicy.lean)
- [`lean4/CampaignGenesisDemandPolicy.lean::CampaignGenesisDemandPolicy.policy_is_not_forced`](../../../lean4/CampaignGenesisDemandPolicy.lean)
- [`lean4/CampaignGenesisDemandPolicy.lean::CampaignGenesisDemandPolicy.seek_is_recorded_source_step`](../../../lean4/CampaignGenesisDemandPolicy.lean)
- `missing obligation: no Lean demand generator for the harness; Generator.generation_never_dries concerns the reflective composite (TFQ-0487)`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/code/rust/src/outside.rs::Outside` (private upstream source, not in this repository)

### Python Oracles & Numerical Evaluators
- [`checks/independent/pgw-endogenous-demand-ob1.py`](../../../checks/independent/pgw-endogenous-demand-ob1.py)
- [`github:dbccpage/19L57G1@85a83ae7c/research/alpha_engine/harness.py::leftover_as_demand`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/alpha_engine/harness.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

*None (Leaf or Terminal derivation in current tree)*

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/genesis_source.txt:531-537`
  - `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_genesis_19l57g1/docs/sources/closeout.txt:70-71`
  - `github:dbccpage/19L57G1@85a83ae7c/docs/ALPHA_HANDOFF.md:78-88`
  - `dag/derivations/independent/pgw-endogenous-demand-ob1.md:1`
