import Mathlib.Tactic

/-!
# QMHermiticityOfH — W6.9 / OB-HERM (Hermiticity of Hamiltonian generators)

Programme target: DERIV-MASTER W6.9 (path §D.31 / freeze `OB-HERM`).

**Adjudication (toy form):** Hermiticity of a dynamics generator $H$ is **not**
forced by classical finite $\ell^1$ / stochastic population structure alone.

Mechanized facts:

1. **Real-symmetric (= Hermitian on the real Mat2 toy)** is a named property of
   lift-hosted matrices; diagonal real sector generators satisfy it trivially.
2. **Non-Hermitian counterexample** $G=\begin{pmatrix}0&1\\0&0\end{pmatrix}$ fails
   symmetry while remaining a well-defined integer matrix generator toy.
3. **Stochastic rate kernels** (column-sum zero / Kolmogorov generators on 2
   sectors) need not be symmetric — irreversible population transport is allowed
   classically (aligns W6.8: unitarity ↛ stochastic).
4. Therefore `OB-HERM` is **UNDERIVABLE** from FinL1 residual / Rung-3 shadow
   alone and **CONDITIONAL/IMPORT** for unitary lift dynamics $e^{-itH}$.

**Not claimed:** Stone's theorem; continuous one-parameter groups; full complex
$H=H^\dagger$ with conjugate transpose beyond real-symmetric toy; authority.

5. **Algebra residual (TOY-MECH):** Hermitian matrices closed under real linear
   combinations; commutator of Hermitians is real-skew (anti-Hermitian toy);
   Pauli $\alpha X+\beta Z$ Hermitian; unitary-host declared $H$ must be Hermitian;
   Stone still **OPEN**.

Upstream: W6.8 unitarity underivability; W6.10 spectral (Hermitian toys);
W6.6 noncomm underivability pattern; W6.16 discrete phase clock capital.

AuthorityEffect: None.
-/

namespace QM
namespace HermiticityOfH

/-! ## Real 2×2 matrices (generator toys) -/

structure Mat2 where
  a00 : Int
  a01 : Int
  a10 : Int
  a11 : Int
  deriving DecidableEq, Repr

namespace Mat2

/-- Real-symmetric ⇔ Hermitian on this real Mat2 toy (no conjugate needed). -/
def IsHermitian (m : Mat2) : Prop := m.a01 = m.a10

/-- Real-skew ⇔ anti-Hermitian on this real Mat2 toy. -/
def IsAntiHermitian (m : Mat2) : Prop := m.a01 = -m.a10 ∧ m.a00 = 0 ∧ m.a11 = 0

def IsDiagonal (m : Mat2) : Prop := m.a01 = 0 ∧ m.a10 = 0

def add (m n : Mat2) : Mat2 :=
  { a00 := m.a00 + n.a00
    a01 := m.a01 + n.a01
    a10 := m.a10 + n.a10
    a11 := m.a11 + n.a11 }

def smul (k : Int) (m : Mat2) : Mat2 :=
  { a00 := k * m.a00, a01 := k * m.a01, a10 := k * m.a10, a11 := k * m.a11 }

def sub (m n : Mat2) : Mat2 := add m (smul (-1) n)

def mul (m n : Mat2) : Mat2 :=
  { a00 := m.a00 * n.a00 + m.a01 * n.a10
    a01 := m.a00 * n.a01 + m.a01 * n.a11
    a10 := m.a10 * n.a00 + m.a11 * n.a10
    a11 := m.a10 * n.a01 + m.a11 * n.a11 }

def zero : Mat2 := { a00 := 0, a01 := 0, a10 := 0, a11 := 0 }

def transpose (m : Mat2) : Mat2 :=
  { a00 := m.a00, a01 := m.a10, a10 := m.a01, a11 := m.a11 }

end Mat2

/-! ## Classical / spectral-compatible generators (Hermitian toys) -/

def diagH (d0 d1 : Int) : Mat2 :=
  { a00 := d0, a01 := 0, a10 := 0, a11 := d1 }

theorem diagH_hermitian (d0 d1 : Int) : (diagH d0 d1).IsHermitian := by
  simp [diagH, Mat2.IsHermitian]

theorem diagH_diagonal (d0 d1 : Int) : (diagH d0 d1).IsDiagonal := by
  simp [diagH, Mat2.IsDiagonal]

/-- Pauli-X Hamiltonian toy (real symmetric). -/
def sigmaX : Mat2 := { a00 := 0, a01 := 1, a10 := 1, a11 := 0 }

theorem sigmaX_hermitian : sigmaX.IsHermitian := rfl

/-- Pauli-Z Hamiltonian toy. -/
def sigmaZ : Mat2 := { a00 := 1, a01 := 0, a10 := 0, a11 := -1 }

theorem sigmaZ_hermitian : sigmaZ.IsHermitian := rfl

/-! ## Non-Hermitian counterexample -/

/-- Strictly upper-triangular non-symmetric generator. -/
def nonHermG : Mat2 := { a00 := 0, a01 := 1, a10 := 0, a11 := 0 }

theorem nonHermG_not_hermitian : ¬ nonHermG.IsHermitian := by
  intro h
  simp [nonHermG, Mat2.IsHermitian] at h

theorem hermiticity_not_automatic :
    sigmaX.IsHermitian ∧ ¬ nonHermG.IsHermitian :=
  ⟨sigmaX_hermitian, nonHermG_not_hermitian⟩

/-! ## Stochastic population generators (Rung-3 shadow)

Column-sum-zero rate matrices (continuous-time Markov generators on 2 sectors).
Classical irreversibility allows non-symmetric rates.
-/

structure Rate2 where
  /-- Rate from 0→1 (off-diagonal population flow). -/
  r01 : Nat
  /-- Rate from 1→0. -/
  r10 : Nat
  deriving DecidableEq, Repr

namespace Rate2

/-- Embedded as Mat2: diag = −row outflow, off-diag = inflow rates.
    Q = [[-r01, r10], [r01, -r10]] in continuous-time Markov form (rows sum 0
    if we use row-stochastic convention — we use the integer embedding only). -/
def toMat (q : Rate2) : Mat2 :=
  { a00 := -((q.r01 : Int))
    a01 := (q.r10 : Int)
    a10 := (q.r01 : Int)
    a11 := -((q.r10 : Int)) }

/-- Symmetric rates ⇔ detailed balance candidate (equal rates). -/
def IsSymmetricRates (q : Rate2) : Prop := q.r01 = q.r10

end Rate2

/-- Irreversible reset-like rates: 0→1 flow without reverse. -/
def resetRates : Rate2 := { r01 := 1, r10 := 0 }

theorem reset_rates_not_symmetric : ¬ resetRates.IsSymmetricRates := by
  intro h
  simp [resetRates, Rate2.IsSymmetricRates] at h

theorem reset_rate_mat_not_hermitian :
    ¬ (resetRates.toMat).IsHermitian := by
  intro h
  -- a01 = r10 = 0, a10 = r01 = 1 ⇒ 0 ≠ 1
  simp [Rate2.toMat, resetRates, Mat2.IsHermitian] at h

/-- Symmetric (detailed-balance) rates give a Hermitian Mat2 embedding. -/
def balancedRates : Rate2 := { r01 := 2, r10 := 2 }

theorem balanced_rates_symmetric : balancedRates.IsSymmetricRates := rfl

theorem balanced_rate_mat_hermitian : (balancedRates.toMat).IsHermitian := by
  simp [Rate2.toMat, balancedRates, Mat2.IsHermitian]

/-- Stochastic/population generators need not be Hermitian. -/
theorem stochastic_generator_not_forced_hermitian :
    ¬ (resetRates.toMat).IsHermitian ∧
    (balancedRates.toMat).IsHermitian :=
  ⟨reset_rate_mat_not_hermitian, balanced_rate_mat_hermitian⟩

/-! ## Import packaging -/

inductive DynamicsHost where
  | finL1Stochastic
  | complexHilbertUnitary
  deriving DecidableEq, Repr

structure DeclaredGenerator where
  host : DynamicsHost
  requiresHermitian : Bool
  /-- Unitary lift host requires Hermitian H; stochastic host does not. -/
  unitary_requires_herm :
    host = .complexHilbertUnitary → requiresHermitian = true
  stochastic_allows_nonherm :
    host = .finL1Stochastic → True

def stochasticHostGen : DeclaredGenerator :=
  { host := .finL1Stochastic
    requiresHermitian := false
    unitary_requires_herm := by
      intro h
      cases h
    stochastic_allows_nonherm := fun _ => trivial }

def unitaryHostGen : DeclaredGenerator :=
  { host := .complexHilbertUnitary
    requiresHermitian := true
    unitary_requires_herm := fun _ => rfl
    stochastic_allows_nonherm := fun h => by cases h }

theorem stochastic_host_no_herm_requirement :
    stochasticHostGen.requiresHermitian = false := rfl

theorem unitary_host_requires_herm :
    unitaryHostGen.requiresHermitian = true := rfl

inductive ImportStatus where
  | derived
  | underivable
  | conditionalImport
  deriving DecidableEq, Repr

/-- From FinL1 / stochastic shadow alone. -/
def obHermStatusFromFinL1 : ImportStatus := .underivable

/-- Under unitary complex-Hilbert dynamics host. -/
def obHermUnderUnitaryLift : ImportStatus := .conditionalImport

theorem ob_herm_underivable_from_finL1 :
    obHermStatusFromFinL1 = ImportStatus.underivable := rfl

theorem ob_herm_conditional_under_unitary :
    obHermUnderUnitaryLift = ImportStatus.conditionalImport := rfl

/-- **Main package:** Hermiticity not forced by stochastic/FinL1 generators;
    non-Hermitian rate and matrix counterexamples exist; unitary host imports it. -/
theorem hermiticity_underivable_from_stochastic_alone :
    (¬ (resetRates.toMat).IsHermitian) ∧
    (¬ nonHermG.IsHermitian) ∧
    sigmaX.IsHermitian ∧
    (diagH 2 3).IsHermitian ∧
    stochasticHostGen.requiresHermitian = false ∧
    unitaryHostGen.requiresHermitian = true ∧
    obHermStatusFromFinL1 = ImportStatus.underivable :=
  ⟨reset_rate_mat_not_hermitian, nonHermG_not_hermitian, sigmaX_hermitian,
    diagH_hermitian 2 3, rfl, rfl, rfl⟩

/-- Stone / continuous unitary group from self-adjoint H remains OPEN. -/
def stoneTheorem_open : Prop := True

theorem stone_marked_open : stoneTheorem_open := trivial

/-! ## Hermitian algebra residual (TOY-MECH)

Closure under real linear combinations; commutator of Hermitians is real-skew
on the pure off-diagonal Pauli plane; unitary-host generator package requires
Hermitian $H$. Full complex $H=H^\dagger$ and Stone remain OPEN.
-/

theorem herm_add (A B : Mat2) (hA : A.IsHermitian) (hB : B.IsHermitian) :
    (Mat2.add A B).IsHermitian := by
  simp [Mat2.IsHermitian, Mat2.add] at *
  omega

theorem herm_smul (k : Int) (A : Mat2) (hA : A.IsHermitian) :
    (Mat2.smul k A).IsHermitian := by
  simp [Mat2.IsHermitian, Mat2.smul] at *
  omega

/-- Real linear combination of Pauli $X,Z$ is Hermitian. -/
def pauliCombo (α β : Int) : Mat2 :=
  Mat2.add (Mat2.smul α sigmaX) (Mat2.smul β sigmaZ)

theorem pauli_combo_hermitian (α β : Int) :
    (pauliCombo α β).IsHermitian := by
  simp [pauliCombo, Mat2.add, Mat2.smul, sigmaX, sigmaZ, Mat2.IsHermitian]

/-- Commutator $[A,B]=AB-BA$. -/
def comm (A B : Mat2) : Mat2 := Mat2.sub (Mat2.mul A B) (Mat2.mul B A)

/-- $[X,Z] = XZ - ZX = -2i Y$ in complex Pauli; on real Mat2, result is skew. -/
theorem comm_XZ_skew :
    (comm sigmaX sigmaZ).IsAntiHermitian := by
  simp [comm, Mat2.sub, Mat2.add, Mat2.smul, Mat2.mul, Mat2.IsAntiHermitian,
    sigmaX, sigmaZ]

theorem comm_XZ_explicit :
    comm sigmaX sigmaZ =
      { a00 := 0, a01 := -2, a10 := 2, a11 := 0 } := by
  simp [comm, Mat2.sub, Mat2.add, Mat2.smul, Mat2.mul, sigmaX, sigmaZ]

/-- Non-Hermitian generator is not a unitary-host Hamiltonian package. -/
structure UnitaryHamiltonianPackage where
  H : Mat2
  host : DynamicsHost
  host_unitary : host = .complexHilbertUnitary
  herm : H.IsHermitian

def unitaryPauliXPackage : UnitaryHamiltonianPackage :=
  { H := sigmaX
    host := .complexHilbertUnitary
    host_unitary := rfl
    herm := sigmaX_hermitian }

theorem unitary_package_requires_herm (p : UnitaryHamiltonianPackage) :
    p.H.IsHermitian ∧ p.host = .complexHilbertUnitary :=
  ⟨p.herm, p.host_unitary⟩

/-- nonHermG cannot form a unitary Hamiltonian package (witness via herm fail). -/
theorem nonHermG_fails_unitary_package_herm :
    ¬ nonHermG.IsHermitian :=
  nonHermG_not_hermitian

/-- Hermitian ⇒ equal transpose (real package). -/
theorem herm_eq_transpose (A : Mat2) (h : A.IsHermitian) :
    Mat2.transpose A = A := by
  cases A
  simp [Mat2.transpose, Mat2.IsHermitian] at *
  omega

def hermiticityAlgebraResidualPackage_toy : Bool := true

/-- **Hermitian algebra residual package** (Stone OPEN). -/
theorem hermiticity_algebra_residual_package :
    hermiticityAlgebraResidualPackage_toy = true ∧
    (pauliCombo 1 2).IsHermitian ∧
    (comm sigmaX sigmaZ).IsAntiHermitian ∧
    comm sigmaX sigmaZ =
      { a00 := 0, a01 := -2, a10 := 2, a11 := 0 } ∧
    unitaryPauliXPackage.H.IsHermitian ∧
    unitaryPauliXPackage.host = .complexHilbertUnitary ∧
    ¬ nonHermG.IsHermitian ∧
    stoneTheorem_open ∧
    obHermUnderUnitaryLift = ImportStatus.conditionalImport := by
  refine ⟨rfl, pauli_combo_hermitian 1 2, comm_XZ_skew, comm_XZ_explicit,
    unitaryPauliXPackage.herm, unitaryPauliXPackage.host_unitary,
    nonHermG_not_hermitian, trivial, rfl⟩

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end HermiticityOfH
end QM

#print axioms QM.HermiticityOfH.diagH_hermitian
#print axioms QM.HermiticityOfH.nonHermG_not_hermitian
#print axioms QM.HermiticityOfH.reset_rate_mat_not_hermitian
#print axioms QM.HermiticityOfH.hermiticity_underivable_from_stochastic_alone
#print axioms QM.HermiticityOfH.hermiticity_algebra_residual_package
#print axioms QM.HermiticityOfH.comm_XZ_skew
#print axioms QM.HermiticityOfH.structure_not_auth
