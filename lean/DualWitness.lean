-- Quantum Dual Witnesses and Contextuality in Lean 4
-- AuthorityEffect: None

namespace DualWitness

/-- Discrete 2-coordinate witness with infinity-norm bounded coefficients in {-1, 0, 1}.
    This models an L-infinity bounded measurement observable on a 2-dimensional discrete carrier. -/
structure DiscreteWitness where
  w0 : Int
  w1 : Int
  h_bound0 : w0.natAbs ≤ 1
  h_bound1 : w1.natAbs ≤ 1

/-- Discrete state difference between two diagonal distributions on 2 states,
    represented as integer coordinate differences (d0, d1). -/
structure StateDifference where
  diff0 : Int
  diff1 : Int

/-- Trace norm (discrete L1 norm) on 2-state coordinate difference: |d0| + |d1|. -/
def trace_norm (d : StateDifference) : Nat :=
  d.diff0.natAbs + d.diff1.natAbs

/-- Dual pairing between a discrete witness w and a state difference d: w0 * d0 + w1 * d1. -/
def dual_pairing (w : DiscreteWitness) (d : StateDifference) : Int :=
  w.w0 * d.diff0 + w.w1 * d.diff1

/-- Dual witness pairing bound: the absolute value of the dual pairing is bounded
    above by the discrete trace norm (L1 norm) of the state difference. -/
theorem dual_witness_certifies_trace_distance (w : DiscreteWitness) (d : StateDifference) :
    (dual_pairing w d).natAbs ≤ trace_norm d := by
  dsimp [dual_pairing, trace_norm]
  have h_tri : (w.w0 * d.diff0 + w.w1 * d.diff1).natAbs ≤ (w.w0 * d.diff0).natAbs + (w.w1 * d.diff1).natAbs :=
    Int.natAbs_add_le (w.w0 * d.diff0) (w.w1 * d.diff1)
  rw [Int.natAbs_mul, Int.natAbs_mul] at h_tri
  have h0 : w.w0.natAbs * d.diff0.natAbs ≤ 1 * d.diff0.natAbs :=
    Nat.mul_le_mul_right d.diff0.natAbs w.h_bound0
  have h1 : w.w1.natAbs * d.diff1.natAbs ≤ 1 * d.diff1.natAbs :=
    Nat.mul_le_mul_right d.diff1.natAbs w.h_bound1
  rw [Nat.one_mul] at h0 h1
  have h_sum := Nat.add_le_add h0 h1
  exact Nat.le_trans h_tri h_sum

/-- Sign values in {-1, 1} for Mermin-Peres magic square combinatorial valuations. -/
inductive SignVal
  | Pos : SignVal  -- +1
  | Neg : SignVal  -- -1
  deriving DecidableEq, Repr

def mulSign : SignVal → SignVal → SignVal
  | SignVal.Pos, s => s
  | SignVal.Neg, SignVal.Pos => SignVal.Neg
  | SignVal.Neg, SignVal.Neg => SignVal.Pos

/-- A classical predetermined sign valuation assignment to the 9 cells of the 3x3 grid. -/
structure MagicSquareAssignment where
  m11 : SignVal
  m12 : SignVal
  m13 : SignVal
  m21 : SignVal
  m22 : SignVal
  m23 : SignVal
  m31 : SignVal
  m32 : SignVal
  m33 : SignVal

def row1_prod (s : MagicSquareAssignment) : SignVal := mulSign (mulSign s.m11 s.m12) s.m13
def row2_prod (s : MagicSquareAssignment) : SignVal := mulSign (mulSign s.m21 s.m22) s.m23
def row3_prod (s : MagicSquareAssignment) : SignVal := mulSign (mulSign s.m31 s.m32) s.m33

def col1_prod (s : MagicSquareAssignment) : SignVal := mulSign (mulSign s.m11 s.m21) s.m31
def col2_prod (s : MagicSquareAssignment) : SignVal := mulSign (mulSign s.m12 s.m22) s.m32
def col3_prod (s : MagicSquareAssignment) : SignVal := mulSign (mulSign s.m13 s.m23) s.m33

def total_row_prod (s : MagicSquareAssignment) : SignVal :=
  mulSign (mulSign (row1_prod s) (row2_prod s)) (row3_prod s)

def total_col_prod (s : MagicSquareAssignment) : SignVal :=
  mulSign (mulSign (col1_prod s) (col2_prod s)) (col3_prod s)

/-- Commutativity and associativity of sign multiplication forces the product of all row products
    to equal the product of all column products. -/
theorem total_row_eq_total_col (s : MagicSquareAssignment) :
    total_row_prod s = total_col_prod s := by
  obtain ⟨m11, m12, m13, m21, m22, m23, m31, m32, m33⟩ := s
  cases m11 <;> cases m12 <;> cases m13 <;>
  cases m21 <;> cases m22 <;> cases m23 <;>
  cases m31 <;> cases m32 <;> cases m33 <;>
  rfl

/-- Mermin-Peres Contextuality Parity Obstruction Theorem:
    No classical non-contextual value assignment can satisfy row products = (+1, +1, +1)
    and column products = (+1, +1, -1). This demonstrates the algebraic obstruction
    to non-contextual hidden variables on the discrete grid. -/
theorem mermin_peres_parity_obstruction (s : MagicSquareAssignment) :
    row1_prod s = SignVal.Pos →
    row2_prod s = SignVal.Pos →
    row3_prod s = SignVal.Pos →
    col1_prod s = SignVal.Pos →
    col2_prod s = SignVal.Pos →
    col3_prod s = SignVal.Neg →
    False := by
  intro hr1 hr2 hr3 hc1 hc2 hc3
  have h_row : total_row_prod s = SignVal.Pos := by
    dsimp [total_row_prod]
    rw [hr1, hr2, hr3]
    rfl
  have h_col : total_col_prod s = SignVal.Neg := by
    dsimp [total_col_prod]
    rw [hc1, hc2, hc3]
    rfl
  have h_eq := total_row_eq_total_col s
  rw [h_row, h_col] at h_eq
  cases h_eq

#print axioms dual_witness_certifies_trace_distance
#print axioms total_row_eq_total_col
#print axioms mermin_peres_parity_obstruction

end DualWitness
