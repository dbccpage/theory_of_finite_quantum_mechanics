import Std

/- Exact Z2 cochain obstruction. No BF state sum, knotted worldsheet or
three-loop braiding model is constructed here. -/
namespace CampaignBfCocycleObstruction

def cocycle (a b c : Bool) : Bool := a && b && c

def coboundary (β : Bool → Bool → Bool) (a b c : Bool) : Bool :=
  Bool.xor (Bool.xor (Bool.xor (β b c) (β (Bool.xor a b) c))
    (β a (Bool.xor b c))) (β a b)

def Normalized (β : Bool → Bool → Bool) : Prop :=
  (∀ a, β false a = false) ∧ (∀ a, β a false = false)

def sign (b : Bool) : Int := if b then -1 else 1

def rephase (β : Bool → Bool → Bool) (a b c : Bool) : Bool :=
  Bool.xor (cocycle a b c) (coboundary β a b c)

theorem normalized_cocycle : ∀ a b : Bool,
    cocycle false a b = false ∧ cocycle a false b = false ∧
    cocycle a b false = false := by decide

theorem cocycle_identity : ∀ a b c d : Bool,
    Bool.xor (Bool.xor (Bool.xor (Bool.xor (cocycle b c d)
      (cocycle (Bool.xor a b) c d)) (cocycle a (Bool.xor b c) d))
      (cocycle a b (Bool.xor c d))) (cocycle a b c) = false := by decide

theorem normalized_coboundary_at_generator (β : Bool → Bool → Bool)
    (h : Normalized β) : coboundary β true true true = false := by
  cases e : β true true <;> simp [coboundary, h.1, h.2, e]

theorem not_a_normalized_coboundary (β : Bool → Bool → Bool)
    (h : Normalized β) : ¬ ∀ a b c, coboundary β a b c = cocycle a b c := by
  intro same
  have bad := same true true true
  rw [normalized_coboundary_at_generator β h] at bad
  cases bad

theorem generator_sign_survives_rephasing (β : Bool → Bool → Bool)
    (h : Normalized β) : sign (rephase β true true true) = -1 := by
  simp [rephase, normalized_coboundary_at_generator β h, cocycle, sign]

theorem no_normalized_rephasing_makes_all_signs_positive
    (β : Bool → Bool → Bool) (h : Normalized β) :
    ¬ ∀ a b c, sign (rephase β a b c) = 1 := by
  intro positive
  have bad := positive true true true
  rw [generator_sign_survives_rephasing β h] at bad
  contradiction

#print axioms normalized_cocycle
#print axioms cocycle_identity
#print axioms normalized_coboundary_at_generator
#print axioms not_a_normalized_coboundary
#print axioms generator_sign_survives_rephasing
#print axioms no_normalized_rephasing_makes_all_signs_positive
end CampaignBfCocycleObstruction
