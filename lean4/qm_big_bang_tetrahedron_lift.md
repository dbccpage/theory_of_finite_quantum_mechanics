import «000_000_big_bang_100_big_bang_dda_ascent»
import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Fin.VecNotation

/-!
# The tetrahedral C2-to-C3 rung is detect-then-repair

The boundary of a tetrahedron has six edges and four triangular faces. A
one-face `F2` 2-cochain is not an edge coboundary. On the hollow boundary there
is no declared volume evaluator, so the residual is locally green and survives.
Declaring the tetrahedral 3-cell exposes nonzero `d2`, but it leaves `im d1`
unchanged and therefore does not exactify the residual. A separate cost-one
face update reaches an exact and closed residual.

This is a finite higher-cochain regression witness. It does not identify
cochain degree with spacetime dimension or derive a higher-form field theory.
-/

namespace QM
namespace BigBangTetrahedronLift

abbrev F2 := ZMod 2

/-- Edge 1-cochains on `01, 02, 03, 12, 13, 23`. -/
abbrev C1 := Fin 6 -> F2

/-- Face 2-cochains on `012, 013, 023, 123`. -/
abbrev C2 := Fin 4 -> F2

/-- One tetrahedral volume evaluator. -/
abbrev C3 := F2

/-- Edge-to-face coboundary. Orientations are immaterial over `F2`. -/
def d1 (x : C1) : C2 :=
  ![x 0 + x 1 + x 3,
    x 0 + x 2 + x 4,
    x 1 + x 2 + x 5,
    x 3 + x 4 + x 5]

/-- Face-to-volume coboundary. -/
def d2 (y : C2) : C3 :=
  y 0 + y 1 + y 2 + y 3

/-- Every edge occurs in exactly two boundary faces. -/
theorem d2_d1_zero : forall x : C1, d2 (d1 x) = 0 := by
  decide

/-- The residual supported on one face. -/
def oneFace : C2 := ![1, 0, 0, 0]

/-- The one-face residual is not an edge coboundary. -/
theorem oneFace_not_in_range : forall x : C1, d1 x ≠ oneFace := by
  decide

/-- The hollow boundary has no declared volume evaluator. -/
def hollowVolumeProbe (_ : C2) : Unit := ()

/-- The one-face residual is locally green on the hollow boundary. -/
theorem hollow_boundary_local_green : hollowVolumeProbe oneFace = () := by
  rfl

/-- Declaring the tetrahedral volume exposes a nonzero closure defect. -/
theorem filled_volume_global_red : d2 oneFace ≠ 0 := by
  decide

/-- The next finite LGGR rung: hollow-boundary green, filled-volume red. -/
theorem tetrahedron_local_green_global_red :
    hollowVolumeProbe oneFace = () /\ d2 oneFace ≠ 0 :=
  ⟨hollow_boundary_local_green, filled_volume_global_red⟩

/-- Adding the volume evaluator does not change the old edge-to-face image. -/
theorem volume_declaration_does_not_exactify :
    Not (exists x : C1, d1 x = oneFace) := by
  rintro ⟨x, hx⟩
  exact oneFace_not_in_range x hx

def bitWeight (x : F2) : Nat :=
  if x = 0 then 0 else 1

/-- Unit support size on the four faces. -/
def supportWeight (x : C2) : Nat :=
  bitWeight (x 0) + bitWeight (x 1) +
    bitWeight (x 2) + bitWeight (x 3)

/-- Residual after an old edge-cochain repair. -/
def residualAfterEdgeRepair (x : C1) : C2 :=
  oneFace - d1 x

/-- Exact finite certificate for `Phi2(oneFace) = 1`. -/
theorem one_face_phi2_certificate :
    (forall x : C1, 1 <= supportWeight (residualAfterEdgeRepair x)) /\
      exists x : C1, supportWeight (residualAfterEdgeRepair x) = 1 := by
  decide

/-- A separately licensed one-face residual update. -/
def oneFaceRepair : C2 := oneFace

def repairedCochain : C2 := oneFace - oneFaceRepair

theorem one_face_repair_has_cost_one : supportWeight oneFaceRepair = 1 := by
  decide

theorem one_face_repair_zeroes_residual : repairedCochain = 0 := by
  decide

theorem one_face_repair_is_exact :
    exists x : C1, d1 x = repairedCochain := by
  refine ⟨0, ?_⟩
  decide

theorem one_face_repair_closes_volume : d2 repairedCochain = 0 := by
  decide

/-- Complete `C2 -> C3` packet: detect, preserve non-exactness, then repair. -/
theorem detect_then_repair_tetrahedron :
    d2 oneFace ≠ 0 /\
      Not (exists x : C1, d1 x = oneFace) /\
      supportWeight oneFaceRepair = 1 /\
      (exists x : C1, d1 x = repairedCochain) /\
      d2 repairedCochain = 0 := by
  exact ⟨filled_volume_global_red,
    volume_declaration_does_not_exactify,
    one_face_repair_has_cost_one,
    one_face_repair_is_exact,
    one_face_repair_closes_volume⟩

end BigBangTetrahedronLift
end QM

#print axioms QM.BigBangTetrahedronLift.d2_d1_zero
#print axioms QM.BigBangTetrahedronLift.tetrahedron_local_green_global_red
#print axioms QM.BigBangTetrahedronLift.volume_declaration_does_not_exactify
#print axioms QM.BigBangTetrahedronLift.one_face_phi2_certificate
#print axioms QM.BigBangTetrahedronLift.detect_then_repair_tetrahedron
