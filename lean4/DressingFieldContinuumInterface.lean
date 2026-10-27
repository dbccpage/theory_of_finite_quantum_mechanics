import FiniteGraphDressing
import Mathlib.Algebra.Group.Basic
import Mathlib.Algebra.Group.TypeTags.Basic
import Mathlib.Tactic.Group

/-!
# Finite non-locality of rooted tree dressing (DFM-CONTINUUM-INTERFACE)

AuthorityEffect: None.
Outcome: Narrowed. The node stays OPEN.

`FiniteGraphDressing.dress` evaluates an edge from a supplied vertex map.
On one supplied rooted tree, that value on the chord `a → b` depends on the
edge `root → p`, which does not meet `{a, b}`. Equal labels on the closed star
of the chord therefore do not determine the dressed chord.

Not proved: a smooth field, a topology, a refinement limit, continuum patching,
or continuum dynamics.
-/

namespace DressingFieldContinuumInterface

open FiniteGraphDressing

/-! Compositional dependency certificates for supplied rooted paths. -/
namespace Dependency
variable {V E G : Type*} [Group G] {src dst : E → V}

def edges : {a b : V} → Walk src dst a b → List E
  | _, _, .nil _ => []
  | _, _, .edge e => [e]
  | _, _, .reverse p => edges p
  | _, _, .append p q => edges p ++ edges q

def AgreeOn (s : List E) (U W : E → G) : Prop := ∀ e ∈ s, U e = W e

theorem transport_agrees {a b : V} (p : Walk src dst a b) (U W : E → G)
    (h : AgreeOn (edges p) U W) : transport src dst U p = transport src dst W p := by
  induction p with
  | nil v => rfl
  | edge e => exact h e (by simp [edges])
  | reverse p ih => exact congrArg Inv.inv (ih h)
  | append p q ihp ihq =>
    have hp : AgreeOn (edges p) U W := fun e he => h e (by simp [edges, he])
    have hq : AgreeOn (edges q) U W := fun e he => h e (by simp [edges, he])
    exact congrArg₂ (· * ·) (ihq hq) (ihp hp)

/-- Rooted paths are supplied, not inferred to be a spanning tree. -/
structure Plan (src dst : E → V) where
  root : V
  paths : ∀ v, Walk src dst root v

def Plan.footprint (P : Plan src dst) (e : E) : List E :=
  e :: (edges (P.paths (src e)) ++ edges (P.paths (dst e)))

def Plan.dressing (P : Plan src dst) (U : E → G) (v : V) : G :=
  (transport src dst U (P.paths v))⁻¹

def Plan.evaluate (P : Plan src dst) (U : E → G) (e : E) : G :=
  dress src dst U (P.dressing U) e

theorem Plan.evaluate_formula (P : Plan src dst) (U : E → G) (e : E) :
    P.evaluate U e = (transport src dst U (P.paths (dst e)))⁻¹ * U e *
      transport src dst U (P.paths (src e)) := by
  simp [Plan.evaluate, dress, Plan.dressing]

theorem Plan.evaluate_agrees (P : Plan src dst) (U W : E → G) (e : E)
    (h : AgreeOn (P.footprint e) U W) : P.evaluate U e = P.evaluate W e := by
  have he : U e = W e := h e (by simp [Plan.footprint])
  have hs : AgreeOn (edges (P.paths (src e))) U W :=
    fun k hk => h k (by simp [Plan.footprint, hk])
  have hd : AgreeOn (edges (P.paths (dst e))) U W :=
    fun k hk => h k (by simp [Plan.footprint, hk])
  rw [P.evaluate_formula, P.evaluate_formula, he,
    transport_agrees _ U W hs, transport_agrees _ U W hd]

/-- A changed result requires a changed label in the certified footprint. -/
theorem Plan.changed_label (P : Plan src dst) (U W : E → G) (e : E)
    (h : P.evaluate U e ≠ P.evaluate W e) :
    ∃ k ∈ P.footprint e, U k ≠ W k := by
  classical
  by_contra hn
  push_neg at hn
  exact h (P.evaluate_agrees U W e hn)

/-- Supersets remain sound dependency certificates. -/
theorem Plan.evaluate_agrees_on_superset (P : Plan src dst) (U W : E → G)
    (e : E) (s : List E) (hs : ∀ k ∈ P.footprint e, k ∈ s)
    (h : AgreeOn s U W) : P.evaluate U e = P.evaluate W e :=
  P.evaluate_agrees U W e (fun k hk => h k (hs k hk))

end Dependency

inductive Vtx
  | root
  | p
  | a
  | b
  deriving DecidableEq

inductive Edg
  | eRP
  | ePA
  | eRB
  | eAB
  deriving DecidableEq

def src : Edg → Vtx
  | .eRP => .root
  | .ePA => .p
  | .eRB => .root
  | .eAB => .a

def dst : Edg → Vtx
  | .eRP => .p
  | .ePA => .a
  | .eRB => .b
  | .eAB => .b

/-- The edge meets the chord `a → b` at `a` or at `b`. -/
def incidentChord (e : Edg) : Prop :=
  src e = .a ∨ src e = .b ∨ dst e = .a ∨ dst e = .b

theorem outer_misses_star : ¬ incidentChord .eRP := by
  intro h
  simp only [incidentChord, src, dst] at h
  rcases h with h | h | h | h <;> cases h

theorem incident_ePA : incidentChord .ePA :=
  Or.inr (Or.inr (Or.inl rfl))

theorem incident_eRB : incidentChord .eRB :=
  Or.inr (Or.inr (Or.inr rfl))

theorem incident_eAB : incidentChord .eAB :=
  Or.inl rfl

def conn {G : Type*} [Group G] (xRP xPA xRB xAB : G) : Edg → G
  | .eRP => xRP
  | .ePA => xPA
  | .eRB => xRB
  | .eAB => xAB

/-- Supplied rooted tree paths. The tree is data, not a proved spanning theorem. -/
def treePath : (v : Vtx) → Walk src dst Vtx.root v
  | .root => .nil Vtx.root
  | .p => .edge Edg.eRP
  | .a => .append (.edge Edg.eRP) (.edge Edg.ePA)
  | .b => .edge Edg.eRB

def treeTransport {G : Type*} [Group G] (U : Edg → G) (v : Vtx) : G :=
  transport src dst U (treePath v)

def treeDressing {G : Type*} [Group G] (U : Edg → G) (v : Vtx) : G :=
  (treeTransport U v)⁻¹

theorem transport_a {G : Type*} [Group G] (U : Edg → G) :
    treeTransport U .a = U .ePA * U .eRP := by
  unfold treeTransport treePath
  rfl

theorem transport_b {G : Type*} [Group G] (U : Edg → G) :
    treeTransport U .b = U .eRB := by
  unfold treeTransport treePath
  rfl

/-- Later factors stand on the left, as in `FiniteGraphDressing.transport`. -/
theorem dressed_chord_formula {G : Type*} [Group G] (xRP xPA xRB xAB : G) :
    dress src dst (conn xRP xPA xRB xAB) (treeDressing (conn xRP xPA xRB xAB)) .eAB
      = xRB⁻¹ * xAB * xPA * xRP := by
  set U : Edg → G := conn xRP xPA xRB xAB
  have ha : treeTransport U .a = U .ePA * U .eRP := transport_a U
  have hb : treeTransport U .b = U .eRB := transport_b U
  have hdef :
      dress src dst U (treeDressing U) .eAB
        = (treeTransport U .b)⁻¹ * U .eAB * ((treeTransport U .a)⁻¹)⁻¹ := by
    rfl
  rw [hdef, ha, hb, inv_inv]
  unfold U
  dsimp only [conn]
  group

theorem dressed_chord_witness {G : Type*} [Group G] (x : G) :
    dress src dst (conn x 1 1 1) (treeDressing (conn x 1 1 1)) .eAB = x := by
  rw [dressed_chord_formula]
  group

theorem star_stable {G : Type*} [Group G] (x x' y z w : G) (e : Edg)
    (he : incidentChord e) :
    conn x y z w e = conn x' y z w e := by
  cases e with
  | eRP => exact (outer_misses_star he).elim
  | ePA => rfl
  | eRB => rfl
  | eAB => rfl

theorem witness_star_agrees {G : Type*} [Group G] (x x' : G) (e : Edg)
    (he : incidentChord e) :
    conn x (1 : G) 1 1 e = conn x' 1 1 1 e :=
  star_stable x x' 1 1 1 e he

theorem not_star_local {G : Type*} [Group G] (x x' : G) (hne : x ≠ x') :
    dress src dst (conn x 1 1 1) (treeDressing (conn x 1 1 1)) .eAB ≠
      dress src dst (conn x' 1 1 1) (treeDressing (conn x' 1 1 1)) .eAB := by
  rw [dressed_chord_witness, dressed_chord_witness]
  exact hne

theorem witness_two_five :
    dress src dst (conn (Multiplicative.ofAdd (2 : ℤ)) 1 1 1)
        (treeDressing (conn (Multiplicative.ofAdd (2 : ℤ)) 1 1 1)) .eAB
      = Multiplicative.ofAdd (2 : ℤ)
    ∧ dress src dst (conn (Multiplicative.ofAdd (5 : ℤ)) 1 1 1)
        (treeDressing (conn (Multiplicative.ofAdd (5 : ℤ)) 1 1 1)) .eAB
      = Multiplicative.ofAdd (5 : ℤ) :=
  ⟨dressed_chord_witness _, dressed_chord_witness _⟩

theorem witness_two_ne_five :
    dress src dst (conn (Multiplicative.ofAdd (2 : ℤ)) 1 1 1)
        (treeDressing (conn (Multiplicative.ofAdd (2 : ℤ)) 1 1 1)) .eAB ≠
      dress src dst (conn (Multiplicative.ofAdd (5 : ℤ)) 1 1 1)
        (treeDressing (conn (Multiplicative.ofAdd (5 : ℤ)) 1 1 1)) .eAB := by
  rw [dressed_chord_witness, dressed_chord_witness]
  intro h
  have hne : (2 : ℤ) ≠ 5 := by decide
  have h' : (2 : ℤ) = 5 := by
    simpa [toAdd_ofAdd] using congrArg Multiplicative.toAdd h
  exact hne h'

def witnessPlan : Dependency.Plan src dst := ⟨Vtx.root, treePath⟩

theorem witness_plan_evaluate {G : Type*} [Group G] (U : Edg → G) (e : Edg) :
    witnessPlan.evaluate U e = dress src dst U (treeDressing U) e := rfl

theorem outer_in_footprint : Edg.eRP ∈ witnessPlan.footprint Edg.eAB := by
  simp [witnessPlan, Dependency.Plan.footprint, treePath, src, dst, Dependency.edges]

#print axioms Dependency.transport_agrees
#print axioms Dependency.Plan.evaluate_formula
#print axioms Dependency.Plan.evaluate_agrees
#print axioms Dependency.Plan.changed_label
#print axioms Dependency.Plan.evaluate_agrees_on_superset
#print axioms witness_plan_evaluate
#print axioms outer_in_footprint
#print axioms dressed_chord_formula
#print axioms dressed_chord_witness
#print axioms not_star_local
#print axioms witness_star_agrees
#print axioms outer_misses_star
#print axioms witness_two_five
#print axioms witness_two_ne_five

end DressingFieldContinuumInterface
