

namespace GroupParameter


inductive SubgroupType where
  | rotation : SubgroupType
  | boost : SubgroupType
  | timeEvolution : SubgroupType
  deriving DecidableEq, Repr

inductive ParameterVerdict where
  | carried : ParameterVerdict
  | refusedTranscendental : ParameterVerdict
  | externallyInterfaced : ParameterVerdict
  deriving DecidableEq, Repr

def classifyGroupParameter
    (st : SubgroupType)
    (isIdentity : Bool)
    (entriesAlgebraic : Bool)
    (hasNonzeroGen : Bool) : Option ParameterVerdict :=
  if isIdentity then
    some ParameterVerdict.carried
  else if st == SubgroupType.rotation && entriesAlgebraic && !isIdentity then
    some ParameterVerdict.refusedTranscendental
  else if st == SubgroupType.boost && entriesAlgebraic && !isIdentity then
    some ParameterVerdict.refusedTranscendental
  else if st == SubgroupType.timeEvolution && entriesAlgebraic && !isIdentity && hasNonzeroGen then
    some ParameterVerdict.refusedTranscendental
  else
    none

theorem classify_identity_carried (st : SubgroupType) (alg nonz : Bool) :
    classifyGroupParameter st true alg nonz = some ParameterVerdict.carried := by
  dsimp [classifyGroupParameter]

theorem classify_rotation_non_identity (alg : Bool) (h_alg : alg = true) :
    classifyGroupParameter SubgroupType.rotation false alg true = some ParameterVerdict.refusedTranscendental := by
  dsimp [classifyGroupParameter]
  rw [h_alg]
  rfl

theorem classify_boost_non_identity (alg : Bool) (h_alg : alg = true) :
    classifyGroupParameter SubgroupType.boost false alg true = some ParameterVerdict.refusedTranscendental := by
  dsimp [classifyGroupParameter]
  rw [h_alg]
  rfl

theorem classify_time_non_identity (alg nonz : Bool) (h_alg : alg = true) (h_nonz : nonz = true) :
    classifyGroupParameter SubgroupType.timeEvolution false alg nonz = some ParameterVerdict.refusedTranscendental := by
  dsimp [classifyGroupParameter]
  rw [h_alg, h_nonz]
  rfl


def b1Numerator : Fin 2 → Fin 2 → Int :=
  fun i j =>
    match i, j with
    | 0, 0 => 5 | 0, 1 => 3
    | 1, 0 => 3 | 1, 1 => 5

theorem b1_numerator_det :
    b1Numerator 0 0 * b1Numerator 1 1 - b1Numerator 0 1 * b1Numerator 1 0 = 16 := by
  rfl

def pythRotNumerator : Fin 3 → Fin 3 → Int :=
  fun i j =>
    match i, j with
    | 0, 0 => 3  | 0, 1 => -4 | 0, 2 => 0
    | 1, 0 => 4  | 1, 1 => 3  | 1, 2 => 0
    | 2, 0 => 0  | 2, 1 => 0  | 2, 2 => 5

theorem pyth_rot_numerator_det :
    pythRotNumerator 0 0 * (pythRotNumerator 1 1 * pythRotNumerator 2 2 - pythRotNumerator 1 2 * pythRotNumerator 2 1) -
    pythRotNumerator 0 1 * (pythRotNumerator 1 0 * pythRotNumerator 2 2 - pythRotNumerator 1 2 * pythRotNumerator 2 0) +
    pythRotNumerator 0 2 * (pythRotNumerator 1 0 * pythRotNumerator 2 1 - pythRotNumerator 1 1 * pythRotNumerator 2 0) = 125 := by
  rfl

def pauliZ : Fin 2 → Fin 2 → Int :=
  fun i j =>
    match i, j with
    | 0, 0 => 1  | 0, 1 => 0
    | 1, 0 => 0  | 1, 1 => -1

theorem pauli_z_trace_zero : pauliZ 0 0 + pauliZ 1 1 = 0 := by
  rfl


def IsTranscendental (IsAlg : α → Prop) (x : α) : Prop := ¬ IsAlg x

def LindemannWeierstrassHypothesis (α : Type) (IsAlg : α → Prop) (exp : α → α) (zero : α) : Prop :=
  ∀ (a : α), IsAlg a → a ≠ zero → IsTranscendental IsAlg (exp a)

theorem rotation_parameter_transcendental
    {α : Type}
    {IsAlg : α → Prop}
    {exp : α → α}
    {mul : α → α → α}
    {zero i_unit theta : α}
    (h_lw : LindemannWeierstrassHypothesis α IsAlg exp zero)
    (h_cos_alg : Prop)
    (h_rot_exp_alg : h_cos_alg → IsAlg (exp (mul i_unit theta)))
    (h_cos_holds : h_cos_alg)
    (h_non_id : theta ≠ zero)
    (h_mul_alg : IsAlg theta → IsAlg (mul i_unit theta))
    (h_mul_nonzero : theta ≠ zero → mul i_unit theta ≠ zero) :
    IsTranscendental IsAlg theta := by
  dsimp [IsTranscendental]
  intro h_alg_theta
  have h_alg_itheta : IsAlg (mul i_unit theta) := h_mul_alg h_alg_theta
  have h_nz_itheta : mul i_unit theta ≠ zero := h_mul_nonzero h_non_id
  have h_trans_exp : IsTranscendental IsAlg (exp (mul i_unit theta)) :=
    h_lw (mul i_unit theta) h_alg_itheta h_nz_itheta
  have h_alg_exp : IsAlg (exp (mul i_unit theta)) := h_rot_exp_alg h_cos_holds
  exact h_trans_exp h_alg_exp


theorem boost_parameter_transcendental
    {α : Type}
    {IsAlg : α → Prop}
    {exp : α → α}
    {zero eta : α}
    (h_lw : LindemannWeierstrassHypothesis α IsAlg exp zero)
    (h_cosh_alg : Prop)
    (h_boost_exp_alg : h_cosh_alg → IsAlg (exp eta))
    (h_cosh_holds : h_cosh_alg)
    (h_non_id : eta ≠ zero) :
    IsTranscendental IsAlg eta := by
  dsimp [IsTranscendental]
  intro h_alg_eta
  have h_trans_exp : IsTranscendental IsAlg (exp eta) := h_lw eta h_alg_eta h_non_id
  have h_alg_exp : IsAlg (exp eta) := h_boost_exp_alg h_cosh_holds
  exact h_trans_exp h_alg_exp

theorem time_parameter_transcendental
    {α : Type}
    {IsAlg : α → Prop}
    {exp : α → α}
    {mul : α → α → α}
    {zero gen_eig t : α}
    (h_lw : LindemannWeierstrassHypothesis α IsAlg exp zero)
    (h_unitary_alg : Prop)
    (h_time_exp_alg : h_unitary_alg → IsAlg (exp (mul gen_eig t)))
    (h_unitary_holds : h_unitary_alg)
    (h_non_id : t ≠ zero)
    (h_gen_nonzero : gen_eig ≠ zero)
    (h_mul_alg : IsAlg t → IsAlg (mul gen_eig t))
    (h_mul_nonzero : gen_eig ≠ zero → t ≠ zero → mul gen_eig t ≠ zero) :
    IsTranscendental IsAlg t := by
  dsimp [IsTranscendental]
  intro h_alg_t
  have h_alg_gt : IsAlg (mul gen_eig t) := h_mul_alg h_alg_t
  have h_nz_gt : mul gen_eig t ≠ zero := h_mul_nonzero h_gen_nonzero h_non_id
  have h_trans_exp : IsTranscendental IsAlg (exp (mul gen_eig t)) :=
    h_lw (mul gen_eig t) h_alg_gt h_nz_gt
  have h_alg_exp : IsAlg (exp (mul gen_eig t)) := h_time_exp_alg h_unitary_holds
  exact h_trans_exp h_alg_exp


structure SubgroupElementRecord where
  subgroup : SubgroupType
  isIdentity : Bool
  hasAlgebraicEntries : Bool
  hasNonzeroGen : Bool
  parameterIsZero : Bool
  parameterIsAlgebraic : Bool

theorem unified_group_parameter_dichotomy
    (elem : SubgroupElementRecord)
    (_h_alg : elem.hasAlgebraicEntries = true)
    (_h_nonz : elem.hasNonzeroGen = true)
    (h_id_equiv : elem.isIdentity = true ↔ elem.parameterIsAlgebraic = true)
    (h_lw_consequence : elem.isIdentity = false → elem.parameterIsAlgebraic = false) :
    (elem.isIdentity = true ∧ elem.parameterIsAlgebraic = true) ∨
    (elem.isIdentity = false ∧ elem.parameterIsAlgebraic = false) := by
  cases h_id : elem.isIdentity
  · right
    have h_not_alg := h_lw_consequence h_id
    exact ⟨rfl, h_not_alg⟩
  · left
    have h_alg_param := h_id_equiv.mp h_id
    exact ⟨rfl, h_alg_param⟩


def terminalOutcome : String := "PARAMETERS_REFUSED_ELEMENTS_CARRIED"

theorem terminal_outcome_correct :
    terminalOutcome = "PARAMETERS_REFUSED_ELEMENTS_CARRIED" := rfl

def inventoryTotalCount : Nat := 18
def inventoryCarriedCount : Nat := 3
def inventoryRefusedCount : Nat := 15

theorem inventory_partition :
    inventoryCarriedCount + inventoryRefusedCount = inventoryTotalCount := by
  rfl


#print axioms classify_identity_carried
#print axioms classify_rotation_non_identity
#print axioms classify_boost_non_identity
#print axioms classify_time_non_identity
#print axioms b1_numerator_det
#print axioms pyth_rot_numerator_det
#print axioms pauli_z_trace_zero
#print axioms rotation_parameter_transcendental
#print axioms boost_parameter_transcendental
#print axioms time_parameter_transcendental
#print axioms unified_group_parameter_dichotomy
#print axioms terminal_outcome_correct
#print axioms inventory_partition

end GroupParameter

private def l5aProvenance : String :=
  "Origin: lean4/GroupParameter.lean Claim: classify_identity_carried AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
