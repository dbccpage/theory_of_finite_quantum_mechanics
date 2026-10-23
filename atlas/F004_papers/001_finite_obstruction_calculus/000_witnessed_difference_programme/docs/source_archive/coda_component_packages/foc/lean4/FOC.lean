import Foundations
import Mathlib.LinearAlgebra.Quotient.Basic
import Mathlib.LinearAlgebra.Dual.Lemmas
import Mathlib.Tactic
import Mathlib.Topology.MetricSpace.HausdorffDistance
namespace Coda.FOC
variable {K V W Z : Type*} [Field K] [AddCommGroup V] [Module K V]
  [AddCommGroup W] [Module K W] [AddCommGroup Z] [Module K Z]

def RepairEquivalent (R : Submodule K V) (x y : V) : Prop := x - y ∈ R

theorem repair_refl (R : Submodule K V) (x : V) : RepairEquivalent R x x := by
  simp [RepairEquivalent]

theorem repair_symm (R : Submodule K V) {x y : V} (h : RepairEquivalent R x y) :
    RepairEquivalent R y x := by
  simpa [RepairEquivalent, neg_sub] using R.neg_mem h

theorem repair_trans (R : Submodule K V) {x y z : V}
    (hxy : RepairEquivalent R x y) (hyz : RepairEquivalent R y z) :
    RepairEquivalent R x z := by
  have h := R.add_mem hxy hyz
  simpa [RepairEquivalent, sub_add_sub_cancel] using h

theorem separator_obstructs (R : Submodule K V) (phi : V →ₗ[K] W)
    (annihilates : ∀ r ∈ R, phi r = 0) {x : V} (nonzero : phi x ≠ 0) : x ∉ R := by
  intro hx
  exact nonzero (annihilates x hx)

theorem exact_closed (d0 : V →ₗ[K] W) (d1 : W →ₗ[K] Z)
    (compatible : ∀ v, d1 (d0 v) = 0) {w : W} (exact : ∃ v, d0 v = w) : d1 w = 0 := by
  obtain ⟨v, rfl⟩ := exact
  exact compatible v

theorem weighted_diagonal_lower (w1 w2 m x y t : ℝ)
    (hm : 0 ≤ m) (hm1 : m ≤ w1) (hm2 : m ≤ w2) :
    m * |x-y| ≤ w1 * |x-t| + w2 * |y-t| := by
  have tri : |x-y| ≤ |x-t| + |y-t| := by
    simpa [abs_sub_comm t y] using abs_sub_le x t y
  have h := mul_le_mul_of_nonneg_left tri hm
  nlinarith [abs_nonneg (x-t), abs_nonneg (y-t)]

theorem diagonal_minimum (w1 w2 x y : ℝ) (h1 : 0 ≤ w1) (h2 : 0 ≤ w2) :
    (∀ t, min w1 w2 * |x-y| ≤ w1 * |x-t| + w2 * |y-t|) ∧
    ∃ t, w1 * |x-t| + w2 * |y-t| = min w1 w2 * |x-y| := by
  constructor
  · intro t
    exact weighted_diagonal_lower w1 w2 (min w1 w2) x y t
      (le_min h1 h2) (min_le_left _ _) (min_le_right _ _)
  · by_cases h : w1 ≤ w2
    · exact ⟨y, by simp [min_eq_left h]⟩
    · exact ⟨x, by simp [min_eq_right (le_of_not_ge h), abs_sub_comm y x]⟩

theorem diagonal_zero_iff (w1 w2 x y : ℝ) (h1 : 0 < w1) (h2 : 0 < w2) :
    min w1 w2 * |x-y| = 0 ↔ x = y := by
  have hm : min w1 w2 ≠ 0 := ne_of_gt (lt_min h1 h2)
  simp [mul_eq_zero, hm, abs_eq_zero, sub_eq_zero]

theorem transport_bound (T : V →ₗ[K] W) (R : Submodule K V) (S : Submodule K W)
    (preserves : ∀ r ∈ R, T r ∈ S) {x y : V} (h : RepairEquivalent R x y) :
    RepairEquivalent S (T x) (T y) := by
  simpa [RepairEquivalent, map_sub] using preserves (x-y) h

/-- Distance to a declared repair set; properness supplies a nearest repair. -/
theorem repair_distance_transport {X Y : Type*} [MetricSpace X] [ProperSpace X]
    [MetricSpace Y] (T : X → Y) (K : NNReal) (lip : LipschitzWith K T)
    (R : Set X) (S : Set Y) (closed : IsClosed R) (inhabited : R.Nonempty)
    (preserves : ∀ r ∈ R, T r ∈ S) (x : X) :
    Metric.infDist (T x) S ≤ (K : ℝ) * Metric.infDist x R := by
  obtain ⟨r,hr,nearest⟩ := closed.exists_infDist_eq_dist inhabited x
  calc
    Metric.infDist (T x) S ≤ dist (T x) (T r) := Metric.infDist_le_dist_of_mem (preserves r hr)
    _ ≤ (K : ℝ) * dist x r := lip.dist_le_mul x r
    _ = (K : ℝ) * Metric.infDist x R := by rw [nearest]

theorem separator_exists (R : Submodule K V) {x : V} (hx : x ∉ R) :
    ∃ phi : V →ₗ[K] K, (∀ r ∈ R, phi r = 0) ∧ phi x ≠ 0 := by
  obtain ⟨phi,hphi,hzero⟩ := R.exists_dual_map_eq_bot_of_notMem hx inferInstance
  refine ⟨phi,?_,hphi⟩
  intro r hr
  have mem : phi r ∈ R.map phi := ⟨r,hr,rfl⟩
  rw [hzero] at mem
  exact mem
end Coda.FOC

