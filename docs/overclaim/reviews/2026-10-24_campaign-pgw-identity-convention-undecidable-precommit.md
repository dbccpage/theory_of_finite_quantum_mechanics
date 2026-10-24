# Pre-Commit Claim Hygiene & Overclaim Review: `PGW-IDENTITY-CONVENTION-UNDECIDABLE` (`TFQ-0423`)

- **Date**: 2026-10-24
- **Branch**: `campaign/pgw-identity-convention-undecidable`
- **Target Node**: `PGW-IDENTITY-CONVENTION-UNDECIDABLE` (`TFQ-0423`)
- **Stage**: `PREGENESIS`
- **Status**: `CONDITIONAL` (`E0 -> E3`, `L4D`)
- **AuthorityEffect**: `None`

## 1. What It Supports
- `lean4/CampaignPgwIdentityConventionUndecidable.lean` (11 exported theorems, 0 `sorry`, standard axioms only, 6/6 semantic mutations killed) formalizes:
  -Observation-family regimes `PreGenesisRegime α β` with `supplyInscription` preserving `obs` ($O_1 = O_0$) and increasing `presented.card` by $+1$ on fresh inscriptions (`supplyInscription_preserves_obs_and_enlarges_presentation`).
  - Equivalence between `obsProfile` equality and `PreMssn.Observation.SameProfile` (`obsProfile_eq_iff_sameProfile_and_empty_obs_collapse`), and between `genesisUnaryProfile` equality and `GenesisComputation.Collapsed` (`genesisUnaryProfile_eq_iff_collapsed`).
  - Explicit convention branching under `GenesisComputation.IdentityConvention` (`.opaqueConv` vs `.exactInscription`) and `queryNewState none` on the Prompt 12 fixture (`supply_markA_after_ground_branch_divergence`, `stateCount_supply_markA_delta_zero_vs_one`), general cardinality bound (`opaque_stateCount_le_exact_stateCount`), and exact agreement on profile-injective regimes (`conventions_agree_iff_fresh_profile`, `injective_obsProfile_implies_conventions_coincide`).
  - Scope fences ruling out convention-free boolean evaluators (`no_convention_free_evaluator_fence`) and recording the split across the three Prompt 12 trial replies (`trial_votes_do_not_determine_convention_fence`).
- `checks/independent/pgw-identity-convention-undecidable.py` independently checks observation-family regimes across $n \in \{1, 2, 3\}$ and Genesis unary-form regimes across $n \in \{1, 2, 3, 4\}$ with zero failures.

## 2. What It Does Not Support
- Does not derive or select either identity convention from the prompt text or from the recorded model replies; the node remains `CONDITIONAL` on the host-declared identity convention.

## 3. Narrowest Defensible Claim
- Within the finite observation-family and Genesis unary-form regime models, whether supplying `<a>` after `<>` introduces a new state branches on `IdentityConvention` (`false` with $\Delta = 0$ under `.opaqueConv` vs `true` with $\Delta = +1$ under `.exactInscription` when $O = \emptyset$), and both conventions agree whenever the observation profile is injective.

## 4. Next Test Needed
- Extend the three-valued convention verdict to `TFQ-0424` (`PGW-ABSENCE-OF-RULE-NOT-IDENTIFICATION`) to separateFormalization A (no relation declared -> `UNDECIDABLE`) from Formalization B (vacuous $\approx_n$ when $O_n = \emptyset$).
