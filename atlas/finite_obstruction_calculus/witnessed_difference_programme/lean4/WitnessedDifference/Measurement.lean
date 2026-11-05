import WitnessedDifference.Observer

/-!
# Measurement packets

This module provides a deliberately bounded data model. A measurand
specification and a reported-value carrier are separate types. Metrological
traceability is represented by a nonempty, structurally unbroken calibration
chain in which every calibration contributes a nonnegative uncertainty term.
Report provenance and later re-access are separate from that chain.

No declaration says that this packet is a complete VIM formalization, that an
observer report is by itself a measurement, or that internal evidence certifies
an external standard.
-/

namespace WitnessedDifference

/-!
The references indexed by `0, ..., length` make consecutive calibrations share
an endpoint by construction. Thus the chain cannot contain an unconnected pair
of adjacent steps.
-/
structure CalibrationChain (Reference Procedure : Type _) where
  length : Nat
  nonempty : 0 < length
  reference : Fin (length + 1) → Reference
  procedure : Fin length → Procedure
  calibrates : Procedure → Reference → Reference → Prop
  step_valid : ∀ index,
    calibrates (procedure index) (reference index.castSucc)
      (reference index.succ)
  uncertaintyContribution : Fin length → ℚ
  uncertainty_nonnegative :
    ∀ index, 0 ≤ uncertaintyContribution index

structure MeasurementPacket
    (World Report Trace Measurand Indication Result Unit
      Reference Procedure : Type _) where
  acceptedObservation : AcceptedObservation World Report Trace
  measurand : Measurand
  indication : Report → Indication
  calibratedValue : Indication → Result
  scale : Result → ℚ
  unit : Unit
  calibrationChain : CalibrationChain Reference Procedure
  resultUncertainty : Result → ℚ
  resultUncertainty_nonnegative :
    ∀ result, 0 ≤ resultUncertainty result
  provenance : Trace → Option (Indication × Result)
  provenance_replay :
    provenance acceptedObservation.receipt.trace =
      some
        (indication acceptedObservation.receipt.report,
          calibratedValue (indication acceptedObservation.receipt.report))

namespace MeasurementPacket

theorem calibration_chain_nonempty
    {World Report Trace Measurand Indication Result Unit
      Reference Procedure : Type _}
    (M : MeasurementPacket World Report Trace Measurand Indication
      Result Unit Reference Procedure) :
    0 < M.calibrationChain.length := by
  exact M.calibrationChain.nonempty

theorem every_calibration_step_documented
    {World Report Trace Measurand Indication Result Unit
      Reference Procedure : Type _}
    (M : MeasurementPacket World Report Trace Measurand Indication
      Result Unit Reference Procedure)
    (index : Fin M.calibrationChain.length) :
    M.calibrationChain.calibrates
      (M.calibrationChain.procedure index)
      (M.calibrationChain.reference index.castSucc)
      (M.calibrationChain.reference index.succ) := by
  exact M.calibrationChain.step_valid index

theorem uncertainty_fields_nonnegative
    {World Report Trace Measurand Indication Result Unit
      Reference Procedure : Type _}
    (M : MeasurementPacket World Report Trace Measurand Indication
      Result Unit Reference Procedure)
    (index : Fin M.calibrationChain.length)
    (result : Result) :
    0 ≤ M.calibrationChain.uncertaintyContribution index ∧
      0 ≤ M.resultUncertainty result := by
  exact ⟨M.calibrationChain.uncertainty_nonnegative index,
    M.resultUncertainty_nonnegative result⟩

theorem report_and_result_reaccessible
    {World Report Trace Measurand Indication Result Unit
      Reference Procedure : Type _}
    (M : MeasurementPacket World Report Trace Measurand Indication
      Result Unit Reference Procedure) :
    M.acceptedObservation.receipt.observer.memory.retrieve
        M.acceptedObservation.receipt.trace =
      some M.acceptedObservation.receipt.report ∧
    M.provenance M.acceptedObservation.receipt.trace =
      some
        (M.indication M.acceptedObservation.receipt.report,
          M.calibratedValue
            (M.indication M.acceptedObservation.receipt.report)) := by
  exact ⟨M.acceptedObservation.receipt.report_reaccessible,
    M.provenance_replay⟩

end MeasurementPacket
end WitnessedDifference
