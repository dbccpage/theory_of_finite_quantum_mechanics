

namespace FableHilbertWalk20260819.H053

structure BranchAmp where
  re : Int
  im : Int
  deriving DecidableEq, Repr

def born_weight_numer (b : BranchAmp) : Int :=
  b.re * b.re + b.im * b.im

theorem int_sq_nonneg (x : Int) : 0 ≤ x * x := by
  have h : 0 ≤ x ∨ 0 ≤ -x := by omega
  cases h with
  | inl hpos => exact Int.mul_nonneg hpos hpos
  | inr hneg =>
    have := Int.mul_nonneg hneg hneg
    rw [Int.neg_mul_neg x x] at this
    exact this

theorem born_weight_nonneg (b : BranchAmp) : 0 ≤ born_weight_numer b := by
  dsimp [born_weight_numer]
  exact Int.add_nonneg (int_sq_nonneg b.re) (int_sq_nonneg b.im)

def is_active (b : BranchAmp) : Prop :=
  born_weight_numer b > 0

def sorkin_i3 (a1 a2 a3 : BranchAmp) : Int :=
  let p1 := born_weight_numer a1
  let p2 := born_weight_numer a2
  let p3 := born_weight_numer a3
  let p12 := born_weight_numer ⟨a1.re + a2.re, a1.im + a2.im⟩
  let p13 := born_weight_numer ⟨a1.re + a3.re, a1.im + a3.im⟩
  let p23 := born_weight_numer ⟨a2.re + a3.re, a2.im + a3.im⟩
  let p123 := born_weight_numer ⟨a1.re + a2.re + a3.re, a1.im + a2.im + a3.im⟩
  p123 - p12 - p13 - p23 + p1 + p2 + p3

theorem sorkin_3slit_fixture_vanishes :
    sorkin_i3 ⟨1, 0⟩ ⟨0, 1⟩ ⟨1, 1⟩ = 0 := by
  decide

theorem sorkin_3slit_pythagorean_vanishes :
    sorkin_i3 ⟨3, 4⟩ ⟨-4, 3⟩ ⟨5, 0⟩ = 0 := by
  decide

theorem measure_decoupling_2branch (w1 w2 : Int) :
    (2 * w1 = w1 + w2 ∧ 2 * w2 = w1 + w2) ↔ w1 = w2 := by
  constructor
  · intro ⟨h1, _⟩
    omega
  · intro h
    constructor <;> omega

theorem pythagorean_measure_decoupled :
    (2 * (9 : Int) ≠ 9 + 16) ∧ (2 * (16 : Int) ≠ 9 + 16) := by
  decide

theorem uniform_measure_coupled :
    (2 * (1 : Int) = 1 + 1) := by
  rfl

theorem chsh_classical_bound (a0 a1 b0 b1 : Int)
    (ha0 : a0 = 1 ∨ a0 = -1) (ha1 : a1 = 1 ∨ a1 = -1)
    (hb0 : b0 = 1 ∨ b0 = -1) (hb1 : b1 = 1 ∨ b1 = -1) :
    let S := a0 * b0 + a0 * b1 - a1 * b0 + a1 * b1
    S = 2 ∨ S = -2 := by
  dsimp
  rcases ha0 with rfl | rfl <;>
  rcases ha1 with rfl | rfl <;>
  rcases hb0 with rfl | rfl <;>
  rcases hb1 with rfl | rfl <;>
  decide

structure BranchLabel where
  tag : Nat
  deriving DecidableEq, Repr

def FiberEquiv (p1 p2 : BranchLabel) : Prop :=
  p1.tag = p2.tag

structure QuotientFiber (tag : Nat) where
  amp : BranchAmp

structure BranchCoproduct where
  left : BranchAmp
  right : BranchAmp
  deriving DecidableEq, Repr

def coproduct_norm_sq (c : BranchCoproduct) : Int :=
  born_weight_numer c.left + born_weight_numer c.right

theorem coproduct_orthogonal_branches_preserve_norm :
    coproduct_norm_sq ⟨⟨1, 0⟩, ⟨-1, 0⟩⟩ = 2 := by
  rfl

def coproduct_fork (f1 f2 : BranchAmp) : BranchAmp :=
  ⟨f1.re + f2.re, f1.im + f2.im⟩

theorem coproduct_fork_components (f1 f2 : BranchAmp) :
    (coproduct_fork f1 f2).re = f1.re + f2.re ∧ (coproduct_fork f1 f2).im = f1.im + f2.im :=
  ⟨rfl, rfl⟩

structure Vec2Int where
  x : Int
  y : Int

def dot2 (u v : Vec2Int) : Int :=
  u.x * v.x + u.y * v.y

def branch_transition (b1 b2 : BranchLabel) (u v : Vec2Int) : Int :=
  if b1 = b2 then dot2 u v else 0

theorem everett_branch_non_signaling (b1 b2 : BranchLabel) (h : b1 ≠ b2) (u v : Vec2Int) :
    branch_transition b1 b2 u v = 0 := by
  dsimp [branch_transition]
  split
  · rename_i heq; contradiction
  · rfl

def a1_vec : Vec2Int := ⟨0, 1⟩
def a2_vec : Vec2Int := ⟨1, 0⟩
def b1_vec : Vec2Int := ⟨-3, -4⟩
def b2_vec : Vec2Int := ⟨4, -3⟩

def E_scaled (a b : Vec2Int) : Int := - dot2 a b

def S_scaled : Int :=
  E_scaled a1_vec b1_vec + E_scaled a1_vec b2_vec + E_scaled a2_vec b1_vec - E_scaled a2_vec b2_vec

theorem chsh_pythagorean_quantum_value :
    S_scaled = 14 := by rfl

theorem chsh_pythagorean_quantum_violates_classical :
    S_scaled > 10 := by decide

theorem cabello_parity_obstruction (k : Int) :
    (9 : Int) ≠ 2 * k := by
  omega

#print axioms int_sq_nonneg
#print axioms born_weight_nonneg
#print axioms coproduct_orthogonal_branches_preserve_norm
#print axioms coproduct_fork_components
#print axioms sorkin_3slit_fixture_vanishes
#print axioms sorkin_3slit_pythagorean_vanishes
#print axioms measure_decoupling_2branch
#print axioms pythagorean_measure_decoupled
#print axioms uniform_measure_coupled
#print axioms chsh_classical_bound
#print axioms chsh_pythagorean_quantum_value
#print axioms chsh_pythagorean_quantum_violates_classical
#print axioms everett_branch_non_signaling
#print axioms cabello_parity_obstruction

end FableHilbertWalk20260819.H053

private def l5aProvenance : String :=
  "Origin: lean4/H053EverettForkingTree.lean Claim: int_sq_nonneg AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
