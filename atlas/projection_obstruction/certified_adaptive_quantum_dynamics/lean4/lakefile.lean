import Lake
open Lake DSL

package "caqd_lean" where
  version := v!"0.1.0"

@[default_target]
lean_lib «CAQD» where
  srcDir := "."
