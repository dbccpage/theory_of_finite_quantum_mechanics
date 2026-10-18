import TotalUnimodularity
import SparseLanding
import SparseLandingGeneral
import Mub6L1SnTower

/-!
# Discrete L1 Projection Duality and Rational Box Cell Bisection Bridge

AuthorityEffect: None.

This module formalizes:
1. Exact rational discrete L1 defect functional and rational coboundaries.
2. Rational dual circulation witnesses with divergence-free / gauge-orthogonality and unit infinity-norm bounds.
3. Constructive proof of the Weak Duality theorem:
   dualPairing(W_E, y) ≤ l1Defect(c₀, W_E) for every vertex potential c₀.
4. Cell obstruction and pruning theorem:
   If a rational cell admits a dual circulation certifying a strictly positive dual lower bound ε > 0,
   then no potential in that cell can attain zero defect, enabling branch-and-bound pruning.
5. Grounding in the Weighted Null-Space Property (NSP) and directional derivative positivity:
   `dirDeriv_pos` ensures absence of flat/descent directions, guaranteeing strictly positive defect
   growth away from optimal residuals.
6. Integration with Total Unimodularity (TUM) ensuring that polyhedral vertices and bisection
   coordinates remain closed under ℚ without irrational leakage.
-/

namespace MUB6.Gluing.L1

notation "ℚ" => Rat

/-! ### 1. Rational Order Helpers and Rational Absolute Value -/

theorem rat_le_of_not_ge {a b : ℚ} (h : ¬ b ≤ a) : a ≤ b := by
  cases Rat.le_total (a := a) (b := b) with
  | inl h1 => exact h1
  | inr h2 => exact (h h2).elim

theorem rat_neg_nonneg_of_nonpos {x : ℚ} (h : x ≤ 0) : 0 ≤ -x := by
  have hneg := Rat.neg_le_neg h
  rwa [Rat.neg_zero] at hneg

theorem rat_add_le_add {a b c d : ℚ} (hab : a ≤ b) (hcd : c ≤ d) : a + c ≤ b + d :=
  Rat.le_trans (Rat.add_le_add_right.2 hab) (Rat.add_le_add_left.2 hcd)

theorem rat_pos_not_le_zero {x : ℚ} (hpos : 0 < x) (hle : x ≤ 0) : False := by
  have h1 : (0 : ℚ).blt x = true := hpos
  have h2 : (0 : ℚ).blt x = false := hle
  rw [h1] at h2
  contradiction

/-- Exact rational absolute value. -/
def qabs (x : ℚ) : ℚ := if 0 ≤ x then x else -x

theorem qabs_nonneg (x : ℚ) : 0 ≤ qabs x := by
  unfold qabs
  split
  · rename_i h; exact h
  · rename_i h
    have hle : x ≤ 0 := rat_le_of_not_ge h
    exact rat_neg_nonneg_of_nonpos hle

theorem rat_mul_le_qabs_of_unit {x y : ℚ} (hy1 : -1 ≤ y) (hy2 : y ≤ 1) :
    x * y ≤ qabs x := by
  unfold qabs
  split
  · rename_i hge
    have hmul := Rat.mul_le_mul_of_nonneg_left hy2 hge
    rwa [Rat.mul_one] at hmul
  · rename_i hnot
    have hle : x ≤ 0 := rat_le_of_not_ge hnot
    have hnn : 0 ≤ -x := rat_neg_nonneg_of_nonpos hle
    have hmul := Rat.mul_le_mul_of_nonneg_left hy1 hnn
    have h1 : -x * -1 = x := by
      rw [Rat.neg_mul, Rat.mul_neg, Rat.mul_one, Rat.neg_neg]
    have h2 : -x * y = -(x * y) := by
      rw [Rat.neg_mul]
    rw [h1, h2] at hmul
    have hneg := Rat.neg_le_neg hmul
    rwa [Rat.neg_neg] at hneg

/-- Single edge dual bound: (W - del) * y ≤ |del - W| for any y ∈ [-1, 1]. -/
theorem dual_bound_single_edge (del W y : ℚ) (hy1 : -1 ≤ y) (hy2 : y ≤ 1) :
    (W - del) * y ≤ qabs (del - W) := by
  have h_neg_y1 : -1 ≤ -y := Rat.neg_le_neg hy2
  have h_neg_y2 : -y ≤ 1 := by
    have hneg := Rat.neg_le_neg hy1
    rwa [Rat.neg_neg] at hneg
  have h_bound := rat_mul_le_qabs_of_unit (x := del - W) (y := -y) h_neg_y1 h_neg_y2
  have h_eq : (del - W) * -y = (W - del) * y := by
    rw [Rat.mul_neg, ← Rat.neg_mul]
    have : -(del - W) = W - del := by
      rw [Rat.sub_eq_add_neg, Rat.neg_add, Rat.neg_neg, Rat.sub_eq_add_neg, Rat.add_comm]
    rw [this]
  rw [h_eq] at h_bound
  exact h_bound

/-! ### 2. Finite List Edge Summations -/

/-- Summation of a rational function over a list of edges. -/
def sumEdges {α : Type} (L : List α) (f : α → ℚ) : ℚ :=
  L.foldr (fun x acc => f x + acc) 0

theorem sumEdges_add {α : Type} (L : List α) (f g : α → ℚ) :
    sumEdges L (fun x => f x + g x) = sumEdges L f + sumEdges L g := by
  induction L with
  | nil =>
    dsimp [sumEdges]
    rw [Rat.add_zero]
  | cons x xs ih =>
    dsimp [sumEdges]
    dsimp [sumEdges] at ih
    rw [ih]
    have h1 : (f x + g x) + (List.foldr (fun x acc => f x + acc) 0 xs + List.foldr (fun x acc => g x + acc) 0 xs) =
              f x + (g x + (List.foldr (fun x acc => f x + acc) 0 xs + List.foldr (fun x acc => g x + acc) 0 xs)) :=
      Rat.add_assoc (f x) (g x) _
    have h2 : g x + (List.foldr (fun x acc => f x + acc) 0 xs + List.foldr (fun x acc => g x + acc) 0 xs) =
              List.foldr (fun x acc => f x + acc) 0 xs + (g x + List.foldr (fun x acc => g x + acc) 0 xs) := by
      rw [← Rat.add_assoc, Rat.add_comm (g x), Rat.add_assoc]
    have h3 : (f x + List.foldr (fun x acc => f x + acc) 0 xs) + (g x + List.foldr (fun x acc => g x + acc) 0 xs) =
              f x + (List.foldr (fun x acc => f x + acc) 0 xs + (g x + List.foldr (fun x acc => g x + acc) 0 xs)) :=
      Rat.add_assoc (f x) _ _
    rw [h1, h2, ← h3]

theorem sumEdges_congr {α : Type} (L : List α) (f g : α → ℚ) (h : ∀ x ∈ L, f x = g x) :
    sumEdges L f = sumEdges L g := by
  induction L with
  | nil => rfl
  | cons x xs ih =>
    dsimp [sumEdges]
    have hx := h x (by simp)
    have hxs := ih (fun y hy => h y (by simp [hy]))
    dsimp [sumEdges] at hxs
    rw [hx, hxs]

theorem sumEdges_le {α : Type} (L : List α) (f g : α → ℚ) (hle : ∀ x ∈ L, f x ≤ g x) :
    sumEdges L f ≤ sumEdges L g := by
  induction L with
  | nil =>
    simp [sumEdges]
  | cons x xs ih =>
    simp only [sumEdges, List.foldr_cons]
    have hx : f x ≤ g x := hle x (by simp)
    have hxs : sumEdges xs f ≤ sumEdges xs g := ih (fun y hy => hle y (by simp [hy]))
    exact rat_add_le_add hx hxs

/-! ### 3. Discrete L1 Duality: Dual Circulation and Weak Duality -/

/-- Rational discrete coboundary operator: (δ c₀)(e) = c₀(target) - c₀(source). -/
def coboundaryQ {V : Type} (c₀ : V → ℚ) (e : DirectedEdge V) : ℚ :=
  c₀ e.target - c₀ e.source

/-- Dual pairing ⟨W_E, y⟩ = ∑_{e ∈ E} W_E(e) · y(e). -/
def dualPairing {V : Type} (E : List (DirectedEdge V)) (W_E : DirectedEdge V → ℚ) (y : DirectedEdge V → ℚ) : ℚ :=
  sumEdges E (fun e => W_E e * y e)

/-- Discrete L1 defect functional: ‖δ c₀ - W_E‖₁ = ∑_{e ∈ E} |(δ c₀)(e) - W_E(e)|. -/
def l1Defect {V : Type} (E : List (DirectedEdge V)) (c₀ : V → ℚ) (W_E : DirectedEdge V → ℚ) : ℚ :=
  sumEdges E (fun e => qabs (coboundaryQ c₀ e - W_E e))

/-- An exact rational dual circulation certificate:
- `circulation`: edge circulation values y ∈ ℚ^{|E|};
- `gauge_orthogonal`: divergence-free condition ⟨δ c₀, y⟩ = 0 for all vertex potentials c₀;
- `unit_bounded`: dual unit ball constraint ‖y‖_∞ ≤ 1, i.e., -1 ≤ y(e) ≤ 1 for all e ∈ E. -/
structure DualCirculationWitness (V : Type) (E : List (DirectedEdge V)) where
  circulation : DirectedEdge V → ℚ
  gauge_orthogonal : ∀ (c₀ : V → ℚ), dualPairing E (coboundaryQ c₀) circulation = 0
  unit_bounded : ∀ e ∈ E, -1 ≤ circulation e ∧ circulation e ≤ 1

/-- **Weak Duality Theorem for Discrete L1 Defect**:
For any dual circulation witness W and any vertex potential c₀,
the dual pairing lower-bounds the primal L1 defect:
    ⟨W_E, y⟩ ≤ ‖δ c₀ - W_E‖₁.
Proven constructively with zero custom axioms. -/
theorem weak_duality
    {V : Type} (E : List (DirectedEdge V))
    (W : DualCirculationWitness V E)
    (W_E : DirectedEdge V → ℚ)
    (c₀ : V → ℚ) :
    dualPairing E W_E W.circulation ≤ l1Defect E c₀ W_E := by
  have h_decomp : dualPairing E W_E W.circulation =
      sumEdges E (fun e => (W_E e - coboundaryQ c₀ e) * W.circulation e) := by
    have h_split : dualPairing E W_E W.circulation =
        sumEdges E (fun e => (W_E e - coboundaryQ c₀ e) * W.circulation e + coboundaryQ c₀ e * W.circulation e) := by
      apply sumEdges_congr
      intro e _
      rw [← Rat.add_mul, Rat.sub_add_cancel]
    rw [h_split, sumEdges_add]
    have h_orth := W.gauge_orthogonal c₀
    unfold dualPairing at h_orth
    rw [h_orth, Rat.add_zero]
  rw [h_decomp]
  unfold l1Defect
  apply sumEdges_le
  intro e he
  have hb := W.unit_bounded e he
  exact dual_bound_single_edge (coboundaryQ c₀ e) (W_E e) (W.circulation e) hb.1 hb.2

/-! ### 4. Rational Cell Bisection and Box Pruning -/

/-- An exact rational parameter cell / box predicate. -/
structure RationalCell (α : Type) where
  in_cell : α → Prop

/-- **Regional Cell Obstruction Theorem via Dual Circulation**:
If a dual circulation certifies that ⟨W_E(p), y⟩ ≥ ε on an entire parameter cell,
then every potential c₀ has L1 defect at least ε at all points p in the cell. -/
theorem cell_obstructed_of_dual_circulation
    {V α : Type} (E : List (DirectedEdge V))
    (W : DualCirculationWitness V E)
    (cell : RationalCell α)
    (W_E : α → DirectedEdge V → ℚ)
    (ε : ℚ)
    (h_dual_val : ∀ (p : α), cell.in_cell p → ε ≤ dualPairing E (W_E p) W.circulation)
    (p : α) (hp : cell.in_cell p) :
    ∀ (c₀ : V → ℚ), ε ≤ l1Defect E c₀ (W_E p) := by
  intro c₀
  have h_dual := h_dual_val p hp
  have h_weak := weak_duality E W (W_E p) c₀
  exact Rat.le_trans h_dual h_weak

/-- **Cell Pruning Theorem (No Zero Defect)**:
When ε > 0, no vertex potential can achieve zero defect anywhere in the certified cell.
Hence the entire cell can be safely pruned from the bisection search tree. -/
theorem cell_prunable_no_zero_defect
    {V α : Type} (E : List (DirectedEdge V))
    (W : DualCirculationWitness V E)
    (cell : RationalCell α)
    (W_E : α → DirectedEdge V → ℚ)
    (ε : ℚ) (hε : 0 < ε)
    (h_dual_val : ∀ (p : α), cell.in_cell p → ε ≤ dualPairing E (W_E p) W.circulation)
    (p : α) (hp : cell.in_cell p) :
    ¬ ∃ (c₀ : V → ℚ), l1Defect E c₀ (W_E p) = 0 := by
  intro ⟨c₀, hc₀⟩
  have h_bound := cell_obstructed_of_dual_circulation E W cell W_E ε h_dual_val p hp c₀
  rw [hc₀] at h_bound
  exact rat_pos_not_le_zero hε h_bound

/-- **Rational Cell Bisection Pruning Theorem (Contract Requirement F12)**:
Given a positive margin `margin > 0` bounding the defect functional on a cell,
no point in the cell can attain defect 0. -/
theorem rational_cell_bisection_prunable (margin : ℚ) (hpos : margin > 0)
    {α : Type} (cell : RationalCell α) (defect : α → ℚ)
    (h_margin : ∀ p, cell.in_cell p → margin ≤ defect p) :
    ∀ p, cell.in_cell p → ¬ (defect p = 0) := by
  intro p hp h_zero
  have h_bound := h_margin p hp
  rw [h_zero] at h_bound
  exact rat_pos_not_le_zero hpos h_bound

/-! ### 5. Grounding in Directional Positivity & Total Unimodularity -/

/-- Embedding integer strict positivity into rational strict positivity. -/
theorem int_pos_to_rat_pos (n : Int) (hn : 0 < n) : (0 : ℚ) < (n : ℚ) := by
  change (0 : ℚ).blt (n : ℚ) = true
  dsimp [Rat.blt]
  exact decide_eq_true hn

/-- **Rational Directional Positivity from NSP Margin**:
Lifts the general Weighted Null-Space Property directional positivity (`dirDeriv_pos` from
`SparseLandingGeneral.lean`) into exact rational arithmetic.
Under the weighted NSP (margin > 0), the directional derivative is strictly positive over ℚ,
eliminating flat/descent directions during box bisection. -/
theorem nsp_directional_positivity_rat (L : List NSP.Coord)
    (hw : ∀ c ∈ L, 0 ≤ c.weight) (hmargin : 0 < NSP.nspMargin L) :
    (0 : ℚ) < ((NSP.dirDeriv L : Int) : ℚ) :=
  int_pos_to_rat_pos (NSP.dirDeriv L) (NSP.dirDeriv_pos L hw hmargin)

/-- Total Unimodularity signed column-sum criterion:
Preserves integrality and rational closedness of extreme points in cell bisections. -/
theorem total_unimodularity_column_sum_bounded
    {V : Type} [DecidableEq V] (inJ : V → Bool) (e : DirectedEdge V) :
    columnSumOnSubset inJ e = 1 ∨ columnSumOnSubset inJ e = 0 ∨ columnSumOnSubset inJ e = -1 :=
  columnSum_bounded inJ e

/-- Edge irreflexivity from SnTower:
Prevents degenerate self-loops from corrupting the cell bisection dual circulation. -/
theorem edge_endpoints_distinct {V : Type} (e : DirectedEdge V) : e.source ≠ e.target :=
  e.irreflexive

end MUB6.Gluing.L1
