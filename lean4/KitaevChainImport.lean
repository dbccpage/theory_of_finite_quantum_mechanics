-- MAJ-IMPORT-KITAEV-CHAIN. Not a default target.
-- Integer reading of sweet-spot index labels and two comparisons of mu * mu with (2 * t) * (2 * t).
-- The fermion Hamiltonian, the BdG spectrum, and a physical wire stay outside this module.

namespace KitaevChainImport

theorem edgeAbsent (L j : Nat) (hL : 2 ≤ L) (hj : 1 ≤ j) (hjU : j ≤ L - 1) :
    2 * j ≠ 1 ∧ 2 * j ≠ 2 * L ∧ 2 * j + 1 ≠ 1 ∧ 2 * j + 1 ≠ 2 * L := by
  omega

theorem edgeWitness :
    (2 : Nat) * 1 = 2 ∧ (2 : Nat) * 1 + 1 = 3 ∧ (2 : Nat) * 2 = 4 ∧
      2 ≠ 1 ∧ 2 ≠ 4 ∧ 3 ≠ 1 ∧ 3 ≠ 4 := by
  decide

theorem insidePoint :
    (1 : Int) * 1 < (2 * 1) * (2 * 1) ∧ (1 : Int) ≠ 0 := by
  decide

theorem outsidePoint :
    ¬ ((3 : Int) * 3 < (2 * 1) * (2 * 1)) ∧ (1 : Int) ≠ 0 := by
  decide

#print axioms edgeAbsent
#print axioms edgeWitness
#print axioms insidePoint
#print axioms outsidePoint

end KitaevChainImport
