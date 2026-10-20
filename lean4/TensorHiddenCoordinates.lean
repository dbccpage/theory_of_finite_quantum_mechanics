import TensorPartialTranspose

/-! A doubled positive carrier with independent preparations, product tests and
reversible matrix operations. Product tests forget the summand flag, so this
model intentionally cannot supply the tomography field of TomographicData. -/
open Matrix Module
open scoped BigOperators Kronecker ComplexOrder
noncomputable section
namespace TensorHiddenCoordinates
open TensorTomography TensorComposition TensorEffectOrder TensorPartialTranspose
variable {n m : Type*} [Fintype n] [Fintype m] [DecidableEq n] [DecidableEq m]

abbrev Doubled (d : Type*) := Herm d × Herm d

def forget {d : Type*} : Doubled d →ₗ[ℝ] Herm d :=
  LinearMap.fst ℝ (Herm d) (Herm d) + LinearMap.snd ℝ (Herm d) (Herm d)

def split {d : Type*} : Herm d →ₗ[ℝ] Doubled d :=
  ((1 / 2 : ℝ) • LinearMap.id).prod ((1 / 2 : ℝ) • LinearMap.id)

@[simp] theorem forget_split {d : Type*} (A : Herm d) : forget (split A) = A := by
  change (1 / 2 : ℝ) • A + (1 / 2 : ℝ) • A = A
  rw [← add_smul]
  norm_num

def prepare : Herm n →ₗ[ℝ] Herm m →ₗ[ℝ] Doubled (n × m) where
  toFun A := split.comp (productMap A)
  map_add' A B := by
    apply LinearMap.ext; intro C
    change split (product (A + B) C) = split (product A C) + split (product B C)
    rw [product_add_left, map_add]
  map_smul' r A := by
    apply LinearMap.ext; intro B
    change split (product (r • A) B) = r • split (product A B)
    rw [product_smul_left, map_smul]

def test : Herm n →ₗ[ℝ] Herm m →ₗ[ℝ] Doubled (n × m) →ₗ[ℝ] ℝ where
  toFun E := {
    toFun := fun F => (pairing (product E F)).comp forget
    map_add' F G := by
      apply LinearMap.ext; intro x
      change pairing (product E (F + G)) (forget x) = _
      simp only [product_add_right, map_add, LinearMap.add_apply, LinearMap.comp_apply]
    map_smul' r F := by
      apply LinearMap.ext; intro x
      change pairing (product E (r • F)) (forget x) = _
      simp only [product_smul_right, map_smul, LinearMap.smul_apply, LinearMap.comp_apply,
        RingHom.id_apply] }
  map_add' E F := by
    apply LinearMap.ext; intro G
    apply LinearMap.ext; intro x
    change pairing (product (E + F) G) (forget x) =
      pairing (product E G) (forget x) + pairing (product F G) (forget x)
    rw [product_add_left, map_add, LinearMap.add_apply]
  map_smul' r E := by
    apply LinearMap.ext; intro F
    apply LinearMap.ext; intro x
    change pairing (product (r • E) F) (forget x) = r • pairing (product E F) (forget x)
    rw [product_smul_left, map_smul, LinearMap.smul_apply]

@[simp] theorem test_apply (E : Herm n) (F : Herm m) (x : Doubled (n × m)) :
    test E F x = pairing (product E F) (x.1 + x.2) := rfl

theorem independent_probabilities (E A : Herm n) (F B : Herm m) :
    test E F (prepare A B) = pairing E A * pairing F B := by
  change pairing (product E F) (forget (split (product A B))) = _
  rw [forget_split, pairing_product]

def PositiveD {d : Type*} (x : Doubled d) : Prop := Positive x.1 ∧ Positive x.2

theorem preparation_positive {A : Herm n} {B : Herm m} (hA : Positive A) (hB : Positive B) :
    PositiveD (prepare A B) := by
  constructor <;> exact (hA.kronecker hB).smul (by norm_num : (0 : ℝ) ≤ 1 / 2)

theorem positiveD_add {d : Type*} {x y : Doubled d} (hx : PositiveD x) (hy : PositiveD y) :
    PositiveD (x + y) := ⟨hx.1.add hy.1, hx.2.add hy.2⟩

theorem positiveD_smul {d : Type*} {x : Doubled d} (hx : PositiveD x) {r : ℝ} (hr : 0 ≤ r) :
    PositiveD (r • x) := ⟨hx.1.smul hr, hx.2.smul hr⟩

theorem product_tests_nonnegative {E : Herm n} {F : Herm m}
    (hE : Positive E) (hF : Positive F) {x : Doubled (n × m)} (hx : PositiveD x) :
    0 ≤ test E F x := pairing_nonneg (hE.kronecker hF) (hx.1.add hx.2)

theorem deterministic_test (x : Doubled (n × m)) :
    test (1 : Herm n) (1 : Herm m) x = x.1.val.trace.re + x.2.val.trace.re := by
  simp [test_apply, pairing_apply, product]

def doubledConj {d : Type*} [Fintype d] (U : Matrix d d ℂ) (x : Doubled d) : Doubled d :=
  (conjMap U x.1, conjMap U x.2)

theorem doubledConj_positive {d : Type*} [Fintype d] (U : Matrix d d ℂ)
    {x : Doubled d} (hx : PositiveD x) : PositiveD (doubledConj U x) :=
  ⟨conjMap_positive U hx.1, conjMap_positive U hx.2⟩

theorem doubledConj_inverse {d : Type*} [Fintype d] [DecidableEq d]
    (U : Matrix.unitaryGroup d ℂ) (x : Doubled d) :
    doubledConj U.valᴴ (doubledConj U.val x) = x :=
  Prod.ext (conjMap_inverse U x.1) (conjMap_inverse U x.2)

theorem doubledConj_statistics (U : Matrix (n × m) (n × m) ℂ)
    (E : Herm n) (F : Herm m) (x : Doubled (n × m)) :
    test E F (doubledConj U x) = pairing (product E F) (conjMap U (forget x)) := by
  change pairing (product E F) (conjMap U x.1 + conjMap U x.2) = _
  rw [← map_add]
  rfl

/-- Both normalized positive states retain the same entire product-test table;
the extra global test reads the first summand's trace and distinguishes them. -/
theorem hidden_normalized_states (ρ : Herm (n × m)) (hρ : Positive ρ)
    (ht : ρ.val.trace.re = 1) :
    PositiveD (ρ, 0) ∧ PositiveD (0, ρ) ∧
    test (1 : Herm n) (1 : Herm m) (ρ, 0) = 1 ∧
    test (1 : Herm n) (1 : Herm m) (0, ρ) = 1 ∧
    (ρ, (0 : Herm (n × m))) ≠ (0, ρ) ∧
    (∀ E F, test E F (ρ, 0) = test E F (0, ρ)) ∧
    (ρ, (0 : Herm (n × m))).1.val.trace.re ≠ ((0 : Herm (n × m)), ρ).1.val.trace.re := by
  have hne : ρ ≠ 0 := by intro h; simp [h] at ht
  refine ⟨⟨hρ, Matrix.PosSemidef.zero⟩, ⟨Matrix.PosSemidef.zero, hρ⟩, ?_, ?_, ?_, ?_, ?_⟩
  · rw [deterministic_test]; simpa using ht
  · rw [deterministic_test]; simpa using ht
  · intro h; exact hne (congrArg Prod.fst h)
  · intro E F; simp
  · simpa [ht]

theorem no_local_tomography (ρ : Herm (n × m)) (hρ : ρ ≠ 0) :
    ¬ (∀ x y : Doubled (n × m), (∀ E F, test E F x = test E F y) → x = y) := by
  intro h
  have he := h (ρ, 0) (0, ρ) (by intro E F; simp)
  exact hρ (congrArg Prod.fst he)

theorem dimension_doubled {d : Type*} [Fintype d] :
    Module.finrank ℝ (Doubled d) = 2 * Module.finrank ℝ (Herm d) := by
  rw [Module.finrank_prod]
  omega

theorem basis_state_normalized (k : n × m) :
    Positive (hermRankOne (Pi.single k 1)) ∧
    (hermRankOne (Pi.single k 1)).val.trace.re = 1 := by
  refine ⟨Matrix.posSemidef_vecMulVec_self_star _, ?_⟩
  simp [hermRankOne, TensorConeReconstruction.rankOne, Matrix.trace, Matrix.diag_apply,
    Matrix.vecMulVec_apply, Pi.single_apply]

#print axioms independent_probabilities
#print axioms doubledConj_inverse
#print axioms hidden_normalized_states
#print axioms no_local_tomography
#print axioms dimension_doubled
#print axioms basis_state_normalized
end TensorHiddenCoordinates
