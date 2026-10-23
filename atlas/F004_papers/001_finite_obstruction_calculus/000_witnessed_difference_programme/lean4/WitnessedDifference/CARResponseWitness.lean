import Std

/-! The actual reconstructed M=1, theta=1/10 response, scaled to integers.
    Python independently binds this table to the declared sixteen-state CAR
    construction. Lean verifies these submitted matrix witnesses, not that
    Python construction or an analytic infinite-M spectral extrapolation. -/
namespace WitnessedDifference.CARResponseWitness

def denominator : Int := 2825760

def scaledMatrix : List (List Int) := [
  [706440, 17240, 840, 17240, 706441, 17241, 841, 17241],
  [17240, 706440, 17240, 840, 17241, 706441, 17241, 841],
  [840, 17240, 706440, 17240, 841, 17241, 706441, 17241],
  [17240, 840, 17240, 706440, 17241, 841, 17241, 706441],
  [706441, 17241, 841, 17241, 706440, 17240, 840, 17240],
  [17241, 706441, 17241, 841, 17240, 706440, 17240, 840],
  [841, 17241, 706441, 17241, 840, 17240, 706440, 17240],
  [17241, 841, 17241, 706441, 17240, 840, 17240, 706440]
]

def basis : List (List Int) := [
  [1,1,1,1,1,1,1,1], [1,-1,1,-1,1,-1,1,-1],
  [1,1,-1,-1,1,1,-1,-1], [1,-1,-1,1,1,-1,-1,1],
  [1,1,1,1,-1,-1,-1,-1], [1,-1,1,-1,-1,1,-1,1],
  [1,1,-1,-1,-1,-1,1,1], [1,-1,-1,1,-1,1,1,-1]
]

def scaledEigenvalues : List Int := [1483524,1345600,1411200,1411200,-4,0,0,0]

def dot (x y : List Int) : Int := (x.zipWith (· * ·) y).sum

theorem eigenvector_equations :
    basis.map (fun v => scaledMatrix.map (fun row => dot row v)) =
      basis.zipWith (fun v lambda => v.map (lambda * ·)) scaledEigenvalues := by decide

theorem full_orthogonal_basis :
    basis.map (fun v => basis.map (fun w => dot v w)) =
      (List.range 8).map (fun i => (List.range 8).map (fun j => if i = j then (8 : Int) else 0)) := by
  decide

theorem negative_energy :
    dot [1,1,1,1,-1,-1,-1,-1]
      (scaledMatrix.map (fun row => dot row [1,1,1,1,-1,-1,-1,-1])) = -32 := by decide

theorem normalization_and_negative_value :
    0 < denominator ∧ denominator = 4*706440 := by decide

theorem actual_inertia_counts :
    (scaledEigenvalues.filter (fun x => x > 0)).length = 4 ∧
    (scaledEigenvalues.filter (fun x => x < 0)).length = 1 ∧
    (scaledEigenvalues.filter (fun x => x = 0)).length = 3 := by decide

end WitnessedDifference.CARResponseWitness

#print axioms WitnessedDifference.CARResponseWitness.eigenvector_equations
#print axioms WitnessedDifference.CARResponseWitness.full_orthogonal_basis
#print axioms WitnessedDifference.CARResponseWitness.negative_energy
#print axioms WitnessedDifference.CARResponseWitness.normalization_and_negative_value
#print axioms WitnessedDifference.CARResponseWitness.actual_inertia_counts
