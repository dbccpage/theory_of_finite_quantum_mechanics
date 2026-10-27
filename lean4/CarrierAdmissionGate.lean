/-
AUTHF-CARRIER-ADMISSION-GATE, one direct candidate slice.
Record admission is open. Direct candidate id AIT-DTM0 is partial,
with syntax and execution partial and universality open, and selected false.
No other candidate and no Rice-style claim.
-/

namespace CarrierAdmissionGate

def recordAdmission : String := "open"
def directId : String := "AIT-DTM0"
def directAdmission : String := "partial"
def syntaxStatus : String := "partial"
def executionStatus : String := "partial"
def universalityStatus : String := "open"
def directSelected : Bool := false

theorem directCeilings :
    recordAdmission = "open" ∧ directId = "AIT-DTM0" ∧
      directAdmission = "partial" ∧ syntaxStatus = "partial" ∧
      executionStatus = "partial" ∧ universalityStatus = "open" := by
  refine ⟨rfl, rfl, rfl, rfl, rfl, rfl⟩

theorem directNotSelected : directSelected = false := rfl

#print axioms directCeilings
#print axioms directNotSelected

end CarrierAdmissionGate
