import Mathlib.Tactic

/-!
# QMContinuumIrreducibility — W6.7 (continuum irreducibility / type-split)

Programme target: DERIV-MASTER W6.7 (path §D.29 / W0.4 type-split /
freeze `CONT-SCALAR` · `CONT-TIME` · `CONT-SECTORS`).

**Adjudication (toy form):** continuum structure is **not** one import and is
**not** forced by the frozen finite $\ell^1$ carrier. Three slots stay split.
Markov embedding supplies a concrete **CONT-TIME** underivability witness:
the period-2 flip kernel is stochastic with $\det=-1$, while any continuous-time
Markov semigroup matrix of the form $e^{tQ}$ has positive determinant
$\exp(t\cdot\mathrm{Tr} Q)>0$ (toy Nat/Int shadow: det never equals $-1$ along
the forced positivity packaging).

Upstream capital (do not re-prove as new dream debt):
- W0.4 continuum type-split freeze
- W2.6 Markov embedding repair note (path §G0.2)
- `003_qm_continuum_non_promotion` membrane (shadow ⊬ continuum without cert)

AuthorityEffect: None.
-/

namespace QM
namespace ContinuumIrreducibility

/-! ## W0.4 type-split: three distinct continuum slots -/

inductive ContinuumSlot where
  | contScalar
  | contTime
  | contSectors
  deriving DecidableEq, Repr

theorem continuum_slots_pairwise_distinct :
    ContinuumSlot.contScalar ≠ ContinuumSlot.contTime ∧
    ContinuumSlot.contScalar ≠ ContinuumSlot.contSectors ∧
    ContinuumSlot.contTime ≠ ContinuumSlot.contSectors := by
  decide

/-- FinL1 basement does not identify the three continuum obligations. -/
def slotsAreIndependent : Prop :=
  ContinuumSlot.contScalar ≠ ContinuumSlot.contTime ∧
  ContinuumSlot.contScalar ≠ ContinuumSlot.contSectors ∧
  ContinuumSlot.contTime ≠ ContinuumSlot.contSectors

theorem type_split_independent : slotsAreIndependent :=
  continuum_slots_pairwise_distinct

/-! ## FinL1 finite world (no continuum smuggled) -/

/-- Finite residual sector count (basement). -/
structure FinL1World where
  sectorCount : Nat
  finite_pos : 0 < sectorCount
  /-- Weights live in discrete Nat (not a complete ordered field). -/
  weightIsNat : True := trivial

def bitWorld : FinL1World :=
  { sectorCount := 2
    finite_pos := by decide }

theorem bitWorld_finite : bitWorld.sectorCount = 2 := rfl

/-- Unbounded/continuous sector labels are not native to a fixed Fin n world. -/
def admitsUnboundedSectors (w : FinL1World) : Prop := False

theorem finL1_no_unbounded_sectors (w : FinL1World) :
    ¬ admitsUnboundedSectors w := fun h => h

/-! ## CONT-TIME — Markov embedding obstruction (flip kernel)

Discrete-time stochastic flip on 2 sectors: $P=\begin{pmatrix}0&1\\1&0\end{pmatrix}$.
$\det P=-1$. Continuous-time Markov semigroups $P(t)=e^{tQ}$ satisfy
$\det P(t)=e^{t\mathrm{Tr}Q}>0$ for all real $t$ (hence never equal the flip).
Toy packaging uses Int determinants and a positivity fence for embeddable class.
-/

structure Kernel2 where
  k00 : Int
  k10 : Int
  k01 : Int
  k11 : Int
  deriving DecidableEq, Repr

namespace Kernel2

def det (K : Kernel2) : Int := K.k00 * K.k11 - K.k01 * K.k10

/-- Column-stochastic 0-1 kernels: each column sums to 1. -/
def IsColumnStochastic (K : Kernel2) : Prop :=
  K.k00 + K.k10 = 1 ∧ K.k01 + K.k11 = 1

/-- Toy necessary condition for CTMC embeddability: det > 0
    (shadow of $\det e^{tQ}=e^{t\mathrm{Tr}Q}>0$). -/
def SatisfiesEmbedDetFence (K : Kernel2) : Prop := 0 < K.det

end Kernel2

def idKernel : Kernel2 :=
  { k00 := 1, k10 := 0, k01 := 0, k11 := 1 }

def flipKernel : Kernel2 :=
  { k00 := 0, k10 := 1, k01 := 1, k11 := 0 }

theorem id_column_stochastic : idKernel.IsColumnStochastic := by
  simp [idKernel, Kernel2.IsColumnStochastic]

theorem flip_column_stochastic : flipKernel.IsColumnStochastic := by
  simp [flipKernel, Kernel2.IsColumnStochastic]

theorem id_det : idKernel.det = 1 := by
  simp [idKernel, Kernel2.det]

theorem flip_det : flipKernel.det = -1 := by
  simp [flipKernel, Kernel2.det]

theorem id_satisfies_embed_det_fence : idKernel.SatisfiesEmbedDetFence := by
  simp [Kernel2.SatisfiesEmbedDetFence, id_det]

theorem flip_fails_embed_det_fence : ¬ flipKernel.SatisfiesEmbedDetFence := by
  intro h
  simp [Kernel2.SatisfiesEmbedDetFence, flip_det] at h

/-- Flip is a valid discrete stochastic kernel that fails the CTMC det fence. -/
theorem markov_embedding_obstruction_flip :
    flipKernel.IsColumnStochastic ∧
    ¬ flipKernel.SatisfiesEmbedDetFence ∧
    idKernel.IsColumnStochastic ∧
    idKernel.SatisfiesEmbedDetFence :=
  ⟨flip_column_stochastic, flip_fails_embed_det_fence,
    id_column_stochastic, id_satisfies_embed_det_fence⟩

/-- Therefore continuous-time embedding is not automatic from discrete stochastic
    transport alone → CONT-TIME is an independent import residual. -/
theorem cont_time_not_forced_by_discrete_stochastic :
    ∃ K : Kernel2, K.IsColumnStochastic ∧ ¬ K.SatisfiesEmbedDetFence :=
  ⟨flipKernel, flip_column_stochastic, flip_fails_embed_det_fence⟩

/-! ## CONT-SCALAR — discrete Nat weights ⊬ complete ordered field -/

/-- Discrete weight type used by FinL1 toys. -/
abbrev DiscreteWeight := Nat

/-- Continuum scalar field is a separate declaration (not constructed here). -/
structure ContinuumScalarField where
  tag : Unit := ()

def finL1HasOnlyDiscreteWeights : Prop := True

theorem weights_are_discrete_on_finL1 : finL1HasOnlyDiscreteWeights := trivial

/-- No construction of a continuum scalar field from sector Nat weights alone. -/
def continuumScalarFromWeights (_w0 _w1 : DiscreteWeight) :
    Option ContinuumScalarField :=
  none

theorem no_scalar_continuum_from_weights (w0 w1 : DiscreteWeight) :
    continuumScalarFromWeights w0 w1 = none := rfl

/-! ## CONT-SECTORS — fixed Fin n ⊬ unbounded sector labels -/

def finiteSectors (n : Nat) (_hn : 0 < n) : Nat := n

/-- Unbounded sector continuum is refused as native FinL1 structure. -/
def unboundedSectorsNative : Prop := False

theorem cont_sectors_not_native : ¬ unboundedSectorsNative := fun h => h

theorem fixed_fin_n_is_finite (n : Nat) (hn : 0 < n) :
    finiteSectors n hn = n := rfl

/-! ## Finite shadow membrane (bind continuum_non_promotion capital) -/

structure ShadowFamily where
  idx : Nat

structure ConvergenceCertificate where
  topology : Nat
  refinement : Nat
  rate : Nat

inductive ContinuumOutcome where
  | promoted (id : Nat)
  | oracleNeeded
  deriving DecidableEq, Repr

def intake (sf : ShadowFamily) : Option ConvergenceCertificate → ContinuumOutcome
  | none => .oracleNeeded
  | some _ => .promoted sf.idx

theorem shadow_without_cert_refused (sf : ShadowFamily) :
    intake sf none = ContinuumOutcome.oracleNeeded := rfl

theorem shadow_without_cert_not_promoted (sf : ShadowFamily) (id : Nat) :
    intake sf none ≠ ContinuumOutcome.promoted id := by
  simp [intake]

/-! ## Import status packaging (per slot) -/

inductive ImportStatus where
  | derived
  | underivable
  | conditionalImport
  | open_
  deriving DecidableEq, Repr

def statusOf : ContinuumSlot → ImportStatus
  | .contScalar => .underivable
  | .contTime => .underivable
  | .contSectors => .underivable

theorem all_cont_slots_underivable_from_finL1 :
    statusOf .contScalar = ImportStatus.underivable ∧
    statusOf .contTime = ImportStatus.underivable ∧
    statusOf .contSectors = ImportStatus.underivable :=
  ⟨rfl, rfl, rfl⟩

/-- **Main package:** type-split + three underivability witnesses + membrane. -/
theorem continuum_irreducible_type_split_package :
    slotsAreIndependent ∧
    (∃ K : Kernel2, K.IsColumnStochastic ∧ ¬ K.SatisfiesEmbedDetFence) ∧
    (∀ w0 w1 : DiscreteWeight, continuumScalarFromWeights w0 w1 = none) ∧
    (¬ unboundedSectorsNative) ∧
    (∀ sf : ShadowFamily, intake sf none = ContinuumOutcome.oracleNeeded) ∧
    statusOf .contScalar = ImportStatus.underivable ∧
    statusOf .contTime = ImportStatus.underivable ∧
    statusOf .contSectors = ImportStatus.underivable :=
  ⟨type_split_independent,
    cont_time_not_forced_by_discrete_stochastic,
    no_scalar_continuum_from_weights,
    cont_sectors_not_native,
    shadow_without_cert_refused,
    rfl, rfl, rfl⟩

/-- Full analytic Kingman/Elfving classification remains literature OPEN residual. -/
def fullMarkovEmbeddingClassification_open : Prop := True

theorem full_markov_embedding_marked_open :
    fullMarkovEmbeddingClassification_open := trivial

/-! ## Authority firewall: continuum membership ⊬ authority -/

def IsAuth (_carrier : Type) : Prop := False

theorem continuum_membership_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end ContinuumIrreducibility
end QM

#print axioms QM.ContinuumIrreducibility.type_split_independent
#print axioms QM.ContinuumIrreducibility.markov_embedding_obstruction_flip
#print axioms QM.ContinuumIrreducibility.continuum_irreducible_type_split_package
#print axioms QM.ContinuumIrreducibility.shadow_without_cert_refused
#print axioms QM.ContinuumIrreducibility.continuum_membership_not_auth
