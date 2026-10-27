




namespace HilbertWalk.SimplicialAreaLawPageCurve


namespace SimplicialAreaLaw

def boundary_area (N M_int : Nat) : Int :=
  4 * (N : Int) - 2 * (M_int : Int)

theorem boundary_area_even (N M_int : Nat) : (boundary_area N M_int) % 2 = 0 := by
  dsimp [boundary_area]
  omega

theorem gluing_reduces_boundary (N M_int : Nat) (h : M_int > 0) :
    boundary_area N M_int < 4 * (N : Int) := by
  dsimp [boundary_area]
  omega

end SimplicialAreaLaw


namespace MicrostateProjection

def bulk_microstates (d N : Nat) : Nat :=
  d ^ (4 * N)

def boundary_microstates (d A : Nat) : Nat :=
  d ^ A

theorem interior_matching_projection (d N M_int A : Nat) (h : A + 2 * M_int = 4 * N) :
    bulk_microstates d N = boundary_microstates d A * d ^ (2 * M_int) := by
  dsimp [bulk_microstates, boundary_microstates]
  rw [← Nat.pow_add]
  congr 1
  omega

theorem holographic_bulk_invariance (d A N1 M1 N2 M2 : Nat)
    (h1 : 4 * N1 - 2 * M1 = A) (h2 : 4 * N2 - 2 * M2 = A) :
    boundary_microstates d (4 * N1 - 2 * M1) = boundary_microstates d (4 * N2 - 2 * M2) := by
  rw [h1, h2]

end MicrostateProjection


namespace SchmidtRankCeiling

def schmidt_rank_bound (d A_B A_R : Nat) : Nat :=
  d ^ (min A_B A_R)

theorem schmidt_rank_subsystem_symmetry (d A_B A_R : Nat) :
    schmidt_rank_bound d A_B A_R = schmidt_rank_bound d A_R A_B := by
  dsimp [schmidt_rank_bound]
  rw [Nat.min_comm]

theorem schmidt_rank_ceiling_min (d A_B A_R : Nat) (hd : d ≥ 1) :
    schmidt_rank_bound d A_B A_R ≤ d ^ A_B ∧ schmidt_rank_bound d A_B A_R ≤ d ^ A_R := by
  dsimp [schmidt_rank_bound]
  constructor
  · exact Nat.pow_le_pow_right hd (Nat.min_le_left A_B A_R)
  · exact Nat.pow_le_pow_right hd (Nat.min_le_right A_B A_R)

end SchmidtRankCeiling


namespace CombinatorialPageCurve

def page_entropy_4x (A_B A_R : Nat) : Nat :=
  min A_B A_R

theorem page_curve_subsystem_symmetry (A_B A_R : Nat) :
    page_entropy_4x A_B A_R = page_entropy_4x A_R A_B := by
  dsimp [page_entropy_4x]
  rw [Nat.min_comm]

theorem page_curve_initial_zero (A_0 : Nat) :
    page_entropy_4x A_0 0 = 0 := by
  dsimp [page_entropy_4x]
  exact Nat.min_zero A_0

theorem page_curve_terminal_unitarity (A_0 : Nat) :
    page_entropy_4x 0 A_0 = 0 := by
  dsimp [page_entropy_4x]
  exact Nat.zero_min A_0

theorem early_phase_bound (A_B A_R : Nat) (h : A_R ≤ A_B) :
    page_entropy_4x A_B A_R = A_R := by
  dsimp [page_entropy_4x]
  exact Nat.min_eq_right h

theorem late_phase_bound (A_B A_R : Nat) (h : A_B ≤ A_R) :
    page_entropy_4x A_B A_R = A_B := by
  dsimp [page_entropy_4x]
  exact Nat.min_eq_left h

theorem page_peak_achieved (A_half : Nat) :
    page_entropy_4x A_half A_half = A_half := by
  dsimp [page_entropy_4x]
  exact Nat.min_self A_half

theorem page_entropy_le_half_total (A_B A_R A_0 : Nat) (h : A_B + A_R = A_0) :
    2 * (page_entropy_4x A_B A_R) ≤ A_0 := by
  dsimp [page_entropy_4x]
  have h1 := Nat.min_le_left A_B A_R
  have h2 := Nat.min_le_right A_B A_R
  omega

end CombinatorialPageCurve


namespace GravitationalBackreaction

theorem cayley_retardation_monotonic (eps1 eps2 : Int) (h : eps1 ≤ eps2) :
    (1 - eps2) * (1 + eps1) ≤ (1 - eps1) * (1 + eps2) := by
  have h1 : (1 - eps2) * (1 + eps1) = 1 + eps1 - eps2 - eps2 * eps1 := by
    calc (1 - eps2) * (1 + eps1)
      _ = 1 * (1 + eps1) - eps2 * (1 + eps1) := by rw [Int.sub_mul]
      _ = (1 + eps1) - (eps2 * 1 + eps2 * eps1) := by rw [Int.one_mul, Int.mul_add]
      _ = 1 + eps1 - eps2 - eps2 * eps1 := by rw [Int.mul_one]; omega
  have h2 : (1 - eps1) * (1 + eps2) = 1 + eps2 - eps1 - eps1 * eps2 := by
    calc (1 - eps1) * (1 + eps2)
      _ = 1 * (1 + eps2) - eps1 * (1 + eps2) := by rw [Int.sub_mul]
      _ = (1 + eps2) - (eps1 * 1 + eps1 * eps2) := by rw [Int.one_mul, Int.mul_add]
      _ = 1 + eps2 - eps1 - eps1 * eps2 := by rw [Int.mul_one]; omega
  have hcomm : eps2 * eps1 = eps1 * eps2 := Int.mul_comm eps2 eps1
  rw [h1, h2, hcomm]
  omega

theorem cayley_slowdown_at_positive_defect (eps : Int) (h : eps > 0) :
    (1 - eps) * (1 + 0) < (1 - 0) * (1 + eps) := by
  have h1 : (1 - eps) * (1 + 0) = 1 - eps := by
    have hzero : (1 : Int) + 0 = 1 := by decide
    rw [hzero, Int.mul_one]
  have h2 : (1 - 0) * (1 + eps) = 1 + eps := by
    have hzero : (1 : Int) - 0 = 1 := by decide
    rw [hzero, Int.one_mul]
  rw [h1, h2]
  omega

end GravitationalBackreaction


#print axioms SimplicialAreaLaw.boundary_area_even
#print axioms SimplicialAreaLaw.gluing_reduces_boundary
#print axioms MicrostateProjection.interior_matching_projection
#print axioms MicrostateProjection.holographic_bulk_invariance
#print axioms SchmidtRankCeiling.schmidt_rank_subsystem_symmetry
#print axioms SchmidtRankCeiling.schmidt_rank_ceiling_min
#print axioms CombinatorialPageCurve.page_curve_subsystem_symmetry
#print axioms CombinatorialPageCurve.page_curve_initial_zero
#print axioms CombinatorialPageCurve.page_curve_terminal_unitarity
#print axioms CombinatorialPageCurve.early_phase_bound
#print axioms CombinatorialPageCurve.late_phase_bound
#print axioms CombinatorialPageCurve.page_peak_achieved
#print axioms CombinatorialPageCurve.page_entropy_le_half_total
#print axioms GravitationalBackreaction.cayley_retardation_monotonic
#print axioms GravitationalBackreaction.cayley_slowdown_at_positive_defect

end HilbertWalk.SimplicialAreaLawPageCurve

private def l5aProvenance : String :=
  "Origin: lean4/SimplicialAreaLawPageCurve.lean Claim: boundary_area_even AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
