/-!
Numeral slice of FQ-GAP-CUSTODY-AND-RECEIPTS.
AuthorityEffect: None.
The module has no import. It compares the numerals named by the custody
statement. It does not recount a ledger, a file tree, or a dependency report.
-/

namespace CampaignFqGapCustodyAndReceipts

theorem untypedRowNumeralGap : (48 - 24 : Nat) = 24 := rfl

theorem coverageNumeralRemainder : (53 - 22 : Nat) = 31 := rfl

theorem coverageIsProper : 22 < 53 := by decide

#print axioms untypedRowNumeralGap
#print axioms coverageNumeralRemainder
#print axioms coverageIsProper

end CampaignFqGapCustodyAndReceipts
