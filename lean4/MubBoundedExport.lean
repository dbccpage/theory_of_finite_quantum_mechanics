import MubBoundedTermCollection
import MubBoundedMUFactor
import Lean.Data.Json

/-!
# Native JSON-lines export of the complete bounded quartet coefficient system

AuthorityEffect: None.

The coefficient semantics are kernel-checked in MubBoundedTermCollection.
This IO program does not kernel-reflect file bytes or establish infeasibility.
Every polynomial is checked at four exact rational points before serialization.
-/

namespace MUB.BoundedExport
open BoundedCoordinates BoundedPolynomials BoundedExpressions BoundedExportIndices
open BoundedTermCollection
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

def checkedRow (kind : String) (id : Nat) (e : Expr) (bound : Nat) : IO (Json × Nat) := do
  let ts := coefficients e
  if !ts.all (fun t => t.1 != 0 && t.2.length ≤ bound &&
      t.2.all (· < 152) && sortedFactors t.2) || !uniqueSortedTerms ts then
    throw (IO.userError s!"Coefficient shape failure: {kind} {id}")
  let mut probes : Array Json := #[]
  for p in List.range 4 do
    let expected := e.eval (fun c => probePoint p (variableCode c))
    let actual := evaluateTerms (probePoint p) ts
    if actual != expected then
      throw (IO.userError s!"Exact evaluation mismatch: {kind} {id}, probe {p}")
    probes := probes.push (Json.str (rationalString actual))
  return (Json.mkObj [
    ("kind", Json.str kind), ("id", toJson id), ("degree_bound", toJson bound),
    ("term_count", toJson ts.length), ("terms", Json.arr (ts.map termJson).toArray),
    ("probe_values", Json.arr probes)], ts.length)

def header : Json := Json.mkObj [
  ("kind", Json.str "header"), ("schema", Json.str "mub6.bounded.coefficients.v1"),
  ("authority_effect", Json.str "None"), ("variable_count", toJson (152 : Nat)),
  ("equation_count", toJson (396 : Nat)),
  ("box", toJson (["-1/1", "1/1"] : List String)),
  ("determinant_lower_bound", Json.str "54/5"),
  ("coordinate_codes", toJson (allVariables.map variableCode)),
  ("equation_codes", toJson (equations.map equationCode)),
  ("probe_count", toJson (4 : Nat)),
  ("probe_definitions", toJson (["0", "(i mod 17 - 7)/13", "1 if i even else -1",
    "((7*i+3) mod 19 - 8)/11"] : List String)),
  ("semantics", Json.str "Sum coefficient times product of factor coordinates; every equation equals zero."),
  ("kernel_reflected_file", Json.bool false), ("infeasibility_claimed", Json.bool false)]

def exportFile (path : System.FilePath) : IO Unit :=
  IO.FS.withFile path .write fun handle => do
    handle.putStrLn header.compress
    let (qrow, qcount) ← checkedRow "determinant_norm_square" 0 eQ 4
    handle.putStrLn qrow.compress
    let mut total := qcount
    let mut maximum := qcount
    for e in equations do
      let id := equationCode e
      let (row, count) ← checkedRow "equation" id (eEquation e) 8
      handle.putStrLn row.compress
      total := total + count
      maximum := max maximum count
      IO.println s!"equation={id}, terms={count}, exact_probes=4, shape_ok=true"
    handle.putStrLn (Json.mkObj [("kind", Json.str "complete"),
      ("equations", toJson equations.length), ("total_terms", toJson total),
      ("maximum_terms", toJson maximum)]).compress
    IO.println s!"COMPLETE equations={equations.length}, total_terms={total}, maximum_terms={maximum}"

def exportMUFactorsFile (path : System.FilePath) : IO Unit :=
  IO.FS.withFile path .write fun handle => do
    let selected := equations.filter (fun e => (BoundedMUFactor.replacement e).isSome)
    if selected.length != 36 then throw (IO.userError "MU replacement coverage changed")
    handle.putStrLn (Json.mkObj [
      ("kind", Json.str "header"), ("schema", Json.str "mub6.bounded.mu_factor_replacements.v1"),
      ("variable_count", toJson (152 : Nat)), ("base_equation_count", toJson (396 : Nat)),
      ("replacement_count", toJson selected.length),
      ("equation_codes", toJson (selected.map equationCode)),
      ("determinant_lower_bound", Json.str "54/5"),
      ("identity", Json.str "original_polynomial = determinant_norm_square * replacement_polynomial"),
      ("kernel_reflected_file", Json.bool false), ("infeasibility_claimed", Json.bool false)]).compress
    let mut total := 0
    for e in selected do
      let id := equationCode e
      let reduced := BoundedMUFactor.eEquationReduced e
      for p in List.range 4 do
        let r := fun c => probePoint p (variableCode c)
        if (eEquation e).eval r != eQ.eval r * reduced.eval r then
          throw (IO.userError s!"MU factor identity mismatch: {id}, probe {p}")
      let (row, count) ← checkedRow "mu_factor_replacement" id reduced 4
      handle.putStrLn row.compress
      total := total + count
      IO.println s!"replacement={id}, terms={count}, exact_probes=4, factor_probes=4, shape_ok=true"
    handle.putStrLn (Json.mkObj [("kind", Json.str "complete"),
      ("replacements", toJson selected.length), ("total_terms", toJson total)]).compress
    IO.println s!"COMPLETE replacements={selected.length}, total_terms={total}"

end MUB.BoundedExport
