import Mathlib

/-!
# P-LQG-B — the flux (conjugate momentum) and the holonomy–flux non-commutation

The `Q-LQG-001` bridge's **missing half**: the *flux* conjugate to the holonomy. On cylindrical
functions `G → 𝕜` (one edge with gauge group `G`):

* the **holonomy** operator is **multiplication** by a function `φ` of the group element (the
  configuration variable) — `holM φ`;
* the **flux** operator is **translation** by a group element `g` (the conjugate momentum — the
  discrete generator of motion on the group, the lattice shadow of the left-invariant vector field)
  — `fluxT g`.

The kinematical heart of the holonomy–flux algebra is that **they do not commute**:
`⁅fluxT g, holM φ⁆ f x = (φ(x·g) − φ(x))·f(x·g)` — multiplication by the *discrete derivative* of
the holonomy function, after translation. This is the discrete shadow of the canonical commutation
`[p, x] ≠ 0`. At the LQG gauge group (`Q₈ ⊂ SU(2)`, as in P-LQG-A) the commutator is provably
nonzero (`flux_hol_noncomm`).

This supplies the configuration↔momentum pairing the holonomy half lacked. It does **not** build the
area/volume operators or the Hamiltonian constraint — those stay Q-held (`Q-LQG-001`, A6). No
authority minted (GTOC-5).
-/

namespace QM.FluxHolonomyLQG

variable {G : Type*} [Group G] {𝕜 : Type*} [Field 𝕜]

/-- **Flux** = the conjugate-momentum operator: right-translation by `g` on cylindrical functions
`G → 𝕜`. The discrete shadow of the left-invariant vector field (the smeared triad). -/
def fluxT (g : G) : (G → 𝕜) →ₗ[𝕜] (G → 𝕜) where
  toFun f := fun x => f (x * g)
  map_add' f h := by funext x; simp only [Pi.add_apply]
  map_smul' c f := by funext x; simp only [Pi.smul_apply, RingHom.id_apply]

@[simp] theorem fluxT_apply (g : G) (f : G → 𝕜) (x : G) : fluxT g f x = f (x * g) := rfl

/-- **Holonomy** = the configuration operator: pointwise multiplication by `φ` (a function of the
holonomy / matrix element). -/
def holM (φ : G → 𝕜) : (G → 𝕜) →ₗ[𝕜] (G → 𝕜) where
  toFun f := fun x => φ x * f x
  map_add' f h := by funext x; simp only [Pi.add_apply, mul_add]
  map_smul' c f := by funext x; simp only [Pi.smul_apply, RingHom.id_apply, smul_eq_mul]; ring

@[simp] theorem holM_apply (φ f : G → 𝕜) (x : G) : holM φ f x = φ x * f x := rfl

/-- **Holonomy–flux commutator (discrete CCR).** Flux (translation) and holonomy (multiplication) do
not commute: the commutator is multiplication by the discrete derivative `φ(·g) − φ`, after
translation. `⁅fluxT g, holM φ⁆ f x = (φ(x·g) − φ(x))·f(x·g)`. -/
theorem flux_hol_commutator_apply (g : G) (φ f : G → 𝕜) (x : G) :
    (fluxT g ∘ₗ holM φ - holM φ ∘ₗ fluxT g) f x = (φ (x * g) - φ x) * f (x * g) := by
  simp only [LinearMap.sub_apply, LinearMap.comp_apply, Pi.sub_apply, fluxT_apply, holM_apply]
  ring

/-! ## The non-commutation at the LQG gauge group `Q₈ ⊂ SU(2)` -/

/-- `Q₈`, the quaternion group — the finite non-abelian subgroup of `SU(2)` (as in P-LQG-A). -/
abbrev Q8 := QuaternionGroup 2
/-- The generator `i ∈ Q₈ ⊂ SU(2)`. -/
def qi : Q8 := QuaternionGroup.a 1
/-- Indicator of the identity in `Q₈` — a basic cylindrical function. -/
def δ : Q8 → 𝕜 := fun x => if x = 1 then 1 else 0

/-- **The holonomy–flux algebra is non-trivial at `SU(2)`** (`Q₈ ⊂ SU(2)`): flux and holonomy do
**not** commute, `⁅fluxT qi, holM δ⁆ ≠ 0`. The discrete shadow of the canonical holonomy–flux
non-commutation — the conjugate-momentum (flux) structure the holonomy half lacked. -/
theorem flux_hol_noncomm :
    (fluxT qi ∘ₗ holM (δ : Q8 → 𝕜) - holM (δ : Q8 → 𝕜) ∘ₗ fluxT qi) ≠ 0 := by
  have hne : (qi⁻¹ : Q8) ≠ 1 := by decide
  intro h
  have key : (fluxT qi ∘ₗ holM (δ : Q8 → 𝕜) - holM (δ : Q8 → 𝕜) ∘ₗ fluxT qi) δ qi⁻¹ = 0 := by
    rw [h]; simp
  rw [flux_hol_commutator_apply] at key
  simp only [inv_mul_cancel] at key
  simp [δ, hne] at key

#print axioms flux_hol_commutator_apply
#print axioms flux_hol_noncomm

end QM.FluxHolonomyLQG
