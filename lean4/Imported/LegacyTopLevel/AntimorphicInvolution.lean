/- Imported so that this repository carries its own Lean evidence.
   Original sha256: f9cc8da1bf683a91dbf7c7b3db23f0bc08cd49b3d170c06a701ed4381d769400 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.LegacyTopLevel.AntimorphicInvolution
   Reason         : MSS-N
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   Renamed        : 2026-10-27, directory and namespace names only (lean4/RENAMES.json).
   AuthorityEffect: None. -/
/-!
# Edge Reversal and Conditional Projection Fragments

This file proves edge reversal is involutive and the empty-path case of reverse
concatenation. It also restates supplied non-collapse and retraction hypotheses.
The general path concatenation reversal identity, construction of an admissible
stage lift, and nonabelian torsion are not established here.

AuthorityEffect: None.
-/

namespace MSSN.AntimorphicInvolution

/-- Directed transition edge between states. -/
structure Edge where
  src : Nat
  dst : Nat
  deriving DecidableEq, Repr

/-- Reversal involution on directed edges: e = (u -> v) maps to e^† = (v -> u). -/
def reverseEdge (e : Edge) : Edge :=
  ⟨e.dst, e.src⟩

/-- Involution Theorem:
    Reversing an edge twice recovers the original edge identically: ((e)^†)^† = e. -/
theorem edge_involution_law (e : Edge) :
    reverseEdge (reverseEdge e) = e := by
  cases e
  rfl

/-- Directed path composed of a sequence of edges. -/
inductive Path : Nat → Nat → Type where
  | nil (v : Nat) : Path v v
  | cons {u v w : Nat} (e : Edge) (h : e.src = u ∧ e.dst = v) (p : Path v w) : Path u w

/-- Path concatenation: p1 ++ p2. -/
def concatPath {u v w : Nat} : Path u v → Path v w → Path u w
  | Path.nil _, q => q
  | Path.cons e h p, q => Path.cons e h (concatPath p q)

/-- Contravariant reversal of a path: reverses edge directions and order. -/
def reversePath {u v : Nat} : Path u v → Path v u
  | Path.nil x => Path.nil x
  | Path.cons e ⟨h1, h2⟩ p =>
    let rev_e : Edge := reverseEdge e
    concatPath (reversePath p) (Path.cons rev_e (by subst h1 h2; exact ⟨rfl, rfl⟩) (Path.nil _))

/-- Empty-path identity for reversal and concatenation; this is only the nil case. -/
theorem path_concatenation_contravariant_nil {u v : Nat} (p : Path u v) :
    concatPath (reversePath (Path.nil v)) (reversePath p) = reversePath p := by
  dsimp [reversePath, concatPath]

/-- Protected distinction between two distinct state identifiers. -/
structure ProtectedDistinction where
  stateA : Nat
  stateB : Nat
  h_distinct : stateA ≠ stateB
  label : String
  deriving Repr

/-- A projection map erases a protected distinction if it collapses stateA and stateB to the same target. -/
def collapsesDistinction (proj : Nat → Nat) (d : ProtectedDistinction) : Prop :=
  proj d.stateA = proj d.stateB

/-- The non-collapse hypothesis supplies distinction preservation directly;
    there is no admission or refusal algorithm in this statement. -/
theorem protected_distinction_non_erasure
    (proj : Nat → Nat) (d : ProtectedDistinction) (h_admissible : ¬ collapsesDistinction proj d) :
    proj d.stateA ≠ proj d.stateB := h_admissible

/-- Specialization at x of the supplied universal retraction hypothesis. -/
theorem stage_lift_down_retraction {α : Type} (x : α) (u : α → α) (d : α → α)
    (h_retract : ∀ y, d (u y) = y) :
    d (u x) = x :=
  h_retract x

end MSSN.AntimorphicInvolution
