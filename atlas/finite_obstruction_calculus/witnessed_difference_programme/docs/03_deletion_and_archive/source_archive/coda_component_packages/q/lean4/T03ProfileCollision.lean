import D01D02Records

/-!
# CODA-Q T03: Profile Collision, Fiber Invariance & Primitive Impossibility

These retained model declarations use historical Q-LEGACY labels.
They are not the metric-completion theorems Q-T1 through Q-T5.

Formalizes:
1. Historical model label Q-LEGACY-T2: Profile collision blocks target factorization.
2. Target invariance on profile fibers <=> observed profile determinacy.
3. Primitive impossibility certificate: target-distinct profile collision.
4. Primitive impossibility blocks profile invariance and factorization.
5. Historical model label Q-LEGACY-T4: Repaired permission must separate primitive impossibility witness.
6. Fiber-respecting profile cannot repair primitive impossibility.

AuthorityEffect: None.
-/

namespace CodaQ

universe u v w

/-- A target is invariant on the fibers of a declared profile. -/
def TargetInvariantOnProfileFibers
    {World : Type u} {Profile : Type v} {Target : Type w}
    (profile : World → Profile) (target : World → Target) : Prop :=
  ∀ {a b : World}, profile a = profile b → target a = target b

/-- The observed profile values determine the target on their realized fibers. -/
def ObservedProfileDeterminesTarget
    {World : Type u} {Profile : Type v} {Target : Type w}
    (profile : World → Profile) (target : World → Target) : Prop :=
  ∀ profileValue : Profile,
    (∃ world : World, profile world = profileValue) →
      ∃ targetValue : Target,
        ∀ world : World,
          profile world = profileValue → target world = targetValue

/-- Target invariance on profile fibers is equivalent to observed profile determinacy. -/
theorem observed_profile_determines_target_iff_profile_fiber_invariance
    {World : Type u} {Profile : Type v} {Target : Type w}
    (profile : World → Profile) (target : World → Target) :
    ObservedProfileDeterminesTarget profile target ↔
      TargetInvariantOnProfileFibers profile target := by
  constructor
  · intro hObserved a b hProfile
    rcases hObserved (profile a) ⟨a, rfl⟩ with ⟨targetValue, hValue⟩
    have hA : target a = targetValue := hValue a rfl
    have hB : target b = targetValue := hValue b hProfile.symm
    exact hA.trans hB.symm
  · intro hInvariant profileValue ⟨world₀, hWorld₀⟩
    refine ⟨target world₀, ?_⟩
    intro world hWorld
    apply hInvariant
    exact hWorld.trans hWorld₀.symm

/-- A primitive impossibility certificate is a target-distinct profile collision. -/
def PrimitiveImpossibility
    {World : Type u} {Profile : Type v} {Target : Type w}
    (profile : World → Profile) (target : World → Target) : Prop :=
  ∃ a b : World, profile a = profile b ∧ target a ≠ target b

/-- Target factorization implies target invariance on profile fibers. -/
theorem target_factorization_implies_profile_fiber_invariance
    {World : Type u} {Profile : Type v} {Target : Type w}
    (profile : World → Profile) (target : World → Target)
    (hFactor : ∃ F : Profile → Target, ∀ w : World, F (profile w) = target w) :
    TargetInvariantOnProfileFibers profile target := by
  rcases hFactor with ⟨F, hF⟩
  intro a b hEq
  have hFa : target a = F (profile a) := (hF a).symm
  have hFb : target b = F (profile b) := (hF b).symm
  rw [hFa, hFb, hEq]

/-- Primitive impossibility blocks profile fiber invariance. -/
theorem primitive_impossibility_blocks_profile_fiber_invariance
    {World : Type u} {Profile : Type v} {Target : Type w}
    (profile : World → Profile) (target : World → Target) :
    PrimitiveImpossibility profile target →
      ¬ TargetInvariantOnProfileFibers profile target := by
  intro ⟨a, b, hProf, hTarg⟩ hInv
  exact hTarg (hInv hProf)

/-- Historical model label Q-LEGACY-T2: Primitive impossibility blocks profile factorization. -/
theorem primitive_impossibility_blocks_profile_factorization
    {World : Type u} {Profile : Type v} {Target : Type w}
    (profile : World → Profile) (target : World → Target) :
    PrimitiveImpossibility profile target →
      ¬ (∃ F : Profile → Target, ∀ w : World, F (profile w) = target w) := by
  intro hImp hFact
  exact (primitive_impossibility_blocks_profile_fiber_invariance profile target hImp)
    (target_factorization_implies_profile_fiber_invariance profile target hFact)

/-- Historical model label Q-LEGACY-T4: Any repairing profile must separate the old primitive impossibility witness. -/
theorem repaired_permission_separates_primitive_impossibility_witness
    {World : Type u} {OldProfile : Type v} {NewProfile : Type w} {Target : Type u}
    (oldProfile : World → OldProfile)
    (newProfile : World → NewProfile)
    (target : World → Target)
    (hImpossible : PrimitiveImpossibility oldProfile target)
    (hFactor : ∃ F : NewProfile → Target, ∀ w : World, F (newProfile w) = target w) :
    ∃ a b : World,
      oldProfile a = oldProfile b ∧
      target a ≠ target b ∧
      newProfile a ≠ newProfile b := by
  rcases hImpossible with ⟨a, b, hOld, hTarget⟩
  refine ⟨a, b, hOld, hTarget, ?_⟩
  intro hNew
  rcases hFactor with ⟨F, hF⟩
  have hFa : target a = F (newProfile a) := (hF a).symm
  have hFb : target b = F (newProfile b) := (hF b).symm
  have hEqTarget : target a = target b := by rw [hFa, hFb, hNew]
  exact hTarget hEqTarget

/-- A fiber-respecting profile preserves collisions and cannot repair primitive impossibility. -/
theorem fiber_respecting_profile_cannot_repair_primitive_impossibility
    {World : Type u} {OldProfile : Type v} {NewProfile : Type w} {Target : Type u}
    (oldProfile : World → OldProfile)
    (newProfile : World → NewProfile)
    (target : World → Target)
    (hRespects : ∀ a b : World, oldProfile a = oldProfile b → newProfile a = newProfile b)
    (hImpossible : PrimitiveImpossibility oldProfile target) :
    ¬ (∃ F : NewProfile → Target, ∀ w : World, F (newProfile w) = target w) := by
  intro hFactor
  rcases hImpossible with ⟨a, b, hOld, hTarget⟩
  have hNew := hRespects a b hOld
  rcases hFactor with ⟨F, hF⟩
  have hFa : target a = F (newProfile a) := (hF a).symm
  have hFb : target b = F (newProfile b) := (hF b).symm
  have hEqTarget : target a = target b := by rw [hFa, hFb, hNew]
  exact hTarget hEqTarget

end CodaQ

