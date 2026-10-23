/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/research_programs/higher_category_theory/Triangulated.lean
   Original sha256: d943958f408d9f86522238555d1c67166bf838fd8edd703bcf215cf9630fd501 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.HigherCategoryTheory.Triangulated
   Reason         : HCT
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
/-
Copyright (c) 2026 Anomalon Research. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Worker M1 (Lean 4 HCT Formalization)
-/

import Imported.HigherCategoryTheory.Monoidal

namespace HigherCategoryTheory

universe u v

set_option linter.checkUnivs false
set_option linter.unusedVariables false

/-- An Additive Category is a category enriched over abelian groups with finite biproducts and a zero object. -/
structure AdditiveCategory (Obj : Type u) where
  cat : Category.{u, v} Obj
  -- Abelian group structure on Hom(X, Y)
  add : {X Y : Obj} → cat.Hom X Y → cat.Hom X Y → cat.Hom X Y
  zero : (X Y : Obj) → cat.Hom X Y
  neg : {X Y : Obj} → cat.Hom X Y → cat.Hom X Y
  add_assoc : ∀ {X Y : Obj} (f g h : cat.Hom X Y), add (add f g) h = add f (add g h)
  add_comm : ∀ {X Y : Obj} (f g : cat.Hom X Y), add f g = add g f
  add_zero : ∀ {X Y : Obj} (f : cat.Hom X Y), add f (zero X Y) = f
  zero_add : ∀ {X Y : Obj} (f : cat.Hom X Y), add (zero X Y) f = f
  add_left_neg : ∀ {X Y : Obj} (f : cat.Hom X Y), add (neg f) f = zero X Y
  add_right_neg : ∀ {X Y : Obj} (f : cat.Hom X Y), add f (neg f) = zero X Y
  neg_neg : ∀ {X Y : Obj} (f : cat.Hom X Y), neg (neg f) = f
  -- Bilinearity of composition
  comp_add : ∀ {X Y Z : Obj} (f : cat.Hom X Y) (g1 g2 : cat.Hom Y Z),
    cat.comp f (add g1 g2) = add (cat.comp f g1) (cat.comp f g2)
  add_comp : ∀ {X Y Z : Obj} (f1 f2 : cat.Hom X Y) (g : cat.Hom Y Z),
    cat.comp (add f1 f2) g = add (cat.comp f1 g) (cat.comp f2 g)
  comp_zero : ∀ {X Y Z : Obj} (f : cat.Hom X Y),
    cat.comp f (zero Y Z) = zero X Z
  zero_comp : ∀ {X Y Z : Obj} (g : cat.Hom Y Z),
    cat.comp (zero X Y) g = zero X Z
  comp_neg : ∀ {X Y Z : Obj} (f : cat.Hom X Y) (g : cat.Hom Y Z),
    cat.comp f (neg g) = neg (cat.comp f g)
  neg_comp : ∀ {X Y Z : Obj} (f : cat.Hom X Y) (g : cat.Hom Y Z),
    cat.comp (neg f) g = neg (cat.comp f g)
  -- Zero object
  zeroObj : Obj
  -- Binary biproducts (direct sums)
  biprod : Obj → Obj → Obj
  fst : (X Y : Obj) → cat.Hom (biprod X Y) X
  snd : (X Y : Obj) → cat.Hom (biprod X Y) Y
  inl : (X Y : Obj) → cat.Hom X (biprod X Y)
  inr : (X Y : Obj) → cat.Hom Y (biprod X Y)
  fst_inl : ∀ (X Y : Obj), cat.comp (inl X Y) (fst X Y) = cat.id X
  snd_inr : ∀ (X Y : Obj), cat.comp (inr X Y) (snd X Y) = cat.id Y
  fst_inr : ∀ (X Y : Obj), cat.comp (inr X Y) (fst X Y) = zero Y X
  snd_inl : ∀ (X Y : Obj), cat.comp (inl X Y) (snd X Y) = zero X Y
  biprod_id : ∀ (X Y : Obj),
    add (cat.comp (fst X Y) (inl X Y)) (cat.comp (snd X Y) (inr X Y)) = cat.id (biprod X Y)

/-- Translation (Shift) Functor $T = [1]$ on an additive category, acting as an autoequivalence. -/
structure TranslationFunctor (Obj : Type u) (A : AdditiveCategory Obj) where
  shiftObj : Obj → Obj
  shiftHom : {X Y : Obj} → A.cat.Hom X Y → A.cat.Hom (shiftObj X) (shiftObj Y)
  shiftHom_id : ∀ (X : Obj), shiftHom (A.cat.id X) = A.cat.id (shiftObj X)
  shiftHom_comp : ∀ {X Y Z : Obj} (f : A.cat.Hom X Y) (g : A.cat.Hom Y Z),
    shiftHom (A.cat.comp f g) = A.cat.comp (shiftHom f) (shiftHom g)
  shiftHom_add : ∀ {X Y : Obj} (f g : A.cat.Hom X Y),
    shiftHom (A.add f g) = A.add (shiftHom f) (shiftHom g)
  shiftHom_zero : ∀ (X Y : Obj),
    shiftHom (A.zero X Y) = A.zero (shiftObj X) (shiftObj Y)
  shiftHom_neg : ∀ {X Y : Obj} (f : A.cat.Hom X Y),
    shiftHom (A.neg f) = A.neg (shiftHom f)
  -- Autoequivalence inverse translation functor $T^{-1} = [-1]$
  invObj : Obj → Obj
  invHom : {X Y : Obj} → A.cat.Hom X Y → A.cat.Hom (invObj X) (invObj Y)
  shift_inv : ∀ (X : Obj), Iso A.cat (shiftObj (invObj X)) X
  inv_shift : ∀ (X : Obj), Iso A.cat (invObj (shiftObj X)) X

/-- A candidate triangle in an additive category equipped with a translation functor:
    $X \xrightarrow{u} Y \xrightarrow{v} Z \xrightarrow{w} T(X)$. -/
structure Triangle {Obj : Type u} (A : AdditiveCategory Obj) (T : TranslationFunctor Obj A) where
  X : Obj
  Y : Obj
  Z : Obj
  u : A.cat.Hom X Y
  v : A.cat.Hom Y Z
  w : A.cat.Hom Z (T.shiftObj X)

/-- Morphism of triangles $(f, g, h) : t_1 \to t_2$ commuting with the triangle differentials. -/
structure TriangleMorphism {Obj : Type u} {A : AdditiveCategory Obj} {T : TranslationFunctor Obj A}
    (t1 t2 : Triangle A T) where
  f : A.cat.Hom t1.X t2.X
  g : A.cat.Hom t1.Y t2.Y
  h : A.cat.Hom t1.Z t2.Z
  comm1 : A.cat.comp t1.u g = A.cat.comp f t2.u
  comm2 : A.cat.comp t1.v h = A.cat.comp g t2.v
  comm3 : A.cat.comp t1.w (T.shiftHom f) = A.cat.comp h t2.w

/-- An isomorphism of triangles. -/
structure TriangleIso {Obj : Type u} {A : AdditiveCategory Obj} {T : TranslationFunctor Obj A}
    (t1 t2 : Triangle A T) where
  morph : TriangleMorphism t1 t2
  isoX : Iso A.cat t1.X t2.X
  isoY : Iso A.cat t1.Y t2.Y
  isoZ : Iso A.cat t1.Z t2.Z
  hx : morph.f = isoX.hom
  hy : morph.g = isoY.hom
  hz : morph.h = isoZ.hom

/-- Rotated triangle under Verdier rotation TR2:
    $(X \xrightarrow{u} Y \xrightarrow{v} Z \xrightarrow{w} T(X))$ rotates to
    $(Y \xrightarrow{v} Z \xrightarrow{w} T(X) \xrightarrow{-T(u)} T(Y))$.
    Note the essential anti-shift sign $-T(u)$! -/
def rotateTriangle {Obj : Type u} {A : AdditiveCategory Obj} {T : TranslationFunctor Obj A}
    (t : Triangle A T) : Triangle A T where
  X := t.Y
  Y := t.Z
  Z := T.shiftObj t.X
  u := t.v
  v := t.w
  w := A.neg (T.shiftHom t.u)

/-- Triangulated Category structure satisfying Verdier's axioms TR1, TR2, TR3, TR4:
    - Additive underlying category `additive`
    - Autoequivalence translation functor `translation`
    - Class of distinguished triangles `isDistinguished` satisfying:
      - TR1a: Identity triangles $(X \xrightarrow{\text{id}} X \to 0 \to T(X))$ are distinguished
      - TR1b: Closure under triangle isomorphism
      - TR1c: Existence of mapping cones for every morphism
      - TR2: Rotation axiom (distinguished $\iff$ rotated is distinguished)
      - TR3: Morphism extension axiom between distinguished triangles
      - TR4: Octahedral axiom (braid of triangles for composable arrows) -/
structure TriangulatedCategory (Obj : Type u) where
  additive : AdditiveCategory.{u, v} Obj
  translation : TranslationFunctor Obj additive
  isDistinguished : Triangle additive translation → Prop
  -- TR1a: Identity triangle is distinguished
  tr1a : ∀ (X : Obj),
    isDistinguished {
      X := X
      Y := X
      Z := additive.zeroObj
      u := additive.cat.id X
      v := additive.zero X additive.zeroObj
      w := additive.zero additive.zeroObj (translation.shiftObj X)
    }
  -- TR1b: Isomorphism closure
  tr1b : ∀ {t1 t2 : Triangle additive translation},
    isDistinguished t1 → TriangleIso t1 t2 → isDistinguished t2
  -- TR1c: Existence of triangles / mapping cones
  tr1c : ∀ {X Y : Obj} (u : additive.cat.Hom X Y),
    ∃ (Z : Obj) (v : additive.cat.Hom Y Z) (w : additive.cat.Hom Z (translation.shiftObj X)),
      isDistinguished { X := X, Y := Y, Z := Z, u := u, v := v, w := w }
  -- TR2: Rotation axiom
  tr2 : ∀ (t : Triangle additive translation),
    isDistinguished t ↔ isDistinguished (rotateTriangle t)
  -- TR3: Morphism extension
  tr3 : ∀ {t1 t2 : Triangle additive translation}
    (f : additive.cat.Hom t1.X t2.X) (g : additive.cat.Hom t1.Y t2.Y),
    isDistinguished t1 → isDistinguished t2 →
    additive.cat.comp t1.u g = additive.cat.comp f t2.u →
    ∃ (h : additive.cat.Hom t1.Z t2.Z),
      additive.cat.comp t1.v h = additive.cat.comp g t2.v ∧
      additive.cat.comp t1.w (translation.shiftHom f) = additive.cat.comp h t2.w
  -- Consecutive compositions in any distinguished triangle vanish
  comp_zero_uv : ∀ (t : Triangle additive translation),
    isDistinguished t → additive.cat.comp t.u t.v = additive.zero t.X t.Z
  comp_zero_vw : ∀ (t : Triangle additive translation),
    isDistinguished t → additive.cat.comp t.v t.w = additive.zero t.Y (translation.shiftObj t.X)
  -- TR4: Octahedral axiom
  tr4 : ∀ {X Y Z Cu Cv Cw : Obj}
    (u : additive.cat.Hom X Y) (v : additive.cat.Hom Y Z)
    (ju : additive.cat.Hom Y Cu) (ku : additive.cat.Hom Cu (translation.shiftObj X))
    (jv : additive.cat.Hom Z Cv) (kv : additive.cat.Hom Cv (translation.shiftObj Y))
    (jw : additive.cat.Hom Z Cw) (kw : additive.cat.Hom Cw (translation.shiftObj X)),
    isDistinguished { X := X, Y := Y, Z := Cu, u := u, v := ju, w := ku } →
    isDistinguished { X := Y, Y := Z, Z := Cv, u := v, v := jv, w := kv } →
    isDistinguished { X := X, Y := Z, Z := Cw, u := additive.cat.comp u v, v := jw, w := kw } →
    ∃ (f : additive.cat.Hom Cu Cw) (g : additive.cat.Hom Cw Cv)
      (h : additive.cat.Hom Cv (translation.shiftObj Cu)),
      isDistinguished { X := Cu, Y := Cw, Z := Cv, u := f, v := g, w := h } ∧
      additive.cat.comp ju f = additive.cat.comp v jw ∧
      additive.cat.comp jw g = jv ∧
      additive.cat.comp f g = additive.zero Cu Cv

namespace TriangulatedCategory

variable {Obj : Type u} (T : TriangulatedCategory Obj)

/-- Constructive theorem: Verdier rotation equivalence TR2 for distinguished triangles. -/
theorem TR2_rotation (t : Triangle T.additive T.translation) :
    T.isDistinguished t ↔ T.isDistinguished (rotateTriangle t) :=
  T.tr2 t

/-- Constructive theorem: Consecutive morphisms in any distinguished triangle compose to zero. -/
theorem distinguished_comp_zero (t : Triangle T.additive T.translation) (h : T.isDistinguished t) :
    T.additive.cat.comp t.u t.v = T.additive.zero t.X t.Z ∧
    T.additive.cat.comp t.v t.w = T.additive.zero t.Y (T.translation.shiftObj t.X) :=
  ⟨T.comp_zero_uv t h, T.comp_zero_vw t h⟩

/-- Constructive theorem: The octahedral braid axiom TR4 holds for composable morphisms. -/
theorem octahedral_braid {X Y Z Cu Cv Cw : Obj}
    (u : T.additive.cat.Hom X Y) (v : T.additive.cat.Hom Y Z)
    (ju : T.additive.cat.Hom Y Cu) (ku : T.additive.cat.Hom Cu (T.translation.shiftObj X))
    (jv : T.additive.cat.Hom Z Cv) (kv : T.additive.cat.Hom Cv (T.translation.shiftObj Y))
    (jw : T.additive.cat.Hom Z Cw) (kw : T.additive.cat.Hom Cw (T.translation.shiftObj X))
    (hu : T.isDistinguished { X := X, Y := Y, Z := Cu, u := u, v := ju, w := ku })
    (hv : T.isDistinguished { X := Y, Y := Z, Z := Cv, u := v, v := jv, w := kv })
    (hw : T.isDistinguished { X := X, Y := Z, Z := Cw, u := T.additive.cat.comp u v, v := jw, w := kw }) :
    ∃ (f : T.additive.cat.Hom Cu Cw) (g : T.additive.cat.Hom Cw Cv)
      (h : T.additive.cat.Hom Cv (T.translation.shiftObj Cu)),
      T.isDistinguished { X := Cu, Y := Cw, Z := Cv, u := f, v := g, w := h } ∧
      T.additive.cat.comp ju f = T.additive.cat.comp v jw ∧
      T.additive.cat.comp jw g = jv ∧
      T.additive.cat.comp f g = T.additive.zero Cu Cv :=
  T.tr4 u v ju ku jv kv jw kw hu hv hw

end TriangulatedCategory

end HigherCategoryTheory
