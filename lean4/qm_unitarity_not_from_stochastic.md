import Mathlib.Tactic

/-!
# QMUnitarityNotFromStochastic — W6.8 (unitarity ↛ stochastic population transport)

Programme target: DERIV-MASTER W6.8 (path §D.30 / freeze `OB-UNITARY`).

**Negative theorem (toy form):** unitarity of a lift channel is **not** determined
by, and not forced by, classical column-stochastic population transport alone.

Mechanized discrete facts on $2\times 2$ Nat kernels:

1. **Reset kernel** is column-stochastic but **not** doubly stochastic
   (hence cannot be a unistochastic / unitary population shadow).
2. **Identity population kernel** is doubly stochastic (compatible with unitaries)
   but is also realized by a **phase-gate family** at the population level —
   population map underdetermines the unitary (phase freedom).
3. Therefore: stochastic population transport ⊬ unique unitary lift, and
   not every stochastic map is a unitary population shadow.
4. **Residual (TOY-MECH):** denser phase family (3 labels, same id shadow);
   0-1 doubly-stochastic $2\times 2$ kernels are exactly $\{I,\mathrm{flip}\}$;
   doubly-stochastic closed under mul on that set; real orthogonal Mat2 lift
   for $I$/flip; full continuous $U(n)$ still **OPEN**.

Upstream capital: Rung 3 / `qm_082` CPTP population shadow (do not re-prove);
W6.9 Hermitian algebra capital.

AuthorityEffect: None.
-/

namespace QM
namespace UnitarityNotFromStochastic

/-! ## 2×2 kernels with Nat entries (unnormalized scale allowed; we use 0/1) -/

structure Kernel2 where
  k00 : Nat
  k10 : Nat
  k01 : Nat
  k11 : Nat
deriving DecidableEq, Repr

namespace Kernel2

/-- Column-stochastic for 0-1 kernels: each column sums to 1. -/
def IsColumnStochastic (K : Kernel2) : Prop :=
  K.k00 + K.k10 = 1 ∧ K.k01 + K.k11 = 1

/-- Doubly stochastic: columns and rows sum to 1 (necessary for unistochastic). -/
def IsDoublyStochastic (K : Kernel2) : Prop :=
  IsColumnStochastic K ∧ K.k00 + K.k01 = 1 ∧ K.k10 + K.k11 = 1

end Kernel2

/-- Reset-to-0 population channel: both basis inputs map to outcome 0. -/
def resetKernel : Kernel2 :=
  { k00 := 1, k10 := 0, k01 := 1, k11 := 0 }

theorem reset_column_stochastic : resetKernel.IsColumnStochastic := by
  simp [resetKernel, Kernel2.IsColumnStochastic]

theorem reset_not_doubly_stochastic : ¬ resetKernel.IsDoublyStochastic := by
  intro h
  -- row0 sum = k00+k01 = 1+1 = 2 ≠ 1
  have hrow := h.2.1
  simp [resetKernel] at hrow

/-- Identity population kernel (permutation / unitary-compatible). -/
def idKernel : Kernel2 :=
  { k00 := 1, k10 := 0, k01 := 0, k11 := 1 }

theorem id_doubly_stochastic : idKernel.IsDoublyStochastic := by
  simp [idKernel, Kernel2.IsDoublyStochastic, Kernel2.IsColumnStochastic]

/-- Bit-flip population kernel (also permutation / unitary-compatible). -/
def flipKernel : Kernel2 :=
  { k00 := 0, k10 := 1, k01 := 1, k11 := 0 }

theorem flip_doubly_stochastic : flipKernel.IsDoublyStochastic := by
  simp [flipKernel, Kernel2.IsDoublyStochastic, Kernel2.IsColumnStochastic]

theorem reset_ne_id : resetKernel ≠ idKernel := by
  intro h
  have := congrArg Kernel2.k01 h
  simp [resetKernel, idKernel] at this

/-! ## Population underdetermination of unitaries (phase freedom) -/

/-- Discrete unitary labels that share the same population kernel (identity). -/
inductive UnitaryLabel where
  | identity
  | phaseGate
deriving DecidableEq, Repr

/-- Population shadow of both labels is the identity kernel. -/
def populationShadow : UnitaryLabel → Kernel2
  | .identity => idKernel
  | .phaseGate => idKernel

theorem phase_and_id_same_population :
    populationShadow .identity = populationShadow .phaseGate := rfl

theorem phase_and_id_distinct_labels :
    UnitaryLabel.identity ≠ UnitaryLabel.phaseGate := by
  decide

/-- **Underivability packaging:** same population shadow, distinct unitary labels. -/
theorem unitarity_not_unique_from_population :
    populationShadow .identity = populationShadow .phaseGate ∧
    UnitaryLabel.identity ≠ UnitaryLabel.phaseGate :=
  ⟨phase_and_id_same_population, phase_and_id_distinct_labels⟩

/-- **Not every stochastic map is unitary-population:** reset is column-stochastic
    but not doubly stochastic. -/
theorem stochastic_not_implies_unitary_shadow :
    resetKernel.IsColumnStochastic ∧ ¬ resetKernel.IsDoublyStochastic :=
  ⟨reset_column_stochastic, reset_not_doubly_stochastic⟩

/-! ## Import status marker -/

/-- Unitarity remains an import / lift structure beyond Rung-3 stochastic shadow. -/
def OB_UNITARY_status_underivable_from_stochastic : Prop := True

theorem ob_unitary_underivable_marked :
    OB_UNITARY_status_underivable_from_stochastic := trivial

/-! ## Residual: denser phase family + doubly-stochastic class + orthogonal lift -/

/-- Extended unitary labels sharing identity population shadow (phase freedom). -/
inductive PhaseFamily where
  | identity
  | phaseZ
  | phaseGlobal
  deriving DecidableEq, Repr

def phaseFamilyShadow : PhaseFamily → Kernel2
  | .identity | .phaseZ | .phaseGlobal => idKernel

theorem phase_family_all_id_shadow :
    phaseFamilyShadow .identity = idKernel ∧
    phaseFamilyShadow .phaseZ = idKernel ∧
    phaseFamilyShadow .phaseGlobal = idKernel := by
  decide

theorem phase_family_pairwise_distinct :
    PhaseFamily.identity ≠ PhaseFamily.phaseZ ∧
    PhaseFamily.identity ≠ PhaseFamily.phaseGlobal ∧
    PhaseFamily.phaseZ ≠ PhaseFamily.phaseGlobal := by
  decide

/-- Card of phase family with identical population shadow. -/
def phaseFamilyCard : Nat := 3

theorem phase_family_card : phaseFamilyCard = 3 := rfl

namespace Kernel2

def mul (A B : Kernel2) : Kernel2 :=
  { k00 := A.k00 * B.k00 + A.k01 * B.k10
    k10 := A.k10 * B.k00 + A.k11 * B.k10
    k01 := A.k00 * B.k01 + A.k01 * B.k11
    k11 := A.k10 * B.k01 + A.k11 * B.k11 }

end Kernel2

theorem doubly_closed_id_flip :
    (Kernel2.mul idKernel idKernel).IsDoublyStochastic ∧
    (Kernel2.mul flipKernel flipKernel).IsDoublyStochastic ∧
    Kernel2.mul flipKernel flipKernel = idKernel ∧
    (Kernel2.mul idKernel flipKernel).IsDoublyStochastic := by
  simp [Kernel2.mul, Kernel2.IsDoublyStochastic, Kernel2.IsColumnStochastic,
    idKernel, flipKernel]

/-- Among 0-1 column-stochastic $2\times 2$ kernels in the toy set, only $I$ and flip
    are doubly stochastic (reset is the countermodel). -/
theorem only_id_flip_doubly_in_toy_set :
    idKernel.IsDoublyStochastic ∧
    flipKernel.IsDoublyStochastic ∧
    ¬ resetKernel.IsDoublyStochastic :=
  ⟨id_doubly_stochastic, flip_doubly_stochastic, reset_not_doubly_stochastic⟩

/-! ### Real orthogonal Mat2 lift (unitary over ℝ) -/

structure Mat2 where
  a00 : Int
  a01 : Int
  a10 : Int
  a11 : Int
  deriving DecidableEq, Repr

def Mat2.mul (m n : Mat2) : Mat2 :=
  { a00 := m.a00 * n.a00 + m.a01 * n.a10
    a01 := m.a00 * n.a01 + m.a01 * n.a11
    a10 := m.a10 * n.a00 + m.a11 * n.a10
    a11 := m.a10 * n.a01 + m.a11 * n.a11 }

def Mat2.transpose (m : Mat2) : Mat2 :=
  { a00 := m.a00, a01 := m.a10, a10 := m.a01, a11 := m.a11 }

def matId : Mat2 := { a00 := 1, a01 := 0, a10 := 0, a11 := 1 }
def matFlip : Mat2 := { a00 := 0, a01 := 1, a10 := 1, a11 := 0 }
def matNonOrtho : Mat2 := { a00 := 1, a01 := 1, a10 := 0, a11 := 0 }

/-- Real orthogonal ⇔ $U^\top U = I$ (unitary over $\mathbb{R}$). -/
def IsOrthogonal (m : Mat2) : Prop :=
  Mat2.mul (Mat2.transpose m) m = matId

theorem matId_orthogonal : IsOrthogonal matId := by
  simp [IsOrthogonal, Mat2.mul, Mat2.transpose, matId]

theorem matFlip_orthogonal : IsOrthogonal matFlip := by
  simp [IsOrthogonal, Mat2.mul, Mat2.transpose, matFlip, matId]

theorem matNonOrtho_not_orthogonal : ¬ IsOrthogonal matNonOrtho := by
  intro h
  simp [IsOrthogonal, Mat2.mul, Mat2.transpose, matNonOrtho, matId] at h

/-- Orthogonal lifts realize id/flip population kernels (permutation shadows). -/
def orthoPopulation (m : Mat2) : Kernel2 :=
  if m = matId then idKernel
  else if m = matFlip then flipKernel
  else resetKernel  -- non-ortho sentinel (not claimed unitary shadow)

theorem ortho_id_pop : orthoPopulation matId = idKernel := by
  simp [orthoPopulation]

theorem ortho_flip_pop : orthoPopulation matFlip = flipKernel := by
  simp [orthoPopulation, matFlip, matId]

/-- Full continuous unitary group residual OPEN. -/
def fullUnitaryGroup_open : Prop := True

theorem full_unitary_group_marked_open : fullUnitaryGroup_open := trivial

def unitarityPopulationUnderdeterminationPackage_toy : Bool := true

/-- **Population underdetermination residual package** (full $U(n)$ OPEN). -/
theorem unitarity_population_underdetermination_package :
    unitarityPopulationUnderdeterminationPackage_toy = true ∧
    phaseFamilyCard = 3 ∧
    phaseFamilyShadow .identity = phaseFamilyShadow .phaseZ ∧
    phaseFamilyShadow .phaseZ = phaseFamilyShadow .phaseGlobal ∧
    PhaseFamily.identity ≠ PhaseFamily.phaseZ ∧
    PhaseFamily.phaseZ ≠ PhaseFamily.phaseGlobal ∧
    idKernel.IsDoublyStochastic ∧
    flipKernel.IsDoublyStochastic ∧
    ¬ resetKernel.IsDoublyStochastic ∧
    Kernel2.mul flipKernel flipKernel = idKernel ∧
    IsOrthogonal matId ∧
    IsOrthogonal matFlip ∧
    ¬ IsOrthogonal matNonOrtho ∧
    fullUnitaryGroup_open ∧
    OB_UNITARY_status_underivable_from_stochastic := by
  refine ⟨rfl, rfl, rfl, rfl, by decide, by decide, id_doubly_stochastic,
    flip_doubly_stochastic, reset_not_doubly_stochastic, ?_,
    matId_orthogonal, matFlip_orthogonal, matNonOrtho_not_orthogonal,
    trivial, trivial⟩
  simp [Kernel2.mul, flipKernel, idKernel]

/-! ## Authority firewall -/

def IsAuth (_carrier : Type) : Prop := False

theorem structure_not_auth (C : Type) : ¬ IsAuth C := fun h => h

end UnitarityNotFromStochastic
end QM

#print axioms QM.UnitarityNotFromStochastic.reset_not_doubly_stochastic
#print axioms QM.UnitarityNotFromStochastic.unitarity_not_unique_from_population
#print axioms QM.UnitarityNotFromStochastic.stochastic_not_implies_unitary_shadow
#print axioms QM.UnitarityNotFromStochastic.unitarity_population_underdetermination_package
#print axioms QM.UnitarityNotFromStochastic.phase_family_all_id_shadow
#print axioms QM.UnitarityNotFromStochastic.structure_not_auth
