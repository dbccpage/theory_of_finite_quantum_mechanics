import Mathlib.Data.Set.Lattice

/-! AuthorityEffect: None. Exact FD closure and strict replay soundness,
projected implications, row equality, and the sufficient binary lossless FD
criterion. Rust bitsets, enumeration completeness, budgets, error order and
the converse database criterion require separate source/native evidence. -/
namespace TFQM.FunctionalDependencies
variable {A V : Type}
abbrev FD (A : Type) := Set A × Set A
def Closed (cover : Set (FD A)) (s : Set A) : Prop :=
  ∀ f ∈ cover, f.1 ⊆ s → f.2 ⊆ s
def closure (cover : Set (FD A)) (x : Set A) : Set A :=
  {a | ∀ s, x ⊆ s → Closed cover s → a ∈ s}

theorem extensive (cover : Set (FD A)) (x : Set A) : x ⊆ closure cover x := by
  intro a ha s hs _
  exact hs ha
theorem least (cover : Set (FD A)) (x s : Set A) (hx : x ⊆ s)
    (hc : Closed cover s) : closure cover x ⊆ s := by
  intro a ha
  exact ha s hx hc
theorem closure_closed (cover : Set (FD A)) (x : Set A) : Closed cover (closure cover x) := by
  intro f hf hdet a ha s hs hc
  apply hc f hf _ ha
  intro b hb
  exact hdet hb s hs hc
theorem monotone (cover : Set (FD A)) {x y : Set A} (h : x ⊆ y) :
    closure cover x ⊆ closure cover y := by
  intro a ha s hs hc
  exact ha s (h.trans hs) hc
theorem idempotent (cover : Set (FD A)) (x : Set A) :
    closure cover (closure cover x) = closure cover x :=
  Set.Subset.antisymm (least _ _ _ (Set.Subset.refl _) (closure_closed _ _)) (extensive _ _)
theorem implication (cover : Set (FD A)) (f : FD A) (hf : f ∈ cover) :
    f.2 ⊆ closure cover f.1 :=
  closure_closed cover f.1 f hf (extensive cover f.1)

inductive Replay (cover : Set (FD A)) (x : Set A) : Set A → Prop
  | start : Replay cover x x
  | step {s : Set A} (prior : Replay cover x s) (f : FD A) (member : f ∈ cover)
      (enabled : f.1 ⊆ s) : Replay cover x (s ∪ f.2)

theorem replay_extensive {cover : Set (FD A)} {x s : Set A} (h : Replay cover x s) : x ⊆ s := by
  induction h with
  | start => exact Set.Subset.refl _
  | step _ _ _ _ ih => exact ih.trans Set.subset_union_left
theorem replay_sound {cover : Set (FD A)} {x s : Set A} (h : Replay cover x s) :
    s ⊆ closure cover x := by
  induction h with
  | start => exact extensive _ _
  | step _ f hf enabled ih =>
    exact Set.union_subset ih (closure_closed _ _ f hf (enabled.trans ih))
theorem accepted_exact {cover : Set (FD A)} {x s : Set A}
    (replay : Replay cover x s) (closed : Closed cover s) : s = closure cover x :=
  Set.Subset.antisymm (replay_sound replay) (least _ _ _ (replay_extensive replay) closed)
theorem projected_implication (cover : Set (FD A)) (x component : Set A) :
    {a | a ∈ closure cover x ∧ a ∈ component ∧ a ∉ x} ⊆ closure cover x := by
  intro a ha
  exact ha.1
theorem nontrivial_projected (cover : Set (FD A)) (x component : Set A) :
    Disjoint ({a | a ∈ closure cover x ∧ a ∈ component ∧ a ∉ x}) x := by
  apply Set.disjoint_left.mpr
  intro a h hx
  exact h.2.2 hx

def Agree (indices : Set A) (a b : A → V) : Prop := ∀ i ∈ indices, a i = b i
def Satisfies (rows : Set (A → V)) (f : FD A) : Prop :=
  ∀ a ∈ rows, ∀ b ∈ rows, Agree f.1 a b → Agree f.2 a b
theorem agree_refl (indices : Set A) (a : A → V) : Agree indices a a := by
  intro _ _
  rfl
theorem agree_symm {indices : Set A} {a b : A → V} (h : Agree indices a b) : Agree indices b a := by
  intro i hi
  exact (h i hi).symm
theorem agree_trans {indices : Set A} {a b c : A → V}
    (h : Agree indices a b) (k : Agree indices b c) : Agree indices a c := by
  intro i hi
  exact (h i hi).trans (k i hi)
theorem agree_restrict {small large : Set A} {a b : A → V}
    (h : small ⊆ large) (same : Agree large a b) : Agree small a b := by
  intro i hi
  exact same i (h hi)

def join (rows : Set (A → V)) (left right : Set A) : Set (A → V) :=
  {r | (∃ a ∈ rows, Agree left r a) ∧ (∃ b ∈ rows, Agree right r b)}
theorem join_extensive (rows : Set (A → V)) (left right : Set A) : rows ⊆ join rows left right := by
  intro r hr
  exact ⟨⟨r, hr, agree_refl _ _⟩, ⟨r, hr, agree_refl _ _⟩⟩
theorem lossless_left (rows : Set (A → V)) (left right : Set A)
    (cover : left ∪ right = Set.univ) (fd : Satisfies rows (left ∩ right, left)) :
    join rows left right = rows := by
  apply Set.Subset.antisymm _ (join_extensive _ _ _)
  rintro r ⟨⟨a, ha, ra⟩, ⟨b, hb, rb⟩⟩
  have ab : Agree (left ∩ right) a b := by
    intro i hi
    exact (ra i hi.1).symm.trans (rb i hi.2)
  have full : r = b := by
    funext i
    have member : i ∈ left ∪ right := by rw [cover]; trivial
    rcases member with hleft | hright
    · exact (ra i hleft).trans (fd a ha b hb ab i hleft)
    · exact rb i hright
  simpa only [full] using hb
theorem lossless_right (rows : Set (A → V)) (left right : Set A)
    (cover : left ∪ right = Set.univ) (fd : Satisfies rows (left ∩ right, right)) :
    join rows left right = rows := by
  have swapped : join rows left right = join rows right left := by
    ext r
    exact And.comm
  rw [swapped]
  apply lossless_left rows right left
  · simpa only [Set.union_comm] using cover
  · simpa only [Set.inter_comm] using fd
end TFQM.FunctionalDependencies

#print axioms TFQM.FunctionalDependencies.extensive
#print axioms TFQM.FunctionalDependencies.least
#print axioms TFQM.FunctionalDependencies.closure_closed
#print axioms TFQM.FunctionalDependencies.monotone
#print axioms TFQM.FunctionalDependencies.idempotent
#print axioms TFQM.FunctionalDependencies.implication
#print axioms TFQM.FunctionalDependencies.replay_extensive
#print axioms TFQM.FunctionalDependencies.replay_sound
#print axioms TFQM.FunctionalDependencies.accepted_exact
#print axioms TFQM.FunctionalDependencies.projected_implication
#print axioms TFQM.FunctionalDependencies.nontrivial_projected
#print axioms TFQM.FunctionalDependencies.agree_refl
#print axioms TFQM.FunctionalDependencies.agree_symm
#print axioms TFQM.FunctionalDependencies.agree_trans
#print axioms TFQM.FunctionalDependencies.agree_restrict
#print axioms TFQM.FunctionalDependencies.join_extensive
#print axioms TFQM.FunctionalDependencies.lossless_left
#print axioms TFQM.FunctionalDependencies.lossless_right
