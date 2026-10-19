
namespace InterferenceNonL1Resource

structure DeviceModel where
  s1_race : Bool
  s2_floor : Bool
  s3_reachability : Bool
  s4_advantage : Bool
deriving DecidableEq, Repr

def satisfies_Set_S (d : DeviceModel) : Bool :=
  d.s1_race && d.s2_floor && d.s3_reachability && d.s4_advantage

def is_useful_quantum_computer (d : DeviceModel) : Bool :=
  satisfies_Set_S d

theorem useful_qc_iff_set_S (d : DeviceModel) :
    is_useful_quantum_computer d = true ↔ satisfies_Set_S d = true := by
  rfl

def eval_set_s (lambda_gen mu_rep eps_mix p_floor : Int) (in_cone has_non_l1 : Bool) : DeviceModel :=
  { s1_race := decide (lambda_gen - mu_rep - eps_mix ≤ 0)
  , s2_floor := decide (0 < p_floor)
  , s3_reachability := in_cone
  , s4_advantage := has_non_l1
  }

def canonical_model : DeviceModel :=
  eval_set_s 10 15 0 1 true true

theorem setS_satisfiable : satisfies_Set_S canonical_model = true := by
  decide

theorem s1_necessary (d : DeviceModel) (h : d.s1_race = false) :
    satisfies_Set_S d = false := by
  dsimp [satisfies_Set_S]
  rw [h]
  rfl

theorem s2_necessary (d : DeviceModel) (h : d.s2_floor = false) :
    satisfies_Set_S d = false := by
  dsimp [satisfies_Set_S]
  rw [h]
  cases d.s1_race <;> rfl

theorem s3_necessary (d : DeviceModel) (h : d.s3_reachability = false) :
    satisfies_Set_S d = false := by
  dsimp [satisfies_Set_S]
  rw [h]
  cases d.s1_race <;> cases d.s2_floor <;> rfl

theorem s4_necessary (d : DeviceModel) (h : d.s4_advantage = false) :
    satisfies_Set_S d = false := by
  dsimp [satisfies_Set_S]
  rw [h]
  cases d.s1_race <;> cases d.s2_floor <;> cases d.s3_reachability <;> rfl


def witness_drop_s1 : DeviceModel := eval_set_s 20 10 0 1 true true
def witness_drop_s2 : DeviceModel := eval_set_s 10 15 0 0 true true
def witness_drop_s3 : DeviceModel := eval_set_s 10 15 0 1 false true
def witness_drop_s4 : DeviceModel := eval_set_s 10 15 0 1 true false

theorem drop_s1_witness_audit :
    witness_drop_s1.s1_race = false ∧
    witness_drop_s1.s2_floor = true ∧
    witness_drop_s1.s3_reachability = true ∧
    witness_drop_s1.s4_advantage = true ∧
    satisfies_Set_S witness_drop_s1 = false := by
  decide

theorem drop_s2_witness_audit :
    witness_drop_s2.s1_race = true ∧
    witness_drop_s2.s2_floor = false ∧
    witness_drop_s2.s3_reachability = true ∧
    witness_drop_s2.s4_advantage = true ∧
    satisfies_Set_S witness_drop_s2 = false := by
  decide

theorem drop_s3_witness_audit :
    witness_drop_s3.s1_race = true ∧
    witness_drop_s3.s2_floor = true ∧
    witness_drop_s3.s3_reachability = false ∧
    witness_drop_s3.s4_advantage = true ∧
    satisfies_Set_S witness_drop_s3 = false := by
  decide

theorem drop_s4_witness_audit :
    witness_drop_s4.s1_race = true ∧
    witness_drop_s4.s2_floor = true ∧
    witness_drop_s4.s3_reachability = true ∧
    witness_drop_s4.s4_advantage = false ∧
    satisfies_Set_S witness_drop_s4 = false := by
  decide

end InterferenceNonL1Resource

private def l5aProvenance : String :=
  "Origin: lean4/BuildabilitySetS.lean Claim: useful_qc_iff_set_S AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
