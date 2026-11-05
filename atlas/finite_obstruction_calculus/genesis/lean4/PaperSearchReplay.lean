import PaperSearch
import PaperWire

/-! Native execution of the proved exhaustive canonical search. The interface
accepts a labelled structural tuple, checks well-formed set collections, and
refuses more than 100,000 permutation pairs before starting the search. -/

open Derivation GenesisPaper GenesisPaper.Orbit GenesisPaper.Search GenesisPaper.Wire

private def hexByte (byte : UInt8) : String :=
  let digits := String.ofList (Nat.toDigits 16 byte.toNat)
  if digits.length = 1 then "0" ++ digits else digits

private def factorial : Nat → Nat
  | 0 => 1
  | n + 1 => (n + 1) * factorial n

private def searchLine (line : String) : Except String String := do
  let words ← (line.trimAscii.toString.splitOn ",").mapM fun part =>
    match part.toNat? with
    | some n => if n < 2 ^ 64 then .ok n else .error "word exceeds unsigned 64-bit range"
    | none => .error "invalid unsigned word"
  let (key, rest) ← match readStructural words with
    | some parsed => .ok parsed
    | none => .error "incomplete structural words"
  if !rest.isEmpty then throw "trailing structural words"
  let r := keyRegime key
  if r.data > 8 || r.forms.length > 8 then throw "native replay dimension cap exceeded"
  if factorial r.data * factorial r.forms.length > 100000 then throw "permutation budget exceeded"
  let validity : Decidable (r.wf ∧ SetCollections r) := by
    unfold Regime.wf SetCollections
    infer_instance
  if !(@decide (r.wf ∧ SetCollections r) validity) then throw "malformed regime or duplicate collections"
  match canonicalKey r with
  | some minimum => return String.join ((portableBytes minimum).map hexByte)
  | none => throw "unexpected empty candidate population"

def main : IO UInt32 := do
  let input ← IO.getStdin
  let output ← IO.getStdout
  let error ← IO.getStderr
  repeat
    let line ← input.getLine
    if line.isEmpty then return 0
    match searchLine line with
    | .ok encoded => output.putStrLn encoded
    | .error message =>
        error.putStrLn message
        return 1
  return 0
