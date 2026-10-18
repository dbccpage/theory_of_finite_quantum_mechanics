import Mathlib.Tactic

/-!
# QMNoncommutativityOrigin — W6.6 / OB-NONCOMM (non-commutativity origin)

Programme target: DERIV-MASTER W6.6 (path §D.28 / freeze `OB-NONCOMM` / QM_209).

**Adjudication (toy form):** non-commutativity of observables is **not** forced by
the classical finite $\ell^1$ / diagonal sector shadow alone. Classical diagonal
observables always commute. Non-commuting pairs appear only under a **lift-hosted**
matrix algebra (Pauli $X,Z$ toy). Therefore `OB-NONCOMM` is **UNDERIVABLE** from
FinL1 residual tables alone and remains **IMPORT / CONDITIONAL** on the named
lift host (aligns W6.10 spectral host discipline).

**Not claimed:** full operator-algebra derivation from contextuality cochains;
Mermin–Peres re-proof; continuum CCR/CAR; authority; promotion.

Upstream capital (do not re-prove): W6.10 Mat2 / σ_x spectral toy; W6.3/W6.4
contextuality packaging; classical sector spectral DERIVED.

AuthorityEffect: None.
-/

namespace QM
namespace NoncommutativityOrigin

/-! ## Integer 2×2 matrices (lift-facing algebra toy) -/

structure Mat2 where
  a00 : Int
  a01 : Int
  a10 : Int
  a11 : Int
  deriving DecidableEq, Repr

namespace Mat2

def add (m n : Mat2) : Mat2 :=
  { a00 := m.a00 + n.a00
    a01 := m.a01 + n.a01
    a10 := m.a10 + n.a10
    a11 := m.a11 + n.a11 }

def smul (k : Int) (m : Mat2) : Mat2 :=
  { a00 := k * m.a00
    a01 := k * m.a01
    a10 := k * m.a10
    a11 := k * m.a11 }

def sub (m n : Mat2) : Mat2 := add m (smul (-1) n)

def mul (m n : Mat2) : Mat2 :=
  { a00 := m.a00 * n.a00 + m.a01 * n.a10
    a01 := m.a00 * n.a01 + m.a01 * n.a11
    a10 := m.a10 * n.a00 + m.a11 * n.a10
    a11 := m.a10 * n.a01 + m.a11 * n.a11 }

def zero : Mat2 := { a00 := 0, a01 := 0, a10 := 0, a11 := 0 }

def IsDiagonal (m : Mat2) : Prop := m.a01 = 0 ∧ m.a10 = 0

/-- Commutator $[A,B] = AB - BA$. -/
def commutator (A B : Mat2) : Mat2 := sub (mul A B) (mul B A)

def Commute (A B : Mat2) : Prop := commutator A B = zero

end Mat2

/-! ## Classical sector observables (FinL1 / diagonal) -/

/-- Diagonal classical observables always commute (pointwise multiplication on sectors). -/
def diagObs (d0 d1 : Int) : Mat2 :=
  { a00 := d0, a01 := 0, a10 := 0, a11 := d1 }

theorem diagObs_is_diagonal (d0 d1 : Int) : (diagObs d0 d1).IsDiagonal := by
  simp [diagObs, Mat2.IsDiagonal]

theorem diag_mul (d0 d1 e0 e1 : Int) :
    Mat2.mul (diagObs d0 d1) (diagObs e0 e1) = diagObs (d0 * e0) (d1 * e1) := by
  simp [Mat2.mul, diagObs]

/-- Any two diagonal observables commute. -/
theorem diagonal_observables_commute (d0 d1 e0 e1 : Int) :
    Mat2.Commute (diagObs d0 d1) (diagObs e0 e1) := by
  simp [Mat2.Commute, Mat2.commutator, Mat2.sub, Mat2.add, Mat2.smul, Mat2.mul,
    Mat2.zero, diagObs]

theorem classical_diag_pair_commutes :
    Mat2.Commute (diagObs 2 3) (diagObs 1 4) :=
  diagonal_observables_commute 2 3 1 4

/-- Classical FinL1 sector functions induce only diagonal matrix readouts. -/
structure ClassicalSectorReadout where
  d0 : Int
  d1 : Int
  off : Int := 0
  off_zero : off = 0 := by rfl

def classicalToMat (c : ClassicalSectorReadout) : Mat2 :=
  diagObs c.d0 c.d1

theorem classical_readout_commutes (c₁ c₂ : ClassicalSectorReadout) :
    Mat2.Commute (classicalToMat c₁) (classicalToMat c₂) := by
  simp [classicalToMat, diagonal_observables_commute]

/-! ## Lift-hosted Pauli pair (non-commuting) -/

def sigmaX : Mat2 := { a00 := 0, a01 := 1, a10 := 1, a11 := 0 }
def sigmaZ : Mat2 := { a00 := 1, a01 := 0, a10 := 0, a11 := -1 }

theorem sigmaX_not_diagonal : ¬ sigmaX.IsDiagonal := by
  intro h
  simp [sigmaX, Mat2.IsDiagonal] at h

theorem sigmaZ_is_diagonal : sigmaZ.IsDiagonal := by
  simp [sigmaZ, Mat2.IsDiagonal]

theorem sigmaX_sigmaZ_products :
    Mat2.mul sigmaX sigmaZ = { a00 := 0, a01 := -1, a10 := 1, a11 := 0 } ∧
    Mat2.mul sigmaZ sigmaX = { a00 := 0, a01 := 1, a10 := -1, a11 := 0 } := by
  simp [Mat2.mul, sigmaX, sigmaZ]

/-- Pauli $X,Z$ do not commute: $[X,Z] \neq 0$. -/
theorem sigmaX_sigmaZ_not_commute : ¬ Mat2.Commute sigmaX sigmaZ := by
  intro h
  simp [Mat2.Commute, Mat2.commutator, Mat2.sub, Mat2.add, Mat2.smul, Mat2.mul,
    Mat2.zero, sigmaX, sigmaZ] at h

theorem sigmaX_sigmaZ_commutator_nonzero :
    Mat2.commutator sigmaX sigmaZ ≠ Mat2.zero := by
  intro h
  have : Mat2.Commute sigmaX sigmaZ := by
    simpa [Mat2.Commute] using h
  exact sigmaX_sigmaZ_not_commute this

/-! ## Underivability packaging -/

/-- Host tag: non-commuting algebra requires a named lift host (not FinL1 alone). -/
inductive AlgebraHost where
  | finL1Classical
  | complexHilbertLift
  deriving DecidableEq, Repr

structure DeclaredObservableAlgebra where
  host : AlgebraHost
  admitsNoncommutingPair : Bool
  /-- Interface law: classical host forbids noncommuting pairs. -/
  classical_commutes :
    host = .finL1Classical → admitsNoncommutingPair = false

def classicalAlgebra : DeclaredObservableAlgebra :=
  { host := .finL1Classical
    admitsNoncommutingPair := false
    classical_commutes := fun _ => rfl }

def complexLiftAlgebra : DeclaredObservableAlgebra :=
  { host := .complexHilbertLift
    admitsNoncommutingPair := true
    classical_commutes := by
      intro h
      cases h }

theorem classical_algebra_no_noncomm :
    classicalAlgebra.admitsNoncommutingPair = false := rfl

theorem complex_algebra_admits_noncomm :
    complexLiftAlgebra.admitsNoncommutingPair = true := rfl

/-- FinL1 classical shadow only yields commuting diagonal observables. -/
theorem finL1_shadow_only_commuting :
    (∀ c₁ c₂ : ClassicalSectorReadout,
      Mat2.Commute (classicalToMat c₁) (classicalToMat c₂)) ∧
    classicalAlgebra.admitsNoncommutingPair = false :=
  ⟨classical_readout_commutes, classical_algebra_no_noncomm⟩

/-- **OB-NONCOMM underivable from FinL1 alone:** classical sector readouts always
    commute, while a non-commuting pair exists only under the lift-hosted algebra. -/
theorem noncomm_underivable_from_finL1_alone :
    (∀ c₁ c₂ : ClassicalSectorReadout,
      Mat2.Commute (classicalToMat c₁) (classicalToMat c₂)) ∧
    (¬ Mat2.Commute sigmaX sigmaZ) ∧
    classicalAlgebra.host = AlgebraHost.finL1Classical ∧
    complexLiftAlgebra.host = AlgebraHost.complexHilbertLift ∧
    classicalAlgebra.admitsNoncommutingPair = false ∧
    complexLiftAlgebra.admitsNoncommutingPair = true :=
  ⟨classical_readout_commutes, sigmaX_sigmaZ_not_commute, rfl, rfl, rfl, rfl⟩

/-- Import status packaging: not derived from residual mass; conditional on lift. -/
inductive ImportStatus where
  | derived
  | underivable
  | conditionalImport
  deriving DecidableEq, Repr

def obNoncommStatus : ImportStatus := .underivable  -- from FinL1 alone

def obNoncommUnderLift : ImportStatus := .conditionalImport

theorem ob_noncomm_status_from_finL1 :
    obNoncommStatus = ImportStatus.underivable := rfl

theorem ob_noncomm_under_lift_conditional :
    obNoncommUnderLift = ImportStatus.conditionalImport := rfl

/-- Contextuality + lift is **not** re-proved here as a derivation of $[X,Z]\neq 0$;
    the toy only separates classical commuting shadow from lift noncomm. -/
def fullContextualityDerivation_open : Prop := True

theorem contextuality_derivation_marked_open : fullContextualityDerivation_open :=
  trivial

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end NoncommutativityOrigin
end QM

#print axioms QM.NoncommutativityOrigin.diagonal_observables_commute
#print axioms QM.NoncommutativityOrigin.sigmaX_sigmaZ_not_commute
#print axioms QM.NoncommutativityOrigin.noncomm_underivable_from_finL1_alone
#print axioms QM.NoncommutativityOrigin.ob_noncomm_status_from_finL1
#print axioms QM.NoncommutativityOrigin.structure_not_auth
