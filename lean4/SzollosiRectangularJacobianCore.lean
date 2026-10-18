import SparseRectangularExclusion
import SzollosiRectangularExclusion

/-!
# Kernel reflection of the actual native rectangular run

AuthorityEffect: None.

All 618 sparse Jacobian rows and 440 images are checked against the actual
quartet polynomial table and full containing box. Every actual system zero
remains in every recorded intersection. The run contracts 24 coordinates and
excludes none. Full 56-cell/cusp coverage and curvature remain open.
-/
namespace MUB.SzollosiRectangularReflection
open SzollosiTermExpansion SzollosiNativeInterval SzollosiIntervalExclusion
open SzollosiExecutableSystem SzollosiQuadraticSystem SzollosiNativeReflection
open SzollosiRectangularExclusion SparseRectangularExclusion
set_option maxRecDepth 30000
set_option maxHeartbeats 100000000

-- Native rectangular receipt SHA-256: eccd3b1c075d0058cf729e2aa0af5e210860da93d2178ea09a9d5cfb3b820a76
-- Executable system SHA-256: 1367d390da36e5ccf65abbc8fbf529ff07f9e154c277bb14c1cd8c36ba24c947
-- Lean coefficient reference SHA-256: 44656965bb72e735febfc69c1bcd599adbeea2e8512ebd6141025f8524e5d2df
-- Native request SHA-256: d44dfd0b14fb610ba354ba2bedbea03c56df5f5d18d141cd58a4bd52c27a76af
def jacEntryKey (p : Nat × Bounds) := (p.1,boundsKey p.2)
def jacKeys (table : List (List (Nat × Bounds))) := table.map (List.map jacEntryKey)
theorem jac_entry_key_injective : Function.Injective jacEntryKey := by
  intro a b h
  change (a.1,boundsKey a.2) = (b.1,boundsKey b.2) at h
  exact Prod.ext (congrArg (fun z : Nat × (Int × Nat × Int × Nat) => z.1) h) (bounds_key_injective (congrArg (fun z : Nat × (Int × Nat × Int × Nat) => z.2) h))
theorem jac_keys_injective : Function.Injective jacKeys :=
  map_injective _ (map_injective _ jac_entry_key_injective)
def supportList (ts : List CodedTerm) : List Nat :=
  (List.insertionSort (· ≤ ·) (ts.flatMap Prod.snd)).eraseDups

theorem support_list_mem (ts : List CodedTerm) (k : Nat) :
    k∈supportList ts ↔ k∈coordinateSupport ts := by
  simp [supportList,coordinateSupport]

def expectedJacobianRow (e : Nat) : List (Nat × Bounds) :=
  (supportList (rows e)).map fun k =>
    (k, RectangularQuadraticExclusion.listGradient codedFullBox (rows e) k)


end MUB.SzollosiRectangularReflection
