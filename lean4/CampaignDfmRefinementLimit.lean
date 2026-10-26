import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Topology.Algebra.Group.Basic
import Mathlib.Topology.UniformSpace.UniformApproximation
import Mathlib.Tactic.Group
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Algebra.Group.TypeTags.Basic

/-! Controlled binary refinement of ordered group transport.
AuthorityEffect: None. The complete metric, refinement family and decay estimate
are supplied. Continuity of a limit does not assert smoothness or field dynamics.
-/
namespace CampaignDfmRefinementLimit
open Filter
open scoped Topology
abbrev Word := List Bool

variable {G : Type*} [Group G]

/-- Right-after-left composition, matching the repository's path convention. -/
def transport (U : Word → G) : ℕ → Word → G
  | 0, p => U p
  | n + 1, p => transport U n (true :: p) * transport U n (false :: p)

/-- Endpoint gauges agree at the new midpoint and preserve the old endpoints. -/
structure EndpointGauge (G : Type*) [Group G] where
  start : Word → G
  finish : Word → G
  start_left : ∀ p, start (false :: p) = start p
  finish_right : ∀ p, finish (true :: p) = finish p
  midpoint : ∀ p, start (true :: p) = finish (false :: p)

def EndpointGauge.dress (g : EndpointGauge G) (U : Word → G) (p : Word) : G :=
  (g.finish p)⁻¹ * U p * g.start p

theorem transport_dress (g : EndpointGauge G) (U : Word → G) (n : ℕ) (p : Word) :
    transport (g.dress U) n p = (g.finish p)⁻¹ * transport U n p * g.start p := by
  induction n generalizing p with
  | zero => rfl
  | succ n ih =>
    simp only [transport, ih, g.start_left, g.finish_right, g.midpoint]
    group

section Metric
variable [MetricSpace G]
variable (hmul : ∀ a b c d : G, dist (a * b) (c * d) ≤ dist a c + dist b d)
include hmul

/-- A uniform bound on each split accumulates over exactly the binary leaf count. -/
theorem step_bound (U : Word → G) (C q : ℝ)
    (hs : ∀ p, dist (U p) (U (true :: p) * U (false :: p)) ≤ C * q ^ p.length)
    (n : ℕ) (p : Word) :
    dist (transport U n p) (transport U (n + 1) p) ≤
      (C * q ^ p.length) * (2 * q) ^ n := by
  induction n generalizing p with
  | zero => simpa [transport] using hs p
  | succ n ih =>
    calc
      _ ≤ dist (transport U n (true :: p)) (transport U (n+1) (true :: p)) +
          dist (transport U n (false :: p)) (transport U (n+1) (false :: p)) :=
        hmul _ _ _ _
      _ ≤ (C * q ^ (true :: p).length) * (2*q)^n +
          (C * q ^ (false :: p).length) * (2*q)^n := add_le_add (ih _) (ih _)
      _ = _ := by simp only [List.length_cons, pow_succ]; ring

structure Controlled (G : Type*) [Group G] [MetricSpace G] where
  edge : Word → G
  C : ℝ
  q : ℝ
  C_nonneg : 0 ≤ C
  q_nonneg : 0 ≤ q
  decay : 2 * q < 1
  split_bound : ∀ p, dist (edge p) (edge (true :: p) * edge (false :: p)) ≤ C * q ^ p.length

variable [CompleteSpace G]

theorem Controlled.exists_limit (U : Controlled G) (p : Word) :
    ∃ a : G, Tendsto (fun n => transport U.edge n p) atTop (𝓝 a) :=
  cauchySeq_tendsto_of_complete
    (cauchySeq_of_le_geometric (2*U.q) (U.C*U.q^p.length) U.decay
      (fun n => step_bound hmul U.edge U.C U.q U.split_bound n p))

noncomputable def Controlled.limit (U : Controlled G) (p : Word) : G :=
  (U.exists_limit hmul p).choose

theorem Controlled.tendsto_limit (U : Controlled G) (p : Word) :
    Tendsto (fun n => transport U.edge n p) atTop (𝓝 (U.limit hmul p)) :=
  (U.exists_limit hmul p).choose_spec

theorem Controlled.error_bound (U : Controlled G) (p : Word) (n : ℕ) :
    dist (transport U.edge n p) (U.limit hmul p) ≤
      (U.C * U.q ^ p.length) * (2*U.q)^n / (1-2*U.q) :=
  dist_le_of_le_geometric_of_tendsto (2*U.q) (U.C*U.q^p.length) U.decay
    (fun n => step_bound hmul U.edge U.C U.q U.split_bound n p)
    (U.tendsto_limit hmul p) n

theorem Controlled.limit_unique (U : Controlled G) (p : Word) (a : G)
    (ha : Tendsto (fun n => transport U.edge n p) atTop (𝓝 a)) :
    a = U.limit hmul p := tendsto_nhds_unique ha (U.tendsto_limit hmul p)

variable [IsTopologicalGroup G]

theorem Controlled.limit_split (U : Controlled G) (p : Word) :
    U.limit hmul p = U.limit hmul (true :: p) * U.limit hmul (false :: p) := by
  apply tendsto_nhds_unique
    ((tendsto_add_atTop_iff_nat 1).2 (U.tendsto_limit hmul p))
  exact (U.tendsto_limit hmul (true :: p)).mul (U.tendsto_limit hmul (false :: p))

theorem Controlled.dressed_tendsto (U : Controlled G) (g : EndpointGauge G) (p : Word) :
    Tendsto (fun n => transport (g.dress U.edge) n p) atTop
      (𝓝 ((g.finish p)⁻¹ * U.limit hmul p * g.start p)) := by
  simp only [transport_dress]
  exact (tendsto_const_nhds.mul (U.tendsto_limit hmul p)).mul tendsto_const_nhds

omit [IsTopologicalGroup G] in
/-- A uniform geometric envelope makes the parameterwise limit uniform. -/
theorem uniform_refinement_limit {X : Type*} (U : X → Controlled G)
    (C q : ℝ) (hC : ∀ x, (U x).C = C) (hq : ∀ x, (U x).q = q)
    (hq0 : 0 ≤ q) (hq1 : 2*q < 1) (p : Word) :
    TendstoUniformly (fun n x => transport (U x).edge n p)
      (fun x => (U x).limit hmul p) atTop := by
  rw [Metric.tendstoUniformly_iff]
  intro ε hε
  have ht : Tendsto (fun n : ℕ => (C*q^p.length)*(2*q)^n/(1-2*q)) atTop (𝓝 0) := by
    simpa using ((tendsto_const_nhds.mul
      (tendsto_pow_atTop_nhds_zero_of_lt_one (by positivity : 0 ≤ 2*q) hq1)).div_const
      (1-2*q) : Tendsto (fun n : ℕ => (C*q^p.length)*(2*q)^n/(1-2*q)) atTop
      (𝓝 ((C*q^p.length)*0/(1-2*q))))
  filter_upwards [ht.eventually (gt_mem_nhds hε)] with n hn
  intro x
  rw [dist_comm]
  have hb := (U x).error_bound hmul p n
  rw [hC x, hq x] at hb
  exact hb.trans_lt hn

omit hmul [CompleteSpace G] in
theorem continuous_transport {X : Type*} [TopologicalSpace X]
    (U : X → Word → G) (hc : ∀ p, Continuous (fun x => U x p)) (n : ℕ) (p : Word) :
    Continuous (fun x => transport (U x) n p) := by
  induction n generalizing p with
  | zero => exact hc p
  | succ n ih => exact (ih (true :: p)).mul (ih (false :: p))

/-- Continuity is obtained from continuous finite data and a uniform error bound. -/
theorem continuous_refinement_limit {X : Type*} [TopologicalSpace X]
    (U : X → Controlled G) (hc : ∀ p, Continuous (fun x => (U x).edge p))
    (C q : ℝ) (hC : ∀ x, (U x).C = C) (hq : ∀ x, (U x).q = q)
    (hq0 : 0 ≤ q) (hq1 : 2*q < 1) (p : Word) :
    Continuous (fun x => (U x).limit hmul p) :=
  (uniform_refinement_limit hmul U C q hC hq hq0 hq1 p).continuous
    (Filter.Eventually.frequently (Filter.Eventually.of_forall
      (fun n => continuous_transport (fun x => (U x).edge) hc n p)))

end Metric
/-- At the excluded threshold q=1/2, each leaf error shrinks but the total diverges. -/
noncomputable def criticalEdge (p : Word) : Multiplicative ℝ :=
  Multiplicative.ofAdd ((p.length : ℝ) / (2:ℝ)^p.length)

theorem critical_transport (n : ℕ) (p : Word) :
    Multiplicative.toAdd (transport criticalEdge n p) =
      ((p.length : ℝ) + n) / (2:ℝ)^p.length := by
  induction n generalizing p with
  | zero => simp [transport, criticalEdge]
  | succ n ih =>
    simp only [transport, toAdd_mul, ih, List.length_cons, Nat.cast_add,
      Nat.cast_one, pow_succ]
    field_simp
    ring

theorem critical_split_defect (p : Word) :
    |Multiplicative.toAdd (criticalEdge p) -
      Multiplicative.toAdd (criticalEdge (true :: p) * criticalEdge (false :: p))| =
      (1/2:ℝ)^p.length := by
  have h : Multiplicative.toAdd (criticalEdge p) -
      Multiplicative.toAdd (criticalEdge (true :: p) * criticalEdge (false :: p)) =
      -(1 / (2:ℝ)^p.length) := by
    simp [criticalEdge, pow_succ]
    field_simp
    ring
  rw [h, abs_neg, abs_of_nonneg (by positivity)]
  simp

theorem critical_no_limit :
    ¬ ∃ a : ℝ, Tendsto (fun n => Multiplicative.toAdd (transport criticalEdge n []))
      atTop (𝓝 a) := by
  rintro ⟨a, ha⟩
  simp only [critical_transport, List.length_nil, Nat.cast_zero, zero_add, pow_zero, div_one] at ha
  have hshift := (tendsto_add_atTop_iff_nat 1).2 ha
  have hdiff := hshift.sub ha
  have hone : Tendsto (fun _ : ℕ => (1:ℝ)) atTop (𝓝 0) := by
    convert hdiff using 1 <;> simp
  have heq : (1:ℝ) = 0 := tendsto_nhds_unique tendsto_const_nhds hone
  norm_num at heq

#print axioms critical_transport
#print axioms critical_split_defect
#print axioms critical_no_limit

#print axioms uniform_refinement_limit
#print axioms continuous_refinement_limit
#print axioms step_bound
#print axioms Controlled.exists_limit
#print axioms Controlled.error_bound
#print axioms Controlled.limit_split
#print axioms Controlled.dressed_tendsto
end CampaignDfmRefinementLimit
