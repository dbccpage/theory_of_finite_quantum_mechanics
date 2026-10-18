import Mathlib.Tactic

/-!
# QMLiftClassificationAxioms — W5.6 (named axiom set + registry classification)

Programme target: DERIV-MASTER W5.6 (path §C.18 / QMREG-54).

**This fire freezes a named axiom set** `AX-LIFT-V0` and classifies the
**declared finite registry** of lifts {complex, real, quaternionic} against it.

It does **not** re-prove the Koecher–Vinberg / Jordan classification of
formally real Jordan algebras; that remains literature capital / OPEN residual
for a full theorem import. It does **not** claim absolute completeness over
all mathematically possible lifts (W5.11 registry fence).

Discrete checkable axioms in `AX-LIFT-V0`:

* `A_finite` — finite positive dimension
* `A_l1_shadow` — lift admits a classical two-sector equal-mass shadow (shared)
* `A_local_tomography` — local density-param product equals composite params at 2⊗2

Among the three registered lifts, only `complexHilbert` satisfies all three.

**This residual also shows:** on the registry, `A_local_tomography` is the
**sole V0 discriminator** (finite + ℓ¹ shadow alone admit all three lifts);
blocking-axiom certificates for rebit/quat; optional `AX-LIFT-V0.1` additives
named without rewriting V0; **partial activation** of `A_purification_capacity`
(TOY-MECH under complex/real tensor purification witness); continuous connectedness
**REFUSED on FinL1** (continuum-host pathway OPEN/import); multipartite LT3
consistency with V0 (W5.5 capital bind — not forced into V0).

AuthorityEffect: None.
-/

namespace QM
namespace LiftClassification

/-! ## Registry of lifts (finite declared menu) -/

inductive NamedLift where
  | complexHilbert
  | realHilbert
  | quaternionicHilbert
deriving DecidableEq, Repr

/-- Free real density parameters (same discrete model as W5.5). -/
def densityParams : NamedLift → Nat → Nat
  | .complexHilbert, d => d * d
  | .realHilbert, d => d * (d + 1) / 2
  | .quaternionicHilbert, d => d * (2 * d - 1)

def localProd (L : NamedLift) (dA dB : Nat) : Nat :=
  densityParams L dA * densityParams L dB

def compositeParams (L : NamedLift) (dA dB : Nat) : Nat :=
  densityParams L (dA * dB)

/-- Finite declared registry as an explicit list (enumeration surface). -/
def registry : List NamedLift :=
  [.complexHilbert, .realHilbert, .quaternionicHilbert]

theorem registry_card : registry.length = 3 := by
  decide

/-! ## Named axiom set AX-LIFT-V0 (frozen labels) -/

inductive AxiomId where
  | A_finite
  | A_l1_shadow
  | A_local_tomography
deriving DecidableEq, Repr

/-- The frozen named set (order irrelevant). -/
def axLiftV0 : List AxiomId :=
  [.A_finite, .A_l1_shadow, .A_local_tomography]

theorem axLiftV0_card : axLiftV0.length = 3 := by
  decide

theorem axLiftV0_has_lt : AxiomId.A_local_tomography ∈ axLiftV0 := by
  simp [axLiftV0]

/-! ## Satisfaction predicates (discrete) -/

/-- A1: dimension is finite and positive (registry models use d=2). -/
def satisfiesFinite (_L : NamedLift) (d : Nat) : Prop := 0 < d

/-- A2: shared classical ℓ¹ shadow toy — always true for registered lifts. -/
def satisfiesL1Shadow (_L : NamedLift) : Prop := True

/-- A3: local tomography at qubit pair 2⊗2. -/
def satisfiesLocalTomography (L : NamedLift) : Prop :=
  localProd L 2 2 = compositeParams L 2 2

def satisfiesAxLiftV0 (L : NamedLift) : Prop :=
  satisfiesFinite L 2 ∧ satisfiesL1Shadow L ∧ satisfiesLocalTomography L

/-- V0 without local tomography: finite + ℓ¹ shadow only. -/
def satisfiesAxLiftV0_minus_LT (L : NamedLift) : Prop :=
  satisfiesFinite L 2 ∧ satisfiesL1Shadow L

/-! ## Classification of the registry -/

theorem complex_satisfies_finite : satisfiesFinite .complexHilbert 2 := by
  unfold satisfiesFinite
  decide

theorem complex_satisfies_lt : satisfiesLocalTomography .complexHilbert := by
  unfold satisfiesLocalTomography localProd compositeParams densityParams
  rfl

theorem complex_satisfies_v0 : satisfiesAxLiftV0 .complexHilbert :=
  ⟨complex_satisfies_finite, trivial, complex_satisfies_lt⟩

theorem real_fails_lt : ¬ satisfiesLocalTomography .realHilbert := by
  unfold satisfiesLocalTomography localProd compositeParams densityParams
  decide

theorem real_fails_v0 : ¬ satisfiesAxLiftV0 .realHilbert := by
  intro h
  exact real_fails_lt h.2.2

theorem quat_fails_lt : ¬ satisfiesLocalTomography .quaternionicHilbert := by
  unfold satisfiesLocalTomography localProd compositeParams densityParams
  decide

theorem quat_fails_v0 : ¬ satisfiesAxLiftV0 .quaternionicHilbert := by
  intro h
  exact quat_fails_lt h.2.2

/-- Registry classification: among the three declared lifts, exactly complex
    satisfies AX-LIFT-V0 (stated as: complex yes; real no; quat no). -/
theorem registry_classification_v0 :
    satisfiesAxLiftV0 .complexHilbert ∧
    ¬ satisfiesAxLiftV0 .realHilbert ∧
    ¬ satisfiesAxLiftV0 .quaternionicHilbert :=
  ⟨complex_satisfies_v0, real_fails_v0, quat_fails_v0⟩

/-! ## Residual: LT is the sole V0 discriminator on the registry

Without `A_local_tomography`, every registered lift passes finite + ℓ¹ shadow.
With V0 complete, only complex remains. Blocking axiom for rebit/quat is LT.
-/

theorem real_satisfies_minus_lt : satisfiesAxLiftV0_minus_LT .realHilbert :=
  ⟨by unfold satisfiesFinite; decide, trivial⟩

theorem quat_satisfies_minus_lt : satisfiesAxLiftV0_minus_LT .quaternionicHilbert :=
  ⟨by unfold satisfiesFinite; decide, trivial⟩

theorem complex_satisfies_minus_lt : satisfiesAxLiftV0_minus_LT .complexHilbert :=
  ⟨complex_satisfies_finite, trivial⟩

/-- All three registry lifts pass {A_finite, A_l1_shadow}. -/
theorem all_registry_pass_v0_minus_lt :
    satisfiesAxLiftV0_minus_LT .complexHilbert ∧
    satisfiesAxLiftV0_minus_LT .realHilbert ∧
    satisfiesAxLiftV0_minus_LT .quaternionicHilbert :=
  ⟨complex_satisfies_minus_lt, real_satisfies_minus_lt, quat_satisfies_minus_lt⟩

/-- Local tomography is the only V0 axiom that excludes rebit/quat on this registry. -/
theorem lt_is_sole_v0_discriminator_on_registry :
    (∀ L : NamedLift, L = .complexHilbert ∨ L = .realHilbert ∨ L = .quaternionicHilbert →
      satisfiesAxLiftV0_minus_LT L) ∧
    satisfiesLocalTomography .complexHilbert ∧
    ¬ satisfiesLocalTomography .realHilbert ∧
    ¬ satisfiesLocalTomography .quaternionicHilbert := by
  refine ⟨?_, complex_satisfies_lt, real_fails_lt, quat_fails_lt⟩
  intro L h
  rcases h with h | h | h
  · simpa [h] using complex_satisfies_minus_lt
  · simpa [h] using real_satisfies_minus_lt
  · simpa [h] using quat_satisfies_minus_lt

/-- Blocking axiom certificate for a lift that fails V0 (only LT fails on registry). -/
inductive BlockingAxiom where
  | none
  | localTomography
deriving DecidableEq, Repr

def blockingAxiom : NamedLift → BlockingAxiom
  | .complexHilbert => .none
  | .realHilbert => .localTomography
  | .quaternionicHilbert => .localTomography

theorem blocking_complex_none : blockingAxiom .complexHilbert = .none := rfl

theorem blocking_real_lt : blockingAxiom .realHilbert = .localTomography := rfl

theorem blocking_quat_lt : blockingAxiom .quaternionicHilbert = .localTomography := rfl

theorem blocking_matches_v0_status :
    (blockingAxiom .complexHilbert = .none ∧ satisfiesAxLiftV0 .complexHilbert) ∧
    (blockingAxiom .realHilbert = .localTomography ∧ ¬ satisfiesAxLiftV0 .realHilbert) ∧
    (blockingAxiom .quaternionicHilbert = .localTomography ∧
      ¬ satisfiesAxLiftV0 .quaternionicHilbert) :=
  ⟨⟨rfl, complex_satisfies_v0⟩, ⟨rfl, real_fails_v0⟩, ⟨rfl, quat_fails_v0⟩⟩

/-- Enumerative uniqueness on the explicit registry list: filter by LT (effective V0 check). -/
def registryV0Satisfiers : List NamedLift :=
  registry.filter (fun L => decide (localProd L 2 2 = compositeParams L 2 2))

theorem registry_v0_satisfiers_is_complex_only :
    registryV0Satisfiers = [.complexHilbert] := by
  native_decide

theorem registry_exactly_one_v0_satisfier :
    registryV0Satisfiers.length = 1 ∧
    registryV0Satisfiers.head? = some .complexHilbert := by
  native_decide

/-! ## Optional AX-LIFT-V0.1 additive labels (named, not forced into V0)

Upgrade path toward purification / continuous reversible connectedness
(W6.14 residual / Hardy–Masanes–Müller style). These are **not** members of
`axLiftV0` and are not used for registry classification this fire.
-/

inductive OptionalAxiomId where
  | A_purification_capacity
  | A_continuous_reversible_connectedness
deriving DecidableEq, Repr

def axLiftV0_1_optional : List OptionalAxiomId :=
  [.A_purification_capacity, .A_continuous_reversible_connectedness]

theorem axLiftV0_1_optional_card : axLiftV0_1_optional.length = 2 := by
  decide

/-- V0.1 optional axioms leave the forced V0 core cardinality unchanged. -/
theorem v0_forced_card_unchanged_by_v01 : axLiftV0.length = 3 :=
  axLiftV0_card

/-! ## Partial V0.1 activation: purification capacity (TOY-MECH)

Bind W6.14 purification capital as an **optional** satisfaction check without
adding it to `axLiftV0`. Continuous reversible connectedness remains unactivated.
-/

/-- Joint residual table (W6.14-shaped purification witness). -/
structure JointWeight where
  w00 : Int
  w01 : Int
  w10 : Int
  w11 : Int
  deriving DecidableEq, Repr

def margA (j : JointWeight) : Int × Int :=
  (j.w00 + j.w01, j.w10 + j.w11)

def IsMixedBit (w0 w1 : Int) : Prop := w0 > 0 ∧ w1 > 0

/-- Quantum pure support (Bell diagonal) — not classical single-atom purity. -/
def IsQuantumPureSupport (j : JointWeight) : Prop :=
  (j.w00 > 0 ∧ j.w01 = 0 ∧ j.w10 = 0 ∧ j.w11 > 0) ∨
  (j.w00 = 0 ∧ j.w01 > 0 ∧ j.w10 > 0 ∧ j.w11 = 0)

def bellLikeJoint : JointWeight :=
  { w00 := 1, w01 := 0, w10 := 0, w11 := 1 }

def fairBit : Int × Int := (1, 1)

theorem bellLike_quantum_pure : IsQuantumPureSupport bellLikeJoint := by
  dsimp [IsQuantumPureSupport, bellLikeJoint]
  exact Or.inl ⟨Int.one_pos, rfl, rfl, Int.one_pos⟩

theorem bellLike_margA_fair : margA bellLikeJoint = fairBit := by
  simp [margA, bellLikeJoint, fairBit]

theorem fairBit_mixed : IsMixedBit fairBit.1 fairBit.2 := by
  simp [fairBit, IsMixedBit]

/-- Optional purification: mixed fair bit is A-marginal of a quantum-pure joint. -/
def satisfiesPurificationCapacity (L : NamedLift) : Prop :=
  match L with
  | .complexHilbert =>
      ∃ j : JointWeight, IsQuantumPureSupport j ∧ margA j = fairBit
  | .realHilbert =>
      -- Rebit bipartite pure states also admit the same real Bell-diagonal support.
      ∃ j : JointWeight, IsQuantumPureSupport j ∧ margA j = fairBit
  | .quaternionicHilbert => False  -- unclaimed this fire

theorem complex_satisfies_purification :
    satisfiesPurificationCapacity .complexHilbert :=
  ⟨bellLikeJoint, bellLike_quantum_pure, bellLike_margA_fair⟩

theorem real_satisfies_purification :
    satisfiesPurificationCapacity .realHilbert :=
  ⟨bellLikeJoint, bellLike_quantum_pure, bellLike_margA_fair⟩

theorem quat_purification_unclaimed :
    ¬ satisfiesPurificationCapacity .quaternionicHilbert := fun h => h

/-- Continuous reversible connectedness is **not** FinL1-native (no continuum group). -/
def satisfiesContinuousReversible (_L : NamedLift) : Prop := False

theorem continuous_rev_refused_on_registry (L : NamedLift) :
    ¬ satisfiesContinuousReversible L := fun h => h

/-- Optional axiom satisfaction dispatcher. -/
def satisfiesOptional (L : NamedLift) : OptionalAxiomId → Prop
  | .A_purification_capacity => satisfiesPurificationCapacity L
  | .A_continuous_reversible_connectedness => satisfiesContinuousReversible L

theorem purification_optional_active_complex :
    satisfiesOptional .complexHilbert .A_purification_capacity :=
  complex_satisfies_purification

theorem continuous_optional_inactive (L : NamedLift) :
    ¬ satisfiesOptional L .A_continuous_reversible_connectedness :=
  continuous_rev_refused_on_registry L

/-- V0 classification is unchanged by optional activation (rebit still fails V0). -/
theorem v0_unaffected_by_purification_activation :
    satisfiesAxLiftV0 .complexHilbert ∧
    ¬ satisfiesAxLiftV0 .realHilbert ∧
    satisfiesPurificationCapacity .realHilbert :=
  ⟨complex_satisfies_v0, real_fails_v0, real_satisfies_purification⟩

/-- Activation status for optional V0.1 additives. -/
inductive OptionalActivationStatus where
  | activatedToyMech
  | refusedOnFinL1
  | openContinuumImport
  | openUnactivated
  deriving DecidableEq, Repr

def purificationActivationStatus : OptionalActivationStatus := .activatedToyMech
/-- Continuous connectedness cannot activate on the discrete FinL1 registry. -/
def continuousActivationStatus : OptionalActivationStatus := .refusedOnFinL1
/-- Continuum-host pathway for continuous dynamics remains an import residual. -/
def continuousContinuumPathwayStatus : OptionalActivationStatus := .openContinuumImport

theorem purification_activation_receipt :
    purificationActivationStatus = OptionalActivationStatus.activatedToyMech := rfl

theorem continuous_refused_on_finL1_receipt :
    continuousActivationStatus = OptionalActivationStatus.refusedOnFinL1 := rfl

theorem continuous_continuum_pathway_open :
    continuousContinuumPathwayStatus = OptionalActivationStatus.openContinuumImport :=
  rfl

/-- Host tags for continuous optional (honest continuum fence). -/
inductive ContinuumHost where
  | finL1Discrete
  | continuumImport
  deriving DecidableEq, Repr

/-- Continuous reversible connectedness is never satisfied under FinL1 host. -/
def continuousUnderHost : ContinuumHost → NamedLift → Prop
  | .finL1Discrete, _ => False
  | .continuumImport, _ => False  -- import pathway named, not activated as MECH

theorem continuous_under_finL1_refused (L : NamedLift) :
    ¬ continuousUnderHost .finL1Discrete L := fun h => h

theorem continuous_under_continuum_import_unactivated (L : NamedLift) :
    ¬ continuousUnderHost .continuumImport L := fun h => h

/-- **V0.1 partial activation package** (does not rewrite V0). -/
theorem v01_partial_activation_package :
    satisfiesPurificationCapacity .complexHilbert ∧
    satisfiesPurificationCapacity .realHilbert ∧
    ¬ satisfiesPurificationCapacity .quaternionicHilbert ∧
    (∀ L, ¬ satisfiesContinuousReversible L) ∧
    axLiftV0.length = 3 ∧
    purificationActivationStatus = .activatedToyMech ∧
    continuousActivationStatus = .refusedOnFinL1 ∧
    continuousContinuumPathwayStatus = .openContinuumImport :=
  ⟨complex_satisfies_purification, real_satisfies_purification,
    quat_purification_unclaimed, continuous_rev_refused_on_registry,
    axLiftV0_card, rfl, rfl, rfl⟩

/-! ## Multipartite LT3 consistency with V0 (W5.5 capital bind)

V0 forces bipartite LT at 2⊗2 only. The multipartite three-qubit LT product
check (SEP-CHSH-FIELD / W5.5) is **consistent** with the V0 registry filter:
only complex satisfies LT3 among the three lifts. This is **not** a new forced
V0 axiom — it is a dual consistency residual (optional upgrade path).
-/

/-- Three-factor local density-param product (qubits). -/
def localProd3 (L : NamedLift) : Nat :=
  densityParams L 2 * densityParams L 2 * densityParams L 2

/-- Composite density params on three-qubit total dim $2^3=8$. -/
def compositeParams3 (L : NamedLift) : Nat :=
  densityParams L 8

def satisfiesLocalTomography3 (L : NamedLift) : Prop :=
  localProd3 L = compositeParams3 L

theorem complex_satisfies_lt3 : satisfiesLocalTomography3 .complexHilbert := by
  unfold satisfiesLocalTomography3 localProd3 compositeParams3 densityParams
  decide

theorem real_fails_lt3 : ¬ satisfiesLocalTomography3 .realHilbert := by
  unfold satisfiesLocalTomography3 localProd3 compositeParams3 densityParams
  decide

theorem quat_fails_lt3 : ¬ satisfiesLocalTomography3 .quaternionicHilbert := by
  unfold satisfiesLocalTomography3 localProd3 compositeParams3 densityParams
  decide

theorem lt3_numbers :
    localProd3 .complexHilbert = 64 ∧ compositeParams3 .complexHilbert = 64 ∧
    localProd3 .realHilbert = 27 ∧ compositeParams3 .realHilbert = 36 ∧
    localProd3 .quaternionicHilbert = 216 ∧ compositeParams3 .quaternionicHilbert = 120 := by
  unfold localProd3 compositeParams3 densityParams
  decide

/-- V0 satisfier also passes multipartite LT3; V0 failers fail LT3. -/
theorem multipartite_lt3_consistent_with_v0 :
    (satisfiesAxLiftV0 .complexHilbert ∧ satisfiesLocalTomography3 .complexHilbert) ∧
    (¬ satisfiesAxLiftV0 .realHilbert ∧ ¬ satisfiesLocalTomography3 .realHilbert) ∧
    (¬ satisfiesAxLiftV0 .quaternionicHilbert ∧ ¬ satisfiesLocalTomography3 .quaternionicHilbert) :=
  ⟨⟨complex_satisfies_v0, complex_satisfies_lt3⟩,
    ⟨real_fails_v0, real_fails_lt3⟩,
    ⟨quat_fails_v0, quat_fails_lt3⟩⟩

/-- LT3 is not a forced member of `axLiftV0` (card remains 3). -/
theorem lt3_not_forced_into_v0 :
    axLiftV0.length = 3 ∧ AxiomId.A_local_tomography ∈ axLiftV0 :=
  ⟨axLiftV0_card, axLiftV0_has_lt⟩

/-- **Continuous fence + multipartite LT3 package** (this residual). -/
theorem continuous_fence_and_lt3_package :
    continuousActivationStatus = .refusedOnFinL1 ∧
    continuousContinuumPathwayStatus = .openContinuumImport ∧
    (∀ L, ¬ continuousUnderHost .finL1Discrete L) ∧
    (∀ L, ¬ continuousUnderHost .continuumImport L) ∧
    satisfiesLocalTomography3 .complexHilbert ∧
    ¬ satisfiesLocalTomography3 .realHilbert ∧
    ¬ satisfiesLocalTomography3 .quaternionicHilbert ∧
    axLiftV0.length = 3 :=
  ⟨rfl, rfl, continuous_under_finL1_refused, continuous_under_continuum_import_unactivated,
    complex_satisfies_lt3, real_fails_lt3, quat_fails_lt3, axLiftV0_card⟩

/-! ## Literature / residual fences (not mechanized theorems) -/

/-- Full Koecher–Vinberg / Jordan classification is **not** claimed derived here. -/
inductive LiteratureTarget where
  | koecherVinbergJordan
  | hardyMasanesMuellerStyle
deriving DecidableEq, Repr

def fullJordanClassification_open : Prop := True

theorem jordan_classification_marked_open : fullJordanClassification_open :=
  trivial

/-- Absolute "all lifts" completeness refused (W5.11 registry fence alignment). -/
def absoluteLiftCompleteness_refused : Prop := False

theorem no_absolute_completeness : ¬ absoluteLiftCompleteness_refused := by
  intro h
  exact h

/-! ## Axiom-set naming receipt (W5.6 exit fragment) -/

structure NamedAxiomSet where
  id : String
  axioms : List AxiomId
  literature_target : Option LiteratureTarget
  optional_axioms : List OptionalAxiomId := []

def axLiftV0_packet : NamedAxiomSet :=
  { id := "AX-LIFT-V0"
    axioms := axLiftV0
    literature_target := some .koecherVinbergJordan
    optional_axioms := [] }

/-- V0.1 packet names optional additives without promoting them into forced V0. -/
def axLiftV0_1_packet : NamedAxiomSet :=
  { id := "AX-LIFT-V0.1"
    axioms := axLiftV0
    literature_target := some .hardyMasanesMuellerStyle
    optional_axioms := axLiftV0_1_optional }

theorem axLiftV0_packet_id : axLiftV0_packet.id = "AX-LIFT-V0" := rfl

theorem axLiftV0_packet_three_axioms : axLiftV0_packet.axioms.length = 3 := by
  decide

theorem axLiftV0_1_packet_keeps_v0_core :
    axLiftV0_1_packet.axioms = axLiftV0 ∧
    axLiftV0_1_packet.optional_axioms.length = 2 ∧
    axLiftV0_1_packet.id = "AX-LIFT-V0.1" := by
  refine ⟨rfl, ?_, rfl⟩
  decide

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end LiftClassification
end QM

#print axioms QM.LiftClassification.registry_classification_v0
#print axioms QM.LiftClassification.complex_satisfies_v0
#print axioms QM.LiftClassification.real_fails_v0
#print axioms QM.LiftClassification.lt_is_sole_v0_discriminator_on_registry
#print axioms QM.LiftClassification.blocking_matches_v0_status
#print axioms QM.LiftClassification.registry_exactly_one_v0_satisfier
#print axioms QM.LiftClassification.axLiftV0_1_packet_keeps_v0_core
#print axioms QM.LiftClassification.axLiftV0_packet_id
#print axioms QM.LiftClassification.v01_partial_activation_package
#print axioms QM.LiftClassification.continuous_fence_and_lt3_package
#print axioms QM.LiftClassification.multipartite_lt3_consistent_with_v0
#print axioms QM.LiftClassification.structure_not_auth
