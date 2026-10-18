import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.Analysis.Matrix.Order
import Mathlib.Analysis.Complex.Circle
import Mathlib.Tactic
import «qm_ob_spectral_finite»
import «qm_ob_instrument_luders»
import «qm_compose_monoidal_structure»
import «qm_import_independence»
import «qm_import_necessity»
import «qm_import_sufficiency»
import «qm_import_minimality»
import «qm_import_completeness_audit»

/-!
# Wave 6 completion boundary

This module closes the stated general-finite-dimensional spectral and
finite-outcome instrument surfaces on an explicit complex-matrix import host.
It also supplies typed LT/OB-U1 split models and the resulting separate-slot
independence matrix. Nothing here derives the complex host from FinL1.

AuthorityEffect: None.
-/

noncomputable section

namespace QM
namespace Wave6Completion

open scoped BigOperators ComplexOrder MatrixOrder
open Matrix

/-! ## W6.10: exact Mathlib general-n Hermitian spectral import -/

section GeneralSpectral

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- General finite-dimensional Hermitian diagonalization on the explicitly
imported complex matrix host. This binds Mathlib's spectral theorem; it is not
a derivation of complex scalars from the FinL1 carrier. -/
theorem hermitian_general_n
    (A : Matrix n n ℂ) (hA : A.IsHermitian) :
    ∃ (U : Matrix.unitaryGroup n ℂ) (eigenvalues : n → ℝ),
      A = (U : Matrix n n ℂ) *
        Matrix.diagonal (RCLike.ofReal ∘ eigenvalues) * star (U : Matrix n n ℂ) := by
  refine ⟨hA.eigenvectorUnitary, hA.eigenvalues, ?_⟩
  simpa [Unitary.conjStarAlgAut_apply] using hA.spectral_theorem

/-- Every selected eigenvector satisfies the eigen-equation. -/
theorem hermitian_general_n_eigenvector
    (A : Matrix n n ℂ) (hA : A.IsHermitian) (j : n) :
    A *ᵥ ⇑(hA.eigenvectorBasis j) =
      (hA.eigenvalues j : ℂ) • ⇑(hA.eigenvectorBasis j) := by
  simpa using hA.mulVec_eigenvectorBasis j

end GeneralSpectral

/-! ## W6.12: arbitrary finite-outcome POVMs and Kraus instruments -/

section FiniteInstrument

variable {n outcome : Type*}
variable [Fintype n] [DecidableEq n] [Nonempty n]
variable [Fintype outcome] [DecidableEq outcome]

/-- A general finite POVM on the explicit complex n-dimensional host. -/
structure FinitePOVM where
  effect : outcome → Matrix n n ℂ
  positive : ∀ i, (effect i).PosSemidef
  resolution : ∑ i, effect i = 1

/-- A general finite-outcome single-Kraus-per-outcome instrument. Multiple
Kraus operators per outcome are represented by refining the finite outcome
index and then coarse-graining. -/
structure FiniteKrausInstrument where
  kraus : outcome → Matrix n n ℂ
  complete : ∑ i, (kraus i)ᴴ * kraus i = 1

def FiniteKrausInstrument.effect
    (I : FiniteKrausInstrument (n := n) (outcome := outcome))
    (i : outcome) : Matrix n n ℂ :=
  (I.kraus i)ᴴ * I.kraus i

theorem FiniteKrausInstrument.effect_positive
    (I : FiniteKrausInstrument (n := n) (outcome := outcome))
    (i : outcome) :
    (I.effect i).PosSemidef := by
  exact Matrix.posSemidef_conjTranspose_mul_self (I.kraus i)

def FiniteKrausInstrument.toPOVM
    (I : FiniteKrausInstrument (n := n) (outcome := outcome)) :
    FinitePOVM (n := n) (outcome := outcome) where
  effect := I.effect
  positive := I.effect_positive
  resolution := I.complete

def FiniteKrausInstrument.branch
    (I : FiniteKrausInstrument (n := n) (outcome := outcome))
    (i : outcome) (ρ : Matrix n n ℂ) : Matrix n n ℂ :=
  I.kraus i * ρ * (I.kraus i)ᴴ

def FiniteKrausInstrument.channel
    (I : FiniteKrausInstrument (n := n) (outcome := outcome))
    (ρ : Matrix n n ℂ) : Matrix n n ℂ :=
  ∑ i, I.branch i ρ

theorem FiniteKrausInstrument.branch_positive
    (I : FiniteKrausInstrument (n := n) (outcome := outcome))
    (i : outcome) (ρ : Matrix n n ℂ) (hρ : ρ.PosSemidef) :
    (I.branch i ρ).PosSemidef := by
  exact hρ.mul_mul_conjTranspose_same (I.kraus i)

theorem FiniteKrausInstrument.channel_positive
    (I : FiniteKrausInstrument (n := n) (outcome := outcome))
    (ρ : Matrix n n ℂ) (hρ : ρ.PosSemidef) :
    (I.channel ρ).PosSemidef := by
  exact Matrix.posSemidef_sum Finset.univ (fun i _ => I.branch_positive i ρ hρ)

theorem FiniteKrausInstrument.channel_trace
    (I : FiniteKrausInstrument (n := n) (outcome := outcome))
    (ρ : Matrix n n ℂ) :
    (I.channel ρ).trace = ρ.trace := by
  calc
    (I.channel ρ).trace =
        ∑ i, (I.branch i ρ).trace := by
          simp [FiniteKrausInstrument.channel]
    _ = ∑ i, (((I.kraus i)ᴴ * I.kraus i) * ρ).trace := by
          apply Finset.sum_congr rfl
          intro i _
          exact Matrix.trace_mul_cycle (I.kraus i) ρ (I.kraus i)ᴴ
    _ = ((∑ i, (I.kraus i)ᴴ * I.kraus i) * ρ).trace := by
          rw [Finset.sum_mul]
          simp
    _ = ρ.trace := by rw [I.complete, one_mul]

/-- Every finite POVM has its canonical square-root Kraus instrument on the
imported complex matrix host. -/
noncomputable def FinitePOVM.sqrtInstrument
    (P : FinitePOVM (n := n) (outcome := outcome)) :
    FiniteKrausInstrument (n := n) (outcome := outcome) where
  kraus i := CFC.sqrt (P.effect i)
  complete := by
    calc
      ∑ i, (CFC.sqrt (P.effect i))ᴴ * CFC.sqrt (P.effect i) =
          ∑ i, (CFC.sqrt (P.effect i)) ^ 2 := by
            apply Finset.sum_congr rfl
            intro i _
            rw [(CFC.sqrt_nonneg (P.effect i)).posSemidef.isHermitian]
            simp [pow_two]
      _ = ∑ i, P.effect i := by
            apply Finset.sum_congr rfl
            intro i _
            exact CFC.sq_sqrt (P.effect i) (P.positive i).nonneg
      _ = 1 := P.resolution

theorem FinitePOVM.sqrtInstrument_effect
    (P : FinitePOVM (n := n) (outcome := outcome)) (i : outcome) :
    P.sqrtInstrument.effect i = P.effect i := by
  change (CFC.sqrt (P.effect i))ᴴ * CFC.sqrt (P.effect i) = P.effect i
  rw [(CFC.sqrt_nonneg (P.effect i)).posSemidef.isHermitian]
  simpa [pow_two] using CFC.sq_sqrt (P.effect i) (P.positive i).nonneg

/-- General finite POVM realization: positivity, normalization, positive
branches, and trace-preserving aggregate channel. -/
theorem general_povm_finite
    (P : FinitePOVM (n := n) (outcome := outcome)) :
    (∀ i, (P.sqrtInstrument.effect i).PosSemidef) ∧
    (∑ i, P.sqrtInstrument.effect i = 1) ∧
    (∀ i ρ, ρ.PosSemidef → (P.sqrtInstrument.branch i ρ).PosSemidef) ∧
    (∀ ρ, (P.sqrtInstrument.channel ρ).trace = ρ.trace) := by
  exact ⟨P.sqrtInstrument.effect_positive,
    P.sqrtInstrument.complete,
    P.sqrtInstrument.branch_positive,
    P.sqrtInstrument.channel_trace⟩

end FiniteInstrument

/-! ## W6.14: typed LT / OB-U1 split models -/

namespace LtU1Split

inductive PhaseKind where
  | trivial
  | unitCircle
  deriving DecidableEq, Repr

/-- The phase tag is not merely a Boolean: its carrier is either the one-point
group-shaped type or Mathlib's actual complex unit circle. -/
def PhaseCarrier : PhaseKind → Type
  | .trivial => PUnit
  | .unitCircle => Circle

structure TomographyPhaseHost where
  localAParams : Nat
  localBParams : Nat
  jointParams : Nat
  phase : PhaseKind
  deriving DecidableEq, Repr

def HasLocalTomography (H : TomographyPhaseHost) : Prop :=
  H.jointParams = H.localAParams * H.localBParams

def HasOBU1 (H : TomographyPhaseHost) : Prop :=
  H.phase = .unitCircle

/-- A classical finite product: locally tomographic parameter count, with only
a trivial phase carrier. -/
def classicalLTWithoutU1 : TomographyPhaseHost :=
  { localAParams := 2, localBParams := 3, jointParams := 6, phase := .trivial }

/-- A U(1)-carrying host with one additional holistic joint parameter, hence
not locally tomographic. -/
def u1WithoutLT : TomographyPhaseHost :=
  { localAParams := 2, localBParams := 2, jointParams := 5, phase := .unitCircle }

theorem trivial_phase_carrier_subsingleton :
    ∀ z : PhaseCarrier .trivial, z = PUnit.unit := by
  intro z
  cases z
  rfl

theorem unit_circle_phase_nontrivial :
    Circle.exp Real.pi ≠ (1 : Circle) :=
  Circle.exp_pi_ne_one

theorem classical_lt_without_u1 :
    HasLocalTomography classicalLTWithoutU1 ∧
    ¬ HasOBU1 classicalLTWithoutU1 := by
  constructor
  · norm_num [HasLocalTomography, classicalLTWithoutU1]
  · simp [HasOBU1, classicalLTWithoutU1]

theorem u1_without_lt :
    HasOBU1 u1WithoutLT ∧
    ¬ HasLocalTomography u1WithoutLT := by
  constructor
  · simp [HasOBU1, u1WithoutLT]
  · norm_num [HasLocalTomography, u1WithoutLT]

def SplitsLtAndU1 (H : TomographyPhaseHost) : Prop :=
  (HasLocalTomography H ∧ ¬ HasOBU1 H) ∨
  (¬ HasLocalTomography H ∧ HasOBU1 H)

theorem two_sided_lt_u1_split :
    SplitsLtAndU1 classicalLTWithoutU1 ∧
    SplitsLtAndU1 u1WithoutLT := by
  exact ⟨Or.inl classical_lt_without_u1,
    Or.inr ⟨u1_without_lt.2, u1_without_lt.1⟩⟩

/-- The old NamedLift coupling theorem remains true on its three constructors;
these countermodels live on a wider typed host class. -/
theorem named_registry_coupling_preserved :
    ∀ L : QM.ComposeMonoidal.NamedLift,
      QM.ComposeMonoidal.SatisfiesCompositeLT L 2 2 ↔
        QM.ComposeMonoidal.HasComplexPhaseCarrier L :=
  QM.ComposeMonoidal.lt_iff_complex_phase_on_registry

end LtU1Split

/-! ## W6.19/W6.20/W6.22: declared full B9 independence matrix -/

namespace FullBasis

inductive ImportSlot where
  | OB_NONCOMM
  | OB_UNITARY
  | OB_CLONE
  | CONT_TIME
  | OB_HERM
  | OB_L2_READOUT
  | OB_BORN
  | OB_U1
  | COMPOSITE_LT
  deriving DecidableEq, Repr

def basisB9 : List ImportSlot :=
  [.OB_NONCOMM, .OB_UNITARY, .OB_CLONE, .CONT_TIME, .OB_HERM,
   .OB_L2_READOUT, .OB_BORN, .OB_U1, .COMPOSITE_LT]

theorem basisB9_card : basisB9.length = 9 := by decide

abbrev LedgerModel := ImportSlot → Bool

def admits (M : LedgerModel) (s : ImportSlot) : Bool := M s

def dropModel (drop : ImportSlot) : LedgerModel :=
  fun s => decide (s ≠ drop)

def failsExactly (M : LedgerModel) (drop : ImportSlot) : Prop :=
  admits M drop = false ∧
  ∀ s, s ≠ drop → admits M s = true

theorem drop_model_fails_exactly (drop : ImportSlot) :
    failsExactly (dropModel drop) drop := by
  constructor
  · simp [admits, dropModel]
  · intro s hs
    simp [admits, dropModel, hs]

def admitsMatrix (row col : ImportSlot) : Bool :=
  admits (dropModel row) col

theorem admits_matrix_diagonal_false (s : ImportSlot) :
    admitsMatrix s s = false := by
  simp [admitsMatrix, admits, dropModel]

theorem admits_matrix_off_diagonal_true
    (row col : ImportSlot) (h : row ≠ col) :
    admitsMatrix row col = true := by
  simp [admitsMatrix, admits, dropModel, Ne.symm h]

/-- Concrete capital attached to every drop row. The first seven rows bind the
existing W6 capital; the final two bind the typed LT/U1 split above. -/
def DropCapital : ImportSlot → Prop
  | .OB_NONCOMM =>
      (QM.ImportIndependence.diagA.1 * QM.ImportIndependence.diagB.1,
       QM.ImportIndependence.diagA.2 * QM.ImportIndependence.diagB.2) =
      (QM.ImportIndependence.diagB.1 * QM.ImportIndependence.diagA.1,
       QM.ImportIndependence.diagB.2 * QM.ImportIndependence.diagA.2)
  | .OB_UNITARY =>
      QM.ImportIndependence.isColumnStochastic QM.ImportIndependence.resetKernel ∧
      ¬ QM.ImportIndependence.isDoublyStochastic QM.ImportIndependence.resetKernel
  | .OB_CLONE =>
      QM.ImportIndependence.classicalClone QM.ImportIndependence.fairBit = (1, 1, 1, 1)
  | .CONT_TIME =>
      QM.ImportIndependence.discreteStepsOnly = true ∧
      QM.ImportIndependence.continuousGeneratorAdmitted = false
  | .OB_HERM =>
      ¬ QM.ImportIndependence.IsHermitianToy QM.ImportIndependence.nonHermG
  | .OB_L2_READOUT =>
      QM.ImportIndependence.l2ReadoutForcedFromL1Shadow = false ∧
      QM.ImportIndependence.quadraticInnerProductStructureAdmitted = false
  | .OB_BORN =>
      QM.ImportIndependence.bornPairingForcedFromL2HostAlone = false ∧
      QM.ImportIndependence.bornUniquenessSelectionAdmitted = false
  | .OB_U1 =>
      LtU1Split.HasLocalTomography LtU1Split.classicalLTWithoutU1 ∧
      ¬ LtU1Split.HasOBU1 LtU1Split.classicalLTWithoutU1
  | .COMPOSITE_LT =>
      LtU1Split.HasOBU1 LtU1Split.u1WithoutLT ∧
      ¬ LtU1Split.HasLocalTomography LtU1Split.u1WithoutLT

theorem drop_capital_complete (s : ImportSlot) : DropCapital s := by
  cases s with
  | OB_NONCOMM => exact QM.ImportIndependence.classical_diag_commute
  | OB_UNITARY => exact QM.ImportIndependence.reset_column_not_doubly
  | OB_CLONE => exact QM.ImportIndependence.classical_clone_fair_exists
  | CONT_TIME => exact QM.ImportIndependence.cont_time_not_forced_by_discrete
  | OB_HERM => exact QM.ImportIndependence.nonHermG_not_hermitian
  | OB_L2_READOUT => exact QM.ImportIndependence.l2_drop_witness_flags
  | OB_BORN => exact QM.ImportIndependence.born_drop_witness_flags
  | OB_U1 => exact LtU1Split.classical_lt_without_u1
  | COMPOSITE_LT => exact LtU1Split.u1_without_lt

/-- Full matrix theorem for the declared B9 ledger: one capital-backed
drop-exactly-one row per slot. This is ledger-relative, not absolute
independence of every conceivable reconstruction axiom. -/
theorem full_basis_independence_matrix :
    basisB9.length = 9 ∧
    (∀ s, failsExactly (dropModel s) s) ∧
    (∀ s, admitsMatrix s s = false) ∧
    (∀ row col, row ≠ col → admitsMatrix row col = true) ∧
    (∀ s, DropCapital s) :=
  ⟨basisB9_card, drop_model_fails_exactly, admits_matrix_diagonal_false,
    admits_matrix_off_diagonal_true, drop_capital_complete⟩

/-- W6.20 ledger dual: the pure FinL1 ledger contains none of the nine
declared imports. This is a model separation statement, not metatheoretic
non-derivability in arbitrary foundations. -/
def pureFinL1Ledger : LedgerModel := fun _ => false

theorem pure_finl1_fails_every_b9_import :
    ∀ s, admits pureFinL1Ledger s = false := by
  intro s
  rfl

def allImportsLedger : LedgerModel := fun _ => true

def CoversB9 (M : LedgerModel) : Prop :=
  ∀ s, admits M s = true

theorem all_imports_covers_b9 : CoversB9 allImportsLedger := by
  intro s
  rfl

/-- W6.22 minimality: deleting any one B9 slot destroys B9 coverage at exactly
that slot. -/
theorem drop_any_slot_loses_coverage (drop : ImportSlot) :
    ¬ CoversB9 (dropModel drop) := by
  intro h
  have hd := h drop
  simpa [admits, dropModel] using hd

theorem b9_minimality :
    CoversB9 allImportsLedger ∧
    ∀ drop, failsExactly (dropModel drop) drop ∧
      ¬ CoversB9 (dropModel drop) :=
  ⟨all_imports_covers_b9, fun drop =>
    ⟨drop_model_fails_exactly drop, drop_any_slot_loses_coverage drop⟩⟩

end FullBasis
/-! ## W6.21: exact conditional sufficiency seal -/

namespace SealedSufficiency

abbrev Target := QM.ImportSufficiency.RecoveryTarget

/-- The seventeen frozen conclusions are parameters, not definitions set to
True. This permits the seal to state exactly which propositions are recovered
in a particular carrier/import instantiation. -/
structure FrozenRecoveryClaims where
  t01 : Prop
  t02 : Prop
  t03 : Prop
  t04 : Prop
  t05 : Prop
  t06 : Prop
  t07 : Prop
  t08 : Prop
  t09 : Prop
  t10 : Prop
  t11 : Prop
  t12 : Prop
  t13 : Prop
  t14 : Prop
  t15 : Prop
  t16 : Prop
  t17 : Prop

def claimAt (C : FrozenRecoveryClaims) : Target → Prop
  | .T01 => C.t01
  | .T02 => C.t02
  | .T03 => C.t03
  | .T04 => C.t04
  | .T05 => C.t05
  | .T06 => C.t06
  | .T07 => C.t07
  | .T08 => C.t08
  | .T09 => C.t09
  | .T10 => C.t10
  | .T11 => C.t11
  | .T12 => C.t12
  | .T13 => C.t13
  | .T14 => C.t14
  | .T15 => C.t15
  | .T16 => C.t16
  | .T17 => C.t17

/-- A sealed import receipt must carry a proof of every frozen claim. The
fields cannot be inhabited by pathway flags or lemma-name strings. -/
structure SealedImportEvidence (C : FrozenRecoveryClaims) : Prop where
  t01 : C.t01
  t02 : C.t02
  t03 : C.t03
  t04 : C.t04
  t05 : C.t05
  t06 : C.t06
  t07 : C.t07
  t08 : C.t08
  t09 : C.t09
  t10 : C.t10
  t11 : C.t11
  t12 : C.t12
  t13 : C.t13
  t14 : C.t14
  t15 : C.t15
  t16 : C.t16
  t17 : C.t17

/-- SUF-SEALED-THEOREM, in its honest conditional form. It proves all
seventeen target propositions from an evidence object containing proofs of
all seventeen; it does not assert that FinL1 alone produces that object. -/
theorem sealed_sufficiency_conditional
    (C : FrozenRecoveryClaims) (E : SealedImportEvidence C) :
    ∀ t : Target, claimAt C t := by
  intro t
  cases t with
  | T01 => exact E.t01
  | T02 => exact E.t02
  | T03 => exact E.t03
  | T04 => exact E.t04
  | T05 => exact E.t05
  | T06 => exact E.t06
  | T07 => exact E.t07
  | T08 => exact E.t08
  | T09 => exact E.t09
  | T10 => exact E.t10
  | T11 => exact E.t11
  | T12 => exact E.t12
  | T13 => exact E.t13
  | T14 => exact E.t14
  | T15 => exact E.t15
  | T16 => exact E.t16
  | T17 => exact E.t17

/-- Exactness: the sealed evidence structure is equivalent to having every
frozen target proof. No target can be omitted from the receipt. -/
theorem sealed_evidence_iff_all_targets (C : FrozenRecoveryClaims) :
    SealedImportEvidence C ↔ ∀ t : Target, claimAt C t := by
  constructor
  · exact sealed_sufficiency_conditional C
  · intro h
    exact {
      t01 := h .T01
      t02 := h .T02
      t03 := h .T03
      t04 := h .T04
      t05 := h .T05
      t06 := h .T06
      t07 := h .T07
      t08 := h .T08
      t09 := h .T09
      t10 := h .T10
      t11 := h .T11
      t12 := h .T12
      t13 := h .T13
      t14 := h .T14
      t15 := h .T15
      t16 := h .T16
      t17 := h .T17 }

theorem frozen_target_count_retained :
    QM.ImportSufficiency.requiredTargets.length = 17 :=
  QM.ImportSufficiency.requiredTargets_card

end SealedSufficiency

/-! ## W6.23 completion audit (scoped) -/

/-- The audit joins actual theorem surfaces. Its scope is the declared B9
ledger plus the conditional 17-target seal; it is not a universal assertion
that no further physical assumption can ever be proposed. -/
theorem wave6_scoped_completion_audit :
    FullBasis.basisB9.length = 9 ∧
    (∀ s, FullBasis.DropCapital s) ∧
    (∀ s, FullBasis.failsExactly (FullBasis.dropModel s) s) ∧
    (∀ s, FullBasis.admits FullBasis.pureFinL1Ledger s = false) ∧
    FullBasis.CoversB9 FullBasis.allImportsLedger :=
  ⟨FullBasis.basisB9_card,
    FullBasis.drop_capital_complete,
    FullBasis.drop_model_fails_exactly,
    FullBasis.pure_finl1_fails_every_b9_import,
    FullBasis.all_imports_covers_b9⟩

end Wave6Completion
end QM
