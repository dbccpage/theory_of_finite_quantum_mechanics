/-!
# Actual one-instance contexts and persistent separation floor

Source contexts contain a hole, plugging replaces every hole by one datum,
and a one-instance, rule-free form is derivable exactly at its admitted tuple.
The carrier is any type with decidable equality. The finite source carrier
specializes it to Fin n. A datum's profile is inhabited iff the tuple mentions
it; two distinct mentioned profiles have no shared context. Hence requirements
are separated exactly when the tuple's mentioned data cover their edges.

This proves the context/cover criterion at all finite arities, not merely the
initial two-datum fixture. The written derivation classifies all two-item
deltas from a no-form regime and identifies minimum arity with minimum cover
size. Neither the token convention nor a positive profile admits irreflexivity.
Concrete Python/Rust programs and vertex-cover optimization are not verified here.
-/
namespace WitnessedDifference.PrimitiveContextFloor

universe u
variable {V : Type u} [DecidableEq V]

def plug (d : V) : List (Option V) → List V
  | [] => []
  | slot :: rest => slot.getD d :: plug d rest

def Recognizes (tuple : List V) (d : V) (context : List (Option V)) : Prop :=
  none ∈ context ∧ plug d context = tuple

def mask (d : V) : List V → List (Option V)
  | [] => []
  | x :: rest => (if x=d then none else some x) :: mask d rest

theorem mask_plugs_to_tuple (d : V) (tuple : List V) : plug d (mask d tuple) = tuple := by
  induction tuple with
  | nil => rfl
  | cons x rest ih =>
    by_cases same : x=d
    · simp [mask,plug,same,ih]
    · simp [mask,plug,same,ih]

theorem mask_has_hole_of_mentioned (d : V) (tuple : List V) (mentioned : d ∈ tuple) :
    none ∈ mask d tuple := by
  induction tuple with
  | nil => simp at mentioned
  | cons x rest ih =>
    simp only [List.mem_cons] at mentioned
    rcases mentioned with same | later
    · subst x
      simp [mask]
    · exact List.mem_cons_of_mem _ (ih later)

omit [DecidableEq V] in
theorem hole_plugs_to_mentioned (d : V) (context : List (Option V)) (hole : none ∈ context) :
    d ∈ plug d context := by
  induction context with
  | nil => simp at hole
  | cons slot rest ih =>
    cases slot with
    | none => simp [plug]
    | some x =>
      have later : none ∈ rest := by simpa using hole
      exact List.mem_cons_of_mem _ (ih later)

omit [DecidableEq V] in
theorem recognized_implies_mentioned (tuple : List V) (d : V) (context : List (Option V))
    (recognized : Recognizes tuple d context) : d ∈ tuple := by
  rw [← recognized.2]
  exact hole_plugs_to_mentioned d context recognized.1

theorem profile_inhabited_iff_mentioned (tuple : List V) (d : V) :
    (∃ context, Recognizes tuple d context) ↔ d ∈ tuple := by
  constructor
  · rintro ⟨context,recognized⟩
    exact recognized_implies_mentioned tuple d context recognized
  · intro mentioned
    exact ⟨mask d tuple,mask_has_hole_of_mentioned d tuple mentioned,mask_plugs_to_tuple d tuple⟩

omit [DecidableEq V] in
theorem hole_reflects_datum_equality (a b : V) (context : List (Option V))
    (hole : none ∈ context) (same : plug a context = plug b context) : a=b := by
  induction context with
  | nil => simp at hole
  | cons slot rest ih =>
    cases slot with
    | none => exact (List.cons.inj same).1
    | some x =>
      have later : none ∈ rest := by simpa using hole
      exact ih later (List.cons.inj same).2

omit [DecidableEq V] in
theorem common_recognition_reflects_equality (tuple : List V) (a b : V) (context : List (Option V))
    (ra : Recognizes tuple a context) (rb : Recognizes tuple b context) : a=b := by
  exact hole_reflects_datum_equality a b context ra.1 (ra.2.trans rb.2.symm)

def Apart (tuple : List V) (a b : V) : Prop :=
  ∃ context, (Recognizes tuple a context ∧ ¬ Recognizes tuple b context) ∨
    (Recognizes tuple b context ∧ ¬ Recognizes tuple a context)

theorem one_instance_separates_iff_touches (tuple : List V) (a b : V) (distinct : a≠b) :
    Apart tuple a b ↔ a ∈ tuple ∨ b ∈ tuple := by
  constructor
  · rintro ⟨context,ha|hb⟩
    · exact Or.inl (recognized_implies_mentioned tuple a context ha.1)
    · exact Or.inr (recognized_implies_mentioned tuple b context hb.1)
  · intro touched
    rcases touched with ha | hb
    · obtain ⟨context,ra⟩ := (profile_inhabited_iff_mentioned tuple a).mpr ha
      refine ⟨context,Or.inl ⟨ra,?_⟩⟩
      intro rb
      exact distinct (common_recognition_reflects_equality tuple a b context ra rb)
    · obtain ⟨context,rb⟩ := (profile_inhabited_iff_mentioned tuple b).mpr hb
      refine ⟨context,Or.inr ⟨rb,?_⟩⟩
      intro ra
      exact distinct (common_recognition_reflects_equality tuple a b context ra rb)

def Separates (tuple : List V) (requirements : List (V×V)) : Prop :=
  ∀ a b, (a,b) ∈ requirements → Apart tuple a b

def Covers (tuple : List V) (requirements : List (V×V)) : Prop :=
  ∀ a b, (a,b) ∈ requirements → a ∈ tuple ∨ b ∈ tuple

theorem persistent_separation_iff_requirement_cover (tuple : List V) (requirements : List (V×V))
    (proper : ∀ a b, (a,b) ∈ requirements → a≠b) :
    Separates tuple requirements ↔ Covers tuple requirements := by
  constructor
  · intro separated a b edge
    exact (one_instance_separates_iff_touches tuple a b (proper a b edge)).mp (separated a b edge)
  · intro covered a b edge
    exact (one_instance_separates_iff_touches tuple a b (proper a b edge)).mpr (covered a b edge)

theorem empty_tuple_separates_no_distinct_pair (a b : V) (distinct : a≠b) :
    ¬ Apart [] a b := by
  rw [one_instance_separates_iff_touches [] a b distinct]
  simp

theorem unary_witness_only_separates_pairs_touching_its_datum (d a b : V) (distinct : a≠b) :
    Apart [d] a b ↔ a=d ∨ b=d := by
  simpa using one_instance_separates_iff_touches [d] a b distinct

end WitnessedDifference.PrimitiveContextFloor

#print axioms WitnessedDifference.PrimitiveContextFloor.mask_plugs_to_tuple
#print axioms WitnessedDifference.PrimitiveContextFloor.mask_has_hole_of_mentioned
#print axioms WitnessedDifference.PrimitiveContextFloor.hole_plugs_to_mentioned
#print axioms WitnessedDifference.PrimitiveContextFloor.recognized_implies_mentioned
#print axioms WitnessedDifference.PrimitiveContextFloor.profile_inhabited_iff_mentioned
#print axioms WitnessedDifference.PrimitiveContextFloor.hole_reflects_datum_equality
#print axioms WitnessedDifference.PrimitiveContextFloor.common_recognition_reflects_equality
#print axioms WitnessedDifference.PrimitiveContextFloor.one_instance_separates_iff_touches
#print axioms WitnessedDifference.PrimitiveContextFloor.persistent_separation_iff_requirement_cover
#print axioms WitnessedDifference.PrimitiveContextFloor.empty_tuple_separates_no_distinct_pair
#print axioms WitnessedDifference.PrimitiveContextFloor.unary_witness_only_separates_pairs_touching_its_datum
