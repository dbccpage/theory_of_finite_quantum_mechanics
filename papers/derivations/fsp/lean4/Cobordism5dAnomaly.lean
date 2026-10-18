


namespace Cobordism5dAnomaly

universe u


structure CobordismClass5D where
  postnikov_arf : Nat
  mixed_gravitational : Nat

def nu5 (c : CobordismClass5D) : Nat :=
  (c.postnikov_arf + c.mixed_gravitational) % 2

abbrev SignInt := Int

def mappingTorusHolonomy (nu : Nat) : SignInt :=
  if nu % 2 = 0 then 1 else -1

theorem anomaly_free_holonomy_is_positive (c : CobordismClass5D) (h : nu5 c = 0) :
    mappingTorusHolonomy (nu5 c) = 1 := by
  dsimp [mappingTorusHolonomy]
  rw [h]
  rfl

theorem gravitational_anomaly_holonomy_is_negative (c : CobordismClass5D) (h : nu5 c = 1) :
    mappingTorusHolonomy (nu5 c) = -1 := by
  dsimp [mappingTorusHolonomy]
  rw [h]
  rfl


def cobordismDefectMass (hol : SignInt) : Nat :=
  if hol = 1 then 0 else 2

theorem anomaly_free_nullifies_defect (c : CobordismClass5D) (h : nu5 c = 0) :
    cobordismDefectMass (mappingTorusHolonomy (nu5 c)) = 0 := by
  have h_pos : mappingTorusHolonomy (nu5 c) = 1 := anomaly_free_holonomy_is_positive c h
  dsimp [cobordismDefectMass]
  rw [h_pos]
  rfl

theorem gravitational_anomaly_obstructs_sign_cancellation (c : CobordismClass5D) (h : nu5 c = 1) :
    cobordismDefectMass (mappingTorusHolonomy (nu5 c)) = 2 := by
  have h_neg : mappingTorusHolonomy (nu5 c) = -1 := gravitational_anomaly_holonomy_is_negative c h
  dsimp [cobordismDefectMass]
  rw [h_neg]
  rfl

def mappingTorusDoubledTrace (nu : Nat) : SignInt :=
  mappingTorusHolonomy nu

theorem anomalous_doubled_trace_is_negative (c : CobordismClass5D) (h : nu5 c = 1) :
    mappingTorusDoubledTrace (nu5 c) = -1 := by
  dsimp [mappingTorusDoubledTrace]
  exact gravitational_anomaly_holonomy_is_negative c h

end Cobordism5dAnomaly
