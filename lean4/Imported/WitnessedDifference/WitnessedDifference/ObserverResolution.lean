/- Imported so that this repository carries its own Lean evidence.
   Original sha256: 3c448fed2801b6e91a5b463a8b44d5d98bb5c8475dc0d1ddb66221966a81bc18 (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.WitnessedDifference.WitnessedDifference.ObserverResolution
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.WitnessedDifference.WitnessedDifference.Core

/-!
# Observer resolution

An observer is a report type together with a report map on a fixed core
carrier. Kernel inclusion orders observers by coarse-graining: `KernelLe O P`
holds when every pair of core elements identified by `O` is also identified by
`P`. The order is a preorder, becomes antisymmetric modulo equal kernels, has
the identity observer as a finest element and the observer into `Unit` as a
coarsest element. An observer is finest exactly when its report map is
injective.

A finite report grammar bounds resolution: a report map from `Fin n` into
`Fin m` with `m < n` has a collision (pigeonhole), so such an observer is not
finest. The proofs use only Lean core.
-/

namespace WitnessedDifference.ObserverResolution

/-! ## Observers and the kernel order -/

structure Observer (Q : Type) where
  Report : Type
  map : Q → Report

/-- `KernelLe O P`: `O` is at least as fine as `P` (`ker O ⊆ ker P`). -/
def KernelLe {Q : Type} (O P : Observer Q) : Prop :=
  ∀ x y : Q, O.map x = O.map y → P.map x = P.map y

def SameKernel {Q : Type} (O P : Observer Q) : Prop :=
  KernelLe O P ∧ KernelLe P O

/-- The identity observer reports the core element itself. -/
def identityObserver (Q : Type) : Observer Q where
  Report := Q
  map := id

/-- The zero observer reports nothing. -/
def unitObserver (Q : Type) : Observer Q where
  Report := Unit
  map := fun _ => ()

theorem observer_kernel_preorder {Q I : Type} (family : I → Observer Q) :
    (∀ i : I, KernelLe (family i) (family i))
      ∧ (∀ i j k : I,
          KernelLe (family i) (family j) →
          KernelLe (family j) (family k) →
          KernelLe (family i) (family k))
      ∧ (∀ i j : I,
          KernelLe (family i) (family j) →
          KernelLe (family j) (family i) →
          SameKernel (family i) (family j)) := by
  refine ⟨?_, ?_, ?_⟩
  · intro _ _ _ hxy
    exact hxy
  · intro _ _ _ hij hjk x y hxy
    exact hjk x y (hij x y hxy)
  · intro _ _ hij hji
    exact ⟨hij, hji⟩

theorem observer_same_kernel_equivalence {Q : Type} :
    Equivalence (@SameKernel Q) := by
  constructor
  · intro _
    exact ⟨fun _ _ h => h, fun _ _ h => h⟩
  · intro _ _ h
    exact ⟨h.2, h.1⟩
  · intro _ _ _ hOP hPR
    exact ⟨
      fun x y hxy => hPR.1 x y (hOP.1 x y hxy),
      fun x y hxy => hOP.2 x y (hPR.2 x y hxy)⟩

theorem identity_observer_finest {Q : Type} (O : Observer Q) :
    KernelLe (identityObserver Q) O := by
  intro x y hxy
  have hsame : x = y := hxy
  rw [hsame]

theorem zero_observer_coarsest {Q : Type} (O : Observer Q) :
    KernelLe O (unitObserver Q) := by
  intro _ _ _
  rfl

/-- An observer is finest in the kernel order exactly when its report map is
injective. -/
theorem finest_iff_injective {Q : Type} (O : Observer Q) :
    (∀ P : Observer Q, KernelLe O P) ↔ _root_.Function.Injective O.map := by
  constructor
  · intro hfinest x y hxy
    exact hfinest (identityObserver Q) x y hxy
  · intro hinj P x y hxy
    rw [hinj hxy]

/-- An observer is coarsest in the kernel order exactly when its report map is
constant. -/
theorem coarsest_iff_constant {Q : Type} (O : Observer Q) :
    (∀ P : Observer Q, KernelLe P O) ↔ ∀ x y : Q, O.map x = O.map y := by
  constructor
  · intro hcoarsest x y
    exact hcoarsest (unitObserver Q) x y rfl
  · intro hconst _ x y _
    exact hconst x y

/-! ## Grammar cardinality and the pigeonhole resolution limit -/

/-- The visible report list of a subgrammar is no longer than the grammar. -/
theorem grammar_cardinality_bound {Report : Type} (visible grammar : List Report)
    (visible_subgrammar : visible.Sublist grammar) :
    visible.length ≤ grammar.length :=
  List.Sublist.length_le visible_subgrammar

theorem grammar_no_injective_visible_count_if_over_capacity {Core Report : Type}
    (classes : List Core) (visible grammar : List Report)
    (visible_subgrammar : visible.Sublist grammar)
    (over_capacity : grammar.length < classes.length) :
    ¬ classes.length ≤ visible.length := by
  intro injective_visible_count
  have hbound : visible.length ≤ grammar.length :=
    grammar_cardinality_bound visible grammar visible_subgrammar
  exact Nat.not_lt_of_ge (Nat.le_trans injective_visible_count hbound) over_capacity

/-- Remove the pivot `i` from an index: indices above `i` shift down by one. -/
def finPredVal (i j : Nat) : Nat :=
  if j < i then j else j - 1

theorem finPredVal_inj (i j1 j2 : Nat) (hj1 : j1 ≠ i) (hj2 : j2 ≠ i)
    (h_eq : finPredVal i j1 = finPredVal i j2) : j1 = j2 := by
  unfold finPredVal at h_eq
  split at h_eq <;> split at h_eq <;> omega

/-- Remove the pivot `i` from `Fin (n + 1)`, landing in `Fin n`. -/
def finPredAbove {n : Nat} (i j : Fin (n + 1)) (hne : j ≠ i) : Fin n :=
  ⟨finPredVal i.1 j.1, by
    unfold finPredVal
    have hj := j.2
    have hi := i.2
    have hne_val : j.1 ≠ i.1 := fun h => hne (Fin.ext h)
    split <;> omega⟩

theorem finPredAbove_inj {n : Nat} (i j1 j2 : Fin (n + 1))
    (h1 : j1 ≠ i) (h2 : j2 ≠ i)
    (heq : finPredAbove i j1 h1 = finPredAbove i j2 h2) :
    j1 = j2 := by
  have heq_val : (finPredAbove i j1 h1).1 = (finPredAbove i j2 h2).1 :=
    congrArg Fin.val heq
  have hne1 : j1.1 ≠ i.1 := fun h => h1 (Fin.ext h)
  have hne2 : j2.1 ≠ i.1 := fun h => h2 (Fin.ext h)
  exact Fin.ext (finPredVal_inj i.1 j1.1 j2.1 hne1 hne2 heq_val)

/-- Pigeonhole: no map from `Fin n` to `Fin m` with `m < n` is injective. -/
theorem not_injective_fin_of_lt :
    ∀ (m n : Nat), m < n → ∀ (f : Fin n → Fin m), ¬ _root_.Function.Injective f
  | 0, _, hlt, f => by
    intro _
    exact Fin.elim0 (f ⟨0, hlt⟩)
  | _ + 1, 0, hlt, _ => by
    omega
  | m + 1, n + 1, hlt, f => by
    intro h_inj
    let target := f ⟨0, Nat.succ_pos n⟩
    have h_ne : ∀ x : Fin n, f ⟨x.1 + 1, Nat.succ_lt_succ x.2⟩ ≠ target := by
      intro x h_eq
      have h_same : (⟨x.1 + 1, Nat.succ_lt_succ x.2⟩ : Fin (n + 1)) =
          ⟨0, Nat.succ_pos n⟩ :=
        h_inj h_eq
      have hval := congrArg Fin.val h_same
      simp at hval
    let g : Fin n → Fin m := fun x =>
      finPredAbove target (f ⟨x.1 + 1, Nat.succ_lt_succ x.2⟩) (h_ne x)
    have g_inj : _root_.Function.Injective g := by
      intro x y hgy
      have hf_eq : f ⟨x.1 + 1, Nat.succ_lt_succ x.2⟩ =
          f ⟨y.1 + 1, Nat.succ_lt_succ y.2⟩ :=
        finPredAbove_inj target _ _ (h_ne x) (h_ne y) hgy
      have hval := congrArg Fin.val (h_inj hf_eq)
      apply Fin.ext
      simp at hval
      exact hval
    exact not_injective_fin_of_lt m n (by omega) g g_inj

/-- An over-capacity report map has an explicit collision. -/
theorem fin_collision_of_lt {n m : Nat} (hlt : m < n) (f : Fin n → Fin m) :
    ∃ x y : Fin n, x ≠ y ∧ f x = f y := by
  apply Classical.byContradiction
  intro hcollision
  have hinj : _root_.Function.Injective f := by
    intro x y hxy
    apply Classical.byContradiction
    intro hne
    exact hcollision ⟨x, y, hne, hxy⟩
  exact not_injective_fin_of_lt m n hlt f hinj

/-- Pigeonhole resolution limit: a report map with fewer reports than core
states identifies two distinct states. -/
theorem pigeonhole_resolution_limit {n m : Nat} (hlt : m < n) (f : Fin n → Fin m) :
    ∃ x y : Fin n, x ≠ y ∧ f x = f y :=
  fin_collision_of_lt hlt f

/-- An observer whose reports come from a grammar smaller than the core is not
finest in the kernel order. -/
theorem grammar_observer_not_finest {n m : Nat} (hlt : m < n) (f : Fin n → Fin m) :
    ¬ ∀ P : Observer (Fin n), KernelLe ⟨Fin m, f⟩ P := by
  intro hfinest
  exact not_injective_fin_of_lt m n hlt f
    ((finest_iff_injective ⟨Fin m, f⟩).mp hfinest)

/-- A report map separating `k` declared core classes needs at least `k`
reports: the visible-class half of the grammar resolution bound. -/
theorem visible_classes_le_grammar {n m k : Nat} (f : Fin n → Fin m) (c : Fin k → Fin n)
    (hsep : ∀ i j, f (c i) = f (c j) → i = j) : k ≤ m := by
  apply Classical.byContradiction
  intro hnot
  have hlt : m < k := by omega
  exact not_injective_fin_of_lt m k hlt (fun i => f (c i)) (fun i j hij => hsep i j hij)

/-- Row WDP-CH10-P03: a report map into `m` reports separates at most `m` core
classes, and when there are more core classes than reports two distinct classes
share a report. -/
theorem grammar_resolution_bound {n m : Nat} (f : Fin n → Fin m) :
    (∀ {k : Nat} (c : Fin k → Fin n), (∀ i j, f (c i) = f (c j) → i = j) → k ≤ m) ∧
    (m < n → ∃ x y : Fin n, x ≠ y ∧ f x = f y) :=
  ⟨fun c hsep => visible_classes_le_grammar f c hsep,
   fun hlt => pigeonhole_resolution_limit hlt f⟩

/-- Row WDP-CH10-P02, bundled: kernel inclusion on a declared family is a
preorder whose mutual inclusions are equal kernels, the identity observer is
finest, and the observer into `Unit` is coarsest. Kernels here are equivalence
kernels of report maps. For a linear map f, f(x)=f(y) exactly when x-y belongs
to its linear zero kernel, so the inclusion comparisons agree. The relation
kernel and the linear zero kernel are different objects. -/
theorem declared_family_order {Q I : Type} (family : I → Observer Q) :
    ((∀ i : I, KernelLe (family i) (family i)) ∧
      (∀ i j k : I, KernelLe (family i) (family j) → KernelLe (family j) (family k) →
        KernelLe (family i) (family k)) ∧
      (∀ i j : I, KernelLe (family i) (family j) → KernelLe (family j) (family i) →
        SameKernel (family i) (family j))) ∧
    (∀ O : Observer Q, KernelLe (identityObserver Q) O) ∧
    (∀ O : Observer Q, KernelLe O (unitObserver Q)) :=
  ⟨observer_kernel_preorder family, identity_observer_finest, zero_observer_coarsest⟩

end WitnessedDifference.ObserverResolution
