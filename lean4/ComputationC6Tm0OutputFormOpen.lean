-- Narrowed slice of COMP-C6-TM0-OUTPUT-FORM-OPEN.
-- One blank-cell writer agrees with a constant evaluator.
-- The Mathlib TM0 output form of M0 stays open.

structure Cell where
  halted : Bool
  value : Nat

def writeHalt (v : Nat) (c : Cell) : Cell :=
  if c.halted then c else { halted := true, value := v }

def evalConst (v _n : Nat) : Nat :=
  v

theorem writeHaltFromBlank (v : Nat) :
    writeHalt v { halted := false, value := 0 } = { halted := true, value := v } := by
  rfl

theorem evalConstReturns (v n : Nat) : evalConst v n = v := by
  rfl

theorem constAgrees (v n : Nat) :
    (writeHalt v { halted := false, value := 0 }).value = evalConst v n := by
  rfl

#print axioms writeHaltFromBlank
#print axioms evalConstReturns
#print axioms constAgrees
