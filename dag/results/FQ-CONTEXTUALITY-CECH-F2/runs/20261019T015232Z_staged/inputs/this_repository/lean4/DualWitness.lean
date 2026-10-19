

namespace DualWitness

structure DiscreteWitness where
  w0 : Int
  w1 : Int
  h_bound0 : w0.natAbs ≤ 1
  h_bound1 : w1.natAbs ≤ 1

structure StateDifference where
  diff0 : Int
  diff1 : Int

def trace_norm (d : StateDifference) : Nat :=
  d.diff0.natAbs + d.diff1.natAbs

def dual_pairing (w : DiscreteWitness) (d : StateDifference) : Int :=
  w.w0 * d.diff0 + w.w1 * d.diff1

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

inductive SignVal
  | Pos : SignVal
  | Neg : SignVal
  deriving DecidableEq, Repr

def mulSign : SignVal → SignVal → SignVal
  | SignVal.Pos, s => s
  | SignVal.Neg, SignVal.Pos => SignVal.Neg
  | SignVal.Neg, SignVal.Neg => SignVal.Pos

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

theorem total_row_eq_total_col (s : MagicSquareAssignment) :
    total_row_prod s = total_col_prod s := by
  obtain ⟨m11, m12, m13, m21, m22, m23, m31, m32, m33⟩ := s
  cases m11 <;> cases m12 <;> cases m13 <;>
  cases m21 <;> cases m22 <;> cases m23 <;>
  cases m31 <;> cases m32 <;> cases m33 <;>
  rfl

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

private def l5aProvenance : String :=
  "Origin: lean4/DualWitness.lean Claim: dual_witness_certifies_trace_distance AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
