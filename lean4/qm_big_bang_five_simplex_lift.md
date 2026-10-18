import «000_000_big_bang_100_big_bang_dda_ascent»
import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Fin.VecNotation

/-!
# The 5-simplex C4-to-C5 rung is detect-then-repair

The boundary of a 5-simplex has fifteen tetrahedral 3-faces and six
4-simplex facets. A one-facet `F2` 4-cochain is not a tetrahedral
coboundary. Declaring the 5-cell exposes a nonzero successor diagnostic while
leaving the old repair image unchanged. A separate cost-one facet update
reaches an exact and closed residual.

This is a finite cellular witness only. It does not identify cochain degree
with spacetime dimension or supply any post-M-theory field content.
-/

namespace QM
namespace BigBangFiveSimplexLift

set_option maxRecDepth 1000000

abbrev F2 := ZMod 2

/-- Tetrahedral 3-cochains on the fifteen four-vertex subsets of `0,...,5`. -/
abbrev C3 := Fin 15 -> F2

/-- 4-cochains on the six boundary 4-simplex facets. -/
abbrev C4 := Fin 6 -> F2

/-- One 5-simplex evaluator. -/
abbrev C5 := F2

/-- Tetrahedron-to-4-facet coboundary on the boundary of a 5-simplex.

The tetrahedra are ordered
`0123,0124,0125,0134,0135,0145,0234,0235,0245,0345,1234,1235,1245,1345,2345`.
The facets are ordered `01234,01235,01245,01345,02345,12345`. -/
def d3 (x : C3) : C4 :=
  ![x 0 + x 1 + x 3 + x 6 + x 10,
    x 0 + x 2 + x 4 + x 7 + x 11,
    x 1 + x 2 + x 5 + x 8 + x 12,
    x 3 + x 4 + x 5 + x 9 + x 13,
    x 6 + x 7 + x 8 + x 9 + x 14,
    x 10 + x 11 + x 12 + x 13 + x 14]

/-- 4-facet-to-5-cell coboundary. -/
def d4 (y : C4) : C5 :=
  y 0 + y 1 + y 2 + y 3 + y 4 + y 5
/-- Addition is self-cancelling over `F2`. -/
theorem f2_add_self : forall z : F2, z + z = 0 := by
  decide

/-- Every tetrahedron occurs in exactly two 4-simplex boundary facets. -/
theorem d4_d3_zero : forall x : C3, d4 (d3 x) = 0 := by
  intro x
  change
    (x 0 + x 1 + x 3 + x 6 + x 10) +
      (x 0 + x 2 + x 4 + x 7 + x 11) +
      (x 1 + x 2 + x 5 + x 8 + x 12) +
      (x 3 + x 4 + x 5 + x 9 + x 13) +
      (x 6 + x 7 + x 8 + x 9 + x 14) +
      (x 10 + x 11 + x 12 + x 13 + x 14) = 0
  calc
    _ = (x 0 + x 0) + (x 1 + x 1) + (x 2 + x 2) +
        (x 3 + x 3) + (x 4 + x 4) + (x 5 + x 5) +
        (x 6 + x 6) + (x 7 + x 7) + (x 8 + x 8) +
        (x 9 + x 9) + (x 10 + x 10) + (x 11 + x 11) +
        (x 12 + x 12) + (x 13 + x 13) + (x 14 + x 14) := by
      ac_rfl
    _ = 0 := by simp only [f2_add_self, zero_add]

/-- Residual supported on one 4-simplex facet. -/
def oneFacet : C4 := ![1, 0, 0, 0, 0, 0]

def hollowFiveCellProbe (_ : C4) : Unit := ()

theorem hollow_boundary_local_green :
    hollowFiveCellProbe oneFacet = () := by
  rfl

theorem filled_five_cell_global_red : d4 oneFacet ≠ 0 := by
  decide

theorem five_simplex_local_green_global_red :
    hollowFiveCellProbe oneFacet = () /\ d4 oneFacet ≠ 0 :=
  ⟨hollow_boundary_local_green, filled_five_cell_global_red⟩

/-- The one-facet residual is not a tetrahedral coboundary. -/
theorem oneFacet_not_in_range : forall x : C3, d3 x ≠ oneFacet := by
  intro x hx
  apply filled_five_cell_global_red
  rw [← hx]
  exact d4_d3_zero x

theorem five_cell_declaration_does_not_exactify :
    Not (exists x : C3, d3 x = oneFacet) := by
  rintro ⟨x, hx⟩
  exact oneFacet_not_in_range x hx

def bitWeight (x : F2) : Nat :=
  if x = 0 then 0 else 1

def supportWeight (x : C4) : Nat :=
  bitWeight (x 0) + bitWeight (x 1) + bitWeight (x 2) +
    bitWeight (x 3) + bitWeight (x 4) + bitWeight (x 5)
/-- Support weight vanishes exactly on the zero 4-cochain. This finite lemma
checks only the 64 possible 4-cochains, not the 32,768 old repairs. -/
theorem supportWeight_eq_zero_iff :
    forall x : C4, supportWeight x = 0 ↔ x = 0 := by
  decide

theorem one_le_supportWeight_of_ne_zero (x : C4) (hne : x ≠ 0) :
    1 <= supportWeight x := by
  apply Nat.one_le_iff_ne_zero.mpr
  intro hzero
  exact hne ((supportWeight_eq_zero_iff x).mp hzero)

def residualAfterTetrahedronRepair (x : C3) : C4 :=
  oneFacet - d3 x
/-- No old tetrahedral repair can annihilate the one-facet residual. -/
theorem residualAfterTetrahedronRepair_ne_zero (x : C3) :
    residualAfterTetrahedronRepair x ≠ 0 := by
  intro hzero
  apply oneFacet_not_in_range x
  exact (sub_eq_zero.mp hzero).symm

/-- Exact finite certificate for `Phi4(oneFacet) = 1`. -/
theorem one_facet_phi4_certificate :
    (forall x : C3, 1 <= supportWeight (residualAfterTetrahedronRepair x)) /\
      exists x : C3, supportWeight (residualAfterTetrahedronRepair x) = 1 := by
  constructor
  · intro x
    exact one_le_supportWeight_of_ne_zero _ (residualAfterTetrahedronRepair_ne_zero x)
  · refine ⟨0, ?_⟩
    decide

def oneFacetRepair : C4 := oneFacet

def repairedCochain : C4 := oneFacet - oneFacetRepair

theorem one_facet_repair_has_cost_one :
    supportWeight oneFacetRepair = 1 := by
  decide

theorem one_facet_repair_zeroes_residual :
    repairedCochain = 0 := by
  decide

theorem one_facet_repair_is_exact :
    exists x : C3, d3 x = repairedCochain := by
  refine ⟨0, ?_⟩
  decide

theorem one_facet_repair_closes_five_cell :
    d4 repairedCochain = 0 := by
  decide

/-- Complete `C4 -> C5` packet: detect, preserve non-exactness, then repair. -/
theorem detect_then_repair_five_simplex :
    d4 oneFacet ≠ 0 /\
      Not (exists x : C3, d3 x = oneFacet) /\
      supportWeight oneFacetRepair = 1 /\
      (exists x : C3, d3 x = repairedCochain) /\
      d4 repairedCochain = 0 := by
  exact ⟨filled_five_cell_global_red,
    five_cell_declaration_does_not_exactify,
    one_facet_repair_has_cost_one,
    one_facet_repair_is_exact,
    one_facet_repair_closes_five_cell⟩

end BigBangFiveSimplexLift
end QM

#print axioms QM.BigBangFiveSimplexLift.d4_d3_zero
#print axioms QM.BigBangFiveSimplexLift.five_simplex_local_green_global_red
#print axioms QM.BigBangFiveSimplexLift.five_cell_declaration_does_not_exactify
#print axioms QM.BigBangFiveSimplexLift.one_facet_phi4_certificate
#print axioms QM.BigBangFiveSimplexLift.detect_then_repair_five_simplex
