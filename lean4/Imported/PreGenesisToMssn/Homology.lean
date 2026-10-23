/- Imported from the sibling atlas so that this repository carries its own Lean evidence.
   Original path : omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/lean4/Homology.lean
   Original sha256: 13d8de140051cd505e7c0b204c030f30fa51b1102cbfc6b58563c92adecb758c (bytes as found)
   Imported on    : 2026-10-22
   Module         : Imported.PreGenesisToMssn.Homology
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.PreGenesisToMssn.Paper
import Init.Grind.Module.Basic

/-! Homology groups and induced maps for a fixed-degree chain-complex fragment.
All quotient and group laws are proved from the displayed additive-group laws.
No equivalence relation, induced-map injectivity or homology law is postulated.
-/
namespace PreMssn.Homology
open Lean.Grind
open AddCommMonoid AddCommGroup
universe u v

structure AddHom (A : Type u) (B : Type v) [AddCommGroup A] [AddCommGroup B] where
  toFun : A → B
  map_zero : toFun 0 = 0
  map_add : ∀ a b, toFun (a + b) = toFun a + toFun b

instance {A : Type u} {B : Type v} [AddCommGroup A] [AddCommGroup B] :
    CoeFun (AddHom A B) (fun _ => A → B) := ⟨AddHom.toFun⟩

theorem AddHom.map_neg {A : Type u} {B : Type v} [AddCommGroup A] [AddCommGroup B]
    (f : AddHom A B) (a : A) : f (-a) = -f a := by
  apply (add_left_inj (f a)).mp
  rw [← f.map_add, neg_add_cancel, f.map_zero, neg_add_cancel]

theorem AddHom.map_sub {A : Type u} {B : Type v} [AddCommGroup A] [AddCommGroup B]
    (f : AddHom A B) (a b : A) : f (a - b) = f a - f b := by
  rw [sub_eq_add_neg, f.map_add, f.map_neg, sub_eq_add_neg]

/-- The three consecutive degrees needed to define one homology group. -/
structure Complex where
  upper : Type u
  middle : Type u
  lower : Type u
  [upperGroup : AddCommGroup upper]
  [middleGroup : AddCommGroup middle]
  [lowerGroup : AddCommGroup lower]
  boundary : AddHom upper middle
  differential : AddHom middle lower
  square_zero : ∀ b, differential (boundary b) = 0

attribute [instance] Complex.upperGroup Complex.middleGroup Complex.lowerGroup

def Cycle (C : Complex.{u}) := {z : C.middle // C.differential z = 0}

instance cycleGroup (C : Complex.{u}) : AddCommGroup (Cycle C) where
  zero := ⟨0, C.differential.map_zero⟩
  add x y := ⟨x.val + y.val, by
    rw [C.differential.map_add, x.property, y.property, zero_add]⟩
  neg x := ⟨-x.val, by rw [C.differential.map_neg, x.property, neg_zero]⟩
  sub x y := ⟨x.val - y.val, by
    rw [C.differential.map_sub, x.property, y.property, sub_self]⟩
  add_zero x := Subtype.ext (add_zero x.val)
  add_comm x y := Subtype.ext (add_comm x.val y.val)
  add_assoc x y z := Subtype.ext (add_assoc x.val y.val z.val)
  neg_add_cancel x := Subtype.ext (neg_add_cancel x.val)
  sub_eq_add_neg x y := Subtype.ext (sub_eq_add_neg x.val y.val)

def boundaryCycle (C : Complex.{u}) : AddHom C.upper (Cycle C) where
  toFun b := ⟨C.boundary b, C.square_zero b⟩
  map_zero := Subtype.ext C.boundary.map_zero
  map_add a b := Subtype.ext (C.boundary.map_add a b)

section ImageQuotient
variable {A B : Type u} [AddCommGroup A] [AddCommGroup B] (f : AddHom A B)

/-- Equality modulo the image, expressed without a chosen representative. -/
def ImageRel (x y : B) : Prop := ∃ a, x = y + f a

theorem imageRel_refl (x : B) : ImageRel f x x := by
  refine ⟨0, ?_⟩
  rw [f.map_zero, add_zero]

theorem imageRel_symm {x y : B} (h : ImageRel f x y) : ImageRel f y x := by
  obtain ⟨a, ha⟩ := h
  refine ⟨-a, ?_⟩
  rw [f.map_neg, ha, add_assoc, add_neg_cancel, add_zero]

theorem imageRel_trans {x y z : B} (hxy : ImageRel f x y)
    (hyz : ImageRel f y z) : ImageRel f x z := by
  obtain ⟨a, ha⟩ := hxy
  obtain ⟨b, hb⟩ := hyz
  refine ⟨a + b, ?_⟩
  rw [ha, hb, f.map_add, add_assoc, add_comm (f b) (f a)]

def imageSetoid : Setoid B where
  r := ImageRel f
  iseqv := ⟨imageRel_refl f, fun h => imageRel_symm f h,
    fun h₁ h₂ => imageRel_trans f h₁ h₂⟩

def ImageQuotient := Quotient (imageSetoid f)

theorem imageRel_add {x x' y y' : B} (hx : ImageRel f x x')
    (hy : ImageRel f y y') : ImageRel f (x + y) (x' + y') := by
  obtain ⟨a, ha⟩ := hx
  obtain ⟨b, hb⟩ := hy
  refine ⟨a + b, ?_⟩
  rw [ha, hb, f.map_add, add_assoc, add_left_comm (f a) y', ← add_assoc]

theorem imageRel_neg {x y : B} (h : ImageRel f x y) : ImageRel f (-x) (-y) := by
  obtain ⟨a, ha⟩ := h
  refine ⟨-a, ?_⟩
  rw [ha, neg_add, f.map_neg]

def quotientZero : ImageQuotient f := Quotient.mk _ 0
def quotientAdd (x y : ImageQuotient f) : ImageQuotient f :=
  Quotient.liftOn₂ x y (fun a b => Quotient.mk _ (a + b))
    (fun _ _ _ _ h₁ h₂ => Quotient.sound (imageRel_add f h₁ h₂))
def quotientNeg (x : ImageQuotient f) : ImageQuotient f :=
  Quotient.liftOn x (fun a => Quotient.mk _ (-a))
    (fun _ _ h => Quotient.sound (imageRel_neg f h))
def quotientSub (x y : ImageQuotient f) : ImageQuotient f :=
  quotientAdd f x (quotientNeg f y)

instance quotientGroup : AddCommGroup (ImageQuotient f) where
  zero := quotientZero f
  add := quotientAdd f
  neg := quotientNeg f
  sub := quotientSub f
  add_zero x := by
    induction x using Quotient.inductionOn with
    | _ a => exact congrArg (Quotient.mk _) (add_zero a)
  add_comm x y := by
    induction x, y using Quotient.inductionOn₂ with
    | _ a b => exact congrArg (Quotient.mk _) (add_comm a b)
  add_assoc x y z := by
    induction x, y, z using Quotient.inductionOn₃ with
    | _ a b c => exact congrArg (Quotient.mk _) (add_assoc a b c)
  neg_add_cancel x := by
    induction x using Quotient.inductionOn with
    | _ a => exact congrArg (Quotient.mk _) (neg_add_cancel a)
  sub_eq_add_neg _ _ := rfl

def quotientProjection : AddHom B (ImageQuotient f) where
  toFun := Quotient.mk _
  map_zero := rfl
  map_add _ _ := rfl

theorem quotient_class_eq_iff (x y : B) :
    quotientProjection f x = quotientProjection f y ↔ ImageRel f x y :=
  ⟨fun h => Quotient.exact (s := imageSetoid f) h,
   fun h => Quotient.sound (s := imageSetoid f) h⟩

theorem quotient_class_zero_iff (x : B) :
    quotientProjection f x = 0 ↔ ∃ a, f a = x := by
  rw [show (0 : ImageQuotient f) = quotientProjection f 0 from rfl,
    quotient_class_eq_iff]
  constructor
  · rintro ⟨a, ha⟩
    have ha' : x = f a := by simpa only [zero_add] using ha
    exact ⟨a, ha'.symm⟩
  · rintro ⟨a, ha⟩
    exact ⟨a, by rw [ha, zero_add]⟩
end ImageQuotient

abbrev Homology (C : Complex.{u}) := ImageQuotient (boundaryCycle C)

structure Morphism (C D : Complex.{u}) where
  upper : AddHom C.upper D.upper
  middle : AddHom C.middle D.middle
  lower : AddHom C.lower D.lower
  boundary_commutes : ∀ b, middle (C.boundary b) = D.boundary (upper b)
  differential_commutes : ∀ z, lower (C.differential z) = D.differential (middle z)

def cycleMap {C D : Complex.{u}} (i : Morphism C D) : AddHom (Cycle C) (Cycle D) where
  toFun z := ⟨i.middle z.val, by
    rw [← i.differential_commutes, z.property, i.lower.map_zero]⟩
  map_zero := Subtype.ext i.middle.map_zero
  map_add x y := Subtype.ext (i.middle.map_add x.val y.val)

theorem cycleMap_boundary {C D : Complex.{u}} (i : Morphism C D) (b : C.upper) :
    cycleMap i (boundaryCycle C b) = boundaryCycle D (i.upper b) :=
  Subtype.ext (i.boundary_commutes b)

theorem cycleMap_respects_classes {C D : Complex.{u}} (i : Morphism C D)
    {x y : Cycle C} (h : ImageRel (boundaryCycle C) x y) :
    ImageRel (boundaryCycle D) (cycleMap i x) (cycleMap i y) := by
  obtain ⟨b, hb⟩ := h
  refine ⟨i.upper b, ?_⟩
  rw [hb, (cycleMap i).map_add, cycleMap_boundary]

def homologyMap {C D : Complex.{u}} (i : Morphism C D) :
    AddHom (Homology C) (Homology D) where
  toFun q := Quotient.liftOn q
    (fun z => quotientProjection (boundaryCycle D) (cycleMap i z))
    (fun _ _ h => Quotient.sound (cycleMap_respects_classes i h))
  map_zero := by
    change quotientProjection (boundaryCycle D) (cycleMap i 0) = 0
    rw [(cycleMap i).map_zero]
    rfl
  map_add x y := by
    induction x, y using Quotient.inductionOn₂ with
    | _ a b =>
      change quotientProjection (boundaryCycle D) (cycleMap i (a + b)) =
        quotientProjection (boundaryCycle D) (cycleMap i a + cycleMap i b)
      rw [(cycleMap i).map_add]

theorem induced_homology_retraction {C D : Complex.{u}}
    (i : Morphism C D) (r : Morphism D C)
    (fixes : ∀ z, r.middle (i.middle z) = z) (q : Homology C) :
    homologyMap r (homologyMap i q) = q := by
  induction q using Quotient.inductionOn with
  | _ z =>
    change Quotient.mk (imageSetoid (boundaryCycle C))
      (cycleMap r (cycleMap i z)) = Quotient.mk _ z
    apply congrArg (Quotient.mk _)
    exact Subtype.ext (fixes z.val)

/-- The induced homology homomorphism of a split chain map is injective. -/
theorem induced_homology_injective {C D : Complex.{u}}
    (i : Morphism C D) (r : Morphism D C)
    (fixes : ∀ z, r.middle (i.middle z) = z)
    (x y : Homology C) (h : homologyMap i x = homologyMap i y) : x = y := by
  have back := congrArg (homologyMap r) h
  simpa only [induced_homology_retraction i r fixes] using back

/-- An integral complex with middle homology Z modulo the image of k ↦ m*k. -/
def integerComplex (m : Int) : Complex where
  upper := Int
  middle := Int
  lower := Int
  boundary := {
    toFun := fun k => m * k
    map_zero := Int.mul_zero m
    map_add := fun a b => Int.mul_add m a b
  }
  differential := {
    toFun := fun _ => 0
    map_zero := rfl
    map_add := fun _ _ => rfl
  }
  square_zero _ := rfl

def integerCycle (m n : Int) : Cycle (integerComplex m) := ⟨n, rfl⟩
def integerClass (m n : Int) : Homology (integerComplex m) :=
  quotientProjection (boundaryCycle (integerComplex m)) (integerCycle m n)

theorem integer_class_eq_iff (m n p : Int) :
    integerClass m n = integerClass m p ↔ ∃ k, n = p + m*k := by
  unfold integerClass
  rw [quotient_class_eq_iff]
  constructor
  · rintro ⟨k, hk⟩
    exact ⟨k, congrArg Subtype.val hk⟩
  · rintro ⟨k, hk⟩
    exact ⟨k, Subtype.ext hk⟩

theorem integer_class_zero_iff (m n : Int) :
    integerClass m n = 0 ↔ ∃ k, m*k = n := by
  unfold integerClass
  rw [quotient_class_zero_iff]
  constructor
  · rintro ⟨k, hk⟩
    exact ⟨k, congrArg Subtype.val hk⟩
  · rintro ⟨k, hk⟩
    exact ⟨k, Subtype.ext hk⟩

/-- Lean's Euclidean remainder is nonnegative for either sign of modulus;
at modulus zero it returns the original integer. -/
def integerRepresentative (m n : Int) : Int := n % m

theorem integer_representative_classifies (m n p : Int) :
    integerClass m n = integerClass m p ↔
      integerRepresentative m n = integerRepresentative m p := by
  rw [integer_class_eq_iff]
  unfold integerRepresentative
  rw [Int.emod_eq_emod_iff_emod_sub_eq_zero, ← Int.dvd_iff_emod_eq_zero]
  constructor
  · rintro ⟨k, hk⟩
    exact ⟨k, by omega⟩
  · rintro ⟨k, hk⟩
    exact ⟨k, by omega⟩

theorem integral_two_torsion_nonzero : integerClass 2 1 ≠ 0 := by
  intro h
  obtain ⟨k, hk⟩ := (integer_class_zero_iff 2 1).mp h
  omega

theorem integral_two_torsion_doubles_to_zero :
    integerClass 2 1 + integerClass 2 1 = 0 := by
  change integerClass 2 2 = 0
  rw [integer_class_zero_iff]
  exact ⟨1, rfl⟩

end PreMssn.Homology
