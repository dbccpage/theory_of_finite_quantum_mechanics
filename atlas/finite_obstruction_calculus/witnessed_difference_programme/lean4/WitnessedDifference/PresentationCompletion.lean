import Mathlib.Topology.MetricSpace.Completion

/-!
# Protected queries on a realized presentation and its metric completion

This is the metric-space statement of Appendix O.1. The source set is
arbitrary; the presentation and answer spaces are admitted metric spaces.
Completeness of the answer space is explicit when extending a query.
The total Mathlib extension construction alone certifies no agreement.
No circle character, Haar integral, physical model or authority is asserted.
-/

namespace WitnessedDifference.PresentationCompletion

open UniformSpace

universe u v w

variable {X : Type u} {P : Type v} {Y : Type w}
variable [MetricSpace P] [MetricSpace Y]

/-- The original source point, retained as a point of the actual image. -/
def imagePresentation (p : X → P) (x : X) : Set.range p :=
  ⟨p x, ⟨x, rfl⟩⟩

/-- Nearby presented values must control nearby protected answers. -/
def RelativeControl (p : X → P) (q : X → Y) : Prop :=
  ∀ ε > 0, ∃ δ > 0, ∀ x x',
    dist (p x) (p x') < δ → dist (q x) (q x') < ε

theorem relative_control_fiber_constant (p : X → P) (q : X → Y)
    (h : RelativeControl p q) {x x' : X} (hp : p x = p x') : q x = q x' := by
  by_contra hne
  have hpos : 0 < dist (q x) (q x') := dist_pos.mpr hne
  obtain ⟨δ, hδ, hc⟩ := h _ hpos
  have hd : dist (p x) (p x') < δ := by simpa [hp] using hδ
  exact (lt_irrefl _) (hc x x' hd)

/-- A chosen image witness defines a map; agreement still needs fibre control. -/
noncomputable def imageQuery (p : X → P) (q : X → Y) (s : Set.range p) : Y :=
  q (Classical.choose s.property)

theorem imageQuery_agrees (p : X → P) (q : X → Y)
    (h : RelativeControl p q) (x : X) : imageQuery p q (imagePresentation p x) = q x := by
  apply relative_control_fiber_constant p q h
  exact Classical.choose_spec (imagePresentation p x).property

theorem uniformContinuous_imageQuery (p : X → P) (q : X → Y)
    (h : RelativeControl p q) : UniformContinuous (imageQuery p q) := by
  rw [Metric.uniformContinuous_iff]
  intro ε hε
  obtain ⟨δ, hδ, hc⟩ := h ε hε
  refine ⟨δ, hδ, ?_⟩
  intro s t hst
  have hs := Classical.choose_spec s.property
  have ht := Classical.choose_spec t.property
  apply hc (Classical.choose s.property) (Classical.choose t.property)
  change dist (s : P) (t : P) < δ at hst
  simpa only [hs, ht] using hst

theorem relativeControl_of_uniform_factor (p : X → P) (q : X → Y)
    (g : Set.range p → Y) (hg : UniformContinuous g)
    (agrees : ∀ x, g (imagePresentation p x) = q x) : RelativeControl p q := by
  intro ε hε
  obtain ⟨δ, hδ, hc⟩ := Metric.uniformContinuous_iff.mp hg ε hε
  refine ⟨δ, hδ, ?_⟩
  intro x x' hxx'
  have hdist : dist (g (imagePresentation p x)) (g (imagePresentation p x')) < ε :=
    hc hxx'
  simpa [agrees] using hdist

theorem relativeControl_iff_image_factor (p : X → P) (q : X → Y) :
    RelativeControl p q ↔ ∃ g : Set.range p → Y,
      UniformContinuous g ∧ ∀ x, g (imagePresentation p x) = q x := by
  constructor
  · intro h
    exact ⟨imageQuery p q, uniformContinuous_imageQuery p q h, imageQuery_agrees p q h⟩
  · rintro ⟨g, hg, agrees⟩
    exact relativeControl_of_uniform_factor p q g hg agrees

omit [MetricSpace P] [MetricSpace Y] in
theorem image_factors_unique (p : X → P) (q : X → Y)
    (g k : Set.range p → Y)
    (hg : ∀ x, g (imagePresentation p x) = q x)
    (hk : ∀ x, k (imagePresentation p x) = q x) : g = k := by
  funext s
  obtain ⟨x, hx⟩ := s.property
  have hs : imagePresentation p x = s := Subtype.ext hx
  calc
    g s = g (imagePresentation p x) := congrArg g hs.symm
    _ = q x := hg x
    _ = k (imagePresentation p x) := (hk x).symm
    _ = k s := congrArg k hs

/-- The construction is total; its recovery theorem requires RelativeControl. -/
noncomputable def completedQuery (p : X → P) (q : X → Y) : Completion (Set.range p) → Y :=
  Completion.extension (imageQuery p q)

theorem completedQuery_uniform [CompleteSpace Y] (p : X → P) (q : X → Y) :
    UniformContinuous (completedQuery p q) := Completion.uniformContinuous_extension

theorem completedQuery_agrees [CompleteSpace Y] (p : X → P) (q : X → Y)
    (h : RelativeControl p q) (x : X) :
    completedQuery p q (imagePresentation p x : Completion (Set.range p)) = q x := by
  rw [completedQuery, Completion.extension_coe (uniformContinuous_imageQuery p q h)]
  exact imageQuery_agrees p q h x

theorem completedQuery_unique [CompleteSpace Y] (p : X → P) (q : X → Y)
    (h : RelativeControl p q) (g : Completion (Set.range p) → Y)
    (hg : UniformContinuous g)
    (agrees : ∀ x, g (imagePresentation p x : Completion (Set.range p)) = q x) :
    completedQuery p q = g := by
  apply Completion.extension_unique (uniformContinuous_imageQuery p q h) hg
  intro s
  obtain ⟨x, hx⟩ := s.property
  have hs : imagePresentation p x = s := Subtype.ext hx
  rw [← hs]
  exact (imageQuery_agrees p q h x).trans (agrees x).symm

theorem relativeControl_iff_unique_completion [CompleteSpace Y]
    (p : X → P) (q : X → Y) :
    RelativeControl p q ↔ ∃! g : Completion (Set.range p) → Y,
      UniformContinuous g ∧ ∀ x,
        g (imagePresentation p x : Completion (Set.range p)) = q x := by
  constructor
  · intro h
    refine ⟨completedQuery p q, ⟨completedQuery_uniform p q, completedQuery_agrees p q h⟩, ?_⟩
    intro g hg
    exact (completedQuery_unique p q h g hg.1 hg.2).symm
  · rintro ⟨g, hg, _⟩
    apply relativeControl_of_uniform_factor p q (fun s => g (s : Completion (Set.range p)))
    · exact hg.1.comp (Completion.uniformContinuous_coe (Set.range p))
    · exact hg.2

section SourceTransport

variable [MetricSpace X]

theorem imagePresentation_uniform (p : X → P) (hp : UniformContinuous p) :
    UniformContinuous (imagePresentation p) := by
  rw [Metric.uniformContinuous_iff] at hp ⊢
  intro ε hε
  obtain ⟨δ, hδ, hc⟩ := hp ε hε
  refine ⟨δ, hδ, ?_⟩
  intro x y hxy
  exact hc hxy

theorem query_uniform (p : X → P) (q : X → Y)
    (h : RelativeControl p q) (hp : UniformContinuous p) : UniformContinuous q := by
  have heq : imageQuery p q ∘ imagePresentation p = q :=
    funext (imageQuery_agrees p q h)
  rw [← heq]
  exact (uniformContinuous_imageQuery p q h).comp (imagePresentation_uniform p hp)

noncomputable def completedPresentation (p : X → P) :
    Completion X → Completion (Set.range p) :=
  Completion.extension (fun x => (imagePresentation p x : Completion (Set.range p)))

theorem completedPresentation_uniform (p : X → P) :
    UniformContinuous (completedPresentation p) := Completion.uniformContinuous_extension

theorem completedPresentation_agrees (p : X → P) (hp : UniformContinuous p) (x : X) :
    completedPresentation p (x : Completion X) =
      (imagePresentation p x : Completion (Set.range p)) := by
  exact Completion.extension_coe
    ((Completion.uniformContinuous_coe (Set.range p)).comp (imagePresentation_uniform p hp)) x

theorem completion_routes_commute [CompleteSpace Y] (p : X → P) (q : X → Y)
    (h : RelativeControl p q) (hp : UniformContinuous p) :
    Completion.extension q = completedQuery p q ∘ completedPresentation p := by
  apply Completion.extension_unique (query_uniform p q h hp)
    ((completedQuery_uniform p q).comp (completedPresentation_uniform p))
  intro x
  simp only [Function.comp_apply]
  rw [completedPresentation_agrees p hp x, completedQuery_agrees p q h x]

end SourceTransport

end WitnessedDifference.PresentationCompletion

