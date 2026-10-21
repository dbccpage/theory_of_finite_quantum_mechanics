import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Algebra.Order.Ring.Abs
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Logic.Equiv.Fin.Rotate
import Mathlib.Data.Fin.VecNotation
import Mathlib.Algebra.Order.Field.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum

/-!
# Residual sector weights on the n-cycle are not determined by Phi1 and Gamma2

AuthorityEffect: None.  Scope: edge cochains `c : Fin n -> alpha` on the n-cycle (edge `i` joins
vertex `i` to `i+1`, indices mod `n`), the coboundary `d0 h i = h (i+1) - h i`, the holonomy
`hol c = sum c` (the class of `c` in `C^1 / im d0`) and the unweighted L1 form `l1 r = sum |r i|`.
`alpha` ranges over every commutative linearly ordered ring (in particular `Int` and `Rat`).

Results, all for general `n` and general `c`:
* `class_iff`: `r` lies in the class of `c` iff `hol r = hol c` (the image of `d0` is the sum-zero cochains);
* `phi1_attained_and_lower_bound`: `Phi1 c = min_h l1 (c - d0 h) = |hol c|`, attained;
* `minimizer_iff`: the minimizers are exactly the cochains with `hol r = hol c` and every entry of the
  sign of `hol c` (a simplex of dimension `n - 1` scaled by `|hol c|`);
* `minimizers_not_unique` / `sector_weights_not_determined`: for `n >= 2` and `hol c != 0` two minimizers have
  the same `l1` and the same `hol` but different residual and different sector weights; the node's
  "no derivation of w from Phi1 and Gamma2" is therefore a theorem for the unweighted cycle model;
* boundaries: `hol c = 0` forces the zero residual (total mass 0, which the node refuses), and `n = 1`
  has a unique minimizer, so non-uniqueness needs `n >= 2` and `hol c != 0`;
* `symmetric_selector`: over a field, the rotation-invariant minimizer exists and is unique, equal to the
  constant `hol c / n`; over `Int` it exists iff `n` divides `hol c` (`symmetric_integral_iff`).  The
  symmetry is an extra input; it is not derived from Phi1 and Gamma2.

`Gamma2` is MODELLED here as the holonomy (the class invariant, as in the TFQ-0354 syndrome); the repository
witness that reads `Gamma_2` as the sum of squares of the weights is not a theorem of this module (the native table
shows the sum of squares is not constant on the minimizers once `|hol c| >= 2`).  All results are for EQUAL edge masses.
With unequal positive masses the minimizer of `sum m_i |r_i|` sits on the edges of minimal mass and is unique when the
minimum is attained once, so non-derivability can fail in the weighted setting; only native rows cover that.

Not claimed: the weighted L1 form (the declared form in the window definition), the Hilbert lift,
any physical reading of the sector weights.  The source `DerivationDagQMClosure` declarations are
fixed `Fin 4` instances and a list-sum additivity; the C4 instances are re-derived here as instances
(`c4_instance_two_minimizers`) and the source "orbit sum" `(1,1,1,1)` is shown not to be a minimizer
(`c4_orbit_sum_not_minimizer`): the canonical weights are the orbit average, not the orbit sum.
-/

namespace ResidualSectorWeights

open Finset

section Core

variable {α : Type*} [CommRing α] [LinearOrder α] [IsStrictOrderedRing α]

/-- Coboundary on the n-cycle: `(d0 h) i = h (i+1) - h i`. -/
def d0 {n : ℕ} (h : Fin n → α) : Fin n → α := fun i => h (finRotate n i) - h i

/-- Holonomy (total residual): the class invariant of an edge cochain. -/
def hol {n : ℕ} (c : Fin n → α) : α := ∑ i, c i

/-- Unweighted L1 form of an edge residual. -/
def l1 {n : ℕ} (r : Fin n → α) : α := ∑ i, |r i|

/-- `r` is in the class of `c` in `C^1 / im d0`. -/
def InClass {n : ℕ} (c r : Fin n → α) : Prop := ∃ h : Fin n → α, r = fun i => c i - d0 h i

/-- `r` minimises the L1 form on the class of `c`. -/
def IsMin {n : ℕ} (c r : Fin n → α) : Prop := InClass c r ∧ ∀ r', InClass c r' → l1 r ≤ l1 r'

theorem hol_d0 {n : ℕ} (h : Fin n → α) : hol (d0 h) = 0 := by
  unfold hol d0
  rw [Finset.sum_sub_distrib]
  have := Equiv.sum_comp (finRotate n) h
  rw [this]; simp

/-- The image of `d0` is exactly the sum-zero cochains. -/
theorem exists_d0_of_hol_zero {n : ℕ} (r : Fin n → α) (hr : hol r = 0) : ∃ h : Fin n → α, d0 h = r := by
  cases n with
  | zero => exact ⟨fun _ => 0, funext fun i => i.elim0⟩
  | succ m =>
    let rr : ℕ → α := fun k => if hk : k < m + 1 then r ⟨k, hk⟩ else 0
    let h : Fin (m + 1) → α := fun i => ∑ k ∈ Finset.range i.val, rr k
    have htot : ∑ k ∈ Finset.range (m + 1), rr k = 0 := by
      rw [← Fin.sum_univ_eq_sum_range (fun k => rr k) (m + 1)]
      have : ∀ i : Fin (m + 1), rr i.val = r i := fun i => by simp [rr, i.isLt]
      simp only [this]; exact hr
    refine ⟨h, funext fun i => ?_⟩
    by_cases hi : i.val < m
    · have e : finRotate (m + 1) i = ⟨i.val + 1, by omega⟩ := by
        have := finRotate_of_lt (n := m) (k := i.val) hi
        simpa using this
      simp only [d0, e, h]
      rw [Finset.sum_range_succ]
      have : rr i.val = r i := by simp [rr, i.isLt]
      rw [this]; ring
    · have hm : i = Fin.last m := Fin.ext (by have := i.isLt; simp; omega)
      subst hm
      simp only [d0, finRotate_last, h]
      rw [Finset.sum_range_succ] at htot
      have : rr m = r (Fin.last m) := by
        show (if hk : m < m + 1 then r ⟨m, hk⟩ else 0) = _
        rw [dif_pos (Nat.lt_succ_self m)]; rfl
      rw [this] at htot
      simp only [Fin.val_zero, Finset.range_zero, Finset.sum_empty, Fin.val_last]
      linarith

theorem hol_sub {n : ℕ} (c r : Fin n → α) : hol (fun i => c i - r i) = hol c - hol r := by
  unfold hol; rw [Finset.sum_sub_distrib]

/-- Class membership is decided by the holonomy alone. -/
theorem class_iff {n : ℕ} (c r : Fin n → α) : InClass c r ↔ hol r = hol c := by
  constructor
  · rintro ⟨h, rfl⟩
    have := hol_d0 h
    rw [hol_sub]; linarith
  · intro hr
    obtain ⟨h, hh⟩ := exists_d0_of_hol_zero (fun i => c i - r i) (by rw [hol_sub]; linarith)
    refine ⟨h, funext fun i => ?_⟩
    have := congrFun hh i
    linarith

/-- Lower bound: every residual in the class has L1 form at least `|hol|`. -/
theorem abs_hol_le_l1 {n : ℕ} (r : Fin n → α) : |hol r| ≤ l1 r :=
  Finset.abs_sum_le_sum_abs _ _

theorem lower_bound {n : ℕ} (c r : Fin n → α) (h : InClass c r) : |hol c| ≤ l1 r := by
  rw [(class_iff c r).mp h |>.symm]; exact abs_hol_le_l1 r

theorem hol_single {n : ℕ} (i : Fin n) (s : α) : hol (Pi.single i s : Fin n → α) = s := by
  unfold hol; simp

theorem l1_single {n : ℕ} (i : Fin n) (s : α) : l1 (Pi.single i s : Fin n → α) = |s| := by
  unfold l1
  have : ∀ k : Fin n, |(Pi.single i s : Fin n → α) k| = (Pi.single i |s| : Fin n → α) k := by
    intro k
    by_cases hk : k = i
    · subst hk; simp
    · simp [Pi.single_apply, hk]
  simp only [this]; simp

/-- `Phi1 c = |hol c|`, attained by the single-edge residual. -/
theorem phi1_attained_and_lower_bound {n : ℕ} (c : Fin n → α) :
    (∀ r, InClass c r → |hol c| ≤ l1 r) ∧ ∃ r, InClass c r ∧ l1 r = |hol c| := by
  refine ⟨lower_bound c, ?_⟩
  rcases isEmpty_or_nonempty (Fin n) with hn | ⟨⟨i0⟩⟩
  · refine ⟨c, (class_iff c c).mpr rfl, ?_⟩
    simp [l1, hol]
  · refine ⟨Pi.single i0 (hol c), (class_iff _ _).mpr (hol_single i0 _), l1_single i0 _⟩

/-- Equality in the triangle inequality for sums: sign-definiteness. -/
theorem l1_eq_abs_hol_iff {n : ℕ} (r : Fin n → α) :
    l1 r = |hol r| ↔ ((0 ≤ hol r → ∀ i, 0 ≤ r i) ∧ (hol r ≤ 0 → ∀ i, r i ≤ 0)) := by
  constructor
  · intro h
    refine ⟨fun hs i => ?_, fun hs i => ?_⟩
    · rw [abs_of_nonneg hs] at h
      have hz : ∑ k, (|r k| - r k) = 0 := by
        rw [Finset.sum_sub_distrib]; unfold l1 hol at *; linarith
      have := (Finset.sum_eq_zero_iff_of_nonneg (fun k _ => sub_nonneg.mpr (le_abs_self (r k)))).mp hz i (mem_univ i)
      have h2 : |r i| = r i := by linarith
      exact abs_eq_self.mp h2
    · rw [abs_of_nonpos hs] at h
      have hz : ∑ k, (|r k| + r k) = 0 := by
        rw [Finset.sum_add_distrib]; unfold l1 hol at *; linarith
      have := (Finset.sum_eq_zero_iff_of_nonneg (fun k _ => by
        have := neg_abs_le (r k); linarith)).mp hz i (mem_univ i)
      have h2 : |r i| = - r i := by linarith
      exact abs_eq_neg_self.mp h2
  · rintro ⟨h1, h2⟩
    rcases le_total 0 (hol r) with hs | hs
    · rw [abs_of_nonneg hs]
      unfold l1; unfold hol at hs ⊢
      exact Finset.sum_congr rfl fun i _ => abs_of_nonneg (h1 hs i)
    · rw [abs_of_nonpos hs]
      unfold l1; unfold hol at hs ⊢
      rw [← Finset.sum_neg_distrib]
      exact Finset.sum_congr rfl fun i _ => abs_of_nonpos (h2 hs i)

theorem isMin_iff {n : ℕ} (c r : Fin n → α) : IsMin c r ↔ InClass c r ∧ l1 r = |hol c| := by
  constructor
  · rintro ⟨hc, hm⟩
    obtain ⟨_, r0, hr0, hl⟩ := phi1_attained_and_lower_bound c
    exact ⟨hc, le_antisymm (hl ▸ hm r0 hr0) (lower_bound c r hc)⟩
  · rintro ⟨hc, hl⟩
    exact ⟨hc, fun r' h' => hl ▸ lower_bound c r' h'⟩

/-- The minimisers are exactly the cochains of the right holonomy whose entries all have the sign of it. -/
theorem minimizer_iff {n : ℕ} (c r : Fin n → α) :
    IsMin c r ↔ hol r = hol c ∧ ((0 ≤ hol c → ∀ i, 0 ≤ r i) ∧ (hol c ≤ 0 → ∀ i, r i ≤ 0)) := by
  rw [isMin_iff, class_iff]
  constructor
  · rintro ⟨h1, h2⟩
    refine ⟨h1, ?_⟩
    have := (l1_eq_abs_hol_iff r).mp (by rw [h1]; exact h2)
    rwa [h1] at this
  · rintro ⟨h1, h2⟩
    refine ⟨h1, ?_⟩
    have := (l1_eq_abs_hol_iff r).mpr (by rw [h1]; exact h2)
    rwa [h1] at this

/-- Two minimisers with the same `Phi1` and the same holonomy `Gamma2`, but different residuals and different
sector weights, whenever there are at least two edges and the holonomy is nonzero. -/
theorem minimizers_not_unique {n : ℕ} (c : Fin n → α) (i j : Fin n) (hij : i ≠ j) (hs : hol c ≠ 0) :
    ∃ r r' : Fin n → α, IsMin c r ∧ IsMin c r' ∧ l1 r = l1 r' ∧ hol r = hol r' ∧ r ≠ r' ∧
      (fun k => |r k|) ≠ (fun k => |r' k|) := by
  have mk : ∀ k : Fin n, IsMin c (Pi.single k (hol c)) := by
    intro k
    rw [minimizer_iff, hol_single]
    refine ⟨rfl, fun h0 m => ?_, fun h0 m => ?_⟩
    · by_cases hm : m = k
      · subst hm; simpa using h0
      · simp [Pi.single_apply, hm]
    · by_cases hm : m = k
      · subst hm; simpa using h0
      · simp [Pi.single_apply, hm]
  refine ⟨Pi.single i (hol c), Pi.single j (hol c), mk i, mk j, ?_, ?_, ?_, ?_⟩
  · rw [l1_single, l1_single]
  · rw [hol_single, hol_single]
  · intro h
    have := congrFun h i
    simp [Pi.single_apply, hij] at this
    exact hs this
  · intro h
    have := congrFun h i
    simp [Pi.single_apply, hij] at this
    exact hs this

/-- Sector weights add up to `Phi1` for every minimiser and every split of the edges into two sectors. -/
theorem sector_weights_sum_to_phi1 {n : ℕ} (c r : Fin n → α) (hm : IsMin c r) (A : Finset (Fin n)) :
    (∑ k ∈ A, |r k|) + (∑ k ∈ Aᶜ, |r k|) = |hol c| := by
  rw [Finset.sum_add_sum_compl]
  exact ((isMin_iff c r).mp hm).2

/-- The sector weights of a bipartition into two nonempty sectors are not determined by `Phi1` and `Gamma2`. -/
theorem sector_weights_not_determined {n : ℕ} (c : Fin n → α) (A : Finset (Fin n)) (i j : Fin n)
    (hi : i ∈ A) (hj : j ∉ A) (hs : hol c ≠ 0) :
    ∃ r r' : Fin n → α, IsMin c r ∧ IsMin c r' ∧ l1 r = l1 r' ∧ hol r = hol r' ∧
      (∑ k ∈ A, |r k|) ≠ (∑ k ∈ A, |r' k|) := by
  have hij : i ≠ j := fun h => hj (h ▸ hi)
  obtain ⟨r, r', h1, h2, h3, h4, -, -⟩ := minimizers_not_unique c i j hij hs
  have mk : ∀ k : Fin n, IsMin c (Pi.single k (hol c)) := by
    intro k
    rw [minimizer_iff, hol_single]
    refine ⟨rfl, fun h0 m => ?_, fun h0 m => ?_⟩
    · by_cases hm : m = k
      · subst hm; simpa using h0
      · simp [Pi.single_apply, hm]
    · by_cases hm : m = k
      · subst hm; simpa using h0
      · simp [Pi.single_apply, hm]
  refine ⟨Pi.single i (hol c), Pi.single j (hol c), mk i, mk j, by rw [l1_single, l1_single],
    by rw [hol_single, hol_single], ?_⟩
  have e1 : ∑ k ∈ A, |(Pi.single i (hol c) : Fin n → α) k| = |hol c| := by
    have : ∀ k : Fin n, |(Pi.single i (hol c) : Fin n → α) k| = (Pi.single i |hol c| : Fin n → α) k := by
      intro k
      by_cases hk : k = i
      · subst hk; simp
      · simp [Pi.single_apply, hk]
    simp only [this]
    rw [Finset.sum_pi_single' i |hol c| A]; simp [hi]
  have e2 : ∑ k ∈ A, |(Pi.single j (hol c) : Fin n → α) k| = 0 := by
    apply Finset.sum_eq_zero
    intro k hk
    have : k ≠ j := fun h => hj (h ▸ hk)
    simp [Pi.single_apply, this]
  rw [e1, e2]
  exact fun h => hs (abs_eq_zero.mp h)

/-- Boundary: a zero holonomy has the zero residual as its only minimiser (total mass 0, which the node refuses). -/
theorem minimizer_unique_of_hol_zero {n : ℕ} (c r : Fin n → α) (hs : hol c = 0) (hm : IsMin c r) :
    r = fun _ => 0 := by
  rw [minimizer_iff] at hm
  obtain ⟨-, h1, h2⟩ := hm
  funext i
  exact le_antisymm (h2 hs.le i) (h1 hs.ge i)

/-- Boundary: with one edge the minimiser is unique, so non-uniqueness needs `n >= 2`. -/
theorem minimizer_unique_of_one_edge (c r r' : Fin 1 → α) (h : IsMin c r) (h' : IsMin c r') : r = r' := by
  rw [minimizer_iff] at h h'
  funext i
  have i0 : i = 0 := Subsingleton.elim _ _
  subst i0
  have e1 : hol r = r 0 := by simp [hol]
  have e2 : hol r' = r' 0 := by simp [hol]
  rw [← e1, ← e2, h.1, h'.1]

end Core

section Symmetric

variable {α : Type*} [CommRing α] [LinearOrder α] [IsStrictOrderedRing α]

/-- Invariance under the cyclic rotation of the edges (any dihedral group containing the rotation also acts). -/
def Inv {n : ℕ} (r : Fin n → α) : Prop := ∀ i, r (finRotate n i) = r i

theorem inv_const {n : ℕ} (r : Fin n → α) (h : Inv r) (i j : Fin n) : r i = r j := by
  cases n with
  | zero => exact i.elim0
  | succ m =>
    have key : ∀ k (hk : k < m + 1), r ⟨k, hk⟩ = r ⟨0, Nat.succ_pos m⟩ := by
      intro k
      induction k with
      | zero => intro hk; rfl
      | succ k ih =>
        intro hk
        have e : finRotate (m + 1) ⟨k, by omega⟩ = ⟨k + 1, hk⟩ := by
          have := finRotate_of_lt (n := m) (k := k) (by omega)
          simpa using this
        have := h ⟨k, by omega⟩
        rw [e] at this
        rw [this]; exact ih (by omega)
    rw [show i = ⟨i.val, i.isLt⟩ from rfl, key _ i.isLt, key _ j.isLt]

/-- Over `Int` the rotation-invariant minimiser exists iff `n` divides the holonomy. -/
theorem symmetric_integral_iff {n : ℕ} (hn : 0 < n) (c : Fin n → ℤ) :
    (∃ r : Fin n → ℤ, IsMin c r ∧ Inv r) ↔ (n : ℤ) ∣ hol c := by
  constructor
  · rintro ⟨r, hm, hi⟩
    rw [minimizer_iff] at hm
    have i0 : Fin n := ⟨0, hn⟩
    have hc : ∀ i, r i = r ⟨0, hn⟩ := fun i => inv_const r hi i _
    refine ⟨r ⟨0, hn⟩, ?_⟩
    rw [← hm.1]; unfold hol; simp [hc]
  · rintro ⟨v, hv⟩
    refine ⟨fun _ => v, ?_, fun _ => rfl⟩
    rw [minimizer_iff]
    have hnz : (0 : ℤ) < n := by exact_mod_cast hn
    have hh : hol (fun _ : Fin n => v) = hol c := by unfold hol at *; simp [hv]
    refine ⟨hh, fun h0 _ => ?_, fun h0 _ => ?_⟩
    · rw [hv] at h0; exact nonneg_of_mul_nonneg_right h0 hnz
    · rw [hv] at h0; exact nonpos_of_mul_nonpos_right h0 hnz

end Symmetric

section SymmetricField

variable {α : Type*} [Field α] [LinearOrder α] [IsStrictOrderedRing α]

/-- Over a field the rotation-invariant minimiser exists, is unique, and is the constant `hol c / n`.
This is the "symmetry selector": it needs the rotation symmetry as an extra declared input. -/
theorem symmetric_selector {n : ℕ} (hn : 0 < n) (c : Fin n → α) :
    IsMin c (fun _ => hol c / n) ∧ Inv (fun _ : Fin n => hol c / n) ∧
      ∀ r : Fin n → α, IsMin c r → Inv r → r = fun _ => hol c / n := by
  have hnz : (0 : α) < n := by exact_mod_cast hn
  have hsum : hol (fun _ : Fin n => hol c / n) = hol c := by
    unfold hol; simp [Finset.sum_const]
    field_simp
  refine ⟨?_, fun _ => rfl, ?_⟩
  · rw [minimizer_iff]
    refine ⟨hsum, fun h0 _ => div_nonneg h0 hnz.le, fun h0 _ => div_nonpos_of_nonpos_of_nonneg h0 hnz.le⟩
  · intro r hm hi
    rw [minimizer_iff] at hm
    have hc : ∀ i, r i = r ⟨0, hn⟩ := fun i => inv_const r hi i _
    have : hol r = n * r ⟨0, hn⟩ := by unfold hol; simp [hc]
    funext i
    rw [hc i]
    have h2 := hm.1
    rw [this] at h2
    field_simp
    linarith

end SymmetricField

section Instances

/-- INSTANCE (the source's C4 data, as a corollary and not as the statement): over `Rat`, the two single-edge
residuals `(1,0,0,0)` and `(0,1,0,0)` are minimisers of the class with holonomy 1 and are different. -/
theorem c4_instance_two_minimizers :
    let c : Fin 4 → ℚ := ![1, 0, 0, 0]
    IsMin c ![1, 0, 0, 0] ∧ IsMin c ![0, 1, 0, 0] ∧ (![1, 0, 0, 0] : Fin 4 → ℚ) ≠ ![0, 1, 0, 0] := by
  intro c
  refine ⟨?_, ?_, ?_⟩
  · rw [minimizer_iff]
    refine ⟨?_, fun _ i => ?_, fun h i => ?_⟩
    · simp [hol, c, Fin.sum_univ_four]
    · fin_cases i <;> simp
    · exfalso; simp [hol, c, Fin.sum_univ_four] at h; norm_num at h
  · rw [minimizer_iff]
    refine ⟨?_, fun _ i => ?_, fun h i => ?_⟩
    · simp [hol, c, Fin.sum_univ_four]
    · fin_cases i <;> simp
    · exfalso; simp [hol, c, Fin.sum_univ_four] at h; norm_num at h
  · intro h
    have := congrFun h 0
    simp at this

/-- INSTANCE: the source's "orbit sum" `(1,1,1,1)` of `(1,0,1,0)` and `(0,1,0,1)` has holonomy 4, not 2, so it
is not in the class (hence not a minimiser) of those residuals; the canonical symmetric point is the orbit
average `(1/2,1/2,1/2,1/2)`. -/
theorem c4_orbit_sum_not_minimizer :
    let c : Fin 4 → ℚ := ![1, 0, 1, 0]
    ¬ IsMin c ![1, 1, 1, 1] ∧ IsMin c (fun _ => hol c / (4 : ℕ)) := by
  intro c
  refine ⟨?_, (symmetric_selector (by norm_num) c).1⟩
  rw [minimizer_iff]
  rintro ⟨h, -⟩
  simp [hol, c, Fin.sum_univ_four] at h
  norm_num at h

end Instances

end ResidualSectorWeights

#print axioms ResidualSectorWeights.hol_d0
#print axioms ResidualSectorWeights.exists_d0_of_hol_zero
#print axioms ResidualSectorWeights.class_iff
#print axioms ResidualSectorWeights.phi1_attained_and_lower_bound
#print axioms ResidualSectorWeights.minimizer_iff
#print axioms ResidualSectorWeights.minimizers_not_unique
#print axioms ResidualSectorWeights.sector_weights_sum_to_phi1
#print axioms ResidualSectorWeights.sector_weights_not_determined
#print axioms ResidualSectorWeights.minimizer_unique_of_hol_zero
#print axioms ResidualSectorWeights.minimizer_unique_of_one_edge
#print axioms ResidualSectorWeights.symmetric_integral_iff
#print axioms ResidualSectorWeights.symmetric_selector
#print axioms ResidualSectorWeights.c4_instance_two_minimizers
#print axioms ResidualSectorWeights.c4_orbit_sum_not_minimizer
