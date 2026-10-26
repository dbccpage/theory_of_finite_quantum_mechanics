import Lake
open Lake DSL

package «sn_presentation» where
  version := v!"0.1.0"

@[default_target]
lean_lib «SnPresentation» where
  srcDir := "."
  roots := #[`SnSyntax, `SnCarrier, `SnTheorems, `SnOffImage]
