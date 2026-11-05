import BellPair
import Init.GrindInstances.Ring.Rat

/-! The missed CHSH orientation is bounded for every normalized nonnegative
rational mixture of deterministic four-output assignments. The bound is a
mathematical statement about this declared finite model, without physical claims. -/
namespace PreMssn.BellMixture
open BellPair

abbrev Assignment := Bool × Bool × Bool × Bool

def assignments : List Assignment :=
  [false,true].flatMap fun a0 => [false,true].flatMap fun a1 =>
    [false,true].flatMap fun b0 => [false,true].map fun b1 => (a0,a1,b0,b1)

theorem assignment_mem (a : Assignment) : a ∈ assignments := by
  rcases a with ⟨a0,a1,b0,b1⟩
  cases a0 <;> cases a1 <;> cases b0 <;> cases b1 <;> decide +kernel

theorem assignment_enumeration : assignments.Nodup ∧ assignments.length = 16 := by decide +kernel

def correlation (a : Assignment) (x y : Bool) : Rat :=
  (sign (if x then a.2.1 else a.1) : Rat) *
    (sign (if y then a.2.2.2 else a.2.2.1) : Rat)

def score (a : Assignment) : Rat :=
  correlation a false false + correlation a false true -
    correlation a true false + correlation a true true

theorem deterministic_score_bound (a : Assignment) : score a ≤ 2 := by
  rcases a with ⟨a0,a1,b0,b1⟩
  cases a0 <;> cases a1 <;> cases b0 <;> cases b1 <;> decide +kernel

structure Distribution where
  weight : Assignment → Rat
  nonnegative : ∀ a, 0 ≤ weight a
  normalized : (assignments.map weight).sum = 1

def mixedCorrelation (p : Distribution) (x y : Bool) : Rat :=
  (assignments.map (fun a => p.weight a * correlation a x y)).sum

def mixedScore (p : Distribution) : Rat :=
  mixedCorrelation p false false + mixedCorrelation p false true -
    mixedCorrelation p true false + mixedCorrelation p true true

theorem sum_score (xs : List Assignment) (weight : Assignment → Rat) :
    (xs.map (fun a => weight a * score a)).sum =
      (xs.map (fun a => weight a * correlation a false false)).sum +
      (xs.map (fun a => weight a * correlation a false true)).sum -
      (xs.map (fun a => weight a * correlation a true false)).sum +
      (xs.map (fun a => weight a * correlation a true true)).sum := by
  induction xs with
  | nil =>
    change (0 : Rat) = 0+0-0+0
    decide +kernel
  | cons a xs ih =>
    simp only [List.map_cons, List.sum_cons]
    rw [ih]
    unfold score
    grind

theorem sum_le_sum (xs : List Assignment) (f g : Assignment → Rat)
    (h : ∀ a, f a ≤ g a) : (xs.map f).sum ≤ (xs.map g).sum := by
  induction xs with
  | nil => exact Rat.le_refl
  | cons a xs ih =>
    simp only [List.map_cons, List.sum_cons]
    exact Rat.le_trans ((Rat.add_le_add_right).mpr (h a))
      ((Rat.add_le_add_left).mpr ih)

theorem sum_scaled (xs : List Assignment) (weight : Assignment → Rat) :
    (xs.map (fun a => weight a * 2)).sum = (xs.map weight).sum * 2 := by
  induction xs with
  | nil => simp
  | cons a xs ih => simp only [List.map_cons, List.sum_cons, ih, Rat.add_mul]

/-- Convex mixtures cannot increase this oriented deterministic CHSH bound. -/
theorem mixed_score_bound (p : Distribution) : mixedScore p ≤ 2 := by
  have h := sum_le_sum assignments (fun a => p.weight a * score a)
    (fun a => p.weight a * 2)
    (fun a => Rat.mul_le_mul_of_nonneg_left (deterministic_score_bound a) (p.nonnegative a))
  rw [sum_scaled, p.normalized] at h
  unfold mixedScore mixedCorrelation
  rw [← sum_score assignments p.weight]
  simpa only [Rat.one_mul] using h

theorem target_has_no_joint_distribution (p : Distribution) :
    ¬(mixedCorrelation p false false = 1 ∧ mixedCorrelation p false true = 1 ∧
      mixedCorrelation p true false = -1 ∧ mixedCorrelation p true true = 1) := by
  rintro ⟨h00,h01,h10,h11⟩
  have h := mixed_score_bound p
  unfold mixedScore at h
  rw [h00,h01,h10,h11] at h
  exact (by decide +kernel : ¬((1 : Rat)+1-(-1)+1 ≤ 2)) h

/-- Runtime inputs are nonnegative integer masses in the displayed sixteen-state
order. Accepted inputs construct the very distribution used in the theorem. -/
def fromWeights (weights : List Int) : Option Distribution := do
  if weights.length != 16 || weights.any (fun w => w < 0) || weights.sum ≤ 0 then return ← none
  let weight := fun a : Assignment => (weights.getD (assignments.idxOf a) 0 : Rat) / (weights.sum : Rat)
  if hn : assignments.all (fun a => decide (0 ≤ weight a)) = true then
    if hz : (assignments.map weight).sum = 1 then
      some ⟨weight, fun a => of_decide_eq_true
        ((List.all_eq_true.mp hn) a (assignment_mem a)), hz⟩
    else none
  else none

def runtimeCorrelations (p : Distribution) : List Rat :=
  [mixedCorrelation p false false, mixedCorrelation p false true,
    mixedCorrelation p true false, mixedCorrelation p true true, mixedScore p]

end PreMssn.BellMixture
