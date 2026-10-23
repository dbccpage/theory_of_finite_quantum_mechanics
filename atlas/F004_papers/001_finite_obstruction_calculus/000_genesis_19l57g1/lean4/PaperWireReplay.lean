import PaperWire

/-! Native execution of the same encoder whose injectivity is mechanized.
Input is a comma-separated sequence of structural words. This small interface
checks the word range and complete parsing; it does not certify orbit minima. -/

open GenesisPaper.Wire

private def hexByte (byte : UInt8) : String :=
  let digits := String.ofList (Nat.toDigits 16 byte.toNat)
  if digits.length = 1 then "0" ++ digits else digits

private def wireLine (line : String) : Except String String := do
  let words ← (line.trimAscii.toString.splitOn ",").mapM fun part =>
    match part.toNat? with
    | some n => if n < 2 ^ 64 then .ok n else .error "word exceeds unsigned 64-bit range"
    | none => .error "invalid unsigned word"
  match readStructural words with
  | some (key, []) => return String.join ((portableBytes key).map hexByte)
  | _ => throw "incomplete or trailing structural words"

def main : IO UInt32 := do
  let input ← IO.getStdin
  let output ← IO.getStdout
  let error ← IO.getStderr
  repeat
    let line ← input.getLine
    if line.isEmpty then return 0
    match wireLine line with
    | .ok encoded => output.putStrLn encoded
    | .error message =>
        error.putStrLn message
        return 1
  return 0
