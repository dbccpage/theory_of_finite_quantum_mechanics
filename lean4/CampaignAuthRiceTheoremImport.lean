-- Three codes on a two-point carrier.
-- Rice's theorem for a Turing-complete language is not stated here.

namespace CampaignAuthRiceTheoremImport

def beh (c : Fin 3) (i : Fin 2) : Fin 2 :=
  match c, i with
  | 0, 0 => 0
  | 0, 1 => 1
  | 1, 0 => 0
  | 1, 1 => 1
  | 2, 0 => 0
  | 2, 1 => 0

def idBit (c : Fin 3) : Bool :=
  (beh c 0 == 0) && (beh c 1 == 1)

def codeZero (c : Fin 3) : Bool :=
  c == 0

theorem beh00 : beh 0 0 = 0 := by decide

theorem beh01 : beh 0 1 = 1 := by decide

theorem beh10 : beh 1 0 = 0 := by decide

theorem beh11 : beh 1 1 = 1 := by decide

theorem beh20 : beh 2 0 = 0 := by decide

theorem beh21 : beh 2 1 = 0 := by decide

theorem id0 : idBit 0 = true := by decide

theorem id1 : idBit 1 = true := by decide

theorem id2 : idBit 2 = false := by decide

theorem z0 : codeZero 0 = true := by decide

theorem z1 : codeZero 1 = false := by decide

theorem z2 : codeZero 2 = false := by decide

#print axioms beh00
#print axioms beh01
#print axioms beh10
#print axioms beh11
#print axioms beh20
#print axioms beh21
#print axioms id0
#print axioms id1
#print axioms id2
#print axioms z0
#print axioms z1
#print axioms z2

end CampaignAuthRiceTheoremImport
