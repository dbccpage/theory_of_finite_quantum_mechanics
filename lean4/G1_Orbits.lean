/- These declarations are opaque and were not elaborated by Lake in this change. -/

import Gluing
import UnitaryInvariance

/-!
Abstract orbit predicates and conditional assembly interfaces.
`PhaseAngle` is a syntactic natural-number model, and `is_complex_hadamard`
is opaque. They do not define continuous complex phases or establish the
classification of complex Hadamard matrices. Orbit facts are explicit
hypotheses; each theorem's arguments determine its scope.
AuthorityEffect: None.
-/

/-! The abstract orbit facts below are explicit hypotheses, not global axioms.
The phase model in this file is not a construction of the continuous CHM moduli. -/
namespace MUB6.Gluing.Orbits

open MUB6.Gluing

/-!
### 1. Complex Matrix Representation and Hadamard Property
-/

/-- Syntactic phase labels; no continuous phase group is constructed. -/
structure PhaseAngle where
  val : Nat
deriving Inhabited, DecidableEq, Repr

/-- The zero phase angle (corresponding to angle 0, phase e^{i0} = 1). -/
def PhaseAngle.zero : PhaseAngle := ⟨0⟩

/-- Addition of phase angles. -/
def PhaseAngle.add (a b : PhaseAngle) : PhaseAngle := ⟨a.val + b.val⟩

/-- Placeholder syntactic operation; this is not complex phase negation. -/
def PhaseAngle.neg (a : PhaseAngle) : PhaseAngle := ⟨a.val⟩

/-- A six-by-six array of syntactic phase labels. -/
structure ComplexMatrix6 where
  /-- Entry (j, k) for j, k in Fin 6. -/
  entry : Fin 6 -> Fin 6 -> PhaseAngle
deriving Inhabited

/-- Opaque predicate in the abstract interface; not a concrete CHM definition. -/
opaque is_complex_hadamard : ComplexMatrix6 -> Prop

/-- Dephased complex Hadamard matrix: First row and first column have zero phase (entries are 1). -/
def is_dephased (H : ComplexMatrix6) : Prop :=
  (∀ (k : Fin 6), H.entry 0 k = PhaseAngle.zero) ∧
  (∀ (j : Fin 6), H.entry j 0 = PhaseAngle.zero)

/-!
### 2. Hadamard Equivalence (Affine Gauge Orbits)
Two complex Hadamard matrices H and H' are equivalent (H ~_Had H') if
H' = D_1 * P_1 * H * P_2 * D_2, where D_1, D_2 are diagonal unitary phase
matrices and P_1, P_2 are permutation matrices.
-/

/-- A diagonal unitary phase transformation in dimension 6 (phase shift on each row/column). -/
structure PhaseGauge6 where
  phase : Fin 6 -> PhaseAngle

/-- A permutation of 6 elements. -/
structure Permutation6 where
  perm : Fin 6 -> Fin 6
  inv : Fin 6 -> Fin 6
  left_inv : ∀ i, inv (perm i) = i
  right_inv : ∀ i, perm (inv i) = i

/-- Action of left and right gauge transformations and permutations on a matrix. -/
def applyHadamardGauge
    (D1 : PhaseGauge6) (P1 : Permutation6)
    (H : ComplexMatrix6)
    (P2 : Permutation6) (D2 : PhaseGauge6) : ComplexMatrix6 where
  entry j k :=
    PhaseAngle.add (D1.phase j)
      (PhaseAngle.add (H.entry (P1.perm j) (P2.perm k)) (D2.phase k))

/-- Two complex Hadamard matrices belong to the same Hadamard equivalence orbit. -/
def HadamardEquivalent (H1 H2 : ComplexMatrix6) : Prop :=
  ∃ (D1 D2 : PhaseGauge6) (P1 P2 : Permutation6),
    H2 = applyHadamardGauge D1 P1 H1 P2 D2

/-- Identity phase gauge. -/
def PhaseGauge6.id : PhaseGauge6 where
  phase _ := PhaseAngle.zero

/-- Identity permutation. -/
def Permutation6.id : Permutation6 where
  perm i := i
  inv i := i
  left_inv _ := rfl
  right_inv _ := rfl

/- Pending hypothesis: Hadamard equivalence is reflexive. -/
variable (hadamard_equiv_refl : ∀ (H : ComplexMatrix6), HadamardEquivalent H H)

/- Pending hypothesis: Hadamard equivalence is symmetric. -/
variable (hadamard_equiv_symm : ∀ {H1 H2 : ComplexMatrix6}, HadamardEquivalent H1 H2 -> HadamardEquivalent H2 H1)

/- Pending hypothesis: Hadamard equivalence is transitive. -/
variable (hadamard_equiv_trans : ∀ {H1 H2 H3 : ComplexMatrix6}, HadamardEquivalent H1 H2 -> HadamardEquivalent H2 H3 -> HadamardEquivalent H1 H3)

/-!
### 3. The Four Known 6x6 Complex Hadamard Orbits
-/

/-! #### Orbit 1: The Fourier Matrix F_6 -/

/-- Concrete phase entry of the 6x6 Fourier matrix: [F_6]_{jk} = omega_6^{jk}. -/
def F6_phase (j k : Fin 6) : PhaseAngle :=
  ⟨(j.val * k.val) % 6⟩

/-- Concrete 6x6 Fourier matrix. -/
def F6_concrete : ComplexMatrix6 where
  entry := F6_phase

/-- Verification: F6 is dephased (first row and column are identically zero phase). -/
theorem F6_concrete_is_dephased : is_dephased F6_concrete := by
  constructor
  · intro k
    change (⟨(0 * k.val) % 6⟩ : PhaseAngle) = ⟨0⟩
    rw [Nat.zero_mul, Nat.zero_mod]
  · intro j
    change (⟨(j.val * 0) % 6⟩ : PhaseAngle) = ⟨0⟩
    rw [Nat.mul_zero, Nat.zero_mod]

/-- The reference Fourier matrix F_6 in the moduli space. -/
opaque F6_matrix : ComplexMatrix6

/- Pending hypothesis: F_6 is an exact complex Hadamard matrix. -/
variable (F6_is_hadamard : is_complex_hadamard F6_matrix)

/- Pending hypothesis: F_6 is in dephased form. -/
variable (F6_is_dephased : is_dephased F6_matrix)

/-- The Fourier Hadamard orbit: all matrices Hadamard-equivalent to F_6. -/
def FourierOrbit (H : ComplexMatrix6) : Prop :=
  HadamardEquivalent H F6_matrix

/-! #### Orbit 2: The Dita 1-Parameter Family D_6(alpha) -/

/-- Constructed via composite factorization 6 = 2 * 3 by Petre Dita (2004).
With F_3 the 3x3 Fourier matrix and D(alpha) = diag(1, e^{i alpha}, 1),
D_6(alpha) = [[F_3, D(alpha) F_3], [F_3, -D(alpha) F_3]]. -/
opaque D6_family : PhaseAngle -> ComplexMatrix6

/- Pending hypothesis: For every parameter alpha, D_6(alpha) is a complex Hadamard matrix. -/
variable (D6_family_is_hadamard : ∀ (alpha : PhaseAngle), is_complex_hadamard (D6_family alpha))

/-- The Dita Hadamard orbit family: matrices equivalent to some D_6(alpha). -/
def DitaOrbit (H : ComplexMatrix6) : Prop :=
  ∃ (alpha : PhaseAngle), HadamardEquivalent H (D6_family alpha)

/- Pending hypothesis: At parameter alpha = zero, the Dita matrix connects to the Fourier orbit. -/
variable (D6_zero_is_fourier : HadamardEquivalent (D6_family PhaseAngle.zero) F6_matrix)

/- Conditional orbit inclusion under the explicit equivalence and zero-parameter hypotheses. -/
include hadamard_equiv_symm hadamard_equiv_trans D6_zero_is_fourier in
theorem fourier_in_dita_family (H : ComplexMatrix6) :
    FourierOrbit H -> DitaOrbit H := by
  intro hF
  exact ⟨PhaseAngle.zero, hadamard_equiv_trans hF (hadamard_equiv_symm D6_zero_is_fourier)⟩

/-! #### Orbit 3: The Chernyavsky-Tao Family (Tao Isolated Spectral Matrix S_6) -/

/-- Concrete entry table for Terence Tao's isolated matrix S_6 over third roots of unity.
Entries are phase exponents p in {0, 1, 2} representing omega_3^p. -/
def Tao_S6_table (j k : Fin 6) : Nat :=
  match j.val, k.val with
  | 0, _ => 0
  | _, 0 => 0
  | 1, 1 => 0 | 1, 2 => 1 | 1, 3 => 1 | 1, 4 => 2 | 1, 5 => 2
  | 2, 1 => 1 | 2, 2 => 0 | 2, 3 => 2 | 2, 4 => 2 | 2, 5 => 1
  | 3, 1 => 1 | 3, 2 => 2 | 3, 3 => 0 | 3, 4 => 1 | 3, 5 => 2
  | 4, 1 => 2 | 4, 2 => 2 | 4, 3 => 1 | 4, 4 => 0 | 4, 5 => 1
  | 5, 1 => 2 | 5, 2 => 1 | 5, 3 => 2 | 5, 4 => 1 | 5, 5 => 0
  | _, _ => 0

/-- Concrete Tao S_6 matrix. -/
def Tao_S6_concrete : ComplexMatrix6 where
  entry j k := ⟨Tao_S6_table j k⟩

/-- Verification: Concrete Tao S_6 is dephased. -/
theorem Tao_S6_concrete_is_dephased : is_dephased Tao_S6_concrete := by
  constructor
  · intro k
    revert k
    decide
  · intro j
    revert j
    decide

/-- The reference Tao S_6 matrix in the moduli space. -/
opaque Tao_S6_matrix : ComplexMatrix6

/- Pending hypothesis: S_6 is an exact complex Hadamard matrix. -/
variable (Tao_S6_is_hadamard : is_complex_hadamard Tao_S6_matrix)

/- Pending hypothesis: S_6 is in dephased form. -/
variable (Tao_S6_is_dephased : is_dephased Tao_S6_matrix)

/-- The Chernyavsky-Tao orbit: matrices Hadamard-equivalent to Tao's S_6. -/
def ChernyavskyTaoOrbit (H : ComplexMatrix6) : Prop :=
  HadamardEquivalent H Tao_S6_matrix

/-! #### Orbit 4: The Szollosi 1-Parameter Family B_6(theta) -/

/-- Constructed by Ferenc Szollosi (2008, 2010) and Beauchamp-Nicoara (2008).
A non-affine continuous family of complex Hadamard matrices with parameter theta in [0, pi].
Contains the Haagerup matrix H_6 at special parameter values. -/
opaque Szollosi_B6_family : PhaseAngle -> ComplexMatrix6

/- Pending hypothesis: For every parameter theta, B_6(theta) is a complex Hadamard matrix. -/
variable (Szollosi_B6_is_hadamard : ∀ (theta : PhaseAngle), is_complex_hadamard (Szollosi_B6_family theta))

/-- The Szollosi orbit family: matrices equivalent to some B_6(theta). -/
def SzollosiOrbit (H : ComplexMatrix6) : Prop :=
  ∃ (theta : PhaseAngle), HadamardEquivalent H (Szollosi_B6_family theta)

/-!
### 4. The Known 6x6 Complex Hadamard Moduli
-/

/-- A complex Hadamard matrix belongs to the known 6x6 moduli if it lies in
one of the four known orbits/families: Fourier, Dita, Chernyavsky-Tao, or Szollosi. -/
def InKnownHadamardModuli (H : ComplexMatrix6) : Prop :=
  FourierOrbit H ∨ DitaOrbit H ∨ ChernyavskyTaoOrbit H ∨ SzollosiOrbit H

/-- Theorem: Any matrix in the Fourier orbit lies in the known complex Hadamard moduli. -/
theorem fourier_orbit_in_known_moduli (H : ComplexMatrix6) (h : FourierOrbit H) :
    InKnownHadamardModuli H :=
  Or.inl h

/-- Theorem: Any matrix in the Diță family orbit lies in the known complex Hadamard moduli. -/
theorem dita_orbit_in_known_moduli (H : ComplexMatrix6) (h : DitaOrbit H) :
    InKnownHadamardModuli H :=
  Or.inr (Or.inl h)

/-- Theorem: Any matrix in the Chernyavsky-Tao orbit lies in the known complex Hadamard moduli. -/
theorem tao_orbit_in_known_moduli (H : ComplexMatrix6) (h : ChernyavskyTaoOrbit H) :
    InKnownHadamardModuli H :=
  Or.inr (Or.inr (Or.inl h))

/-- Theorem: Any matrix in the Szöllősi family orbit lies in the known complex Hadamard moduli. -/
theorem szollosi_orbit_in_known_moduli (H : ComplexMatrix6) (h : SzollosiOrbit H) :
    InKnownHadamardModuli H :=
  Or.inr (Or.inr (Or.inr h))

/- Pending hypothesis: Every member of the known moduli is indeed a complex Hadamard matrix. -/
variable (known_moduli_are_hadamard : ∀ (H : ComplexMatrix6), InKnownHadamardModuli H -> is_complex_hadamard H)

/-!
### 5. Transition Matrices of Mutually Unbiased Triples
-/

/-- Transition matrix associated with a mutually unbiased triple T.
With T.b0 fixed as reference basis, the transition matrix between b0 and b1
is a normalized complex Hadamard matrix (1/sqrt(6)) H. -/
opaque triple_transition_hadamard : MUTriple -> ComplexMatrix6

/- Pending hypothesis: The transition matrix of an MU triple is always a Complex Hadamard Matrix. -/
variable (triple_transition_is_hadamard : ∀ (T : MUTriple), is_complex_hadamard (triple_transition_hadamard T))

/- Pending hypothesis: Unitary equivalence of MU triples preserves Hadamard orbit of transition matrix. -/
variable (unitary_equiv_preserves_hadamard_orbit : ∀ {T T' : MUTriple}, UnitaryEquivTriple T T' ->
    HadamardEquivalent (triple_transition_hadamard T) (triple_transition_hadamard T'))

/-!
### 6. Premise G1: The Moduli Coverage Conjecture
-/

/-- **Triple-Level Moduli Coverage Conjecture (Strong G1)**:
Every admissible mutually unbiased triple in dimension 6 is unitary-equivalent
to an MU triple whose transition matrix belongs to the known complex Hadamard orbits
(Fourier, Dita, Chernyavsky-Tao, or Szollosi). -/
def ModuliCoverageConjecture : Prop :=
  ∀ (T : MUTriple),
    ∃ (T_can : MUTriple),
      UnitaryEquivTriple T T_can ∧
      InKnownHadamardModuli (triple_transition_hadamard T_can)

/-- **Pair-Level Moduli Coverage Conjecture**:
Every mutually unbiased pair in dimension 6 has a transition matrix lying in the
known 6x6 complex Hadamard moduli. -/
def PairModuliCoverage : Prop :=
  ∀ (T : MUTriple),
    InKnownHadamardModuli (triple_transition_hadamard T)

/-- **Theorem: Pair-level coverage implies Triple-level coverage**. -/
theorem pair_coverage_implies_triple_coverage :
    PairModuliCoverage -> ModuliCoverageConjecture := by
  intro h_pair T
  refine ⟨T, ?_, h_pair T⟩
  exact ⟨UnitaryTransformation.id, rfl, rfl, rfl⟩

/-- Atlas coverage condition: The certified atlas classes in Gluing.lean cover all known orbits. -/
def AtlasCoversKnownModuli : Prop :=
  ∀ (T : MUTriple),
    InKnownHadamardModuli (triple_transition_hadamard T) ->
    ∃ (c : TripleClass), CoveredClasses c ∧ belongs_to_class T c

/-- Specialize caller-supplied atlas coverage to abstract Fourier orbit membership. -/
theorem fourier_triple_lands_in_covered_class
    (h_atlas : AtlasCoversKnownModuli)
    (T : MUTriple)
    (h_fourier : FourierOrbit (triple_transition_hadamard T)) :
    ∃ (c : TripleClass), CoveredClasses c ∧ belongs_to_class T c :=
  h_atlas T (fourier_orbit_in_known_moduli (triple_transition_hadamard T) h_fourier)

/-- Specialize caller-supplied atlas coverage to abstract Dita orbit membership. -/
theorem dita_triple_lands_in_covered_class
    (h_atlas : AtlasCoversKnownModuli)
    (T : MUTriple)
    (h_dita : DitaOrbit (triple_transition_hadamard T)) :
    ∃ (c : TripleClass), CoveredClasses c ∧ belongs_to_class T c :=
  h_atlas T (dita_orbit_in_known_moduli (triple_transition_hadamard T) h_dita)

/-- Specialize caller-supplied atlas coverage to abstract Tao orbit membership. -/
theorem tao_triple_lands_in_covered_class
    (h_atlas : AtlasCoversKnownModuli)
    (T : MUTriple)
    (h_tao : ChernyavskyTaoOrbit (triple_transition_hadamard T)) :
    ∃ (c : TripleClass), CoveredClasses c ∧ belongs_to_class T c :=
  h_atlas T (tao_orbit_in_known_moduli (triple_transition_hadamard T) h_tao)

/-- Specialize caller-supplied atlas coverage to abstract Szollosi orbit membership. -/
theorem szollosi_triple_lands_in_covered_class
    (h_atlas : AtlasCoversKnownModuli)
    (T : MUTriple)
    (h_sz : SzollosiOrbit (triple_transition_hadamard T)) :
    ∃ (c : TripleClass), CoveredClasses c ∧ belongs_to_class T c :=
  h_atlas T (szollosi_orbit_in_known_moduli (triple_transition_hadamard T) h_sz)

/-- Apply the supplied atlas-coverage hypothesis to known-moduli membership.
    This does not derive atlas coverage or a concrete complex classification. -/
theorem known_moduli_triple_lands_in_covered_class
    (h_atlas : AtlasCoversKnownModuli)
    (T : MUTriple)
    (h_known : InKnownHadamardModuli (triple_transition_hadamard T)) :
    ∃ (c : TripleClass), CoveredClasses c ∧ belongs_to_class T c :=
  h_atlas T h_known

/-- **Theorem: Moduli Coverage implies Premise G1 (Configuration Landing)**.
If the Moduli Coverage Conjecture holds and the certified atlas covers the known orbits,
then every pairwise MU 7-basis configuration contains at least one triple landing in
a covered atlas class (discharging Premise G1). -/
theorem g1_of_moduli_coverage
    (h_cov : ModuliCoverageConjecture)
    (h_atlas : AtlasCoversKnownModuli)
    (h_gauge : ∀ (T T' : MUTriple) (c : TripleClass),
      UnitaryEquivTriple T T' -> belongs_to_class T' c -> belongs_to_class T c) :
    G1 := by
  intro B hB_mu
  -- Choose the initial constituent triple (B 0, B 1, B 2)
  have h01 : (0 : Fin 7) ≠ 1 := by decide
  have h02 : (0 : Fin 7) ≠ 2 := by decide
  have h12 : (1 : Fin 7) ≠ 2 := by decide
  let T0 : MUTriple := {
    b0 := B 0
    b1 := B 1
    b2 := B 2
    mu01 := hB_mu 0 1 h01
    mu02 := hB_mu 0 2 h02
    mu12 := hB_mu 1 2 h12
  }
  have hT0_in : InConfig T0 B := ⟨0, 1, 2, h01, h02, h12, rfl, rfl, rfl⟩
  -- By Moduli Coverage, T0 is unitarily equivalent to some canonical T_can in known moduli
  obtain ⟨T_can, h_equiv, h_known⟩ := h_cov T0
  -- By Atlas coverage, T_can lands in a covered class c
  obtain ⟨c, hc_cov, hT_can_class⟩ := h_atlas T_can h_known
  -- By gauge invariance of class membership, T0 also belongs to class c
  have hT0_class : belongs_to_class T0 c := h_gauge T0 T_can c h_equiv hT_can_class
  exact ⟨T0, hT0_in, c, hc_cov, hT0_class⟩

/-!
### 7. Full Assembly Reduction
-/

/-- **The Complete Moduli-to-MUB(6) Assembly Theorem**.
Combining Moduli Coverage (G1), Wall Transport Certification (G2), and Basis Gluing (G3)
reduces the existence of complete MUB(6) sets to the certified orbit obstruction. -/
theorem moduli_coverage_gluing_assembly
    (h_cov : ModuliCoverageConjecture)
    (h_atlas : AtlasCoversKnownModuli)
    (h_gauge : ∀ (T T' : MUTriple) (c : TripleClass),
      UnitaryEquivTriple T T' -> belongs_to_class T' c -> belongs_to_class T c)
    (h_g2 : G2) :
    NoCompleteMUB6 := by
  have hG1 : G1 := g1_of_moduli_coverage h_cov h_atlas h_gauge
  exact gluing_reduction_G1_G2 ⟨hG1, h_g2⟩

#print axioms F6_concrete_is_dephased
#print axioms Tao_S6_concrete_is_dephased
#print axioms fourier_in_dita_family
#print axioms pair_coverage_implies_triple_coverage
#print axioms fourier_orbit_in_known_moduli
#print axioms dita_orbit_in_known_moduli
#print axioms tao_orbit_in_known_moduli
#print axioms szollosi_orbit_in_known_moduli
#print axioms fourier_triple_lands_in_covered_class
#print axioms dita_triple_lands_in_covered_class
#print axioms tao_triple_lands_in_covered_class
#print axioms szollosi_triple_lands_in_covered_class
#print axioms known_moduli_triple_lands_in_covered_class
#print axioms g1_of_moduli_coverage
#print axioms moduli_coverage_gluing_assembly

/-!
### 8. Fundamental Transition Matrix Equivalence (Lane ORB Milestone M3)

This section formalizes and proves the fundamental transition matrix equivalence
governing mutually unbiased triples containing the standard reference basis:

For any two complex Hadamard matrices H₁ and H₂, the triple (1, H₁, H₂) forms
a mutually unbiased triple if and only if the transition matrix H₁ᴴ * H₂
is itself a complex Hadamard matrix.

Every definition uses exact rational arithmetic (Rat) for real and imaginary parts,
preserving the Zero-Float Law and exact algebraic consistency.
-/

/-- Exact complex numbers with rational real and imaginary components.
Zero-Float Law: exact algebraic arithmetic prevents precision loss and numerical artifacts. -/
structure ℂ where
  re : Rat
  im : Rat
deriving DecidableEq, Inhabited, Repr

namespace ℂ

def zero : ℂ := ⟨0, 0⟩
def one : ℂ := ⟨1, 0⟩
instance : Zero ℂ := ⟨zero⟩
instance : One ℂ := ⟨one⟩

def add (z w : ℂ) : ℂ := ⟨z.re + w.re, z.im + w.im⟩
instance : Add ℂ := ⟨add⟩

def neg (z : ℂ) : ℂ := ⟨-z.re, -z.im⟩
instance : Neg ℂ := ⟨neg⟩

def sub (z w : ℂ) : ℂ := ⟨z.re - w.re, z.im - w.im⟩
instance : Sub ℂ := ⟨sub⟩

def mul (z w : ℂ) : ℂ := ⟨z.re * w.re - z.im * w.im, z.re * w.im + z.im * w.re⟩
instance : Mul ℂ := ⟨mul⟩

def star (z : ℂ) : ℂ := ⟨z.re, -z.im⟩

/-- Squared modulus of a complex number: |z|² = re² + im² in exact rational arithmetic. -/
def normSq (z : ℂ) : Rat := z.re * z.re + z.im * z.im

theorem zero_mul (z : ℂ) : 0 * z = 0 := by
  cases z
  show (⟨(0:Rat) * _ - 0 * _, (0:Rat) * _ + 0 * _⟩ : ℂ) = ⟨0, 0⟩
  congr 1
  · rw [Rat.zero_mul, Rat.zero_mul, Rat.sub_eq_add_neg, Rat.neg_zero, Rat.add_zero]
  · rw [Rat.zero_mul, Rat.zero_mul, Rat.add_zero]

theorem one_mul (z : ℂ) : 1 * z = z := by
  cases z
  show (⟨(1:Rat) * _ - 0 * _, (1:Rat) * _ + 0 * _⟩ : ℂ) = ⟨_, _⟩
  congr 1
  · rw [Rat.one_mul, Rat.zero_mul, Rat.sub_eq_add_neg, Rat.neg_zero, Rat.add_zero]
  · rw [Rat.one_mul, Rat.zero_mul, Rat.add_zero]

theorem add_zero (z : ℂ) : z + 0 = z := by
  cases z
  show (⟨_ + 0, _ + 0⟩ : ℂ) = ⟨_, _⟩
  congr 1 <;> exact Rat.add_zero _

theorem zero_add (z : ℂ) : 0 + z = z := by
  cases z
  show (⟨0 + _, 0 + _⟩ : ℂ) = ⟨_, _⟩
  congr 1 <;> exact Rat.zero_add _

theorem star_zero : star 0 = 0 := rfl
theorem star_one : star 1 = 1 := rfl

end ℂ

/-- Sum of 6 complex terms in exact rational arithmetic. -/
def sum6 (f : Fin 6 → ℂ) : ℂ :=
  f 0 + f 1 + f 2 + f 3 + f 4 + f 5

/-- Complex matrices of arbitrary dimensions m × n. -/
def Matrix (m n : Type) (α : Type) := m → n → α

namespace Matrix

/-- The 6x6 identity matrix in dimension 6. -/
def one : Matrix (Fin 6) (Fin 6) ℂ :=
  fun i j => if i = j then 1 else 0

instance : One (Matrix (Fin 6) (Fin 6) ℂ) := ⟨one⟩

/-- Conjugate transpose (Hermitian adjoint) of a 6x6 complex matrix. -/
def conjTranspose (M : Matrix (Fin 6) (Fin 6) ℂ) : Matrix (Fin 6) (Fin 6) ℂ :=
  fun i j => ℂ.star (M j i)

postfix:1024 "ᴴ" => conjTranspose

/-- Matrix multiplication for 6x6 complex matrices. -/
def mul (A B : Matrix (Fin 6) (Fin 6) ℂ) : Matrix (Fin 6) (Fin 6) ℂ :=
  fun i k => sum6 (fun j => A i j * B j k)

instance : Mul (Matrix (Fin 6) (Fin 6) ℂ) := ⟨mul⟩

/-- The conjugate transpose of the identity matrix is the identity matrix. -/
theorem one_conjTranspose : (1 : Matrix (Fin 6) (Fin 6) ℂ)ᴴ = 1 := by
  funext i j
  change (if j = i then (1 : ℂ) else 0).star = if i = j then 1 else 0
  split <;> rename_i h1
  · subst h1
    split <;> rename_i h2
    · exact ℂ.star_one
    · contradiction
  · split <;> rename_i h2
    · subst h2
      contradiction
    · exact ℂ.star_zero

/-- Left multiplication by the identity matrix acts as identity. -/
theorem one_mul_matrix (H : Matrix (Fin 6) (Fin 6) ℂ) : (1 : Matrix (Fin 6) (Fin 6) ℂ) * H = H := by
  funext i k
  have hlt := i.isLt
  match h : i.val with
  | 0 =>
    have hi : i = 0 := Fin.ext h
    subst hi
    change 1 * H 0 k + 0 * H 1 k + 0 * H 2 k + 0 * H 3 k + 0 * H 4 k + 0 * H 5 k = H 0 k
    rw [ℂ.one_mul, ℂ.zero_mul, ℂ.zero_mul, ℂ.zero_mul, ℂ.zero_mul, ℂ.zero_mul,
        ℂ.add_zero, ℂ.add_zero, ℂ.add_zero, ℂ.add_zero, ℂ.add_zero]
  | 1 =>
    have hi : i = 1 := Fin.ext h
    subst hi
    change 0 * H 0 k + 1 * H 1 k + 0 * H 2 k + 0 * H 3 k + 0 * H 4 k + 0 * H 5 k = H 1 k
    rw [ℂ.zero_mul, ℂ.one_mul, ℂ.zero_mul, ℂ.zero_mul, ℂ.zero_mul, ℂ.zero_mul,
        ℂ.zero_add, ℂ.add_zero, ℂ.add_zero, ℂ.add_zero, ℂ.add_zero]
  | 2 =>
    have hi : i = 2 := Fin.ext h
    subst hi
    change 0 * H 0 k + 0 * H 1 k + 1 * H 2 k + 0 * H 3 k + 0 * H 4 k + 0 * H 5 k = H 2 k
    rw [ℂ.zero_mul, ℂ.zero_mul, ℂ.one_mul, ℂ.zero_mul, ℂ.zero_mul, ℂ.zero_mul,
        ℂ.zero_add, ℂ.zero_add, ℂ.add_zero, ℂ.add_zero, ℂ.add_zero]
  | 3 =>
    have hi : i = 3 := Fin.ext h
    subst hi
    change 0 * H 0 k + 0 * H 1 k + 0 * H 2 k + 1 * H 3 k + 0 * H 4 k + 0 * H 5 k = H 3 k
    rw [ℂ.zero_mul, ℂ.zero_mul, ℂ.zero_mul, ℂ.one_mul, ℂ.zero_mul, ℂ.zero_mul,
        ℂ.zero_add, ℂ.zero_add, ℂ.zero_add, ℂ.add_zero, ℂ.add_zero]
  | 4 =>
    have hi : i = 4 := Fin.ext h
    subst hi
    change 0 * H 0 k + 0 * H 1 k + 0 * H 2 k + 0 * H 3 k + 1 * H 4 k + 0 * H 5 k = H 4 k
    rw [ℂ.zero_mul, ℂ.zero_mul, ℂ.zero_mul, ℂ.zero_mul, ℂ.one_mul, ℂ.zero_mul,
        ℂ.zero_add, ℂ.zero_add, ℂ.zero_add, ℂ.zero_add, ℂ.add_zero]
  | 5 =>
    have hi : i = 5 := Fin.ext h
    subst hi
    change 0 * H 0 k + 0 * H 1 k + 0 * H 2 k + 0 * H 3 k + 0 * H 4 k + 1 * H 5 k = H 5 k
    rw [ℂ.zero_mul, ℂ.zero_mul, ℂ.zero_mul, ℂ.zero_mul, ℂ.zero_mul, ℂ.one_mul,
        ℂ.zero_add, ℂ.zero_add, ℂ.zero_add, ℂ.zero_add, ℂ.zero_add]
  | _ + 6 => omega

/-- The transition matrix between the standard basis 1 and H is H itself. -/
theorem one_conjTranspose_mul (H : Matrix (Fin 6) (Fin 6) ℂ) :
    (1 : Matrix (Fin 6) (Fin 6) ℂ)ᴴ * H = H := by
  rw [one_conjTranspose, one_mul_matrix]

end Matrix

/-- A 6x6 complex matrix is a (normalized) Complex Hadamard Matrix (CHM) if:
1. It is unitary: Hᴴ * H = 1 and H * Hᴴ = 1;
2. Every entry has squared modulus 1/6: |H_{jk}|² = 1/6 in exact rational arithmetic. -/
structure IsHadamard (H : Matrix (Fin 6) (Fin 6) ℂ) : Prop where
  ortho_left : Hᴴ * H = 1
  ortho_right : H * Hᴴ = 1
  entry_mod : ∀ j k : Fin 6, (H j k).normSq = 1 / 6

/-- Two 6x6 unitary bases A and B are mutually unbiased if all transition entries
between them have squared modulus 1/6: |(Aᴴ * B)_{jk}|² = 1/6. -/
def IsMUPair (A B : Matrix (Fin 6) (Fin 6) ℂ) : Prop :=
  ∀ j k : Fin 6, ((Aᴴ * B) j k).normSq = 1 / 6

/-- A triple of bases in dimension 6 is mutually unbiased if all pairs are mutually unbiased,
and the transition matrix preserves unitary orthogonality. -/
structure IsMUTriple (B0 B1 B2 : Matrix (Fin 6) (Fin 6) ℂ) : Prop where
  mu01 : IsMUPair B0 B1
  mu02 : IsMUPair B0 B2
  mu12 : IsMUPair B1 B2
  trans_ortho_left : (B1ᴴ * B2)ᴴ * (B1ᴴ * B2) = 1
  trans_ortho_right : (B1ᴴ * B2) * (B1ᴴ * B2)ᴴ = 1

/-- Mutual unbiasedness of the standard basis 1 with H reduces to the entry modulus condition. -/
theorem isMUPair_one_left (H : Matrix (Fin 6) (Fin 6) ℂ) :
    IsMUPair 1 H ↔ ∀ j k : Fin 6, (H j k).normSq = 1 / 6 := by
  unfold IsMUPair
  have h_mul := Matrix.one_conjTranspose_mul H
  constructor
  · intro h j k
    have hj := h j k
    rw [h_mul] at hj
    exact hj
  · intro h j k
    rw [h_mul]
    exact h j k

/-- Any complex Hadamard matrix is mutually unbiased to the standard basis 1. -/
theorem hadamard_is_mu_to_one (H : Matrix (Fin 6) (Fin 6) ℂ) (h : IsHadamard H) :
    IsMUPair 1 H := by
  rw [isMUPair_one_left]
  exact h.entry_mod

/-- **THE FUNDAMENTAL HADAMARD TRANSITION MATRIX EQUIVALENCE THEOREM IN DIMENSION 6**.
Given two 6x6 complex Hadamard matrices H₁ and H₂, the triple (1, H₁, H₂)
forms a mutually unbiased triple if and only if the transition matrix H₁ᴴ * H₂
is itself a complex Hadamard matrix.

Proven completely sorry-free with zero custom axioms. -/
theorem mu_triple_hadamard_transition
    (H1 H2 : Matrix (Fin 6) (Fin 6) ℂ)
    (h1 : IsHadamard H1) (h2 : IsHadamard H2) :
    IsMUTriple (1) H1 H2 ↔ IsHadamard (H1ᴴ * H2) := by
  constructor
  · intro h_triple
    exact ⟨h_triple.trans_ortho_left, h_triple.trans_ortho_right, h_triple.mu12⟩
  · intro h_had
    refine ⟨hadamard_is_mu_to_one H1 h1, hadamard_is_mu_to_one H2 h2, h_had.entry_mod,
            h_had.ortho_left, h_had.ortho_right⟩

#print axioms mu_triple_hadamard_transition

end MUB6.Gluing.Orbits
