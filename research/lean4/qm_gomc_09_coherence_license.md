namespace QM.GOMC09

/--
Amplitude presentation data is representation-layer data only. The fields are
intentionally finite/natural here: GOMC-09 is about the license boundary, not
about analytic square roots.
-/
structure AmplitudePresentation where
  amp0_re : Nat
  amp0_im : Nat
  amp1_re : Nat
  amp1_im : Nat

/-- A request that carries amplitudes plus the extra license fields. -/
structure CoherenceRequest where
  amplitude : AmplitudePresentation
  phase_relation_declared : Bool
  interference_rule_declared : Bool

/--
Licensed coherence requires more than amplitude coordinates. It requires both
a declared phase relation and a declared interference/update rule.
-/
def LicensedCoherence (r : CoherenceRequest) : Prop :=
  r.phase_relation_declared = true ∧ r.interference_rule_declared = true

/-- A concrete amplitude-only request: coordinates are present, licenses absent. -/
def amplitudeOnlyRequest : CoherenceRequest where
  amplitude :=
    { amp0_re := 1
      amp0_im := 0
      amp1_re := 1
      amp1_im := 0 }
  phase_relation_declared := false
  interference_rule_declared := false

/--
GOMC-09: amplitude coordinates by themselves do not imply licensed coherence.
The missing phase/interference license blocks promotion.
-/
theorem amplitude_not_implies_licensed_coherence :
    ¬ LicensedCoherence amplitudeOnlyRequest := by
  intro h
  exact Bool.false_ne_true h.left

/--
There exists a request with amplitude data whose coherence license is absent.
This records the finite boundary used by the GOMC ledger.
-/
theorem coherence_license_boundary :
    ∃ r : CoherenceRequest, ¬ LicensedCoherence r := by
  exact ⟨amplitudeOnlyRequest, amplitude_not_implies_licensed_coherence⟩

#print axioms QM.GOMC09.amplitude_not_implies_licensed_coherence
#print axioms QM.GOMC09.coherence_license_boundary

end QM.GOMC09
