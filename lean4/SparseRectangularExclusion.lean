import RectangularQuadraticExclusion

/-!
# Finite-support rectangular exclusion

AuthorityEffect: None.

Finite equation and coordinate sets permit exact sparse native-image checks.
Every zero of the selected equations is retained, and every actual full-system
zero satisfies those equations. Coordinate support is derived from the actual
term lists. No root existence or complete-cover computation is supplied here.
-/
namespace MUB.SparseRectangularExclusion
open SzollosiTermExpansion SzollosiNativeInterval SzollosiIntervalExclusion
open RectangularQuadraticExclusion
open scoped BigOperators

theorem term_secant_identity_on (S : Finset Nat) (c : Nat → Rat) (r : Nat → ℝ)
    (t : CodedTerm) (hdeg : t.2.length≤2) (hvars : ∀ k∈t.2, k∈S) :
    termValue r t - termValue (fun k => (c k:ℝ)) t =
      ∑ k ∈ S, termDerivative (RectangularQuadraticExclusion.midpoint c r) k t * (r k-(c k:ℝ)) := by
  rcases t with ⟨q,vs⟩
  rcases vs with _ | ⟨i,is⟩
  · simp [termValue,termDerivative]
  rcases is with _ | ⟨j,js⟩
  · have hi : i∈S := hvars i (by simp)
    simp [termValue,termDerivative,ite_mul,hi,mul_sub]
  rcases js with _ | ⟨l,ls⟩
  · have hi : i∈S := hvars i (by simp)
    have hj : j∈S := hvars j (by simp)
    simp only [termValue,List.map_cons,List.map_nil,List.prod_cons,List.prod_nil,mul_one,
      termDerivative,mul_add,add_mul,Finset.sum_add_distrib]
    simp only [mul_ite,mul_zero,ite_mul,zero_mul]
    simp only [Finset.sum_ite_eq',hi,hj,if_true]
    dsimp [RectangularQuadraticExclusion.midpoint]
    ring
  · simp at hdeg

theorem list_secant_identity_on (S : Finset Nat) (c : Nat → Rat) (r : Nat → ℝ)
    (ts : List CodedTerm)
    (hshape : ∀ t∈ts, t.2.length≤2 ∧ ∀ k∈t.2, k∈S) :
    listValue r ts - listValue (fun k => (c k:ℝ)) ts =
      ∑ k ∈ S, listDerivative (RectangularQuadraticExclusion.midpoint c r) ts k * (r k-(c k:ℝ)) := by
  induction ts with
  | nil => simp [listValue,listDerivative]
  | cons t ts ih =>
    have ht := term_secant_identity_on S c r t (hshape t (by simp)).1 (hshape t (by simp)).2
    have hs := ih (fun u hu => hshape u (by simp [hu]))
    simp only [listValue,listDerivative,List.map_cons,List.sum_cons,add_mul,Finset.sum_add_distrib] at *
    linarith

def imageOn (S E : Finset Nat) (rows : Nat → List CodedTerm) (box : Nat → Bounds)
    (c : Nat → Rat) (C : Nat → Nat → Rat) (i : Nat) : Bounds :=
  ((Bounds.point (c i)).add (sumBounds (E)
    (fun e => scale (listRange (fun k => Bounds.point (c k)) (rows e)) (C i e))).neg).add
      (sumBounds (S) (fun k =>
        ((Bounds.point (delta i k)).add
          (sumBounds (E) (fun e => scale (listGradient box (rows e) k) (C i e))).neg).mul
            ((box k).add (Bounds.point (-c k)))))

theorem root_identity_on (S E : Finset Nat) (rows : Nat → List CodedTerm) (c : Nat → Rat)
    (C : Nat → Nat → Rat) (r : Nat → ℝ) (i : Nat) (hi : i∈S)
    (hshape : ∀ e∈E, ∀ t∈rows e, t.2.length≤2 ∧ ∀ k∈t.2, k∈S)
    (hz : ∀ e∈E, listValue r (rows e)=0) :
    r i = (c i:ℝ) - (∑ e ∈ E, (C i e:ℝ)*listValue (fun k => (c k:ℝ)) (rows e)) +
      ∑ k ∈ S, ((delta i k:ℝ) -
        ∑ e ∈ E, (C i e:ℝ)*listDerivative (RectangularQuadraticExclusion.midpoint c r) (rows e) k) * (r k-(c k:ℝ)) := by
  have hsum : (∑ k ∈ S, (∑ e ∈ E,
      (C i e:ℝ)*listDerivative (RectangularQuadraticExclusion.midpoint c r) (rows e) k)*(r k-(c k:ℝ))) =
      -(∑ e ∈ E, (C i e:ℝ)*listValue (fun k => (c k:ℝ)) (rows e)) := by
    simp only [Finset.sum_mul,mul_assoc]
    rw [Finset.sum_comm]
    simp only [← Finset.mul_sum]
    have he : ∀ e ∈ E,
        (∑ k ∈ S, listDerivative (RectangularQuadraticExclusion.midpoint c r) (rows e) k*(r k-(c k:ℝ))) =
        -listValue (fun k => (c k:ℝ)) (rows e) := by
      intro e he
      rw [← list_secant_identity_on S c r (rows e) (hshape e he),
        hz e he,zero_sub]
    rw [Finset.sum_congr rfl (fun e he' => congrArg ((C i e:ℝ)*·) (he e he'))]
    simp
  simp only [sub_mul,Finset.sum_sub_distrib]
  rw [hsum]
  have hd : (∑ k ∈ S, (delta i k:ℝ)*(r k-(c k:ℝ))) = r i-(c i:ℝ) := by
    simp [delta,apply_ite,ite_mul,hi]
  rw [hd]
  ring

theorem root_in_image_on (S E : Finset Nat) (rows : Nat → List CodedTerm) (box : Nat → Bounds)
    (c : Nat → Rat) (C : Nat → Nat → Rat) (r : Nat → ℝ)
    (hc : ∀ k, (box k).Contains (c k:ℝ)) (hr : ∀ k, (box k).Contains (r k))
    (hshape : ∀ e∈E, ∀ t∈rows e, t.2.length≤2 ∧ ∀ k∈t.2, k∈S)
    (hz : ∀ e∈E, listValue r (rows e)=0) (i : Nat) (hi : i∈S) :
    (imageOn S E rows box c C i).Contains (r i) := by
  rw [root_identity_on S E rows c C r i hi hshape hz]
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
      exact scale_enclosed _ _ _ (list_derivative_enclosed box (RectangularQuadraticExclusion.midpoint c r) (midpoint_enclosed box c r hc hr) (rows e) k)
    · simpa only [sub_eq_add_neg,Rat.cast_neg] using contains_add (hr k) (point_contains (-c k))

def coordinateSupport (ts : List CodedTerm) : Finset Nat :=
  (ts.flatMap Prod.snd).toFinset

def usedCoordinates (rows : Nat → List CodedTerm) (E : Finset Nat) (i : Nat) : Finset Nat :=
  insert i (E.biUnion fun e => coordinateSupport (rows e))

theorem used_coordinates_contains (rows : Nat → List CodedTerm) (E : Finset Nat) (i e : Nat)
    (he : e∈E) (t : CodedTerm) (ht : t∈rows e) (k : Nat) (hk : k∈t.2) :
    k∈usedCoordinates rows E i := by
  apply Finset.mem_insert_of_mem
  apply Finset.mem_biUnion.mpr
  exact ⟨e,he,List.mem_toFinset.mpr (List.mem_flatMap.mpr ⟨t,ht,hk⟩)⟩

theorem root_in_used_image (E : Finset Nat) (rows : Nat → List CodedTerm)
    (box : Nat → Bounds) (c : Nat → Rat) (C : Nat → Nat → Rat) (r : Nat → ℝ)
    (hc : ∀ k, (box k).Contains (c k:ℝ)) (hr : ∀ k, (box k).Contains (r k))
    (hdeg : ∀ e∈E, ∀ t∈rows e, t.2.length≤2)
    (hz : ∀ e∈E, listValue r (rows e)=0) (i : Nat) :
    (imageOn (usedCoordinates rows E i) E rows box c C i).Contains (r i) := by
  apply root_in_image_on _ E rows box c C r hc hr
  · intro e he t ht
    exact ⟨hdeg e he t ht,fun k hk => used_coordinates_contains rows E i e he t ht k hk⟩
  · exact hz
  · exact Finset.mem_insert_self _ _

#print axioms list_secant_identity_on
#print axioms root_identity_on
#print axioms root_in_image_on
#print axioms root_in_used_image
end MUB.SparseRectangularExclusion
