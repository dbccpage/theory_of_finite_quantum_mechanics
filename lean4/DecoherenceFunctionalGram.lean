-- DS-QM043-DECOHERENCE-FUNCTIONAL-IMPORT. Not a default target.
-- Integer Gram square, determinant 0, and two cleared witnesses: (1, 1) over 2 and (3, 4) over 5.
-- The trace formula and a transport bridge stay outside this module.

namespace DecoherenceFunctionalGram

theorem negMulNeg (m : Int) : (-m) * (-m) = m * m := by
  calc
    (-m) * (-m) = -(m * -m) := by rw [Int.neg_mul]
    _ = -(-(m * m)) := by rw [Int.mul_neg]
    _ = m * m := by rw [Int.neg_neg]

theorem squareNonneg (n : Int) : 0 ≤ n * n := by
  have h : n * n = ↑(n.natAbs * n.natAbs) := by
    cases n with
    | ofNat k =>
        simp [Int.natAbs]
    | negSucc k =>
        simp only [Int.natAbs, Int.negSucc_eq]
        rw [negMulNeg ((k : Int) + 1)]
        simp
  rw [h]
  exact Int.natCast_nonneg (n.natAbs * n.natAbs)

theorem gramValueNonneg (a b x y : Int) :
    0 ≤ (a * x + b * y) * (a * x + b * y) :=
  squareNonneg (a * x + b * y)

theorem diagNonneg (a : Int) : 0 ≤ a * a :=
  squareNonneg a

theorem gramProd (a b : Int) : (a * b) * (a * b) = a * a * (b * b) := by
  calc
    (a * b) * (a * b) = a * (b * (a * b)) := by rw [Int.mul_assoc]
    _ = a * ((b * a) * b) := by rw [← Int.mul_assoc b a b]
    _ = a * ((a * b) * b) := by rw [Int.mul_comm b a]
    _ = a * (a * (b * b)) := by rw [Int.mul_assoc a b b]
    _ = (a * a) * (b * b) := by rw [← Int.mul_assoc a a (b * b)]

theorem gramDet (a b : Int) : a * a * (b * b) - (a * b) * (a * b) = 0 := by
  rw [gramProd]
  omega

theorem traceSquaresNonneg (a b : Int) : 0 ≤ a * a + b * b := by
  have ha := diagNonneg a
  have hb := diagNonneg b
  omega

theorem halfClass : (1 : Int) + 1 = 2 * 1 := by decide

theorem halfSquares : (1 : Int) * 1 + 1 * 1 = 2 := by decide

theorem halfDenom : (2 : Int) * 2 = 4 := by decide

theorem halfSeparates : (2 : Int) ≠ 4 := by decide

theorem halfGlobal : ((1 : Int) + 1) * (1 + 1) = 4 := by decide

theorem halfGlobalOne : (4 : Int) = 4 * 1 := by decide

theorem krausSquares : (3 : Int) * 3 + 4 * 4 = 25 := by decide

theorem fiveSquare : (5 : Int) * 5 = 25 := by decide

theorem krausHolds : (3 : Int) * 3 + 4 * 4 = 5 * 5 := by decide

theorem classSum : (3 : Int) + 4 = 7 := by decide

theorem sevenSquare : (7 : Int) * 7 = 49 := by decide

theorem classSeparates : (49 : Int) ≠ 25 := by decide

theorem gramAtOnes :
    (1 * 1 + 1 * 1) * (1 * 1 + 1 * 1) = 4 ∧
      1 * 1 * 1 * 1 + 2 * 1 * 1 * 1 * 1 + 1 * 1 * 1 * 1 = 4 := by
  decide

#print axioms negMulNeg
#print axioms squareNonneg
#print axioms gramValueNonneg
#print axioms diagNonneg
#print axioms gramProd
#print axioms gramDet
#print axioms traceSquaresNonneg
#print axioms halfClass
#print axioms halfSquares
#print axioms halfDenom
#print axioms halfSeparates
#print axioms halfGlobal
#print axioms halfGlobalOne
#print axioms krausSquares
#print axioms fiveSquare
#print axioms krausHolds
#print axioms classSum
#print axioms sevenSquare
#print axioms classSeparates
#print axioms gramAtOnes

end DecoherenceFunctionalGram
