/-!
# Mermin-Peres square as an F2 cochain obstruction

This is the linear Bool/F2 formulation of the QM_047 Mermin-Peres parity
packet. `false` is 0 / +1, `true` is 1 / -1, addition is xor, and `d0` is the
incidence matrix from variables to context products.

The concrete brute-force witness remains in `QM.MerminPeresCochainObstruction`.
This file is the main cochain theorem layer: the parity functional kills every
`d0` image because every variable appears in an even number of contexts, but it
does not kill the declared target sign vector.
-/

namespace QM
namespace MerminPeresF2

abbrev F2 := Bool

def add (x y : F2) : F2 := Bool.xor x y

def xorList (xs : List F2) : F2 := xs.foldl add false

def mask : F2 -> F2 -> F2
  | true, x => x
  | false, _ => false

inductive V where
  | a11 | a12 | a13
  | a21 | a22 | a23
  | a31 | a32 | a33

inductive C where
  | r1 | r2 | r3
  | c1 | c2 | c3

open V
open C

def allVariables : List V :=
  [a11, a12, a13, a21, a22, a23, a31, a32, a33]

def contexts : List C :=
  [r1, r2, r3, c1, c2, c3]

def row1 : V -> F2
  | a11 => true
  | a12 => true
  | a13 => true
  | a21 => false
  | a22 => false
  | a23 => false
  | a31 => false
  | a32 => false
  | a33 => false

def row2 : V -> F2
  | a11 => false
  | a12 => false
  | a13 => false
  | a21 => true
  | a22 => true
  | a23 => true
  | a31 => false
  | a32 => false
  | a33 => false

def row3 : V -> F2
  | a11 => false
  | a12 => false
  | a13 => false
  | a21 => false
  | a22 => false
  | a23 => false
  | a31 => true
  | a32 => true
  | a33 => true

def col1 : V -> F2
  | a11 => true
  | a12 => false
  | a13 => false
  | a21 => true
  | a22 => false
  | a23 => false
  | a31 => true
  | a32 => false
  | a33 => false

def col2 : V -> F2
  | a11 => false
  | a12 => true
  | a13 => false
  | a21 => false
  | a22 => true
  | a23 => false
  | a31 => false
  | a32 => true
  | a33 => false

def col3 : V -> F2
  | a11 => false
  | a12 => false
  | a13 => true
  | a21 => false
  | a22 => false
  | a23 => true
  | a31 => false
  | a32 => false
  | a33 => true

/-- Incidence matrix from contexts to variables. -/
def A : C -> V -> F2
  | r1 => row1
  | r2 => row2
  | r3 => row3
  | c1 => col1
  | c2 => col2
  | c3 => col3
abbrev Assignment := V -> F2

/-- `d0 a c` is the xor of assignment bits whose incidence in context `c` is 1. -/
def d0 (a : Assignment) (c : C) : F2 :=
  xorList (allVariables.map fun v => mask (A c v) (a v))

/-- Declared target sign vector: five positive contexts and one negative context. -/
def target : C -> F2
  | r1 => false
  | r2 => false
  | r3 => false
  | c1 => false
  | c2 => false
  | c3 => true

/-- Parity functional on context vectors. -/
def ell (y : C -> F2) : F2 :=
  xorList (contexts.map y)

def incidenceParity (v : V) : F2 :=
  xorList (contexts.map fun c => A c v)

theorem all_variable_incidences_even :
    forall v : V, incidenceParity v = false
  | a11 => rfl
  | a12 => rfl
  | a13 => rfl
  | a21 => rfl
  | a22 => rfl
  | a23 => rfl
  | a31 => rfl
  | a32 => rfl
  | a33 => rfl

theorem ell_d0_eq_false (a : Assignment) :
    ell (d0 a) = false := by
  change
    xorList
      [xorList [a a11, a a12, a a13, false, false, false, false, false, false],
       xorList [false, false, false, a a21, a a22, a a23, false, false, false],
       xorList [false, false, false, false, false, false, a a31, a a32, a a33],
       xorList [a a11, false, false, a a21, false, false, a a31, false, false],
       xorList [false, a a12, false, false, a a22, false, false, a a32, false],
       xorList [false, false, a a13, false, false, a a23, false, false, a a33]]
      = false
  cases a a11 <;>
  cases a a12 <;>
  cases a a13 <;>
  cases a a21 <;>
  cases a a22 <;>
  cases a a23 <;>
  cases a a31 <;>
  cases a a32 <;>
  cases a a33 <;>
  rfl

theorem ell_target_eq_true :
    ell target = true := by
  rfl

def InImageOfD0 (s : C -> F2) : Prop :=
  exists a : Assignment, d0 a = s

theorem target_not_in_image :
    Not (InImageOfD0 target) := by
  intro hImage
  cases hImage with
  | intro a hA =>
      have hZero : ell (d0 a) = false := ell_d0_eq_false a
      have hOne : ell (d0 a) = true := by
        rw [hA]
        exact ell_target_eq_true
      rw [hOne] at hZero
      cases hZero

def SatisfiesTarget (a : Assignment) : Prop :=
  d0 a = target

theorem no_global_assignment :
    Not (exists a : Assignment, SatisfiesTarget a) := by
  intro h
  exact target_not_in_image h

theorem mermin_peres_f2_cochain_obstruction :
    Not (InImageOfD0 target) :=
  target_not_in_image

end MerminPeresF2
end QM

#print axioms QM.MerminPeresF2.all_variable_incidences_even
#print axioms QM.MerminPeresF2.ell_d0_eq_false
#print axioms QM.MerminPeresF2.ell_target_eq_true
#print axioms QM.MerminPeresF2.target_not_in_image
#print axioms QM.MerminPeresF2.no_global_assignment
#print axioms QM.MerminPeresF2.mermin_peres_f2_cochain_obstruction