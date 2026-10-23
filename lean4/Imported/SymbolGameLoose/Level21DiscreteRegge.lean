/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/Level21DiscreteRegge.lean
   Original sha256: 8f34409644a2b9da5a2d974722fbde2dd931d869efed93a4662925521640c404 (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.SymbolGameLoose.Level21DiscreteRegge
   Reason         : MSS-N
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
/-!
# Level 21: the scalar deficit sum does not certify closure

**Withdrawn as evidence for MSS-021 (2026-09-25, round P2).** This file used to
prove `discrete_bianchi_identity`: an alternating sum of four scalar deficits
vanishes under a hypothesis that restated the conclusion, with a full turn
written as the truncated integer `6283`. That is the scalar identity MSS-021's
own negative instance rejects ("a scalar sum of deficits cannot stand in for
closure"), so the file argued against its stage. The theorem and the truncated
turn are removed, not renamed.

What the file now proves is the negative instance's content, on a declared
finite instance: two quarter-turns in SO(4) with integer entries whose ordered
loop product is not the identity, while the loop's scalar angle sum
(`1 + 1 - 1 - 1`, the exponent sum of each generator) is zero. So a checker that
certifies closure from the scalar sum accepts a nontrivial loop. Everything is
decided by the kernel on concrete integer matrices.

The target checker of record for MSS-021 is
`research/mssn_sn_tower/code/python/targets/stage_021.py`; this file is not
cited as its evidence.
-/

namespace MSSN.Level21

/-- A 4x4 integer matrix, as a list of rows. -/
abbrev Mat := List (List Int)

def dot (u v : List Int) : Int := (List.zipWith (· * ·) u v).foldl (· + ·) 0

def col (m : Mat) (j : Nat) : List Int := m.map (fun row => row.getD j 0)

def transpose (m : Mat) : Mat := (List.range 4).map (col m)

def mul (a b : Mat) : Mat := a.map (fun row => (List.range 4).map (fun j => dot row (col b j)))

def identity : Mat := [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

/-- A quarter-turn in the y-z plane. -/
def rotYZ : Mat := [[1, 0, 0, 0], [0, 0, -1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]

/-- A quarter-turn in the x-z plane. -/
def rotXZ : Mat := [[0, 0, 1, 0], [0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 0, 1]]

/-- The ordered loop product `Rx * Ry * Rx⁻¹ * Ry⁻¹`; an inverse is a transpose. -/
def loopProduct : Mat := mul (mul (mul rotYZ rotXZ) (transpose rotYZ)) (transpose rotXZ)

/-- The scalar angle sum of the loop, in quarter-turns: `+1 +1 -1 -1`. -/
def scalarSum : Int := 1 + 1 - 1 - 1

theorem rotYZ_orthogonal : mul rotYZ (transpose rotYZ) = identity := by decide

theorem rotXZ_orthogonal : mul rotXZ (transpose rotXZ) = identity := by decide

theorem scalar_sum_vanishes : scalarSum = 0 := by decide

theorem ordered_product_is_not_identity : loopProduct ≠ identity := by decide

/-- The negative instance, decided: the scalar sum vanishes on a loop whose
ordered product is not the identity. -/
theorem scalar_sum_does_not_certify_closure : scalarSum = 0 ∧ loopProduct ≠ identity :=
  ⟨scalar_sum_vanishes, ordered_product_is_not_identity⟩

#print axioms rotYZ_orthogonal
#print axioms rotXZ_orthogonal
#print axioms scalar_sum_does_not_certify_closure

end MSSN.Level21
