



import HWKernel
import FinitePresentedCarrier
import ProbabilitySimplex
import HilbertWalkRationals
import ReportDynamics
import ReversibilityGate
import FreeLinearization
import InnerProductAdmission
import PermutationUnitary
import HilbertWalkEnvelope
import Complexification
import HilbertWalkPhaseBlindPresentation
import PhaseFiber
import InterferenceNonDescent
import HilbertWalkScale
import HilbertWalkHadamard
import U1SelectorBoundary
import HilbertWalkCircle
import OperatorAlgebraShadow
import BornPairingBoundary
import FrameAdditivity
import HilbertWalkSameContract
import TensorCompositionBoundary
import BilinearProduct
import HilbertWalkInterface
import IrreversibleFork
import DilationCount
import CollapseDilations
import ContinuousDynamicsFork
import FiniteHilbertBoundary
import MatrixFiniteRecovery
import HilbertWalkDensity
import HilbertWalkChannel
import HilbertWalkGleasonFin
import HilbertWalkGleason
import HilbertWalkGleasonExtras
import HilbertWalkGleasonExtrasDropOne
import HilbertWalkGleasonFinish
import HWThread
import HWCarrierThread
import HWFullThread

namespace HilbertWalk

theorem walk_root_reaches_boundary :
    HilbertWalk.FiniteHilbertBoundary.AllDischarged
      HilbertWalk.FiniteHilbertBoundary.walkLedger = false :=
  HilbertWalk.FiniteHilbertBoundary.import_ledger_gate.1

#print axioms walk_root_reaches_boundary

theorem walk_root_reaches_frame_additivity :
    ¬ HilbertWalk.FrameAdditivity.frameAdditiveAtScaleTwo
      HilbertWalk.FrameAdditivity.quarticAlong :=
  HilbertWalk.FrameAdditivity.fourth_power_dies_under_frame_additivity

#print axioms walk_root_reaches_frame_additivity

theorem walk_root_assigns_superposition_and_entanglement :
    HilbertWalk.PhaseBlindPresentation.psi1 ≠
      HilbertWalk.PhaseBlindPresentation.psi2 ∧
      ¬ ∃ u v : Bool → Int,
        ∀ p : Bool × Bool,
          HilbertWalk.TensorCompositionBoundary.bell p =
            HilbertWalk.TensorCompositionBoundary.tensor u v p :=
  ⟨HilbertWalk.HWCarrierThread.superposition_is_the_phase_blind_fiber.2,
    HilbertWalk.HWCarrierThread.entanglement_needs_a_tensor_host⟩

#print axioms walk_root_assigns_superposition_and_entanglement

theorem walk_root_threads_one_carrier_through_mixing :
    (∀ (v : HilbertWalk.FreeLinearization.Vec
          HilbertWalk.HWKernel.GaussInt Bool)
        (x y : Bool × Bool),
      HilbertWalk.FinitePresentedCarrier.sameReport
          HilbertWalk.FinitePresentedCarrier.boolFixture x y →
        HilbertWalk.HWCarrierThread.alongPres
            HilbertWalk.FinitePresentedCarrier.boolFixture v x =
          HilbertWalk.HWCarrierThread.alongPres
            HilbertWalk.FinitePresentedCarrier.boolFixture v y) ∧
      ¬ ∃ f : (Bool → Int) → (Bool → Int),
        ∀ v : HilbertWalk.FreeLinearization.Vec
            HilbertWalk.HWKernel.GaussInt Bool,
          HilbertWalk.InterferenceNonDescent.readout v =
            f (HilbertWalk.PhaseBlindPresentation.phaseBlind v) :=
  ⟨HilbertWalk.HWCarrierThread.one_carrier_through_mixing_leftover.1,
    HilbertWalk.HWCarrierThread.one_carrier_through_mixing_leftover.2.2.2.2⟩

#print axioms walk_root_threads_one_carrier_through_mixing

theorem walk_root_bilinear_product_unique
    (E : HilbertWalk.BilinearProduct.BilinearKroneckerEmbed) :
    ∀ u v p,
      E.embed u v p = HilbertWalk.TensorCompositionBoundary.tensor u v p :=
  (HilbertWalk.BilinearProduct.bilinear_product_unique_on_bool_prod E).1

#print axioms walk_root_bilinear_product_unique

theorem walk_root_two_effect_rules_share_unit_total :
    HilbertWalk.SameContract.bornRule
        HilbertWalk.BornPairingBoundary.psi21
        (HilbertWalk.BornPairingBoundary.indicator false) ≠
      HilbertWalk.SameContract.swappedRule
        HilbertWalk.BornPairingBoundary.psi21
        (HilbertWalk.BornPairingBoundary.indicator false) :=
  HilbertWalk.SameContract.two_effect_rules_share_unit_total_and_disagree.2.2.2.2

#print axioms walk_root_two_effect_rules_share_unit_total

theorem walk_root_sign_fails_connectedness_shadow :
    ¬ HilbertWalk.Circle.ConnectednessShadow
        HilbertWalk.Circle.signCarrier ∧
      HilbertWalk.Circle.ConnectednessShadow
        HilbertWalk.Circle.gaussUnitCarrier ∧
      HilbertWalk.Circle.ConnectednessShadow
        HilbertWalk.Circle.cyc3Carrier :=
  ⟨HilbertWalk.Circle.sign_fails_connectedness_shadow,
    HilbertWalk.Circle.gauss_units_meet_connectedness_shadow,
    HilbertWalk.Circle.cyc3_meets_connectedness_shadow⟩

#print axioms walk_root_sign_fails_connectedness_shadow

theorem walk_root_two_level_gauss_matrix_algebra :
    (∀ (T : HilbertWalk.MatrixFiniteRecovery.LinearEnd
          HilbertWalk.HWKernel.gaussPack)
        (v : HilbertWalk.FreeLinearization.Vec
          HilbertWalk.HWKernel.GaussInt Bool)
        (x : Bool),
      T.map v x =
        HilbertWalk.MatrixFiniteRecovery.applyMat
          HilbertWalk.HWKernel.gaussPack
          (HilbertWalk.MatrixFiniteRecovery.matOf T) v x) ∧
      ¬ ∃ A : Bool → Bool → Int,
        ∀ i j : Bool,
          HilbertWalk.MatrixFiniteRecovery.pauliY i j =
            HilbertWalk.Complexification.embed (A i j) :=
  ⟨HilbertWalk.MatrixFiniteRecovery.two_level_gauss_matrix_algebra.1,
    HilbertWalk.MatrixFiniteRecovery.two_level_gauss_matrix_algebra.2.2.2.2.2.2.2.2⟩

#print axioms walk_root_two_level_gauss_matrix_algebra

theorem walk_root_finite_gauss_matrix_algebra :
    ∀ (T : HilbertWalk.GleasonFin.LinearEnd
          Bool HilbertWalk.HWKernel.gaussPack)
      (v : HilbertWalk.FreeLinearization.Vec
        HilbertWalk.HWKernel.GaussInt Bool)
      (x : Bool),
      T.map v x =
        HilbertWalk.GleasonFin.applyMat
          HilbertWalk.HWKernel.gaussPack
          HilbertWalk.HWKernel.enumBool
          (HilbertWalk.GleasonFin.matOf T) v x :=
  HilbertWalk.GleasonFin.two_label_gauss_matrix_algebra

#print axioms walk_root_finite_gauss_matrix_algebra

theorem walk_root_gleason_cannot_run_on_two_label :
    ¬ HilbertWalk.Gleason.GleasonDimAtLeastThree
        HilbertWalk.HWKernel.enumBool :=
  HilbertWalk.Gleason.two_label_host_not_gleason_dimension

#print axioms walk_root_gleason_cannot_run_on_two_label

theorem walk_root_gleason_pack_still_imported :
    HilbertWalk.BornPairingBoundary.UniquenessDischarged
        HilbertWalk.BornPairingBoundary.hostSupplies = false :=
  HilbertWalk.BornPairingBoundary.uniqueness_not_discharged

#print axioms walk_root_gleason_pack_still_imported

theorem walk_root_remaining_mnC_extras :
    ¬ HilbertWalk.GleasonExtras.IsFieldPack
        HilbertWalk.HWKernel.gaussPack ∧
      ¬ HilbertWalk.GleasonExtras.SpectralEigenvalueExtra
          HilbertWalk.HWKernel.enumBool :=
  ⟨HilbertWalk.GleasonExtras.gauss_not_a_field,
    HilbertWalk.GleasonExtras.spectral_eigenvalue_extra_fails_on_two_label⟩

#print axioms walk_root_remaining_mnC_extras

theorem walk_root_drop_one_count :
    HilbertWalk.GleasonExtrasDropOne.allExtras.length = 8 ∧
      HilbertWalk.GleasonExtrasDropOne.lostExtras.length = 3 ∧
      HilbertWalk.GleasonExtrasDropOne.openExtras.length = 5 ∧
      HilbertWalk.GleasonExtrasDropOne.dropVerdict
          HilbertWalk.GleasonExtrasDropOne.FrozenExtra.pythonDual =
        HilbertWalk.GleasonExtrasDropOne.DropVerdict.open :=
  ⟨HilbertWalk.GleasonExtrasDropOne.extra_list_length,
    HilbertWalk.GleasonExtrasDropOne.lost_length,
    HilbertWalk.GleasonExtrasDropOne.open_length,
    HilbertWalk.GleasonExtrasDropOne.drop_pythonDual_necessity_open⟩

#print axioms walk_root_drop_one_count

theorem walk_root_four_report_id_dilations :
    (∀ x, HilbertWalk.DilationCount.dilFF.map x =
      HilbertWalk.IrreversibleFork.dil1 x) ∧
      (∀ (D : HilbertWalk.DilationCount.ReportIdDilation),
        (∀ x, D.map x =
            HilbertWalk.DilationCount.dilFF.map x) ∨
          (∀ x, D.map x =
              HilbertWalk.DilationCount.dilFT.map x) ∨
          (∀ x, D.map x =
              HilbertWalk.DilationCount.dilTF.map x) ∨
          (∀ x, D.map x =
              HilbertWalk.DilationCount.dilTT.map x)) :=
  ⟨HilbertWalk.DilationCount.four_reversible_dilations_of_report_identity.1.1,
    HilbertWalk.DilationCount.four_reversible_dilations_of_report_identity.2.2⟩

#print axioms walk_root_four_report_id_dilations

theorem walk_root_mix_doubles_total_any
    (v : HilbertWalk.FreeLinearization.Vec
      HilbertWalk.HWKernel.GaussInt Bool) :
    HilbertWalk.PhaseBlindPresentation.totalWeight
        HilbertWalk.HWKernel.enumBool
        (HilbertWalk.InterferenceNonDescent.mix v) =
      2 *
        HilbertWalk.PhaseBlindPresentation.totalWeight
          HilbertWalk.HWKernel.enumBool v :=
  HilbertWalk.Scale.mix_doubles_total_any v

#print axioms walk_root_mix_doubles_total_any

theorem walk_root_mix_mix_is_two
    (v : HilbertWalk.FreeLinearization.Vec
      HilbertWalk.HWKernel.GaussInt Bool) :
    ∀ q : Bool,
      HilbertWalk.InterferenceNonDescent.mix
          (HilbertWalk.InterferenceNonDescent.mix v) q =
        HilbertWalk.HWKernel.GaussInt.gadd (v q) (v q) :=
  HilbertWalk.Hadamard.mix_mix_is_two v

#print axioms walk_root_mix_mix_is_two

theorem walk_root_bell_ptr_eq_ident :
    HilbertWalk.Density.ptrSecond
        (HilbertWalk.Density.ketbra4
          HilbertWalk.Density.bellAmp) =
      HilbertWalk.MatrixFiniteRecovery.ident
        HilbertWalk.HWKernel.gaussPack :=
  HilbertWalk.Density.bell_ptr_eq_ident

#print axioms walk_root_bell_ptr_eq_ident

theorem walk_root_diagonal_shadow_does_not_fix_channel :
    HilbertWalk.Channel.dephase
        (HilbertWalk.Channel.conjMix
          HilbertWalk.Density.e00) =
      HilbertWalk.MatrixFiniteRecovery.ident
        HilbertWalk.HWKernel.gaussPack ∧
      HilbertWalk.Channel.conjMix
          HilbertWalk.Density.e00 false true ≠
        HilbertWalk.MatrixFiniteRecovery.ident
          HilbertWalk.HWKernel.gaussPack false true :=
  HilbertWalk.Channel.diagonal_shadow_does_not_fix_channel

#print axioms walk_root_diagonal_shadow_does_not_fix_channel

theorem walk_root_combining_interface_has_rival :
    HilbertWalk.Interface.dumpRight
        (HilbertWalk.FreeLinearization.delta
          HilbertWalk.HWKernel.intPack false)
        (HilbertWalk.FreeLinearization.delta
          HilbertWalk.HWKernel.intPack true)
        (false, true) ≠
      HilbertWalk.TensorCompositionBoundary.tensor
        (HilbertWalk.FreeLinearization.delta
          HilbertWalk.HWKernel.intPack false)
        (HilbertWalk.FreeLinearization.delta
          HilbertWalk.HWKernel.intPack true)
        (false, true) :=
  HilbertWalk.Interface.two_combinings_share_interface_and_disagree.2.2.1

#print axioms walk_root_combining_interface_has_rival

theorem walk_root_one_carrier_through_H000_H016 :
    HilbertWalk.FinitePresentedCarrier.sameReport
        HilbertWalk.FinitePresentedCarrier.boolFixture
        (false, false) (false, true) ∧
      (¬ ∃ v : Bool → Int, ∀ p : Bool × Bool,
        v (HilbertWalk.FinitePresentedCarrier.boolFixture.pres p) =
          HilbertWalk.TensorCompositionBoundary.bell p) ∧
      ¬ ∃ σ : Bool → Bool, ∀ q : Bool,
        σ (σ q) = HilbertWalk.ReversibilityGate.toggle q :=
  HilbertWalk.HWFullThread.one_carrier_through_H000_H016

#print axioms walk_root_one_carrier_through_H000_H016

theorem walk_root_choice_free_fractional_weights :
    HilbertWalk.HWKernel.rsum
        HilbertWalk.Rationals.fracPack
        [HilbertWalk.Rationals.half,
          HilbertWalk.Rationals.half] =
      HilbertWalk.Rationals.fone ∧
      HilbertWalk.Rationals.half ≠
        HilbertWalk.Rationals.fzero ∧
      HilbertWalk.Rationals.half ≠
        HilbertWalk.Rationals.fone :=
  ⟨HilbertWalk.Rationals.rsum_two_halves,
    HilbertWalk.Rationals.half_ne_zero,
    HilbertWalk.Rationals.half_ne_one⟩

#print axioms walk_root_choice_free_fractional_weights

theorem walk_root_two_permutation_lifts :
    (HilbertWalk.PermutationUnitary.permU
        HilbertWalk.HWKernel.gaussPack
        HilbertWalk.Envelope.idRev ≠
      HilbertWalk.PermutationUnitary.permU
        HilbertWalk.HWKernel.gaussPack
        HilbertWalk.ReversibilityGate.toggleRev) ∧
      ((∀ v q,
          HilbertWalk.PermutationUnitary.permU
              HilbertWalk.HWKernel.gaussPack
              HilbertWalk.Envelope.idRev v q = v q) ∧
        (∀ v q,
          HilbertWalk.PermutationUnitary.permU
              HilbertWalk.HWKernel.gaussPack
              HilbertWalk.ReversibilityGate.toggleRev v q =
            v (HilbertWalk.ReversibilityGate.toggle q))) ∧
      (∀ {τ : Bool → Bool}
          (R : HilbertWalk.ReversibilityGate.Reversible τ),
        (∀ v q,
          HilbertWalk.PermutationUnitary.permU
              HilbertWalk.HWKernel.gaussPack R v q = v q) ∨
        (∀ v q,
          HilbertWalk.PermutationUnitary.permU
              HilbertWalk.HWKernel.gaussPack R v q =
            v (HilbertWalk.ReversibilityGate.toggle q))) ∧
      ¬ ∃ (τ : Bool → Bool)
        (R : HilbertWalk.ReversibilityGate.Reversible τ),
        ∀ v, HilbertWalk.PermutationUnitary.swapI v =
          HilbertWalk.PermutationUnitary.permU
            HilbertWalk.HWKernel.gaussPack R v :=
  HilbertWalk.Envelope.two_permutation_lifts_envelope_strict

#print axioms walk_root_two_permutation_lifts

theorem walk_root_four_collapse_dilations :
    (HilbertWalk.CollapseDilations.dFF.map ≠
        HilbertWalk.CollapseDilations.dFT.map ∧
      HilbertWalk.CollapseDilations.dFF.map ≠
        HilbertWalk.CollapseDilations.dTF.map ∧
      HilbertWalk.CollapseDilations.dFF.map ≠
        HilbertWalk.CollapseDilations.dTT.map ∧
      HilbertWalk.CollapseDilations.dFT.map ≠
        HilbertWalk.CollapseDilations.dTF.map ∧
      HilbertWalk.CollapseDilations.dFT.map ≠
        HilbertWalk.CollapseDilations.dTT.map ∧
      HilbertWalk.CollapseDilations.dTF.map ≠
        HilbertWalk.CollapseDilations.dTT.map) ∧
      (∀ (D : HilbertWalk.CollapseDilations.CollapseDilation),
        (∀ x, D.map x =
            HilbertWalk.CollapseDilations.dFF.map x) ∨
          (∀ x, D.map x =
              HilbertWalk.CollapseDilations.dFT.map x) ∨
          (∀ x, D.map x =
              HilbertWalk.CollapseDilations.dTF.map x) ∨
          (∀ x, D.map x =
              HilbertWalk.CollapseDilations.dTT.map x)) ∧
      (∀ (D : HilbertWalk.CollapseDilations.CollapseDilation)
          (q : Bool),
        (D.map (q, HilbertWalk.CollapseDilations.prepared)).1 =
          HilbertWalk.ReversibilityGate.collapse q) :=
  HilbertWalk.CollapseDilations.four_reversible_dilations_of_collapse

#print axioms walk_root_four_collapse_dilations

theorem walk_root_remaining_import_list :
    (GleasonFinish.finishFate GleasonExtrasDropOne.FrozenExtra.fieldC =
        GleasonFinish.FinishFate.refused ∧
      ¬ GleasonExtras.IsFieldPack HWKernel.gaussPack) ∧
    (GleasonFinish.finishFate GleasonExtrasDropOne.FrozenExtra.spectral =
        GleasonFinish.FinishFate.refused ∧
      ¬ GleasonExtras.SpectralEigenvalueExtra HWKernel.enumBool) ∧
    (GleasonFinish.finishFate
          GleasonExtrasDropOne.FrozenExtra.gleasonUniqueness =
        GleasonFinish.FinishFate.imported ∧
      BornPairingBoundary.UniquenessDischarged BornPairingBoundary.hostSupplies = false) ∧
    (GleasonFinish.finishFate GleasonExtrasDropOne.FrozenExtra.cptp =
        GleasonFinish.FinishFate.imported ∧
      ¬ Nonempty (ReversibilityGate.Reversible ReversibilityGate.collapse) ∧
      (¬ ∃ U : FreeLinearization.Vec Int Bool → FreeLinearization.Vec Int Bool,
        (∀ u v,
          InnerProductAdmission.sesq HWKernel.intPack HWKernel.enumBool (U u) (U v) =
            InnerProductAdmission.sesq HWKernel.intPack HWKernel.enumBool u v) ∧
        U (FreeLinearization.delta HWKernel.intPack false) =
          FreeLinearization.delta HWKernel.intPack false ∧
        U (FreeLinearization.delta HWKernel.intPack true) =
          FreeLinearization.delta HWKernel.intPack false) ∧
      (∀ x, DilationCount.dilFF.map x = IrreversibleFork.dil1 x)) ∧
    (GleasonFinish.finishFate GleasonExtrasDropOne.FrozenExtra.uniqueTensor =
        GleasonFinish.FinishFate.imported ∧
      ¬ ∀ u v p, Interface.dumpRight u v p = TensorCompositionBoundary.tensor u v p) ∧
    (GleasonFinish.finishFate GleasonExtrasDropOne.FrozenExtra.circle =
        GleasonFinish.FinishFate.imported ∧
      ¬ Circle.ConnectednessShadow Circle.signCarrier) ∧
    (GleasonFinish.finishFate GleasonExtrasDropOne.FrozenExtra.continuousTime =
        GleasonFinish.FinishFate.refused ∧
      (¬ ∃ σ : Bool → Bool, ∀ q : Bool, σ (σ q) = ReversibilityGate.toggle q)) ∧
    GleasonFinish.finishFate GleasonExtrasDropOne.FrozenExtra.pythonDual =
      GleasonFinish.FinishFate.dualOutsideLean ∧
    GleasonFinish.assigned GleasonFinish.PhysicsName.susy = false ∧
    GleasonFinish.assigned GleasonFinish.PhysicsName.standardModelGauge = false :=
  GleasonFinish.remaining_import_list

#print axioms walk_root_remaining_import_list

end HilbertWalk

private def l5aProvenance : String :=
  "Origin: lean4/HilbertWalkAll.lean Claim: walk_root_reaches_boundary AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
