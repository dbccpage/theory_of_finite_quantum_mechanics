

import CausalOrder
import NoSignalling

namespace CommutingObservables

open CausalOrder
open NoSignalling

def comm4 (A B : Matrix4) : Matrix4 :=
  fun x y => mul4 A B x y - mul4 B A x y

def isCommuting4 (A B : Matrix4) : Prop :=
  ∀ x y, comm4 A B x y = 0

theorem comm4_skew (A B : Matrix4) (x y : Coord2 × Coord2) :
    comm4 B A x y = - comm4 A B x y := by
  dsimp [comm4]
  omega

def isScalar4 (A : Matrix4) : Prop :=
  ∃ c : Int, ∀ x y, A x y = if x = y then c else 0

def id4 : Matrix4 := fun x y => if x = y then 1 else 0

def isScalar2 (A : Matrix2) : Prop :=
  ∃ c : Int, ∀ i j, A i j = if i = j then c else 0

def isSymmetric2 (A : Matrix2) : Prop :=
  ∀ i j, A i j = A j i

def comm2 (A B : Matrix2) : Matrix2 :=
  fun i j => mul2 A B i j - mul2 B A i j

def isCommuting2 (A B : Matrix2) : Prop :=
  ∀ i j, comm2 A B i j = 0

inductive FactorChoice where
  | factor1
  | factor2
  deriving DecidableEq

def embedFactor1 (A : Matrix2) : Matrix4 :=
  tensorComp A id2

def embedFactor2 (B : Matrix2) : Matrix4 :=
  tensorComp id2 B

theorem factor_commutation (A B : Matrix2) (x y : Coord2 × Coord2) :
    comm4 (embedFactor1 A) (embedFactor2 B) x y = 0 := by
  rcases x with ⟨i1, j1⟩
  rcases y with ⟨i2, j2⟩
  cases i1 <;> cases j1 <;> cases i2 <;> cases j2 <;>
  · dsimp [comm4, embedFactor1, embedFactor2, mul4, tensorComp, id2]
    simp only [Int.mul_one, Int.one_mul, Int.mul_zero, Int.zero_mul, Int.add_zero, Int.zero_add]
    rw [Int.mul_comm (A _ _) (B _ _)]
    omega

theorem factor_commutation_all (A B : Matrix2) :
    isCommuting4 (embedFactor1 A) (embedFactor2 B) := by
  intro x y
  exact factor_commutation A B x y

theorem factor_commutation_rev (A B : Matrix2) (x y : Coord2 × Coord2) :
    comm4 (embedFactor2 B) (embedFactor1 A) x y = 0 := by
  rw [comm4_skew]
  have h := factor_commutation A B x y
  rw [h]
  rfl

def embedFactor : FactorChoice → Matrix2 → Matrix4
  | .factor1, A => embedFactor1 A
  | .factor2, A => embedFactor2 A


theorem id4_eq_tensor : id4 = tensorComp id2 id2 := by
  funext x y
  rcases x with ⟨i1, j1⟩
  rcases y with ⟨i2, j2⟩
  cases i1 <;> cases j1 <;> cases i2 <;> cases j2 <;>
    dsimp [id4, tensorComp, id2] <;> decide

def MasaWitness2 (A B : Matrix2) : Prop :=
  ∃ γ α β : Int, γ ≠ 0 ∧ ∀ i j, γ * B i j = α * id2 i j + β * A i j

def sameMasa2 (A B : Matrix2) : Prop := MasaWitness2 A B ∧ MasaWitness2 B A

def MasaWitness4 (M N : Matrix4) : Prop :=
  ∃ γ α β : Int, γ ≠ 0 ∧ ∀ x y, γ * N x y = α * id4 x y + β * M x y

def sameMasa4 (M N : Matrix4) : Prop := MasaWitness4 M N ∧ MasaWitness4 N M

theorem sameMasa4_symm {M N : Matrix4} (h : sameMasa4 M N) : sameMasa4 N M :=
  ⟨h.2, h.1⟩

theorem scalar2_of_offdiag_zero_diag_eq
    (A : Matrix2) (hsym : isSymmetric2 A)
    (hb : A .zero .one = 0) (hd : A .zero .zero = A .one .one) :
    isScalar2 A := by
  refine ⟨A .zero .zero, ?_⟩
  intro i j
  cases i <;> cases j <;> simp [hb, hd]
  · exact (hsym .one .zero).trans hb

theorem symm_comm_equation (A B : Matrix2) (h : isCommuting2 A B) :
    A .zero .zero * B .zero .one + A .zero .one * B .one .one
      = B .zero .zero * A .zero .one + B .zero .one * A .one .one := by
  have h01 := h .zero .one
  dsimp [comm2, mul2] at h01
  omega


theorem masa_of_commuting_symmetric
    (A B : Matrix2) (hA : isSymmetric2 A) (hB : isSymmetric2 B)
    (hAns : ¬ isScalar2 A) (hcomm : isCommuting2 A B) :
    ∃ γ α β : Int, γ ≠ 0 ∧ ∀ i j, γ * B i j = α * id2 i j + β * A i j := by
  have heq := symm_comm_equation A B hcomm
  have hA10 : A .one .zero = A .zero .one := hA .one .zero
  have hB10 : B .one .zero = B .zero .one := hB .one .zero
  by_cases hb0 : A .zero .one = 0
  ·
    have hd : A .zero .zero ≠ A .one .one := fun heqd =>
      hAns (scalar2_of_offdiag_zero_diag_eq A hA hb0 heqd)
    rw [hb0] at heq
    simp only [Int.zero_mul, Int.mul_zero, Int.add_zero, Int.zero_add] at heq
    have hq : B .zero .one = 0 := by
      have hkey : B .zero .one * (A .zero .zero - A .one .one) = 0 := by
        rw [Int.mul_sub]
        have hc : A .zero .zero * B .zero .one
            = B .zero .one * A .zero .zero := Int.mul_comm _ _
        omega
      rcases Int.mul_eq_zero.mp hkey with h | h
      · exact h
      · exact absurd (by omega : A .zero .zero = A .one .one) hd
    refine ⟨A .zero .zero - A .one .one,
            (A .zero .zero - A .one .one) * B .zero .zero
              - (B .zero .zero - B .one .one) * A .zero .zero,
            B .zero .zero - B .one .one, by omega, ?_⟩
    intro i j
    cases i <;> cases j
    · dsimp [id2]; omega
    · dsimp [id2]; rw [hq, hb0]; simp
    · dsimp [id2]; rw [hA10, hB10, hq, hb0]; simp
    · dsimp [id2]
      simp only [Int.sub_mul]
      have m1 : B .zero .zero * A .zero .zero
          = A .zero .zero * B .zero .zero := Int.mul_comm _ _
      have m2 : B .one .one * A .zero .zero
          = A .zero .zero * B .one .one := Int.mul_comm _ _
      have m3 : B .zero .zero * A .one .one
          = A .one .one * B .zero .zero := Int.mul_comm _ _
      have m4 : B .one .one * A .one .one
          = A .one .one * B .one .one := Int.mul_comm _ _
      omega
  ·
    refine ⟨A .zero .one,
            A .zero .one * B .zero .zero - B .zero .one * A .zero .zero,
            B .zero .one, hb0, ?_⟩
    have c1 : A .zero .one * B .zero .one
        = B .zero .one * A .zero .one := Int.mul_comm _ _
    have c2 : B .zero .zero * A .zero .one
        = A .zero .one * B .zero .zero := Int.mul_comm _ _
    have c3 : A .zero .zero * B .zero .one
        = B .zero .one * A .zero .zero := Int.mul_comm _ _
    intro i j
    cases i <;> cases j
    · dsimp [id2]; omega
    · dsimp [id2]; omega
    · dsimp [id2]; rw [hA10, hB10]; omega
    · dsimp [id2]; omega

theorem beta_ne_zero_of_not_scalar
    (A B : Matrix2) (γ α β : Int) (hγ : γ ≠ 0)
    (h : ∀ i j, γ * B i j = α * id2 i j + β * A i j)
    (hBns : ¬ isScalar2 B) : β ≠ 0 := by
  intro hβ
  refine hBns ⟨B .zero .zero, ?_⟩
  have e00 := h .zero .zero
  have e01 := h .zero .one
  have e10 := h .one .zero
  have e11 := h .one .one
  rw [hβ] at e00 e01 e10 e11
  simp only [Int.zero_mul, Int.add_zero] at e00 e01 e10 e11
  dsimp [id2] at e00 e01 e10 e11
  intro i j
  cases i <;> cases j <;> simp
  · exact Int.eq_of_mul_eq_mul_left hγ (by omega)
  · exact Int.eq_of_mul_eq_mul_left hγ (by omega)
  · exact Int.eq_of_mul_eq_mul_left hγ (by omega)

theorem sameMasa2_of_commuting_symmetric
    (A B : Matrix2) (hA : isSymmetric2 A) (hB : isSymmetric2 B)
    (hAns : ¬ isScalar2 A) (hBns : ¬ isScalar2 B) (hcomm : isCommuting2 A B) :
    sameMasa2 A B := by
  obtain ⟨γ, α, β, hγ, h⟩ := masa_of_commuting_symmetric A B hA hB hAns hcomm
  refine ⟨⟨γ, α, β, hγ, h⟩, ⟨β, -α, γ, ?_, ?_⟩⟩
  · exact beta_ne_zero_of_not_scalar A B γ α β hγ h hBns
  · intro i j
    have hij := h i j
    simp only [Int.neg_mul]
    omega


theorem comm4_embed1 (A B : Matrix2) (i1 j1 i2 j2 : Coord2) :
    comm4 (embedFactor1 A) (embedFactor1 B) (i1, j1) (i2, j2)
      = comm2 A B i1 i2 * id2 j1 j2 := by
  cases i1 <;> cases j1 <;> cases i2 <;> cases j2 <;>
    dsimp [comm4, comm2, mul4, mul2, embedFactor1, tensorComp, id2] <;>
    simp only [Int.mul_one, Int.one_mul, Int.mul_zero, Int.zero_mul, Int.add_zero, Int.zero_add, Int.sub_zero, Int.zero_sub] <;> omega

theorem comm4_embed2 (A B : Matrix2) (i1 j1 i2 j2 : Coord2) :
    comm4 (embedFactor2 A) (embedFactor2 B) (i1, j1) (i2, j2)
      = id2 i1 i2 * comm2 A B j1 j2 := by
  cases i1 <;> cases j1 <;> cases i2 <;> cases j2 <;>
    dsimp [comm4, comm2, mul4, mul2, embedFactor2, tensorComp, id2] <;>
    simp only [Int.mul_one, Int.one_mul, Int.mul_zero, Int.zero_mul, Int.add_zero, Int.zero_add, Int.sub_zero, Int.zero_sub] <;> omega

theorem isCommuting2_of_embed1 (A B : Matrix2)
    (h : isCommuting4 (embedFactor1 A) (embedFactor1 B)) : isCommuting2 A B := by
  intro i k
  have hik := h (i, .zero) (k, .zero)
  rw [comm4_embed1] at hik
  dsimp [id2] at hik
  omega

theorem isCommuting2_of_embed2 (A B : Matrix2)
    (h : isCommuting4 (embedFactor2 A) (embedFactor2 B)) : isCommuting2 A B := by
  intro i k
  have hik := h (.zero, i) (.zero, k)
  rw [comm4_embed2] at hik
  dsimp [id2] at hik
  omega

theorem isScalar4_of_isScalar2_f1 (A : Matrix2) (h : isScalar2 A) :
    isScalar4 (embedFactor1 A) := by
  obtain ⟨c, hc⟩ := h
  refine ⟨c, ?_⟩
  intro x y
  rcases x with ⟨i1, j1⟩
  rcases y with ⟨i2, j2⟩
  dsimp [embedFactor1, tensorComp, id2]
  rw [hc]
  cases i1 <;> cases j1 <;> cases i2 <;> cases j2 <;> simp

theorem isScalar4_of_isScalar2_f2 (A : Matrix2) (h : isScalar2 A) :
    isScalar4 (embedFactor2 A) := by
  obtain ⟨c, hc⟩ := h
  refine ⟨c, ?_⟩
  intro x y
  rcases x with ⟨i1, j1⟩
  rcases y with ⟨i2, j2⟩
  dsimp [embedFactor2, tensorComp, id2]
  rw [hc]
  cases i1 <;> cases j1 <;> cases i2 <;> cases j2 <;> simp

theorem masaWitness4_of_2_f1 (A B : Matrix2) (h : MasaWitness2 A B) :
    MasaWitness4 (embedFactor1 A) (embedFactor1 B) := by
  obtain ⟨γ, α, β, hγ, hab⟩ := h
  refine ⟨γ, α, β, hγ, ?_⟩
  intro x y
  rcases x with ⟨i1, j1⟩
  rcases y with ⟨i2, j2⟩
  have hij := hab i1 i2
  cases i1 <;> cases j1 <;> cases i2 <;> cases j2 <;>
    dsimp [embedFactor1, tensorComp, id4, id2] at * <;>
    simp only [Int.mul_one, Int.one_mul, Int.mul_zero, Int.zero_mul, Int.add_zero, Int.zero_add] at * <;> omega

theorem masaWitness4_of_2_f2 (A B : Matrix2) (h : MasaWitness2 A B) :
    MasaWitness4 (embedFactor2 A) (embedFactor2 B) := by
  obtain ⟨γ, α, β, hγ, hab⟩ := h
  refine ⟨γ, α, β, hγ, ?_⟩
  intro x y
  rcases x with ⟨i1, j1⟩
  rcases y with ⟨i2, j2⟩
  have hij := hab j1 j2
  cases i1 <;> cases j1 <;> cases i2 <;> cases j2 <;>
    dsimp [embedFactor2, tensorComp, id4, id2] at * <;>
    simp only [Int.mul_one, Int.one_mul, Int.mul_zero, Int.zero_mul, Int.add_zero, Int.zero_add] at * <;> omega

theorem sameMasa4_of_2_f1 (A B : Matrix2) (h : sameMasa2 A B) :
    sameMasa4 (embedFactor1 A) (embedFactor1 B) :=
  ⟨masaWitness4_of_2_f1 A B h.1, masaWitness4_of_2_f1 B A h.2⟩

theorem sameMasa4_of_2_f2 (A B : Matrix2) (h : sameMasa2 A B) :
    sameMasa4 (embedFactor2 A) (embedFactor2 B) :=
  ⟨masaWitness4_of_2_f2 A B h.1, masaWitness4_of_2_f2 B A h.2⟩



structure ObservableAssignment (n : Nat) where
  obs : Fin n → Matrix4
  factor : Fin n → FactorChoice
  local2 : Fin n → Matrix2
  sym : ∀ x, isSymmetric2 (local2 x)
  localized : ∀ x, obs x = embedFactor (factor x) (local2 x)

def satisfiesMicrocausality {n : Nat} (P : FiniteStrictPoset n) (assign : ObservableAssignment n) : Prop :=
  ∀ x y : Fin n, isSpacelike P x y → isCommuting4 (assign.obs x) (assign.obs y)


def isNonDegenerate {n : Nat} (P : FiniteStrictPoset n) (assign : ObservableAssignment n) : Prop :=
  (∀ x : Fin n, ¬ isScalar4 (assign.obs x)) ∧
  (∀ x y : Fin n, isSpacelike P x y → ¬ sameMasa4 (assign.obs x) (assign.obs y))

def pauliX : Matrix2 :=
  fun i j => if i ≠ j then 1 else 0

def pauliZ : Matrix2 :=
  fun i j => if i = j then (if i = .zero then 1 else -1) else 0

theorem pauliX_symm : isSymmetric2 pauliX := by
  intro i j; cases i <;> cases j <;> rfl

theorem pauliZ_symm : isSymmetric2 pauliZ := by
  intro i j; cases i <;> cases j <;> rfl

theorem not_sameMasa_z1_z2 :
    ¬ sameMasa4 (embedFactor1 pauliZ) (embedFactor2 pauliZ) := by
  intro h
  obtain ⟨⟨γ, α, β, hγ, hw⟩, _⟩ := h
  have e1 := hw (.zero, .zero) (.zero, .zero)
  have e2 := hw (.zero, .one) (.zero, .one)
  dsimp [embedFactor1, embedFactor2, tensorComp, id4, id2, pauliZ] at e1 e2
  omega


def c1_obs (x : Fin 3) : Matrix4 :=
  match x.val with
  | 0 => embedFactor1 pauliX
  | 1 => embedFactor1 pauliZ
  | _ => embedFactor2 pauliZ

def c1_factor (x : Fin 3) : FactorChoice :=
  match x.val with
  | 0 => FactorChoice.factor1
  | 1 => FactorChoice.factor1
  | _ => FactorChoice.factor2

def c1_local2 (x : Fin 3) : Matrix2 :=
  match x.val with
  | 0 => pauliX
  | 1 => pauliZ
  | _ => pauliZ

theorem c1_local2_symm : ∀ x : Fin 3, isSymmetric2 (c1_local2 x)
  | ⟨0, _⟩ => pauliX_symm
  | ⟨1, _⟩ => pauliZ_symm
  | ⟨2, _⟩ => pauliZ_symm

theorem c1_localized :
    ∀ x : Fin 3, c1_obs x = embedFactor (c1_factor x) (c1_local2 x)
  | ⟨0, _⟩ => rfl
  | ⟨1, _⟩ => rfl
  | ⟨2, _⟩ => rfl

def c1_assignment : ObservableAssignment 3 where
  obs := c1_obs
  factor := c1_factor
  local2 := c1_local2
  sym := c1_local2_symm
  localized := c1_localized

theorem c1_microcausality : satisfiesMicrocausality C1 c1_assignment := by
  intro x y hsp
  have h_cases : (x.val = 1 ∧ y.val = 2) ∨ (x.val = 2 ∧ y.val = 1) := by
    rcases x with ⟨xv, hx⟩
    rcases y with ⟨yv, hy⟩
    revert xv hx yv hy hsp
    decide
  rcases h_cases with ⟨hx, hy⟩ | ⟨hx, hy⟩
  · intro u v
    have hx_fin : x = ⟨1, by decide⟩ := by ext; exact hx
    have hy_fin : y = ⟨2, by decide⟩ := by ext; exact hy
    rw [hx_fin, hy_fin]
    dsimp [c1_assignment, c1_obs]
    exact factor_commutation pauliZ pauliZ u v
  · intro u v
    have hx_fin : x = ⟨2, by decide⟩ := by ext; exact hx
    have hy_fin : y = ⟨1, by decide⟩ := by ext; exact hy
    rw [hx_fin, hy_fin]
    dsimp [c1_assignment, c1_obs]
    exact factor_commutation_rev pauliZ pauliZ u v

theorem not_scalar_embed_pauliX : ¬ isScalar4 (embedFactor1 pauliX) := by
  intro ⟨c, hc⟩
  have h00 := hc (.zero, .zero) (.zero, .zero)
  have h01 := hc (.zero, .zero) (.one, .zero)
  dsimp [embedFactor1, tensorComp, id2, pauliX] at h00 h01
  omega

theorem not_scalar_embed_pauliZ_f1 : ¬ isScalar4 (embedFactor1 pauliZ) := by
  intro ⟨c, hc⟩
  have h00 := hc (.zero, .zero) (.zero, .zero)
  have h11 := hc (.one, .zero) (.one, .zero)
  dsimp [embedFactor1, tensorComp, id2, pauliZ] at h00 h11
  omega

theorem not_scalar_embed_pauliZ_f2 : ¬ isScalar4 (embedFactor2 pauliZ) := by
  intro ⟨c, hc⟩
  have h00 := hc (.zero, .zero) (.zero, .zero)
  have h01 := hc (.zero, .one) (.zero, .one)
  dsimp [embedFactor2, tensorComp, id2, pauliZ] at h00 h01
  omega

theorem c1_non_degenerate : isNonDegenerate C1 c1_assignment := by
  constructor
  · intro ⟨xv, hx⟩
    match xv with
    | 0 => exact not_scalar_embed_pauliX
    | 1 => exact not_scalar_embed_pauliZ_f1
    | 2 => exact not_scalar_embed_pauliZ_f2
    | n + 3 => omega
  · intro x y hsp
    have h_cases : (x.val = 1 ∧ y.val = 2) ∨ (x.val = 2 ∧ y.val = 1) := by
      rcases x with ⟨xv, hx⟩
      rcases y with ⟨yv, hy⟩
      revert xv hx yv hy hsp
      decide
    rcases h_cases with ⟨hx, hy⟩ | ⟨hx, hy⟩
    · have hx_fin : x = ⟨1, by decide⟩ := by ext; exact hx
      have hy_fin : y = ⟨2, by decide⟩ := by ext; exact hy
      rw [hx_fin, hy_fin]
      dsimp [c1_assignment, c1_obs]
      exact not_sameMasa_z1_z2
    · have hx_fin : x = ⟨2, by decide⟩ := by ext; exact hx
      have hy_fin : y = ⟨1, by decide⟩ := by ext; exact hy
      rw [hx_fin, hy_fin]
      dsimp [c1_assignment, c1_obs]
      exact fun hs => not_sameMasa_z1_z2 (sameMasa4_symm hs)

theorem c1_commuting_assignment_exists :
    ∃ a : ObservableAssignment 3, satisfiesMicrocausality C1 a ∧ isNonDegenerate C1 a :=
  ⟨c1_assignment, c1_microcausality, c1_non_degenerate⟩


def c2_obs (x : Fin 4) : Matrix4 :=
  match x.val with
  | 0 => embedFactor1 pauliX
  | 1 => embedFactor1 pauliZ
  | 2 => embedFactor2 pauliZ
  | _ => embedFactor2 pauliX

def c2_factor (x : Fin 4) : FactorChoice :=
  match x.val with
  | 0 => FactorChoice.factor1
  | 1 => FactorChoice.factor1
  | 2 => FactorChoice.factor2
  | _ => FactorChoice.factor2

def c2_local2 (x : Fin 4) : Matrix2 :=
  match x.val with
  | 0 => pauliX
  | 1 => pauliZ
  | 2 => pauliZ
  | _ => pauliX

theorem c2_local2_symm : ∀ x : Fin 4, isSymmetric2 (c2_local2 x)
  | ⟨0, _⟩ => pauliX_symm
  | ⟨1, _⟩ => pauliZ_symm
  | ⟨2, _⟩ => pauliZ_symm
  | ⟨3, _⟩ => pauliX_symm

theorem c2_localized :
    ∀ x : Fin 4, c2_obs x = embedFactor (c2_factor x) (c2_local2 x)
  | ⟨0, _⟩ => rfl
  | ⟨1, _⟩ => rfl
  | ⟨2, _⟩ => rfl
  | ⟨3, _⟩ => rfl

def c2_assignment : ObservableAssignment 4 where
  obs := c2_obs
  factor := c2_factor
  local2 := c2_local2
  sym := c2_local2_symm
  localized := c2_localized

theorem not_scalar_embed_pauliX_f2 : ¬ isScalar4 (embedFactor2 pauliX) := by
  intro ⟨c, hc⟩
  have h00 := hc (.zero, .zero) (.zero, .zero)
  have h01 := hc (.zero, .zero) (.zero, .one)
  dsimp [embedFactor2, tensorComp, id2, pauliX] at h00 h01
  omega

theorem c2_microcausality : satisfiesMicrocausality C2 c2_assignment := by
  intro x y hsp
  have h_cases : (x.val = 1 ∧ y.val = 2) ∨ (x.val = 2 ∧ y.val = 1) := by
    rcases x with ⟨xv, hx⟩
    rcases y with ⟨yv, hy⟩
    revert xv hx yv hy hsp
    decide
  rcases h_cases with ⟨hx, hy⟩ | ⟨hx, hy⟩
  · intro u v
    have hx_fin : x = ⟨1, by decide⟩ := by ext; exact hx
    have hy_fin : y = ⟨2, by decide⟩ := by ext; exact hy
    rw [hx_fin, hy_fin]
    dsimp [c2_assignment, c2_obs]
    exact factor_commutation pauliZ pauliZ u v
  · intro u v
    have hx_fin : x = ⟨2, by decide⟩ := by ext; exact hx
    have hy_fin : y = ⟨1, by decide⟩ := by ext; exact hy
    rw [hx_fin, hy_fin]
    dsimp [c2_assignment, c2_obs]
    exact factor_commutation_rev pauliZ pauliZ u v

theorem c2_non_degenerate : isNonDegenerate C2 c2_assignment := by
  constructor
  · intro ⟨xv, hx⟩
    match xv with
    | 0 => exact not_scalar_embed_pauliX
    | 1 => exact not_scalar_embed_pauliZ_f1
    | 2 => exact not_scalar_embed_pauliZ_f2
    | 3 => exact not_scalar_embed_pauliX_f2
    | n + 4 => omega
  · intro x y hsp
    have h_cases : (x.val = 1 ∧ y.val = 2) ∨ (x.val = 2 ∧ y.val = 1) := by
      rcases x with ⟨xv, hx⟩
      rcases y with ⟨yv, hy⟩
      revert xv hx yv hy hsp
      decide
    rcases h_cases with ⟨hx, hy⟩ | ⟨hx, hy⟩
    · have hx_fin : x = ⟨1, by decide⟩ := by ext; exact hx
      have hy_fin : y = ⟨2, by decide⟩ := by ext; exact hy
      rw [hx_fin, hy_fin]
      dsimp [c2_assignment, c2_obs]
      exact not_sameMasa_z1_z2
    · have hx_fin : x = ⟨2, by decide⟩ := by ext; exact hx
      have hy_fin : y = ⟨1, by decide⟩ := by ext; exact hy
      rw [hx_fin, hy_fin]
      dsimp [c2_assignment, c2_obs]
      exact fun hs => not_sameMasa_z1_z2 (sameMasa4_symm hs)

theorem c2_commuting_assignment_exists :
    ∃ a : ObservableAssignment 4, satisfiesMicrocausality C2 a ∧ isNonDegenerate C2 a :=
  ⟨c2_assignment, c2_microcausality, c2_non_degenerate⟩


def c3_antichain_rel (_ _ : Fin 3) : Prop := False

instance : DecidableRel c3_antichain_rel := fun _ _ => isFalse (by intro h; contradiction)

def C3_antichain : FiniteStrictPoset 3 where
  rel := c3_antichain_rel
  decRel := inferInstance
  irrefl := by intro _ h; contradiction
  trans := by intro _ _ _ h; contradiction

theorem c3_antichain_all_spacelike (x y : Fin 3) (hne : x ≠ y) : isSpacelike C3_antichain x y := by
  dsimp [isSpacelike, C3_antichain, c3_antichain_rel]
  exact ⟨hne, not_false, not_false⟩

theorem pigeonhole_factor (f : Fin 3 → FactorChoice) :
    ∃ x y : Fin 3, x ≠ y ∧ f x = f y := by
  cases h0 : f ⟨0, by decide⟩ <;> cases h1 : f ⟨1, by decide⟩ <;> cases h2 : f ⟨2, by decide⟩
  · exact ⟨⟨0, by decide⟩, ⟨1, by decide⟩, by decide, by rw [h0, h1]⟩
  · exact ⟨⟨0, by decide⟩, ⟨1, by decide⟩, by decide, by rw [h0, h1]⟩
  · exact ⟨⟨0, by decide⟩, ⟨2, by decide⟩, by decide, by rw [h0, h2]⟩
  · exact ⟨⟨1, by decide⟩, ⟨2, by decide⟩, by decide, by rw [h1, h2]⟩
  · exact ⟨⟨1, by decide⟩, ⟨2, by decide⟩, by decide, by rw [h1, h2]⟩
  · exact ⟨⟨0, by decide⟩, ⟨2, by decide⟩, by decide, by rw [h0, h2]⟩
  · exact ⟨⟨0, by decide⟩, ⟨1, by decide⟩, by decide, by rw [h0, h1]⟩
  · exact ⟨⟨0, by decide⟩, ⟨1, by decide⟩, by decide, by rw [h0, h1]⟩



theorem sameMasa4_of_common_factor (f : FactorChoice) (A B : Matrix2)
    (hA : isSymmetric2 A) (hB : isSymmetric2 B)
    (hAns : ¬ isScalar4 (embedFactor f A)) (hBns : ¬ isScalar4 (embedFactor f B))
    (hc : isCommuting4 (embedFactor f A) (embedFactor f B)) :
    sameMasa4 (embedFactor f A) (embedFactor f B) := by
  cases f with
  | factor1 =>
    dsimp [embedFactor] at hAns hBns hc ⊢
    exact sameMasa4_of_2_f1 _ _
      (sameMasa2_of_commuting_symmetric _ _ hA hB
        (fun hs => hAns (isScalar4_of_isScalar2_f1 _ hs))
        (fun hs => hBns (isScalar4_of_isScalar2_f1 _ hs))
        (isCommuting2_of_embed1 _ _ hc))
  | factor2 =>
    dsimp [embedFactor] at hAns hBns hc ⊢
    exact sameMasa4_of_2_f2 _ _
      (sameMasa2_of_commuting_symmetric _ _ hA hB
        (fun hs => hAns (isScalar4_of_isScalar2_f2 _ hs))
        (fun hs => hBns (isScalar4_of_isScalar2_f2 _ hs))
        (isCommuting2_of_embed2 _ _ hc))

theorem c3_antichain_obstructed (a : ObservableAssignment 3) :
    ¬ (satisfiesMicrocausality C3_antichain a ∧ isNonDegenerate C3_antichain a) := by
  intro ⟨hmc, hns, hmasa⟩
  obtain ⟨x, y, hne, h_eq⟩ := pigeonhole_factor a.factor
  have hsp := c3_antichain_all_spacelike x y hne
  have hlx : a.obs x = embedFactor (a.factor y) (a.local2 x) := by
    rw [← h_eq]; exact a.localized x
  have hly : a.obs y = embedFactor (a.factor y) (a.local2 y) := a.localized y
  refine hmasa x y hsp ?_
  rw [hlx, hly]
  exact sameMasa4_of_common_factor (a.factor y) _ _ (a.sym x) (a.sym y)
    (by rw [← hlx]; exact hns x)
    (by rw [← hly]; exact hns y)
    (by rw [← hlx, ← hly]; exact hmc x y hsp)

#print axioms not_sameMasa_z1_z2
#print axioms c1_non_degenerate
#print axioms sameMasa4_of_common_factor


theorem nondegeneracy_is_about_the_matrices
    (a : ObservableAssignment 3) (h : isNonDegenerate C3_antichain a)
    (x y : Fin 3) (hsp : isSpacelike C3_antichain x y) :
    ¬ sameMasa4 (a.obs x) (a.obs y) := h.2 x y hsp

theorem factor_label_is_pinned_to_the_observable
    (a : ObservableAssignment 3) (x : Fin 3) :
    a.obs x = embedFactor (a.factor x) (a.local2 x) := a.localized x

#print axioms masa_of_commuting_symmetric
#print axioms sameMasa2_of_commuting_symmetric
#print axioms nondegeneracy_is_about_the_matrices
#print axioms c3_antichain_obstructed

end CommutingObservables

private def l5aProvenance : String :=
  "Origin: lean4/CommutingObservables.lean Claim: comm4_skew AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
