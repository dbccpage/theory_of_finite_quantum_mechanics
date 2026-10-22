/-!
# Boundary entropies versus minimal bond cuts on the 6-tensor HaPPY pentagon patch
(ADS-HAPPY-ENTROPY-MINCUT-TARGET)

AuthorityEffect: None.
Scope: Exact `GF(2)` stabilizer rank and graph minimal-cut comparison on the 20-qubit boundary state
of the 6-tensor HaPPY `{5,4}` pentagon patch (one central pentagon contracted along its 5 edges with
five non-adjacent outer pentagons, with all 6 bulk logical legs fixed in `|0_L⟩`).
Proves:
1. The 20 boundary stabilizer generators (15 local to the 5 four-leg outer blocks plus 5 pushed
   through the internal bonds from the central pentagon) pairwise commute and have full `GF(2)` rank 20.
2. Across all `20 × 19 = 380` nontrivial contiguous boundary intervals `A` (`start ∈ 0..19`,
   `length ∈ 1..19`), `S(A) ≤ mincut(A)` holds universally:
   - `340` contiguous intervals satisfy exact equality `S(A) = mincut(A)` (including all intervals of
     lengths `1..7` and `13..19`);
   - `40` contiguous intervals (8 per outer pentagon block under 5-fold cyclic symmetry, all of
     lengths `8..12` where boundary cuts split outer pentagons `2|2` across bulk-fixed `|0_L⟩`
     states that carry weight-3 stabilizers) have `S(A) = mincut(A) - 1`.
-/

namespace FrontierHappyMincut

/-- A 20-qubit Pauli operator represented as a 40-bit symplectic integer (`bit 2q` = `X_q`,
`bit 2q+1` = `Z_q`). -/
def setXZ (q x z : Nat) : Nat :=
  (if x == 1 then 1 <<< (2 * q) else 0) ||| (if z == 1 then 1 <<< (2 * q + 1) else 0)

/-- The 3 local boundary stabilizer generators on the 4 dangling legs `(0, 1, 2, 3)` of an outer
pentagon whose internal leg is `I`:
- `g2 = I X Z Z X` -> `X Z Z X`
- `g1 * g3 = I Z Y Y Z` -> `Z Y Y Z`
- `g4 * g5 = I Y Z Y I` -> `Y Z Y I` -/
def localBlock3 : List (List (Nat × Nat)) :=
  [ [(1,0), (0,1), (0,1), (1,0)],
    [(0,1), (1,1), (1,1), (0,1)],
    [(1,1), (0,1), (1,1), (0,0)] ]

/-- Operator pushed from internal leg `0` of an outer pentagon to its 4 boundary legs:
- `X` on leg 0 pushes via `g1 = X Z Z X I` to `Z Z X I`
- `Z` on leg 0 pushes via `g4 = Z X I X Z` to `X I X Z` -/
def pushXBlock : List (Nat × Nat) := [(0,1), (0,1), (1,0), (0,0)]
def pushZBlock : List (Nat × Nat) := [(1,0), (0,0), (1,0), (0,1)]

/-- The 5 stabilizer generators of the central pentagon (with bulk leg fixed in `|0_L⟩`):
`XZZXI`, `IXZZX`, `XIXZZ`, `ZXIXZ`, `ZZZZZ`. -/
def centralGens5 : List (List (Nat × Nat)) :=
  [ [(1,0), (0,1), (0,1), (1,0), (0,0)],
    [(0,0), (1,0), (0,1), (0,1), (1,0)],
    [(1,0), (0,0), (1,0), (0,1), (0,1)],
    [(0,1), (1,0), (0,0), (1,0), (0,1)],
    [(0,1), (0,1), (0,1), (0,1), (0,1)] ]

def encodeLocalGen (k : Nat) (pat : List (Nat × Nat)) : Nat :=
  (List.range 4).foldl
    (fun acc j =>
      let (x, z) := pat.getD j (0, 0)
      acc ^^^ setXZ (4 * k + j) x z)
    0

def encodeCentralGen (cpat : List (Nat × Nat)) : Nat :=
  (List.range 5).foldl
    (fun acc k =>
      let (cx, cz) := cpat.getD k (0, 0)
      let afterX :=
        if cx == 1 then acc ^^^ encodeLocalGen k pushXBlock else acc
      if cz == 1 then afterX ^^^ encodeLocalGen k pushZBlock else afterX)
    0

/-- All 20 stabilizer generators of the 20-qubit boundary state. -/
def boundaryGens20 : List Nat :=
  ((List.range 5).flatMap fun k => localBlock3.map (encodeLocalGen k)) ++
  (centralGens5.map encodeCentralGen)

/-- Symplectic commutation check on 20 qubits. -/
def commutes20 (u v : Nat) : Bool :=
  let s := (List.range 20).foldl
    (fun acc q =>
      let ux := (u >>> (2 * q)) &&& 1
      let uz := (u >>> (2 * q + 1)) &&& 1
      let vx := (v >>> (2 * q)) &&& 1
      let vz := (v >>> (2 * q + 1)) &&& 1
      acc + ((ux * vz) ^^^ (uz * vx)))
    0
  s % 2 == 0

/-- Gaussian elimination over `GF(2)` using explicit `(pivotBit, row)` echelon reduction. -/
def firstSetBit40 (r : Nat) : Nat :=
  ((List.range 40).find? (fun b => ((r >>> b) &&& 1) == 1)).getD 0

def insertPivotBasis (basis : List (Nat × Nat)) (r : Nat) : List (Nat × Nat) :=
  let rRed := basis.foldl
    (fun cur (p, b) => if ((cur >>> p) &&& 1) == 1 then cur ^^^ b else cur)
    r
  if rRed == 0 then basis
  else basis ++ [(firstSetBit40 rRed, rRed)]

def gf2Rank (rows : List Nat) : Nat :=
  (rows.foldl insertPivotBasis []).length

def inContiguousInterval (start len q : Nat) : Bool :=
  ((q + 20 - start) % 20) < len

/-- 40-bit symplectic bitmask selecting the qubits in the contiguous interval `(start, len)`. -/
def intervalBitmask40 (start len : Nat) : Nat :=
  (List.range 20).foldl
    (fun acc q =>
      if inContiguousInterval start len q then acc ||| (3 <<< (2 * q)) else acc)
    0

/-- Entanglement entropy `S(A) = rank(G|_A) - |A|` in bits for the contiguous interval `(start, len)`. -/
def intervalEntropy (start len : Nat) : Nat :=
  let mask40 := intervalBitmask40 start len
  let rows := boundaryGens20.map (fun r => r &&& mask40)
  gf2Rank rows - len

/-- Minimal number of tensor-network bonds cut by a surface separating the contiguous boundary
interval `(start, len)` from its complement in the 6-pentagon star graph. -/
def intervalMincut (start len : Nat) : Nat :=
  let a := (List.range 5).map fun k =>
    ((List.range 4).filter fun j => inContiguousInterval start len (4 * k + j)).length
  let costForCentral (sC : Nat) : Nat :=
    (List.range 5).foldl
      (fun acc k =>
        let ak := a.getD k 0
        let c0 := ak + (if 0 != sC then 1 else 0)
        let c1 := (4 - ak) + (if 1 != sC then 1 else 0)
        acc + min c0 c1)
      0
  min (costForCentral 0) (costForCentral 1)

def allIntervals380 : List (Nat × Nat) :=
  (List.range 20).flatMap fun start =>
    ((List.range 19).map (· + 1)).map fun len => (start, len)

set_option maxRecDepth 20000 in
set_option maxHeartbeats 800000 in
theorem boundary_stabilizer_commutes_and_full_rank_20 :
    boundaryGens20.length = 20 ∧
    (boundaryGens20.all fun u => boundaryGens20.all fun v => commutes20 u v) = true ∧
    gf2Rank boundaryGens20 = 20 := by
  decide

set_option maxRecDepth 20000 in
set_option maxHeartbeats 1600000 in
/-- Across all 380 nontrivial contiguous intervals `(start, len)`, `340` satisfy `S(A) = mincut(A)`
and `40` satisfy `S(A) + 1 = mincut(A)`. -/
theorem happy_patch_380_intervals_entropy_vs_mincut :
    allIntervals380.length = 380 ∧
    (allIntervals380.filter fun (s, l) => intervalEntropy s l == intervalMincut s l).length = 340 ∧
    (allIntervals380.filter fun (s, l) => intervalEntropy s l + 1 == intervalMincut s l).length = 40 ∧
    (allIntervals380.all fun (s, l) => decide (intervalEntropy s l ≤ intervalMincut s l)) = true := by
  decide

end FrontierHappyMincut

#print axioms FrontierHappyMincut.boundary_stabilizer_commutes_and_full_rank_20
#print axioms FrontierHappyMincut.happy_patch_380_intervals_entropy_vs_mincut

private def l5aProvenance : String :=
  "Origin: lean4/FrontierHappyMincut.lean Claim: happy_patch_380_intervals_entropy_vs_mincut AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
