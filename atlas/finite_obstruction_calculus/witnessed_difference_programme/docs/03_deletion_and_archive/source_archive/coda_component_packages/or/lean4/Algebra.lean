namespace Coda.OR

variable {A B C : Type _}

def Compatible (left : A × B) (right : B × C) : Prop :=
  left.2 = right.1

theorem pair_gluing (left : A × B) (right : B × C)
    (h : Compatible left right) :
    ∃ t : A × B × C, ((t.1, t.2.1) = left ∧ (t.2.1, t.2.2) = right) ∧
      ∀ y : A × B × C, ((y.1, y.2.1) = left ∧ (y.2.1, y.2.2) = right) → y = t := by
  refine ⟨(left.1, left.2, right.2), ⟨?_, ?_⟩, ?_⟩
  · exact Prod.eta left
  · exact Prod.ext h rfl
  · rintro ⟨a,b,c⟩ ⟨hl,hr⟩
    have ha := congrArg Prod.fst hl
    have hb := congrArg Prod.snd hl
    have hc := congrArg Prod.snd hr
    exact Prod.ext ha (Prod.ext hb hc)

theorem gluing_requires_overlap (left : A × B) (right : B × C)
    (h : ∃ t : A × B × C, (t.1,t.2.1) = left ∧ (t.2.1,t.2.2) = right) :
    Compatible left right := by
  obtain ⟨t,hl,hr⟩ := h
  exact (congrArg Prod.snd hl).symm.trans (congrArg Prod.fst hr)

theorem incompatible_countermodel :
    ¬ ∃ t : Unit × Bool × Unit, (t.1,t.2.1) = ((),false) ∧
      (t.2.1,t.2.2) = (true,()) := by
  intro h
  have impossible : false = true := gluing_requires_overlap ((),false) (true,()) h
  cases impossible

end Coda.OR

#check Coda.OR.pair_gluing
#print axioms Coda.OR.pair_gluing
#check Coda.OR.gluing_requires_overlap
#print axioms Coda.OR.gluing_requires_overlap
#check Coda.OR.incompatible_countermodel
#print axioms Coda.OR.incompatible_countermodel
