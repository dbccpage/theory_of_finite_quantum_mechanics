import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Algebra.Order.Ring.Abs
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Option
import Mathlib.Data.Fintype.Prod
import Mathlib.Data.Fintype.Sum
import Mathlib.Algebra.GroupWithZero.Units.Fintype
import Mathlib.Data.Fin.Tuple.Basic
import Mathlib.Data.Fin.VecNotation
import Mathlib.Data.Rat.Defs
import Mathlib.Data.Rat.Lemmas
import Mathlib.Logic.Equiv.Fin.Basic
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
# Campaign Proof: `PGW-SN-E08-WEIGHTED-L1-DUALITY`

Finite-dimensional weighted `ℓ¹` cochain approximation and dual flow certificate
over an arbitrary linearly ordered field `K` (including `ℚ`), proved from scratch
via Fourier–Motzkin elimination without external LP or convex-duality axioms.
-/

open scoped BigOperators

namespace CampaignSnE08WeightedL1Duality

section WeakDuality

variable {V E K : Type*} [Fintype V] [Fintype E]
variable [Field K] [LinearOrder K] [IsStrictOrderedRing K]

/-- Weighted `ℓ¹` cochain repair objective `∑ e, w e * |h e - (D x) e|`. -/
def cost (D : E → V → K) (w h : E → K) (x : V → K) : K :=
  ∑ e, w e * |h e - ∑ v, D e v * x v|

/-- Dual objective `∑ e, y e * h e`. -/
def dualObj (h y : E → K) : K :=
  ∑ e, y e * h e

/-- Dual feasibility: `Dᵀ y = 0` (`∀ v, ∑ e, D e v * y e = 0`) and `∀ e, |y e| ≤ w e`. -/
def DualFeasible (D : E → V → K) (w y : E → K) : Prop :=
  (∀ v, ∑ e, D e v * y e = 0) ∧ (∀ e, |y e| ≤ w e)

omit [LinearOrder K] [IsStrictOrderedRing K] in
/-- Orthogonality identity: if `Dᵀ y = 0`, then `∑ e, y e * (D x) e = 0`. -/
theorem dual_annihilates_coboundary (D : E → V → K) (x : V → K) (y : E → K)
    (h_div : ∀ v, ∑ e, D e v * y e = 0) :
    ∑ e, y e * (∑ v, D e v * x v) = 0 := by
  calc
    ∑ e, y e * (∑ v, D e v * x v)
        = ∑ e, ∑ v, y e * (D e v * x v) := by
          refine Finset.sum_congr rfl ?_
          intro e _
          rw [Finset.mul_sum]
    _ = ∑ v, ∑ e, y e * (D e v * x v) := Finset.sum_comm
    _ = ∑ v, (∑ e, D e v * y e) * x v := by
          refine Finset.sum_congr rfl ?_
          intro v _
          rw [Finset.sum_mul]
          refine Finset.sum_congr rfl ?_
          intro e _
          ring
    _ = ∑ v, 0 * x v := by
          refine Finset.sum_congr rfl ?_
          intro v _
          rw [h_div v]
    _ = 0 := by simp

/-- Pointwise bound: if `|y| ≤ w`, then `y * r ≤ w * |r|`. -/
theorem mul_le_mul_abs_of_abs_le {w y r : K} (hy : |y| ≤ w) :
    y * r ≤ w * |r| := by
  have h1 : y * r ≤ |y * r| := le_abs_self (y * r)
  have h2 : |y * r| = |y| * |r| := abs_mul y r
  have h3 : |y| * |r| ≤ w * |r| :=
    mul_le_mul_of_nonneg_right hy (abs_nonneg r)
  linarith

/-- Weak duality for weighted `ℓ¹` cochain approximation. -/
theorem weak_duality (D : E → V → K) (w h : E → K) (x : V → K) (y : E → K)
    (hy : DualFeasible D w y) :
    dualObj h y ≤ cost D w h x := by
  rcases hy with ⟨h_div, h_box⟩
  have h_orth : ∑ e, y e * (∑ v, D e v * x v) = 0 :=
    dual_annihilates_coboundary D x y h_div
  have h_rewrite : dualObj h y = ∑ e, y e * (h e - ∑ v, D e v * x v) := by
    unfold dualObj
    have h_diff :
        ∑ e, y e * (h e - ∑ v, D e v * x v) =
          (∑ e, y e * h e) - ∑ e, y e * (∑ v, D e v * x v) := by
      rw [← Finset.sum_sub_distrib]
      refine Finset.sum_congr rfl ?_
      intro e _
      ring
    linarith
  rw [h_rewrite]
  unfold cost
  refine Finset.sum_le_sum ?_
  intro e _
  exact mul_le_mul_abs_of_abs_le (h_box e)

/-- Zero gap between primal cost and dual objective certifies mutual global optimality. -/
theorem certificate_optimal (D : E → V → K) (w h : E → K) (x : V → K) (y : E → K)
    (hy : DualFeasible D w y) (h_eq : cost D w h x = dualObj h y) :
    (∀ x', cost D w h x ≤ cost D w h x') ∧
      (∀ y', DualFeasible D w y' → dualObj h y' ≤ dualObj h y) := by
  refine ⟨?_, ?_⟩
  · intro x'
    rw [h_eq]
    exact weak_duality D w h x' y hy
  · intro y' hy'
    rw [← h_eq]
    exact weak_duality D w h x y' hy'

end WeakDuality

/-!
## Fourier–Motzkin Elimination and Farkas' Lemma over a Linearly Ordered Field
-/

section Farkas

variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]

omit [IsStrictOrderedRing K] in
/-- In a finite family of lower and upper bounds where every lower bound
is at most every upper bound, there exists a point between all of them. -/
lemma exists_between_finset {α β : Type*} (P : Finset α) (Q : Finset β)
    (L : α → K) (U : β → K) (h : ∀ p ∈ P, ∀ q ∈ Q, L p ≤ U q) :
    ∃ t : K, (∀ p ∈ P, L p ≤ t) ∧ (∀ q ∈ Q, t ≤ U q) := by
  classical
  by_cases hP : P.Nonempty
  · refine ⟨P.sup' hP L, ?_, ?_⟩
    · intro p hp
      exact Finset.le_sup' L hp
    · intro q hq
      rw [Finset.sup'_le_iff]
      intro p hp
      exact h p hp q hq
  · rw [Finset.not_nonempty_iff_eq_empty] at hP
    by_cases hQ : Q.Nonempty
    · refine ⟨Q.inf' hQ U, ?_, ?_⟩
      · intro p hp
        rw [hP] at hp
        exact False.elim (Finset.notMem_empty p hp)
      · intro q hq
        exact Finset.inf'_le U hq
    · rw [Finset.not_nonempty_iff_eq_empty] at hQ
      refine ⟨0, ?_, ?_⟩
      · intro p hp
        rw [hP] at hp
        exact False.elim (Finset.notMem_empty p hp)
      · intro q hq
        rw [hQ] at hq
        exact False.elim (Finset.notMem_empty q hq)

/-- Single-variable Fourier–Motzkin reconstruction: if all zero-coefficient bounds
are nonnegative and all negative/positive pairs satisfy `0 ≤ c q * d p + (-c p) * d q`,
then there exists `t : K` with `∀ i, c i * t ≤ d i`. -/
lemma fm_feasibility_of_eliminated {m : ℕ} (c d : Fin m → K)
    (hZ : ∀ z : Fin m, c z = 0 → 0 ≤ d z)
    (hPQ : ∀ p q : Fin m, c p < 0 → 0 < c q → 0 ≤ c q * d p + (-c p) * d q) :
    ∃ t : K, ∀ i : Fin m, c i * t ≤ d i := by
  classical
  let P : Finset (Fin m) := Finset.univ.filter (fun p => c p < 0)
  let Q : Finset (Fin m) := Finset.univ.filter (fun q => 0 < c q)
  have h_le : ∀ p ∈ P, ∀ q ∈ Q, d p / c p ≤ d q / c q := by
    intro p hp q hq
    have hcp : c p < 0 := (Finset.mem_filter.mp hp).2
    have hcq : 0 < c q := (Finset.mem_filter.mp hq).2
    have hcp_ne : c p ≠ 0 := ne_of_lt hcp
    have hcq_ne : c q ≠ 0 := ne_of_gt hcq
    have h_comb : 0 ≤ c q * d p + (-c p) * d q := hPQ p q hcp hcq
    have h_id : ((d q / c q) - (d p / c p)) * (c q * (-c p)) = c q * d p + (-c p) * d q := by
      calc
        ((d q / c q) - (d p / c p)) * (c q * (-c p))
            = (d q / c q * c q) * (-c p) + (d p / c p * c p) * c q := by ring
        _ = d q * (-c p) + d p * c q := by
              rw [div_mul_cancel₀ (d q) hcq_ne, div_mul_cancel₀ (d p) hcp_ne]
        _ = c q * d p + (-c p) * d q := by ring
    by_contra! h_lt
    have h_pos_denom : 0 < c q * (-c p) := mul_pos hcq (neg_pos.mpr hcp)
    have h_neg : ((d q / c q) - (d p / c p)) * (c q * (-c p)) < 0 :=
      mul_neg_of_neg_of_pos (sub_neg.mpr h_lt) h_pos_denom
    linarith
  obtain ⟨t, htP, htQ⟩ :=
    exists_between_finset P Q (fun p => d p / c p) (fun q => d q / c q) h_le
  refine ⟨t, ?_⟩
  intro i
  rcases lt_trichotomy (c i) 0 with hlt | heq | hgt
  · have hiP : i ∈ P := Finset.mem_filter.mpr ⟨Finset.mem_univ i, hlt⟩
    have hti : d i / c i ≤ t := htP i hiP
    have hci_ne : c i ≠ 0 := ne_of_lt hlt
    have hmul : t * c i ≤ (d i / c i) * c i :=
      mul_le_mul_of_nonpos_right hti (le_of_lt hlt)
    rw [div_mul_cancel₀ (d i) hci_ne] at hmul
    linarith
  · rw [heq, zero_mul]
    exact hZ i heq
  · have hiQ : i ∈ Q := Finset.mem_filter.mpr ⟨Finset.mem_univ i, hgt⟩
    have hti : t ≤ d i / c i := htQ i hiQ
    have hci_ne : c i ≠ 0 := ne_of_gt hgt
    have hmul : t * c i ≤ (d i / c i) * c i :=
      mul_le_mul_of_nonneg_right hti (le_of_lt hgt)
    rw [div_mul_cancel₀ (d i) hci_ne] at hmul
    linarith

/-- Farkas' lemma on `Fin m × Fin n` over a linearly ordered field `K`, proved by
induction on the variable dimension `n` via Fourier–Motzkin elimination. -/
theorem farkas :
    ∀ (n m : ℕ) (A : Fin m → Fin n → K) (b : Fin m → K),
      (∃ x : Fin n → K, ∀ i : Fin m, ∑ j : Fin n, A i j * x j ≤ b i) ∨
        (∃ u : Fin m → K,
          (∀ i, 0 ≤ u i) ∧
          (∀ j : Fin n, ∑ i : Fin m, u i * A i j = 0) ∧
          (∑ i : Fin m, u i * b i < 0))
  | 0, m, A, b => by
      classical
      by_cases hb : ∀ i : Fin m, 0 ≤ b i
      · refine Or.inl ⟨Fin.elim0, ?_⟩
        intro i
        simpa using hb i
      · push Not at hb
        rcases hb with ⟨z, hbz⟩
        refine Or.inr ⟨fun i => if i = z then 1 else 0, ?_, ?_, ?_⟩
        · intro i
          dsimp only
          split_ifs <;> linarith
        · intro j
          exact Fin.elim0 j
        · simpa using hbz
  | n + 1, m, A, b => by
      classical
      let m' := m * m
      let ev : Fin m' ≃ Fin m × Fin m := finProdFinEquiv.symm
      let W : Fin m' → Fin m → K := fun r i =>
        if (ev r).1 = (ev r).2 then
          if A (ev r).1 (Fin.last n) = 0 then (if i = (ev r).1 then 1 else 0) else 0
        else
          if A (ev r).1 (Fin.last n) < 0 ∧ 0 < A (ev r).2 (Fin.last n) then
            (if i = (ev r).1 then A (ev r).2 (Fin.last n) else 0) +
              (if i = (ev r).2 then -A (ev r).1 (Fin.last n) else 0)
          else 0
      have hW_nonneg : ∀ r : Fin m', ∀ i : Fin m, 0 ≤ W r i := by
        intro r i
        dsimp [W]
        by_cases hpq : (ev r).1 = (ev r).2
        · simp only [hpq, ↓reduceIte]
          split_ifs <;> linarith
        · simp only [hpq, ↓reduceIte]
          by_cases h2 : A (ev r).1 (Fin.last n) < 0 ∧ 0 < A (ev r).2 (Fin.last n)
          · simp only [h2, and_self, ↓reduceIte]
            rcases h2 with ⟨hcp_neg, hcq_pos⟩
            have h_first : 0 ≤ (if i = (ev r).1 then A (ev r).2 (Fin.last n) else 0) := by
              split_ifs <;> linarith
            have h_second : 0 ≤ (if i = (ev r).2 then -A (ev r).1 (Fin.last n) else 0) := by
              split_ifs <;> linarith
            linarith
          · simp only [h2, ↓reduceIte, le_refl]
      have hW_ann : ∀ r : Fin m', ∑ i : Fin m, W r i * A i (Fin.last n) = 0 := by
        intro r
        dsimp [W]
        by_cases hpq : (ev r).1 = (ev r).2
        · simp [hpq]
        · by_cases h2 : A (ev r).1 (Fin.last n) < 0 ∧ 0 < A (ev r).2 (Fin.last n)
          · have h_sum :
                ∑ i : Fin m,
                  ((if i = (ev r).1 then A (ev r).2 (Fin.last n) else 0) +
                    (if i = (ev r).2 then -A (ev r).1 (Fin.last n) else 0)) *
                    A i (Fin.last n) =
                  A (ev r).2 (Fin.last n) * A (ev r).1 (Fin.last n) +
                    (-A (ev r).1 (Fin.last n)) * A (ev r).2 (Fin.last n) := by
              simp [add_mul, Finset.sum_add_distrib]
            simp only [hpq, h2, and_self, ↓reduceIte]
            rw [h_sum]
            ring
          · simp [hpq, h2]
      let A' : Fin m' → Fin n → K := fun r j => ∑ i : Fin m, W r i * A i (Fin.castSucc j)
      let b' : Fin m' → K := fun r => ∑ i : Fin m, W r i * b i
      rcases farkas n m' A' b' with ⟨x₀, hx₀⟩ | ⟨v, hv_nonneg, hv_ann, hv_neg⟩
      · let c : Fin m → K := fun i => A i (Fin.last n)
        let d : Fin m → K := fun i => b i - ∑ j : Fin n, A i (Fin.castSucc j) * x₀ j
        have hZ : ∀ z : Fin m, c z = 0 → 0 ≤ d z := by
          intro z hcz
          have hcz' : A z (Fin.last n) = 0 := hcz
          let r : Fin m' := finProdFinEquiv (z, z)
          have hev : ev r = (z, z) := Equiv.symm_apply_apply finProdFinEquiv (z, z)
          have hWr : ∀ i : Fin m, W r i = if i = z then 1 else 0 := by
            intro i
            dsimp [W]
            rw [hev]
            simp [hcz']
          have hA' : ∀ j : Fin n, A' r j = A z (Fin.castSucc j) := by
            intro j
            dsimp [A']
            simp [hWr]
          have hb' : b' r = b z := by
            dsimp [b']
            simp [hWr]
          have h_ineq := hx₀ r
          simp only [hA', hb'] at h_ineq
          dsimp [d]
          linarith
        have hPQ : ∀ p q : Fin m, c p < 0 → 0 < c q → 0 ≤ c q * d p + (-c p) * d q := by
          intro p q hcp hcq
          have hcp' : A p (Fin.last n) < 0 := hcp
          have hcq' : 0 < A q (Fin.last n) := hcq
          have hpq : p ≠ q := by
            intro h_eq
            subst h_eq
            linarith
          let r : Fin m' := finProdFinEquiv (p, q)
          have hev : ev r = (p, q) := Equiv.symm_apply_apply finProdFinEquiv (p, q)
          have hWr : ∀ i : Fin m,
              W r i = (if i = p then c q else 0) + (if i = q then -c p else 0) := by
            intro i
            dsimp [W, c]
            rw [hev]
            simp only [hpq, hcp', hcq', and_self, ↓reduceIte]
          have h_eval : ∀ f : Fin m → K,
              ∑ i : Fin m, W r i * f i = c q * f p + (-c p) * f q := by
            intro f
            simp [hWr, add_mul, Finset.sum_add_distrib]
          have hA' : ∀ j : Fin n,
              A' r j = c q * A p (Fin.castSucc j) + (-c p) * A q (Fin.castSucc j) := by
            intro j
            exact h_eval (fun i => A i (Fin.castSucc j))
          have hb' : b' r = c q * b p + (-c p) * b q := h_eval b
          have h_ineq := hx₀ r
          have h_lhs :
              ∑ j : Fin n, A' r j * x₀ j =
                c q * (∑ j : Fin n, A p (Fin.castSucc j) * x₀ j) +
                  (-c p) * (∑ j : Fin n, A q (Fin.castSucc j) * x₀ j) := by
            calc
              ∑ j : Fin n, A' r j * x₀ j
                  = ∑ j : Fin n,
                      (c q * (A p (Fin.castSucc j) * x₀ j) +
                        (-c p) * (A q (Fin.castSucc j) * x₀ j)) := by
                    refine Finset.sum_congr rfl ?_
                    intro j _
                    rw [hA' j]
                    ring
              _ = c q * (∑ j : Fin n, A p (Fin.castSucc j) * x₀ j) +
                    (-c p) * (∑ j : Fin n, A q (Fin.castSucc j) * x₀ j) := by
                    rw [Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum]
          rw [h_lhs, hb'] at h_ineq
          dsimp [d]
          linarith
        obtain ⟨t, ht⟩ := fm_feasibility_of_eliminated c d hZ hPQ
        refine Or.inl ⟨Fin.snoc x₀ t, ?_⟩
        intro i
        rw [Fin.sum_univ_castSucc]
        simp only [Fin.snoc_castSucc, Fin.snoc_last]
        have hti : c i * t ≤ d i := ht i
        dsimp [c, d] at hti
        linarith
      · let u : Fin m → K := fun i => ∑ r : Fin m', v r * W r i
        refine Or.inr ⟨u, ?_, ?_, ?_⟩
        · intro i
          refine Finset.sum_nonneg ?_
          intro r _
          exact mul_nonneg (hv_nonneg r) (hW_nonneg r i)
        · intro j
          refine Fin.lastCases ?_ ?_ j
          · calc
              ∑ i : Fin m, u i * A i (Fin.last n)
                  = ∑ i : Fin m, (∑ r : Fin m', v r * W r i) * A i (Fin.last n) := rfl
              _ = ∑ i : Fin m, ∑ r : Fin m', v r * (W r i * A i (Fin.last n)) := by
                    refine Finset.sum_congr rfl ?_
                    intro i _
                    rw [Finset.sum_mul]
                    refine Finset.sum_congr rfl ?_
                    intro r _
                    ring
              _ = ∑ r : Fin m', ∑ i : Fin m, v r * (W r i * A i (Fin.last n)) := Finset.sum_comm
              _ = ∑ r : Fin m', v r * (∑ i : Fin m, W r i * A i (Fin.last n)) := by
                    refine Finset.sum_congr rfl ?_
                    intro r _
                    rw [← Finset.mul_sum]
              _ = ∑ r : Fin m', v r * 0 := by
                    refine Finset.sum_congr rfl ?_
                    intro r _
                    rw [hW_ann r]
              _ = 0 := by simp
          · intro j₀
            calc
              ∑ i : Fin m, u i * A i (Fin.castSucc j₀)
                  = ∑ i : Fin m, (∑ r : Fin m', v r * W r i) * A i (Fin.castSucc j₀) := rfl
              _ = ∑ i : Fin m, ∑ r : Fin m', v r * (W r i * A i (Fin.castSucc j₀)) := by
                    refine Finset.sum_congr rfl ?_
                    intro i _
                    rw [Finset.sum_mul]
                    refine Finset.sum_congr rfl ?_
                    intro r _
                    ring
              _ = ∑ r : Fin m', ∑ i : Fin m, v r * (W r i * A i (Fin.castSucc j₀)) := Finset.sum_comm
              _ = ∑ r : Fin m', v r * A' r j₀ := by
                    refine Finset.sum_congr rfl ?_
                    intro r _
                    dsimp [A']
                    rw [← Finset.mul_sum]
              _ = 0 := hv_ann j₀
        · calc
            ∑ i : Fin m, u i * b i
                = ∑ i : Fin m, (∑ r : Fin m', v r * W r i) * b i := rfl
            _ = ∑ i : Fin m, ∑ r : Fin m', v r * (W r i * b i) := by
                  refine Finset.sum_congr rfl ?_
                  intro i _
                  rw [Finset.sum_mul]
                  refine Finset.sum_congr rfl ?_
                  intro r _
                  ring
            _ = ∑ r : Fin m', ∑ i : Fin m, v r * (W r i * b i) := Finset.sum_comm
            _ = ∑ r : Fin m', v r * b' r := by
                  refine Finset.sum_congr rfl ?_
                  intro r _
                  dsimp [b']
                  rw [← Finset.mul_sum]
            _ < 0 := hv_neg
termination_by n => n

/-- Farkas' lemma indexed by arbitrary finite types `I` and `J`. -/
theorem farkas_fintype {I J : Type*} [Fintype I] [Fintype J]
    (A : I → J → K) (b : I → K) :
    (∃ x : J → K, ∀ i : I, ∑ j : J, A i j * x j ≤ b i) ∨
      (∃ u : I → K,
        (∀ i : I, 0 ≤ u i) ∧
        (∀ j : J, ∑ i : I, u i * A i j = 0) ∧
        (∑ i : I, u i * b i < 0)) := by
  classical
  let eI : I ≃ Fin (Fintype.card I) := Fintype.equivFin I
  let eJ : J ≃ Fin (Fintype.card J) := Fintype.equivFin J
  rcases farkas (Fintype.card J) (Fintype.card I)
      (fun i j => A (eI.symm i) (eJ.symm j)) (fun i => b (eI.symm i)) with
    ⟨x, hx⟩ | ⟨u, hu_nonneg, hu_ann, hu_neg⟩
  · refine Or.inl ⟨fun j => x (eJ j), ?_⟩
    intro i
    have hi := hx (eI i)
    simp only [Equiv.symm_apply_apply] at hi
    have hsum' :
        ∑ j : Fin (Fintype.card J), A i (eJ.symm j) * x j =
          ∑ j : J, A i j * x (eJ j) := by
      simpa using (Equiv.sum_comp eJ.symm (fun j => A i j * x (eJ j)))
    linarith
  · refine Or.inr ⟨fun i => u (eI i), ?_, ?_, ?_⟩
    · intro i
      exact hu_nonneg (eI i)
    · intro j
      have hj := hu_ann (eJ j)
      simp only [Equiv.symm_apply_apply] at hj
      have hsum' :
          ∑ i : Fin (Fintype.card I), u i * A (eI.symm i) j =
            ∑ i : I, u (eI i) * A i j := by
        simpa using (Equiv.sum_comp eI.symm (fun i => u (eI i) * A i j))
      linarith
    · have hsum' :
          ∑ i : Fin (Fintype.card I), u i * b (eI.symm i) =
            ∑ i : I, u (eI i) * b i := by
        simpa using (Equiv.sum_comp eI.symm (fun i => u (eI i) * b i))
      linarith

end Farkas

/-!
## Strong Linear Programming Duality from Farkas' Lemma
-/

section StrongLPDuality

variable {I J K : Type*} [Fintype I] [Fintype J]
variable [Field K] [LinearOrder K] [IsStrictOrderedRing K]

/-- Primal feasibility for `max_y cᵀ y` subject to `G y ≤ g`. -/
def PFeas (G : I → J → K) (g : I → K) (y : J → K) : Prop :=
  ∀ i : I, ∑ j : J, G i j * y j ≤ g i

/-- Dual feasibility for `min_{u ≥ 0} gᵀ u` subject to `Gᵀ u = c`. -/
def DFeas (G : I → J → K) (c : J → K) (u : I → K) : Prop :=
  (∀ i : I, 0 ≤ u i) ∧ (∀ j : J, ∑ i : I, u i * G i j = c j)

/-- Weak LP duality: for primal-feasible `y` and dual-feasible `u`,
`∑ j, c j * y j ≤ ∑ i, g i * u i`. -/
theorem lp_weak_duality (G : I → J → K) (g : I → K) (c : J → K)
    (y : J → K) (u : I → K) (hy : PFeas G g y) (hu : DFeas G c u) :
    ∑ j : J, c j * y j ≤ ∑ i : I, g i * u i := by
  rcases hu with ⟨hu_nonneg, hu_eq⟩
  calc
    ∑ j : J, c j * y j
        = ∑ j : J, (∑ i : I, u i * G i j) * y j := by
          refine Finset.sum_congr rfl ?_
          intro j _
          rw [hu_eq j]
    _ = ∑ j : J, ∑ i : I, u i * (G i j * y j) := by
          refine Finset.sum_congr rfl ?_
          intro j _
          rw [Finset.sum_mul]
          refine Finset.sum_congr rfl ?_
          intro i _
          ring
    _ = ∑ i : I, ∑ j : J, u i * (G i j * y j) := Finset.sum_comm
    _ = ∑ i : I, u i * (∑ j : J, G i j * y j) := by
          refine Finset.sum_congr rfl ?_
          intro i _
          rw [← Finset.mul_sum]
    _ ≤ ∑ i : I, u i * g i := by
          refine Finset.sum_le_sum ?_
          intro i _
          exact mul_le_mul_of_nonneg_left (hy i) (hu_nonneg i)
    _ = ∑ i : I, g i * u i := by
          refine Finset.sum_congr rfl ?_
          intro i _
          ring

/-- Strong LP duality over any linearly ordered field `K`: if both primal and dual
are feasible, there exist primal-feasible `y` and dual-feasible `u` with equal objectives. -/
theorem lp_strong_duality (G : I → J → K) (g : I → K) (c : J → K)
    (hP : ∃ y₀ : J → K, PFeas G g y₀) (hD : ∃ u₀ : I → K, DFeas G c u₀) :
    ∃ y : J → K, ∃ u : I → K,
      PFeas G g y ∧ DFeas G c u ∧ ∑ j : J, c j * y j = ∑ i : I, g i * u i := by
  classical
  let Row := (I ⊕ I) ⊕ ((J ⊕ J) ⊕ Unit)
  let Col := J ⊕ I
  let M : Row → Col → K := fun r k =>
    match r, k with
    | .inl (.inl i), .inl j => G i j
    | .inl (.inl _), .inr _ => 0
    | .inl (.inr _), .inl _ => 0
    | .inl (.inr i), .inr i' => if i' = i then -1 else 0
    | .inr (.inl (.inl _)), .inl _ => 0
    | .inr (.inl (.inl j)), .inr i => -G i j
    | .inr (.inl (.inr _)), .inl _ => 0
    | .inr (.inl (.inr j)), .inr i => G i j
    | .inr (.inr ()), .inl j => -c j
    | .inr (.inr ()), .inr i => g i
  let rhs : Row → K := fun r =>
    match r with
    | .inl (.inl i) => g i
    | .inl (.inr _) => 0
    | .inr (.inl (.inl j)) => -c j
    | .inr (.inl (.inr j)) => c j
    | .inr (.inr ()) => 0
  rcases farkas_fintype M rhs with ⟨z, hz⟩ | ⟨w, hw_nonneg, hw_ann, hw_neg⟩
  · let y : J → K := fun j => z (.inl j)
    let u : I → K := fun i => z (.inr i)
    have hy : PFeas G g y := by
      intro i
      have hi := hz (.inl (.inl i))
      simp only [Col, M, rhs, Fintype.sum_sum_type] at hi
      simpa [y] using hi
    have hu_nonneg : ∀ i : I, 0 ≤ u i := by
      intro i
      have hi := hz (.inl (.inr i))
      simp only [Col, M, rhs, Fintype.sum_sum_type] at hi
      have h_s : ∑ x : I, (if x = i then (-1 : K) else 0) * z (.inr x) = -u i := by
        simp [u]
      have hi' : (∑ x : J, (0 : K) * z (.inl x)) +
          ∑ x : I, (if x = i then (-1 : K) else 0) * z (.inr x) ≤ 0 := hi
      rw [h_s] at hi'
      simp only [zero_mul, Finset.sum_const_zero, zero_add] at hi'
      linarith
    have hu_eq : ∀ j : J, ∑ i : I, u i * G i j = c j := by
      intro j
      have hj1 := hz (.inr (.inl (.inl j)))
      have hj2 := hz (.inr (.inl (.inr j)))
      simp only [Col, M, rhs, Fintype.sum_sum_type] at hj1 hj2
      have h_neg_sum : ∑ i : I, -G i j * z (.inr i) = -(∑ i : I, u i * G i j) := by
        rw [← Finset.sum_neg_distrib]
        refine Finset.sum_congr rfl ?_
        intro i _
        dsimp [u]
        ring
      have h_pos_sum : ∑ i : I, G i j * z (.inr i) = ∑ i : I, u i * G i j := by
        refine Finset.sum_congr rfl ?_
        intro i _
        dsimp [u]
        ring
      simp only [zero_mul, Finset.sum_const_zero, zero_add, h_neg_sum] at hj1
      simp only [zero_mul, Finset.sum_const_zero, zero_add, h_pos_sum] at hj2
      linarith
    have hu : DFeas G c u := ⟨hu_nonneg, hu_eq⟩
    have h_obj_le : ∑ i : I, g i * u i ≤ ∑ j : J, c j * y j := by
      have h_top := hz (.inr (.inr ()))
      simp only [Col, M, rhs, Fintype.sum_sum_type] at h_top
      have h_neg_c : ∑ j : J, -c j * z (.inl j) = -(∑ j : J, c j * y j) := by
        rw [← Finset.sum_neg_distrib]
        refine Finset.sum_congr rfl ?_
        intro j _
        dsimp [y]
        ring
      have h_pos_g : ∑ i : I, g i * z (.inr i) = ∑ i : I, g i * u i := rfl
      rw [h_neg_c, h_pos_g] at h_top
      linarith
    have h_weak := lp_weak_duality G g c y u hy hu
    refine ⟨y, u, hy, hu, by linarith⟩
  · exfalso
    let u' : I → K := fun i => w (.inl (.inl i))
    let s : I → K := fun i => w (.inl (.inr i))
    let y_pos : J → K := fun j => w (.inr (.inl (.inl j)))
    let y_neg : J → K := fun j => w (.inr (.inl (.inr j)))
    let t : K := w (.inr (.inr ()))
    let y' : J → K := fun j => y_pos j - y_neg j
    have hu'_nonneg : ∀ i : I, 0 ≤ u' i := fun i => hw_nonneg (.inl (.inl i))
    have hs_nonneg : ∀ i : I, 0 ≤ s i := fun i => hw_nonneg (.inl (.inr i))
    have ht_nonneg : 0 ≤ t := hw_nonneg (.inr (.inr ()))
    have h_col_J : ∀ j : J, ∑ i : I, u' i * G i j = t * c j := by
      intro j
      have hj := hw_ann (.inl j)
      simp only [Row, M, Fintype.sum_sum_type, Fintype.sum_unique] at hj
      have hj' : (∑ i : I, u' i * G i j) + t * (-c j) = 0 := by
        simpa [u', t] using hj
      linarith
    have h_col_I : ∀ i : I, ∑ j : J, G i j * y' j ≤ t * g i := by
      intro i
      have hi := hw_ann (.inr i)
      simp only [Row, M, Fintype.sum_sum_type, Fintype.sum_unique] at hi
      have h_s : ∑ x : I, w (.inl (.inr x)) * (if i = x then (-1 : K) else 0) = -s i := by
        simp [s]
      have h_y :
          (∑ j : J, y_pos j * -G i j) + ∑ j : J, y_neg j * G i j =
            -(∑ j : J, G i j * y' j) := by
        rw [← Finset.sum_add_distrib, ← Finset.sum_neg_distrib]
        refine Finset.sum_congr rfl ?_
        intro j _
        dsimp [y']
        ring
      have hi' : -s i + -(∑ j : J, G i j * y' j) + t * g i = 0 := by
        have h_raw :
            (0 + ∑ x : I, w (.inl (.inr x)) * (if i = x then (-1 : K) else 0)) +
              (((∑ x : J, y_pos x * -G i x) + ∑ x : J, y_neg x * G i x) + t * g i) = 0 := by
          simpa [y_pos, y_neg, t] using hi
        linarith
      have hsi : 0 ≤ s i := hs_nonneg i
      linarith
    have h_rhs_neg : ∑ i : I, g i * u' i < ∑ j : J, c j * y' j := by
      have h_raw := hw_neg
      simp only [Row, rhs, Fintype.sum_sum_type, Fintype.sum_unique] at h_raw
      have h_u : ∑ i : I, u' i * g i = ∑ i : I, g i * u' i := by
        refine Finset.sum_congr rfl ?_
        intro i _
        ring
      have h_y :
          (∑ j : J, y_pos j * -c j) + ∑ j : J, y_neg j * c j =
            -(∑ j : J, c j * y' j) := by
        rw [← Finset.sum_add_distrib, ← Finset.sum_neg_distrib]
        refine Finset.sum_congr rfl ?_
        intro j _
        dsimp [y']
        ring
      have h_raw' : (∑ i : I, u' i * g i + 0) + (((∑ j : J, y_pos j * -c j) + ∑ j : J, y_neg j * c j) + 0) < 0 := by
        simpa [u', y_pos, y_neg] using h_raw
      linarith
    rcases lt_or_eq_of_le ht_nonneg with ht_pos | ht_zero
    · have h_bilin : t * (∑ j : J, c j * y' j) ≤ t * (∑ i : I, g i * u' i) := by
        calc
          t * (∑ j : J, c j * y' j)
              = ∑ j : J, (t * c j) * y' j := by
                rw [Finset.mul_sum]
                refine Finset.sum_congr rfl ?_
                intro j _
                ring
          _ = ∑ j : J, (∑ i : I, u' i * G i j) * y' j := by
                refine Finset.sum_congr rfl ?_
                intro j _
                rw [h_col_J j]
          _ = ∑ j : J, ∑ i : I, u' i * (G i j * y' j) := by
                refine Finset.sum_congr rfl ?_
                intro j _
                rw [Finset.sum_mul]
                refine Finset.sum_congr rfl ?_
                intro i _
                ring
          _ = ∑ i : I, ∑ j : J, u' i * (G i j * y' j) := Finset.sum_comm
          _ = ∑ i : I, u' i * (∑ j : J, G i j * y' j) := by
                refine Finset.sum_congr rfl ?_
                intro i _
                rw [← Finset.mul_sum]
          _ ≤ ∑ i : I, u' i * (t * g i) := by
                refine Finset.sum_le_sum ?_
                intro i _
                exact mul_le_mul_of_nonneg_left (h_col_I i) (hu'_nonneg i)
          _ = t * (∑ i : I, g i * u' i) := by
                rw [Finset.mul_sum]
                refine Finset.sum_congr rfl ?_
                intro i _
                ring
      have h_strict_t : t * (∑ i : I, g i * u' i) < t * (∑ j : J, c j * y' j) :=
        mul_lt_mul_of_pos_left h_rhs_neg ht_pos
      linarith
    · rcases hP with ⟨y₀, hy₀⟩
      rcases hD with ⟨u₀, hu₀_nonneg, hu₀_eq⟩
      have h_u'_nonneg_sum : 0 ≤ ∑ i : I, g i * u' i := by
        calc
          (0 : K) = ∑ j : J, (0 * c j) * y₀ j := by simp
          _ = ∑ j : J, (∑ i : I, u' i * G i j) * y₀ j := by
                refine Finset.sum_congr rfl ?_
                intro j _
                rw [h_col_J j, ← ht_zero]
          _ = ∑ j : J, ∑ i : I, u' i * (G i j * y₀ j) := by
                refine Finset.sum_congr rfl ?_
                intro j _
                rw [Finset.sum_mul]
                refine Finset.sum_congr rfl ?_
                intro i _
                ring
          _ = ∑ i : I, ∑ j : J, u' i * (G i j * y₀ j) := Finset.sum_comm
          _ = ∑ i : I, u' i * (∑ j : J, G i j * y₀ j) := by
                refine Finset.sum_congr rfl ?_
                intro i _
                rw [← Finset.mul_sum]
          _ ≤ ∑ i : I, u' i * g i := by
                refine Finset.sum_le_sum ?_
                intro i _
                exact mul_le_mul_of_nonneg_left (hy₀ i) (hu'_nonneg i)
          _ = ∑ i : I, g i * u' i := by
                refine Finset.sum_congr rfl ?_
                intro i _
                ring
      have h_y'_nonpos_sum : ∑ j : J, c j * y' j ≤ 0 := by
        calc
          ∑ j : J, c j * y' j
              = ∑ j : J, (∑ i : I, u₀ i * G i j) * y' j := by
                refine Finset.sum_congr rfl ?_
                intro j _
                rw [hu₀_eq j]
          _ = ∑ j : J, ∑ i : I, u₀ i * (G i j * y' j) := by
                refine Finset.sum_congr rfl ?_
                intro j _
                rw [Finset.sum_mul]
                refine Finset.sum_congr rfl ?_
                intro i _
                ring
          _ = ∑ i : I, ∑ j : J, u₀ i * (G i j * y' j) := Finset.sum_comm
          _ = ∑ i : I, u₀ i * (∑ j : J, G i j * y' j) := by
                refine Finset.sum_congr rfl ?_
                intro i _
                rw [← Finset.mul_sum]
          _ ≤ ∑ i : I, u₀ i * (0 * g i) := by
                refine Finset.sum_le_sum ?_
                intro i _
                have hi0 : ∑ j : J, G i j * y' j ≤ 0 * g i := by
                  rw [ht_zero]
                  exact h_col_I i
                exact mul_le_mul_of_nonneg_left hi0 (hu₀_nonneg i)
          _ = 0 := by simp
      linarith

end StrongLPDuality

/-!
## Weighted `ℓ¹` Cochain Approximation Strong Duality
-/

section StrongWeightedL1Duality

variable {V E K : Type*} [Fintype V] [Fintype E]
variable [Field K] [LinearOrder K] [IsStrictOrderedRing K]

/-- Strong duality for finite-dimensional weighted `ℓ¹` cochain approximation:
for any coboundary matrix `D : E → V → K`, nonnegative edge weights `w : E → K`,
and measured edge cochain `h : E → K`, there exist a primal potential `x : V → K`
and a dual flow `y : E → K` such that `DualFeasible D w y` and
`cost D w h x = dualObj h y`. -/
theorem weighted_l1_strong_duality (D : E → V → K) (w h : E → K)
    (hw : ∀ e : E, 0 ≤ w e) :
    ∃ x : V → K, ∃ y : E → K,
      DualFeasible D w y ∧ cost D w h x = dualObj h y := by
  classical
  let I := (V ⊕ V) ⊕ (E ⊕ E)
  let G : I → E → K := fun i e =>
    match i with
    | .inl (.inl v) => D e v
    | .inl (.inr v) => -D e v
    | .inr (.inl e₀) => if e = e₀ then 1 else 0
    | .inr (.inr e₀) => if e = e₀ then -1 else 0
  let g : I → K := fun i =>
    match i with
    | .inl (.inl _) => 0
    | .inl (.inr _) => 0
    | .inr (.inl e₀) => w e₀
    | .inr (.inr e₀) => w e₀
  have hP : ∃ y₀ : E → K, PFeas G g y₀ := by
    refine ⟨fun _ => 0, ?_⟩
    intro i
    rcases i with (v | v) | (e₀ | e₀) <;> simp [G, g, hw]
  have hD : ∃ u₀ : I → K, DFeas G h u₀ := by
    let u₀ : I → K := fun i =>
      match i with
      | .inl (.inl _) => 0
      | .inl (.inr _) => 0
      | .inr (.inl e₀) => max (h e₀) 0
      | .inr (.inr e₀) => max (-h e₀) 0
    refine ⟨u₀, ?_, ?_⟩
    · intro i
      rcases i with (v | v) | (e₀ | e₀) <;> simp [u₀]
    · intro e
      simp only [I, G, u₀, Fintype.sum_sum_type]
      have h_max : max (h e) 0 - max (-h e) 0 = h e := by
        rcases le_total 0 (h e) with h_nonneg | h_nonpos
        · have h_neg : -h e ≤ 0 := by linarith
          rw [max_eq_left h_nonneg, max_eq_right h_neg]
          ring
        · have h_neg : 0 ≤ -h e := by linarith
          rw [max_eq_right h_nonpos, max_eq_left h_neg]
          ring
      simp [← sub_eq_add_neg, h_max]
  obtain ⟨y, u, hy_feas, ⟨hu_nonneg, hu_eq⟩, h_lp_eq⟩ :=
    lp_strong_duality G g h hP hD
  have hy_dual : DualFeasible D w y := by
    refine ⟨?_, ?_⟩
    · intro v
      have hv1 := hy_feas (.inl (.inl v))
      have hv2 := hy_feas (.inl (.inr v))
      simp only [G, g] at hv1 hv2
      have hv2' : -(∑ e : E, D e v * y e) ≤ 0 := by
        have h_neg : ∑ e : E, -D e v * y e = -(∑ e : E, D e v * y e) := by
          rw [← Finset.sum_neg_distrib]
          refine Finset.sum_congr rfl ?_
          intro e _
          ring
        linarith
      linarith
    · intro e
      have he1 := hy_feas (.inr (.inl e))
      have he2 := hy_feas (.inr (.inr e))
      simp only [G, g] at he1 he2
      have he1' : y e ≤ w e := by simpa using he1
      have he2' : -y e ≤ w e := by simpa using he2
      exact abs_le.mpr ⟨by linarith, he1'⟩
  let x : V → K := fun v => u (.inl (.inl v)) - u (.inl (.inr v))
  let u_pos : E → K := fun e => u (.inr (.inl e))
  let u_neg : E → K := fun e => u (.inr (.inr e))
  have h_res_eq : ∀ e : E, h e - ∑ v : V, D e v * x v = u_pos e - u_neg e := by
    intro e
    have he := hu_eq e
    simp only [I, G, Fintype.sum_sum_type] at he
    have h_p : ∑ x_1 : E, u (.inr (.inl x_1)) * (if e = x_1 then (1 : K) else 0) = u_pos e := by
      simp [u_pos]
    have h_n : ∑ x_1 : E, u (.inr (.inr x_1)) * (if e = x_1 then (-1 : K) else 0) = -u_neg e := by
      simp [u_neg]
    have h_v :
        (∑ v : V, u (.inl (.inl v)) * D e v) + ∑ v : V, u (.inl (.inr v)) * -D e v =
          ∑ v : V, D e v * x v := by
      rw [← Finset.sum_add_distrib]
      refine Finset.sum_congr rfl ?_
      intro v _
      dsimp [x]
      ring
    rw [h_v, h_p, h_n] at he
    linarith
  have h_cost_le : cost D w h x ≤ dualObj h y := by
    have h_rhs :
        ∑ i : I, g i * u i = ∑ e : E, w e * (u_pos e + u_neg e) := by
      simp only [I, g, Fintype.sum_sum_type]
      simp [u_pos, u_neg, mul_add, Finset.sum_add_distrib]
    have h_lhs :
        ∑ e : E, h e * y e = dualObj h y := by
      unfold dualObj
      refine Finset.sum_congr rfl ?_
      intro e _
      ring
    calc
      cost D w h x
          = ∑ e : E, w e * |u_pos e - u_neg e| := by
            unfold cost
            refine Finset.sum_congr rfl ?_
            intro e _
            rw [h_res_eq e]
      _ ≤ ∑ e : E, w e * (u_pos e + u_neg e) := by
            refine Finset.sum_le_sum ?_
            intro e _
            have hp : 0 ≤ u_pos e := hu_nonneg (.inr (.inl e))
            have hn : 0 ≤ u_neg e := hu_nonneg (.inr (.inr e))
            have h_abs : |u_pos e - u_neg e| ≤ u_pos e + u_neg e :=
              abs_le.mpr ⟨by linarith, by linarith⟩
            exact mul_le_mul_of_nonneg_left h_abs (hw e)
      _ = ∑ i : I, g i * u i := h_rhs.symm
      _ = ∑ e : E, h e * y e := h_lp_eq.symm
      _ = dualObj h y := h_lhs
  have h_weak := weak_duality D w h x y hy_dual
  refine ⟨x, y, hy_dual, by linarith⟩

/-- Rational specialization (`K = ℚ`) matching Example E08 (`TFQ-0522`). -/
theorem e08_rational {V E : Type*} [Fintype V] [Fintype E]
    (D : E → V → ℚ) (w h : E → ℚ) (hw : ∀ e : E, 0 ≤ w e) :
    ∃ x : V → ℚ, ∃ y : E → ℚ,
      DualFeasible D w y ∧ cost D w h x = dualObj h y :=
  weighted_l1_strong_duality D w h hw

end StrongWeightedL1Duality

/-!
## Concrete Oriented 3-Cycle Witnesses: Non-Unique `ℓ¹` Minimizers vs. `ℓ²` Harmonic Residual
-/

section ThreeCycleWitness

/-- Oriented 3-cycle coboundary matrix `d₀ : (Fin 3 → ℚ) → (Fin 3 → ℚ)`:
edge 0 is `x₁ - x₀`, edge 1 is `x₂ - x₁`, edge 2 is `x₀ - x₂`. -/
def cycD : Fin 3 → Fin 3 → ℚ :=
  ![![-1, 1, 0], ![0, -1, 1], ![1, 0, -1]]

/-- Unit edge weights `ω = (1, 1, 1)` on the 3-cycle. -/
def cycW : Fin 3 → ℚ := ![1, 1, 1]

/-- Measured 1-cochain `c = (1, 0, 0)` on the 3-cycle. -/
def cycH : Fin 3 → ℚ := ![1, 0, 0]

/-- First optimal primal potential `g⁽¹⁾ = (0, 0, 0)`. -/
def cycX1 : Fin 3 → ℚ := ![0, 0, 0]

/-- Second optimal primal potential `g⁽²⁾ = (0, 1, 1)`. -/
def cycX2 : Fin 3 → ℚ := ![0, 1, 1]

/-- Optimal dual circulation `y* = (1, 1, 1)`. -/
def cycY : Fin 3 → ℚ := ![1, 1, 1]

/-- Harmonic (`ℓ²`-optimal) primal potential `g_harm = (0, 2/3, 1/3)`. -/
def cycXHarm : Fin 3 → ℚ := ![0, 2 / 3, 1 / 3]

/-- Residual cochain `r(x)_e = c_e - (d₀ x)_e` on the 3-cycle. -/
def cycResidual (x : Fin 3 → ℚ) (e : Fin 3) : ℚ :=
  cycH e - ∑ v : Fin 3, cycD e v * x v

/-- Dual feasibility of `y* = (1, 1, 1)` on the unit-weighted 3-cycle. -/
theorem cyc_dual_feasible : DualFeasible cycD cycW cycY := by
  refine ⟨?_, ?_⟩
  · intro v
    fin_cases v <;>
      simp [cycD, cycY, Fin.sum_univ_three]
  · intro e
    fin_cases e <;>
      simp [cycW, cycY]

/-- On the oriented 3-cycle with unit weights and `c = (1, 0, 0)`, both `cycX1` and `cycX2`
achieve cost `1`, `cycY` achieves dual objective `1`, and every potential has cost at least `1`. -/
theorem cyc_optimum :
    cost cycD cycW cycH cycX1 = 1 ∧
      cost cycD cycW cycH cycX2 = 1 ∧
      dualObj cycH cycY = 1 ∧
      (∀ x : Fin 3 → ℚ, 1 ≤ cost cycD cycW cycH x) := by
  have h1 : cost cycD cycW cycH cycX1 = 1 := by
    unfold cost
    simp [cycD, cycW, cycH, cycX1, Fin.sum_univ_three]
  have h2 : cost cycD cycW cycH cycX2 = 1 := by
    unfold cost
    simp [cycD, cycW, cycH, cycX2, Fin.sum_univ_three]
  have hd : dualObj cycH cycY = 1 := by
    unfold dualObj
    simp [cycH, cycY, Fin.sum_univ_three]
  refine ⟨h1, h2, hd, ?_⟩
  intro x
  have hw := weak_duality cycD cycW cycH x cycY cyc_dual_feasible
  linarith

/-- The two `ℓ¹`-optimal potentials `cycX1` and `cycX2` induce distinct optimal edge residuals
`(1, 0, 0)` and `(0, 0, 1)`, demonstrating non-uniqueness of the `ℓ¹` residual. -/
theorem cyc_residuals_differ : cycResidual cycX1 ≠ cycResidual cycX2 := by
  intro h_eq
  have h0 := congrFun h_eq 0
  revert h0
  simp [cycResidual, cycD, cycH, cycX1, cycX2, Fin.sum_univ_three]

/-- The harmonic potential `cycXHarm = (0, 2/3, 1/3)` yields the uniform `ℓ²` harmonic residual
`(1/3, 1/3, 1/3)` in `ker(d₀ᵀ)`, which differs from both `ℓ¹`-optimal residuals. -/
theorem cyc_harmonic :
    (∀ e : Fin 3, cycResidual cycXHarm e = 1 / 3) ∧
      (∀ v : Fin 3, ∑ e : Fin 3, cycD e v * cycResidual cycXHarm e = 0) ∧
      cycResidual cycXHarm ≠ cycResidual cycX1 ∧
      cycResidual cycXHarm ≠ cycResidual cycX2 := by
  have h_res : ∀ e : Fin 3, cycResidual cycXHarm e = 1 / 3 := by
    intro e
    fin_cases e <;>
      simp [cycResidual, cycD, cycH, cycXHarm, Fin.sum_univ_three] <;>
      norm_num
  refine ⟨h_res, ?_, ?_, ?_⟩
  · intro v
    fin_cases v <;>
      simp [h_res, cycD, Fin.sum_univ_three]
  · intro h_eq
    have h0 : cycResidual cycXHarm 0 = cycResidual cycX1 0 := congrFun h_eq 0
    rw [h_res 0] at h0
    revert h0
    simp [cycResidual, cycD, cycH, cycX1, Fin.sum_univ_three]
  · intro h_eq
    have h0 : cycResidual cycXHarm 0 = cycResidual cycX2 0 := congrFun h_eq 0
    rw [h_res 0] at h0
    revert h0
    simp [cycResidual, cycD, cycH, cycX2, Fin.sum_univ_three]

end ThreeCycleWitness

/-!
## Categorical Adjunction Triangle Laws vs. `AdjunctionCochain` Product Section/Projection
-/

section AdjunctionSeparation

/-- Explicit unit-counit triangle identities for a pair of maps `L : A → B` and `R : B → A`
equipped with unit action `η : A → A` (`R ∘ L`) and counit action `ε : B → B` (`L ∘ R`):
`ε (L a) = L a` (`counit_left`) and `R (ε b) = R b` (`unit_right`). -/
structure AdjunctionTriangleData (A B : Type*) where
  L : A → B
  R : B → A
  η : A → A := fun a => R (L a)
  ε : B → B := fun b => L (R b)
  triangle_left : ∀ a : A, L (η a) = ε (L a)
  triangle_right : ∀ b : B, R (ε b) = η (R b)

/-- Product section `x ↦ (x, 0)` from `AdjunctionCochain` in `sn_realizations.py`. -/
def adjunctionCochainSection (x : ℚ) : ℚ × ℚ := (x, 0)

/-- First-coordinate projection `(x, y) ↦ x` from `AdjunctionCochain` in `sn_realizations.py`. -/
def adjunctionCochainProj (p : ℚ × ℚ) : ℚ := p.1

/-- `adjunctionCochainSection` and `adjunctionCochainProj` satisfy the induced triangle equations
`L (R (L x)) = L x` and `R (L (R p)) = R p`, while `L ∘ R` is not the identity on `ℚ × ℚ`. -/
theorem adjunctionCochain_section_retraction :
    (∀ x : ℚ, adjunctionCochainProj (adjunctionCochainSection x) = x) ∧
      adjunctionCochainSection (adjunctionCochainProj (0, 1)) ≠ (0, 1) := by
  refine ⟨fun _ => rfl, ?_⟩
  simp [adjunctionCochainSection, adjunctionCochainProj]

/-- The matrix pair `(d₀, d₀ᵀ)` on the 3-cycle does not satisfy the section-retraction law
`d₀ᵀ (d₀ x) = x` of `AdjunctionCochain`: for `x = (1, 0, 0)`, `(d₀ᵀ (d₀ x))₀ = 2 ≠ 1`. -/
theorem adjunctionCochain_not_cycD_transpose :
    (∑ e : Fin 3, cycD e 0 * (∑ v : Fin 3, cycD e v * (![1, 0, 0] : Fin 3 → ℚ) v)) ≠
      (![1, 0, 0] : Fin 3 → ℚ) 0 := by
  simp [cycD, Fin.sum_univ_three]

end AdjunctionSeparation

end CampaignSnE08WeightedL1Duality
