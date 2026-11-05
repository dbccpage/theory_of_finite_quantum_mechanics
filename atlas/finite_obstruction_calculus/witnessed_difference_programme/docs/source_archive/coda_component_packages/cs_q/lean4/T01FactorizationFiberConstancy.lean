import D01D02Records

/-!
# CODA-CS-Q T01: Profile Factorization & Fiber Constancy (BRIDGE-001 / BRIDGE-002)

Formalizes:
1. BRIDGE-001 Forward: Total profile factorization implies fiber constancy.
2. Constructive Image Reverse: Fiber constancy implies well-defined factor on `ImagePoint`.
3. Image-Restricted Iff: Factorization on `ImagePoint` iff fiber constancy.
4. Total Reverse Fence: Total reverse on all `β` is OPEN without section/choice.
5. BRIDGE-002: Degree-bounded query family factorization implies member fiber constancy.

AuthorityEffect: None.
-/

namespace CodaCsQ

open CodaCsQ

set_option linter.unusedVariables false

variable {α β γ : Type}

/-- Theorem 2.1 (FORWARD): Profile Factorization implies Fiber Constancy (BRIDGE-001). -/
theorem factorization_implies_fiber_constancy
    (Prof : α → β) (q : α → γ) (q_bar : β → γ)
    (h : profile_factorization Prof q q_bar) :
    fiber_constant Prof q := by
  intro x y h_prof
  dsimp [profile_factorization] at h
  rw [h x, h y, h_prof]

/-- Pointwise section helper (FACTORIZATION_ASSUMED) - not a total reverse without choice. -/
theorem factorization_from_pointwise_section
    (Prof : α → β) (q : α → γ)
    (q_bar : β → γ)
    (h_factor : ∀ b : β, ∀ x : α, Prof x = b → q_bar b = q x) :
    profile_factorization Prof q q_bar := by
  intro x
  exact (h_factor (Prof x) x rfl).symm

/-- Under fiber constancy, `q_bar_on_image` depends only on `val` (well-definedness). -/
theorem q_bar_on_image_well_defined
    (Prof : α → β) (q : α → γ) (h_fc : fiber_constant Prof q)
    (p₁ p₂ : ImagePoint Prof) (h_val : p₁.val = p₂.val) :
    q_bar_on_image Prof q h_fc p₁ = q_bar_on_image Prof q h_fc p₂ := by
  dsimp [q_bar_on_image]
  apply h_fc
  calc
    Prof p₁.witness = p₁.val := p₁.eq
    _ = p₂.val := h_val
    _ = Prof p₂.witness := p₂.eq.symm

/-- FORWARD on image: well-defined image factorization implies fiber constancy. -/
theorem image_factorization_implies_fiber_constancy
    (Prof : α → β) (q : α → γ) (q_bar_im : ImagePoint Prof → γ)
    (h : image_profile_factorization Prof q q_bar_im) :
    fiber_constant Prof q := by
  intro x y h_prof
  have h_pt := h.1
  have h_wd := h.2
  calc
    q x = q_bar_im (imagePoint_of Prof x) := h_pt x
    _ = q_bar_im (imagePoint_of Prof y) :=
      h_wd (imagePoint_of Prof x) (imagePoint_of Prof y) h_prof
    _ = q y := (h_pt y).symm

/-- REVERSE on image: fiber constancy implies pointwise identity on canonical image points. -/
theorem fiber_constancy_implies_image_factorization
    (Prof : α → β) (q : α → γ) (h_fc : fiber_constant Prof q) :
    ∀ x : α, q x = q_bar_on_image Prof q h_fc (imagePoint_of Prof x) := by
  intro x
  rfl

/-- Package reverse as full `image_profile_factorization` for the constructive factor. -/
theorem fiber_constancy_implies_image_profile_factorization
    (Prof : α → β) (q : α → γ) (h_fc : fiber_constant Prof q) :
    image_profile_factorization Prof q (q_bar_on_image Prof q h_fc) := by
  refine ⟨fiber_constancy_implies_image_factorization Prof q h_fc, ?_⟩
  intro p₁ p₂ h_val
  exact q_bar_on_image_well_defined Prof q h_fc p₁ p₂ h_val

/--
True **iff on the image-restricted statement**:
existence of a well-defined factor out of `ImagePoint` ↔ fiber constancy.
Total reverse on all of `β` remains OPEN.
-/
theorem factorization_iff_fiber_constancy_on_image
    (Prof : α → β) (q : α → γ) :
    (∃ q_bar_im : ImagePoint Prof → γ, image_profile_factorization Prof q q_bar_im) ↔
      fiber_constant Prof q := by
  constructor
  · intro h
    rcases h with ⟨q_bar_im, h_im⟩
    exact image_factorization_implies_fiber_constancy Prof q q_bar_im h_im
  · intro h_fc
    exact ⟨q_bar_on_image Prof q h_fc,
      fiber_constancy_implies_image_profile_factorization Prof q h_fc⟩

/-- Total factorization restricts to a well-defined image factorization. -/
theorem total_factorization_implies_image_factorization
    (Prof : α → β) (q : α → γ) (q_bar : β → γ)
    (h : profile_factorization Prof q q_bar) :
    image_profile_factorization Prof q (fun p : ImagePoint Prof => q_bar p.val) := by
  refine ⟨?_, ?_⟩
  · intro x
    exact h x
  · intro p₁ p₂ h_val
    exact congrArg q_bar h_val

/-- Degree-bounded query family Q_{≤ n} factorization predicate (BRIDGE-002). -/
def query_family_factorization (Prof : α → β) : List (α → γ) → List (β → γ) → Prop
  | [], [] => True
  | q :: qs, q_bar :: q_bars => profile_factorization Prof q q_bar ∧ query_family_factorization Prof qs q_bars
  | _, _ => False

/-- Theorem: Query family factorization implies every member is fiber constant (FORWARD). -/
theorem query_family_factorization_implies_fiber_constant
    (Prof : α → β) (queries : List (α → γ)) (q_bars : List (β → γ))
    (h_fact : query_family_factorization Prof queries q_bars) :
    ∀ q ∈ queries, fiber_constant Prof q := by
  intro q h_in
  induction queries generalizing q_bars with
  | nil =>
    nomatch h_in
  | cons q' qs ih =>
    cases q_bars with
    | nil =>
      dsimp [query_family_factorization] at h_fact
    | cons q_bar' q_bars' =>
      dsimp [query_family_factorization] at h_fact
      rcases List.mem_cons.mp h_in with h_eq | h_tail
      · rw [h_eq]
        exact factorization_implies_fiber_constancy Prof q' q_bar' h_fact.1
      · exact ih q_bars' h_fact.2 h_tail

end CodaCsQ
