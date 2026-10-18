import Lake
open Lake DSL

package «po026» where
  version := v!"1.0.0"

@[default_target]
lean_lib «MajoranaCore» where
  srcDir := "."
  roots := #[`MajoranaCore, `MajoranaGinCore]
