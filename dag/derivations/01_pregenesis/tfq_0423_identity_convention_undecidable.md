# [TFQ-0423] identity-convention-undecidable

> **Stage**: `PREGENESIS` | **Status**: `SOURCE_RECORD`  
> **UUID**: `6d6e7a7c-9122-57a2-8c43-6382aca0dc9f`  
> **Parent Derivation**: [TFQ-0422](tfq_0422_presentation_not_expressive_lift.md)

---

## 1. Abstract & Formal Statement

Whether <a> supplied after <> is a new state depends on an identity convention that no prompt had declared. Under the opaque convention a state is what the regime can tell apart, and with O empty <> and <a> are not told apart; under the exact-inscription convention a state is the inscription itself, the strings differ, and the regime has one more syntactic state. Trials 1 and 2 answered under the first convention and the full replay under the second, calling <a> a new state. The analysis keeps both branches and records the effect as undecidable until one convention is declared.

### Governing Obligation
Require a declared identity convention before answering whether a supplied inscription is a new state, and report the opaque and exact-inscription answers as separate branches until one is declared.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `A declared identity convention, opaque or exact-inscription, chosen by the host (assumption)`

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Records that the answer is relative to the convention; it does not choose one, and the three replies are behaviour of one unrecorded model, not evidence for either convention. Narrowed in lean4/CampaignPgwIdentityConventionUndecidable.lean and checks/independent/pgw-identity-convention-undecidable.py: models observation-family regimes PreGenesisRegime alpha beta with supplyInscription preserving obs (O_1 = O_0) and enlarging presented.card by +1, links obsProfile equality to PreMssn.Observation.SameProfile and genesisUnaryProfile equality to GenesisComputation.Collapsed, checks the Prompt 12 branch split (false with delta = 0 under opaqueConv vs true with delta = +1 under exactInscription, and undecidableWithoutConvention false true when no convention is declared), establishes agreement on profile-injective regimes, and keeps the host-declared identity convention as an explicit import (status remains CONDITIONAL).

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- [`lean4/CampaignPgwIdentityConventionUndecidable.lean::CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.conventions_agree_iff_fresh_profile`](../../../lean4/CampaignPgwIdentityConventionUndecidable.lean)
- [`lean4/CampaignPgwIdentityConventionUndecidable.lean::CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.genesisUnaryProfile_eq_iff_collapsed`](../../../lean4/CampaignPgwIdentityConventionUndecidable.lean)
- [`lean4/CampaignPgwIdentityConventionUndecidable.lean::CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.injective_obsProfile_implies_conventions_coincide`](../../../lean4/CampaignPgwIdentityConventionUndecidable.lean)
- [`lean4/CampaignPgwIdentityConventionUndecidable.lean::CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.no_convention_free_evaluator_fence`](../../../lean4/CampaignPgwIdentityConventionUndecidable.lean)
- [`lean4/CampaignPgwIdentityConventionUndecidable.lean::CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.obsProfile_eq_iff_sameProfile_and_empty_obs_collapse`](../../../lean4/CampaignPgwIdentityConventionUndecidable.lean)
- [`lean4/CampaignPgwIdentityConventionUndecidable.lean::CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.opaque_stateCount_le_exact_stateCount`](../../../lean4/CampaignPgwIdentityConventionUndecidable.lean)
- [`lean4/CampaignPgwIdentityConventionUndecidable.lean::CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.stateCount_supply_markA_delta_zero_vs_one`](../../../lean4/CampaignPgwIdentityConventionUndecidable.lean)
- [`lean4/CampaignPgwIdentityConventionUndecidable.lean::CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.supplyInscription_preserves_obs_and_enlarges_presentation`](../../../lean4/CampaignPgwIdentityConventionUndecidable.lean)
- [`lean4/CampaignPgwIdentityConventionUndecidable.lean::CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.supply_markA_after_ground_branch_divergence`](../../../lean4/CampaignPgwIdentityConventionUndecidable.lean)
- [`lean4/CampaignPgwIdentityConventionUndecidable.lean::CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.trial_votes_do_not_determine_convention_fence`](../../../lean4/CampaignPgwIdentityConventionUndecidable.lean)
- [`lean4/CampaignPgwIdentityConventionUndecidable.lean::CampaignPgwIdentityConventionUndecidable.CampaignPgwIdentityConventionUndecidable.unformed_vs_firstSeparation_regime_convention_bridge`](../../../lean4/CampaignPgwIdentityConventionUndecidable.lean)

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust switch between identity conventions`

### Python Oracles & Numerical Evaluators
- [`checks/independent/pgw-identity-convention-undecidable.py::main`](../../../checks/independent/pgw-identity-convention-undecidable.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0424](tfq_0424_absence_of_rule_not_identification.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `omega_engine_education/documentation/000_oepregen/sources/analysis_derivation_v1.md:731-737`
  - `omega_engine_education/documentation/000_oepregen/03_results_and_arguments.md:36-43`
  - `omega_engine_education/documentation/000_oepregen/02_trial_record.md:43-53`
  - `dag/derivations/independent/pgw-identity-convention-undecidable.md:1-35`
  - `dag/research/campaign_pgw-identity-convention-undecidable_lean_replay.json:1-20`
  - `dag/research/campaign_pgw-identity-convention-undecidable_lean_mutation.json:1-20`
  - `dag/research/campaign_pgw-identity-convention-undecidable_independent.json:1-20`
