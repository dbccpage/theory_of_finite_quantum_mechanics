import Mathlib.LinearAlgebra.Quotient.Basic
import Mathlib.LinearAlgebra.Pi
import Mathlib.Algebra.Module.Submodule.Range
import Mathlib.Algebra.Ring.Int.Defs

/-!
# A chain retraction cannot kill an old homology class

AuthorityEffect: None.  Scope: one degree of a chain complex of modules over a ring `R` (the three consecutive
modules `U --bd--> M --d--> L` with `d . bd = 0`), chain maps `i : C -> D` and `r : D -> C`, and the hypothesis
`r . i = id` on the middle module.  Sources: `chain_retraction_cannot_kill` (Paper.lean line 147, written for
fragments with explicit `sub`), `induced_homology_injective` (Homology.lean line 210, group-valued, Lean-core
`Lean.Grind` algebra) and `homology_kernel_trivial` (Paper001.lean line 460).  Re-proved here for
`R`-modules with Mathlib.  Scope notes:

* only the middle section law `r . i = id` and the boundary commutation `r . bd' = bd . r` are used, so the
  statement holds degree by degree for every chain complex over `R` (and for infinite ones), not only finite ones;
* the converse (H(i) injective implies a chain retraction exists) is FALSE over `Z` for the one-term instance
  `x -> 2x` (`TimesTwo.converse_fails_over_int`, stated through `Hmap`; it is not a subcomplex inclusion) and is not
  proved over a field here;
* the two named non-examples (two isolated points in an edge, a triangle boundary in the filled triangle) are
  built as concrete degree fragments over any ring, the inclusion is shown to be a chain map, the killed class is
  exhibited in `Hom` (`cls_ne_zero`, `cls_killed`), and `no_retraction_of_killed` gives that no linear
  `rU, rM, rL` commuting with `bd, d` and with `rM . iM = id` exists over any nontrivial ring.  The source
  theorems (`two_point_retraction_impossible`, `triangle_retraction_impossible`) take the pointwise facts
  `r0 (-1,1) = (-1,1)` and `r0 (-1,1) = (0,0)` as hypotheses; here they are derived from the chain-map
  structure.  Only the degree fragment where the class lives is modelled (degree 0 for the points, degree 1 for the
  triangle); other degrees of those complexes are not formalised in Lean, and retractions are required to be linear.
-/

namespace ChainRetraction

variable {R : Type} [Ring R]
variable {U M L U' M' L' : Type}
variable [AddCommGroup U] [AddCommGroup M] [AddCommGroup L] [AddCommGroup U'] [AddCommGroup M'] [AddCommGroup L']
variable [Module R U] [Module R M] [Module R L] [Module R U'] [Module R M'] [Module R L']

/-- Boundaries inside the cycle module, `ker d`. -/
def bdries (bd : U →ₗ[R] M) (d : M →ₗ[R] L) : Submodule R (LinearMap.ker d) :=
  (LinearMap.range bd).comap (LinearMap.ker d).subtype

/-- Homology at `M`: cycles modulo boundaries. -/
abbrev Hom (bd : U →ₗ[R] M) (d : M →ₗ[R] L) := (LinearMap.ker d) ⧸ bdries bd d

section Elementwise
variable {bd : U →ₗ[R] M} {bd' : U' →ₗ[R] M'}
variable (iM : M →ₗ[R] M') (rM : M' →ₗ[R] M) (rU : U' →ₗ[R] U)

/-- Elementwise form (the source theorem): if `r . i = id` on the middle and `r` commutes with the boundary,
a class that is not a boundary in `C` stays a non-boundary in `D`. -/
theorem cannot_kill (fixes : ∀ z, rM (iM z) = z) (rcomm : ∀ u', rM (bd' u') = bd (rU u'))
    (z : M) (hz : ¬ ∃ u, bd u = z) : ¬ ∃ u', bd' u' = iM z := by
  rintro ⟨u', hu'⟩
  apply hz
  refine ⟨rU u', ?_⟩
  rw [← rcomm, hu', fixes]

end Elementwise

section Homology
variable {bd : U →ₗ[R] M} {d : M →ₗ[R] L} {bd' : U' →ₗ[R] M'} {d' : M' →ₗ[R] L'}

/-- The induced map on homology, from a chain map `(iU, iM, iL)`. -/
def Hmap (iU : U →ₗ[R] U') (iM : M →ₗ[R] M') (iL : L →ₗ[R] L')
    (hb : ∀ u, iM (bd u) = bd' (iU u)) (hd : ∀ z, iL (d z) = d' (iM z)) :
    Hom bd d →ₗ[R] Hom bd' d' :=
  Submodule.mapQ (bdries bd d) (bdries bd' d')
    (LinearMap.restrict iM (fun z hz => by
      have : d' (iM z) = 0 := by rw [← hd, LinearMap.mem_ker.mp hz]; exact map_zero iL
      exact LinearMap.mem_ker.mpr this))
    (by
      rintro ⟨z, hz⟩ hb0
      obtain ⟨u, hu⟩ := hb0
      refine ⟨iU u, ?_⟩
      show bd' (iU u) = iM z
      rw [← hb]
      exact congrArg iM hu)

theorem Hmap_mk (iU : U →ₗ[R] U') (iM : M →ₗ[R] M') (iL : L →ₗ[R] L')
    (hb : ∀ u, iM (bd u) = bd' (iU u)) (hd : ∀ z, iL (d z) = d' (iM z)) (z : LinearMap.ker d) :
    Hmap iU iM iL hb hd (Submodule.Quotient.mk z) =
      Submodule.Quotient.mk ⟨iM z, by
        have : d' (iM z) = 0 := by rw [← hd, LinearMap.mem_ker.mp z.2]; exact map_zero iL
        exact LinearMap.mem_ker.mpr this⟩ := rfl

/-- Injectivity on homology from a chain retraction: general, over any ring, any modules. -/
theorem Hmap_injective (iU : U →ₗ[R] U') (iM : M →ₗ[R] M') (iL : L →ₗ[R] L')
    (hb : ∀ u, iM (bd u) = bd' (iU u)) (hd : ∀ z, iL (d z) = d' (iM z))
    (rU : U' →ₗ[R] U) (rM : M' →ₗ[R] M) (rL : L' →ₗ[R] L)
    (hrb : ∀ u', rM (bd' u') = bd (rU u')) (hrd : ∀ z', rL (d' z') = d (rM z'))
    (fixes : ∀ z, rM (iM z) = z) :
    Function.Injective (Hmap iU iM iL hb hd) := by
  have left : Function.LeftInverse (Hmap rU rM rL hrb hrd) (Hmap iU iM iL hb hd) := by
    intro q
    induction q using Submodule.Quotient.induction_on with
    | H z =>
      rw [Hmap_mk, Hmap_mk]
      exact congrArg Submodule.Quotient.mk (Subtype.ext (fixes z.1))
  exact left.injective

/-- Kernel form: a cycle that becomes a boundary in `D` was already a boundary in `C`. -/
theorem kernel_trivial (iU : U →ₗ[R] U') (iM : M →ₗ[R] M') (iL : L →ₗ[R] L')
    (hb : ∀ u, iM (bd u) = bd' (iU u)) (hd : ∀ z, iL (d z) = d' (iM z))
    (rU : U' →ₗ[R] U) (rM : M' →ₗ[R] M) (rL : L' →ₗ[R] L)
    (hrb : ∀ u', rM (bd' u') = bd (rU u')) (hrd : ∀ z', rL (d' z') = d (rM z'))
    (fixes : ∀ z, rM (iM z) = z) (q : Hom bd d) (h : Hmap iU iM iL hb hd q = 0) : q = 0 := by
  apply Hmap_injective iU iM iL hb hd rU rM rL hrb hrd fixes
  rw [h, map_zero]

end Homology

/-! ### A killed class excludes every retraction -/

section Killed
variable {bd : U →ₗ[R] M} {d : M →ₗ[R] L} {bd' : U' →ₗ[R] M'} {d' : M' →ₗ[R] L'}
variable (iU : U →ₗ[R] U') (iM : M →ₗ[R] M') (iL : L →ₗ[R] L')
variable (hb : ∀ u, iM (bd u) = bd' (iU u)) (hd : ∀ z, iL (d z) = d' (iM z))

/-- If the induced map on homology kills a nonzero class, no chain retraction of `i` exists
(contrapositive of `kernel_trivial`, with the full chain-map hypotheses on `r`). -/
theorem no_retraction_of_killed (q : Hom bd d) (hq : q ≠ 0) (hk : Hmap iU iM iL hb hd q = 0) :
    ¬ ∃ (rU : U' →ₗ[R] U) (rM : M' →ₗ[R] M) (rL : L' →ₗ[R] L),
      (∀ u', rM (bd' u') = bd (rU u')) ∧ (∀ z', rL (d' z') = d (rM z')) ∧ (∀ z, rM (iM z) = z) := by
  rintro ⟨rU, rM, rL, hrb, hrd, fixes⟩
  exact hq (kernel_trivial iU iM iL hb hd rU rM rL hrb hrd fixes q hk)

end Killed

/-! ### The two named non-examples as chain complexes

Each is one degree fragment `U --bd--> M --d--> L` over a ring `R`, the inclusion `i` is a chain map
(`hb`, `hd` are proved), the killed class is exhibited in `Hom` (nonzero, sent to zero by `Hmap`), and the
non-existence of a chain retraction (linear `rU, rM, rL` commuting with `bd, d` and with `rM . iM = id`) is
obtained from `no_retraction_of_killed`.  Nontrivial `R` is needed for the class to be nonzero. -/

namespace TwoPoints
variable (R : Type) [Ring R]

/-- C: two points, no 1-chains.  D: the edge from point 0 to point 1.  Degree-0 fragment (L = 0). -/
def bdC : Unit →ₗ[R] (Fin 2 → R) := 0
def dC : (Fin 2 → R) →ₗ[R] Unit := 0
def bdD : R →ₗ[R] (Fin 2 → R) := LinearMap.toSpanSingleton R (Fin 2 → R) ![-1, 1]
def iU : Unit →ₗ[R] R := 0
def iM : (Fin 2 → R) →ₗ[R] (Fin 2 → R) := LinearMap.id
def iL : Unit →ₗ[R] Unit := 0

theorem hb (u : Unit) : iM R (bdC R u) = bdD R (iU R u) := by simp [bdC, bdD, iU, iM]
theorem hd (z : Fin 2 → R) : iL R (dC R z) = dC R (iM R z) := Subsingleton.elim _ _

/-- The cycle `q - p` (the boundary of the edge). -/
def cls : LinearMap.ker (dC R) := ⟨![-1, 1], by simp [dC]⟩

theorem cls_ne_zero [Nontrivial R] : (Submodule.Quotient.mk (cls R) : Hom (bdC R) (dC R)) ≠ 0 := by
  intro h
  rw [Submodule.Quotient.mk_eq_zero] at h
  obtain ⟨u, hu⟩ := h
  have := congrFun hu 1
  simp [bdC, cls] at this

theorem cls_killed : Hmap (bd := bdC R) (d := dC R) (bd' := bdD R) (d' := dC R) (iU R) (iM R) (iL R) (hb R) (hd R)
    (Submodule.Quotient.mk (cls R)) = 0 := by
  rw [Hmap_mk, Submodule.Quotient.mk_eq_zero]
  refine ⟨1, ?_⟩
  simp [bdD, iM, cls]

theorem no_chain_retraction [Nontrivial R] :
    ¬ ∃ (rU : R →ₗ[R] Unit) (rM : (Fin 2 → R) →ₗ[R] (Fin 2 → R)) (rL : Unit →ₗ[R] Unit),
      (∀ u', rM (bdD R u') = bdC R (rU u')) ∧ (∀ z', rL (dC R z') = dC R (rM z')) ∧ (∀ z, rM (iM R z) = z) :=
  no_retraction_of_killed (iU R) (iM R) (iL R) (hb R) (hd R) _ (cls_ne_zero R) (cls_killed R)

end TwoPoints

namespace Triangle
variable (R : Type) [Ring R]

/-- Vertex boundary of the edge chains `(e01, e12, e02)`: `(-a - c, a - b, b + c)`. -/
def dV : (Fin 3 → R) →ₗ[R] (Fin 3 → R) where
  toFun v := ![-v 0 - v 2, v 0 - v 1, v 1 + v 2]
  map_add' x y := by
    ext i; fin_cases i <;> simp [sub_eq_add_neg, add_comm, add_left_comm, add_assoc]
  map_smul' c x := by
    ext i; fin_cases i <;> simp [sub_eq_add_neg, mul_add]

/-- C: the triangle boundary (no 2-chains).  D: the filled triangle, `bd f = f (e01 + e12 - e02)`.  Degree-1 fragment. -/
def bdC : Unit →ₗ[R] (Fin 3 → R) := 0
def bdD : R →ₗ[R] (Fin 3 → R) := LinearMap.toSpanSingleton R (Fin 3 → R) ![1, 1, -1]
def iU : Unit →ₗ[R] R := 0
def iM : (Fin 3 → R) →ₗ[R] (Fin 3 → R) := LinearMap.id
def iL : (Fin 3 → R) →ₗ[R] (Fin 3 → R) := LinearMap.id

theorem hb (u : Unit) : iM R (bdC R u) = bdD R (iU R u) := by simp [bdC, bdD, iU, iM]
theorem hd (z : Fin 3 → R) : iL R (dV R z) = dV R (iM R z) := rfl

/-- `d . bd = 0` for the filled triangle: the complex axiom. -/
theorem square_zero (f : R) : dV R (bdD R f) = 0 := by
  ext i; fin_cases i <;> simp [dV, bdD]

/-- The boundary cycle `e01 + e12 - e02`. -/
def cls : LinearMap.ker (dV R) := ⟨![1, 1, -1], by ext i; fin_cases i <;> simp [dV]⟩

theorem cls_ne_zero [Nontrivial R] : (Submodule.Quotient.mk (cls R) : Hom (bdC R) (dV R)) ≠ 0 := by
  intro h
  rw [Submodule.Quotient.mk_eq_zero] at h
  obtain ⟨u, hu⟩ := h
  have := congrFun hu 0
  simp [bdC, cls] at this

theorem cls_killed : Hmap (bd := bdC R) (d := dV R) (bd' := bdD R) (d' := dV R) (iU R) (iM R) (iL R) (hb R) (hd R)
    (Submodule.Quotient.mk (cls R)) = 0 := by
  rw [Hmap_mk, Submodule.Quotient.mk_eq_zero]
  refine ⟨1, ?_⟩
  simp [bdD, iM, cls]

theorem no_chain_retraction [Nontrivial R] :
    ¬ ∃ (rU : R →ₗ[R] Unit) (rM : (Fin 3 → R) →ₗ[R] (Fin 3 → R)) (rL : (Fin 3 → R) →ₗ[R] (Fin 3 → R)),
      (∀ u', rM (bdD R u') = bdC R (rU u')) ∧ (∀ z', rL (dV R z') = dV R (rM z')) ∧ (∀ z, rM (iM R z) = z) :=
  no_retraction_of_killed (iU R) (iM R) (iL R) (hb R) (hd R) _ (cls_ne_zero R) (cls_killed R)

end Triangle

/-! ### The converse fails over `Z`: a labelled one-term instance (not a subcomplex inclusion) -/

namespace TimesTwo
def bdZ : Unit →ₗ[Int] Int := 0
def dZ : Int →ₗ[Int] Unit := 0
def iUZ : Unit →ₗ[Int] Unit := 0
def iMZ : Int →ₗ[Int] Int := LinearMap.id + LinearMap.id
def iLZ : Unit →ₗ[Int] Unit := 0

theorem hb (u : Unit) : iMZ (bdZ u) = bdZ (iUZ u) := by simp [bdZ, iMZ]
theorem hd (z : Int) : iLZ (dZ z) = dZ (iMZ z) := Subsingleton.elim _ _

/-- `H(i)` is injective (it is `x -> 2x` on `Z`), yet no chain retraction exists. -/
theorem converse_fails_over_int :
    Function.Injective (Hmap (bd := bdZ) (d := dZ) (bd' := bdZ) (d' := dZ) iUZ iMZ iLZ hb hd) ∧
    ¬ ∃ (rU : Unit →ₗ[Int] Unit) (rM : Int →ₗ[Int] Int) (rL : Unit →ₗ[Int] Unit),
      (∀ u', rM (bdZ u') = bdZ (rU u')) ∧ (∀ z', rL (dZ z') = dZ (rM z')) ∧ (∀ z, rM (iMZ z) = z) := by
  constructor
  · rw [injective_iff_map_eq_zero]
    intro q hq
    induction q using Submodule.Quotient.induction_on with
    | H z =>
      rw [Hmap_mk, Submodule.Quotient.mk_eq_zero] at hq
      obtain ⟨u, hu⟩ := hq
      have h2 : (z : Int) + z = 0 := by
        have := hu.symm
        simpa [bdZ, iMZ] using this
      have hz : (z : Int) = 0 := by omega
      rw [Submodule.Quotient.mk_eq_zero]
      exact ⟨0, by simp [bdZ, hz]⟩
  · rintro ⟨_, rM, _, _, _, fixes⟩
    have h1 := fixes 1
    simp only [iMZ, LinearMap.add_apply, LinearMap.id_apply, map_add] at h1
    omega

end TimesTwo

end ChainRetraction

#print axioms ChainRetraction.cannot_kill
#print axioms ChainRetraction.Hmap_injective
#print axioms ChainRetraction.kernel_trivial
#print axioms ChainRetraction.no_retraction_of_killed
#print axioms ChainRetraction.TwoPoints.cls_ne_zero
#print axioms ChainRetraction.TwoPoints.cls_killed
#print axioms ChainRetraction.TwoPoints.no_chain_retraction
#print axioms ChainRetraction.Triangle.square_zero
#print axioms ChainRetraction.Triangle.cls_ne_zero
#print axioms ChainRetraction.Triangle.cls_killed
#print axioms ChainRetraction.Triangle.no_chain_retraction
#print axioms ChainRetraction.TimesTwo.converse_fails_over_int
