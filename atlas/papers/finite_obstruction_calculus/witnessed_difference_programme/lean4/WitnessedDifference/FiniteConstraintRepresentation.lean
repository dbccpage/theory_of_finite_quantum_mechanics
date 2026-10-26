import WitnessedDifference.FaithfulRepresentation

/-!
# Constructive constraint gluing and finite enumeration

The gluing theorem holds for arbitrary explicitly covered scopes. Finite
domains and row lists make its encoder, verifier, and enumeration effective.
The predicates below denote actual relation membership, not supplied solution
bits. No assumption of global solvability occurs in encoding or augmentation.
The Python parser/storage implementation is separately replay-tested.
-/
namespace WitnessedDifference.FiniteConstraintRepresentation

open FaithfulRepresentation

universe u v w

def Row {V : Type u} (A : Type v) (scope : V → Prop) := (x : V) → scope x → A

structure Network (V : Type u) (A : Type v) (I : Type w) where
  domain : V → A → Prop
  scope : I → V → Prop
  relation : (i : I) → Row A (scope i) → Prop

def Family {V : Type u} {A : Type v} {I : Type w} (N : Network V A I) :=
  (i : I) → Row A (N.scope i)

def restrict {V : Type u} {A : Type v} {I : Type w} (N : Network V A I)
    (x : V → A) : Family N := fun _ v _ => x v

def Global {V : Type u} {A : Type v} {I : Type w} (N : Network V A I) (x : V → A) : Prop :=
  (∀ v, N.domain v (x v)) ∧ ∀ i, N.relation i (restrict N x i)

def Local {V : Type u} {A : Type v} {I : Type w} (N : Network V A I) (f : Family N) : Prop :=
  ∀ i, N.relation i (f i) ∧ ∀ v h, N.domain v (f i v h)

def Compatible {V : Type u} {A : Type v} {I : Type w} (N : Network V A I) (f : Family N) : Prop :=
  ∀ i j v hi hj, f i v hi = f j v hj

abbrev Cover {V : Type u} {A : Type v} {I : Type w} (N : Network V A I) :=
  (v : V) → {i : I // N.scope i v}

def glue {V : Type u} {A : Type v} {I : Type w} {N : Network V A I}
    (cover : Cover N) (f : Family N) : V → A := fun v => f (cover v).val v (cover v).property

theorem restrict_compatible {V : Type u} {A : Type v} {I : Type w}
    (N : Network V A I) (x : V → A) : Compatible N (restrict N x) := by
  intro i j v hi hj
  rfl

theorem restrict_local {V : Type u} {A : Type v} {I : Type w}
    {N : Network V A I} {x : V → A} (h : Global N x) : Local N (restrict N x) := by
  intro i
  exact ⟨h.2 i, fun v _ => h.1 v⟩

theorem glue_restrict {V : Type u} {A : Type v} {I : Type w}
    {N : Network V A I} (cover : Cover N) (x : V → A) : glue cover (restrict N x) = x := rfl

theorem restrict_glue {V : Type u} {A : Type v} {I : Type w}
    {N : Network V A I} (cover : Cover N) {f : Family N} (h : Compatible N f) :
    restrict N (glue cover f) = f := by
  funext i v hi
  exact h (cover v).val i v (cover v).property hi

theorem glue_global {V : Type u} {A : Type v} {I : Type w}
    {N : Network V A I} (cover : Cover N) {f : Family N}
    (admitted : Local N f) (compatible : Compatible N f) : Global N (glue cover f) := by
  constructor
  · intro v
    exact (admitted (cover v).val).2 v (cover v).property
  · intro i
    rw [restrict_glue cover compatible]
    exact (admitted i).1

theorem unique_gluing {V : Type u} {A : Type v} {I : Type w}
    {N : Network V A I} (cover : Cover N) {f : Family N} {x y : V → A}
    (hx : restrict N x = f) (hy : restrict N y = f) : x = y := by
  have e := congrArg (glue cover) (hx.trans hy.symm)
  simpa [glue_restrict] using e

def witnessSystem {V : Type u} {A : Type v} {I : Type w}
    (N : Network V A I) (cover : Cover N) : System (V → A) where
  Witness := Family N
  accepts := fun f => Local N f ∧ Compatible N f
  decode := glue cover

theorem concrete_system_sound {V : Type u} {A : Type v} {I : Type w}
    (N : Network V A I) (cover : Cover N) : Sound (Global N) (witnessSystem N cover) := by
  intro f hf
  exact glue_global cover hf.1 hf.2

def concrete_system_coverage {V : Type u} {A : Type v} {I : Type w}
    (N : Network V A I) (cover : Cover N) : Coverage (Global N) (witnessSystem N cover) where
  lift := restrict N
  valid := fun x hx => ⟨restrict_local hx, restrict_compatible N x⟩
  recovers := fun x _ => glue_restrict cover x

theorem concrete_solution_iff_certificate {V : Type u} {A : Type v} {I : Type w}
    (N : Network V A I) (cover : Cover N) :
    (∃ x, Global N x) ↔ ∃ f, Local N f ∧ Compatible N f := by
  exact solution_iff_certificate (concrete_system_sound N cover)
    (concrete_system_coverage N cover) (History.nil (witnessSystem N cover))

theorem concrete_history_sound {V : Type u} {A : Type v} {I : Type w}
    (N : Network V A I) (cover : Cover N) {T : System (V → A)}
    (history : History (witnessSystem N cover) T) : Sound (Global N) T :=
  every_history_sound (concrete_system_sound N cover) history

theorem concrete_history_solution_iff {V : Type u} {A : Type v} {I : Type w}
    (N : Network V A I) (cover : Cover N) {T : System (V → A)}
    (history : History (witnessSystem N cover) T) :
    (∃ x, Global N x) ↔ ∃ w, T.accepts w :=
  solution_iff_certificate (concrete_system_sound N cover) (concrete_system_coverage N cover) history

def indicator {A : Type u} [DecidableEq A] (value test : A) : Int := if value = test then 1 else 0

theorem indicator_difference_zero_iff {A : Type u} [DecidableEq A] (x y : A) :
    (∀ a, indicator x a - indicator y a = 0) ↔ x = y := by
  constructor
  · intro h
    by_cases he : x = y
    · exact he
    · have bad := h x
      have hy : y ≠ x := fun e => he e.symm
      simp [indicator, hy] at bad
  · intro h
    subst y
    intro a
    simp

def ZeroDefect {V : Type u} {A : Type v} {I : Type w} [DecidableEq A]
    {N : Network V A I} (cover : Cover N) (f : Family N) : Prop :=
  ∀ i v hi a, indicator (f i v hi) a - indicator (glue cover f v) a = 0

theorem zero_defect_iff_compatible {V : Type u} {A : Type v} {I : Type w} [DecidableEq A]
    {N : Network V A I} (cover : Cover N) (f : Family N) :
    ZeroDefect cover f ↔ Compatible N f := by
  constructor
  · intro h i j v hi hj
    have left := (indicator_difference_zero_iff (f i v hi) (glue cover f v)).mp (h i v hi)
    have right := (indicator_difference_zero_iff (f j v hj) (glue cover f v)).mp (h j v hj)
    exact left.trans right.symm
  · intro h i v hi a
    have eq := h i (cover v).val v hi (cover v).property
    change indicator (f i v hi) a - indicator (f (cover v).val v (cover v).property) a = 0
    rw [eq]
    simp

/-- Add a unary domain row exactly at variables lacking any original occurrence. -/
def AugIndex {V : Type u} {A : Type v} {I : Type w} (N : Network V A I) :=
  Sum I {v : V // ∀ i, ¬N.scope i v}

def augment {V : Type u} {A : Type v} {I : Type w} (N : Network V A I) : Network V A (AugIndex N) where
  domain := N.domain
  scope := fun i => match i with
    | .inl j => N.scope j
    | .inr v => fun x => x = v.val
  relation := fun i => match i with
    | .inl j => N.relation j
    | .inr _ => fun _ => True

noncomputable def augmented_cover {V : Type u} {A : Type v} {I : Type w}
    (N : Network V A I) : Cover (augment N) := by
  classical
  intro v
  by_cases h : ∃ i, N.scope i v
  · exact ⟨.inl (Classical.choose h), Classical.choose_spec h⟩
  · exact ⟨.inr ⟨v, fun i hi => h ⟨i, hi⟩⟩, rfl⟩

theorem augmentation_preserves_original_goal {V : Type u} {A : Type v} {I : Type w}
    (N : Network V A I) (x : V → A) : Global (augment N) x ↔ Global N x := by
  constructor
  · intro h
    exact ⟨h.1, fun i => h.2 (.inl i)⟩
  · intro h
    refine ⟨h.1, ?_⟩
    intro i
    cases i with
    | inl j => exact h.2 j
    | inr v => trivial

theorem arbitrary_network_faithful {V : Type u} {A : Type v} {I : Type w}
    (N : Network V A I) :
    (∃ x, Global N x) ↔ ∃ f, Local (augment N) f ∧ Compatible (augment N) f := by
  have h := concrete_solution_iff_certificate (augment N) (augmented_cover N)
  constructor
  · rintro ⟨x, hx⟩
    exact h.mp ⟨x, (augmentation_preserves_original_goal N x).mpr hx⟩
  · intro hf
    obtain ⟨x, hx⟩ := h.mpr hf
    exact ⟨x, (augmentation_preserves_original_goal N x).mp hx⟩

def cartesian {A : Type u} : List (List A) → List (List A)
  | [] => [[]]
  | row :: rows => row.flatMap (fun x => (cartesian rows).map (fun xs => x :: xs))

def Choices {A : Type u} : List (List A) → List A → Prop
  | [], [] => True
  | row :: rows, x :: xs => x ∈ row ∧ Choices rows xs
  | _, _ => False

theorem cartesian_exact {A : Type u} (rows : List (List A)) (xs : List A) :
    xs ∈ cartesian rows ↔ Choices rows xs := by
  induction rows generalizing xs with
  | nil => cases xs <;> simp [cartesian, Choices]
  | cons row rows ih =>
    cases xs with
    | nil => simp [cartesian, Choices, List.mem_flatMap, List.mem_map]
    | cons x xs =>
      simp [cartesian, Choices, List.mem_flatMap, List.mem_map, ih]

theorem cartesian_empty_domain {A : Type u} (rows : List (List A)) :
    cartesian ([] :: rows) = [] := by simp [cartesian]

/-- Exact finite exhaustion checks the constructed product, not supplied solution bits. -/
theorem constructed_exhaustion {A : Type u} (rows : List (List A)) (accept : List A → Bool)
    (h : scan accept (cartesian rows) = none) : ∀ xs, Choices rows xs → accept xs = false := by
  intro xs hx
  exact (scan_none_iff accept (cartesian rows)).mp h xs ((cartesian_exact rows xs).mpr hx)

/-- A bijective value/variable recoding reduces to this checked inverse law. -/
theorem rename_predicate_iff {X Y : Type u} (good : X → Prop) (forth : X → Y) (back : Y → X)
    (inverse : ∀ x, back (forth x) = x) (x : X) : good (back (forth x)) ↔ good x := by
  rw [inverse]

def Joined {X L R : Type u} (left : L → Prop) (right : R → Prop)
    (pl : X → L) (pr : X → R) (x : X) : Prop := left (pl x) ∧ right (pr x)

theorem join_exact {X L R : Type u} (left : L → Prop) (right : R → Prop)
    (pl : X → L) (pr : X → R) (x : X) :
    Joined left right pl pr x ↔ left (pl x) ∧ right (pr x) := Iff.rfl

def Projected {X Y : Type u} (relation : X → Prop) (p : X → Y) (y : Y) : Prop :=
  ∃ x, relation x ∧ p x = y

theorem projection_join_contains_original {X L R : Type u} (relation : X → Prop)
    (pl : X → L) (pr : X → R) {x : X} (h : relation x) :
    Joined (Projected relation pl) (Projected relation pr) pl pr x := by
  exact ⟨⟨x, h, rfl⟩, ⟨x, h, rfl⟩⟩

theorem lossless_split_iff_no_spurious {X L R : Type u} (relation : X → Prop)
    (pl : X → L) (pr : X → R) :
    (∀ x, Joined (Projected relation pl) (Projected relation pr) pl pr x ↔ relation x) ↔
    (∀ x, Joined (Projected relation pl) (Projected relation pr) pl pr x → relation x) := by
  constructor
  · exact fun h x => (h x).mp
  · intro h x
    exact ⟨h x, projection_join_contains_original relation pl pr⟩

def Auxiliary {X Y : Type u} (good : X → Prop) (f : X → Y) (pair : X × Y) : Prop :=
  good pair.1 ∧ pair.2 = f pair.1

theorem auxiliary_forward {X Y : Type u} {good : X → Prop} (f : X → Y) {x : X}
    (h : good x) : Auxiliary good f (x, f x) := ⟨h, rfl⟩

theorem auxiliary_backward {X Y : Type u} {good : X → Prop} {f : X → Y} {pair : X × Y}
    (h : Auxiliary good f pair) : good pair.1 := h.1

theorem auxiliary_roundtrip {X Y : Type u} {good : X → Prop} {f : X → Y} {pair : X × Y}
    (h : Auxiliary good f pair) : (pair.1, f pair.1) = pair := by
  cases pair with
  | mk x y => simpa only [Prod.mk.injEq, true_and] using h.2.symm

/-- Empty domains are unsatisfiable even when their variables occur nowhere. -/
theorem empty_domain_refutes {V : Type u} {A : Type v} {I : Type w}
    (N : Network V A I) (v : V) (empty : ∀ a, ¬N.domain v a) : ¬∃ x, Global N x := by
  rintro ⟨x, hx⟩
  exact empty (x v) (hx.1 v)

theorem empty_relation_refutes {V : Type u} {A : Type v} {I : Type w}
    (N : Network V A I) (i : I) (empty : ∀ row, ¬N.relation i row) : ¬∃ x, Global N x := by
  rintro ⟨x, hx⟩
  exact empty _ (hx.2 i)

end WitnessedDifference.FiniteConstraintRepresentation

#print axioms WitnessedDifference.FiniteConstraintRepresentation.restrict_compatible
#print axioms WitnessedDifference.FiniteConstraintRepresentation.restrict_local
#print axioms WitnessedDifference.FiniteConstraintRepresentation.glue_restrict
#print axioms WitnessedDifference.FiniteConstraintRepresentation.restrict_glue
#print axioms WitnessedDifference.FiniteConstraintRepresentation.glue_global
#print axioms WitnessedDifference.FiniteConstraintRepresentation.unique_gluing
#print axioms WitnessedDifference.FiniteConstraintRepresentation.concrete_system_sound
#print axioms WitnessedDifference.FiniteConstraintRepresentation.concrete_solution_iff_certificate
#print axioms WitnessedDifference.FiniteConstraintRepresentation.concrete_history_sound
#print axioms WitnessedDifference.FiniteConstraintRepresentation.concrete_history_solution_iff
#print axioms WitnessedDifference.FiniteConstraintRepresentation.indicator_difference_zero_iff
#print axioms WitnessedDifference.FiniteConstraintRepresentation.zero_defect_iff_compatible
#print axioms WitnessedDifference.FiniteConstraintRepresentation.augmentation_preserves_original_goal
#print axioms WitnessedDifference.FiniteConstraintRepresentation.arbitrary_network_faithful
#print axioms WitnessedDifference.FiniteConstraintRepresentation.cartesian_exact
#print axioms WitnessedDifference.FiniteConstraintRepresentation.cartesian_empty_domain
#print axioms WitnessedDifference.FiniteConstraintRepresentation.constructed_exhaustion
#print axioms WitnessedDifference.FiniteConstraintRepresentation.rename_predicate_iff
#print axioms WitnessedDifference.FiniteConstraintRepresentation.join_exact
#print axioms WitnessedDifference.FiniteConstraintRepresentation.projection_join_contains_original
#print axioms WitnessedDifference.FiniteConstraintRepresentation.lossless_split_iff_no_spurious
#print axioms WitnessedDifference.FiniteConstraintRepresentation.auxiliary_forward
#print axioms WitnessedDifference.FiniteConstraintRepresentation.auxiliary_backward
#print axioms WitnessedDifference.FiniteConstraintRepresentation.auxiliary_roundtrip
#print axioms WitnessedDifference.FiniteConstraintRepresentation.empty_domain_refutes
#print axioms WitnessedDifference.FiniteConstraintRepresentation.empty_relation_refutes
