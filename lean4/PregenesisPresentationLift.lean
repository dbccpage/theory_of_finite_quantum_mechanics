import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Finset.Card
import Mathlib.Logic.Function.Basic

/-!
# PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT

Target: PGW-PRESENTATION-NOT-EXPRESSIVE-LIFT (TFQ-0422)
Stage: PREGENESIS
Outcome: Narrowed. Model-level only: the distinction map q is the constant empty map by definition (emptyDistinctions), so O = empty, q non-injective and the opaque/exact comparison are properties of that definition on a two-inscription type, not derived from an observation family; the node stays CONDITIONAL (PR 185 review).

Mathematical Statement:
"Write P for the presented inscriptions and O for the internal observations.
Supplying <a> after <> changes P from {<>} to {<a>} and leaves O_1 = O_0 = ∅,
so no new internal distinction is available. With q : P → N sending an
inscription to the distinctions the regime has, x ≠ y in P can hold while
q(x) = q(y) in N, so a new presentation does not imply a new internal class,
and in the other direction q(x) = q(y) does not imply x = y. Under the opaque
convention <a> is a new presentation state in the same internal class as <>;
the statement holds under that convention only."

This module formalizes:
1. `Inscription`: The syntactic inscriptions `<>` (`nil`) and `<a>` (`markA`),
   with `nil ≠ markA` and card(P) = 2.
2. Presentation states `P0` (initial `{<>}`) and `P1` (after supply `{<>, <a>}`),
   showing strict enlargement `P0 ⊂ P1`.
3. Internal observations `O0` and `O1` in the unformed regime, proving
   `O0 = ∅`, `O1 = ∅`, `O1 = O0`, and difference `O1 \ O0 = ∅`.
4. The distinction map `q : P → N`, proving non-injectivity:
   `∃ x y, x ≠ y ∧ q x = q y`.
5. The non-implications:
   - A new presentation does not imply a new internal class:
     `¬ (∀ x y, x ≠ y → q x ≠ q y)`.
   - Equal internal class does not imply identical presentation:
     `¬ (∀ x y, q x = q y → x = y)`.
6. Identity conventions:
   - `IdentityConvention`: `opaqueConv` vs `exactInscription`.
   - Under `opaqueConv`, `nil` and `markA` collapse into the same internal class.
   - Under `exactInscription`, `nil` and `markA` remain strictly distinct.
7. Convention characterization:
   The existence of distinct inscriptions sharing an internal class holds if
   and only if the identity convention is `opaqueConv` ("holds under that
   convention only").
8. Quotient cardinality: Under the opaque convention, the image has cardinality 1,
   while under exact-inscription, the presentation retains cardinality 2.
9. Constructive unformed regime collapse: Two data marks in an unformed regime
   have no separating unary forms and are collapsed.
-/

namespace PregenesisPresentationLift

/-! ## 1. Presentation Inscriptions -/

/-- Syntactic inscriptions presented to the regime: `<>` (`nil`) and `<a>` (`markA`). -/
inductive Inscription
  | nil
  | markA
  deriving DecidableEq, Repr

instance : Fintype Inscription :=
  ⟨⟨[Inscription.nil, Inscription.markA], by decide⟩, by intro x; cases x <;> decide⟩

@[simp] theorem inscription_card : Fintype.card Inscription = 2 := rfl

theorem nil_ne_markA : Inscription.nil ≠ Inscription.markA := by
  intro h; contradiction

theorem markA_ne_nil : Inscription.markA ≠ Inscription.nil := by
  intro h; contradiction

/-! ## 2. Presentation Sets: Initial vs After Supply -/

/-- Initial presentation set P0 containing only `<>`. -/
def P0 : Finset Inscription := {Inscription.nil}

/-- Presentation set P1 after supplying `<a>`, containing `<>` and `<a>`. -/
def P1 : Finset Inscription := {Inscription.nil, Inscription.markA}

@[simp] theorem P0_card : P0.card = 1 := rfl

@[simp] theorem P1_card : P1.card = 2 := rfl

theorem markA_not_in_P0 : Inscription.markA ∉ P0 := by
  simp [P0]

theorem markA_in_P1 : Inscription.markA ∈ P1 := by
  simp [P1]

theorem P0_subset_P1 : P0 ⊆ P1 := by
  intro x hx
  simp [P0] at hx
  subst hx
  simp [P1]

theorem P0_ssubset_P1 : P0 ⊂ P1 := by
  refine Finset.ssubset_iff_subset_ne.mpr ⟨P0_subset_P1, ?_⟩
  intro heq
  have h1 : Inscription.markA ∈ P1 := markA_in_P1
  have h2 : Inscription.markA ∉ P0 := markA_not_in_P0
  rw [← heq] at h1
  exact h2 h1

/-! ## 3. Internal Observations and Distinctions -/

/-- Distinction set: a finite set of internal distinction / form IDs. -/
abbrev Distinctions := Finset Nat

/-- Internal observation function in the unformed regime:
every inscription is associated with the empty distinction set. -/
def emptyDistinctions (_ : Inscription) : Distinctions := ∅

/-- Internal observations for `<>`. -/
def O0 : Distinctions := emptyDistinctions Inscription.nil

/-- Internal observations for `<a>`. -/
def O1 : Distinctions := emptyDistinctions Inscription.markA

@[simp] theorem O0_empty : O0 = ∅ := rfl

@[simp] theorem O1_empty : O1 = ∅ := rfl

theorem O1_eq_O0 : O1 = O0 := rfl

/-- No new internal distinction is available after supplying `<a>`. -/
theorem no_new_internal_distinction : O1 \ O0 = ∅ := by
  change (∅ : Distinctions) \ ∅ = ∅
  exact Finset.sdiff_self ∅

/-! ## 4. The Distinction Quotient Map q : P → N -/

/-- The distinction map `q` sending each presented inscription to its distinctions. -/
def q : Inscription → Distinctions := emptyDistinctions

/-- Non-injectivity witness: `<>` and `<a>` are distinct presentations with identical image. -/
theorem q_non_injective_witness :
    Inscription.nil ≠ Inscription.markA ∧ q Inscription.nil = q Inscription.markA :=
  ⟨nil_ne_markA, rfl⟩

/-- x ≠ y can hold while q(x) = q(y). -/
theorem exists_distinct_presentations_same_class :
    ∃ x y : Inscription, x ≠ y ∧ q x = q y :=
  ⟨Inscription.nil, Inscription.markA, q_non_injective_witness⟩

/-- A new presentation does not imply a new internal class. -/
theorem new_presentation_not_implies_new_internal_class :
    ¬ (∀ x y : Inscription, x ≠ y → q x ≠ q y) := by
  intro h
  have hne := h Inscription.nil Inscription.markA nil_ne_markA
  exact hne rfl

/-- In the other direction, identical internal distinction does not imply identical presentation. -/
theorem same_internal_class_not_implies_same_presentation :
    ¬ (∀ x y : Inscription, q x = q y → x = y) := by
  intro h
  have heq : Inscription.nil = Inscription.markA := h Inscription.nil Inscription.markA rfl
  exact nil_ne_markA heq

/-- General algebraic non-injectivity principle for arbitrary types P and N. -/
theorem general_non_injectivity_consequences {P N : Type} (map : P → N)
    (x y : P) (hne : x ≠ y) (heq : map x = map y) :
    (¬ ∀ a b : P, a ≠ b → map a ≠ map b) ∧ (¬ ∀ a b : P, map a = map b → a = b) := by
  constructor
  · intro h; exact (h x y hne) heq
  · intro h; exact hne (h x y heq)

/-! ## 5. Identity Conventions -/

/-- The declared identity convention: opaque vs exact-inscription. -/
inductive IdentityConvention
  | opaqueConv
  | exactInscription
  deriving DecidableEq, Repr

/-- Equivalence relation on presentations under a given identity convention and observation map. -/
def ConvEquiv (c : IdentityConvention) (obs : Inscription → Distinctions) (x y : Inscription) : Prop :=
  match c with
  | .opaqueConv => obs x = obs y
  | .exactInscription => x = y

instance (c : IdentityConvention) (obs : Inscription → Distinctions) :
    DecidableRel (ConvEquiv c obs) := by
  intro x y
  cases c with
  | opaqueConv =>
    dsimp [ConvEquiv]
    infer_instance
  | exactInscription =>
    dsimp [ConvEquiv]
    infer_instance

theorem convEquiv_refl (c : IdentityConvention) (obs : Inscription → Distinctions) (x : Inscription) :
    ConvEquiv c obs x x := by
  cases c <;> simp [ConvEquiv]

theorem convEquiv_symm (c : IdentityConvention) (obs : Inscription → Distinctions) {x y : Inscription} :
    ConvEquiv c obs x y → ConvEquiv c obs y x := by
  cases c
  · intro h; exact h.symm
  · intro h; exact h.symm

theorem convEquiv_trans (c : IdentityConvention) (obs : Inscription → Distinctions) {x y z : Inscription} :
    ConvEquiv c obs x y → ConvEquiv c obs y z → ConvEquiv c obs x z := by
  cases c
  · intro h1 h2; exact h1.trans h2
  · intro h1 h2; exact h1.trans h2

/-! ## 6. Behavior Under Opaque vs Exact Conventions -/

/-- Under the opaque convention, `<>` and `<a>` are in the same internal class. -/
theorem opaque_nil_markA_equiv :
    ConvEquiv IdentityConvention.opaqueConv emptyDistinctions Inscription.nil Inscription.markA :=
  rfl

/-- Under the exact-inscription convention, `<>` and `<a>` are NOT in the same class. -/
theorem exact_nil_markA_not_equiv :
    ¬ ConvEquiv IdentityConvention.exactInscription emptyDistinctions Inscription.nil Inscription.markA :=
  nil_ne_markA

/-- Under exact-inscription, every internal equivalence implies syntactic equality. -/
theorem exact_convention_injective (obs : Inscription → Distinctions) (x y : Inscription) :
    ConvEquiv IdentityConvention.exactInscription obs x y → x = y := by
  intro h; exact h

/-- Predicate: Does the convention permit distinct presentations in the same internal class? -/
def HasCollapsingPresentations (c : IdentityConvention) (obs : Inscription → Distinctions) : Prop :=
  ∃ x y : Inscription, x ≠ y ∧ ConvEquiv c obs x y

/-- Under the opaque convention, collapsing presentations exist. -/
theorem holds_under_opaque :
    HasCollapsingPresentations IdentityConvention.opaqueConv emptyDistinctions :=
  ⟨Inscription.nil, Inscription.markA, nil_ne_markA, rfl⟩

/-- Under the exact-inscription convention, collapsing presentations DO NOT exist. -/
theorem fails_under_exact :
    ¬ HasCollapsingPresentations IdentityConvention.exactInscription emptyDistinctions := by
  intro ⟨x, y, hne, heq⟩
  exact hne heq

/-- Main theorem: The statement holds under the opaque convention only. -/
theorem statement_holds_under_opaque_only (c : IdentityConvention) :
    HasCollapsingPresentations c emptyDistinctions ↔ c = IdentityConvention.opaqueConv := by
  constructor
  · intro h
    cases c with
    | opaqueConv => rfl
    | exactInscription => exact (fails_under_exact h).elim
  · intro h
    subst h
    exact holds_under_opaque

/-! ## 7. Quotient Cardinality -/

/-- Under the opaque convention, the image of presentations under `q` has cardinality 1. -/
theorem opaque_quotient_card :
    (Finset.univ.image emptyDistinctions).card = 1 := by
  have : (Finset.univ.image emptyDistinctions : Finset Distinctions) = {∅} := by
    ext s
    simp only [Finset.mem_image, Finset.mem_univ, true_and, Finset.mem_singleton]
    constructor
    · rintro ⟨a, rfl⟩; rfl
    · rintro rfl; exact ⟨Inscription.nil, rfl⟩
  rw [this]
  rfl

/-- Under exact-inscription, presentations retain cardinality 2. -/
theorem exact_presentation_card :
    (Finset.univ.image (fun (x : Inscription) => x)).card = 2 := by
  have : (Finset.univ.image (fun (x : Inscription) => x) : Finset Inscription) = Finset.univ := by
    simp
  rw [this]
  exact inscription_card

/-- Collapse ratio: 2 presented inscriptions collapse to 1 internal class under opaque convention. -/
theorem opaque_collapse_card_ratio :
    Fintype.card Inscription = 2 ∧ (Finset.univ.image emptyDistinctions).card = 1 :=
  ⟨inscription_card, opaque_quotient_card⟩

/-! ## 8. Constructive Genesis Unformed Regime -/

/-- A minimal Genesis regime representation. -/
structure Regime where
  data  : Nat
  forms : List Nat
  insts : List (Nat × List Nat)
  rules : List Nat
  reqs  : List (Nat × Nat)
  deriving Repr, DecidableEq

/-- The unformed regime on `n` data marks: no forms, instances, rules, or requirements. -/
def unformedRegime (n : Nat) : Regime :=
  ⟨n, [], [], [], []⟩

/-- Datum `i` is separated from `j` by a unary form instance. -/
def UnarySep (r : Regime) (i j : Nat) : Prop :=
  ∃ f, f < r.forms.length ∧ r.forms.getD f 0 = 1 ∧
    (((f, [i]) ∈ r.insts ∧ (f, [j]) ∉ r.insts) ∨ ((f, [j]) ∈ r.insts ∧ (f, [i]) ∉ r.insts))

/-- Two data marks are collapsed when neither is separated from the other. -/
def Collapsed (r : Regime) (i j : Nat) : Prop :=
  ¬ UnarySep r i j ∧ ¬ UnarySep r j i

/-- In an unformed regime, no unary separation exists because there are no forms. -/
theorem unformed_not_unarySep (n i j : Nat) :
    ¬ UnarySep (unformedRegime n) i j := by
  intro ⟨f, hf, _, _⟩
  dsimp [unformedRegime] at hf
  cases hf

/-- Constructive collapse theorem: Two marks in an unformed regime are collapsed. -/
theorem two_marks_in_unformed_regime_collapsed :
    Collapsed (unformedRegime 2) 0 1 := by
  constructor
  · exact unformed_not_unarySep 2 0 1
  · exact unformed_not_unarySep 2 1 0

end PregenesisPresentationLift

/-! ## Axiom Audits -/

#print axioms PregenesisPresentationLift.inscription_card
#print axioms PregenesisPresentationLift.nil_ne_markA
#print axioms PregenesisPresentationLift.P0_ssubset_P1
#print axioms PregenesisPresentationLift.no_new_internal_distinction
#print axioms PregenesisPresentationLift.q_non_injective_witness
#print axioms PregenesisPresentationLift.exists_distinct_presentations_same_class
#print axioms PregenesisPresentationLift.new_presentation_not_implies_new_internal_class
#print axioms PregenesisPresentationLift.same_internal_class_not_implies_same_presentation
#print axioms PregenesisPresentationLift.general_non_injectivity_consequences
#print axioms PregenesisPresentationLift.opaque_nil_markA_equiv
#print axioms PregenesisPresentationLift.exact_nil_markA_not_equiv
#print axioms PregenesisPresentationLift.holds_under_opaque
#print axioms PregenesisPresentationLift.fails_under_exact
#print axioms PregenesisPresentationLift.statement_holds_under_opaque_only
#print axioms PregenesisPresentationLift.opaque_quotient_card
#print axioms PregenesisPresentationLift.exact_presentation_card
#print axioms PregenesisPresentationLift.two_marks_in_unformed_regime_collapsed
