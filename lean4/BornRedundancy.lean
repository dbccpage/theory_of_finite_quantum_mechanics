



namespace BornRedundancy


def listSum : List Rat → Rat
  | [] => 0
  | x :: xs => x + listSum xs

def smul (c : Rat) : List Rat → List Rat
  | [] => []
  | x :: xs => (c * x) :: smul c xs

theorem listSum_smul (c : Rat) (w : List Rat) :
    listSum (smul c w) = c * listSum w := by
  induction w with
  | nil =>
    simp [smul, listSum, Rat.mul_zero]
  | cons x xs ih =>
    simp [smul, listSum, ih, Rat.mul_add]

theorem smul_smul (c1 c2 : Rat) (w : List Rat) :
    smul c1 (smul c2 w) = smul (c1 * c2) w := by
  induction w with
  | nil => rfl
  | cons x xs ih =>
    simp [smul, ih, Rat.mul_assoc]

theorem smul_one (w : List Rat) :
    smul 1 w = w := by
  induction w with
  | nil => rfl
  | cons x xs ih =>
    simp [smul, ih, Rat.one_mul]

theorem one_inv : (1 : Rat)⁻¹ = 1 := by
  have h := Rat.mul_inv_cancel 1 (by decide)
  rw [Rat.one_mul] at h
  exact h

def normalize (w : List Rat) : List Rat :=
  smul (listSum w)⁻¹ w

theorem listSum_normalize (w : List Rat) (hw : listSum w ≠ 0) :
    listSum (normalize w) = 1 := by
  unfold normalize
  rw [listSum_smul, Rat.mul_comm, Rat.mul_inv_cancel (listSum w) hw]

theorem normalize_idempotent (w : List Rat) (hw : listSum w ≠ 0) :
    normalize (normalize w) = normalize w := by
  have h1 : listSum (normalize w) = 1 := listSum_normalize w hw
  show smul (listSum (normalize w))⁻¹ (normalize w) = normalize w
  rw [h1, one_inv, smul_one]

theorem rat_mul_left_cancel (a b c : Rat) (hc : c ≠ 0) (h : c * a = c * b) : a = b := by
  have h1 : c⁻¹ * (c * a) = c⁻¹ * (c * b) := by rw [h]
  rw [← Rat.mul_assoc, ← Rat.mul_assoc, Rat.mul_comm c⁻¹ c, Rat.mul_inv_cancel c hc, Rat.one_mul, Rat.one_mul] at h1
  exact h1

theorem rat_mul_right_cancel (a b c : Rat) (hc : c ≠ 0) (h : a * c = b * c) : a = b := by
  apply rat_mul_left_cancel a b c hc
  rw [Rat.mul_comm c a, Rat.mul_comm c b]
  exact h

theorem rat_inv_mul_cancel_left (c d : Rat) (hc : c ≠ 0) (hd : d ≠ 0) :
    (c * d)⁻¹ * c = d⁻¹ := by
  have hcd : c * d ≠ 0 := by
    intro h
    rw [Rat.mul_eq_zero] at h
    rcases h with h1 | h2
    · exact hc h1
    · exact hd h2
  apply rat_mul_right_cancel _ _ d hd
  rw [Rat.mul_assoc, Rat.mul_comm ((c * d)⁻¹) (c * d), Rat.mul_inv_cancel (c * d) hcd,
      Rat.mul_comm d⁻¹ d, Rat.mul_inv_cancel d hd]

theorem normalize_smul (c : Rat) (w : List Rat) (hc : c ≠ 0) (hw : listSum w ≠ 0) :
    normalize (smul c w) = normalize w := by
  unfold normalize
  rw [listSum_smul, smul_smul, rat_inv_mul_cancel_left c (listSum w) hc hw]

theorem ne_zero_of_pos {a : Rat} (ha : 0 < a) : a ≠ 0 := by
  intro h
  rw [h] at ha
  exact Rat.lt_irrefl ha

theorem smul_cancel_inv (c : Rat) (w : List Rat) (hc : c ≠ 0) :
    smul c (smul c⁻¹ w) = w := by
  rw [smul_smul, Rat.mul_inv_cancel c hc, smul_one]

theorem ray_quotient_classification (w1 w2 : List Rat)
    (hw1 : 0 < listSum w1) (hw2 : 0 < listSum w2) :
    normalize w1 = normalize w2 ↔ ∃ c : Rat, 0 < c ∧ w2 = smul c w1 := by
  constructor
  · intro hnorm
    have hw1_ne : listSum w1 ≠ 0 := ne_zero_of_pos hw1
    have hw2_ne : listSum w2 ≠ 0 := ne_zero_of_pos hw2
    let c := listSum w2 * (listSum w1)⁻¹
    have hc_pos : 0 < c := by
      apply Rat.mul_pos hw2
      rw [Rat.inv_pos]
      exact hw1
    have hinv : w2 = smul (listSum w2) (normalize w2) := by
      unfold normalize
      rw [smul_cancel_inv (listSum w2) w2 hw2_ne]
    have hw2_eq : w2 = smul c w1 := by
      rw [hinv, ← hnorm]
      unfold normalize
      rw [smul_smul]
    exact ⟨c, hc_pos, hw2_eq⟩
  · intro h
    rcases h with ⟨c, hc_pos, rfl⟩
    have hc_ne : c ≠ 0 := ne_zero_of_pos hc_pos
    have hw1_ne : listSum w1 ≠ 0 := ne_zero_of_pos hw1
    exact (normalize_smul c w1 hc_ne hw1_ne).symm



def iabs (x : Int) : Int :=
  if x < 0 then -x else x

theorem iabs_nonneg (x : Int) : 0 ≤ iabs x := by
  unfold iabs
  split <;> omega

def D1 (x y : Int) : Int :=
  iabs x + iabs y - iabs (x + y)

theorem D1_nonneg (x y : Int) : 0 ≤ D1 x y := by
  unfold D1 iabs
  split <;> split <;> split <;> omega

theorem D1_zero_iff_same_sign (x y : Int) :
    D1 x y = 0 ↔ (0 ≤ x ∧ 0 ≤ y) ∨ (x ≤ 0 ∧ y ≤ 0) := by
  unfold D1 iabs
  constructor
  · intro h
    split at h <;> split at h <;> split at h <;> omega
  · rintro (⟨hx, hy⟩ | ⟨hx, hy⟩)
    · split <;> split <;> split <;> omega
    · split <;> split <;> split <;> omega

theorem mul_nonneg_iff (a b : Int) :
    0 ≤ a * b ↔ (0 ≤ a ∧ 0 ≤ b) ∨ (a ≤ 0 ∧ b ≤ 0) := by
  constructor
  · intro h
    by_cases ha : 0 ≤ a
    · by_cases hb : 0 ≤ b
      · left; exact ⟨ha, hb⟩
      · by_cases ha0 : a = 0
        · right; omega
        · have ha_pos : 0 < a := by omega
          have hb_neg : b < 0 := by omega
          have hneg : a * b < 0 := Int.mul_neg_of_pos_of_neg ha_pos hb_neg
          omega
    · by_cases hb : 0 ≤ b
      · by_cases hb0 : b = 0
        · right; omega
        · have ha_neg : a < 0 := by omega
          have hb_pos : 0 < b := by omega
          have hneg : a * b < 0 := Int.mul_neg_of_neg_of_pos ha_neg hb_pos
          omega
      · right; omega
  · rintro (⟨ha, hb⟩ | ⟨ha, hb⟩)
    · exact Int.mul_nonneg ha hb
    · exact Int.mul_nonneg_of_nonpos_of_nonpos ha hb

theorem D1_zero_iff_mul_nonneg (x y : Int) :
    D1 x y = 0 ↔ 0 ≤ x * y := by
  rw [D1_zero_iff_same_sign, mul_nonneg_iff]



theorem sq_mul (a b : Int) : (a * b) * (a * b) = (a * a) * (b * b) := by
  calc
    (a * b) * (a * b) = a * (b * (a * b)) := by rw [Int.mul_assoc]
    _ = a * (b * a * b) := by rw [← Int.mul_assoc b a b]
    _ = a * (a * b * b) := by rw [Int.mul_comm b a]
    _ = a * (a * (b * b)) := by rw [Int.mul_assoc a b b]
    _ = (a * a) * (b * b) := by rw [← Int.mul_assoc a a]

theorem sq_diff_cross (a b : Int) :
    (a + b) * (a + b) - (a - b) * (a - b) = 4 * (a * b) := by
  have h1 : (a + b) * (a + b) = a * a + (a * b + b * a) + b * b := by
    rw [Int.add_mul, Int.mul_add, Int.mul_add]
    omega
  have h2 : (a - b) * (a - b) = a * a - (a * b + b * a) + b * b := by
    rw [Int.sub_mul, Int.mul_sub, Int.mul_sub]
    omega
  rw [h1, h2]
  have hab : b * a = a * b := Int.mul_comm b a
  rw [hab]
  omega

structure Mat2 where
  a : Int
  b : Int
  c : Int
  d : Int

structure Vec2 where
  x : Int
  y : Int
deriving DecidableEq

def applyMat2 (M : Mat2) (v : Vec2) : Vec2 :=
  ⟨M.a * v.x + M.b * v.y, M.c * v.x + M.d * v.y⟩

def sqNorm (v : Vec2) : Vec2 :=
  ⟨v.x * v.x, v.y * v.y⟩

def PhaseEquiv (v1 v2 : Vec2) : Prop :=
  sqNorm v1 = sqNorm v2

def DescentCompatible (M : Mat2) : Prop :=
  ∀ v1 v2 : Vec2, PhaseEquiv v1 v2 → PhaseEquiv (applyMat2 M v1) (applyMat2 M v2)

def RowSparse (M : Mat2) : Prop :=
  (M.a = 0 ∨ M.b = 0) ∧ (M.c = 0 ∨ M.d = 0)

theorem row_sparse_implies_descent_compatible (M : Mat2) (hM : RowSparse M) :
    DescentCompatible M := by
  intro v1 v2 hpe
  unfold PhaseEquiv sqNorm at hpe
  simp only [Vec2.mk.injEq] at hpe
  rcases hpe with ⟨hx, hy⟩
  unfold PhaseEquiv sqNorm applyMat2
  simp only [Vec2.mk.injEq]
  rcases hM with ⟨ha | hb, hc | hd⟩
  · rw [ha, hc]
    simp only [Int.zero_mul, Int.zero_add]
    constructor
    · rw [sq_mul, hy, ← sq_mul]
    · rw [sq_mul, hy, ← sq_mul]
  · rw [ha, hd]
    simp only [Int.zero_mul, Int.zero_add, Int.add_zero]
    constructor
    · rw [sq_mul, hy, ← sq_mul]
    · rw [sq_mul, hx, ← sq_mul]
  · rw [hb, hc]
    simp only [Int.zero_mul, Int.add_zero, Int.zero_add]
    constructor
    · rw [sq_mul, hx, ← sq_mul]
    · rw [sq_mul, hy, ← sq_mul]
  · rw [hb, hd]
    simp only [Int.zero_mul, Int.add_zero]
    constructor
    · rw [sq_mul, hx, ← sq_mul]
    · rw [sq_mul, hx, ← sq_mul]

theorem not_row_sparse_first_row (M : Mat2) (ha : M.a ≠ 0) (hb : M.b ≠ 0) :
    ¬ DescentCompatible M := by
  intro hdc
  let v1 : Vec2 := ⟨1, 1⟩
  let v2 : Vec2 := ⟨1, -1⟩
  have hpe : PhaseEquiv v1 v2 := by
    unfold PhaseEquiv sqNorm
    rfl
  have hres := hdc v1 v2 hpe
  unfold PhaseEquiv sqNorm applyMat2 at hres
  simp only [Vec2.mk.injEq] at hres
  have hrow1 := hres.1
  have h_eval1 : M.a * (1 : Int) + M.b * (1 : Int) = M.a + M.b := by omega
  have h_eval2 : M.a * (1 : Int) + M.b * (-1 : Int) = M.a - M.b := by omega
  rw [h_eval1, h_eval2] at hrow1
  have h_sub : (M.a + M.b) * (M.a + M.b) - (M.a - M.b) * (M.a - M.b) = 0 := by
    omega
  rw [sq_diff_cross] at h_sub
  have hab0 : M.a * M.b = 0 := by omega
  cases Int.mul_eq_zero.mp hab0 with
  | inl h1 => exact ha h1
  | inr h2 => exact hb h2

theorem not_row_sparse_second_row (M : Mat2) (hc : M.c ≠ 0) (hd : M.d ≠ 0) :
    ¬ DescentCompatible M := by
  intro hdc
  let v1 : Vec2 := ⟨1, 1⟩
  let v2 : Vec2 := ⟨1, -1⟩
  have hpe : PhaseEquiv v1 v2 := by
    unfold PhaseEquiv sqNorm
    rfl
  have hres := hdc v1 v2 hpe
  unfold PhaseEquiv sqNorm applyMat2 at hres
  simp only [Vec2.mk.injEq] at hres
  have hrow2 := hres.2
  have h_eval1 : M.c * (1 : Int) + M.d * (1 : Int) = M.c + M.d := by omega
  have h_eval2 : M.c * (1 : Int) + M.d * (-1 : Int) = M.c - M.d := by omega
  rw [h_eval1, h_eval2] at hrow2
  have h_sub : (M.c + M.d) * (M.c + M.d) - (M.c - M.d) * (M.c - M.d) = 0 := by
    omega
  rw [sq_diff_cross] at h_sub
  have hcd0 : M.c * M.d = 0 := by omega
  cases Int.mul_eq_zero.mp hcd0 with
  | inl h1 => exact hc h1
  | inr h2 => exact hd h2

theorem descent_compatible_iff_row_sparse (M : Mat2) :
    DescentCompatible M ↔ RowSparse M := by
  constructor
  · intro hdc
    unfold RowSparse
    constructor
    · by_cases ha : M.a = 0
      · left; exact ha
      · by_cases hb : M.b = 0
        · right; exact hb
        · exfalso; exact not_row_sparse_first_row M ha hb hdc
    · by_cases hc : M.c = 0
      · left; exact hc
      · by_cases hd : M.d = 0
        · right; exact hd
        · exfalso; exact not_row_sparse_second_row M hc hd hdc
  · exact row_sparse_implies_descent_compatible M

end BornRedundancy

private def l5aProvenance : String :=
  "Origin: lean4/BornRedundancy.lean Claim: listSum_smul AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
