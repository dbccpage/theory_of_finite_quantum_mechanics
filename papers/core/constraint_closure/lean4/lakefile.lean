import Lake
open Lake DSL

package gr002 where
  version := v!"0.1.0"
  keywords := #["math", "simplicial", "exterior-calculus", "l1-norm", "regge-calculus"]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "v4.34.0-rc1"

@[default_target]
lean_lib GR002 where
  srcDir := "."
  roots := #[`GR002]
