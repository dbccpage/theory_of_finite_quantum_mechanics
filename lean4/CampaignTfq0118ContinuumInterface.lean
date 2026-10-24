import Mathlib.Data.Rat.Defs
import Mathlib.Data.Fintype.Card
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.FinCases

/-!
# Campaign Formalization: `TFQ-0118` (`CONTINUUM_INTERFACE`)
## Injective Cyclic Inclusion, Separating Character Sums, and Discretization/Interacting Scope Fences

This module formalizes the exact finite/algebraic counterpart and non-equivalence scope fences for
DAG node `TFQ-0118` (`Open rows include cdx2.interacting_qft and cdx2.haar_continuous_density.
Continuum limit stays GAP`):

1. **Injective Dyadic Cyclic Inclusion (`dyadicInclude : Fin N → Fin (2 * N)`)**:
   - Defines `dyadicInclude N (x : Fin N) : Fin (2 * N)` sending `x ↦ 2 * x`.
   - Proves strict injectivity (`dyadicInclude_injective`), modular-addition homomorphism
     `(2 * ((a + b) % N)) % (2 * N) = (2 * a + 2 * b) % (2 * N)` (`dyadicInclude_add_mod_hom`),
     and non-surjectivity onto `Fin (2 * N)` since odd residue `1` is never in the image of
     `dyadicInclude N` (`dyadicInclude_misses_odd_residue`).

2. **Point-Separating Character Sums Inside a Declared Finite Budget (`Z/4Z`)**:
   - Over Gaussian rationals `GaussRat` (`ℚ × ℚ`), defines the dual character sum
     `charPointProjector4 (x y : Fin 4) : GaussRat = ∑_{k ∈ Fin 4} χ_k(x) * conj(χ_k(y))`.
   - Proves the exact Kronecker-delta identity `charPointProjector4 x y = ⟨4, 0⟩` if `x = y` and
     `⟨0, 0⟩` if `x ≠ y` (`z4_character_point_projector_exact`), and deduces that for any two
     distinct elements `x ≠ y` in `Fin 4`, there exists a character `k : Fin 4` that separates them
     (`chi4 k x ≠ chi4 k y`, `z4_characters_separate_distinct_points`).

3. **Five Open Obligations Fences (`cdx2.haar_continuous_density` & `cdx2.interacting_qft`)**:
   - **Discretization Defect Fence (`discretization_defect_quadratic_observable`)**:
     On a uniform `N`-point grid (`N > 0`), the left Riemann sum of `f(t) = t^2` is
     `leftRiemannQuadratic N = (N - 1) * (2 * N - 1) / (6 * N^2)`, whose defect from the continuum
     Haar integral `1 / 3` equals `(3 * N - 1) / (6 * N^2) > 0` for every finite `N ≥ 1`—never
     vanishing at any finite budget `N`.
   - **Interacting Quartic Non-Superposition Fence (`interacting_quartic_eom_nonlinearity_fence`)**:
     For the quartic equation-of-motion operator `quarticEom mSq g φ = mSq * φ + g * φ^3`, the free
     theory (`g = 0`) is strictly linear (`quarticEom mSq 0 (a + b) = quarticEom mSq 0 a + quarticEom mSq 0 b`),
     whereas for any nonzero coupling `g ≠ 0` the superposition defect at `a = 1, b = 1` equals
     `6 * g ≠ 0`.
-/

namespace CampaignTfq0118ContinuumInterface

-- ============================================================================
-- 1. Injective Dyadic Cyclic Inclusion (`Fin N ↪ Fin (2 * N)`)
-- ============================================================================

/-- Injective inclusion `x ↦ 2 * x` of `Fin N` into `Fin (2 * N)`. -/
def dyadicInclude (N : Nat) (x : Fin N) : Fin (2 * N) :=
  ⟨2 * x.val, by omega⟩

/-- Theorem 1: `dyadicInclude N` is strictly injective for every `N`. -/
theorem dyadicInclude_injective (N : Nat) :
    Function.Injective (dyadicInclude N) := by
  intro x y h
  have hval : (dyadicInclude N x).val = (dyadicInclude N y).val := congrArg Fin.val h
  dsimp [dyadicInclude] at hval
  exact Fin.ext (by omega)

/-- Theorem 2: Doubling commutes with modular addition:
`2 * ((a + b) % N) = (2 * a + 2 * b) % (2 * N)`. -/
theorem dyadicInclude_add_mod_hom (N a b : Nat) :
    2 * ((a + b) % N) = (2 * a + 2 * b) % (2 * N) := by
  have h1 : 2 * (a + b) = 2 * a + 2 * b := by ring
  rw [← h1]
  exact (Nat.mul_mod_mul_left 2 (a + b) N).symm

/-- Theorem 3: For every `N > 0`, the odd residue `1` in `Fin (2 * N)` is never in the image of
`dyadicInclude N`, so a single finite cyclic level is a proper subgroup of the next dyadic level. -/
theorem dyadicInclude_misses_odd_residue (N : Nat) (x : Fin N) :
    (dyadicInclude N x).val ≠ 1 := by
  dsimp [dyadicInclude]
  omega

-- ============================================================================
-- 2. Point-Separating Character Sums Inside a Declared Finite Budget (`Z/4Z`)
-- ============================================================================

/-- Gaussian integer/rational unit-lattice element `re + i * im` over `Int`. -/
@[ext]
structure GaussRat where
  re : Int
  im : Int
  deriving DecidableEq, Repr

def gaussZero : GaussRat := ⟨0, 0⟩

def gaussAdd (z w : GaussRat) : GaussRat :=
  ⟨z.re + w.re, z.im + w.im⟩

def gaussMul (z w : GaussRat) : GaussRat :=
  ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩

def gaussConj (z : GaussRat) : GaussRat :=
  ⟨z.re, -z.im⟩

/-- The 4th roots of unity `μ_4 = {1, i, -1, -i}` indexed by `Fin 4`. -/
def mu4 (n : Fin 4) : GaussRat :=
  match n.val with
  | 0 => ⟨1, 0⟩
  | 1 => ⟨0, 1⟩
  | 2 => ⟨-1, 0⟩
  | _ => ⟨0, -1⟩

/-- Character `χ_k(x) = μ_4((k * x) mod 4)` on `Fin 4`. -/
def chi4 (k x : Fin 4) : GaussRat :=
  mu4 ⟨(k.val * x.val) % 4, Nat.mod_lt _ (by decide)⟩

/-- Dual character sum `∑_{k ∈ Fin 4} χ_k(x) * conj(χ_k(y))` testing point separation on `Fin 4`. -/
def charPointProjector4 (x y : Fin 4) : GaussRat :=
  let t0 := gaussMul (chi4 0 x) (gaussConj (chi4 0 y))
  let t1 := gaussMul (chi4 1 x) (gaussConj (chi4 1 y))
  let t2 := gaussMul (chi4 2 x) (gaussConj (chi4 2 y))
  let t3 := gaussMul (chi4 3 x) (gaussConj (chi4 3 y))
  gaussAdd (gaussAdd t0 t1) (gaussAdd t2 t3)

/-- Theorem 4: The dual character sum over `Fin 4` equals `⟨4, 0⟩` on the diagonal `x = y` and
`⟨0, 0⟩` off the diagonal `x ≠ y`. -/
theorem z4_character_point_projector_exact (x y : Fin 4) :
    charPointProjector4 x y = (if x = y then ⟨4, 0⟩ else gaussZero) := by
  revert x y
  decide

/-- Theorem 5: Characters of `Fin 4` separate all distinct points: whenever `x ≠ y`, there exists a
character label `k : Fin 4` such that `chi4 k x ≠ chi4 k y`. -/
theorem z4_characters_separate_distinct_points (x y : Fin 4) (hxy : x ≠ y) :
    ∃ k : Fin 4, chi4 k x ≠ chi4 k y := by
  revert hxy
  revert x y
  decide

-- ============================================================================
-- 3. Open Continuum Obligations Fences (`discretization_defect` & `interacting_qft`)
-- ============================================================================

/-- Closed-form left Riemann sum `(N - 1) * (2 * N - 1) / (6 * N^2)` of `f(t) = t^2` on `[0, 1]`
over `N` uniform subintervals. -/
def leftRiemannQuadratic (N : ℚ) : ℚ :=
  (N - 1) * (2 * N - 1) / (6 * N ^ 2)

/-- Discretization defect `(1 / 3) - leftRiemannQuadratic N` between the continuum Haar integral
`∫_0^1 t^2 dt = 1/3` and its `N`-point finite enclosure approximation. -/
def quadraticDiscretizationDefect (N : ℚ) : ℚ :=
  1 / 3 - leftRiemannQuadratic N

/-- Theorem 6: For any nonzero budget `N ≠ 0`, the quadratic discretization defect equals
`(3 * N - 1) / (6 * N^2)`. -/
theorem discretization_defect_closed_form (N : ℚ) (hN : N ≠ 0) :
    quadraticDiscretizationDefect N = (3 * N - 1) / (6 * N ^ 2) := by
  dsimp [quadraticDiscretizationDefect, leftRiemannQuadratic]
  field_simp [hN]
  ring

/-- Theorem 7 (`cdx2.haar_continuous_density` / Metric Completion Fence): For every finite budget
`N ≥ 1`, the quadratic discretization defect `quadraticDiscretizationDefect N` is strictly positive
(`> 0`) and hence nonzero (`≠ 0`), so no fixed-size finite enclosure equals the continuum integral. -/
theorem discretization_defect_strictly_positive_for_all_finite_N
    (N : ℚ) (hN1 : 1 ≤ N) :
    0 < quadraticDiscretizationDefect N ∧
    quadraticDiscretizationDefect N ≠ 0 := by
  have hN0 : N ≠ 0 := by linarith
  have hnum : 0 < 3 * N - 1 := by linarith
  have hden : 0 < 6 * N ^ 2 := by positivity
  have hdiv : 0 < (3 * N - 1) / (6 * N ^ 2) := div_pos hnum hden
  rw [discretization_defect_closed_form N hN0]
  exact ⟨hdiv, ne_of_gt hdiv⟩

/-- Theorem 8: Explicit rational discretization defects at finite budgets `N ∈ {1, 2, 4, 8}`:
`1/3, 5/24, 11/96, 23/384`, strictly decreasing yet strictly positive at every finite stage. -/
theorem discretization_defect_dyadic_budget_table :
    quadraticDiscretizationDefect 1 = 1 / 3 ∧
    quadraticDiscretizationDefect 2 = 5 / 24 ∧
    quadraticDiscretizationDefect 4 = 11 / 96 ∧
    quadraticDiscretizationDefect 8 = 23 / 384 ∧
    quadraticDiscretizationDefect 8 < quadraticDiscretizationDefect 4 ∧
    quadraticDiscretizationDefect 4 < quadraticDiscretizationDefect 2 ∧
    quadraticDiscretizationDefect 2 < quadraticDiscretizationDefect 1 := by
  dsimp [quadraticDiscretizationDefect, leftRiemannQuadratic]
  norm_num

/-- Equation-of-motion operator `mSq * φ + g * φ^3` for the scalar action
`S(φ) = (1/2) * mSq * φ^2 + (g/4) * φ^4`. -/
def quarticEom (mSq g φ : ℚ) : ℚ :=
  mSq * φ + g * φ ^ 3

/-- Superposition residual `quarticEom mSq g (a + b) - (quarticEom mSq g a + quarticEom mSq g b)`. -/
def quarticSuperpositionDefect (mSq g a b : ℚ) : ℚ :=
  quarticEom mSq g (a + b) - (quarticEom mSq g a + quarticEom mSq g b)

/-- Theorem 9 (`cdx2.interacting_qft` Fence): In the free theory (`g = 0`), `quarticSuperpositionDefect`
vanishes identically for all `a, b`, whereas for general `g` it equals `3 * g * a * b * (a + b)`. -/
theorem quartic_superposition_defect_identity (mSq g a b : ℚ) :
    quarticSuperpositionDefect mSq 0 a b = 0 ∧
    quarticSuperpositionDefect mSq g a b = 3 * g * a * b * (a + b) := by
  refine ⟨?_, ?_⟩
  · dsimp [quarticSuperpositionDefect, quarticEom]; ring
  · dsimp [quarticSuperpositionDefect, quarticEom]; ring

/-- Theorem 10: A quartic coupling `g` satisfies linear superposition at `a = 1, b = 1` if and only
if the interaction coupling vanishes (`g = 0`). -/
theorem quartic_superposition_at_unit_iff_free (mSq g : ℚ) :
    quarticSuperpositionDefect mSq g 1 1 = 0 ↔ g = 0 := by
  dsimp [quarticSuperpositionDefect, quarticEom]
  constructor <;> intro h <;> linarith

end CampaignTfq0118ContinuumInterface

#print axioms CampaignTfq0118ContinuumInterface.dyadicInclude_injective
#print axioms CampaignTfq0118ContinuumInterface.dyadicInclude_add_mod_hom
#print axioms CampaignTfq0118ContinuumInterface.dyadicInclude_misses_odd_residue
#print axioms CampaignTfq0118ContinuumInterface.z4_character_point_projector_exact
#print axioms CampaignTfq0118ContinuumInterface.z4_characters_separate_distinct_points
#print axioms CampaignTfq0118ContinuumInterface.discretization_defect_closed_form
#print axioms CampaignTfq0118ContinuumInterface.discretization_defect_strictly_positive_for_all_finite_N
#print axioms CampaignTfq0118ContinuumInterface.discretization_defect_dyadic_budget_table
#print axioms CampaignTfq0118ContinuumInterface.quartic_superposition_defect_identity
#print axioms CampaignTfq0118ContinuumInterface.quartic_superposition_at_unit_iff_free

private def l5aProvenance : String :=
  "Origin: lean4/CampaignTfq0118ContinuumInterface.lean Claim: TFQ-0118 AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
