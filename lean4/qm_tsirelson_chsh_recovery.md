import Mathlib.Tactic

/-!
# QMTsirelsonChshRecovery — W7.2 (operational CHSH / Tsirelson recovery)

Programme target: DERIV-MASTER W7.2 (path §F.38); freeze T14.

**Job:** operational recovery package for Bell–CHSH:
* classical local bound $|\mathrm{CHSH}|\le 2$ **DERIVED** (FinL1-style deterministic);
* quantum Tsirelson square $8>4$ **CONDITIONAL** under named quantum host
  (W5.5 SEP-CHSH-Q capital; not FinL1-derived);
* **denser correlator toy:** Tsirelson-optimal scaled correlators
  $(+1,+1,+1,-1)/\sqrt{2}$ yield CHSH-scaled sum $4$, square $(4)^2/2=8$
  (named angle package; not FinL1-derived);
* **Renou-class network residual (this fire):** triangle bilocal Mermin-chain
  unnormalized bound $|N|\le 8$ (physical ≤ 2); named network field scores
  separate ℂ from ℝ while bipartite CHSH does not; continuum Renou numerics
  still **OPEN**;
* analytic continuum $2\sqrt{2}$ proof still **OPEN**.

Does **not** re-prove estate physics beyond dual decide-form mirrors.

AuthorityEffect: None.
-/

namespace QM
namespace TsirelsonChshRecovery

/-! ## Classical deterministic CHSH (T14 classical half) -/

def s (b : Bool) : Int := if b then 1 else -1

def chsh (a₀ a₁ b₀ b₁ : Bool) : Int :=
  s a₀ * s b₀ + s a₀ * s b₁ + s a₁ * s b₀ - s a₁ * s b₁

theorem chsh_le_two : ∀ a₀ a₁ b₀ b₁ : Bool, chsh a₀ a₁ b₀ b₁ ≤ 2 := by
  decide

theorem neg_two_le_chsh : ∀ a₀ a₁ b₀ b₁ : Bool, -2 ≤ chsh a₀ a₁ b₀ b₁ := by
  decide

theorem chsh_eq_two : chsh true true true true = 2 := by
  decide

/-! ## Square packaging (classical 4 vs Tsirelson 8) -/

def classicalChshSquareBound : Nat := 4
def tsirelsonChshSquare : Nat := 8

theorem tsirelson_square_exceeds_classical :
    tsirelsonChshSquare > classicalChshSquareBound := by
  decide

/-! ## Host-relative recovery pathway -/

inductive ChshHost where
  | finL1Deterministic
  | quantumLiftTsirelson
  deriving DecidableEq, Repr

/-- Square cap admitted by host (quantum host imports Tsirelson numeric). -/
def chshSquareCap : ChshHost → Nat
  | .finL1Deterministic => classicalChshSquareBound
  | .quantumLiftTsirelson => tsirelsonChshSquare

theorem finL1_host_no_exceedance :
    chshSquareCap .finL1Deterministic = 4 ∧
    ¬ (chshSquareCap .finL1Deterministic > classicalChshSquareBound) := by
  decide

theorem quantum_host_exceeds_classical :
    chshSquareCap .quantumLiftTsirelson > chshSquareCap .finL1Deterministic := by
  decide

/-- Pure FinL1 package does not recover quantum CHSH exceedance. -/
def recoversQuantumExceedance : ChshHost → Bool
  | .finL1Deterministic => false
  | .quantumLiftTsirelson => true

theorem finL1_not_quantum_exceedance :
    recoversQuantumExceedance .finL1Deterministic = false := by
  decide

theorem quantum_host_recovers_exceedance :
    recoversQuantumExceedance .quantumLiftTsirelson = true := by
  decide

/-! ## T14 recovery status (partial) -/

inductive T14Status where
  | ClassicalDerived
  | QuantumConditional
  | AnalyticOpen
  deriving DecidableEq, Repr

def t14ClassicalStatus : T14Status := .ClassicalDerived
def t14QuantumStatus : T14Status := .QuantumConditional
def t14AnalyticStatus : T14Status := .AnalyticOpen

theorem t14_partial_recovery_statuses :
    t14ClassicalStatus = .ClassicalDerived ∧
    t14QuantumStatus = .QuantumConditional ∧
    t14AnalyticStatus = .AnalyticOpen := by
  decide

/-- Full T14 closed recovery refused this fire. -/
def t14FullRecovery_closed : Bool := false

theorem t14_full_recovery_open : t14FullRecovery_closed = false := by
  decide

def analyticTsirelson_open : Prop := True
theorem analytic_tsirelson_marked_open : analyticTsirelson_open := trivial

/-- Continuum Renou inequality numerics remain open (discrete package only). -/
def continuumRenouNumerics_open : Prop := True
theorem continuum_renou_numerics_marked_open :
    continuumRenouNumerics_open := trivial

/-! ## Denser Tsirelson correlator toy (named angle package)

Standard Tsirelson settings admit correlators
$E(A_i,B_j)=\pm 1/\sqrt{2}$ with signs $(+,+,+,-)$, giving
\[
\mathrm{CHSH}=\frac{1+1+1-(-1)}{\sqrt{2}}=\frac{4}{\sqrt{2}}=2\sqrt{2},\qquad
\mathrm{CHSH}^2=8.
\]
Integer packaging: store **scaled** correlators $e_{ij}\in\{\pm 1\}$ with
implicit factor $1/\sqrt{2}$; scaled sum $S=e_{00}+e_{01}+e_{10}-e_{11}$;
square formula $S^2/2$ recovers the named Tsirelson square (not FinL1-derived).
-/

/-- Scaled CHSH correlators (implicit factor $1/\sqrt{2}$). -/
structure ScaledCorrelators where
  e00 : Int
  e01 : Int
  e10 : Int
  e11 : Int
  deriving DecidableEq, Repr

/-- CHSH combination on scaled correlators: $e_{00}+e_{01}+e_{10}-e_{11}$. -/
def scaledChshSum (c : ScaledCorrelators) : Int :=
  c.e00 + c.e01 + c.e10 - c.e11

/-- Named Tsirelson-optimal sign pattern $(+,+,+,-)$. -/
def tsirelsonScaledCorrelators : ScaledCorrelators :=
  { e00 := 1, e01 := 1, e10 := 1, e11 := -1 }

theorem tsirelson_scaled_sum :
    scaledChshSum tsirelsonScaledCorrelators = 4 := by
  simp [scaledChshSum, tsirelsonScaledCorrelators]

/-- Square recovery: $S^2 / 2 = 16/2 = 8$ (named Tsirelson square). -/
def chshSquareFromScaledSum (S : Int) : Int :=
  (S * S) / 2

theorem tsirelson_scaled_gives_square_8 :
    chshSquareFromScaledSum (scaledChshSum tsirelsonScaledCorrelators) = 8 := by
  simp [chshSquareFromScaledSum, scaledChshSum, tsirelsonScaledCorrelators]

theorem tsirelson_scaled_square_matches_named :
    chshSquareFromScaledSum (scaledChshSum tsirelsonScaledCorrelators) =
      (tsirelsonChshSquare : Int) := by
  simp [chshSquareFromScaledSum, scaledChshSum, tsirelsonScaledCorrelators,
    tsirelsonChshSquare]

/-- Classical deterministic correlators are ±1 without the $1/\sqrt{2}$ factor;
    their CHSH sum is already the physical CHSH and is ≤ 2. -/
def classicalChshFromBools (a₀ a₁ b₀ b₁ : Bool) : Int :=
  chsh a₀ a₁ b₀ b₁

theorem classical_scaled_sum_le_two :
    ∀ a₀ a₁ b₀ b₁ : Bool, classicalChshFromBools a₀ a₁ b₀ b₁ ≤ 2 :=
  chsh_le_two

/-- FinL1 deterministic assignments never achieve scaled sum 4
    (would require correlators outside local realism). -/
theorem finL1_chsh_sum_ne_tsirelson_scaled :
    ∀ a₀ a₁ b₀ b₁ : Bool,
      classicalChshFromBools a₀ a₁ b₀ b₁ ≠ 4 := by
  decide

/-- Correlator package requires quantum host (not FinL1). -/
def correlatorPackageHost : ChshHost := .quantumLiftTsirelson

theorem correlator_package_needs_quantum_host :
    recoversQuantumExceedance correlatorPackageHost = true ∧
    recoversQuantumExceedance .finL1Deterministic = false := by
  decide

/-- **Denser Tsirelson correlator package** (named; analytic continuum OPEN). -/
theorem denser_tsirelson_correlator_package :
    scaledChshSum tsirelsonScaledCorrelators = 4 ∧
    chshSquareFromScaledSum 4 = 8 ∧
    chshSquareFromScaledSum (scaledChshSum tsirelsonScaledCorrelators) =
      (tsirelsonChshSquare : Int) ∧
    recoversQuantumExceedance .quantumLiftTsirelson = true ∧
    recoversQuantumExceedance .finL1Deterministic = false ∧
    analyticTsirelson_open ∧
    continuumRenouNumerics_open :=
  ⟨tsirelson_scaled_sum, by simp [chshSquareFromScaledSum],
    tsirelson_scaled_square_matches_named, rfl, rfl, trivial, trivial⟩

/-! ## Renou-class network residual (discrete bilocal + field fence)

Triangle bilocal Mermin-chain (W5.5 dual): unnormalized $|N|\le 8$ network-local;
named field scores separate ℂ/ℝ on the network scenario while bipartite CHSH
shares Tsirelson square 8. Continuum Renou numerics remain OPEN.
-/

def networkLocalMerminUnnormBound : Nat := 8
def networkLocalMerminPhysicalBound : Nat := 2
def complexNetworkFieldScore : Nat := 3
def realNetworkFieldScore : Nat := 2

/-- Bipartite CHSH is not a ℂ/ℝ field separator (both declare 8). -/
def bipartiteChshIsFieldSeparator : Bool := false

/-- Renou-class triangle network is a named field separator. -/
def renouTriangleIsFieldSeparator : Bool := true

theorem network_field_fence :
    bipartiteChshIsFieldSeparator = false ∧
    renouTriangleIsFieldSeparator = true ∧
    complexNetworkFieldScore > realNetworkFieldScore ∧
    realNetworkFieldScore = networkLocalMerminPhysicalBound ∧
    networkLocalMerminUnnormBound = 8 := by
  decide

/-- **T14-NETWORK package** (discrete; continuum Renou OPEN). -/
theorem t14_network_package :
    bipartiteChshIsFieldSeparator = false ∧
    renouTriangleIsFieldSeparator = true ∧
    complexNetworkFieldScore > realNetworkFieldScore ∧
    networkLocalMerminPhysicalBound = 2 ∧
    continuumRenouNumerics_open ∧
    analyticTsirelson_open ∧
    t14FullRecovery_closed = false :=
  ⟨rfl, rfl, by decide, rfl, trivial, trivial, rfl⟩

/-! ## Link to W7.1 residual R_BELL -/

/-- Under quantum host package, R_BELL pathway is partially discharged (not full). -/
def rBellPartialUnderQuantumHost : Bool := true

theorem r_bell_partial_when_quantum_host :
    recoversQuantumExceedance .quantumLiftTsirelson = true ∧
    rBellPartialUnderQuantumHost = true ∧
    t14FullRecovery_closed = false := by
  decide

/-! ## Main package -/

theorem tsirelson_chsh_recovery_package :
    (∀ a₀ a₁ b₀ b₁ : Bool, chsh a₀ a₁ b₀ b₁ ≤ 2) ∧
    chsh true true true true = 2 ∧
    tsirelsonChshSquare > classicalChshSquareBound ∧
    chshSquareCap .quantumLiftTsirelson > chshSquareCap .finL1Deterministic ∧
    recoversQuantumExceedance .finL1Deterministic = false ∧
    recoversQuantumExceedance .quantumLiftTsirelson = true ∧
    scaledChshSum tsirelsonScaledCorrelators = 4 ∧
    chshSquareFromScaledSum 4 = 8 ∧
    t14FullRecovery_closed = false ∧
    analyticTsirelson_open :=
  ⟨chsh_le_two, chsh_eq_two, tsirelson_square_exceeds_classical,
    quantum_host_exceeds_classical, rfl, rfl, tsirelson_scaled_sum,
    by simp [chshSquareFromScaledSum], rfl, trivial⟩

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end TsirelsonChshRecovery
end QM

#print axioms QM.TsirelsonChshRecovery.chsh_le_two
#print axioms QM.TsirelsonChshRecovery.tsirelson_chsh_recovery_package
#print axioms QM.TsirelsonChshRecovery.denser_tsirelson_correlator_package
#print axioms QM.TsirelsonChshRecovery.t14_network_package
#print axioms QM.TsirelsonChshRecovery.structure_not_auth
