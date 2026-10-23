/-!
Finite proofs for WDP Paper 000.
-/

theorem no_factor_through_common_view {H V S : Type} (view : H → V) (answer : H → S)
    (h1 h2 : H) (sameView : view h1 = view h2) (differentAnswer : answer h1 ≠ answer h2) :
    ¬ ∃ auditor : V → S, ∀ h, auditor (view h) = answer h := by
  intro ⟨auditor, agrees⟩
  have leftEq := agrees h1
  have rightEq := agrees h2
  rw [sameView] at leftEq
  exact differentAnswer (by rw [← leftEq, rightEq])

theorem separation_not_on_quotient {A Q S : Type} (q : A → Q) (f : A → S)
    (x y : A) (sameClass : q x = q y) (separated : f x ≠ f y) :
    ¬ ∃ g : Q → S, ∀ a, g (q a) = f a :=
  no_factor_through_common_view q f x y sameClass separated

theorem insufficient_history_view {H V S : Type} (pi : H → V) (sigma : H → S)
    (h1 h2 : H) (sameView : pi h1 = pi h2) (differentState : sigma h1 ≠ sigma h2) :
    ¬ ∃ auditor : V → S, ∀ h, auditor (pi h) = sigma h :=
  no_factor_through_common_view pi sigma h1 h2 sameView differentState

inductive AdmissionAct where
  | datum
  | form
  | inst
  deriving DecidableEq, Repr

def applyAct (hasForm hasInst : Bool) : AdmissionAct → Bool × Bool
  | .datum => (hasForm, hasInst)
  | .form => (true, hasInst)
  | .inst => if hasForm then (hasForm, true) else (hasForm, hasInst)

def separates (hasForm hasInst : Bool) : Bool := hasForm && hasInst

theorem single_admission_does_not_separate (act : AdmissionAct) :
    separates (applyAct false false act).1 (applyAct false false act).2 = false := by
  cases act <;> rfl

theorem form_then_instance_separates :
    let afterForm := applyAct false false .form
    let afterInst := applyAct afterForm.1 afterForm.2 .inst
    separates afterInst.1 afterInst.2 = true := by
  rfl

def maxPairRounds (n : Nat) : Nat := n * (n - 1) / 2

theorem hits_within (f : Nat → Nat)
    (hdrop : ∀ k, 0 < f k → f (k + 1) + 1 ≤ f k)
    (hstay : ∀ k, f k = 0 → f (k + 1) = 0) : f (f 0) = 0 := by
  have hle : ∀ t, t ≤ f 0 → f t + t ≤ f 0 := by
    intro t
    induction t with
    | zero =>
      intro _
      omega
    | succ t ih =>
      intro ht
      have ht' : t ≤ f 0 := by omega
      have ih' := ih ht'
      by_cases h0 : f t = 0
      · have hnext := hstay t h0
        omega
      · have hpos : 0 < f t := by omega
        have hstep := hdrop t hpos
        omega
  have hfuel := hle (f 0) (Nat.le_refl _)
  omega

theorem stays_zero (f : Nat → Nat) (hstay : ∀ k, f k = 0 → f (k + 1) = 0)
    (start : Nat) (hstart : f start = 0) (t : Nat) : f (start + t) = 0 := by
  induction t with
  | zero => simpa using hstart
  | succ t ih =>
    have hnext := hstay (start + t) ih
    simpa [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm] using hnext

theorem hits_by_fuel (f : Nat → Nat) (fuel : Nat) (h0 : f 0 ≤ fuel)
    (hdrop : ∀ k, 0 < f k → f (k + 1) + 1 ≤ f k)
    (hstay : ∀ k, f k = 0 → f (k + 1) = 0) : f fuel = 0 := by
  have hzero := hits_within f hdrop hstay
  have hsplit : fuel = f 0 + (fuel - f 0) := (Nat.add_sub_of_le h0).symm
  rw [hsplit]
  exact stays_zero f hstay (f 0) hzero (fuel - f 0)

theorem pair_resolution_hits_zero (n : Nat) (f : Nat → Nat)
    (h0 : f 0 ≤ maxPairRounds n)
    (hdrop : ∀ k, 0 < f k → f (k + 1) + 1 ≤ f k)
    (hstay : ∀ k, f k = 0 → f (k + 1) = 0) :
    f (maxPairRounds n) = 0 :=
  hits_by_fuel f (maxPairRounds n) h0 hdrop hstay

theorem endpoint_distinct {A : Type} (R : A → A → Prop)
    (irrefl : ∀ x, ¬ R x x) {a b : A} (edge : R a b) : a ≠ b := by
  intro same
  subst same
  exact irrefl a edge

theorem two_point_support {A : Type} (R : A → A → Prop)
    (irrefl : ∀ x, ¬ R x x) {a b : A} (edge : R a b) :
    a ≠ b ∧ R a b :=
  ⟨endpoint_distinct R irrefl edge, edge⟩
