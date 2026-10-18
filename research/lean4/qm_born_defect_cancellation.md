import Mathlib

/-!
LT-J — Born defect cancellation under trace cyclicity (Stage 1).

Paper: `09_…` (PO-D19b); `05_…` §3; `01_…` §3.

In any ring `M` carrying an additive trace `Tr : M →+ K` (to an additive
commutative group `K`) that is **cyclic** (`Tr (x*y) = Tr (y*x)`), the Born-coordinate
gauge-repair defect cancels:

  `- Tr (E (Aρ - ρA)) - Tr ((AE - EA) ρ) = 0`.

This encodes Born **invariance under gauge repair**, NOT a derivation of the Born
rule. Stage 2 (instantiating `Tr = Matrix.trace` on `Matrix (Fin 2) (Fin 2) ℂ`, where
cyclicity is `Matrix.trace_mul_comm`) is a direct consequence and is deferred. No
authority minted.
-/

namespace QM

/-- **Born defect cancellation (Stage 1).** Trace cyclicity makes the Born-coordinate
gauge-repair defect vanish. -/
theorem born_defect_cancels {M K : Type*} [Ring M] [AddCommGroup K]
    (Tr : M →+ K) (hcyc : ∀ x y : M, Tr (x * y) = Tr (y * x)) (E ρ A : M) :
    (- Tr (E * (A * ρ - ρ * A)) - Tr ((A * E - E * A) * ρ)) = 0 := by
  rw [mul_sub, sub_mul, map_sub, map_sub]
  simp only [mul_assoc]
  have key : Tr (E * (ρ * A)) = Tr (A * (E * ρ)) := by
    rw [← mul_assoc, hcyc (E * ρ) A]
  rw [key]
  abel

/-- **Born defect cancellation (Stage 2).** The concrete `Matrix (Fin 2) (Fin 2) ℂ`
instance: the trace is the additive hom `Matrix.trace` and cyclicity is
`Matrix.trace_mul_comm`. Born invariance under gauge repair on the M₂ carrier;
still NOT a Born derivation. -/
theorem born_defect_cancels_M2 (E ρ A : Matrix (Fin 2) (Fin 2) ℂ) :
    (- Matrix.trace (E * (A * ρ - ρ * A)) - Matrix.trace ((A * E - E * A) * ρ)) = 0 := by
  have h := born_defect_cancels
    (AddMonoidHom.mk' (Matrix.trace : Matrix (Fin 2) (Fin 2) ℂ → ℂ)
      (fun X Y => Matrix.trace_add X Y))
    (fun x y => Matrix.trace_mul_comm x y) E ρ A
  simpa using h

end QM

#print axioms QM.born_defect_cancels
#print axioms QM.born_defect_cancels_M2
