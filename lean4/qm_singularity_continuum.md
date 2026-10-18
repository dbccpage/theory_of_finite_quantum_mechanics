import Mathlib

/-!
# GR-5 / GR-6 — singularity = refusal, and continuum = certified limit

The two edge rungs of the GR series, both **anti-noun-inflation** moves.

**GR-5 — the singularity is a refusal, not a thing.** A GR singularity is *geodesic incompleteness*:
a geodesic that cannot be extended past a finite affine parameter — "the boundary of the maximal
extension", not a point of spacetime. Here a geodesic is iterated transport `step : V → Option V`
(`none` at the boundary); the singularity is the `none` (a typed **Refusal**), which is never a
carrier vertex `some v`. There is no "point" at the singularity to transport to or through.

**GR-6 — the continuum is a certified limit, not a primitive.** The continuum is reached as a
*certified `Tendsto` limit* of finite shadows (with a convergence certificate), exactly as
`cross_Zn_to_U1_refinement` does for interference: as a loop is subdivided into `n` finer elements of
phase `θ/n`, the per-element holonomy `cos(θ/n) → 1`. The continuum stays **Q-held** until such a
certificate exists — never posited as primitive.

Firewall: finite/limit facts on toy carriers — the singularity-as-refusal and continuum-as-limit
shadows, NOT the continuum manifold, the singularity theorems' physics, or any dynamics (Q-held). No
authority minted (GTOC-5).
-/

namespace QM.SingularityContinuum

/-! ## GR-5 — singularity = refusal (geodesic incompleteness) -/

variable {V : Type*}

/-- A geodesic from `v0` under a transport step `step : V → Option V` (`none` = the boundary, no
continuation): `geo 0 = some v0`, `geo (n+1) = (geo n) >>= step`. -/
def geo (step : V → Option V) (v0 : V) : ℕ → Option V
  | 0 => some v0
  | n + 1 => (geo step v0 n).bind step

/-- **Refusal is absorbing.** Once a geodesic refuses (`none` — hits the boundary of the maximal
extension), it stays refused: you do not pass *through* a singularity. -/
theorem geo_none_absorbing (step : V → Option V) (v0 : V) (n : ℕ)
    (h : geo step v0 n = none) : geo step v0 (n + 1) = none := by
  simp [geo, h]

/-- **The singularity is a refusal, not a carrier object.** Where a geodesic is incomplete the value
is `none`, which is never `some v` — the singularity is a typed **Refusal** (geodesic-incompleteness),
NOT an element of the carrier `V`. There is no point "at" the singularity. -/
theorem singularity_not_a_point (step : V → Option V) (v0 : V) (n : ℕ)
    (hsing : geo step v0 n = none) : ∀ v : V, geo step v0 n ≠ some v := by
  intro v; rw [hsing]; simp

/-! ## GR-6 — continuum = certified limit of finite shadows -/

open Filter Topology

/-- **The continuum is a certified limit.** Subdividing a loop into `n` finer elements each carrying
phase `θ/n`, the per-element holonomy `cos(θ/n)` converges to the identity `1` (a certified `Tendsto`
limit). The continuum object is *reached* as a limit of finite shadows — not posited as primitive;
absent such a certificate it stays Q-held. Same pattern as `cross_Zn_to_U1_refinement`. -/
theorem subdivision_to_continuum (θ : ℝ) :
    Tendsto (fun n : ℕ => Real.cos (θ / n)) atTop (𝓝 1) := by
  have h0 : Tendsto (fun n : ℕ => θ / (n : ℝ)) atTop (𝓝 0) := by
    simpa using tendsto_const_div_atTop_nhds_zero_nat θ
  have hcos : Tendsto (fun n : ℕ => Real.cos (θ / n)) atTop (𝓝 (Real.cos 0)) :=
    (Real.continuous_cos.tendsto 0).comp h0
  simpa using hcos

#print axioms geo_none_absorbing
#print axioms singularity_not_a_point
#print axioms subdivision_to_continuum

end QM.SingularityContinuum
