import PrimitiveDifference

/-!
# Presented question families as Primitive Difference observers

This file is an independent local re-proof of the bridge suggested by the
finite compression results in `dbccpage/19L57G1` at merge commit
`1f272ef269496d8f8a9d52ca4a078f3789e67d73`.  It imports no foreign source.

The bridge is deliberately narrow:

* a represented family of questions induces a profile presentation;
* equality of profiles is exactly the presentation's `ZeroRel`;
* a retained and protected pair in that relation is an active obstruction;
* a target that separates the pair cannot factor through the old quotient;
* any replay record or derived observer that factors through the old profile
  cannot separate the pair;
* a genuine split refines the quotient and is therefore new structure
  relative to the old presentation.

No cochain complex, solver completeness, authorization, or universal
ontology is inferred.  `AuthorityEffect = None` is a scope statement, not a
Lean-level authority constructor.
-/

namespace OmegaCore.FablePrimitiveDifferenceBridge

open PrimitiveDifference

universe u v w

variable {α : Type u} {γ : Type v} {τ : Type w}

/-- The ordered answer profile of `x` under the represented question family.
Order is represented data; no symmetry or quotient of questions is assumed. -/
def profile (questions : List (α → γ)) (x : α) : List γ :=
  questions.map (fun question => question x)

/-- A question family misses a pair exactly when its represented answer
profiles agree. -/
def FamilyMisses (questions : List (α → γ)) (x y : α) : Prop :=
  profile questions x = profile questions y

/-- The Primitive Difference induced by a question-family presentation.
The difference value retains both endpoint profiles; `Zero` is equality of
those profiles. -/
def presentationDifference (questions : List (α → γ)) :
    PrimitiveDifference α (List γ × List γ) where
  δ x y := (profile questions x, profile questions y)
  Zero answerPair := answerPair.1 = answerPair.2
  zero_refl := fun _ => rfl
  zero_symm := fun _ _ h => h.symm
  zero_trans := fun _ _ _ hxy hyz => hxy.trans hyz

/-- Fable-style family collapse and the Omega kernel's `ZeroRel` are the same
relation for this presentation. -/
theorem familyMisses_iff_zeroRel
    (questions : List (α → γ)) (x y : α) :
    FamilyMisses questions x y ↔
      (presentationDifference questions).ZeroRel x y :=
  Iff.rfl

/-- Retention is represented separately from observation. -/
def RetainedDifference (retained : α → α → Prop) (x y : α) : Prop :=
  retained x y

/-- Protection is represented separately from both retention and
observation. -/
def Protected (guarded : α → α → Prop) (x y : α) : Prop :=
  guarded x y

/-- The minimal active-obstruction bridge: retained, protected, and missed by
the declared presentation. -/
def ActiveObstruction
    (questions : List (α → γ))
    (retained guarded : α → α → Prop) (x y : α) : Prop :=
  RetainedDifference retained x y ∧
    Protected guarded x y ∧
    FamilyMisses questions x y

theorem retained_protected_miss_active
    (questions : List (α → γ))
    (retained guarded : α → α → Prop) (x y : α)
    (hretained : retained x y)
    (hprotected : guarded x y)
    (hmissed : FamilyMisses questions x y) :
    ActiveObstruction questions retained guarded x y :=
  ⟨hretained, hprotected, hmissed⟩

/-- A derived observer adds no separating information: it is a function of
the old represented profile. -/
def DerivedFromProfile
    (questions : List (α → γ)) (observer : α → τ) : Prop :=
  ∃ derive : List γ → τ,
    ∀ x : α, observer x = derive (profile questions x)

/-- Replay records, hashes, summaries, and other deterministic
postcompositions of the old profile cannot split an old zero-related pair. -/
theorem derived_observer_cannot_separate
    (questions : List (α → γ)) (observer : α → τ)
    {x y : α}
    (hderived : DerivedFromProfile questions observer)
    (hmissed : FamilyMisses questions x y) :
    observer x = observer y := by
  obtain ⟨derive, hderive⟩ := hderived
  rw [hderive x, hderive y, hmissed]

/-- A target that separates a pair missed by the old presentation cannot be
recovered from the old residual quotient.  This is the exact local-red side
of the Local-Green/Global-Red bridge. -/
theorem separator_no_factor_through_old_quotient
    (questions : List (α → γ)) (target : α → τ)
    {x y : α}
    (hmissed : FamilyMisses questions x y)
    (hseparates : target x ≠ target y) :
    ¬ (∃ factor :
          (presentationDifference questions).ResidualQuotient → τ,
        ∀ z : α,
          factor ((presentationDifference questions).classOf z) = target z) := by
  exact invariantFactor_no_factor_of_zeroRel_ne
    (presentationDifference questions) target
    ((familyMisses_iff_zeroRel questions x y).mp hmissed)
    hseparates

/-- Consequently, a genuine separator cannot itself be a replay-only
postcomposition of the old profile. -/
theorem separator_not_derived_from_old_profile
    (questions : List (α → γ)) (target : α → τ)
    {x y : α}
    (hmissed : FamilyMisses questions x y)
    (hseparates : target x ≠ target y) :
    ¬ DerivedFromProfile questions target := by
  intro hderived
  exact hseparates
    (derived_observer_cannot_separate questions target hderived hmissed)

/-- The new presentation preserves every distinction already represented by
the old presentation. Equivalently, every new zero-related pair was already
old-zero-related. This prevents a local split from hiding a collapse
elsewhere in the carrier. -/
def PresentationRefines
    (oldQuestions newQuestions : List (α → γ)) : Prop :=
  ∀ a b : α,
    FamilyMisses newQuestions a b → FamilyMisses oldQuestions a b

/-- A strict split is a global refinement-preserving extension that also
separates one particular pair missed by the old presentation. -/
def StrictSplit
    (oldQuestions newQuestions : List (α → γ)) (x y : α) : Prop :=
  PresentationRefines oldQuestions newQuestions ∧
    FamilyMisses oldQuestions x y ∧
    ¬ FamilyMisses newQuestions x y

/-- A strict split refines the complete represented zero relation, rather than
only improving one selected pair. -/
theorem strictSplit_refines_zeroRel
    (oldQuestions newQuestions : List (α → γ))
    {x y : α}
    (hsplit : StrictSplit oldQuestions newQuestions x y) :
    ∀ a b : α,
      (presentationDifference newQuestions).ZeroRel a b →
        (presentationDifference oldQuestions).ZeroRel a b := by
  intro a b hnew
  exact (familyMisses_iff_zeroRel oldQuestions a b).mp
    (hsplit.1 a b
      ((familyMisses_iff_zeroRel newQuestions a b).mpr hnew))

/-- Global presentation refinement induces the canonical map from finer new
residual classes to coarser old residual classes. -/
def residualRefinementMap
    (oldQuestions newQuestions : List (α → γ))
    (hrefines : PresentationRefines oldQuestions newQuestions) :
    (presentationDifference newQuestions).ResidualQuotient →
      (presentationDifference oldQuestions).ResidualQuotient :=
  quotientMapOfSetoidImp
    (zeroSetoid (presentationDifference newQuestions))
    (zeroSetoid (presentationDifference oldQuestions))
    (by
      intro a b hnew
      exact (familyMisses_iff_zeroRel oldQuestions a b).mp
        (hrefines a b
          ((familyMisses_iff_zeroRel newQuestions a b).mpr hnew)))

theorem residualRefinementMap_classOf
    (oldQuestions newQuestions : List (α → γ))
    (hrefines : PresentationRefines oldQuestions newQuestions)
    (a : α) :
    residualRefinementMap oldQuestions newQuestions hrefines
        ((presentationDifference newQuestions).classOf a) =
      (presentationDifference oldQuestions).classOf a :=
  rfl

/-- A strict split identifies the old quotient classes and distinguishes the
new quotient classes. -/
theorem strictSplit_refines_residual_quotient
    (oldQuestions newQuestions : List (α → γ))
    {x y : α}
    (hsplit : StrictSplit oldQuestions newQuestions x y) :
    (presentationDifference oldQuestions).classOf x =
        (presentationDifference oldQuestions).classOf y ∧
      (presentationDifference newQuestions).classOf x ≠
        (presentationDifference newQuestions).classOf y := by
  constructor
  · exact classOf_eq_of_zero (presentationDifference oldQuestions)
      ((familyMisses_iff_zeroRel oldQuestions x y).mp hsplit.2.1)
  · intro heq
    have hzero : (presentationDifference newQuestions).ZeroRel x y :=
      (classOf_eq_iff_zeroRel (presentationDifference newQuestions)).mp heq
    exact hsplit.2.2
      ((familyMisses_iff_zeroRel newQuestions x y).mpr hzero)

/-- If retention and protection persist but the new presentation does not
split the pair, the active obstruction persists. -/
theorem obstruction_persists_without_split
    (oldQuestions newQuestions : List (α → γ))
    (retained guarded : α → α → Prop) {x y : α}
    (hold : ActiveObstruction oldQuestions retained guarded x y)
    (hnewMissed : FamilyMisses newQuestions x y) :
    ActiveObstruction newQuestions retained guarded x y :=
  ⟨hold.1, hold.2.1, hnewMissed⟩

/-- Under an explicit exhaustiveness premise saying every admitted
same-level observer is derived from the old profile, any actual separator is
outside that same-level family.  This is a boundary theorem, not a proof that
any concrete registry is exhaustive. -/
theorem separator_outside_profile_derived_family
    (questions : List (α → γ))
    (admitted : List (α → τ))
    (hexhaustive : ∀ observer, observer ∈ admitted →
      DerivedFromProfile questions observer)
    {target : α → τ} {x y : α}
    (hmissed : FamilyMisses questions x y)
    (hseparates : target x ≠ target y) :
    target ∉ admitted := by
  intro htarget
  exact (separator_not_derived_from_old_profile
    questions target hmissed hseparates) (hexhaustive target htarget)

end OmegaCore.FablePrimitiveDifferenceBridge

#print axioms OmegaCore.FablePrimitiveDifferenceBridge.familyMisses_iff_zeroRel
#print axioms OmegaCore.FablePrimitiveDifferenceBridge.retained_protected_miss_active
#print axioms OmegaCore.FablePrimitiveDifferenceBridge.derived_observer_cannot_separate
#print axioms OmegaCore.FablePrimitiveDifferenceBridge.separator_no_factor_through_old_quotient
#print axioms OmegaCore.FablePrimitiveDifferenceBridge.separator_not_derived_from_old_profile
#print axioms OmegaCore.FablePrimitiveDifferenceBridge.strictSplit_refines_zeroRel
#print axioms OmegaCore.FablePrimitiveDifferenceBridge.residualRefinementMap_classOf
#print axioms OmegaCore.FablePrimitiveDifferenceBridge.strictSplit_refines_residual_quotient
#print axioms OmegaCore.FablePrimitiveDifferenceBridge.obstruction_persists_without_split
#print axioms OmegaCore.FablePrimitiveDifferenceBridge.separator_outside_profile_derived_family
