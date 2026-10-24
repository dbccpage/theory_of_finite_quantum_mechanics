import Mathlib.Tactic.Group
import Mathlib.Tactic.IntervalCases
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Zify
import Mathlib.GroupTheory.Perm.Fin

/-!
Finite QCD control for TFQ-0011.

The four-edge plaquette product is conjugated by the basepoint gauge in any group.
S3 supplies a non-commuting pair and a product that is not the identity.
The SU(3) Casimir channel formulae, the one- and two-loop rational beta coefficients,
and the Creutz ratios of area and perimeter monomials are exact rational identities.
The integers 9 and 12 satisfy 9 - 1 = 8, 12 - 9 + 1 = 4 and 12 - 8 = 4.
No complex is constructed, and no continuum confinement statement is made.
-/

namespace CampaignTfq0011FiniteQcd

theorem plaquette_gauge {G : Type*} [Group G] (g h k m a b c d : G) :
    (a⁻¹ * g * b) * (b⁻¹ * h * c) * (c⁻¹ * k * d) * (d⁻¹ * m * a)
      = a⁻¹ * (g * h * k * m) * a := by
  group

def s01 : Equiv.Perm (Fin 3) := Equiv.swap 0 1
def s12 : Equiv.Perm (Fin 3) := Equiv.swap 1 2

theorem s3_swaps_do_not_commute : s01 * s12 ≠ s12 * s01 := by
  decide

theorem s3_two_swap_product_ne_one :
    s01 * s12 * (1 : Equiv.Perm (Fin 3)) * 1 ≠ 1 := by
  decide

def cF (nc : Rat) : Rat := (nc ^ 2 - 1) / (2 * nc)
def cA (nc : Rat) : Rat := nc
def singlet (nc : Rat) : Rat := -cF nc
def octet (nc : Rat) : Rat := cA nc / 2 - cF nc
def sextet (nc : Rat) : Rat := (1 : Rat) / 2 - 1 / (2 * nc)
def antitriplet (nc : Rat) : Rat := -(1 : Rat) / 2 - 1 / (2 * nc)

theorem su3_channel_values :
    cF 3 = 4 / 3 ∧
    cA 3 = 3 ∧
    singlet 3 = -4 / 3 ∧
    octet 3 = 1 / 6 ∧
    sextet 3 = 1 / 3 ∧
    antitriplet 3 = -2 / 3 ∧
    singlet 3 < 0 ∧
    octet 3 > 0 := by
  simp only [cF, cA, singlet, octet, sextet, antitriplet]
  norm_num

def beta0 (nc nf : Rat) : Rat := (11 / 3) * nc - (2 / 3) * nf

def beta1 (nc nf : Rat) : Rat :=
  (34 / 3) * (nc ^ 2) - ((10 / 3) * nc + (nc ^ 2 - 1) / nc) * nf

theorem gluon_split_and_one_flavor :
    (4 : Rat) * cA 3 + (-1 / 3) * cA 3 = 11 ∧
    (-4 / 3 : Rat) * (1 / 2) = -2 / 3 ∧
    (-4 / 3 : Rat) < 0 := by
  simp only [cA]
  norm_num

theorem beta0_values :
    beta0 3 0 = 11 ∧
    beta0 3 3 = 9 ∧
    beta0 3 5 = 23 / 3 ∧
    beta0 3 6 = 7 ∧
    beta0 3 16 = 1 / 3 ∧
    beta0 3 17 = -1 / 3 := by
  simp only [beta0]
  norm_num

theorem beta0_window (nf : Rat) : beta0 3 nf > 0 ↔ nf < 33 / 2 := by
  unfold beta0
  constructor <;> intro h <;> linarith

theorem beta0_nat_through_16 (n : Nat) (hn : n ≤ 16) : beta0 3 (n : Rat) > 0 := by
  interval_cases n <;> unfold beta0 <;> norm_num

theorem beta0_17_negative : beta0 3 17 < 0 := by
  simp only [beta0]
  norm_num

theorem beta1_su3 (nf : Rat) : beta1 3 nf = 102 - (38 / 3) * nf := by
  unfold beta1
  ring

theorem beta1_values :
    beta1 3 0 = 102 ∧
    beta1 3 5 = 116 / 3 ∧
    beta1 3 16 = -302 / 3 := by
  simp only [beta1]
  norm_num

theorem banks_zaks_ratio_nf16 : (-beta0 3 16) / beta1 3 16 = 1 / 302 := by
  simp only [beta0, beta1]
  norm_num

def areaMonomial (b : Rat) (r t : Nat) : Rat := b ^ (r * t)
def perimMonomial (b : Rat) (r t : Nat) : Rat := b ^ (2 * (r + t))

def creutz (wRt wPrev wRt1 wR1t : Rat) : Rat := (wRt * wPrev) / (wRt1 * wR1t)

theorem area_exponent (r t : Nat) (hr : 1 ≤ r) (ht : 1 ≤ t) :
    r * t + (r - 1) * (t - 1) = r * (t - 1) + (r - 1) * t + 1 := by
  zify [hr, ht]
  linarith

theorem perim_exponent (r t : Nat) :
    2 * (r + t) + 2 * ((r - 1) + (t - 1))
      = 2 * (r + (t - 1)) + 2 * ((r - 1) + t) := by
  omega

theorem creutz_area (b : Rat) (hb : b ≠ 0) (r t : Nat) (hr : 1 ≤ r) (ht : 1 ≤ t) :
    creutz (areaMonomial b r t) (areaMonomial b (r - 1) (t - 1))
      (areaMonomial b r (t - 1)) (areaMonomial b (r - 1) t) = b := by
  unfold creutz areaMonomial
  rw [← pow_add, ← pow_add]
  have hexp : r * t + (r - 1) * (t - 1) = (r * (t - 1) + (r - 1) * t) + 1 :=
    area_exponent r t hr ht
  rw [hexp, pow_succ]
  exact mul_div_cancel_left₀ b (pow_ne_zero _ hb)

theorem creutz_perim (b : Rat) (hb : b ≠ 0) (r t : Nat) (hr : 1 ≤ r) (ht : 1 ≤ t) :
    creutz (perimMonomial b r t) (perimMonomial b (r - 1) (t - 1))
      (perimMonomial b r (t - 1)) (perimMonomial b (r - 1) t) = 1 := by
  unfold creutz perimMonomial
  have _ := Nat.add_le_add hr ht
  rw [← pow_add, ← pow_add]
  have hexp :
      2 * (r + t) + 2 * ((r - 1) + (t - 1))
        = 2 * (r + (t - 1)) + 2 * ((r - 1) + t) :=
    perim_exponent r t
  rw [hexp]
  exact div_self (pow_ne_zero _ hb)

theorem creutz_one_ninth :
    creutz (areaMonomial (1 / 9) 2 2) (areaMonomial (1 / 9) 1 1)
      (areaMonomial (1 / 9) 2 1) (areaMonomial (1 / 9) 1 2) = 1 / 9 ∧
    creutz (areaMonomial (1 / 9) 3 3) (areaMonomial (1 / 9) 2 2)
      (areaMonomial (1 / 9) 3 2) (areaMonomial (1 / 9) 2 3) = 1 / 9 ∧
    creutz (perimMonomial (1 / 9) 2 2) (perimMonomial (1 / 9) 1 1)
      (perimMonomial (1 / 9) 2 1) (perimMonomial (1 / 9) 1 2) = 1 ∧
    creutz (perimMonomial (1 / 9) 3 3) (perimMonomial (1 / 9) 2 2)
      (perimMonomial (1 / 9) 3 2) (perimMonomial (1 / 9) 2 3) = 1 ∧
    (1 / 9 : Rat) ≠ 1 := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · simpa using creutz_area (1 / 9) (by norm_num) 2 2 (by decide) (by decide)
  · simpa using creutz_area (1 / 9) (by norm_num) 3 3 (by decide) (by decide)
  · simpa using creutz_perim (1 / 9) (by norm_num) 2 2 (by decide) (by decide)
  · simpa using creutz_perim (1 / 9) (by norm_num) 3 3 (by decide) (by decide)
  · norm_num

theorem declared_lattice_counts :
    ((9 : Int) - 1 = 8) ∧
    ((12 : Int) - 9 + 1 = 4) ∧
    ((12 : Int) - 8 = 4) := by
  omega

#print axioms CampaignTfq0011FiniteQcd.plaquette_gauge
#print axioms CampaignTfq0011FiniteQcd.s3_swaps_do_not_commute
#print axioms CampaignTfq0011FiniteQcd.s3_two_swap_product_ne_one
#print axioms CampaignTfq0011FiniteQcd.su3_channel_values
#print axioms CampaignTfq0011FiniteQcd.gluon_split_and_one_flavor
#print axioms CampaignTfq0011FiniteQcd.beta0_values
#print axioms CampaignTfq0011FiniteQcd.beta0_window
#print axioms CampaignTfq0011FiniteQcd.beta0_nat_through_16
#print axioms CampaignTfq0011FiniteQcd.beta0_17_negative
#print axioms CampaignTfq0011FiniteQcd.beta1_su3
#print axioms CampaignTfq0011FiniteQcd.beta1_values
#print axioms CampaignTfq0011FiniteQcd.banks_zaks_ratio_nf16
#print axioms CampaignTfq0011FiniteQcd.area_exponent
#print axioms CampaignTfq0011FiniteQcd.perim_exponent
#print axioms CampaignTfq0011FiniteQcd.creutz_area
#print axioms CampaignTfq0011FiniteQcd.creutz_perim
#print axioms CampaignTfq0011FiniteQcd.creutz_one_ninth
#print axioms CampaignTfq0011FiniteQcd.declared_lattice_counts

end CampaignTfq0011FiniteQcd
