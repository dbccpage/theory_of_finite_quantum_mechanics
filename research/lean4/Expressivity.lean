








namespace OmegaCosmology.SymbolGame

def expressivityNorm (h : List Int) : Nat :=
  h.foldr (fun x acc => x.natAbs + acc) 0

theorem expressivityNorm_nil : expressivityNorm [] = 0 := rfl

theorem expressivityNorm_cons (x : Int) (xs : List Int) :
    expressivityNorm (x :: xs) = x.natAbs + expressivityNorm xs := rfl

theorem expressivityNorm_nonneg (h : List Int) : 0 ≤ expressivityNorm h := by
  exact Nat.zero_le _

theorem expressivityNorm_append (h1 h2 : List Int) :
    expressivityNorm (h1 ++ h2) = expressivityNorm h1 + expressivityNorm h2 := by
  induction h1 with
  | nil =>
    rw [List.nil_append, expressivityNorm_nil, Nat.zero_add]
  | cons x xs ih =>
    rw [List.cons_append, expressivityNorm_cons, ih, expressivityNorm_cons, Nat.add_assoc]

theorem expressivityNorm_neg (h : List Int) :
    expressivityNorm (h.map Neg.neg) = expressivityNorm h := by
  induction h with
  | nil => rfl
  | cons x xs ih =>
    rw [List.map_cons, expressivityNorm_cons, expressivityNorm_cons, Int.natAbs_neg, ih]

theorem nonconstant_shift_changes_norm :
    expressivityNorm [1, -1] = 2 ∧
      expressivityNorm [2, -1] = 3 ∧
      expressivityNorm [1, -1] ≠ expressivityNorm [2, -1] := by
  decide

end OmegaCosmology.SymbolGame

private def l5aProvenance : String :=
  "Origin: lean4/Expressivity.lean Claim: expressivityNorm_nil AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
