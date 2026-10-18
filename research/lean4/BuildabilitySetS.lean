/-
  BuildabilitySetS.lean
  Necessary and sufficient Set S buildability conditions for Paper 061.
  AuthorityEffect: None
-/

namespace InterferenceNonL1Resource

/--
  Architecture profile of a discrete quantum computational apparatus.
  - s1_race: Generation rate does not outpace repair and mixing: λ_gen - μ_rep - ε_mix ≤ 0
  - s2_floor: Strictly positive floor detection probability: p_floor > 0
  - s3_reachability: State lies within causal light-cone / reachability envelope
  - s4_advantage: System hosts genuine non-L1 interference deficit resource
-/
structure DeviceModel where
  s1_race : Bool
  s2_floor : Bool
  s3_reachability : Bool
  s4_advantage : Bool
deriving DecidableEq, Repr

/-- Evaluates whether an architecture satisfies all 4 Set S criteria -/
def satisfies_Set_S (d : DeviceModel) : Bool :=
  d.s1_race && d.s2_floor && d.s3_reachability && d.s4_advantage

/--
  Criterion for useful discrete quantum computation:
  Non-classical speedup / advantage is supported iff all four physical conditions hold.
-/
def is_useful_quantum_computer (d : DeviceModel) : Bool :=
  satisfies_Set_S d

/-- THEOREM B1: Useful discrete quantum computation holds if and only if Set S is fully satisfied -/
theorem useful_qc_iff_set_S (d : DeviceModel) :
    is_useful_quantum_computer d = true ↔ satisfies_Set_S d = true := by
  rfl

/-- Concrete evaluation function matching discrete integer parameters -/
def eval_set_s (lambda_gen mu_rep eps_mix p_floor : Int) (in_cone has_non_l1 : Bool) : DeviceModel :=
  { s1_race := decide (lambda_gen - mu_rep - eps_mix ≤ 0)
  , s2_floor := decide (0 < p_floor)
  , s3_reachability := in_cone
  , s4_advantage := has_non_l1
  }

/-- THEOREM B3: Set S is satisfiable (witnessed by canonical physical parameters) -/
def canonical_model : DeviceModel :=
  eval_set_s 10 15 0 1 true true

theorem setS_satisfiable : satisfies_Set_S canonical_model = true := by
  decide

/-- THEOREM B2: Each of the 4 conditions in Set S is independently necessary -/
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

/-! ### The Four Drop-One Necessity Witnesses -/

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
