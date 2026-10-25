/-
Campaign narrowing of MAJ-OPEN-LINDBLAD-TRANSFER-ENVELOPE.

Integer envelope f(T) = 4 + T^3 compared with 3 T^2 at T = 1, 2 and 3.
Status stays OPEN. The Lindblad transfer envelope is not derived here.
-/

def f (T : Nat) : Nat := 4 + T * T * T

def comparison (T : Nat) : Nat := 3 * T * T

theorem envelope_at_one : f 1 = 5 ∧ comparison 1 = 3 ∧ f 1 > comparison 1 := by
  decide

theorem envelope_at_two : f 2 = 12 ∧ comparison 2 = 12 ∧ f 2 = comparison 2 := by
  decide

theorem envelope_at_three : f 3 = 31 ∧ comparison 3 = 27 ∧ f 3 > comparison 3 := by
  decide

theorem envelope_positive : f 2 = 12 ∧ 12 > 0 := by
  decide

theorem defect_zero_below_envelope : (0 : Nat) < f 2 := by
  decide

#print axioms envelope_at_one
#print axioms envelope_at_two
#print axioms envelope_at_three
#print axioms envelope_positive
#print axioms defect_zero_below_envelope
