namespace CampaignOpsRustReceiptsAndLimits

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

end CampaignOpsRustReceiptsAndLimits

#print axioms CampaignOpsRustReceiptsAndLimits.maxGlobal_eq_pow
#print axioms CampaignOpsRustReceiptsAndLimits.maxGlobal_eq_decimal
#print axioms CampaignOpsRustReceiptsAndLimits.maxLp_eq_pow
#print axioms CampaignOpsRustReceiptsAndLimits.maxLp_eq_decimal
#print axioms CampaignOpsRustReceiptsAndLimits.sixty_four_assignments_above
#print axioms CampaignOpsRustReceiptsAndLimits.twenty_one_sections_eq
#print axioms CampaignOpsRustReceiptsAndLimits.twenty_one_sections_above
#print axioms CampaignOpsRustReceiptsAndLimits.ten_rows
#print axioms CampaignOpsRustReceiptsAndLimits.ten_assignments
#print axioms CampaignOpsRustReceiptsAndLimits.ten_entries
#print axioms CampaignOpsRustReceiptsAndLimits.ten_assignments_inside
#print axioms CampaignOpsRustReceiptsAndLimits.ten_entries_inside
