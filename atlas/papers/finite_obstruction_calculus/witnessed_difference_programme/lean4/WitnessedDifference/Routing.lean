import WitnessedDifference.Core

/-!
# Relative-status routing

`outsideProfile` records lack of applicability. It is a different constructor
from `refuted`, which is reachable only for an in-profile item.
-/

namespace WitnessedDifference.Routing

inductive RelativeStatus where
  | supported
  | refuted
  | outsideProfile
  | undetermined
  deriving DecidableEq, Repr

def route (inProfile contradicted supported : Bool) : RelativeStatus :=
  match inProfile, contradicted, supported with
  | false, _, _ => .outsideProfile
  | true, true, _ => .refuted
  | true, false, true => .supported
  | true, false, false => .undetermined

theorem outside_profile_ne_refuted :
    RelativeStatus.outsideProfile ≠ RelativeStatus.refuted := by
  decide

@[simp] theorem route_outside_profile
    (contradicted supported : Bool) :
    route false contradicted supported = .outsideProfile := by
  cases contradicted <;> cases supported <;> rfl

@[simp] theorem route_refuted (supported : Bool) :
    route true true supported = .refuted := by
  cases supported <;> rfl

theorem refuted_route_requires_profile
    {inProfile contradicted supported : Bool}
    (hroute : route inProfile contradicted supported = .refuted) :
    inProfile = true := by
  cases inProfile <;> simp [route] at hroute ⊢

end WitnessedDifference.Routing
