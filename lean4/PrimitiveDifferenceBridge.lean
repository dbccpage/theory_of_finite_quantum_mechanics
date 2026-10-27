
import PrimitiveDifference






namespace ObstructionCore.PrimitiveDifferenceBridge

open PrimitiveDifference

universe u v w

variable {α : Type u} {γ : Type v} {τ : Type w}

def profile (questions : List (α → γ)) (x : α) : List γ :=
  questions.map (fun question => question x)

def FamilyMisses (questions : List (α → γ)) (x y : α) : Prop :=
  profile questions x = profile questions y

def presentationDifference (questions : List (α → γ)) :
    PrimitiveDifference α (List γ × List γ) where
  δ x y := (profile questions x, profile questions y)
  Zero answerPair := answerPair.1 = answerPair.2
  zero_refl := fun _ => rfl
  zero_symm := fun _ _ h => h.symm
  zero_trans := fun _ _ _ hxy hyz => hxy.trans hyz

theorem familyMisses_iff_zeroRel
    (questions : List (α → γ)) (x y : α) :
    FamilyMisses questions x y ↔
      (presentationDifference questions).ZeroRel x y :=
  Iff.rfl

def RetainedDifference (retained : α → α → Prop) (x y : α) : Prop :=
  retained x y

def Protected (guarded : α → α → Prop) (x y : α) : Prop :=
  guarded x y

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

def DerivedFromProfile
    (questions : List (α → γ)) (observer : α → τ) : Prop :=
  ∃ derive : List γ → τ,
    ∀ x : α, observer x = derive (profile questions x)

theorem derived_observer_cannot_separate
    (questions : List (α → γ)) (observer : α → τ)
    {x y : α}
    (hderived : DerivedFromProfile questions observer)
    (hmissed : FamilyMisses questions x y) :
    observer x = observer y := by
  obtain ⟨derive, hderive⟩ := hderived
  rw [hderive x, hderive y, hmissed]

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

theorem separator_not_derived_from_old_profile
    (questions : List (α → γ)) (target : α → τ)
    {x y : α}
    (hmissed : FamilyMisses questions x y)
    (hseparates : target x ≠ target y) :
    ¬ DerivedFromProfile questions target := by
  intro hderived
  exact hseparates
    (derived_observer_cannot_separate questions target hderived hmissed)

def PresentationRefines
    (oldQuestions newQuestions : List (α → γ)) : Prop :=
  ∀ a b : α,
    FamilyMisses newQuestions a b → FamilyMisses oldQuestions a b

def StrictSplit
    (oldQuestions newQuestions : List (α → γ)) (x y : α) : Prop :=
  PresentationRefines oldQuestions newQuestions ∧
    FamilyMisses oldQuestions x y ∧
    ¬ FamilyMisses newQuestions x y

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

theorem obstruction_persists_without_split
    (oldQuestions newQuestions : List (α → γ))
    (retained guarded : α → α → Prop) {x y : α}
    (hold : ActiveObstruction oldQuestions retained guarded x y)
    (hnewMissed : FamilyMisses newQuestions x y) :
    ActiveObstruction newQuestions retained guarded x y :=
  ⟨hold.1, hold.2.1, hnewMissed⟩

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

end ObstructionCore.PrimitiveDifferenceBridge

#print axioms ObstructionCore.PrimitiveDifferenceBridge.familyMisses_iff_zeroRel
#print axioms ObstructionCore.PrimitiveDifferenceBridge.retained_protected_miss_active
#print axioms ObstructionCore.PrimitiveDifferenceBridge.derived_observer_cannot_separate
#print axioms ObstructionCore.PrimitiveDifferenceBridge.separator_no_factor_through_old_quotient
#print axioms ObstructionCore.PrimitiveDifferenceBridge.separator_not_derived_from_old_profile
#print axioms ObstructionCore.PrimitiveDifferenceBridge.strictSplit_refines_zeroRel
#print axioms ObstructionCore.PrimitiveDifferenceBridge.residualRefinementMap_classOf
#print axioms ObstructionCore.PrimitiveDifferenceBridge.strictSplit_refines_residual_quotient
#print axioms ObstructionCore.PrimitiveDifferenceBridge.obstruction_persists_without_split
#print axioms ObstructionCore.PrimitiveDifferenceBridge.separator_outside_profile_derived_family

private def l5aProvenance : String :=
  "Origin: lean4/PrimitiveDifferenceBridge.lean Claim: familyMisses_iff_zeroRel AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
