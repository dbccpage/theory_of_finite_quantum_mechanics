import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Fin.VecNotation

/-!
# QM_000 Γ₂-declaration on a concrete 3-site loop (cycle 002)

QM_000 (Projection Obstruction) leaves `Γ₂` (the closure-failure mass) undefined — it carries
rate symbols instead of a `C²` norm (the Γ₂ FLAG in `03_finite_qm_ladder.md`). This file pins
`Γ₂` on the smallest nontrivial architecture: a 3-site loop (triangle) over `𝔽₂`.

- `C⁰ = C¹ = Fin 3 → 𝔽₂` (vertex gauges / edge sign-defects); `C² = 𝔽₂` (one face).
- `d₀` is the gauge coboundary; `d₁` is the face-holonomy (parity) coboundary.
- The cochain law `d₁ ∘ d₀ = 0` holds, so `Q¹ = C¹/im(d₀)` and `Γ₂([c]) = ‖d̄₁ c‖` are defined.

The defect `c = (1,0,0)` is **not** gauge-removable (`c ∉ im(d₀)`), so `Φ₁ > 0` by the cycle-001
identity `QM.CofiberPhi1.phi1_eq_quotient_norm`. Declaring the face (`d₁`) makes the closure charge
active (`Γ₂ > 0`, an OpenSignObstruction); on the hollow loop (`C² = 0`) the same class is a
ClosedSurvivor (`Γ₂ = 0`). Thus the open/closed split is fixed by the **declared** face structure
(cf. Paper 042 App. C.3).

All facts here are closed-form finite checks (`decide`): no `sorry`, no `native_decide`, no custom
axioms. No authority is minted (LGGR).
-/

namespace QM.QM000Gamma2

abbrev F2 := ZMod 2

/-- 0-cochains: vertex gauges on the 3-site loop. -/
abbrev C0 := Fin 3 → F2
/-- 1-cochains: edge sign-defects on edges `e₀=(0→1)`, `e₁=(1→2)`, `e₂=(0→2)`. -/
abbrev C1 := Fin 3 → F2

/-- Gauge coboundary `d₀ : C⁰ → C¹`, `(d₀ f)(i→j) = f j − f i`. -/
def d0 (f : C0) : C1 := ![f 1 - f 0, f 2 - f 1, f 2 - f 0]

/-- Face-holonomy coboundary `d₁ : C¹ → C² = 𝔽₂`, the oriented sum around the face. -/
def d1 (c : C1) : F2 := c 0 + c 1 - c 2

/-- **The cochain-complex law** `d₁ ∘ d₀ = 0`: closure is consistent, so `Q¹` and `Γ₂` are defined. -/
theorem d1_d0_zero : ∀ f : C0, d1 (d0 f) = 0 := by decide

/-- The projection/noise defect `c = (1,0,0)` on the loop. -/
def c : C1 := ![1, 0, 0]

/-- **`c` is not gauge-removable**: no admissible repair `f` has `d₀ f = c`, so `[c] ≠ 0` in
`Q¹ = C¹/im(d₀)`, hence `Φ₁([c]) > 0` (by the cycle-001 identity). -/
theorem c_not_in_range : ∀ f : C0, d0 f ≠ c := by decide

/-- **Filled loop: the closure charge is active** (`Γ₂([c]) > 0`): `d₁ c = 1 ≠ 0`, so `[c]` is an
`OpenSignObstruction`. (On the hollow loop, `C² = 0` gives `Γ₂ = 0` and `[c]` is a
`ClosedSurvivor`.) -/
theorem d1_c_active : d1 c = 1 := by decide

end QM.QM000Gamma2

#print axioms QM.QM000Gamma2.d1_d0_zero
#print axioms QM.QM000Gamma2.c_not_in_range
#print axioms QM.QM000Gamma2.d1_c_active
