import FiniteCoordinates

/-! The effect of a declared added edge on actual connected components.
Cardinality statements use enumerations of the quotient carriers, not a
runtime union-find result assumed equal to the mathematical quotient. -/
namespace PreMssn.GraphExtensions
open GraphHomology
open Lean.Grind
open Homology FreeAbelian
universe u v

def addEdge (G : Graph.{u}) (a b : G.Vertex) : Graph where
  Vertex := G.Vertex
  Edge := Sum G.Edge PUnit
  source := fun e => match e with | .inl e => G.source e | .inr _ => a
  target := fun e => match e with | .inl e => G.target e | .inr _ => b

theorem connected_old (G : Graph.{u}) (a b : G.Vertex) {v w : G.Vertex}
    (h : Connected G v w) : Connected (addEdge G a b) v w := by
  induction h with
  | refl v => exact Connected.refl (G := addEdge G a b) v
  | edge e => exact Connected.edge (G := addEdge G a b) (Sum.inl e)
  | symm _ ih => exact .symm ih
  | trans _ _ ih₁ ih₂ => exact .trans ih₁ ih₂

def componentMap (G : Graph.{u}) (a b : G.Vertex) : Component G → Component (addEdge G a b) :=
  fun q => Quotient.liftOn q (component (addEdge G a b))
    (fun _ _ h => Quotient.sound (connected_old G a b h))

theorem component_map_surjective (G : Graph.{u}) (a b : G.Vertex)
    (q : Component (addEdge G a b)) : ∃ p, componentMap G a b p = q := by
  induction q using Quotient.inductionOn with
  | _ v => exact ⟨component G v, rfl⟩

theorem connected_added_iff (G : Graph.{u}) (a b : G.Vertex) (hab : Connected G a b)
    (v w : G.Vertex) : Connected (addEdge G a b) v w ↔ Connected G v w := by
  constructor
  · intro h
    induction h using Connected.rec (G := addEdge G a b) with
    | refl v => exact Connected.refl (G := G) v
    | edge e =>
      cases e with
      | inl e => exact Connected.edge (G := G) e
      | inr _ => exact hab
    | symm _ ih => exact .symm ih
    | trans _ _ ih₁ ih₂ => exact .trans ih₁ ih₂
  · exact connected_old G a b

theorem component_map_injective_iff (G : Graph.{u}) (a b : G.Vertex) :
    (∀ p q, componentMap G a b p = componentMap G a b q → p = q) ↔ Connected G a b := by
  constructor
  · intro injective
    have h : componentMap G a b (component G a) = componentMap G a b (component G b) :=
      Quotient.sound (Connected.edge (G := addEdge G a b) (.inr PUnit.unit))
    exact (component_eq_iff G a b).mp (injective _ _ h)
  · intro hab p q h
    induction p, q using Quotient.inductionOn₂ with
    | _ v w =>
      exact Quotient.sound ((connected_added_iff G a b hab v w).mp (Quotient.exact h))

theorem finite_surjection_card_le {n m : Nat} (f : Fin n → Fin m)
    (onto : ∀ j, ∃ i, f i = j) : m ≤ n := by
  classical
  let g : Fin m → Fin n := fun j => Classical.choose (onto j)
  have hg : ∀ j, f (g j) = j := fun j => Classical.choose_spec (onto j)
  apply finite_injection_card_le g
  intro j k h
  rw [← hg j, ← hg k, h]

/-- A collision in a finite surjection forces a strictly smaller target. -/
theorem finite_collision_card_lt {n m : Nat} (f : Fin n → Fin m)
    (onto : ∀ j, ∃ i, f i = j) (a b : Fin n) (distinct : a ≠ b)
    (collision : f a = f b) : m < n := by
  classical
  let g : Fin m → Fin n := fun j => Classical.choose (onto j)
  have hg : ∀ j, f (g j) = j := fun j => Classical.choose_spec (onto j)
  have injective : ∀ j k, g j = g k → j = k := by
    intro j k h
    rw [← hg j, ← hg k, h]
  have missing : ∃ z : Fin n, ∀ j, g j ≠ z := by
    by_cases ha : ∃ j, g j = a
    · obtain ⟨j, hj⟩ := ha
      refine ⟨b, ?_⟩
      intro k hk
      have jk : j = k := by rw [← hg j, ← hg k, hj, hk, collision]
      exact distinct (hj.symm.trans ((congrArg g jk).trans hk))
    · exact ⟨a, fun j h => ha ⟨j, h⟩⟩
  obtain ⟨z, hz⟩ := missing
  have nodup : ((List.finRange m).map g).Nodup := by
    apply List.pairwise_map.mpr
    exact (List.nodup_finRange m).imp (fun hne heq => hne (injective _ _ heq))
  have extended : (z :: (List.finRange m).map g).Nodup := by
    apply List.nodup_cons.mpr
    refine ⟨?_, nodup⟩
    intro h
    obtain ⟨j, _, hj⟩ := List.mem_map.mp h
    exact hz j hj
  have bound := extended.length_le_of_subset (l₂ := List.finRange n)
    (fun _ _ => List.mem_finRange _)
  have hbound : m + 1 ≤ n := by simpa using bound
  omega

structure Enumeration (A : Type u) (n : Nat) where
  number : A → Fin n
  representative : Fin n → A
  left_inverse : ∀ a, representative (number a) = a
  right_inverse : ∀ i, number (representative i) = i

def Enumeration.map {A : Type u} {B : Type v} {n m : Nat}
    (a : Enumeration A n) (b : Enumeration B m) (f : A → B) : Fin n → Fin m :=
  fun i => b.number (f (a.representative i))

theorem enumeration_map_surjective {A : Type u} {B : Type v} {n m : Nat}
    (a : Enumeration A n) (b : Enumeration B m) (f : A → B)
    (onto : ∀ y, ∃ x, f x = y) : ∀ j, ∃ i, a.map b f i = j := by
  intro j
  obtain ⟨x, hx⟩ := onto (b.representative j)
  refine ⟨a.number x, ?_⟩
  change b.number (f (a.representative (a.number x))) = j
  rw [a.left_inverse, hx, b.right_inverse]

theorem enumeration_injection_card_le {A : Type u} {B : Type v} {n m : Nat}
    (a : Enumeration A n) (b : Enumeration B m) (f : A → B)
    (injective : ∀ x y, f x = f y → x = y) : n ≤ m := by
  apply finite_injection_card_le (a.map b f)
  intro i j h
  have h' := congrArg b.representative h
  change b.representative (b.number (f (a.representative i))) =
    b.representative (b.number (f (a.representative j))) at h'
  rw [b.left_inverse, b.left_inverse] at h'
  have h'' := congrArg a.number (injective _ _ h')
  simpa only [a.right_inverse] using h''

theorem enumeration_surjection_card_le {A : Type u} {B : Type v} {n m : Nat}
    (a : Enumeration A n) (b : Enumeration B m) (f : A → B)
    (onto : ∀ y, ∃ x, f x = y) : m ≤ n :=
  finite_surjection_card_le (a.map b f) (enumeration_map_surjective a b f onto)

theorem enumeration_collision_card_lt {A : Type u} {B : Type v} {n m : Nat}
    (a : Enumeration A n) (b : Enumeration B m) (f : A → B)
    (onto : ∀ y, ∃ x, f x = y) (x y : A) (distinct : x ≠ y) (collision : f x = f y) :
    m < n := by
  apply finite_collision_card_lt (a.map b f) (enumeration_map_surjective a b f onto)
    (a.number x) (a.number y)
  · intro h
    apply distinct
    rw [← a.left_inverse x, ← a.left_inverse y, h]
  · change b.number (f (a.representative (a.number x))) =
      b.number (f (a.representative (a.number y)))
    rw [a.left_inverse, a.left_inverse, collision]

theorem component_count_after_edge (G : Graph.{u}) (a b : G.Vertex) {n m : Nat}
    (old : Enumeration (Component G) n) (new : Enumeration (Component (addEdge G a b)) m) :
    m ≤ n ∧ (m = n ↔ Connected G a b) ∧ (m < n ↔ ¬Connected G a b) := by
  have le := enumeration_surjection_card_le old new (componentMap G a b)
    (component_map_surjective G a b)
  have same (hab : Connected G a b) : m = n := Nat.le_antisymm le
    (enumeration_injection_card_le old new (componentMap G a b)
      ((component_map_injective_iff G a b).mpr hab))
  have drops (hab : ¬Connected G a b) : m < n := by
    apply enumeration_collision_card_lt old new (componentMap G a b)
      (component_map_surjective G a b) (component G a) (component G b)
    · intro h
      exact hab ((component_eq_iff G a b).mp h)
    · exact Quotient.sound (Connected.edge (G := addEdge G a b) (.inr PUnit.unit))
  refine ⟨le, ⟨?_, same⟩, ⟨?_, drops⟩⟩
  · intro h
    classical
    by_cases hab : Connected G a b
    · exact hab
    · have d := drops hab
      omega
  · intro h hab
    have eq := same hab
    omega

theorem connected_eq_of_loops (G : Graph.{u}) (loops : ∀ e, G.source e = G.target e)
    {a b : G.Vertex} (h : Connected G a b) : a = b := by
  induction h with
  | refl _ => rfl
  | edge e => exact loops e
  | symm _ ih => exact ih.symm
  | trans _ _ ih₁ ih₂ => exact ih₁.trans ih₂

theorem component_count_maximum (G : Graph.{u}) {n c : Nat}
    (vertices : Enumeration G.Vertex n) (components : Enumeration (Component G) c) :
    c ≤ n ∧ (c = n ↔ ∀ e, G.source e = G.target e) := by
  have onto : ∀ q : Component G, ∃ v, component G v = q := by
    intro q
    induction q using Quotient.inductionOn with
    | _ v => exact ⟨v, rfl⟩
  have le := enumeration_surjection_card_le vertices components (component G) onto
  refine ⟨le, ?_, ?_⟩
  · intro h e
    classical
    by_cases endpoints : G.source e = G.target e
    · exact endpoints
    · have drop := enumeration_collision_card_lt vertices components (component G) onto
        (G.source e) (G.target e) endpoints (Quotient.sound (Connected.edge e))
      omega
  · intro loops
    apply Nat.le_antisymm le
    apply enumeration_injection_card_le vertices components (component G)
    intro a b h
    exact connected_eq_of_loops G loops ((component_eq_iff G a b).mp h)

def graphH1Complex (G : Graph.{u}) : Complex where
  upper := PUnit
  middle := Free G.Edge
  lower := Free G.Vertex
  boundary := AddHom.zero _ _
  differential := GraphHomology.boundary G
  square_zero _ := (GraphHomology.boundary G).map_zero

def loopCycle (G : Graph.{u}) (e : G.Edge) (loop : G.target e = G.source e) :
    Cycle (graphH1Complex G) := ⟨gen e, loop_boundary_zero G e loop⟩

def loopH1Class (G : Graph.{u}) (e : G.Edge) (loop : G.target e = G.source e) :
    Homology (graphH1Complex G) :=
  quotientProjection (boundaryCycle (graphH1Complex G)) (loopCycle G e loop)

/-- With no two-cells, each actual loop edge gives a nonzero integral H1 class. -/
theorem loop_h1_nonzero (G : Graph.{u}) (e : G.Edge) (loop : G.target e = G.source e) :
    loopH1Class G e loop ≠ 0 := by
  intro h
  obtain ⟨b, hb⟩ := (quotient_class_zero_iff (boundaryCycle (graphH1Complex G)) _).mp h
  have bad := congrArg (fun z : Cycle (graphH1Complex G) =>
    extend (fun _ : G.Edge => (1 : Int)) z.val) hb
  change (0 : Int) = 1 at bad
  contradiction

end PreMssn.GraphExtensions
