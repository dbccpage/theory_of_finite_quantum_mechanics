import Mathlib.Analysis.SpecialFunctions.Complex.Log
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Data.Set.Finite.Basic

/-!
# Torsion exclusion for the U(1) one-parameter group (cycle 006, QM_028 L3 sharpening)

Cycle 005 mechanized the `SO(2)=U(1)` angle addition but left "a finite torsion shadow has no such
ℝ-generator" **interpretive** (its C4). This cycle derives it: the kernel (period lattice) of the
one-parameter group `θ ↦ e^{iθ}` is the **infinite** set `2πℤ`, and the group is **nonconstant**
(value `−1` at `π`). A finite cyclic / torsion group has no infinite period lattice — so `U(1)` is a
genuine continuum, **not** a finite torsion shadow. This turns cycle-005 C4 from interpretive into
`[DERIVED]`.

These are facts about cycle-005's phase map `QM.U1Transport.phase θ = Complex.exp (↑θ * I)`, restated
self-contained (Mathlib only) for a clean check.

> **Routing (prompt §3a).** Representation-transport — this sharpens the L3 *continuity* object; it is
> **not** a verdict that `ℂ`/`U(1)` is forced. No authority minted (LGGR).
-/

namespace QM.U1Torsion

/-- **Torsion exclusion.** The kernel (period lattice) `{θ | e^{iθ} = 1}` of the U(1) one-parameter
group is **infinite** — it contains `2πℤ`. A finite cyclic / torsion group has no infinite period
lattice, so `U(1)` is a continuum, not torsion. -/
theorem kernel_infinite :
    {θ : ℝ | Complex.exp (↑θ * Complex.I) = 1}.Infinite := by
  apply Set.infinite_of_injective_forall_mem (f := fun n : ℤ => 2 * Real.pi * (n : ℝ))
  · -- the lattice map `n ↦ 2πn` is injective
    intro a b hab
    have h2 : (2 * Real.pi) ≠ 0 := by positivity
    exact_mod_cast mul_left_cancel₀ h2 hab
  · -- every lattice point is in the kernel: `e^{i·2πn} = 1`
    intro n
    show Complex.exp (↑(2 * Real.pi * (n : ℝ)) * Complex.I) = 1
    rw [show (↑(2 * Real.pi * (n : ℝ)) : ℂ) * Complex.I
          = (n : ℂ) * (2 * (Real.pi : ℂ) * Complex.I) by push_cast; ring]
    exact Complex.exp_int_mul_two_pi_mul_I n

/-- The generator value `e^{iπ} = −1`. -/
theorem exp_pi_eq_neg_one : Complex.exp (↑Real.pi * Complex.I) = -1 :=
  Complex.exp_pi_mul_I

/-- **Nonconstant.** The one-parameter group acts nontrivially: `e^{iπ} ≠ e^{i·0}` (`−1 ≠ 1`). Hence
its image has more than one point, so it is not the trivial group either. -/
theorem nonconstant :
    Complex.exp (↑Real.pi * Complex.I) ≠ Complex.exp (↑(0 : ℝ) * Complex.I) := by
  have h0 : Complex.exp (↑(0 : ℝ) * Complex.I) = 1 := by simp
  rw [exp_pi_eq_neg_one, h0]; norm_num

end QM.U1Torsion

#print axioms QM.U1Torsion.kernel_infinite
#print axioms QM.U1Torsion.exp_pi_eq_neg_one
#print axioms QM.U1Torsion.nonconstant
