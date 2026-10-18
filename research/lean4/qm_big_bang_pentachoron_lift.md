import «000_000_big_bang_100_big_bang_dda_ascent»
import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Fin.VecNotation

/-!
# The 4-simplex C3-to-C4 rung is detect-then-repair

The boundary of a 4-simplex has ten triangles and five tetrahedral facets. A
one-facet `F2` 3-cochain is not a triangle coboundary. On the hollow boundary
there is no declared 4-cell evaluator. Declaring the 4-simplex exposes nonzero
`d3` without changing `im d2`. A separate cost-one facet update reaches an
exact and closed residual.

This finite cochain witness occupies the algebraic `C3 -> C4` slot. It does not
supply a spacetime dimension, a 3-form gauge field, M-theory flux, or dynamics.
-/

namespace QM
namespace BigBangPentachoronLift

-- The largest closed decision procedure enumerates 2^10 triangle cochains.
set_option maxRecDepth 100000

abbrev F2 := ZMod 2

/-- Triangle 2-cochains on `012,013,014,023,024,034,123,124,134,234`. -/
abbrev C2 := Fin 10 -> F2

/-- Tetrahedral 3-cochains on `0123,0124,0134,0234,1234`. -/
abbrev C3 := Fin 5 -> F2

/-- One 4-simplex evaluator. -/
abbrev C4 := F2

/-- Triangle-to-tetrahedron coboundary on the boundary of a 4-simplex. -/
def d2 (x : C2) : C3 :=
  ![x 0 + x 1 + x 3 + x 6,
    x 0 + x 2 + x 4 + x 7,
    x 1 + x 2 + x 5 + x 8,
    x 3 + x 4 + x 5 + x 9,
    x 6 + x 7 + x 8 + x 9]

/-- Tetrahedron-to-4-cell coboundary. -/
def d3 (y : C3) : C4 :=
  y 0 + y 1 + y 2 + y 3 + y 4

/-- Every triangle occurs in exactly two tetrahedral boundary facets. -/
theorem d3_d2_zero : forall x : C2, d3 (d2 x) = 0 := by
  decide

/-- Residual supported on one tetrahedral facet. -/
def oneTetrahedron : C3 := ![1, 0, 0, 0, 0]

theorem oneTetrahedron_not_in_range :
    forall x : C2, d2 x ≠ oneTetrahedron := by
  decide

def hollowFourCellProbe (_ : C3) : Unit := ()

theorem hollow_boundary_local_green :
    hollowFourCellProbe oneTetrahedron = () := by
  rfl

theorem filled_four_cell_global_red : d3 oneTetrahedron ≠ 0 := by
  decide

theorem pentachoron_local_green_global_red :
    hollowFourCellProbe oneTetrahedron = () /\ d3 oneTetrahedron ≠ 0 :=
  ⟨hollow_boundary_local_green, filled_four_cell_global_red⟩

theorem four_cell_declaration_does_not_exactify :
    Not (exists x : C2, d2 x = oneTetrahedron) := by
  rintro ⟨x, hx⟩
  exact oneTetrahedron_not_in_range x hx

def bitWeight (x : F2) : Nat :=
  if x = 0 then 0 else 1

def supportWeight (x : C3) : Nat :=
  bitWeight (x 0) + bitWeight (x 1) + bitWeight (x 2) +
    bitWeight (x 3) + bitWeight (x 4)

def residualAfterTriangleRepair (x : C2) : C3 :=
  oneTetrahedron - d2 x

/-- Exact finite certificate for `Phi3(oneTetrahedron) = 1`. -/
theorem one_tetrahedron_phi3_certificate :
    (forall x : C2, 1 <= supportWeight (residualAfterTriangleRepair x)) /\
      exists x : C2, supportWeight (residualAfterTriangleRepair x) = 1 := by
  decide

def oneTetrahedronRepair : C3 := oneTetrahedron

def repairedCochain : C3 := oneTetrahedron - oneTetrahedronRepair

theorem one_tetrahedron_repair_has_cost_one :
    supportWeight oneTetrahedronRepair = 1 := by
  decide

theorem one_tetrahedron_repair_zeroes_residual : repairedCochain = 0 := by
  decide

theorem one_tetrahedron_repair_is_exact :
    exists x : C2, d2 x = repairedCochain := by
  refine ⟨0, ?_⟩
  decide

theorem one_tetrahedron_repair_closes_four_cell :
    d3 repairedCochain = 0 := by
  decide

/-- Complete `C3 -> C4` packet: detect, preserve non-exactness, then repair. -/
theorem detect_then_repair_pentachoron :
    d3 oneTetrahedron ≠ 0 /\
      Not (exists x : C2, d2 x = oneTetrahedron) /\
      supportWeight oneTetrahedronRepair = 1 /\
      (exists x : C2, d2 x = repairedCochain) /\
      d3 repairedCochain = 0 := by
  exact ⟨filled_four_cell_global_red,
    four_cell_declaration_does_not_exactify,
    one_tetrahedron_repair_has_cost_one,
    one_tetrahedron_repair_is_exact,
    one_tetrahedron_repair_closes_four_cell⟩

end BigBangPentachoronLift
end QM

#print axioms QM.BigBangPentachoronLift.d3_d2_zero
#print axioms QM.BigBangPentachoronLift.pentachoron_local_green_global_red
#print axioms QM.BigBangPentachoronLift.four_cell_declaration_does_not_exactify
#print axioms QM.BigBangPentachoronLift.one_tetrahedron_phi3_certificate
#print axioms QM.BigBangPentachoronLift.detect_then_repair_pentachoron
