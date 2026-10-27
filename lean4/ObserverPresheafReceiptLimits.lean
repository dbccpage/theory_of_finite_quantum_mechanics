namespace ObserverPresheafReceiptLimits

def maxGlobal : Nat := 2 ^ 20

def maxLp : Nat := 2 ^ 22

theorem maxGlobal_eq_pow : maxGlobal = 2 ^ 20 := rfl

theorem maxGlobal_eq_decimal : maxGlobal = 1048576 := by decide

theorem maxLp_eq_pow : maxLp = 2 ^ 22 := rfl

theorem maxLp_eq_decimal : maxLp = 4194304 := by decide

theorem sixty_four_assignments_above : 2 ^ 64 > maxGlobal := by decide

theorem twenty_one_sections_eq : 2 ^ 21 = 2097152 := by decide

theorem twenty_one_sections_above : 2 ^ 21 > maxGlobal := by decide

theorem ten_rows : 10 * 2 = 20 := rfl

theorem ten_assignments : 2 ^ 10 = 1024 := rfl

theorem ten_entries : 20 * 1024 = 20480 := rfl

theorem ten_assignments_inside : 2 ^ 10 < maxGlobal := by decide

theorem ten_entries_inside : 20 * 1024 < maxLp := by decide

end ObserverPresheafReceiptLimits

#print axioms ObserverPresheafReceiptLimits.maxGlobal_eq_pow
#print axioms ObserverPresheafReceiptLimits.maxGlobal_eq_decimal
#print axioms ObserverPresheafReceiptLimits.maxLp_eq_pow
#print axioms ObserverPresheafReceiptLimits.maxLp_eq_decimal
#print axioms ObserverPresheafReceiptLimits.sixty_four_assignments_above
#print axioms ObserverPresheafReceiptLimits.twenty_one_sections_eq
#print axioms ObserverPresheafReceiptLimits.twenty_one_sections_above
#print axioms ObserverPresheafReceiptLimits.ten_rows
#print axioms ObserverPresheafReceiptLimits.ten_assignments
#print axioms ObserverPresheafReceiptLimits.ten_entries
#print axioms ObserverPresheafReceiptLimits.ten_assignments_inside
#print axioms ObserverPresheafReceiptLimits.ten_entries_inside
