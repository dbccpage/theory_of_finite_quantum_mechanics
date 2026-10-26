-- Campaign: FSP-THETA-TERM-COMPLEX-WEIGHT. Not a default target.
-- Four quarter-turn indices and charges 0 and 1.
-- No exponential, no real angle, and no plaquette sum.

namespace CampaignFspThetaTermComplexWeight

def mulNegI (p : Int × Int) : Int × Int :=
  (p.2, -p.1)

def gMul (a b c d : Int) : Int × Int :=
  (a * c - b * d, a * d + b * c)

def quarter : Nat → Int × Int
  | 0 => (1, 0)
  | n + 1 => mulNegI (quarter n)

def weight (k q : Nat) : Int × Int :=
  if q = 0 then (1, 0) else if q = 1 then quarter k else (0, 0)

theorem quarter0 : quarter 0 = (1, 0) := rfl
theorem quarter1 : quarter 1 = (0, -1) := rfl
theorem quarter2 : quarter 2 = (-1, 0) := rfl
theorem quarter3 : quarter 3 = (0, 1) := rfl
theorem quarter4 : quarter 4 = (1, 0) := rfl

theorem mulNegI_eq_gMul (a b : Int) : mulNegI (a, b) = gMul a b 0 (-1) := by
  unfold mulNegI gMul
  apply Prod.ext <;> omega

theorem phaseProduct : gMul 1 0 0 (-1) = (0, -1) := rfl

theorem weight00 : weight 0 0 = (1, 0) := rfl
theorem weight10 : weight 1 0 = (1, 0) := rfl
theorem weight20 : weight 2 0 = (1, 0) := rfl
theorem weight30 : weight 3 0 = (1, 0) := rfl

theorem weight01 : weight 0 1 = (1, 0) := rfl
theorem weight11 : weight 1 1 = (0, -1) := rfl
theorem weight21 : weight 2 1 = (-1, 0) := rfl
theorem weight31 : weight 3 1 = (0, 1) := rfl

theorem im01 : (weight 0 1).2 = 0 := rfl
theorem im11 : (weight 1 1).2 = -1 := rfl
theorem im21 : (weight 2 1).2 = 0 := rfl
theorem im31 : (weight 3 1).2 = 1 := rfl

theorem im11_ne : (weight 1 1).2 ≠ 0 := by decide
theorem im31_ne : (weight 3 1).2 ≠ 0 := by decide

theorem re21 : (weight 2 1).1 = -1 := rfl

theorem notPositive21 : ¬ (weight 2 1).1 > 0 := by decide

theorem positive01 : (weight 0 1).1 > 0 ∧ (weight 0 1).2 = 0 := by decide

theorem charge1PositiveOnlyAtZero :
    ((weight 0 1).1 > 0 ∧ (weight 0 1).2 = 0) ∧
      ¬ ((weight 1 1).1 > 0 ∧ (weight 1 1).2 = 0) ∧
      ¬ ((weight 2 1).1 > 0 ∧ (weight 2 1).2 = 0) ∧
      ¬ ((weight 3 1).1 > 0 ∧ (weight 3 1).2 = 0) := by
  decide

#print axioms quarter0
#print axioms quarter1
#print axioms quarter2
#print axioms quarter3
#print axioms quarter4
#print axioms mulNegI_eq_gMul
#print axioms phaseProduct
#print axioms weight00
#print axioms weight10
#print axioms weight20
#print axioms weight30
#print axioms weight01
#print axioms weight11
#print axioms weight21
#print axioms weight31
#print axioms im01
#print axioms im11
#print axioms im21
#print axioms im31
#print axioms im11_ne
#print axioms im31_ne
#print axioms re21
#print axioms notPositive21
#print axioms positive01
#print axioms charge1PositiveOnlyAtZero

end CampaignFspThetaTermComplexWeight
