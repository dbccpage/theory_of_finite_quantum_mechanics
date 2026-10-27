/- Imported so that this repository carries its own Lean evidence.
   Original sha256: cee217329b9175e8b9cd5335b06ac9d489daff4410d39343782851fc00a03b13 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.LegacyTopLevel.Stage1LiftNecessity
   Reason         : S(n)
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   Renamed        : 2026-10-27, directory and namespace names only (lean4/RENAMES.json).
   AuthorityEffect: None. -/
import Imported.LegacyTopLevel.SLevel
import Imported.LegacyTopLevel.Stage0LiftNecessity

namespace Stage1LiftNecessity

open SnPacketGame
open Stage0LiftNecessity

/-- Directed path of length 2 with distinct endpoints on a carrier α:
    a -> b -> c with a, b, c pairwise distinct. -/
def HasDirectedPath2 {α : Type} (r : BinaryRel α) : Prop :=
  ∃ a b c : α, r a b ∧ r b c ∧ a ≠ b ∧ b ≠ c ∧ a ≠ c

/-- Directed 3-cycle on a carrier α:
    a -> b -> c -> a with a, b, c pairwise distinct. -/
def HasDirectedCycle3 {α : Type} (r : BinaryRel α) : Prop :=
  ∃ a b c : α, r a b ∧ r b c ∧ r c a ∧ a ≠ b ∧ b ≠ c ∧ a ≠ c

/-- Transitive closure gap: a length-2 path exists, but the shortcut edge does not. -/
def HasTransitiveGap {α : Type} (r : BinaryRel α) : Prop :=
  ∃ a b c : α, r a b ∧ r b c ∧ ¬ r a c ∧ a ≠ b ∧ b ≠ c ∧ a ≠ c

/-! ## Stage 1: Carrier of size 2 (Bool) -/

/-- Theorem 1 (Countermodel for Isolated Edge at Stage 1):
    An irreflexive witnessed relation (isolated edge) is satisfiable on Bool.
    Therefore, isolated edges do NOT force a lift beyond Stage 1. -/
theorem isolated_edge_satisfiable_at_stage1 :
    ∃ r : BinaryRel Bool, IrreflWitnessed r :=
  ⟨D2, stage1_resolves_irrefl_witness⟩

/-- Lemma: On a carrier of size 2 (Bool), if a ≠ b and b ≠ c, then a = c.
    (Pigeonhole Principle on 2 elements) -/
theorem pigeonhole_bool (a b c : Bool) (h1 : a ≠ b) (h2 : b ≠ c) : a = c := by
  cases a <;> cases b <;> cases c <;> first | rfl | contradiction

/-- Theorem 2 (Obstruction: No Length-2 Path with Distinct Endpoints on Bool):
    On a 2-element carrier, no relation can contain a length-2 path with distinct endpoints.
    Every length-2 path must collapse endpoints (a = c). -/
theorem no_directed_path2_on_bool (r : BinaryRel Bool) :
    ¬ HasDirectedPath2 r := by
  intro ⟨a, b, c, _, _, hab, hbc, hac⟩
  have heq := pigeonhole_bool a b c hab hbc
  exact hac heq

/-- Theorem 3 (Obstruction: No Directed 3-Cycle on Bool):
    On a 2-element carrier, no relation can contain a directed 3-cycle with distinct vertices. -/
theorem no_directed_cycle3_on_bool (r : BinaryRel Bool) :
    ¬ HasDirectedCycle3 r := by
  intro ⟨a, b, c, _, _, _, hab, hbc, hac⟩
  have heq := pigeonhole_bool a b c hab hbc
  exact hac heq

/-! ## Stage 2: Carrier of size 3 (Fin 3) -/

/-- Length-2 path relation on Fin 3: 0 -> 1 and 1 -> 2. -/
def PathRel3 : BinaryRel (Fin 3) :=
  fun x y => (x.val = 0 ∧ y.val = 1) ∨ (x.val = 1 ∧ y.val = 2)

theorem pathRel3_irrefl : Irrefl PathRel3 := by
  intro x
  cases x with | mk v h =>
  intro hrel
  rcases hrel with ⟨h1, h2⟩ | ⟨h1, h2⟩
  · omega
  · omega

theorem pathRel3_has_path2 : HasDirectedPath2 PathRel3 := by
  exact ⟨⟨0, by decide⟩, ⟨1, by decide⟩, ⟨2, by decide⟩,
         Or.inl ⟨rfl, rfl⟩, Or.inr ⟨rfl, rfl⟩,
         by decide, by decide, by decide⟩

/-- Theorem 4 (Stage 2 Resolves Directed Path Composition):
    Stage 2 carrier Fin 3 admits an irreflexive relation with a length-2 path. -/
theorem stage2_resolves_directed_path2 :
    Irrefl PathRel3 ∧ HasDirectedPath2 PathRel3 :=
  ⟨pathRel3_irrefl, pathRel3_has_path2⟩

/-- Directed 3-cycle relation on Fin 3: 0 -> 1 -> 2 -> 0. -/
def CycleRel3 : BinaryRel (Fin 3) :=
  fun x y => (x.val = 0 ∧ y.val = 1) ∨ (x.val = 1 ∧ y.val = 2) ∨ (x.val = 2 ∧ y.val = 0)

theorem cycleRel3_irrefl : Irrefl CycleRel3 := by
  intro x
  cases x with | mk v h =>
  intro hrel
  rcases hrel with ⟨h1, h2⟩ | ⟨h1, h2⟩ | ⟨h1, h2⟩
  · omega
  · omega
  · omega

theorem cycleRel3_has_cycle3 : HasDirectedCycle3 CycleRel3 := by
  exact ⟨⟨0, by decide⟩, ⟨1, by decide⟩, ⟨2, by decide⟩,
         Or.inl ⟨rfl, rfl⟩, Or.inr (Or.inl ⟨rfl, rfl⟩), Or.inr (Or.inr ⟨rfl, rfl⟩),
         by decide, by decide, by decide⟩

/-- Theorem 5 (Stage 2 Resolves Directed 3-Cycle):
    Stage 2 carrier Fin 3 admits an irreflexive relation with a directed 3-cycle. -/
theorem stage2_resolves_directed_cycle3 :
    Irrefl CycleRel3 ∧ HasDirectedCycle3 CycleRel3 :=
  ⟨cycleRel3_irrefl, cycleRel3_has_cycle3⟩

/-- Theorem 6 (Stage 1 -> Stage 2 Lift is Strictly Necessary for Directed Path Composition):
    Stage 1 cannot satisfy HasDirectedPath2, whereas Stage 2 can. -/
theorem stage1_lift_strictly_necessary_for_path_composition :
    (∀ r : BinaryRel Bool, ¬ HasDirectedPath2 r) ∧
    (∃ r : BinaryRel (Fin 3), Irrefl r ∧ HasDirectedPath2 r) :=
  ⟨no_directed_path2_on_bool, ⟨PathRel3, stage2_resolves_directed_path2⟩⟩

/-- Theorem 7 (Stage 1 -> Stage 2 Lift is Strictly Necessary for Directed 3-Cycle):
    Stage 1 cannot satisfy HasDirectedCycle3, whereas Stage 2 can. -/
theorem stage1_lift_strictly_necessary_for_directed_cycle :
    (∀ r : BinaryRel Bool, ¬ HasDirectedCycle3 r) ∧
    (∃ r : BinaryRel (Fin 3), Irrefl r ∧ HasDirectedCycle3 r) :=
  ⟨no_directed_cycle3_on_bool, ⟨CycleRel3, stage2_resolves_directed_cycle3⟩⟩

#print axioms isolated_edge_satisfiable_at_stage1
#print axioms no_directed_path2_on_bool
#print axioms no_directed_cycle3_on_bool
#print axioms stage2_resolves_directed_path2
#print axioms stage2_resolves_directed_cycle3
#print axioms stage1_lift_strictly_necessary_for_path_composition
#print axioms stage1_lift_strictly_necessary_for_directed_cycle

end Stage1LiftNecessity
