import Imported.PreGenesisToMssn.Observation
import GenesisComputation
import Mathlib.Data.Finset.Card
import Mathlib.Data.Finset.Image
import Mathlib.Data.List.Basic
import Mathlib.Tactic

/-!
# Campaign: PGW-IDENTITY-CONVENTION-UNDECIDABLE (TFQ-0423)

AuthorityEffect: None.

Target: `PGW-IDENTITY-CONVENTION-UNDECIDABLE` (`TFQ-0423`, Stage: `PREGENESIS`, Status: `CONDITIONAL`).
Outcome: Narrowed (`CONDITIONAL` preserved; the host-declared identity convention remains an explicit
imported assumption).

Mathematical Content:
1. **Observation-Family Regime & Supply Step (`PreGenesisRegime α β`)**:
   - Models a finite presentation set `presented : Finset α` paired with an explicit list of
     internal observations `obs : List (α → β)` rather than a hard-coded constant map.
   - `supplyInscription` inserts an inscription `x` into `presented` while preserving `obs`:
     `(supplyInscription R x).obs = R.obs` ($O_1 = O_0$), and for `x ∉ R.presented`,
     `(supplyInscription R x).presented.card = R.presented.card + 1`.
2. **Bridge to `PreMssn.Observation.SameProfile` and `empty_profiles_equal`**:
   - Establishes that equality of the observation profile `obsProfile R x = obsProfile R y` is
     equivalent to `PreMssn.Observation.SameProfile (indexedObs R) x y`, hence to equality in
     the observational quotient `PreMssn.Observation.profileClass (indexedObs R) x = profileClass (indexedObs R) y`.
   - When `R.obs = []` ($O = \emptyset$), `obsProfile R x = []` and `SameProfile (indexedObs R) x y`
     holds for all `x, y : α`.
3. **Explicit Identity-Convention Branching (`GenesisComputation.IdentityConvention`)**:
   - Defines `isNewStateUnder (c : GenesisComputation.IdentityConvention) (R : PreGenesisRegime α β) (x : α) : Bool`:
     under `.opaqueConv`, `x` is a new state iff its observation profile `obsProfile R x` does not
     already appear in `R.presented.image (obsProfile R)`; under `.exactInscription`, `x` is a new
     state iff `x ∉ R.presented`.
   - Defines the three-valued convention-gated query `queryNewState`: when no convention is
     declared (`none`), it returns `.undecidableWithoutConvention opaqueBranch exactBranch`, keeping
     both branches distinct until a convention (`some c`) is supplied.
4. **Prompt 12 Branch Divergence (`<>` vs `<a>` with $O = \emptyset$)**:
   - On `initialRegime` (`presented = {ground}`, `obs = []`) and supplied inscription `markA` (`<a>`),
     `isNewStateUnder .opaqueConv initialRegime .markA = false` (Trials 1 & 2 branch) whereas
     `isNewStateUnder .exactInscription initialRegime .markA = true` (full replay branch), and
     the post-supply state count is `1` under `.opaqueConv` ($\Delta = 0$) vs `2` under
     `.exactInscription` ($\Delta = +1$).
5. **General Cardinality Bound & Pairwise-Separation Agreement**:
   - For any finite regime `R`, `stateCountUnder .opaqueConv R ≤ stateCountUnder .exactInscription R`.
   - When `obsProfile R` is injective on `α`, both conventions coincide (`isNewStateUnder` and
     `stateCountUnder` agree).
6. **Bridge to `GenesisComputation.GenesisCopy.Regime`, `UnarySep`, and `Collapsed`**:
   - Defines `genesisUnaryProfile` over the admitted unary forms of a `GenesisComputation.GenesisCopy.Regime`
     and establishes `genesisUnaryProfile r i = genesisUnaryProfile r j ↔ GenesisComputation.Collapsed r i j`,
     connecting the Pre-Genesis profile quotient directly to `GenesisComputation.UnarySep` and
     `GenesisComputation.firstSeparationRegime`.
7. **Scope Fences**:
   - No convention-independent boolean evaluator simultaneously matches both `.opaqueConv` and
     `.exactInscription` on `(initialRegime, .markA)`.
   - Recording the three model replies (`![.opaqueConv, .opaqueConv, .exactInscription]`) exhibits
     both branches and does not resolve the convention without a host declaration.
-/

namespace CampaignPgwIdentityConventionUndecidable

open GenesisComputation
open GenesisComputation.GenesisCopy
open PreMssn.Observation

/-- A finite Pre-Genesis regime with presented inscriptions `presented : Finset α`
and internal observation family `obs : List (α → β)`. -/
structure PreGenesisRegime (α β : Type*) where
  presented : Finset α
  obs : List (α → β)

/-- Supplying an inscription `x` adds `x` to the presentation set `presented` and leaves
the internal observation family `obs` unchanged ($O_1 = O_0$). -/
def supplyInscription {α β : Type*} [DecidableEq α]
    (R : PreGenesisRegime α β) (x : α) : PreGenesisRegime α β :=
  ⟨insert x R.presented, R.obs⟩

/-- The internal observation profile of an inscription `x` under `R.obs`. -/
def obsProfile {α β : Type*} (R : PreGenesisRegime α β) (x : α) : List β :=
  R.obs.map (fun o => o x)

/-- Theorem 1 (Supply Preserves Observation Family and Enlarges Presentation by `+1`):
Supplying a fresh inscription `x ∉ R.presented` preserves the observation family
`(supplyInscription R x).obs = R.obs`, preserves `obsProfile`, and increases
`presented.card` by `1`. -/
theorem supplyInscription_preserves_obs_and_enlarges_presentation
    {α β : Type*} [DecidableEq α] (R : PreGenesisRegime α β) (x : α)
    (hfresh : x ∉ R.presented) :
    (supplyInscription R x).obs = R.obs ∧
    obsProfile (supplyInscription R x) = obsProfile R ∧
    (supplyInscription R x).presented.card = R.presented.card + 1 := by
  refine ⟨rfl, rfl, ?_⟩
  simp [supplyInscription, Finset.card_insert_of_notMem hfresh]

/-- Indexed observation family `Fin R.obs.length → α → β` for `PreMssn.Observation.SameProfile`. -/
def indexedObs {α β : Type*} (R : PreGenesisRegime α β) (i : Fin R.obs.length) (x : α) : β :=
  (R.obs.get i) x

/-- Theorem 2 (Profile Equality Matches `PreMssn.Observation.SameProfile` and Empty-`O` Collapse):
`obsProfile R x = obsProfile R y` holds iff `SameProfile (indexedObs R) x y` holds (and hence iff
their observational quotient classes in `Observed (indexedObs R)` are equal); when `R.obs = []`,
every pair of inscriptions has equal empty profile and equal `profileClass`. -/
theorem obsProfile_eq_iff_sameProfile_and_empty_obs_collapse
    {α β : Type*} (R : PreGenesisRegime α β) (x y : α) :
    (obsProfile R x = obsProfile R y ↔ SameProfile (indexedObs R) x y) ∧
    (R.obs = [] →
      obsProfile R x = [] ∧
      SameProfile (indexedObs R) x y ∧
      profileClass (indexedObs R) x = profileClass (indexedObs R) y) := by
  refine ⟨?_, ?_⟩
  · constructor
    · intro h i
      have hget := congrArg (fun l : List β => l[i.val]?) h
      simp [obsProfile] at hget
      exact hget
    · intro h
      apply List.ext_getElem
      · simp [obsProfile]
      · intro n hn1 hn2
        have hn : n < R.obs.length := by simpa [obsProfile] using hn1
        simpa [obsProfile, indexedObs] using h ⟨n, hn⟩
  · intro hempty
    have hpx : obsProfile R x = [] := by simp [obsProfile, hempty]
    have hsame : SameProfile (indexedObs R) x y := by
      intro ⟨i, hi⟩
      simp [hempty] at hi
    exact ⟨hpx, hsame, (profile_class_eq_iff (indexedObs R) x y).mpr hsame⟩

/-- Whether supplying `x` to `R` yields a new state under identity convention `c`:
- Under `.opaqueConv`: `x` is a new state iff `obsProfile R x` is not already in the image of `R.presented`.
- Under `.exactInscription`: `x` is a new state iff `x` is not already in `R.presented`. -/
def isNewStateUnder {α β : Type*} [DecidableEq α] [DecidableEq β]
    (c : IdentityConvention) (R : PreGenesisRegime α β) (x : α) : Bool :=
  match c with
  | .opaqueConv => decide (obsProfile R x ∉ R.presented.image (obsProfile R))
  | .exactInscription => decide (x ∉ R.presented)

/-- Three-valued verdict returned when querying whether `x` is a new state:
without a declared convention (`none`), both branch answers are kept and the query is marked
undecidable until one convention is declared. -/
inductive ConventionVerdict
  | undecidableWithoutConvention (opaqueBranch exactBranch : Bool)
  | decided (isNew : Bool)
  deriving DecidableEq, Repr

/-- Convention-gated state novelty query. -/
def queryNewState {α β : Type*} [DecidableEq α] [DecidableEq β]
    (optConv : Option IdentityConvention) (R : PreGenesisRegime α β) (x : α) :
    ConventionVerdict :=
  match optConv with
  | none =>
      .undecidableWithoutConvention
        (isNewStateUnder .opaqueConv R x)
        (isNewStateUnder .exactInscription R x)
  | some c => .decided (isNewStateUnder c R x)

/-- State count of `R` under identity convention `c`:
cardinality of the observation-profile quotient image under `.opaqueConv`,
and syntactic presentation cardinality under `.exactInscription`. -/
def stateCountUnder {α β : Type*} [DecidableEq α] [DecidableEq β]
    (c : IdentityConvention) (R : PreGenesisRegime α β) : Nat :=
  match c with
  | .opaqueConv => (R.presented.image (obsProfile R)).card
  | .exactInscription => R.presented.card

/-- Finite Pre-Genesis inscription tokens (`<>`, `<a>`, `<b>`, `<ab>`). -/
inductive PreGenesisToken
  | ground
  | markA
  | markB
  | markAB
  deriving DecidableEq, Repr

/-- Initial Pre-Genesis regime before `<a>` is supplied: `P_0 = {<>}` and `O_0 = []`. -/
def initialRegime : PreGenesisRegime PreGenesisToken Bool :=
  ⟨{.ground}, []⟩

/-- Post-supply Pre-Genesis regime after `<a>` is supplied after `<>`: `P_1 = {<>, <a>}` and `O_1 = []`. -/
def afterSupplyRegime : PreGenesisRegime PreGenesisToken Bool :=
  supplyInscription initialRegime .markA

/-- Theorem 3 (Prompt 12 Branch Divergence for `<a>` Supplied After `<>` with $O = \emptyset$):
With `initialRegime` (`P_0 = {<>}`, `O_0 = []`) and supplied token `markA` (`<a>`),
the opaque convention reports `false` (no new state, matching Trials 1 & 2), the
exact-inscription convention reports `true` (a new syntactic state, matching the full replay),
and `queryNewState none` keeps both branches as `.undecidableWithoutConvention false true`. -/
theorem supply_markA_after_ground_branch_divergence :
    PreGenesisToken.ground ≠ PreGenesisToken.markA ∧
    isNewStateUnder .opaqueConv initialRegime .markA = false ∧
    isNewStateUnder .exactInscription initialRegime .markA = true ∧
    isNewStateUnder .opaqueConv initialRegime .markA ≠
      isNewStateUnder .exactInscription initialRegime .markA ∧
    queryNewState none initialRegime .markA = .undecidableWithoutConvention false true ∧
    queryNewState (some .opaqueConv) initialRegime .markA = .decided false ∧
    queryNewState (some .exactInscription) initialRegime .markA = .decided true := by
  decide

/-- Theorem 4 (State-Count Increment Dichotomy: $\Delta = 0$ Opaque vs $\Delta = +1$ Exact):
Supplying `<a>` after `<>` with $O = \emptyset$ leaves the opaque state count at `1`
($\Delta = 0$) while increasing the exact-inscription state count from `1` to `2` ($\Delta = +1$). -/
theorem stateCount_supply_markA_delta_zero_vs_one :
    stateCountUnder .opaqueConv initialRegime = 1 ∧
    stateCountUnder .exactInscription initialRegime = 1 ∧
    stateCountUnder .opaqueConv afterSupplyRegime = 1 ∧
    stateCountUnder .exactInscription afterSupplyRegime = 2 ∧
    stateCountUnder .exactInscription afterSupplyRegime -
      stateCountUnder .opaqueConv afterSupplyRegime = 1 := by
  decide

/-- Theorem 5 (General Opaque-vs-Exact State Count Inequality):
For every finite Pre-Genesis regime `R`, the opaque state count never exceeds the
exact-inscription state count. -/
theorem opaque_stateCount_le_exact_stateCount
    {α β : Type*} [DecidableEq α] [DecidableEq β] (R : PreGenesisRegime α β) :
    stateCountUnder .opaqueConv R ≤ stateCountUnder .exactInscription R := by
  simpa [stateCountUnder] using Finset.card_image_le (s := R.presented) (f := obsProfile R)

/-- Theorem 6 (Exact Criterion for Branch Agreement on a Fresh Inscription):
For any fresh inscription `x ∉ R.presented`, the opaque and exact-inscription conventions
give the same novelty answer if and only if `obsProfile R x` does not collide with the
observation profile of any already-presented inscription. -/
theorem conventions_agree_iff_fresh_profile
    {α β : Type*} [DecidableEq α] [DecidableEq β]
    (R : PreGenesisRegime α β) (x : α) (hfresh : x ∉ R.presented) :
    (isNewStateUnder .opaqueConv R x = isNewStateUnder .exactInscription R x) ↔
      obsProfile R x ∉ R.presented.image (obsProfile R) := by
  simp [isNewStateUnder, hfresh]

/-- Theorem 7 (Injective Observation Profile Makes Opaque and Exact Conventions Coincide):
Whenever the observation profile map `obsProfile R` is injective (every pair of distinct
inscriptions is separated by some observation in `R.obs`), `isNewStateUnder` and
`stateCountUnder` agree across `.opaqueConv` and `.exactInscription`. -/
theorem injective_obsProfile_implies_conventions_coincide
    {α β : Type*} [DecidableEq α] [DecidableEq β]
    (R : PreGenesisRegime α β) (hinj : Function.Injective (obsProfile R)) (x : α) :
    isNewStateUnder .opaqueConv R x = isNewStateUnder .exactInscription R x ∧
    stateCountUnder .opaqueConv R = stateCountUnder .exactInscription R := by
  refine ⟨?_, ?_⟩
  · simp only [isNewStateUnder, Finset.mem_image]
    congr 1
    apply propext
    constructor
    · intro h hx
      exact h ⟨x, hx, rfl⟩
    · rintro h ⟨y, hy, heq⟩
      have hyx : y = x := hinj heq
      subst hyx
      exact h hy
  · simpa [stateCountUnder] using Finset.card_image_of_injective R.presented hinj

/-- Unary observation profile of a datum `i` in a `GenesisComputation.GenesisCopy.Regime` `r`. -/
def genesisUnaryProfile (r : Regime) (i : Nat) : List Bool :=
  (List.range r.forms.length).map (fun f => decide (r.forms.getD f 0 = 1 ∧ (f, [i]) ∈ r.insts))

/-- Theorem 8 (Genesis Unary Profile Equality Characterizes `GenesisComputation.Collapsed`):
In any `GenesisComputation.GenesisCopy.Regime` `r`, two data `i` and `j` have identical
`genesisUnaryProfile` if and only if they are `Collapsed r i j` (`¬ UnarySep r i j ∧ ¬ UnarySep r j i`). -/
theorem genesisUnaryProfile_eq_iff_collapsed (r : Regime) (i j : Nat) :
    genesisUnaryProfile r i = genesisUnaryProfile r j ↔ Collapsed r i j := by
  constructor
  · intro heq
    have hpoint : ∀ f < r.forms.length,
        ((r.forms.getD f 0 = 1 ∧ (f, [i]) ∈ r.insts) ↔
         (r.forms.getD f 0 = 1 ∧ (f, [j]) ∈ r.insts)) := by
      intro f hf
      have hget := congrArg (fun l : List Bool => l[f]?) heq
      simp only [genesisUnaryProfile, List.getElem?_map, List.getElem?_range, hf,
        Option.map_some, Option.some.injEq, decide_eq_decide] at hget
      exact hget
    refine ⟨?_, ?_⟩
    · rintro ⟨f, hf, har, ⟨hi, hj⟩ | ⟨hj, hi⟩⟩
      · exact hj ((hpoint f hf).mp ⟨har, hi⟩).2
      · exact hi ((hpoint f hf).mpr ⟨har, hj⟩).2
    · rintro ⟨f, hf, har, ⟨hj, hi⟩ | ⟨hi, hj⟩⟩
      · exact hi ((hpoint f hf).mpr ⟨har, hj⟩).2
      · exact hj ((hpoint f hf).mp ⟨har, hi⟩).2
  · rintro ⟨hnot1, _⟩
    apply List.ext_getElem
    · simp [genesisUnaryProfile]
    · intro f hf1 _
      have hf : f < r.forms.length := by simpa [genesisUnaryProfile] using hf1
      simp only [genesisUnaryProfile, List.getElem_map, List.getElem_range, decide_eq_decide]
      constructor
      · rintro ⟨har, hi⟩
        refine ⟨har, ?_⟩
        by_contra hj
        exact hnot1 ⟨f, hf, har, Or.inl ⟨hi, hj⟩⟩
      · rintro ⟨har, hj⟩
        refine ⟨har, ?_⟩
        by_contra hi
        exact hnot1 ⟨f, hf, har, Or.inr ⟨hj, hi⟩⟩

/-- Theorem 9 (Unformed Two-Datum Regime vs `firstSeparationRegime` Profile Contrast):
In the unformed 2-datum Genesis regime `⟨2, [], [], [], []⟩` ($O = \emptyset$), data `0` and `1`
are `Collapsed` and share the empty unary profile `[]`; in `firstSeparationRegime`
(`⟨2, [1], [(0, [0])], [], [(0, 1)]⟩`), data `0` and `1` have distinct unary profiles
`[true] ≠ [false]` and are not `Collapsed`. -/
theorem unformed_vs_firstSeparation_regime_convention_bridge :
    genesisUnaryProfile ⟨2, [], [], [], []⟩ 0 = genesisUnaryProfile ⟨2, [], [], [], []⟩ 1 ∧
    Collapsed ⟨2, [], [], [], []⟩ 0 1 ∧
    genesisUnaryProfile firstSeparationRegime 0 = [true] ∧
    genesisUnaryProfile firstSeparationRegime 1 = [false] ∧
    genesisUnaryProfile firstSeparationRegime 0 ≠ genesisUnaryProfile firstSeparationRegime 1 ∧
    ¬ Collapsed firstSeparationRegime 0 1 := by
  decide

/-- Theorem 10 (Scope Fence — No Convention-Free Evaluator Factors Both Conventions):
No convention-independent boolean evaluator `eval : PreGenesisRegime PreGenesisToken Bool → PreGenesisToken → Bool`
can simultaneously agree with both `isNewStateUnder .opaqueConv` and
`isNewStateUnder .exactInscription`. -/
theorem no_convention_free_evaluator_fence :
    ¬ ∃ eval : PreGenesisRegime PreGenesisToken Bool → PreGenesisToken → Bool,
      (∀ R x, eval R x = isNewStateUnder .opaqueConv R x) ∧
      (∀ R x, eval R x = isNewStateUnder .exactInscription R x) := by
  rintro ⟨eval, hop, hex⟩
  have h1 := hop initialRegime .markA
  have h2 := hex initialRegime .markA
  rw [h1] at h2
  revert h2
  decide

/-- Recorded Prompt 12 model trial replies: Trial 1 (`.opaqueConv`), Trial 2 (`.opaqueConv`),
and Full Replay (`.exactInscription`). -/
def prompt12TrialConventions : Fin 3 → IdentityConvention :=
  ![.opaqueConv, .opaqueConv, .exactInscription]

/-- Theorem 11 (Scope Fence — Recorded Trial Replies Split Across Both Conventions):
The recorded Prompt 12 replies realize both `.opaqueConv` (Trials 1 & 2, yielding `false`) and
`.exactInscription` (Full Replay, yielding `true`), so the trial record exhibits the
branch split rather than resolving the undeclared convention. -/
theorem trial_votes_do_not_determine_convention_fence :
    prompt12TrialConventions 0 = .opaqueConv ∧
    prompt12TrialConventions 1 = .opaqueConv ∧
    prompt12TrialConventions 2 = .exactInscription ∧
    isNewStateUnder (prompt12TrialConventions 0) initialRegime .markA = false ∧
    isNewStateUnder (prompt12TrialConventions 2) initialRegime .markA = true := by
  decide

end CampaignPgwIdentityConventionUndecidable

#print axioms CampaignPgwIdentityConventionUndecidable.supplyInscription_preserves_obs_and_enlarges_presentation
#print axioms CampaignPgwIdentityConventionUndecidable.obsProfile_eq_iff_sameProfile_and_empty_obs_collapse
#print axioms CampaignPgwIdentityConventionUndecidable.supply_markA_after_ground_branch_divergence
#print axioms CampaignPgwIdentityConventionUndecidable.stateCount_supply_markA_delta_zero_vs_one
#print axioms CampaignPgwIdentityConventionUndecidable.opaque_stateCount_le_exact_stateCount
#print axioms CampaignPgwIdentityConventionUndecidable.conventions_agree_iff_fresh_profile
#print axioms CampaignPgwIdentityConventionUndecidable.injective_obsProfile_implies_conventions_coincide
#print axioms CampaignPgwIdentityConventionUndecidable.genesisUnaryProfile_eq_iff_collapsed
#print axioms CampaignPgwIdentityConventionUndecidable.unformed_vs_firstSeparation_regime_convention_bridge
#print axioms CampaignPgwIdentityConventionUndecidable.no_convention_free_evaluator_fence
#print axioms CampaignPgwIdentityConventionUndecidable.trial_votes_do_not_determine_convention_fence
