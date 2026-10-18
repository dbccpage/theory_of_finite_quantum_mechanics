import «primitive_bridge»
import «q_level_lggr_bridge»

/-!
QM bridge for PaperQF003 trace/density representation limits.

The imported PaperQF003 facts are representation-firewall facts: diagonal lifts
preserve selected finite `l1` magnitude, while density normalization can erase
absolute trace mass.  They are used as QM non-promotion support, not as a
derivation of quantum mechanics.
-/

namespace QM

namespace PaperQF003TraceBridge

noncomputable section

variable {E : Type*} [Fintype E]

theorem selected_diagonal_trace_preserves_l1 (h : E -> ℚ) :
    PaperQF003.diagonalTraceNorm (PaperQF003.diagonalLift h) =
      PaperQF003.l1Magnitude h :=
  PaperQF003.flin_trace_norm_eq_l1 h

theorem density_lift_forgets_nonzero_scale
    {a : ℚ} (ha : a ≠ 0) (mass : E -> ℚ) :
    PaperQF003.densityLift (fun e => a * mass e) =
      PaperQF003.densityLift mass :=
  PaperQF003.densityLift_scale_invariant ha mass

theorem density_local_green_trace_mass_global_red :
    (∃ F :
        (PaperQF002.scalarRayPrimitiveDifference (Γ := Bool)).ResidualQuotient ->
          (Bool -> ℚ),
      ∀ mass : Bool -> ℚ,
        F ((PaperQF002.scalarRayPrimitiveDifference (Γ := Bool)).classOf mass) =
          PaperQF003.densityLift mass) ∧
      ¬ (∃ F :
        (PaperQF002.scalarRayPrimitiveDifference (Γ := Bool)).ResidualQuotient ->
          ((Bool -> ℚ) × ℚ),
      ∀ mass : Bool -> ℚ,
        F ((PaperQF002.scalarRayPrimitiveDifference (Γ := Bool)).classOf mass) =
          (PaperQF003.densityLift mass, PaperQF002.totalWeight mass)) :=
  PaperQF003.density_local_green_trace_mass_global_red

theorem density_traceMass_lggr_of_scaled_witness
    {E : Type} [Fintype E]
    {a : ℚ} (ha : a ≠ 0) (mass : E -> ℚ)
    (hMass :
      PaperQF002.totalWeight mass ≠
        PaperQF002.totalWeight (fun e => a * mass e)) :
    (∃ F :
        (PaperQF002.scalarRayPrimitiveDifference (Γ := E)).ResidualQuotient ->
          (E -> ℚ),
      ∀ w : E -> ℚ,
        F ((PaperQF002.scalarRayPrimitiveDifference (Γ := E)).classOf w) =
          PaperQF003.densityLift w) ∧
      ¬ (∃ F :
        (PaperQF002.scalarRayPrimitiveDifference (Γ := E)).ResidualQuotient ->
          ((E -> ℚ) × ℚ),
      ∀ w : E -> ℚ,
        F ((PaperQF002.scalarRayPrimitiveDifference (Γ := E)).classOf w) =
          (PaperQF003.densityLift w, PaperQF002.totalWeight w)) :=
  PaperQF003.density_traceMass_lggr_of_scaled_witness ha mass hMass

/--
PaperQF003 as a Q-level non-promotion theorem: normalized density is a
quotient-compatible diagnostic, but the paired density/trace-mass readout is
blocked by a scalar-ray witness. This is an authority-firewall statement, not a
derivation of QM.
-/
theorem density_traceMass_q_bridge_not_authority_certificate
    {E : Type} [Fintype E]
    {a : ℚ} (ha : a ≠ 0) (mass : E -> ℚ)
    (hMass :
      PaperQF002.totalWeight mass ≠
        PaperQF002.totalWeight (fun e => a * mass e)) :
    (∃ F :
        (PaperQF002.scalarRayPrimitiveDifference (Γ := E)).ResidualQuotient ->
          (E -> ℚ),
      ∀ w : E -> ℚ,
        F ((PaperQF002.scalarRayPrimitiveDifference (Γ := E)).classOf w) =
          PaperQF003.densityLift w) ∧
      ¬ (∃ F :
        (PaperQF002.scalarRayPrimitiveDifference (Γ := E)).ResidualQuotient ->
          ((E -> ℚ) × ℚ),
      ∀ w : E -> ℚ,
        F ((PaperQF002.scalarRayPrimitiveDifference (Γ := E)).classOf w) =
          (PaperQF003.densityLift w, PaperQF002.totalWeight w)) := by
  let P := PaperQF002.scalarRayPrimitiveDifference (Γ := E)
  have hDensity :
      ResidualDensityBridge.QuotientCompatible P
        (fun w : E -> ℚ => PaperQF003.densityLift w) := by
    intro x y hxy
    exact PaperQF002.directProb_invariantCongruent_scalarRay x y hxy
  have hxy : P.ZeroRel mass (fun e => a * mass e) := by
    exact PaperQF003.scalarRay_zeroRel_scaled ha mass
  have hBridge :=
    QLevelLGGRBridge.density_q_bridge_not_authority_certificate
      P
      (fun w : E -> ℚ => PaperQF003.densityLift w)
      (fun w : E -> ℚ => PaperQF002.totalWeight w)
      hDensity
      (x := mass) (y := fun e => a * mass e)
      hxy hMass
  simpa [P] using hBridge

/--
Declared-domain version of the PaperQF003 Q-level non-promotion theorem. This is
the QM-facing form of the finite PrimitiveDifference/Rust-checker witness.
-/
theorem finiteDomain_density_traceMass_q_bridge_not_authority_certificate
    {E : Type} [Fintype E]
    {a : ℚ} (ha : a ≠ 0) (mass : E -> ℚ)
    (hMass :
      PaperQF002.totalWeight mass ≠
        PaperQF002.totalWeight (fun e => a * mass e)) :
    (∃ F :
        (OmegaCore.PrimitiveDifferenceFinite.restrict
          (PaperQF002.scalarRayPrimitiveDifference (Γ := E))
          (PaperQF003.twoScaleDomain (E := E) a mass)).ResidualQuotient ->
          (E -> ℚ),
      ∀ c : {w : E -> ℚ // PaperQF003.twoScaleDomain (E := E) a mass w},
        F ((OmegaCore.PrimitiveDifferenceFinite.restrict
            (PaperQF002.scalarRayPrimitiveDifference (Γ := E))
            (PaperQF003.twoScaleDomain (E := E) a mass)).classOf c) =
          PaperQF003.densityLift c.val) ∧
      ¬ (∃ F :
        (OmegaCore.PrimitiveDifferenceFinite.restrict
          (PaperQF002.scalarRayPrimitiveDifference (Γ := E))
          (PaperQF003.twoScaleDomain (E := E) a mass)).ResidualQuotient ->
          ((E -> ℚ) × ℚ),
      ∀ c : {w : E -> ℚ // PaperQF003.twoScaleDomain (E := E) a mass w},
        F ((OmegaCore.PrimitiveDifferenceFinite.restrict
            (PaperQF002.scalarRayPrimitiveDifference (Γ := E))
            (PaperQF003.twoScaleDomain (E := E) a mass)).classOf c) =
          (PaperQF003.densityLift c.val, PaperQF002.totalWeight c.val)) := by
  let P := PaperQF002.scalarRayPrimitiveDifference (Γ := E)
  let S := PaperQF003.twoScaleDomain (E := E) a mass
  let base : {w : E -> ℚ // S w} := ⟨mass, Or.inl rfl⟩
  let scaled : {w : E -> ℚ // S w} := ⟨fun e => a * mass e, Or.inr rfl⟩
  have hDensity :
      ResidualDensityBridge.QuotientCompatible
        (OmegaCore.PrimitiveDifferenceFinite.restrict P S)
        (fun c : {w : E -> ℚ // S w} => PaperQF003.densityLift c.val) := by
    intro x y hxy
    exact PaperQF002.directProb_invariantCongruent_scalarRay x.val y.val hxy
  have hxy :
      (OmegaCore.PrimitiveDifferenceFinite.restrict P S).ZeroRel
        base scaled := by
    exact PaperQF003.scalarRay_zeroRel_scaled ha mass
  have hne :
      (fun c : {w : E -> ℚ // S w} => PaperQF002.totalWeight c.val) base ≠
        (fun c : {w : E -> ℚ // S w} => PaperQF002.totalWeight c.val) scaled := by
    simpa [base, scaled] using hMass
  have hBridge :=
    QLevelLGGRBridge.density_q_bridge_not_authority_certificate
      (OmegaCore.PrimitiveDifferenceFinite.restrict P S)
      (fun c : {w : E -> ℚ // S w} => PaperQF003.densityLift c.val)
      (fun c : {w : E -> ℚ // S w} => PaperQF002.totalWeight c.val)
      hDensity
      (x := base) (y := scaled)
      hxy hne
  simpa [P, S] using hBridge

/--
Q-level non-promotion form for downstream trace-mass readouts. If a declared
readout of trace mass still separates the scalar-ray witness, pairing that
readout with density remains global-red.
-/
theorem density_traceMass_readout_q_bridge_not_authority_certificate
    {E : Type} [Fintype E] {Readout : Type}
    {a : ℚ} (ha : a ≠ 0) (mass : E -> ℚ)
    (readout : ℚ -> Readout)
    (hReadout :
      readout (PaperQF002.totalWeight mass) ≠
        readout (PaperQF002.totalWeight (fun e => a * mass e))) :
    (∃ F :
        (PaperQF002.scalarRayPrimitiveDifference (Γ := E)).ResidualQuotient ->
          (E -> ℚ),
      ∀ w : E -> ℚ,
        F ((PaperQF002.scalarRayPrimitiveDifference (Γ := E)).classOf w) =
          PaperQF003.densityLift w) ∧
      ¬ (∃ F :
        (PaperQF002.scalarRayPrimitiveDifference (Γ := E)).ResidualQuotient ->
          ((E -> ℚ) × Readout),
      ∀ w : E -> ℚ,
        F ((PaperQF002.scalarRayPrimitiveDifference (Γ := E)).classOf w) =
          (PaperQF003.densityLift w, readout (PaperQF002.totalWeight w))) := by
  let P := PaperQF002.scalarRayPrimitiveDifference (Γ := E)
  have hDensity :
      ResidualDensityBridge.QuotientCompatible P
        (fun w : E -> ℚ => PaperQF003.densityLift w) := by
    intro x y hxy
    exact PaperQF002.directProb_invariantCongruent_scalarRay x y hxy
  have hxy : P.ZeroRel mass (fun e => a * mass e) := by
    exact PaperQF003.scalarRay_zeroRel_scaled ha mass
  have hBridge :=
    QLevelLGGRBridge.density_q_bridge_not_authority_certificate
      P
      (fun w : E -> ℚ => PaperQF003.densityLift w)
      (fun w : E -> ℚ => readout (PaperQF002.totalWeight w))
      hDensity
      (x := mass) (y := fun e => a * mass e)
      hxy hReadout
  simpa [P] using hBridge

/--
Finite declared-domain/Rust-checker form of the Q-level non-promotion theorem
for downstream trace-mass readouts.
-/
theorem finiteDomain_density_traceMass_readout_q_bridge_not_authority_certificate
    {E : Type} [Fintype E] {Readout : Type}
    {a : ℚ} (ha : a ≠ 0) (mass : E -> ℚ)
    (readout : ℚ -> Readout)
    (hReadout :
      readout (PaperQF002.totalWeight mass) ≠
        readout (PaperQF002.totalWeight (fun e => a * mass e))) :
    (∃ F :
        (OmegaCore.PrimitiveDifferenceFinite.restrict
          (PaperQF002.scalarRayPrimitiveDifference (Γ := E))
          (PaperQF003.twoScaleDomain (E := E) a mass)).ResidualQuotient ->
          (E -> ℚ),
      ∀ c : {w : E -> ℚ // PaperQF003.twoScaleDomain (E := E) a mass w},
        F ((OmegaCore.PrimitiveDifferenceFinite.restrict
            (PaperQF002.scalarRayPrimitiveDifference (Γ := E))
            (PaperQF003.twoScaleDomain (E := E) a mass)).classOf c) =
          PaperQF003.densityLift c.val) ∧
      ¬ (∃ F :
        (OmegaCore.PrimitiveDifferenceFinite.restrict
          (PaperQF002.scalarRayPrimitiveDifference (Γ := E))
          (PaperQF003.twoScaleDomain (E := E) a mass)).ResidualQuotient ->
          ((E -> ℚ) × Readout),
      ∀ c : {w : E -> ℚ // PaperQF003.twoScaleDomain (E := E) a mass w},
        F ((OmegaCore.PrimitiveDifferenceFinite.restrict
            (PaperQF002.scalarRayPrimitiveDifference (Γ := E))
            (PaperQF003.twoScaleDomain (E := E) a mass)).classOf c) =
          (PaperQF003.densityLift c.val,
            readout (PaperQF002.totalWeight c.val))) := by
  let P := PaperQF002.scalarRayPrimitiveDifference (Γ := E)
  let S := PaperQF003.twoScaleDomain (E := E) a mass
  let base : {w : E -> ℚ // S w} := ⟨mass, Or.inl rfl⟩
  let scaled : {w : E -> ℚ // S w} := ⟨fun e => a * mass e, Or.inr rfl⟩
  have hDensity :
      ResidualDensityBridge.QuotientCompatible
        (OmegaCore.PrimitiveDifferenceFinite.restrict P S)
        (fun c : {w : E -> ℚ // S w} => PaperQF003.densityLift c.val) := by
    intro x y hxy
    exact PaperQF002.directProb_invariantCongruent_scalarRay x.val y.val hxy
  have hxy :
      (OmegaCore.PrimitiveDifferenceFinite.restrict P S).ZeroRel
        base scaled := by
    exact PaperQF003.scalarRay_zeroRel_scaled ha mass
  have hne :
      (fun c : {w : E -> ℚ // S w} =>
        readout (PaperQF002.totalWeight c.val)) base ≠
        (fun c : {w : E -> ℚ // S w} =>
          readout (PaperQF002.totalWeight c.val)) scaled := by
    simpa [base, scaled] using hReadout
  have hBridge :=
    QLevelLGGRBridge.density_q_bridge_not_authority_certificate
      (OmegaCore.PrimitiveDifferenceFinite.restrict P S)
      (fun c : {w : E -> ℚ // S w} => PaperQF003.densityLift c.val)
      (fun c : {w : E -> ℚ // S w} =>
        readout (PaperQF002.totalWeight c.val))
      hDensity
      (x := base) (y := scaled)
      hxy hne
  simpa [P, S] using hBridge

/--
QM-facing EPK dashboard form of the PaperQF003 scalar-ray obstruction. An
arbitrary family of local density-derived diagnostics descends, but a
trace-mass readout that still separates the scalar witness cannot be glued into
the same quotient dashboard.
-/
theorem density_dashboard_traceMass_readout_epk_not_authority_certificate
    {E : Type} [Fintype E] {ι Local Global : Type}
    {a : ℚ} (ha : a ≠ 0) (mass : E -> ℚ)
    (localReadout : ι -> (E -> ℚ) -> Local)
    (traceReadout : ℚ -> Global)
    (hTrace :
      traceReadout (PaperQF002.totalWeight mass) ≠
        traceReadout (PaperQF002.totalWeight (fun e => a * mass e))) :
    (∃ F :
        (PaperQF002.scalarRayPrimitiveDifference (Γ := E)).ResidualQuotient ->
          (ι -> Local),
      ∀ w : E -> ℚ,
        F ((PaperQF002.scalarRayPrimitiveDifference (Γ := E)).classOf w) =
          (fun i => localReadout i (PaperQF003.densityLift w))) ∧
      ¬ (∃ F :
        (PaperQF002.scalarRayPrimitiveDifference (Γ := E)).ResidualQuotient ->
          ((ι -> Local) × Global),
      ∀ w : E -> ℚ,
        F ((PaperQF002.scalarRayPrimitiveDifference (Γ := E)).classOf w) =
          ((fun i => localReadout i (PaperQF003.densityLift w)),
            traceReadout (PaperQF002.totalWeight w))) := by
  exact
    PaperQF003.density_dashboard_traceMass_readout_epk_lggr_of_scaled_witness
      ha mass localReadout traceReadout hTrace

/--
Finite declared-domain/Rust-checker QM-facing EPK dashboard form of the
PaperQF003 scalar-ray obstruction.
-/
theorem finiteDomain_density_dashboard_traceMass_readout_epk_not_authority_certificate
    {E : Type} [Fintype E] {ι Local Global : Type}
    {a : ℚ} (ha : a ≠ 0) (mass : E -> ℚ)
    (localReadout : ι -> (E -> ℚ) -> Local)
    (traceReadout : ℚ -> Global)
    (hTrace :
      traceReadout (PaperQF002.totalWeight mass) ≠
        traceReadout (PaperQF002.totalWeight (fun e => a * mass e))) :
    (∃ F :
        (OmegaCore.PrimitiveDifferenceFinite.restrict
          (PaperQF002.scalarRayPrimitiveDifference (Γ := E))
          (PaperQF003.twoScaleDomain (E := E) a mass)).ResidualQuotient ->
          (ι -> Local),
      ∀ c : {w : E -> ℚ // PaperQF003.twoScaleDomain (E := E) a mass w},
        F ((OmegaCore.PrimitiveDifferenceFinite.restrict
            (PaperQF002.scalarRayPrimitiveDifference (Γ := E))
            (PaperQF003.twoScaleDomain (E := E) a mass)).classOf c) =
          (fun i => localReadout i (PaperQF003.densityLift c.val))) ∧
      ¬ (∃ F :
        (OmegaCore.PrimitiveDifferenceFinite.restrict
          (PaperQF002.scalarRayPrimitiveDifference (Γ := E))
          (PaperQF003.twoScaleDomain (E := E) a mass)).ResidualQuotient ->
          ((ι -> Local) × Global),
      ∀ c : {w : E -> ℚ // PaperQF003.twoScaleDomain (E := E) a mass w},
        F ((OmegaCore.PrimitiveDifferenceFinite.restrict
            (PaperQF002.scalarRayPrimitiveDifference (Γ := E))
            (PaperQF003.twoScaleDomain (E := E) a mass)).classOf c) =
          ((fun i => localReadout i (PaperQF003.densityLift c.val)),
            traceReadout (PaperQF002.totalWeight c.val))) := by
  exact
    PaperQF003.finiteDomain_density_dashboard_traceMass_readout_epk_lggr_of_scaled_witness
      ha mass localReadout traceReadout hTrace

end

end PaperQF003TraceBridge

end QM

#print axioms QM.PaperQF003TraceBridge.selected_diagonal_trace_preserves_l1
#print axioms QM.PaperQF003TraceBridge.density_lift_forgets_nonzero_scale
#print axioms QM.PaperQF003TraceBridge.density_local_green_trace_mass_global_red
#print axioms QM.PaperQF003TraceBridge.density_traceMass_lggr_of_scaled_witness
#print axioms QM.PaperQF003TraceBridge.density_traceMass_q_bridge_not_authority_certificate
#print axioms QM.PaperQF003TraceBridge.finiteDomain_density_traceMass_q_bridge_not_authority_certificate
#print axioms QM.PaperQF003TraceBridge.density_traceMass_readout_q_bridge_not_authority_certificate
#print axioms QM.PaperQF003TraceBridge.finiteDomain_density_traceMass_readout_q_bridge_not_authority_certificate
#print axioms QM.PaperQF003TraceBridge.density_dashboard_traceMass_readout_epk_not_authority_certificate
#print axioms QM.PaperQF003TraceBridge.finiteDomain_density_dashboard_traceMass_readout_epk_not_authority_certificate
