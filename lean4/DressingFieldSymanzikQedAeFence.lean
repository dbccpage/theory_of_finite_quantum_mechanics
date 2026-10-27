/-!
Eight connected 3-edge subsets of one five-edge graph, and the cotree sum 247.

Edges, in order, are `(0,1), (0,2), (1,3), (2,3), (1,2)`.
No QED interval is constructed.
-/

namespace DressingFieldSymanzikQedAeFence

structure UF where
  p0 : Nat
  p1 : Nat
  p2 : Nat
  p3 : Nat

def start : UF := ⟨0, 1, 2, 3⟩

def parent (u : UF) : Nat → Nat
  | 0 => u.p0
  | 1 => u.p1
  | 2 => u.p2
  | 3 => u.p3
  | n => n

def find (u : UF) (x : Nat) : Nat :=
  let x1 := parent u x
  let x2 := parent u x1
  parent u x2

def union (u : UF) (a b : Nat) : UF :=
  let ra := find u a
  let rb := find u b
  bif ra == rb then u
  else bif rb == 0 then {u with p0 := ra}
  else bif rb == 1 then {u with p1 := ra}
  else bif rb == 2 then {u with p2 := ra}
  else bif rb == 3 then {u with p3 := ra}
  else u

def addEdge (u : UF) (i : Nat) : UF :=
  match i with
  | 0 => union u 0 1
  | 1 => union u 0 2
  | 2 => union u 1 3
  | 3 => union u 2 3
  | 4 => union u 1 2
  | _ => u

def addIf (u : UF) (mask i : Nat) : UF :=
  bif Nat.testBit mask i then addEdge u i else u

def run (mask : Nat) : UF :=
  addIf (addIf (addIf (addIf (addIf start mask 0) mask 1) mask 2) mask 3) mask 4

def ncomp (mask : Nat) : Nat :=
  let u := run mask
  let r0 := find u 0
  let r1 := find u 1
  let r2 := find u 2
  let r3 := find u 3
  let n1 := bif r1 == r0 then 0 else 1
  let n2 := bif r2 == r0 || r2 == r1 then 0 else 1
  let n3 := bif r3 == r0 || r3 == r1 || r3 == r2 then 0 else 1
  1 + n1 + n2 + n3

def pop5 (m : Nat) : Nat :=
  (if Nat.testBit m 0 then 1 else 0) +
  (if Nat.testBit m 1 then 1 else 0) +
  (if Nat.testBit m 2 then 1 else 0) +
  (if Nat.testBit m 3 then 1 else 0) +
  (if Nat.testBit m 4 then 1 else 0)

def weight (i : Nat) : Nat :=
  match i with
  | 0 => 2
  | 1 => 3
  | 2 => 5
  | 3 => 7
  | 4 => 11
  | _ => 0

def factor (w : Nat → Nat) (mask i : Nat) : Nat :=
  bif Nat.testBit mask i then 1 else w i

def prodW (w : Nat → Nat) (mask : Nat) : Nat :=
  factor w mask 0 * factor w mask 1 * factor w mask 2 * factor w mask 3 * factor w mask 4

def oneW (_ : Nat) : Nat := 1

def treeSum (w : Nat → Nat) : Nat :=
  prodW w 7 + prodW w 11 + prodW w 13 + prodW w 14 +
    prodW w 21 + prodW w 22 + prodW w 25 + prodW w 26

def isListed (m : Nat) : Bool :=
  m == 7 || m == 11 || m == 13 || m == 14 || m == 19 ||
    m == 21 || m == 22 || m == 25 || m == 26 || m == 28

def okMask (m : Nat) : Bool :=
  bif pop5 m == 3 then isListed m else true

def scan : Nat → Bool
  | 0 => okMask 0
  | n + 1 => okMask (n + 1) && scan n

theorem component_counts :
    ncomp 7 = 1 ∧ ncomp 11 = 1 ∧ ncomp 13 = 1 ∧ ncomp 14 = 1 ∧
    ncomp 21 = 1 ∧ ncomp 22 = 1 ∧ ncomp 25 = 1 ∧ ncomp 26 = 1 ∧
    ncomp 19 = 2 ∧ ncomp 28 = 2 := by
  decide

theorem three_bit_masks_are_listed : scan 31 = true := by
  decide

theorem cotree_sums :
    treeSum weight = 247 ∧ treeSum oneW = 8 := by
  decide

#print axioms DressingFieldSymanzikQedAeFence.component_counts
#print axioms DressingFieldSymanzikQedAeFence.three_bit_masks_are_listed
#print axioms DressingFieldSymanzikQedAeFence.cotree_sums

end DressingFieldSymanzikQedAeFence
