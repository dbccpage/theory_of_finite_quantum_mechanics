-- Campaign: DS-CPTP-COMPLETE-POSITIVITY-IMPORT. Not a default target.
-- Nonnegative product t * (x + w) * (x + w), and the strict sign of t * (-2).
-- Complete positivity, Kraus, Choi and Stinespring stay outside this module.

namespace CampaignDsCptpCompletePositivity

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

theorem mulOfNat (k m : Nat) : Int.ofNat k * Int.ofNat m = Int.ofNat (k * m) := by
  simp

theorem mulNonneg (a b : Int) (ha : 0 ≤ a) (hb : 0 ≤ b) : 0 ≤ a * b := by
  cases a with
  | ofNat k =>
      cases b with
      | ofNat m =>
          rw [mulOfNat]
          exact Int.natCast_nonneg (k * m)
      | negSucc m =>
          simp [Int.negSucc_eq] at hb
          omega
  | negSucc k =>
      simp [Int.negSucc_eq] at ha
      omega

theorem bellNonneg (t x w : Int) (ht : 0 ≤ t) :
    0 ≤ t * ((x + w) * (x + w)) :=
  mulNonneg t ((x + w) * (x + w)) ht (squareNonneg (x + w))

theorem pairing : (1 : Int) * -1 + (-1) * 1 = -2 := by decide

theorem scaled (t : Int) : t * ((1 : Int) * -1 + (-1) * 1) = -2 * t := by
  rw [pairing]
  exact Int.mul_comm t (-2)

theorem scaleTwice (t : Int) : t * -2 = 2 * -t := by omega

theorem negOut (t : Int) (ht : 0 < t) : t * -2 < 0 := by omega

theorem negT (t : Int) (ht : 0 < t) : -t < 0 := by omega

theorem zeroScale : (0 : Int) * -2 = 0 := by decide

theorem normSq : (0 : Int) * 0 + 1 * 1 + (-1) * (-1) + 0 * 0 = 2 := by decide

#print axioms negMulNeg
#print axioms squareNonneg
#print axioms mulOfNat
#print axioms mulNonneg
#print axioms bellNonneg
#print axioms pairing
#print axioms scaled
#print axioms scaleTwice
#print axioms negOut
#print axioms negT
#print axioms zeroScale
#print axioms normSq

end CampaignDsCptpCompletePositivity
