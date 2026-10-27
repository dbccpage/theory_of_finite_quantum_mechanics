import «l010_01_born_redundancy»
import «primitive_lift_certificate»
import «primitive_repair_boundary»
import «primitive_spine_summary»
import «primitive_terminal_packet»
/-!
Paper 010 / PL-010-1 theorem aggregator.

This file gives stable theorem names for the four PL-010-1 Lean hardening
targets. The underlying kernels live in `L010_01_BornRedundancy`; the statements
below only package those checked results and do not claim a Born-rule derivation.
ENC-0317 remains imported/conditional.
-/

open scoped BigOperators

namespace PaperQF002

noncomputable section

variable {Γ ι : Type*}

/-! Theorem 1: direct normalization. -/

theorem PL010_1_Theorem1_direct_normalization
    [Fintype Γ] (w : Γ → ℚ)
    (hw : ∀ γ, 0 ≤ w γ) (hW : 0 < totalWeight w) :
    (∀ γ, 0 ≤ directProb w γ ∧ directProb w γ ≤ 1) ∧
      ∑ γ, directProb w γ = 1 := by
  exact directNormalization_unit_interval_certificate w hw hW

/-! Theorem 2: finite rational natural-power proxy for strict `p > 1` aggregation. -/

theorem PL010_1_Theorem2_strict_disjoint_power_subadditivity
    {a b : ℚ} {p : ℕ}
    (ha : 0 < a) (hb : 0 < b) (hp : 2 ≤ p) :
    a ^ p + b ^ p < (a + b) ^ p := by
  exact lp_nat_power_strict_subadditivity_two_positive_blocks ha hb hp

theorem PL010_1_Theorem2_l1_disjoint_additivity_certificate
    [Fintype Γ] (x y : Γ → ℚ) (hdisj : disjointSupport x y) :
    l1Norm (fun γ => x γ + y γ) = l1Norm x + l1Norm y ∧
      l1AdditivityDefect x y = 0 := by
  exact ⟨l1Norm_add_of_disjointSupport x y hdisj,
    l1AdditivityDefect_eq_zero_of_disjointSupport x y hdisj⟩

/-! Theorem 3: finite row-sparsity of descent-compatible rows. -/

theorem PL010_1_Theorem3_row_sparsity
    [Fintype ι] [DecidableEq ι] (a : ι → ℚ) :
    finiteRowDescentCompatible a ↔ rowSupportSubsingleton a := by
  exact finiteRowDescentCompatible_iff_rowSupportSubsingleton a

theorem PL010_1_Theorem3_squared_row_factors_iff_sparse
    [Fintype ι] [DecidableEq ι] (a : ι → ℚ) :
    (∃ F :
        (phaseBlindPrimitiveDifference :
          ObstructionCore.PrimitiveDifference (ι → ℚ) (ι → ℚ)).ResidualQuotient → ℚ,
        ∀ x : ι → ℚ,
          F ((phaseBlindPrimitiveDifference :
            ObstructionCore.PrimitiveDifference (ι → ℚ) (ι → ℚ)).classOf x) =
            finiteRowSquaredEval a x) ↔
      rowSupportSubsingleton a := by
  exact finiteRowSquaredEval_factor_exists_iff_rowSupportSubsingleton a

/-! Theorem 4: Hilbert-lift/Born-normalization redundancy. -/

theorem PL010_1_Theorem4_born_normalization_redundancy
    [Fintype Γ] (w normSq : Γ → ℚ)
    (h : ∀ γ, normSq γ = w γ)
    (hw : ∀ γ, 0 ≤ w γ) (hW : 0 < totalWeight w) :
    (∀ γ, 0 ≤ bornProbFromNormSq normSq γ) ∧
      (∑ γ, bornProbFromNormSq normSq γ = 1) ∧
        (∀ γ, bornProbFromNormSq normSq γ = directProb w γ) := by
  exact bornNormalization_redundant_certificate w normSq h hw hW

/-! Operator-atlas LGGR non-promotion.

This is the primitive-difference kernel behind Paper 011 §6a / ENC-0931:
local chart descent, even chartwise and as a bundled atlas, does not make a
global diagnostic descend when the global diagnostic separates zero-related
states.
-/

universe u v w

variable {α : Type u} {β : Type v} {I Ω γ η Q : Type w}

theorem operatorAtlas_invariant_of_each_chart
    (P : ObstructionCore.PrimitiveDifference α β)
    (chart : I → α → γ)
    (hchart : ∀ i : I,
      P.InvariantCongruent (fun x : α => chart i x)) :
    P.InvariantCongruent (fun x : α => fun i : I => chart i x) := by
  intro x y hxy
  funext i
  exact hchart i x y hxy

theorem operatorAtlas_localGreen_globalRed_nonpromotion
    (P : ObstructionCore.PrimitiveDifference α β)
    (chart : I → α → γ) (global : α → η)
    (hchart : ∀ i : I,
      P.InvariantCongruent (fun x : α => chart i x))
    {x y : α} (hxy : P.ZeroRel x y) (hglobal : global x ≠ global y) :
    (∀ i : I,
      ∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = chart i x) ∧
      (∃ F : P.ResidualQuotient → (I → γ),
        ∀ x : α, F (P.classOf x) = (fun i : I => chart i x)) ∧
      ¬ (∃ F : P.ResidualQuotient → (I → γ) × η,
        ∀ x : α,
          F (P.classOf x) = ((fun i : I => chart i x), global x)) := by
  have hatlas :
      P.InvariantCongruent (fun x : α => fun i : I => chart i x) :=
    operatorAtlas_invariant_of_each_chart P chart hchart
  refine ⟨?_, ?_, ?_⟩
  · intro i
    exact
      (ObstructionCore.PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
          P (fun x : α => chart i x)).mpr (hchart i)
  · exact
      (ObstructionCore.PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
          P (fun x : α => fun i : I => chart i x)).mpr hatlas
  · exact
      (ObstructionCore.PrimitiveDifference.localGreenGlobalRed_pair_obstruction_of_witness
          P (fun x : α => fun i : I => chart i x) global hatlas hxy hglobal).2

def operatorAtlasOverlapPairs
    (left right : Ω → I) (chart : I → α → γ) (x : α) :
    Ω → γ × γ :=
  fun overlap => (chart (left overlap) x, chart (right overlap) x)

theorem operatorAtlas_overlapPairs_invariant_of_each_chart
    (P : ObstructionCore.PrimitiveDifference α β)
    (left right : Ω → I) (chart : I → α → γ)
    (hchart : ∀ i : I,
      P.InvariantCongruent (fun x : α => chart i x)) :
    P.InvariantCongruent
      (operatorAtlasOverlapPairs (α := α) left right chart) := by
  intro x y hxy
  funext overlap
  exact Prod.ext (hchart (left overlap) x y hxy)
    (hchart (right overlap) x y hxy)

theorem operatorAtlas_overlapGate_globalRed_nonpromotion
    (P : ObstructionCore.PrimitiveDifference α β)
    (left right : Ω → I) (chart : I → α → γ) (global : α → η)
    (hchart : ∀ i : I,
      P.InvariantCongruent (fun x : α => chart i x))
    {x y : α} (hxy : P.ZeroRel x y) (hglobal : global x ≠ global y) :
    (∀ i : I,
      ∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = chart i x) ∧
      (∃ F : P.ResidualQuotient → (I → γ),
        ∀ x : α, F (P.classOf x) = (fun i : I => chart i x)) ∧
      (∃ F : P.ResidualQuotient → (Ω → γ × γ),
        ∀ x : α,
          F (P.classOf x) =
            operatorAtlasOverlapPairs (α := α) left right chart x) ∧
      ¬ (∃ F :
        P.ResidualQuotient → ((I → γ) × (Ω → γ × γ)) × η,
        ∀ x : α,
          F (P.classOf x) =
            (((fun i : I => chart i x),
              operatorAtlasOverlapPairs (α := α) left right chart x),
              global x)) := by
  have hbase :=
    operatorAtlas_localGreen_globalRed_nonpromotion
      P chart global hchart hxy hglobal
  have hatlas :
      P.InvariantCongruent (fun x : α => fun i : I => chart i x) :=
    operatorAtlas_invariant_of_each_chart P chart hchart
  have hoverlap :
      P.InvariantCongruent
        (operatorAtlasOverlapPairs (α := α) left right chart) :=
    operatorAtlas_overlapPairs_invariant_of_each_chart P left right chart hchart
  have hlocal := hbase.1
  have hatlasFactor := hbase.2.1
  have hoverlapFactor :
      ∃ F : P.ResidualQuotient → (Ω → γ × γ),
        ∀ x : α,
          F (P.classOf x) =
            operatorAtlasOverlapPairs (α := α) left right chart x :=
    (ObstructionCore.PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
      P (operatorAtlasOverlapPairs (α := α) left right chart)).mpr hoverlap
  have hpairInvariant :
      P.InvariantCongruent
        (fun x : α =>
          ((fun i : I => chart i x),
            operatorAtlasOverlapPairs (α := α) left right chart x)) := by
    intro a b hab
    exact Prod.ext (hatlas a b hab) (hoverlap a b hab)
  have hno :
      ¬ (∃ F :
        P.ResidualQuotient → ((I → γ) × (Ω → γ × γ)) × η,
        ∀ x : α,
          F (P.classOf x) =
            (((fun i : I => chart i x),
              operatorAtlasOverlapPairs (α := α) left right chart x),
              global x)) :=
    (ObstructionCore.PrimitiveDifference.localGreenGlobalRed_pair_obstruction_of_witness
      P
      (fun x : α =>
        ((fun i : I => chart i x),
          operatorAtlasOverlapPairs (α := α) left right chart x))
      global hpairInvariant hxy hglobal).2
  exact ⟨hlocal, hatlasFactor, hoverlapFactor, hno⟩

theorem operatorAtlas_overlapGate_terminalCertificate_nonpromotion
    (P : ObstructionCore.PrimitiveDifference α β)
    (left right : Ω → I) (chart : I → α → γ) (global : α → η)
    (hchart : ∀ i : I,
      P.InvariantCongruent (fun x : α => chart i x))
    {x y : α} (hxy : P.ZeroRel x y) (hglobal : global x ≠ global y)
    (C : ObstructionCore.ObstructionClassifier Q) (q : Q)
    (packet : ObstructionCore.PrimitiveTerminalPacket.TerminalPacket C q)
    (hExact : C.IsExactRepair q) (hCertificate : packet.hasCertificate = false) :
    ((∀ i : I,
      ∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = chart i x) ∧
      (∃ F : P.ResidualQuotient → (I → γ),
        ∀ x : α, F (P.classOf x) = (fun i : I => chart i x)) ∧
      (∃ F : P.ResidualQuotient → (Ω → γ × γ),
        ∀ x : α,
          F (P.classOf x) =
            operatorAtlasOverlapPairs (α := α) left right chart x) ∧
      ¬ (∃ F :
        P.ResidualQuotient → ((I → γ) × (Ω → γ × γ)) × η,
        ∀ x : α,
          F (P.classOf x) =
            (((fun i : I => chart i x),
              operatorAtlasOverlapPairs (α := α) left right chart x),
              global x))) ∧
      ¬ ObstructionCore.PrimitiveTerminalPacket.PacketRepaired packet := by
  exact
    ⟨operatorAtlas_overlapGate_globalRed_nonpromotion
        P left right chart global hchart hxy hglobal,
      ObstructionCore.PrimitiveTerminalPacket.packet_exact_without_certificate_not_repaired
        C q packet hExact hCertificate⟩

theorem operatorAtlas_overlapGate_terminalReady_nonpromotion
    (P : ObstructionCore.PrimitiveDifference α β)
    (left right : Ω → I) (chart : I → α → γ) (global : α → η)
    (hchart : ∀ i : I,
      P.InvariantCongruent (fun x : α => chart i x))
    {x y : α} (hxy : P.ZeroRel x y) (hglobal : global x ≠ global y)
    (C : ObstructionCore.ObstructionClassifier Q) (q : Q)
    (packet : ObstructionCore.PrimitiveTerminalPacket.TerminalPacket C q)
    (hBoundary :
      packet.boundary =
        ObstructionCore.PrimitiveRepairBoundary.RepairBoundaryStatus.repaired)
    (hCertificate : packet.hasCertificate = false) :
    ((∀ i : I,
      ∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = chart i x) ∧
      (∃ F : P.ResidualQuotient → (I → γ),
        ∀ x : α, F (P.classOf x) = (fun i : I => chart i x)) ∧
      (∃ F : P.ResidualQuotient → (Ω → γ × γ),
        ∀ x : α,
          F (P.classOf x) =
            operatorAtlasOverlapPairs (α := α) left right chart x) ∧
      ¬ (∃ F :
        P.ResidualQuotient → ((I → γ) × (Ω → γ × γ)) × η,
        ∀ x : α,
          F (P.classOf x) =
            (((fun i : I => chart i x),
              operatorAtlasOverlapPairs (α := α) left right chart x),
              global x))) ∧
      ¬ ObstructionCore.PrimitiveTerminalPacket.PacketReady packet := by
  exact
    ⟨operatorAtlas_overlapGate_globalRed_nonpromotion
        P left right chart global hchart hxy hglobal,
      (ObstructionCore.PrimitiveTerminalPacket.packet_not_ready_iff_repaired_boundary_without_certificate
        C q packet).mpr ⟨hBoundary, hCertificate⟩⟩

theorem operatorAtlas_overlapGate_terminalBudget_nonpromotion
    (P : ObstructionCore.PrimitiveDifference α β)
    (left right : Ω → I) (chart : I → α → γ) (global : α → η)
    (hchart : ∀ i : I,
      P.InvariantCongruent (fun x : α => chart i x))
    {x y : α} (hxy : P.ZeroRel x y) (hglobal : global x ≠ global y)
    (C : ObstructionCore.ObstructionClassifier Q) (q : Q)
    (packet : ObstructionCore.PrimitiveTerminalPacket.TerminalPacket C q)
    (hTerminal : ObstructionCore.PrimitiveTerminalPacket.PacketTerminal packet)
    (hBoundary :
      packet.boundary =
        ObstructionCore.PrimitiveRepairBoundary.RepairBoundaryStatus.budgetUnknown) :
    ((∀ i : I,
      ∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = chart i x) ∧
      (∃ F : P.ResidualQuotient → (I → γ),
        ∀ x : α, F (P.classOf x) = (fun i : I => chart i x)) ∧
      (∃ F : P.ResidualQuotient → (Ω → γ × γ),
        ∀ x : α,
          F (P.classOf x) =
            operatorAtlasOverlapPairs (α := α) left right chart x) ∧
      ¬ (∃ F :
        P.ResidualQuotient → ((I → γ) × (Ω → γ × γ)) × η,
        ∀ x : α,
          F (P.classOf x) =
            (((fun i : I => chart i x),
              operatorAtlasOverlapPairs (α := α) left right chart x),
              global x))) ∧
      ¬ ObstructionCore.PrimitiveTerminalPacket.PacketRepaired packet := by
  exact
    ⟨operatorAtlas_overlapGate_globalRed_nonpromotion
        P left right chart global hchart hxy hglobal,
      ObstructionCore.PrimitiveTerminalPacket.packet_budgetUnknown_terminal_not_repaired
        C q packet hTerminal hBoundary⟩

theorem operatorAtlas_overlapGate_terminalRefused_nonpromotion
    (P : ObstructionCore.PrimitiveDifference α β)
    (left right : Ω → I) (chart : I → α → γ) (global : α → η)
    (hchart : ∀ i : I,
      P.InvariantCongruent (fun x : α => chart i x))
    {x y : α} (hxy : P.ZeroRel x y) (hglobal : global x ≠ global y)
    (C : ObstructionCore.ObstructionClassifier Q) (q : Q)
    (packet : ObstructionCore.PrimitiveTerminalPacket.TerminalPacket C q)
    (hTerminal : ObstructionCore.PrimitiveTerminalPacket.PacketTerminal packet)
    (hBoundary :
      packet.boundary =
        ObstructionCore.PrimitiveRepairBoundary.RepairBoundaryStatus.refused) :
    ((∀ i : I,
      ∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = chart i x) ∧
      (∃ F : P.ResidualQuotient → (I → γ),
        ∀ x : α, F (P.classOf x) = (fun i : I => chart i x)) ∧
      (∃ F : P.ResidualQuotient → (Ω → γ × γ),
        ∀ x : α,
          F (P.classOf x) =
            operatorAtlasOverlapPairs (α := α) left right chart x) ∧
      ¬ (∃ F :
        P.ResidualQuotient → ((I → γ) × (Ω → γ × γ)) × η,
        ∀ x : α,
          F (P.classOf x) =
            (((fun i : I => chart i x),
              operatorAtlasOverlapPairs (α := α) left right chart x),
              global x))) ∧
      ¬ ObstructionCore.PrimitiveTerminalPacket.PacketRepaired packet := by
  exact
    ⟨operatorAtlas_overlapGate_globalRed_nonpromotion
        P left right chart global hchart hxy hglobal,
      ObstructionCore.PrimitiveTerminalPacket.packet_refused_terminal_not_repaired
        C q packet hTerminal hBoundary⟩

theorem operatorAtlas_overlapGate_terminalNoRule_nonpromotion
    (P : ObstructionCore.PrimitiveDifference α β)
    (left right : Ω → I) (chart : I → α → γ) (global : α → η)
    (hchart : ∀ i : I,
      P.InvariantCongruent (fun x : α => chart i x))
    {x y : α} (hxy : P.ZeroRel x y) (hglobal : global x ≠ global y)
    (C : ObstructionCore.ObstructionClassifier Q) (q : Q)
    (packet : ObstructionCore.PrimitiveTerminalPacket.TerminalPacket C q)
    (hTerminal : ObstructionCore.PrimitiveTerminalPacket.PacketTerminal packet)
    (hBoundary :
      packet.boundary =
        ObstructionCore.PrimitiveRepairBoundary.RepairBoundaryStatus.noRule) :
    ((∀ i : I,
      ∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = chart i x) ∧
      (∃ F : P.ResidualQuotient → (I → γ),
        ∀ x : α, F (P.classOf x) = (fun i : I => chart i x)) ∧
      (∃ F : P.ResidualQuotient → (Ω → γ × γ),
        ∀ x : α,
          F (P.classOf x) =
            operatorAtlasOverlapPairs (α := α) left right chart x) ∧
      ¬ (∃ F :
        P.ResidualQuotient → ((I → γ) × (Ω → γ × γ)) × η,
        ∀ x : α,
          F (P.classOf x) =
            (((fun i : I => chart i x),
              operatorAtlasOverlapPairs (α := α) left right chart x),
              global x))) ∧
      ¬ ObstructionCore.PrimitiveTerminalPacket.PacketRepaired packet := by
  exact
    ⟨operatorAtlas_overlapGate_globalRed_nonpromotion
        P left right chart global hchart hxy hglobal,
      ObstructionCore.PrimitiveTerminalPacket.packet_noRule_terminal_not_repaired
        C q packet hTerminal hBoundary⟩

theorem operatorAtlas_overlapGate_liftSource_nonpromotion
    (P : ObstructionCore.PrimitiveDifference α β)
    (left right : Ω → I) (chart : I → α → γ) (global : α → η)
    (hchart : ∀ i : I,
      P.InvariantCongruent (fun x : α => chart i x))
    {x y : α} (hxy : P.ZeroRel x y) (hglobal : global x ≠ global y)
    (L : ObstructionCore.PrimitiveLiftCandidate.LiftCandidate)
    (hSourceBit : L.hasSourceObstruction = false)
    (evidence : ObstructionCore.PrimitiveLiftCertificate.LiftEvidence)
    (hNoSource : ¬ evidence.sourceObstruction) :
    ((∀ i : I,
      ∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = chart i x) ∧
      (∃ F : P.ResidualQuotient → (I → γ),
        ∀ x : α, F (P.classOf x) = (fun i : I => chart i x)) ∧
      (∃ F : P.ResidualQuotient → (Ω → γ × γ),
        ∀ x : α,
          F (P.classOf x) =
            operatorAtlasOverlapPairs (α := α) left right chart x) ∧
      ¬ (∃ F :
        P.ResidualQuotient → ((I → γ) × (Ω → γ × γ)) × η,
        ∀ x : α,
          F (P.classOf x) =
            (((fun i : I => chart i x),
              operatorAtlasOverlapPairs (α := α) left right chart x),
              global x))) ∧
      ¬ ObstructionCore.PrimitiveLiftCandidate.IsLicensedLiftCandidate L ∧
      ¬ ObstructionCore.PrimitiveLiftCertificate.HasLiftCertificate evidence := by
  have hNoCert :
      ¬ ObstructionCore.PrimitiveLiftCertificate.HasLiftCertificate evidence := by
    intro hCert
    cases hCert with
    | intro cert =>
        have hSource : evidence.sourceObstruction := by
          rw [← cert.property]
          exact cert.val.source_obstruction
        exact hNoSource hSource
  exact
    ⟨operatorAtlas_overlapGate_globalRed_nonpromotion
        P left right chart global hchart hxy hglobal,
      ObstructionCore.PrimitiveLiftCandidate.missing_source_obstruction_blocks_lift
        L hSourceBit,
      hNoCert⟩

theorem operatorAtlas_overlapGate_liftCarrier_nonpromotion
    (P : ObstructionCore.PrimitiveDifference α β)
    (left right : Ω → I) (chart : I → α → γ) (global : α → η)
    (hchart : ∀ i : I,
      P.InvariantCongruent (fun x : α => chart i x))
    {x y : α} (hxy : P.ZeroRel x y) (hglobal : global x ≠ global y)
    (L : ObstructionCore.PrimitiveLiftCandidate.LiftCandidate)
    (hCarrierBit : L.hasNewCarrier = false)
    (evidence : ObstructionCore.PrimitiveLiftCertificate.LiftEvidence)
    (hNoCarrier : ¬ evidence.newCarrierDeclared) :
    ((∀ i : I,
      ∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = chart i x) ∧
      (∃ F : P.ResidualQuotient → (I → γ),
        ∀ x : α, F (P.classOf x) = (fun i : I => chart i x)) ∧
      (∃ F : P.ResidualQuotient → (Ω → γ × γ),
        ∀ x : α,
          F (P.classOf x) =
            operatorAtlasOverlapPairs (α := α) left right chart x) ∧
      ¬ (∃ F :
        P.ResidualQuotient → ((I → γ) × (Ω → γ × γ)) × η,
        ∀ x : α,
          F (P.classOf x) =
            (((fun i : I => chart i x),
              operatorAtlasOverlapPairs (α := α) left right chart x),
              global x))) ∧
      ¬ ObstructionCore.PrimitiveLiftCandidate.IsLicensedLiftCandidate L ∧
      ¬ ObstructionCore.PrimitiveLiftCertificate.HasLiftCertificate evidence := by
  have hNoCert :
      ¬ ObstructionCore.PrimitiveLiftCertificate.HasLiftCertificate evidence := by
    intro hCert
    cases hCert with
    | intro cert =>
        have hCarrier : evidence.newCarrierDeclared := by
          rw [← cert.property]
          exact cert.val.new_carrier
        exact hNoCarrier hCarrier
  exact
    ⟨operatorAtlas_overlapGate_globalRed_nonpromotion
        P left right chart global hchart hxy hglobal,
      ObstructionCore.PrimitiveLiftCandidate.missing_new_carrier_blocks_lift
        L hCarrierBit,
      hNoCert⟩

theorem operatorAtlas_overlapGate_liftReplay_nonpromotion
    (P : ObstructionCore.PrimitiveDifference α β)
    (left right : Ω → I) (chart : I → α → γ) (global : α → η)
    (hchart : ∀ i : I,
      P.InvariantCongruent (fun x : α => chart i x))
    {x y : α} (hxy : P.ZeroRel x y) (hglobal : global x ≠ global y)
    (L : ObstructionCore.PrimitiveLiftCandidate.LiftCandidate)
    (hReplayBit : L.hasReplay = false)
    (evidence : ObstructionCore.PrimitiveLiftCertificate.LiftEvidence)
    (hNoReplay : ¬ evidence.replayAvailable) :
    ((∀ i : I,
      ∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = chart i x) ∧
      (∃ F : P.ResidualQuotient → (I → γ),
        ∀ x : α, F (P.classOf x) = (fun i : I => chart i x)) ∧
      (∃ F : P.ResidualQuotient → (Ω → γ × γ),
        ∀ x : α,
          F (P.classOf x) =
            operatorAtlasOverlapPairs (α := α) left right chart x) ∧
      ¬ (∃ F :
        P.ResidualQuotient → ((I → γ) × (Ω → γ × γ)) × η,
        ∀ x : α,
          F (P.classOf x) =
            (((fun i : I => chart i x),
              operatorAtlasOverlapPairs (α := α) left right chart x),
              global x))) ∧
      ¬ ObstructionCore.PrimitiveLiftCandidate.IsLicensedLiftCandidate L ∧
      ¬ ObstructionCore.PrimitiveLiftCertificate.HasLiftCertificate evidence := by
  exact
    ⟨operatorAtlas_overlapGate_globalRed_nonpromotion
        P left right chart global hchart hxy hglobal,
      ObstructionCore.PrimitiveLiftCandidate.missing_replay_blocks_lift
        L hReplayBit,
      ObstructionCore.PrimitiveLiftCertificate.no_lift_certificate_without_replay
        evidence hNoReplay⟩

theorem operatorAtlas_overlapGate_liftReduction_nonpromotion
    (P : ObstructionCore.PrimitiveDifference α β)
    (left right : Ω → I) (chart : I → α → γ) (global : α → η)
    (hchart : ∀ i : I,
      P.InvariantCongruent (fun x : α => chart i x))
    {x y : α} (hxy : P.ZeroRel x y) (hglobal : global x ≠ global y)
    (L : ObstructionCore.PrimitiveLiftCandidate.LiftCandidate)
    (hReductionBit : L.reducesPhi = false)
    (evidence : ObstructionCore.PrimitiveLiftCertificate.LiftEvidence)
    (hNoReduction : ¬ evidence.residualReduced) :
    ((∀ i : I,
      ∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = chart i x) ∧
      (∃ F : P.ResidualQuotient → (I → γ),
        ∀ x : α, F (P.classOf x) = (fun i : I => chart i x)) ∧
      (∃ F : P.ResidualQuotient → (Ω → γ × γ),
        ∀ x : α,
          F (P.classOf x) =
            operatorAtlasOverlapPairs (α := α) left right chart x) ∧
      ¬ (∃ F :
        P.ResidualQuotient → ((I → γ) × (Ω → γ × γ)) × η,
        ∀ x : α,
          F (P.classOf x) =
            (((fun i : I => chart i x),
              operatorAtlasOverlapPairs (α := α) left right chart x),
              global x))) ∧
      ¬ ObstructionCore.PrimitiveLiftCandidate.IsLicensedLiftCandidate L ∧
      ¬ ObstructionCore.PrimitiveLiftCertificate.HasLiftCertificate evidence := by
  exact
    ⟨operatorAtlas_overlapGate_globalRed_nonpromotion
        P left right chart global hchart hxy hglobal,
      ObstructionCore.PrimitiveLiftCandidate.missing_reduction_blocks_lift
        L hReductionBit,
      ObstructionCore.PrimitiveLiftCertificate.no_lift_certificate_without_reduction
        evidence hNoReduction⟩

theorem operatorAtlas_overlapGate_liftClosure_nonpromotion
    (P : ObstructionCore.PrimitiveDifference α β)
    (left right : Ω → I) (chart : I → α → γ) (global : α → η)
    (hchart : ∀ i : I,
      P.InvariantCongruent (fun x : α => chart i x))
    {x y : α} (hxy : P.ZeroRel x y) (hglobal : global x ≠ global y)
    (L : ObstructionCore.PrimitiveLiftCandidate.LiftCandidate)
    (hClosureBit : L.preservesClosure = false)
    (evidence : ObstructionCore.PrimitiveLiftCertificate.LiftEvidence)
    (hNoClosure : ¬ evidence.closurePreserved) :
    ((∀ i : I,
      ∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = chart i x) ∧
      (∃ F : P.ResidualQuotient → (I → γ),
        ∀ x : α, F (P.classOf x) = (fun i : I => chart i x)) ∧
      (∃ F : P.ResidualQuotient → (Ω → γ × γ),
        ∀ x : α,
          F (P.classOf x) =
            operatorAtlasOverlapPairs (α := α) left right chart x) ∧
      ¬ (∃ F :
        P.ResidualQuotient → ((I → γ) × (Ω → γ × γ)) × η,
        ∀ x : α,
          F (P.classOf x) =
            (((fun i : I => chart i x),
              operatorAtlasOverlapPairs (α := α) left right chart x),
              global x))) ∧
      ¬ ObstructionCore.PrimitiveLiftCandidate.IsLicensedLiftCandidate L ∧
      ¬ ObstructionCore.PrimitiveLiftCertificate.HasLiftCertificate evidence := by
  exact
    ⟨operatorAtlas_overlapGate_globalRed_nonpromotion
        P left right chart global hchart hxy hglobal,
      ObstructionCore.PrimitiveLiftCandidate.missing_closure_preservation_blocks_lift
        L hClosureBit,
      ObstructionCore.PrimitiveLiftCertificate.no_lift_certificate_without_closure
        evidence hNoClosure⟩

theorem operatorAtlas_overlapGate_repairBoundaryWitness_nonpromotion
    (P : ObstructionCore.PrimitiveDifference α β)
    (left right : Ω → I) (chart : I → α → γ) (global : α → η)
    (hchart : ∀ i : I,
      P.InvariantCongruent (fun x : α => chart i x))
    {x y : α} (hxy : P.ZeroRel x y) (hglobal : global x ≠ global y)
    (input : ObstructionCore.PrimitiveRepairBoundary.RepairBoundaryInput)
    (hPolicy : input.policyAllowed = true)
    (hRule : input.hasRule = true)
    (hBudget : input.withinBudget = true)
    (hWitness : input.hasAdmissibleWitness = false) :
    ((∀ i : I,
      ∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = chart i x) ∧
      (∃ F : P.ResidualQuotient → (I → γ),
        ∀ x : α, F (P.classOf x) = (fun i : I => chart i x)) ∧
      (∃ F : P.ResidualQuotient → (Ω → γ × γ),
        ∀ x : α,
          F (P.classOf x) =
            operatorAtlasOverlapPairs (α := α) left right chart x) ∧
      ¬ (∃ F :
        P.ResidualQuotient → ((I → γ) × (Ω → γ × γ)) × η,
        ∀ x : α,
          F (P.classOf x) =
            (((fun i : I => chart i x),
              operatorAtlasOverlapPairs (α := α) left right chart x),
              global x))) ∧
      ObstructionCore.PrimitiveRepairBoundary.repairBoundaryDecision input =
        ObstructionCore.PrimitiveRepairBoundary.RepairBoundaryStatus.noRule ∧
      ObstructionCore.PrimitiveRepairBoundary.repairBoundaryDecision input ≠
        ObstructionCore.PrimitiveRepairBoundary.RepairBoundaryStatus.repaired := by
  have hNoRule :
      ObstructionCore.PrimitiveRepairBoundary.repairBoundaryDecision input =
        ObstructionCore.PrimitiveRepairBoundary.RepairBoundaryStatus.noRule :=
    (ObstructionCore.PrimitiveRepairBoundary.repairBoundary_noRule_iff input).mpr
      (Or.inr ⟨hPolicy, hRule, hBudget, hWitness⟩)
  have hNotRepaired :
      ObstructionCore.PrimitiveRepairBoundary.repairBoundaryDecision input ≠
        ObstructionCore.PrimitiveRepairBoundary.RepairBoundaryStatus.repaired := by
    rw [hNoRule]
    exact ObstructionCore.PrimitiveRepairBoundary.noRule_not_repaired
  exact
    ⟨operatorAtlas_overlapGate_globalRed_nonpromotion
        P left right chart global hchart hxy hglobal,
      hNoRule,
      hNotRepaired⟩

theorem operatorAtlas_overlapGate_repairBoundaryPolicy_nonpromotion
    (P : ObstructionCore.PrimitiveDifference α β)
    (left right : Ω → I) (chart : I → α → γ) (global : α → η)
    (hchart : ∀ i : I,
      P.InvariantCongruent (fun x : α => chart i x))
    {x y : α} (hxy : P.ZeroRel x y) (hglobal : global x ≠ global y)
    (input : ObstructionCore.PrimitiveRepairBoundary.RepairBoundaryInput)
    (hPolicy : input.policyAllowed = false) :
    ((∀ i : I,
      ∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = chart i x) ∧
      (∃ F : P.ResidualQuotient → (I → γ),
        ∀ x : α, F (P.classOf x) = (fun i : I => chart i x)) ∧
      (∃ F : P.ResidualQuotient → (Ω → γ × γ),
        ∀ x : α,
          F (P.classOf x) =
            operatorAtlasOverlapPairs (α := α) left right chart x) ∧
      ¬ (∃ F :
        P.ResidualQuotient → ((I → γ) × (Ω → γ × γ)) × η,
        ∀ x : α,
          F (P.classOf x) =
            (((fun i : I => chart i x),
              operatorAtlasOverlapPairs (α := α) left right chart x),
              global x))) ∧
      ObstructionCore.PrimitiveRepairBoundary.repairBoundaryDecision input =
        ObstructionCore.PrimitiveRepairBoundary.RepairBoundaryStatus.refused ∧
      ObstructionCore.PrimitiveRepairBoundary.repairBoundaryDecision input ≠
        ObstructionCore.PrimitiveRepairBoundary.RepairBoundaryStatus.repaired := by
  have hRefused :
      ObstructionCore.PrimitiveRepairBoundary.repairBoundaryDecision input =
        ObstructionCore.PrimitiveRepairBoundary.RepairBoundaryStatus.refused :=
    ObstructionCore.PrimitiveRepairBoundary.policy_failure_routes_refused
      input hPolicy
  have hNotRepaired :
      ObstructionCore.PrimitiveRepairBoundary.repairBoundaryDecision input ≠
        ObstructionCore.PrimitiveRepairBoundary.RepairBoundaryStatus.repaired := by
    rw [hRefused]
    exact ObstructionCore.PrimitiveRepairBoundary.refused_not_repaired
  exact
    ⟨operatorAtlas_overlapGate_globalRed_nonpromotion
        P left right chart global hchart hxy hglobal,
      hRefused,
      hNotRepaired⟩

theorem operatorAtlas_overlapGate_repairBoundaryRule_nonpromotion
    (P : ObstructionCore.PrimitiveDifference α β)
    (left right : Ω → I) (chart : I → α → γ) (global : α → η)
    (hchart : ∀ i : I,
      P.InvariantCongruent (fun x : α => chart i x))
    {x y : α} (hxy : P.ZeroRel x y) (hglobal : global x ≠ global y)
    (input : ObstructionCore.PrimitiveRepairBoundary.RepairBoundaryInput)
    (hPolicy : input.policyAllowed = true)
    (hRule : input.hasRule = false) :
    ((∀ i : I,
      ∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = chart i x) ∧
      (∃ F : P.ResidualQuotient → (I → γ),
        ∀ x : α, F (P.classOf x) = (fun i : I => chart i x)) ∧
      (∃ F : P.ResidualQuotient → (Ω → γ × γ),
        ∀ x : α,
          F (P.classOf x) =
            operatorAtlasOverlapPairs (α := α) left right chart x) ∧
      ¬ (∃ F :
        P.ResidualQuotient → ((I → γ) × (Ω → γ × γ)) × η,
        ∀ x : α,
          F (P.classOf x) =
            (((fun i : I => chart i x),
              operatorAtlasOverlapPairs (α := α) left right chart x),
              global x))) ∧
      ObstructionCore.PrimitiveRepairBoundary.repairBoundaryDecision input =
        ObstructionCore.PrimitiveRepairBoundary.RepairBoundaryStatus.noRule ∧
      ObstructionCore.PrimitiveRepairBoundary.repairBoundaryDecision input ≠
        ObstructionCore.PrimitiveRepairBoundary.RepairBoundaryStatus.repaired := by
  have hNoRule :
      ObstructionCore.PrimitiveRepairBoundary.repairBoundaryDecision input =
        ObstructionCore.PrimitiveRepairBoundary.RepairBoundaryStatus.noRule :=
    ObstructionCore.PrimitiveRepairBoundary.missing_rule_routes_noRule
      input hPolicy hRule
  have hNotRepaired :
      ObstructionCore.PrimitiveRepairBoundary.repairBoundaryDecision input ≠
        ObstructionCore.PrimitiveRepairBoundary.RepairBoundaryStatus.repaired := by
    rw [hNoRule]
    exact ObstructionCore.PrimitiveRepairBoundary.noRule_not_repaired
  exact
    ⟨operatorAtlas_overlapGate_globalRed_nonpromotion
        P left right chart global hchart hxy hglobal,
      hNoRule,
      hNotRepaired⟩

theorem operatorAtlas_overlapGate_repairBoundaryBudget_nonpromotion
    (P : ObstructionCore.PrimitiveDifference α β)
    (left right : Ω → I) (chart : I → α → γ) (global : α → η)
    (hchart : ∀ i : I,
      P.InvariantCongruent (fun x : α => chart i x))
    {x y : α} (hxy : P.ZeroRel x y) (hglobal : global x ≠ global y)
    (input : ObstructionCore.PrimitiveRepairBoundary.RepairBoundaryInput)
    (hPolicy : input.policyAllowed = true)
    (hRule : input.hasRule = true)
    (hBudget : input.withinBudget = false) :
    ((∀ i : I,
      ∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = chart i x) ∧
      (∃ F : P.ResidualQuotient → (I → γ),
        ∀ x : α, F (P.classOf x) = (fun i : I => chart i x)) ∧
      (∃ F : P.ResidualQuotient → (Ω → γ × γ),
        ∀ x : α,
          F (P.classOf x) =
            operatorAtlasOverlapPairs (α := α) left right chart x) ∧
      ¬ (∃ F :
        P.ResidualQuotient → ((I → γ) × (Ω → γ × γ)) × η,
        ∀ x : α,
          F (P.classOf x) =
            (((fun i : I => chart i x),
              operatorAtlasOverlapPairs (α := α) left right chart x),
              global x))) ∧
      ObstructionCore.PrimitiveRepairBoundary.repairBoundaryDecision input =
        ObstructionCore.PrimitiveRepairBoundary.RepairBoundaryStatus.budgetUnknown ∧
      ObstructionCore.PrimitiveRepairBoundary.repairBoundaryDecision input ≠
        ObstructionCore.PrimitiveRepairBoundary.RepairBoundaryStatus.repaired := by
  have hBudgetUnknown :
      ObstructionCore.PrimitiveRepairBoundary.repairBoundaryDecision input =
        ObstructionCore.PrimitiveRepairBoundary.RepairBoundaryStatus.budgetUnknown :=
    ObstructionCore.PrimitiveRepairBoundary.budget_failure_routes_budgetUnknown
      input hPolicy hRule hBudget
  have hNotRepaired :
      ObstructionCore.PrimitiveRepairBoundary.repairBoundaryDecision input ≠
        ObstructionCore.PrimitiveRepairBoundary.RepairBoundaryStatus.repaired := by
    rw [hBudgetUnknown]
    exact ObstructionCore.PrimitiveRepairBoundary.budgetUnknown_not_repaired
  exact
    ⟨operatorAtlas_overlapGate_globalRed_nonpromotion
        P left right chart global hchart hxy hglobal,
      hBudgetUnknown,
      hNotRepaired⟩

theorem operatorAtlas_overlapGate_repairCertificate_nonpromotion
    (P : ObstructionCore.PrimitiveDifference α β)
    (left right : Ω → I) (chart : I → α → γ) (global : α → η)
    (hchart : ∀ i : I,
      P.InvariantCongruent (fun x : α => chart i x))
    {x y : α} (hxy : P.ZeroRel x y) (hglobal : global x ≠ global y)
    (C : ObstructionCore.ObstructionClassifier Q) (zeroClass q : Q)
    (hExact : ObstructionCore.PrimitiveRepairCertificate.ExactStatusOnly C q) :
    ((∀ i : I,
      ∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = chart i x) ∧
      (∃ F : P.ResidualQuotient → (I → γ),
        ∀ x : α, F (P.classOf x) = (fun i : I => chart i x)) ∧
      (∃ F : P.ResidualQuotient → (Ω → γ × γ),
        ∀ x : α,
          F (P.classOf x) =
            operatorAtlasOverlapPairs (α := α) left right chart x) ∧
      ¬ (∃ F :
        P.ResidualQuotient → ((I → γ) × (Ω → γ × γ)) × η,
        ∀ x : α,
          F (P.classOf x) =
            (((fun i : I => chart i x),
              operatorAtlasOverlapPairs (α := α) left right chart x),
              global x))) ∧
      ∃ S : ObstructionCore.PrimitiveAdmissibleRepair.AdmissibleRepairSystem Q,
        ObstructionCore.PrimitiveRepairCertificate.ExactStatusOnly C q ∧
          ¬ ObstructionCore.PrimitiveRepairCertificate.HasRepairCertificate
            C S zeroClass q := by
  exact
    ⟨operatorAtlas_overlapGate_globalRed_nonpromotion
        P left right chart global hchart hxy hglobal,
      ObstructionCore.PrimitiveRepairCertificate.exact_status_alone_is_not_repairCertificate
        C zeroClass q hExact⟩

theorem operatorAtlas_overlapGate_admissibleRepairWitness_nonpromotion
    (P : ObstructionCore.PrimitiveDifference α β)
    (left right : Ω → I) (chart : I → α → γ) (global : α → η)
    (hchart : ∀ i : I,
      P.InvariantCongruent (fun x : α => chart i x))
    {x y : α} (hxy : P.ZeroRel x y) (hglobal : global x ≠ global y)
    (C : ObstructionCore.ObstructionClassifier Q)
    (S : ObstructionCore.PrimitiveAdmissibleRepair.AdmissibleRepairSystem Q)
    (zeroClass q : Q)
    (hExact : C.IsExactRepair q)
    (hNoWitness :
      ¬ Nonempty
        (ObstructionCore.PrimitiveAdmissibleRepair.AdmissibleRepairWitness
          S zeroClass q)) :
    ((∀ i : I,
      ∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = chart i x) ∧
      (∃ F : P.ResidualQuotient → (I → γ),
        ∀ x : α, F (P.classOf x) = (fun i : I => chart i x)) ∧
      (∃ F : P.ResidualQuotient → (Ω → γ × γ),
        ∀ x : α,
          F (P.classOf x) =
            operatorAtlasOverlapPairs (α := α) left right chart x) ∧
      ¬ (∃ F :
        P.ResidualQuotient → ((I → γ) × (Ω → γ × γ)) × η,
        ∀ x : α,
          F (P.classOf x) =
            (((fun i : I => chart i x),
              operatorAtlasOverlapPairs (α := α) left right chart x),
              global x))) ∧
      C.IsExactRepair q ∧
      ¬ ObstructionCore.PrimitiveAdmissibleRepair.AdmissibleWitnessedExactRepair
        C S zeroClass q := by
  exact
    ⟨operatorAtlas_overlapGate_globalRed_nonpromotion
        P left right chart global hchart hxy hglobal,
      hExact,
      fun hWitnessed => hNoWitness hWitnessed.2⟩

theorem operatorAtlas_overlapGate_noTrivialRepairCollapse_nonpromotion
    (P : ObstructionCore.PrimitiveDifference α β)
    (left right : Ω → I) (chart : I → α → γ) (global : α → η)
    (hchart : ∀ i : I,
      P.InvariantCongruent (fun x : α => chart i x))
    {x y : α} (hxy : P.ZeroRel x y) (hglobal : global x ≠ global y)
    (S : ObstructionCore.PrimitiveAdmissibleRepair.AdmissibleRepairSystem Q)
    (zeroClass q : Q)
    (hNoCollapse :
      ObstructionCore.PrimitiveAdmissibleRepair.NoTrivialRepairCollapse
        S zeroClass) :
    ((∀ i : I,
      ∃ F : P.ResidualQuotient → γ,
        ∀ x : α, F (P.classOf x) = chart i x) ∧
      (∃ F : P.ResidualQuotient → (I → γ),
        ∀ x : α, F (P.classOf x) = (fun i : I => chart i x)) ∧
      (∃ F : P.ResidualQuotient → (Ω → γ × γ),
        ∀ x : α,
          F (P.classOf x) =
            operatorAtlasOverlapPairs (α := α) left right chart x) ∧
      ¬ (∃ F :
        P.ResidualQuotient → ((I → γ) × (Ω → γ × γ)) × η,
        ∀ x : α,
          F (P.classOf x) =
            (((fun i : I => chart i x),
              operatorAtlasOverlapPairs (α := α) left right chart x),
              global x))) ∧
      ¬ (∃ w :
        ObstructionCore.PrimitiveAdmissibleRepair.AdmissibleRepairWitness
          S zeroClass q,
        w.repair =
          ObstructionCore.PrimitiveAdmissibleRepair.constantZeroRepair
            zeroClass) := by
  exact
    ⟨operatorAtlas_overlapGate_globalRed_nonpromotion
        P left right chart global hchart hxy hglobal,
      ObstructionCore.PrimitiveAdmissibleRepair.noTrivialRepairCollapse_blocks_constant_zero_witness
        S zeroClass q hNoCollapse⟩

theorem operatorAtlas_overlapGate_repairWitness_nonpromotion
    (P : ObstructionCore.PointedPrimitiveDifference α β)
    (left right : Ω → I) (chart : I → α → γ) (global : α → η)
    (hchart : ∀ i : I,
      ObstructionCore.PrimitiveDifference.InvariantCongruent
        P.toPrimitiveDifference (fun x : α => chart i x))
    {x y : α} (hxy : P.toPrimitiveDifference.ZeroRel x y)
    (hglobal : global x ≠ global y)
    (C : ObstructionCore.ObstructionClassifier (ObstructionCore.PointedResidualQuotient P))
    (r : ObstructionCore.PrimitiveRepairWitness.RepairMap P)
    (q : ObstructionCore.PointedResidualQuotient P)
    (hExact : C.IsExactRepair q)
    (hNoWitness :
      ¬ ObstructionCore.PrimitiveRepairWitness.ExactRepairHasWitness P C r q) :
    ((∀ i : I,
      ∃ F : ObstructionCore.PointedResidualQuotient P → γ,
        ∀ x : α,
          F (ObstructionCore.PrimitiveDifference.classOf
            P.toPrimitiveDifference x) = chart i x) ∧
      (∃ F : ObstructionCore.PointedResidualQuotient P → (I → γ),
        ∀ x : α,
          F (ObstructionCore.PrimitiveDifference.classOf
            P.toPrimitiveDifference x) = (fun i : I => chart i x)) ∧
      (∃ F : ObstructionCore.PointedResidualQuotient P → (Ω → γ × γ),
        ∀ x : α,
          F (ObstructionCore.PrimitiveDifference.classOf
            P.toPrimitiveDifference x) =
            operatorAtlasOverlapPairs (α := α) left right chart x) ∧
      ¬ (∃ F :
        ObstructionCore.PointedResidualQuotient P → ((I → γ) × (Ω → γ × γ)) × η,
        ∀ x : α,
          F (ObstructionCore.PrimitiveDifference.classOf
            P.toPrimitiveDifference x) =
            (((fun i : I => chart i x),
              operatorAtlasOverlapPairs (α := α) left right chart x),
              global x))) ∧
      ObstructionCore.PrimitiveRepairWitness.ExactRepairStatusOnly P C q ∧
      ¬ ObstructionCore.PrimitiveRepairWitness.WitnessedExactRepair P C r q := by
  exact
    ⟨operatorAtlas_overlapGate_globalRed_nonpromotion
        P.toPrimitiveDifference left right chart global hchart hxy hglobal,
      ObstructionCore.PrimitiveRepairWitness.exactRepair_status_without_witness_is_only_classifier
        P C q hExact,
      fun hWitnessed => hNoWitness hWitnessed.2⟩

theorem operatorAtlas_rawPhiClassifier_nonpromotion
    (P : ObstructionCore.PointedPrimitiveDifference α β)
    (left right : Ω → I) (chart : I → α → γ)
    (phiRaw : α → Nat)
    (hchart : ∀ i : I,
      ObstructionCore.PrimitiveDifference.InvariantCongruent
        P.toPrimitiveDifference (fun x : α => chart i x))
    (hPhiNot :
      ¬ ObstructionCore.PrimitiveDifference.InvariantCongruent
        P.toPrimitiveDifference phiRaw) :
    (∀ i : I,
      ∃ F : ObstructionCore.PointedResidualQuotient P → γ,
        ∀ x : α,
          F (ObstructionCore.PrimitiveDifference.classOf
            P.toPrimitiveDifference x) = chart i x) ∧
      (∃ F : ObstructionCore.PointedResidualQuotient P → (I → γ),
        ∀ x : α,
          F (ObstructionCore.PrimitiveDifference.classOf
            P.toPrimitiveDifference x) = (fun i : I => chart i x)) ∧
      (∃ F : ObstructionCore.PointedResidualQuotient P → (Ω → γ × γ),
        ∀ x : α,
          F (ObstructionCore.PrimitiveDifference.classOf
            P.toPrimitiveDifference x) =
            operatorAtlasOverlapPairs (α := α) left right chart x) ∧
      ¬ (∃ C :
        ObstructionCore.ObstructionClassifier (ObstructionCore.PointedResidualQuotient P),
        ∀ x : α,
          C.Phi (ObstructionCore.PrimitiveDifference.classOf
            P.toPrimitiveDifference x) = phiRaw x) := by
  have hatlas :
      ObstructionCore.PrimitiveDifference.InvariantCongruent
        P.toPrimitiveDifference (fun x : α => fun i : I => chart i x) :=
    operatorAtlas_invariant_of_each_chart P.toPrimitiveDifference chart hchart
  have hoverlap :
      ObstructionCore.PrimitiveDifference.InvariantCongruent
        P.toPrimitiveDifference
        (operatorAtlasOverlapPairs (α := α) left right chart) :=
    operatorAtlas_overlapPairs_invariant_of_each_chart
      P.toPrimitiveDifference left right chart hchart
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro i
    exact
      (ObstructionCore.PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
        P.toPrimitiveDifference (fun x : α => chart i x)).mpr (hchart i)
  · exact
      (ObstructionCore.PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
        P.toPrimitiveDifference
        (fun x : α => fun i : I => chart i x)).mpr hatlas
  · exact
      (ObstructionCore.PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
        P.toPrimitiveDifference
        (operatorAtlasOverlapPairs (α := α) left right chart)).mpr hoverlap
  · exact
      ObstructionCore.PrimitiveSpineSummary.spine_raw_phi_noncongruent_blocks_classifier
        P phiRaw hPhiNot

theorem operatorAtlas_rawGammaClassifier_nonpromotion
    (P : ObstructionCore.PointedPrimitiveDifference α β)
    (left right : Ω → I) (chart : I → α → γ)
    (gammaRaw : α → Nat)
    (hchart : ∀ i : I,
      ObstructionCore.PrimitiveDifference.InvariantCongruent
        P.toPrimitiveDifference (fun x : α => chart i x))
    (hGammaNot :
      ¬ ObstructionCore.PrimitiveDifference.InvariantCongruent
        P.toPrimitiveDifference gammaRaw) :
    (∀ i : I,
      ∃ F : ObstructionCore.PointedResidualQuotient P → γ,
        ∀ x : α,
          F (ObstructionCore.PrimitiveDifference.classOf
            P.toPrimitiveDifference x) = chart i x) ∧
      (∃ F : ObstructionCore.PointedResidualQuotient P → (I → γ),
        ∀ x : α,
          F (ObstructionCore.PrimitiveDifference.classOf
            P.toPrimitiveDifference x) = (fun i : I => chart i x)) ∧
      (∃ F : ObstructionCore.PointedResidualQuotient P → (Ω → γ × γ),
        ∀ x : α,
          F (ObstructionCore.PrimitiveDifference.classOf
            P.toPrimitiveDifference x) =
            operatorAtlasOverlapPairs (α := α) left right chart x) ∧
      ¬ (∃ C :
        ObstructionCore.ObstructionClassifier (ObstructionCore.PointedResidualQuotient P),
        ∀ x : α,
          C.Gamma (ObstructionCore.PrimitiveDifference.classOf
            P.toPrimitiveDifference x) = gammaRaw x) := by
  have hatlas :
      ObstructionCore.PrimitiveDifference.InvariantCongruent
        P.toPrimitiveDifference (fun x : α => fun i : I => chart i x) :=
    operatorAtlas_invariant_of_each_chart P.toPrimitiveDifference chart hchart
  have hoverlap :
      ObstructionCore.PrimitiveDifference.InvariantCongruent
        P.toPrimitiveDifference
        (operatorAtlasOverlapPairs (α := α) left right chart) :=
    operatorAtlas_overlapPairs_invariant_of_each_chart
      P.toPrimitiveDifference left right chart hchart
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro i
    exact
      (ObstructionCore.PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
        P.toPrimitiveDifference (fun x : α => chart i x)).mpr (hchart i)
  · exact
      (ObstructionCore.PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
        P.toPrimitiveDifference
        (fun x : α => fun i : I => chart i x)).mpr hatlas
  · exact
      (ObstructionCore.PrimitiveDifference.invariantFactor_exists_iff_invariantCongruent
        P.toPrimitiveDifference
        (operatorAtlasOverlapPairs (α := α) left right chart)).mpr hoverlap
  · exact
      fun hClassifier => by
        rcases hClassifier with ⟨C, hGamma⟩
        exact
          ObstructionCore.PrimitiveObstructionPipeline.no_gammaQuot_if_not_congruent
            P gammaRaw hGammaNot ⟨C.Gamma, hGamma⟩

end

end PaperQF002
