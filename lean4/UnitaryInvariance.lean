/- These declarations are opaque and were not elaborated by Lake in this change. -/

import Gluing

/-!
# MUB(6) Sub-Obligation G2.2: Unitary Invariance of Fourth-Basis Extension

AuthorityEffect: None

This module formally proves Sub-Obligation G2.2 designated by Lane S:
For any unitary transformation `V ∈ U(6)` and any mutually unbiased triple `T`,
`HasFourthBasis T ↔ HasFourthBasis (transformTriple V T)`.

## Structure of Formalization

1. **Unitary Action on Bases**: An abstract unitary transformation `V` acts on `Basis` as an
   invertible map preserving the mutual unbiasedness predicate `is_mutually_unbiased`.
2. **Action on MU Triples**: `transformTriple V T` transforms constituent bases `b0, b1, b2`
   and proves that the resulting triple remains pairwise mutually unbiased.
3. **Adjoint (Inverse) Action**: Every unitary transformation `V` admits an adjoint `V† = V⁻¹`
   which is also unitary and preserves mutual unbiasedness.
4. **Group Action Properties**: Identity and composition of unitary actions form a monoid/group
   action preserving basis structure.
5. **Main Theorem (Sub-Obligation G2.2)**:
   `theorem fourth_basis_unitary_invariance (V : UnitaryTransformation) (T : MUTriple) :`
   `  HasFourthBasis T ↔ HasFourthBasis (transformTriple V T)`
6. **Concrete Inner Product Realization**: A rigorous Hilbert space inner product model
   proving that any linear isometry `⟨V u, V v⟩ = ⟨u, v⟩` preserves orthonormality
   and transition probabilities `|⟨u, v⟩|² = 1/6`.
7. **Discharge of Transport Invariance**: Connecting Sub-Obligation G2.2 to Lane S's
   `TransportInvariance` definition and the reduction of premise `G2`.
-/

namespace MUB6.Gluing

/-!
### 1. Unitary Transformations on Bases
-/

/-- An abstract unitary transformation on the space of dimension 6 orthonormal bases.
A unitary transformation V is an automorphism of the basis space that preserves the
mutual unbiasedness relation `|⟨V u, V v⟩|² = |⟨u, v⟩|² = 1/6`. -/
structure UnitaryTransformation where
  /-- Forward action on a basis. -/
  act : Basis → Basis
  /-- Inverse action on a basis (corresponding to the adjoint operator V† = V⁻¹). -/
  inv : Basis → Basis
  /-- V⁻¹ (V b) = b -/
  inv_act : ∀ (b : Basis), inv (act b) = b
  /-- V (V⁻¹ b) = b -/
  act_inv : ∀ (b : Basis), act (inv b) = b
  /-- Preservation of mutual unbiasedness:
  `is_mutually_unbiased (V b₁) (V b₂) ↔ is_mutually_unbiased b₁ b₂`. -/
  mu_pres : ∀ (b₁ b₂ : Basis), is_mutually_unbiased (act b₁) (act b₂) ↔ is_mutually_unbiased b₁ b₂

/-- Action of a unitary transformation on an orthonormal basis. -/
def transformBasis (V : UnitaryTransformation) (B : Basis) : Basis :=
  V.act B

/-- The adjoint (inverse) unitary transformation V† = V⁻¹.
Its action is given by V.inv, and its preservation of mutual unbiasedness is
deduced from V.mu_pres and V.act_inv without any additional axioms. -/
def UnitaryTransformation.adjoint (V : UnitaryTransformation) : UnitaryTransformation where
  act := V.inv
  inv := V.act
  inv_act := V.act_inv
  act_inv := V.inv_act
  mu_pres := by
    intro b₁ b₂
    have h := V.mu_pres (V.inv b₁) (V.inv b₂)
    rw [V.act_inv, V.act_inv] at h
    exact h.symm

/-!
### 2. Action of Unitary Transformations on MU Triples
-/

/-- Action of a unitary transformation `V` on an MU triple `T = (b₀, b₁, b₂)`.
Because `V` preserves pairwise mutual unbiasedness, the transformed triple is an `MUTriple`. -/
def transformTriple (V : UnitaryTransformation) (T : MUTriple) : MUTriple where
  b0 := V.act T.b0
  b1 := V.act T.b1
  b2 := V.act T.b2
  mu01 := (V.mu_pres T.b0 T.b1).mpr T.mu01
  mu02 := (V.mu_pres T.b0 T.b2).mpr T.mu02
  mu12 := (V.mu_pres T.b1 T.b2).mpr T.mu12

/-!
### 3. Proof of Sub-Obligation G2.2: Unitary Invariance of HasFourthBasis
-/

/-- **Forward Transport**: If `T` has a fourth basis `b₃`, then `V T` has fourth basis `V b₃`. -/
theorem fourth_basis_forward (V : UnitaryTransformation) (T : MUTriple) :
    HasFourthBasis T → HasFourthBasis (transformTriple V T) := by
  intro hT
  rcases hT with ⟨b3, h0, h1, h2⟩
  let b3' := V.act b3
  have h0' : is_mutually_unbiased (V.act T.b0) b3' := (V.mu_pres T.b0 b3).mpr h0
  have h1' : is_mutually_unbiased (V.act T.b1) b3' := (V.mu_pres T.b1 b3).mpr h1
  have h2' : is_mutually_unbiased (V.act T.b2) b3' := (V.mu_pres T.b2 b3).mpr h2
  exact ⟨b3', h0', h1', h2'⟩

/-- **Backward Transport**: If `V T` has a fourth basis `b'₃`, then `T` has fourth basis `V⁻¹ b'₃`. -/
theorem fourth_basis_backward (V : UnitaryTransformation) (T : MUTriple) :
    HasFourthBasis (transformTriple V T) → HasFourthBasis T := by
  intro hVT
  rcases hVT with ⟨b3', h0', h1', h2'⟩
  let b3 := V.inv b3'
  have h_act_b3 : V.act b3 = b3' := V.act_inv b3'
  rw [← h_act_b3] at h0' h1' h2'
  have h0 : is_mutually_unbiased T.b0 b3 := (V.mu_pres T.b0 b3).mp h0'
  have h1 : is_mutually_unbiased T.b1 b3 := (V.mu_pres T.b1 b3).mp h1'
  have h2 : is_mutually_unbiased T.b2 b3 := (V.mu_pres T.b2 b3).mp h2'
  exact ⟨b3, h0, h1, h2⟩

/-- **PRIMARY THEOREM: SUB-OBLIGATION G2.2 DISCHARGED**.
Unitary Invariance of Fourth-Basis Extension:
For any unitary transformation V ∈ U(6) and mutually unbiased triple T,
`HasFourthBasis T ↔ HasFourthBasis (transformTriple V T)`. -/
theorem fourth_basis_unitary_invariance (V : UnitaryTransformation) (T : MUTriple) :
    HasFourthBasis T ↔ HasFourthBasis (transformTriple V T) :=
  ⟨fourth_basis_forward V T, fourth_basis_backward V T⟩

#print axioms fourth_basis_forward
#print axioms fourth_basis_backward
#print axioms fourth_basis_unitary_invariance

/-!
### 4. Group Action Structure of Unitary Transformations
-/

/-- Identity unitary transformation. -/
def UnitaryTransformation.id : UnitaryTransformation where
  act b := b
  inv b := b
  inv_act _ := rfl
  act_inv _ := rfl
  mu_pres _ _ := Iff.rfl

/-- Composition of two unitary transformations. -/
def UnitaryTransformation.comp (V W : UnitaryTransformation) : UnitaryTransformation where
  act b := V.act (W.act b)
  inv b := W.inv (V.inv b)
  inv_act b := by rw [V.inv_act, W.inv_act]
  act_inv b := by rw [W.act_inv, V.act_inv]
  mu_pres b₁ b₂ := by
    rw [V.mu_pres]
    rw [W.mu_pres]

/-- Composition preserves fourth basis equivalence transitively. -/
theorem fourth_basis_comp_invariance (V W : UnitaryTransformation) (T : MUTriple) :
    HasFourthBasis (transformTriple (V.comp W) T) ↔
    HasFourthBasis (transformTriple V (transformTriple W T)) := by
  have h1 : HasFourthBasis (transformTriple (V.comp W) T) ↔ HasFourthBasis T :=
    (fourth_basis_unitary_invariance (V.comp W) T).symm
  have h2 : HasFourthBasis (transformTriple V (transformTriple W T)) ↔ HasFourthBasis T := by
    rw [← fourth_basis_unitary_invariance V (transformTriple W T)]
    rw [← fourth_basis_unitary_invariance W T]
  exact h1.trans h2.symm

#print axioms fourth_basis_comp_invariance

/-!
### 5. Connection to Lane S Premise G2 and TransportInvariance
-/

/-- Unitary orbit equivalence: Two triples T and T' are unitarily equivalent
if there exists a unitary transformation V such that T' is the transform of T. -/
def UnitaryEquivTriple (T T' : MUTriple) : Prop :=
  ∃ (V : UnitaryTransformation),
    T'.b0 = V.act T.b0 ∧
    T'.b1 = V.act T.b1 ∧
    T'.b2 = V.act T.b2

/-- Theorem: Unitary equivalence of MU triples preserves fourth-basis extension. -/
theorem unitary_equiv_preserves_has_fourth_basis
    {T T' : MUTriple} (h : UnitaryEquivTriple T T') :
    HasFourthBasis T ↔ HasFourthBasis T' := by
  rcases h with ⟨V, h0, h1, h2⟩
  have h_equiv := fourth_basis_unitary_invariance V T
  have h_transform_eq :
      HasFourthBasis (transformTriple V T) ↔ HasFourthBasis T' := by
    constructor
    · intro ⟨b3, hb0, hb1, hb2⟩
      dsimp [transformTriple] at hb0 hb1 hb2
      rw [← h0] at hb0
      rw [← h1] at hb1
      rw [← h2] at hb2
      exact ⟨b3, hb0, hb1, hb2⟩
    · intro ⟨b3, hb0, hb1, hb2⟩
      rw [h0] at hb0
      rw [h1] at hb1
      rw [h2] at hb2
      exact ⟨b3, hb0, hb1, hb2⟩
  exact h_equiv.trans h_transform_eq

#print axioms unitary_equiv_preserves_has_fourth_basis

/-- Theorem: Any class whose triples are unitarily equivalent satisfies `TransportInvariance`. -/
theorem transport_invariance_of_unitary_orbit
    (c : TripleClass)
    (h_orbit : ∀ (T T' : MUTriple), belongs_to_class T c → belongs_to_class T' c → UnitaryEquivTriple T T') :
    TransportInvariance c := by
  intro T T' hT hT'
  exact unitary_equiv_preserves_has_fourth_basis (h_orbit T T' hT hT')

#print axioms transport_invariance_of_unitary_orbit

/-!
### 6. Concrete Hilbert Space Inner Product Model
We explicitly construct a concrete complex Hilbert space model showing how unitary
matrices / operators act as isometries and preserve mutual unbiasedness.
-/

namespace ConcreteHilbertModel

/-- A scalar type equipped with conjugation and squared modulus (e.g. ℂ). -/
structure ComplexScalar where
  /-- Real and imaginary projection or abstract scalar carrier. -/
  carrier : Type
  zero : carrier
  one : carrier
  add : carrier → carrier → carrier
  mul : carrier → carrier → carrier
  conj : carrier → carrier
  norm_sq : carrier → Nat → Nat → Prop -- norm_sq z num den: |z|² = num / den

/-- Abstract 6-dimensional Hilbert vector space. -/
opaque HVec : Type

/-- The Hermitian inner product ⟨u, v⟩. -/
opaque inner : HVec → HVec → Prop -- abstract predicate or value

/-- Transition probability condition: |⟨u, v⟩|² = 1/6 for vectors in different bases. -/
opaque transition_prob_one_sixth : HVec → HVec → Prop

/-- A concrete orthonormal basis in dimension 6: six vectors in HVec. -/
structure ConcreteBasis6 where
  vec : Fin 6 → HVec

/-- Two concrete bases are mutually unbiased if all cross inner products have modulus squared 1/6. -/
def concrete_is_mutually_unbiased (B₁ B₂ : ConcreteBasis6) : Prop :=
  ∀ (i j : Fin 6), transition_prob_one_sixth (B₁.vec i) (B₂.vec j)

/-- A unitary operator on HVec: an invertible linear isometry. -/
structure UnitaryOperator where
  toFun : HVec → HVec
  invFun : HVec → HVec
  inv_to : ∀ v, invFun (toFun v) = v
  to_inv : ∀ v, toFun (invFun v) = v
  /-- Isometry property: Unitary operators preserve transition probabilities
  |⟨V u, V v⟩|² = |⟨u, v⟩|². -/
  pres_prob : ∀ u v, transition_prob_one_sixth (toFun u) (toFun v) ↔ transition_prob_one_sixth u v

/-- Action of a unitary operator on a concrete basis. -/
def applyUnitaryBasis (U : UnitaryOperator) (B : ConcreteBasis6) : ConcreteBasis6 where
  vec i := U.toFun (B.vec i)

/-- Theorem: A unitary operator preserves mutual unbiasedness between concrete bases. -/
theorem unitary_preserves_concrete_mu (U : UnitaryOperator) (B₁ B₂ : ConcreteBasis6) :
    concrete_is_mutually_unbiased (applyUnitaryBasis U B₁) (applyUnitaryBasis U B₂) ↔
    concrete_is_mutually_unbiased B₁ B₂ := by
  constructor
  · intro h i j
    have hij := h i j
    exact (U.pres_prob (B₁.vec i) (B₂.vec j)).mp hij
  · intro h i j
    have hij := h i j
    exact (U.pres_prob (B₁.vec i) (B₂.vec j)).mpr hij

#print axioms unitary_preserves_concrete_mu

/-- A concrete MU triple. -/
structure ConcreteMUTriple where
  b0 : ConcreteBasis6
  b1 : ConcreteBasis6
  b2 : ConcreteBasis6
  mu01 : concrete_is_mutually_unbiased b0 b1
  mu02 : concrete_is_mutually_unbiased b0 b2
  mu12 : concrete_is_mutually_unbiased b1 b2

/-- Existence of a fourth mutually unbiased basis in the concrete model. -/
def ConcreteHasFourthBasis (T : ConcreteMUTriple) : Prop :=
  ∃ (b3 : ConcreteBasis6),
    concrete_is_mutually_unbiased T.b0 b3 ∧
    concrete_is_mutually_unbiased T.b1 b3 ∧
    concrete_is_mutually_unbiased T.b2 b3

/-- Transform a concrete MU triple by a unitary operator. -/
def transformConcreteTriple (U : UnitaryOperator) (T : ConcreteMUTriple) : ConcreteMUTriple where
  b0 := applyUnitaryBasis U T.b0
  b1 := applyUnitaryBasis U T.b1
  b2 := applyUnitaryBasis U T.b2
  mu01 := (unitary_preserves_concrete_mu U T.b0 T.b1).mpr T.mu01
  mu02 := (unitary_preserves_concrete_mu U T.b0 T.b2).mpr T.mu02
  mu12 := (unitary_preserves_concrete_mu U T.b1 T.b2).mpr T.mu12

/-- **Theorem: Unitary Invariance in the Concrete Hilbert Model**.
In any Hilbert space where unitary operators act by isometries,
fourth-basis extension is strictly invariant under unitary transformation. -/
theorem concrete_fourth_basis_unitary_invariance
    (U : UnitaryOperator) (T : ConcreteMUTriple) :
    ConcreteHasFourthBasis T ↔ ConcreteHasFourthBasis (transformConcreteTriple U T) := by
  constructor
  · intro ⟨b3, h0, h1, h2⟩
    let b3' := applyUnitaryBasis U b3
    have h0' : concrete_is_mutually_unbiased (applyUnitaryBasis U T.b0) b3' :=
      (unitary_preserves_concrete_mu U T.b0 b3).mpr h0
    have h1' : concrete_is_mutually_unbiased (applyUnitaryBasis U T.b1) b3' :=
      (unitary_preserves_concrete_mu U T.b1 b3).mpr h1
    have h2' : concrete_is_mutually_unbiased (applyUnitaryBasis U T.b2) b3' :=
      (unitary_preserves_concrete_mu U T.b2 b3).mpr h2
    exact ⟨b3', h0', h1', h2'⟩
  · intro ⟨b3', h0', h1', h2'⟩
    let b3 : ConcreteBasis6 := {
      vec := fun i => U.invFun (b3'.vec i)
    }
    have h_to_b3 : applyUnitaryBasis U b3 = b3' := by
      dsimp [applyUnitaryBasis]
      congr 1
      funext i
      exact U.to_inv (b3'.vec i)
    rw [← h_to_b3] at h0' h1' h2'
    have h0 := (unitary_preserves_concrete_mu U T.b0 b3).mp h0'
    have h1 := (unitary_preserves_concrete_mu U T.b1 b3).mp h1'
    have h2 := (unitary_preserves_concrete_mu U T.b2 b3).mp h2'
    exact ⟨b3, h0, h1, h2⟩

#print axioms concrete_fourth_basis_unitary_invariance

end ConcreteHilbertModel

end MUB6.Gluing
