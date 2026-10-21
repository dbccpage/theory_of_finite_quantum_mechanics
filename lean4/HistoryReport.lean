import Mathlib.Logic.Function.Basic

/-!
# History-report criterion: factoring through the report image, and what each direction costs

AuthorityEffect: None.  Scope: arbitrary types `H` (histories), `V` (reports), `S` (answers) and
functions `report : H -> V`, `answer : H -> S`.  Nothing here concerns physical histories, measurement,
probability, or any structure on `H`, `V`, `S`.

Re-derivation of the criterion declared in `Paper.lean` (`history_report_criterion`,
`history_factor_unique`) with the axiom bill of each direction recorded by `#print axioms` at the end:

* factors-through-the-image  =>  constant on report fibers   needs no representative selection;
* constant on fibers  =>  factors, GIVEN a selector of a history in every nonempty fiber, needs none either;
* constant on fibers  =>  factors, for an arbitrary report, obtains the selector from `Classical.choice`.
  The kernel report below says exactly which axioms each statement uses; nothing is claimed about
  independence of the choice axiom (this file proves no unprovability result).

The constructive listed-history reconstruction is the sibling node PG-PREGEN-CONSTRUCTIVE-SUMMARY
(`PregenConstructive.lean`); it is deliberately not repeated here.
-/

namespace HistoryReport

universe u v w
variable {H : Type u} {V : Type v} {S : Type w}

/-- The image of the report, as a subtype of the report type. -/
def ReportImage (report : H → V) : Type v := {v : V // ∃ h, report h = v}

/-- A history, seen through its report, as a point of the report image. -/
def imageReport (report : H → V) (h : H) : ReportImage report := ⟨report h, ⟨h, rfl⟩⟩

/-- Constant on report fibers: histories with equal reports have equal answers. -/
def FiberConstant (report : H → V) (answer : H → S) : Prop :=
  ∀ h h', report h = report h' → answer h = answer h'

/-- The answer factors through the report image. -/
def FactorsOnImage (report : H → V) (answer : H → S) : Prop :=
  ∃ g : ReportImage report → S, ∀ h, g (imageReport report h) = answer h

/-- Factoring implies fiber constancy.  No representative is selected. -/
theorem fiberConstant_of_factors {report : H → V} {answer : H → S}
    (hf : FactorsOnImage report answer) : FiberConstant report answer := by
  obtain ⟨g, hg⟩ := hf
  intro h h' heq
  have hv : imageReport report h = imageReport report h' := Subtype.ext heq
  rw [← hg h, ← hg h', hv]

/-- Fiber constancy implies factoring, GIVEN a selector `rep` of a history in each fiber of the image.
No choice axiom is used: the selector is a hypothesis. -/
theorem factors_of_fiberConstant_of_selector {report : H → V} {answer : H → S}
    (rep : ReportImage report → H) (hrep : ∀ v, report (rep v) = v.1)
    (hc : FiberConstant report answer) : FactorsOnImage report answer := by
  refine ⟨fun v => answer (rep v), ?_⟩
  intro h
  exact hc _ _ (hrep (imageReport report h))

/-- For an arbitrary report the selector is obtained from `Classical.choice`. -/
theorem selector_exists (report : H → V) :
    ∃ rep : ReportImage report → H, ∀ v, report (rep v) = v.1 :=
  ⟨fun v => Classical.choose v.2, fun v => Classical.choose_spec v.2⟩

/-- The criterion for arbitrary types: factors on the image iff constant on fibers. -/
theorem history_report_criterion (report : H → V) (answer : H → S) :
    FactorsOnImage report answer ↔ FiberConstant report answer := by
  refine ⟨fiberConstant_of_factors, fun hc => ?_⟩
  obtain ⟨rep, hrep⟩ := selector_exists report
  exact factors_of_fiberConstant_of_selector rep hrep hc

/-- Uniqueness on the image: two factorizations through the image are equal. -/
theorem factor_unique_on_image {report : H → V} {answer : H → S}
    (a b : ReportImage report → S)
    (ha : ∀ h, a (imageReport report h) = answer h)
    (hb : ∀ h, b (imageReport report h) = answer h) : a = b := by
  funext v
  obtain ⟨h, hh⟩ := v.2
  have hv : imageReport report h = v := Subtype.ext hh
  rw [← hv, ha, hb]

/-- Boundary: two histories with one report and two answers refute factoring (the hypothesis cannot be dropped). -/
theorem not_factors_of_split {report : H → V} {answer : H → S} {h h' : H}
    (same : report h = report h') (different : answer h ≠ answer h') :
    ¬ FactorsOnImage report answer :=
  fun hf => different (fiberConstant_of_factors hf h h' same)

/-- Off the image the extension is NOT unique: moving the value at an unreported point keeps the factorization. -/
theorem off_image_not_unique [DecidableEq V] {report : H → V} {answer : H → S}
    (f : V → S) (hf : ∀ h, f (report h) = answer h) (v0 : V) (hv0 : ∀ h, report h ≠ v0)
    (s : S) (hs : s ≠ f v0) :
    ∃ f' : V → S, (∀ h, f' (report h) = answer h) ∧ f' ≠ f := by
  refine ⟨Function.update f v0 s, ?_, ?_⟩
  · intro h
    rw [Function.update_of_ne (hv0 h)]
    exact hf h
  · intro heq
    have := congrFun heq v0
    simp at this
    exact hs this

/-- On the image the extension is forced: if the report is surjective, an extension is unique. -/
theorem extension_unique_of_surjective {report : H → V} {answer : H → S}
    (hsurj : ∀ v, ∃ h, report h = v) (f f' : V → S)
    (hf : ∀ h, f (report h) = answer h) (hf' : ∀ h, f' (report h) = answer h) : f = f' := by
  funext v
  obtain ⟨h, rfl⟩ := hsurj v
  rw [hf, hf']

/-- Instance, not the general statement: reports `h % 2` on three histories, answer `h`, is NOT fiber constant. -/
theorem instance_split : ¬ FiberConstant (fun h : Fin 3 => h.val % 2) (fun h : Fin 3 => h.val) := by
  intro hc
  have := hc 0 2 (by decide)
  simp at this

end HistoryReport

#print axioms HistoryReport.fiberConstant_of_factors
#print axioms HistoryReport.factors_of_fiberConstant_of_selector
#print axioms HistoryReport.selector_exists
#print axioms HistoryReport.history_report_criterion
#print axioms HistoryReport.factor_unique_on_image
#print axioms HistoryReport.not_factors_of_split
#print axioms HistoryReport.off_image_not_unique
#print axioms HistoryReport.extension_unique_of_surjective
#print axioms HistoryReport.instance_split
