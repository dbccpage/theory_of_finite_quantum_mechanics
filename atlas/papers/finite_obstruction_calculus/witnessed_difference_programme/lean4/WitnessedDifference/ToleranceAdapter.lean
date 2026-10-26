import Mathlib
import WitnessedDifference.EmpiricalModel

/-!
# The tolerant packet adapter

`WDP-CH19-P02` builds an empirical model from a table of measurement packets
when the frequencies agree exactly on every overlap of contexts, and refuses
the table otherwise. The interface `WDP-CH19-O01` stays open for tables whose
frequencies agree only up to sampling error. This module gives the part of that
case that needs no probability model.

* `WDP-CH19-P06`. The signalling defect `pairDefect` of two contexts is the
  `ℓ¹` distance between the two overlap marginals of their weights. The tolerant
  adapter `adaptTol` accepts a table exactly when no context is empty and every
  pairwise defect is at most `ε`, returns the table of frequencies, and
  otherwise names the empty context or the pair whose defect exceeds `ε`. At
  `ε = 0` it accepts exactly the tables the exact adapter accepts, and
  acceptance is monotone in `ε`. If the weights are within `ε` in `ℓ¹`, in every
  context, of a compatible model, then every pairwise defect is at most `2ε`, so
  the defect is a computable necessary test for the sampling hypothesis.
* `WDP-CH19-P07`. On a cover with two contexts the test is also sufficient:
  averaging the two overlap marginals and rescaling the conditionals gives a
  compatible model within `D/2` in `ℓ¹` of each context, where `D` is the
  defect. So a compatible model within `ε` of both contexts exists exactly when
  `D ≤ 2ε`.

The sampling hypothesis here is a declared closeness to a compatible model. It
is not derived from a trial protocol or an independence assumption (§13.6,
§9.9), and covers with three or more contexts are not treated: their exact
distance to the compatible polytope is a linear program. This file declares no
synthetic axioms.
-/

set_option linter.unusedSectionVars false
set_option linter.unusedSimpArgs false

namespace WitnessedDifference.ToleranceAdapter

open Finset WitnessedDifference.Empirical

universe u v w z

/-! ## The signalling defect -/

section Defect

variable {X : Type u} [DecidableEq X] {O : Type v} [Fintype O] [DecidableEq O]
  {ι : Type w}

/-- The `ℓ¹` distance between two weights on the sections of `C`. -/
def l1 {C : Finset X} (p q : (C → O) → ℚ) : ℚ :=
  ∑ s, |p s - q s|

/-- The signalling defect of contexts `i` and `j`: the `ℓ¹` distance between
the marginals of their weights on the overlap. -/
def pairDefect (ctx : ι → Finset X) (w : ∀ i, (ctx i → O) → ℚ) (i j : ι) : ℚ :=
  ∑ t : ↥(ctx i ∩ ctx j) → O,
    |marginal inter_subset_left (w i) t - marginal inter_subset_right (w j) t|

/-- Every pairwise defect is at most `ε`. -/
def IsTolerant (ctx : ι → Finset X) (w : ∀ i, (ctx i → O) → ℚ) (ε : ℚ) : Prop :=
  ∀ i j, pairDefect ctx w i j ≤ ε

theorem pairDefect_nonneg (ctx : ι → Finset X) (w : ∀ i, (ctx i → O) → ℚ)
    (i j : ι) : 0 ≤ pairDefect ctx w i j :=
  Finset.sum_nonneg fun _ _ => abs_nonneg _

theorem pairDefect_eq_zero_iff (ctx : ι → Finset X) (w : ∀ i, (ctx i → O) → ℚ)
    (i j : ι) :
    pairDefect ctx w i j = 0 ↔ ∀ t : ↥(ctx i ∩ ctx j) → O,
      marginal inter_subset_left (w i) t = marginal inter_subset_right (w j) t := by
  unfold pairDefect
  rw [Finset.sum_eq_zero_iff_of_nonneg fun _ _ => abs_nonneg _]
  simp [sub_eq_zero]

/-- At `ε = 0` the tolerance condition is exactly compatibility. -/
theorem isTolerant_zero_iff (ctx : ι → Finset X) (w : ∀ i, (ctx i → O) → ℚ) :
    IsTolerant ctx w 0 ↔ Compatible ctx w := by
  constructor
  · intro h i j t
    exact (pairDefect_eq_zero_iff ctx w i j).1
      (le_antisymm (h i j) (pairDefect_nonneg ctx w i j)) t
  · intro h i j
    exact ((pairDefect_eq_zero_iff ctx w i j).2 (h i j)).le

theorem IsTolerant.mono {ctx : ι → Finset X} {w : ∀ i, (ctx i → O) → ℚ}
    {ε ε' : ℚ} (h : IsTolerant ctx w ε) (hε : ε ≤ ε') : IsTolerant ctx w ε' :=
  fun i j => (h i j).trans hε

theorem marginal_sub {C D : Finset X} (h : D ⊆ C) (p q : (C → O) → ℚ)
    (t : D → O) :
    marginal h p t - marginal h q t =
      ∑ s ∈ univ.filter (fun s => restrict h s = t), (p s - q s) := by
  simp [marginal, Finset.sum_sub_distrib]

/-- Marginalization does not increase the `ℓ¹` distance. -/
theorem l1_marginal_le {C D : Finset X} (h : D ⊆ C) (p q : (C → O) → ℚ) :
    ∑ t : D → O, |marginal h p t - marginal h q t| ≤ l1 p q := by
  calc ∑ t : D → O, |marginal h p t - marginal h q t|
      = ∑ t : D → O, |∑ s ∈ univ.filter (fun s => restrict h s = t), (p s - q s)| := by
        simp_rw [marginal_sub]
    _ ≤ ∑ t : D → O, ∑ s ∈ univ.filter (fun s => restrict h s = t), |p s - q s| :=
        Finset.sum_le_sum fun t _ => Finset.abs_sum_le_sum_abs _ _
    _ = l1 p q := Finset.sum_fiberwise (s := univ) (g := restrict h) (f := fun s => |p s - q s|)

/-- `WDP-CH19-P06`. If the weights are within `ε` in `ℓ¹`, in every context, of
a compatible model, then every pairwise signalling defect is at most `2ε`. -/
theorem tolerant_of_within (ctx : ι → Finset X) (w : ∀ i, (ctx i → O) → ℚ)
    (m : EmpiricalModel ctx O) {ε : ℚ} (hw : ∀ i, l1 (w i) (m.weight i) ≤ ε) :
    IsTolerant ctx w (2 * ε) := by
  intro i j
  unfold pairDefect
  calc ∑ t : ↥(ctx i ∩ ctx j) → O,
        |marginal inter_subset_left (w i) t - marginal inter_subset_right (w j) t|
      ≤ ∑ t : ↥(ctx i ∩ ctx j) → O,
        (|marginal inter_subset_left (w i) t - marginal inter_subset_left (m.weight i) t| +
          |marginal inter_subset_right (w j) t -
            marginal inter_subset_right (m.weight j) t|) := by
        refine Finset.sum_le_sum fun t _ => ?_
        have hc := m.compatible i j t
        have h1 := abs_sub_le (marginal inter_subset_left (w i) t)
          (marginal inter_subset_left (m.weight i) t)
          (marginal inter_subset_right (w j) t)
        have h2 : |marginal inter_subset_left (m.weight i) t -
              marginal inter_subset_right (w j) t| =
            |marginal inter_subset_right (w j) t -
              marginal inter_subset_right (m.weight j) t| := by
          rw [hc, abs_sub_comm]
        rw [h2] at h1
        exact h1
    _ = ∑ t : ↥(ctx i ∩ ctx j) → O,
          |marginal inter_subset_left (w i) t - marginal inter_subset_left (m.weight i) t| +
        ∑ t : ↥(ctx i ∩ ctx j) → O,
          |marginal inter_subset_right (w j) t -
            marginal inter_subset_right (m.weight j) t| := Finset.sum_add_distrib
    _ ≤ ε + ε := add_le_add ((l1_marginal_le _ _ _).trans (hw i))
        ((l1_marginal_le _ _ _).trans (hw j))
    _ = 2 * ε := by ring

end Defect

/-! ## `WDP-CH19-P07`: exact repair on a two-context cover -/

section Repair

variable {S T : Type*} [Fintype S] [Fintype T] [DecidableEq T] [DecidableEq S]

/-- The mass that `p` puts over the point `t` of `T`. -/
def fibreMass (π : S → T) (p : S → ℚ) (t : T) : ℚ :=
  ∑ s ∈ univ.filter (fun s => π s = t), p s

/-- Rescale the conditionals of `p` over each point `t` so that the mass over
`t` becomes `ν t`. Where `p` has no mass over `t`, put `ν t` on the chosen
point `c t`. -/
def repairWeight (π : S → T) (c : T → S) (p : S → ℚ) (ν : T → ℚ) (s : S) : ℚ :=
  (if fibreMass π p (π s) = 0 then 0 else p s * ν (π s) / fibreMass π p (π s)) +
    (if fibreMass π p (π s) = 0 ∧ s = c (π s) then ν (π s) else 0)

theorem sum_fibreMass (π : S → T) (p : S → ℚ) :
    ∑ t, fibreMass π p t = ∑ s, p s :=
  Finset.sum_fiberwise (s := univ) (g := π) (f := p)

theorem repairWeight_nonneg (π : S → T) (c : T → S) {p : S → ℚ}
    (hp : ∀ s, 0 ≤ p s) {ν : T → ℚ} (hν : ∀ t, 0 ≤ ν t) (s : S) :
    0 ≤ repairWeight π c p ν s := by
  unfold repairWeight
  have hm : 0 ≤ fibreMass π p (π s) := Finset.sum_nonneg fun s _ => hp s
  refine add_nonneg ?_ ?_
  · split_ifs
    · exact le_rfl
    · exact div_nonneg (mul_nonneg (hp s) (hν _)) hm
  · split_ifs
    · exact hν _
    · exact le_rfl

theorem fibreMass_repair (π : S → T) (c : T → S) (hc : ∀ t, π (c t) = t)
    {p : S → ℚ} (hp : ∀ s, 0 ≤ p s) (ν : T → ℚ) (t : T) :
    fibreMass π (repairWeight π c p ν) t = ν t := by
  unfold fibreMass repairWeight
  have hfib : ∀ s ∈ univ.filter (fun s => π s = t), π s = t := fun s hs =>
    (Finset.mem_filter.1 hs).2
  rw [Finset.sum_congr rfl fun s hs => by rw [hfib s hs]]
  rw [Finset.sum_add_distrib]
  by_cases hz : ∑ s ∈ univ.filter (fun s => π s = t), p s = 0
  · have hz' : fibreMass π p t = 0 := hz
    simp only [hz', if_true, true_and, Finset.sum_const_zero, zero_add]
    rw [Finset.sum_eq_single (c t)]
    · simp [hc]
    · intro s hs hne
      have := hfib s hs
      simp [this, hne]
    · intro h
      simp [hc] at h
  · have hz' : fibreMass π p t ≠ 0 := hz
    simp only [hz', if_false, false_and, Finset.sum_const_zero, add_zero]
    rw [← Finset.sum_div, ← Finset.sum_mul]
    change fibreMass π p t * ν t / fibreMass π p t = ν t
    field_simp

theorem l1_repair (π : S → T) (c : T → S) (hc : ∀ t, π (c t) = t)
    {p : S → ℚ} (hp : ∀ s, 0 ≤ p s) {ν : T → ℚ} (hν : ∀ t, 0 ≤ ν t) :
    ∑ s, |p s - repairWeight π c p ν s| = ∑ t, |fibreMass π p t - ν t| := by
  rw [← Finset.sum_fiberwise (s := univ) (g := π)
    (f := fun s => |p s - repairWeight π c p ν s|)]
  refine Finset.sum_congr rfl fun t _ => ?_
  have hfib : ∀ s ∈ univ.filter (fun s => π s = t), π s = t := fun s hs =>
    (Finset.mem_filter.1 hs).2
  by_cases hz : fibreMass π p t = 0
  · have hpz : ∀ s ∈ univ.filter (fun s => π s = t), p s = 0 := by
      have := (Finset.sum_eq_zero_iff_of_nonneg fun s _ => hp s).1 hz
      exact this
    have hrw : ∀ s ∈ univ.filter (fun s => π s = t),
        |p s - repairWeight π c p ν s| = if s = c t then ν t else 0 := by
      intro s hs
      have h1 := hfib s hs
      have h2 := hpz s hs
      simp only [repairWeight, h1, h2, hz, if_true, true_and, zero_mul, zero_div,
        zero_add, zero_sub]
      split_ifs
      · rw [abs_neg, abs_of_nonneg (hν t)]
      · simp
    rw [Finset.sum_congr rfl hrw, Finset.sum_eq_single (c t)]
    · rw [hz, if_pos rfl, zero_sub, abs_neg, abs_of_nonneg (hν t)]
    · intro s _ hne
      simp [hne]
    · intro h
      simp [hc] at h
  · have hpos : 0 < fibreMass π p t :=
      lt_of_le_of_ne (Finset.sum_nonneg fun s _ => hp s) (Ne.symm hz)
    have hrw : ∀ s ∈ univ.filter (fun s => π s = t),
        |p s - repairWeight π c p ν s| =
          p s * (|fibreMass π p t - ν t| / fibreMass π p t) := by
      intro s hs
      have h1 := hfib s hs
      simp only [repairWeight, h1, hz, if_false, false_and, add_zero]
      have : p s - p s * ν t / fibreMass π p t =
          p s * ((fibreMass π p t - ν t) / fibreMass π p t) := by
        field_simp
      rw [this, abs_mul, abs_of_nonneg (hp s), abs_div, abs_of_pos hpos]
    rw [Finset.sum_congr rfl hrw, ← Finset.sum_mul]
    change fibreMass π p t * (|fibreMass π p t - ν t| / fibreMass π p t) = _
    field_simp

end Repair

theorem marginal_transport {X : Type u} [DecidableEq X] {O : Type v} [Fintype O]
    [DecidableEq O] {C D D' : Finset X} (e : D = D') (h : D ⊆ C) (h' : D' ⊆ C)
    (p : (C → O) → ℚ) (t : D' → O) :
    marginal h p (fun x => t ⟨x.1, by rw [← e]; exact x.2⟩) = marginal h' p t := by
  subst e
  rfl

section TwoContexts

variable {X : Type u} [DecidableEq X] {O : Type v} [Fintype O] [DecidableEq O]
  [Nonempty O]

/-- Extend an overlap section by the first outcome on the remaining
measurements. -/
noncomputable def extend {C D : Finset X} (h : D ⊆ C) (t : D → O) : C → O :=
  fun x => if hx : x.1 ∈ D then t ⟨x.1, hx⟩ else Classical.arbitrary O

theorem restrict_extend {C D : Finset X} (h : D ⊆ C) (t : D → O) :
    Empirical.restrict h (extend h t) = t := by
  funext x
  simp [Empirical.restrict, extend, x.2]

variable (ctx : Bool → Finset X)

/-- The overlap marginal of context `false`. -/
abbrev mL (w : ∀ i, (ctx i → O) → ℚ) (t : ↥(ctx false ∩ ctx true) → O) : ℚ :=
  marginal (inter_subset_left (s₁ := ctx false) (s₂ := ctx true)) (w false) t

/-- The overlap marginal of context `true`. -/
abbrev mR (w : ∀ i, (ctx i → O) → ℚ) (t : ↥(ctx false ∩ ctx true) → O) : ℚ :=
  marginal (inter_subset_right (s₁ := ctx false) (s₂ := ctx true)) (w true) t

/-- The average of the two overlap marginals. -/
noncomputable def avgMarginal (w : ∀ i, (ctx i → O) → ℚ)
    (t : ↥(ctx false ∩ ctx true) → O) : ℚ :=
  (mL ctx w t + mR ctx w t) / 2

/-- The repaired weight of context `i`: rescale to the average overlap
marginal. -/
noncomputable def repair2 (w : ∀ i, (ctx i → O) → ℚ) :
    ∀ i, (ctx i → O) → ℚ
  | false => repairWeight
      (Empirical.restrict (inter_subset_left (s₁ := ctx false) (s₂ := ctx true)))
      (extend inter_subset_left) (w false) (avgMarginal ctx w)
  | true => repairWeight
      (Empirical.restrict (inter_subset_right (s₁ := ctx false) (s₂ := ctx true)))
      (extend inter_subset_right) (w true) (avgMarginal ctx w)

theorem sum_avgMarginal (w : ∀ i, (ctx i → O) → ℚ)
    (hn : ∀ i, ∑ s, w i s = 1) : ∑ t, avgMarginal ctx w t = 1 := by
  have e0 : ∑ t, mL ctx w t = 1 :=
    (sum_fibreMass (Empirical.restrict
      (inter_subset_left (s₁ := ctx false) (s₂ := ctx true))) (w false)).trans (hn false)
  have e1 : ∑ t, mR ctx w t = 1 :=
    (sum_fibreMass (Empirical.restrict
      (inter_subset_right (s₁ := ctx false) (s₂ := ctx true))) (w true)).trans (hn true)
  simp only [avgMarginal, ← Finset.sum_div, Finset.sum_add_distrib, e0, e1]
  norm_num

/-- `WDP-CH19-P07`. On a cover with two contexts and nonempty outcomes, a table
of nonnegative normalized weights has a compatible model whose weight in each
context is at `ℓ¹` distance exactly `D/2`, where `D` is the signalling
defect. -/
theorem exists_repair (w : ∀ i, (ctx i → O) → ℚ) (hw : ∀ i s, 0 ≤ w i s)
    (hn : ∀ i, ∑ s, w i s = 1) :
    ∃ m : EmpiricalModel ctx O,
      ∀ i, l1 (w i) (m.weight i) = pairDefect ctx w false true / 2 := by
  have hμ0 : ∀ t : ↥(ctx false ∩ ctx true) → O, 0 ≤ mL ctx w t := fun t =>
    Finset.sum_nonneg fun s _ => hw false s
  have hμ1 : ∀ t : ↥(ctx false ∩ ctx true) → O, 0 ≤ mR ctx w t := fun t =>
    Finset.sum_nonneg fun s _ => hw true s
  have hν : ∀ t : ↥(ctx false ∩ ctx true) → O, 0 ≤ avgMarginal ctx w t := fun t => by
    have := hμ0 t
    have := hμ1 t
    unfold avgMarginal
    positivity
  have hc0 : ∀ t : ↥(ctx false ∩ ctx true) → O, Empirical.restrict (inter_subset_left (s₁ := ctx false) (s₂ := ctx true))
      (extend (inter_subset_left (s₁ := ctx false) (s₂ := ctx true)) t) = t :=
    fun t => restrict_extend _ t
  have hc1 : ∀ t : ↥(ctx false ∩ ctx true) → O, Empirical.restrict (inter_subset_right (s₁ := ctx false) (s₂ := ctx true))
      (extend (inter_subset_right (s₁ := ctx false) (s₂ := ctx true)) t) = t :=
    fun t => restrict_extend _ t
  have hm0 : ∀ t : ↥(ctx false ∩ ctx true) → O, fibreMass (Empirical.restrict (inter_subset_left (s₁ := ctx false) (s₂ := ctx true)))
      (repair2 ctx w false) t = avgMarginal ctx w t := fun t =>
    fibreMass_repair _ _ hc0 (hw false) _ t
  have hm1 : ∀ t : ↥(ctx false ∩ ctx true) → O, fibreMass (Empirical.restrict (inter_subset_right (s₁ := ctx false) (s₂ := ctx true)))
      (repair2 ctx w true) t = avgMarginal ctx w t := fun t =>
    fibreMass_repair _ _ hc1 (hw true) _ t
  have hnn : ∀ i s, 0 ≤ repair2 ctx w i s := by
    intro i s
    cases i
    · exact repairWeight_nonneg _ _ (hw false) hν s
    · exact repairWeight_nonneg _ _ (hw true) hν s
  have hsum : ∀ i, ∑ s, repair2 ctx w i s = 1 := by
    intro i
    cases i
    · rw [← Finset.sum_fiberwise (s := univ) (g := restrict (inter_subset_left
        (s₁ := ctx false) (s₂ := ctx true)))]
      change ∑ t, fibreMass _ (repair2 ctx w false) t = 1
      simp_rw [hm0]
      exact sum_avgMarginal ctx w hn
    · rw [← Finset.sum_fiberwise (s := univ) (g := restrict (inter_subset_right
        (s₁ := ctx false) (s₂ := ctx true)))]
      change ∑ t, fibreMass _ (repair2 ctx w true) t = 1
      simp_rw [hm1]
      exact sum_avgMarginal ctx w hn
  have hcomp : Compatible ctx (repair2 ctx w) := by
    intro i j t
    cases i <;> cases j
    · rfl
    · exact (hm0 t).trans (hm1 t).symm
    · have e : ctx true ∩ ctx false = ctx false ∩ ctx true := Finset.inter_comm _ _
      let t' : ↥(ctx false ∩ ctx true) → O := fun x => t ⟨x.1, by rw [e]; exact x.2⟩
      have ht : t = fun x => t' ⟨x.1, by rw [← e]; exact x.2⟩ := rfl
      rw [ht, marginal_transport e inter_subset_left inter_subset_right,
        marginal_transport e inter_subset_right inter_subset_left]
      exact (hm1 t').trans (hm0 t').symm
    · rfl
  refine ⟨⟨repair2 ctx w, hnn, hsum, hcomp⟩, ?_⟩
  have hD : pairDefect ctx w false true = ∑ t, |mL ctx w t - mR ctx w t| := rfl
  intro i
  cases i
  · unfold l1
    change ∑ s, |w false s - repairWeight _ _ (w false) (avgMarginal ctx w) s| = _
    rw [l1_repair _ _ hc0 (hw false) hν, hD, Finset.sum_div]
    refine Finset.sum_congr rfl fun t _ => ?_
    change |mL ctx w t - avgMarginal ctx w t| = _
    unfold avgMarginal
    rw [show mL ctx w t - (mL ctx w t + mR ctx w t) / 2 =
        (mL ctx w t - mR ctx w t) / 2 by ring, abs_div]
    norm_num
  · unfold l1
    change ∑ s, |w true s - repairWeight _ _ (w true) (avgMarginal ctx w) s| = _
    rw [l1_repair _ _ hc1 (hw true) hν, hD, Finset.sum_div]
    refine Finset.sum_congr rfl fun t _ => ?_
    change |mR ctx w t - avgMarginal ctx w t| = _
    unfold avgMarginal
    rw [show mR ctx w t - (mL ctx w t + mR ctx w t) / 2 =
        (mR ctx w t - mL ctx w t) / 2 by ring, abs_div, abs_sub_comm]
    norm_num

/-- `WDP-CH19-P07`, bundled. On a two-context cover a compatible model within
`ε` in `ℓ¹` of every context exists exactly when the signalling defect is at
most `2ε`. -/
theorem two_context_tolerance_iff (w : ∀ i, (ctx i → O) → ℚ) (hw : ∀ i s, 0 ≤ w i s)
    (hn : ∀ i, ∑ s, w i s = 1) (ε : ℚ) :
    (∃ m : EmpiricalModel ctx O, ∀ i, l1 (w i) (m.weight i) ≤ ε) ↔
      pairDefect ctx w false true ≤ 2 * ε := by
  constructor
  · rintro ⟨m, hm⟩
    exact tolerant_of_within ctx w m hm false true
  · intro h
    obtain ⟨m, hm⟩ := exists_repair ctx w hw hn
    exact ⟨m, fun i => by rw [hm i]; linarith⟩

end TwoContexts

/-! ## The typed tolerant adapter -/

section Adapter

variable {X : Type u} [DecidableEq X] {O : Type v} [Fintype O] [DecidableEq O]
  {ι : Type w} {P : Type z} {admissible : X → P → Prop} (readout : X → P → O)

/-- Why the tolerant adapter declines a table. -/
inductive TolRefusal (ctx : ι → Finset X)
    (T : ∀ i, List (Run P admissible (ctx i))) (ε : ℚ) : Type (max u v w)
  /-- Context `i` has no runs, so it has no frequencies. -/
  | emptyContext (i : ι) (empty : T i = [])
  /-- The frequencies of contexts `i` and `j` disagree on their overlap by more
  than `ε` in `ℓ¹`. -/
  | excessSignalling (i j : ι)
      (excess : ε < pairDefect ctx (freqs readout ctx T) i j)

/-- What the tolerant adapter returns: the frequencies of a table in which no
context is empty and every pairwise defect is at most `ε`. It is a model only
up to `ε`: its overlap marginals need not agree. -/
structure TolerantModel (ctx : ι → Finset X) (O : Type v) [Fintype O]
    [DecidableEq O] (ε : ℚ) where
  weight : ∀ i, (ctx i → O) → ℚ
  nonneg : ∀ i s, 0 ≤ weight i s
  normalized : ∀ i, ∑ s, weight i s = 1
  tolerant : IsTolerant ctx weight ε

open Classical in
/-- The tolerant map from run tables on a declared cover. -/
noncomputable def adaptTol (ctx : ι → Finset X)
    (T : ∀ i, List (Run P admissible (ctx i))) (ε : ℚ) :
    TolRefusal readout ctx T ε ⊕ TolerantModel ctx O ε :=
  if h : ∃ i, T i = [] then .inl (.emptyContext h.choose h.choose_spec)
  else if hc : IsTolerant ctx (freqs readout ctx T) ε then
    .inr
      { weight := freqs readout ctx T
        nonneg := fun i s => freq_nonneg readout (T i) s
        normalized := fun i => sum_freq readout (T i) fun he => h ⟨i, he⟩
        tolerant := hc }
  else
    have h2 : ∃ i j, ε < pairDefect ctx (freqs readout ctx T) i j := by
      simpa [IsTolerant, not_forall, not_le] using hc
    .inl (.excessSignalling h2.choose h2.choose_spec.choose
      h2.choose_spec.choose_spec)

/-- The tolerant adapter returns `m` exactly when no context is empty and `m`
is the table of frequencies. -/
theorem adaptTol_eq_inr_iff (ctx : ι → Finset X)
    (T : ∀ i, List (Run P admissible (ctx i))) (ε : ℚ)
    (m : TolerantModel ctx O ε) :
    adaptTol readout ctx T ε = .inr m ↔
      (∀ i, T i ≠ []) ∧ m.weight = freqs readout ctx T := by
  unfold adaptTol
  split_ifs with h hc
  · simp only [false_iff, not_and]
    obtain ⟨i, hi⟩ := h
    exact fun hne => absurd hi (hne i)
  · constructor
    · intro hm
      have hw : (⟨freqs readout ctx T, fun i s => freq_nonneg readout (T i) s,
          fun i => sum_freq readout (T i) fun he => h ⟨i, he⟩, hc⟩ :
            TolerantModel ctx O ε) = m := Sum.inr.inj hm
      exact ⟨fun i he => h ⟨i, he⟩, by rw [← hw]⟩
    · rintro ⟨_, hw⟩
      congr 1
      cases m
      simp only at hw
      subst hw
      rfl
  · simp only [false_iff, not_and]
    intro _ hw
    exact hc (hw ▸ m.tolerant)

/-- The tolerant adapter succeeds exactly when no context is empty and every
pairwise defect of the frequencies is at most `ε`. -/
theorem adaptTol_succeeds_iff (ctx : ι → Finset X)
    (T : ∀ i, List (Run P admissible (ctx i))) (ε : ℚ) :
    (∃ m, adaptTol readout ctx T ε = .inr m) ↔
      (∀ i, T i ≠ []) ∧ IsTolerant ctx (freqs readout ctx T) ε := by
  constructor
  · rintro ⟨m, hm⟩
    obtain ⟨hne, hw⟩ := (adaptTol_eq_inr_iff readout ctx T ε m).1 hm
    exact ⟨hne, hw ▸ m.tolerant⟩
  · rintro ⟨hne, hc⟩
    exact ⟨⟨freqs readout ctx T, fun i s => freq_nonneg readout (T i) s,
      fun i => sum_freq readout (T i) (hne i), hc⟩,
      (adaptTol_eq_inr_iff readout ctx T ε _).2 ⟨hne, rfl⟩⟩

/-- Acceptance is monotone in the tolerance. -/
theorem adaptTol_mono (ctx : ι → Finset X)
    (T : ∀ i, List (Run P admissible (ctx i))) {ε ε' : ℚ} (hε : ε ≤ ε') :
    (∃ m, adaptTol readout ctx T ε = .inr m) →
      ∃ m, adaptTol readout ctx T ε' = .inr m := by
  intro h
  obtain ⟨hne, ht⟩ := (adaptTol_succeeds_iff readout ctx T ε).1 h
  exact (adaptTol_succeeds_iff readout ctx T ε').2 ⟨hne, ht.mono hε⟩

/-- `WDP-CH19-P06`. At tolerance `0` the tolerant adapter accepts exactly the
tables that the exact adapter of `WDP-CH19-P02` accepts, with the same
frequencies. -/
theorem adaptTol_zero_iff_adapt (ctx : ι → Finset X)
    (T : ∀ i, List (Run P admissible (ctx i))) :
    (∃ m, adaptTol readout ctx T 0 = .inr m) ↔
      ∃ m, adapt readout ctx T = .inr m := by
  rw [adaptTol_succeeds_iff, adapt_succeeds_iff, isTolerant_zero_iff]

/-- `WDP-CH19-P06`, bundled. -/
theorem tolerant_adapter_signature (ctx : ι → Finset X)
    (T : ∀ i, List (Run P admissible (ctx i))) :
    ((∃ m, adaptTol readout ctx T 0 = .inr m) ↔ ∃ m, adapt readout ctx T = .inr m) ∧
      (∀ ε ε' : ℚ, ε ≤ ε' → (∃ m, adaptTol readout ctx T ε = .inr m) →
        ∃ m, adaptTol readout ctx T ε' = .inr m) ∧
      (∀ (m : EmpiricalModel ctx O) (ε : ℚ),
        (∀ i, l1 (freqs readout ctx T i) (m.weight i) ≤ ε) →
          IsTolerant ctx (freqs readout ctx T) (2 * ε)) :=
  ⟨adaptTol_zero_iff_adapt readout ctx T, fun _ _ h => adaptTol_mono readout ctx T h,
    fun m _ h => tolerant_of_within ctx _ m h⟩

end Adapter

end WitnessedDifference.ToleranceAdapter
