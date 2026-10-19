import Mathlib.Data.Set.Lattice

/-! AuthorityEffect: None. Greatest strong report-respecting bisimulation,
bounded-map fibers/factors and positive reachability/SCC order. Finite Rust
refinement, canonical identifiers, Warshall storage and replay are separate
source/native obligations; no trace/HoTT equivalence is inferred. -/
namespace TFQM.FiniteRelational
variable {X Y I O C : Type}

def Bisim (obs : X → O) (edge : X → I → X → Prop) (r : X → X → Prop) : Prop :=
  ∀ x y, r x y → obs x = obs y ∧ ∀ i,
    (∀ u, edge x i u → ∃ v, edge y i v ∧ r u v) ∧
    (∀ v, edge y i v → ∃ u, edge x i u ∧ r u v)
theorem equality_bisim (obs : X → O) (edge : X → I → X → Prop) : Bisim obs edge Eq := by
  intro x y same
  subst y
  exact ⟨rfl, fun _ => ⟨fun u hu => ⟨u, hu, rfl⟩, fun v hv => ⟨v, hv, rfl⟩⟩⟩
theorem flip_bisim {obs : X → O} {edge : X → I → X → Prop} {r : X → X → Prop}
    (h : Bisim obs edge r) : Bisim obs edge (fun x y => r y x) := by
  intro x y same
  obtain ⟨reports, steps⟩ := h y x same
  refine ⟨reports.symm, fun i => ⟨?_, ?_⟩⟩
  · intro u hu
    obtain ⟨v, hv, related⟩ := (steps i).2 u hu
    exact ⟨v, hv, related⟩
  · intro v hv
    obtain ⟨u, hu, related⟩ := (steps i).1 v hv
    exact ⟨u, hu, related⟩
theorem compose_bisim {obs : X → O} {edge : X → I → X → Prop} {r s : X → X → Prop}
    (hr : Bisim obs edge r) (hs : Bisim obs edge s) :
    Bisim obs edge (fun x z => ∃ y, r x y ∧ s y z) := by
  rintro x z ⟨y, rxy, syz⟩
  obtain ⟨a, ar⟩ := hr x y rxy
  obtain ⟨b, br⟩ := hs y z syz
  refine ⟨a.trans b, fun i => ⟨?_, ?_⟩⟩
  · intro u hu
    obtain ⟨v, hv, ruv⟩ := (ar i).1 u hu
    obtain ⟨w, hw, svw⟩ := (br i).1 v hv
    exact ⟨w, hw, v, ruv, svw⟩
  · intro w hw
    obtain ⟨v, hv, svw⟩ := (br i).2 w hw
    obtain ⟨u, hu, ruv⟩ := (ar i).2 v hv
    exact ⟨u, hu, v, ruv, svw⟩

def Greatest (obs : X → O) (edge : X → I → X → Prop) (x y : X) : Prop :=
  ∃ r, Bisim obs edge r ∧ r x y
theorem contains {obs : X → O} {edge : X → I → X → Prop} {r : X → X → Prop}
    (h : Bisim obs edge r) {x y : X} (same : r x y) : Greatest obs edge x y := ⟨r, h, same⟩
theorem greatest_refl (obs : X → O) (edge : X → I → X → Prop) (x : X) : Greatest obs edge x x :=
  contains (equality_bisim obs edge) rfl
theorem greatest_symm {obs : X → O} {edge : X → I → X → Prop} {x y : X}
    (h : Greatest obs edge x y) : Greatest obs edge y x := by
  obtain ⟨r, hr, same⟩ := h
  exact contains (flip_bisim hr) same
theorem greatest_trans {obs : X → O} {edge : X → I → X → Prop} {x y z : X}
    (h : Greatest obs edge x y) (k : Greatest obs edge y z) : Greatest obs edge x z := by
  obtain ⟨r, hr, rxy⟩ := h
  obtain ⟨s, hs, syz⟩ := k
  exact contains (compose_bisim hr hs) ⟨y, rxy, syz⟩
theorem greatest_bisim (obs : X → O) (edge : X → I → X → Prop) :
    Bisim obs edge (Greatest obs edge) := by
  rintro x y ⟨r, hr, same⟩
  obtain ⟨reports, steps⟩ := hr x y same
  refine ⟨reports, fun i => ⟨?_, ?_⟩⟩
  · intro u hu
    obtain ⟨v, hv, related⟩ := (steps i).1 u hu
    exact ⟨v, hv, contains hr related⟩
  · intro v hv
    obtain ⟨u, hu, related⟩ := (steps i).2 v hv
    exact ⟨u, hu, contains hr related⟩
theorem greatest_reports {obs : X → O} {edge : X → I → X → Prop} {x y : X}
    (h : Greatest obs edge x y) : obs x = obs y := (greatest_bisim obs edge x y h).1

def Bounded (obs : X → O) (edge : X → I → X → Prop) (out : Y → O)
    (target : Y → I → Y → Prop) (q : X → Y) : Prop :=
  (∀ x, obs x = out (q x)) ∧
    ∀ x i y, target (q x) i y ↔ ∃ u, edge x i u ∧ q u = y
theorem bounded_kernel {obs : X → O} {edge : X → I → X → Prop} {out : Y → O}
    {target : Y → I → Y → Prop} {q : X → Y} (h : Bounded obs edge out target q) :
    Bisim obs edge (fun x y => q x = q y) := by
  intro x y same
  refine ⟨(h.1 x).trans ((congrArg out same).trans (h.1 y).symm), fun i => ⟨?_, ?_⟩⟩
  · intro u hu
    have targetEdge := (h.2 x i (q u)).mpr ⟨u, hu, rfl⟩
    rw [same] at targetEdge
    obtain ⟨v, hv, equal⟩ := (h.2 y i (q u)).mp targetEdge
    exact ⟨v, hv, equal.symm⟩
  · intro v hv
    have targetEdge := (h.2 y i (q v)).mpr ⟨v, hv, rfl⟩
    rw [← same] at targetEdge
    exact (h.2 x i (q v)).mp targetEdge
theorem bounded_fibers {obs : X → O} {edge : X → I → X → Prop} {out : Y → O}
    {target : Y → I → Y → Prop} {q : X → Y} (h : Bounded obs edge out target q)
    {x y : X} (same : q x = q y) : Greatest obs edge x y := contains (bounded_kernel h) same
noncomputable def factor (q : X → Y) (onto : Function.Surjective q) (classes : X → C) (y : Y) : C :=
  classes (Classical.choose (onto y))
theorem factor_spec (q : X → Y) (onto : Function.Surjective q) (classes : X → C)
    (fibers : ∀ x y, q x = q y → classes x = classes y) (x : X) :
    factor q onto classes (q x) = classes x :=
  fibers _ _ (Classical.choose_spec (onto (q x)))
theorem factor_unique (q : X → Y) (onto : Function.Surjective q) (classes : X → C)
    (f g : Y → C) (hf : ∀ x, f (q x) = classes x) (hg : ∀ x, g (q x) = classes x) : f = g := by
  funext y
  obtain ⟨x, rfl⟩ := onto y
  exact (hf x).trans (hg x).symm
theorem coverage_iff (a : X → C) (b : Y → C) :
    Set.range a = Set.range b ↔ (∀ x, ∃ y, a x = b y) ∧ (∀ y, ∃ x, a x = b y) := by
  constructor
  · intro same
    constructor
    · intro x
      have member : a x ∈ Set.range b := by rw [← same]; exact ⟨x, rfl⟩
      obtain ⟨y, hy⟩ := member
      exact ⟨y, hy.symm⟩
    · intro y
      have member : b y ∈ Set.range a := by rw [same]; exact ⟨y, rfl⟩
      exact member
  · rintro ⟨ab, ba⟩
    apply Set.Subset.antisymm
    · rintro c ⟨x, rfl⟩
      obtain ⟨y, hy⟩ := ab x
      exact ⟨y, hy.symm⟩
    · rintro c ⟨y, rfl⟩
      exact ba y

inductive Reach (edge : X → X → Prop) : X → X → Prop
  | edge {x y} : edge x y → Reach edge x y
  | trans {x y z} : Reach edge x y → Reach edge y z → Reach edge x z
theorem reach_trans {edge : X → X → Prop} {x y z : X}
    (h : Reach edge x y) (k : Reach edge y z) : Reach edge x z := .trans h k
theorem reach_least {edge r : X → X → Prop} (containsEdge : ∀ x y, edge x y → r x y)
    (trans : ∀ x y z, r x y → r y z → r x z) {x y : X} (path : Reach edge x y) : r x y := by
  induction path with
  | edge h => exact containsEdge _ _ h
  | trans _ _ ih ik => exact trans _ _ _ ih ik
def Le (edge : X → X → Prop) (x y : X) : Prop := x = y ∨ Reach edge x y
theorem le_refl (edge : X → X → Prop) (x : X) : Le edge x x := Or.inl rfl
theorem le_trans {edge : X → X → Prop} {x y z : X} (h : Le edge x y) (k : Le edge y z) : Le edge x z := by
  rcases h with rfl | h
  · exact k
  rcases k with rfl | k
  · exact Or.inr h
  exact Or.inr (.trans h k)
def SCC (edge : X → X → Prop) (x y : X) : Prop := Le edge x y ∧ Le edge y x
theorem scc_refl (edge : X → X → Prop) (x : X) : SCC edge x x := ⟨le_refl _ _, le_refl _ _⟩
theorem scc_symm {edge : X → X → Prop} {x y : X} (h : SCC edge x y) : SCC edge y x := h.symm
theorem scc_trans {edge : X → X → Prop} {x y z : X} (h : SCC edge x y) (k : SCC edge y z) : SCC edge x z :=
  ⟨le_trans h.1 k.1, le_trans k.2 h.2⟩
theorem representative_invariant {edge : X → X → Prop} {x x' y y' : X}
    (a : SCC edge x x') (b : SCC edge y y') : Le edge x y ↔ Le edge x' y' :=
  ⟨fun h => le_trans a.2 (le_trans h b.1), fun h => le_trans a.1 (le_trans h b.2)⟩
def Strict (edge : X → X → Prop) (x y : X) : Prop := Le edge x y ∧ ¬Le edge y x
theorem strict_irreflexive (edge : X → X → Prop) (x : X) : ¬Strict edge x x := fun h => h.2 h.1
theorem strict_trans {edge : X → X → Prop} {x y z : X}
    (h : Strict edge x y) (k : Strict edge y z) : Strict edge x z :=
  ⟨le_trans h.1 k.1, fun reverse => k.2 (le_trans reverse h.1)⟩
theorem distinct_components_strict {edge : X → X → Prop} {x y : X}
    (forward : Le edge x y) (different : ¬SCC edge x y) : Strict edge x y :=
  ⟨forward, fun reverse => different ⟨forward, reverse⟩⟩
end TFQM.FiniteRelational

#print axioms TFQM.FiniteRelational.equality_bisim
#print axioms TFQM.FiniteRelational.flip_bisim
#print axioms TFQM.FiniteRelational.compose_bisim
#print axioms TFQM.FiniteRelational.contains
#print axioms TFQM.FiniteRelational.greatest_refl
#print axioms TFQM.FiniteRelational.greatest_symm
#print axioms TFQM.FiniteRelational.greatest_trans
#print axioms TFQM.FiniteRelational.greatest_bisim
#print axioms TFQM.FiniteRelational.greatest_reports
#print axioms TFQM.FiniteRelational.bounded_kernel
#print axioms TFQM.FiniteRelational.bounded_fibers
#print axioms TFQM.FiniteRelational.factor_spec
#print axioms TFQM.FiniteRelational.factor_unique
#print axioms TFQM.FiniteRelational.coverage_iff
#print axioms TFQM.FiniteRelational.reach_trans
#print axioms TFQM.FiniteRelational.reach_least
#print axioms TFQM.FiniteRelational.le_refl
#print axioms TFQM.FiniteRelational.le_trans
#print axioms TFQM.FiniteRelational.scc_refl
#print axioms TFQM.FiniteRelational.scc_symm
#print axioms TFQM.FiniteRelational.scc_trans
#print axioms TFQM.FiniteRelational.representative_invariant
#print axioms TFQM.FiniteRelational.strict_irreflexive
#print axioms TFQM.FiniteRelational.strict_trans
#print axioms TFQM.FiniteRelational.distinct_components_strict
