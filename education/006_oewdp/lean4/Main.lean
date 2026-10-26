import WdpSyntax
import WdpParser

/-!
# WDP Parity Checker Executable

AuthorityEffect: None. GenesisEffect: None.
Executable CLI harness to verify multi-system parity between Python and Lean 4 wire AST representations.
-/

open WdpPresentation

def main (args : List String) : IO UInt32 := do
  if args.isEmpty then
    IO.println "Usage: wdp_parity_check <wire_token_1> [<wire_token_2> ...]"
    return 1

  let mut failed := false
  for wire in args do
    match parseWdp? wire with
    | some stmt =>
      let serialized := stmt.toWire
      if serialized == wire then
        IO.println s!"OK: {wire}"
      else
        IO.println s!"MISMATCH: wire={wire}, serialized={serialized}"
        failed := true
    | none =>
      IO.println s!"REJECT: {wire}"
      failed := true

  if failed then
    return 1
  else
    return 0
