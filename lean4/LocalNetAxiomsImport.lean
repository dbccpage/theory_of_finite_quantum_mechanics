/-!
Finite four-point order and two-site integer matrices.

No continuum region index and no Minkowski light cone are constructed.
This module does not import CausalOrder.lean.
-/

namespace LocalNetAxiomsImport

def relBool (i j : Nat) : Bool :=
  (i == 0 && j == 2) || (i == 1 && j == 2) || (i == 1 && j == 3)

def spacelike (i j : Nat) : Bool :=
  i != j && !relBool i j && !relBool j i

def tripleOk (x y z : Nat) : Bool :=
  bif relBool x y && relBool y z then relBool x z else true

def scanTriples : Nat → Bool
  | 0 => tripleOk 0 0 0
  | n + 1 =>
    let k := n + 1
    tripleOk (k / 16) ((k / 4) % 4) (k % 4) && scanTriples n

def irreflOk : Bool :=
  !relBool 0 0 && !relBool 1 1 && !relBool 2 2 && !relBool 3 3

def relCount : Nat :=
  (if relBool 0 0 then 1 else 0) + (if relBool 0 1 then 1 else 0) +
  (if relBool 0 2 then 1 else 0) + (if relBool 0 3 then 1 else 0) +
  (if relBool 1 0 then 1 else 0) + (if relBool 1 1 then 1 else 0) +
  (if relBool 1 2 then 1 else 0) + (if relBool 1 3 then 1 else 0) +
  (if relBool 2 0 then 1 else 0) + (if relBool 2 1 then 1 else 0) +
  (if relBool 2 2 then 1 else 0) + (if relBool 2 3 then 1 else 0) +
  (if relBool 3 0 then 1 else 0) + (if relBool 3 1 then 1 else 0) +
  (if relBool 3 2 then 1 else 0) + (if relBool 3 3 then 1 else 0)

def spacelikeUnordered : Nat :=
  (if spacelike 0 1 then 1 else 0) + (if spacelike 0 2 then 1 else 0) +
  (if spacelike 0 3 then 1 else 0) + (if spacelike 1 2 then 1 else 0) +
  (if spacelike 1 3 then 1 else 0) + (if spacelike 2 3 then 1 else 0)

theorem n_poset_pair_counts :
    scanTriples 63 = true ∧ irreflOk = true ∧ relCount = 3 ∧ spacelikeUnordered = 3 ∧
    spacelike 0 1 = true ∧ spacelike 1 0 = true ∧
    spacelike 0 3 = true ∧ spacelike 3 0 = true ∧
    spacelike 2 3 = true ∧ spacelike 3 2 = true ∧
    spacelike 0 2 = false ∧ spacelike 1 2 = false ∧ spacelike 1 3 = false := by
  decide

structure M2 where
  a : Int
  b : Int
  c : Int
  d : Int
deriving DecidableEq, Repr

def mm (x y : M2) : M2 where
  a := x.a * y.a + x.b * y.c
  b := x.a * y.b + x.b * y.d
  c := x.c * y.a + x.d * y.c
  d := x.c * y.b + x.d * y.d

def add2 (x y : M2) : M2 where
  a := x.a + y.a
  b := x.b + y.b
  c := x.c + y.c
  d := x.d + y.d

def trp (x : M2) : M2 where
  a := x.a
  b := x.c
  c := x.b
  d := x.d

def det2 (x : M2) : Int := x.a * x.d - x.b * x.c

def z2 : M2 := ⟨0, 0, 0, 0⟩
def I2 : M2 := ⟨1, 0, 0, 1⟩
def Xm : M2 := ⟨0, 1, 1, 0⟩
def Zm : M2 := ⟨1, 0, 0, -1⟩
def Am : M2 := ⟨1, 2, 3, 4⟩
def Bm : M2 := ⟨5, 6, 7, 8⟩

structure M4 where
  a00 : Int
  a01 : Int
  a02 : Int
  a03 : Int
  a10 : Int
  a11 : Int
  a12 : Int
  a13 : Int
  a20 : Int
  a21 : Int
  a22 : Int
  a23 : Int
  a30 : Int
  a31 : Int
  a32 : Int
  a33 : Int
deriving DecidableEq, Repr

def kron (x y : M2) : M4 where
  a00 := x.a * y.a
  a01 := x.a * y.b
  a02 := x.b * y.a
  a03 := x.b * y.b
  a10 := x.a * y.c
  a11 := x.a * y.d
  a12 := x.b * y.c
  a13 := x.b * y.d
  a20 := x.c * y.a
  a21 := x.c * y.b
  a22 := x.d * y.a
  a23 := x.d * y.b
  a30 := x.c * y.c
  a31 := x.c * y.d
  a32 := x.d * y.c
  a33 := x.d * y.d

def row (m : M4) : Nat → Int × Int × Int × Int
  | 0 => (m.a00, m.a01, m.a02, m.a03)
  | 1 => (m.a10, m.a11, m.a12, m.a13)
  | 2 => (m.a20, m.a21, m.a22, m.a23)
  | 3 => (m.a30, m.a31, m.a32, m.a33)
  | _ => (0, 0, 0, 0)

def col (m : M4) : Nat → Int × Int × Int × Int
  | 0 => (m.a00, m.a10, m.a20, m.a30)
  | 1 => (m.a01, m.a11, m.a21, m.a31)
  | 2 => (m.a02, m.a12, m.a22, m.a32)
  | 3 => (m.a03, m.a13, m.a23, m.a33)
  | _ => (0, 0, 0, 0)

def dot4 (r c : Int × Int × Int × Int) : Int :=
  r.1 * c.1 + r.2.1 * c.2.1 + r.2.2.1 * c.2.2.1 + r.2.2.2 * c.2.2.2

def mm4 (p q : M4) : M4 where
  a00 := dot4 (row p 0) (col q 0)
  a01 := dot4 (row p 0) (col q 1)
  a02 := dot4 (row p 0) (col q 2)
  a03 := dot4 (row p 0) (col q 3)
  a10 := dot4 (row p 1) (col q 0)
  a11 := dot4 (row p 1) (col q 1)
  a12 := dot4 (row p 1) (col q 2)
  a13 := dot4 (row p 1) (col q 3)
  a20 := dot4 (row p 2) (col q 0)
  a21 := dot4 (row p 2) (col q 1)
  a22 := dot4 (row p 2) (col q 2)
  a23 := dot4 (row p 2) (col q 3)
  a30 := dot4 (row p 3) (col q 0)
  a31 := dot4 (row p 3) (col q 1)
  a32 := dot4 (row p 3) (col q 2)
  a33 := dot4 (row p 3) (col q 3)

def sum4 (m : M4) : Int :=
  let s (r : Int × Int × Int × Int) := r.1 + r.2.1 + r.2.2.1 + r.2.2.2
  s (row m 0) + s (row m 1) + s (row m 2) + s (row m 3)

def leftEmb : M4 := kron Am I2
def rightEmb : M4 := kron I2 Bm
def prodAB : M4 := kron Am Bm
def sameLeft : M4 := mm4 (kron Xm I2) (kron Zm I2)
def sameRight : M4 := mm4 (kron Zm I2) (kron Xm I2)

theorem disjoint_site_products :
    mm4 leftEmb rightEmb = prodAB ∧
    mm4 rightEmb leftEmb = prodAB ∧
    sum4 prodAB = 260 := by
  decide

theorem same_site_and_star :
    add2 (mm Xm Zm) (mm Zm Xm) = z2 ∧
    mm Xm Zm ≠ mm Zm Xm ∧
    sameLeft ≠ sameRight ∧
    sameLeft.a02 = -1 ∧
    sameRight.a02 = 1 ∧
    mm I2 Am = Am ∧ mm Am I2 = Am ∧
    mm I2 Bm = Bm ∧ mm Bm I2 = Bm ∧
    mm I2 Xm = Xm ∧ mm Xm I2 = Xm ∧
    mm I2 Zm = Zm ∧ mm Zm I2 = Zm ∧
    trp (trp Am) = Am ∧
    trp (mm Am Bm) = mm (trp Bm) (trp Am) ∧
    det2 Am = -2 ∧ det2 Bm = -2 ∧ det2 Xm = -1 ∧ det2 Zm = -1 := by
  decide

#print axioms LocalNetAxiomsImport.n_poset_pair_counts
#print axioms LocalNetAxiomsImport.disjoint_site_products
#print axioms LocalNetAxiomsImport.same_site_and_star

end LocalNetAxiomsImport
