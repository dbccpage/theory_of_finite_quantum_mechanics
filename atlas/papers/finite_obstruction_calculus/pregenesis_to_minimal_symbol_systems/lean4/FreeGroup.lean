import GraphExtensions

/-! A nonabelian free group constructed from group terms modulo the group
laws. Its universal property is proved. A finite permutation interpretation
detects the two-generator commutator, while abelianization sends it to zero.
The comparison with continuous loops in a topological CW realization is a
separate obligation; it is not assumed by this algebraic construction. -/
namespace PreMssn.FreeGroup
universe u v w

class Group (G : Type u) extends One G, Mul G where
  inverse : G → G
  mul_one : ∀ a : G, a * 1 = a
  one_mul : ∀ a : G, 1 * a = a
  mul_assoc : ∀ a b c : G, (a*b)*c = a*(b*c)
  inverse_mul : ∀ a : G, inverse a * a = 1
  mul_inverse : ∀ a : G, a * inverse a = 1

attribute [instance] Group.toOne Group.toMul

def inv {G : Type u} [Group G] : G → G := Group.inverse

inductive Expr (A : Type u) where
  | one
  | gen (a : A)
  | mul (x y : Expr A)
  | inv (x : Expr A)

inductive Rel {A : Type u} : Expr A → Expr A → Prop where
  | refl (x) : Rel x x
  | symm {x y} : Rel x y → Rel y x
  | trans {x y z} : Rel x y → Rel y z → Rel x z
  | mul {x x' y y'} : Rel x x' → Rel y y' → Rel (.mul x y) (.mul x' y')
  | inv {x y} : Rel x y → Rel (.inv x) (.inv y)
  | mul_one (x) : Rel (.mul x .one) x
  | one_mul (x) : Rel (.mul .one x) x
  | mul_assoc (x y z) : Rel (.mul (.mul x y) z) (.mul x (.mul y z))
  | inverse_mul (x) : Rel (.mul (.inv x) x) .one
  | mul_inverse (x) : Rel (.mul x (.inv x)) .one

def exprSetoid (A : Type u) : Setoid (Expr A) where
  r := Rel
  iseqv := ⟨Rel.refl, Rel.symm, Rel.trans⟩

def Free (A : Type u) := Quotient (exprSetoid A)
def ofExpr {A : Type u} (x : Expr A) : Free A := Quotient.mk _ x
def gen {A : Type u} (a : A) : Free A := ofExpr (.gen a)

def freeMul {A : Type u} (x y : Free A) : Free A :=
  Quotient.liftOn₂ x y (fun a b => ofExpr (.mul a b))
    (fun _ _ _ _ h₁ h₂ => Quotient.sound (Rel.mul h₁ h₂))
def freeInv {A : Type u} (x : Free A) : Free A :=
  Quotient.liftOn x (fun a => ofExpr (.inv a))
    (fun _ _ h => Quotient.sound (Rel.inv h))

instance freeGroup (A : Type u) : Group (Free A) where
  one := ofExpr .one
  mul := freeMul
  inverse := freeInv
  mul_one x := by
    induction x using Quotient.inductionOn with
    | _ a => exact Quotient.sound (Rel.mul_one a)
  one_mul x := by
    induction x using Quotient.inductionOn with
    | _ a => exact Quotient.sound (Rel.one_mul a)
  mul_assoc x y z := by
    induction x, y, z using Quotient.inductionOn₃ with
    | _ a b c => exact Quotient.sound (Rel.mul_assoc a b c)
  inverse_mul x := by
    induction x using Quotient.inductionOn with
    | _ a => exact Quotient.sound (Rel.inverse_mul a)
  mul_inverse x := by
    induction x using Quotient.inductionOn with
    | _ a => exact Quotient.sound (Rel.mul_inverse a)

structure Hom (G : Type u) (H : Type v) [Group G] [Group H] where
  toFun : G → H
  map_one : toFun 1 = 1
  map_mul : ∀ a b, toFun (a*b) = toFun a * toFun b
  map_inv : ∀ a, toFun (inv a) = inv (toFun a)

instance {G : Type u} {H : Type v} [Group G] [Group H] :
    CoeFun (Hom G H) (fun _ => G → H) := ⟨Hom.toFun⟩

def Hom.comp {G : Type u} {H : Type v} {K : Type w} [Group G] [Group H] [Group K]
    (g : Hom H K) (f : Hom G H) : Hom G K where
  toFun a := g (f a)
  map_one := by rw [f.map_one, g.map_one]
  map_mul a b := by rw [f.map_mul, g.map_mul]
  map_inv a := by rw [f.map_inv, g.map_inv]

def interpret {A : Type u} {G : Type v} [Group G] (f : A → G) : Expr A → G
  | .one => 1
  | .gen a => f a
  | .mul x y => interpret f x * interpret f y
  | .inv x => inv (interpret f x)

theorem interpret_respects {A : Type u} {G : Type v} [Group G] (f : A → G)
    {x y : Expr A} (h : Rel x y) : interpret f x = interpret f y := by
  induction h with
  | refl => rfl
  | symm _ ih => exact ih.symm
  | trans _ _ ih₁ ih₂ => exact ih₁.trans ih₂
  | mul _ _ ih₁ ih₂ =>
    change interpret f _ * interpret f _ = interpret f _ * interpret f _
    rw [ih₁, ih₂]
  | inv _ ih => exact congrArg inv ih
  | mul_one x => exact Group.mul_one (interpret f x)
  | one_mul x => exact Group.one_mul (interpret f x)
  | mul_assoc x y z => exact Group.mul_assoc (interpret f x) (interpret f y) (interpret f z)
  | inverse_mul x => exact Group.inverse_mul (interpret f x)
  | mul_inverse x => exact Group.mul_inverse (interpret f x)

def extend {A : Type u} {G : Type v} [Group G] (f : A → G) : Hom (Free A) G where
  toFun q := Quotient.liftOn q (interpret f) (fun _ _ h => interpret_respects f h)
  map_one := rfl
  map_mul x y := by
    induction x, y using Quotient.inductionOn₂ with
    | _ a b => rfl
  map_inv x := by
    induction x using Quotient.inductionOn with
    | _ a => rfl

theorem extend_gen {A : Type u} {G : Type v} [Group G] (f : A → G) (a : A) :
    extend f (gen a) = f a := rfl

theorem hom_ext {A : Type u} {G : Type v} [Group G] (f g : Hom (Free A) G)
    (same : ∀ a, f (gen a) = g (gen a)) : ∀ q, f q = g q := by
  intro q
  induction q using Quotient.inductionOn with
  | _ x =>
    induction x with
    | one => exact f.map_one.trans g.map_one.symm
    | gen a => exact same a
    | mul x y ih₁ ih₂ =>
      change f (ofExpr x) = g (ofExpr x) at ih₁
      change f (ofExpr y) = g (ofExpr y) at ih₂
      change f (ofExpr x * ofExpr y) = g (ofExpr x * ofExpr y)
      rw [f.map_mul, g.map_mul, ih₁, ih₂]
    | inv x ih =>
      change f (ofExpr x) = g (ofExpr x) at ih
      change f (inv (ofExpr x)) = g (inv (ofExpr x))
      rw [f.map_inv, g.map_inv, ih]

theorem extension_unique {A : Type u} {G : Type v} [Group G] (f : A → G)
    (h : Hom (Free A) G) (on_gen : ∀ a, h (gen a) = f a) :
    ∀ q, h q = extend f q := hom_ext h (extend f) on_gen

def commutator {G : Type u} [Group G] (a b : G) : G := a * b * inv a * inv b

structure Perm (A : Type u) where
  forward : A → A
  backward : A → A
  left_inverse : ∀ a, backward (forward a) = a
  right_inverse : ∀ a, forward (backward a) = a

theorem Perm.ext {A : Type u} {p q : Perm A} (hf : p.forward = q.forward)
    (hb : p.backward = q.backward) : p = q := by
  cases p; cases q; cases hf; cases hb; rfl

instance permutationGroup (A : Type u) : Group (Perm A) where
  one := ⟨fun a => a, fun a => a, fun _ => rfl, fun _ => rfl⟩
  mul p q := ⟨fun a => p.forward (q.forward a), fun a => q.backward (p.backward a),
    fun a => by rw [p.left_inverse, q.left_inverse],
    fun a => by rw [q.right_inverse, p.right_inverse]⟩
  inverse p := ⟨p.backward, p.forward, p.right_inverse, p.left_inverse⟩
  mul_one _ := Perm.ext rfl rfl
  one_mul _ := Perm.ext rfl rfl
  mul_assoc _ _ _ := Perm.ext rfl rfl
  inverse_mul p := Perm.ext (funext p.left_inverse) (funext p.left_inverse)
  mul_inverse p := Perm.ext (funext p.right_inverse) (funext p.right_inverse)

def swap01 (i : Fin 3) : Fin 3 := if i = 0 then 1 else if i = 1 then 0 else i
def swap12 (i : Fin 3) : Fin 3 := if i = 1 then 2 else if i = 2 then 1 else i

theorem swap01_squared : ∀ i, swap01 (swap01 i) = i := by decide +kernel
theorem swap12_squared : ∀ i, swap12 (swap12 i) = i := by decide +kernel

def generatorPermutation (b : Bool) : Perm (Fin 3) :=
  if b then ⟨swap12, swap12, swap12_squared, swap12_squared⟩
  else ⟨swap01, swap01, swap01_squared, swap01_squared⟩

theorem two_generator_commutator_nontrivial :
    commutator (gen false) (gen true) ≠ (1 : Free Bool) := by
  have distinguishes : ((extend generatorPermutation)
      (commutator (gen false) (gen true))).forward 0 ≠ (0 : Fin 3) := by decide +kernel
  intro h
  apply distinguishes
  rw [h, (extend generatorPermutation).map_one]
  rfl

instance additiveFreeGroup (A : Type u) : Group (FreeAbelian.Free A) where
  one := 0
  mul a b := a+b
  inverse a := -a
  mul_one := Lean.Grind.AddCommMonoid.add_zero
  one_mul := Lean.Grind.AddCommMonoid.zero_add
  mul_assoc := Lean.Grind.AddCommMonoid.add_assoc
  inverse_mul := Lean.Grind.AddCommGroup.neg_add_cancel
  mul_inverse := Lean.Grind.AddCommGroup.add_neg_cancel

def abelianization {A : Type u} : Hom (Free A) (FreeAbelian.Free A) :=
  extend FreeAbelian.gen

theorem abelianized_commutator {A : Type u} (a b : Free A) :
    abelianization (commutator a b) = 0 := by
  rw [commutator, abelianization.map_mul, abelianization.map_mul, abelianization.map_mul,
    abelianization.map_inv, abelianization.map_inv]
  change (abelianization a + abelianization b) + -abelianization a + -abelianization b = 0
  open Lean.Grind.AddCommMonoid Lean.Grind.AddCommGroup in
    rw [add_assoc (abelianization a) (abelianization b) (-abelianization a),
      add_comm (abelianization b) (-abelianization a),
      ← add_assoc, add_neg_cancel, zero_add, add_neg_cancel]

structure AsMultiplicative (B : Type v) where
  val : B

theorem AsMultiplicative.ext {B : Type v} {a b : AsMultiplicative B} (h : a.val = b.val) :
    a = b := by cases a; cases b; cases h; rfl

instance multiplicativeGroup (B : Type v) [Lean.Grind.AddCommGroup B] :
    Group (AsMultiplicative B) where
  one := ⟨0⟩
  mul a b := ⟨a.val+b.val⟩
  inverse a := ⟨-a.val⟩
  mul_one a := AsMultiplicative.ext (Lean.Grind.AddCommMonoid.add_zero a.val)
  one_mul a := AsMultiplicative.ext (Lean.Grind.AddCommMonoid.zero_add a.val)
  mul_assoc a b c := AsMultiplicative.ext (Lean.Grind.AddCommMonoid.add_assoc a.val b.val c.val)
  inverse_mul a := AsMultiplicative.ext (Lean.Grind.AddCommGroup.neg_add_cancel a.val)
  mul_inverse a := AsMultiplicative.ext (Lean.Grind.AddCommGroup.add_neg_cancel a.val)

def abelianFactor {A : Type u} {B : Type v} [Lean.Grind.AddCommGroup B]
    (h : Hom (Free A) (AsMultiplicative B)) : Homology.AddHom (FreeAbelian.Free A) B :=
  FreeAbelian.extend (fun a => (h (gen a)).val)

def abelianFactorHom {A : Type u} {B : Type v} [Lean.Grind.AddCommGroup B]
    (h : Hom (Free A) (AsMultiplicative B)) : Hom (FreeAbelian.Free A) (AsMultiplicative B) where
  toFun a := ⟨abelianFactor h a⟩
  map_one := AsMultiplicative.ext (abelianFactor h).map_zero
  map_mul a b := AsMultiplicative.ext ((abelianFactor h).map_add a b)
  map_inv a := AsMultiplicative.ext ((abelianFactor h).map_neg a)

/-- Every homomorphism into an abelian target factors through the displayed
map into the free abelian group. This establishes the abelianization contract. -/
theorem abelianization_factors {A : Type u} {B : Type v} [Lean.Grind.AddCommGroup B]
    (h : Hom (Free A) (AsMultiplicative B)) (q : Free A) :
    (abelianFactorHom h) (abelianization q) = h q :=
  hom_ext ((abelianFactorHom h).comp abelianization) h (fun _ => rfl) q

theorem abelianization_factor_unique {A : Type u} {B : Type v} [Lean.Grind.AddCommGroup B]
    (h : Hom (Free A) (AsMultiplicative B)) (f : Homology.AddHom (FreeAbelian.Free A) B)
    (factors : ∀ q, f (abelianization q) = (h q).val) : ∀ a, f a = abelianFactor h a :=
  FreeAbelian.hom_ext f (abelianFactor h) (fun a => factors (gen a))

end PreMssn.FreeGroup
