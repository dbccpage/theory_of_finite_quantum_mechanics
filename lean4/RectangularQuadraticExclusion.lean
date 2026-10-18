import SzollosiNativeInterval
import Mathlib.Algebra.MvPolynomial.PDeriv

/-!
# Rectangular exclusion for rational quadratic systems

AuthorityEffect: None.

Every zero in a box lies in the computed rectangular Krawczyk image for any
rational preconditioner. A coordinate disjointness check excludes zeros.
The proof uses the exact midpoint secant identity for quadratics, without an
inverse, a square subsystem, a root-existence conclusion or a supplied secant
soundness hypothesis. Concrete native data and full-cover execution are separate.
-/

namespace MUB.RectangularQuadraticExclusion
open SzollosiTermExpansion SzollosiNativeInterval SzollosiIntervalExclusion
open scoped BigOperators

noncomputable def midpoint (c : Nat → Rat) (r : Nat → ℝ) (k : Nat) : ℝ :=
  ((c k : ℝ)+r k)/2

noncomputable def termDerivative (x : Nat → ℝ) (k : Nat) (t : CodedTerm) : ℝ :=
  match t.2 with
  | [] => 0
  | [i] => if k=i then (t.1:ℝ) else 0
  | [i,j] => (t.1:ℝ)*((if k=i then x j else 0)+(if k=j then x i else 0))
  | _ => 0

def termGradient (box : Nat → Bounds) (k : Nat) (t : CodedTerm) : Bounds :=
  match t.2 with
  | [] => Bounds.point 0
  | [i] => if k=i then Bounds.point t.1 else Bounds.point 0
  | [i,j] => scale ((if k=i then box j else Bounds.point 0).add
      (if k=j then box i else Bounds.point 0)) t.1
  | _ => Bounds.point 0

theorem point_contains (q : Rat) : (Bounds.point q).Contains (q:ℝ) := ⟨le_rfl,le_rfl⟩

theorem zero_contains : (Bounds.point 0).Contains (0:ℝ) := by
  simp [Bounds.Contains,Bounds.point]

theorem midpoint_enclosed (box : Nat → Bounds) (c : Nat → Rat) (r : Nat → ℝ)
    (hc : ∀ k, (box k).Contains (c k:ℝ)) (hr : ∀ k, (box k).Contains (r k)) :
    ∀ k, (box k).Contains (midpoint c r k) := by
  intro k
  rcases hc k with ⟨hcl,hcu⟩
  rcases hr k with ⟨hrl,hru⟩
  constructor <;> dsimp [midpoint] <;> linarith

theorem term_derivative_enclosed (box : Nat → Bounds) (x : Nat → ℝ)
    (hx : ∀ k, (box k).Contains (x k)) (k : Nat) (t : CodedTerm) :
    (termGradient box k t).Contains (termDerivative x k t) := by
  rcases t with ⟨q,vs⟩
  rcases vs with _ | ⟨i,is⟩
  · exact zero_contains
  rcases is with _ | ⟨j,js⟩
  · by_cases h : k=i <;> simp only [termGradient,termDerivative,h,if_true,if_false]
    · exact point_contains q
    · exact zero_contains
  rcases js with _ | ⟨l,ls⟩
  · apply scale_enclosed
    apply contains_add
    · split <;> first | exact hx j | exact zero_contains
    · split <;> first | exact hx i | exact zero_contains
  · exact zero_contains

theorem sum_indicator (n i : Nat) (hi : i<n) (a : ℝ) (f : Nat → ℝ) :
    (∑ k ∈ Finset.range n, (if k=i then a else 0)*f k) = a*f i := by
  simp [ite_mul,hi]

theorem term_secant_identity (n : Nat) (c : Nat → Rat) (r : Nat → ℝ)
    (t : CodedTerm) (hdeg : t.2.length≤2) (hvars : ∀ k∈t.2, k<n) :
    termValue r t - termValue (fun k => (c k:ℝ)) t =
      ∑ k ∈ Finset.range n, termDerivative (midpoint c r) k t * (r k-(c k:ℝ)) := by
  rcases t with ⟨q,vs⟩
  rcases vs with _ | ⟨i,is⟩
  · simp [termValue,termDerivative]
  rcases is with _ | ⟨j,js⟩
  · have hi : i<n := hvars i (by simp)
    simp [termValue,termDerivative,ite_mul,hi,mul_sub]
  rcases js with _ | ⟨l,ls⟩
  · have hi : i<n := hvars i (by simp)
    have hj : j<n := hvars j (by simp)
    simp only [termValue,List.map_cons,List.map_nil,List.prod_cons,List.prod_nil,mul_one,
      termDerivative,mul_add,add_mul,Finset.sum_add_distrib]
    simp only [mul_ite,mul_zero,ite_mul,zero_mul]
    simp only [Finset.sum_ite_eq',Finset.mem_range,hi,hj,if_true]
    dsimp [midpoint]
    ring
  · simp at hdeg

/-- The enclosed expression is the actual formal partial derivative. -/
theorem term_derivative_polynomial (x : Nat → ℝ) (k : Nat) (t : CodedTerm)
    (hdeg : t.2.length≤2) :
    codedEval x (MvPolynomial.pderiv k (codedTermPolynomial t)) = termDerivative x k t := by
  rcases t with ⟨q,vs⟩
  rcases vs with _ | ⟨i,is⟩
  · simp [codedTermPolynomial,termDerivative,codedEval]
  rcases is with _ | ⟨j,js⟩
  · by_cases h : k=i <;>
      simp [codedTermPolynomial,termDerivative,codedEval,MvPolynomial.pderiv_X,eq_comm,h]
  rcases js with _ | ⟨l,ls⟩
  · by_cases hi : k=i <;> by_cases hj : k=j <;>
      simp_all [codedTermPolynomial,termDerivative,codedEval]
  · simp at hdeg

noncomputable def listDerivative (x : Nat → ℝ) (ts : List CodedTerm) (k : Nat) : ℝ :=
  (ts.map (termDerivative x k)).sum

def listGradient (box : Nat → Bounds) (ts : List CodedTerm) (k : Nat) : Bounds :=
  ts.foldr (fun t b => (termGradient box k t).add b) (Bounds.point 0)

theorem list_derivative_polynomial (x : Nat → ℝ) (k : Nat) (ts : List CodedTerm)
    (hdeg : ∀ t∈ts, t.2.length≤2) :
    codedEval x (MvPolynomial.pderiv k (codedListPolynomial ts)) = listDerivative x ts k := by
  induction ts with
  | nil => simp [codedListPolynomial,listDerivative]
  | cons t ts ih =>
    change codedEval x (MvPolynomial.pderiv k (codedTermPolynomial t + codedListPolynomial ts)) =
      termDerivative x k t + listDerivative x ts k
    rw [map_add,map_add,term_derivative_polynomial x k t (hdeg t (by simp)),
      ih (fun u hu => hdeg u (by simp [hu]))]

theorem list_derivative_enclosed (box : Nat → Bounds) (x : Nat → ℝ)
    (hx : ∀ k, (box k).Contains (x k)) (ts : List CodedTerm) (k : Nat) :
    (listGradient box ts k).Contains (listDerivative x ts k) := by
  induction ts with
  | nil => exact zero_contains
  | cons t ts ih =>
    exact contains_add (term_derivative_enclosed box x hx k t) ih

theorem list_secant_identity (n : Nat) (c : Nat → Rat) (r : Nat → ℝ)
    (ts : List CodedTerm)
    (hshape : ∀ t∈ts, t.2.length≤2 ∧ ∀ k∈t.2, k<n) :
    listValue r ts - listValue (fun k => (c k:ℝ)) ts =
      ∑ k ∈ Finset.range n, listDerivative (midpoint c r) ts k * (r k-(c k:ℝ)) := by
  induction ts with
  | nil => simp [listValue,listDerivative]
  | cons t ts ih =>
    have ht := term_secant_identity n c r t (hshape t (by simp)).1 (hshape t (by simp)).2
    have hs := ih (fun u hu => hshape u (by simp [hu]))
    simp only [listValue,listDerivative,List.map_cons,List.sum_cons,add_mul,Finset.sum_add_distrib] at *
    linarith

/-- Rational interval sum, including empty sums. -/
def sumBounds (s : Finset Nat) (b : Nat → Bounds) : Bounds := ⟨∑ k∈s, (b k).lo,∑ k∈s, (b k).hi⟩

theorem sum_enclosed (s : Finset Nat) (b : Nat → Bounds) (v : Nat → ℝ)
    (hv : ∀ k∈s, (b k).Contains (v k)) :
    (sumBounds s b).Contains (∑ k∈s, v k) := by
  constructor
  · simpa only [sumBounds,Rat.cast_sum] using Finset.sum_le_sum (fun k hk => (hv k hk).1)
  · simpa only [sumBounds,Rat.cast_sum] using Finset.sum_le_sum (fun k hk => (hv k hk).2)

def delta (i k : Nat) : Rat := if i=k then 1 else 0

/-- n coordinates, m equations; the n-by-m preconditioner is arbitrary. -/
def image (n m : Nat) (rows : Nat → List CodedTerm) (box : Nat → Bounds)
    (c : Nat → Rat) (C : Nat → Nat → Rat) (i : Nat) : Bounds :=
  ((Bounds.point (c i)).add (sumBounds (Finset.range m)
    (fun e => scale (listRange (fun k => Bounds.point (c k)) (rows e)) (C i e))).neg).add
      (sumBounds (Finset.range n) (fun k =>
        ((Bounds.point (delta i k)).add
          (sumBounds (Finset.range m) (fun e => scale (listGradient box (rows e) k) (C i e))).neg).mul
            ((box k).add (Bounds.point (-c k)))))

/-- Algebraic Krawczyk identity at any zero; no invertibility is required. -/
theorem root_identity (n m : Nat) (rows : Nat → List CodedTerm) (c : Nat → Rat)
    (C : Nat → Nat → Rat) (r : Nat → ℝ) (i : Nat) (hi : i<n)
    (hshape : ∀ e < m, ∀ t∈rows e, t.2.length≤2 ∧ ∀ k∈t.2, k<n)
    (hz : ∀ e < m, listValue r (rows e)=0) :
    r i = (c i:ℝ) - (∑ e ∈ Finset.range m, (C i e:ℝ)*listValue (fun k => (c k:ℝ)) (rows e)) +
      ∑ k ∈ Finset.range n, ((delta i k:ℝ) -
        ∑ e ∈ Finset.range m, (C i e:ℝ)*listDerivative (midpoint c r) (rows e) k) * (r k-(c k:ℝ)) := by
  have hsum : (∑ k ∈ Finset.range n, (∑ e ∈ Finset.range m,
      (C i e:ℝ)*listDerivative (midpoint c r) (rows e) k)*(r k-(c k:ℝ))) =
      -(∑ e ∈ Finset.range m, (C i e:ℝ)*listValue (fun k => (c k:ℝ)) (rows e)) := by
    simp only [Finset.sum_mul,mul_assoc]
    rw [Finset.sum_comm]
    simp only [← Finset.mul_sum]
    have he : ∀ e ∈ Finset.range m,
        (∑ k ∈ Finset.range n, listDerivative (midpoint c r) (rows e) k*(r k-(c k:ℝ))) =
        -listValue (fun k => (c k:ℝ)) (rows e) := by
      intro e he
      rw [← list_secant_identity n c r (rows e) (hshape e (Finset.mem_range.mp he)),
        hz e (Finset.mem_range.mp he),zero_sub]
    rw [Finset.sum_congr rfl (fun e he' => congrArg ((C i e:ℝ)*·) (he e he'))]
    simp
  simp only [sub_mul,Finset.sum_sub_distrib]
  rw [hsum]
  have hd : (∑ k ∈ Finset.range n, (delta i k:ℝ)*(r k-(c k:ℝ))) = r i-(c i:ℝ) := by
    simp [delta,apply_ite,ite_mul,hi]
  rw [hd]
  ring

/-- Every zero retained by the box lies in the computed image. -/
theorem root_in_image (n m : Nat) (rows : Nat → List CodedTerm) (box : Nat → Bounds)
    (c : Nat → Rat) (C : Nat → Nat → Rat) (r : Nat → ℝ)
    (hc : ∀ k, (box k).Contains (c k:ℝ)) (hr : ∀ k, (box k).Contains (r k))
    (hshape : ∀ e < m, ∀ t∈rows e, t.2.length≤2 ∧ ∀ k∈t.2, k<n)
    (hz : ∀ e < m, listValue r (rows e)=0) (i : Nat) (hi : i<n) :
    (image n m rows box c C i).Contains (r i) := by
  rw [root_identity n m rows c C r i hi hshape hz]
  simp only [sub_eq_add_neg]
  apply contains_add
  · apply contains_add (point_contains (c i))
    apply contains_neg
    apply sum_enclosed
    intro e he
    exact scale_enclosed _ _ _ (list_enclosed _ _ (fun k => point_contains (c k)) (rows e))
  · apply sum_enclosed
    intro k hk
    apply contains_mul
    · apply contains_add (point_contains (delta i k))
      apply contains_neg
      apply sum_enclosed
      intro e he
      exact scale_enclosed _ _ _ (list_derivative_enclosed box (midpoint c r) (midpoint_enclosed box c r hc hr) (rows e) k)
    · simpa only [sub_eq_add_neg,Rat.cast_neg] using contains_add (hr k) (point_contains (-c k))

/-- Only strict separation is an exclusion; endpoint contact is retained. -/
def disjoint (a b : Bounds) : Bool := decide (a.hi<b.lo) || decide (b.hi<a.lo)

theorem disjoint_sound (a b : Bounds) (h : disjoint a b=true) (x : ℝ) :
    ¬ (a.Contains x ∧ b.Contains x) := by
  rintro ⟨ha,hb⟩
  simp only [disjoint,Bool.or_eq_true,decide_eq_true_eq] at h
  rcases h with h | h
  · have h' : (a.hi:ℝ)<b.lo := by exact_mod_cast h
    exact (not_lt_of_ge (hb.1.trans ha.2)) h'
  · have h' : (b.hi:ℝ)<a.lo := by exact_mod_cast h
    exact (not_lt_of_ge (ha.1.trans hb.2)) h'

def exclusionCheck (n m : Nat) (rows : Nat → List CodedTerm) (box : Nat → Bounds)
    (c : Nat → Rat) (C : Nat → Nat → Rat) : Bool :=
  (List.range n).any fun i => disjoint (image n m rows box c C i) (box i)

theorem exclusion_sound (n m : Nat) (rows : Nat → List CodedTerm) (box : Nat → Bounds)
    (c : Nat → Rat) (C : Nat → Nat → Rat)
    (hc : ∀ k, (box k).Contains (c k:ℝ))
    (hshape : ∀ e < m, ∀ t∈rows e, t.2.length≤2 ∧ ∀ k∈t.2, k<n)
    (hcheck : exclusionCheck n m rows box c C=true) :
    ¬ ∃ r : Nat → ℝ, (∀ k, (box k).Contains (r k)) ∧ ∀ e < m, listValue r (rows e)=0 := by
  rintro ⟨r,hr,hz⟩
  obtain ⟨i,hi,hsep⟩ := List.any_eq_true.mp hcheck
  exact disjoint_sound _ _ hsep (r i)
    ⟨root_in_image n m rows box c C r hc hr hshape hz i (List.mem_range.mp hi),hr i⟩

/-- Synthetic rectangular example; this is not a MUB cover cell. -/
def exampleRows (e : Nat) : List CodedTerm :=
  if e=0 then [(1,[0]),(1,[1])]
  else if e=1 then [(1,[0]),(-1,[1])]
  else [(1,[0,1])]

def exampleBox (k : Nat) : Bounds :=
  if k=0 then ⟨1,2⟩ else if k=1 then ⟨-2,2⟩ else Bounds.point 0

def exampleCenter (k : Nat) : Rat := if k=0 then 3/2 else 0

def examplePreconditioner (i e : Nat) : Rat :=
  if i=0 then (if e=0 ∨ e=1 then 1/2 else 0)
  else if i=1 then (if e=0 then 1/2 else if e=1 then -1/2 else 0)
  else 0

/-- All natural residual intervals contain zero, despite absence of a common zero. -/
theorem example_residual_intervals_unresolved :
    (List.range 3).all (fun e => !(listRange exampleBox (exampleRows e)).excludesZero) = true := by decide +kernel

/-- The rectangular image separates the first coordinate. -/
theorem example_check_excludes :
    exclusionCheck 2 3 exampleRows exampleBox exampleCenter examplePreconditioner = true := by decide +kernel

theorem example_has_no_zero :
    ¬ ∃ r : Nat → ℝ, (∀ k, (exampleBox k).Contains (r k)) ∧
      ∀ e < 3, listValue r (exampleRows e)=0 := by
  apply exclusion_sound 2 3 exampleRows exampleBox exampleCenter examplePreconditioner
  · intro k
    by_cases h0 : k=0
    · norm_num [exampleBox,exampleCenter,h0,Bounds.Contains]
    · by_cases h1 : k=1
      · simp [exampleBox,exampleCenter,h1,Bounds.Contains]
      · simp [exampleBox,exampleCenter,h0,h1,Bounds.Contains,Bounds.point]
  · intro e he
    interval_cases e <;> norm_num [exampleRows]
  · exact example_check_excludes

/-- Contact at an endpoint cannot be declared disjoint. -/
def touchingBox (k : Nat) : Bounds :=
  if k=0 then ⟨0,1⟩ else if k=1 then ⟨-1,1⟩ else Bounds.point 0

theorem touching_check_retains :
    exclusionCheck 2 3 exampleRows touchingBox (fun _ => 0) examplePreconditioner = false := by decide +kernel

/-- Overdetermined strict inclusion alone need not supply a common root. -/
def inconsistentRows (e : Nat) : List CodedTerm :=
  if e=0 then [(1,[0])] else [(1,[])]

def inconsistentPreconditioner (_i e : Nat) : Rat := if e=0 then 1 else 0

def unitBox (_k : Nat) : Bounds := ⟨-1,1⟩

theorem strict_inclusion_example :
    (unitBox 0).lo < (image 1 2 inconsistentRows unitBox (fun _ => 0) inconsistentPreconditioner 0).lo ∧
      (image 1 2 inconsistentRows unitBox (fun _ => 0) inconsistentPreconditioner 0).hi < (unitBox 0).hi := by decide +kernel

theorem strict_example_has_no_root :
    ¬ ∃ r : Nat → ℝ, ∀ e < 2, listValue r (inconsistentRows e)=0 := by
  rintro ⟨r,hr⟩
  have h := hr 1 (by decide)
  norm_num [inconsistentRows,listValue,termValue] at h

#print axioms strict_inclusion_example
#print axioms strict_example_has_no_root
#print axioms list_derivative_polynomial
#print axioms example_has_no_zero
#print axioms touching_check_retains
#print axioms list_secant_identity
#print axioms root_identity
#print axioms root_in_image
#print axioms exclusion_sound
end MUB.RectangularQuadraticExclusion
