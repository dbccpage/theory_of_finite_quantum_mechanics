-- Narrowed slice of FQ-PRIM-TO-QM-SELECTION-OPEN.
-- Amplitudes 1 and 2, two positive normalized monomial rules.
-- No primitive-difference selector and no continuum readout.

def amp0 : Nat := 1
def amp1 : Nat := 2

def quad0 : Nat := amp0 * amp0
def quad1 : Nat := amp1 * amp1
def quadDen : Nat := quad0 + quad1

def quart0 : Nat := quad0 * quad0
def quart1 : Nat := quad1 * quad1
def quartDen : Nat := quart0 + quart1

theorem quad_weights :
    quad0 = 1 ∧ quad1 = 4 ∧ quadDen = 5 ∧
      quad0 + quad1 = quadDen ∧ 0 < quad0 ∧ 0 < quad1 := by
  decide

theorem quart_weights :
    quart0 = 1 ∧ quart1 = 16 ∧ quartDen = 17 ∧
      quart0 + quart1 = quartDen ∧ 0 < quart0 ∧ 0 < quart1 := by
  decide

theorem normalized_first_weights_differ :
    quad0 * quartDen = 17 ∧ quart0 * quadDen = 5 ∧
      quad0 * quartDen ≠ quart0 * quadDen := by
  decide

theorem symmetric_agreement :
    (1 * 1 = 1 ∧ 1 * 1 = 1 ∧ 1 + 1 = 2) ∧
      ((1 * 1) * (1 * 1) = 1 ∧ (1 * 1) * (1 * 1) = 1 ∧ 1 + 1 = 2) := by
  decide

#print axioms quad_weights
#print axioms quart_weights
#print axioms normalized_first_weights_differ
#print axioms symmetric_agreement
