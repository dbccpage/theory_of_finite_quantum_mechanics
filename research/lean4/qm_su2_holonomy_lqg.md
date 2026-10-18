import «holonomy_curvature»

/-!
# P-LQG-A — the SU(2) instance of the non-abelian holonomy (LQG gauge group)

The `Q-LQG-001` bridge's first concrete probe: instantiate the non-abelian holonomy
(`HolonomyCurvature.lean`) at the **LQG gauge group `SU(2)`**, using its canonical **finite
non-abelian subgroup** `Q₈ = {±1, ±i, ±j, ±k}` (the unit Lipschitz quaternions, `QuaternionGroup 2`)
— the decidable finite gauge shadow of `SU(2)`.

Two facts, the flat and the curved:

* **Flat ⇒ trivial Wilson loop** (`q8_flat_wilson_loop_trivial`): a pure-gauge `SU(2)`-connection has
  trivial holonomy around any closed loop. This is just the general `loop_pureGauge_holonomy_trivial`
  at `G = Q₈`; the law holds *verbatim* for the continuum `SU(2)` (it is true for **any** group).
* **Curvature ≠ 0** (`q8_curvature_wilson_nonflat`): the **plaquette** `a·b·a⁻¹·b⁻¹` of the two
  generators is the commutator `⁅a,b⁆ = -1 ≠ 1` — genuine non-abelian curvature, the finite shadow of
  LQG's `[∇_μ,∇_ν]V = R·V ≠ 0`. This is **impossible** for the abelian `U(1)` interference holonomy,
  where every plaquette commutes to `1`. So the SU(2) gauge group carries curvature that interference
  cannot — the structural step from QM-interference to GR-curvature on the same ladder.

Continuum `SU(2)`, the holonomy–flux algebra, area/volume, and the Hamiltonian constraint stay
Q-held (`Q-LQG-001`, A6). No authority minted (GTOC-5).
-/

namespace QM.SU2HolonomyLQG

open QM.HolonomyCurvature

/-- `Q₈`, the quaternion group — the canonical **finite non-abelian subgroup of `SU(2)`** (unit
Lipschitz quaternions `{±1,±i,±j,±k}`); the decidable finite gauge shadow of the LQG gauge group. -/
abbrev Q8 := QuaternionGroup 2

/-- The generator `i ∈ Q₈ ⊂ SU(2)` (order 4). -/
def qi : Q8 := QuaternionGroup.a 1
/-- The generator `j ∈ Q₈ ⊂ SU(2)`. -/
def qj : Q8 := QuaternionGroup.xa 0

/-- **Flat ⇒ trivial Wilson loop at the `SU(2)` gauge shadow.** A pure-gauge connection valued in
`Q₈ ⊂ SU(2)` has trivial holonomy around any closed loop — the `SU(2)` instance of the general
non-abelian `loop_pureGauge_holonomy_trivial`. (The same statement holds for continuum `SU(2)`: it is
true for any group.) -/
theorem q8_flat_wilson_loop_trivial (x0 : Q8) (l : List Q8) (hclosed : endptG x0 l = x0) :
    holoG x0 l = 1 :=
  loop_pureGauge_holonomy_trivial x0 l hclosed

/-- The **general** Wilson loop: the ordered product of the edge group elements around a loop. For
pure-gauge edges it is trivial; in general it is the curvature. -/
def wilson {G : Type*} [Group G] (edges : List G) : G := edges.prod

/-- A **plaquette** `[a, b, a⁻¹, b⁻¹]` has Wilson loop equal to the commutator `a·b·a⁻¹·b⁻¹` — the
discrete curvature 2-cell (the failure of the connection to be flat). -/
theorem wilson_plaquette {G : Type*} [Group G] (a b : G) :
    wilson [a, b, a⁻¹, b⁻¹] = a * b * a⁻¹ * b⁻¹ := by
  simp [wilson, List.prod_cons, List.prod_nil, mul_one, mul_assoc]

/-- The commutator of the two `Q₈ ⊂ SU(2)` generators is `-1 ≠ 1` (decidable, finite group). -/
theorem q8_commutator_ne_one : qi * qj * qi⁻¹ * qj⁻¹ ≠ 1 := by decide

/-- **Curvature at the `SU(2)` gauge group.** The plaquette of the two `Q₈ ⊂ SU(2)` generators has
**nontrivial** Wilson loop (`= ⁅i,j⁆ = -1 ≠ 1`): the connection is *not flat*. Genuine non-abelian
curvature — the finite shadow of `[∇,∇] = R ≠ 0` — which the abelian `U(1)` interference holonomy
**cannot** exhibit (every abelian plaquette commutes to `1`). -/
theorem q8_curvature_wilson_nonflat : wilson [qi, qj, qi⁻¹, qj⁻¹] ≠ 1 := by
  rw [wilson_plaquette]; exact q8_commutator_ne_one

#print axioms q8_flat_wilson_loop_trivial
#print axioms wilson_plaquette
#print axioms q8_curvature_wilson_nonflat

end QM.SU2HolonomyLQG
