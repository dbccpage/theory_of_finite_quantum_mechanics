import Lake
open Lake DSL

package «coda_cs_q» where
  version := v!"3.0.1"

@[default_target]
lean_lib «coda_cs_q» where
  srcDir := "."
  roots := #[
    `D01D02Records,
    `T01FactorizationFiberConstancy,
    `T02BridgeAdmissibility,
    `T03NamedTerminalizers,
    `Algebra,
    `Core
  ]
