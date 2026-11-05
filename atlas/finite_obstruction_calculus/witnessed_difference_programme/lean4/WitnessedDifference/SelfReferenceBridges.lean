/-! Explicit finite-compatible R1/R2/R3 bridges. All tables are hypotheses;
comparison availability is separate from successful equality. Richer accessible
self-state sigma is not silently identified with its presentation. -/
namespace WitnessedDifference.SelfReferenceBridges
universe u v w z

structure ReflexiveLink (Observer : Type u) (Accessible : Type v) (Report : Type w) where
  source : Observer
  target : Observer
  captured : Accessible
  reaccessed : Accessible
  reported : Report

def VerifiedLink {X : Type u} {O : Type v} {A : Type w} {R : Type z}
    (observer : O) (sigma : X → A) (report : X → Option R)
    (generation : A → R → Prop) (x : X) (p : ReflexiveLink O A R) : Prop :=
  p.source = observer ∧ p.target = observer ∧ p.captured = sigma x ∧
  p.reaccessed = sigma x ∧ report x = some p.reported ∧ generation (sigma x) p.reported

def LinkedAt {X : Type u} {O : Type v} {A : Type w} {R : Type z}
    (observer : O) (sigma : X → A) (report : X → Option R)
    (generation : A → R → Prop)
    (provenance : X → Option (ReflexiveLink O A R)) (x : X) : Prop :=
  ∃ p, provenance x = some p ∧ VerifiedLink observer sigma report generation x p

def ReportTotal {X : Type u} {R : Type v} (report : X → Option R) : Prop :=
  ∀ x, ∃ r, report x = some r

/-- Checked reflexive linkage entails an actually available report. -/
theorem linked_report_available {X : Type u} {O : Type v} {A : Type w} {R : Type z}
    (observer : O) (sigma : X → A) (report : X → Option R)
    (generation : A → R → Prop) (provenance : X → Option (ReflexiveLink O A R))
    (x : X) (h : LinkedAt observer sigma report generation provenance x) :
    ∃ r, report x = some r := by
  obtain ⟨p, _, _, _, _, _, hr, _⟩ := h
  exact ⟨p.reported, hr⟩

/-- Deterministic generation is the missing hypothesis for report factorization. -/
theorem deterministic_link_fiber_constancy
    {X : Type u} {O : Type v} {A : Type w} {R : Type z}
    (observer : O) (sigma : X → A) (report : X → Option R)
    (generation : A → R → Prop) (provenance : X → Option (ReflexiveLink O A R))
    (hlinked : ∀ x, LinkedAt observer sigma report generation provenance x)
    (hdet : ∀ a r s, generation a r → generation a s → r = s) :
    ∀ x y, sigma x = sigma y → report x = report y := by
  intro x y hsig
  obtain ⟨px, _, _, _, _, _, hrx, hgx⟩ := hlinked x
  obtain ⟨py, _, _, _, _, _, hry, hgy⟩ := hlinked y
  rw [hrx, hry]
  have hr : px.reported = py.reported := by
    apply hdet (sigma x) px.reported py.reported hgx
    rw [hsig]
    exact hgy
  exact congrArg some hr

def FiberConstant {X : Type u} {A : Type v} {R : Type w}
    (sigma : X → A) (values : X → Option R) : Prop :=
  ∀ x y, sigma x = sigma y → values x = values y

/-- Exact iff criterion, including undefined values: a partial decoder exists
on accessible self-states iff the requested table is constant on sigma fibers.
Outside the realized image the decoder is explicitly undefined. -/
theorem partial_factor_iff {X : Type u} {A : Type v} {R : Type w}
    (sigma : X → A) (values : X → Option R) :
    (∃ decoder : A → Option R, ∀ x, decoder (sigma x) = values x) ↔
    FiberConstant sigma values := by
  constructor
  · rintro ⟨decoder, h⟩ x y heq
    rw [← h x, ← h y, heq]
  · intro hfiber
    classical
    let decoder : A → Option R := fun a =>
      if h : ∃ x, sigma x = a then values (Classical.choose h) else none
    refine ⟨decoder, ?_⟩
    intro x
    have hex : ∃ y, sigma y = sigma x := ⟨x, rfl⟩
    simp only [decoder, dif_pos hex]
    exact hfiber (Classical.choose hex) x (Classical.choose_spec hex)

/-- A prescribed target can be realized at a later state exactly when it is
constant on the fibers of the declared later-state map. -/
theorem later_realization_iff {X : Type u} {R : Type v}
    (later : X → X) (prescribed : X → Option R) :
    (∃ target : X → Option R, ∀ x, target (later x) = prescribed x) ↔
    FiberConstant later prescribed := partial_factor_iff later prescribed

/-- The actual later target is inferable from accessible self-state exactly
when its composite table is constant on sigma fibers. -/
theorem later_target_accessible_iff {X : Type u} {A : Type v} {R : Type w}
    (sigma : X → A) (later : X → X) (target : X → Option R) :
    (∃ decoder : A → Option R, ∀ x, decoder (sigma x) = target (later x)) ↔
    FiberConstant sigma (fun x => target (later x)) :=
  partial_factor_iff sigma (fun x => target (later x))

def StabilityAvailable {X : Type u} {R : Type v}
    (report : X → Option R) (context : X → X) : Prop :=
  ∀ x, (∃ r, report x = some r) ∧ (∃ r, report (context x) = some r)

/-- Total context transports make universal availability exactly report totality. -/
theorem stability_available_iff_total {X : Type u} {R : Type v}
    (report : X → Option R) (context : X → X) :
    StabilityAvailable report context ↔ ReportTotal report := by
  constructor
  · intro h x
    exact (h x).1
  · intro h x
    exact ⟨h x, h (context x)⟩

def ReportEventsPreserved {X : Type u} {R : Type v}
    (report : X → Option R) (context : X → X) : Prop :=
  ∀ x r, report x = some r → report (context x) = some r

def StabilitySuccess {X : Type u} {R : Type v}
    (report : X → Option R) (context : X → X) : Prop :=
  ∀ x, ∃ r, report x = some r ∧ report (context x) = some r

/-- Original R2 on actual report events is independent of reporting availability;
universal successful stability requires precisely totality plus preservation. -/
theorem stability_success_iff_total_preserved {X : Type u} {R : Type v}
    (report : X → Option R) (context : X → X) :
    StabilitySuccess report context ↔ ReportTotal report ∧ ReportEventsPreserved report context := by
  constructor
  · intro h
    constructor
    · intro x
      obtain ⟨r, hr, _⟩ := h x
      exact ⟨r, hr⟩
    · intro x r hr
      obtain ⟨s, hs, ht⟩ := h x
      have heq : r = s := Option.some.inj (hr.symm.trans hs)
      rw [heq]
      exact ht
  · rintro ⟨htotal, hpreserved⟩ x
    obtain ⟨r, hr⟩ := htotal x
    exact ⟨r, hr, hpreserved x r hr⟩

def ComparisonAvailable {R : Type u}
    (report target : Option R) (domain : R → R → Prop) : Prop :=
  ∃ r b, report = some r ∧ target = some b ∧ domain r b

def ComparisonSuccess {R : Type u}
    (report target : Option R) (domain : R → R → Prop) : Prop :=
  ComparisonAvailable report target domain ∧ report = target

/-- Equality is not success without an executable comparison-domain witness. -/
theorem comparison_success_iff {R : Type u}
    (report target : Option R) (domain : R → R → Prop) :
    ComparisonSuccess report target domain ↔
    ∃ r, report = some r ∧ target = some r ∧ domain r r := by
  constructor
  · rintro ⟨⟨r, b, hr, hb, hd⟩, heq⟩
    have hsome : some r = some b := hr.symm.trans (heq.trans hb)
    have hvalues : r = b := Option.some.inj hsome
    subst b
    exact ⟨r, hr, hb, hd⟩
  · rintro ⟨r, hr, hb, hd⟩
    exact ⟨⟨r, r, hr, hb, hd⟩, hr.trans hb.symm⟩

/-- Successful later comparison plus deterministic linkage forces the later
target to be constant on accessible-state fibers: collision refutes success. -/
theorem later_collision_obstruction
    {X : Type u} {A : Type v} {R : Type w}
    (sigma : X → A) (report : X → Option R) (later : X → X)
    (target : X → Option R) (hfactor : FiberConstant sigma report)
    (hsuccess : ∀ x, report x = target (later x)) :
    FiberConstant sigma (fun x => target (later x)) := by
  intro x y hsig
  change target (later x) = target (later y)
  rw [← hsuccess x, ← hsuccess y]
  exact hfactor x y hsig

/-- Complete fixed-bridge existence criterion: a linked report can successfully
compare against every later target iff each later value is defined, admitted by
its generation relation, and executable on the comparator's diagonal. -/
theorem successful_linked_report_exists_iff
    {X : Type u} {O : Type v} {A : Type w} {R : Type z}
    (observer : O) (sigma : X → A) (later : X → X) (target : X → Option R)
    (generation : A → R → Prop) (domain : R → R → Prop) :
    (∃ (report : X → Option R) (provenance : X → Option (ReflexiveLink O A R)),
      (∀ x, LinkedAt observer sigma report generation provenance x) ∧
      (∀ x, ComparisonSuccess (report x) (target (later x)) domain)) ↔
    (∀ x, ∃ r, target (later x) = some r ∧ generation (sigma x) r ∧ domain r r) := by
  constructor
  · rintro ⟨report, provenance, hlink, hsuccess⟩ x
    obtain ⟨p, _, _, _, _, _, hr, hg⟩ := hlink x
    obtain ⟨r, hreport, htarget, hd⟩ :=
      (comparison_success_iff (report x) (target (later x)) domain).mp (hsuccess x)
    have hvalues : p.reported = r := Option.some.inj (hr.symm.trans hreport)
    rw [hvalues] at hg
    exact ⟨r, htarget, hg, hd⟩
  · intro h
    classical
    let value : X → R := fun x => Classical.choose (h x)
    have hv : ∀ x, target (later x) = some (value x) ∧
        generation (sigma x) (value x) ∧ domain (value x) (value x) := by
      intro x
      exact Classical.choose_spec (h x)
    let report : X → Option R := fun x => some (value x)
    let link : X → ReflexiveLink O A R := fun x =>
      ⟨observer, observer, sigma x, sigma x, value x⟩
    let provenance : X → Option (ReflexiveLink O A R) := fun x => some (link x)
    refine ⟨report, provenance, ?_, ?_⟩
    · intro x
      refine ⟨link x, rfl, ?_⟩
      exact ⟨rfl, rfl, rfl, rfl, rfl, (hv x).2.1⟩
    · intro x
      apply (comparison_success_iff (report x) (target (later x)) domain).mpr
      exact ⟨value x, rfl, (hv x).1, (hv x).2.2⟩

end WitnessedDifference.SelfReferenceBridges
#print axioms WitnessedDifference.SelfReferenceBridges.linked_report_available
#print axioms WitnessedDifference.SelfReferenceBridges.deterministic_link_fiber_constancy
#print axioms WitnessedDifference.SelfReferenceBridges.partial_factor_iff
#print axioms WitnessedDifference.SelfReferenceBridges.later_realization_iff
#print axioms WitnessedDifference.SelfReferenceBridges.later_target_accessible_iff
#print axioms WitnessedDifference.SelfReferenceBridges.stability_available_iff_total
#print axioms WitnessedDifference.SelfReferenceBridges.comparison_success_iff
#print axioms WitnessedDifference.SelfReferenceBridges.later_collision_obstruction

#print axioms WitnessedDifference.SelfReferenceBridges.successful_linked_report_exists_iff

#print axioms WitnessedDifference.SelfReferenceBridges.stability_success_iff_total_preserved
