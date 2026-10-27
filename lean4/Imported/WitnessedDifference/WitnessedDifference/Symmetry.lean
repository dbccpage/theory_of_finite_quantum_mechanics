/- Imported so that this repository carries its own Lean evidence.
   Original sha256: 5cbc349795aa927aca9a850768d539bc478ab1cca8a7367b1f7458bed8260f90 (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.WitnessedDifference.WitnessedDifference.Symmetry
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.WitnessedDifference.WitnessedDifference.Core

/-!
# Finite symmetry boundaries

These results concern a declared full permutation action on one finite carrier.
They do not construct a preferred point, order, or orientation.
-/

namespace WitnessedDifference.Symmetry

def FullyInvariantPoint {α : Type _} (x : α) : Prop :=
  ∀ σ : Equiv.Perm α, σ x = x

def PermutationInvariantSet {α : Type _} (s : Set α) : Prop :=
  ∀ (σ : Equiv.Perm α) (x : α), x ∈ s ↔ σ x ∈ s

theorem invariant_point_forces_all_equal
    {α : Type _} [DecidableEq α] {x : α}
    (hx : FullyInvariantPoint x) (y : α) : y = x := by
  have hswap : (Equiv.swap x y) x = y := Equiv.swap_apply_left x y
  have hinv : (Equiv.swap x y) x = x := hx (Equiv.swap x y)
  rw [← hswap, hinv]

theorem no_fully_invariant_point
    {α : Type _} [Fintype α] [DecidableEq α] [Nontrivial α] :
    ¬ ∃ x : α, FullyInvariantPoint x := by
  rintro ⟨x, hx⟩
  obtain ⟨y, hy⟩ := exists_ne x
  exact hy (invariant_point_forces_all_equal hx y)

theorem invariant_set_empty_or_univ
    {α : Type _} [Fintype α] [DecidableEq α]
    (s : Set α) (hs : PermutationInvariantSet s) :
    s = ∅ ∨ s = Set.univ := by
  by_cases hnonempty : s.Nonempty
  · right
    funext x
    apply propext
    constructor
    · intro _
      trivial
    · intro _
      obtain ⟨a, ha⟩ := hnonempty
      have hmem := (hs (Equiv.swap a x) a).mp ha
      have hswap : (Equiv.swap a x) a = x := Equiv.swap_apply_left a x
      rw [hswap] at hmem
      exact hmem
  · left
    funext x
    apply propext
    constructor
    · intro hx
      exact False.elim (hnonempty ⟨x, hx⟩)
    · intro hx
      exact False.elim hx

theorem no_invariant_oriented_edge
    {α : Type _} [Fintype α] [DecidableEq α]
    {a b : α} (hab : a ≠ b) :
    ¬ ∀ σ : Equiv.Perm α, (σ a, σ b) = (a, b) := by
  intro hinvariant
  have hpair := hinvariant (Equiv.swap a b)
  have hswap : (Equiv.swap a b) a = b := Equiv.swap_apply_left a b
  have hfst : ((Equiv.swap a b) a, (Equiv.swap a b) b).1 = a := congrArg Prod.fst hpair
  dsimp only at hfst
  rw [hswap] at hfst
  exact hab hfst.symm

end WitnessedDifference.Symmetry
