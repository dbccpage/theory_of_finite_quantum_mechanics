import Lake
open Lake DSL

package "coda_higher_cell_lean" where
  version := v!"0.1.0"

@[default_target]
lean_lib «HigherCell» where
  srcDir := "."
  roots := #[`HigherCell]
