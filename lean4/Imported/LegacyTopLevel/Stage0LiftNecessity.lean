/- Imported so that this repository carries its own Lean evidence.
   Original sha256: 206461cb038efe9b88892f229766c4e8830c00e09fadb210661924e70d96233a (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.LegacyTopLevel.Stage0LiftNecessity
   Reason         : S(n)
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   Renamed        : 2026-10-27, directory and namespace names only (lean4/RENAMES.json).
   AuthorityEffect: None. -/
import Imported.LegacyTopLevel.SLevel

namespace Stage0LiftNecessity

open SnPacketGame

/-- A binary relation over a carrier type α. -/
def BinaryRel (α : Type) := α → α → Prop

/-- Irreflexivity property: no element is related to itself. -/
def Irrefl {α : Type} (r : BinaryRel α) : Prop :=
  ∀ x : α, ¬ r x x

/-- Witnessed property: at least one pair is related. -/
def HasWitness {α : Type} (r : BinaryRel α) : Prop :=
  ∃ a b : α, r a b

/-- Bare Assertion (A1): a relation with at least one witnessed pair. -/
def BareAssertion {α : Type} (r : BinaryRel α) : Prop :=
  HasWitness r

/-- Irreflexive Witnessed Relation (A1i): irreflexivity combined with a witnessed pair. -/
def IrreflWitnessed {α : Type} (r : BinaryRel α) : Prop :=
  Irrefl r ∧ HasWitness r

/-! ## Stage 0: Single-Element Carrier Model (Unit) -/

/-- Theorem 1 (Countermodel for Bare Assertion A1):
    Bare assertion is satisfiable on a single-element carrier (Unit).
    Thus, bare assertion alone does NOT force an extension beyond Stage 0. -/
theorem bare_assertion_satisfiable_at_stage0 :
    ∃ r : BinaryRel Unit, BareAssertion r :=
  ⟨fun _ _ => True, ⟨(), (), trivial⟩⟩

/-- Theorem 2 (Obstruction on Subsingleton / Stage 0 Carrier):
    No irreflexive relation on a subsingleton carrier can have a witness.
    This is the formal mathematical obstruction encountered at Stage 0. -/
theorem no_irrefl_witness_on_subsingleton {α : Type} [Subsingleton α]
    (r : BinaryRel α) (hirr : Irrefl r) : ¬ HasWitness r := by
  intro hw
  rcases hw with ⟨a, b, hr⟩
  have hab : a = b := Subsingleton.elim a b
  rw [hab] at hr
  exact hirr b hr

/-- Corollary: Stage 0 carrier Unit cannot satisfy IrreflWitnessed. -/
theorem stage0_cannot_satisfy_irrefl_witness :
    ∀ r : BinaryRel Unit, ¬ IrreflWitnessed r := by
  intro r ⟨hirr, hwit⟩
  exact no_irrefl_witness_on_subsingleton r hirr hwit

/-! ## Stage 0 Syntax Evaluation -/

/-- Abstract syntax tree for expressions generated at Stage 0. -/
inductive Stage0Expr where
  | void : Stage0Expr
  | wrap : Stage0Expr → Stage0Expr
  deriving DecidableEq, Repr

/-- Semantic evaluation map into the Stage 0 single-point carrier. -/
def eval0 : Stage0Expr → Unit :=
  fun _ => ()

/-- Theorem 3 (Semantic Collapse of Stage 0 Expressions):
    Any two Stage 0 expressions evaluate to the identical semantic value.
    Stage 0 cannot produce distinct named endpoints. -/
theorem stage0_semantic_collapse (e1 e2 : Stage0Expr) :
    eval0 e1 = eval0 e2 := by
  rfl

/-! ## Stage 1: Two-Element Extension (Bool) -/

/-- Canonical directed relation on Bool: false relates to true. -/
def D2 : BinaryRel Bool :=
  fun x y => x = false ∧ y = true

theorem d2_irrefl : Irrefl D2 := by
  intro x
  cases x
  · intro h
    cases h.2
  · intro h
    cases h.1

theorem d2_witness : HasWitness D2 :=
  ⟨false, true, ⟨rfl, rfl⟩⟩

/-- Theorem 4 (Stage 1 Resolves Irreflexive Witness):
    The two-element carrier Bool admits an irreflexive relation with a witness. -/
theorem stage1_resolves_irrefl_witness :
    IrreflWitnessed D2 :=
  ⟨d2_irrefl, d2_witness⟩

/-! ## Lift Necessity Certificate -/

/-- A verified Certificate recording an attested same-stage obstruction
    and its verified resolution in the next stage. -/
structure LiftNecessityCertificate where
  source_level : Nat
  target_level : Nat
  goal_name : String
  obstruction_name : String
  level_step : target_level = source_level + 1
  stage0_obstructed : ∀ r : BinaryRel Unit, ¬ IrreflWitnessed r
  stage1_resolves : IrreflWitnessed D2

/-- Canonical Stage 0 -> Stage 1 Lift Necessity Certificate. -/
def stage0_to_stage1_certificate : LiftNecessityCertificate :=
  { source_level := 0
    target_level := 1
    goal_name := "IrreflexiveWitnessedRelation"
    obstruction_name := "SubsingletonDiagonalSelfRelationObstruction"
    level_step := rfl
    stage0_obstructed := stage0_cannot_satisfy_irrefl_witness
    stage1_resolves := stage1_resolves_irrefl_witness }

/-- Theorem 5 (Stage 0 -> Stage 1 Lift is Strictly Necessary for Irreflexive Relation):
    Under the goal of realizing an irreflexive relation with a witness,
    Stage 0 is provably insufficient while Stage 1 is sufficient. -/
theorem stage0_lift_strictly_necessary_for_irrefl_relation :
    (∀ r : BinaryRel Unit, ¬ IrreflWitnessed r) ∧
    (∃ r : BinaryRel Bool, IrreflWitnessed r) :=
  ⟨stage0_cannot_satisfy_irrefl_witness, ⟨D2, stage1_resolves_irrefl_witness⟩⟩

#print axioms bare_assertion_satisfiable_at_stage0
#print axioms stage0_cannot_satisfy_irrefl_witness
#print axioms stage1_resolves_irrefl_witness
#print axioms stage0_lift_strictly_necessary_for_irrefl_relation

end Stage0LiftNecessity
