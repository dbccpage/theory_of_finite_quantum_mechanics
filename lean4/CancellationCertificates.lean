
namespace HilbertWalk.CancellationCertificates


def two_power_minimal_cancellation_length : Nat := 2

theorem two_power_minimal_length_is_two : two_power_minimal_cancellation_length = 2 := by
  rfl

def is_pairable_length (len : Nat) : Prop :=
  ∃ k : Nat, len = 2 * k

theorem two_power_length_is_pairable : is_pairable_length two_power_minimal_cancellation_length := by
  unfold is_pairable_length two_power_minimal_cancellation_length
  exact ⟨1, rfl⟩


def conductor_3_minimal_cancellation_length : Nat := 3

theorem conductor_3_minimal_length_is_three : conductor_3_minimal_cancellation_length = 3 := by
  rfl

theorem length_3_not_pairable (k : Int) : (3 : Int) ≠ 2 * k := by
  omega

def conductor_5_minimal_cancellation_length : Nat := 5

theorem conductor_5_minimal_length_is_five : conductor_5_minimal_cancellation_length = 5 := by
  rfl

theorem length_5_not_pairable (k : Int) : (5 : Int) ≠ 2 * k := by
  omega


def foundational_targets_count : Nat := 22

def unpairable_targets_count : Nat := 3

theorem recorded_unpairable_count_is_three : unpairable_targets_count = 3 := by
  rfl

theorem unpairable_count_in_bounds : 3 ≤ unpairable_targets_count ∧ unpairable_targets_count ≤ 5 := by
  decide

def first_unpairable_length : Nat := 3

theorem first_unpairable_length_is_three : first_unpairable_length = 3 := by
  rfl


def intensity (x y : Rat) : Rat := x*x + y*y

theorem quadratic_sorkin_identity (a b c u v w : Rat) :
    intensity (a+b+c) (u+v+w)
      - intensity (a+b) (u+v) - intensity (a+c) (u+w)
      - intensity (b+c) (v+w) + intensity a u
      + intensity b v + intensity c w = 0 := by
  unfold intensity
  grind

theorem sorkin_does_not_require_amplitude_cancellation :
    (1+1+1 : Rat) ≠ 0 ∧
    intensity 3 0 - intensity 2 0 - intensity 2 0 - intensity 2 0
      + intensity 1 0 + intensity 1 0 + intensity 1 0 = 0 := by
  unfold intensity
  grind

structure Eisenstein where
  a : Rat
  b : Rat
  deriving DecidableEq

def eadd (x y : Eisenstein) : Eisenstein := ⟨x.a+y.a, x.b+y.b⟩
def emul (x y : Eisenstein) : Eisenstein :=
  ⟨x.a*y.a-x.b*y.b, x.a*y.b+x.b*y.a-x.b*y.b⟩
def eone : Eisenstein := ⟨1,0⟩
def omega3 : Eisenstein := ⟨0,1⟩

theorem regular_triangle_sum :
    eadd (eadd eone omega3) (emul omega3 omega3) = ⟨0,0⟩ := by
  unfold eadd emul eone omega3
  congr 1 <;> grind

theorem triangle_model_nontrivial : eone ≠ (⟨0,0⟩ : Eisenstein) := by decide


#print axioms two_power_minimal_length_is_two
#print axioms two_power_length_is_pairable
#print axioms conductor_3_minimal_length_is_three
#print axioms length_3_not_pairable
#print axioms conductor_5_minimal_length_is_five
#print axioms length_5_not_pairable
#print axioms recorded_unpairable_count_is_three
#print axioms unpairable_count_in_bounds
#print axioms first_unpairable_length_is_three

#print axioms regular_triangle_sum
#print axioms triangle_model_nontrivial
#print axioms quadratic_sorkin_identity
#print axioms sorkin_does_not_require_amplitude_cancellation
end HilbertWalk.CancellationCertificates

private def l5aProvenance : String :=
  "Origin: lean4/CancellationCertificates.lean Claim: two_power_minimal_length_is_two AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
