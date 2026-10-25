namespace CampaignTfq0319UnjoinedReceipt

/-- Two marks. The carrier in this file is the set of functions on these marks. -/
abbrev Mark := Fin 2

/-- Coboundary of a mark function, evaluated on an ordered pair. -/
def coboundary (f : Mark → Fin 2) (u v : Mark) : Fin 2 := f v - f u

def map00 : Mark → Fin 2
  | 0 => 0
  | 1 => 0

def map01 : Mark → Fin 2
  | 0 => 0
  | 1 => 1

def map10 : Mark → Fin 2
  | 0 => 1
  | 1 => 0

def map11 : Mark → Fin 2
  | 0 => 1
  | 1 => 1

def applyMap : Fin 4 → Mark → Fin 2
  | 0 => map00
  | 1 => map01
  | 2 => map10
  | 3 => map11

def image (i : Fin 4) : Fin 2 × Fin 2 := (applyMap i 0, applyMap i 1)

/-- Seven nibbles of the prefix named 3100c4e in TFQ-0319, plus a green bit.
The fields are data. They are not a function into the mark carrier. -/
structure Receipt where
  n0 : Fin 16
  n1 : Fin 16
  n2 : Fin 16
  n3 : Fin 16
  n4 : Fin 16
  n5 : Fin 16
  n6 : Fin 16
  green : Bool
deriving DecidableEq, Repr

def sealed : Receipt := ⟨3, 1, 0, 0, 12, 4, 14, true⟩

def sealedNibbles : List (Fin 16) := [3, 1, 0, 0, 12, 4, 14]

/-- A receipt paired with a map index. The index is a separate field. -/
structure Pairing where
  receipt : Receipt
  mapIndex : Fin 4
deriving DecidableEq, Repr

def pairing (i : Fin 4) : Pairing := ⟨sealed, i⟩

theorem sealed_nibble_count : sealedNibbles.length = 7 := by
  decide

theorem sealed_nibbles_match :
    sealed.n0 = 3 ∧ sealed.n1 = 1 ∧ sealed.n2 = 0 ∧ sealed.n3 = 0
      ∧ sealed.n4 = 12 ∧ sealed.n5 = 4 ∧ sealed.n6 = 14 ∧ sealed.green = true
      ∧ sealedNibbles = [sealed.n0, sealed.n1, sealed.n2, sealed.n3, sealed.n4, sealed.n5, sealed.n6] := by
  decide

theorem all_self_coboundaries_zero :
    coboundary map00 0 0 = 0 ∧ coboundary map00 1 1 = 0
      ∧ coboundary map01 0 0 = 0 ∧ coboundary map01 1 1 = 0
      ∧ coboundary map10 0 0 = 0 ∧ coboundary map10 1 1 = 0
      ∧ coboundary map11 0 0 = 0 ∧ coboundary map11 1 1 = 0 := by
  decide

theorem edge_coboundaries :
    coboundary map00 0 1 = 0 ∧ coboundary map01 0 1 = 1
      ∧ coboundary map10 0 1 = 1 ∧ coboundary map11 0 1 = 0 := by
  decide

theorem images_are_the_four :
    image 0 = (0, 0) ∧ image 1 = (0, 1) ∧ image 2 = (1, 0) ∧ image 3 = (1, 1) := by
  decide

theorem images_pairwise_distinct :
    image 0 ≠ image 1 ∧ image 0 ≠ image 2 ∧ image 0 ≠ image 3
      ∧ image 1 ≠ image 2 ∧ image 1 ≠ image 3 ∧ image 2 ≠ image 3 := by
  decide

theorem every_value_pair_is_listed :
    ∀ x y : Fin 2,
      (x = 0 ∧ y = 0) ∨ (x = 0 ∧ y = 1) ∨ (x = 1 ∧ y = 0) ∨ (x = 1 ∧ y = 1) := by
  decide

theorem pairing_keeps_sealed :
    ∀ i : Fin 4, (pairing i).receipt = sealed ∧ (pairing i).receipt.green = true := by
  decide

theorem pairing_indices :
    ∀ i : Fin 4, (pairing i).mapIndex = i := by
  decide

theorem pairing_distinct :
    pairing 0 ≠ pairing 1 ∧ pairing 0 ≠ pairing 2 ∧ pairing 0 ≠ pairing 3
      ∧ pairing 1 ≠ pairing 2 ∧ pairing 1 ≠ pairing 3 ∧ pairing 2 ≠ pairing 3 := by
  decide

/-- One green receipt, two map indices, two edge coboundaries. -/
theorem green_receipt_two_edge_values :
    (pairing 0).receipt = (pairing 1).receipt
      ∧ (pairing 0).receipt.green = true
      ∧ (pairing 1).receipt.green = true
      ∧ (pairing 0).mapIndex ≠ (pairing 1).mapIndex
      ∧ coboundary (applyMap (pairing 0).mapIndex) 0 1 = 0
      ∧ coboundary (applyMap (pairing 1).mapIndex) 0 1 = 1
      ∧ coboundary (applyMap (pairing 0).mapIndex) 0 1
          ≠ coboundary (applyMap (pairing 1).mapIndex) 0 1 := by
  decide

#print axioms sealed_nibble_count
#print axioms sealed_nibbles_match
#print axioms all_self_coboundaries_zero
#print axioms edge_coboundaries
#print axioms images_are_the_four
#print axioms images_pairwise_distinct
#print axioms every_value_pair_is_listed
#print axioms pairing_keeps_sealed
#print axioms pairing_indices
#print axioms pairing_distinct
#print axioms green_receipt_two_edge_values

end CampaignTfq0319UnjoinedReceipt
