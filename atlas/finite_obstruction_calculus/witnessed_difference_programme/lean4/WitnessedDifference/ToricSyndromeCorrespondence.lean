import Std

/-! Concrete L = 3 encoding of the periodic toric commutation syndrome.
    Lattice assumption: periodic Z_3 x Z_3, one qubit on each edge.
    Weight convention of the shipped checker: wt(e) = |supp e_X| + |supp e_Z|.
    These theorems are the binary encoding obligations. They are not a
    formalization of a physical readout or of the analytic locality bounds. -/

namespace WitnessedDifference.ToricSyndromeCorrespondence

def bitGet (row : List Bool) (j : Nat) : Bool :=
  row.getD j false

def bitZip (a b : List Bool) : List Bool :=
  List.zipWith Bool.xor a b

def findPivot (rows : List (List Bool)) (col start : Nat) : Option Nat :=
  let rec go (i : Nat) (rest : List (List Bool)) : Option Nat :=
    match rest with
    | [] => none
    | row :: tail =>
      if i < start then go (i + 1) tail
      else if bitGet row col then some i
      else go (i + 1) tail
  go 0 rows

def swapRows (rows : List (List Bool)) (i j : Nat) : List (List Bool) :=
  if i = j then rows else
    let ri := rows.getD i []
    let rj := rows.getD j []
    let rec go : Nat → List (List Bool) → List (List Bool)
      | _, [] => []
      | k, row :: tail =>
        let row' := if k = i then rj else if k = j then ri else row
        row' :: go (k + 1) tail
    go 0 rows

def clearColumn (prow : List Bool) (pivot col i : Nat) (rows : List (List Bool)) :
    List (List Bool) :=
  match rows with
  | [] => []
  | row :: tail =>
    let row' := if i ≠ pivot && bitGet row col then bitZip row prow else row
    row' :: clearColumn prow pivot col (i + 1) tail

def rankFuel (fuel col start width : Nat) (rows : List (List Bool)) : Nat :=
  match fuel with
  | 0 => 0
  | fuel' + 1 =>
    if col ≥ width then 0
    else
      match findPivot rows col start with
      | none => rankFuel fuel' (col + 1) start width rows
      | some p =>
        let swapped := swapRows rows start p
        match swapped[start]? with
        | none => 0
        | some prow =>
          1 + rankFuel fuel' (col + 1) (start + 1) width
            (clearColumn prow start col 0 swapped)

def matrixRank (rows : List (List Bool)) : Nat :=
  let width := (rows.head?.map List.length).getD 0
  rankFuel width 0 0 width rows

def dot (a b : List Bool) : Bool :=
  (List.zip a b).foldl (fun acc p => Bool.xor acc (p.1 && p.2)) false

def mulVec (rows : List (List Bool)) (v : List Bool) : List Bool :=
  rows.map (fun row => dot row v)

def weight (v : List Bool) : Nat :=
  v.foldl (fun n b => if b then n + 1 else n) 0

theorem commutation_quotient_dimension (L : Nat) (hL : 1 ≤ L) :
    (2 * L * L + 2) - (2 * L * L - 2) = 4 := by
  have hsq : 1 * 1 ≤ L * L := Nat.mul_le_mul hL hL
  have hone : 1 ≤ L * L := by simpa [Nat.one_mul] using hsq
  have hmul : 2 * 1 ≤ 2 * (L * L) := Nat.mul_le_mul_left 2 hone
  have h2 : 2 ≤ 2 * L * L := by
    simpa [Nat.mul_one, Nat.mul_assoc] using hmul
  have cancel : (2 * L * L - 2) + 2 = 2 * L * L := Nat.sub_add_cancel h2
  have bridge : 2 + (2 * L * L - 2) = 2 * L * L := by
    rw [Nat.add_comm, cancel]
  have four : (4 : Nat) = 2 + 2 := rfl
  have key : 4 + (2 * L * L - 2) = 2 * L * L + 2 := by
    calc
      4 + (2 * L * L - 2) = (2 + 2) + (2 * L * L - 2) := by rw [← four]
      _ = 2 + (2 + (2 * L * L - 2)) := by rw [Nat.add_assoc]
      _ = 2 + 2 * L * L := by rw [bridge]
      _ = 2 * L * L + 2 := by rw [Nat.add_comm]
  exact Nat.sub_eq_of_eq_add key.symm

theorem quotient_at_L3 : (2 * 3 * 3 + 2) - (2 * 3 * 3 - 2) = 4 := by decide

def faceRows : List (List Bool) := [
  [true, true, false, true, false, false, true, false, false, false, false, false, false, false, false, false, false, false],
  [false, false, true, true, false, true, false, false, true, false, false, false, false, false, false, false, false, false],
  [false, true, false, false, true, true, false, false, false, false, true, false, false, false, false, false, false, false],
  [false, false, false, false, false, false, true, true, false, true, false, false, true, false, false, false, false, false],
  [false, false, false, false, false, false, false, false, true, true, false, true, false, false, true, false, false, false],
  [false, false, false, false, false, false, false, true, false, false, true, true, false, false, false, false, true, false],
  [true, false, false, false, false, false, false, false, false, false, false, false, true, true, false, true, false, false],
  [false, false, true, false, false, false, false, false, false, false, false, false, false, false, true, true, false, true],
  [false, false, false, false, true, false, false, false, false, false, false, false, false, true, false, false, true, true]
]
def starRows : List (List Bool) := [
  [true, true, false, false, true, false, false, false, false, false, false, false, false, true, false, false, false, false],
  [true, false, true, true, false, false, false, false, false, false, false, false, false, false, false, true, false, false],
  [false, false, true, false, true, true, false, false, false, false, false, false, false, false, false, false, false, true],
  [false, true, false, false, false, false, true, true, false, false, true, false, false, false, false, false, false, false],
  [false, false, false, true, false, false, true, false, true, true, false, false, false, false, false, false, false, false],
  [false, false, false, false, false, true, false, false, true, false, true, true, false, false, false, false, false, false],
  [false, false, false, false, false, false, false, true, false, false, false, false, true, true, false, false, true, false],
  [false, false, false, false, false, false, false, false, false, true, false, false, true, false, true, true, false, false],
  [false, false, false, false, false, false, false, false, false, false, false, true, false, false, true, false, true, true]
]
def logicalZ1 : List Bool := [true, false, false, false, false, false, true, false, false, false, false, false, true, false, false, false, false, false]
def rowZeroHorizontalMask : List Bool := [true, false, true, false, true, false, false, false, false, false, false, false, false, false, false, false, false, false]

theorem face_rank : matrixRank faceRows = 8 := by decide

theorem star_rank : matrixRank starRows = 8 := by decide

theorem logical_z1_in_face_kernel :
    mulVec faceRows logicalZ1 = List.replicate 9 false := by decide

theorem logical_z1_not_in_star_span :
    matrixRank (logicalZ1 :: starRows) = matrixRank starRows + 1 := by decide

theorem logical_z1_weight : weight logicalZ1 = 3 := by decide

theorem row_flux_of_logical : dot rowZeroHorizontalMask logicalZ1 = true := by decide

theorem stars_have_zero_row_flux :
    mulVec starRows rowZeroHorizontalMask = List.replicate 9 false := by decide

end WitnessedDifference.ToricSyndromeCorrespondence

#print axioms WitnessedDifference.ToricSyndromeCorrespondence.commutation_quotient_dimension
#print axioms WitnessedDifference.ToricSyndromeCorrespondence.quotient_at_L3
#print axioms WitnessedDifference.ToricSyndromeCorrespondence.face_rank
#print axioms WitnessedDifference.ToricSyndromeCorrespondence.star_rank
#print axioms WitnessedDifference.ToricSyndromeCorrespondence.logical_z1_in_face_kernel
#print axioms WitnessedDifference.ToricSyndromeCorrespondence.logical_z1_not_in_star_span
#print axioms WitnessedDifference.ToricSyndromeCorrespondence.logical_z1_weight
#print axioms WitnessedDifference.ToricSyndromeCorrespondence.row_flux_of_logical
#print axioms WitnessedDifference.ToricSyndromeCorrespondence.stars_have_zero_row_flux
