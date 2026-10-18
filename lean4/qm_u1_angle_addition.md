import Mathlib.Analysis.Complex.Circle
import Mathlib.Analysis.Complex.Trigonometric

/-!
# SO(2) = U(1) angle addition — the U(1)-selector's continuity rung (cycle 005, QM_028)

QM_028 (The U(1)-Selector) forces the complex structure `J² = −I` at the two-level core **given**
continuous reversible pairing-preserving transport (the `L3` continuity input), which is what
separates `U(1)` from finite torsion shadows. QM_028's stated next test is to mechanize the
`SO(2) = U(1)` angle-addition over `ℝ` — the one-parameter group law.

This file does exactly that: the phase map `θ ↦ e^{iθ}` is a homomorphism `(ℝ,+) → (ℂˣ, ·)` lying on
the unit circle (`SO(2) ≅ U(1)`), and Mathlib's `Circle.exp : ℝ → Circle` packages the same
`ℝ → U(1)` one-parameter group.

> **Representation-transport routing (prompt §3a).** This is a representation-transport / composition
> residual, **not** a verdict that `ℂ`/`U(1)` is or is not forced. It supplies the L3 continuity
> object; the `L1 ∧ L2 ∧ L3 ⇒ ℂ/U(1)` forcing stays **conditional**, and continuity itself remains an
> imported postulate. No authority minted (LGGR).
-/

namespace QM.U1Transport

/-- The `U(1)` phase map `e^{iθ}`. -/
noncomputable def phase (θ : ℝ) : ℂ := Complex.exp (θ * Complex.I)

/-- **Angle addition — the one-parameter group law** `e^{iθ₁}·e^{iθ₂} = e^{i(θ₁+θ₂)}`.
`phase` is a homomorphism `(ℝ,+) → (ℂ, ·)`: the continuity content (`L3`) the U(1)-selector imports. -/
theorem phase_add (θ₁ θ₂ : ℝ) : phase θ₁ * phase θ₂ = phase (θ₁ + θ₂) := by
  unfold phase
  rw [← Complex.exp_add]
  congr 1
  push_cast; ring

/-- `phase 0 = 1` — the identity of the one-parameter group. -/
theorem phase_zero : phase 0 = 1 := by simp [phase]

/-- **Unit modulus** `‖e^{iθ}‖ = 1` — the phase lies on the unit circle (`SO(2)`). -/
theorem norm_phase (θ : ℝ) : ‖phase θ‖ = 1 := by
  unfold phase
  rw [Complex.norm_exp]
  simp

/-- **Mathlib packaging.** `Circle.exp : ℝ → Circle` is the same `ℝ → U(1)` one-parameter group; its
homomorphism law `Circle.exp_add` is the abstract `SO(2) = U(1)` angle addition. -/
theorem u1_one_parameter (x y : ℝ) : Circle.exp (x + y) = Circle.exp x * Circle.exp y :=
  Circle.exp_add x y

end QM.U1Transport

#print axioms QM.U1Transport.phase_add
#print axioms QM.U1Transport.phase_zero
#print axioms QM.U1Transport.norm_phase
#print axioms QM.U1Transport.u1_one_parameter
