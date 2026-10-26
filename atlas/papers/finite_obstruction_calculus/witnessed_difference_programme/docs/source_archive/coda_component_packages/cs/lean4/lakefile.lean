import Lake
open Lake DSL

package «coda_cs» where
  version := v!"1.1.0"

@[default_target]
lean_lib «coda_cs» where
  srcDir := "."
  roots := #[
    `D01D02Records,
    `L01ContinuumNonCreation,
    `L02QueryAuthority,
    `T01FiberConstancy,
    `T02BridgeAdmissibility,
    `Algebra,
    `Core
  ]
