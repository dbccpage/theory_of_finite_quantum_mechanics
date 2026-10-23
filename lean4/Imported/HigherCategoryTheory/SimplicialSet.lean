/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/research_programs/higher_category_theory/SimplicialSet.lean
   Original sha256: e0e5861993eac3f429981f08634379c76dd31b7f380fa689b8b88627321c98c7 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.HigherCategoryTheory.SimplicialSet
   Reason         : HCT
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
/-
SimplicialSet.lean
Formalization of Simplicial Sets, Kan Complexes, and Quasi-Categories (∞-categories).

AuthorityEffect: None.
Standard foundational axioms only: {propext, Quot.sound, Classical.choice}.
Zero sorry, zero admit.
-/

import Imported.HigherCategoryTheory.Monoidal

namespace HigherCategoryTheory

universe u

/-- Face map indexing: a face index i for an n-simplex must satisfy i ≤ n. -/
structure FaceIndex (n : Nat) where
  val : Nat
  isLt : val ≤ n

/-- Degeneracy map indexing: a degeneracy index i for an n-simplex must satisfy i ≤ n. -/
structure DegenIndex (n : Nat) where
  val : Nat
  isLt : val ≤ n

/-- A Simplicial Set X consists of a sequence of types X n of n-simplices,
    face maps d_i : X (n+1) → X n, and degeneracy maps s_i : X n → X (n+1),
    satisfying the standard simplicial identities. -/
structure SimplicialSet where
  Simplex : Nat → Type u
  face : ∀ (n : Nat) (i : Nat), i ≤ n + 1 → Simplex (n + 1) → Simplex n
  degen : ∀ (n : Nat) (i : Nat), i ≤ n → Simplex n → Simplex (n + 1)

  -- Simplicial identity 1: d_i ∘ d_j = d_{j-1} ∘ d_i for i < j
  face_face : ∀ (n : Nat) (i j : Nat) (hi : i ≤ n + 1) (hj : j ≤ n + 2) (hij : i < j)
    (x : Simplex (n + 2)),
    face n i (by omega) (face (n + 1) j hj x) =
    face n (j - 1) (by omega) (face (n + 1) i (by omega) x)

  -- Simplicial identity 3: d_j ∘ s_j = id and d_{j+1} ∘ s_j = id
  face_degen_eq : ∀ (n : Nat) (j : Nat) (hj : j ≤ n) (x : Simplex n),
    face n j (by omega) (degen n j hj x) = x
  face_degen_succ : ∀ (n : Nat) (j : Nat) (hj : j ≤ n) (x : Simplex n),
    face n (j + 1) (by omega) (degen n j hj x) = x

/-- A Horn Λ^k_{n+1} in a simplicial set X is a collection of compatible n-faces
    missing the k-th face.
    For an (n+1)-simplex, a horn consists of a family of n-simplices x_i for i ≠ k
    such that d_i x_j = d_{j-1} x_i for i < j (with i, j ≠ k). -/
structure HornData (X : SimplicialSet.{u}) (n : Nat) (k : Nat) (hk : k ≤ n + 1) where
  faces : ∀ (i : Nat), i ≤ n + 1 → i ≠ k → X.Simplex n

/-- A filler for a horn Λ^k_{n+1} is an (n+1)-simplex x such that d_i x = x_i for all i ≠ k. -/
structure HornFiller (X : SimplicialSet.{u}) {n : Nat} {k : Nat} {hk : k ≤ n + 1}
    (horn : HornData X n k hk) where
  filler : X.Simplex (n + 1)
  matches_face : ∀ (i : Nat) (hi : i ≤ n + 1) (hni : i ≠ k),
    X.face n i hi filler = horn.faces i hi hni

/-- A Kan Complex is a simplicial set where every horn Λ^k_{n+1} has a filler (for all 0 ≤ k ≤ n+1). -/
def IsKanComplex (X : SimplicialSet.{u}) : Prop :=
  ∀ (n : Nat) (k : Nat) (hk : k ≤ n + 1) (horn : HornData X n k hk),
    Nonempty (HornFiller X horn)

/-- An inner horn is a horn Λ^k_{n+1} where 0 < k < n + 1 (strictly interior). -/
def IsInnerHorn (n : Nat) (k : Nat) : Prop :=
  0 < k ∧ k < n + 1

/-- A Quasi-Category (or Joyal ∞-category / weak Kan complex) is a simplicial set
    where every INNER horn Λ^k_{n+1} (0 < k < n+1) has a filler. -/
def IsQuasiCategory (X : SimplicialSet.{u}) : Prop :=
  ∀ (n : Nat) (k : Nat) (hk : k ≤ n + 1),
    IsInnerHorn n k →
    ∀ (horn : HornData X n k hk),
      Nonempty (HornFiller X horn)

/-- Theorem: Every Kan complex is a quasi-category.
    Since Kan complexes have fillers for ALL horns, they in particular have fillers
    for inner horns. -/
theorem kan_complex_is_quasi_category (X : SimplicialSet.{u})
    (hKan : IsKanComplex X) : IsQuasiCategory X := by
  intro n k hk hinner horn
  exact hKan n k hk horn


/-- 0-simplices of a quasi-category are its objects (0-cells). -/
def Objects (X : SimplicialSet.{u}) : Type u :=
  X.Simplex 0

/-- 1-simplices of a quasi-category are its 1-morphisms (1-cells). -/
def Morphisms (X : SimplicialSet.{u}) : Type u :=
  X.Simplex 1

/-- Source of a 1-morphism f is its 0-face d_1 f. -/
def Source (X : SimplicialSet.{u}) (f : Morphisms X) : Objects X :=
  X.face 0 1 (by decide) f

/-- Target of a 1-morphism f is its 1-face d_0 f. -/
def Target (X : SimplicialSet.{u}) (f : Morphisms X) : Objects X :=
  X.face 0 0 (by decide) f

/-- Identity 1-morphism on an object x is the degenerate 1-simplex s_0 x. -/
def Identity (X : SimplicialSet.{u}) (x : Objects X) : Morphisms X :=
  X.degen 0 0 (by decide) x

/-- Theorem: Source of the identity 1-morphism on x is x. -/
theorem source_identity (X : SimplicialSet.{u}) (x : Objects X) :
    Source X (Identity X x) = x := by
  dsimp [Source, Identity]
  exact X.face_degen_succ 0 0 (by decide) x

/-- Theorem: Target of the identity 1-morphism on x is x. -/
theorem target_identity (X : SimplicialSet.{u}) (x : Objects X) :
    Target X (Identity X x) = x := by
  dsimp [Target, Identity]
  exact X.face_degen_eq 0 0 (by decide) x

end HigherCategoryTheory
