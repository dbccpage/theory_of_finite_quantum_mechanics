import Mathlib

/-!
# P-LQG-C — the area-operator finite shadow: discrete area spectrum + the area gap

The `Q-LQG-001` bridge's geometric observable. In LQG the **area** of a surface punctured by edges
carrying spin `j` has eigenvalues `∝ √(j(j+1))`, where `j(j+1)` is the `SU(2)` Casimir eigenvalue of
the flux `Ê·Ê` (P-LQG-B). The hallmark of LQG — *"quantum geometry is discrete"* — is that this
spectrum is a **discrete, strictly increasing sequence with a smallest positive quantum** (the area
gap), not a continuum.

This file mechanizes exactly that discreteness, with the spin label `j = n/2` ranging over the
**discrete set `ℕ`** (`n = 2j`) — the discrete-first source of the discreteness (we do not quantize a
continuum *into* discreteness; the label set is discrete by construction, and the spectrum inherits
it).

Imported (not re-derived here): the physical scale `8πγℓ_P²` (a units prefactor) and the Casimir
eigenvalue `Ê·Ê = j(j+1)` (`SU(2)` representation theory). The dynamics (Hamiltonian constraint)
stays Q-held (`Q-LQG-001`, A6). No authority minted (GTOC-5).
-/

namespace QM.AreaSpectrumLQG

/-- The LQG **area eigenvalue** for spin label `j = n/2` (`n : ℕ`): `√(j(j+1)) = √((n/2)(n/2+1))`
(in units of the imported scale `8πγℓ_P²`). The label `n = 2j` ranges over the discrete set `ℕ`. -/
noncomputable def area (n : ℕ) : ℝ := Real.sqrt (((n : ℝ) / 2) * ((n : ℝ) / 2 + 1))

/-- The trivial rep `j = 0` carries zero area. -/
theorem area_zero : area 0 = 0 := by simp [area]

/-- **Discreteness — the spectrum is strictly increasing in the spin label.** The area eigenvalues
form a strictly monotone sequence: distinct labels give distinct, ordered areas — a *discrete*
spectrum, not a continuum. -/
theorem area_strictMono : StrictMono area := by
  intro a b hab
  have hab' : (a : ℝ) < b := by exact_mod_cast hab
  apply Real.sqrt_lt_sqrt
  · positivity
  · nlinarith [hab', (Nat.cast_nonneg a : (0:ℝ) ≤ (a:ℝ)), (Nat.cast_nonneg b : (0:ℝ) ≤ (b:ℝ))]

/-- The area spectrum is **injective in the label** — the precise "discrete spectrum" statement. -/
theorem area_injective : Function.Injective area := area_strictMono.injective

/-- **The area gap is positive** — there is a smallest nonzero quantum of area. -/
theorem area_gap_pos : 0 < area 1 := by
  unfold area; apply Real.sqrt_pos.mpr; norm_num

/-- **The area gap, explicitly** `= √3 / 2` (in units `8πγℓ_P²`) — the smallest quantum of area
(`j = 1/2`). -/
theorem area_one_eq : area 1 = Real.sqrt 3 / 2 := by
  have h : area 1 = Real.sqrt (3 * (1 / 2) ^ 2) := by unfold area; congr 1; norm_num
  rw [h, Real.sqrt_mul (by norm_num : (0:ℝ) ≤ 3), Real.sqrt_sq (by norm_num : (0:ℝ) ≤ 1 / 2)]
  ring

/-- **The gap is the minimum nonzero area** — every nonzero spin label has area at least the gap. -/
theorem area_gap_min (n : ℕ) (hn : 1 ≤ n) : area 1 ≤ area n :=
  area_strictMono.monotone hn

#print axioms area_strictMono
#print axioms area_gap_pos
#print axioms area_one_eq
#print axioms area_gap_min

end QM.AreaSpectrumLQG
