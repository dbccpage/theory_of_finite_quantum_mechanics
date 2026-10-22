/-!
# The [[5,1,3]] code and its 6-leg perfect Choi tensor (ADS-FIVE-QUBIT-PERFECT-TENSOR-TARGET)

AuthorityEffect: None.
Scope: Symplectic `GF(2)` arithmetic on the 5-qubit Laflamme-Miquel-Paz-Zurek `[[5,1,3]]` stabilizer
code (`XZZXI, IXZZX, XIXZZ, ZXIXZ` with logicals `XXXXX, ZZZZZ`) and its 6-qubit Choi stabilizer
state (`g_i ⊗ I` for `i=1..4`, `XXXXX ⊗ X`, `ZZZZZ ⊗ Z`).
Proves:
1. All 6 Choi generators pairwise commute and generate a 64-element stabilizer group.
2. The weight distribution of the 64-element Choi stabilizer group is exactly
   `1` element of weight `0`, `45` elements of weight `4`, and `18` elements of weight `6`
   (the hexacode weight enumerator `1 + 45 z^4 + 18 z^6`); every non-identity stabilizer element
   has weight at least `4`.
3. For all twenty `3|3` bipartitions `A ⊂ {0..5}` (`|A| = 3`), the subgroup of Choi stabilizers
   supported inside `A` is trivial (order 1, `GF(2)` restriction rank 6), so every `3|3` bipartition
   has entanglement entropy `3` bits (maximal entanglement across every cut).
4. In the 5-qubit `[[5,1,3]]` code, the centralizer (normalizer) of the 16-element stabilizer group
   inside the 1024-element 5-qubit Pauli group has order `64`, and the `48` nontrivial logical
   operators have minimum weight `3`.
-/

namespace FrontierFiveQubitPerfectTensor

/-- Symplectic bitmask representation of an `n`-qubit Pauli operator (modulo phase):
`xMask` records `X/Y` support bits and `zMask` records `Z/Y` support bits. -/
structure PauliMask where
  xMask : Nat
  zMask : Nat
  deriving DecidableEq, Repr

def mulPauli (p q : PauliMask) : PauliMask :=
  ⟨p.xMask ^^^ q.xMask, p.zMask ^^^ q.zMask⟩

/-- Number of set bits in a bitmask of width at most `n`. -/
def popCount (n mask : Nat) : Nat :=
  ((List.range n).filter fun i => ((mask >>> i) &&& 1) == 1).length

/-- Two Pauli operators commute iff their symplectic inner product mod 2 vanishes. -/
def commutes (n : Nat) (p q : PauliMask) : Bool :=
  (popCount n ((p.xMask &&& q.zMask) ^^^ (p.zMask &&& q.xMask))) % 2 == 0

/-- Hamming weight (number of non-identity tensor factors) of an `n`-qubit Pauli operator. -/
def pauliWeight (n : Nat) (p : PauliMask) : Nat :=
  popCount n (p.xMask ||| p.zMask)

/-- The 4 stabilizer generators of the `[[5,1,3]]` code:
`g1 = XZZXI`, `g2 = IXZZX`, `g3 = XIXZZ`, `g4 = ZXIXZ`. -/
def g1_5 : PauliMask := ⟨0b01001, 0b00110⟩
def g2_5 : PauliMask := ⟨0b10010, 0b01100⟩
def g3_5 : PauliMask := ⟨0b00101, 0b11000⟩
def g4_5 : PauliMask := ⟨0b01010, 0b10001⟩

def fiveQubitGens : List PauliMask := [g1_5, g2_5, g3_5, g4_5]

/-- Logical operators `X_L = XXXXX` and `Z_L = ZZZZZ` on 5 qubits. -/
def xL_5 : PauliMask := ⟨0b11111, 0b00000⟩
def zL_5 : PauliMask := ⟨0b00000, 0b11111⟩

/-- The 6 generators of the 6-qubit Choi state:
`g1 ⊗ I`, `g2 ⊗ I`, `g3 ⊗ I`, `g4 ⊗ I`, `XXXXX ⊗ X`, `ZZZZZ ⊗ Z`. -/
def choiGens : List PauliMask :=
  [g1_5, g2_5, g3_5, g4_5, ⟨0b111111, 0b000000⟩, ⟨0b000000, 0b111111⟩]

/-- Combine generators by a `GF(2)` coefficient bitmask `c`. -/
def spanElement (gens : List PauliMask) (c : Nat) : PauliMask :=
  (List.range gens.length).foldl
    (fun acc i => if ((c >>> i) &&& 1) == 1 then mulPauli acc (gens.getD i ⟨0, 0⟩) else acc)
    ⟨0, 0⟩

/-- The 64 elements of the 6-qubit Choi stabilizer group. -/
def choiGroup : List PauliMask :=
  (List.range 64).map (spanElement choiGens)

theorem choi_generators_commute_and_group_order_64 :
    (choiGens.all fun p => choiGens.all fun q => commutes 6 p q) = true ∧
    choiGroup.Nodup = true ∧
    choiGroup.length = 64 := by
  decide

/-- Weight enumerator of the 64-element Choi stabilizer group:
`1` element of weight `0`, `45` of weight `4`, `18` of weight `6`, and `0` of weights `1, 2, 3, 5`. -/
def countChoiWeight (w : Nat) : Nat :=
  (choiGroup.filter fun p => pauliWeight 6 p == w).length

theorem choi_perfect_tensor_weight_distribution :
    countChoiWeight 0 = 1 ∧
    countChoiWeight 1 = 0 ∧
    countChoiWeight 2 = 0 ∧
    countChoiWeight 3 = 0 ∧
    countChoiWeight 4 = 45 ∧
    countChoiWeight 5 = 0 ∧
    countChoiWeight 6 = 18 ∧
    ((choiGroup.drop 1).all fun p => decide (4 ≤ pauliWeight 6 p)) = true := by
  decide

/-- All twenty `3|3` bipartitions `A ⊂ {0..5}` (`popCount 6 maskA == 3`) have trivial stabilizer
subgroup supported inside `A` (`xMask &&& complement == 0` and `zMask &&& complement == 0`),
giving entanglement entropy `3 - 0 = 3` bits across every `3|3` cut. -/
def bipartitions3of6 : List Nat :=
  (List.range 64).filter fun m => popCount 6 m == 3

def supportedInMask (maskA : Nat) (p : PauliMask) : Bool :=
  let comp := 0b111111 ^^^ maskA
  ((p.xMask &&& comp) == 0) && ((p.zMask &&& comp) == 0)

def localStabilizerCount (maskA : Nat) : Nat :=
  (choiGroup.filter (supportedInMask maskA)).length

theorem all_twenty_3_3_bipartitions_maximal_entropy :
    bipartitions3of6.length = 20 ∧
    (bipartitions3of6.all fun maskA => localStabilizerCount maskA == 1) = true := by
  decide

/-- The 16-element stabilizer group of the 5-qubit `[[5,1,3]]` code and its 64-element normalizer
(centralizer) inside the 1024-element 5-qubit Pauli group: the 48 nontrivial logical operators
have minimum weight 3. -/
def fiveQubitStabilizer : List PauliMask :=
  (List.range 16).map (spanElement fiveQubitGens)

def allFiveQubitPaulis : List PauliMask :=
  (List.range 1024).map fun k => ⟨k &&& 0b11111, (k >>> 5) &&& 0b11111⟩

def isNormalizer5 (p : PauliMask) : Bool :=
  fiveQubitGens.all fun g => commutes 5 p g

def nontrivialLogicals5 : List PauliMask :=
  allFiveQubitPaulis.filter fun p => isNormalizer5 p && !(fiveQubitStabilizer.contains p)

set_option maxRecDepth 20000 in
set_option maxHeartbeats 800000 in
theorem five_qubit_logical_minimum_weight_3 :
    (allFiveQubitPaulis.filter isNormalizer5).length = 64 ∧
    nontrivialLogicals5.length = 48 ∧
    (nontrivialLogicals5.all fun p => decide (3 ≤ pauliWeight 5 p)) = true ∧
    (nontrivialLogicals5.any fun p => pauliWeight 5 p == 3) = true := by
  decide

end FrontierFiveQubitPerfectTensor

#print axioms FrontierFiveQubitPerfectTensor.choi_generators_commute_and_group_order_64
#print axioms FrontierFiveQubitPerfectTensor.choi_perfect_tensor_weight_distribution
#print axioms FrontierFiveQubitPerfectTensor.all_twenty_3_3_bipartitions_maximal_entropy
#print axioms FrontierFiveQubitPerfectTensor.five_qubit_logical_minimum_weight_3

private def l5aProvenance : String :=
  "Origin: lean4/FrontierFiveQubitPerfectTensor.lean Claim: choi_perfect_tensor_weight_distribution AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
