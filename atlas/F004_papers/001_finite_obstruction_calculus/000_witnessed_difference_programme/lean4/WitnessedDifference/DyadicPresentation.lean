/-!
# Finite dyadic refinement and character-index restriction

Core-only arithmetic laws for every natural level, without a native word cap.
Pairing below is a residue exponent, not a constructed complex character.
No topology, infinite dual, real completion or Haar integral is formalized.
-/
namespace WitnessedDifference.DyadicPresentation

def order : Nat → Nat
  | 0 => 1
  | n+1 => 2 * order n

theorem order_positive (n : Nat) : 0 < order n := by
  induction n with
  | zero => simp [order]
  | succ n ih => simp only [order]; omega

theorem inclusion_bound (N a : Nat) (h : a < N) : 2*a < 2*N := by omega

theorem inclusion_injective (a b : Nat) : 2*a = 2*b ↔ a=b := by omega

theorem inclusion_addition (N a b : Nat) :
    (2*a + 2*b) % (2*N) = 2*((a+b)%N) := by
  rw [← Nat.mul_add, Nat.mul_mod_mul_left]

theorem pairing_inclusion (N k m : Nat) :
    (k*(2*m)) % (2*N) = 2*((k*m)%N) := by
  rw [Nat.mul_left_comm k 2 m, Nat.mul_mod_mul_left]

theorem pairing_restriction (N k m : Nat) :
    ((k%N)*m)%N = (k*m)%N := by
  simp [Nat.mul_mod]

theorem restriction_bound (N k : Nat) (h : 0<N) : k%N < N := Nat.mod_lt k h

theorem restriction_composition (N k : Nat) : (k%(2*N))%N=k%N := by
  exact Nat.mod_mod_of_dvd k ⟨2, Nat.mul_comm 2 N⟩

theorem lower_extension_restricts (N a : Nat) (h : a<N) : a%N=a :=
  Nat.mod_eq_of_lt h

theorem upper_extension_restricts (N a : Nat) (h : a<N) : (a+N)%N=a := by
  rw [Nat.add_mod_right, Nat.mod_eq_of_lt h]

theorem extensions_in_carrier (N a : Nat) (h : a<N) :
    a<2*N ∧ a+N<2*N := by omega

theorem extensions_distinct (N a : Nat) (h : 0<N) : a≠a+N := by omega

theorem restriction_fiber (N a b : Nat) (ha : a<N) (hb : b<2*N) :
    b%N=a ↔ b=a ∨ b=a+N := by
  constructor
  · intro h
    by_cases small : b<N
    · rw [Nat.mod_eq_of_lt small] at h
      exact Or.inl h
    · have ge : N≤b := by omega
      have sub_lt : b-N<N := by omega
      rw [Nat.mod_eq_sub_mod ge, Nat.mod_eq_of_lt sub_lt] at h
      right
      omega
  · intro h
    rcases h with h | h
    · subst b
      exact lower_extension_restricts N a ha
    · subst b
      exact upper_extension_restricts N a ha

theorem tower_pairing (n k m : Nat) :
    (k*(2*m)) % order (n+1) = 2*((k*m)%order n) :=
  pairing_inclusion (order n) k m

theorem no_unique_adjacent_extension (n a : Nat) (h : a<order n) :
    ∃ b c, b<order (n+1) ∧ c<order (n+1) ∧ b≠c ∧
      b%order n=a ∧ c%order n=a := by
  refine ⟨a,a+order n,?_,?_,?_,?_,?_⟩
  · exact (extensions_in_carrier (order n) a h).1
  · exact (extensions_in_carrier (order n) a h).2
  · exact extensions_distinct (order n) a (order_positive n)
  · exact lower_extension_restricts (order n) a h
  · exact upper_extension_restricts (order n) a h

end WitnessedDifference.DyadicPresentation

#print axioms WitnessedDifference.DyadicPresentation.order_positive
#print axioms WitnessedDifference.DyadicPresentation.inclusion_bound
#print axioms WitnessedDifference.DyadicPresentation.inclusion_injective
#print axioms WitnessedDifference.DyadicPresentation.inclusion_addition
#print axioms WitnessedDifference.DyadicPresentation.pairing_inclusion
#print axioms WitnessedDifference.DyadicPresentation.pairing_restriction
#print axioms WitnessedDifference.DyadicPresentation.restriction_bound
#print axioms WitnessedDifference.DyadicPresentation.restriction_composition
#print axioms WitnessedDifference.DyadicPresentation.lower_extension_restricts
#print axioms WitnessedDifference.DyadicPresentation.upper_extension_restricts
#print axioms WitnessedDifference.DyadicPresentation.extensions_in_carrier
#print axioms WitnessedDifference.DyadicPresentation.extensions_distinct
#print axioms WitnessedDifference.DyadicPresentation.restriction_fiber
#print axioms WitnessedDifference.DyadicPresentation.tower_pairing
#print axioms WitnessedDifference.DyadicPresentation.no_unique_adjacent_extension
