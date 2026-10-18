/-
  H053EverettForkingTree.lean
  AuthorityEffect: None.
  Citation: sealed-derivation-v1 (3100c4e)

  PR #205 scope correction; proof terms and historical names retained.
  Integer branch weights under a declared squared-norm rule, two Sorkin
  fixtures, and finite CHSH/parity arithmetic. Cross-branch entries vanish by
  definition; this is not a bipartite marginal non-signaling theorem. No
  repository quotient-fiber transport or derivation of the Born rule is proved.
-/

namespace FableHilbertWalk20260819.H053

/-- A branch amplitude in Z[i] (or scaled cyclotomic integers). -/
structure BranchAmp where
  re : Int
  im : Int
  deriving DecidableEq, Repr

/-- Born weight numerator |psi|^2 = re^2 + im^2. -/
def born_weight_numer (b : BranchAmp) : Int :=
  b.re * b.re + b.im * b.im

/-- Lemma: Integer square is non-negative. -/
theorem int_sq_nonneg (x : Int) : 0 ≤ x * x := by
  have h : 0 ≤ x ∨ 0 ≤ -x := by omega
  cases h with
  | inl hpos => exact Int.mul_nonneg hpos hpos
  | inr hneg =>
    have := Int.mul_nonneg hneg hneg
    rw [Int.neg_mul_neg x x] at this
    exact this

/-- Born weight is always non-negative. -/
theorem born_weight_nonneg (b : BranchAmp) : 0 ≤ born_weight_numer b := by
  dsimp [born_weight_numer]
  exact Int.add_nonneg (int_sq_nonneg b.re) (int_sq_nonneg b.im)

/-- Condition for a branch to be active (non-zero weight). -/
def is_active (b : BranchAmp) : Prop :=
  born_weight_numer b > 0

/-- Sorkin 3-slit interference identity:
    For any three amplitudes in Z^2, the third-order interference parameter
    I_3 = P(123) - P(12) - P(13) - P(23) + P(1) + P(2) + P(3)
    vanishes identically under the quadratic Born rule. -/
def sorkin_i3 (a1 a2 a3 : BranchAmp) : Int :=
  let p1 := born_weight_numer a1
  let p2 := born_weight_numer a2
  let p3 := born_weight_numer a3
  let p12 := born_weight_numer ⟨a1.re + a2.re, a1.im + a2.im⟩
  let p13 := born_weight_numer ⟨a1.re + a3.re, a1.im + a3.im⟩
  let p23 := born_weight_numer ⟨a2.re + a3.re, a2.im + a3.im⟩
  let p123 := born_weight_numer ⟨a1.re + a2.re + a3.re, a1.im + a2.im + a3.im⟩
  p123 - p12 - p13 - p23 + p1 + p2 + p3

/-- Sorkin 3-slit vanishing on standard slit fixture. -/
theorem sorkin_3slit_fixture_vanishes :
    sorkin_i3 ⟨1, 0⟩ ⟨0, 1⟩ ⟨1, 1⟩ = 0 := by
  decide

/-- Sorkin 3-slit vanishing on Pythagorean slit fixture. -/
theorem sorkin_3slit_pythagorean_vanishes :
    sorkin_i3 ⟨3, 4⟩ ⟨-4, 3⟩ ⟨5, 0⟩ = 0 := by
  decide

/-- Measure Decoupling for two branches:
    For weights w1, w2 > 0 with total W = w1 + w2,
    branch counting gives weight 1/2 each (scaled by W: W/2 = (w1+w2)/2).
    Born measure gives w1 and w2.
    They coincide (2*w1 = W and 2*w2 = W) iff w1 = w2. -/
theorem measure_decoupling_2branch (w1 w2 : Int) :
    (2 * w1 = w1 + w2 ∧ 2 * w2 = w1 + w2) ↔ w1 = w2 := by
  constructor
  · intro ⟨h1, _⟩
    omega
  · intro h
    constructor <;> omega

/-- Explicit Pythagorean non-uniform state: w1 = 9, w2 = 16.
    Branch counting assigns 1/2 each (scaled: 25/2).
    Born measure assigns 9/25 and 16/25.
    They strictly decouple: 2 * 9 != 9 + 16. -/
theorem pythagorean_measure_decoupled :
    (2 * (9 : Int) ≠ 9 + 16) ∧ (2 * (16 : Int) ≠ 9 + 16) := by
  decide

/-- Uniform state: w1 = w2 = 1 (e.g. 1/sqrt(2) superpositions).
    Branch counting and Born measure coincide. -/
theorem uniform_measure_coupled :
    (2 * (1 : Int) = 1 + 1) := by
  rfl

/-- CHSH Bell parameter for any non-contextual assignment in {-1, 1}^4
    satisfies |a0*b0 + a0*b1 - a1*b0 + a1*b1| <= 2. -/
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

/-- A branch label in a finite outcome index set. -/
structure BranchLabel where
  tag : Nat
  deriving DecidableEq, Repr

/-- Equivalence relation on state paths defining the Everett quotient fiber.
    Two path configurations belong to the same macro-branch fiber iff they share the same outcome tag. -/
def FiberEquiv (p1 p2 : BranchLabel) : Prop :=
  p1.tag = p2.tag

/-- An Everett quotient fiber element over outcome tag k. -/
structure QuotientFiber (tag : Nat) where
  amp : BranchAmp

/-- Forking coproduct: A superposition on two fibers is represented as a structured coproduct / direct sum of branches, preserving branch labels rather than collapsing into scalar addition. -/
structure BranchCoproduct where
  left : BranchAmp
  right : BranchAmp
  deriving DecidableEq, Repr

def coproduct_norm_sq (c : BranchCoproduct) : Int :=
  born_weight_numer c.left + born_weight_numer c.right

/-- Orthogonal branches with amplitudes 1 and -1 preserve both branches with norm-squared 2,
    preventing spurious destructive interference across distinct quotient fibers. -/
theorem coproduct_orthogonal_branches_preserve_norm :
    coproduct_norm_sq ⟨⟨1, 0⟩, ⟨-1, 0⟩⟩ = 2 := by
  rfl

/-- Scalar amplitude combination on a single branch. -/
def coproduct_fork (f1 f2 : BranchAmp) : BranchAmp :=
  ⟨f1.re + f2.re, f1.im + f2.im⟩

theorem coproduct_fork_components (f1 f2 : BranchAmp) :
    (coproduct_fork f1 f2).re = f1.re + f2.re ∧ (coproduct_fork f1 f2).im = f1.im + f2.im :=
  ⟨rfl, rfl⟩

/-- 2D integer vector for Pythagorean CHSH measurement bases. -/
structure Vec2Int where
  x : Int
  y : Int

def dot2 (u v : Vec2Int) : Int :=
  u.x * v.x + u.y * v.y

/-- Everett branch fiber transition amplitude. -/
def branch_transition (b1 b2 : BranchLabel) (u v : Vec2Int) : Int :=
  if b1 = b2 then dot2 u v else 0

/-- Non-signaling across Everett branches: distinct measurement branches have zero transition amplitude. -/
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

/-- Scaled quantum singlet correlation: E(a, b) = - a . b (scaled by 5). -/
def E_scaled (a b : Vec2Int) : Int := - dot2 a b

/-- Scaled CHSH correlation parameter:
    S = E(a1, b1) + E(a1, b2) + E(a2, b1) - E(a2, b2) = 4 + 3 + 3 - (-4) = 14. -/
def S_scaled : Int :=
  E_scaled a1_vec b1_vec + E_scaled a1_vec b2_vec + E_scaled a2_vec b1_vec - E_scaled a2_vec b2_vec

/-- Theorem: Quantum singlet on Pythagorean bases gives exact scaled CHSH value 14 (i.e. S = 14/5 = 2.8). -/
theorem chsh_pythagorean_quantum_value :
    S_scaled = 14 := by rfl

/-- Theorem: Scaled quantum CHSH value 14 strictly violates the classical bound of 10 (2 * 5). -/
theorem chsh_pythagorean_quantum_violates_classical :
    S_scaled > 10 := by decide

/-- Cabello 18-ray parity obstruction:
    9 tetrads require odd sum 9, but each ray appears twice (even sum 2k).
    No integer solution exists to 9 = 2k. -/
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
