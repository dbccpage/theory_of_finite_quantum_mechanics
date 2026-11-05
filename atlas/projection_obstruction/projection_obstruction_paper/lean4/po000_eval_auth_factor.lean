/-
  EvalAuthFactor.

  Fable's NC1 audit (2026-08-18) left this as Grok's assignment:
  the joint evaluation × authorization factorization. Not Lawvere.
  Not TOP-EXT. Not sealed 19L57G1.

  One residual / one report p. Two measurements:
    eval : X → Nat     (0 = exact; size is the leftover)
    valid : X → Bool   (independently supplied authorization)

  A proposer is any map out of p. Joint close is a single
  report-only map that recovers both exactness and valid.

  AuthorityEffect: None.
-/

namespace EvalAuthFactor

def Exact {X : Type} (eval : X → Nat) (x : X) : Bool :=
  decide (eval x = 0)

def JointClose {X M : Type}
    (p : X → M) (eval : X → Nat) (valid : X → Bool)
    (k : M → Bool × Bool) : Prop :=
  ∀ x, k (p x) = (Exact eval x, valid x)

/-- If authorization splits a report fiber, no proposer map
recovers both measurements. -/
theorem no_joint_close_auth_split {X M : Type}
    (p : X → M) (eval : X → Nat) (valid : X → Bool)
    (h : ∃ x y : X, p x = p y ∧ valid x ≠ valid y) :
    ¬ ∃ k : M → Bool × Bool, JointClose p eval valid k := by
  rintro ⟨k, hk⟩
  rcases h with ⟨x, y, hp, hv⟩
  have hx := hk x
  have hy := hk y
  have : valid x = valid y := by
    have : (Exact eval x, valid x) = (Exact eval y, valid y) :=
      hx.symm.trans ((congrArg k hp).trans hy)
    exact congrArg Prod.snd this
  exact hv this

/-- If exactness splits a report fiber, no proposer map
recovers both measurements. -/
theorem no_joint_close_eval_split {X M : Type}
    (p : X → M) (eval : X → Nat) (valid : X → Bool)
    (h : ∃ x y : X, p x = p y ∧ Exact eval x ≠ Exact eval y) :
    ¬ ∃ k : M → Bool × Bool, JointClose p eval valid k := by
  rintro ⟨k, hk⟩
  rcases h with ⟨x, y, hp, he⟩
  have hx := hk x
  have hy := hk y
  have : Exact eval x = Exact eval y := by
    have : (Exact eval x, valid x) = (Exact eval y, valid y) :=
      hx.symm.trans ((congrArg k hp).trans hy)
    exact congrArg Prod.fst this
  exact he this

/-! ## Model A: always-exact eval, hidden auth bit.

SOUND ⇏ AUTH. The proposer can report Φ = 0 and still not authorize. -/

def pA : Bool × Bool → Bool := Prod.fst
def evalA : Bool × Bool → Nat := fun _ => 0
def validA : Bool × Bool → Bool := Prod.snd

theorem modelA_eval_exact (x : Bool × Bool) : Exact evalA x = true := by
  simp [Exact, evalA]

theorem modelA_auth_splits :
    ∃ x y : Bool × Bool, pA x = pA y ∧ validA x ≠ validA y :=
  ⟨(false, false), (false, true), rfl, fun h => Bool.noConfusion h⟩

theorem modelA_no_joint_close :
    ¬ ∃ k : Bool → Bool × Bool, JointClose pA evalA validA k :=
  no_joint_close_auth_split pA evalA validA modelA_auth_splits

/-! ## Model B: everyone authorized, residual is the hidden bit.

AUTH ⇏ SOUND. A license does not zero the residual. -/

def pB : Bool × Bool → Bool := Prod.fst
def evalB : Bool × Bool → Nat := fun x => if x.2 then 0 else 1
def validB : Bool × Bool → Bool := fun _ => true

theorem modelB_eval_splits :
    ∃ x y : Bool × Bool, pB x = pB y ∧ Exact evalB x ≠ Exact evalB y :=
  ⟨(false, false), (false, true), rfl, fun h => by
    have : Exact evalB (false, false) = false := rfl
    have : Exact evalB (false, true) = true := rfl
    cases h⟩

theorem modelB_no_joint_close :
    ¬ ∃ k : Bool → Bool × Bool, JointClose pB evalB validB k :=
  no_joint_close_eval_split pB evalB validB modelB_eval_splits

/-! ## Model C: license lives in the report (n₂ / setAugLicense grain).

This *does* jointly close — because valid did not split.
That is evaluation of an operational field, not independent AUTH. -/

def pC : Bool → Bool := id
def evalC : Bool → Nat := fun _ => 0
def validC : Bool → Bool := id

def closeC (m : Bool) : Bool × Bool := (true, m)

theorem modelC_joint_close : JointClose pC evalC validC closeC := by
  intro x
  rfl

theorem license_in_report_is_fiber_constant {X M : Type}
    (p : X → M) (license : X → Bool)
    (k : M → Bool) (hk : ∀ x, k (p x) = license x) :
    ∀ x y, p x = p y → license x = license y := by
  intro x y hp
  exact (hk x).symm.trans ((congrArg k hp).trans (hk y))

/-- Extra input recovers Model A authorization without
pretending the residual moved. -/
def extraA : Bool × Bool → Bool := Prod.snd

theorem extra_recovers_A :
    ∀ x, extraA x = validA x := by
  intro
  rfl

end EvalAuthFactor

#print axioms EvalAuthFactor.no_joint_close_auth_split
#print axioms EvalAuthFactor.no_joint_close_eval_split
#print axioms EvalAuthFactor.modelA_no_joint_close
#print axioms EvalAuthFactor.modelB_no_joint_close
#print axioms EvalAuthFactor.modelC_joint_close
#print axioms EvalAuthFactor.license_in_report_is_fiber_constant
