import Lake

open Lake DSL

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "56a005855ea17e0b0958f73ec801ae140b0a1679"

package witnessed_difference where
  version := v!"0.1.0"
  keywords := #["finite", "witness", "observer", "measurement"]
  buildDir := "b"

@[default_target]
lean_lib WitnessedDifference where
  roots := #[`WitnessedDifference, `WitnessedDifference.AxiomReport]
