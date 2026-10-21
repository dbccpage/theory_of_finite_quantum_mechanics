import OperationalTomography
import ComplexFieldSelection

/-! Conditional link to PR 138. The dimension family and its composite carrier
are supplied. This theorem replaces the tomography premise by explicit descent
and irreducibility premises; it does not derive those premises from difference.
AuthorityEffect: None.
-/
namespace OperationalFieldSelection
open OperationalTomography

variable {K V G : Type*} [Field K] [AddCommGroup V] [Module K V]

theorem selected_parameter (d : ℕ) (hd : 0 < d)
    (D : Calibrated K V
      (Fin (ComplexFieldSelection.K d 2) × Fin (ComplexFieldSelection.K d 2) → K))
    (dimension : Module.finrank K V = ComplexFieldSelection.K d 4)
    (ops : G → V →ₗ[K] V)
    (localOps : G → (Fin (ComplexFieldSelection.K d 2) ×
      Fin (ComplexFieldSelection.K d 2) → K) →ₗ[K]
      (Fin (ComplexFieldSelection.K d 2) × Fin (ComplexFieldSelection.K d 2) → K))
    (descent : ∀ g x, D.observe (ops g x) = localOps g (D.observe x))
    (irreducible : OperationalTomography.Irreducible ops) (nonzero : D.observe ≠ 0) : d = 2 := by
  apply ComplexFieldSelection.two_pair_selects d hd
  rw [← dimension]
  have injective := tomography_of_irreducible D.observe ops localOps descent irreducible nonzero
  simpa using product_dimension D injective

end OperationalFieldSelection
#print axioms OperationalFieldSelection.selected_parameter
