import Mathlib

/-!
# GR-2 — the Bianchi identity as the cochain `d ∘ d = 0` shadow

The contracted second Bianchi identity `∇^μ G_μν = 0` (the Einstein tensor is divergence-free) is
the geometric shadow of the defining cochain-complex identity `d ∘ d = 0` — *"the boundary of a
boundary is empty"*. This file mechanizes that identity on the simplest 2-complex carrying a genuine
`d₁`: the oriented filled triangle (2-simplex) `{0,1,2}`, with vertices `C⁰`, edges `01,02,12` `C¹`,
and one face `012` `C²`.

`bianchi_dd_zero` proves `d₁ ∘ d₀ = 0`; hence `im d₀ ⊆ ker d₁` (`im_d0_subset_ker_d1`), so the
curvature class `H¹ = ker d₁ / im d₀` is well-defined — gauge (a coboundary) is always closed, and
curvature lives in `H¹`. This is **GR-2** of the GR paper series (after GR-1 = curvature =
non-abelian holonomy, `SU2HolonomyLQG.lean`).

Scope (honest): the filled triangle is contractible, so here `H¹ = 0`; `d∘d=0` is an **identity**,
true on every complex, *not* a cohomology computation — it is the Bianchi shadow, not the graph
first Betti number `b₁ = E − V + C` (that is the 1-skeleton, a separate finrank computation,
PL-QM030-1). A finite cochain identity on a toy carrier — the forced geometric shadow of Bianchi,
NOT the continuum Einstein tensor or its dynamics (Q-held). No authority minted (GTOC-5).
-/

namespace QM.BianchiDdZero

variable {𝕜 : Type*} [CommRing 𝕜]

/-- `d₀ : C⁰ → C¹` on the triangle `{0,1,2}`: vertices `Fin 3 → 𝕜`, edges `01,02,12` indexed by
`Fin 3`, with `(d₀ f)(ij) = f j − f i`. -/
def d0 (f : Fin 3 → 𝕜) : Fin 3 → 𝕜
  | 0 => f 1 - f 0   -- edge 01
  | 1 => f 2 - f 0   -- edge 02
  | 2 => f 2 - f 1   -- edge 12

/-- `d₁ : C¹ → C²` on the triangle: the oriented face boundary `∂{012} = 01 − 02 + 12`, so
`(d₁ g) = g(01) − g(02) + g(12)`. -/
def d1 (g : Fin 3 → 𝕜) : 𝕜 := g 0 - g 1 + g 2

/-- **Bianchi = `d ∘ d = 0`.** The oriented face-boundary alternating sum of a coboundary
telescopes to zero: `d₁ (d₀ f) = (f₂−f₁) − (f₂−f₀) + (f₁−f₀) = 0`. The finite shadow of the
contracted second Bianchi identity `∇^μ G_μν = 0` (curvature's covariant exterior derivative
vanishes). -/
theorem bianchi_dd_zero (f : Fin 3 → 𝕜) : d1 (d0 f) = 0 := by
  simp only [d1, d0]; ring

/-- Hence `im d₀ ⊆ ker d₁`: every coboundary (pure-gauge 1-cochain) is closed, so the curvature
class `H¹ = ker d₁ / im d₀` is well-defined — gauge carries no curvature, curvature lives in `H¹`. -/
theorem im_d0_subset_ker_d1 (g : Fin 3 → 𝕜) (hg : ∃ f, d0 f = g) : d1 g = 0 := by
  obtain ⟨f, rfl⟩ := hg; exact bianchi_dd_zero f

#print axioms bianchi_dd_zero
#print axioms im_d0_subset_ker_d1

end QM.BianchiDdZero
