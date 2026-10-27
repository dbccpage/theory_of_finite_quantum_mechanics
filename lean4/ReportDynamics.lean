






import HWKernel
import Core
import FiberDynamicsCongruence
import UniqueDescendedDynamics
import DescentFailureWithoutEscape

namespace HilbertWalk.ReportDynamics

open HilbertWalk.HWKernel
open ProjectionFiber.Core

def pushforward {X Q : Type} [DecidableEq Q] (E : Enum X)
    (τ : X → Q) (w : X → Int) : Q → Int :=
  fun q => rsum intPack ((E.elems.filter (fun x => τ x == q)).map w)

theorem pushforward_mass {X Q : Type} [DecidableEq Q]
    (EX : Enum X) (EQ : Enum Q) (τ : X → Q) (w : X → Int) :
    rsum intPack (EQ.elems.map (pushforward EX τ w)) =
      rsum intPack (EX.elems.map w) :=
  rsum_fiber_partition intPack EQ τ w EX.elems

#print axioms pushforward_mass


open ProjectionFiber.E011
  (FiberDynamicsCongruent fiber_dynamics_congruent_iff)
open ProjectionFiber.E012 (AgreesOnImage)
open ProjectionFiber.E018 (fstBool fixDyn)

theorem descent_failure_replay :
    ¬ ∃ Tbar : Bool → Bool, AgreesOnImage fstBool fixDyn Tbar :=
  ProjectionFiber.E018.no_tbar

#print axioms descent_failure_replay

theorem descent_congruence_gate :
    ¬ FiberDynamicsCongruent fstBool fixDyn :=
  ProjectionFiber.E018.not_congruent

#print axioms descent_congruence_gate


def idDyn : AmbientDynamics (Bool × Bool) Unit where
  T := id
  provenance := ()

theorem mutation_descent_restored :
    FiberDynamicsCongruent fstBool idDyn ∧
      ∃ Tbar : Bool → Bool, AgreesOnImage fstBool idDyn Tbar := by
  constructor
  · exact (fiber_dynamics_congruent_iff fstBool idDyn).mpr
      (fun _ _ h => h)
  · exact ⟨fun b => b, fun _ => rfl⟩

#print axioms mutation_descent_restored

theorem report_dynamics :
    (∀ (τ : Bool × Bool → Bool) (w : Bool × Bool → Int),
      rsum intPack (enumBool.elems.map (pushforward enumBoolProd τ w)) =
        rsum intPack (enumBoolProd.elems.map w)) ∧
      ¬ FiberDynamicsCongruent fstBool fixDyn ∧
      ¬ ∃ Tbar : Bool → Bool, AgreesOnImage fstBool fixDyn Tbar :=
  ⟨fun τ w => pushforward_mass enumBoolProd enumBool τ w,
    descent_congruence_gate, descent_failure_replay⟩

#print axioms report_dynamics

end HilbertWalk.ReportDynamics

private def l5aProvenance : String :=
  "Origin: lean4/ReportDynamics.lean Claim: pushforward_mass AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
