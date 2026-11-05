import ChainHomotopy

/-! Attaching an algebraic face with boundary m times the triangle cycle gives
H1 = Z/(m Z), including m=0 and negative m. No surface realization is inferred. -/
namespace PreMssn.TriangleDegree
open Homology TriangleHomology
open Lean.Grind AddCommMonoid AddCommGroup

def faceBoundary (m : Int) : AddHom Int Chain where
  toFun k := diagonal (m*k)
  map_zero := by
    change diagonal (m*0) = diagonal 0
    rw [Int.mul_zero]
  map_add a b := by
    change diagonal (m*(a+b)) = diagonal (m*a) + diagonal (m*b)
    rw [Int.mul_add]
    rfl

def complex (m : Int) : Complex where
  upper := Int
  middle := Chain
  lower := Chain
  boundary := faceBoundary m
  differential := differential
  square_zero _ := (kernel_iff _).mpr rfl

def coordinate : AddHom Chain Int where
  toFun a := a.x
  map_zero := rfl
  map_add _ _ := rfl

def diagonalHom : AddHom Int Chain where
  toFun := diagonal
  map_zero := rfl
  map_add _ _ := rfl

def toInteger (m : Int) : Morphism (complex m) (integerComplex m) where
  upper := AddHom.identity _
  middle := coordinate
  lower := AddHom.zero _ _
  boundary_commutes _ := rfl
  differential_commutes _ := rfl

def fromInteger (m : Int) : Morphism (integerComplex m) (complex m) where
  upper := AddHom.identity _
  middle := diagonalHom
  lower := AddHom.zero _ _
  boundary_commutes _ := rfl
  differential_commutes k := ((kernel_iff (diagonal k)).mpr rfl).symm

def h1Iso (m : Int) : AddIso (Homology (complex m)) (Homology (integerComplex m)) where
  forward := homologyMap (toInteger m)
  backward := homologyMap (fromInteger m)
  left_inverse q := by
    induction q using Quotient.inductionOn with
    | _ z =>
      apply congrArg (quotientProjection (boundaryCycle (complex m)))
      apply Subtype.ext
      exact ((kernel_iff z.val).mp z.property).symm
  right_inverse q := by
    induction q using Quotient.inductionOn with
    | _ z =>
      apply congrArg (quotientProjection (boundaryCycle (integerComplex m)))
      exact Subtype.ext rfl

def cycle (m k : Int) : Cycle (complex m) :=
  ⟨diagonal k, (kernel_iff (diagonal k)).mpr rfl⟩

def cycleClass (m k : Int) : Homology (complex m) :=
  quotientProjection (boundaryCycle (complex m)) (cycle m k)

theorem class_eq_iff (m k l : Int) :
    cycleClass m k = cycleClass m l ↔ ∃ t, k=l+m*t := by
  constructor
  · intro h
    have hi : integerClass m k = integerClass m l := congrArg (h1Iso m).forward h
    exact (integer_class_eq_iff m k l).mp hi
  · intro h
    have hi := (integer_class_eq_iff m k l).mpr h
    exact congrArg (h1Iso m).backward hi

theorem degree_two_torsion : cycleClass 2 1 ≠ 0 ∧ cycleClass 2 1 + cycleClass 2 1 = 0 := by
  constructor
  · intro h
    have hi : integerClass 2 1 = 0 := (congrArg (h1Iso 2).forward h).trans (h1Iso 2).forward.map_zero
    exact integral_two_torsion_nonzero hi
  · have hi := integral_two_torsion_doubles_to_zero
    have h := congrArg (h1Iso 2).backward hi
    have hc : (h1Iso 2).backward (integerClass 2 1) = cycleClass 2 1 := rfl
    rw [(h1Iso 2).backward.map_add, (h1Iso 2).backward.map_zero, hc] at h
    exact h

def classify (m : Int) (a : Chain) : Option Int :=
  if a.x == a.y && a.y == a.z then some (integerRepresentative m a.x) else none

theorem classify_refuses_iff (m : Int) (a : Chain) :
    classify m a = none ↔ differential a ≠ 0 := by
  simp [classify, kernel_coordinates_iff]

theorem classify_diagonal (m k : Int) :
    classify m (diagonal k) = some (integerRepresentative m k) := by
  simp [classify, diagonal]

theorem encoded_classification (m k l : Int) :
    classify m (diagonal k) = classify m (diagonal l) ↔ cycleClass m k = cycleClass m l := by
  rw [classify_diagonal, classify_diagonal, Option.some.injEq,
    ← integer_representative_classifies, integer_class_eq_iff, class_eq_iff]

end PreMssn.TriangleDegree
