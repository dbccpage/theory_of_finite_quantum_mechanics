import TensorCountermodelWitnesses

/-! Embed the two-qubit separations into every pair of finite local systems
with two distinct levels. The local embedding maps, and their left inverses,
are constructed explicitly; no numerical search or entanglement oracle is used. -/
open Matrix Module
open scoped BigOperators Kronecker ComplexOrder MatrixOrder
noncomputable section
namespace TensorCountermodelEmbeddings
open TensorTomography TensorEffectOrder TensorPartialTranspose TensorCountermodelCones
open TensorCountermodelWitnesses

def inclusion {a b : Type*} [DecidableEq b] (e : a ↪ b) : Matrix b a ℂ :=
  fun i j => if i = e j then 1 else 0

theorem inclusion_left_inverse {a b : Type*} [Fintype b] [DecidableEq a] [DecidableEq b]
    (e : a ↪ b) : (inclusion e)ᴴ * inclusion e = 1 := by
  ext i j
  simp [Matrix.mul_apply, Matrix.conjTranspose_apply, inclusion,
    e.injective.eq_iff, Matrix.one_apply, eq_comm]

theorem inclusion_real {a b : Type*} [DecidableEq b] (e : a ↪ b) :
    (inclusion e).map star = inclusion e := by ext i j; simp [inclusion, Matrix.map_apply]

variable {n m : Type*} [Fintype n] [Fintype m] [DecidableEq n] [DecidableEq m]

def embed (e : Q ↪ n) (f : Q ↪ m) : Herm J →ₗ[ℝ] Herm (n × m) :=
  conjMap (inclusion e ⊗ₖ inclusion f)

theorem embedding_left_inverse (e : Q ↪ n) (f : Q ↪ m) :
    (inclusion e ⊗ₖ inclusion f)ᴴ * (inclusion e ⊗ₖ inclusion f) = 1 := by
  rw [conjTranspose_kronecker, ← mul_kronecker_mul, inclusion_left_inverse, inclusion_left_inverse]
  simp

theorem compress_embed (e : Q ↪ n) (f : Q ↪ m) (H : Herm J) :
    conjMap (inclusion e ⊗ₖ inclusion f)ᴴ (embed e f H) = H := by
  apply Subtype.ext
  change (inclusion e ⊗ₖ inclusion f)ᴴ *
    ((inclusion e ⊗ₖ inclusion f) * H.val * (inclusion e ⊗ₖ inclusion f)ᴴ) *
    ((inclusion e ⊗ₖ inclusion f)ᴴ)ᴴ = H.val
  simp only [conjTranspose_conjTranspose, ← Matrix.mul_assoc]
  rw [embedding_left_inverse, Matrix.one_mul, Matrix.mul_assoc,
    embedding_left_inverse, Matrix.mul_one]

theorem gamma_embed (e : Q ↪ n) (f : Q ↪ m) (H : Herm J) :
    gamma (embed e f H) = embed e f (gamma H) := by
  unfold embed
  rw [gamma_conjMap_product, inclusion_real]

theorem embedded_swap_not_positive (e : Q ↪ n) (f : Q ↪ m) :
    ¬ Positive (embed e f swapWitness) := by
  intro h
  have hc := conjMap_positive (inclusion e ⊗ₖ inclusion f)ᴴ h
  rw [compress_embed] at hc
  exact swap_not_positive hc

theorem embedded_swap_twisted (e : Q ↪ n) (f : Q ↪ m) : embed e f swapWitness ∈ twisted := by
  change Positive (gamma (embed e f swapWitness))
  rw [gamma_embed]
  exact conjMap_positive _ swap_twisted

/-- General finite-dimensional cone separation with explicit local embeddings. -/
theorem cone_separations (e : Q ↪ n) (f : Q ↪ m) :
    Positive (embed e f bell) ∧ embed e f bell ∉ sep ∧
    BlockPositive (embed e f swapWitness) ∧ ¬ Positive (embed e f swapWitness) ∧
    embed e f swapWitness ∈ twisted := by
  refine ⟨conjMap_positive _ bell_positive, ?_,
    twisted_blockPositive (embedded_swap_twisted e f), embedded_swap_not_positive e f,
    embedded_swap_twisted e f⟩
  intro h
  have hp := sep_ppt h
  rw [gamma_embed] at hp
  exact embedded_swap_not_positive e f hp

theorem cone_separations_all_dimensions {n m : ℕ} (hn : 2 ≤ n) (hm : 2 ≤ m) :
    ∃ B W : Herm (Fin n × Fin m), Positive B ∧ B ∉ sep ∧
      BlockPositive W ∧ ¬ Positive W ∧ W ∈ twisted := by
  let e : Q ↪ Fin n := ⟨Fin.castLE hn, Fin.castLE_injective hn⟩
  let f : Q ↪ Fin m := ⟨Fin.castLE hm, Fin.castLE_injective hm⟩
  exact ⟨embed e f bell, embed e f swapWitness, cone_separations e f⟩

#print axioms cone_separations
#print axioms cone_separations_all_dimensions
end TensorCountermodelEmbeddings
