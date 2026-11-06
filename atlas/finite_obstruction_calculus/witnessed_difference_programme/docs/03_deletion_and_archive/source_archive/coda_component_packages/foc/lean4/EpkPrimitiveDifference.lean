import PrimitiveDifference

/-!
# Primitive-difference EPK/LGGR kernel

The EPK lesson used by Paper 993 is a quotient statement: a family of local
diagnostics may be invariant on the primitive zero-difference relation while a
global diagnostic is not.  In that case local dashboards factor through the
quotient, but the joint local-plus-global dashboard cannot.
-/

namespace FOC.EPK

open OmegaCore

universe u v w x y

variable {α : Type u} {β : Type v} {ι : Type w} {γ : Type x} {η : Type y}

/-- A bundle of local diagnostics is invariant exactly when every coordinate is
invariant. -/
theorem invariant_family_iff
    (P : PrimitiveDifference α β) (localObs : α → ι → γ) :
    P.InvariantCongruent localObs ↔
      ∀ i : ι, P.InvariantCongruent (fun a : α => localObs a i) := by
  constructor
  · intro h i a b hab
    exact congrFun (h a b hab) i
  · intro h a b hab
    funext i
    exact h i a b hab

/-- A local diagnostic family factors through the primitive quotient exactly
when each local coordinate is invariant on zero-difference classes. -/
theorem local_family_factor_exists_iff
    (P : PrimitiveDifference α β) (localObs : α → ι → γ) :
    (∃ F : P.ResidualQuotient → (ι → γ),
        ∀ a : α, F (P.classOf a) = localObs a)
      ↔ ∀ i : ι, P.InvariantCongruent (fun a : α => localObs a i) :=
  (PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
    P localObs).trans (invariant_family_iff P localObs)

/-- The exact positive gluing criterion: a joint local/global dashboard
descends through the primitive quotient exactly when every local coordinate and
the global diagnostic are invariant on zero-difference classes. -/
theorem joint_local_global_factor_exists_iff
    (P : PrimitiveDifference α β) (localObs : α → ι → γ) (global : α → η) :
    (∃ F : P.ResidualQuotient → ((ι → γ) × η),
        ∀ a : α, F (P.classOf a) = (localObs a, global a))
      ↔
        (∀ i : ι, P.InvariantCongruent (fun a : α => localObs a i)) ∧
          P.InvariantCongruent global := by
  constructor
  · intro hfactor
    have hpairInv :
        P.InvariantCongruent (fun a : α => (localObs a, global a)) :=
      (PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
        P (fun a : α => (localObs a, global a))).mp hfactor
    constructor
    · intro i a b hab
      exact congrFun (congrArg Prod.fst (hpairInv a b hab)) i
    · intro a b hab
      exact congrArg Prod.snd (hpairInv a b hab)
  · intro h
    have hlocalBundle : P.InvariantCongruent localObs :=
      (invariant_family_iff P localObs).mpr h.1
    have hpairInv :
        P.InvariantCongruent (fun a : α => (localObs a, global a)) := by
      intro a b hab
      exact Prod.ext (hlocalBundle a b hab) (h.2 a b hab)
    exact
      (PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
        P (fun a : α => (localObs a, global a))).mpr hpairInv

/-- Local Green != Global Red, abstract form: local coordinates can descend to
the quotient while a global diagnostic cannot be glued to them if two
zero-related states disagree globally. -/
theorem local_family_global_obstruction_of_witness
    (P : PrimitiveDifference α β) (localObs : α → ι → γ) (global : α → η)
    (hlocal : ∀ i : ι, P.InvariantCongruent (fun a : α => localObs a i))
    {a b : α} (hab : P.ZeroRel a b) (hglobal : global a ≠ global b) :
    (∃ F : P.ResidualQuotient → (ι → γ),
        ∀ a : α, F (P.classOf a) = localObs a) ∧
      ¬ (∃ F : P.ResidualQuotient → ((ι → γ) × η),
        ∀ a : α, F (P.classOf a) = (localObs a, global a)) := by
  have hbundle : P.InvariantCongruent localObs :=
    (invariant_family_iff P localObs).mpr hlocal
  constructor
  · exact
      (PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
        P localObs).mpr hbundle
  · intro hfactor
    have hpairInv :
        P.InvariantCongruent (fun a : α => (localObs a, global a)) :=
      (PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
        P (fun a : α => (localObs a, global a))).mp hfactor
    have hpair := hpairInv a b hab
    exact hglobal (congrArg Prod.snd hpair)

/-- If a zero-related pair disagrees globally, even an already descended local
family cannot be upgraded to a joint local/global factorization. -/
theorem local_factor_does_not_force_global_factor
    (P : PrimitiveDifference α β) (localObs : α → ι → γ) (global : α → η)
    (_hlocalFactor :
      ∃ F : P.ResidualQuotient → (ι → γ),
        ∀ a : α, F (P.classOf a) = localObs a)
    {a b : α} (hab : P.ZeroRel a b) (hglobal : global a ≠ global b) :
    ¬ (∃ F : P.ResidualQuotient → ((ι → γ) × η),
        ∀ a : α, F (P.classOf a) = (localObs a, global a)) := by
  intro hfactor
  have hpairInv :
      P.InvariantCongruent (fun a : α => (localObs a, global a)) :=
    (PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
      P (fun a : α => (localObs a, global a))).mp hfactor
  have hpair := hpairInv a b hab
  exact hglobal (congrArg Prod.snd hpair)

/-! ## Minimal finite LGGR witness -/

inductive MinimalTrace where
  | allGreen
  | localGreenGlobalRed
  deriving DecidableEq

inductive LocalProbe where
  | left
  | right
  deriving DecidableEq

def localVerdict (_t : MinimalTrace) (_p : LocalProbe) : Bool :=
  true

def globalVerdict : MinimalTrace → Bool
  | .allGreen => true
  | .localGreenGlobalRed => false

def localDashboardDifference : PrimitiveDifference MinimalTrace Bool where
  δ := fun _ _ => true
  Zero := fun b => b = true
  zero_refl := by intro t; rfl
  zero_symm := by intro t u htu; rfl
  zero_trans := by intro t u v htu huv; rfl

theorem minimal_traces_are_locally_zero_related :
    localDashboardDifference.ZeroRel
      MinimalTrace.allGreen MinimalTrace.localGreenGlobalRed := by
  rfl

theorem minimal_local_family_factors :
    ∃ F : localDashboardDifference.ResidualQuotient → (LocalProbe → Bool),
      ∀ t : MinimalTrace,
        F (localDashboardDifference.classOf t) = localVerdict t := by
  apply (local_family_factor_exists_iff
    localDashboardDifference localVerdict).mpr
  intro i t u htu
  rfl

theorem minimal_global_verdict_no_factor :
    ¬ (∃ F : localDashboardDifference.ResidualQuotient → Bool,
        ∀ t : MinimalTrace,
          F (localDashboardDifference.classOf t) = globalVerdict t) := by
  exact
    PrimitiveDifference.invariantFactor_no_factor_of_zeroRel_ne
      localDashboardDifference globalVerdict
      minimal_traces_are_locally_zero_related
      (by decide)

theorem minimal_joint_local_global_no_factor :
    ¬ (∃ F :
          localDashboardDifference.ResidualQuotient →
            ((LocalProbe → Bool) × Bool),
        ∀ t : MinimalTrace,
          F (localDashboardDifference.classOf t) =
            (localVerdict t, globalVerdict t)) := by
  exact
    (local_family_global_obstruction_of_witness
      localDashboardDifference localVerdict globalVerdict
      (by intro i t u htu; rfl)
      minimal_traces_are_locally_zero_related
      (by decide)).2

#print axioms FOC.EPK.invariant_family_iff
#print axioms FOC.EPK.local_family_factor_exists_iff
#print axioms FOC.EPK.joint_local_global_factor_exists_iff
#print axioms FOC.EPK.local_family_global_obstruction_of_witness
#print axioms FOC.EPK.local_factor_does_not_force_global_factor
#print axioms FOC.EPK.minimal_traces_are_locally_zero_related
#print axioms FOC.EPK.minimal_local_family_factors
#print axioms FOC.EPK.minimal_global_verdict_no_factor
#print axioms FOC.EPK.minimal_joint_local_global_no_factor

end FOC.EPK
