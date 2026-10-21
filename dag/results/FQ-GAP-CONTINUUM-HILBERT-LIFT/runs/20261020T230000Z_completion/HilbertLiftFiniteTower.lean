import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Algebra.BigOperators.Finsupp.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Data.Finsupp.SMulWithZero
import Mathlib.Tactic.Linarith

/-!
# Exact finite carriers and their directed union

Origin: dag/results/FQ-GAP-CONTINUUM-HILBERT-LIFT/runs/20261020T230000Z_completion
Claim: the exact finite carriers `Fin n → ℚ` with the rational inner product form a tower under
zero padding; its directed union is the finitely supported rational sequences `ℕ →₀ ℚ`, exhausted
by the finite stages, with an exact rational inner product satisfying Cauchy–Schwarz.
AuthorityEffect: None
Scope Fence: no topology, no completion and no real or complex number is used in this module;
every statement is exact rational algebra on supplied carriers.
Level: L5

The finite carrier at report size `n` is `FinCarrier n := Fin n → ℚ`, the carrier a finite
report set supplies (integer weights sit inside it).  `pad h` is zero padding along `n ≤ m`;
it is `ℚ`-linear, injective, functorial (`pad_refl`, `pad_trans`) and inner-product preserving
(`finInner_pad`).  The colimit carrier is `Carrier := ℕ →₀ ℚ` with `ofFin` the canonical
injections; `ofFin_pad` is the cocone identity, `exhaustion` says every exact sequence comes
from some finite stage, `trunc` is the left inverse, and `qinner` is the exact inner product
with `qinner_ofFin` the restriction identity.  `qinner_sq_le` is Cauchy–Schwarz over `ℚ`,
proved from Mathlib's finite-sum inequality, and `two_mul_qinner_le` is the arithmetic–quadratic
bound that later replaces every square root.
-/

namespace HilbertLift

open Finset

/-- The exact finite carrier at report size `n`: rational coordinates on `Fin n`. -/
abbrev FinCarrier (n : ℕ) : Type := Fin n → ℚ

/-- The exact rational inner product of the finite carrier. -/
def finInner {n : ℕ} (x y : FinCarrier n) : ℚ := ∑ i, x i * y i

/-- Extension by zero of a finite carrier vector to all of `ℕ`. -/
def ext {n : ℕ} (x : FinCarrier n) : ℕ → ℚ :=
  fun i => if h : i < n then x ⟨i, h⟩ else 0

theorem ext_of_lt {n : ℕ} (x : FinCarrier n) {i : ℕ} (h : i < n) : ext x i = x ⟨i, h⟩ := by
  simp [ext, h]

theorem ext_of_le {n : ℕ} (x : FinCarrier n) {i : ℕ} (h : n ≤ i) : ext x i = 0 := by
  simp [ext, not_lt.mpr h]

theorem ext_fin {n : ℕ} (x : FinCarrier n) (i : Fin n) : ext x i = x i := by
  rw [ext_of_lt x i.isLt]

/-- Zero padding from report size `n` to report size `m ≥ n`. -/
def pad {n m : ℕ} (_h : n ≤ m) (x : FinCarrier n) : FinCarrier m :=
  fun j => ext x j

theorem pad_apply {n m : ℕ} (h : n ≤ m) (x : FinCarrier n) (j : Fin m) :
    pad h x j = ext x j := rfl

theorem pad_refl {n : ℕ} (x : FinCarrier n) : pad (le_refl n) x = x := by
  funext j
  exact ext_fin x j

theorem ext_pad {n m : ℕ} (h : n ≤ m) (x : FinCarrier n) : ext (pad h x) = ext x := by
  funext i
  by_cases hi : i < m
  · rw [ext_of_lt _ hi]
    rfl
  · rw [ext_of_le _ (not_lt.mp hi), ext_of_le x (h.trans (not_lt.mp hi))]

theorem pad_trans {n m k : ℕ} (h₁ : n ≤ m) (h₂ : m ≤ k) (x : FinCarrier n) :
    pad h₂ (pad h₁ x) = pad (h₁.trans h₂) x := by
  funext j
  rw [pad_apply, ext_pad]
  rfl

theorem pad_add {n m : ℕ} (h : n ≤ m) (x y : FinCarrier n) :
    pad h (x + y) = pad h x + pad h y := by
  funext j
  by_cases hj : (j : ℕ) < n
  · simp [pad, ext, hj]
  · simp [pad, ext, hj]

theorem pad_smul {n m : ℕ} (h : n ≤ m) (c : ℚ) (x : FinCarrier n) :
    pad h (c • x) = c • pad h x := by
  funext j
  by_cases hj : (j : ℕ) < n
  · simp [pad, ext, hj]
  · simp [pad, ext, hj]

theorem pad_injective {n m : ℕ} (h : n ≤ m) : Function.Injective (pad h) := by
  intro x y hxy
  funext i
  have hi : (i : ℕ) < m := lt_of_lt_of_le i.isLt h
  have := congrFun hxy ⟨i, hi⟩
  rw [pad_apply, pad_apply] at this
  simp only [ext_of_lt x i.isLt, ext_of_lt y i.isLt] at this
  exact this

/-- The exact colimit carrier: finitely supported rational sequences. -/
abbrev Carrier : Type := ℕ →₀ ℚ

/-- The exact rational inner product on the colimit carrier. -/
def qinner (f g : Carrier) : ℚ := f.sum fun i a => a * g i

theorem qinner_eq_sum (f g : Carrier) {s : Finset ℕ} (hs : f.support ⊆ s) :
    qinner f g = ∑ i ∈ s, f i * g i :=
  Finsupp.sum_of_support_subset f hs _ (fun _ _ => zero_mul _)

theorem qinner_comm (f g : Carrier) : qinner f g = qinner g f := by
  rw [qinner_eq_sum f g (s := f.support ∪ g.support) subset_union_left,
    qinner_eq_sum g f (s := f.support ∪ g.support) subset_union_right]
  exact Finset.sum_congr rfl fun i _ => mul_comm _ _

theorem qinner_add_left (f g h : Carrier) : qinner (f + g) h = qinner f h + qinner g h := by
  classical
  rw [qinner_eq_sum (f + g) h (s := f.support ∪ g.support) Finsupp.support_add,
    qinner_eq_sum f h (s := f.support ∪ g.support) subset_union_left,
    qinner_eq_sum g h (s := f.support ∪ g.support) subset_union_right,
    ← Finset.sum_add_distrib]
  exact Finset.sum_congr rfl fun i _ => by rw [Finsupp.add_apply, add_mul]

theorem qinner_sub_left (f g h : Carrier) : qinner (f - g) h = qinner f h - qinner g h := by
  classical
  rw [qinner_eq_sum (f - g) h (s := f.support ∪ g.support) Finsupp.support_sub,
    qinner_eq_sum f h (s := f.support ∪ g.support) subset_union_left,
    qinner_eq_sum g h (s := f.support ∪ g.support) subset_union_right,
    ← Finset.sum_sub_distrib]
  exact Finset.sum_congr rfl fun i _ => by rw [Finsupp.sub_apply, sub_mul]

theorem qinner_smul_left (c : ℚ) (f g : Carrier) : qinner (c • f) g = c * qinner f g := by
  rw [qinner_eq_sum (c • f) g (s := f.support) Finsupp.support_smul,
    qinner_eq_sum f g (subset_refl _), Finset.mul_sum]
  exact Finset.sum_congr rfl fun i _ => by rw [Finsupp.smul_apply, smul_eq_mul, mul_assoc]

theorem qinner_add_right (f g h : Carrier) : qinner f (g + h) = qinner f g + qinner f h := by
  rw [qinner_comm, qinner_add_left, qinner_comm g, qinner_comm h]

theorem qinner_sub_right (f g h : Carrier) : qinner f (g - h) = qinner f g - qinner f h := by
  rw [qinner_comm, qinner_sub_left, qinner_comm g, qinner_comm h]

theorem qinner_smul_right (c : ℚ) (f g : Carrier) : qinner f (c • g) = c * qinner f g := by
  rw [qinner_comm, qinner_smul_left, qinner_comm]

theorem qinner_self_nonneg (f : Carrier) : 0 ≤ qinner f f := by
  rw [qinner_eq_sum f f (subset_refl _)]
  exact Finset.sum_nonneg fun i _ => mul_self_nonneg _

theorem mul_self_apply_le_qinner_self (f : Carrier) (i : ℕ) : f i * f i ≤ qinner f f := by
  rw [qinner_eq_sum f f (subset_refl _)]
  by_cases hi : i ∈ f.support
  · exact Finset.single_le_sum (fun j _ => mul_self_nonneg (f j)) hi
  · rw [Finsupp.notMem_support_iff.mp hi, mul_zero]
    exact Finset.sum_nonneg fun j _ => mul_self_nonneg _

theorem qinner_self_eq_zero_iff (f : Carrier) : qinner f f = 0 ↔ f = 0 := by
  constructor
  · intro h
    ext i
    have h1 := mul_self_apply_le_qinner_self f i
    rw [h] at h1
    have h2 : f i * f i = 0 := le_antisymm h1 (mul_self_nonneg _)
    simpa using mul_self_eq_zero.mp h2
  · rintro rfl
    simp [qinner]

/-- Cauchy–Schwarz over `ℚ`, from Mathlib's finite-sum inequality. -/
theorem qinner_sq_le (f g : Carrier) : qinner f g ^ 2 ≤ qinner f f * qinner g g := by
  rw [qinner_eq_sum f g (s := f.support ∪ g.support) subset_union_left,
    qinner_eq_sum f f (s := f.support ∪ g.support) subset_union_left,
    qinner_eq_sum g g (s := f.support ∪ g.support) subset_union_right]
  have h := Finset.sum_mul_sq_le_sq_mul_sq (f.support ∪ g.support) (fun i => f i) (fun i => g i)
  simpa only [sq] using h

/-- The arithmetic–quadratic bound; it replaces every square root in the later modules. -/
theorem two_mul_qinner_le (f g : Carrier) : 2 * qinner f g ≤ qinner f f + qinner g g := by
  have h := qinner_self_nonneg (f - g)
  rw [qinner_sub_left, qinner_sub_right, qinner_sub_right, qinner_comm g f] at h
  linarith

/-- Canonical injection of the stage-`n` carrier into the colimit carrier. -/
noncomputable def ofFin {n : ℕ} (x : FinCarrier n) : Carrier :=
  Finsupp.onFinset (range n) (ext x) fun i hi => by
    by_contra h
    exact hi (ext_of_le x (not_lt.mp fun h' => h (mem_range.mpr h')))

@[simp] theorem ofFin_apply {n : ℕ} (x : FinCarrier n) (i : ℕ) : ofFin x i = ext x i :=
  Finsupp.onFinset_apply

theorem support_ofFin_subset {n : ℕ} (x : FinCarrier n) : (ofFin x).support ⊆ range n :=
  Finsupp.support_onFinset_subset

/-- The cocone identity: padding does not change the exact sequence. -/
theorem ofFin_pad {n m : ℕ} (h : n ≤ m) (x : FinCarrier n) : ofFin (pad h x) = ofFin x :=
  Finsupp.ext fun i => by rw [ofFin_apply, ofFin_apply, ext_pad]

theorem ofFin_injective {n : ℕ} : Function.Injective (ofFin (n := n)) := by
  intro x y hxy
  funext i
  have := congrArg (fun f : Carrier => f i) hxy
  simp only [ofFin_apply, ext_fin] at this
  exact this

theorem ofFin_add {n : ℕ} (x y : FinCarrier n) : ofFin (x + y) = ofFin x + ofFin y :=
  Finsupp.ext fun i => by
    rw [Finsupp.add_apply, ofFin_apply, ofFin_apply, ofFin_apply]
    by_cases hi : i < n
    · simp [ext, hi]
    · simp [ext, hi]

theorem ofFin_smul {n : ℕ} (c : ℚ) (x : FinCarrier n) : ofFin (c • x) = c • ofFin x :=
  Finsupp.ext fun i => by
    rw [Finsupp.smul_apply, ofFin_apply, ofFin_apply]
    by_cases hi : i < n
    · simp [ext, hi]
    · simp [ext, hi]

/-- The restriction identity: the exact inner product restricts to the finite one. -/
theorem qinner_ofFin {n : ℕ} (x y : FinCarrier n) : qinner (ofFin x) (ofFin y) = finInner x y := by
  rw [qinner_eq_sum _ _ (support_ofFin_subset x)]
  simp only [ofFin_apply]
  unfold finInner
  rw [← Fin.sum_univ_eq_sum_range (fun i => ext x i * ext y i) n]
  exact Finset.sum_congr rfl fun i _ => by rw [ext_fin, ext_fin]

/-- Zero padding preserves the exact inner product. -/
theorem finInner_pad {n m : ℕ} (h : n ≤ m) (x y : FinCarrier n) :
    finInner (pad h x) (pad h y) = finInner x y := by
  rw [← qinner_ofFin, ofFin_pad, ofFin_pad, qinner_ofFin]

theorem finInner_self_nonneg {n : ℕ} (x : FinCarrier n) : 0 ≤ finInner x x := by
  rw [← qinner_ofFin]
  exact qinner_self_nonneg _

theorem finInner_sq_le {n : ℕ} (x y : FinCarrier n) :
    finInner x y ^ 2 ≤ finInner x x * finInner y y := by
  rw [← qinner_ofFin, ← qinner_ofFin, ← qinner_ofFin]
  exact qinner_sq_le _ _

/-- Truncation of an exact sequence to report size `n`. -/
def trunc (n : ℕ) (f : Carrier) : FinCarrier n := fun i => f i

theorem trunc_ofFin {n : ℕ} (x : FinCarrier n) : trunc n (ofFin x) = x := by
  funext i
  simp [trunc, ext_fin]

theorem ofFin_trunc (n : ℕ) (f : Carrier) (hf : f.support ⊆ range n) : ofFin (trunc n f) = f :=
  Finsupp.ext fun i => by
    rw [ofFin_apply]
    by_cases hi : i < n
    · rw [ext_of_lt _ hi]
      rfl
    · rw [ext_of_le _ (not_lt.mp hi)]
      symm
      exact Finsupp.notMem_support_iff.mp fun h => hi (mem_range.mp (hf h))

/-- Exhaustion: every exact sequence lives at some finite report size. -/
theorem exhaustion (f : Carrier) : ∃ n : ℕ, ∃ x : FinCarrier n, ofFin x = f := by
  obtain ⟨n, hn⟩ := Finset.exists_nat_subset_range f.support
  exact ⟨n, trunc n f, ofFin_trunc n f hn⟩

/-- Bessel-type inequality for coordinate truncation. -/
theorem finInner_trunc_le (n : ℕ) (f : Carrier) :
    finInner (trunc n f) (trunc n f) ≤ qinner f f := by
  classical
  rw [← qinner_ofFin,
    qinner_eq_sum _ _ (s := f.support ∪ range n) ((support_ofFin_subset _).trans subset_union_right),
    qinner_eq_sum f f (s := f.support ∪ range n) subset_union_left]
  refine Finset.sum_le_sum fun i _ => ?_
  rw [ofFin_apply]
  by_cases hi : i < n
  · rw [ext_of_lt _ hi]
    exact le_rfl
  · rw [ext_of_le _ (not_lt.mp hi), mul_zero]
    exact mul_self_nonneg _

end HilbertLift

#print axioms HilbertLift.pad_refl
#print axioms HilbertLift.pad_trans
#print axioms HilbertLift.pad_add
#print axioms HilbertLift.pad_smul
#print axioms HilbertLift.pad_injective
#print axioms HilbertLift.qinner_comm
#print axioms HilbertLift.qinner_add_left
#print axioms HilbertLift.qinner_sub_left
#print axioms HilbertLift.qinner_smul_left
#print axioms HilbertLift.qinner_add_right
#print axioms HilbertLift.qinner_sub_right
#print axioms HilbertLift.qinner_smul_right
#print axioms HilbertLift.qinner_self_nonneg
#print axioms HilbertLift.mul_self_apply_le_qinner_self
#print axioms HilbertLift.qinner_self_eq_zero_iff
#print axioms HilbertLift.qinner_sq_le
#print axioms HilbertLift.two_mul_qinner_le
#print axioms HilbertLift.ofFin_pad
#print axioms HilbertLift.ofFin_injective
#print axioms HilbertLift.ofFin_add
#print axioms HilbertLift.ofFin_smul
#print axioms HilbertLift.qinner_ofFin
#print axioms HilbertLift.finInner_pad
#print axioms HilbertLift.finInner_self_nonneg
#print axioms HilbertLift.finInner_sq_le
#print axioms HilbertLift.trunc_ofFin
#print axioms HilbertLift.ofFin_trunc
#print axioms HilbertLift.exhaustion
#print axioms HilbertLift.finInner_trunc_le
