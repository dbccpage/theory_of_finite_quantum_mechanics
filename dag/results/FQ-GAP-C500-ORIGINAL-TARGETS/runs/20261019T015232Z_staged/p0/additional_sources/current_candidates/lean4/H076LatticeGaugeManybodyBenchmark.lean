
namespace FableHilbertWalk20260819.H076

abbrev Matrix4 := List (List Int)

def entry (a : Matrix4) (i j : Nat) : Int := (a.getD i []).getD j 0

def mm (a b : Matrix4) : Matrix4 :=
  (List.range 4).map fun i => (List.range 4).map fun j =>
    ((List.range 4).map fun k => entry a i k * entry b k j).sum

def transpose (a : Matrix4) : Matrix4 :=
  (List.range 4).map fun i => (List.range 4).map fun j => entry a j i

def hMatrix : Matrix4 :=
  [[-1, -1, -1, 0], [-1, 1, 0, -1], [-1, 0, 1, -1], [0, -1, -1, -1]]

def changeBasis : Matrix4 :=
  [[1, 0, 1, 0], [0, 1, 0, 1], [0, 1, 0, -1], [1, 0, -1, 0]]

def blockMatrix : Matrix4 :=
  [[-1, -2, 0, 0], [-2, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]]

theorem tfim_block_identity : mm hMatrix changeBasis = mm changeBasis blockMatrix := by decide

theorem tfim_basis_gram_identity :
    mm (transpose changeBasis) changeBasis =
    [[2, 0, 0, 0], [0, 2, 0, 0], [0, 0, 2, 0], [0, 0, 0, 2]] := by decide

def hPolynomial : Matrix4 :=
  let h2 := mm hMatrix hMatrix
  let h4 := mm h2 h2
  (List.range 4).map fun i => (List.range 4).map fun j =>
    entry h4 i j - 6 * entry h2 i j + (if i = j then 5 else 0)

theorem tfim_matrix_polynomial_identity :
    hPolynomial = List.replicate 4 (List.replicate 4 0) := by decide

theorem old_tfim_eigenvalue_two_fails_polynomial : (2 : Int)^4 - 6*2^2 + 5 = -3 := by decide

def bitAt (label link : Nat) : Nat := (label / 2^link) % 2

def satisfiesGauss (label : Nat) : Bool :=
  (bitAt label 0 + bitAt label 3) % 2 == 0 &&
  (bitAt label 0 + bitAt label 1) % 2 == 0 &&
  (bitAt label 1 + bitAt label 2) % 2 == 0 &&
  (bitAt label 2 + bitAt label 3) % 2 == 0

def physicalLabels : List Nat := (List.range 16).filter satisfiesGauss

theorem physical_x_basis_census : physicalLabels = [0, 15] := by decide

theorem flux_preserves_enumerated_physical_labels :
    ((physicalLabels.map fun label => 15 - label).all physicalLabels.contains) = true := by decide

inductive ContinuumScalingObligation where
  | ThermodynamicVolumeLimit | GaugeTruncationLimit | UltravioletLatticeSpacingLimit
  deriving DecidableEq, Repr

theorem volume_ne_spacing_limit :
    ContinuumScalingObligation.ThermodynamicVolumeLimit ≠
    ContinuumScalingObligation.UltravioletLatticeSpacingLimit := by intro h; nomatch h

theorem truncation_ne_spacing_limit :
    ContinuumScalingObligation.GaugeTruncationLimit ≠
    ContinuumScalingObligation.UltravioletLatticeSpacingLimit := by intro h; nomatch h

#print axioms tfim_block_identity
#print axioms tfim_basis_gram_identity
#print axioms tfim_matrix_polynomial_identity
#print axioms old_tfim_eigenvalue_two_fails_polynomial
#print axioms physical_x_basis_census
#print axioms flux_preserves_enumerated_physical_labels
#print axioms volume_ne_spacing_limit
#print axioms truncation_ne_spacing_limit
end FableHilbertWalk20260819.H076

private def l5aProvenance : String :=
  "Origin: lean4/H076LatticeGaugeManybodyBenchmark.lean Claim: tfim_block_identity AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
