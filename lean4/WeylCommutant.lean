namespace FiniteQm.WeylCommutant
variable {K : Type} [Lean.Grind.Field K]

theorem off_diagonal_zero {n : Nat} (A : Fin n → Fin n → K)
    (eigenvalue : Fin n → K)
    (distinct : ∀ i j, eigenvalue i = eigenvalue j → i = j)
    (commutes : ∀ i j, eigenvalue i * A i j = A i j * eigenvalue j)
    (i j : Fin n) (hne : i ≠ j) : A i j = 0 := by
  have he : eigenvalue i ≠ eigenvalue j := fun h => hne (distinct i j h)
  have hc := commutes i j
  grind

theorem clock_shift_commutant_scalar {n : Nat} (A : Fin (n+1) → Fin (n+1) → K)
    (eigenvalue : Fin (n+1) → K)
    (distinct : ∀ i j, eigenvalue i = eigenvalue j → i = j)
    (clock : ∀ i j, eigenvalue i * A i j = A i j * eigenvalue j)
    (shift : ∀ i : Fin n, A i.succ i.succ = A i.castSucc i.castSucc) :
    ∀ i j, A i j = if i = j then A 0 0 else 0 := by
  have diag : ∀ i, A i i = A 0 0 := by
    apply Fin.induction
    · rfl
    · intro i hi
      exact (shift i).trans hi
  intro i j
  by_cases hij : i = j
  · subst j
    simp [diag]
  · simp [hij, off_diagonal_zero A eigenvalue distinct clock i j hij]

#print axioms off_diagonal_zero
#print axioms clock_shift_commutant_scalar
end FiniteQm.WeylCommutant


theorem falsification_degenerate_carrier : ¬ (1 = 0) := by
  decide

private def l5aProvenance : String :=
  "Origin: lean4/WeylCommutant.lean Claim: off_diagonal_zero AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
