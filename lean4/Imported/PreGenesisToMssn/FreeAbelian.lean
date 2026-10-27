/- Imported so that this repository carries its own Lean evidence.
   Original sha256: 3ebe59f3e8f0b99dc015094d27e723a6047d10e800954a924272540d8237befa (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.PreGenesisToMssn.FreeAbelian
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.PreGenesisToMssn.Homology

/-! The free abelian group on an arbitrary carrier, constructed as a term
quotient. The generated congruence has exactly the additive abelian-group laws.
Its interpretation in every additive abelian group is proved well-defined;
extension and uniqueness establish the free universal property.
-/
namespace PreMssn.FreeAbelian
open Lean.Grind
open AddCommMonoid AddCommGroup
open Homology
universe u v

inductive Expr (A : Type u) where
  | zero
  | gen (a : A)
  | add (x y : Expr A)
  | neg (x : Expr A)

inductive Rel {A : Type u} : Expr A → Expr A → Prop where
  | refl (x) : Rel x x
  | symm {x y} : Rel x y → Rel y x
  | trans {x y z} : Rel x y → Rel y z → Rel x z
  | add {x x' y y'} : Rel x x' → Rel y y' → Rel (.add x y) (.add x' y')
  | neg {x y} : Rel x y → Rel (.neg x) (.neg y)
  | add_zero (x) : Rel (.add x .zero) x
  | add_comm (x y) : Rel (.add x y) (.add y x)
  | add_assoc (x y z) : Rel (.add (.add x y) z) (.add x (.add y z))
  | neg_add_cancel (x) : Rel (.add (.neg x) x) .zero

def exprSetoid (A : Type u) : Setoid (Expr A) where
  r := Rel
  iseqv := ⟨Rel.refl, Rel.symm, Rel.trans⟩

def Free (A : Type u) := Quotient (exprSetoid A)
def ofExpr {A : Type u} (x : Expr A) : Free A := Quotient.mk _ x
def gen {A : Type u} (a : A) : Free A := ofExpr (.gen a)

def freeAdd {A : Type u} (x y : Free A) : Free A :=
  Quotient.liftOn₂ x y (fun a b => ofExpr (.add a b))
    (fun _ _ _ _ h₁ h₂ => Quotient.sound (Rel.add h₁ h₂))
def freeNeg {A : Type u} (x : Free A) : Free A :=
  Quotient.liftOn x (fun a => ofExpr (.neg a))
    (fun _ _ h => Quotient.sound (Rel.neg h))

instance freeGroup (A : Type u) : AddCommGroup (Free A) where
  zero := ofExpr .zero
  add := freeAdd
  neg := freeNeg
  sub x y := freeAdd x (freeNeg y)
  add_zero x := by
    induction x using Quotient.inductionOn with
    | _ a => exact Quotient.sound (Rel.add_zero a)
  add_comm x y := by
    induction x, y using Quotient.inductionOn₂ with
    | _ a b => exact Quotient.sound (Rel.add_comm a b)
  add_assoc x y z := by
    induction x, y, z using Quotient.inductionOn₃ with
    | _ a b c => exact Quotient.sound (Rel.add_assoc a b c)
  neg_add_cancel x := by
    induction x using Quotient.inductionOn with
    | _ a => exact Quotient.sound (Rel.neg_add_cancel a)
  sub_eq_add_neg _ _ := rfl

def interpret {A : Type u} {B : Type v} [AddCommGroup B] (f : A → B) : Expr A → B
  | .zero => 0
  | .gen a => f a
  | .add x y => interpret f x + interpret f y
  | .neg x => -interpret f x

theorem interpret_respects {A : Type u} {B : Type v} [AddCommGroup B] (f : A → B)
    {x y : Expr A} (h : Rel x y) : interpret f x = interpret f y := by
  induction h with
  | refl => rfl
  | symm _ ih => exact ih.symm
  | trans _ _ ih₁ ih₂ => exact ih₁.trans ih₂
  | add _ _ ih₁ ih₂ =>
    change interpret f _ + interpret f _ = interpret f _ + interpret f _
    rw [ih₁, ih₂]
  | neg _ ih => exact congrArg (-·) ih
  | add_zero x => exact add_zero (interpret f x)
  | add_comm x y => exact add_comm (interpret f x) (interpret f y)
  | add_assoc x y z => exact add_assoc (interpret f x) (interpret f y) (interpret f z)
  | neg_add_cancel x => exact neg_add_cancel (interpret f x)

def extend {A : Type u} {B : Type v} [AddCommGroup B] (f : A → B) : AddHom (Free A) B where
  toFun q := Quotient.liftOn q (interpret f) (fun _ _ h => interpret_respects f h)
  map_zero := rfl
  map_add x y := by
    induction x, y using Quotient.inductionOn₂ with
    | _ a b => rfl

theorem extend_gen {A : Type u} {B : Type v} [AddCommGroup B] (f : A → B) (a : A) :
    extend f (gen a) = f a := rfl

theorem hom_ext {A : Type u} {B : Type v} [AddCommGroup B]
    (f g : AddHom (Free A) B) (same : ∀ a, f (gen a) = g (gen a)) :
    ∀ q, f q = g q := by
  intro q
  induction q using Quotient.inductionOn with
  | _ x =>
    induction x with
    | zero => exact f.map_zero.trans g.map_zero.symm
    | gen a => exact same a
    | add x y ih₁ ih₂ =>
      change f (ofExpr x) = g (ofExpr x) at ih₁
      change f (ofExpr y) = g (ofExpr y) at ih₂
      change f (ofExpr x + ofExpr y) = g (ofExpr x + ofExpr y)
      rw [f.map_add, g.map_add, ih₁, ih₂]
    | neg x ih =>
      change f (ofExpr x) = g (ofExpr x) at ih
      change f (-ofExpr x) = g (-ofExpr x)
      rw [f.map_neg, g.map_neg, ih]

theorem extension_unique {A : Type u} {B : Type v} [AddCommGroup B]
    (f : A → B) (h : AddHom (Free A) B) (on_gen : ∀ a, h (gen a) = f a) :
    ∀ q, h q = extend f q := hom_ext h (extend f) on_gen

def map {A : Type u} {B : Type v} (f : A → B) : AddHom (Free A) (Free B) :=
  extend (fun a => gen (f a))

theorem map_gen {A : Type u} {B : Type v} (f : A → B) (a : A) :
    map f (gen a) = gen (f a) := rfl

end PreMssn.FreeAbelian

namespace PreMssn.Homology
open Lean.Grind
open AddCommMonoid AddCommGroup
universe u v w

def AddHom.comp {A : Type u} {B : Type v} {C : Type w}
    [AddCommGroup A] [AddCommGroup B] [AddCommGroup C]
    (g : AddHom B C) (f : AddHom A B) : AddHom A C where
  toFun a := g (f a)
  map_zero := by rw [f.map_zero, g.map_zero]
  map_add a b := by rw [f.map_add, g.map_add]

def AddHom.identity (A : Type u) [AddCommGroup A] : AddHom A A where
  toFun a := a
  map_zero := rfl
  map_add _ _ := rfl

def AddHom.zero (A : Type u) (B : Type v) [AddCommGroup A] [AddCommGroup B] : AddHom A B where
  toFun _ := 0
  map_zero := rfl
  map_add _ _ := (zero_add 0).symm

def quotientDescend {A B C : Type u} [AddCommGroup A] [AddCommGroup B] [AddCommGroup C]
    (f : AddHom A B) (g : AddHom B C) (kills : ∀ a, g (f a) = 0) :
    AddHom (ImageQuotient f) C where
  toFun q := Quotient.liftOn q g (by
    intro x y h
    obtain ⟨a, ha⟩ := h
    rw [ha, g.map_add, kills, add_zero])
  map_zero := g.map_zero
  map_add x y := by
    induction x, y using Quotient.inductionOn₂ with
    | _ a b => exact g.map_add a b

structure AddIso (A : Type u) (B : Type v) [AddCommGroup A] [AddCommGroup B] where
  forward : AddHom A B
  backward : AddHom B A
  left_inverse : ∀ a, backward (forward a) = a
  right_inverse : ∀ b, forward (backward b) = b

def AddIso.comp {A : Type u} {B : Type v} {C : Type w}
    [AddCommGroup A] [AddCommGroup B] [AddCommGroup C]
    (f : AddIso A B) (g : AddIso B C) : AddIso A C where
  forward := g.forward.comp f.forward
  backward := f.backward.comp g.backward
  left_inverse a := by
    change f.backward (g.backward (g.forward (f.forward a))) = a
    rw [g.left_inverse, f.left_inverse]
  right_inverse c := by
    change g.forward (f.forward (f.backward (g.backward c))) = c
    rw [f.right_inverse, g.right_inverse]

end PreMssn.Homology
