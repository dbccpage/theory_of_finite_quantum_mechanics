import OperationalTomography
import ComplexFieldSelection

/-! Conditional link to PR 138. The dimension family and its composite carrier
are supplied. The Schur-type reformulation uses explicit descent and irreducibility
premises; it does not derive those premises from difference.
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
    (irreducible : OperationalTomography.Irreducible ops) : d = 2 := by
  apply ComplexFieldSelection.two_pair_selects d hd
  rw [← dimension]
  haveI : NeZero (ComplexFieldSelection.K d 2) := ⟨by simp [ComplexFieldSelection.K]⟩
  have injective := calibrated_tomography D ops localOps descent irreducible
  simpa using product_dimension D injective

/-- Selects the supplied catalogue label. It does not identify the ambient
coefficient field K with the complex numbers or derive the catalogue itself. -/
theorem selected_carrier (c : ComplexFieldSelection.Carrier)
    (D : Calibrated K V
      (Fin (ComplexFieldSelection.K (ComplexFieldSelection.scalarDimension c) 2) ×
        Fin (ComplexFieldSelection.K (ComplexFieldSelection.scalarDimension c) 2) → K))
    (dimension : Module.finrank K V = ComplexFieldSelection.K (ComplexFieldSelection.scalarDimension c) 4)
    (ops : G → V →ₗ[K] V)
    (localOps : G → (Fin (ComplexFieldSelection.K (ComplexFieldSelection.scalarDimension c) 2) ×
      Fin (ComplexFieldSelection.K (ComplexFieldSelection.scalarDimension c) 2) → K) →ₗ[K]
      (Fin (ComplexFieldSelection.K (ComplexFieldSelection.scalarDimension c) 2) ×
      Fin (ComplexFieldSelection.K (ComplexFieldSelection.scalarDimension c) 2) → K))
    (descent : ∀ g x, D.observe (ops g x) = localOps g (D.observe x))
    (irreducible : OperationalTomography.Irreducible ops) : c = .complex := by
  have hd : 0 < ComplexFieldSelection.scalarDimension c := by cases c <;> decide
  have h := selected_parameter _ hd D dimension ops localOps descent irreducible
  cases c <;> simp_all [ComplexFieldSelection.scalarDimension]

abbrev ComplexPairIndex := Fin (ComplexFieldSelection.K 2 2) × Fin (ComplexFieldSelection.K 2 2)
abbrev ComplexPairCoordinates := ComplexPairIndex → ℚ

/-- An algebraic consistency witness for every headline hypothesis at d = 2.
The rational coordinate model is not claimed to be a complex quantum system. -/
theorem two_hypotheses_satisfiable :
    ∃ (D : Calibrated ℚ ComplexPairCoordinates ComplexPairCoordinates)
      (ops loc : ComplexPairIndex × ComplexPairIndex → ComplexPairCoordinates →ₗ[ℚ] ComplexPairCoordinates),
      (0 < (2 : ℕ)) ∧
      Module.finrank ℚ ComplexPairCoordinates = ComplexFieldSelection.K 2 4 ∧
      (∀ g x, D.observe (ops g x) = loc g (D.observe x)) ∧
      OperationalTomography.Irreducible ops := by
  refine ⟨identityCalibration, fun ij => matrixUnit ij.1 ij.2,
    fun ij => matrixUnit ij.1 ij.2, by decide, ?_, fun _ _ => rfl, matrix_units_irreducible⟩
  norm_num [ComplexPairCoordinates, ComplexPairIndex, ComplexFieldSelection.K, Nat.choose]

end OperationalFieldSelection
#print axioms OperationalFieldSelection.selected_parameter

#print axioms OperationalFieldSelection.selected_carrier
#print axioms OperationalFieldSelection.two_hypotheses_satisfiable
