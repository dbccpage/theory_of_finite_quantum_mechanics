import Std

/-!
Definitional replay of the finite phase table used by mub6_tao_confluence.rs.
The theorem is about the enumerated phase exponents. It supplies no family
confluence, neighborhood cover, curvature bound, or exclusion of candidate bases.
AuthorityEffect: None.
-/

namespace MUB.KernelReflectionTaoConfluence

def phaseTable : Array (Array Int) := #[
  #[0,0,0,0,0,0], #[0,0,1,1,2,2], #[0,1,0,2,2,1],
  #[0,1,2,0,1,2], #[0,2,2,1,0,1], #[0,2,1,2,1,0]]

def crossRatioExponents : List Int :=
  (List.range 6).flatMap fun i =>
    ((List.range 6).filter (fun j => i < j)).flatMap fun j =>
      (List.range 6).flatMap fun k =>
        ((List.range 6).filter (fun l => k < l)).map fun l =>
          8 * ((phaseTable[i]![k]! + phaseTable[j]![l]!
            - phaseTable[i]![l]! - phaseTable[j]![k]!) % 3)

def checkPhaseReceipt : Bool :=
  crossRatioExponents.length == 225 &&
    crossRatioExponents.all (fun e => (3 * e) % 24 == 0 && e != 12)

set_option maxRecDepth 100000 in
theorem tao_phase_receipt_checked : checkPhaseReceipt = true := by rfl

#print axioms tao_phase_receipt_checked
end MUB.KernelReflectionTaoConfluence
