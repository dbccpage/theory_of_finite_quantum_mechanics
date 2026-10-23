import Mathlib.Data.Fintype.Option
import «gs002_l003_03_weighted_cycle_quotient»

open scoped BigOperators

/-!
Anchored single-cycle exactness kernel (PaperGS002 C13 / §5).

The paper uses the standard graph fact that, on a single directed cycle, the
only quotient invariant is total circulation. This file records the finite
algebraic core without importing graph-chain infrastructure:

* an anchored cycle cochain is determined by arbitrary non-closing edge values;
* the closing edge is forced to be the negative of their sum;
* these are exactly the zero-circulation cochains;
* hence two cycle cochains have the same circulation iff their difference is an
  anchored exact cycle repair.
-/

noncomputable section

variable {A V : Type*} [Fintype A] [NormedAddCommGroup V]

def anchoredCycleCochain (tail : A → V) : Option A → V
  | none => -∑ a : A, tail a
  | some a => tail a

lemma cycleCirculation_anchoredCycleCochain (tail : A → V) :
    cycleCirculation (anchoredCycleCochain tail) = 0 := by
  simp [cycleCirculation, anchoredCycleCochain, Fintype.sum_option]

lemma cycleCirculation_add (η θ : Option A → V) :
    cycleCirculation (fun e => η e + θ e) =
      cycleCirculation η + cycleCirculation θ := by
  unfold cycleCirculation
  rw [Finset.sum_add_distrib]

theorem cycleCirculation_sub_anchoredCycleCochain
    (η : Option A → V) (tail : A → V) :
    cycleCirculation (fun e => η e - anchoredCycleCochain tail e) =
      cycleCirculation η := by
  rw [cycleCirculation_sub, cycleCirculation_anchoredCycleCochain, sub_zero]

theorem zero_circulation_iff_anchored_cycle (η : Option A → V) :
    cycleCirculation η = 0 ↔
      ∃ tail : A → V, η = anchoredCycleCochain tail := by
  constructor
  · intro h
    use fun a => η (some a)
    funext e
    cases e with
    | none =>
        have hs : η none + ∑ a : A, η (some a) = 0 := by
          simpa [cycleCirculation, Fintype.sum_option] using h
        exact eq_neg_of_add_eq_zero_left hs
    | some a =>
        rfl
  · rintro ⟨tail, rfl⟩
    exact cycleCirculation_anchoredCycleCochain tail

theorem same_circulation_iff_difference_anchored_cycle
    (η θ : Option A → V) :
    cycleCirculation η = cycleCirculation θ ↔
      ∃ tail : A → V,
        (fun e => η e - θ e) = anchoredCycleCochain tail := by
  rw [same_cycle_circulation_iff_zero_difference,
    zero_circulation_iff_anchored_cycle]

theorem same_circulation_iff_anchored_cycle_coset
    (η θ : Option A → V) :
    cycleCirculation θ = cycleCirculation η ↔
      ∃ tail : A → V, θ = fun e => η e + anchoredCycleCochain tail e := by
  constructor
  · intro h
    rcases (same_circulation_iff_difference_anchored_cycle θ η).mp h with
      ⟨tail, htail⟩
    use tail
    funext e
    have heq := congr_fun htail e
    have htheta : θ e = anchoredCycleCochain tail e + η e :=
      sub_eq_iff_eq_add.mp heq
    simpa [add_comm] using htheta
  · rintro ⟨tail, rfl⟩
    rw [cycleCirculation_add, cycleCirculation_anchoredCycleCochain, add_zero]

#print axioms cycleCirculation_anchoredCycleCochain
#print axioms cycleCirculation_add
#print axioms cycleCirculation_sub_anchoredCycleCochain
#print axioms zero_circulation_iff_anchored_cycle
#print axioms same_circulation_iff_difference_anchored_cycle
#print axioms same_circulation_iff_anchored_cycle_coset
