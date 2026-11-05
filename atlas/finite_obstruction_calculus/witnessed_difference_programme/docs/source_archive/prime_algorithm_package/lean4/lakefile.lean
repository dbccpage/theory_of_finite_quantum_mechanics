import Lake
open Lake DSL

package «Prime» where
  version := v!"1.0.0"
  buildDir := "b"

@[default_target]
lean_lib «Prime» where
  srcDir := "."
  roots := #[`Prime]
