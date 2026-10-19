import Mathlib.Logic.Relation

/-! AuthorityEffect: None. Quotient of the supplied tagged relation only.
No category/bifunctor or actual coend admission. Worklist/dense-label predicates
are the source refinement obligations; no extraction of Rust is asserted. -/
namespace TFQM.TaggedCoend

variable {V W : Type} (edge : V → V → Prop)

abbrev Connected := Relation.EqvGen edge

theorem connected_refl (x : V) : Connected edge x x := .refl x
theorem connected_symm {x y : V} (h : Connected edge x y) :
    Connected edge y x := .symm x y h
theorem connected_trans {x y z : V} (h : Connected edge x y)
    (k : Connected edge y z) : Connected edge x z := .trans x y z h k
theorem supplied_pair {x y : V} (h : edge x y) : Connected edge x y := .rel x y h

abbrev Partition := Quotient (Relation.EqvGen.setoid edge)
def project (x : V) : Partition edge := Quotient.mk _ x

theorem projection_exact (x y : V) :
    project edge x = project edge y ↔ Connected edge x y := by
  constructor
  · exact Quotient.exact
  · intro h
    exact @Quotient.sound V (Relation.EqvGen.setoid edge) x y h

theorem respects_closure (f : V → W)
    (respects : ∀ x y, edge x y → f x = f y) {x y : V}
    (h : Connected edge x y) : f x = f y := by
  induction h with
  | rel a b h => exact respects a b h
  | refl a => rfl
  | symm a b _ ih => exact ih.symm
  | trans a b c _ _ ih jk => exact ih.trans jk

def factor (f : V → W) (respects : ∀ x y, edge x y → f x = f y) :
    Partition edge → W :=
  Quotient.lift f (fun _ _ h => respects_closure edge f respects h)

theorem factor_projection (f : V → W)
    (respects : ∀ x y, edge x y → f x = f y) (x : V) :
    factor edge f respects (project edge x) = f x := rfl

theorem factor_unique (f : V → W)
    (respects : ∀ x y, edge x y → f x = f y) (g : Partition edge → W)
    (agrees : ∀ x, g (project edge x) = f x) : g = factor edge f respects := by
  funext q
  exact Quotient.inductionOn q agrees

theorem closed_contains_component (root : V) (seen : V → Prop)
    (start : seen root)
    (forward : ∀ x y, seen x → edge x y → seen y)
    (backward : ∀ x y, seen y → edge x y → seen x)
    {x : V} (h : Connected edge root x) : seen x := by
  have transport : ∀ a b, Connected edge a b → (seen a ↔ seen b) := by
    intro a b p
    induction p with
    | rel a b h => exact ⟨fun s => forward a b s h, fun s => backward a b s h⟩
    | refl a => exact Iff.rfl
    | symm a b _ ih => exact ih.symm
    | trans a b c _ _ ih jk => exact ih.trans jk
  exact (transport root x h).mp start

theorem frontier_fresh_sound (root parent next : V)
    (parentSound : Connected edge root parent) (neighbor : edge parent next) :
    Connected edge root next := .trans root parent next parentSound (.rel parent next neighbor)

theorem frontier_reverse_sound (root parent next : V)
    (parentSound : Connected edge root parent) (neighbor : edge next parent) :
    Connected edge root next :=
  .trans root parent next parentSound (.symm next parent (.rel next parent neighbor))

theorem labels_exact (labels : V → Nat)
    (sound : ∀ x y, labels x = labels y → Connected edge x y)
    (complete : ∀ x y, Connected edge x y → labels x = labels y) (x y : V) :
    labels x = labels y ↔ Connected edge x y := ⟨sound x y, complete x y⟩

theorem dense_nonempty (labels : V → Nat) (count : Nat)
    (dense : ∀ c, c < count → ∃ x, labels x = c) (c : Fin count) :
    ∃ x, labels x = c.val := dense c.val c.isLt

theorem range_after_increment (labels : V → Nat) (count : Nat)
    (range : ∀ x, labels x < count) (x : V) : labels x < count + 1 :=
  Nat.lt_succ_of_lt (range x)

theorem new_root_fits (count : Nat) : count < count + 1 := Nat.lt_succ_self count

theorem component_increment_fits (count vertices maximum : Nat)
    (fresh : count < vertices) (fits : vertices ≤ maximum) : count + 1 ≤ maximum :=
  Nat.le_trans (Nat.succ_le_of_lt fresh) fits

theorem local_equal_no_range (maximum : Nat) : maximum = maximum := rfl

end TFQM.TaggedCoend

#print axioms TFQM.TaggedCoend.connected_refl
#print axioms TFQM.TaggedCoend.connected_symm
#print axioms TFQM.TaggedCoend.connected_trans
#print axioms TFQM.TaggedCoend.supplied_pair
#print axioms TFQM.TaggedCoend.project
#print axioms TFQM.TaggedCoend.projection_exact
#print axioms TFQM.TaggedCoend.respects_closure
#print axioms TFQM.TaggedCoend.factor
#print axioms TFQM.TaggedCoend.factor_projection
#print axioms TFQM.TaggedCoend.factor_unique
#print axioms TFQM.TaggedCoend.closed_contains_component
#print axioms TFQM.TaggedCoend.frontier_fresh_sound
#print axioms TFQM.TaggedCoend.frontier_reverse_sound
#print axioms TFQM.TaggedCoend.labels_exact
#print axioms TFQM.TaggedCoend.dense_nonempty
#print axioms TFQM.TaggedCoend.range_after_increment
#print axioms TFQM.TaggedCoend.new_root_fits
#print axioms TFQM.TaggedCoend.component_increment_fits
#print axioms TFQM.TaggedCoend.local_equal_no_range
