# Independent review of PR #321

Scope: original head 1f8d6736e3be21354376e73d10ad47c9e50d3e69. Exact source lean4/CampaignPgwIdentityConventionUndecidable.lean, SHA-256 a3bb1c027c2e3421e71fa2dbb67bca6a1d60e9c33dfdcb181d07bfd157b4bc09.

AuthorityEffect: None. Result: BLOCKED. No status was raised.

## Statement versus theorem

Finite presentation sets and supplied observation lists define two explicit identity conventions. Supply preserves the observation list; profile equality matches SameProfile; profile-image cardinality is bounded by presentation cardinality; injective profiles make the conventions agree; unary-profile equality matches the imported Collapsed predicate. A closed fixture distinguishes the two conventions, so one Boolean evaluator cannot agree with both everywhere. This is model ambiguity, not a computability-theoretic undecidability theorem. The absent-convention query returns its tagged result even when its branch values agree. The trial-convention list is supplied data, not a checked transcription of trial files. The independent observation-family sweep uses carrier sizes 1 through 3, despite its introductory mention of 4; size 4 belongs to the separate unary-regime sweep.

| Declaration | Checked statement boundary |
|---|---|
| `lean4/CampaignPgwIdentityConventionUndecidable.lean:37 supplyInscription_preserves_obs_and_enlarges_presentation` | `{α β : Type*} [DecidableEq α] (R : PreGenesisRegime α β) (x : α) (hfresh : x ∉ R.presented) : (supplyInscription R x).obs = R.obs ∧ obsProfile (supplyInscription R x) = obsProfile R ∧ (supplyInscription R x).presented.card = R.presented.card + 1` |
| `lean4/CampaignPgwIdentityConventionUndecidable.lean:51 obsProfile_eq_iff_sameProfile_and_empty_obs_collapse` | `{α β : Type*} (R : PreGenesisRegime α β) (x y : α) : (obsProfile R x = obsProfile R y ↔ SameProfile (indexedObs R) x y) ∧ (R.obs = [] → obsProfile R x = [] ∧ SameProfile (indexedObs R) x y ∧ profileClass (indexedObs R) x = profileClass (indexedObs R) y)` |
| `lean4/CampaignPgwIdentityConventionUndecidable.lean:125 supply_markA_after_ground_branch_divergence` | `: PreGenesisToken.ground ≠ PreGenesisToken.markA ∧ isNewStateUnder .opaqueConv initialRegime .markA = false ∧ isNewStateUnder .exactInscription initialRegime .markA = true ∧ isNewStateUnder .opaqueConv initialRegime .markA ≠ isNewStateUnder .exactInscription initialRegime .markA ∧ queryNewState none initialRegime .markA = .undecidableWithoutConvention false true ∧ queryNewState (some .opaqueConv) initialRegime .markA = .decided false ∧ queryNewState (some .exactInscription) initialRegime .markA = .decided true` |
| `lean4/CampaignPgwIdentityConventionUndecidable.lean:137 stateCount_supply_markA_delta_zero_vs_one` | `: stateCountUnder .opaqueConv initialRegime = 1 ∧ stateCountUnder .exactInscription initialRegime = 1 ∧ stateCountUnder .opaqueConv afterSupplyRegime = 1 ∧ stateCountUnder .exactInscription afterSupplyRegime = 2 ∧ stateCountUnder .exactInscription afterSupplyRegime - stateCountUnder .opaqueConv afterSupplyRegime = 1` |
| `lean4/CampaignPgwIdentityConventionUndecidable.lean:147 opaque_stateCount_le_exact_stateCount` | `{α β : Type*} [DecidableEq α] [DecidableEq β] (R : PreGenesisRegime α β) : stateCountUnder .opaqueConv R ≤ stateCountUnder .exactInscription R` |
| `lean4/CampaignPgwIdentityConventionUndecidable.lean:153 conventions_agree_iff_fresh_profile` | `{α β : Type*} [DecidableEq α] [DecidableEq β] (R : PreGenesisRegime α β) (x : α) (hfresh : x ∉ R.presented) : (isNewStateUnder .opaqueConv R x = isNewStateUnder .exactInscription R x) ↔ obsProfile R x ∉ R.presented.image (obsProfile R)` |
| `lean4/CampaignPgwIdentityConventionUndecidable.lean:161 injective_obsProfile_implies_conventions_coincide` | `{α β : Type*} [DecidableEq α] [DecidableEq β] (R : PreGenesisRegime α β) (hinj : Function.Injective (obsProfile R)) (x : α) : isNewStateUnder .opaqueConv R x = isNewStateUnder .exactInscription R x ∧ stateCountUnder .opaqueConv R = stateCountUnder .exactInscription R` |
| `lean4/CampaignPgwIdentityConventionUndecidable.lean:184 genesisUnaryProfile_eq_iff_collapsed` | `(r : Regime) (i j : Nat) : genesisUnaryProfile r i = genesisUnaryProfile r j ↔ Collapsed r i j` |
| `lean4/CampaignPgwIdentityConventionUndecidable.lean:220 unformed_vs_firstSeparation_regime_convention_bridge` | `: genesisUnaryProfile ⟨2, [], [], [], []⟩ 0 = genesisUnaryProfile ⟨2, [], [], [], []⟩ 1 ∧ Collapsed ⟨2, [], [], [], []⟩ 0 1 ∧ genesisUnaryProfile firstSeparationRegime 0 = [true] ∧ genesisUnaryProfile firstSeparationRegime 1 = [false] ∧ genesisUnaryProfile firstSeparationRegime 0 ≠ genesisUnaryProfile firstSeparationRegime 1 ∧ ¬ Collapsed firstSeparationRegime 0 1` |
| `lean4/CampaignPgwIdentityConventionUndecidable.lean:230 no_convention_free_evaluator_fence` | `: ¬ ∃ eval : PreGenesisRegime PreGenesisToken Bool → PreGenesisToken → Bool, (∀ R x, eval R x = isNewStateUnder .opaqueConv R x) ∧ (∀ R x, eval R x = isNewStateUnder .exactInscription R x)` |
| `lean4/CampaignPgwIdentityConventionUndecidable.lean:246 trial_votes_do_not_determine_convention_fence` | `: prompt12TrialConventions 0 = .opaqueConv ∧ prompt12TrialConventions 1 = .opaqueConv ∧ prompt12TrialConventions 2 = .exactInscription ∧ isNewStateUnder (prompt12TrialConventions 0) initialRegime .markA = false ∧ isNewStateUnder (prompt12TrialConventions 2) initialRegime .markA = true` |

## Corrections and acceptance

Current capability: **L3**. The substantive L4 floor is not met. SCORING.md section 2 distinguishes elementary tables and bounded-domain developments from production architecture. A topic, proof count or passing compiler is not a level basis.

Missing companions and stale source bindings are repaired. Existing assessment history is retained; former L4 claims and unrelated supergravity gate text are superseded where present. No policy, baseline, support-exception, floor or scanner allowlist is changed.

Existing six-mutant summaries are historical reports. Their logs and complete candidate bytes were not supplied for independent fault attribution. They do not establish a new mutation score; current generated/killed counts are zero and the ratio is null.

## Verification and numbers

Fresh original-head checks and the repaired-source reruns are in `dag/research/pr_321_independent_review_validation.json`. Independent normal and optimized execution recompute the finite numbers; a passing enumeration does not prove an unbounded or physical interpretation. Compiler module-system warnings are retained. No A/B engineering score is claimed.

## Remaining work

A substantive, actually needed L4 mathematical/API development is required before acceptance. Artificial wrappers and a relabelled score would not resolve this. The current L1D build registration also needs a reviewed current-byte binding under its already-authorized support rule; no new exception is introduced here.

The required DAG/pipeline errors are reported as failures, including errors inherited from the base. This PR must remain a draft until all acceptance requirements pass.
