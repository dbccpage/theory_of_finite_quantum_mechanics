import WitnessedDifference.Core

/-!
# Fiberwise descent

The sufficiency direction uses the stated surjectivity of the presentation map.
No selected section is treated as canonical.

The presentation-descent obstruction is the predicate
`∃ x y, q x = q y ∧ F x ≠ F y`: a pair of states with equal presentation and
unequal target. It is empty exactly when the target factors through the
surjective presentation; the factor is then unique. A section `i` of `q`
reproduces `F` as `F ∘ i ∘ q` exactly when the obstruction is empty, and then
every section does, so the equality does not single out a section.

The retraction-defect section states the commuting-square identity for the
defect `ε = 1 - i ∘ r` of a pair `(i, r)` that intertwines two differentials,
and the idempotence of `i ∘ r` when `r ∘ i` is the identity. It assumes only
that the differential respects subtraction; no group, module, or chain-homotopy
structure is used.
-/

namespace WitnessedDifference.Descent

def FiberConstant
    {State Presentation Output : Type _}
    (present : State → Presentation) (target : State → Output) : Prop :=
  ∀ ⦃left right : State⦄,
    present left = present right → target left = target right

def FactorsThrough
    {State Presentation Output : Type _}
    (present : State → Presentation) (target : State → Output) : Prop :=
  ∃ descended : Presentation → Output,
    ∀ state, descended (present state) = target state

theorem function_descends_iff_fiber_constant
    {State Presentation Output : Type _}
    (present : State → Presentation) (target : State → Output)
    (hsurjective : Function.Surjective present) :
    FactorsThrough present target ↔ FiberConstant present target := by
  constructor
  · rintro ⟨descended, hagree⟩ left right hsame
    rw [← hagree left, ← hagree right, hsame]
  · intro hfiber
    let preimage (value : Presentation) : State :=
      Classical.choose (hsurjective value)
    have hpreimage (value : Presentation) : present (preimage value) = value :=
      Classical.choose_spec (hsurjective value)
    refine ⟨fun value => target (preimage value), ?_⟩
    intro state
    exact hfiber (hpreimage (present state))

/-! ## The presentation-descent obstruction -/

section PresentationObstruction

variable {State Presentation Output : Type _}

/-- An empty obstruction predicate is fiber constancy. -/
theorem obstruction_empty_iff_fiber_constant
    (present : State → Presentation) (target : State → Output) :
    (¬ ∃ x y, present x = present y ∧ target x ≠ target y) ↔
      FiberConstant present target := by
  constructor
  · intro hempty left right hsame
    exact Classical.byContradiction fun hne => hempty ⟨left, right, hsame, hne⟩
  · rintro hfiber ⟨x, y, hsame, hne⟩
    exact hne (hfiber hsame)

/-- The obstruction set of pairs with equal presentation and unequal target is
empty exactly when the target factors through the surjective presentation. -/
theorem obstruction_empty_iff_factors
    (present : State → Presentation) (target : State → Output)
    (hsurjective : Function.Surjective present) :
    (¬ ∃ x y, present x = present y ∧ target x ≠ target y) ↔
      FactorsThrough present target := by
  rw [obstruction_empty_iff_fiber_constant,
    function_descends_iff_fiber_constant present target hsurjective]

/-- A factor through a surjective presentation is unique. -/
theorem factor_unique_of_surjective
    (present : State → Presentation) (target : State → Output)
    (hsurjective : Function.Surjective present)
    (first second : Presentation → Output)
    (hfirst : ∀ state, first (present state) = target state)
    (hsecond : ∀ state, second (present state) = target state) :
    first = second := by
  funext value
  obtain ⟨state, rfl⟩ := hsurjective value
  rw [hfirst state, hsecond state]

/-- For a section `i` of the presentation (`q ∘ i = id`), the target equals
`F ∘ i ∘ q` exactly when the obstruction set is empty. -/
theorem section_factorization_iff
    (present : State → Presentation) (target : State → Output)
    (sect : Presentation → State)
    (hsection : ∀ value, present (sect value) = value) :
    target = target ∘ sect ∘ present ↔
      ¬ ∃ x y, present x = present y ∧ target x ≠ target y := by
  rw [obstruction_empty_iff_fiber_constant]
  constructor
  · intro heq left right hsame
    have hleft := congrFun heq left
    have hright := congrFun heq right
    simp only [Function.comp] at hleft hright
    rw [hleft, hright, hsame]
  · intro hfiber
    funext state
    simp only [Function.comp]
    exact (hfiber (hsection (present state))).symm

/-- If the target equals `F ∘ i ∘ q` for one section `i`, the equality holds
for every section. -/
theorem section_factorization_all_sections
    (present : State → Presentation) (target : State → Output)
    (sect : Presentation → State)
    (hsection : ∀ value, present (sect value) = value)
    (heq : target = target ∘ sect ∘ present) :
    ∀ other : Presentation → State,
      (∀ value, present (other value) = value) →
        target = target ∘ other ∘ present := by
  intro other hother
  have hempty := (section_factorization_iff present target sect hsection).mp heq
  exact (section_factorization_iff present target other hother).mpr hempty

/-- The presentation-descent signature for a surjective presentation `q` and
a target `F`: (1) the obstruction set is empty exactly when `F` factors
through `q`; (2) any two factors agree; (3) for each section `i` of `q`,
`F = F ∘ i ∘ q` exactly when the obstruction set is empty; (4) an empty
obstruction set gives `F = F ∘ i ∘ q` for every section `i`. -/
theorem presentation_descent_signature
    (present : State → Presentation) (target : State → Output)
    (hsurjective : Function.Surjective present) :
    ((¬ ∃ x y, present x = present y ∧ target x ≠ target y) ↔
        FactorsThrough present target)
      ∧ (∀ first second : Presentation → Output,
          (∀ state, first (present state) = target state) →
          (∀ state, second (present state) = target state) →
            first = second)
      ∧ (∀ sect : Presentation → State,
          (∀ value, present (sect value) = value) →
            (target = target ∘ sect ∘ present ↔
              ¬ ∃ x y, present x = present y ∧ target x ≠ target y))
      ∧ ((¬ ∃ x y, present x = present y ∧ target x ≠ target y) →
          ∀ sect : Presentation → State,
            (∀ value, present (sect value) = value) →
              target = target ∘ sect ∘ present) := by
  refine ⟨obstruction_empty_iff_factors present target hsurjective,
    factor_unique_of_surjective present target hsurjective,
    fun sect hsection => section_factorization_iff present target sect hsection,
    ?_⟩
  intro hempty sect hsection
  exact (section_factorization_iff present target sect hsection).mpr hempty

end PresentationObstruction

/-! ## Retraction defect -/

section RetractionDefect

variable {C D : Type _}

/-- The retraction defect `ε = 1 - i ∘ r`, pointwise. -/
def retractionDefect [Sub C] (incl : D → C) (retr : C → D) (x : C) : C :=
  x - incl (retr x)

/-- The retraction defect commutes with the differential: for a differential
`d` that respects subtraction and a pair `(i, r)` with `d ∘ i = i ∘ dD` and
`dD ∘ r = r ∘ d`, `d (x - i (r x)) = d x - i (r (d x))`, that is,
`d ∘ ε = ε ∘ d`. -/
theorem retraction_defect_commutes [Sub C]
    (d : C → C) (dD : D → D) (incl : D → C) (retr : C → D)
    (d_sub : ∀ x y, d (x - y) = d x - d y)
    (d_incl : ∀ z, d (incl z) = incl (dD z))
    (dD_retr : ∀ x, dD (retr x) = retr (d x))
    (x : C) :
    d (x - incl (retr x)) = d x - incl (retr (d x)) := by
  rw [d_sub, d_incl, dD_retr]

/-- The function form of `retraction_defect_commutes`: `d ∘ ε = ε ∘ d`. -/
theorem retraction_defect_comp_eq [Sub C]
    (d : C → C) (dD : D → D) (incl : D → C) (retr : C → D)
    (d_sub : ∀ x y, d (x - y) = d x - d y)
    (d_incl : ∀ z, d (incl z) = incl (dD z))
    (dD_retr : ∀ x, dD (retr x) = retr (d x)) :
    d ∘ retractionDefect incl retr = retractionDefect incl retr ∘ d := by
  funext x
  exact retraction_defect_commutes d dD incl retr d_sub d_incl dD_retr x

/-- When `r ∘ i` is the identity, `i ∘ r` is idempotent. -/
theorem ir_idempotent (incl : D → C) (retr : C → D)
    (hretract : ∀ z, retr (incl z) = z) :
    (incl ∘ retr) ∘ (incl ∘ retr) = incl ∘ retr := by
  funext x
  simp only [Function.comp, hretract]

end RetractionDefect

end WitnessedDifference.Descent
