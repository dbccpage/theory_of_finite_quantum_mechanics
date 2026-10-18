import MubBalancedCodedSystem
import Lean.Data.Json

/-!
# Native export of the balanced quadratic model

AuthorityEffect: None. Every row is compared with direct rational matrix
arithmetic at four points. This does not kernel-reflect the file or exclude it.
-/
namespace MUB.BalancedExport
open BalancedQuadraticLift BalancedIndices BalancedCoefficients BoundedBlockChart
open QuadraticLiftPolynomials (Equation)
open QuadraticLiftIndices (equations equationCode)
open BoundedCoordinates (fillE fillB fillC fillBasis)
open BoundedTermCollection (Term keyLE)
open Lean (Json toJson)

def rationalString (q : Rat) : String := s!"{q.num}/{q.den}"

def probePoint (p i : Nat) : Rat :=
  if p = 0 then 0
  else if p = 1 then (i % 17 : Nat) / 13 - 7 / 13
  else if p = 2 then if i % 2 = 0 then 1 else -1
  else ((7 * i + 3) % 19 : Nat) / 11 - 8 / 11

def evaluateTerms (r : Nat → Rat) (ts : List Term) : Rat :=
  ts.foldl (fun total t => total + t.1 * t.2.foldl (fun z i => z * r i) 1) 0

def sortedFactors : List Nat → Bool
  | [] => true
  | [_] => true
  | i :: j :: js => decide (i ≤ j) && sortedFactors (j :: js)

def uniqueSortedTerms : List Term → Bool
  | [] => true
  | [_] => true
  | t :: u :: us => (t.2 != u.2) && keyLE t.2 u.2 && uniqueSortedTerms (u :: us)

def termJson (t : Term) : Json :=
  Json.arr #[Json.str (rationalString t.1), toJson t.2]

abbrev RC := QuadraticAlgebra Rat (-1) 0
abbrev RMat6 := Matrix I6 I6 RC

def directVariable (r : Nat → Rat) (s : Slot) : RC :=
  ⟨r (variableCode (s,false)),r (variableCode (s,true))⟩
def directOld (r : Nat → Rat) (s : BoundedCoordinates.Slot) : RC := directVariable r (.inl s)
def directH (r : Nat → Rat) : RMat6 := Matrix.fromBlocks
  (fillE (fun s => directOld r (.inl s)))
  (fillB (fun s => directOld r (.inr (.inl s))))
  (fillC (fun s => directOld r (.inr (.inr (.inl s)))))
  (fun i j => directVariable r (.inr (.inl (i,j))))
def directU (r : Nat → Rat) : RMat6 := fillBasis (fun s => directOld r (.inr (.inr (.inr (.inl s)))))
def directV (r : Nat → Rat) : RMat6 := fillBasis (fun s => directOld r (.inr (.inr (.inr (.inr s)))))
def directCore (r : Nat → Rat) (a : Fin 3) : Matrix (Fin 5) (Fin 5) RC :=
  fun i j => directVariable r (.inr (.inr (a,i,j)))
def directW (r : Nat → Rat) (a : Fin 3) : RMat6 := fun i j =>
  BalancedCompletion.complete (directCore r a) (blockIndex i) (blockIndex j)
def directBases (r : Nat → Rat) : Fin 3 → RMat6 := ![directH r,directU r,directV r]
def directTransition (A B : RMat6) (i j : I6) : RC :=
  (List.finRange 6).foldl (fun z k => z + star (A (blockIndex.symm k) i) * B (blockIndex.symm k) j) 0
def directTransitions (r : Nat → Rat) : Fin 3 → RMat6 :=
  ![directTransition (directH r) (directU r),directTransition (directH r) (directV r),
    directTransition (directU r) (directV r)]
def directNorm (z : RC) : Rat := z.re*z.re+z.im*z.im
def directComponent (z : RC) (b : Bool) : Rat := if b then z.im else z.re

def directEquation (r : Nat → Rat) : Equation → Rat
  | .inl (a,i,j) => directNorm (directBases r a i j) - 1
  | .inr (.inl (a,i,j,b)) => directComponent
      (directTransition (directBases r a) (directBases r a) i j - if i=j then 6 else 0) b
  | .inr (.inr (.inl (a,i,j,b))) => directComponent (directW r a i j - directTransitions r a i j) b
  | .inr (.inr (.inr (a,i,j))) => directNorm (directW r a i j) - 6

def checkedTerms (e : Equation) (ts : List Term) : IO (Json × Nat) := do
  let id := equationCode e
  if !ts.all (fun t => t.1 != 0 && t.2.length ≤ 2 &&
      t.2.all (· < 320) && sortedFactors t.2) || !uniqueSortedTerms ts then
    throw (IO.userError s!"Coefficient shape failure: {id}")
  let mut probes : Array Json := #[]
  for p in List.range 4 do
    let expected := directEquation (probePoint p) e
    let actual := evaluateTerms (probePoint p) ts
    if actual != expected then
      throw (IO.userError s!"Direct matrix evaluation mismatch: equation={id}, probe={p}")
    probes := probes.push (Json.str (rationalString actual))
  return (Json.mkObj [
    ("kind", Json.str "equation"), ("id", toJson id), ("degree_bound", toJson (2 : Nat)),
    ("term_count", toJson ts.length), ("terms", Json.arr (ts.map termJson).toArray),
    ("probe_values", Json.arr probes)], ts.length)

def checkedRow (e : Equation) : IO (Json × Nat) := checkedTerms e (equationCoefficients e)

def header : Json := Json.mkObj [
  ("kind", Json.str "header"), ("schema", Json.str "mub6.balanced_quadratic.coefficients.v1"),
  ("authority_effect", Json.str "None"), ("variable_count", toJson (320 : Nat)),
  ("equation_count", toJson (648 : Nat)),
  ("coordinate_codes", toJson (allVariables.map variableCode)),
  ("equation_codes", toJson (equations.map equationCode)),
  ("coordinate_bounds", toJson ((List.range 320).map fun i =>
    [rationalString (-codeRadius i),rationalString (codeRadius i)])),
  ("probe_count", toJson (4 : Nat)),
  ("probe_definitions", toJson (["0", "(i mod 17 - 7)/13", "1 if i even else -1",
    "((7*i+3) mod 19 - 8)/11"] : List String)),
  ("semantics", Json.str "Sum coefficient times product of factor coordinates; every equation equals zero."),
  ("determinant_inequality", Json.null),
  ("kernel_reflected_file", Json.bool false), ("infeasibility_claimed", Json.bool false)]

def exportFile (path : System.FilePath) : IO Unit := do
  if ← path.pathExists then throw (IO.userError "Output path already exists")
  IO.FS.withFile path .write fun handle => do
    handle.putStrLn header.compress
    let mut total := 0
    let mut maximum := 0
    for e in equations do
      let id := equationCode e
      let (row, count) ← checkedRow e
      handle.putStrLn row.compress
      total := total + count
      maximum := max maximum count
      IO.println s!"equation={id}, terms={count}, direct_matrix_probes=4, shape_ok=true"
    handle.putStrLn (Json.mkObj [("kind", Json.str "complete"),
      ("equations", toJson equations.length), ("total_terms", toJson total),
      ("maximum_terms", toJson maximum)]).compress
    IO.println s!"COMPLETE equations={equations.length}, total_terms={total}, maximum_terms={maximum}"

end MUB.BalancedExport
