/-
  AuthorizationBoundary.

  A report projection cannot certify a validity condition that
  distinguishes points the report has identified.

  `valid` is supplied independently of `p`. "Self" means the
  decider receives only `p x` (and functions of it). An external
  authorization event is an added input, refinement, witness, or
  rule — not a magical knower.

  Finite experiment. Not "LLMs cannot self-authorize." Not T1.
  A011 remains an open audit/policy requirement; this file proves
  only the factorization obstruction.

  AuthorityEffect: None.
-/

namespace AuthorizationBoundary

def FactorsThrough {X M : Type} (p : X → M) (valid : X → Bool)
    (decide : M → Bool) : Prop :=
  ∀ x, decide (p x) = valid x

def FiberConstant {X M : Type} (p : X → M) (valid : X → Bool) : Prop :=
  ∀ x y, p x = p y → valid x = valid y

/-- If two points share a report but disagree on independently
defined validity, no report-only decider recovers validity. -/
theorem no_report_decision {X M : Type}
    (p : X → M) (valid : X → Bool)
    (h : ∃ x y : X, p x = p y ∧ valid x ≠ valid y) :
    ¬ ∃ decide : M → Bool, FactorsThrough p valid decide := by
  rintro ⟨decide, hd⟩
  rcases h with ⟨x, y, hp, hv⟩
  have : valid x = valid y :=
    (hd x).symm.trans ((congrArg decide hp).trans (hd y))
  exact hv this

/-- Positive counterpart: fiber-constant validity plus a section
yields a report-level decider. -/
def decideFromSection {X M : Type}
    (p : X → M) (s : M → X) (valid : X → Bool)
    (_hs : ∀ m, p (s m) = m) : M → Bool :=
  fun m => valid (s m)

theorem report_decision_if_fiber_constant {X M : Type}
    (p : X → M) (s : M → X) (valid : X → Bool)
    (hs : ∀ m, p (s m) = m)
    (hconst : FiberConstant p valid) :
    FactorsThrough p valid (decideFromSection p s valid hs) := by
  intro x
  change valid (s (p x)) = valid x
  exact hconst (s (p x)) x (hs (p x))

/-- External authorization: the decider may read an added input. -/
def withExtra {X M E : Type}
    (p : X → M) (extra : X → E) (k : M → E → Bool) (x : X) : Bool :=
  k (p x) (extra x)

/-! ## Negative model: Bool → Unit. The report erases the bit. -/

def pNeg : Bool → Unit := fun _ => ()
def validNeg : Bool → Bool := id

theorem negative_fiber :
    ∃ x y : Bool, pNeg x = pNeg y ∧ validNeg x ≠ validNeg y :=
  ⟨false, true, rfl, fun h => Bool.noConfusion h⟩

theorem negative_model :
    ¬ ∃ decide : Unit → Bool, FactorsThrough pNeg validNeg decide :=
  no_report_decision pNeg validNeg negative_fiber

/-! ## Positive model: identity projection retains the bit. -/

def pPos : Bool → Bool := id
def validPos : Bool → Bool := id
def sPos : Bool → Bool := id

theorem positive_fiber_constant : FiberConstant pPos validPos := by
  intro x y h
  exact h

theorem positive_model :
    FactorsThrough pPos validPos (decideFromSection pPos sPos validPos (fun _ => rfl)) :=
  report_decision_if_fiber_constant pPos sPos validPos (fun _ => rfl)
    positive_fiber_constant

/-- Extra input that retains the erased distinction recovers validity. -/
theorem extra_recovers_negative :
    ∀ x, withExtra pNeg id (fun _ e => e) x = validNeg x := by
  intro
  rfl

end AuthorizationBoundary

#print axioms AuthorizationBoundary.no_report_decision
#print axioms AuthorizationBoundary.report_decision_if_fiber_constant
#print axioms AuthorizationBoundary.negative_model
#print axioms AuthorizationBoundary.positive_model
#print axioms AuthorizationBoundary.extra_recovers_negative
