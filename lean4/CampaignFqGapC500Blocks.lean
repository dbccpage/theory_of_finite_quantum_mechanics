/-
Narrowed census for FQ-GAP-C500-ORIGINAL-TARGETS.
The ten clause lists are a transcription of gap_register.yaml.
This module does not read that file.
-/

def c500ClauseRows : List (String × List String) := [
  ("GAP-C500-B01", []),
  ("GAP-C500-B02", ["M2", "M5"]),
  ("GAP-C500-B03", ["M1", "M3", "M5", "J2"]),
  ("GAP-C500-B04", ["M3", "M5"]),
  ("GAP-C500-B05", ["M2", "M5", "M6", "J2"]),
  ("GAP-C500-B06", ["M5"]),
  ("GAP-C500-B07", ["M6"]),
  ("GAP-C500-B08", ["M6"]),
  ("GAP-C500-B09", ["M6"]),
  ("GAP-C500-B10", ["M2", "M5", "M7", "J1", "J2"])
]

def c500ClauseSum : Nat := (c500ClauseRows.map fun p => p.snd.length).foldl (· + ·) 0

def isingPoly (n : Int) : Int := n ^ 4 - 6 * n ^ 2 + 5

theorem c500_block_count : c500ClauseRows.length = 10 := rfl

theorem c500_clause_sum : c500ClauseSum = 21 := rfl

theorem c500_block01_clauses :
    c500ClauseRows.get ⟨0, by decide⟩ = ("GAP-C500-B01", []) := by
  decide

theorem c500_block10_clauses :
    c500ClauseRows.get ⟨9, by decide⟩ = ("GAP-C500-B10", ["M2", "M5", "M7", "J1", "J2"]) := by
  decide

theorem c500_block10_length :
    (c500ClauseRows.get ⟨9, by decide⟩).snd.length = 5 := by
  decide

theorem c500_target_product : 25 * 10 = 250 := rfl

theorem c500_target_last : 301 + 250 - 1 = 550 := rfl

theorem ising_poly_one : isingPoly 1 = 0 := by
  decide

theorem ising_poly_neg_one : isingPoly (-1) = 0 := by
  decide

theorem ising_poly_on_square_five : (5 : Int) * 5 - 6 * 5 + 5 = 0 := by
  decide

#print axioms c500_block_count
#print axioms c500_clause_sum
#print axioms c500_block01_clauses
#print axioms c500_block10_clauses
#print axioms c500_block10_length
#print axioms c500_target_product
#print axioms c500_target_last
#print axioms ising_poly_one
#print axioms ising_poly_neg_one
#print axioms ising_poly_on_square_five
