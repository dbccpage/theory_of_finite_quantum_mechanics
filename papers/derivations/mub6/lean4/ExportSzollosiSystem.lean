import SzollosiExecutableSystem

def main (args : List String) : IO Unit := do
  match args with
  | [output] =>
    IO.FS.writeFile output (MUB.SzollosiExecutableSystem.exportJson.compress ++ "\n")
    IO.println s!"Exported 440 coordinates and 618 equations to {output}"
  | _ => throw (IO.userError "usage: ExportSzollosiSystem.lean <output.json>")

