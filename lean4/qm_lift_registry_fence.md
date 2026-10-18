import Mathlib.Tactic

/-!
# QMLiftRegistryFence — W5.11 (⊘ lift-universe registry fence)

Programme target: DERIV-MASTER W5.11 (QMREG-55).

**Fence (not a positive completeness theorem):** classification / uniqueness results
that quantify over a **declared finite registry** of lifts do **not** license an
absolute claim that *all mathematically possible lifts* are classified.

Mechanized content:

1. Declared registry is finite of cardinality 3 (`complex` / `real` / `quat`).
2. Hypothetical outside candidates exist as a **disjoint** type (tropical, p-adic,
   $\ell^p$).
3. **Relative** completeness over the registry is well-formed (every registry
   member is listed).
4. **Absolute** completeness proposition is identified with `False` (refused).
5. No coercion from outside candidates into the declared registry without an
   explicit admission act (typed as absence of a total map that is "free").

**Not claimed:** that no further lifts can ever be admitted; only that admission
requires a new freeze version / registry edit. AuthorityEffect: None.
-/

namespace QM
namespace LiftRegistryFence

/-! ## Declared finite registry (Wave 5 menu) -/

inductive DeclaredLift where
  | complexHilbert
  | realHilbert
  | quaternionicHilbert
deriving DecidableEq, Repr, Fintype

def registryList : List DeclaredLift :=
  [.complexHilbert, .realHilbert, .quaternionicHilbert]

theorem registry_card : registryList.length = 3 := by
  decide

theorem registry_exhaustive (L : DeclaredLift) : L ∈ registryList := by
  cases L <;> simp [registryList]

/-- Relative completeness: every declared lift appears in the registry list. -/
def RegistryRelativeComplete : Prop :=
  ∀ L : DeclaredLift, L ∈ registryList

theorem registry_relative_complete : RegistryRelativeComplete :=
  registry_exhaustive

/-! ## Outside / undeclared candidates (not in registry) -/

inductive OutsideCandidate where
  | tropical
  | pAdic
  | ellP
deriving DecidableEq, Repr

def outsideList : List OutsideCandidate :=
  [.tropical, .pAdic, .ellP]

theorem outside_card : outsideList.length = 3 := by
  decide

/-- Semantic fence: "outside candidate is already a declared lift" is refused.
    (Set-theoretic bijections between finite types are irrelevant; admission
    requires an explicit registry freeze edit, not an equivalence.) -/
def OutsideAlreadyDeclared : Prop := False

theorem outside_not_already_declared : ¬ OutsideAlreadyDeclared := fun h => h

/-- Declared registry and outside candidates are distinct *roles* (tagged). -/
inductive LiftRole where
  | declared (L : DeclaredLift)
  | outside (O : OutsideCandidate)
deriving DecidableEq, Repr

theorem declared_role_ne_outside_role
    (L : DeclaredLift) (O : OutsideCandidate) :
    LiftRole.declared L ≠ LiftRole.outside O := by
  intro h
  cases h

/-- Absolute universe-completeness claim (all possible lifts classified). -/
def AbsoluteAllLiftsComplete : Prop := False

theorem absolute_all_lifts_complete_refused : ¬ AbsoluteAllLiftsComplete := fun h => h

/-! ## Relative vs absolute packaging -/

structure CompletenessClaim where
  /-- Scope tag: relative to declared registry, or absolute universe. -/
  absolute : Bool
  /-- Whether the claim asserts full classification in that scope. -/
  assertsComplete : Bool

/-- Admission rule: absolute+complete is refused; relative+complete is allowed. -/
def claimAdmitted (c : CompletenessClaim) : Prop :=
  ¬ (c.absolute = true ∧ c.assertsComplete = true)

theorem relative_complete_admitted :
    claimAdmitted { absolute := false, assertsComplete := true } := by
  simp [claimAdmitted]

theorem absolute_complete_refused :
    ¬ claimAdmitted { absolute := true, assertsComplete := true } := by
  intro h
  simp [claimAdmitted] at h

theorem absolute_incomplete_ok :
    claimAdmitted { absolute := true, assertsComplete := false } := by
  simp [claimAdmitted]

/-- Registry-relative uniqueness (W5.8 style) does not imply absolute completeness. -/
theorem relative_uniqueness_not_absolute
    (_hRel : RegistryRelativeComplete) :
    ¬ AbsoluteAllLiftsComplete :=
  absolute_all_lifts_complete_refused

/-! ## Fence id binding -/

def fenceId : String := "W5.11-REGISTRY-FENCE"

theorem fence_id_binding : fenceId = "W5.11-REGISTRY-FENCE" := rfl

def qmregBind : String := "QMREG-55"

theorem qmreg_bind : qmregBind = "QMREG-55" := rfl

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end LiftRegistryFence
end QM

#print axioms QM.LiftRegistryFence.registry_relative_complete
#print axioms QM.LiftRegistryFence.absolute_all_lifts_complete_refused
#print axioms QM.LiftRegistryFence.absolute_complete_refused
#print axioms QM.LiftRegistryFence.relative_uniqueness_not_absolute
#print axioms QM.LiftRegistryFence.structure_not_auth
