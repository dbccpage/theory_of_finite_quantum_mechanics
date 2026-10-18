/-
  H002 -- deterministic report dynamics. AuthorityEffect: None.
  Candidate only. Not PROVEN. Kind: LIFT RUNG.

  Claim identifier: HW-H002
  Source-paper contact: J011 trunk (E007 ambient dynamics, E011
  fiber congruence, E012 unique descended dynamics, E018 descent
  failure). QM_121 rung "report dynamics".

  Target proposition
    A report map tau : Q -> Q pushes weight vectors forward, and the
    pushforward preserves total mass (finite Fubini, proved in full
    generality). tau descends from ambient T : X -> X only under the
    fiber law; the E018 model is re-exported as the countermodel.

  Imports added at this rung
    The dynamics tau itself (declared data). Nothing else new: mass
    carrier from H001, enumeration from H000.

  Theorem or counterexample
    pushforward_mass: total mass is preserved by pushforward along
    any tau (general theorem, not a fixture check).
    descent_failure_replay: the trunk's E018 model has no descended
    report dynamics -- the countermodel demanded by the work order.

  Nonclaim boundary
    No claim that report dynamics is reversible (H003), linear
    (H004), or continuous (H016). No claim that a selected projected
    map is descended dynamics without the fiber law (E013/E021
    nonconflation stands).

  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
-/

import HWKernel
import Core
import E011_fiber_dynamics_congruence
import E012_unique_descended_dynamics
import E018_descent_failure_without_escape

namespace FableHilbertWalk20260819.H002

open FableHilbertWalk20260819.HWKernel
open GrokPdNight20260814.Core

/-- Pushforward of a weight vector along a report map, fiberwise. -/
def pushforward {X Q : Type} [DecidableEq Q] (E : Enum X)
    (τ : X → Q) (w : X → Int) : Q → Int :=
  fun q => rsum intPack ((E.elems.filter (fun x => τ x == q)).map w)

/-- Total mass is preserved by pushforward along ANY map: the
    general finite Fubini theorem, not a fixture check. -/
theorem pushforward_mass {X Q : Type} [DecidableEq Q]
    (EX : Enum X) (EQ : Enum Q) (τ : X → Q) (w : X → Int) :
    rsum intPack (EQ.elems.map (pushforward EX τ w)) =
      rsum intPack (EX.elems.map w) :=
  rsum_fiber_partition intPack EQ τ w EX.elems

#print axioms pushforward_mass

/-! ## Descent refusal: tau descends from ambient T only under the
    fiber law. The trunk's E018 model is the countermodel. -/

open GrokPdNight20260814.E011
  (FiberDynamicsCongruent fiber_dynamics_congruent_iff)
open GrokPdNight20260814.E012 (AgreesOnImage)
open GrokPdNight20260814.E018 (fstBool fixDyn)

/-- Replay: the E018 dynamics fixes the section, yet no descended
    report map exists. Selected-representative checks cannot certify
    descent. Direct reuse of the trunk theorem, no new proof. -/
theorem descent_failure_replay :
    ¬ ∃ Tbar : Bool → Bool, AgreesOnImage fstBool fixDyn Tbar :=
  GrokPdNight20260814.E018.no_tbar

#print axioms descent_failure_replay

theorem descent_congruence_gate :
    ¬ FiberDynamicsCongruent fstBool fixDyn :=
  GrokPdNight20260814.E018.not_congruent

#print axioms descent_congruence_gate

/-! ## G6 descent-witness mutation: strip the fiber-splitting flip
    from the E018 dynamics and descent is RESTORED. Together with
    descent_failure_replay this makes the descent witness
    mutation-sensitive, as gate G6 requires. -/

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

/-- H002 punchline: mass conservation is general; descent is gated
    by the fiber law, with the trunk countermodel re-exported. -/
theorem report_dynamics :
    (∀ (τ : Bool × Bool → Bool) (w : Bool × Bool → Int),
      rsum intPack (enumBool.elems.map (pushforward enumBoolProd τ w)) =
        rsum intPack (enumBoolProd.elems.map w)) ∧
      ¬ FiberDynamicsCongruent fstBool fixDyn ∧
      ¬ ∃ Tbar : Bool → Bool, AgreesOnImage fstBool fixDyn Tbar :=
  ⟨fun τ w => pushforward_mass enumBoolProd enumBool τ w,
    descent_congruence_gate, descent_failure_replay⟩

#print axioms report_dynamics

end FableHilbertWalk20260819.H002
