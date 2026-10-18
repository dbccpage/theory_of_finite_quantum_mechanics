import Conjecture2GeneralMechanization
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Data.Complex.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

/-!
# Complex semantics of the all-pattern Tao calculation

AuthorityEffect: None.

An integer-pair evaluator is mapped into the actual complex numbers. The
finite check is thereby tied to a sum of column products of the recorded Tao
entries and their conjugates. No necessary condition for arbitrary MUB
triples, or nonextension theorem, is asserted.
-/

namespace MUB.TaoLaurent
open Conjecture2GeneralMechanization

abbrev Pair := Int × Int
def addPair (p q : Pair) : Pair := (p.1 + q.1, p.2 + q.2)
def mulPair (p q : Pair) : Pair :=
  (p.1 * q.1 - p.2 * q.2, p.1 * q.2 + p.2 * q.1 - p.2 * q.2)
def starPair (p : Pair) : Pair := (p.1 - p.2, -p.2)
def normPair (p : Pair) : Int := p.1 * p.1 - p.1 * p.2 + p.2 * p.2
def sumPair (xs : List Pair) : Pair := xs.foldr addPair (0, 0)
def prodPair (xs : List Pair) : Pair := xs.foldr mulPair (1, 0)
def entryPair (r c : Fin 6) : Pair :=
  if phaseTable r.val c.val = 0 then (1, 0)
  else if phaseTable r.val c.val = 1 then (0, 1) else (-1, -1)
def termPair (mask : Fin 64) (r c : Fin 6) : Pair :=
  if maskSign mask r = 1 then entryPair r c else starPair (entryPair r c)
def expressionPair (mask : Fin 64) : Pair :=
  sumPair ((List.finRange 6).map fun c =>
    prodPair ((List.finRange 6).map fun r => termPair mask r c))

set_option maxRecDepth 8192 in
set_option maxHeartbeats 2000000 in
theorem pair_norm_eq_integer_norm :
    ∀ mask : Fin 64, normPair (expressionPair mask) = maskTaoNormSq mask := by
  decide

theorem entry_pair_norm : ∀ r c : Fin 6, normPair (entryPair r c) = 1 := by decide

noncomputable section

def omega : ℂ := ⟨-1 / 2, Real.sqrt 3 / 2⟩
def toComplex (p : Pair) : ℂ := (p.1 : ℂ) + (p.2 : ℂ) * omega
def taoMatrix (r c : Fin 6) : ℂ := toComplex (entryPair r c)
def signedTerm (mask : Fin 64) (r c : Fin 6) : ℂ :=
  if maskSign mask r = 1 then taoMatrix r c else star (taoMatrix r c)
def signedExpression (mask : Fin 64) : ℂ :=
  ((List.finRange 6).map fun c =>
    ((List.finRange 6).map fun r => signedTerm mask r c).prod).sum
def laurentExpression (mask : Fin 64) : ℂ :=
  ((List.finRange 6).map fun c =>
    ((List.finRange 6).map fun r => taoMatrix r c ^ maskSign mask r).prod).sum

theorem omega_sq : omega ^ 2 = -1 - omega := by
  have hs : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  apply Complex.ext <;> simp [omega, pow_two, Complex.mul_re, Complex.mul_im] <;>
    nlinarith [hs]

theorem omega_star : star omega = -1 - omega := by
  apply Complex.ext
  · norm_num [omega]
  · simp [omega]

theorem toComplex_add (p q : Pair) :
    toComplex (addPair p q) = toComplex p + toComplex q := by
  simp [toComplex, addPair]
  ring

theorem toComplex_mul (p q : Pair) :
    toComplex (mulPair p q) = toComplex p * toComplex q := by
  simp only [toComplex, mulPair, Int.cast_add, Int.cast_sub, Int.cast_mul]
  ring_nf
  rw [omega_sq]
  ring

theorem toComplex_star (p : Pair) : toComplex (starPair p) = star (toComplex p) := by
  simp [toComplex, starPair, omega_star]
  ring

theorem toComplex_norm (p : Pair) : Complex.normSq (toComplex p) = (normPair p : ℝ) := by
  have hs : (Real.sqrt 3) ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  norm_num [toComplex, omega, normPair, Complex.normSq_apply, Complex.mul_re, Complex.mul_im]
  ring_nf
  rw [hs]
  ring

theorem toComplex_sum (xs : List Pair) :
    toComplex (sumPair xs) = (xs.map toComplex).sum := by
  induction xs with
  | nil => simp [sumPair, toComplex]
  | cons p ps ih =>
    change toComplex (addPair p (sumPair ps)) = toComplex p + (ps.map toComplex).sum
    rw [toComplex_add, ih]

theorem toComplex_prod (xs : List Pair) :
    toComplex (prodPair xs) = (xs.map toComplex).prod := by
  induction xs with
  | nil => simp [prodPair, toComplex]
  | cons p ps ih =>
    change toComplex (mulPair p (prodPair ps)) = toComplex p * (ps.map toComplex).prod
    rw [toComplex_mul, ih]

theorem toComplex_term (mask : Fin 64) (r c : Fin 6) :
    toComplex (termPair mask r c) = signedTerm mask r c := by
  unfold termPair signedTerm taoMatrix
  split <;> simp [toComplex_star]

theorem toComplex_expression (mask : Fin 64) :
    toComplex (expressionPair mask) = signedExpression mask := by
  simp [expressionPair, signedExpression, toComplex_sum, toComplex_prod,
    List.map_map, Function.comp_def, toComplex_term]

theorem tao_entry_norm (r c : Fin 6) : Complex.normSq (taoMatrix r c) = 1 := by
  rw [taoMatrix, toComplex_norm, entry_pair_norm]
  norm_num

theorem tao_all_balanced_complex (mask : Fin 64) (h : maskPositiveCount mask = 3) :
    Complex.normSq (signedExpression mask) = 9 := by
  rw [← toComplex_expression, toComplex_norm, pair_norm_eq_integer_norm,
    tao_all_balanced_masks mask h]
  norm_num

private theorem unit_inv (z : ℂ) (h : Complex.normSq z = 1) : z⁻¹ = star z := by
  have hz : z ≠ 0 := by
    intro hz
    simp [hz] at h
  have hc : star z * z = 1 := by
    simpa [Complex.star_def, Complex.normSq_eq_conj_mul_self] using
      congrArg (fun t : ℝ => (t : ℂ)) h
  apply mul_right_cancel₀ hz
  rw [inv_mul_cancel₀ hz, hc]

theorem signedTerm_eq_zpow (mask : Fin 64) (r c : Fin 6) :
    signedTerm mask r c = taoMatrix r c ^ maskSign mask r := by
  have hi := unit_inv (taoMatrix r c) (tao_entry_norm r c)
  by_cases hbit : mask.val / 2 ^ r.val % 2 = 1 <;>
    simp [signedTerm, maskSign, hbit, hi]

theorem signedExpression_eq_laurent (mask : Fin 64) :
    signedExpression mask = laurentExpression mask := by
  simp only [signedExpression, laurentExpression, signedTerm_eq_zpow]

theorem tao_all_balanced_laurent (mask : Fin 64) (h : maskPositiveCount mask = 3) :
    Complex.normSq (laurentExpression mask) = 9 := by
  rw [← signedExpression_eq_laurent]
  exact tao_all_balanced_complex mask h

#print axioms pair_norm_eq_integer_norm
#print axioms toComplex_mul
#print axioms toComplex_norm
#print axioms toComplex_expression
#print axioms tao_entry_norm
#print axioms tao_all_balanced_complex
#print axioms signedTerm_eq_zpow
#print axioms tao_all_balanced_laurent
end
end MUB.TaoLaurent
