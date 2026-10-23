import Lake
open Lake DSL

package «wdp_paper_001» where
  version := v!"0.1.0"

require «sn_presentation» from "../../../../../../omega_engine_education/documentation/002_oesn/lean4"

@[default_target]
lean_lib «WdpPaper001» where
  srcDir := "."
  roots := #[`Paper001, `SnCarrierDischarge]
