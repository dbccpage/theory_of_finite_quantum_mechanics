/-
Node MAJ-IMPORT-COSET-WEIGHT-NP-HARD.
AuthorityEffect: None.

Finite case: the 2 by 4 parity-check matrix over the two-element field with rows
(1, 1, 0, 0) and (0, 1, 1, 1). Labels 0 through 15 use the least significant bit
as coordinate 0. Syndrome (1, 0) is row1 = 1 and row2 = 0. This module does not
formalize a reduction and does not treat a general binary matrix.
-/

def bit (n i : Nat) : Nat := n / (2 ^ i) % 2

def row1 (n : Nat) : Nat := (bit n 0 + bit n 1) % 2

def row2 (n : Nat) : Nat := (bit n 1 + bit n 2 + bit n 3) % 2

def dot4 (a b c d n : Nat) : Nat :=
  (a * bit n 0 + b * bit n 1 + c * bit n 2 + d * bit n 3) % 2

def inCoset (n : Nat) : Bool := row1 n == 1 && row2 n == 0

def inKernel (n : Nat) : Bool := row1 n == 0 && row2 n == 0

def wt (n : Nat) : Nat := bit n 0 + bit n 1 + bit n 2 + bit n 3

def weight1 (n : Nat) : Bool := wt n == 1

def coset : List Nat := (List.range 16).filter inCoset

def kernel : List Nat := (List.range 16).filter inKernel

theorem length_sixteen : (List.range 16).length = 16 := by decide

theorem row1_matches :
    (List.range 16).all (fun n => row1 n == dot4 1 1 0 0 n) = true := by decide

theorem row2_matches :
    (List.range 16).all (fun n => row2 n == dot4 0 1 1 1 n) = true := by decide

theorem coset_is : coset = [1, 6, 10, 13] := by decide

theorem coset_weights : coset.map wt = [1, 2, 2, 3] := by decide

theorem min_weight_one : coset.foldl Nat.min 4 = 1 := by decide

theorem weight_one_labels : coset.filter weight1 = [1] := by decide

theorem label_one_coordinates :
    bit 1 0 = 1 ∧ bit 1 1 = 0 ∧ bit 1 2 = 0 ∧ bit 1 3 = 0 := by decide

theorem kernel_is : kernel = [0, 7, 11, 12] := by decide

#print axioms length_sixteen
#print axioms row1_matches
#print axioms row2_matches
#print axioms coset_is
#print axioms coset_weights
#print axioms min_weight_one
#print axioms weight_one_labels
#print axioms label_one_coordinates
#print axioms kernel_is
