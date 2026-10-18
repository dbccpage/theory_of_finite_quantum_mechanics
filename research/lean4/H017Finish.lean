/-
  H017Finish -- declared dispositions with theorem-bound host facts.
  AuthorityEffect: None. Candidate only. Not PROVEN.

  After drop-one (historical census at dba1434b: three classified
  lost, five OPEN necessity), this file records a later finish
  table. Each frozen extra receives a declared disposition paired
  with the narrower host fact available here. This is not an
  assumption-removal interface or a theorem that the dispositions
  are necessary. SUSY and SU(3)×SU(2)×U(1) stay unassigned. This
  is not M_n(C).

  Historical H017ExtrasDropone.dropVerdict is untouched.

  AuthorityEffect: None
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import HWKernel
import H003ReversibilityGate
import H004FreeLinearization
import H005InnerProductAdmission
import H011Circle
import H013BornPairingBoundary
import H014TensorCompositionBoundary
import H014Interface
import H015IrreversibleFork
import H015DilationCount
import H016ContinuousDynamicsFork
import H017Extras
import H017ExtrasDropone
import H017Gleason

namespace FableHilbertWalk20260819.H017Finish

open FableHilbertWalk20260819.HWKernel
open FableHilbertWalk20260819.H017Extras
open FableHilbertWalk20260819.H017ExtrasDropone

/-- Later finish label. Not dropVerdict. Not an assumption-removal
    interface. `dualOutsideLean` is a declared receipt that the
    Python dual is tests, not a Lean theorem. -/
inductive FinishFate
  | refused
  | imported
  | dualOutsideLean
  deriving DecidableEq, Repr

def finishFate : FrozenExtra → FinishFate
  | FrozenExtra.fieldC => FinishFate.refused
  | FrozenExtra.spectral => FinishFate.refused
  | FrozenExtra.gleasonUniqueness => FinishFate.imported
  | FrozenExtra.cptp => FinishFate.imported
  | FrozenExtra.uniqueTensor => FinishFate.imported
  | FrozenExtra.circle => FinishFate.imported
  | FrozenExtra.continuousTime => FinishFate.refused
  | FrozenExtra.pythonDual => FinishFate.dualOutsideLean

theorem finish_fieldC_refused :
    finishFate FrozenExtra.fieldC = FinishFate.refused ∧
      ¬ IsFieldPack gaussPack :=
  ⟨rfl, gauss_not_a_field⟩

#print axioms finish_fieldC_refused

theorem finish_spectral_refused :
    finishFate FrozenExtra.spectral = FinishFate.refused ∧
      ¬ SpectralEigenvalueExtra enumBool :=
  ⟨rfl, spectral_eigenvalue_extra_fails_on_two_label⟩

#print axioms finish_spectral_refused

/-- R7 stays imported. Cardinality failure on Bool is not Gleason. -/
theorem finish_gleason_imported :
    finishFate FrozenExtra.gleasonUniqueness = FinishFate.imported ∧
      FableHilbertWalk20260819.H013.UniquenessDischarged
          FableHilbertWalk20260819.H013.hostSupplies = false ∧
      ¬ FableHilbertWalk20260819.H017Gleason.GleasonDimAtLeastThree
          enumBool :=
  ⟨rfl,
    FableHilbertWalk20260819.H017Gleason.gleason_pack_uniqueness_still_imported.2.2.2.2.2,
    FableHilbertWalk20260819.H017Gleason.two_label_host_not_gleason_dimension⟩

#print axioms finish_gleason_imported

/-- CPTP stays imported because this host defines no channel class.
    Collapse is not reversible and has no same-basis isometry;
    identity dilations exist as Bool×Bool bijections. Those are
    narrower host facts, not obstructions to CPTP channels. -/
theorem finish_cptp_imported :
    finishFate FrozenExtra.cptp = FinishFate.imported ∧
      ¬ Nonempty (FableHilbertWalk20260819.H003.Reversible
          FableHilbertWalk20260819.H003.collapse) ∧
      (¬ ∃ U : FableHilbertWalk20260819.H004.Vec Int Bool →
            FableHilbertWalk20260819.H004.Vec Int Bool,
        (∀ u v,
          FableHilbertWalk20260819.H005.sesq
              intPack enumBool (U u) (U v) =
            FableHilbertWalk20260819.H005.sesq intPack enumBool u v) ∧
          U (FableHilbertWalk20260819.H004.delta intPack false) =
            FableHilbertWalk20260819.H004.delta intPack false ∧
          U (FableHilbertWalk20260819.H004.delta intPack true) =
            FableHilbertWalk20260819.H004.delta intPack false) ∧
      (∀ x, FableHilbertWalk20260819.H015DilationCount.dilFF.map x =
        FableHilbertWalk20260819.H015.dil1 x) :=
  ⟨rfl, FableHilbertWalk20260819.H003.collapse_not_reversible,
    FableHilbertWalk20260819.H015.collapse_no_isometry,
    FableHilbertWalk20260819.H015DilationCount.dilFF_is_dil1⟩

#print axioms finish_cptp_imported

/-- Hilbert-tensor uniqueness stays imported. The dumpRight rival
    is a rival of CombiningEmbed, not uniqueness of Hilbert tensor. -/
theorem finish_uniqueTensor_imported :
    finishFate FrozenExtra.uniqueTensor = FinishFate.imported ∧
      ¬ ∀ u v p,
        FableHilbertWalk20260819.H014Interface.dumpRight u v p =
          FableHilbertWalk20260819.H014.tensor u v p :=
  ⟨rfl, FableHilbertWalk20260819.H014Interface.dumpRight_not_tensor⟩

#print axioms finish_uniqueTensor_imported

theorem finish_circle_imported :
    finishFate FrozenExtra.circle = FinishFate.imported ∧
      ¬ FableHilbertWalk20260819.H011Circle.ConnectednessShadow
          FableHilbertWalk20260819.H011Circle.signCarrier ∧
      FableHilbertWalk20260819.H011Circle.ConnectednessShadow
        FableHilbertWalk20260819.H011Circle.gaussUnitCarrier :=
  ⟨rfl,
    FableHilbertWalk20260819.H011Circle.sign_excluded_circle_still_imported.1,
    FableHilbertWalk20260819.H011Circle.sign_excluded_circle_still_imported.2.1⟩

#print axioms finish_circle_imported

theorem finish_continuousTime_refused :
    finishFate FrozenExtra.continuousTime = FinishFate.refused ∧
      (¬ ∃ σ : Bool → Bool,
        ∀ q : Bool, σ (σ q) = FableHilbertWalk20260819.H003.toggle q) :=
  ⟨rfl, FableHilbertWalk20260819.H016.no_report_half_step⟩

#print axioms finish_continuousTime_refused

theorem finish_pythonDual_outside_lean :
    finishFate FrozenExtra.pythonDual = FinishFate.dualOutsideLean :=
  rfl

#print axioms finish_pythonDual_outside_lean

/-! ## Physics names. Declared assignment table, not a derivation. -/

inductive PhysicsName
  | superposition
  | entanglement
  | mixingLeftover
  | susy
  | standardModelGauge
  deriving DecidableEq, Repr

def assigned : PhysicsName → Bool
  | PhysicsName.superposition => true
  | PhysicsName.entanglement => true
  | PhysicsName.mixingLeftover => true
  | PhysicsName.susy => false
  | PhysicsName.standardModelGauge => false

theorem susy_unassigned : assigned PhysicsName.susy = false :=
  rfl

#print axioms susy_unassigned

theorem standard_model_gauge_unassigned :
    assigned PhysicsName.standardModelGauge = false :=
  rfl

#print axioms standard_model_gauge_unassigned

theorem assigned_leftovers_are_the_three :
    assigned PhysicsName.superposition = true ∧
      assigned PhysicsName.entanglement = true ∧
      assigned PhysicsName.mixingLeftover = true :=
  ⟨rfl, rfl, rfl⟩

#print axioms assigned_leftovers_are_the_three

/-- Punchline: each frozen extra has a declared finish fate paired
    with a narrower host theorem or a dual-outside-Lean receipt.
    This is not a requirements or necessity theorem. SUSY and the
    Standard Model gauge group stay unassigned. This is not
    ordinary M_n(C). Historical drop-one OPEN verdicts at dba1434b
    are not rewritten. -/
theorem remaining_import_list :
    (finishFate FrozenExtra.fieldC = FinishFate.refused ∧
      ¬ IsFieldPack gaussPack) ∧
      (finishFate FrozenExtra.spectral = FinishFate.refused ∧
        ¬ SpectralEigenvalueExtra enumBool) ∧
      (finishFate FrozenExtra.gleasonUniqueness = FinishFate.imported ∧
        FableHilbertWalk20260819.H013.UniquenessDischarged
            FableHilbertWalk20260819.H013.hostSupplies = false) ∧
      (finishFate FrozenExtra.cptp = FinishFate.imported ∧
        ¬ Nonempty (FableHilbertWalk20260819.H003.Reversible
            FableHilbertWalk20260819.H003.collapse) ∧
        (¬ ∃ U : FableHilbertWalk20260819.H004.Vec Int Bool →
              FableHilbertWalk20260819.H004.Vec Int Bool,
          (∀ u v,
            FableHilbertWalk20260819.H005.sesq
                intPack enumBool (U u) (U v) =
              FableHilbertWalk20260819.H005.sesq intPack enumBool u v) ∧
            U (FableHilbertWalk20260819.H004.delta intPack false) =
              FableHilbertWalk20260819.H004.delta intPack false ∧
            U (FableHilbertWalk20260819.H004.delta intPack true) =
              FableHilbertWalk20260819.H004.delta intPack false) ∧
        (∀ x, FableHilbertWalk20260819.H015DilationCount.dilFF.map x =
          FableHilbertWalk20260819.H015.dil1 x)) ∧
      (finishFate FrozenExtra.uniqueTensor = FinishFate.imported ∧
        ¬ ∀ u v p,
          FableHilbertWalk20260819.H014Interface.dumpRight u v p =
            FableHilbertWalk20260819.H014.tensor u v p) ∧
      (finishFate FrozenExtra.circle = FinishFate.imported ∧
        ¬ FableHilbertWalk20260819.H011Circle.ConnectednessShadow
            FableHilbertWalk20260819.H011Circle.signCarrier) ∧
      (finishFate FrozenExtra.continuousTime = FinishFate.refused ∧
        (¬ ∃ σ : Bool → Bool,
          ∀ q : Bool,
            σ (σ q) = FableHilbertWalk20260819.H003.toggle q)) ∧
      finishFate FrozenExtra.pythonDual = FinishFate.dualOutsideLean ∧
      assigned PhysicsName.susy = false ∧
      assigned PhysicsName.standardModelGauge = false :=
  ⟨finish_fieldC_refused, finish_spectral_refused,
    ⟨rfl,
      FableHilbertWalk20260819.H017Gleason.gleason_pack_uniqueness_still_imported.2.2.2.2.2⟩,
    finish_cptp_imported,
    finish_uniqueTensor_imported,
    ⟨rfl,
      FableHilbertWalk20260819.H011Circle.sign_excluded_circle_still_imported.1⟩,
    finish_continuousTime_refused, finish_pythonDual_outside_lean,
    susy_unassigned, standard_model_gauge_unassigned⟩

#print axioms remaining_import_list

theorem finish_is_not_ordinary_mnC :
    finishFate FrozenExtra.gleasonUniqueness = FinishFate.imported ∧
      finishFate FrozenExtra.uniqueTensor = FinishFate.imported ∧
      finishFate FrozenExtra.circle = FinishFate.imported ∧
      ¬ IsFieldPack gaussPack :=
  ⟨rfl, rfl, rfl, gauss_not_a_field⟩

#print axioms finish_is_not_ordinary_mnC

/-- Historical drop-one census is still the five OPEN necessity
    verdicts at dba1434b. This finish table does not rewrite it. -/
theorem dropone_open_verdicts_untouched :
    FableHilbertWalk20260819.H017ExtrasDropone.dropVerdict
        FrozenExtra.gleasonUniqueness =
      FableHilbertWalk20260819.H017ExtrasDropone.DropVerdict.open ∧
      FableHilbertWalk20260819.H017ExtrasDropone.dropVerdict
          FrozenExtra.cptp =
        FableHilbertWalk20260819.H017ExtrasDropone.DropVerdict.open ∧
      FableHilbertWalk20260819.H017ExtrasDropone.dropVerdict
          FrozenExtra.uniqueTensor =
        FableHilbertWalk20260819.H017ExtrasDropone.DropVerdict.open ∧
      FableHilbertWalk20260819.H017ExtrasDropone.dropVerdict
          FrozenExtra.circle =
        FableHilbertWalk20260819.H017ExtrasDropone.DropVerdict.open ∧
      FableHilbertWalk20260819.H017ExtrasDropone.dropVerdict
          FrozenExtra.pythonDual =
        FableHilbertWalk20260819.H017ExtrasDropone.DropVerdict.open :=
  ⟨rfl, rfl, rfl, rfl, rfl⟩

#print axioms dropone_open_verdicts_untouched

end FableHilbertWalk20260819.H017Finish
