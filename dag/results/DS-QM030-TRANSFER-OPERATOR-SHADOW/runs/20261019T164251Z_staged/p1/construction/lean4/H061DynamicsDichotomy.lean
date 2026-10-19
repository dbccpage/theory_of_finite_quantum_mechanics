
namespace FableHilbertWalk20260819.H061


def pythPower : Nat → Int × Int
  | 0 => (3, 4)
  | n + 1 =>
    let (a, b) := pythPower n
    (3 * a - 4 * b, 4 * a + 3 * b)


def HasPythResidue (p : Int × Int) : Prop :=
  ∃ qa qb : Int, p.1 = 5 * qa + 3 ∧ p.2 = 5 * qb + 4

theorem pythPower_zero_residue : HasPythResidue (pythPower 0) := by
  dsimp [pythPower, HasPythResidue]
  exact ⟨0, 0, by omega, by omega⟩

theorem pythPower_step_residue (p : Int × Int) (h : HasPythResidue p) :
    HasPythResidue (3 * p.1 - 4 * p.2, 4 * p.1 + 3 * p.2) := by
  rcases h with ⟨qa, qb, h1, h2⟩
  refine ⟨3 * qa - 4 * qb - 2, 4 * qa + 3 * qb + 4, ?_, ?_⟩
  · rw [h1, h2]; omega
  · rw [h1, h2]; omega

theorem pythPower_has_residue (n : Nat) : HasPythResidue (pythPower n) := by
  induction n with
  | zero => exact pythPower_zero_residue
  | succ m ih =>
    dsimp [pythPower]
    exact pythPower_step_residue (pythPower m) ih


theorem pythPower_im_ne_zero (n : Nat) : (pythPower n).2 ≠ 0 := by
  have h := pythPower_has_residue n
  rcases h with ⟨_, qb, _, h2⟩
  intro hzero
  have : 5 * qb + 4 = 0 := by rw [← h2, hzero]
  omega

def Matrix2x2IsIdentity (a b : Int) : Prop :=
  b = 0 ∧ a = 1

theorem pythagorean_rotation_power_ne_identity (n : Nat) :
    ¬ Matrix2x2IsIdentity (pythPower n).1 (pythPower n).2 := by
  intro ⟨hb, _⟩
  exact pythPower_im_ne_zero n hb

theorem pythagorean_rotation_order_infinite :
    ∀ n : Nat, (pythPower n).2 ≠ 0 := by
  intro n
  exact pythPower_im_ne_zero n


structure TorsionPhase where
  num : Int
  den : Nat
  den_pos : den > 0
  deriving Repr

structure GeneratorBranchSelection where
  branch_index : Int
  declared : Bool
  price : Nat

def periodic_generator_price : GeneratorBranchSelection :=
  ⟨0, true, 1⟩

def aperiodic_closure_price : GeneratorBranchSelection :=
  ⟨0, false, 0⟩

theorem periodic_sector_requires_declaration :
    periodic_generator_price.price = 1 := by
  rfl

theorem aperiodic_sector_closure_no_declaration :
    aperiodic_closure_price.price = 0 := by
  rfl

end FableHilbertWalk20260819.H061

#print axioms FableHilbertWalk20260819.H061.pythPower_zero_residue
#print axioms FableHilbertWalk20260819.H061.pythPower_step_residue
#print axioms FableHilbertWalk20260819.H061.pythPower_has_residue
#print axioms FableHilbertWalk20260819.H061.pythPower_im_ne_zero
#print axioms FableHilbertWalk20260819.H061.pythagorean_rotation_power_ne_identity
#print axioms FableHilbertWalk20260819.H061.pythagorean_rotation_order_infinite
#print axioms FableHilbertWalk20260819.H061.periodic_sector_requires_declaration
#print axioms FableHilbertWalk20260819.H061.aperiodic_sector_closure_no_declaration

private def l5aProvenance : String :=
  "Origin: lean4/H061DynamicsDichotomy.lean Claim: pythPower_zero_residue AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
