



import HWKernel
import H000FinitePresentedCarrier
import H001ProbabilitySimplex
import H001Rats
import H002ReportDynamics
import H003ReversibilityGate
import H004FreeLinearization
import H005InnerProductAdmission
import H006PermutationUnitary
import H006Envelope
import H007Complexification
import H008PhaseBlindPresentation
import H009PhaseFiber
import H010InterferenceNonDescent
import H010Scale
import H010Hadamard
import H011U1SelectorBoundary
import H011Circle
import H012OperatorAlgebraShadow
import H013BornPairingBoundary
import H013FrameAdditivity
import H013SameContract
import H014TensorCompositionBoundary
import H014BilinearProduct
import H014Interface
import H015IrreversibleFork
import H015DilationCount
import H015CollapseDilations
import H016ContinuousDynamicsFork
import H017FiniteHilbertBoundary
import H017MatrixFiniteRecovery
import H018Density
import H018Channel
import H017Fin
import H017Gleason
import H017Extras
import H017ExtrasDropone
import H017Finish
import HWThread
import HWCarrierThread
import HWFullThread

namespace FableHilbertWalk20260819

theorem walk_root_reaches_boundary :
    FableHilbertWalk20260819.H017.AllDischarged
      FableHilbertWalk20260819.H017.walkLedger = false :=
  FableHilbertWalk20260819.H017.import_ledger_gate.1

#print axioms walk_root_reaches_boundary

theorem walk_root_reaches_frame_additivity :
    ¬ FableHilbertWalk20260819.H013Frame.frameAdditiveAtScaleTwo
      FableHilbertWalk20260819.H013Frame.quarticAlong :=
  FableHilbertWalk20260819.H013Frame.fourth_power_dies_under_frame_additivity

#print axioms walk_root_reaches_frame_additivity

theorem walk_root_assigns_superposition_and_entanglement :
    FableHilbertWalk20260819.H008.psi1 ≠
      FableHilbertWalk20260819.H008.psi2 ∧
      ¬ ∃ u v : Bool → Int,
        ∀ p : Bool × Bool,
          FableHilbertWalk20260819.H014.bell p =
            FableHilbertWalk20260819.H014.tensor u v p :=
  ⟨FableHilbertWalk20260819.HWCarrierThread.superposition_is_the_phase_blind_fiber.2,
    FableHilbertWalk20260819.HWCarrierThread.entanglement_needs_a_tensor_host⟩

#print axioms walk_root_assigns_superposition_and_entanglement

theorem walk_root_threads_one_carrier_through_mixing :
    (∀ (v : FableHilbertWalk20260819.H004.Vec
          FableHilbertWalk20260819.HWKernel.GaussInt Bool)
        (x y : Bool × Bool),
      FableHilbertWalk20260819.H000.sameReport
          FableHilbertWalk20260819.H000.boolFixture x y →
        FableHilbertWalk20260819.HWCarrierThread.alongPres
            FableHilbertWalk20260819.H000.boolFixture v x =
          FableHilbertWalk20260819.HWCarrierThread.alongPres
            FableHilbertWalk20260819.H000.boolFixture v y) ∧
      ¬ ∃ f : (Bool → Int) → (Bool → Int),
        ∀ v : FableHilbertWalk20260819.H004.Vec
            FableHilbertWalk20260819.HWKernel.GaussInt Bool,
          FableHilbertWalk20260819.H010.readout v =
            f (FableHilbertWalk20260819.H008.phaseBlind v) :=
  ⟨FableHilbertWalk20260819.HWCarrierThread.one_carrier_through_mixing_leftover.1,
    FableHilbertWalk20260819.HWCarrierThread.one_carrier_through_mixing_leftover.2.2.2.2⟩

#print axioms walk_root_threads_one_carrier_through_mixing

theorem walk_root_bilinear_product_unique
    (E : FableHilbertWalk20260819.H014Bilin.BilinearKroneckerEmbed) :
    ∀ u v p,
      E.embed u v p = FableHilbertWalk20260819.H014.tensor u v p :=
  (FableHilbertWalk20260819.H014Bilin.bilinear_product_unique_on_bool_prod E).1

#print axioms walk_root_bilinear_product_unique

theorem walk_root_two_effect_rules_share_unit_total :
    FableHilbertWalk20260819.H013Contract.bornRule
        FableHilbertWalk20260819.H013.psi21
        (FableHilbertWalk20260819.H013.indicator false) ≠
      FableHilbertWalk20260819.H013Contract.swappedRule
        FableHilbertWalk20260819.H013.psi21
        (FableHilbertWalk20260819.H013.indicator false) :=
  FableHilbertWalk20260819.H013Contract.two_effect_rules_share_unit_total_and_disagree.2.2.2.2

#print axioms walk_root_two_effect_rules_share_unit_total

theorem walk_root_sign_fails_connectedness_shadow :
    ¬ FableHilbertWalk20260819.H011Circle.ConnectednessShadow
        FableHilbertWalk20260819.H011Circle.signCarrier ∧
      FableHilbertWalk20260819.H011Circle.ConnectednessShadow
        FableHilbertWalk20260819.H011Circle.gaussUnitCarrier ∧
      FableHilbertWalk20260819.H011Circle.ConnectednessShadow
        FableHilbertWalk20260819.H011Circle.cyc3Carrier :=
  ⟨FableHilbertWalk20260819.H011Circle.sign_fails_connectedness_shadow,
    FableHilbertWalk20260819.H011Circle.gauss_units_meet_connectedness_shadow,
    FableHilbertWalk20260819.H011Circle.cyc3_meets_connectedness_shadow⟩

#print axioms walk_root_sign_fails_connectedness_shadow

theorem walk_root_two_level_gauss_matrix_algebra :
    (∀ (T : FableHilbertWalk20260819.H017Matrix.LinearEnd
          FableHilbertWalk20260819.HWKernel.gaussPack)
        (v : FableHilbertWalk20260819.H004.Vec
          FableHilbertWalk20260819.HWKernel.GaussInt Bool)
        (x : Bool),
      T.map v x =
        FableHilbertWalk20260819.H017Matrix.applyMat
          FableHilbertWalk20260819.HWKernel.gaussPack
          (FableHilbertWalk20260819.H017Matrix.matOf T) v x) ∧
      ¬ ∃ A : Bool → Bool → Int,
        ∀ i j : Bool,
          FableHilbertWalk20260819.H017Matrix.pauliY i j =
            FableHilbertWalk20260819.H007.embed (A i j) :=
  ⟨FableHilbertWalk20260819.H017Matrix.two_level_gauss_matrix_algebra.1,
    FableHilbertWalk20260819.H017Matrix.two_level_gauss_matrix_algebra.2.2.2.2.2.2.2.2⟩

#print axioms walk_root_two_level_gauss_matrix_algebra

theorem walk_root_finite_gauss_matrix_algebra :
    ∀ (T : FableHilbertWalk20260819.H017Fin.LinearEnd
          Bool FableHilbertWalk20260819.HWKernel.gaussPack)
      (v : FableHilbertWalk20260819.H004.Vec
        FableHilbertWalk20260819.HWKernel.GaussInt Bool)
      (x : Bool),
      T.map v x =
        FableHilbertWalk20260819.H017Fin.applyMat
          FableHilbertWalk20260819.HWKernel.gaussPack
          FableHilbertWalk20260819.HWKernel.enumBool
          (FableHilbertWalk20260819.H017Fin.matOf T) v x :=
  FableHilbertWalk20260819.H017Fin.two_label_gauss_matrix_algebra

#print axioms walk_root_finite_gauss_matrix_algebra

theorem walk_root_gleason_cannot_run_on_two_label :
    ¬ FableHilbertWalk20260819.H017Gleason.GleasonDimAtLeastThree
        FableHilbertWalk20260819.HWKernel.enumBool :=
  FableHilbertWalk20260819.H017Gleason.two_label_host_not_gleason_dimension

#print axioms walk_root_gleason_cannot_run_on_two_label

theorem walk_root_gleason_pack_still_imported :
    FableHilbertWalk20260819.H013.UniquenessDischarged
        FableHilbertWalk20260819.H013.hostSupplies = false :=
  FableHilbertWalk20260819.H013.uniqueness_not_discharged

#print axioms walk_root_gleason_pack_still_imported

theorem walk_root_remaining_mnC_extras :
    ¬ FableHilbertWalk20260819.H017Extras.IsFieldPack
        FableHilbertWalk20260819.HWKernel.gaussPack ∧
      ¬ FableHilbertWalk20260819.H017Extras.SpectralEigenvalueExtra
          FableHilbertWalk20260819.HWKernel.enumBool :=
  ⟨FableHilbertWalk20260819.H017Extras.gauss_not_a_field,
    FableHilbertWalk20260819.H017Extras.spectral_eigenvalue_extra_fails_on_two_label⟩

#print axioms walk_root_remaining_mnC_extras

theorem walk_root_drop_one_count :
    FableHilbertWalk20260819.H017ExtrasDropone.allExtras.length = 8 ∧
      FableHilbertWalk20260819.H017ExtrasDropone.lostExtras.length = 3 ∧
      FableHilbertWalk20260819.H017ExtrasDropone.openExtras.length = 5 ∧
      FableHilbertWalk20260819.H017ExtrasDropone.dropVerdict
          FableHilbertWalk20260819.H017ExtrasDropone.FrozenExtra.pythonDual =
        FableHilbertWalk20260819.H017ExtrasDropone.DropVerdict.open :=
  ⟨FableHilbertWalk20260819.H017ExtrasDropone.extra_list_length,
    FableHilbertWalk20260819.H017ExtrasDropone.lost_length,
    FableHilbertWalk20260819.H017ExtrasDropone.open_length,
    FableHilbertWalk20260819.H017ExtrasDropone.drop_pythonDual_necessity_open⟩

#print axioms walk_root_drop_one_count

theorem walk_root_four_report_id_dilations :
    (∀ x, FableHilbertWalk20260819.H015DilationCount.dilFF.map x =
      FableHilbertWalk20260819.H015.dil1 x) ∧
      (∀ (D : FableHilbertWalk20260819.H015DilationCount.ReportIdDilation),
        (∀ x, D.map x =
            FableHilbertWalk20260819.H015DilationCount.dilFF.map x) ∨
          (∀ x, D.map x =
              FableHilbertWalk20260819.H015DilationCount.dilFT.map x) ∨
          (∀ x, D.map x =
              FableHilbertWalk20260819.H015DilationCount.dilTF.map x) ∨
          (∀ x, D.map x =
              FableHilbertWalk20260819.H015DilationCount.dilTT.map x)) :=
  ⟨FableHilbertWalk20260819.H015DilationCount.four_reversible_dilations_of_report_identity.1.1,
    FableHilbertWalk20260819.H015DilationCount.four_reversible_dilations_of_report_identity.2.2⟩

#print axioms walk_root_four_report_id_dilations

theorem walk_root_mix_doubles_total_any
    (v : FableHilbertWalk20260819.H004.Vec
      FableHilbertWalk20260819.HWKernel.GaussInt Bool) :
    FableHilbertWalk20260819.H008.totalWeight
        FableHilbertWalk20260819.HWKernel.enumBool
        (FableHilbertWalk20260819.H010.mix v) =
      2 *
        FableHilbertWalk20260819.H008.totalWeight
          FableHilbertWalk20260819.HWKernel.enumBool v :=
  FableHilbertWalk20260819.H010Scale.mix_doubles_total_any v

#print axioms walk_root_mix_doubles_total_any

theorem walk_root_mix_mix_is_two
    (v : FableHilbertWalk20260819.H004.Vec
      FableHilbertWalk20260819.HWKernel.GaussInt Bool) :
    ∀ q : Bool,
      FableHilbertWalk20260819.H010.mix
          (FableHilbertWalk20260819.H010.mix v) q =
        FableHilbertWalk20260819.HWKernel.GaussInt.gadd (v q) (v q) :=
  FableHilbertWalk20260819.H010Hadamard.mix_mix_is_two v

#print axioms walk_root_mix_mix_is_two

theorem walk_root_bell_ptr_eq_ident :
    FableHilbertWalk20260819.H018Density.ptrSecond
        (FableHilbertWalk20260819.H018Density.ketbra4
          FableHilbertWalk20260819.H018Density.bellAmp) =
      FableHilbertWalk20260819.H017Matrix.ident
        FableHilbertWalk20260819.HWKernel.gaussPack :=
  FableHilbertWalk20260819.H018Density.bell_ptr_eq_ident

#print axioms walk_root_bell_ptr_eq_ident

theorem walk_root_diagonal_shadow_does_not_fix_channel :
    FableHilbertWalk20260819.H018Channel.dephase
        (FableHilbertWalk20260819.H018Channel.conjMix
          FableHilbertWalk20260819.H018Density.e00) =
      FableHilbertWalk20260819.H017Matrix.ident
        FableHilbertWalk20260819.HWKernel.gaussPack ∧
      FableHilbertWalk20260819.H018Channel.conjMix
          FableHilbertWalk20260819.H018Density.e00 false true ≠
        FableHilbertWalk20260819.H017Matrix.ident
          FableHilbertWalk20260819.HWKernel.gaussPack false true :=
  FableHilbertWalk20260819.H018Channel.diagonal_shadow_does_not_fix_channel

#print axioms walk_root_diagonal_shadow_does_not_fix_channel

theorem walk_root_combining_interface_has_rival :
    FableHilbertWalk20260819.H014Interface.dumpRight
        (FableHilbertWalk20260819.H004.delta
          FableHilbertWalk20260819.HWKernel.intPack false)
        (FableHilbertWalk20260819.H004.delta
          FableHilbertWalk20260819.HWKernel.intPack true)
        (false, true) ≠
      FableHilbertWalk20260819.H014.tensor
        (FableHilbertWalk20260819.H004.delta
          FableHilbertWalk20260819.HWKernel.intPack false)
        (FableHilbertWalk20260819.H004.delta
          FableHilbertWalk20260819.HWKernel.intPack true)
        (false, true) :=
  FableHilbertWalk20260819.H014Interface.two_combinings_share_interface_and_disagree.2.2.1

#print axioms walk_root_combining_interface_has_rival

theorem walk_root_one_carrier_through_H000_H016 :
    FableHilbertWalk20260819.H000.sameReport
        FableHilbertWalk20260819.H000.boolFixture
        (false, false) (false, true) ∧
      (¬ ∃ v : Bool → Int, ∀ p : Bool × Bool,
        v (FableHilbertWalk20260819.H000.boolFixture.pres p) =
          FableHilbertWalk20260819.H014.bell p) ∧
      ¬ ∃ σ : Bool → Bool, ∀ q : Bool,
        σ (σ q) = FableHilbertWalk20260819.H003.toggle q :=
  FableHilbertWalk20260819.HWFullThread.one_carrier_through_H000_H016

#print axioms walk_root_one_carrier_through_H000_H016

theorem walk_root_choice_free_fractional_weights :
    FableHilbertWalk20260819.HWKernel.rsum
        FableHilbertWalk20260819.H001Rats.fracPack
        [FableHilbertWalk20260819.H001Rats.half,
          FableHilbertWalk20260819.H001Rats.half] =
      FableHilbertWalk20260819.H001Rats.fone ∧
      FableHilbertWalk20260819.H001Rats.half ≠
        FableHilbertWalk20260819.H001Rats.fzero ∧
      FableHilbertWalk20260819.H001Rats.half ≠
        FableHilbertWalk20260819.H001Rats.fone :=
  ⟨FableHilbertWalk20260819.H001Rats.rsum_two_halves,
    FableHilbertWalk20260819.H001Rats.half_ne_zero,
    FableHilbertWalk20260819.H001Rats.half_ne_one⟩

#print axioms walk_root_choice_free_fractional_weights

theorem walk_root_two_permutation_lifts :
    (FableHilbertWalk20260819.H006.permU
        FableHilbertWalk20260819.HWKernel.gaussPack
        FableHilbertWalk20260819.H006Envelope.idRev ≠
      FableHilbertWalk20260819.H006.permU
        FableHilbertWalk20260819.HWKernel.gaussPack
        FableHilbertWalk20260819.H003.toggleRev) ∧
      ((∀ v q,
          FableHilbertWalk20260819.H006.permU
              FableHilbertWalk20260819.HWKernel.gaussPack
              FableHilbertWalk20260819.H006Envelope.idRev v q = v q) ∧
        (∀ v q,
          FableHilbertWalk20260819.H006.permU
              FableHilbertWalk20260819.HWKernel.gaussPack
              FableHilbertWalk20260819.H003.toggleRev v q =
            v (FableHilbertWalk20260819.H003.toggle q))) ∧
      (∀ {τ : Bool → Bool}
          (R : FableHilbertWalk20260819.H003.Reversible τ),
        (∀ v q,
          FableHilbertWalk20260819.H006.permU
              FableHilbertWalk20260819.HWKernel.gaussPack R v q = v q) ∨
        (∀ v q,
          FableHilbertWalk20260819.H006.permU
              FableHilbertWalk20260819.HWKernel.gaussPack R v q =
            v (FableHilbertWalk20260819.H003.toggle q))) ∧
      ¬ ∃ (τ : Bool → Bool)
        (R : FableHilbertWalk20260819.H003.Reversible τ),
        ∀ v, FableHilbertWalk20260819.H006.swapI v =
          FableHilbertWalk20260819.H006.permU
            FableHilbertWalk20260819.HWKernel.gaussPack R v :=
  FableHilbertWalk20260819.H006Envelope.two_permutation_lifts_envelope_strict

#print axioms walk_root_two_permutation_lifts

theorem walk_root_four_collapse_dilations :
    (FableHilbertWalk20260819.H015CollapseDilations.dFF.map ≠
        FableHilbertWalk20260819.H015CollapseDilations.dFT.map ∧
      FableHilbertWalk20260819.H015CollapseDilations.dFF.map ≠
        FableHilbertWalk20260819.H015CollapseDilations.dTF.map ∧
      FableHilbertWalk20260819.H015CollapseDilations.dFF.map ≠
        FableHilbertWalk20260819.H015CollapseDilations.dTT.map ∧
      FableHilbertWalk20260819.H015CollapseDilations.dFT.map ≠
        FableHilbertWalk20260819.H015CollapseDilations.dTF.map ∧
      FableHilbertWalk20260819.H015CollapseDilations.dFT.map ≠
        FableHilbertWalk20260819.H015CollapseDilations.dTT.map ∧
      FableHilbertWalk20260819.H015CollapseDilations.dTF.map ≠
        FableHilbertWalk20260819.H015CollapseDilations.dTT.map) ∧
      (∀ (D : FableHilbertWalk20260819.H015CollapseDilations.CollapseDilation),
        (∀ x, D.map x =
            FableHilbertWalk20260819.H015CollapseDilations.dFF.map x) ∨
          (∀ x, D.map x =
              FableHilbertWalk20260819.H015CollapseDilations.dFT.map x) ∨
          (∀ x, D.map x =
              FableHilbertWalk20260819.H015CollapseDilations.dTF.map x) ∨
          (∀ x, D.map x =
              FableHilbertWalk20260819.H015CollapseDilations.dTT.map x)) ∧
      (∀ (D : FableHilbertWalk20260819.H015CollapseDilations.CollapseDilation)
          (q : Bool),
        (D.map (q, FableHilbertWalk20260819.H015CollapseDilations.prepared)).1 =
          FableHilbertWalk20260819.H003.collapse q) :=
  FableHilbertWalk20260819.H015CollapseDilations.four_reversible_dilations_of_collapse

#print axioms walk_root_four_collapse_dilations

theorem walk_root_remaining_import_list :
    (H017Finish.finishFate H017ExtrasDropone.FrozenExtra.fieldC =
        H017Finish.FinishFate.refused ∧
      ¬ H017Extras.IsFieldPack HWKernel.gaussPack) ∧
    (H017Finish.finishFate H017ExtrasDropone.FrozenExtra.spectral =
        H017Finish.FinishFate.refused ∧
      ¬ H017Extras.SpectralEigenvalueExtra HWKernel.enumBool) ∧
    (H017Finish.finishFate
          H017ExtrasDropone.FrozenExtra.gleasonUniqueness =
        H017Finish.FinishFate.imported ∧
      H013.UniquenessDischarged H013.hostSupplies = false) ∧
    (H017Finish.finishFate H017ExtrasDropone.FrozenExtra.cptp =
        H017Finish.FinishFate.imported ∧
      ¬ Nonempty (H003.Reversible H003.collapse) ∧
      (¬ ∃ U : H004.Vec Int Bool → H004.Vec Int Bool,
        (∀ u v,
          H005.sesq HWKernel.intPack HWKernel.enumBool (U u) (U v) =
            H005.sesq HWKernel.intPack HWKernel.enumBool u v) ∧
        U (H004.delta HWKernel.intPack false) =
          H004.delta HWKernel.intPack false ∧
        U (H004.delta HWKernel.intPack true) =
          H004.delta HWKernel.intPack false) ∧
      (∀ x, H015DilationCount.dilFF.map x = H015.dil1 x)) ∧
    (H017Finish.finishFate H017ExtrasDropone.FrozenExtra.uniqueTensor =
        H017Finish.FinishFate.imported ∧
      ¬ ∀ u v p, H014Interface.dumpRight u v p = H014.tensor u v p) ∧
    (H017Finish.finishFate H017ExtrasDropone.FrozenExtra.circle =
        H017Finish.FinishFate.imported ∧
      ¬ H011Circle.ConnectednessShadow H011Circle.signCarrier) ∧
    (H017Finish.finishFate H017ExtrasDropone.FrozenExtra.continuousTime =
        H017Finish.FinishFate.refused ∧
      (¬ ∃ σ : Bool → Bool, ∀ q : Bool, σ (σ q) = H003.toggle q)) ∧
    H017Finish.finishFate H017ExtrasDropone.FrozenExtra.pythonDual =
      H017Finish.FinishFate.dualOutsideLean ∧
    H017Finish.assigned H017Finish.PhysicsName.susy = false ∧
    H017Finish.assigned H017Finish.PhysicsName.standardModelGauge = false :=
  H017Finish.remaining_import_list

#print axioms walk_root_remaining_import_list

end FableHilbertWalk20260819

private def l5aProvenance : String :=
  "Origin: lean4/HilbertWalkAll.lean Claim: walk_root_reaches_boundary AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
