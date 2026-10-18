/-
  Campaign C1000 Block 02: No-Signalling, Marginal Uniqueness, and Admitted Composition.
  AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e).

  Formalizes:
  - 2x2 and 4x4 matrix representations over Int
  - Admitted tensor composition rule on local observables
  - Trace and partial traces Tr_B, Tr_A
  - Theorem: Marginal identity (local statistics reproduction)
  - Theorem: Uniqueness of partial trace from local statistics reproduction
  - Theorem: No-signalling under admitted composition with composition rule as explicit hypothesis
-/

namespace NoSignalling

inductive Coord2 where
  | zero
  | one
  deriving DecidableEq

abbrev Matrix2 := Coord2 → Coord2 → Int
abbrev Matrix4 := (Coord2 × Coord2) → (Coord2 × Coord2) → Int

def id2 (i j : Coord2) : Int :=
  if i = j then 1 else 0

def elementary2 (r c : Coord2) : Matrix2 :=
  fun i j => if i = r ∧ j = c then 1 else 0

def tensorComp (A B : Matrix2) : Matrix4 :=
  fun ⟨i1, j1⟩ ⟨i2, j2⟩ => A i1 i2 * B j1 j2

def mul2 (A B : Matrix2) : Matrix2 :=
  fun i k => A i .zero * B .zero k + A i .one * B .one k

def tr2 (A : Matrix2) : Int :=
  A .zero .zero + A .one .one

def mul4 (A B : Matrix4) : Matrix4 :=
  fun ⟨i1, j1⟩ ⟨i2, j2⟩ =>
    A (i1, j1) (.zero, .zero) * B (.zero, .zero) (i2, j2) +
    A (i1, j1) (.zero, .one) * B (.zero, .one) (i2, j2) +
    A (i1, j1) (.one, .zero) * B (.one, .zero) (i2, j2) +
    A (i1, j1) (.one, .one) * B (.one, .one) (i2, j2)

def tr4 (A : Matrix4) : Int :=
  A (.zero, .zero) (.zero, .zero) +
  A (.zero, .one) (.zero, .one) +
  A (.one, .zero) (.one, .zero) +
  A (.one, .one) (.one, .one)

def partialTraceB (ρ : Matrix4) : Matrix2 :=
  fun i1 i2 => ρ (i1, .zero) (i2, .zero) + ρ (i1, .one) (i2, .one)

def partialTraceA (ρ : Matrix4) : Matrix2 :=
  fun j1 j2 => ρ (.zero, j1) (.zero, j2) + ρ (.one, j1) (.one, j2)

/-! ### Target C1000-T831 & T843: Marginal Identity -/

/-- Target C1000-T843: The marginal identity:
    Tr[(A ⊗ I) ρ] = Tr[A · Tr_B(ρ)] identically over the finite carrier. -/
theorem marginal_identity (A : Matrix2) (ρ : Matrix4) :
    tr4 (mul4 (tensorComp A id2) ρ) = tr2 (mul2 A (partialTraceB ρ)) := by
  dsimp [tr4, mul4, tensorComp, id2, tr2, mul2, partialTraceB]
  simp only [Int.mul_add, Int.mul_one, Int.mul_zero, Int.zero_mul]
  omega

/-! ### Elementary matrix duality and algebra helpers -/

theorem mul_reorder (u r v : Int) : (u * r) * v = (v * u) * r := by
  rw [Int.mul_comm (u * r) v, ← Int.mul_assoc]

theorem pair_combine (v1 u1 v2 u2 r : Int) :
    (u1 * r) * v1 + (u2 * r) * v2 = (v1 * u1 + v2 * u2) * r := by
  rw [mul_reorder u1 r v1, mul_reorder u2 r v2, ← Int.add_mul]

theorem pair_combine_one (v1 u1 v2 u2 r : Int) (h : v1 * u1 + v2 * u2 = 1) :
    (u1 * r) * v1 + (u2 * r) * v2 = r := by
  rw [pair_combine, h, Int.one_mul]

theorem pair_combine_zero (v1 u1 v2 u2 r : Int) (h : v1 * u1 + v2 * u2 = 0) :
    (u1 * r) * v1 + (u2 * r) * v2 = 0 := by
  rw [pair_combine, h, Int.zero_mul]

theorem sum8_reorder (c d e f g h i j : Int) :
    c + d + (e + f) + (g + h + (i + j)) = (c + g) + (d + h) + (e + i) + (f + j) := by
  omega

theorem elementary_trace_eval (M : Matrix2) (r c : Coord2) :
    tr2 (mul2 (elementary2 c r) M) = M r c := by
  dsimp [tr2, mul2, elementary2]
  cases r <;> cases c <;> (dsimp; omega)

/-! ### Target C1000-T831 & T844: Uniqueness of Partial Trace -/

/-- Target C1000-T844: Prove that the partial trace is the UNIQUE linear map
    satisfying the local statistics identity.
    If M : Matrix4 → Matrix2 satisfies Tr[A · M(ρ)] = Tr[(A ⊗ I) ρ] for all A,
    then M(ρ) = Tr_B(ρ) identically. -/
theorem partial_trace_uniqueness
    (M : Matrix4 → Matrix2)
    (h_local_stats : ∀ (A : Matrix2) (ρ : Matrix4), tr2 (mul2 A (M ρ)) = tr4 (mul4 (tensorComp A id2) ρ))
    (ρ : Matrix4) :
    M ρ = partialTraceB ρ := by
  funext r c
  have hM := elementary_trace_eval (M ρ) r c
  have hPT := elementary_trace_eval (partialTraceB ρ) r c
  rw [← hM]
  rw [h_local_stats (elementary2 c r) ρ]
  rw [marginal_identity (elementary2 c r) ρ]
  exact hPT

/-! ### Target C1000-T832 & T845: No-Signalling with Admitted Composition Hypothesis -/

/-- Property that a bilinear composition rule coincides with the admitted tensor product. -/
def IsAdmittedTensorComp (comp : Matrix2 → Matrix2 → Matrix4) : Prop :=
  ∀ (A B : Matrix2) (i1 j1 i2 j2 : Coord2),
    comp A B (i1, j1) (i2, j2) = A i1 i2 * B j1 j2

/-- Composite state after local operation U on Alice under composition rule comp. -/
def aliceLocalOp (comp : Matrix2 → Matrix2 → Matrix4) (U U_dag : Matrix2) (ρ : Matrix4) : Matrix4 :=
  mul4 (mul4 (comp U id2) ρ) (comp U_dag id2)

/-- Target C1000-T845: Prove no-signalling under admitted composition.
    The composition rule 'comp' and its admitted assumption 'h_comp' appear
    as EXPLICIT HYPOTHESES in the theorem statement type.
    
    Statement: Bob's marginal state Tr_A(ρ') after any local operation on Alice
    is identical to Bob's unperturbed marginal state Tr_A(ρ). -/
theorem no_signalling_under_admitted_composition
    (comp : Matrix2 → Matrix2 → Matrix4)
    (h_comp : IsAdmittedTensorComp comp)
    (U : Matrix2)
    (U_dag : Matrix2)
    (h_unitary : mul2 U_dag U = id2)
    (ρ : Matrix4) :
    partialTraceA (aliceLocalOp comp U U_dag ρ) = partialTraceA ρ := by
  have h_comp_eval : ∀ A B, comp A B = tensorComp A B := by
    intro A B
    funext ⟨i1, j1⟩ ⟨i2, j2⟩
    exact h_comp A B i1 j1 i2 j2
  dsimp [aliceLocalOp]
  rw [h_comp_eval U id2]
  rw [h_comp_eval U_dag id2]
  have hu00 : U_dag .zero .zero * U .zero .zero + U_dag .zero .one * U .one .zero = 1 := by
    have h := congrFun (congrFun h_unitary .zero) .zero
    dsimp [mul2, id2] at h
    exact h
  have hu01 : U_dag .zero .zero * U .zero .one + U_dag .zero .one * U .one .one = 0 := by
    have h := congrFun (congrFun h_unitary .zero) .one
    dsimp [mul2, id2] at h
    exact h
  have hu10 : U_dag .one .zero * U .zero .zero + U_dag .one .one * U .one .zero = 0 := by
    have h := congrFun (congrFun h_unitary .one) .zero
    dsimp [mul2, id2] at h
    exact h
  have hu11 : U_dag .one .zero * U .zero .one + U_dag .one .one * U .one .one = 1 := by
    have h := congrFun (congrFun h_unitary .one) .one
    dsimp [mul2, id2] at h
    exact h
  funext j1 j2
  cases j1 <;> cases j2
  · dsimp [partialTraceA, mul4, tensorComp, id2]
    simp only [Int.mul_zero, Int.zero_mul, Int.add_zero, Int.mul_one, Int.add_mul]
    rw [sum8_reorder]
    rw [pair_combine_one (U_dag .zero .zero) (U .zero .zero) (U_dag .zero .one) (U .one .zero) (ρ (.zero, .zero) (.zero, .zero)) hu00]
    rw [pair_combine_zero (U_dag .zero .zero) (U .zero .one) (U_dag .zero .one) (U .one .one) (ρ (.one, .zero) (.zero, .zero)) hu01]
    rw [pair_combine_zero (U_dag .one .zero) (U .zero .zero) (U_dag .one .one) (U .one .zero) (ρ (.zero, .zero) (.one, .zero)) hu10]
    rw [pair_combine_one (U_dag .one .zero) (U .zero .one) (U_dag .one .one) (U .one .one) (ρ (.one, .zero) (.one, .zero)) hu11]
    omega
  · dsimp [partialTraceA, mul4, tensorComp, id2]
    simp only [Int.mul_zero, Int.zero_mul, Int.add_zero, Int.zero_add, Int.mul_one, Int.add_mul]
    rw [sum8_reorder]
    rw [pair_combine_one (U_dag .zero .zero) (U .zero .zero) (U_dag .zero .one) (U .one .zero) (ρ (.zero, .zero) (.zero, .one)) hu00]
    rw [pair_combine_zero (U_dag .zero .zero) (U .zero .one) (U_dag .zero .one) (U .one .one) (ρ (.one, .zero) (.zero, .one)) hu01]
    rw [pair_combine_zero (U_dag .one .zero) (U .zero .zero) (U_dag .one .one) (U .one .zero) (ρ (.zero, .zero) (.one, .one)) hu10]
    rw [pair_combine_one (U_dag .one .zero) (U .zero .one) (U_dag .one .one) (U .one .one) (ρ (.one, .zero) (.one, .one)) hu11]
    omega
  · dsimp [partialTraceA, mul4, tensorComp, id2]
    simp only [Int.mul_zero, Int.zero_mul, Int.add_zero, Int.zero_add, Int.mul_one, Int.add_mul]
    rw [sum8_reorder]
    rw [pair_combine_one (U_dag .zero .zero) (U .zero .zero) (U_dag .zero .one) (U .one .zero) (ρ (.zero, .one) (.zero, .zero)) hu00]
    rw [pair_combine_zero (U_dag .zero .zero) (U .zero .one) (U_dag .zero .one) (U .one .one) (ρ (.one, .one) (.zero, .zero)) hu01]
    rw [pair_combine_zero (U_dag .one .zero) (U .zero .zero) (U_dag .one .one) (U .one .zero) (ρ (.zero, .one) (.one, .zero)) hu10]
    rw [pair_combine_one (U_dag .one .zero) (U .zero .one) (U_dag .one .one) (U .one .one) (ρ (.one, .one) (.one, .zero)) hu11]
    omega
  · dsimp [partialTraceA, mul4, tensorComp, id2]
    simp only [Int.mul_zero, Int.zero_mul, Int.add_zero, Int.zero_add, Int.mul_one, Int.add_mul]
    rw [sum8_reorder]
    rw [pair_combine_one (U_dag .zero .zero) (U .zero .zero) (U_dag .zero .one) (U .one .zero) (ρ (.zero, .one) (.zero, .one)) hu00]
    rw [pair_combine_zero (U_dag .zero .zero) (U .zero .one) (U_dag .zero .one) (U .one .one) (ρ (.one, .one) (.zero, .one)) hu01]
    rw [pair_combine_zero (U_dag .one .zero) (U .zero .zero) (U_dag .one .one) (U .one .zero) (ρ (.zero, .one) (.one, .one)) hu10]
    rw [pair_combine_one (U_dag .one .zero) (U .zero .one) (U_dag .one .one) (U .one .one) (ρ (.one, .one) (.one, .one)) hu11]
    omega

#print axioms marginal_identity
#print axioms partial_trace_uniqueness
#print axioms no_signalling_under_admitted_composition

end NoSignalling
