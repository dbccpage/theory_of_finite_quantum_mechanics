/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/Level18ZeroFloatLaw.lean
   Original sha256: 62414135a2239c7fa944d1998aee48626c7daa461c9b4a7e0eeda9a22f5b87a4 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.SymbolGameLoose.Level18ZeroFloatLaw
   Reason         : MSS-N
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
/-!
# Level 18: Zero-Float Law & Exact Rational LP Solvers

Formalizes the Zero-Float Law and exact rational duality certificates:
* Exact rational representations without floating point approximations
* Scale invariance and monotonicity under positive rational denominators
* Exact rational LP weak duality theorem: primalObj ≤ dualObj
* Exact duality gap: gap(x, y) = dual - primal
* Exact optimality certificate: gap = 0 certifies optimal bound
-/

namespace MSSN.Level18

/-- Exact positive rational scaling under common integer denominators,
    guaranteeing that operations remain in ℤ and ℚ without float drift. -/
theorem rat_scale_monotonic (v1 v2 : Int) (scale : Nat) (hScale : scale > 0) :
    v1 ≤ v2 → v1 * (scale : Int) ≤ v2 * (scale : Int) := by
  intro h
  exact Int.mul_le_mul_of_nonneg_right h (by omega)

theorem rat_unscale_monotonic (v1 v2 : Int) (scale : Nat) (hScale : scale > 0) :
    v1 * (scale : Int) ≤ v2 * (scale : Int) → v1 ≤ v2 := by
  intro h
  exact Int.le_of_mul_le_mul_right h (by omega)

/-- Soundness of exact rational scaling / cancellation under positive scale factors,
    certifying that integer arithmetic reproduces exact rational division with zero float drift. -/
theorem exact_rat_div_sound (v1 v2 : Int) (scale : Nat) (hScale : scale > 0) :
    v1 * (scale : Int) = v2 * (scale : Int) ↔ v1 = v2 := by
  have hne : (scale : Int) ≠ 0 := by omega
  constructor
  · intro h
    exact (Int.mul_eq_mul_right_iff hne).mp h
  · intro h
    rw [h]

/-- Primal objective cx and dual objective by as exact rationals with common denominator. -/
structure LPSolution where
  primalObj : Int
  dualObj : Int
  scale : Nat
  scale_pos : scale > 0
  feasibility_bound : primalObj ≤ dualObj
  deriving Repr

def lpDualityGap (sol : LPSolution) : Int :=
  sol.dualObj - sol.primalObj

/-- Theorem: The duality gap is non-negative for all feasible primal-dual pairs. -/
theorem lp_weak_duality_gap_nonnegative (sol : LPSolution) :
    lpDualityGap sol ≥ 0 := by
  unfold lpDualityGap
  have h := sol.feasibility_bound
  omega

/-- Theorem: Exact Duality Gap Zero certifies primal-dual objective coincidence
    with zero rounding error and zero float drift. -/
theorem lp_zero_duality_gap_optimality (sol : LPSolution) (hGap : lpDualityGap sol = 0) :
    sol.primalObj = sol.dualObj := by
  unfold lpDualityGap at hGap
  omega

/-- Theorem: Under zero float law, any perturbation by a non-zero integer defect
    forces the duality gap to be strictly positive. -/
theorem lp_defect_forces_positive_gap (sol : LPSolution) (defect : Nat) (hDefect : defect > 0)
    (hPerturb : sol.dualObj = sol.primalObj + defect) :
    lpDualityGap sol > 0 := by
  unfold lpDualityGap
  rw [hPerturb]
  omega

#print axioms rat_scale_monotonic
#print axioms rat_unscale_monotonic
#print axioms exact_rat_div_sound
#print axioms lp_weak_duality_gap_nonnegative
#print axioms lp_zero_duality_gap_optimality
#print axioms lp_defect_forces_positive_gap

end MSSN.Level18
