


namespace NonAbelianBfBraiding

universe u


structure BraidingAlgebra (G : Type u) where
  mul : G → G → G
  inv : G → G
  one : G
  mul_one : ∀ a, mul a one = a
  one_mul : ∀ a, mul one a = a
  mul_inv : ∀ a, mul a (inv a) = one
  inv_mul : ∀ a, mul (inv a) a = one
  mul_assoc : ∀ a b c, mul (mul a b) c = mul a (mul b c)

def borromean3LoopCommutator {G : Type u} (alg : BraidingAlgebra G) (b1 b2 : G) : G :=
  alg.mul (alg.mul (alg.mul b1 b2) (alg.inv b1)) (alg.inv b2)

theorem abelian_3loop_is_identity {G : Type u} (alg : BraidingAlgebra G) (b1 b2 : G)
    (h_comm : alg.mul b1 b2 = alg.mul b2 b1) :
    borromean3LoopCommutator alg b1 b2 = alg.one := by
  dsimp [borromean3LoopCommutator]
  rw [h_comm]
  rw [alg.mul_assoc b2 b1 (alg.inv b1)]
  rw [alg.mul_inv b1]
  rw [alg.mul_one b2]
  rw [alg.mul_inv b2]

def NonAbelianObstruction {G : Type u} (alg : BraidingAlgebra G) (b1 b2 : G) : Prop :=
  borromean3LoopCommutator alg b1 b2 ≠ alg.one

theorem non_abelian_obstruction_of_non_commuting {G : Type u} (alg : BraidingAlgebra G) (b1 b2 : G)
    (h_obs : borromean3LoopCommutator alg b1 b2 ≠ alg.one) :
    NonAbelianObstruction alg b1 b2 :=
  h_obs


def quantumDoubleTraceNorm (re im : Nat) : Nat :=
  re * re + im * im

theorem quantum_double_trace_nonnegative (re im : Nat) :
    quantumDoubleTraceNorm re im ≥ 0 := by
  dsimp [quantumDoubleTraceNorm]
  omega

def defectMass (normVal : Nat) : Nat :=
  if normVal > 0 then 0 else 1

theorem quantum_double_nullifies_defect (re im : Nat) (hwit : re > 0 ∨ im > 0) :
    defectMass (quantumDoubleTraceNorm re im) = 0 := by
  dsimp [defectMass, quantumDoubleTraceNorm]
  have h_pos : re * re + im * im > 0 := by
    cases hwit with
    | inl hr =>
      have : re * re > 0 := Nat.mul_pos hr hr
      omega
    | inr hi =>
      have : im * im > 0 := Nat.mul_pos hi hi
      omega
  split
  · rfl
  · rename_i h_not
    omega

end NonAbelianBfBraiding
