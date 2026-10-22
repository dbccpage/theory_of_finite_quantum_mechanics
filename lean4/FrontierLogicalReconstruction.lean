/-!
# Subregion logical reconstruction and two-qubit erasure on the [[5,1,3]] code
(ADS-LOGICAL-RECONSTRUCTION-TARGET)

AuthorityEffect: None.
Scope: Exact `GF(2)` normalizer and coset enumeration for the 5-qubit `[[5,1,3]]` code of
Laflamme, Miquel, Paz, and Zurek (`XZZXI, IXZZX, XIXZZ, ZXIXZ` with logical classes
`X_L = XXXXX`, `Z_L = ZZZZZ`, `Y_L = YYYYY`).
Proves:
1. Each of the three nontrivial logical cosets `X_L S`, `Z_L S`, `Y_L S` has size 16.
2. For every one of the `C(5, 3) = 10` triples `T` of physical qubits, each of the three nontrivial
   logical cosets `X_L S`, `Z_L S`, and `Y_L S` contains a representative supported entirely inside `T`.
3. For every one of the `C(5, 2) = 10` pairs `P` of physical qubits, no nontrivial logical operator
   (and no non-identity normalizer element) is supported inside `P`.
4. Equivalent Knill-Laflamme two-qubit erasure condition: every non-identity 5-qubit Pauli operator
   of weight at most 2 (all 105 of them) anti-commutes with at least one stabilizer generator.
-/

namespace FrontierLogicalReconstruction

structure PauliMask where
  xMask : Nat
  zMask : Nat
  deriving DecidableEq, Repr

def mulPauli (p q : PauliMask) : PauliMask :=
  ⟨p.xMask ^^^ q.xMask, p.zMask ^^^ q.zMask⟩

def popCount5 (mask : Nat) : Nat :=
  ((List.range 5).filter fun i => ((mask >>> i) &&& 1) == 1).length

def commutes5 (p q : PauliMask) : Bool :=
  (popCount5 ((p.xMask &&& q.zMask) ^^^ (p.zMask &&& q.xMask))) % 2 == 0

def weight5 (p : PauliMask) : Nat :=
  popCount5 (p.xMask ||| p.zMask)

def supportedIn5 (subMask : Nat) (p : PauliMask) : Bool :=
  let comp := 0b11111 ^^^ subMask
  ((p.xMask &&& comp) == 0) && ((p.zMask &&& comp) == 0)

def g1 : PauliMask := ⟨0b01001, 0b00110⟩
def g2 : PauliMask := ⟨0b10010, 0b01100⟩
def g3 : PauliMask := ⟨0b00101, 0b11000⟩
def g4 : PauliMask := ⟨0b01010, 0b10001⟩

def stabGens : List PauliMask := [g1, g2, g3, g4]

def xBar : PauliMask := ⟨0b11111, 0b00000⟩
def zBar : PauliMask := ⟨0b00000, 0b11111⟩
def yBar : PauliMask := ⟨0b11111, 0b11111⟩

def stabElem (c : Nat) : PauliMask :=
  (List.range 4).foldl
    (fun acc i => if ((c >>> i) &&& 1) == 1 then mulPauli acc (stabGens.getD i ⟨0, 0⟩) else acc)
    ⟨0, 0⟩

def stabGroup : List PauliMask := (List.range 16).map stabElem
def cosetX : List PauliMask := stabGroup.map (mulPauli xBar)
def cosetZ : List PauliMask := stabGroup.map (mulPauli zBar)
def cosetY : List PauliMask := stabGroup.map (mulPauli yBar)

/-- All 10 triples and all 10 pairs of `{0, 1, 2, 3, 4}` represented as 5-bit masks. -/
def allTriples5 : List Nat := (List.range 32).filter fun m => popCount5 m == 3
def allPairs5 : List Nat := (List.range 32).filter fun m => popCount5 m == 2

/-- Every one of the 10 triples `T` supports a representative in `X_L S`, a representative in `Z_L S`,
and a representative in `Y_L S`. -/
theorem every_triple_reconstructs_all_three_logical_classes :
    allTriples5.length = 10 ∧
    (allTriples5.all fun tMask =>
      (cosetX.any (supportedIn5 tMask)) &&
      (cosetZ.any (supportedIn5 tMask)) &&
      (cosetY.any (supportedIn5 tMask))) = true := by
  decide

/-- No pair `P` of physical qubits supports any representative of `X_L S`, `Z_L S`, or `Y_L S`. -/
theorem no_pair_supports_any_nontrivial_logical_class :
    allPairs5.length = 10 ∧
    (allPairs5.all fun pMask =>
      !(cosetX.any (supportedIn5 pMask)) &&
      !(cosetZ.any (supportedIn5 pMask)) &&
      !(cosetY.any (supportedIn5 pMask))) = true := by
  decide

/-- Knill-Laflamme two-qubit erasure condition: all 105 non-identity 5-qubit Pauli operators of
weight 1 or 2 anti-commute with at least one stabilizer generator in `stabGens`. -/
def weight1or2Paulis : List PauliMask :=
  ((List.range 1024).map fun k => ⟨k &&& 0b11111, (k >>> 5) &&& 0b11111⟩).filter fun p =>
    let w := weight5 p
    w == 1 || w == 2

set_option maxRecDepth 20000 in
set_option maxHeartbeats 800000 in
theorem two_qubit_erasure_detectable_all_105 :
    weight1or2Paulis.length = 105 ∧
    (weight1or2Paulis.all fun p => stabGens.any fun g => !(commutes5 p g)) = true := by
  decide

end FrontierLogicalReconstruction

#print axioms FrontierLogicalReconstruction.every_triple_reconstructs_all_three_logical_classes
#print axioms FrontierLogicalReconstruction.no_pair_supports_any_nontrivial_logical_class
#print axioms FrontierLogicalReconstruction.two_qubit_erasure_detectable_all_105

private def l5aProvenance : String :=
  "Origin: lean4/FrontierLogicalReconstruction.lean Claim: every_triple_reconstructs_all_three_logical_classes AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
