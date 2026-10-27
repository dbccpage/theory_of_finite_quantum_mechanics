

namespace HilbertWalk.DiscreteDynamicsStone


def toggle : Bool → Bool := fun b => !b

theorem no_bool_half_step :
    ¬ ∃ σ : Bool → Bool, ∀ b : Bool, σ (σ b) = toggle b := by
  intro h
  rcases h with ⟨σ, hσ⟩
  cases hf : σ false with
  | false =>
      have h1 := hσ false
      dsimp [toggle] at h1
      rw [hf, hf] at h1
      cases h1
  | true =>
      cases ht : σ true with
      | false =>
          have h1 := hσ false
          dsimp [toggle] at h1
          rw [hf, ht] at h1
          cases h1
      | true =>
          have h1 := hσ true
          dsimp [toggle] at h1
          rw [ht, ht] at h1
          cases h1


structure GaussInt where
  re : Int
  im : Int
  deriving DecidableEq, Repr

def gadd (a b : GaussInt) : GaussInt :=
  ⟨a.re + b.re, a.im + b.im⟩

def gmul (a b : GaussInt) : GaussInt :=
  ⟨a.re * b.re - a.im * b.im, a.re * b.im + a.im * b.re⟩

structure Mat2G where
  m00 : GaussInt
  m01 : GaussInt
  m10 : GaussInt
  m11 : GaussInt
  deriving DecidableEq, Repr

def mat2g_mul (A B : Mat2G) : Mat2G := {
  m00 := gadd (gmul A.m00 B.m00) (gmul A.m01 B.m10)
  m01 := gadd (gmul A.m00 B.m01) (gmul A.m01 B.m11)
  m10 := gadd (gmul A.m10 B.m00) (gmul A.m11 B.m10)
  m11 := gadd (gmul A.m10 B.m01) (gmul A.m11 B.m11)
}

def M_scaled : Mat2G := {
  m00 := ⟨1, 1⟩,  m01 := ⟨1, -1⟩,
  m10 := ⟨1, -1⟩, m11 := ⟨1, 1⟩
}

def four_X : Mat2G := {
  m00 := ⟨0, 0⟩, m01 := ⟨4, 0⟩,
  m10 := ⟨4, 0⟩, m11 := ⟨0, 0⟩
}

theorem sqrt_toggle_scaled_squares :
    mat2g_mul M_scaled M_scaled = four_X := by
  decide

def neg_M_scaled : Mat2G := {
  m00 := ⟨-1, -1⟩, m01 := ⟨-1, 1⟩,
  m10 := ⟨-1, 1⟩,  m11 := ⟨-1, -1⟩
}

theorem interpolant_not_unique :
    mat2g_mul neg_M_scaled neg_M_scaled = four_X ∧
    neg_M_scaled ≠ M_scaled := by
  decide


theorem cayley_norm_identity (t : Int) :
    (1 - t * t) * (1 - t * t) + 4 * (t * t) = (1 + t * t) * (1 + t * t) := by
  have h_exp_l : (1 - t * t) * (1 - t * t) + 4 * (t * t) =
      1 - 2 * (t * t) + (t * t) * (t * t) + 4 * (t * t) := by
    repeat rw [Int.sub_mul]
    repeat rw [Int.mul_sub]
    repeat rw [Int.one_mul]
    repeat rw [Int.mul_one]
    omega
  have h_exp_r : (1 + t * t) * (1 + t * t) =
      1 + 2 * (t * t) + (t * t) * (t * t) := by
    repeat rw [Int.add_mul]
    repeat rw [Int.mul_add]
    repeat rw [Int.one_mul]
    repeat rw [Int.mul_one]
    omega
  rw [h_exp_l, h_exp_r]
  omega


structure GeneratorBranch where
  branch_index : Int
  deriving DecidableEq, Repr

theorem branch_ambiguity_distinct (k1 k2 : Int) (h : k1 ≠ k2) :
    GeneratorBranch.mk k1 ≠ GeneratorBranch.mk k2 := by
  intro heq
  injection heq with h_idx
  exact h h_idx

def generator_energy_branch (k : Int) : Int :=
  2 * k + 1

theorem generator_energies_distinct (k1 k2 : Int) (h : k1 ≠ k2) :
    generator_energy_branch k1 ≠ generator_energy_branch k2 := by
  dsimp [generator_energy_branch]
  omega

theorem stone_discrete_generator_ambiguity (k1 k2 : Int) (h : k1 ≠ k2) :
    GeneratorBranch.mk (generator_energy_branch k1) ≠ GeneratorBranch.mk (generator_energy_branch k2) := by
  have h_ne := generator_energies_distinct k1 k2 h
  exact branch_ambiguity_distinct (generator_energy_branch k1) (generator_energy_branch k2) h_ne


inductive StoneCosting where
  | priced_continuum_interface (rationale : String)
  deriving Repr, DecidableEq

def resolution_gap_008 : StoneCosting :=
  StoneCosting.priced_continuum_interface
    "Requires strongly continuous one-parameter group U(t) and infinite-branch logarithmic resolution"

structure StoneContinuumPriceReceipt where
  discrete_generator_ambiguity : ∀ k1 k2 : Int, k1 ≠ k2 → generator_energy_branch k1 ≠ generator_energy_branch k2
  resolution : StoneCosting

def stone_interface_receipt : StoneContinuumPriceReceipt := {
  discrete_generator_ambiguity := generator_energies_distinct,
  resolution := resolution_gap_008
}

theorem stone_continuum_interface_priced :
    stone_interface_receipt.resolution = resolution_gap_008 ∧
    generator_energy_branch 0 ≠ generator_energy_branch 1 := by
  refine ⟨rfl, stone_interface_receipt.discrete_generator_ambiguity 0 1 (by decide)⟩

#print axioms no_bool_half_step
#print axioms sqrt_toggle_scaled_squares
#print axioms interpolant_not_unique
#print axioms cayley_norm_identity
#print axioms branch_ambiguity_distinct
#print axioms generator_energies_distinct
#print axioms stone_discrete_generator_ambiguity
#print axioms stone_continuum_interface_priced

end HilbertWalk.DiscreteDynamicsStone

private def l5aProvenance : String :=
  "Origin: lean4/DiscreteDynamicsStone.lean Claim: no_bool_half_step AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
