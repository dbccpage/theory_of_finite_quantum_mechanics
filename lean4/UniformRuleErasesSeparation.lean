namespace UniformRuleErasesSeparation

/-- Two data. Index 0 is the first. -/
abbrev Datum := Fin 2

/-- Derivability of the unary plugging of datum `d` at form 0.
`rule0` is the uniform rule AdmitRuleAll on that form.
`inst0` is the one admitted instance on datum 0. -/
def derivable (rule0 inst0 : Bool) (d : Datum) : Bool :=
  rule0 || (inst0 && decide (d = 0))

/-- One bit of the profile: the unique unary hole-context, plugged at `d`. -/
def profileBit (rule0 inst0 : Bool) (d : Datum) : Bool :=
  derivable rule0 inst0 d

def classCount (rule0 inst0 : Bool) : Nat :=
  if profileBit rule0 inst0 0 == profileBit rule0 inst0 1 then 1 else 2

theorem two_data : ∀ d : Datum, d = 0 ∨ d = 1 := by
  decide

/-- Before the rule: the instance on datum 0 separates the two data. -/
theorem marked_separates :
    profileBit false true 0 = true
      ∧ profileBit false true 1 = false
      ∧ profileBit false true 0 ≠ profileBit false true 1
      ∧ classCount false true = 2 := by
  decide

/-- After AdmitRuleAll on form 0: both profile bits are true, so the class count is 1. -/
theorem rule_collapses :
    profileBit true true 0 = true
      ∧ profileBit true true 1 = true
      ∧ profileBit true true 0 = profileBit true true 1
      ∧ classCount true true = 1 := by
  decide

/-- The instance bit stays, and the rule bit is what changes. The class count falls from 2 to 1. -/
theorem uniform_rule_erases_separation :
    classCount false true = 2
      ∧ classCount true true = 1
      ∧ classCount false true ≠ classCount true true
      ∧ profileBit false true 0 = profileBit true true 0
      ∧ profileBit false true 1 ≠ profileBit true true 1 := by
  decide

#print axioms two_data
#print axioms marked_separates
#print axioms rule_collapses
#print axioms uniform_rule_erases_separation

end UniformRuleErasesSeparation
