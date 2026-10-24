Status: AI-drafted, awaiting human review.
AuthorityEffect: None.

# Independent Derivation Note: `PGW-IDENTITY-CONVENTION-UNDECIDABLE` (`TFQ-0423`)

- **Node ID**: `PGW-IDENTITY-CONVENTION-UNDECIDABLE` (`TFQ-0423`)
- **Stage**: `PREGENESIS`
- **Status**: `CONDITIONAL` (Narrowed; the declared identity convention remains an explicit host import)
- **Lean 4 Module**: `lean4/CampaignPgwIdentityConventionUndecidable.lean`
- **Independent Checker**: `checks/independent/pgw-identity-convention-undecidable.py`

---

## 1. Narrowed Mathematical Scope

The Pre-Genesis node `PGW-IDENTITY-CONVENTION-UNDECIDABLE` (`TFQ-0423`) states that whether supplying `<a>` after `<>` introduces a new state depends on an identity convention (`opaque` vs `exact-inscription`) that no prompt had declared:
1. Under the **opaque convention** (`GenesisComputation.IdentityConvention.opaqueConv`), internal states are observation classes under the regime's internal observation family $O$. When $O = \emptyset$, `<>` and `<a>` share the empty observation profile, so `<a>` is not a new state ($\Delta = 0$, matching Trials 1 and 2).
2. Under the **exact-inscription convention** (`GenesisComputation.IdentityConvention.exactInscription`), states are syntactic inscriptions; since $\text{\texttt{<>}} \ne \text{\texttt{<a>}}$, supplying `<a>` adds one syntactic state ($\Delta = +1$, matching the full replay).
3. Until one convention is declared by the host, `queryNewState none` retains both branch verdicts as `.undecidableWithoutConvention false true`.

To avoid hard-coding a constant map (compare the PR 185 review of `TFQ-0422`), `lean4/CampaignPgwIdentityConventionUndecidable.lean` models a general observation-family regime `PreGenesisRegime α β` with presented inscriptions `presented : Finset α` and an explicit observation list `obs : List (α → β)`, connects profile equality directly to `PreMssn.Observation.SameProfile` (`lean4/Imported/PreGenesisToMssn/Observation.lean`) and to `GenesisComputation.Collapsed` / `GenesisComputation.UnarySep` (`lean4/GenesisComputation.lean`), and keeps the node at `CONDITIONAL`.

---

## 2. Summary of Formalized Theorems (`lean4/CampaignPgwIdentityConventionUndecidable.lean`)

1. `supplyInscription_preserves_obs_and_enlarges_presentation`:
   For any `R : PreGenesisRegime α β` and fresh inscription `x ∉ R.presented`, `(supplyInscription R x).obs = R.obs` ($O_1 = O_0$), `obsProfile (supplyInscription R x) = obsProfile R`, and `(supplyInscription R x).presented.card = R.presented.card + 1`.
2. `obsProfile_eq_iff_sameProfile_and_empty_obs_collapse`:
   `obsProfile R x = obsProfile R y ↔ PreMssn.Observation.SameProfile (indexedObs R) x y`; when `R.obs = []`, `obsProfile R x = []`, `SameProfile (indexedObs R) x y`, and `profileClass (indexedObs R) x = profileClass (indexedObs R) y` for all `x, y : α`.
3. `supply_markA_after_ground_branch_divergence`:
   On `initialRegime` (`presented = {ground}`, `obs = []`) and supplied token `markA`, `isNewStateUnder .opaqueConv initialRegime .markA = false`, `isNewStateUnder .exactInscription initialRegime .markA = true`, and `queryNewState none initialRegime .markA = .undecidableWithoutConvention false true`.
4. `stateCount_supply_markA_delta_zero_vs_one`:
   Supplying `markA` to `initialRegime` leaves `stateCountUnder .opaqueConv` at `1` ($\Delta = 0$) and increases `stateCountUnder .exactInscription` from `1` to `2` ($\Delta = +1$).
5. `opaque_stateCount_le_exact_stateCount`:
   For every finite regime `R`, `stateCountUnder .opaqueConv R ≤ stateCountUnder .exactInscription R`.
6. `conventions_agree_iff_fresh_profile`:
   For any `x ∉ R.presented`, `isNewStateUnder .opaqueConv R x = isNewStateUnder .exactInscription R x ↔ obsProfile R x ∉ R.presented.image (obsProfile R)`.
7. `injective_obsProfile_implies_conventions_coincide`:
   When `obsProfile R` is injective, `isNewStateUnder` and `stateCountUnder` coincide across `.opaqueConv` and `.exactInscription`.
8. `genesisUnaryProfile_eq_iff_collapsed`:
   For any `r : GenesisComputation.GenesisCopy.Regime` and data `i, j : Nat`, `genesisUnaryProfile r i = genesisUnaryProfile r j ↔ GenesisComputation.Collapsed r i j`.
9. `unformed_vs_firstSeparation_regime_convention_bridge`:
   Contrasts the unformed 2-datum Genesis regime `⟨2, [], [], [], []⟩` (`Collapsed`, equal empty profiles) with `GenesisComputation.firstSeparationRegime` (`[true] ≠ [false]`, not `Collapsed`).
10. `no_convention_free_evaluator_fence`:
    No convention-independent boolean evaluator simultaneously agrees with both `.opaqueConv` and `.exactInscription` on `(initialRegime, .markA)`.
11. `trial_votes_do_not_determine_convention_fence`:
    The recorded Prompt 12 replies (`![.opaqueConv, .opaqueConv, .exactInscription]`) realize both conventions and exhibit the branch split rather than resolving the undeclared convention.

---

## 3. Claim Hygiene Summary

1. **What it supports**:
   - In the finite observation-family and Genesis unary-form regime models, supplying a fresh inscription with $O = \emptyset$ yields `false` ($\Delta = 0$) under `.opaqueConv` and `true` ($\Delta = +1$) under `.exactInscription`, while both conventions coincide whenever the observation profile map is injective.
2. **What it does not support**:
   - Does not derive or select either identity convention from unannotated prompt text or from the three recorded model replies; the identity convention remains an explicit host import (`CONDITIONAL`).
3. **Narrowest defensible claim**:
   - Within `PreGenesisRegime` and `GenesisComputation.GenesisCopy.Regime`, state novelty of a supplied inscription is decidable once an `IdentityConvention` is supplied, coincides across conventions on profile-injective regimes, and splits into two distinct branches (`false` vs `true`) when $O = \emptyset$ and no convention is declared.
4. **Next test needed**:
   - Connect the three-valued convention-gated query to `TFQ-0424` (`PGW-ABSENCE-OF-RULE-NOT-IDENTIFICATION`) to verify that an undeclared relation returns `UNDECIDABLE` rather than installing an object-language identification rule.
