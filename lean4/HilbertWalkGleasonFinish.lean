



import HWKernel
import ReversibilityGate
import FreeLinearization
import InnerProductAdmission
import HilbertWalkCircle
import BornPairingBoundary
import TensorCompositionBoundary
import HilbertWalkInterface
import IrreversibleFork
import DilationCount
import ContinuousDynamicsFork
import HilbertWalkGleasonExtras
import HilbertWalkGleasonExtrasDropOne
import HilbertWalkGleason

namespace HilbertWalk.GleasonFinish

open HilbertWalk.HWKernel
open HilbertWalk.GleasonExtras
open HilbertWalk.GleasonExtrasDropOne

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

theorem finish_gleason_imported :
    finishFate FrozenExtra.gleasonUniqueness = FinishFate.imported ∧
      HilbertWalk.BornPairingBoundary.UniquenessDischarged
          HilbertWalk.BornPairingBoundary.hostSupplies = false ∧
      ¬ HilbertWalk.Gleason.GleasonDimAtLeastThree
          enumBool :=
  ⟨rfl,
    HilbertWalk.Gleason.gleason_pack_uniqueness_still_imported.2.2.2.2.2,
    HilbertWalk.Gleason.two_label_host_not_gleason_dimension⟩

#print axioms finish_gleason_imported

theorem finish_cptp_imported :
    finishFate FrozenExtra.cptp = FinishFate.imported ∧
      ¬ Nonempty (HilbertWalk.ReversibilityGate.Reversible
          HilbertWalk.ReversibilityGate.collapse) ∧
      (¬ ∃ U : HilbertWalk.FreeLinearization.Vec Int Bool →
            HilbertWalk.FreeLinearization.Vec Int Bool,
        (∀ u v,
          HilbertWalk.InnerProductAdmission.sesq
              intPack enumBool (U u) (U v) =
            HilbertWalk.InnerProductAdmission.sesq intPack enumBool u v) ∧
          U (HilbertWalk.FreeLinearization.delta intPack false) =
            HilbertWalk.FreeLinearization.delta intPack false ∧
          U (HilbertWalk.FreeLinearization.delta intPack true) =
            HilbertWalk.FreeLinearization.delta intPack false) ∧
      (∀ x, HilbertWalk.DilationCount.dilFF.map x =
        HilbertWalk.IrreversibleFork.dil1 x) :=
  ⟨rfl, HilbertWalk.ReversibilityGate.collapse_not_reversible,
    HilbertWalk.IrreversibleFork.collapse_no_isometry,
    HilbertWalk.DilationCount.dilFF_is_dil1⟩

#print axioms finish_cptp_imported

theorem finish_uniqueTensor_imported :
    finishFate FrozenExtra.uniqueTensor = FinishFate.imported ∧
      ¬ ∀ u v p,
        HilbertWalk.Interface.dumpRight u v p =
          HilbertWalk.TensorCompositionBoundary.tensor u v p :=
  ⟨rfl, HilbertWalk.Interface.dumpRight_not_tensor⟩

#print axioms finish_uniqueTensor_imported

theorem finish_circle_imported :
    finishFate FrozenExtra.circle = FinishFate.imported ∧
      ¬ HilbertWalk.Circle.ConnectednessShadow
          HilbertWalk.Circle.signCarrier ∧
      HilbertWalk.Circle.ConnectednessShadow
        HilbertWalk.Circle.gaussUnitCarrier :=
  ⟨rfl,
    HilbertWalk.Circle.sign_excluded_circle_still_imported.1,
    HilbertWalk.Circle.sign_excluded_circle_still_imported.2.1⟩

#print axioms finish_circle_imported

theorem finish_continuousTime_refused :
    finishFate FrozenExtra.continuousTime = FinishFate.refused ∧
      (¬ ∃ σ : Bool → Bool,
        ∀ q : Bool, σ (σ q) = HilbertWalk.ReversibilityGate.toggle q) :=
  ⟨rfl, HilbertWalk.ContinuousDynamicsFork.no_report_half_step⟩

#print axioms finish_continuousTime_refused

theorem finish_pythonDual_outside_lean :
    finishFate FrozenExtra.pythonDual = FinishFate.dualOutsideLean :=
  rfl

#print axioms finish_pythonDual_outside_lean


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

theorem remaining_import_list :
    (finishFate FrozenExtra.fieldC = FinishFate.refused ∧
      ¬ IsFieldPack gaussPack) ∧
      (finishFate FrozenExtra.spectral = FinishFate.refused ∧
        ¬ SpectralEigenvalueExtra enumBool) ∧
      (finishFate FrozenExtra.gleasonUniqueness = FinishFate.imported ∧
        HilbertWalk.BornPairingBoundary.UniquenessDischarged
            HilbertWalk.BornPairingBoundary.hostSupplies = false) ∧
      (finishFate FrozenExtra.cptp = FinishFate.imported ∧
        ¬ Nonempty (HilbertWalk.ReversibilityGate.Reversible
            HilbertWalk.ReversibilityGate.collapse) ∧
        (¬ ∃ U : HilbertWalk.FreeLinearization.Vec Int Bool →
              HilbertWalk.FreeLinearization.Vec Int Bool,
          (∀ u v,
            HilbertWalk.InnerProductAdmission.sesq
                intPack enumBool (U u) (U v) =
              HilbertWalk.InnerProductAdmission.sesq intPack enumBool u v) ∧
            U (HilbertWalk.FreeLinearization.delta intPack false) =
              HilbertWalk.FreeLinearization.delta intPack false ∧
            U (HilbertWalk.FreeLinearization.delta intPack true) =
              HilbertWalk.FreeLinearization.delta intPack false) ∧
        (∀ x, HilbertWalk.DilationCount.dilFF.map x =
          HilbertWalk.IrreversibleFork.dil1 x)) ∧
      (finishFate FrozenExtra.uniqueTensor = FinishFate.imported ∧
        ¬ ∀ u v p,
          HilbertWalk.Interface.dumpRight u v p =
            HilbertWalk.TensorCompositionBoundary.tensor u v p) ∧
      (finishFate FrozenExtra.circle = FinishFate.imported ∧
        ¬ HilbertWalk.Circle.ConnectednessShadow
            HilbertWalk.Circle.signCarrier) ∧
      (finishFate FrozenExtra.continuousTime = FinishFate.refused ∧
        (¬ ∃ σ : Bool → Bool,
          ∀ q : Bool,
            σ (σ q) = HilbertWalk.ReversibilityGate.toggle q)) ∧
      finishFate FrozenExtra.pythonDual = FinishFate.dualOutsideLean ∧
      assigned PhysicsName.susy = false ∧
      assigned PhysicsName.standardModelGauge = false :=
  ⟨finish_fieldC_refused, finish_spectral_refused,
    ⟨rfl,
      HilbertWalk.Gleason.gleason_pack_uniqueness_still_imported.2.2.2.2.2⟩,
    finish_cptp_imported,
    finish_uniqueTensor_imported,
    ⟨rfl,
      HilbertWalk.Circle.sign_excluded_circle_still_imported.1⟩,
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

theorem dropone_open_verdicts_untouched :
    HilbertWalk.GleasonExtrasDropOne.dropVerdict
        FrozenExtra.gleasonUniqueness =
      HilbertWalk.GleasonExtrasDropOne.DropVerdict.open ∧
      HilbertWalk.GleasonExtrasDropOne.dropVerdict
          FrozenExtra.cptp =
        HilbertWalk.GleasonExtrasDropOne.DropVerdict.open ∧
      HilbertWalk.GleasonExtrasDropOne.dropVerdict
          FrozenExtra.uniqueTensor =
        HilbertWalk.GleasonExtrasDropOne.DropVerdict.open ∧
      HilbertWalk.GleasonExtrasDropOne.dropVerdict
          FrozenExtra.circle =
        HilbertWalk.GleasonExtrasDropOne.DropVerdict.open ∧
      HilbertWalk.GleasonExtrasDropOne.dropVerdict
          FrozenExtra.pythonDual =
        HilbertWalk.GleasonExtrasDropOne.DropVerdict.open :=
  ⟨rfl, rfl, rfl, rfl, rfl⟩

#print axioms dropone_open_verdicts_untouched

end HilbertWalk.GleasonFinish

private def l5aProvenance : String :=
  "Origin: lean4/HilbertWalkGleasonFinish.lean Claim: finish_fieldC_refused AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
