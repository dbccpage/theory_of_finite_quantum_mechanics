/-
Exact algebraic model; AuthorityEffect: None.
Modular-addition maps have explicit inverses; finite-set cardinalities multiply; supplied integer CNOT/Bell/partial-transpose models obey the displayed polynomial identities. ZMod 0 is infinite, so the arbitrary-n theorem is algebraic rather than an exclusively finite-carrier theorem. The dimension functions are declared formulas, not constructed state spaces; normalized and unnormalized dimensions must not be conflated. The integer quadratic-form example does not construct two full physical cone theories satisfying all constructor axioms.
Historical names are labels; their physical or operational interpretations require separate evidence.
-/

import Mathlib.Data.Matrix.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Perm
import Mathlib.GroupTheory.Perm.Basic
import Mathlib.Tactic



namespace CampaignCtInformationMediaInteroperability


def cnotClone (n : ℕ) (p : ZMod n × ZMod n) : ZMod n × ZMod n :=
  (p.1, p.1 + p.2)


def cnotUnclone (n : ℕ) (p : ZMod n × ZMod n) : ZMod n × ZMod n :=
  (p.1, p.2 - p.1)


theorem cnotClone_bijective_and_clones_zero (n : ℕ) :
    (∀ p : ZMod n × ZMod n, cnotUnclone n (cnotClone n p) = p) ∧
    (∀ p : ZMod n × ZMod n, cnotClone n (cnotUnclone n p) = p) ∧
    Function.Bijective (cnotClone n) ∧
    (∀ x : ZMod n, cnotClone n (x, 0) = (x, x)) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro ⟨x, y⟩
    simp [cnotClone, cnotUnclone]
  · intro ⟨x, y⟩
    simp [cnotClone, cnotUnclone]
  · rw [Function.bijective_iff_has_inverse]
    exact ⟨cnotUnclone n,
      fun ⟨x, y⟩ => by simp [cnotClone, cnotUnclone],
      fun ⟨x, y⟩ => by simp [cnotClone, cnotUnclone]⟩
  · intro x
    simp [cnotClone]


theorem cnotClone_zmod2_involutive (p : ZMod 2 × ZMod 2) :
    cnotClone 2 (cnotClone 2 p) = p := by
  rcases p with ⟨x, y⟩
  fin_cases x <;> fin_cases y <;> rfl


theorem singleton_not_computation_variable_fence (n : ℕ) :
    (∀ x y : Fin 1, x = y) ∧
    Fintype.card (Equiv.Perm (Fin 1)) = 1 ∧
    ((0 : Fin (n + 2)) ≠ (1 : Fin (n + 2))) ∧
    Equiv.swap (0 : Fin (n + 2)) (1 : Fin (n + 2)) (0 : Fin (n + 2)) = (1 : Fin (n + 2)) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro x y
    exact Subsingleton.elim x y
  · simp
  · simp
  · exact Equiv.swap_apply_left (0 : Fin (n + 2)) (1 : Fin (n + 2))


theorem clonable_computation_implies_distinguishable {X Y : Type*} (n : ℕ)
    (f : X → ZMod n) (g : ZMod n → Y) (x y : X) :
    (Function.Injective f → x ≠ y → cnotClone n (f x, 0) ≠ cnotClone n (f y, 0)) ∧
    (f x = f y → g (f x) = g (f y)) := by
  refine ⟨?_, ?_⟩
  · intro hinj hne hclone
    apply hne
    apply hinj
    have hfst := congrArg Prod.fst hclone
    simpa [cnotClone] using hfst
  · intro hcol
    rw [hcol]


def compositeClone (n₁ n₂ : ℕ)
    (p : (ZMod n₁ × ZMod n₂) × (ZMod n₁ × ZMod n₂)) :
    (ZMod n₁ × ZMod n₂) × (ZMod n₁ × ZMod n₂) :=
  ((p.1.1, p.1.2), (p.1.1 + p.2.1, p.1.2 + p.2.2))


def compositeUnclone (n₁ n₂ : ℕ)
    (p : (ZMod n₁ × ZMod n₂) × (ZMod n₁ × ZMod n₂)) :
    (ZMod n₁ × ZMod n₂) × (ZMod n₁ × ZMod n₂) :=
  ((p.1.1, p.1.2), (p.2.1 - p.1.1, p.2.2 - p.1.2))


theorem principle_III_composite_cloning_and_cardinality (n₁ n₂ d₁ d₂ : ℕ) :
    Function.Bijective (compositeClone n₁ n₂) ∧
    (∀ x₁ : ZMod n₁, ∀ x₂ : ZMod n₂,
      compositeClone n₁ n₂ ((x₁, x₂), (0, 0)) = ((x₁, x₂), (x₁, x₂))) ∧
    Fintype.card (Fin d₁ × Fin d₂) = d₁ * d₂ := by
  refine ⟨?_, ?_, ?_⟩
  · rw [Function.bijective_iff_has_inverse]
    exact ⟨compositeUnclone n₁ n₂,
      fun ⟨⟨x1, x2⟩, ⟨y1, y2⟩⟩ => by simp [compositeClone, compositeUnclone],
      fun ⟨⟨x1, x2⟩, ⟨y1, y2⟩⟩ => by simp [compositeClone, compositeUnclone]⟩
  · intro x₁ x₂
    simp [compositeClone]
  · simp [Fintype.card_prod]


def crossCopy (n : ℕ) (p : ZMod n × ZMod n) : ZMod n × ZMod n :=
  (p.1, p.1 + p.2)


theorem cross_medium_copy_transfer (n : ℕ) (π : Equiv.Perm (ZMod n)) (x₁ : ZMod n) :
    Function.Bijective (crossCopy n) ∧
    crossCopy n (x₁, 0) = (x₁, x₁) ∧
    Prod.map id π (crossCopy n (x₁, 0)) = (x₁, π x₁) := by
  refine ⟨?_, ?_, ?_⟩
  · exact (cnotClone_bijective_and_clones_zero n).2.2.1
  · simp [crossCopy]
  · simp [crossCopy]


def cnot4 (v : ℤ × ℤ × ℤ × ℤ) : ℤ × ℤ × ℤ × ℤ :=
  (v.1, v.2.1, v.2.2.2, v.2.2.1)


def schmidtDet4 (v : ℤ × ℤ × ℤ × ℤ) : ℤ :=
  v.1 * v.2.2.2 - v.2.1 * v.2.2.1


theorem unitary_cnot_clones_computational_basis_not_superposition_fence
    (u0 u1 v0 v1 : ℤ) :
    cnot4 (1, 0, 0, 0) = (1, 0, 0, 0) ∧
    cnot4 (0, 0, 1, 0) = (0, 0, 0, 1) ∧
    cnot4 (1, 0, 1, 0) = (1, 0, 0, 1) ∧
    cnot4 (1, 0, 1, 0) ≠ (1, 1, 1, 1) ∧
    schmidtDet4 (cnot4 (1, 0, 1, 0)) = 1 ∧
    schmidtDet4 (u0 * v0, u0 * v1, u1 * v0, u1 * v1) = 0 := by
  refine ⟨rfl, rfl, rfl, by decide, rfl, ?_⟩
  dsimp [schmidtDet4]
  ring


def classicalSimplexDim (d₁ d₂ : ℕ) : ℕ := d₁ * d₂ - 1


def realLocalProductDim (d₁ d₂ : ℕ) : ℕ := (d₁ * (d₁ + 1) / 2) * (d₂ * (d₂ + 1) / 2)


def realQuantumDim (d₁ d₂ : ℕ) : ℕ := (d₁ * d₂) * (d₁ * d₂ + 1) / 2


def complexHermitianDim (d₁ d₂ : ℕ) : ℕ := (d₁ * d₂) ^ 2


theorem composite_state_space_dimension_trichotomy_fence :
    Fintype.card (Fin 2 × Fin 2) = 4 ∧
    classicalSimplexDim 2 2 = 3 ∧
    realLocalProductDim 2 2 = 9 ∧
    realQuantumDim 2 2 = 10 ∧
    complexHermitianDim 2 2 = 16 ∧
    classicalSimplexDim 2 2 < realLocalProductDim 2 2 ∧
    realLocalProductDim 2 2 < realQuantumDim 2 2 ∧
    realQuantumDim 2 2 < complexHermitianDim 2 2 := by
  refine ⟨by decide, rfl, rfl, rfl, rfl, by decide, by decide, by decide⟩


theorem real_vs_complex_bilinear_tomography_fence (d₁ d₂ : ℕ) (z₁ z₂ : ℤ) :
    complexHermitianDim d₁ d₂ = complexHermitianDim d₁ 1 * complexHermitianDim 1 d₂ ∧
    (z₁ * z₂ * (z₁ * z₂ + 1) * 2 - z₁ * (z₁ + 1) * (z₂ * (z₂ + 1)) =
      z₁ * z₂ * (z₁ - 1) * (z₂ - 1)) := by
  refine ⟨?_, ?_⟩
  · dsimp [complexHermitianDim]
    ring
  · ring


def partialTransposeIndex (i j : Fin 4) : Fin 4 × Fin 4 :=
  if (i.val % 2) = (j.val % 2) then (i, j)
  else
    let flipB (k : Fin 4) : Fin 4 :=
      if k = 0 then 1 else if k = 1 then 0 else if k = 2 then 3 else 2
    (flipB i, flipB j)


def partialTranspose4 (M : Matrix (Fin 4) (Fin 4) ℤ) : Matrix (Fin 4) (Fin 4) ℤ :=
  Matrix.of fun i j =>
    let ij := partialTransposeIndex i j
    M ij.1 ij.2


theorem psd_vs_pt_cone_classical_interoperability_agreement_fence (d : Fin 4 → ℤ) :
    partialTranspose4 (Matrix.diagonal d) = Matrix.diagonal d := by
  ext i j
  fin_cases i <;> fin_cases j <;> rfl


def bellState4 : Matrix (Fin 4) (Fin 4) ℤ :=
  !![1, 0, 0, 1;
     0, 0, 0, 0;
     0, 0, 0, 0;
     1, 0, 0, 1]


def swapWitness4 : Matrix (Fin 4) (Fin 4) ℤ :=
  partialTranspose4 bellState4


def singletVec : Fin 4 → ℤ := ![0, 1, -1, 0]


def prodVec4 (u0 u1 v0 v1 : ℤ) : Fin 4 → ℤ :=
  ![u0 * v0, u0 * v1, u1 * v0, u1 * v1]


theorem psd_vs_pt_cone_bell_witness_separation_fence
    (w : Fin 4 → ℤ) (u0 u1 v0 v1 : ℤ) :
    dotProduct w (bellState4.mulVec w) = (w 0 + w 3) ^ 2 ∧
    0 ≤ dotProduct w (bellState4.mulVec w) ∧
    dotProduct (prodVec4 u0 u1 v0 v1) (swapWitness4.mulVec (prodVec4 u0 u1 v0 v1)) =
      (u0 * v0 + u1 * v1) ^ 2 ∧
    dotProduct singletVec (bellState4.mulVec singletVec) = 0 ∧
    dotProduct singletVec (swapWitness4.mulVec singletVec) = -2 := by
  have hw : dotProduct w (bellState4.mulVec w) = (w 0 + w 3) ^ 2 := by
    simp [dotProduct, Matrix.mulVec, bellState4, Fin.sum_univ_four]
    ring
  have hprod : dotProduct (prodVec4 u0 u1 v0 v1) (swapWitness4.mulVec (prodVec4 u0 u1 v0 v1)) =
      (u0 * v0 + u1 * v1) ^ 2 := by
    simp [dotProduct, Matrix.mulVec, swapWitness4, partialTranspose4, partialTransposeIndex,
      bellState4, prodVec4, Fin.sum_univ_four]
    ring
  refine ⟨hw, ?_, hprod, by decide, by decide⟩
  rw [hw]
  exact sq_nonneg (w 0 + w 3)

end CampaignCtInformationMediaInteroperability

#print axioms CampaignCtInformationMediaInteroperability.cnotClone_bijective_and_clones_zero
#print axioms CampaignCtInformationMediaInteroperability.cnotClone_zmod2_involutive
#print axioms CampaignCtInformationMediaInteroperability.singleton_not_computation_variable_fence
#print axioms CampaignCtInformationMediaInteroperability.clonable_computation_implies_distinguishable
#print axioms CampaignCtInformationMediaInteroperability.principle_III_composite_cloning_and_cardinality
#print axioms CampaignCtInformationMediaInteroperability.cross_medium_copy_transfer
#print axioms CampaignCtInformationMediaInteroperability.unitary_cnot_clones_computational_basis_not_superposition_fence
#print axioms CampaignCtInformationMediaInteroperability.composite_state_space_dimension_trichotomy_fence
#print axioms CampaignCtInformationMediaInteroperability.real_vs_complex_bilinear_tomography_fence
#print axioms CampaignCtInformationMediaInteroperability.psd_vs_pt_cone_classical_interoperability_agreement_fence
#print axioms CampaignCtInformationMediaInteroperability.psd_vs_pt_cone_bell_witness_separation_fence
