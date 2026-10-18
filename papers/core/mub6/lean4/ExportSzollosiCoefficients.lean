import SzollosiTermExpansion

def main (args : List String) : IO Unit := do
  match args with
  | [path] => IO.FS.writeFile path (MUB.SzollosiTermExpansion.coefficientExport.compress ++ "\n")
  | _ => throw (IO.userError "expected output path")
