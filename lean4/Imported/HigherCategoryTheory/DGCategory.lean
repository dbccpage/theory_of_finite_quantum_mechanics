/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/research_programs/higher_category_theory/DGCategory.lean
   Original sha256: 2db5ed1fcd3e5e8c314383e24d4261dedd8ac26c7e29fcc7180e8acdf7efbfe9 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.HigherCategoryTheory.DGCategory
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

/-- Degree sign function $(-1)^q$ for $q \in \mathbb{Z}$.
    Returns $+1$ if $q$ is even and $-1$ if $q$ is odd. -/
def degSign (q : Int) : Int :=
  if q % 2 = 0 then 1 else -1

/-- Degree arithmetic helper: $(q + 1) + p = (q + p) + 1$. -/
theorem deg_add_left (q p : Int) : (q + 1) + p = (q + p) + 1 := by omega

/-- Degree arithmetic helper: $q + (p + 1) = (q + p) + 1$. -/
theorem deg_add_right (q p : Int) : q + (p + 1) = (q + p) + 1 := by omega

/-- Degree arithmetic helper: associativity $(r + q) + p = r + (q + p)$. -/
theorem deg_assoc (r q p : Int) : (r + q) + p = r + (q + p) := by omega

/-- Basic degree reduction lemma: $-1 + 1 = 0$. -/
theorem neg_one_add_one : (-1 : Int) + 1 = 0 := rfl

/-- Transport a graded family element along an integer equality index proof. -/
def castGraded {F : Int → Type v} {n m : Int} (h : n = m) (x : F n) : F m :=
  h ▸ x

@[simp]
theorem castGraded_rfl {F : Int → Type v} {n : Int} (x : F n) :
    castGraded (rfl : n = n) x = x := rfl

/-- Graded abelian group / module structure for Hom spaces in a DG-category. -/
structure GradedModule (M : Int → Type v) where
  add : {n : Int} → M n → M n → M n
  zero : {n : Int} → M n
  neg : {n : Int} → M n → M n
  smul : {n : Int} → Int → M n → M n
  add_assoc : ∀ {n : Int} (x y z : M n), add (add x y) z = add x (add y z)
  add_comm : ∀ {n : Int} (x y : M n), add x y = add y x
  add_zero : ∀ {n : Int} (x : M n), add x zero = x
  zero_add : ∀ {n : Int} (x : M n), add zero x = x
  add_left_neg : ∀ {n : Int} (x : M n), add (neg x) x = zero
  add_right_neg : ∀ {n : Int} (x : M n), add x (neg x) = zero
  sub : {n : Int} → M n → M n → M n
  sub_eq : ∀ {n : Int} (x y : M n), sub x y = add x (neg y)
  neg_neg : ∀ {n : Int} (x : M n), neg (neg x) = x
  neg_add : ∀ {n : Int} (x y : M n), neg (add x y) = add (neg x) (neg y)
  neg_zero : ∀ {n : Int}, neg (zero : M n) = zero
  smul_zero : ∀ {n : Int} (c : Int), smul c (zero : M n) = zero
  smul_one : ∀ {n : Int} (x : M n), smul 1 x = x
  smul_neg_one : ∀ {n : Int} (x : M n), smul (-1) x = neg x
  smul_add : ∀ {n : Int} (c : Int) (x y : M n), smul c (add x y) = add (smul c x) (smul c y)

/-- Differential Graded (DG) Category structure:
    - Objects `Obj : Type u`
    - Graded Hom-modules $\text{Hom}(X, Y) = \bigoplus_{n \in \mathbb{Z}} \text{Hom}^n(X, Y)$
    - Degree $+1$ differential $d$ satisfying $d^2 = 0$
    - Associative and unital composition satisfying the graded Leibniz rule:
      $d(g \circ f) = d(g) \circ f + (-1)^{|g|} g \circ d(f)$
    - 0th cohomology category $H^0(\mathcal{C})$ with canonical projection -/
structure DGCategory (Obj : Type u) where
  Hom : Obj → Obj → Int → Type v
  homMod : (X Y : Obj) → GradedModule (Hom X Y)
  d : {X Y : Obj} → {n : Int} → Hom X Y n → Hom X Y (n + 1)
  d_add : ∀ {X Y : Obj} {n : Int} (f g : Hom X Y n),
    d ((homMod X Y).add f g) = (homMod X Y).add (d f) (d g)
  d_sq : ∀ {X Y : Obj} {n : Int} (f : Hom X Y n),
    d (d f) = (homMod X Y).zero
  d_smul : ∀ {X Y : Obj} {n : Int} (c : Int) (f : Hom X Y n),
    d ((homMod X Y).smul c f) = (homMod X Y).smul c (d f)
  d_zero : ∀ {X Y : Obj} {n : Int},
    d ((homMod X Y).zero : Hom X Y n) = (homMod X Y).zero
  d_neg : ∀ {X Y : Obj} {n : Int} (f : Hom X Y n),
    d ((homMod X Y).neg f) = (homMod X Y).neg (d f)
  comp : {X Y Z : Obj} → {p q : Int} → Hom Y Z q → Hom X Y p → Hom X Z (q + p)
  comp_assoc : ∀ {W X Y Z : Obj} {p q r : Int} (f : Hom W X p) (g : Hom X Y q) (h : Hom Y Z r),
    comp (comp h g) f = castGraded (deg_assoc r q p).symm (comp h (comp g f))
  id : (X : Obj) → Hom X X 0
  id_comp : ∀ {X Y : Obj} {p : Int} (f : Hom X Y p),
    comp (id Y) f = castGraded (by omega) f
  comp_id : ∀ {X Y : Obj} {p : Int} (f : Hom X Y p),
    comp f (id X) = castGraded (by omega) f
  id_comp0 : ∀ {X Y : Obj} (f : Hom X Y 0),
    comp (id Y) f = f
  comp_id0 : ∀ {X Y : Obj} (f : Hom X Y 0),
    comp f (id X) = f
  comp_assoc0 : ∀ {W X Y Z : Obj} (f : Hom W X 0) (g : Hom X Y 0) (h : Hom Y Z 0),
    comp (comp h g) f = comp h (comp g f)
  d_id : ∀ (X : Obj),
    d (id X) = (homMod X X).zero
  comp_add : ∀ {X Y Z : Obj} {p q : Int} (g1 g2 : Hom Y Z q) (f : Hom X Y p),
    comp ((homMod Y Z).add g1 g2) f = (homMod X Z).add (comp g1 f) (comp g2 f)
  add_comp : ∀ {X Y Z : Obj} {p q : Int} (g : Hom Y Z q) (f1 f2 : Hom X Y p),
    comp g ((homMod X Y).add f1 f2) = (homMod X Z).add (comp g f1) (comp g f2)
  comp_zero : ∀ {X Y Z : Obj} {p q : Int} (f : Hom X Y p),
    comp ((homMod Y Z).zero (n := q)) f = (homMod X Z).zero (n := q + p)
  zero_comp : ∀ {X Y Z : Obj} {p q : Int} (g : Hom Y Z q),
    comp g ((homMod X Y).zero (n := p)) = (homMod X Z).zero (n := q + p)
  comp_neg : ∀ {X Y Z : Obj} {p q : Int} (g : Hom Y Z q) (f : Hom X Y p),
    comp g ((homMod X Y).neg f) = (homMod X Z).neg (comp g f)
  neg_comp : ∀ {X Y Z : Obj} {p q : Int} (g : Hom Y Z q) (f : Hom X Y p),
    comp ((homMod Y Z).neg g) f = (homMod X Z).neg (comp g f)
  leibniz : ∀ {X Y Z : Obj} {p q : Int} (g : Hom Y Z q) (f : Hom X Y p),
    d (comp g f) = (homMod X Z).add
      (castGraded (deg_add_left q p) (comp (d g) f))
      (castGraded (deg_add_right q p) ((homMod X Z).smul (degSign q) (comp g (d f))))
  comp_closed : ∀ {X Y Z : Obj} (g : Hom Y Z 0) (f : Hom X Y 0),
    d g = (homMod Y Z).zero → d f = (homMod X Y).zero →
    d (comp g f) = (homMod X Z).zero
  H0 : Category.{u, v} Obj
  h0_proj : {X Y : Obj} → Hom X Y 0 → H0.Hom X Y
  h0_proj_id : ∀ (X : Obj), h0_proj (id X) = H0.id X
  h0_proj_comp : ∀ {X Y Z : Obj} (f : Hom X Y 0) (g : Hom Y Z 0),
    h0_proj (comp g f) = H0.comp (h0_proj f) (h0_proj g)
  h0_homotopy_sound : ∀ {X Y : Obj} (f1 f2 : Hom X Y 0) (h : Hom X Y (-1)),
    (homMod X Y).sub f1 f2 = castGraded neg_one_add_one (d h) →
    h0_proj f1 = h0_proj f2

namespace DGCategory

variable {Obj : Type u} (C : DGCategory Obj)

/-- Constructive theorem: The differential squared identically vanishes on all morphism complexes. -/
theorem d_sq_zero {X Y : Obj} {n : Int} (f : C.Hom X Y n) :
    C.d (C.d f) = (C.homMod X Y).zero :=
  C.d_sq f

/-- Constructive theorem: Graded Leibniz product rule for composition. -/
theorem leibniz_rule {X Y Z : Obj} {p q : Int} (g : C.Hom Y Z q) (f : C.Hom X Y p) :
    C.d (C.comp g f) = (C.homMod X Z).add
      (castGraded (deg_add_left q p) (C.comp (C.d g) f))
      (castGraded (deg_add_right q p) ((C.homMod X Z).smul (degSign q) (C.comp g (C.d f)))) :=
  C.leibniz g f

/-- A closed degree 0 morphism (0-cycle): $f \in \text{Hom}^0(X, Y)$ with $d(f) = 0$. -/
structure ClosedHom0 (X Y : Obj) where
  val : C.Hom X Y 0
  is_closed : C.d val = (C.homMod X Y).zero

/-- Identity closed degree 0 morphism. -/
def idClosed (X : Obj) : ClosedHom0 C X X where
  val := C.id X
  is_closed := C.d_id X

/-- Composition of closed degree 0 morphisms produces a closed degree 0 morphism. -/
def compClosed {X Y Z : Obj} (g : ClosedHom0 C Y Z) (f : ClosedHom0 C X Y) : ClosedHom0 C X Z where
  val := C.comp g.val f.val
  is_closed := C.comp_closed g.val f.val g.is_closed f.is_closed

/-- Chain homotopy relation on closed degree 0 morphisms:
    $f \sim g$ iff there exists $h \in \text{Hom}^{-1}(X, Y)$ such that $f - g = d(h)$. -/
def IsHomotopic {X Y : Obj} (f g : ClosedHom0 C X Y) : Prop :=
  ∃ (h : C.Hom X Y (-1)), (C.homMod X Y).sub f.val g.val = castGraded neg_one_add_one (C.d h)

/-- Reflexivity of chain homotopy. -/
theorem isHomotopic_refl {X Y : Obj} (f : ClosedHom0 C X Y) : IsHomotopic C f f := by
  refine ⟨(C.homMod X Y).zero, ?_⟩
  rw [C.d_zero]
  have hz : castGraded neg_one_add_one ((C.homMod X Y).zero (n := -1 + 1)) = (C.homMod X Y).zero (n := 0) := by
    rfl
  rw [hz]
  rw [(C.homMod X Y).sub_eq]
  exact (C.homMod X Y).add_right_neg f.val

/-- Symmetry of chain homotopy. -/
theorem isHomotopic_symm {X Y : Obj} {f g : ClosedHom0 C X Y} (h : IsHomotopic C f g) :
    IsHomotopic C g f := by
  obtain ⟨w, hw⟩ := h
  refine ⟨(C.homMod X Y).neg w, ?_⟩
  rw [C.d_neg]
  have hz : castGraded neg_one_add_one ((C.homMod X Y).neg (C.d w)) =
      (C.homMod X Y).neg (castGraded neg_one_add_one (C.d w)) := by
    rfl
  rw [hz, ← hw]
  rw [(C.homMod X Y).sub_eq, (C.homMod X Y).sub_eq]
  have hna := (C.homMod X Y).neg_add f.val ((C.homMod X Y).neg g.val)
  have hnn := (C.homMod X Y).neg_neg g.val
  have hcomm := (C.homMod X Y).add_comm ((C.homMod X Y).neg f.val) g.val
  rw [hna, hnn, hcomm]

/-- Transitivity of chain homotopy. -/
theorem isHomotopic_trans {X Y : Obj} {f g k : ClosedHom0 C X Y}
    (h1 : IsHomotopic C f g) (h2 : IsHomotopic C g k) : IsHomotopic C f k := by
  obtain ⟨w1, hw1⟩ := h1
  obtain ⟨w2, hw2⟩ := h2
  refine ⟨(C.homMod X Y).add w1 w2, ?_⟩
  rw [C.d_add]
  have hz : castGraded neg_one_add_one ((C.homMod X Y).add (C.d w1) (C.d w2)) =
      (C.homMod X Y).add (castGraded neg_one_add_one (C.d w1)) (castGraded neg_one_add_one (C.d w2)) := by
    rfl
  rw [hz, ← hw1, ← hw2]
  rw [(C.homMod X Y).sub_eq, (C.homMod X Y).sub_eq, (C.homMod X Y).sub_eq]
  have ha1 := (C.homMod X Y).add_assoc f.val ((C.homMod X Y).neg g.val)
    ((C.homMod X Y).add g.val ((C.homMod X Y).neg k.val))
  have ha2 := (C.homMod X Y).add_assoc ((C.homMod X Y).neg g.val) g.val ((C.homMod X Y).neg k.val)
  have hcancel := (C.homMod X Y).add_left_neg g.val
  have hzero := (C.homMod X Y).zero_add ((C.homMod X Y).neg k.val)
  rw [ha1, ← ha2, hcancel, hzero]

/-- The 1-category of closed degree 0 morphisms $Z^0(\mathcal{C})$. -/
def Z0 : Category Obj where
  Hom := fun X Y => ClosedHom0 C X Y
  id := fun X => idClosed C X
  comp := fun {X Y Z} f g => compClosed C g f
  comp_assoc := by
    intro W X Y Z f g h
    cases f; cases g; cases h
    dsimp [compClosed]
    congr 1
    exact (C.comp_assoc0 _ _ _).symm
  id_comp := by
    intro X Y f
    cases f
    dsimp [compClosed, idClosed]
    congr 1
    exact C.comp_id0 _
  comp_id := by
    intro X Y f
    cases f
    dsimp [compClosed, idClosed]
    congr 1
    exact C.id_comp0 _

/-- The 0th cohomology category $H^0(\mathcal{C})$ of a DG-category. -/
def H0_category : Category Obj := C.H0

/-- Projection to $H^0(\mathcal{C})$ preserves identities. -/
theorem h0_preserves_id (X : Obj) : C.h0_proj (C.id X) = C.H0.id X :=
  C.h0_proj_id X

/-- Projection to $H^0(\mathcal{C})$ preserves composition. -/
theorem h0_preserves_comp {X Y Z : Obj} (f : C.Hom X Y 0) (g : C.Hom Y Z 0) :
    C.h0_proj (C.comp g f) = C.H0.comp (C.h0_proj f) (C.h0_proj g) :=
  C.h0_proj_comp f g

/-- Homotopic closed morphisms project to identical morphisms in $H^0(\mathcal{C})$. -/
theorem h0_homotopy_invariant {X Y : Obj} (f g : ClosedHom0 C X Y) (h : IsHomotopic C f g) :
    C.h0_proj f.val = C.h0_proj g.val := by
  obtain ⟨w, hw⟩ := h
  exact C.h0_homotopy_sound f.val g.val w hw

end DGCategory

end HigherCategoryTheory
