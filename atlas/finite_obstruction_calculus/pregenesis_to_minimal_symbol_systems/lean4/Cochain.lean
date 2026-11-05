import TriangleHomology

/-! The dual cochain construction. Cochains are actual additive homomorphisms
into an arbitrary abelian coefficient group. Coboundary is precomposition with
the chain differential, and the square-zero equation is proved pointwise. -/
namespace PreMssn.Cochain
open Lean.Grind
open AddCommMonoid AddCommGroup
open Homology
universe u v

theorem hom_ext {A : Type u} {B : Type v} [AddCommGroup A] [AddCommGroup B]
    {f g : AddHom A B} (h : ∀ a, f a = g a) : f = g := by
  cases f with
  | mk ff fz fa =>
    cases g with
    | mk gf gz ga =>
      have hf : ff = gf := funext h
      cases hf
      rfl

def homAdd {A : Type u} {B : Type v} [AddCommGroup A] [AddCommGroup B]
    (f g : AddHom A B) : AddHom A B where
  toFun a := f a + g a
  map_zero := by rw [f.map_zero, g.map_zero, zero_add]
  map_add a b := by
    rw [f.map_add, g.map_add, add_assoc, add_left_comm (f b) (g a), ← add_assoc]

def homNeg {A : Type u} {B : Type v} [AddCommGroup A] [AddCommGroup B]
    (f : AddHom A B) : AddHom A B where
  toFun a := -f a
  map_zero := by rw [f.map_zero, neg_zero]
  map_add a b := by rw [f.map_add, neg_add]

instance homGroup {A : Type u} {B : Type v} [AddCommGroup A] [AddCommGroup B] :
    AddCommGroup (AddHom A B) where
  zero := AddHom.zero A B
  add := homAdd
  neg := homNeg
  sub f g := homAdd f (homNeg g)
  add_zero f := hom_ext (fun a => add_zero (f a))
  add_comm f g := hom_ext (fun a => add_comm (f a) (g a))
  add_assoc f g h := hom_ext (fun a => add_assoc (f a) (g a) (h a))
  neg_add_cancel f := hom_ext (fun a => neg_add_cancel (f a))
  sub_eq_add_neg _ _ := rfl

/-- Precomposition reverses the arrow, and is additive in the cochain. -/
def precompose {A : Type u} {B : Type u} {R : Type v}
    [AddCommGroup A] [AddCommGroup B] [AddCommGroup R] (d : AddHom A B) :
    AddHom (AddHom B R) (AddHom A R) where
  toFun φ := φ.comp d
  map_zero := hom_ext (fun _ => rfl)
  map_add _ _ := hom_ext (fun _ => rfl)

def dual (C : Complex.{u}) (R : Type v) [AddCommGroup R] : Complex where
  upper := AddHom C.lower R
  middle := AddHom C.middle R
  lower := AddHom C.upper R
  boundary := precompose C.differential
  differential := precompose C.boundary
  square_zero φ := hom_ext (fun b => by
    change φ (C.differential (C.boundary b)) = 0
    rw [C.square_zero, φ.map_zero])

theorem dual_differential (C : Complex.{u}) (R : Type v) [AddCommGroup R] :
    (dual C R).differential = precompose C.boundary := rfl

theorem coboundary_formula (C : Complex.{u}) (R : Type v) [AddCommGroup R]
    (φ : AddHom C.middle R) (b : C.upper) :
    (precompose C.boundary φ).toFun b = φ (C.boundary b) := rfl

theorem coboundary_square_zero (C : Complex.{u}) (R : Type v) [AddCommGroup R]
    (φ : AddHom C.lower R) :
    (dual C R).differential ((dual C R).boundary φ) = 0 := (dual C R).square_zero φ

abbrev IntegralCohomology (C : Complex.{u}) := Homology (dual C Int)

/-- A chain map pulls cochains back, reversing its direction. -/
def dualMorphism {C D : Complex.{u}} (i : Morphism C D) (R : Type v) [AddCommGroup R] :
    Morphism (dual D R) (dual C R) where
  upper := precompose i.lower
  middle := precompose i.middle
  lower := precompose i.upper
  boundary_commutes φ := hom_ext (fun a =>
    congrArg (show AddHom D.lower R from φ).toFun (i.differential_commutes a).symm)
  differential_commutes φ := hom_ext (fun a =>
    congrArg (show AddHom D.middle R from φ).toFun (i.boundary_commutes a).symm)

theorem cohomology_retraction {C D : Complex.{u}} (i : Morphism C D) (r : Morphism D C)
    (fixes : ∀ a, r.middle (i.middle a) = a) (R : Type v) [AddCommGroup R]
    (q : Homology (dual C R)) :
    homologyMap (dualMorphism i R) (homologyMap (dualMorphism r R) q) = q := by
  apply induced_homology_retraction (dualMorphism r R) (dualMorphism i R) _ q
  intro φ
  apply hom_ext
  intro a
  exact congrArg (show AddHom C.middle R from φ).toFun (fixes a)

theorem cohomology_pullback_surjective {C D : Complex.{u}}
    (i : Morphism C D) (r : Morphism D C)
    (fixes : ∀ a, r.middle (i.middle a) = a) (R : Type v) [AddCommGroup R]
    (q : Homology (dual C R)) :
    ∃ p, homologyMap (dualMorphism i R) p = q :=
  ⟨homologyMap (dualMorphism r R) q, cohomology_retraction i r fixes R q⟩

def triangleCochain (p q r : Int) : AddHom TriangleHomology.Chain Int where
  toFun a := p * a.x + q * a.y + r * a.z
  map_zero := by
    change p * 0 + q * 0 + r * 0 = 0
    simp
  map_add a b := by
    change p * (a.x + b.x) + q * (a.y + b.y) + r * (a.z + b.z) =
      (p * a.x + q * a.y + r * a.z) + (p * b.x + q * b.y + r * b.z)
    simp only [Int.mul_add]
    omega

/-- For the attached face, the integral coboundary is the sum of its edge
cochain coordinates. This relates the runtime formula to precomposition. -/
theorem triangle_face_coboundary (p q r k : Int) :
    (precompose TriangleHomology.faceBoundary (triangleCochain p q r)).toFun k =
      (p + q + r) * k := by
  change p * k + q * k + r * k = (p + q + r) * k
  simp only [Int.add_mul]

def triangleCoordinate (p q r : Int) : Int := p + q + r

theorem triangle_coordinate_correct (p q r : Int) :
    triangleCoordinate p q r =
      (precompose TriangleHomology.faceBoundary (triangleCochain p q r)).toFun 1 := by
  rw [triangle_face_coboundary, Int.mul_one]
  rfl

/-- The vertex-potential repair used at the WDP handoff has zero circulation. -/
theorem triangle_potential_coboundary (a b c : Int) :
    precompose TriangleHomology.differential (triangleCochain a b c) =
      triangleCochain (b-a) (c-b) (a-c) := by
  apply hom_ext
  intro z
  change a*(z.z-z.x) + b*(z.x-z.y) + c*(z.y-z.z) =
    (b-a)*z.x + (c-b)*z.y + (a-c)*z.z
  simp only [Int.mul_sub, Int.sub_mul]
  omega

theorem triangle_potential_circulation (a b c : Int) :
    triangleCoordinate (b-a) (c-b) (a-c) = 0 := by
  unfold triangleCoordinate
  omega

theorem triangle_repair_invariant (p q r a b c : Int) :
    triangleCoordinate (p-(b-a)) (q-(c-b)) (r-(a-c)) = triangleCoordinate p q r := by
  unfold triangleCoordinate
  omega

/-- Zero circulation is also sufficient for an integral potential repair. -/
theorem triangle_repair_exact_iff (p q r : Int) :
    (∃ a b c : Int, p=b-a ∧ q=c-b ∧ r=a-c) ↔ triangleCoordinate p q r = 0 := by
  unfold triangleCoordinate
  constructor
  · rintro ⟨a,b,c,hp,hq,hr⟩
    omega
  · intro h
    exact ⟨0,p,p+q,by omega,by omega,by omega⟩

theorem triangle_constant_not_repairable (a b c : Int) :
    ¬ (1-(b-a)=0 ∧ 1-(c-b)=0 ∧ 1-(a-c)=0) := by omega

end PreMssn.Cochain
