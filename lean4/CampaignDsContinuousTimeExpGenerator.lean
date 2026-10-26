-- Campaign: DS-CONTINUOUS-TIME-EXP-GENERATOR. Not a default target.
-- Boolean toggle, two scale-4 matrices, a Cayley polynomial, odd branch energies,
-- and one absent nilpotent integer logarithm of the swap.
-- Continuous time, exp, log, and a path-integral measure stay outside this module.

namespace CampaignDsContinuousTimeExpGenerator

def toggle (q : Bool) : Bool := !q

theorem toggleImages : toggle false = true ∧ toggle true = false := ⟨rfl, rfl⟩

theorem noToggleSquare :
    ¬ ∃ σ : Bool → Bool, ∀ q : Bool, σ (σ q) = toggle q := by
  intro h
  rcases h with ⟨σ, hσ⟩
  cases hff : σ false with
  | false =>
      have h1 := hσ false
      rw [hff, hff] at h1
      cases h1
  | true =>
      cases hft : σ true with
      | false =>
          have h1 := hσ false
          rw [hff, hft] at h1
          cases h1
      | true =>
          have h1 := hσ true
          rw [hft, hft] at h1
          cases h1

abbrev G := Int × Int

def gAdd (x y : G) : G := (x.1 + y.1, x.2 + y.2)

def gMul (x y : G) : G := (x.1 * y.1 - x.2 * y.2, x.1 * y.2 + x.2 * y.1)

theorem gAddCoords (a b c d : Int) : gAdd (a, b) (c, d) = (a + c, b + d) := rfl

theorem gMulCoords (a b c d : Int) : gMul (a, b) (c, d) = (a * c - b * d, a * d + b * c) := rfl

structure Mat where
  m00 : G
  m01 : G
  m10 : G
  m11 : G
  deriving DecidableEq

def mmul (A B : Mat) : Mat where
  m00 := gAdd (gMul A.m00 B.m00) (gMul A.m01 B.m10)
  m01 := gAdd (gMul A.m00 B.m01) (gMul A.m01 B.m11)
  m10 := gAdd (gMul A.m10 B.m00) (gMul A.m11 B.m10)
  m11 := gAdd (gMul A.m10 B.m01) (gMul A.m11 B.m11)

def scaled : Mat where
  m00 := (1, 1)
  m01 := (1, -1)
  m10 := (1, -1)
  m11 := (1, 1)

def scaledNeg : Mat where
  m00 := (-1, -1)
  m01 := (-1, 1)
  m10 := (-1, 1)
  m11 := (-1, -1)

def fourX : Mat where
  m00 := (0, 0)
  m01 := (4, 0)
  m10 := (4, 0)
  m11 := (0, 0)

theorem scaledSquare : mmul scaled scaled = fourX := by
  decide

theorem negSquare : mmul scaledNeg scaledNeg = fourX := by
  decide

theorem scaledDiffer : scaled ≠ scaledNeg := by
  decide

theorem cayleyNorm (t : Int) :
    (1 - t * t) * (1 - t * t) + 4 * (t * t) = (1 + t * t) * (1 + t * t) := by
  have hL : (1 - t * t) * (1 - t * t) + 4 * (t * t) =
      1 - 2 * (t * t) + (t * t) * (t * t) + 4 * (t * t) := by
    repeat rw [Int.sub_mul]
    repeat rw [Int.mul_sub]
    repeat rw [Int.one_mul]
    repeat rw [Int.mul_one]
    omega
  have hR : (1 + t * t) * (1 + t * t) =
      1 + 2 * (t * t) + (t * t) * (t * t) := by
    repeat rw [Int.add_mul]
    repeat rw [Int.mul_add]
    repeat rw [Int.one_mul]
    repeat rw [Int.mul_one]
    omega
  rw [hL, hR]
  omega

def energy (k : Int) : Int := 2 * k + 1

theorem energyZero : energy 0 = 1 := by
  decide

theorem energyOne : energy 1 = 3 := by
  decide

theorem energyDistinct (k1 k2 : Int) (h : k1 ≠ k2) : energy k1 ≠ energy k2 := by
  dsimp [energy]
  omega

theorem candidateCorner : (-1) * (-1) + 1 * 1 = 2 := by
  decide

theorem noNilpotentIntegerLog :
    ¬ ∃ a b c d : Int,
        a + 1 = 0 ∧ b = 1 ∧ c = 1 ∧ d + 1 = 0 ∧
          a * a + b * c = 0 ∧ a * b + b * d = 0 ∧
          c * a + d * c = 0 ∧ c * b + d * d = 0 := by
  intro h
  rcases h with ⟨a, b, c, d, ha, hb, hc, hd, h00, h01, h10, h11⟩
  have ha' : a = -1 := by omega
  rw [ha', hb, hc] at h00
  have h2 : (-1 : Int) * -1 + 1 * 1 = 2 := by decide
  rw [h2] at h00
  omega

#print axioms toggleImages
#print axioms noToggleSquare
#print axioms gAddCoords
#print axioms gMulCoords
#print axioms scaledSquare
#print axioms negSquare
#print axioms scaledDiffer
#print axioms cayleyNorm
#print axioms energyZero
#print axioms energyOne
#print axioms energyDistinct
#print axioms candidateCorner
#print axioms noNilpotentIntegerLog

end CampaignDsContinuousTimeExpGenerator
