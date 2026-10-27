/- Imported so that this repository carries its own Lean evidence.
   Original sha256: 4a411cc41b32f12f333e451895bfc8aea861d3cf5dda9b8e1563235b8f9c37d9 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.HigherCategoryTheory.DerivedCategory
   Reason         : HCT
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
/-
Released under Apache 2.0 license as described in the file LICENSE.
-/

import Imported.HigherCategoryTheory.Monoidal
import Imported.HigherCategoryTheory.Triangulated

namespace HigherCategoryTheory

universe u v

set_option linter.checkUnivs false
set_option linter.unusedVariables false

/-- A chain complex over an additive category $\mathcal{A}$:
    A collection of objects $X_n$ and boundary differentials $d_n : X_n \to X_{n-1}$
    satisfying $d_{n-1} \circ d_n = 0$. -/
structure ChainComplex {Obj : Type u} (A : AdditiveCategory.{u, v} Obj) where
  X : Int → Obj
  d : (n : Int) → A.cat.Hom (X n) (X (n - 1))
  d_sq : ∀ (n : Int), A.cat.comp (d n) (d (n - 1)) = A.zero (X n) (X (n - 1 - 1))

/-- A chain map $f : C \to D$ is a degree 0 morphism commuting with the differentials:
    $f_n \circ d_n^D = d_n^C \circ f_{n-1}$. -/
structure ChainMap {Obj : Type u} {A : AdditiveCategory.{u, v} Obj}
    (C D : ChainComplex A) where
  f : (n : Int) → A.cat.Hom (C.X n) (D.X n)
  comm : ∀ (n : Int), A.cat.comp (f n) (D.d n) = A.cat.comp (C.d n) (f (n - 1))

/-- Identity chain map on a chain complex. -/
def idChainMap {Obj : Type u} {A : AdditiveCategory.{u, v} Obj}
    (C : ChainComplex A) : ChainMap C C where
  f := fun n => A.cat.id (C.X n)
  comm := by
    intro n
    rw [A.cat.id_comp, A.cat.comp_id]

/-- Composition of chain maps is a chain map. -/
def compChainMap {Obj : Type u} {A : AdditiveCategory.{u, v} Obj}
    {C D E : ChainComplex A} (f : ChainMap C D) (g : ChainMap D E) : ChainMap C E where
  f := fun n => A.cat.comp (f.f n) (g.f n)
  comm := by
    intro n
    rw [A.cat.comp_assoc]
    rw [g.comm n]
    rw [← A.cat.comp_assoc]
    rw [f.comm n]
    rw [A.cat.comp_assoc]

/-- A 2x2 block morphism representing a morphism between biproducts $Y \oplus X \to Y' \oplus X'$.
    Components:
    - `m11 : Y → Y'`
    - `m12 : X → Y'`
    - `m21 : Y → X'`
    - `m22 : X → X'` -/
structure BlockHom2x2 {Obj : Type u} (A : AdditiveCategory.{u, v} Obj)
    (Y X Y' X' : Obj) where
  m11 : A.cat.Hom Y Y'
  m12 : A.cat.Hom X Y'
  m21 : A.cat.Hom Y X'
  m22 : A.cat.Hom X X'

/-- Composition of 2x2 block morphisms via biproduct matrix multiplication. -/
def compBlock {Obj : Type u} {A : AdditiveCategory.{u, v} Obj}
    {Y X Y' X' Y'' X'' : Obj}
    (M1 : BlockHom2x2 A Y X Y' X') (M2 : BlockHom2x2 A Y' X' Y'' X'') :
    BlockHom2x2 A Y X Y'' X'' where
  m11 := A.add (A.cat.comp M1.m11 M2.m11) (A.cat.comp M1.m21 M2.m12)
  m12 := A.add (A.cat.comp M1.m12 M2.m11) (A.cat.comp M1.m22 M2.m12)
  m21 := A.add (A.cat.comp M1.m11 M2.m21) (A.cat.comp M1.m21 M2.m22)
  m22 := A.add (A.cat.comp M1.m12 M2.m21) (A.cat.comp M1.m22 M2.m22)

/-- The zero 2x2 block morphism. -/
def zeroBlock {Obj : Type u} (A : AdditiveCategory.{u, v} Obj)
    (Y X Y' X' : Obj) : BlockHom2x2 A Y X Y' X' where
  m11 := A.zero Y Y'
  m12 := A.zero X Y'
  m21 := A.zero Y X'
  m22 := A.zero X X'

/-- The mapping cone block differential matrix:
    $\begin{pmatrix} d_Y & f \\ 0 & -d_X \end{pmatrix}$. -/
def coneDifferential {Obj : Type u} (A : AdditiveCategory.{u, v} Obj)
    {Y X Y' X' : Obj}
    (dY : A.cat.Hom Y Y') (dX : A.cat.Hom X X') (f : A.cat.Hom X Y') :
    BlockHom2x2 A Y X Y' X' where
  m11 := dY
  m12 := f
  m21 := A.zero Y X'
  m22 := A.neg dX

/-- Constructive theorem: The mapping cone differential squares to zero identically.
    Given chain differentials $d_Y, d_X$ and chain map component $f$ satisfying:
    - $d_Y \circ d_Y' = 0$
    - $d_X \circ d_X' = 0$
    - $f \circ d_Y' = d_X \circ f'$ (chain map commutativity),
    the composed cone differential block matrix evaluates identically to the zero block morphism. -/
theorem mapping_cone_differential_sq {Obj : Type u} (A : AdditiveCategory.{u, v} Obj)
    {Y X Y' X' Y'' X'' : Obj}
    (dY : A.cat.Hom Y Y') (dX : A.cat.Hom X X') (f : A.cat.Hom X Y')
    (dY' : A.cat.Hom Y' Y'') (dX' : A.cat.Hom X' X'') (f' : A.cat.Hom X' Y'')
    (hdY_sq : A.cat.comp dY dY' = A.zero Y Y'')
    (hdX_sq : A.cat.comp dX dX' = A.zero X X'')
    (hchain : A.cat.comp f dY' = A.cat.comp dX f') :
    compBlock (coneDifferential A dY dX f) (coneDifferential A dY' dX' f') =
      zeroBlock A Y X Y'' X'' := by
  dsimp [compBlock, coneDifferential, zeroBlock]
  congr 1
  · -- m11: dY ∘ dY' + 0 ∘ f' = 0 + 0 = 0
    rw [hdY_sq, A.zero_comp, A.add_zero]
  · -- m12: f ∘ dY' + (-dX) ∘ f' = f ∘ dY' - dX ∘ f' = 0
    rw [A.neg_comp, hchain, A.add_right_neg]
  · -- m21: dY ∘ 0 + 0 ∘ (-dX') = 0 + 0 = 0
    rw [A.comp_zero, A.zero_comp, A.add_zero]
  · -- m22: f ∘ 0 + (-dX) ∘ (-dX') = 0 + dX ∘ dX' = 0
    rw [A.comp_zero, A.neg_comp, A.comp_neg]
    rw [A.neg_neg, hdX_sq, A.zero_add]

/-- The Mapping Cone data for a chain map $f : C \to D$, with objects $D_n \oplus C_{n-1}$
    and block differentials squaring to zero. -/
structure MappingConeData {Obj : Type u} (A : AdditiveCategory.{u, v} Obj)
    {C D : ChainComplex A} (f : ChainMap C D) where
  coneObj : Int → Obj
  coneDiff : (n : Int) → BlockHom2x2 A (D.X n) (C.X (n - 1)) (D.X (n - 1)) (C.X (n - 1 - 1))
  coneDiff_eq : ∀ (n : Int),
    coneDiff n = coneDifferential A (D.d n) (C.d (n - 1)) (f.f (n - 1))
  diff_sq : ∀ (n : Int),
    compBlock (coneDiff n) (coneDiff (n - 1)) =
      zeroBlock A (D.X n) (C.X (n - 1)) (D.X (n - 1 - 1)) (C.X (n - 1 - 1 - 1))

/-- Canonical construction of the Mapping Cone data from any chain map $f : C \to D$,
    proved constructively via `mapping_cone_differential_sq`. -/
def canonicalMappingConeData {Obj : Type u} {A : AdditiveCategory.{u, v} Obj}
    {C D : ChainComplex A} (f : ChainMap C D) : MappingConeData A f where
  coneObj := fun n => A.biprod (D.X n) (C.X (n - 1))
  coneDiff := fun n => coneDifferential A (D.d n) (C.d (n - 1)) (f.f (n - 1))
  coneDiff_eq := fun n => rfl
  diff_sq := fun n => by
    have h1 := D.d_sq n
    have h2 := C.d_sq (n - 1)
    have h3 := f.comm (n - 1)
    exact mapping_cone_differential_sq A (D.d n) (C.d (n - 1)) (f.f (n - 1))
      (D.d (n - 1)) (C.d (n - 1 - 1)) (f.f (n - 1 - 1))
      h1 h2 h3

/-- Predicate for a chain map being a quasi-isomorphism. -/
def IsQuasiIso {Obj : Type u} {A : AdditiveCategory.{u, v} Obj}
    {C D : ChainComplex A} (f : ChainMap C D) : Prop :=
  ∀ (n : Int), ∃ (h : A.cat.Hom (D.X n) (C.X n)),
    A.cat.comp (f.f n) h = A.cat.id (C.X n) ∨
    A.cat.comp h (f.f n) = A.cat.id (D.X n)

/-- Identity chain map is a quasi-isomorphism. -/
theorem idChainMap_is_quasi_iso {Obj : Type u} {A : AdditiveCategory.{u, v} Obj}
    (C : ChainComplex A) : IsQuasiIso (idChainMap C) := by
  intro n
  refine ⟨A.cat.id (C.X n), ?_⟩
  left
  exact A.cat.id_comp (A.cat.id (C.X n))

/-- A Roof (formal fraction) $C \xleftarrow{s} Z \xrightarrow{g} D$ representing a morphism
    in the Derived Category obtained by localizing at quasi-isomorphisms. -/
structure Roof {Obj : Type u} (A : AdditiveCategory.{u, v} Obj)
    (C D : ChainComplex A) where
  apex : ChainComplex A
  s : ChainMap apex C
  g : ChainMap apex D
  s_quasi_iso : IsQuasiIso s

/-- Identity roof on a chain complex $C \xleftarrow{\text{id}} C \xrightarrow{\text{id}} C$. -/
def idRoof {Obj : Type u} {A : AdditiveCategory.{u, v} Obj}
    (C : ChainComplex A) : Roof A C C where
  apex := C
  s := idChainMap C
  g := idChainMap C
  s_quasi_iso := idChainMap_is_quasi_iso C

/-- Bounded Chain Complex: A complex $C$ whose terms $C_n = 0$ for $|n| > N$. -/
structure BoundedChainComplex {Obj : Type u} (A : AdditiveCategory.{u, v} Obj) where
  complex : ChainComplex A
  bound_N : Nat
  is_bounded : ∀ (n : Int), n.natAbs > bound_N → complex.X n = A.zeroObj

/-- The Bounded Derived Category $\mathcal{D}^b(\mathcal{A})$ of an additive category $\mathcal{A}$.
    Objects are bounded complexes, and morphisms are roofs with quasi-isomorphism left legs. -/
structure BoundedDerivedCategory (Obj : Type u) where
  additive : AdditiveCategory.{u, v} Obj
  cat : Category.{max u v, max u v} (BoundedChainComplex additive)
  triangulated : TriangulatedCategory (BoundedChainComplex additive)
  triangulated_cat_eq : triangulated.additive.cat = cat

/-- The Unbounded Derived Category $\mathcal{D}(\mathcal{A})$. -/
structure UnboundedDerivedCategory (Obj : Type u) where
  additive : AdditiveCategory.{u, v} Obj
  cat : Category.{max u v, max u v} (ChainComplex additive)
  triangulated : TriangulatedCategory (ChainComplex additive)
  triangulated_cat_eq : triangulated.additive.cat = cat

end HigherCategoryTheory
