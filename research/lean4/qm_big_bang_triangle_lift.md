import «000_000_big_bang_100_big_bang_dda_ascent»
import «qm000_gamma2_triangle»

/-!
# The frustrated triangle is detect-then-repair, not automatic exactification

The hollow graph has no declared degree-two evaluator, so the defect is
locally green there. Declaring the face exposes `d1 c = 1`; it does not change
`im d0`, and therefore does not make `c` exact. A separate one-edge update
then produces the zero cochain, with exact replayable cost one.
-/

namespace QM
namespace BigBangTriangleLift

open QM000Gamma2

/-- The hollow 1-skeleton has no face probe. -/
def hollowProbe (_ : C1) : Unit := ()

theorem hollow_loop_local_green : hollowProbe c = () := by
  rfl

theorem filled_face_global_red : d1 c ≠ 0 := by
  rw [d1_c_active]
  decide

/-- The smallest concrete LGGR transition: the hollow graph is green to its
declared probe, while the filled face detects nonzero closure. -/
theorem triangle_local_green_global_red :
    hollowProbe c = () /\ d1 c ≠ 0 :=
  ⟨hollow_loop_local_green, filled_face_global_red⟩

/-- Face declaration exposes the defect but does not enlarge `im d0`. -/
theorem face_declaration_does_not_exactify :
    Not (exists f : C0, d0 f = c) := by
  rintro ⟨f, hf⟩
  exact c_not_in_range f hf

def bitWeight (x : F2) : Nat :=
  if x = 0 then 0 else 1

/-- Unit-weight support size on the three edges. -/
def supportWeight (x : C1) : Nat :=
  bitWeight (x 0) + bitWeight (x 1) + bitWeight (x 2)

/-- Residual after a flat vertex-gauge repair. -/
def residualAfterGauge (f : C0) : C1 :=
  c - d0 f

/-- Exact finite certificate for `Phi1(c) = 1`: every flat gauge leaves at
least one frustrated edge, and the zero gauge attains one. -/
theorem frustrated_triangle_phi1_certificate :
    (forall f : C0, 1 <= supportWeight (residualAfterGauge f)) /\
      exists f : C0, supportWeight (residualAfterGauge f) = 1 := by
  decide

/-- A one-edge cochain update; unlike face declaration, this changes the
residual representative. -/
def oneEdgeRepair : C1 := c

def repairedCochain : C1 := c - oneEdgeRepair

theorem one_edge_repair_has_cost_one : supportWeight oneEdgeRepair = 1 := by
  decide

theorem one_edge_repair_zeroes_residual : repairedCochain = 0 := by
  decide

theorem one_edge_repair_is_exact : exists f : C0, d0 f = repairedCochain := by
  refine ⟨0, ?_⟩
  decide

theorem one_edge_repair_closes_face : d1 repairedCochain = 0 := by
  decide

/-- The corrected finite DDA packet: detect first, then perform an explicit
cost-one repair that reaches both exactness and closure. -/
theorem detect_then_repair_triangle :
    d1 c ≠ 0 /\
      Not (exists f : C0, d0 f = c) /\
      supportWeight oneEdgeRepair = 1 /\
      (exists f : C0, d0 f = repairedCochain) /\
      d1 repairedCochain = 0 := by
  exact ⟨filled_face_global_red,
    face_declaration_does_not_exactify,
    one_edge_repair_has_cost_one,
    one_edge_repair_is_exact,
    one_edge_repair_closes_face⟩

end BigBangTriangleLift
end QM

#print axioms QM.BigBangTriangleLift.triangle_local_green_global_red
#print axioms QM.BigBangTriangleLift.face_declaration_does_not_exactify
#print axioms QM.BigBangTriangleLift.frustrated_triangle_phi1_certificate
#print axioms QM.BigBangTriangleLift.detect_then_repair_triangle
