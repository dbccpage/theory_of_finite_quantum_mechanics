/-
Campaign narrowing of MAJ-OPEN-EVIDENCE-ADEQUACY.

Two integer coordinate maps on the readings (1, 0) and (1, 1).
Status stays OPEN. No laboratory protocol is derived here.
-/

def topo : Int × Int := (1, 0)

def andreev : Int × Int := (1, 1)

def readingDiff : Int × Int := (topo.1 - andreev.1, topo.2 - andreev.2)

def firstCoord (v : Int × Int) : Int := v.1

def secondCoord (v : Int × Int) : Int := v.2

theorem diff_is_zero_neg_one : readingDiff = (0, -1) := by
  decide

theorem first_coord_kernel :
    firstCoord readingDiff = 0 ∧ firstCoord topo = 1 ∧ firstCoord andreev = 1 := by
  decide

theorem second_coord_separates :
    secondCoord readingDiff = -1 ∧ secondCoord topo = 0 ∧ secondCoord andreev = 1 ∧
      secondCoord topo ≠ secondCoord andreev := by
  decide

#print axioms diff_is_zero_neg_one
#print axioms first_coord_kernel
#print axioms second_coord_separates
