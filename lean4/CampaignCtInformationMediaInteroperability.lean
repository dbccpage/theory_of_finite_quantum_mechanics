import Mathlib.Data.Matrix.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Perm
import Mathlib.GroupTheory.Perm.Basic
import Mathlib.Tactic

/-!
# Campaign: CT-INFORMATION-MEDIA-INTEROPERABILITY (TFQ-2006)

Formalizes the finite deterministic algebraic core of Constructor Theory Principle III
(Interoperability of Information Media, Deutsch & Marletto 2015, Proc. R. Soc. A 471,
20140540, arXiv:1405.5563, Sections 3-6 pp. 9-12) and the scope fences explaining why
Principle III does not discharge `FQ-GAP-TENSOR-UNIQUENESS` (`TFQ-2007`):

1. **Reversible Cloning on Finite Computation Variables (`ZMod n`)**:
   - `cnotClone n (x, y) = (x, x + y)` and `cnotUnclone n (x, y) = (x, y - x)` are
     two-sided inverses, establishing that `cnotClone n` is bijective and clones every
     attribute `x : ZMod n` when the target is prepared in the blank attribute `0`.
   - On `ZMod 2` (classical bit medium), `cnotClone 2` is an involution.
2. **Computation Variable Threshold and Distinguishability (Sections 3-5)**:
   - On `Fin 1` (`|S| = 1 < 2`), all attributes are equal and `|Perm (Fin 1)| = 1`, whereas
     for `Fin (n + 2)` (`|S| ≥ 2`) there exist distinct attributes `0 ≠ 1` swapped by
     `Equiv.swap 0 1`.
   - Any injective mapping into an information variable separates distinct source attributes
     both before and after cloning, whereas a non-injective mapping cannot be separated by
     any deterministic post-processing.
3. **Principle III (Interoperability of Information Media) on Finite Sets (Section 6)**:
   - Given two information media `ZMod n₁` and `ZMod n₂`, the composite Cartesian medium
     `ZMod n₁ × ZMod n₂` admits the reversible componentwise cloning bijection
     `compositeClone n₁ n₂` with composite blank `(0, 0)`, and the composite attribute set
     `Fin d₁ × Fin d₂` has cardinality `d₁ * d₂`.
   - Cross-medium copy `crossCopy n (x₁, x₂) = (x₁, x₁ + x₂)` is a bijection on
     `ZMod n × ZMod n` that copies attribute `x₁` of medium 1 into medium 2 prepared in blank `0`.
4. **Quantum vs Classical Cloning Fence (Off-Diagonal Superposition Non-Clonability)**:
   - The 2-qubit CNOT operator `cnot4` on `ℤ⁴` clones computational basis vectors
     `(1, 0, 0, 0) mapsto (1, 0, 0, 0)` and `(0, 0, 1, 0) mapsto (0, 0, 0, 1)`, but maps the equal
     superposition `(1, 0, 1, 0)` to the entangled Bell vector `(1, 0, 0, 1)` rather than
     the product clone `(1, 1, 1, 1)`, with nonzero entanglement determinant `1 ≠ 0`.
5. **State-Space Dimension and Bipartite Cone Non-Selection Fences (TFQ-2007 Bridge)**:
   - Set-level interoperability (`|S₁ × S₂| = d₁ * d₂ = 4` for `d₁ = d₂ = 2`) is shared by
     four pairwise distinct composite state-space dimension formulas: classical simplex
     dimension `3`, local-tomographic real product `9`, real symmetric quantum space `10`,
     and complex Hermitian tensor product `16`.
   - Complex Hermitian dimension satisfies exact multiplicative local tomography
     `(d₁ * d₂)² = d₁² * d₂²`, whereas real symmetric dimension has positive holism excess.
   - On `4 × 4` matrices over `ℤ`, the partial transpose `partialTranspose4` leaves every
     classical diagonal matrix `Matrix.diagonal d` invariant, so the quantum PSD cone and
     the Partially-Transposed (PT) cone share the exact same classical information media
     interoperability on `{0,1}²`, yet are separated by the Bell state `bellState4` and its
     partial transpose `swapWitness4` on the singlet vector `![0, 1, -1, 0]`.
-/

namespace CampaignCtInformationMediaInteroperability

/-- Reversible modular addition (generalized CNOT) cloning map on `ZMod n × ZMod n`. -/
def cnotClone (n : ℕ) (p : ZMod n × ZMod n) : ZMod n × ZMod n :=
  (p.1, p.1 + p.2)

/-- Inverse of `cnotClone n` on `ZMod n × ZMod n`. -/
def cnotUnclone (n : ℕ) (p : ZMod n × ZMod n) : ZMod n × ZMod n :=
  (p.1, p.2 - p.1)

/-- Theorem 1: `cnotClone n` and `cnotUnclone n` are two-sided inverses, `cnotClone n` is
bijective, and preparing the second slot in the blank attribute `0` clones every `x : ZMod n`. -/
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

/-- Theorem 2: On the binary information medium `ZMod 2`, `cnotClone 2` is an involution. -/
theorem cnotClone_zmod2_involutive (p : ZMod 2 × ZMod 2) :
    cnotClone 2 (cnotClone 2 p) = p := by
  rcases p with ⟨x, y⟩
  fin_cases x <;> fin_cases y <;> rfl

/-- Theorem 3 (Computation Variable Cardinality Threshold Fence):
A 1-state attribute set `Fin 1` has no distinct attributes and only 1 permutation, whereas
every attribute set `Fin (n + 2)` of cardinality `≥ 2` admits distinct attributes `0 ≠ 1`
and a nontrivial swap permutation exchanging them. -/
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

/-- Theorem 4 (Distinguishability via Cloning, Section 5 Eq. (4)):
An injective encoding `f : X → ZMod n` into a clonable medium maps distinct attributes
`x ≠ y` to distinct cloned pairs `cnotClone n (f x, 0) ≠ cnotClone n (f y, 0)`, whereas
any non-injective collision `f x = f y` cannot be separated by any downstream map `g`. -/
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

/-- Componentwise reversible cloning on the composite information medium
`ZMod n₁ × ZMod n₂` (Principle III: Interoperability of Information Media). -/
def compositeClone (n₁ n₂ : ℕ)
    (p : (ZMod n₁ × ZMod n₂) × (ZMod n₁ × ZMod n₂)) :
    (ZMod n₁ × ZMod n₂) × (ZMod n₁ × ZMod n₂) :=
  ((p.1.1, p.1.2), (p.1.1 + p.2.1, p.1.2 + p.2.2))

/-- Inverse of `compositeClone n₁ n₂`. -/
def compositeUnclone (n₁ n₂ : ℕ)
    (p : (ZMod n₁ × ZMod n₂) × (ZMod n₁ × ZMod n₂)) :
    (ZMod n₁ × ZMod n₂) × (ZMod n₁ × ZMod n₂) :=
  ((p.1.1, p.1.2), (p.2.1 - p.1.1, p.2.2 - p.1.2))

/-- Theorem 5 (Principle III Composite Cloning and Attribute Cardinality):
For any two finite information media `ZMod n₁` and `ZMod n₂`, the composite medium
`ZMod n₁ × ZMod n₂` has a bijective reversible cloning map `compositeClone n₁ n₂` with
composite blank `(0, 0)`, and the Cartesian attribute set `Fin d₁ × Fin d₂` has
cardinality `d₁ * d₂`. -/
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

/-- Cross-medium reversible copy from medium 1 (`ZMod n`) to medium 2 (`ZMod n`). -/
def crossCopy (n : ℕ) (p : ZMod n × ZMod n) : ZMod n × ZMod n :=
  (p.1, p.1 + p.2)

/-- Theorem 6 (Cross-Medium Copy Bijection):
Cross-medium copy `crossCopy n` is a bijection on `ZMod n × ZMod n` that copies any
attribute `x₁` of medium 1 into medium 2 initialized in blank `0`, and composing with
any permutation `π : Equiv.Perm (ZMod n)` on medium 2 realizes every recoded copy `(x₁, π x₁)`. -/
theorem cross_medium_copy_transfer (n : ℕ) (π : Equiv.Perm (ZMod n)) (x₁ : ZMod n) :
    Function.Bijective (crossCopy n) ∧
    crossCopy n (x₁, 0) = (x₁, x₁) ∧
    Prod.map id π (crossCopy n (x₁, 0)) = (x₁, π x₁) := by
  refine ⟨?_, ?_, ?_⟩
  · exact (cnotClone_bijective_and_clones_zero n).2.2.1
  · simp [crossCopy]
  · simp [crossCopy]

/-- 2-qubit CNOT action on unnormalized amplitude vectors `(a00, a01, a10, a11) ∈ ℤ⁴`. -/
def cnot4 (v : ℤ × ℤ × ℤ × ℤ) : ℤ × ℤ × ℤ × ℤ :=
  (v.1, v.2.1, v.2.2.2, v.2.2.1)

/-- Entanglement (rank-2) polynomial `a00 * a11 - a01 * a10` on `ℤ⁴`, which vanishes on all
product vectors `(u0 * v0, u0 * v1, u1 * v0, u1 * v1)`. -/
def schmidtDet4 (v : ℤ × ℤ × ℤ × ℤ) : ℤ :=
  v.1 * v.2.2.2 - v.2.1 * v.2.2.1

/-- Theorem 7 (Quantum Off-Diagonal Non-Clonability / Entanglement Fence):
While `cnot4` clones the classical basis vectors `(1,0,0,0)` and `(0,0,1,0)` with zero
entanglement determinant, applying `cnot4` to the superposition `(1,0,1,0)` yields the
Bell state `(1,0,0,1)` rather than the product clone `(1,1,1,1)`, and `schmidtDet4`
detects that `(1,0,0,1)` cannot be written as any tensor product `(u0*v0, u0*v1, u1*v0, u1*v1)`. -/
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

/-- Classical probability simplex dimension `d₁ * d₂ - 1`. -/
def classicalSimplexDim (d₁ d₂ : ℕ) : ℕ := d₁ * d₂ - 1

/-- Local-tomographic real symmetric product dimension `(d₁(d₁+1)/2) * (d₂(d₂+1)/2)`. -/
def realLocalProductDim (d₁ d₂ : ℕ) : ℕ := (d₁ * (d₁ + 1) / 2) * (d₂ * (d₂ + 1) / 2)

/-- Real symmetric composite density-matrix space dimension `d₁ d₂ (d₁ d₂ + 1) / 2`. -/
def realQuantumDim (d₁ d₂ : ℕ) : ℕ := (d₁ * d₂) * (d₁ * d₂ + 1) / 2

/-- Complex Hermitian composite operator-space dimension `(d₁ * d₂)²`. -/
def complexHermitianDim (d₁ d₂ : ℕ) : ℕ := (d₁ * d₂) ^ 2

/-- Theorem 8 (Composite State-Space Dimension Non-Selection Fence):
For two interoperable binary media (`d₁ = 2, d₂ = 2`, composite attribute count `2 * 2 = 4`),
the classical simplex (`3`), real local-tomographic product (`9`), real quantum symmetric
space (`10`), and complex Hermitian tensor product (`16`) have strictly increasing
dimensions `3 < 9 < 10 < 16` despite sharing the exact same 4-element classical information
medium `Fin 2 × Fin 2`. -/
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

/-- Theorem 9 (Complex Local Tomography vs Real Holism Excess):
Complex Hermitian operator dimension factors multiplicatively (`complexHermitianDim d₁ d₂ =
complexHermitianDim d₁ 1 * complexHermitianDim 1 d₂`) for all `d₁, d₂`, whereas the fourfold
real symmetric dimensions satisfy the exact algebraic holism identity
`d₁ d₂ (d₁ d₂ + 1) * 2 - d₁(d₁+1) * d₂(d₂+1) = d₁ d₂ (d₁ - 1)(d₂ - 1)`. -/
theorem real_vs_complex_bilinear_tomography_fence (d₁ d₂ : ℕ) (z₁ z₂ : ℤ) :
    complexHermitianDim d₁ d₂ = complexHermitianDim d₁ 1 * complexHermitianDim 1 d₂ ∧
    (z₁ * z₂ * (z₁ * z₂ + 1) * 2 - z₁ * (z₁ + 1) * (z₂ * (z₂ + 1)) =
      z₁ * z₂ * (z₁ - 1) * (z₂ - 1)) := by
  refine ⟨?_, ?_⟩
  · dsimp [complexHermitianDim]
    ring
  · ring

/-- Subsystem-B partial transpose on `4 × 4` matrices (indices `0=(0,0), 1=(0,1), 2=(1,0), 3=(1,1)`):
flips the second bit of both row and column indices when they differ (`1 % 2 ≠ j % 2`), i.e.,
swaps off-diagonal entries within each `2 × 2` subsystem-B block. -/
def partialTransposeIndex (i j : Fin 4) : Fin 4 × Fin 4 :=
  if (i.val % 2) = (j.val % 2) then (i, j)
  else
    let flipB (k : Fin 4) : Fin 4 :=
      if k = 0 then 1 else if k = 1 then 0 else if k = 2 then 3 else 2
    (flipB i, flipB j)

/-- Partial transpose on `4 × 4` integer matrices. -/
def partialTranspose4 (M : Matrix (Fin 4) (Fin 4) ℤ) : Matrix (Fin 4) (Fin 4) ℤ :=
  Matrix.of fun i j =>
    let ij := partialTransposeIndex i j
    M ij.1 ij.2

/-- Theorem 10 (Classical Diagonal Invariance Under Partial Transpose):
Every diagonal `4 × 4` matrix `Matrix.diagonal d` (representing a classical probability
distribution or observable over the composite information medium `{0,1} × {0,1}`) is
strictly invariant under `partialTranspose4`. -/
theorem psd_vs_pt_cone_classical_interoperability_agreement_fence (d : Fin 4 → ℤ) :
    partialTranspose4 (Matrix.diagonal d) = Matrix.diagonal d := by
  ext i j
  fin_cases i <;> fin_cases j <;> rfl

/-- Unnormalized Bell density matrix `|Φ⁺⟩⟨Φ⁺|` with `|Φ⁺⟩ = |00⟩ + |11⟩`. -/
def bellState4 : Matrix (Fin 4) (Fin 4) ℤ :=
  !![1, 0, 0, 1;
     0, 0, 0, 0;
     0, 0, 0, 0;
     1, 0, 0, 1]

/-- Partially transposed Bell matrix (the 2-qubit swap operator `W = bellState4^{T_B}`). -/
def swapWitness4 : Matrix (Fin 4) (Fin 4) ℤ :=
  partialTranspose4 bellState4

/-- Singlet test vector `|Ψ⁻⟩ = (0, 1, -1, 0)`. -/
def singletVec : Fin 4 → ℤ := ![0, 1, -1, 0]

/-- Product vector `(u0, u1) ⊗ (v0, v1) = (u0*v0, u0*v1, u1*v0, u1*v1)`. -/
def prodVec4 (u0 u1 v0 v1 : ℤ) : Fin 4 → ℤ :=
  ![u0 * v0, u0 * v1, u1 * v0, u1 * v1]

/-- Theorem 11 (PSD vs PT Cone Separation by Entangled Bell Witness):
`bellState4` has non-negative quadratic form `(w 0 + w 3)^2 ≥ 0` on all vectors `w : Fin 4 → ℤ`
(so it lies in the PSD cone), and its partial transpose `swapWitness4` has the exact same
non-negative quadratic form `(u0 * v0 + u1 * v1)^2 ≥ 0` on every product vector `prodVec4 u0 u1 v0 v1`,
yet `swapWitness4` evaluates to `-2 < 0` on `singletVec` whereas `bellState4` evaluates to `0`. -/
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
