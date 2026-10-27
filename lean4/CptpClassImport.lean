-- GP-IMPORT-CPTP-CLASS.
-- Boolean collapse, an integer mass image, and four ancilla-false reversible dilations.
-- AuthorityEffect: None.

namespace CptpClassImport

def collapse (_ : Bool) : Bool := false

def TwoSided (f inv : Bool → Bool) : Prop :=
  (∀ q, inv (f q) = q) ∧ (∀ q, f (inv q) = q)

theorem collapse_both_false : collapse false = false ∧ collapse true = false :=
  ⟨rfl, rfl⟩

theorem collapse_labels_agree : collapse false = collapse true := rfl

theorem collapse_no_two_sided_inverse (inv : Bool → Bool) : ¬ TwoSided collapse inv := by
  intro h
  have ht : inv (collapse true) = true := h.1 true
  have hf : inv (collapse false) = false := h.1 false
  rw [collapse] at ht
  rw [collapse] at hf
  cases ht.symm.trans hf

def collapseMass (wF wT : Int) : Int × Int := (wF + wT, 0)

theorem collapseMass_coords (wF wT : Int) :
    (collapseMass wF wT).1 = wF + wT ∧ (collapseMass wF wT).2 = 0 :=
  ⟨rfl, rfl⟩

theorem collapseMass_preserves_sum (wF wT : Int) :
    (collapseMass wF wT).1 + (collapseMass wF wT).2 = wF + wT :=
  Int.add_zero (wF + wT)

theorem collapseMass_nonneg (wF wT : Int) (hF : 0 ≤ wF) (hT : 0 ≤ wT) :
    0 ≤ (collapseMass wF wT).1 ∧ 0 ≤ (collapseMass wF wT).2 :=
  ⟨Int.add_nonneg hF hT, Int.le_refl 0⟩

theorem collapseMass_two_three : collapseMass 2 3 = (5, 0) := rfl

def prepared : Bool := false

theorem prepared_is_false : prepared = false := rfl

structure CollapseDilation where
  map : Bool × Bool → Bool × Bool
  inv : Bool × Bool → Bool × Bool
  left : ∀ x, inv (map x) = x
  right : ∀ x, map (inv x) = x
  reduces : ∀ q, (map (q, prepared)).1 = collapse q

def colOf (swapP swapU : Bool) : Bool × Bool → Bool × Bool
  | (false, false) => (false, swapP)
  | (true, false) => (false, !swapP)
  | (false, true) => (true, swapU)
  | (true, true) => (true, !swapU)

def colInv (swapP swapU : Bool) : Bool × Bool → Bool × Bool
  | (false, b) => (if swapP then !b else b, false)
  | (true, b) => (if swapU then !b else b, true)

theorem colOf_left (swapP swapU : Bool) (x : Bool × Bool) :
    colInv swapP swapU (colOf swapP swapU x) = x := by
  rcases x with ⟨a, b⟩
  cases a <;> cases b <;> cases swapP <;> cases swapU <;> rfl

theorem colOf_right (swapP swapU : Bool) (x : Bool × Bool) :
    colOf swapP swapU (colInv swapP swapU x) = x := by
  rcases x with ⟨a, b⟩
  cases a <;> cases b <;> cases swapP <;> cases swapU <;> rfl

theorem colOf_reduces (swapP swapU : Bool) (q : Bool) :
    (colOf swapP swapU (q, prepared)).1 = collapse q := by
  cases q <;> rfl

def ofSwaps (swapP swapU : Bool) : CollapseDilation where
  map := colOf swapP swapU
  inv := colInv swapP swapU
  left := colOf_left swapP swapU
  right := colOf_right swapP swapU
  reduces := colOf_reduces swapP swapU

def dFF : CollapseDilation := ofSwaps false false
def dFT : CollapseDilation := ofSwaps false true
def dTF : CollapseDilation := ofSwaps true false
def dTT : CollapseDilation := ofSwaps true true

theorem four_maps_pairwise_unequal :
    dFF.map ≠ dFT.map ∧
      dFF.map ≠ dTF.map ∧
      dFF.map ≠ dTT.map ∧
      dFT.map ≠ dTF.map ∧
      dFT.map ≠ dTT.map ∧
      dTF.map ≠ dTT.map := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩
  · intro h; have := congrFun h (false, true); cases this
  · intro h; have := congrFun h (false, false); cases this
  · intro h; have := congrFun h (false, false); cases this
  · intro h; have := congrFun h (false, false); cases this
  · intro h; have := congrFun h (false, false); cases this
  · intro h; have := congrFun h (false, true); cases this

theorem four_named_are_dilations :
    (∀ x, dFF.inv (dFF.map x) = x) ∧
      (∀ x, dFF.map (dFF.inv x) = x) ∧
      (∀ q, (dFF.map (q, prepared)).1 = collapse q) ∧
      (∀ x, dFT.inv (dFT.map x) = x) ∧
      (∀ x, dFT.map (dFT.inv x) = x) ∧
      (∀ q, (dFT.map (q, prepared)).1 = collapse q) ∧
      (∀ x, dTF.inv (dTF.map x) = x) ∧
      (∀ x, dTF.map (dTF.inv x) = x) ∧
      (∀ q, (dTF.map (q, prepared)).1 = collapse q) ∧
      (∀ x, dTT.inv (dTT.map x) = x) ∧
      (∀ x, dTT.map (dTT.inv x) = x) ∧
      (∀ q, (dTT.map (q, prepared)).1 = collapse q) :=
  ⟨dFF.left, dFF.right, dFF.reduces,
    dFT.left, dFT.right, dFT.reduces,
    dTF.left, dTF.right, dTF.reduces,
    dTT.left, dTT.right, dTT.reduces⟩

theorem prepared_pair_injective (D : CollapseDilation)
    (h : D.map (false, false) = D.map (true, false)) : False := by
  have hinv := congrArg D.inv h
  rw [D.left (false, false), D.left (true, false)] at hinv
  cases hinv

theorem prepared_seconds_differ (D : CollapseDilation) :
    (D.map (false, false)).2 ≠ (D.map (true, false)).2 := by
  intro h
  exact prepared_pair_injective D
    (Prod.ext ((D.reduces false).trans (D.reduces true).symm) h)

theorem prepared_false_false (D : CollapseDilation) :
    D.map (false, false) = (false, (D.map (false, false)).2) :=
  Prod.ext (D.reduces false) rfl

theorem prepared_true_false (D : CollapseDilation) :
    D.map (true, false) = (false, !(D.map (false, false)).2) := by
  have h1 := D.reduces true
  have hneq := prepared_seconds_differ D
  cases hP : (D.map (false, false)).2 <;> cases hQ : (D.map (true, false)).2
  · exact (hneq (hP.trans hQ.symm)).elim
  · exact Prod.ext h1 hQ
  · exact Prod.ext h1 (hQ.trans (by simp))
  · exact (hneq (hP.trans hQ.symm)).elim

theorem unprepared_pair_injective (D : CollapseDilation)
    (h : D.map (false, true) = D.map (true, true)) : False := by
  have hinv := congrArg D.inv h
  rw [D.left (false, true), D.left (true, true)] at hinv
  cases hinv

theorem collide_prepared (D : CollapseDilation) (q : Bool)
    (hcol : D.map (q, true) = D.map (false, false) ∨
      D.map (q, true) = D.map (true, false)) : False := by
  rcases hcol with hcol | hcol
  · have hinv := congrArg D.inv hcol
    rw [D.left (q, true), D.left (false, false)] at hinv
    cases hinv
  · have hinv := congrArg D.inv hcol
    rw [D.left (q, true), D.left (true, false)] at hinv
    cases hinv

theorem unprepared_not_in_false_fiber (D : CollapseDilation) (q : Bool)
    (h : (D.map (q, true)).1 = false) : False := by
  have hx : D.map (q, true) = (false, (D.map (q, true)).2) :=
    Prod.ext h rfl
  have hP := prepared_false_false D
  have hQ := prepared_true_false D
  cases hs : (D.map (q, true)).2 <;> cases hR : (D.map (false, false)).2
  · have hx' : D.map (q, true) = (false, false) := by rw [hx, hs]
    have hP' : D.map (false, false) = (false, false) := by
      rw [hR] at hP; exact hP
    exact collide_prepared D q (Or.inl (hx'.trans hP'.symm))
  · have hx' : D.map (q, true) = (false, false) := by rw [hx, hs]
    have hQ' : D.map (true, false) = (false, false) := by
      rw [hR] at hQ; simpa using hQ
    exact collide_prepared D q (Or.inr (hx'.trans hQ'.symm))
  · have hx' : D.map (q, true) = (false, true) := by rw [hx, hs]
    have hQ' : D.map (true, false) = (false, true) := by
      rw [hR] at hQ; simpa using hQ
    exact collide_prepared D q (Or.inr (hx'.trans hQ'.symm))
  · have hx' : D.map (q, true) = (false, true) := by rw [hx, hs]
    have hP' : D.map (false, false) = (false, true) := by
      rw [hR] at hP; exact hP
    exact collide_prepared D q (Or.inl (hx'.trans hP'.symm))

theorem unprepared_report_true (D : CollapseDilation) (q : Bool) :
    (D.map (q, true)).1 = true := by
  cases h : (D.map (q, true)).1
  · exact (unprepared_not_in_false_fiber D q h).elim
  · rfl

theorem unprepared_seconds_differ (D : CollapseDilation) :
    (D.map (false, true)).2 ≠ (D.map (true, true)).2 := by
  intro h
  exact unprepared_pair_injective D
    (Prod.ext ((unprepared_report_true D false).trans
      (unprepared_report_true D true).symm) h)

theorem map_eq_colOf (D : CollapseDilation) (a b : Bool) :
    D.map (a, b) =
      colOf (D.map (false, false)).2 (D.map (false, true)).2 (a, b) := by
  cases a <;> cases b
  · simpa [colOf] using prepared_false_false D
  · have h1 := unprepared_report_true D false
    exact Prod.ext h1 rfl
  · have hQ := prepared_true_false D
    simpa [colOf] using hQ
  · have h1 := unprepared_report_true D true
    have hneq := unprepared_seconds_differ D
    cases hU : (D.map (false, true)).2 <;> cases hV : (D.map (true, true)).2
    · exact (hneq (hU.trans hV.symm)).elim
    · exact Prod.ext h1 hV
    · exact Prod.ext h1 hV
    · exact (hneq (hU.trans hV.symm)).elim

theorem every_dilation_agrees (D : CollapseDilation) :
    (∀ x, D.map x = dFF.map x) ∨
      (∀ x, D.map x = dFT.map x) ∨
      (∀ x, D.map x = dTF.map x) ∨
      (∀ x, D.map x = dTT.map x) := by
  have h := map_eq_colOf D
  cases hP : (D.map (false, false)).2 <;>
    cases hU : (D.map (false, true)).2
  · refine Or.inl fun x => ?_
    rcases x with ⟨a, b⟩
    simpa [dFF, ofSwaps, hP, hU] using h a b
  · refine Or.inr (Or.inl fun x => ?_)
    rcases x with ⟨a, b⟩
    simpa [dFT, ofSwaps, hP, hU] using h a b
  · refine Or.inr (Or.inr (Or.inl fun x => ?_))
    rcases x with ⟨a, b⟩
    simpa [dTF, ofSwaps, hP, hU] using h a b
  · refine Or.inr (Or.inr (Or.inr fun x => ?_))
    rcases x with ⟨a, b⟩
    simpa [dTT, ofSwaps, hP, hU] using h a b

#print axioms collapse_both_false
#print axioms collapse_labels_agree
#print axioms collapse_no_two_sided_inverse
#print axioms collapseMass_coords
#print axioms collapseMass_preserves_sum
#print axioms collapseMass_nonneg
#print axioms collapseMass_two_three
#print axioms prepared_is_false
#print axioms four_maps_pairwise_unequal
#print axioms four_named_are_dilations
#print axioms every_dilation_agrees

end CptpClassImport
