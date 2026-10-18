

namespace Superposition

structure DiscreteState2 where
  c0 : Int
  c1 : Int

def base_probabilities (ψ : DiscreteState2) : Int × Int :=
  (ψ.c0 * ψ.c0, ψ.c1 * ψ.c1)

def is_basis_state (ψ : DiscreteState2) : Prop :=
  ψ.c0 = 0 ∨ ψ.c1 = 0

def is_superposition (ψ : DiscreteState2) : Prop :=
  ψ.c0 ≠ 0 ∧ ψ.c1 ≠ 0

theorem superposition_not_basis (ψ : DiscreteState2) (h : is_superposition ψ) :
    ¬ is_basis_state ψ := by
  intro hb
  rcases hb with h0 | h1
  · exact h.1 h0
  · exact h.2 h1

def interference_capacity_sq (ψ : DiscreteState2) : Int :=
  4 * (ψ.c0 * ψ.c0) * (ψ.c1 * ψ.c1)

theorem basis_state_zero_interference (ψ : DiscreteState2) (h : is_basis_state ψ) :
    interference_capacity_sq ψ = 0 := by
  dsimp [interference_capacity_sq]
  rcases h with h0 | h1
  · rw [h0]
    simp
  · rw [h1]
    simp

theorem int_sq_pos_of_ne_zero {x : Int} (hx : x ≠ 0) : x * x > 0 := by
  have h_cases : x < 0 ∨ x > 0 := by omega
  rcases h_cases with hlt | hgt
  · have hpos : -x > 0 := by omega
    have h_sq : (-x) * (-x) > 0 := Int.mul_pos hpos hpos
    have h_eq : (-x) * (-x) = x * x := by simp [Int.neg_mul_neg]
    rw [h_eq] at h_sq
    exact h_sq
  · exact Int.mul_pos hgt hgt

theorem superposition_positive_interference (ψ : DiscreteState2) (h : is_superposition ψ) :
    interference_capacity_sq ψ > 0 := by
  dsimp [interference_capacity_sq]
  have h0_pos := int_sq_pos_of_ne_zero h.1
  have h1_pos := int_sq_pos_of_ne_zero h.2
  have h_prod1 : (4 : Int) * (ψ.c0 * ψ.c0) > 0 := Int.mul_pos (by decide) h0_pos
  exact Int.mul_pos h_prod1 h1_pos

def beam_splitter_prob0 (ψ : DiscreteState2) : Int :=
  (ψ.c0 + ψ.c1) * (ψ.c0 + ψ.c1)

def classical_prob_sum (ψ : DiscreteState2) : Int :=
  ψ.c0 * ψ.c0 + ψ.c1 * ψ.c1

def interference_cross_term (ψ : DiscreteState2) : Int :=
  2 * ψ.c0 * ψ.c1

theorem beam_splitter_interference_expansion (ψ : DiscreteState2) :
    beam_splitter_prob0 ψ = classical_prob_sum ψ + interference_cross_term ψ := by
  dsimp [beam_splitter_prob0, classical_prob_sum, interference_cross_term]
  have h1 : (ψ.c0 + ψ.c1) * (ψ.c0 + ψ.c1) = (ψ.c0 + ψ.c1) * ψ.c0 + (ψ.c0 + ψ.c1) * ψ.c1 :=
    Int.mul_add (ψ.c0 + ψ.c1) ψ.c0 ψ.c1
  have h2 : (ψ.c0 + ψ.c1) * ψ.c0 = ψ.c0 * ψ.c0 + ψ.c1 * ψ.c0 :=
    Int.add_mul ψ.c0 ψ.c1 ψ.c0
  have h3 : (ψ.c0 + ψ.c1) * ψ.c1 = ψ.c0 * ψ.c1 + ψ.c1 * ψ.c1 :=
    Int.add_mul ψ.c0 ψ.c1 ψ.c1
  rw [h1, h2, h3]
  have hcomm : ψ.c1 * ψ.c0 = ψ.c0 * ψ.c1 := Int.mul_comm ψ.c1 ψ.c0
  rw [hcomm]
  have h2mul : 2 * ψ.c0 * ψ.c1 = ψ.c0 * ψ.c1 + ψ.c0 * ψ.c1 := by
    have h_two : (2 : Int) * ψ.c0 = ψ.c0 + ψ.c0 := by omega
    rw [h_two]
    exact Int.add_mul ψ.c0 ψ.c0 ψ.c1
  rw [h2mul]
  omega

def P (x : Int) : Int := x * x

theorem P_add (x y : Int) : P (x + y) = P x + P y + x * y + y * x := by
  dsimp [P]
  have h1 : (x + y) * (x + y) = (x + y) * x + (x + y) * y := Int.mul_add (x + y) x y
  have h2 : (x + y) * x = x * x + y * x := Int.add_mul x y x
  have h3 : (x + y) * y = x * y + y * y := Int.add_mul x y y
  rw [h1, h2, h3]
  omega

def sorkin_i3 (a b c : Int) : Int :=
  P (a + b + c) - (P (a + b) + P (b + c) + P (c + a)) + (P a + P b + P c)

theorem sorkin_third_order_interference_vanishes (a b c : Int) :
    sorkin_i3 a b c = 0 := by
  dsimp [sorkin_i3]
  have h1 : P (a + b + c) = P ((a + b) + c) := rfl
  rw [h1, P_add (a + b) c]
  have h_ac : (a + b) * c = a * c + b * c := Int.add_mul a b c
  have h_ca : c * (a + b) = c * a + c * b := Int.mul_add c a b
  rw [h_ac, h_ca]
  rw [P_add b c, P_add c a]
  omega

def sorkin_i2 (a b : Int) : Int :=
  P (a + b) - (P a + P b)

theorem sorkin_second_order_interference (a b : Int) :
    sorkin_i2 a b = 2 * a * b := by
  dsimp [sorkin_i2]
  rw [P_add a b]
  have hcomm : b * a = a * b := Int.mul_comm b a
  rw [hcomm]
  have h2mul : 2 * a * b = a * b + a * b := by
    have h_two : (2 : Int) * a = a + a := by omega
    rw [h_two]
    exact Int.add_mul a a b
  rw [h2mul]
  omega

#print axioms superposition_not_basis
#print axioms basis_state_zero_interference
#print axioms superposition_positive_interference
#print axioms beam_splitter_interference_expansion
#print axioms sorkin_third_order_interference_vanishes
#print axioms sorkin_second_order_interference

end Superposition

private def l5aProvenance : String :=
  "Origin: lean4/Superposition.lean Claim: superposition_not_basis AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
