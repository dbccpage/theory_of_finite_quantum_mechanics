import Mathlib.Data.List.Basic

/-! AuthorityEffect: None. Exact relation-indexed report/answer refinement,
fiber semantics, realized-image decoder uniqueness, and replay equality.
Local quotient construction and Rust storage/index/overflow correspondence are
separate obligations; no Cartesian preparation or physical interpretation. -/
namespace TFQM.JointCarrier

variable {X L R A H C : Type}

def profile (left : X → L) (right : X → R) (answer : X → A) (x : X) : (L × R) × A :=
  ((left x, right x), answer x)

theorem profile_equal (left : X → L) (right : X → R) (answer : X → A) (x y : X) :
    profile left right answer x = profile left right answer y ↔
      left x = left y ∧ right x = right y ∧ answer x = answer y := by
  simp only [profile, Prod.mk.injEq, and_assoc]

theorem profile_retains_left (left : X → L) (right : X → R) (answer : X → A) (x : X) :
    (profile left right answer x).1.1 = left x := rfl

theorem profile_retains_right (left : X → L) (right : X → R) (answer : X → A) (x : X) :
    (profile left right answer x).1.2 = right x := rfl

theorem profile_retains_answer (left : X → L) (right : X → R) (answer : X → A) (x : X) :
    (profile left right answer x).2 = answer x := rfl

theorem coarsest_refinement (left : X → L) (right : X → R) (answer : X → A)
    (h : X → H) (retains : ∀ x y, h x = h y →
      left x = left y ∧ right x = right y ∧ answer x = answer y) :
    ∀ x y, h x = h y → profile left right answer x = profile left right answer y := by
  intro x y eq
  exact (profile_equal left right answer x y).mpr (retains x y eq)

def fiber (report : X → L × R) (locals : L × R) (x : X) : Prop := report x = locals

theorem fiber_member (report : X → L × R) (locals : L × R) (x : X) :
    fiber report locals x ↔ report x = locals := Iff.rfl

theorem fiber_disjoint (report : X → L × R) (a b : L × R) (ne : a ≠ b) :
    ¬ ∃ x, fiber report a x ∧ fiber report b x := by
  rintro ⟨x, ha, hb⟩
  exact ne (ha.symm.trans hb)

theorem fiber_cover (report : X → L × R) (x : X) : fiber report (report x) x := rfl

def fiberAnswer (report : X → L × R) (answer : X → A) (locals : L × R) (a : A) : Prop :=
  ∃ x, fiber report locals x ∧ answer x = a

theorem fiber_answer (report : X → L × R) (answer : X → A) (locals : L × R) (a : A) :
    fiberAnswer report answer locals a ↔ ∃ x, report x = locals ∧ answer x = a := Iff.rfl

theorem empty_fiber_answers (report : X → L × R) (answer : X → A) (locals : L × R)
    (empty : ¬ ∃ x, fiber report locals x) : ¬ ∃ a, fiberAnswer report answer locals a := by
  rintro ⟨a, x, hx, _⟩
  exact empty ⟨x, hx⟩

theorem decoder_unique_on_image (report : X → L × R) (answer : X → A)
    (d e : L × R → A) (hd : ∀ x, d (report x) = answer x)
    (he : ∀ x, e (report x) = answer x) (r : L × R) (realized : ∃ x, report x = r) :
    d r = e r := by
  obtain ⟨x, rfl⟩ := realized
  exact (hd x).trans (he x).symm

theorem collision_refuses_decoder (report : X → L × R) (answer : X → A)
    (x y : X) (same : report x = report y) (different : answer x ≠ answer y) :
    ¬ ∃ d : L × R → A, ∀ z, d (report z) = answer z := by
  rintro ⟨d, hd⟩
  apply different
  exact (hd x).symm.trans ((congrArg d same).trans (hd y))

def replay [DecidableEq C] (expected supplied : C) : Bool := decide (expected = supplied)

theorem replay_success [DecidableEq C] (expected supplied : C) :
    replay expected supplied = true ↔ expected = supplied := by simp [replay]

theorem replay_refuses [DecidableEq C] (expected supplied : C) (ne : expected ≠ supplied) :
    replay expected supplied = false := by simp [replay, ne]

theorem budget_boundary (cost limit : Nat) : ¬ cost > limit ↔ cost ≤ limit := by omega

end TFQM.JointCarrier
