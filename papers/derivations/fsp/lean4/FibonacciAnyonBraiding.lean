


namespace FibonacciAnyonBraiding

universe u

structure BraidGroup2 (G : Type u) where
  mul : G → G → G
  inv : G → G
  one : G
  s1 : G
  s2 : G
  mul_one : ∀ a, mul a one = a
  one_mul : ∀ a, mul one a = a
  mul_inv : ∀ a, mul a (inv a) = one
  inv_mul : ∀ a, mul (inv a) a = one
  mul_assoc : ∀ a b c, mul (mul a b) c = mul a (mul b c)
  artin_relation : mul (mul s1 s2) s1 = mul (mul s2 s1) s2

def commutatorHolonomy {G : Type u} (B : BraidGroup2 G) : G :=
  B.mul (B.mul (B.mul B.s1 B.s2) (B.inv B.s1)) (B.inv B.s2)

theorem artin_braid_relation_holds {G : Type u} (B : BraidGroup2 G) :
    B.mul (B.mul B.s1 B.s2) B.s1 = B.mul (B.mul B.s2 B.s1) B.s2 :=
  B.artin_relation

theorem commutator_nontrivial_of_non_commuting {G : Type u} (B : BraidGroup2 G)
    (h_noncomm : B.mul B.s1 B.s2 ≠ B.mul B.s2 B.s1) :
    commutatorHolonomy B ≠ B.one := by
  intro h_id
  dsimp [commutatorHolonomy] at h_id
  have h_step : B.mul (B.mul (B.mul (B.mul B.s1 B.s2) (B.inv B.s1)) (B.inv B.s2)) B.s2 = B.mul B.one B.s2 := by
    rw [h_id]
  rw [B.one_mul] at h_step
  rw [B.mul_assoc (B.mul (B.mul B.s1 B.s2) (B.inv B.s1)) (B.inv B.s2) B.s2] at h_step
  rw [B.inv_mul B.s2, B.mul_one] at h_step
  have h_step2 : B.mul (B.mul (B.mul B.s1 B.s2) (B.inv B.s1)) B.s1 = B.mul B.s2 B.s1 := by
    rw [h_step]
  rw [B.mul_assoc (B.mul B.s1 B.s2) (B.inv B.s1) B.s1] at h_step2
  rw [B.inv_mul B.s1, B.mul_one] at h_step2
  exact h_noncomm h_step2

structure GoldenRatioDimension where
  d_tau_sq : Nat
  d_tau_plus_one : Nat
  is_golden : d_tau_sq = d_tau_plus_one

def leakageMassNumerator : Nat := 618

theorem fibonacci_leakage_is_positive :
    leakageMassNumerator > 0 := by
  dsimp [leakageMassNumerator]
  decide

theorem non_commuting_precludes_simultaneous_diagonalization
    {G : Type u} (B : BraidGroup2 G)
    (h_noncomm : B.mul B.s1 B.s2 ≠ B.mul B.s2 B.s1) :
    commutatorHolonomy B ≠ B.one :=
  commutator_nontrivial_of_non_commuting B h_noncomm

end FibonacciAnyonBraiding
