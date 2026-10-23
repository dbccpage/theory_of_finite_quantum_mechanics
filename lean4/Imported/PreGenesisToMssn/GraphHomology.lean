/- Imported from the sibling atlas so that this repository carries its own Lean evidence.
   Original path : omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/GraphHomology.lean
   Original sha256: ca85b02417bf1ce3d0d61ee15bf04c4842f107f69671bed4a35255219bdf0d52 (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.PreGenesisToMssn.GraphHomology
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.PreGenesisToMssn.FreeAbelian

/-! Integral zeroth graph homology is free on the connected components.
Graphs have separately typed vertices and edges; loops and parallel edges are
allowed. Connectivity ignores edge orientation but the chain boundary retains it.
The construction works for arbitrary carriers, including the empty graph.
-/
namespace PreMssn.GraphHomology
open Lean.Grind
open AddCommMonoid AddCommGroup
open Homology FreeAbelian
universe u

structure Graph where
  Vertex : Type u
  Edge : Type u
  source : Edge → Vertex
  target : Edge → Vertex

inductive Connected (G : Graph.{u}) : G.Vertex → G.Vertex → Prop where
  | refl (v) : Connected G v v
  | edge (e) : Connected G (G.source e) (G.target e)
  | symm {v w} : Connected G v w → Connected G w v
  | trans {v w z} : Connected G v w → Connected G w z → Connected G v z

def componentSetoid (G : Graph.{u}) : Setoid G.Vertex where
  r := Connected G
  iseqv := ⟨Connected.refl, Connected.symm, Connected.trans⟩

def Component (G : Graph.{u}) := Quotient (componentSetoid G)
def component (G : Graph.{u}) (v : G.Vertex) : Component G := Quotient.mk _ v

theorem component_eq_iff (G : Graph.{u}) (v w : G.Vertex) :
    component G v = component G w ↔ Connected G v w :=
  ⟨fun h => Quotient.exact (s := componentSetoid G) h,
   fun h => Quotient.sound (s := componentSetoid G) h⟩

def boundary (G : Graph.{u}) : AddHom (Free G.Edge) (Free G.Vertex) :=
  extend (fun e => gen (G.target e) - gen (G.source e))

theorem boundary_gen (G : Graph.{u}) (e : G.Edge) :
    boundary G (gen e) = gen (G.target e) - gen (G.source e) := rfl

theorem loop_boundary_zero (G : Graph.{u}) (e : G.Edge)
    (loop : G.target e = G.source e) : boundary G (gen e) = 0 := by
  rw [boundary_gen, loop, sub_self]

abbrev H0 (G : Graph.{u}) := ImageQuotient (boundary G)
def vertexClass (G : Graph.{u}) (v : G.Vertex) : H0 G :=
  quotientProjection (boundary G) (gen v)

theorem vertexClass_connected (G : Graph.{u}) {v w : G.Vertex}
    (h : Connected G v w) : vertexClass G v = vertexClass G w := by
  induction h with
  | refl => rfl
  | edge e =>
    have hz : quotientProjection (boundary G) (boundary G (gen e)) = 0 :=
      (quotient_class_zero_iff (boundary G) _).mpr ⟨gen e, rfl⟩
    rw [boundary_gen, (quotientProjection (boundary G)).map_sub] at hz
    exact (sub_eq_zero_iff.mp hz).symm
  | symm _ ih => exact ih.symm
  | trans _ _ ih₁ ih₂ => exact ih₁.trans ih₂

def componentClass (G : Graph.{u}) : Component G → H0 G := fun c =>
  Quotient.liftOn c (vertexClass G) (fun _ _ h => vertexClass_connected G h)

def componentProjection (G : Graph.{u}) : AddHom (Free G.Vertex) (Free (Component G)) :=
  FreeAbelian.map (component G)

theorem componentProjection_boundary (G : Graph.{u}) (b : Free G.Edge) :
    componentProjection G (boundary G b) = 0 := by
  apply hom_ext ((componentProjection G).comp (boundary G))
    (AddHom.zero (Free G.Edge) (Free (Component G))) _ b
  intro e
  change componentProjection G (boundary G (gen e)) = 0
  rw [boundary_gen, (componentProjection G).map_sub]
  change gen (component G (G.target e)) - gen (component G (G.source e)) = 0
  rw [(component_eq_iff G _ _).mpr (Connected.edge e), sub_self]

def toComponents (G : Graph.{u}) : AddHom (H0 G) (Free (Component G)) :=
  quotientDescend (boundary G) (componentProjection G) (componentProjection_boundary G)

def fromComponents (G : Graph.{u}) : AddHom (Free (Component G)) (H0 G) :=
  extend (componentClass G)

theorem from_to_vertex (G : Graph.{u}) (v : G.Vertex) :
    fromComponents G (toComponents G (vertexClass G v)) = vertexClass G v := rfl

theorem from_to (G : Graph.{u}) (q : H0 G) :
    fromComponents G (toComponents G q) = q := by
  induction q using Quotient.inductionOn with
  | _ x =>
    exact hom_ext
      ((fromComponents G).comp ((toComponents G).comp (quotientProjection (boundary G))))
      (quotientProjection (boundary G)) (from_to_vertex G) x

theorem to_from (G : Graph.{u}) (q : Free (Component G)) :
    toComponents G (fromComponents G q) = q := by
  apply hom_ext ((toComponents G).comp (fromComponents G)) (AddHom.identity _) _ q
  intro c
  induction c using Quotient.inductionOn with
  | _ v => rfl

/-- The integral boundary quotient is isomorphic to the free abelian group
on the actual orientation-forgetting connected-component quotient. -/
def h0ComponentIso (G : Graph.{u}) : AddIso (H0 G) (Free (Component G)) where
  forward := toComponents G
  backward := fromComponents G
  left_inverse := from_to G
  right_inverse := to_from G

theorem vertex_class_eq_iff_connected (G : Graph.{u}) (v w : G.Vertex) :
    vertexClass G v = vertexClass G w ↔ Connected G v w := by
  constructor
  · intro h
    have hgen : gen (component G v) = gen (component G w) := congrArg (toComponents G) h
    classical
    let distinguish : Component G → Int := fun c => if c = component G v then 1 else 0
    have heq := congrArg (extend distinguish) hgen
    change distinguish (component G v) = distinguish (component G w) at heq
    have hc : component G w = component G v := by
      by_cases hn : component G w = component G v
      · exact hn
      · simp [distinguish, hn] at heq
    exact (component_eq_iff G v w).mp hc.symm
  · exact vertexClass_connected G

instance punitGroup : AddCommGroup PUnit where
  zero := PUnit.unit
  add _ _ := PUnit.unit
  neg _ := PUnit.unit
  sub _ _ := PUnit.unit
  add_zero _ := Subsingleton.elim _ _
  add_comm _ _ := rfl
  add_assoc _ _ _ := rfl
  neg_add_cancel _ := rfl
  sub_eq_add_neg _ _ := rfl

/-- The degree-zero chain fragment of the graph, with zero outgoing group. -/
def complex (G : Graph.{u}) : Complex where
  upper := Free G.Edge
  middle := Free G.Vertex
  lower := PUnit
  boundary := boundary G
  differential := AddHom.zero _ _
  square_zero _ := rfl

def asCycle (G : Graph.{u}) : AddHom (Free G.Vertex) (Cycle (complex G)) where
  toFun x := ⟨x, rfl⟩
  map_zero := rfl
  map_add _ _ := rfl

def cycleValue (G : Graph.{u}) : AddHom (Cycle (complex G)) (Free G.Vertex) where
  toFun x := x.val
  map_zero := rfl
  map_add _ _ := rfl

def toH0 (G : Graph.{u}) : AddHom (Homology (complex G)) (H0 G) :=
  quotientDescend (boundaryCycle (complex G))
    ((quotientProjection (boundary G)).comp (cycleValue G)) (by
      intro b
      exact (quotient_class_zero_iff (boundary G) _).mpr ⟨b, rfl⟩)

def fromH0 (G : Graph.{u}) : AddHom (H0 G) (Homology (complex G)) :=
  quotientDescend (boundary G)
    ((quotientProjection (boundaryCycle (complex G))).comp (asCycle G)) (by
      intro b
      exact (quotient_class_zero_iff (boundaryCycle (complex G)) _).mpr ⟨b, rfl⟩)

/-- Identifies the graph presentation quotient with the previously constructed
kernel/image homology group, not merely a group named H0. -/
def homologyH0Iso (G : Graph.{u}) : AddIso (Homology (complex G)) (H0 G) where
  forward := toH0 G
  backward := fromH0 G
  left_inverse q := by
    induction q using Quotient.inductionOn with
    | _ z =>
      apply congrArg (quotientProjection (boundaryCycle (complex G)))
      exact Subtype.ext rfl
  right_inverse q := by
    induction q using Quotient.inductionOn with
    | _ x => rfl

end PreMssn.GraphHomology

namespace PreMssn.GraphHomology.Finite

/-- A finite closure calculation for the bounded runtime replay. Its comparison
with the other runtimes is tested separately from the carrier-general theorem. -/
def adjacent (endpoints : List Int) (a b : Nat) : Bool :=
  (List.range (endpoints.length / 2)).any fun k =>
    let s := endpoints.getD (2*k) 0
    let t := endpoints.getD (2*k+1) 0
    (s == (a : Int) && t == (b : Int)) || (s == (b : Int) && t == (a : Int))

def reach (n : Nat) (endpoints : List Int) (v : Nat) : Nat → List Nat
  | 0 => [v]
  | k+1 =>
    let old := reach n endpoints v k
    (List.range n).filter fun w => old.any fun x => x == w || adjacent endpoints x w

def root (n : Nat) (endpoints : List Int) (v : Nat) : Nat :=
  (reach n endpoints v n).foldl Nat.min v

def componentTotals (n : Nat) (endpoints coefficients : List Int) : List Int :=
  ((List.range n).filter (fun v => root n endpoints v == v)).flatMap fun (v : Nat) =>
    [(v : Int), ((List.range n).map fun w =>
      if root n endpoints w == v then coefficients.getD w 0 else 0).sum]

end PreMssn.GraphHomology.Finite
