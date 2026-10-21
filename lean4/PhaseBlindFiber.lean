import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Positivity

/-!
# Phase-blind weights, phase fibers and unnormalized Hadamard interference over Z[i]

AuthorityEffect: None.  Scope: the Gaussian-integer amplitude pair (a, b), the phase-blind weight
`w z = re^2 + im^2`, and the *unnormalized* two-sector mixing readout `(w (a+b), w (a-b))`.
Nothing here concerns a complex Hilbert space, normalized or projective states, more than two
sectors, or any physical interpretation.  Every theorem is a general statement over all of Z[i];
the two witnesses (1,1) and (1,-1) are instances only.
-/

namespace PhaseBlindFiber

/-- A Gaussian integer as a pair of integers. -/
@[ext]
structure G where
  re : Int
  im : Int
  deriving DecidableEq

namespace G
instance : Add G := ⟨fun a b => ⟨a.re + b.re, a.im + b.im⟩⟩
instance : Sub G := ⟨fun a b => ⟨a.re - b.re, a.im - b.im⟩⟩
instance : Neg G := ⟨fun a => ⟨-a.re, -a.im⟩⟩
instance : Mul G := ⟨fun a b => ⟨a.re * b.re - a.im * b.im, a.re * b.im + a.im * b.re⟩⟩
instance : Zero G := ⟨⟨0, 0⟩⟩
instance : One G := ⟨⟨1, 0⟩⟩

@[simp] theorem add_re (a b : G) : (a + b).re = a.re + b.re := rfl
@[simp] theorem add_im (a b : G) : (a + b).im = a.im + b.im := rfl
@[simp] theorem sub_re (a b : G) : (a - b).re = a.re - b.re := rfl
@[simp] theorem sub_im (a b : G) : (a - b).im = a.im - b.im := rfl
@[simp] theorem neg_re (a : G) : (-a).re = -a.re := rfl
@[simp] theorem neg_im (a : G) : (-a).im = -a.im := rfl
@[simp] theorem mul_re (a b : G) : (a * b).re = a.re * b.re - a.im * b.im := rfl
@[simp] theorem mul_im (a b : G) : (a * b).im = a.re * b.im + a.im * b.re := rfl
@[simp] theorem zero_re : (0 : G).re = 0 := rfl
@[simp] theorem zero_im : (0 : G).im = 0 := rfl

/-- The unit `i`. -/
def I : G := ⟨0, 1⟩
@[simp] theorem I_re : I.re = 0 := rfl
@[simp] theorem I_im : I.im = 1 := rfl

/-- Phase-blind weight `|z|^2`. -/
def w (z : G) : Int := z.re * z.re + z.im * z.im

/-- Real part of `a * conj b`. -/
def cross (a b : G) : Int := a.re * b.re + a.im * b.im

/-- Unnormalized Hadamard mixing readout of a two-sector vector (a, b). -/
def readout (a b : G) : Int × Int := (w (a + b), w (a - b))
end G

open G

/-- Multiplication by the unit `i` preserves the weight: the phase fiber contains the orbit. -/
theorem w_I_mul (z : G) : w (I * z) = w z := by
  simp only [w, mul_re, mul_im, I_re, I_im]; ring

theorem w_neg (z : G) : w (-z) = w z := by
  simp only [w, neg_re, neg_im]; ring

/-- Mixing doubles the total weight, whatever the amplitudes. -/
theorem readout_total (a b : G) :
    (readout a b).1 + (readout a b).2 = 2 * (w a + w b) := by
  simp only [readout, w, add_re, add_im, sub_re, sub_im]; ring

/-- The interference term: the difference of the two readouts is `4 Re(a conj b)`. -/
theorem readout_interference (a b : G) :
    (readout a b).1 - (readout a b).2 = 4 * cross a b := by
  simp only [readout, w, cross, add_re, add_im, sub_re, sub_im]; ring

/-- Rotating the second amplitude by `i` turns the interference term into the imaginary cross part. -/
theorem cross_I_mul (a b : G) : cross a (I * b) = a.im * b.re - a.re * b.im := by
  simp only [cross, mul_re, mul_im, I_re, I_im]; ring

theorem cross_neg (a b : G) : cross a (-b) = -cross a b := by
  simp only [cross, neg_re, neg_im]; ring

/-- Cauchy-Schwarz for the cross term: `cross^2 + (Im part)^2 = w a * w b`. -/
theorem cross_sq_add (a b : G) :
    cross a b * cross a b + (a.im * b.re - a.re * b.im) * (a.im * b.re - a.re * b.im) = w a * w b := by
  simp only [cross, w]; ring

theorem w_eq_zero {z : G} (h : w z = 0) : z = 0 := by
  have h1 : z.re = 0 := by simp only [w] at h; nlinarith [mul_self_nonneg z.re, mul_self_nonneg z.im]
  have h2 : z.im = 0 := by simp only [w] at h; nlinarith [mul_self_nonneg z.re, mul_self_nonneg z.im]
  ext <;> simp [h1, h2]

theorem w_pos {z : G} (h : z ≠ 0) : 0 < w z := by
  rcases lt_or_eq_of_le (show 0 ≤ w z by simp only [w]; nlinarith [mul_self_nonneg z.re, mul_self_nonneg z.im]) with h' | h'
  · exact h'
  · exact absurd (w_eq_zero h'.symm) h

/-- Both sectors nonzero: some rotation inside the second phase fiber changes the readout. -/
theorem fiber_changes_readout (a b : G) (ha : a ≠ 0) (hb : b ≠ 0) :
    (readout a (I * b) ≠ readout a b) ∨ (readout a (-b) ≠ readout a b) := by
  by_contra hcon
  push Not at hcon
  obtain ⟨h1, h2⟩ := hcon
  have e1 := readout_interference a (I * b)
  have e2 := readout_interference a (-b)
  have e0 := readout_interference a b
  rw [h1] at e1
  rw [h2] at e2
  have c1 := cross_I_mul a b
  have c2 := cross_neg a b
  have hr : cross a b = 0 := by linarith
  have hi : a.im * b.re - a.re * b.im = 0 := by linarith
  have hs := cross_sq_add a b
  rw [hr, hi] at hs
  have : w a * w b = 0 := by linarith
  rcases mul_eq_zero.mp this with h | h
  · exact ha (w_eq_zero h)
  · exact hb (w_eq_zero h)

/-- Non-descent: for any two nonzero sector amplitudes, no function of the pair of weights
determines the mixed readout on the product of the two phase fibers. -/
theorem no_descent (a b : G) (ha : a ≠ 0) (hb : b ≠ 0) :
    ¬ ∃ f : Int × Int → Int × Int, ∀ x y : G, w x = w a → w y = w b → readout x y = f (w x, w y) := by
  rintro ⟨f, hf⟩
  have base := hf a b rfl rfl
  have rot := hf a (I * b) rfl (w_I_mul b)
  have neg := hf a (-b) rfl (w_neg b)
  rw [w_I_mul] at rot
  rw [w_neg] at neg
  rcases fiber_changes_readout a b ha hb with h | h
  · exact h (rot.trans base.symm)
  · exact h (neg.trans base.symm)

/-- Sharp boundary: a zero-weight sector has a trivial fiber, and then the readout does descend. -/
theorem descends_when_zero_sector (b : G) :
    ∃ f : Int × Int → Int × Int, ∀ y : G, w y = w b → readout 0 y = f (0, w y) := by
  refine ⟨fun p => (p.2, p.2), ?_⟩
  intro y _
  simp only [readout]
  ext <;> simp [w] <;> ring

/-- Symmetric boundary: a zero SECOND sector also descends (the zero amplitude is the only point of its fiber). -/
theorem descends_when_second_zero (a : G) :
    ∃ f : Int × Int → Int × Int, ∀ x : G, w x = w a → readout x 0 = f (w x, 0) := by
  refine ⟨fun p => (p.1, p.1), ?_⟩
  intro x _
  simp only [readout]
  ext <;> simp [w]

/-- The two named witnesses are instances of the general statement. -/
def psi1b : G := ⟨1, 0⟩
def psi2b : G := ⟨-1, 0⟩

theorem witness_readouts :
    readout ⟨1, 0⟩ psi1b = (4, 0) ∧ readout ⟨1, 0⟩ psi2b = (0, 4) ∧ w psi1b = w psi2b := by
  decide

theorem phase_blind_fiber_interference (a b : G) (ha : a ≠ 0) (hb : b ≠ 0) :
    (∀ z : G, w (I * z) = w z) ∧
    (∀ x y : G, (readout x y).1 + (readout x y).2 = 2 * (w x + w y)) ∧
    ¬ ∃ f : Int × Int → Int × Int, ∀ x y : G, w x = w a → w y = w b → readout x y = f (w x, w y) :=
  ⟨w_I_mul, readout_total, no_descent a b ha hb⟩

end PhaseBlindFiber

#print axioms PhaseBlindFiber.w_I_mul
#print axioms PhaseBlindFiber.readout_total
#print axioms PhaseBlindFiber.readout_interference
#print axioms PhaseBlindFiber.fiber_changes_readout
#print axioms PhaseBlindFiber.no_descent
#print axioms PhaseBlindFiber.descends_when_zero_sector
#print axioms PhaseBlindFiber.descends_when_second_zero
#print axioms PhaseBlindFiber.w_eq_zero
#print axioms PhaseBlindFiber.witness_readouts
#print axioms PhaseBlindFiber.phase_blind_fiber_interference
