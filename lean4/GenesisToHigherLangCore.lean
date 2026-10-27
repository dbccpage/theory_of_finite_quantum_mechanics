-- Narrowed slice of GTH-LANG-CORE.
-- One five-slot regime carrier. No syntax and no typing judgement.

structure Regime where
  data : Nat
  forms : Nat
  instances : Nat
  rules : Nat
  requirements : Nat
  deriving DecidableEq

def carrier : Regime :=
  { data := 1, forms := 0, instances := 0, rules := 0, requirements := 0 }

def withRule : Regime :=
  { carrier with rules := 1 }

def slotSum (r : Regime) : Nat :=
  r.data + r.forms + r.instances + r.rules + r.requirements

def reach (_v : Nat) : Nat := 0

theorem carrier_slots :
    carrier.data = 1 ∧ carrier.forms = 0 ∧ carrier.instances = 0
      ∧ carrier.rules = 0 ∧ carrier.requirements = 0 := by
  decide

theorem carrier_sum : slotSum carrier = 1 := by
  decide

theorem withRule_differs : withRule ≠ carrier := by
  decide

theorem withRule_slots :
    withRule.rules = 1 ∧ withRule.data = 1 ∧ withRule.forms = 0
      ∧ withRule.instances = 0 ∧ withRule.requirements = 0 := by
  decide

theorem reach_collapses : reach 0 = 0 ∧ reach 1 = 0 := by
  decide

#print axioms carrier_slots
#print axioms carrier_sum
#print axioms withRule_differs
#print axioms withRule_slots
#print axioms reach_collapses
