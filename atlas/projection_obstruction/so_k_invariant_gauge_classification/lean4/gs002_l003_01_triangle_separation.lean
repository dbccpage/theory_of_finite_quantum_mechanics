import Mathlib.Data.Rat.Defs
import Mathlib.Tactic.NormNum

/-!
# paper_gs002_l003_01_triangle_separation

Local gauge selection vs global coordinate separability.
-/

def triangleCycleX : ℚ := 1

def triangleCycleY : ℚ := 1

def coordinateSeparableTriangleCost : ℚ :=
  triangleCycleX + triangleCycleY

def euclideanTriangleSquaredCost : ℚ :=
  triangleCycleX ^ 2 + triangleCycleY ^ 2

theorem coordinate_separable_triangle_cost :
    coordinateSeparableTriangleCost = 2 := by
  norm_num [coordinateSeparableTriangleCost, triangleCycleX, triangleCycleY]

theorem euclidean_triangle_squared_cost :
    euclideanTriangleSquaredCost = 2 := by
  norm_num [euclideanTriangleSquaredCost, triangleCycleX, triangleCycleY]

theorem coordinate_separable_triangle_cost_squared :
    coordinateSeparableTriangleCost ^ 2 = 4 := by
  norm_num [coordinateSeparableTriangleCost, triangleCycleX, triangleCycleY]

theorem triangle_separation : (2 : ℚ)^2 ≠ 2 := by
  norm_num

theorem normalized_triangle_observer_separation :
    coordinateSeparableTriangleCost ^ 2 ≠ euclideanTriangleSquaredCost := by
  norm_num [coordinateSeparableTriangleCost, euclideanTriangleSquaredCost, triangleCycleX, triangleCycleY]

#print axioms coordinate_separable_triangle_cost
#print axioms euclidean_triangle_squared_cost
#print axioms coordinate_separable_triangle_cost_squared
#print axioms triangle_separation
#print axioms normalized_triangle_observer_separation
