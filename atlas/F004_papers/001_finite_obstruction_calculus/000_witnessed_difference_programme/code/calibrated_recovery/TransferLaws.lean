import Init

namespace CalibratedRecovery

def Compatible {X I O P : Type} (allowed : X → I → O → Prop)
    (visible : X → P) (p : P) (queried : I → Prop) (report : I → O) (x : X) : Prop :=
  visible x = p ∧ ∀ i, queried i → allowed x i (report i)

def Lifted {X I O : Type} (allowed : X → I → O → Prop)
    (x : X) (reports : I → O) : Prop := ∀ i, allowed x i (reports i)

theorem partial_report_extends {X I O : Type} (allowed : X → I → O → Prop)
    (x : X) (queried : I → Prop) (report : I → O)
    (nonempty : ∀ i, ∃ o, allowed x i o) :
    (∀ i, queried i → allowed x i (report i)) ↔
      ∃ reports, Lifted allowed x reports ∧ ∀ i, queried i → reports i = report i := by
  classical
  constructor
  · intro h
    let reports := fun i => if queried i then report i else Classical.choose (nonempty i)
    refine ⟨reports, ?_, ?_⟩
    · intro i
      by_cases hi : queried i
      · simpa [reports, hi] using h i hi
      · simpa [reports, hi] using Classical.choose_spec (nonempty i)
    · intro i hi
      simp [reports, hi]
  · intro h i hi
    obtain ⟨reports, valid, agrees⟩ := h
    rw [← agrees i hi]
    exact valid i

theorem compatible_iff_lifted {X I O P : Type} (allowed : X → I → O → Prop)
    (visible : X → P) (p : P) (queried : I → Prop) (report : I → O) (x : X)
    (nonempty : ∀ i, ∃ o, allowed x i o) :
    Compatible allowed visible p queried report x ↔
      ∃ reports, Lifted allowed x reports ∧ visible x = p ∧
        ∀ i, queried i → reports i = report i := by
  constructor
  · intro ⟨hp, hr⟩
    obtain ⟨reports, valid, agrees⟩ :=
      (partial_report_extends allowed x queried report nonempty).mp hr
    exact ⟨reports, valid, hp, agrees⟩
  · intro ⟨reports, valid, hp, agrees⟩
    exact ⟨hp, (partial_report_extends allowed x queried report nonempty).mpr
      ⟨reports, valid, agrees⟩⟩

theorem answer_transfers_to_lift {X I O P A : Type} (allowed : X → I → O → Prop)
    (visible : X → P) (p : P) (queried : I → Prop) (report : I → O)
    (q : X → A) (answer : A) (nonempty : ∀ x i, ∃ o, allowed x i o) :
    (∀ x, Compatible allowed visible p queried report x → q x = answer) ↔
    (∀ x reports, Lifted allowed x reports → visible x = p →
      (∀ i, queried i → reports i = report i) → q x = answer) := by
  constructor
  · intro h x reports valid hp agrees
    apply h x
    exact (compatible_iff_lifted allowed visible p queried report x (nonempty x)).mpr
      ⟨reports, valid, hp, agrees⟩
  · intro h x hx
    obtain ⟨reports, valid, hp, agrees⟩ :=
      (compatible_iff_lifted allowed visible p queried report x (nonempty x)).mp hx
    exact h x reports valid hp agrees

theorem outer_support_sound {X I O P : Type} (actual outer : X → I → O → Prop)
    (included : ∀ x i o, actual x i o → outer x i o)
    (visible : X → P) (p : P) (queried : I → Prop) (report : I → O) (x : X)
    (h : Compatible actual visible p queried report x) :
    Compatible outer visible p queried report x := by
  exact ⟨h.1, fun i hi => included x i (report i) (h.2 i hi)⟩

theorem verified_answer_correct {X A : Type} (candidates : X → Prop)
    (q : X → A) (answer : A) (checked : ∀ x, candidates x → q x = answer)
    (actual : X) (included : candidates actual) : q actual = answer :=
  checked actual included

theorem shared_report_forces_abstention {X R A : Type} (possible : X → R → Prop)
    (q : X → A) (x y : X) (r : R) (hx : possible x r) (hy : possible y r)
    (different : q x ≠ q y) :
    ¬ ∃ decoder : R → A, ∀ s z, possible s z → decoder z = q s := by
  intro ⟨decoder, correct⟩
  exact different ((correct x r hx).symm.trans (correct y r hy))

end CalibratedRecovery

#print axioms CalibratedRecovery.partial_report_extends
#print axioms CalibratedRecovery.compatible_iff_lifted
#print axioms CalibratedRecovery.answer_transfers_to_lift
#print axioms CalibratedRecovery.outer_support_sound
#print axioms CalibratedRecovery.verified_answer_correct
#print axioms CalibratedRecovery.shared_report_forces_abstention
