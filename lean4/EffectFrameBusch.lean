
namespace HilbertWalk.EffectFrameBusch


def half : Rat := (2 : Rat)⁻¹

theorem two_ne_zero : (2 : Rat) ≠ 0 := by decide

theorem two_mul_half : (2 : Rat) * half = 1 := by
  dsimp [half]
  exact Rat.mul_inv_cancel 2 two_ne_zero

theorem half_mul_two : half * (2 : Rat) = 1 := by
  dsimp [half]
  exact Rat.inv_mul_cancel 2 two_ne_zero

theorem half_ne_zero : half ≠ 0 := by
  intro h
  have h1 : (2 : Rat) * half = 1 := two_mul_half
  rw [h, Rat.mul_zero] at h1
  contradiction

theorem rat_add_le_add {a b c d : Rat} (h1 : a ≤ b) (h2 : c ≤ d) : a + c ≤ b + d := by
  have h1' : a + c ≤ b + c := Rat.add_le_add_right.mpr h1
  have h2' : b + c ≤ b + d := Rat.add_le_add_left.mpr h2
  exact Rat.le_trans h1' h2'

theorem rat_le_add_of_nonneg_right {a b : Rat} (h : 0 ≤ b) : a ≤ a + b := by
  have h' : a + 0 ≤ a + b := rat_add_le_add (Rat.le_refl) h
  rw [Rat.add_zero] at h'
  exact h'

theorem rat_add_sub_cancel_alt (a b : Rat) : a + (b - a) = b := by
  rw [Rat.add_comm a (b - a), Rat.sub_add_cancel]

theorem rat_zero_add_six : (0 : Rat) + 0 + 0 + 0 + 0 + 0 = 0 := by
  have hz : (0 : Rat) + 0 = 0 := Rat.add_zero 0
  rw [hz, hz, hz, hz, hz]


structure Herm2 where
  a : Rat
  b_re : Rat
  b_im : Rat
  d : Rat
  deriving DecidableEq, Repr

def zero2 : Herm2 := ⟨0, 0, 0, 0⟩
def id2 : Herm2 := ⟨1, 0, 0, 1⟩

def add2 (A B : Herm2) : Herm2 :=
  ⟨A.a + B.a, A.b_re + B.b_re, A.b_im + B.b_im, A.d + B.d⟩

def sub2 (A B : Herm2) : Herm2 :=
  ⟨A.a - B.a, A.b_re - B.b_re, A.b_im - B.b_im, A.d - B.d⟩

def smul2 (c : Rat) (A : Herm2) : Herm2 :=
  ⟨c * A.a, c * A.b_re, c * A.b_im, c * A.d⟩

def tr2 (A : Herm2) : Rat := A.a + A.d

def tr_prod2 (A B : Herm2) : Rat :=
  A.a * B.a + A.d * B.d + 2 * (A.b_re * B.b_re + A.b_im * B.b_im)

def is_pos2 (A : Herm2) : Prop :=
  0 ≤ A.a ∧ 0 ≤ A.d ∧ 0 ≤ A.a * A.d - (A.b_re * A.b_re + A.b_im * A.b_im)

def le2 (A B : Herm2) : Prop := is_pos2 (sub2 B A)

def is_effect2 (E : Herm2) : Prop := is_pos2 E ∧ is_pos2 (sub2 id2 E)

structure Eff2 where
  mat : Herm2
  h_pos : is_pos2 mat
  h_le_id : is_pos2 (sub2 id2 mat)

def D0_2 : Herm2 := ⟨1, 0, 0, 0⟩
def D1_2 : Herm2 := ⟨0, 0, 0, 1⟩
def S01_2 : Herm2 := ⟨0, 1, 0, 0⟩
def T01_2 : Herm2 := ⟨0, 0, 1, 0⟩

def P_plus_2 : Herm2 := ⟨half, half, 0, half⟩
def P_R_2 : Herm2 := ⟨half, 0, half, half⟩

theorem herm2_basis_expansion (A : Herm2) :
    A = add2 (smul2 A.a D0_2)
         (add2 (smul2 A.d D1_2)
               (add2 (smul2 A.b_re S01_2) (smul2 A.b_im T01_2))) := by
  cases A
  dsimp [add2, smul2, D0_2, D1_2, S01_2, T01_2]
  repeat rw [Rat.mul_zero]
  repeat rw [Rat.mul_one]
  repeat rw [Rat.add_zero]
  repeat rw [Rat.zero_add]

structure Herm3 where
  a00 : Rat
  a11 : Rat
  a22 : Rat
  a01_re : Rat
  a01_im : Rat
  a02_re : Rat
  a02_im : Rat
  a12_re : Rat
  a12_im : Rat
  deriving DecidableEq, Repr

def zero3 : Herm3 := ⟨0, 0, 0, 0, 0, 0, 0, 0, 0⟩
def id3 : Herm3 := ⟨1, 1, 1, 0, 0, 0, 0, 0, 0⟩

def add3 (A B : Herm3) : Herm3 :=
  ⟨A.a00 + B.a00, A.a11 + B.a11, A.a22 + B.a22,
   A.a01_re + B.a01_re, A.a01_im + B.a01_im,
   A.a02_re + B.a02_re, A.a02_im + B.a02_im,
   A.a12_re + B.a12_re, A.a12_im + B.a12_im⟩

def sub3 (A B : Herm3) : Herm3 :=
  ⟨A.a00 - B.a00, A.a11 - B.a11, A.a22 - B.a22,
   A.a01_re - B.a01_re, A.a01_im - B.a01_im,
   A.a02_re - B.a02_re, A.a02_im - B.a02_im,
   A.a12_re - B.a12_re, A.a12_im - B.a12_im⟩

def smul3 (c : Rat) (A : Herm3) : Herm3 :=
  ⟨c * A.a00, c * A.a11, c * A.a22,
   c * A.a01_re, c * A.a01_im,
   c * A.a02_re, c * A.a02_im,
   c * A.a12_re, c * A.a12_im⟩

def tr3 (A : Herm3) : Rat := A.a00 + A.a11 + A.a22

def tr_prod3 (A B : Herm3) : Rat :=
  A.a00 * B.a00 + A.a11 * B.a11 + A.a22 * B.a22 +
  2 * (A.a01_re * B.a01_re + A.a01_im * B.a01_im +
       A.a02_re * B.a02_re + A.a02_im * B.a02_im +
       A.a12_re * B.a12_re + A.a12_im * B.a12_im)

def det3 (A : Herm3) : Rat :=
  A.a00 * A.a11 * A.a22 -
  A.a00 * (A.a12_re * A.a12_re + A.a12_im * A.a12_im) -
  A.a11 * (A.a02_re * A.a02_re + A.a02_im * A.a02_im) -
  A.a22 * (A.a01_re * A.a01_re + A.a01_im * A.a01_im) +
  2 * ((A.a01_re * A.a12_re - A.a01_im * A.a12_im) * A.a02_re +
       (A.a01_re * A.a12_im + A.a01_im * A.a12_re) * A.a02_im)

def principal_minors_le_two3 (A : Herm3) : Prop :=
  0 ≤ A.a00 ∧ 0 ≤ A.a11 ∧ 0 ≤ A.a22 ∧
  0 ≤ A.a00 * A.a11 - (A.a01_re * A.a01_re + A.a01_im * A.a01_im) ∧
  0 ≤ A.a00 * A.a22 - (A.a02_re * A.a02_re + A.a02_im * A.a02_im) ∧
  0 ≤ A.a11 * A.a22 - (A.a12_re * A.a12_re + A.a12_im * A.a12_im)

def is_pos3 (A : Herm3) : Prop := principal_minors_le_two3 A ∧ 0 ≤ det3 A

def le3 (A B : Herm3) : Prop := is_pos3 (sub3 B A)

def is_effect3 (E : Herm3) : Prop := is_pos3 E ∧ is_pos3 (sub3 id3 E)

def negative_minor_control3 : Herm3 :=
  ⟨1/4, 1/4, 1/4, -1/4, 0, -1/4, 0, -1/4, 0⟩

theorem lower_minors_can_admit_a_false_effect :
    principal_minors_le_two3 negative_minor_control3 ∧
    principal_minors_le_two3 (sub3 id3 negative_minor_control3) := by
  dsimp [principal_minors_le_two3, negative_minor_control3, sub3, id3]
  grind

theorem negative_minor_control_determinant :
    det3 negative_minor_control3 = -1/16 := by
  dsimp [det3, negative_minor_control3]
  grind

theorem negative_minor_control_not_effect :
    ¬ is_effect3 negative_minor_control3 := by
  dsimp [is_effect3, is_pos3, principal_minors_le_two3, det3, negative_minor_control3, sub3, id3]
  grind

def phase_rank_one_control3 : Herm3 :=
  ⟨1/3, 1/3, 1/3, 0, -1/3, 1/3, 0, 0, 1/3⟩

theorem phase_rank_one_control_is_effect :
    det3 phase_rank_one_control3 = 0 ∧ is_effect3 phase_rank_one_control3 := by
  dsimp [is_effect3, is_pos3, principal_minors_le_two3, det3, phase_rank_one_control3, sub3, id3]
  grind

theorem zero_and_identity_are_effects3 : is_effect3 zero3 ∧ is_effect3 id3 := by
  dsimp [is_effect3, is_pos3, principal_minors_le_two3, det3, sub3, zero3, id3]
  grind

structure Eff3 where
  mat : Herm3
  h_pos : is_pos3 mat
  h_le_id : is_pos3 (sub3 id3 mat)

def D0_3 : Herm3 := ⟨1, 0, 0, 0, 0, 0, 0, 0, 0⟩
def D1_3 : Herm3 := ⟨0, 1, 0, 0, 0, 0, 0, 0, 0⟩
def D2_3 : Herm3 := ⟨0, 0, 1, 0, 0, 0, 0, 0, 0⟩
def S01_3 : Herm3 := ⟨0, 0, 0, 1, 0, 0, 0, 0, 0⟩
def T01_3 : Herm3 := ⟨0, 0, 0, 0, 1, 0, 0, 0, 0⟩
def S02_3 : Herm3 := ⟨0, 0, 0, 0, 0, 1, 0, 0, 0⟩
def T02_3 : Herm3 := ⟨0, 0, 0, 0, 0, 0, 1, 0, 0⟩
def S12_3 : Herm3 := ⟨0, 0, 0, 0, 0, 0, 0, 1, 0⟩
def T12_3 : Herm3 := ⟨0, 0, 0, 0, 0, 0, 0, 0, 1⟩

theorem herm3_basis_expansion (A : Herm3) :
    A = add3 (smul3 A.a00 D0_3)
         (add3 (smul3 A.a11 D1_3)
          (add3 (smul3 A.a22 D2_3)
           (add3 (smul3 A.a01_re S01_3)
            (add3 (smul3 A.a01_im T01_3)
             (add3 (smul3 A.a02_re S02_3)
              (add3 (smul3 A.a02_im T02_3)
               (add3 (smul3 A.a12_re S12_3) (smul3 A.a12_im T12_3)))))))) := by
  cases A
  dsimp [add3, smul3, D0_3, D1_3, D2_3, S01_3, T01_3, S02_3, T02_3, S12_3, T12_3]
  repeat rw [Rat.mul_zero]
  repeat rw [Rat.mul_one]
  repeat rw [Rat.add_zero]
  repeat rw [Rat.zero_add]


structure EffectFrameFunction2 where
  eval : Herm2 → Rat
  h_norm : eval id2 = 1
  h_zero : eval zero2 = 0
  h_pos : ∀ E : Herm2, is_pos2 E → 0 ≤ eval E
  h_add : ∀ E1 E2 : Herm2, is_pos2 E1 → is_pos2 E2 → is_pos2 (sub2 id2 (add2 E1 E2)) →
            eval (add2 E1 E2) = eval E1 + eval E2

structure EffectFrameFunction3 where
  eval : Herm3 → Rat
  h_norm : eval id3 = 1
  h_zero : eval zero3 = 0
  h_pos : ∀ E : Herm3, is_pos3 E → 0 ≤ eval E
  h_add : ∀ E1 E2 : Herm3, is_pos3 E1 → is_pos3 E2 → is_pos3 (sub3 id3 (add3 E1 E2)) →
            eval (add3 E1 E2) = eval E1 + eval E2


theorem herm2_add_sub_cancel (E1 E2 : Herm2) : add2 E1 (sub2 E2 E1) = E2 := by
  cases E1
  cases E2
  dsimp [add2, sub2]
  rw [rat_add_sub_cancel_alt, rat_add_sub_cancel_alt, rat_add_sub_cancel_alt, rat_add_sub_cancel_alt]

theorem monotonicity2 (f : EffectFrameFunction2) (E1 E2 : Herm2)
    (hE1 : is_pos2 E1) (_hE2 : is_pos2 E2) (hE2_le : is_pos2 (sub2 id2 E2))
    (hle : le2 E1 E2) :
    f.eval E1 ≤ f.eval E2 := by
  have h_delta : is_pos2 (sub2 E2 E1) := hle
  have h_decomp : add2 E1 (sub2 E2 E1) = E2 := herm2_add_sub_cancel E1 E2
  have h_sum_le : is_pos2 (sub2 id2 (add2 E1 (sub2 E2 E1))) := by
    rw [h_decomp]
    exact hE2_le
  have h_add : f.eval (add2 E1 (sub2 E2 E1)) = f.eval E1 + f.eval (sub2 E2 E1) :=
    f.h_add E1 (sub2 E2 E1) hE1 h_delta h_sum_le
  rw [h_decomp] at h_add
  have h_pos_delta : 0 ≤ f.eval (sub2 E2 E1) := f.h_pos (sub2 E2 E1) h_delta
  have h_le : f.eval E1 ≤ f.eval E1 + f.eval (sub2 E2 E1) :=
    rat_le_add_of_nonneg_right h_pos_delta
  rw [← h_add] at h_le
  exact h_le

theorem herm3_add_sub_cancel (E1 E2 : Herm3) : add3 E1 (sub3 E2 E1) = E2 := by
  cases E1
  cases E2
  dsimp [add3, sub3]
  rw [rat_add_sub_cancel_alt, rat_add_sub_cancel_alt, rat_add_sub_cancel_alt,
      rat_add_sub_cancel_alt, rat_add_sub_cancel_alt, rat_add_sub_cancel_alt,
      rat_add_sub_cancel_alt, rat_add_sub_cancel_alt, rat_add_sub_cancel_alt]

theorem monotonicity3 (f : EffectFrameFunction3) (E1 E2 : Herm3)
    (hE1 : is_pos3 E1) (_hE2 : is_pos3 E2) (hE2_le : is_pos3 (sub3 id3 E2))
    (hle : le3 E1 E2) :
    f.eval E1 ≤ f.eval E2 := by
  have h_delta : is_pos3 (sub3 E2 E1) := hle
  have h_decomp : add3 E1 (sub3 E2 E1) = E2 := herm3_add_sub_cancel E1 E2
  have h_sum_le : is_pos3 (sub3 id3 (add3 E1 (sub3 E2 E1))) := by
    rw [h_decomp]
    exact hE2_le
  have h_add : f.eval (add3 E1 (sub3 E2 E1)) = f.eval E1 + f.eval (sub3 E2 E1) :=
    f.h_add E1 (sub3 E2 E1) hE1 h_delta h_sum_le
  rw [h_decomp] at h_add
  have h_pos_delta : 0 ≤ f.eval (sub3 E2 E1) := f.h_pos (sub3 E2 E1) h_delta
  have h_le : f.eval E1 ≤ f.eval E1 + f.eval (sub3 E2 E1) :=
    rat_le_add_of_nonneg_right h_pos_delta
  rw [← h_add] at h_le
  exact h_le


def nat_smul2 (n : Nat) (A : Herm2) : Herm2 :=
  match n with
  | 0 => zero2
  | n + 1 => add2 (nat_smul2 n A) A

theorem nat_smul2_eval (f : EffectFrameFunction2) (n : Nat) (A : Herm2)
    (_hA_pos : is_pos2 A)
    (h_step : ∀ k : Nat, k < n → is_pos2 (nat_smul2 k A) →
      is_pos2 (sub2 id2 (add2 (nat_smul2 k A) A)) →
      f.eval (add2 (nat_smul2 k A) A) = f.eval (nat_smul2 k A) + f.eval A)
    (h_pos_k : ∀ k : Nat, k ≤ n → is_pos2 (nat_smul2 k A))
    (h_le_k : ∀ k : Nat, k < n → is_pos2 (sub2 id2 (add2 (nat_smul2 k A) A))) :
    f.eval (nat_smul2 n A) = (n : Nat) * f.eval A := by
  induction n with
  | zero =>
    dsimp [nat_smul2]
    rw [f.h_zero]
    simp
  | succ n ih =>
    have h_eval_step := h_step n (Nat.lt_succ_self n) (h_pos_k n (Nat.le_succ n)) (h_le_k n (Nat.lt_succ_self n))
    have h_pos_rec : ∀ k : Nat, k ≤ n → is_pos2 (nat_smul2 k A) :=
      fun k hk => h_pos_k k (Nat.le_succ_of_le hk)
    have h_le_rec : ∀ k : Nat, k < n → is_pos2 (sub2 id2 (add2 (nat_smul2 k A) A)) :=
      fun k hk => h_le_k k (Nat.lt_succ_of_lt hk)
    have h_step_rec : ∀ k : Nat, k < n → is_pos2 (nat_smul2 k A) →
      is_pos2 (sub2 id2 (add2 (nat_smul2 k A) A)) →
      f.eval (add2 (nat_smul2 k A) A) = f.eval (nat_smul2 k A) + f.eval A :=
      fun k hk => h_step k (Nat.lt_succ_of_lt hk)
    have ih_val := ih h_step_rec h_pos_rec h_le_rec
    dsimp [nat_smul2]
    rw [h_eval_step, ih_val]
    push_cast
    have h_dist : ((n : Rat) + 1) * f.eval A = (n : Rat) * f.eval A + 1 * f.eval A :=
      Rat.add_mul (n : Rat) 1 (f.eval A)
    rw [h_dist, Rat.one_mul]

structure RationalHomogeneityWitness2 (f : EffectFrameFunction2) (E : Herm2) where
  m : Nat
  n : Nat
  hn_pos : n > 0
  hn_ne : (n : Rat) ≠ 0
  hm_le_n : m ≤ n
  E_prime : Herm2
  h_div : nat_smul2 n E_prime = E
  h_scale : nat_smul2 m E_prime = smul2 ((m : Rat) / (n : Rat)) E
  h_f_n : f.eval (nat_smul2 n E_prime) = (n : Nat) * f.eval E_prime
  h_f_m : f.eval (nat_smul2 m E_prime) = (m : Nat) * f.eval E_prime

theorem rational_homogeneity2 (f : EffectFrameFunction2) (E : Herm2)
    (w : RationalHomogeneityWitness2 f E) :
    f.eval (smul2 ((w.m : Rat) / (w.n : Rat)) E) = ((w.m : Rat) / (w.n : Rat)) * f.eval E := by
  have h_scaled := w.h_scale
  rw [← h_scaled, w.h_f_m]
  have h_div_n := w.h_div
  have h_fn := w.h_f_n
  rw [h_div_n] at h_fn
  have hn_ne := w.hn_ne
  have h_inv : f.eval w.E_prime = (w.n : Rat)⁻¹ * f.eval E := by
    rw [h_fn]
    rw [← Rat.mul_assoc, Rat.inv_mul_cancel (w.n : Rat) hn_ne, Rat.one_mul]
  rw [h_inv]
  push_cast
  have h_assoc : (w.m : Rat) * ((w.n : Rat)⁻¹ * f.eval E) = ((w.m : Rat) * (w.n : Rat)⁻¹) * f.eval E := by
    rw [Rat.mul_assoc]
  exact h_assoc


theorem density_squeeze_bracket
    (f_val_r f_val_lam f_val_s f_E : Rat)
    (r s : Rat)
    (h_hr : f_val_r = r * f_E)
    (h_hs : f_val_s = s * f_E)
    (h_mon1 : f_val_r ≤ f_val_lam)
    (h_mon2 : f_val_lam ≤ f_val_s) :
    r * f_E ≤ f_val_lam ∧ f_val_lam ≤ s * f_E := by
  constructor
  · rw [← h_hr]
    exact h_mon1
  · rw [← h_hs]
    exact h_mon2

theorem density_squeeze_forces_equality (V W lambda : Rat)
    (h_bracket : ∀ r s : Rat, r ≤ lambda → lambda ≤ s → r * W ≤ V ∧ V ≤ s * W) :
    V = lambda * W := by
  have h_self := h_bracket lambda lambda (Rat.le_refl) (Rat.le_refl)
  have h1 : lambda * W ≤ V := h_self.1
  have h2 : V ≤ lambda * W := h_self.2
  exact Rat.le_antisymm h2 h1


theorem D0_add_D1_eq_id2 : add2 D0_2 D1_2 = id2 := by
  dsimp [add2, D0_2, D1_2, id2]
  repeat rw [Rat.add_zero]
  repeat rw [Rat.zero_add]

def recover_rho2 (f : EffectFrameFunction2) : Herm2 :=
  ⟨f.eval D0_2,
   f.eval P_plus_2 - half,
   f.eval P_R_2 - half,
   f.eval D1_2⟩

theorem recover_rho2_unit_trace (f : EffectFrameFunction2)
    (h_pos_D0 : is_pos2 D0_2)
    (h_pos_D1 : is_pos2 D1_2)
    (h_ortho : is_pos2 (sub2 id2 (add2 D0_2 D1_2))) :
    tr2 (recover_rho2 f) = 1 := by
  dsimp [tr2, recover_rho2]
  have h_add := f.h_add D0_2 D1_2 h_pos_D0 h_pos_D1 h_ortho
  have h_id : add2 D0_2 D1_2 = id2 := D0_add_D1_eq_id2
  rw [h_id] at h_add
  rw [f.h_norm] at h_add
  exact h_add.symm

theorem tr_prod2_D0 (A : Herm2) : tr_prod2 A D0_2 = A.a := by
  unfold tr_prod2 D0_2
  have h1 : A.d * 0 = 0 := Rat.mul_zero A.d
  have h2 : A.b_re * 0 = 0 := Rat.mul_zero A.b_re
  have h3 : A.b_im * 0 = 0 := Rat.mul_zero A.b_im
  have h4 : A.a * 1 = A.a := Rat.mul_one A.a
  rw [h1, h2, h3, h4]
  have hz : (0 : Rat) + 0 = 0 := Rat.add_zero 0
  rw [hz]
  have hmz : (2 : Rat) * 0 = 0 := Rat.mul_zero 2
  rw [hmz]
  have ha1 : A.a + 0 = A.a := Rat.add_zero A.a
  rw [ha1, ha1]

theorem tr_prod2_D1 (A : Herm2) : tr_prod2 A D1_2 = A.d := by
  unfold tr_prod2 D1_2
  have h1 : A.a * 0 = 0 := Rat.mul_zero A.a
  have h2 : A.b_re * 0 = 0 := Rat.mul_zero A.b_re
  have h3 : A.b_im * 0 = 0 := Rat.mul_zero A.b_im
  have h4 : A.d * 1 = A.d := Rat.mul_one A.d
  rw [h1, h2, h3, h4]
  have hz : (0 : Rat) + 0 = 0 := Rat.add_zero 0
  rw [hz]
  have hmz : (2 : Rat) * 0 = 0 := Rat.mul_zero 2
  rw [hmz]
  have hz_add : (0 : Rat) + A.d = A.d := Rat.zero_add A.d
  rw [hz_add]
  have ha1 : A.d + 0 = A.d := Rat.add_zero A.d
  exact ha1

theorem state_representation_unique2 (rho sigma : Herm2)
    (h_D0 : tr_prod2 rho D0_2 = tr_prod2 sigma D0_2)
    (h_D1 : tr_prod2 rho D1_2 = tr_prod2 sigma D1_2)
    (h_re : rho.b_re = sigma.b_re)
    (h_im : rho.b_im = sigma.b_im) :
    rho = sigma := by
  rw [tr_prod2_D0] at h_D0
  rw [tr_prod2_D0] at h_D0
  rw [tr_prod2_D1] at h_D1
  rw [tr_prod2_D1] at h_D1
  cases rho
  cases sigma
  dsimp at h_D0 h_D1 h_re h_im
  rw [h_D0, h_D1, h_re, h_im]

theorem four_tomographic_probes_are_effects :
    is_effect2 D0_2 ∧ is_effect2 D1_2 ∧
    is_effect2 P_plus_2 ∧ is_effect2 P_R_2 := by
  dsimp [is_effect2, is_pos2, sub2, id2, D0_2, D1_2, P_plus_2, P_R_2, half]
  grind

theorem four_effect_readouts_determine_hermitian2 (rho sigma : Herm2)
    (h0 : tr_prod2 rho D0_2 = tr_prod2 sigma D0_2)
    (h1 : tr_prod2 rho D1_2 = tr_prod2 sigma D1_2)
    (hplus : tr_prod2 rho P_plus_2 = tr_prod2 sigma P_plus_2)
    (hphase : tr_prod2 rho P_R_2 = tr_prod2 sigma P_R_2) : rho = sigma := by
  apply state_representation_unique2 rho sigma h0 h1
  all_goals
    dsimp [tr_prod2, D0_2, D1_2, P_plus_2, P_R_2, half] at h0 h1 hplus hphase
    grind

theorem recover_rho2_matches_four_effects (f : EffectFrameFunction2) :
    tr_prod2 (recover_rho2 f) D0_2 = f.eval D0_2 ∧
    tr_prod2 (recover_rho2 f) D1_2 = f.eval D1_2 ∧
    tr_prod2 (recover_rho2 f) P_plus_2 = f.eval P_plus_2 ∧
    tr_prod2 (recover_rho2 f) P_R_2 = f.eval P_R_2 := by
  have ht := recover_rho2_unit_trace f
    (by dsimp [is_pos2, D0_2]; grind) (by dsimp [is_pos2, D1_2]; grind)
    (by dsimp [is_pos2, sub2, add2, id2, D0_2, D1_2]; grind)
  dsimp [tr2, recover_rho2] at ht
  dsimp [tr_prod2, recover_rho2, D0_2, D1_2, P_plus_2, P_R_2, half] at ht ⊢
  grind

theorem D_sum_eq_id3 : add3 (add3 D0_3 D1_3) D2_3 = id3 := by
  dsimp [add3, D0_3, D1_3, D2_3, id3]
  repeat rw [Rat.add_zero]
  repeat rw [Rat.zero_add]

def recover_rho3 (f : EffectFrameFunction3)
    (s01_re s01_im s02_re s02_im s12_re s12_im : Rat) : Herm3 :=
  ⟨f.eval D0_3, f.eval D1_3, f.eval D2_3,
   s01_re, s01_im, s02_re, s02_im, s12_re, s12_im⟩

theorem recover_rho3_unit_trace (f : EffectFrameFunction3)
    (s01_re s01_im s02_re s02_im s12_re s12_im : Rat)
    (h_pos_D0 : is_pos3 D0_3)
    (h_pos_D1 : is_pos3 D1_3)
    (h_pos_D2 : is_pos3 D2_3)
    (h_pos_01 : is_pos3 (add3 D0_3 D1_3))
    (h_ortho_01 : is_pos3 (sub3 id3 (add3 D0_3 D1_3)))
    (h_ortho_all : is_pos3 (sub3 id3 (add3 (add3 D0_3 D1_3) D2_3))) :
    tr3 (recover_rho3 f s01_re s01_im s02_re s02_im s12_re s12_im) = 1 := by
  dsimp [tr3, recover_rho3]
  have h_add1 := f.h_add D0_3 D1_3 h_pos_D0 h_pos_D1 h_ortho_01
  have h_add2 := f.h_add (add3 D0_3 D1_3) D2_3 h_pos_01 h_pos_D2 h_ortho_all
  have h_id : add3 (add3 D0_3 D1_3) D2_3 = id3 := D_sum_eq_id3
  rw [h_id] at h_add2
  rw [f.h_norm] at h_add2
  rw [h_add1] at h_add2
  exact h_add2.symm

theorem tr_prod3_D0 (A : Herm3) : tr_prod3 A D0_3 = A.a00 := by
  unfold tr_prod3 D0_3
  have h1 : A.a11 * 0 = 0 := Rat.mul_zero A.a11
  have h2 : A.a22 * 0 = 0 := Rat.mul_zero A.a22
  have h3 : A.a01_re * 0 = 0 := Rat.mul_zero A.a01_re
  have h4 : A.a01_im * 0 = 0 := Rat.mul_zero A.a01_im
  have h5 : A.a02_re * 0 = 0 := Rat.mul_zero A.a02_re
  have h6 : A.a02_im * 0 = 0 := Rat.mul_zero A.a02_im
  have h7 : A.a12_re * 0 = 0 := Rat.mul_zero A.a12_re
  have h8 : A.a12_im * 0 = 0 := Rat.mul_zero A.a12_im
  have h0 : A.a00 * 1 = A.a00 := Rat.mul_one A.a00
  rw [h1, h2, h3, h4, h5, h6, h7, h8, h0]
  rw [rat_zero_add_six]
  have hmz : (2 : Rat) * 0 = 0 := Rat.mul_zero 2
  rw [hmz]
  have ha1 : A.a00 + 0 + 0 + 0 = A.a00 := by
    rw [Rat.add_zero, Rat.add_zero, Rat.add_zero]
  exact ha1

theorem tr_prod3_D1 (A : Herm3) : tr_prod3 A D1_3 = A.a11 := by
  unfold tr_prod3 D1_3
  have h1 : A.a00 * 0 = 0 := Rat.mul_zero A.a00
  have h2 : A.a22 * 0 = 0 := Rat.mul_zero A.a22
  have h3 : A.a01_re * 0 = 0 := Rat.mul_zero A.a01_re
  have h4 : A.a01_im * 0 = 0 := Rat.mul_zero A.a01_im
  have h5 : A.a02_re * 0 = 0 := Rat.mul_zero A.a02_re
  have h6 : A.a02_im * 0 = 0 := Rat.mul_zero A.a02_im
  have h7 : A.a12_re * 0 = 0 := Rat.mul_zero A.a12_re
  have h8 : A.a12_im * 0 = 0 := Rat.mul_zero A.a12_im
  have h0 : A.a11 * 1 = A.a11 := Rat.mul_one A.a11
  rw [h1, h2, h3, h4, h5, h6, h7, h8, h0]
  rw [rat_zero_add_six]
  have hmz : (2 : Rat) * 0 = 0 := Rat.mul_zero 2
  rw [hmz]
  have ha1 : (0 : Rat) + A.a11 + 0 + 0 = A.a11 := by
    rw [Rat.zero_add, Rat.add_zero, Rat.add_zero]
  exact ha1

theorem tr_prod3_D2 (A : Herm3) : tr_prod3 A D2_3 = A.a22 := by
  unfold tr_prod3 D2_3
  have h1 : A.a00 * 0 = 0 := Rat.mul_zero A.a00
  have h2 : A.a11 * 0 = 0 := Rat.mul_zero A.a11
  have h3 : A.a01_re * 0 = 0 := Rat.mul_zero A.a01_re
  have h4 : A.a01_im * 0 = 0 := Rat.mul_zero A.a01_im
  have h5 : A.a02_re * 0 = 0 := Rat.mul_zero A.a02_re
  have h6 : A.a02_im * 0 = 0 := Rat.mul_zero A.a02_im
  have h7 : A.a12_re * 0 = 0 := Rat.mul_zero A.a12_re
  have h8 : A.a12_im * 0 = 0 := Rat.mul_zero A.a12_im
  have h0 : A.a22 * 1 = A.a22 := Rat.mul_one A.a22
  rw [h1, h2, h3, h4, h5, h6, h7, h8, h0]
  rw [rat_zero_add_six]
  have hmz : (2 : Rat) * 0 = 0 := Rat.mul_zero 2
  rw [hmz]
  have ha1 : (0 : Rat) + 0 + A.a22 + 0 = A.a22 := by
    rw [Rat.zero_add, Rat.zero_add, Rat.add_zero]
  exact ha1

theorem state_representation_unique3 (rho sigma : Herm3)
    (h_D0 : tr_prod3 rho D0_3 = tr_prod3 sigma D0_3)
    (h_D1 : tr_prod3 rho D1_3 = tr_prod3 sigma D1_3)
    (h_D2 : tr_prod3 rho D2_3 = tr_prod3 sigma D2_3)
    (h01_re : rho.a01_re = sigma.a01_re) (h01_im : rho.a01_im = sigma.a01_im)
    (h02_re : rho.a02_re = sigma.a02_re) (h02_im : rho.a02_im = sigma.a02_im)
    (h12_re : rho.a12_re = sigma.a12_re) (h12_im : rho.a12_im = sigma.a12_im) :
    rho = sigma := by
  rw [tr_prod3_D0] at h_D0
  rw [tr_prod3_D0] at h_D0
  rw [tr_prod3_D1] at h_D1
  rw [tr_prod3_D1] at h_D1
  rw [tr_prod3_D2] at h_D2
  rw [tr_prod3_D2] at h_D2
  cases rho
  cases sigma
  dsimp at h_D0 h_D1 h_D2 h01_re h01_im h02_re h02_im h12_re h12_im
  rw [h_D0, h_D1, h_D2, h01_re, h01_im, h02_re, h02_im, h12_re, h12_im]


theorem d2_binary_valuation_non_extension
    (f_eval_D0 f_eval_D1 f_eval_P_plus : Rat)
    (h_rho_rep : f_eval_P_plus = half * f_eval_D0 + half * f_eval_D1)
    (h_v_D0 : f_eval_D0 = 1)
    (h_v_D1 : f_eval_D1 = 0)
    (h_v_P : f_eval_P_plus = 0) :
    False := by
  rw [h_v_D0, h_v_D1] at h_rho_rep
  have h_d1_zero : half * (0 : Rat) = 0 := Rat.mul_zero half
  have h_d0_one : half * (1 : Rat) = half := Rat.mul_one half
  rw [h_d1_zero, h_d0_one, Rat.add_zero] at h_rho_rep
  have h_contra : half = (0 : Rat) := by
    rw [← h_rho_rep, h_v_P]
  exact half_ne_zero h_contra


#print axioms two_mul_half
#print axioms half_mul_two
#print axioms half_ne_zero
#print axioms rat_add_le_add
#print axioms rat_le_add_of_nonneg_right
#print axioms rat_add_sub_cancel_alt
#print axioms rat_zero_add_six
#print axioms herm2_basis_expansion
#print axioms herm3_basis_expansion
#print axioms lower_minors_can_admit_a_false_effect
#print axioms negative_minor_control_determinant
#print axioms negative_minor_control_not_effect
#print axioms phase_rank_one_control_is_effect
#print axioms zero_and_identity_are_effects3
#print axioms herm2_add_sub_cancel
#print axioms monotonicity2
#print axioms herm3_add_sub_cancel
#print axioms monotonicity3
#print axioms nat_smul2_eval
#print axioms rational_homogeneity2
#print axioms density_squeeze_bracket
#print axioms density_squeeze_forces_equality
#print axioms D0_add_D1_eq_id2
#print axioms recover_rho2_unit_trace
#print axioms tr_prod2_D0
#print axioms tr_prod2_D1
#print axioms state_representation_unique2
#print axioms four_tomographic_probes_are_effects
#print axioms four_effect_readouts_determine_hermitian2
#print axioms recover_rho2_matches_four_effects
#print axioms D_sum_eq_id3
#print axioms recover_rho3_unit_trace
#print axioms tr_prod3_D0
#print axioms tr_prod3_D1
#print axioms tr_prod3_D2
#print axioms state_representation_unique3
#print axioms d2_binary_valuation_non_extension

end HilbertWalk.EffectFrameBusch

private def l5aProvenance : String :=
  "Origin: lean4/EffectFrameBusch.lean Claim: two_ne_zero AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
