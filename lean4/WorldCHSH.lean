
import WorldPresentation



namespace OmegaWorld

structure CHSHSquareCertificate where
  chshSquare : Nat
  termSquareSum : Nat
  normSquareSum : Nat
  scalarSumBound : chshSquare <= 2 * termSquareSum
  cauchyBound : termSquareSum <= normSquareSum
  parallelogram : normSquareSum = 4

theorem chsh_square_le_eight (certificate : CHSHSquareCertificate) :
    certificate.chshSquare <= 8 := by
  calc
    certificate.chshSquare <= 2 * certificate.termSquareSum :=
      certificate.scalarSumBound
    _ <= 2 * certificate.normSquareSum :=
      Nat.mul_le_mul_left 2 certificate.cauchyBound
    _ = 8 := by rw [certificate.parallelogram]

#print axioms chsh_square_le_eight

end OmegaWorld

private def l5aProvenance : String :=
  "Origin: lean4/WorldCHSH.lean Claim: chsh_square_le_eight AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
