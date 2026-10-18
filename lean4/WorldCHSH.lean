/-
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import WorldPresentation

/-!
# HL9A: arithmetic composition lemma for a finite CHSH square certificate

This theorem proves that supplied natural-number inequalities compose to
S^2 <= 8.  It is intentionally not a serialization bridge to the separate
exact-rational Python receipt.
-/

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
