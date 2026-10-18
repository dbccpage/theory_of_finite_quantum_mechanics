import «rdb_02_diagonal_density_trace»

/-!
GOMC-06: diagonal residual-density representability boundary.

The finite diagonal density layer is exactly the normalized, nonnegative,
trace-one face of residual-sector bookkeeping. A well-formed residual ledger
canonically produces a diagonal density certificate; conversely, any finite
diagonal density can be read as a well-formed residual ledger by taking its
diagonal entries as the residual masses.
-/

open scoped BigOperators

namespace QM

namespace GOMC06

noncomputable section

variable {S : Type*} [Fintype S]

def WellFormedResidualLedger (mass : S -> ℚ) : Prop :=
  (∀ s, 0 ≤ mass s) ∧ 0 < RDB01.residualTotalMass mass

def FiniteDiagonalDensity (diag : S -> ℚ) : Prop :=
  RDB02.DiagonalPSD diag ∧ RDB02.DiagonalTrace diag = 1

theorem wellFormedLedger_to_diagonalDensity
    (mass : S -> ℚ) (h : WellFormedResidualLedger mass) :
    FiniteDiagonalDensity (RDB02.residualDiagonalDensity mass) := by
  have hcert :=
    RDB02.residualDensityRepresentation_certificate mass h.1 h.2
  exact ⟨hcert.1, hcert.2.1⟩

theorem diagonalDensity_to_wellFormedLedger
    (diag : S -> ℚ) (hdiag : FiniteDiagonalDensity diag) :
    WellFormedResidualLedger diag := by
  constructor
  · exact hdiag.1
  · have hposTrace : 0 < RDB02.DiagonalTrace diag := by
      rw [hdiag.2]
      norm_num
    simpa [RDB01.residualTotalMass, RDB02.DiagonalTrace,
      PaperQF002.totalWeight] using hposTrace

theorem diagonalDensity_normalization_fixed
    (diag : S -> ℚ) (hdiag : FiniteDiagonalDensity diag) (s : S) :
    RDB02.residualDiagonalDensity diag s = diag s := by
  have hTotal : PaperQF002.totalWeight diag = 1 := by
    simpa [RDB02.DiagonalTrace, PaperQF002.totalWeight] using hdiag.2
  unfold RDB02.residualDiagonalDensity RDB01.residualWeight PaperQF002.directProb
  rw [hTotal]
  ring

theorem diagonalResidualDensity_boundary :
    (∀ mass : S -> ℚ,
      WellFormedResidualLedger mass ->
        FiniteDiagonalDensity (RDB02.residualDiagonalDensity mass)) ∧
      (∀ diag : S -> ℚ,
        FiniteDiagonalDensity diag -> WellFormedResidualLedger diag) := by
  exact ⟨wellFormedLedger_to_diagonalDensity,
    diagonalDensity_to_wellFormedLedger⟩

end

end GOMC06

end QM

#print axioms QM.GOMC06.wellFormedLedger_to_diagonalDensity
#print axioms QM.GOMC06.diagonalDensity_to_wellFormedLedger
#print axioms QM.GOMC06.diagonalDensity_normalization_fixed
#print axioms QM.GOMC06.diagonalResidualDensity_boundary
