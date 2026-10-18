/-
Dimension-independent scalar commutant lemma over an arbitrary field.
The input clock equation is entrywise ZA=AZ with distinct diagonal entries.
The shift premise is the adjacent-diagonal consequence of AX=XA for the
canonical cyclic shift. Distinct eigenvalues and that premise are supplied;
this file does not construct roots, representations, or classify all irreps.
Lean.Grind.Field supplies the ordinary field laws from Lean core.
AuthorityEffect: None.
-/
namespace FiniteQm.WeylCommutant
variable {K : Type} [Lean.Grind.Field K]

/-- Entrywise form of commuting with a clock having distinct eigenvalues. -/
theorem off_diagonal_zero {n : Nat} (A : Fin n → Fin n → K)
    (eigenvalue : Fin n → K)
    (distinct : ∀ i j, eigenvalue i = eigenvalue j → i = j)
    (commutes : ∀ i j, eigenvalue i * A i j = A i j * eigenvalue j)
    (i j : Fin n) (hne : i ≠ j) : A i j = 0 := by
  have he : eigenvalue i ≠ eigenvalue j := fun h => hne (distinct i j h)
  have hc := commutes i j
  grind

/-- A distinct clock kills off-diagonals; the shift connects all diagonals. -/
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
