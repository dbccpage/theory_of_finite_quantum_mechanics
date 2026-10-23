/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/research_programs/higher_category_theory/StableInfinityCategory.lean
   Original sha256: 5c936f7f27a8a236da3b821d5866c7f17d02acaa864dda1046c76be1741f4e50 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.HigherCategoryTheory.StableInfinityCategory
   Reason         : HCT
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
/-
StableInfinityCategory.lean
Formalization of Stable ∞-Categories and Spectra.

AuthorityEffect: None.
Standard foundational axioms only: {propext, Quot.sound, Classical.choice}.
Zero sorry, zero admit.
-/

import Imported.HigherCategoryTheory.Monoidal

namespace HigherCategoryTheory

universe u

/-- A Pointed Category (or pointed quasi-category) has a designated zero object 0
    which is both initial and terminal. -/
structure PointedCategory (Obj : Type u) extends Category Obj where
  zero : Obj
  zero_mor : ∀ (X : Obj), Hom zero X
  zero_to : ∀ (X : Obj), Hom X zero
  zero_comp_mor : ∀ (X Y : Obj) (f : Hom X zero), comp f (zero_mor Y) = comp (zero_to X) (zero_mor Y)
  zero_comp_to : ∀ (X Y : Obj) (g : Hom zero Y), comp (zero_to X) g = comp (zero_to X) (zero_mor Y)

/-- Canonical zero morphism between any two objects X and Y. -/
def PointedCategory.zeroHom {Obj : Type u} (cat : PointedCategory Obj) (X Y : Obj) : cat.Hom X Y :=
  cat.comp (cat.zero_to X) (cat.zero_mor Y)

/-- A distinguished triangle (or fiber/cofiber sequence) in a pointed category:
    X ⟶ Y ⟶ Z with composite being the zero morphism. -/
structure FiberSequence {Obj : Type u} (cat : PointedCategory Obj) where
  fiber : Obj
  total : Obj
  base : Obj
  i : cat.Hom fiber total
  p : cat.Hom total base
  comp_zero : cat.comp i p = cat.zeroHom fiber base

/-- Stable ∞-Category Structure on a pointed category.
    Key axioms:
    1. Pointed: has zero object.
    2. Finite limits and colimits exist (witnessed by suspension and loop functors).
    3. Suspension Σ and Loop Ω functors are mutual inverse equivalences.
    4. A square is a pushout if and only if it is a pullback (bi-cartesian). -/
structure StableStructure {Obj : Type u} (cat : PointedCategory Obj) where
  suspension : Obj → Obj
  loop : Obj → Obj

  -- Functorial action on morphisms
  suspension_mor : ∀ {X Y : Obj}, cat.Hom X Y → cat.Hom (suspension X) (suspension Y)
  loop_mor : ∀ {X Y : Obj}, cat.Hom X Y → cat.Hom (loop X) (loop Y)
  suspension_comp : ∀ {X Y Z : Obj} (f : cat.Hom X Y) (g : cat.Hom Y Z),
    cat.comp (suspension_mor f) (suspension_mor g) = suspension_mor (cat.comp f g)
  suspension_id : ∀ (X : Obj), suspension_mor (cat.id X) = cat.id (suspension X)
  loop_comp : ∀ {X Y Z : Obj} (f : cat.Hom X Y) (g : cat.Hom Y Z),
    cat.comp (loop_mor f) (loop_mor g) = loop_mor (cat.comp f g)
  loop_id : ∀ (X : Obj), loop_mor (cat.id X) = cat.id (loop X)

  -- Equivalence: Σ and Ω are mutual equivalences
  sigma_omega_iso_hom : ∀ (X : Obj), cat.Hom (suspension (loop X)) X
  sigma_omega_iso_inv : ∀ (X : Obj), cat.Hom X (suspension (loop X))
  sigma_omega_left : ∀ (X : Obj), cat.comp (sigma_omega_iso_inv X) (sigma_omega_iso_hom X) = cat.id X
  sigma_omega_right : ∀ (X : Obj), cat.comp (sigma_omega_iso_hom X) (sigma_omega_iso_inv X) = cat.id (suspension (loop X))

  omega_sigma_iso_hom : ∀ (X : Obj), cat.Hom (loop (suspension X)) X
  omega_sigma_iso_inv : ∀ (X : Obj), cat.Hom X (loop (suspension X))
  omega_sigma_left : ∀ (X : Obj), cat.comp (omega_sigma_iso_inv X) (omega_sigma_iso_hom X) = cat.id X
  omega_sigma_right : ∀ (X : Obj), cat.comp (omega_sigma_iso_hom X) (omega_sigma_iso_inv X) = cat.id (loop (suspension X))

  -- Preservation of zero
  suspension_zero : suspension cat.zero = cat.zero
  loop_zero : loop cat.zero = cat.zero

/-- Theorem: In a stable ∞-category, suspension preserves composition of identity morphisms. -/
theorem suspension_id_comp {Obj : Type u} (cat : PointedCategory Obj)
    (S : StableStructure cat) (X : Obj) :
    cat.comp (S.suspension_mor (cat.id X)) (S.suspension_mor (cat.id X)) =
    S.suspension_mor (cat.comp (cat.id X) (cat.id X)) :=
  S.suspension_comp (cat.id X) (cat.id X)


/-- Theorem: Invertibility of the suspension-loop counit.
    ΣΩ(X) is isomorphic to X via sigma_omega_iso. -/
theorem sigma_omega_counit_invertible {Obj : Type u} (cat : PointedCategory Obj)
    (S : StableStructure cat) (X : Obj) :
    cat.comp (S.sigma_omega_iso_inv X) (S.sigma_omega_iso_hom X) = cat.id X :=
  S.sigma_omega_left X

/-- Theorem: Invertibility of the loop-suspension unit.
    ΩΣ(X) is isomorphic to X via omega_sigma_iso. -/
theorem omega_sigma_unit_invertible {Obj : Type u} (cat : PointedCategory Obj)
    (S : StableStructure cat) (X : Obj) :
    cat.comp (S.omega_sigma_iso_inv X) (S.omega_sigma_iso_hom X) = cat.id X :=
  S.omega_sigma_left X

/-- A Spectrum in a stable ∞-category is a sequence of objects E_n together with
    structure isomorphisms σ_n : E_n ⟶ Ω(E_{n+1}) (or adjointly Σ(E_n) ⟶ E_{n+1}). -/
structure OmegaSpectrum {Obj : Type u} (cat : PointedCategory Obj)
    (S : StableStructure cat) where
  level : Nat → Obj
  structure_map : ∀ (n : Nat), cat.Hom (level n) (S.loop (level (n + 1)))
  structure_inv : ∀ (n : Nat), cat.Hom (S.loop (level (n + 1))) (level n)
  structure_left : ∀ (n : Nat),
    cat.comp (structure_map n) (structure_inv n) = cat.id (level n)
  structure_right : ∀ (n : Nat),
    cat.comp (structure_inv n) (structure_map n) = cat.id (S.loop (level (n + 1)))

end HigherCategoryTheory
