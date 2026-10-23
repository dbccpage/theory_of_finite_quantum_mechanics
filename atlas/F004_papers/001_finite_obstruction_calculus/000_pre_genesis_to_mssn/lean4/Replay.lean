import Paper
import Homology
import GraphHomology
import TriangleHomology
import TriangleDegree
import Cochain
import BellPair
import BellMixture
import WordRecovery
import FreeWord
import UnionComponents
import SnTheorems

namespace PreMssn.Replay

def nums (s : String) : Option (List Int) := do
  let parts := if s.isEmpty then [] else s.splitOn ","
  let values ← parts.mapM String.toInt?
  if values.all (fun x => x.natAbs ≤ 1000000) &&
     (values.zip parts).all (fun (x, s) => toString x == s) then some values else none

def natural (s : String) : Option Nat := do
  let value ← s.toNat?
  if toString value == s then some value else none

def factorOK (reports answers : List Int) : Bool :=
  let pairs := reports.zip answers
  pairs.all (fun x => pairs.all (fun y => x.1 != y.1 || x.2 == y.2))

def intCSV (xs : List Int) := String.intercalate "," (xs.map toString)

def decimalDigit (c : Char) : Option (Fin 10) :=
  if h : c.toNat - 48 < 10 then
    if c.toNat ≥ 48 then some ⟨c.toNat - 48, h⟩ else none
  else none

def bit (c : Char) : Option Bool :=
  if c == '0' then some false else if c == '1' then some true else none

def traceEdges : List Int → Option (List (WordRecovery.EdgeSyntax Int))
  | [] => some []
  | a :: direction :: b :: rest => do
    if direction != 0 && direction != 1 then return ← none
    let tail ← traceEdges rest
    return ⟨a, direction == 1, b⟩ :: tail
  | _ => none

def endpointPairs : List Int → List (Nat × Nat)
  | a::b::rest => (a.toNat,b.toNat)::endpointPairs rest
  | _ => []

def wordRecovery (erase : Bool) (word : String) : Option String := do
  if word.length > 64 || word.toList.any (fun c => c != 'a' && c != 'b' && c != 'c')
  then return ← none
  let old : Char → Prop := fun c => c = 'a' ∨ c = 'b'
  if erase then
    some (String.ofList ((WordRecovery.eraseWord old word.toList).map Subtype.val))
  else match WordRecovery.recoverWord old word.toList with
    | .inl source => some (String.ofList (source.map Subtype.val))
    | .inr _ => some "NON_DESCENT"

def run (line : String) : Option String := do
  match line.splitOn "\t" with
  | ["v1", "factor", rs, ss] =>
    let r ← nums rs
    let s ← nums ss
    if r.length > 8 || r.length != s.length then none
    else some (if factorOK r s then "1" else "0")
  | ["v1", "demand", ns, ws, ds, bs] =>
    let n ← natural ns
    let w ← natural ws
    let d ← natural ds
    let b ← natural bs
    if n > 8 || [w,d,b].any (fun x => x ≥ 2^n) then return ← none
    let active := (List.range n).filter w.testBit
    let removed := (List.range n).filter d.testBit
    let births := (List.range n).filter b.testBit
    let residual := active.filter (fun x => !(d.testBit x))
    if removed.any (fun x => !(w.testBit x)) || births.any (fun x => x ∈ residual)
    then none else some (toString (residual.length + births.length))
  | ["v1", "boundary", ns, es, cs] =>
    let n ← natural ns
    let endpoints ← nums es
    let coefficients ← nums cs
    if n > 8 || endpoints.length != 2*coefficients.length || coefficients.length > 16
    then return ← none
    if endpoints.any (fun x => x < 0 || x ≥ (n : Int)) then return ← none
    let result := (List.range n).map fun (v : Nat) =>
      ((List.range coefficients.length).map fun k =>
        let a := endpoints.getD (2*k) 0
        let b := endpoints.getD (2*k+1) 0
        let c := coefficients.getD k 0
        (if b == (v : Int) then c else 0) - (if a == (v : Int) then c else 0)).sum
    some (intCSV result)
  | ["v1", "components", ns, es, cs] =>
    let n ← natural ns
    let endpoints ← nums es
    let coefficients ← nums cs
    if n > 8 || endpoints.length % 2 != 0 || endpoints.length > 32 || coefficients.length != n
    then return ← none
    if endpoints.any (fun x => x < 0 || x ≥ (n : Int)) then return ← none
    some (intCSV (UnionComponents.componentTotals n (endpointPairs endpoints) coefficients))
  | ["v1", "cyclic", values] =>
    match ← nums values with
    | [m,n] => some (toString (Homology.integerRepresentative m n))
    | _ => none
  | ["v1", "triangle", fs, values] =>
    let filled ← natural fs
    if filled > 1 then return ← none
    match ← nums values with
    | [x,y,z] => return toString (← TriangleHomology.classify (filled == 1) ⟨x,y,z⟩)
    | _ => none
  | ["v1", "cochain", values] =>
    match ← nums values with
    | [p,q,r] => some (toString (Cochain.triangleCoordinate p q r))
    | _ => none
  | ["v1", "triangle_degree", values] =>
    match ← nums values with
    | [m,x,y,z] => return toString (← TriangleDegree.classify m ⟨x,y,z⟩)
    | _ => none
  | ["v1", "bellpair", flag] =>
    let negative ← natural flag
    if negative > 1 then none else some (intCSV (BellPair.numerators (negative == 1)))
  | ["v1", "decimal", word] =>
    if word.length > 16 then return ← none
    let digits ← word.toList.mapM decimalDigit
    some (String.ofList ((WordRecovery.encodeDecimal digits).map (fun b => if b then '1' else '0')))
  | ["v1", "decimal_decode", bits] =>
    if bits.length > 64 then return ← none
    let bits ← bits.toList.mapM bit
    let digits ← WordRecovery.decodeDecimal bits
    some (String.join (digits.map (fun d => toString d.val)))
  | ["v1", "recover", word] => wordRecovery false word
  | ["v1", "erase", word] => wordRecovery true word
  | ["v1", "rename", ms, ws] =>
    let mapping ← nums ms
    let word ← nums ws
    if mapping.length > 8 || word.length > 64 ||
      word.any (fun i => i < 0 || i ≥ (mapping.length : Int)) then return ← none
    some (intCSV (word.map (fun i => mapping.getD i.toNat 0)))
  | ["v1", "trace", values] =>
    let values ← nums values
    if values.length > 48 then return ← none
    let edges ← traceEdges values
    let reversed := WordRecovery.reverseTrace edges
    some (intCSV (reversed.flatMap (fun e => [e.first, if e.arrow then 1 else 0, e.last])))
  | ["v1", "code", word] =>
    if word.length > 64 || word.toList.any (fun c => c != 'a' && c != 'b') then none
    else some (String.join (word.toList.map fun c => if c == 'a' then "0" else "00"))
  | ["v1", "chsh", values] =>
    match ← nums values with
    | [a,b,c,d] => let result := chsh a b c d; some (intCSV [result.1,result.2])
    | _ => none
  | ["v1", "freeword", word] =>
    if word.length > 64 || word.toList.any (fun c => !(['a','b','A','B'].contains c))
    then return ← none
    let signed := word.toList.map (fun c => (c == 'b' || c == 'B', c == 'A' || c == 'B'))
    let reduced := FreeWord.reduce signed
    some (String.ofList (reduced.map (fun (a, inverse) =>
      if a then (if inverse then 'B' else 'b') else (if inverse then 'A' else 'a'))))
  | ["v1", "bellmix", values] =>
    let weights ← nums values
    let distribution ← BellMixture.fromWeights weights
    some (String.intercalate "," ((BellMixture.runtimeCorrelations distribution).map toString))
  | _ => none

end PreMssn.Replay

def main : IO Unit := do
  let input ← IO.getStdin
  let output ← IO.getStdout
  repeat
    let line ← input.getLine
    if line.isEmpty then break
    let record := (line.dropEndWhile (fun c => c == '\n' || c == '\r')).toString
    output.putStrLn ((PreMssn.Replay.run record).getD "REFUSE")
