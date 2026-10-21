import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Sum

/-!
# Off-image refusal for a section/retraction pair, and for the pinned S(n) retraction

AuthorityEffect: None.  Two parts, both general over their parameters.

**Part 1, abstract.**  A section `s : S → Y` and a retraction `r : Y → S ⊕ Unit` (the refusal summand is `Unit`)
form a `SectionRetraction` when `r (s x) = inl x` (the old-image law) and every accepted point round-trips,
`r y = inl x → s x = y` (soundness).  Then `s` is injective, `r y = inr ()` holds exactly off the image of `s`
(`refused_iff_off_image`), `s (r y) = y` fails exactly off the image (`roundtrip_fails_off_image`), and the
soundness hypothesis cannot be dropped: a lax retraction obeying the law accepts an off-image point
(`lax_retraction_obeys_law_but_accepts_off_image`).  The law alone does not refuse; soundness is what refuses.

**Part 2, the pinned S(n) model.**  `Pres`, `Base`, `sectionLift` and `retr` restate `SnPresentation`,
`BasePresentation`, `sectionLift` and `retractionDownMap` of the pinned `SnCarrier.lean` (sha256 357376de...), the
glyph alphabet abstracted to an arbitrary type `G` and the one-field wrapper structures flattened.  The source
file `omega_engine_education/documentation/002_oesn/lean4/SnOffImage.lean` proves the same statements for the
36-glyph alphabet; this file proves them for every `G`, independently:
`accepted_only_from_section`, `nonDescent_iff_off_image`, `accepted_iff`, `retraction_stage_strict`, `inImage_iff`.

Scope: the five base shapes at one stage index each, nothing about cardinalities of the declared carrier table
(node PG-SN-CARRIER) and nothing about nested lift/retraction/refusal terms as base members.
-/

namespace SnOffImageRefusal

/-! ### Part 1: abstract section and retraction -/

/-- Old-image law and soundness: the content of "off-image points are refused by the round trip". -/
structure SectionRetraction {S Y : Type} (s : S → Y) (r : Y → S ⊕ Unit) : Prop where
  law : ∀ x, r (s x) = Sum.inl x
  sound : ∀ y x, r y = Sum.inl x → s x = y

section
variable {S Y : Type} {s : S → Y} {r : Y → S ⊕ Unit}

theorem SectionRetraction.injective (h : SectionRetraction s r) : Function.Injective s := by
  intro x x' hxx
  have : (Sum.inl x : S ⊕ Unit) = Sum.inl x' := by rw [← h.law x, hxx, h.law x']
  exact Sum.inl.inj this

/-- The refusal summand is returned exactly off the image of the section. -/
theorem refused_iff_off_image (h : SectionRetraction s r) (y : Y) :
    r y = Sum.inr () ↔ ∀ x, s x ≠ y := by
  constructor
  · intro hr x hx
    have := h.law x
    rw [hx, hr] at this
    cases this
  · intro hoff
    cases hy : r y with
    | inl x => exact absurd (h.sound y x hy) (hoff x)
    | inr u => cases u; rfl

/-- The round trip `s (r y) = y` holds exactly on the image; off the image it fails. -/
theorem roundtrip_iff_in_image (h : SectionRetraction s r) (y : Y) :
    (∃ x, r y = Sum.inl x ∧ s x = y) ↔ ∃ x, s x = y := by
  constructor
  · rintro ⟨x, _, hx⟩; exact ⟨x, hx⟩
  · rintro ⟨x, hx⟩
    exact ⟨x, by rw [← hx]; exact h.law x, hx⟩

theorem roundtrip_fails_off_image (h : SectionRetraction s r) (y : Y) (hoff : ∀ x, s x ≠ y) :
    ¬ ∃ x, r y = Sum.inl x ∧ s x = y := by
  rintro ⟨x, _, hx⟩
  exact hoff x hx

end

/-- CIRCULAR BY CONSTRUCTION: refusal is defined as failure of the round trip, so refusal-iff-off-image holds by
construction here and is not evidence for the S(n) statement (`sn_refused_iff_off_image`).  Any total left inverse
`r0` of a section yields a refusing retraction by testing the round trip `s (r0 y) = y`; the result is a
`SectionRetraction`.  This is the construction behind the toy witness of the source
(`s x = 2 x`, `r0 y = y / 2`; odd points are refused). -/
def refuseOffImage {S Y : Type} [DecidableEq Y] (s : S → Y) (r0 : Y → S) : Y → S ⊕ Unit :=
  fun y => if s (r0 y) = y then Sum.inl (r0 y) else Sum.inr ()

theorem refuseOffImage_isSectionRetraction {S Y : Type} [DecidableEq Y] (s : S → Y) (r0 : Y → S)
    (h : ∀ x, r0 (s x) = x) : SectionRetraction s (refuseOffImage s r0) := by
  constructor
  · intro x
    simp [refuseOffImage, h]
  · intro y x hx
    unfold refuseOffImage at hx
    by_cases hc : s (r0 y) = y
    · rw [if_pos hc] at hx
      have : r0 y = x := Sum.inl.inj hx
      rw [← this]; exact hc
    · rw [if_neg hc] at hx
      cases hx

/-- The toy witness over `ℕ` (section `2x`, total retraction `y / 2`): a point is refused exactly when it is odd.
Circular by construction (refusal is the round-trip test); it reproduces the source toy witness only. -/
theorem toy_refused_iff_odd (y : ℕ) :
    refuseOffImage (fun x : ℕ => 2 * x) (fun y => y / 2) y = Sum.inr () ↔ y % 2 = 1 := by
  have hsr : SectionRetraction (fun x : ℕ => 2 * x) (refuseOffImage (fun x : ℕ => 2 * x) (fun y => y / 2)) :=
    refuseOffImage_isSectionRetraction _ _ (fun x => by omega)
  rw [refused_iff_off_image hsr]
  constructor
  · intro h
    by_contra hne
    exact h (y / 2) (by omega)
  · intro h x hx
    omega

/-- Soundness cannot be dropped: the law alone does not refuse.  On `Fin 1 → Fin 2` the retraction that sends
the off-image point to the old term obeys the law and accepts it (instance). -/
theorem lax_retraction_obeys_law_but_accepts_off_image :
    ∃ (s : Fin 1 → Fin 2) (r : Fin 2 → Fin 1 ⊕ Unit),
      (∀ x, r (s x) = Sum.inl x) ∧ (∀ x, s x ≠ 1) ∧ r 1 ≠ Sum.inr () ∧
        ¬ ∀ y x, r y = Sum.inl x → s x = y :=
  ⟨fun _ => 0, fun _ => Sum.inl 0, by decide, by decide, by decide, by decide⟩

/-! ### Part 2: the pinned S(n) model over an arbitrary alphabet -/

inductive Rel (G : Type) where
  | pair (first second : G)
  | cut (src tgt : G)
  | simplex (v0 v1 : G)
  deriving DecidableEq

inductive Base (G : Type) where
  | ground
  | supplied (mark : G)
  | relation (r : Rel G)
  deriving DecidableEq

inductive Body (G : Type) where
  | arrow (src tgt : G)
  | pair (first second : G)
  | glyphs (gs : List G)
  deriving DecidableEq

inductive Pres (G : Type) where
  | ground
  | supplied (mark : G)
  | relation (r : Rel G)
  | lift (stage : Nat) (body : Body G)
  | retraction (stage : Nat) (body : Body G)
  | nonDescent
  deriving DecidableEq

inductive Outcome (G : Type) where
  | accepted (p : Pres G)
  | nonDescent
  deriving DecidableEq

variable {G : Type}

def Base.toPres : Base G → Pres G
  | .ground => .ground
  | .supplied m => .supplied m
  | .relation r => .relation r

def sectionLift (stage : Nat) : Base G → Pres G
  | .ground => .lift stage (.glyphs [])
  | .supplied m => .lift stage (.glyphs [m])
  | .relation (.pair f s) => .lift stage (.glyphs [f, s])
  | .relation (.cut a b) => .lift stage (.arrow a b)
  | .relation (.simplex a b) => .lift stage (.pair a b)

def retr (stage : Nat) : Pres G → Outcome G
  | .lift n body =>
    if n = stage then
      match body with
      | .glyphs [] => .accepted .ground
      | .glyphs [m] => .accepted (.supplied m)
      | .glyphs [f, s] => .accepted (.relation (.pair f s))
      | .arrow a b => .accepted (.relation (.cut a b))
      | .pair a b => .accepted (.relation (.simplex a b))
      | _ => .nonDescent
    else .nonDescent
  | _ => .nonDescent

theorem old_image_base (n : Nat) (b : Base G) : retr n (sectionLift n b) = .accepted b.toPres := by
  cases b with
  | ground => simp [sectionLift, retr, Base.toPres]
  | supplied m => simp [sectionLift, retr, Base.toPres]
  | relation r => cases r <;> simp [sectionLift, retr, Base.toPres]

theorem toPres_injective {b b' : Base G} (h : b.toPres = b'.toPres) : b = b' := by
  cases b with
  | ground => cases b' with
    | ground => rfl
    | supplied m => cases h
    | relation r => cases h
  | supplied m => cases b' with
    | ground => cases h
    | supplied m' => cases h; rfl
    | relation r => cases h
  | relation r => cases b' with
    | ground => cases h
    | supplied m' => cases h
    | relation r' => cases h; rfl

theorem sectionLift_injective (n : Nat) : Function.Injective (sectionLift n : Base G → Pres G) := by
  intro b b' h
  have h1 := old_image_base n b
  have h2 := old_image_base n b'
  rw [h] at h1
  rw [h1] at h2
  injection h2 with h3
  exact toPres_injective h3

/-- Every accepted outcome comes from a section image, and the payload is the base presentation read back. -/
theorem accepted_only_from_section (n : Nat) (p q : Pres G) (h : retr n p = .accepted q) :
    ∃ b : Base G, p = sectionLift n b ∧ q = b.toPres := by
  cases p with
  | ground => simp [retr] at h
  | supplied m => simp [retr] at h
  | relation r => simp [retr] at h
  | retraction k body => simp [retr] at h
  | nonDescent => simp [retr] at h
  | lift k body =>
    by_cases hk : k = n
    · subst hk
      cases body with
      | arrow a c => exact ⟨.relation (.cut a c), rfl, by simpa [retr, Base.toPres] using h.symm⟩
      | pair a c => exact ⟨.relation (.simplex a c), rfl, by simpa [retr, Base.toPres] using h.symm⟩
      | glyphs gs =>
        match gs, h with
        | [], h => exact ⟨.ground, rfl, by simpa [retr, Base.toPres] using h.symm⟩
        | [m], h => exact ⟨.supplied m, rfl, by simpa [retr, Base.toPres] using h.symm⟩
        | [f, s], h => exact ⟨.relation (.pair f s), rfl, by simpa [retr, Base.toPres] using h.symm⟩
        | _ :: _ :: _ :: _, h => simp [retr] at h
    · simp [retr, hk] at h

/-- The accepted outcomes are exactly the section images, with the expected payload. -/
theorem accepted_iff (n : Nat) (p q : Pres G) :
    retr n p = .accepted q ↔ ∃ b : Base G, p = sectionLift n b ∧ q = b.toPres := by
  constructor
  · exact accepted_only_from_section n p q
  · rintro ⟨b, rfl, rfl⟩
    exact old_image_base n b

/-- Refusal is exactly "not a section image at this stage". -/
theorem nonDescent_iff_off_image (n : Nat) (p : Pres G) :
    retr n p = .nonDescent ↔ ∀ b : Base G, p ≠ sectionLift n b := by
  constructor
  · intro h b hp
    subst hp
    rw [old_image_base] at h
    cases h
  · intro h
    cases hr : retr n p with
    | accepted q =>
      obtain ⟨b, hb, _⟩ := accepted_only_from_section n p q hr
      exact absurd hb (h b)
    | nonDescent => rfl

/-! ### Bridge: the S(n) pair is a `SectionRetraction` of Part 1 -/

/-- Read an accepted presentation back as a base presentation. -/
def toBase : Pres G → Option (Base G)
  | .ground => some .ground
  | .supplied m => some (.supplied m)
  | .relation r => some (.relation r)
  | _ => none

theorem toBase_toPres (b : Base G) : toBase b.toPres = some b := by
  cases b <;> rfl

/-- The retraction with the outcome read as `Base G ⊕ Unit` (accepted payloads that are not base shapes
cannot occur, see `accepted_only_from_section`). -/
def retrB (n : Nat) (p : Pres G) : Base G ⊕ Unit :=
  match retr n p with
  | .accepted q => match toBase q with
    | some b => Sum.inl b
    | none => Sum.inr ()
  | .nonDescent => Sum.inr ()

/-- The pinned pair (restated) is a section/retraction pair in the sense of Part 1: law and soundness. -/
theorem sn_is_section_retraction (n : Nat) : SectionRetraction (sectionLift n : Base G → Pres G) (retrB n) := by
  constructor
  · intro b
    simp [retrB, old_image_base, toBase_toPres]
  · intro p b h
    unfold retrB at h
    cases hr : retr n p with
    | nonDescent => rw [hr] at h; cases h
    | accepted q =>
      obtain ⟨b0, hp, hq⟩ := accepted_only_from_section n p q hr
      rw [hr] at h
      simp only [hq, toBase_toPres] at h
      have : b0 = b := Sum.inl.inj h
      rw [← this, hp]

/-- Hence, for the S(n) pair, refusal (`retrB n p = inr ()`) is exactly "no base presentation lifts to `p`",
and the round trip `s (r p) = p` fails exactly there (Part 1 applied to the restated model). -/
theorem sn_refused_iff_off_image (n : Nat) (p : Pres G) :
    retrB n p = Sum.inr () ↔ ∀ b : Base G, sectionLift n b ≠ p :=
  refused_iff_off_image (sn_is_section_retraction n) p

/-- The stage carried by a lift. -/
def liftStage : Pres G → Option Nat
  | .lift l _ => some l
  | _ => none

theorem liftStage_sectionLift (m : Nat) (b : Base G) : liftStage (sectionLift m b) = some m := by
  cases b with
  | ground => rfl
  | supplied m' => rfl
  | relation r => cases r <;> rfl

/-- A section image at stage `m` is refused at any other stage `n`. -/
theorem retraction_stage_strict (n m : Nat) (b : Base G) (hm : m ≠ n) :
    retr n (sectionLift m b) = .nonDescent := by
  apply (nonDescent_iff_off_image n (sectionLift m b)).mpr
  intro b' hb
  apply hm
  have hst := congrArg liftStage hb
  rw [liftStage_sectionLift, liftStage_sectionLift] at hst
  injection hst

/-- The image test read off the outcome. -/
def inImage (n : Nat) (p : Pres G) : Bool :=
  match retr n p with
  | .accepted _ => true
  | .nonDescent => false

theorem inImage_iff (n : Nat) (p : Pres G) : inImage n p = true ↔ ∃ b : Base G, p = sectionLift n b := by
  unfold inImage
  cases hr : retr n p with
  | accepted q =>
    constructor
    · intro _
      obtain ⟨b, hb, _⟩ := accepted_only_from_section n p q hr
      exact ⟨b, hb⟩
    · intro _; rfl
  | nonDescent =>
    constructor
    · intro h; cases h
    · rintro ⟨b, hb⟩
      have := (nonDescent_iff_off_image n p).mp hr b
      exact absurd hb this

/-- A lax retraction that accepts everything the pinned one refuses (as the ground presentation) still obeys
the old-image law on the section image, yet it refuses nothing: the law is not the refusal.  (For every alphabet.) -/
def laxRetr (n : Nat) (p : Pres G) : Outcome G :=
  match retr n p with
  | .accepted q => .accepted q
  | .nonDescent => .accepted .ground

theorem lax_obeys_law (n : Nat) (b : Base G) : laxRetr n (sectionLift n b) = .accepted b.toPres := by
  simp [laxRetr, old_image_base]

theorem lax_never_refuses (n : Nat) (p : Pres G) : laxRetr n p ≠ .nonDescent := by
  unfold laxRetr
  cases retr n p <;> simp

/-- Hence for the lax retraction the refusal characterisation fails at every off-image point (here the
three-glyph body over any alphabet with a glyph is off the image; the instance uses `Bool`). -/
theorem lax_breaks_refusal_characterisation :
    ¬ ∀ p : Pres Bool, laxRetr 0 p = .nonDescent ↔ ∀ b : Base Bool, p ≠ sectionLift 0 b := by
  intro h
  have := (h (.lift 0 (.glyphs [true, true, true]))).mpr (by
    intro b hb
    cases b with
    | ground => cases hb
    | supplied m => cases hb
    | relation r => cases r <;> cases hb)
  exact lax_never_refuses 0 _ this

/-- Instance checks on `Bool` glyphs: a three-glyph body, a wrong stage, a non-lift and the refusal token are refused. -/
theorem instance_refusals :
    retr 2 (.lift 2 (.glyphs [true, false, true]) : Pres Bool) = .nonDescent ∧
    retr 2 (.lift 3 (.glyphs [true]) : Pres Bool) = .nonDescent ∧
    retr 2 (.supplied true : Pres Bool) = .nonDescent ∧
    retr 2 (.retraction 2 (.glyphs []) : Pres Bool) = .nonDescent ∧
    retr 2 (.nonDescent : Pres Bool) = .nonDescent ∧
    inImage 2 (.lift 2 (.glyphs [true, false, true]) : Pres Bool) = false := by
  decide

end SnOffImageRefusal

#print axioms SnOffImageRefusal.SectionRetraction.injective
#print axioms SnOffImageRefusal.refused_iff_off_image
#print axioms SnOffImageRefusal.roundtrip_iff_in_image
#print axioms SnOffImageRefusal.roundtrip_fails_off_image
#print axioms SnOffImageRefusal.refuseOffImage_isSectionRetraction
#print axioms SnOffImageRefusal.toy_refused_iff_odd
#print axioms SnOffImageRefusal.lax_retraction_obeys_law_but_accepts_off_image
#print axioms SnOffImageRefusal.sn_is_section_retraction
#print axioms SnOffImageRefusal.sn_refused_iff_off_image
#print axioms SnOffImageRefusal.sectionLift_injective
#print axioms SnOffImageRefusal.old_image_base
#print axioms SnOffImageRefusal.accepted_only_from_section
#print axioms SnOffImageRefusal.accepted_iff
#print axioms SnOffImageRefusal.nonDescent_iff_off_image
#print axioms SnOffImageRefusal.retraction_stage_strict
#print axioms SnOffImageRefusal.inImage_iff
#print axioms SnOffImageRefusal.lax_breaks_refusal_characterisation
#print axioms SnOffImageRefusal.instance_refusals
