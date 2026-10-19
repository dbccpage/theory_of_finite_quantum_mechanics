import Mathlib.Data.List.Basic

/-! AuthorityEffect: None. Literal boundary-presence precedence and independent
endpoint/coherence membership diagnostics. No 2-category functor, invertibility,
pentagon or triangle theorem. Raw lookup/formatting refinement remains reviewed. -/
namespace TFQM.HigherFunctorInventory

def boundary (image source target actual wrongSource wrongTarget : Bool) : List Nat :=
  if !image then [0] else if !source then [1] else if !target then [2]
  else if !actual then [3]
  else (if wrongSource then [4] else []) ++ (if wrongTarget then [5] else [])

theorem image_missing (s t a ws wt : Bool) : boundary false s t a ws wt = [0] := rfl
theorem source_missing (t a ws wt : Bool) : boundary true false t a ws wt = [1] := rfl
theorem target_missing (a ws wt : Bool) : boundary true true false a ws wt = [2] := rfl
theorem actual_missing (ws wt : Bool) : boundary true true true false ws wt = [3] := rfl
theorem both_boundaries_wrong : boundary true true true true true true = [4,5] := rfl
theorem source_wrong : boundary true true true true true false = [4] := rfl
theorem target_wrong : boundary true true true true false true = [5] := rfl
theorem correct_boundaries : boundary true true true true false false = [] := rfl
theorem boundary_passes_iff (i s t a ws wt : Bool) :
    boundary i s t a ws wt = [] ↔
      i = true ∧ s = true ∧ t = true ∧ a = true ∧ ws = false ∧ wt = false := by
  cases i <;> cases s <;> cases t <;> cases a <;> cases ws <;> cases wt <;> simp [boundary]

def pairMissing (forward inverse : Bool) : List Nat :=
  (if forward then [] else [0]) ++ (if inverse then [] else [1])

theorem pair_absent : pairMissing false false = [0,1] := rfl
theorem forward_missing : pairMissing false true = [0] := rfl
theorem inverse_missing : pairMissing true false = [1] := rfl
theorem names_present : pairMissing true true = [] := rfl
theorem pair_passes_iff (f i : Bool) : pairMissing f i = [] ↔ f = true ∧ i = true := by
  cases f <;> cases i <;> simp [pairMissing]

def inventory (pairs : List (Bool × Bool)) : List (List Nat) :=
  pairs.map (fun p => pairMissing p.1 p.2)
theorem empty_inventory : inventory [] = [] := rfl
theorem inventory_append (first last : List (Bool × Bool)) :
    inventory (first ++ last) = inventory first ++ inventory last := by simp [inventory]

end TFQM.HigherFunctorInventory

#print axioms TFQM.HigherFunctorInventory.image_missing
#print axioms TFQM.HigherFunctorInventory.source_missing
#print axioms TFQM.HigherFunctorInventory.target_missing
#print axioms TFQM.HigherFunctorInventory.actual_missing
#print axioms TFQM.HigherFunctorInventory.both_boundaries_wrong
#print axioms TFQM.HigherFunctorInventory.source_wrong
#print axioms TFQM.HigherFunctorInventory.target_wrong
#print axioms TFQM.HigherFunctorInventory.correct_boundaries
#print axioms TFQM.HigherFunctorInventory.boundary_passes_iff
#print axioms TFQM.HigherFunctorInventory.pair_absent
#print axioms TFQM.HigherFunctorInventory.forward_missing
#print axioms TFQM.HigherFunctorInventory.inverse_missing
#print axioms TFQM.HigherFunctorInventory.names_present
#print axioms TFQM.HigherFunctorInventory.pair_passes_iff
#print axioms TFQM.HigherFunctorInventory.empty_inventory
#print axioms TFQM.HigherFunctorInventory.inventory_append
