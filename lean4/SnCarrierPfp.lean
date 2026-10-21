import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Sum
import Mathlib.Data.Fintype.Prod
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-!
# The S(n) base presentations, their section lift and retraction, and the declared carrier table

AuthorityEffect: None.  Scope: a self-contained re-statement of the pinned `SnCarrier` model of
`000_pre_genesis_to_mssn/lean4/SnCarrier.lean` (sha256 357376de...), with the glyph alphabet abstracted to an
arbitrary type `G` (the source alphabet has 36 glyphs) and the one-field wrapper structures flattened (the source
`GroundToken` and `NonDescent` each have a single value).  `Pres`, `Base`, `sectionLift` and `retr` mirror
`SnPresentation`, `BasePresentation`, `sectionLift` and `retractionDownMap`.  The source carries the assumption
`Classical.choice in old_image_base`; the re-proof here is separate and its axiom report is printed at the end.

What is established, for every alphabet `G`:
* `old_image_base`, `sectionLift_injective`: the old-image law on base presentations and injectivity of the lift;
* `unrestricted_lift_not_injective`, `no_recovery_for_unrestricted_lift`,
  `refusal_token_round_trip_changes_input`: the unrestricted lift (the pre-repair interface of the ledger row
  WDP-P001-019, reproduced here as a definition, since the source `SnCarrier` defines only the restricted one) has
  no recovery and sends the refusal token to the ground presentation;
* `card_base` : `|Base G| = 1 + g + 3 g^2` for `g = |G|`, and `card_image_sectionLift`: the image of the lift at
  every stage has that same cardinality;
* the declared table `carrierCard` and what it does not equal: `table_ne_base_stage_zero/two/three`,
  `table_eq_base_stage_one_iff`, `no_alphabet_matches_stages_one_two`, `ground_carrier_empty`.
The table is a declared definition (the source says "declared cardinalities for finite examples; not
source-derived stage counts") with no theorem tying `Carrier n` to `Base` or `sectionLift`; nothing here repairs
or endorses it.  Off-image refusal is in `SnOffImageRefusal.lean` (node PG-SN-OFF-IMAGE-REFUSAL).
-/

namespace SnCarrierPfp

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

/-- Section on base presentations. -/
def sectionLift (stage : Nat) : Base G → Pres G
  | .ground => .lift stage (.glyphs [])
  | .supplied m => .lift stage (.glyphs [m])
  | .relation (.pair f s) => .lift stage (.glyphs [f, s])
  | .relation (.cut a b) => .lift stage (.arrow a b)
  | .relation (.simplex a b) => .lift stage (.pair a b)

/-- Retraction down-map `r_N`. -/
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

/-- The old-image law on base presentations, at every stage and for every alphabet. -/
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

/-- The lift is injective (hence its image has the cardinality of `Base G`). -/
theorem sectionLift_injective (n : Nat) : Function.Injective (sectionLift n : Base G → Pres G) := by
  intro b b' h
  have h1 := old_image_base n b
  have h2 := old_image_base n b'
  rw [h] at h1
  rw [h1] at h2
  injection h2 with h3
  exact toPres_injective h3

/-! ### Unrestricted lift (the pre-repair interface of ledger row WDP-P001-019) -/

/-- Lift defined on every presentation; any presentation outside the five base shapes is sent to the empty
glyph body, as in `SnCarrierDischarge.unconstrainedSectionLift`. -/
def unrestrictedLift (stage : Nat) : Pres G → Pres G
  | .ground => .lift stage (.glyphs [])
  | .supplied m => .lift stage (.glyphs [m])
  | .relation (.pair f s) => .lift stage (.glyphs [f, s])
  | .relation (.cut a b) => .lift stage (.arrow a b)
  | .relation (.simplex a b) => .lift stage (.pair a b)
  | _ => .lift stage (.glyphs [])

theorem unrestricted_lift_not_injective (n : Nat) :
    ¬ Function.Injective (unrestrictedLift n : Pres G → Pres G) := by
  intro h
  have : (Pres.ground : Pres G) = Pres.nonDescent := h rfl
  cases this

/-- No recovery with the old-image law exists for the unrestricted lift. -/
theorem no_recovery_for_unrestricted_lift (n : Nat) {E : Type} :
    ¬ ∃ r : Pres G → Pres G ⊕ E, ∀ p, r (unrestrictedLift n p) = Sum.inl p := by
  rintro ⟨r, hr⟩
  apply unrestricted_lift_not_injective (G := G) n
  intro p q hpq
  have h1 : (Sum.inl p : Pres G ⊕ E) = Sum.inl q := by rw [← hr p, hpq, hr q]
  exact Sum.inl.inj h1

/-- The ledger defect: the refusal token, lifted and retracted at stage 0, comes back as the ground presentation. -/
theorem refusal_token_round_trip_changes_input :
    retr 0 (unrestrictedLift 0 (Pres.nonDescent : Pres G)) = .accepted .ground ∧
      retr 0 (unrestrictedLift 0 (Pres.nonDescent : Pres G)) ≠ .accepted .nonDescent := by
  refine ⟨by simp [unrestrictedLift, retr], ?_⟩
  simp [unrestrictedLift, retr]

/-! ### Carrier cardinalities -/

/-- Declared cardinalities of the source (a table; the source calls them declared, not derived). -/
def carrierCard : Nat → Nat
  | 0 => 0
  | 1 => 1
  | 2 => 2
  | 3 => 2
  | 4 => 4
  | 5 => 5
  | 6 => 6
  | n => n

abbrev Carrier (n : Nat) := Fin (carrierCard n)

theorem ground_carrier_empty (x : Carrier 0) : False := Fin.elim0 x

/-- `Base G` is the sum `1 + G + 3 (G x G)`. -/
def baseEquiv (G : Type) : Base G ≃ Unit ⊕ (G ⊕ ((G × G) ⊕ ((G × G) ⊕ (G × G)))) where
  toFun
    | .ground => .inl ()
    | .supplied m => .inr (.inl m)
    | .relation (.pair f s) => .inr (.inr (.inl (f, s)))
    | .relation (.cut a b) => .inr (.inr (.inr (.inl (a, b))))
    | .relation (.simplex a b) => .inr (.inr (.inr (.inr (a, b))))
  invFun
    | .inl _ => .ground
    | .inr (.inl m) => .supplied m
    | .inr (.inr (.inl (f, s))) => .relation (.pair f s)
    | .inr (.inr (.inr (.inl (a, b)))) => .relation (.cut a b)
    | .inr (.inr (.inr (.inr (a, b)))) => .relation (.simplex a b)
  left_inv := by
    intro b
    cases b with
    | ground => rfl
    | supplied m => rfl
    | relation r => cases r <;> rfl
  right_inv := by
    intro x
    rcases x with ⟨⟩ | m | ⟨f, s⟩ | ⟨a, b⟩ | ⟨a, b⟩ <;> rfl

instance [Fintype G] : Fintype (Base G) := Fintype.ofEquiv _ (baseEquiv G).symm

/-- Number of base presentations over an alphabet of `g` glyphs. -/
def baseCard (g : Nat) : Nat := 1 + g + 3 * g ^ 2

theorem card_base [Fintype G] : Fintype.card (Base G) = baseCard (Fintype.card G) := by
  rw [Fintype.card_congr (baseEquiv G)]
  simp only [Fintype.card_sum, Fintype.card_prod, Fintype.card_unit, baseCard]
  ring

/-- The image of the lift at every stage has the cardinality of `Base G`, independent of the stage. -/
theorem card_image_sectionLift [Fintype G] [DecidableEq G] (n : Nat) :
    (Finset.univ.image (sectionLift n : Base G → Pres G)).card = baseCard (Fintype.card G) := by
  rw [Finset.card_image_of_injective _ (sectionLift_injective n), Finset.card_univ, card_base]

theorem table_ne_base_stage_zero (g : Nat) : carrierCard 0 ≠ baseCard g := by
  simp only [carrierCard, baseCard]; omega

theorem table_ne_base_stage_two (g : Nat) : carrierCard 2 ≠ baseCard g := by
  simp only [carrierCard, baseCard]
  intro h
  rcases Nat.eq_zero_or_pos g with rfl | hg
  · simp at h
  · have h2 : 1 ≤ g ^ 2 := Nat.one_le_pow _ _ hg
    linarith

theorem table_ne_base_stage_three (g : Nat) : carrierCard 3 ≠ baseCard g := by
  simp only [carrierCard, baseCard]
  intro h
  rcases Nat.eq_zero_or_pos g with rfl | hg
  · simp at h
  · have h2 : 1 ≤ g ^ 2 := Nat.one_le_pow _ _ hg
    linarith

theorem table_eq_base_stage_one_iff (g : Nat) : carrierCard 1 = baseCard g ↔ g = 0 := by
  simp only [carrierCard, baseCard]
  constructor
  · intro h; nlinarith
  · intro h; subst h; rfl

/-- Per-shape counts (supplied `g`, pair `g^2`) cannot match the table entries at stages 1 and 2 together. -/
theorem no_alphabet_matches_stages_one_two (g : Nat) : ¬ (g = carrierCard 1 ∧ g ^ 2 = carrierCard 2) := by
  simp only [carrierCard]
  rintro ⟨h1, h2⟩
  subst h1
  omega

/-- Instance: over the 36-glyph alphabet of the source the lift image has 3925 points at every stage. -/
theorem baseCard_36 : baseCard 36 = 3925 := by decide

end SnCarrierPfp

#print axioms SnCarrierPfp.old_image_base
#print axioms SnCarrierPfp.sectionLift_injective
#print axioms SnCarrierPfp.unrestricted_lift_not_injective
#print axioms SnCarrierPfp.no_recovery_for_unrestricted_lift
#print axioms SnCarrierPfp.refusal_token_round_trip_changes_input
#print axioms SnCarrierPfp.ground_carrier_empty
#print axioms SnCarrierPfp.card_base
#print axioms SnCarrierPfp.card_image_sectionLift
#print axioms SnCarrierPfp.table_ne_base_stage_zero
#print axioms SnCarrierPfp.table_ne_base_stage_two
#print axioms SnCarrierPfp.table_ne_base_stage_three
#print axioms SnCarrierPfp.table_eq_base_stage_one_iff
#print axioms SnCarrierPfp.no_alphabet_matches_stages_one_two
#print axioms SnCarrierPfp.baseCard_36
