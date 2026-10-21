import Lake
open Lake DSL

package «meron_sign_problem» where
  version := v!"0.1.0"

@[default_target]
lean_lib «MeronSignLib» where
  srcDir := "."
  roots := #[
    `MeronCharacter,
    `MeronClusterInvolution
  ]
