/-
Narrowed census for FQ-GAP-CUSTODY-AND-RECEIPTS.
The fourteen type counts are a transcription of the claims list in
claim_ledger.yaml. This module does not read that file.
-/

def typeCensus : List (String × Nat) := [
  ("FINITE COMPUTATION", 160),
  ("SCOPE FENCE", 156),
  ("OPEN", 115),
  ("DEFINITION", 104),
  ("EXACT FINITE ALGEBRA", 80),
  ("CONDITIONAL", 57),
  ("UNTYPED", 48),
  ("ASSERTED", 36),
  ("REFUTED BY AUDIT", 31),
  ("DECLARED", 17),
  ("FINITE FIXTURE", 12),
  ("REFUTED BY COMPUTATION", 10),
  ("REFUSAL", 7),
  ("PARTIAL", 1)
]

def censusSum : Nat := (typeCensus.map Prod.snd).foldl (· + ·) 0

theorem census_length : typeCensus.length = 14 := rfl

theorem census_sum_eq : censusSum = 834 := rfl

theorem untyped_row : typeCensus.get ⟨6, by decide⟩ = ("UNTYPED", 48) := by
  decide

theorem one_untyped_label :
    (typeCensus.filter fun p => p.fst == "UNTYPED").length = 1 := by
  decide

theorem ledger_untyped_ne_gap_text : 48 ≠ 24 := by
  decide

theorem ledger_rows_ne_gap_text : 834 ≠ 189 := by
  decide

#print axioms census_length
#print axioms census_sum_eq
#print axioms untyped_row
#print axioms one_untyped_label
#print axioms ledger_untyped_ne_gap_text
#print axioms ledger_rows_ne_gap_text
