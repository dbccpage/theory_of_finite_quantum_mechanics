import Lake
open Lake DSL

package «wdp_presentation» where
  version := v!"0.1.0"

@[default_target]
lean_lib «WdpPresentation» where
  srcDir := "."
  roots := #[`WdpSyntax, `WdpParser, `GenesisIncidence]

@[default_target]
lean_exe «wdp_parity_check» where
  root := `Main
