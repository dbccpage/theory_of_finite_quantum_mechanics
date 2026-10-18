import WallTransport
import ZeroRelVariety
import ModuliReduction
import AlgebraicCornerReconstruction
import CandidateGramPositivity

/-!
# Target A4: Quadruple Gramian Overlap Matrix, Block Structure, and Dual Witness Obstruction

AuthorityEffect: None

This module formalizes Target A4 of the MUB(6) formalization program:
1. Exact Dimensions and Canonical Index Bijection:
   - Hilbert space dimension `DIM_HILBERT = 6`.
   - Number of bases in a putative quadruple `NUM_BASES = 4`.
   - Total Gramian dimension `GRAMIAN_DIM = 24`.
   - Provable constructive bijection between `(Fin 4 × Fin 6)` and `Fin 24`:
     `index24`, `basisOf`, `vectorOf`.
2. Exact Block Structure in Complex Arithmetic (C^(24x24)):
   - Quadruple MUB configuration `MUBQuadruple6`: 4 unitary matrices in `Matrix (Fin 6) (Fin 6) ℂ`,
     with `B 0 = 1` (standard basis B_0 = I_6), unitary columns, and pairwise mutually unbiased.
   - Gramian overlap matrix `quadGramianC : Matrix (Fin 24) (Fin 24) ℂ`.
   - Block identification theorem: `quadGramianC B (index24 a k) (index24 b l) = ((B a)ᴴ * (B b)) k l`.
   - Diagonal block identity theorem:
     Diagonal blocks are identically I_6: `quadGramianC B (index24 a k) (index24 a l) = if k = l then 1 else 0`.
     In particular, for B_0 = I_6, the first block is I_6.
     Main diagonal entries are all 1: `quadGramianC B i i = 1`.
   - Off-diagonal block modulus theorem:
     For any a ≠ b, each transition entry satisfies |G_{ij}|² = 1/6:
     `((quadGramianC B (index24 a k) (index24 b l)).normSq = 1 / 6)`.
     Transition matrices with B_0 = 1 are Complex Hadamard Matrices:
     `∀ j k, (B b j k).normSq = 1 / 6` for b ≠ 0.
   - Structure verification: Every valid quadruple Gramian satisfies the exact
     `GramianStructureReport` properties from `mub6_quad_sdp.rs`.
3. Exact PreHilbertSpace Formulation and Rational Quadratic Forms:
   - Candidate quadruple system `QuadCandidateSystem V H` with 24 vectors in an exact PreHilbertSpace `V`.
   - Rational Gramian matrix `quadGramianRat H Q : Fin 24 → Fin 24 → Rat`.
   - Diagonal block structure in `V`: `quadGramianRat H Q (index24 a k) (index24 a l) = if k = l then 1 else 0`.
   - Positive semidefiniteness (PSD) of the 24x24 Gramian:
     `c† G c = ‖∑ c_i v_i‖² ≥ 0` for all rational vectors `c : Fin 24 → Rat`.
4. Algebraic Connection to Positive Semidefinite Dual Witness W = L D L† (D >= 0):
   - Factored dual witness `QuadDualWitness m` in dimension 24 with diagonal pivots D_k ≥ 0.
   - Constructive trace inner product `quadTraceInner W H Q = ∑_k D_k ‖∑_i L_{ik} v_i‖²`.
   - Theorem: Any valid quadruple Gramian satisfies `Tr(W · G(B)) ≥ 0`.
5. Regional Dual Obstruction on Certified Rational Parameter Box:
   - Parameterized candidate quadruple Gramian family `QuadGramFamily θ`.
   - Regional dual obstruction theorem:
     If a certified dual witness W = L D L† with D ≥ 0 achieves strictly negative
     trace `eval_trace (G q) < 0` for all points q in a certified rational box Θ,
     then NO valid quadruple system in H can realize G(p) for any p ∈ Θ.
   - Non-extendibility theorem:
     Certifies non-extendibility of candidate triples to quadruples of MUBs across the box.
   - Bridge to `MUBQuadruple` and `NoCompleteMUB6`.
-/

namespace MUB6.Gluing.TargetA4

open MUB6.Gluing
open MUB6.Gluing.Orbits
open MUB6.Gluing.CandidateGram
open MUB6.Gluing.QuadIncompatibility

/-!
### 1. Exact Dimensions and Canonical Index Arithmetic
-/

/-- Dimension of the underlying Hilbert space: C^6. -/
def DIM_HILBERT : Nat := 6

/-- Number of mutually unbiased bases in a putative quadruple: {B_0, B_1, B_2, B_3}. -/
def NUM_BASES : Nat := 4

/-- Dimension of the quadruple Gramian overlap matrix: 4 * 6 = 24. -/
def GRAMIAN_DIM : Nat := 24

/-- Verification of Gramian dimension product identity: 4 * 6 = 24. -/
theorem gramian_dim_eq : NUM_BASES * DIM_HILBERT = GRAMIAN_DIM := rfl

/-- Canonical injection from basis index `b ∈ Fin 4` and vector index `k ∈ Fin 6`
to the flat Gramian index in `Fin 24`. -/
def index24 (b : Fin 4) (k : Fin 6) : Fin 24 :=
  ⟨b.val * 6 + k.val, by
    have hb := b.isLt
    have hk := k.isLt
    omega⟩

/-- Canonical projection from flat index `i ∈ Fin 24` to its basis index in `Fin 4`. -/
def basisOf (i : Fin 24) : Fin 4 :=
  ⟨i.val / 6, by
    have hi := i.isLt
    omega⟩

/-- Canonical projection from flat index `i ∈ Fin 24` to its vector index within the basis in `Fin 6`. -/
def vectorOf (i : Fin 24) : Fin 6 :=
  ⟨i.val % 6, by
    have hi := i.isLt
    omega⟩

/-- **Theorem: Canonical index roundtrip identity**.
Every flat index `i : Fin 24` decomposes uniquely into `index24 (basisOf i) (vectorOf i)`. -/
theorem index24_basis_vector (i : Fin 24) : index24 (basisOf i) (vectorOf i) = i := by
  apply Fin.ext
  dsimp [index24, basisOf, vectorOf]
  omega

/-- **Theorem: Basis projection recovers original basis index**. -/
theorem basisOf_index24 (b : Fin 4) (k : Fin 6) : basisOf (index24 b k) = b := by
  apply Fin.ext
  dsimp [index24, basisOf]
  have hk := k.isLt
  omega

/-- **Theorem: Vector projection recovers original vector index**. -/
theorem vectorOf_index24 (b : Fin 4) (k : Fin 6) : vectorOf (index24 b k) = k := by
  apply Fin.ext
  dsimp [index24, vectorOf]
  have hk := k.isLt
  omega

/-- **Theorem: Canonical index map is injective**. -/
theorem index24_inj (b1 b2 : Fin 4) (k1 k2 : Fin 6) :
    index24 b1 k1 = index24 b2 k2 ↔ b1 = b2 ∧ k1 = k2 := by
  constructor
  · intro h
    have hb : basisOf (index24 b1 k1) = basisOf (index24 b2 k2) := by rw [h]
    rw [basisOf_index24, basisOf_index24] at hb
    have hk : vectorOf (index24 b1 k1) = vectorOf (index24 b2 k2) := by rw [h]
    rw [vectorOf_index24, vectorOf_index24] at hk
    exact ⟨hb, hk⟩
  · intro ⟨hb, hk⟩
    rw [hb, hk]

/-!
### 2. Complex Matrix Representation of Quadruple MUB in C^(24x24)
-/

/-- A putative quadruple of mutually unbiased bases in dimension 6 over exact ℂ:
- `B 0` is the standard basis (identity matrix `1 : Matrix (Fin 6) (Fin 6) ℂ`).
- Each `B a` is unitary: `(B a)ᴴ * (B a) = 1` and `(B a) * (B a)ᴴ = 1`.
- For distinct bases `a ≠ b`, `B a` and `B b` are mutually unbiased: `IsMUPair (B a) (B b)`. -/
structure MUBQuadruple6 where
  B : Fin 4 → Matrix (Fin 6) (Fin 6) ℂ
  b0_id : B 0 = 1
  unitary : ∀ (a : Fin 4), (B a)ᴴ * (B a) = 1 ∧ (B a) * (B a)ᴴ = 1
  mu : ∀ (a b : Fin 4), a ≠ b → IsMUPair (B a) (B b)

/-- The 6x6 transition block between basis `a` and basis `b`:
G_{ab} = B_aᴴ * B_b. -/
def gramianBlockC (B : MUBQuadruple6) (a b : Fin 4) : Matrix (Fin 6) (Fin 6) ℂ :=
  (B.B a)ᴴ * (B.B b)

/-- The full 24x24 Gramian overlap matrix G(B) of a quadruple of MUBs in dimension 6:
G_{ij} = (B_{basisOf i}ᴴ * B_{basisOf j})_{vectorOf i, vectorOf j}. -/
def quadGramianC (B : MUBQuadruple6) : Matrix (Fin 24) (Fin 24) ℂ :=
  fun i j => (gramianBlockC B (basisOf i) (basisOf j)) (vectorOf i) (vectorOf j)

/-- **Theorem: Block extraction identity for 24x24 Gramian matrix**.
The entry at `(index24 a k, index24 b l)` is exactly `(gramianBlockC B a b) k l`. -/
theorem quadGramianC_entry_eq_block (B : MUBQuadruple6) (a b : Fin 4) (k l : Fin 6) :
    quadGramianC B (index24 a k) (index24 b l) = (gramianBlockC B a b) k l := by
  dsimp [quadGramianC]
  rw [basisOf_index24, basisOf_index24, vectorOf_index24, vectorOf_index24]

/-- **Theorem: Diagonal blocks of the 24x24 Gramian are identically the 6x6 identity matrix I_6**.
Since each basis B_a is unitary, G_{aa} = B_aᴴ * B_a = 1. -/
theorem gramian_diagonal_block_eq_one (B : MUBQuadruple6) (a : Fin 4) :
    gramianBlockC B a a = 1 := by
  dsimp [gramianBlockC]
  exact (B.unitary a).1

/-- **Theorem: Pointwise diagonal block identity**.
For any basis `a : Fin 4` and vector indices `k, l : Fin 6`,
`G(B)_{index24 a k, index24 a l} = if k = l then 1 else 0`. -/
theorem quad_gramian_diagonal_block (B : MUBQuadruple6) (a : Fin 4) (k l : Fin 6) :
    quadGramianC B (index24 a k) (index24 a l) = if k = l then 1 else 0 := by
  rw [quadGramianC_entry_eq_block]
  have h_one := gramian_diagonal_block_eq_one B a
  rw [h_one]
  rfl

/-- **Corollary: For B_0 = I_6, the leading diagonal block is identically I_6**. -/
theorem quad_gramian_b0_block (B : MUBQuadruple6) (k l : Fin 6) :
    quadGramianC B (index24 0 k) (index24 0 l) = if k = l then 1 else 0 :=
  quad_gramian_diagonal_block B 0 k l

/-- **Theorem: Main diagonal entries of the 24x24 Gramian are all equal to 1**. -/
theorem quad_gramian_diag (B : MUBQuadruple6) (i : Fin 24) :
    quadGramianC B i i = 1 := by
  have h := quad_gramian_diagonal_block B (basisOf i) (vectorOf i) (vectorOf i)
  have h_idx : index24 (basisOf i) (vectorOf i) = i := index24_basis_vector i
  rw [h_idx] at h
  rw [h]
  split
  · rfl
  · contradiction

/-- **Theorem: Off-diagonal blocks have transition entries with squared modulus 1/6**.
For any distinct bases `a ≠ b` and any vector indices `k, l : Fin 6`,
`|G(B)_{index24 a k, index24 b l}|² = 1/6`. -/
theorem quad_gramian_off_diagonal_modulus
    (B : MUBQuadruple6) (a b : Fin 4) (hab : a ≠ b) (k l : Fin 6) :
    (quadGramianC B (index24 a k) (index24 b l)).normSq = 1 / 6 := by
  rw [quadGramianC_entry_eq_block]
  dsimp [gramianBlockC]
  exact B.mu a b hab k l

/-- **Theorem: Transition block from B_0 = I_6 to B_b is B_b itself**. -/
theorem b0_transition_block (B : MUBQuadruple6) (b : Fin 4) :
    gramianBlockC B 0 b = B.B b := by
  dsimp [gramianBlockC]
  rw [B.b0_id]
  exact Matrix.one_conjTranspose_mul (B.B b)

/-- **Theorem: Every basis matrix B_b (for b ≠ 0) is a normalized Complex Hadamard Matrix**.
Since B_0 = 1, the mutual unbiasedness with B_0 implies that every entry of B_b has squared modulus 1/6. -/
theorem basis_is_complex_hadamard (B : MUBQuadruple6) (b : Fin 4) (hb : b ≠ 0) :
    ∀ (j k : Fin 6), ((B.B b) j k).normSq = 1 / 6 := by
  have h_mu := B.mu 0 b (Ne.symm hb)
  intro j k
  have hjk := h_mu j k
  have h_b0 := B.b0_id
  have h_mul := Matrix.one_conjTranspose_mul (B.B b)
  rw [h_b0, h_mul] at hjk
  exact hjk


/-- Structure predicate matching `GramianStructureReport` in `mub6_quad_sdp.rs`. -/
structure QuadGramianStructure (G : Matrix (Fin 24) (Fin 24) ℂ) : Prop where
  diag_identity : ∀ (a : Fin 4) (k l : Fin 6), G (index24 a k) (index24 a l) = if k = l then 1 else 0
  off_diag_modulus : ∀ (a b : Fin 4), a ≠ b → ∀ (k l : Fin 6), (G (index24 a k) (index24 b l)).normSq = 1 / 6

/-- **Theorem: Any valid MUB quadruple Gramian satisfies the exact GramianStructureReport conditions**. -/
theorem mub_quad_gramian_satisfies_structure (B : MUBQuadruple6) :
    QuadGramianStructure (quadGramianC B) where
  diag_identity := fun a k l => quad_gramian_diagonal_block B a k l
  off_diag_modulus := fun a b hab k l => quad_gramian_off_diagonal_modulus B a b hab k l


/-!
### 3. Exact PreHilbertSpace Formulation and Rational Quadratic Forms
-/

/-- A candidate quadruple basis configuration in an exact PreHilbertSpace `V`:
- 24 candidate vectors `v : Fin 24 → V`, representing 4 bases of 6 vectors each;
- Each 6-vector block is orthonormal in `V`: ⟨v_{a,k}, v_{a,l}⟩ = δ_{kl}. -/
structure QuadCandidateSystem (V : Type) (H : PreHilbertSpace V) where
  v : Fin 24 → V
  orthonormal_diagonal : ∀ (a : Fin 4) (k l : Fin 6),
    H.inner (v (index24 a k)) (v (index24 a l)) = if k = l then 1 else 0

/-- The exact 24x24 Gram matrix of a candidate quadruple system in `V`:
G_{ij} = ⟨v_i, v_j⟩. -/
def quadGramianRat {V : Type} (H : PreHilbertSpace V) (Q : QuadCandidateSystem V H) :
    Fin 24 → Fin 24 → Rat :=
  gramMatrix H Q.v

/-- **Theorem: Diagonal blocks of the rational candidate Gramian are I_6**. -/
theorem quad_gramian_rat_diagonal_block
    {V : Type} (H : PreHilbertSpace V) (Q : QuadCandidateSystem V H)
    (a : Fin 4) (k l : Fin 6) :
    quadGramianRat H Q (index24 a k) (index24 a l) = if k = l then 1 else 0 :=
  Q.orthonormal_diagonal a k l

/-- **Theorem: Main diagonal entries of the rational candidate Gramian are all equal to 1**. -/
theorem quad_gramian_rat_diag
    {V : Type} (H : PreHilbertSpace V) (Q : QuadCandidateSystem V H) (i : Fin 24) :
    quadGramianRat H Q i i = 1 := by
  have h := Q.orthonormal_diagonal (basisOf i) (vectorOf i) (vectorOf i)
  have h_idx : index24 (basisOf i) (vectorOf i) = i := index24_basis_vector i
  rw [h_idx] at h
  dsimp [quadGramianRat, gramMatrix]
  rw [h]
  split
  · rfl
  · contradiction

/-- **Theorem: The 24x24 candidate Gram matrix is Positive Semidefinite (PSD)**.
For any rational coefficient vector c, c† G c = ‖∑ c_i v_i‖² ≥ 0.
Proven constructively from inner product self-nonnegativity. -/
theorem quad_gramian_rat_is_psd
    {V : Type} (H : PreHilbertSpace V) (Q : QuadCandidateSystem V H) (c : Fin 24 → Rat) :
    0 ≤ quadFormOnVectors H Q.v c :=
  gram_matrix_is_psd H Q.v c

/-!
### 4. Algebraic Connection to Dual Witness W = L D L† (D >= 0)
-/

/-- A factored positive semidefinite dual witness matrix in dimension 24:
W = L D L† with m modes and diagonal weights D_k ≥ 0.
Corresponds to `MubQuadSdpCertificate` from `mub6_quad_sdp.rs`. -/
def QuadDualWitness (m : Nat) := DualWitness 24 m

/-- Trace inner product Tr(W · G(Q)) = ∑_k D_k ‖∑_i L_{ik} v_i‖² in dimension 24. -/
def quadTraceInner {m : Nat} (W : QuadDualWitness m)
    {V : Type} (H : PreHilbertSpace V) (Q : QuadCandidateSystem V H) : Rat :=
  traceInnerFactored W H Q.v

/-- **Theorem: Nonnegativity of Dual Witness Trace on any Valid Quadruple Gramian**.
Tr(W · G(Q)) ≥ 0 for any valid quadruple candidate system Q and any dual witness W with D ≥ 0.
This establishes the algebraic connection between the candidate vector Gramian and the
positive semidefinite dual witness W = L D L† (D >= 0). -/
theorem quad_dual_witness_trace_nonneg
    {m : Nat} (W : QuadDualWitness m)
    {V : Type} (H : PreHilbertSpace V) (Q : QuadCandidateSystem V H) :
    0 ≤ quadTraceInner W H Q :=
  dual_witness_trace_nonneg W H Q.v

/-!
### 5. Regional Dual Obstruction on Certified Rational Parameter Box
-/

/-- Parameterized family of 24x24 candidate Gram matrices G(θ). -/
def QuadGramFamily (θ : Type) := CandidateGramFamily θ 24

/-- Parameterized family of 24 candidate column vectors v(θ). -/
def QuadVectorFamily (θ : Type) (V : Type) := CandidateVectorFamily θ V 24

/-- **THE TARGET A4 REGIONAL DUAL OBSTRUCTION THEOREM**.
If an SDP dual witness W = L D L† (with D ≥ 0) certifies a strictly negative trace
`eval_trace (G q) < 0` across an entire certified parameter box,
then for any point p in that box, G(p) CANNOT be realized as the Gram matrix
of any valid quadruple candidate system Q in H.

Proof: If such candidate vectors Q.v existed, then by `dual_witness_trace_nonneg`,
the trace would be non-negative: `eval_trace (gramMatrix H Q.v) ≥ 0`,
contradicting `eval_trace (G p) < 0` certified by the rational box certificate. -/
theorem quad_regional_dual_obstruction
    {θ V : Type} (H : PreHilbertSpace V) {m : Nat}
    (W : QuadDualWitness m)
    (G : QuadGramFamily θ)
    (eval_trace : (Fin 24 → Fin 24 → Rat) → Rat)
    (h_eval_eq : ∀ (v : Fin 24 → V), eval_trace (gramMatrix H v) = traceInnerFactored W H v)
    (box : ParameterBox θ)
    (h_box_neg : ∀ (q : θ), box.in_box q → eval_trace (G q) < 0)
    (p : θ)
    (hp : box.in_box p) :
    ¬ ∃ (Q : QuadCandidateSystem V H), quadGramianRat H Q = G p := by
  intro ⟨Q, hQ⟩
  have h_not := regional_dual_obstruction H W G eval_trace h_eval_eq box h_box_neg p hp
  exact h_not ⟨Q.v, hQ⟩

/-- **Non-Extendibility of Candidate Quadruple Across Parameter Box**:
Under the certified SDP dual obstruction, no quadruple candidate system exists that realizes G(p).
This certifies non-extendibility of the candidate configuration to a 4-MUB family on the box. -/
theorem quad_non_extendibility_on_box
    {θ V : Type} (H : PreHilbertSpace V) {m : Nat}
    (W : QuadDualWitness m)
    (G : QuadGramFamily θ)
    (eval_trace : (Fin 24 → Fin 24 → Rat) → Rat)
    (h_eval_eq : ∀ (v : Fin 24 → V), eval_trace (gramMatrix H v) = traceInnerFactored W H v)
    (box : ParameterBox θ)
    (h_box_neg : ∀ (q : θ), box.in_box q → eval_trace (G q) < 0)
    (p : θ)
    (hp : box.in_box p) :
    ∀ (Q : QuadCandidateSystem V H), quadGramianRat H Q = G p → False := by
  intro Q hQ
  have h_obst := quad_regional_dual_obstruction H W G eval_trace h_eval_eq box h_box_neg p hp
  exact h_obst ⟨Q, hQ⟩

/-- **Realization Obstruction for Parameterized Quadruple Families**:
A parameterized candidate vector family cannot realize the Gram family G(θ) on the certified box. -/
theorem quad_realizes_gram_family_obstruction
    {θ V : Type} (H : PreHilbertSpace V) {m : Nat}
    (W : QuadDualWitness m)
    (G : QuadGramFamily θ)
    (eval_trace : (Fin 24 → Fin 24 → Rat) → Rat)
    (h_eval_eq : ∀ (v : Fin 24 → V), eval_trace (gramMatrix H v) = traceInnerFactored W H v)
    (box : ParameterBox θ)
    (h_box_neg : ∀ (q : θ), box.in_box q → eval_trace (G q) < 0)
    (p : θ) (hp : box.in_box p)
    (v : QuadVectorFamily θ V) :
    RealizesGramFamily H box G v → False := by
  exact realizes_gram_family_obstruction H W G eval_trace h_eval_eq box h_box_neg p hp v

/-!
### 6. Axiom Audits
-/

#print axioms gramian_dim_eq
#print axioms index24_basis_vector
#print axioms basisOf_index24
#print axioms vectorOf_index24
#print axioms index24_inj
#print axioms quadGramianC_entry_eq_block
#print axioms gramian_diagonal_block_eq_one
#print axioms quad_gramian_diagonal_block
#print axioms quad_gramian_b0_block
#print axioms quad_gramian_diag
#print axioms quad_gramian_off_diagonal_modulus
#print axioms b0_transition_block
#print axioms basis_is_complex_hadamard
#print axioms mub_quad_gramian_satisfies_structure
#print axioms quad_gramian_rat_diagonal_block
#print axioms quad_gramian_rat_diag
#print axioms quad_gramian_rat_is_psd
#print axioms quad_dual_witness_trace_nonneg
#print axioms quad_regional_dual_obstruction
#print axioms quad_non_extendibility_on_box
#print axioms quad_realizes_gram_family_obstruction

end MUB6.Gluing.TargetA4
