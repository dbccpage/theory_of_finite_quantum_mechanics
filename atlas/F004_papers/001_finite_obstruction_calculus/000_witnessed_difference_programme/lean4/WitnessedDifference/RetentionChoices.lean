/-!
# Structural retention choices and arbitrary report tolerance

Typing imposes no relation between the three data fields of a retention
packet. Compatibility is a separate predicate. All-word tolerance agreement
is the greatest report-respecting forward-compatible relation; with a
reflexive symmetric tolerance it is reflexive symmetric, but a quotient
requires an additional transitivity proof. A raw report map requires the
separate condition that reports be literally constant on classes.
-/

namespace WitnessedDifference.RetentionChoices

universe u v w

structure Packet (Memory : Type u) (Input : Type v) (Report : Type w) where
  update : Input → Memory → Memory
  readout : Memory → Report
  comparison : Report → Report → Prop

/-- The complete typed extension space is a Cartesian product. -/
def assemble {M : Type u} {I : Type v} {O : Type w}
    (update : I → M → M) (readout : M → O) (comparison : O → O → Prop) : Packet M I O :=
  ⟨update, readout, comparison⟩

theorem every_packet_reassembles {M : Type u} {I : Type v} {O : Type w} (p : Packet M I O) :
    assemble p.update p.readout p.comparison = p := by
  cases p
  rfl

/-- Every independent combination has exactly the requested projections. -/
theorem independently_combined_projections {M : Type u} {I : Type v} {O : Type w}
    (update : I → M → M) (readout : M → O) (comparison : O → O → Prop) :
    (assemble update readout comparison).update = update ∧
    (assemble update readout comparison).readout = readout ∧
    (assemble update readout comparison).comparison = comparison := ⟨rfl, rfl, rfl⟩

def run {M : Type u} {I : Type v} (update : I → M → M) : List I → M → M
  | [], x => x
  | i :: word, x => run update word (update i x)

def WordCompatible {M : Type u} {I : Type v} {O : Type w}
    (p : Packet M I O) (x y : M) : Prop :=
  ∀ word : List I, p.comparison (p.readout (run p.update word x)) (p.readout (run p.update word y))

def ForwardCompatible {M : Type u} {I : Type v} {O : Type w}
    (p : Packet M I O) (R : M → M → Prop) : Prop :=
  ∀ x y, R x y → p.comparison (p.readout x) (p.readout y) ∧
    ∀ i, R (p.update i x) (p.update i y)

theorem word_compatible_is_forward_compatible {M : Type u} {I : Type v} {O : Type w}
    (p : Packet M I O) : ForwardCompatible p (WordCompatible p) := by
  intro x y hxy
  refine ⟨hxy [], ?_⟩
  intro i word
  exact hxy (i :: word)

theorem greatest_forward_relation {M : Type u} {I : Type v} {O : Type w}
    (p : Packet M I O) (R : M → M → Prop) (hR : ForwardCompatible p R) :
    ∀ x y, R x y → WordCompatible p x y := by
  intro x y hxy word
  induction word generalizing x y with
  | nil => exact (hR x y hxy).1
  | cons i word ih => exact ih (p.update i x) (p.update i y) ((hR x y hxy).2 i)

theorem word_compatible_reflexive {M : Type u} {I : Type v} {O : Type w}
    (p : Packet M I O) (hreflexive : ∀ o, p.comparison o o) :
    ∀ x, WordCompatible p x x := by
  intro x word
  exact hreflexive _

theorem word_compatible_symmetric {M : Type u} {I : Type v} {O : Type w}
    (p : Packet M I O) (hsymmetric : ∀ a b, p.comparison a b → p.comparison b a) :
    ∀ x y, WordCompatible p x y → WordCompatible p y x := by
  intro x y hxy word
  exact hsymmetric _ _ (hxy word)

/-- Transitivity of the declared report comparison suffices, but is not
necessary, for transitivity of the retained state relation. -/
theorem comparison_transitive_implies_word_compatible_transitive
    {M : Type u} {I : Type v} {O : Type w}
    (p : Packet M I O)
    (htransitive : ∀ a b c, p.comparison a b → p.comparison b c → p.comparison a c) :
    ∀ x y z, WordCompatible p x y → WordCompatible p y z → WordCompatible p x z := by
  intro x y z hxy hyz word
  exact htransitive _ _ _ (hxy word) (hyz word)

/-- With reflexive symmetric tolerance, the state relation is an equivalence
exactly when its own transitivity holds; tolerance does not supply it. -/
theorem word_compatible_equivalence_iff_transitive
    {M : Type u} {I : Type v} {O : Type w}
    (p : Packet M I O) (hreflexive : ∀ o, p.comparison o o)
    (hsymmetric : ∀ a b, p.comparison a b → p.comparison b a) :
    Equivalence (WordCompatible p) ↔
      ∀ x y z, WordCompatible p x y → WordCompatible p y z → WordCompatible p x z := by
  constructor
  · intro h
    exact fun _ _ _ hxy hyz => h.trans hxy hyz
  · intro htrans
    exact ⟨word_compatible_reflexive p hreflexive,
      fun hxy => word_compatible_symmetric p hsymmetric _ _ hxy,
      fun hxy hyz => htrans _ _ _ hxy hyz⟩

def compatibleSetoid {M : Type u} {I : Type v} {O : Type w}
    (p : Packet M I O) (hequivalence : Equivalence (WordCompatible p)) : Setoid M :=
  ⟨WordCompatible p, hequivalence⟩

def quotientUpdate {M : Type u} {I : Type v} {O : Type w}
    (p : Packet M I O) (hequivalence : Equivalence (WordCompatible p)) (i : I) :
    Quotient (compatibleSetoid p hequivalence) → Quotient (compatibleSetoid p hequivalence) :=
  Quotient.lift (fun x => Quotient.mk (compatibleSetoid p hequivalence) (p.update i x))
    (fun x y h => Quotient.sound ((word_compatible_is_forward_compatible p x y h).2 i))

/-- Literal readout descent has a separate necessary and sufficient condition
even after the state relation is known to be an equivalence. -/
theorem raw_readout_descends_iff {M : Type u} {I : Type v} {O : Type w}
    (p : Packet M I O) (hequivalence : Equivalence (WordCompatible p)) :
    (∃ readout : Quotient (compatibleSetoid p hequivalence) → O,
      ∀ x, readout (Quotient.mk (compatibleSetoid p hequivalence) x) = p.readout x) ↔
      ∀ x y, WordCompatible p x y → p.readout x = p.readout y := by
  constructor
  · intro h
    obtain ⟨readout, hreadout⟩ := h
    intro x y hxy
    calc
      p.readout x = readout (Quotient.mk (compatibleSetoid p hequivalence) x) := (hreadout x).symm
      _ = readout (Quotient.mk (compatibleSetoid p hequivalence) y) := congrArg readout (Quotient.sound hxy)
      _ = p.readout y := hreadout y
  · intro hconstant
    exact ⟨Quotient.lift p.readout hconstant, fun _ => rfl⟩

/-- An output symmetry without fixed values refutes a report choice invariant
under that symmetry. Identity updates and equality comparisons still exist:
this is not a blanket assertion that no natural component can be chosen. -/
theorem fixed_point_free_output_symmetry_refutes_readout
    {M : Type u} {O : Type w} (readout : M → O) (permute : O → O)
    (hfixedfree : ∀ o, permute o ≠ o) (hinvariant : ∀ x, permute (readout x) = readout x)
    (x : M) : False := hfixedfree (readout x) (hinvariant x)

def forwardApproximation {M : Type u} {I : Type v} {O : Type w}
    (p : Packet M I O) : Nat → M → M → Prop
  | 0 => fun x y => p.comparison (p.readout x) (p.readout y)
  | depth + 1 => fun x y => forwardApproximation p depth x y ∧
      ∀ i, forwardApproximation p depth (p.update i x) (p.update i y)

theorem word_compatible_below_every_approximation {M : Type u} {I : Type v} {O : Type w}
    (p : Packet M I O) (depth : Nat) :
    ∀ x y, WordCompatible p x y → forwardApproximation p depth x y := by
  induction depth with
  | zero =>
    intro x y hxy
    exact hxy []
  | succ depth ih =>
    intro x y hxy
    exact ⟨ih x y hxy, fun i => ih _ _ ((word_compatible_is_forward_compatible p x y hxy).2 i)⟩

theorem approximation_respects_reports {M : Type u} {I : Type v} {O : Type w}
    (p : Packet M I O) (depth : Nat) :
    ∀ x y, forwardApproximation p depth x y → p.comparison (p.readout x) (p.readout y) := by
  induction depth with
  | zero => exact fun _ _ h => h
  | succ depth ih => exact fun _ _ h => ih _ _ h.1

theorem stabilized_approximation_iff_word_compatible {M : Type u} {I : Type v} {O : Type w}
    (p : Packet M I O) (depth : Nat)
    (hstable : ∀ x y, forwardApproximation p depth x y → forwardApproximation p (depth + 1) x y)
    (x y : M) : forwardApproximation p depth x y ↔ WordCompatible p x y := by
  constructor
  · intro hxy
    apply greatest_forward_relation p (forwardApproximation p depth) ?_ x y hxy
    intro a b hab
    exact ⟨approximation_respects_reports p depth a b hab, (hstable a b hab).2⟩
  · exact word_compatible_below_every_approximation p depth x y

theorem run_identity {M : Type u} {I : Type v} (word : List I) (x : M) :
    run (fun (_ : I) (x : M) => x) word x = x := by
  induction word with
  | nil => rfl
  | cons _ _ ih => exact ih

/-- Static updates retain the declared comparison on the attained readout image,
including failures of transitivity witnessed on that image. -/
theorem identity_updates_word_compatible_iff
    {M : Type u} {I : Type v} {O : Type w}
    (readout : M → O) (comparison : O → O → Prop) (x y : M) :
    WordCompatible (assemble (fun (_ : I) (x : M) => x) readout comparison) x y ↔
      comparison (readout x) (readout y) := by
  constructor
  · intro h
    exact h []
  · intro h word
    change comparison (readout (run (fun (_ : I) (x : M) => x) word x))
      (readout (run (fun (_ : I) (x : M) => x) word y))
    rw [run_identity, run_identity]
    exact h

inductive ThreeReport where
  | a | b | c

def nontransitiveTolerance : ThreeReport → ThreeReport → Prop
  | .a, .c => False
  | .c, .a => False
  | _, _ => True

theorem declared_tolerance_reflexive_symmetric :
    (∀ x, nontransitiveTolerance x x) ∧
      (∀ x y, nontransitiveTolerance x y → nontransitiveTolerance y x) := by
  constructor
  · intro x
    cases x <;> trivial
  · intro x y hxy
    cases x <;> cases y <;> exact hxy

/-- A concrete reflexive symmetric tolerance survives as a nontransitive
greatest relation. No equivalence quotient can use this relation as equality. -/
theorem static_tolerance_nontransitive_countermodel :
    let p : Packet ThreeReport Unit ThreeReport :=
      assemble (fun _ x => x) id nontransitiveTolerance
    WordCompatible p .a .b ∧ WordCompatible p .b .c ∧ ¬ WordCompatible p .a .c := by
  dsimp
  refine ⟨?_, ?_, ?_⟩
  · exact (identity_updates_word_compatible_iff (I := Unit) id nontransitiveTolerance .a .b).mpr True.intro
  · exact (identity_updates_word_compatible_iff (I := Unit) id nontransitiveTolerance .b .c).mpr True.intro
  · intro h
    exact (identity_updates_word_compatible_iff (I := Unit) id nontransitiveTolerance .a .c).mp h

end WitnessedDifference.RetentionChoices

#print axioms WitnessedDifference.RetentionChoices.Packet
#print axioms WitnessedDifference.RetentionChoices.assemble
#print axioms WitnessedDifference.RetentionChoices.every_packet_reassembles
#print axioms WitnessedDifference.RetentionChoices.independently_combined_projections
#print axioms WitnessedDifference.RetentionChoices.run
#print axioms WitnessedDifference.RetentionChoices.WordCompatible
#print axioms WitnessedDifference.RetentionChoices.ForwardCompatible
#print axioms WitnessedDifference.RetentionChoices.word_compatible_is_forward_compatible
#print axioms WitnessedDifference.RetentionChoices.greatest_forward_relation
#print axioms WitnessedDifference.RetentionChoices.word_compatible_reflexive
#print axioms WitnessedDifference.RetentionChoices.word_compatible_symmetric
#print axioms WitnessedDifference.RetentionChoices.comparison_transitive_implies_word_compatible_transitive
#print axioms WitnessedDifference.RetentionChoices.word_compatible_equivalence_iff_transitive
#print axioms WitnessedDifference.RetentionChoices.compatibleSetoid
#print axioms WitnessedDifference.RetentionChoices.quotientUpdate
#print axioms WitnessedDifference.RetentionChoices.raw_readout_descends_iff
#print axioms WitnessedDifference.RetentionChoices.fixed_point_free_output_symmetry_refutes_readout
#print axioms WitnessedDifference.RetentionChoices.forwardApproximation
#print axioms WitnessedDifference.RetentionChoices.word_compatible_below_every_approximation
#print axioms WitnessedDifference.RetentionChoices.approximation_respects_reports
#print axioms WitnessedDifference.RetentionChoices.stabilized_approximation_iff_word_compatible
#print axioms WitnessedDifference.RetentionChoices.run_identity
#print axioms WitnessedDifference.RetentionChoices.identity_updates_word_compatible_iff
#print axioms WitnessedDifference.RetentionChoices.ThreeReport
#print axioms WitnessedDifference.RetentionChoices.nontransitiveTolerance
#print axioms WitnessedDifference.RetentionChoices.declared_tolerance_reflexive_symmetric
#print axioms WitnessedDifference.RetentionChoices.static_tolerance_nontransitive_countermodel
#print axioms WitnessedDifference.RetentionChoices.Packet.mk
#print axioms WitnessedDifference.RetentionChoices.Packet.update
#print axioms WitnessedDifference.RetentionChoices.Packet.readout
#print axioms WitnessedDifference.RetentionChoices.Packet.comparison
#print axioms WitnessedDifference.RetentionChoices.ThreeReport.a
#print axioms WitnessedDifference.RetentionChoices.ThreeReport.b
#print axioms WitnessedDifference.RetentionChoices.ThreeReport.c
