import Lake
open Lake DSL

package «DDC» where
  version := v!"1.0.3"
  buildDir := "b"

@[default_target]
lean_lib «Ddc» where
  srcDir := "."
  roots := #[`Ddc]
