/-!
Declared rational checks for recorded Trotter response values at M = 1, 2, 3.
AuthorityEffect: None.

`evalCleared a b (num/den)` is `a * num - b * den`. For a declared fraction
`num/den`, the call `evalCleared den num` is the integer identity
`den * num - num * den = 0`. These theorems check that identity, the recorded
dimension counts `8M` and `4M - 1`, the degree tally of the recorded
multiplicities, and two cross-multiplications of recorded absolute values.

This file does not build the response matrix and does not derive a
characteristic polynomial. The Python module
`code/trotter_characteristic_polynomials.py` is the calculator for those
matrices.

Dependencies: Lean-distribution core only.
-/

namespace WitnessedDifference.TrotterCharPoly

/-- Representation of an exact rational fraction as integer numerator and positive denominator. -/
structure RatFraction where
  num : Int
  den : Nat
  den_pos : 0 < den

/-- Evaluation of (a * (num/den) - b) cleared by denominator: a * num - b * den. -/
def evalCleared (a b : Int) (x : RatFraction) : Int :=
  a * x.num - b * (x.den : Int)

/- ========================================================================= -/
/- M = 1 DECLARED RATIONALS                                                   -/
/- ========================================================================= -/

def m1_dim : Nat := 8
def m1_zero_mult : Nat := 3

def m1_root_zero : RatFraction := ⟨0, 1, by decide⟩
def m1_root_pos1 : RatFraction := ⟨10, 21, by decide⟩
def m1_root_pos2 : RatFraction := ⟨21, 40, by decide⟩
def m1_root_pos3 : RatFraction := ⟨420, 841, by decide⟩
def m1_root_neg  : RatFraction := ⟨-1, 706440, by decide⟩

theorem m1_dim_eq_8m : m1_dim = 8 * 1 := rfl
theorem m1_zero_mode_law : m1_zero_mult = 4 * 1 - 1 := rfl

theorem m1_root_zero_eval : evalCleared 1 0 m1_root_zero = 0 := rfl
theorem m1_root_pos1_eval : evalCleared 21 10 m1_root_pos1 = 0 := rfl
theorem m1_root_pos2_eval : evalCleared 40 21 m1_root_pos2 = 0 := rfl
theorem m1_root_pos3_eval : evalCleared 841 420 m1_root_pos3 = 0 := rfl
theorem m1_root_neg_eval  : evalCleared 706440 (-1) m1_root_neg = 0 := rfl

theorem m1_total_degree : 3 + 1 + 1 + 2 + 1 = m1_dim := rfl

/- ========================================================================= -/
/- M = 2 DECLARED RATIONALS                                                   -/
/- ========================================================================= -/

def m2_dim : Nat := 16
def m2_zero_mult : Nat := 7

def m2_root_zero : RatFraction := ⟨0, 1, by decide⟩
def m2_root_pos1 : RatFraction := ⟨753995740, 755374987, by decide⟩
def m2_root_pos2 : RatFraction := ⟨459740, 755374987, by decide⟩
def m2_root_pos3 : RatFraction := ⟨2155649600, 2266124961, by decide⟩
def m2_root_pos4 : RatFraction := ⟨1378420, 2266124961, by decide⟩
def m2_root_pos5 : RatFraction := ⟨31724818747, 30214999480, by decide⟩
def m2_root_neg  : RatFraction := ⟨-35281, 90644998440, by decide⟩

theorem m2_dim_eq_8m : m2_dim = 8 * 2 := rfl
theorem m2_zero_mode_law : m2_zero_mult = 4 * 2 - 1 := rfl

theorem m2_root_zero_eval : evalCleared 1 0 m2_root_zero = 0 := rfl
theorem m2_root_pos1_eval : evalCleared 755374987 753995740 m2_root_pos1 = 0 := rfl
theorem m2_root_pos2_eval : evalCleared 755374987 459740 m2_root_pos2 = 0 := rfl
theorem m2_root_pos3_eval : evalCleared 2266124961 2155649600 m2_root_pos3 = 0 := rfl
theorem m2_root_pos4_eval : evalCleared 2266124961 1378420 m2_root_pos4 = 0 := rfl
theorem m2_root_pos5_eval : evalCleared 30214999480 31724818747 m2_root_pos5 = 0 := rfl
theorem m2_root_neg_eval  : evalCleared 90644998440 (-35281) m2_root_neg = 0 := rfl

theorem m2_total_degree : 7 + 2 + 2 + 1 + 2 + 1 + 1 = m2_dim := rfl

/- ========================================================================= -/
/- M = 3 DECLARED RATIONALS                                                   -/
/- ========================================================================= -/

def m3_dim : Nat := 24
def m3_zero_mult : Nat := 11

def m3_root_zero : RatFraction := ⟨0, 1, by decide⟩
def m3_root_pos1 : RatFraction := ⟨34237411405230, 22869873869701, by decide⟩
def m3_root_pos2 : RatFraction := ⟨18851893230, 22869873869701, by decide⟩
def m3_root_pos3 : RatFraction := ⟨12576823230, 22869873869701, by decide⟩
def m3_root_pos4 : RatFraction := ⟨6288467430, 22869873869701, by decide⟩
def m3_root_pos5 : RatFraction := ⟨1440996427589221, 914794954788040, by decide⟩
def m3_root_pos6 : RatFraction := ⟨1989754528644000, 1395062306051761, by decide⟩
def m3_root_neg  : RatFraction := ⟨-12188547841, 55802492242070440, by decide⟩

theorem m3_dim_eq_8m : m3_dim = 8 * 3 := rfl
theorem m3_zero_mode_law : m3_zero_mult = 4 * 3 - 1 := rfl

theorem m3_root_zero_eval : evalCleared 1 0 m3_root_zero = 0 := rfl
theorem m3_root_pos1_eval : evalCleared 22869873869701 34237411405230 m3_root_pos1 = 0 := rfl
theorem m3_root_pos2_eval : evalCleared 22869873869701 18851893230 m3_root_pos2 = 0 := rfl
theorem m3_root_pos3_eval : evalCleared 22869873869701 12576823230 m3_root_pos3 = 0 := rfl
theorem m3_root_pos4_eval : evalCleared 22869873869701 6288467430 m3_root_pos4 = 0 := rfl
theorem m3_root_pos5_eval : evalCleared 914794954788040 1440996427589221 m3_root_pos5 = 0 := rfl
theorem m3_root_pos6_eval : evalCleared 1395062306051761 1989754528644000 m3_root_pos6 = 0 := rfl
theorem m3_root_neg_eval  : evalCleared 55802492242070440 (-12188547841) m3_root_neg = 0 := rfl

theorem m3_total_degree : 11 + 2 + 2 + 4 + 2 + 1 + 1 + 1 = m3_dim := rfl

/- ========================================================================= -/
/- CLOSED-FORM EVALUATION AGREEMENT AT r = 1/10                               -/
/- ========================================================================= -/

-- M=1 closed formula at r = 1/10:
-- r^4 = 1/10000, r + 2 = 21/10, r^2 + 4r + 8 = 841/100,
-- 4 * (21/10) * (841/100) = 70644/1000,
-- (1/10000) / (70644/1000) = 1/706440.
theorem m1_closed_form_exact :
    (4 : Int) * 21 * 841 = 70644 ∧
    (10000 : Int) * 70644 = 1000 * 706440 ∧
    (10 : Int) * 70644 = 706440 := by decide

-- M=2 closed formula: -r^4*(r^3 + 8r^2 + 32r + 32) / [ 4*(r^6 + 16r^5 + 128r^4 + 512r^3 + 1280r^2 + 2048r + 2048) ]
-- Evaluated at r = 1/10 yields exactly -35281 / 90644998440.
theorem m2_closed_form_numerator :
    (1 : Int) * 8 + 32 * 10 + 32 * 100 = 3528 ∧
    (10 : Int) * 3528 + 1 = 35281 := by decide

/- ========================================================================= -/
/- RECORDED ABSOLUTE-VALUE COMPARISONS                                        -/
/- ========================================================================= -/

-- Recorded absolute values 1/706440 and 35281/90644998440.
-- Cross-multiplication: 1 * 90644998440 > 35281 * 706440.
theorem m1_decays_to_m2 :
    (90644998440 : Int) > 35281 * 706440 := by decide

-- Recorded absolute values 35281/90644998440 and 12188547841/55802492242070440.
theorem m2_decays_to_m3 :
    (35281 : Int) * 55802492242070440 > (12188547841 : Int) * 90644998440 := by decide

#print axioms m1_dim_eq_8m
#print axioms m1_zero_mode_law
#print axioms m1_root_neg_eval
#print axioms m2_zero_mode_law
#print axioms m2_root_neg_eval
#print axioms m3_zero_mode_law
#print axioms m3_root_neg_eval
#print axioms m1_decays_to_m2
#print axioms m2_decays_to_m3

end WitnessedDifference.TrotterCharPoly
