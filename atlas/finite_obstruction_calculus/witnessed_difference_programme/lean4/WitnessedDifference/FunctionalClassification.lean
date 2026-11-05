import WitnessedDifference.BehavioralQuotient

/-! Universal necessity lemmas for explicitly declared functional predicates.
Linking means report factorization on realized presentation fibers. Calibration
means equality to a declared target; R3 comparator availability is not silently
equated to calibration success. No phenomenology or physical truth is inferred. -/
namespace WitnessedDifference.FunctionalClassification
universe u v w

def Linked {X : Type u} {P : Type v} {R : Type w}
    (q : X → P) (s : X → R) : Prop := ∀ x y, q x = q y → s x = s y

def Stable {X : Type u} {P : Type v} (q : X → P) (t : X → X) : Prop :=
  ∀ x, q x = q (t x)

def BlindSpot {X : Type u} {P : Type v} (q : X → P) : Prop :=
  ∃ x y, x ≠ y ∧ q x = q y

/-- No presentation collision forces every report to be linked. -/
theorem no_blind_spot_linked {X : Type u} {P : Type v} {R : Type w}
    (q : X → P) (s : X → R) (h : ¬ BlindSpot q) : Linked q s := by
  intro x y hq
  by_cases hxy : x = y
  · exact congrArg s hxy
  · exact False.elim (h ⟨x, y, hxy, hq⟩)

/-- Linked reports inherit presentation stability. -/
theorem linked_stability {X : Type u} {P : Type v} {R : Type w}
    (q : X → P) (s : X → R) (t : X → X)
    (hlink : Linked q s) (hstable : Stable q t) : Stable s t := by
  intro x
  exact hlink x (t x) (hstable x)

/-- A declared report on presentations supplies linking structurally. -/
theorem composed_report_linked {X : Type u} {P : Type v} {R : Type w}
    (q : X → P) (h : P → R) : Linked q (fun x => h (q x)) := by
  intro x y heq
  exact congrArg h heq

/-- Exact calibration transfers linkage to/from the declared target. -/
theorem calibrated_linkage {X : Type u} {P : Type v} {R : Type w}
    (q : X → P) (s b : X → R) (hcal : ∀ x, s x = b x) :
    Linked q s ↔ Linked q b := by
  constructor
  · intro h x y hq
    rw [← hcal x, ← hcal y]
    exact h x y hq
  · intro h x y hq
    rw [hcal x, hcal y]
    exact h x y hq

/-- Linked reports cannot distinguish a presentation blind spot. -/
theorem linked_blind_spot {X : Type u} {P : Type v} {R : Type w}
    (q : X → P) (s : X → R) (hlink : Linked q s) (hblind : BlindSpot q) :
    ∃ x y, x ≠ y ∧ s x = s y := by
  obtain ⟨x, y, hxy, hq⟩ := hblind
  exact ⟨x, y, hxy, hlink x y hq⟩

/-- No realized off-diagonal tolerance preserves raw-report injectivity. -/
theorem faithful_without_tolerance {X : Type u} {O : Type v} {P : Type w}
    (raw : X → O) (recognize : O → P)
    (hraw : ∀ x y, raw x = raw y → x = y)
    (htol : ¬ ∃ x y, raw x ≠ raw y ∧ recognize (raw x) = recognize (raw y)) :
    ∀ x y, recognize (raw x) = recognize (raw y) → x = y := by
  intro x y hrec
  by_cases heq : raw x = raw y
  · exact hraw x y heq
  · exact False.elim (htol ⟨x, y, heq, hrec⟩)

/-- Immediate recognized injectivity forces behavioral minimality. -/
theorem injective_report_behavioral_minimal
    {X : Type u} {I : Type v} {R : Type w}
    (action : I → X → X) (q : X → R)
    (hq : ∀ x y, q x = q y → x = y) :
    ∀ x y, BehavioralQuotient.BehavioralEq action q x y → x = y := by
  intro x y heq
  exact hq x y (heq [])

theorem identity_run {X : Type u} {I : Type v}
    (action : I → X → X) (hid : ∀ i x, action i x = x) :
    ∀ word x, BehavioralQuotient.run action word x = x := by
  intro word
  induction word with
  | nil => intro x; rfl
  | cons i word ih =>
    intro x
    change BehavioralQuotient.run action word (action i x) = x
    rw [hid i x]
    exact ih x

/-- Identity updates create no future distinctions. -/
theorem inactive_behavior_iff_report
    {X : Type u} {I : Type v} {R : Type w}
    (action : I → X → X) (q : X → R) (hid : ∀ i x, action i x = x)
    (x y : X) : BehavioralQuotient.BehavioralEq action q x y ↔ q x = q y := by
  constructor
  · intro h
    exact h []
  · intro h word
    rw [identity_run action hid word x, identity_run action hid word y]
    exact h

/-- Singleton carriers force identity updates. -/
theorem singleton_identity {X : Type u} [Subsingleton X]
    {I : Type v} (action : I → X → X) : ∀ i x, action i x = x := by
  intro i x
  exact Subsingleton.elim _ _

theorem singleton_no_blind_spot {X : Type u} [Subsingleton X]
    {P : Type v} (q : X → P) : ¬ BlindSpot q := by
  intro h
  obtain ⟨x, y, hxy, _⟩ := h
  exact hxy (Subsingleton.elim _ _)
end WitnessedDifference.FunctionalClassification

#print axioms WitnessedDifference.FunctionalClassification.no_blind_spot_linked
#print axioms WitnessedDifference.FunctionalClassification.linked_stability
#print axioms WitnessedDifference.FunctionalClassification.composed_report_linked
#print axioms WitnessedDifference.FunctionalClassification.calibrated_linkage
#print axioms WitnessedDifference.FunctionalClassification.linked_blind_spot
#print axioms WitnessedDifference.FunctionalClassification.faithful_without_tolerance
#print axioms WitnessedDifference.FunctionalClassification.injective_report_behavioral_minimal
#print axioms WitnessedDifference.FunctionalClassification.identity_run
#print axioms WitnessedDifference.FunctionalClassification.inactive_behavior_iff_report
#print axioms WitnessedDifference.FunctionalClassification.singleton_identity
#print axioms WitnessedDifference.FunctionalClassification.singleton_no_blind_spot
