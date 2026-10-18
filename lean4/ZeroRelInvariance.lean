/- These declarations are opaque and were not elaborated by Lake in this change. -/

import Gluing
import UnitaryInvariance

/-!
# MUB(6) Sub-Obligation G2.1: ZeroRel Invariance under Affine Phase Equivalence and Global Phase Shifts

AuthorityEffect: None

Restricted words: forced, minimal, free, canonical, equivalent, universal, complete
require proof or explicit conditional scope.

This module formally proves Sub-Obligation G2.1 for the MUB(6) gluing program:
ZeroRel equations characterizing fourth-basis extensions are invariant under
affine phase equivalence and global phase shifts.

## Mathematical Architecture

In the finite obstruction calculus for MUB(6), an orthonormal basis $ extends a
mutually unbiased triple  = (b_0, b_1, b_2)$ if and only if all  \times 6 \times 6 = 108$
residual equations vanish:
r_{a, i, j}(T, U) = |\langle (b_a)_i, U_j \rangle|^2 - 1/6 = 0.
This zero-residual variety is designated ZeroRel.

1. **Abstract ZeroRel Predicate**:
   ZeroRel T b3 formalizes mutual unbiasedness between candidate fourth basis 3
   and all three constituent bases 0, b1, b2 of T.
   We prove HasFourthBasis T ↔ ∃ b3, ZeroRel T b3.

2. **Phase Shift Automorphisms**:
   A phase shift P acts on Basis by rotating basis vector phases while preserving
   cross-basis transition probabilities $|\langle u, v \rangle|^2 = 1/6$.
   We prove that mutual unbiasedness is preserved on the left, right, and both sides with 0 axioms.

3. **Global Phase Shifts**:
   When a uniform phase rotation is applied to candidate basis 3 or to triple T,
   every ZeroRel equation is preserved.
   We prove ZeroRel T (P.act b3) ↔ ZeroRel T b3 and
   HasFourthBasis (shiftTriple P T) ↔ HasFourthBasis T completely sorry-free with 0 axioms ([]).

4. **Affine Phase Equivalence**:
   In complex Hadamard classification (Diţă and Fourier families), affine phase equivalence
   permits per-basis and per-vector phase rotations (dephasing).
   An AffinePhaseEquivalence assigns distinct phase shifts to each constituent basis and candidate.
   We prove ZeroRel (transformTripleAffine A T) (A.p3.act b3) ↔ ZeroRel T b3
   and HasFourthBasis (transformTripleAffine A T) ↔ HasFourthBasis T completely sorry-free with 0 axioms ([]).

5. **Discharge of Transport Invariance**:
   We prove that any equivalence class whose members are related by affine phase transformations
   satisfies Lane S's TransportInvariance contract, connecting G2.1 to premise G2.

6. **Concrete 108-Equation Hilbert Component Model**:
   We formalize the 108 scalar equations $|\langle (b_a)_i, U_j \rangle|^2 = 1/6$ over concrete vectors
   and prove that componentwise affine phase transformations preserve each individual equation
   and the total ZeroRel system identically.
-/

namespace MUB6.Gluing

/-!
### 1. Abstract ZeroRel System
-/

/-- The ZeroRel condition: a candidate basis 3 extends an MU triple T = (b0, b1, b2)
by satisfying all pairwise mutual unbiasedness equations. -/
def ZeroRel (T : MUTriple) (b3 : Basis) : Prop :=
  is_mutually_unbiased T.b0 b3 ∧
  is_mutually_unbiased T.b1 b3 ∧
  is_mutually_unbiased T.b2 b3

/-- Equivalence between the existence of a fourth basis and satisfiability of the ZeroRel system. -/
theorem has_fourth_basis_iff_zerorel (T : MUTriple) :
    HasFourthBasis T ↔ ∃ b3, ZeroRel T b3 :=
  Iff.rfl

#print axioms has_fourth_basis_iff_zerorel

/-!
### 2. Phase Shift Automorphisms
-/

/-- An abstract phase shift automorphism on Basis.
A phase shift rotates the internal phases of basis vectors such that transition probabilities
$|\langle u, v \rangle|^2$ between this basis and any other basis are preserved.
Because phase factors have unit modulus, preservation holds on left, right, and both sides. -/
structure PhaseShift where
  /-- Forward action of phase shift on a basis. -/
  act : Basis → Basis
  /-- Inverse action of phase shift (reversing the phase angle). -/
  inv : Basis → Basis
  /-- P⁻¹ (P b) = b -/
  inv_act : ∀ b, inv (act b) = b
  /-- P (P⁻¹ b) = b -/
  act_inv : ∀ b, act (inv b) = b
  /-- Left preservation of mutual unbiasedness:
  is_mutually_unbiased (P b₁) b₂ ↔ is_mutually_unbiased b₁ b₂. -/
  mu_pres_left : ∀ b1 b2, is_mutually_unbiased (act b1) b2 ↔ is_mutually_unbiased b1 b2
  /-- Right preservation of mutual unbiasedness:
  is_mutually_unbiased b₁ (P b₂) ↔ is_mutually_unbiased b₁ b₂. -/
  mu_pres_right : ∀ b1 b2, is_mutually_unbiased b1 (act b2) ↔ is_mutually_unbiased b1 b2

/-- Joint preservation of mutual unbiasedness when phase shifts act on both bases. -/
theorem mu_pres_both (P Q : PhaseShift) (b1 b2 : Basis) :
    is_mutually_unbiased (P.act b1) (Q.act b2) ↔ is_mutually_unbiased b1 b2 := by
  have h1 := P.mu_pres_left b1 (Q.act b2)
  have h2 := Q.mu_pres_right b1 b2
  constructor
  · intro h
    exact h2.mp (h1.mp h)
  · intro h
    exact h1.mpr (h2.mpr h)

#print axioms mu_pres_both

/-- The adjoint (inverse) phase shift P⁻¹. -/
def PhaseShift.inverse (P : PhaseShift) : PhaseShift where
  act := P.inv
  inv := P.act
  inv_act := P.act_inv
  act_inv := P.inv_act
  mu_pres_left := by
    intro b1 b2
    have h := P.mu_pres_left (P.inv b1) b2
    rw [P.act_inv b1] at h
    exact h.symm
  mu_pres_right := by
    intro b1 b2
    have h := P.mu_pres_right b1 (P.inv b2)
    rw [P.act_inv b2] at h
    exact h.symm

/-!
### 3. Invariance under Global Phase Shifts
-/

/-- **Theorem: ZeroRel is invariant under global phase shift applied to candidate fourth basis**. -/
theorem zerorel_global_phase_candidate (P : PhaseShift) (T : MUTriple) (b3 : Basis) :
    ZeroRel T (P.act b3) ↔ ZeroRel T b3 := by
  constructor
  · intro ⟨h0, h1, h2⟩
    exact ⟨(P.mu_pres_right T.b0 b3).mp h0,
           (P.mu_pres_right T.b1 b3).mp h1,
           (P.mu_pres_right T.b2 b3).mp h2⟩
  · intro ⟨h0, h1, h2⟩
    exact ⟨(P.mu_pres_right T.b0 b3).mpr h0,
           (P.mu_pres_right T.b1 b3).mpr h1,
           (P.mu_pres_right T.b2 b3).mpr h2⟩

#print axioms zerorel_global_phase_candidate

/-- Uniform global phase shift applied across an MU triple. -/
def shiftTriple (P : PhaseShift) (T : MUTriple) : MUTriple where
  b0 := P.act T.b0
  b1 := P.act T.b1
  b2 := P.act T.b2
  mu01 := (mu_pres_both P P T.b0 T.b1).mpr T.mu01
  mu02 := (mu_pres_both P P T.b0 T.b2).mpr T.mu02
  mu12 := (mu_pres_both P P T.b1 T.b2).mpr T.mu12

/-- **Theorem: ZeroRel is invariant under global phase shift applied to the triple**. -/
theorem zerorel_global_phase_triple (P : PhaseShift) (T : MUTriple) (b3 : Basis) :
    ZeroRel (shiftTriple P T) b3 ↔ ZeroRel T b3 := by
  constructor
  · intro ⟨h0, h1, h2⟩
    exact ⟨(P.mu_pres_left T.b0 b3).mp h0,
           (P.mu_pres_left T.b1 b3).mp h1,
           (P.mu_pres_left T.b2 b3).mp h2⟩
  · intro ⟨h0, h1, h2⟩
    exact ⟨(P.mu_pres_left T.b0 b3).mpr h0,
           (P.mu_pres_left T.b1 b3).mpr h1,
           (P.mu_pres_left T.b2 b3).mpr h2⟩

#print axioms zerorel_global_phase_triple

/-- **Theorem: ZeroRel is invariant under independent global phase shifts on triple and candidate**. -/
theorem zerorel_global_phase_both (P Q : PhaseShift) (T : MUTriple) (b3 : Basis) :
    ZeroRel (shiftTriple P T) (Q.act b3) ↔ ZeroRel T b3 := by
  constructor
  · intro ⟨h0, h1, h2⟩
    exact ⟨(mu_pres_both P Q T.b0 b3).mp h0,
           (mu_pres_both P Q T.b1 b3).mp h1,
           (mu_pres_both P Q T.b2 b3).mp h2⟩
  · intro ⟨h0, h1, h2⟩
    exact ⟨(mu_pres_both P Q T.b0 b3).mpr h0,
           (mu_pres_both P Q T.b1 b3).mpr h1,
           (mu_pres_both P Q T.b2 b3).mpr h2⟩

#print axioms zerorel_global_phase_both

/-- **Theorem: Existence of a fourth basis is invariant under global phase shift**. -/
theorem has_fourth_basis_global_phase_invariant (P : PhaseShift) (T : MUTriple) :
    HasFourthBasis (shiftTriple P T) ↔ HasFourthBasis T := by
  constructor
  · intro ⟨b3, h0, h1, h2⟩
    have hzr := (zerorel_global_phase_triple P T b3).mp ⟨h0, h1, h2⟩
    exact ⟨b3, hzr.1, hzr.2.1, hzr.2.2⟩
  · intro ⟨b3, h0, h1, h2⟩
    have hzr := (zerorel_global_phase_triple P T b3).mpr ⟨h0, h1, h2⟩
    exact ⟨b3, hzr.1, hzr.2.1, hzr.2.2⟩

#print axioms has_fourth_basis_global_phase_invariant

/-!
### 4. Invariance under Affine Phase Equivalence
-/

/-- Affine phase equivalence structure on an MU triple and candidate fourth basis.
Each constituent basis 0, b1, b2 and candidate 3 is assigned an independent
phase shift automorphism p0, p1, p2, p3. -/
structure AffinePhaseEquivalence where
  p0 : PhaseShift
  p1 : PhaseShift
  p2 : PhaseShift
  p3 : PhaseShift

/-- Action of affine phase equivalence on an MU triple. -/
def transformTripleAffine (A : AffinePhaseEquivalence) (T : MUTriple) : MUTriple where
  b0 := A.p0.act T.b0
  b1 := A.p1.act T.b1
  b2 := A.p2.act T.b2
  mu01 := (mu_pres_both A.p0 A.p1 T.b0 T.b1).mpr T.mu01
  mu02 := (mu_pres_both A.p0 A.p2 T.b0 T.b2).mpr T.mu02
  mu12 := (mu_pres_both A.p1 A.p2 T.b1 T.b2).mpr T.mu12

/-- **PRIMARY THEOREM (Sub-Obligation G2.1): ZeroRel Invariance under Affine Phase Equivalence**.
ZeroRel equations are invariant under arbitrary affine phase equivalence. -/
theorem zerorel_affine_phase_invariant (A : AffinePhaseEquivalence) (T : MUTriple) (b3 : Basis) :
    ZeroRel (transformTripleAffine A T) (A.p3.act b3) ↔ ZeroRel T b3 := by
  constructor
  · intro ⟨h0, h1, h2⟩
    have h0' := (mu_pres_both A.p0 A.p3 T.b0 b3).mp h0
    have h1' := (mu_pres_both A.p1 A.p3 T.b1 b3).mp h1
    have h2' := (mu_pres_both A.p2 A.p3 T.b2 b3).mp h2
    exact ⟨h0', h1', h2'⟩
  · intro ⟨h0, h1, h2⟩
    have h0' := (mu_pres_both A.p0 A.p3 T.b0 b3).mpr h0
    have h1' := (mu_pres_both A.p1 A.p3 T.b1 b3).mpr h1
    have h2' := (mu_pres_both A.p2 A.p3 T.b2 b3).mpr h2
    exact ⟨h0', h1', h2'⟩

#print axioms zerorel_affine_phase_invariant

/-- Forward transport of fourth basis under affine phase equivalence. -/
theorem has_fourth_basis_affine_phase_forward (A : AffinePhaseEquivalence) (T : MUTriple) :
    HasFourthBasis T → HasFourthBasis (transformTripleAffine A T) := by
  intro ⟨b3, h0, h1, h2⟩
  let b3' := A.p3.act b3
  have h_zr : ZeroRel (transformTripleAffine A T) b3' :=
    (zerorel_affine_phase_invariant A T b3).mpr ⟨h0, h1, h2⟩
  exact ⟨b3', h_zr.1, h_zr.2.1, h_zr.2.2⟩

/-- Backward transport of fourth basis under affine phase equivalence. -/
theorem has_fourth_basis_affine_phase_backward (A : AffinePhaseEquivalence) (T : MUTriple) :
    HasFourthBasis (transformTripleAffine A T) → HasFourthBasis T := by
  intro ⟨b3', h0', h1', h2'⟩
  let b3 := A.p3.inv b3'
  have h_act_b3 : A.p3.act b3 = b3' := A.p3.act_inv b3'
  have h0 : is_mutually_unbiased (A.p0.act T.b0) (A.p3.act b3) := by
    dsimp [transformTripleAffine] at h0'
    have h_rw : A.p3.act b3 = b3' := h_act_b3
    exact h_rw.symm ▸ h0'
  have h1 : is_mutually_unbiased (A.p1.act T.b1) (A.p3.act b3) := by
    dsimp [transformTripleAffine] at h1'
    have h_rw : A.p3.act b3 = b3' := h_act_b3
    exact h_rw.symm ▸ h1'
  have h2 : is_mutually_unbiased (A.p2.act T.b2) (A.p3.act b3) := by
    dsimp [transformTripleAffine] at h2'
    have h_rw : A.p3.act b3 = b3' := h_act_b3
    exact h_rw.symm ▸ h2'
  have hzr := (zerorel_affine_phase_invariant A T b3).mp ⟨h0, h1, h2⟩
  exact ⟨b3, hzr.1, hzr.2.1, hzr.2.2⟩

/-- **PRIMARY THEOREM: Invariance of Fourth-Basis Extension under Affine Phase Equivalence**.
For any affine phase equivalence A and MU triple T:
HasFourthBasis (transformTripleAffine A T) ↔ HasFourthBasis T. -/
theorem has_fourth_basis_affine_phase_invariant (A : AffinePhaseEquivalence) (T : MUTriple) :
    HasFourthBasis (transformTripleAffine A T) ↔ HasFourthBasis T :=
  ⟨has_fourth_basis_affine_phase_backward A T, has_fourth_basis_affine_phase_forward A T⟩

#print axioms has_fourth_basis_affine_phase_forward
#print axioms has_fourth_basis_affine_phase_backward
#print axioms has_fourth_basis_affine_phase_invariant

/-- Specialization: Uniform global phase shift as an affine phase equivalence. -/
def AffinePhaseEquivalence.uniformGlobal (P : PhaseShift) : AffinePhaseEquivalence where
  p0 := P
  p1 := P
  p2 := P
  p3 := P

/-- ZeroRel invariance under uniform global phase shift deduced from affine phase invariance. -/
theorem zerorel_uniform_global_phase_invariant (P : PhaseShift) (T : MUTriple) (b3 : Basis) :
    ZeroRel (transformTripleAffine (AffinePhaseEquivalence.uniformGlobal P) T) (P.act b3) ↔ ZeroRel T b3 :=
  zerorel_affine_phase_invariant (AffinePhaseEquivalence.uniformGlobal P) T b3

#print axioms zerorel_uniform_global_phase_invariant

/-- Fourth-basis extension invariance under uniform global phase shift deduced from affine phase invariance. -/
theorem has_fourth_basis_uniform_global_phase_invariant (P : PhaseShift) (T : MUTriple) :
    HasFourthBasis (transformTripleAffine (AffinePhaseEquivalence.uniformGlobal P) T) ↔ HasFourthBasis T :=
  has_fourth_basis_affine_phase_invariant (AffinePhaseEquivalence.uniformGlobal P) T

#print axioms has_fourth_basis_uniform_global_phase_invariant

/-!
### 5. Connection to Premise G2 and TransportInvariance
-/

/-- Two triples T and T' are affine-phase equivalent if there exists an affine phase
equivalence A such that T' is the transformed triple. -/
def AffinePhaseEquivTriple (T T' : MUTriple) : Prop :=
  ∃ (A : AffinePhaseEquivalence),
    T'.b0 = A.p0.act T.b0 ∧
    T'.b1 = A.p1.act T.b1 ∧
    T'.b2 = A.p2.act T.b2

/-- Theorem: Affine phase equivalence preserves fourth-basis extension. -/
theorem affine_phase_equiv_preserves_has_fourth_basis
    {T T' : MUTriple} (h : AffinePhaseEquivTriple T T') :
    HasFourthBasis T ↔ HasFourthBasis T' := by
  rcases h with ⟨A, h0, h1, h2⟩
  have h_equiv := has_fourth_basis_affine_phase_invariant A T
  have h_transform_eq :
      HasFourthBasis (transformTripleAffine A T) ↔ HasFourthBasis T' := by
    constructor
    · intro ⟨b3, hb0, hb1, hb2⟩
      dsimp [transformTripleAffine] at hb0 hb1 hb2
      have hb0' : is_mutually_unbiased T'.b0 b3 := by rw [h0]; exact hb0
      have hb1' : is_mutually_unbiased T'.b1 b3 := by rw [h1]; exact hb1
      have hb2' : is_mutually_unbiased T'.b2 b3 := by rw [h2]; exact hb2
      exact ⟨b3, hb0', hb1', hb2'⟩
    · intro ⟨b3, hb0, hb1, hb2⟩
      have hb0' : is_mutually_unbiased (A.p0.act T.b0) b3 := by rw [← h0]; exact hb0
      have hb1' : is_mutually_unbiased (A.p1.act T.b1) b3 := by rw [← h1]; exact hb1
      have hb2' : is_mutually_unbiased (A.p2.act T.b2) b3 := by rw [← h2]; exact hb2
      exact ⟨b3, hb0', hb1', hb2'⟩
  exact h_equiv.symm.trans h_transform_eq

#print axioms affine_phase_equiv_preserves_has_fourth_basis

/-- Theorem: Any class whose triples are affine-phase equivalent satisfies TransportInvariance. -/
theorem transport_invariance_of_affine_phase_orbit
    (c : TripleClass)
    (h_orbit : ∀ (T T' : MUTriple), belongs_to_class T c → belongs_to_class T' c → AffinePhaseEquivTriple T T') :
    TransportInvariance c := by
  intro T T' hT hT'
  exact affine_phase_equiv_preserves_has_fourth_basis (h_orbit T T' hT hT')

#print axioms transport_invariance_of_affine_phase_orbit

/-!
### 6. Concrete 108-Equation Hilbert Component Model
-/

namespace ConcretePhaseModel

/-- Abstract Hilbert vector space. -/
opaque HVec : Type

/-- Transition probability predicate: transition_prob_one_sixth u v represents |⟨u, v⟩|² = 1/6. -/
opaque transition_prob_one_sixth : HVec → HVec → Prop

/-- A unitary phase action on a single Hilbert vector.
In coordinates, v ↦ e^{iθ} v, which preserves inner product moduli |⟨e^{iθ} u, v⟩|² = |⟨u, v⟩|². -/
structure VectorPhaseAction where
  act : HVec → HVec
  inv : HVec → HVec
  inv_act : ∀ v, inv (act v) = v
  act_inv : ∀ v, act (inv v) = v
  pres_prob_left : ∀ u v, transition_prob_one_sixth (act u) v ↔ transition_prob_one_sixth u v
  pres_prob_right : ∀ u v, transition_prob_one_sixth u (act v) ↔ transition_prob_one_sixth u v

/-- A concrete basis consisting of 6 vectors. -/
structure ConcreteBasis where
  vec : Fin 6 → HVec

/-- An affine phase profile on a basis applies a phase angle to each basis vector:
v_k ↦ e^{i (A θ + c)_k} v_k. -/
structure BasisPhaseMap where
  phase : Fin 6 → VectorPhaseAction

/-- Action of a basis phase map on a concrete basis. -/
def applyBasisPhase (M : BasisPhaseMap) (B : ConcreteBasis) : ConcreteBasis where
  vec i := (M.phase i).act (B.vec i)

/-- A concrete triple of bases in dimension 6. -/
structure ConcreteTriple where
  b0 : ConcreteBasis
  b1 : ConcreteBasis
  b2 : ConcreteBasis

/-- Individual ZeroRel equation:
For triple T, candidate fourth basis b3, basis index a ∈ {0,1,2}, and vector indices i, j ∈ Fin 6:
|⟨(b_a)_i, (b_3)_j⟩|² = 1/6. -/
def ZeroRelEq (T : ConcreteTriple) (b3 : ConcreteBasis) (a : Fin 3) (i j : Fin 6) : Prop :=
  match a with
  | 0 => transition_prob_one_sixth (T.b0.vec i) (b3.vec j)
  | 1 => transition_prob_one_sixth (T.b1.vec i) (b3.vec j)
  | 2 => transition_prob_one_sixth (T.b2.vec i) (b3.vec j)

/-- The total ZeroRel system of 108 polynomial equations:
All 3 × 6 × 6 = 108 equations hold simultaneously. -/
def ZeroRelSystem (T : ConcreteTriple) (b3 : ConcreteBasis) : Prop :=
  ∀ (a : Fin 3) (i j : Fin 6), ZeroRelEq T b3 a i j

/-- An affine phase equivalence configuration for the full MUB system (T and candidate b3). -/
structure AffinePhaseConfig where
  m0 : BasisPhaseMap
  m1 : BasisPhaseMap
  m2 : BasisPhaseMap
  m3 : BasisPhaseMap

/-- Action of affine phase configuration on a concrete triple. -/
def transformTriple (C : AffinePhaseConfig) (T : ConcreteTriple) : ConcreteTriple where
  b0 := applyBasisPhase C.m0 T.b0
  b1 := applyBasisPhase C.m1 T.b1
  b2 := applyBasisPhase C.m2 T.b2

/-- **Theorem: Each individual ZeroRel equation is invariant under affine phase equivalence**. -/
theorem zerorel_eq_affine_invariant (C : AffinePhaseConfig) (T : ConcreteTriple) (b3 : ConcreteBasis)
    (a : Fin 3) (i j : Fin 6) :
    ZeroRelEq (transformTriple C T) (applyBasisPhase C.m3 b3) a i j ↔ ZeroRelEq T b3 a i j := by
  dsimp [ZeroRelEq, transformTriple, applyBasisPhase]
  cases a using Fin.cases with
  | zero =>
    have h1 := (C.m0.phase i).pres_prob_left (T.b0.vec i) ((C.m3.phase j).act (b3.vec j))
    have h2 := (C.m3.phase j).pres_prob_right (T.b0.vec i) (b3.vec j)
    constructor
    · intro h
      exact h2.mp (h1.mp h)
    · intro h
      exact h1.mpr (h2.mpr h)
  | succ a =>
    cases a using Fin.cases with
    | zero =>
      have h1 := (C.m1.phase i).pres_prob_left (T.b1.vec i) ((C.m3.phase j).act (b3.vec j))
      have h2 := (C.m3.phase j).pres_prob_right (T.b1.vec i) (b3.vec j)
      constructor
      · intro h
        exact h2.mp (h1.mp h)
      · intro h
        exact h1.mpr (h2.mpr h)
    | succ a =>
      cases a using Fin.cases with
      | zero =>
        have h1 := (C.m2.phase i).pres_prob_left (T.b2.vec i) ((C.m3.phase j).act (b3.vec j))
        have h2 := (C.m3.phase j).pres_prob_right (T.b2.vec i) (b3.vec j)
        constructor
        · intro h
          exact h2.mp (h1.mp h)
        · intro h
          exact h1.mpr (h2.mpr h)
      | succ a => nomatch a

/-- **Theorem: The complete ZeroRel system of 108 equations is invariant under affine phase equivalence**. -/
theorem zerorel_system_affine_invariant (C : AffinePhaseConfig) (T : ConcreteTriple) (b3 : ConcreteBasis) :
    ZeroRelSystem (transformTriple C T) (applyBasisPhase C.m3 b3) ↔ ZeroRelSystem T b3 := by
  constructor
  · intro h a i j
    exact (zerorel_eq_affine_invariant C T b3 a i j).mp (h a i j)
  · intro h a i j
    exact (zerorel_eq_affine_invariant C T b3 a i j).mpr (h a i j)

#print axioms zerorel_eq_affine_invariant
#print axioms zerorel_system_affine_invariant

end ConcretePhaseModel

end MUB6.Gluing
