import SzollosiTermExpansion
import SzollosiIntervalExclusion

/-!
# Sound rational enclosures for sparse quartet coefficient lists

AuthorityEffect: None.

These rational operations enclose each polynomial value on a containing box.
Degree-two terms use the native square refinement, and terms are accumulated
in list order. This module supplies interval semantics; current emitted data
are compared in SzollosiNativeReflection. No Krawczyk or complete-cover result
is asserted here.
-/

namespace MUB.SzollosiNativeInterval
open SzollosiTermExpansion SzollosiIntervalExclusion SzollosiExecutableSystem SzollosiQuadraticSystem

def scale (b : Bounds) (q : Rat) : Bounds :=
  if 0≤q then ⟨b.lo*q,b.hi*q⟩ else ⟨b.hi*q,b.lo*q⟩

theorem scale_enclosed (b : Bounds) (q : Rat) (x : ℝ) (hx : b.Contains x) :
    (scale b q).Contains ((q:ℝ)*x) := by
  unfold scale
  split
  next h =>
    have hq : (0:ℝ)≤q := by exact_mod_cast h
    simp only [Bounds.Contains,Rat.cast_mul]
    simpa only [mul_comm (q:ℝ) x] using
      And.intro (mul_le_mul_of_nonneg_right hx.1 hq) (mul_le_mul_of_nonneg_right hx.2 hq)
  next h =>
    have hq : (q:ℝ)≤0 := by exact_mod_cast (le_of_not_ge h)
    simp only [Bounds.Contains,Rat.cast_mul]
    simpa only [mul_comm (q:ℝ) x] using
      And.intro (mul_le_mul_of_nonpos_right hx.2 hq) (mul_le_mul_of_nonpos_right hx.1 hq)

def square (b : Bounds) : Bounds :=
  if 0≤b.lo then ⟨b.lo*b.lo,b.hi*b.hi⟩
  else if b.hi≤0 then ⟨b.hi*b.hi,b.lo*b.lo⟩
  else ⟨0,max (b.lo*b.lo) (b.hi*b.hi)⟩

theorem square_enclosed (b : Bounds) (x : ℝ) (hx : b.Contains x) :
    (square b).Contains (x*x) := by
  unfold square
  split
  next h =>
    have hl : (0:ℝ)≤b.lo := by exact_mod_cast h
    simp only [Bounds.Contains,Rat.cast_mul]
    exact ⟨mul_self_le_mul_self hl hx.1,mul_self_le_mul_self (hl.trans hx.1) hx.2⟩
  next h =>
    split
    next hh =>
      have hhi : (b.hi:ℝ)≤0 := by exact_mod_cast hh
      have hnx : (0:ℝ)≤-x := neg_nonneg.mpr (hx.2.trans hhi)
      have hl := mul_self_le_mul_self (neg_nonneg.mpr hhi) (neg_le_neg hx.2)
      have hu := mul_self_le_mul_self hnx (neg_le_neg hx.1)
      simp only [Bounds.Contains,Rat.cast_mul]
      simpa only [neg_mul_neg] using And.intro hl hu
    next hh =>
      simp only [Bounds.Contains,Rat.cast_zero,Rat.cast_max,Rat.cast_mul]
      refine ⟨mul_self_nonneg x,?_⟩
      by_cases hpos : 0≤x
      · exact (mul_self_le_mul_self hpos hx.2).trans (le_max_right _ _)
      · have hnx : (0:ℝ)≤-x := neg_nonneg.mpr (le_of_not_ge hpos)
        have hu := mul_self_le_mul_self hnx (neg_le_neg hx.1)
        simp only [neg_mul_neg] at hu
        exact hu.trans (le_max_left _ _)

def productRange (box : Nat → Bounds) : List Nat → Bounds
  | [] => Bounds.point 1
  | i::is => (box i).mul (productRange box is)

theorem product_enclosed (box : Nat → Bounds) (r : Nat → ℝ)
    (hr : ∀ n, (box n).Contains (r n)) (vs : List Nat) :
    (productRange box vs).Contains (vs.map r).prod := by
  induction vs with
  | nil => simp [productRange, Bounds.Contains, Bounds.point]
  | cons i is ih => simpa only [productRange,List.map_cons,List.prod_cons] using contains_mul (hr i) ih

def factorsRange (box : Nat → Bounds) (vs : List Nat) : Bounds :=
  match vs with
  | [] => Bounds.point 1
  | [i] => box i
  | [i,j] => if i=j then square (box i) else (box i).mul (box j)
  | _ => productRange box vs

theorem factors_enclosed (box : Nat → Bounds) (r : Nat → ℝ)
    (hr : ∀ n, (box n).Contains (r n)) (vs : List Nat) :
    (factorsRange box vs).Contains (vs.map r).prod := by
  rcases vs with _ | ⟨i,is⟩
  · simp [factorsRange, Bounds.Contains, Bounds.point]
  rcases is with _ | ⟨j,js⟩
  · simpa [factorsRange] using hr i
  rcases js with _ | ⟨k,ks⟩
  · by_cases h : i=j
    · subst j
      simpa [factorsRange] using square_enclosed (box i) (r i) (hr i)
    · simpa [factorsRange,h] using contains_mul (hr i) (hr j)
  · exact product_enclosed box r hr _

def termValue (r : Nat → ℝ) (t : CodedTerm) : ℝ := (t.1:ℝ)*(t.2.map r).prod

def termRange (box : Nat → Bounds) (t : CodedTerm) : Bounds := scale (factorsRange box t.2) t.1

theorem term_enclosed (box : Nat → Bounds) (r : Nat → ℝ)
    (hr : ∀ n, (box n).Contains (r n)) (t : CodedTerm) :
    (termRange box t).Contains (termValue r t) := scale_enclosed _ _ _ (factors_enclosed box r hr t.2)

def listValue (r : Nat → ℝ) (ts : List CodedTerm) : ℝ := (ts.map (termValue r)).sum

def listRange (box : Nat → Bounds) (ts : List CodedTerm) : Bounds :=
  ts.foldl (fun acc t => acc.add (termRange box t)) (Bounds.point 0)

theorem fold_enclosed (box : Nat → Bounds) (r : Nat → ℝ)
    (hr : ∀ n, (box n).Contains (r n)) (ts : List CodedTerm) (acc : Bounds)
    (x : ℝ) (hx : acc.Contains x) :
    (ts.foldl (fun a t => a.add (termRange box t)) acc).Contains (x+listValue r ts) := by
  induction ts generalizing acc x with
  | nil => simpa [listValue] using hx
  | cons t ts ih =>
    have h := ih (acc.add (termRange box t)) (x+termValue r t) (contains_add hx (term_enclosed box r hr t))
    simpa only [List.foldl_cons,listValue,List.map_cons,List.sum_cons,add_assoc] using h

theorem list_enclosed (box : Nat → Bounds) (r : Nat → ℝ)
    (hr : ∀ n, (box n).Contains (r n)) (ts : List CodedTerm) :
    (listRange box ts).Contains (listValue r ts) := by
  simpa only [listRange,zero_add] using fold_enclosed box r hr ts (Bounds.point 0) 0 (by simp [Bounds.Contains, Bounds.point])

noncomputable def codedEval (r : Nat → ℝ) : CodedPoly →+* ℝ := MvPolynomial.eval₂Hom (algebraMap Rat ℝ) r

@[simp] theorem coded_eval_C (r : Nat → ℝ) (q : Rat) : codedEval r (MvPolynomial.C q) = (q:ℝ) := by simp [codedEval]
@[simp] theorem coded_eval_X (r : Nat → ℝ) (n : Nat) : codedEval r (MvPolynomial.X n) = r n := by simp [codedEval]

theorem coded_term_eval (r : Nat → ℝ) (t : CodedTerm) : codedEval r (codedTermPolynomial t) = termValue r t := by
  have hp : codedEval r (t.2.map (MvPolynomial.X : Nat → CodedPoly)).prod = (t.2.map r).prod := by
    induction t.2 with
    | nil => simp
    | cons n ns ih => simp only [List.map_cons,List.prod_cons,map_mul,coded_eval_X,ih]
  simpa only [codedTermPolynomial,termValue,map_mul,coded_eval_C] using congrArg ((t.1:ℝ)*·) hp

theorem coded_list_eval (r : Nat → ℝ) (ts : List CodedTerm) : codedEval r (codedListPolynomial ts) = listValue r ts := by
  induction ts with
  | nil => simp [codedListPolynomial,listValue]
  | cons t ts ih => simpa only [codedListPolynomial,listValue,List.map_cons,List.sum_cons,map_add,coded_term_eval] using congrArg (termValue r t+·) ih

theorem polynomial_enclosed (box : Nat → Bounds) (r : Nat → ℝ)
    (hr : ∀ n, (box n).Contains (r n)) (ts : List CodedTerm) :
    (listRange box ts).Contains (codedEval r (codedListPolynomial ts)) := by
  rw [coded_list_eval]
  exact list_enclosed box r hr ts

#print axioms polynomial_enclosed
end MUB.SzollosiNativeInterval
