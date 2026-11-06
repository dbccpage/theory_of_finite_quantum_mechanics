import Lake
open Lake DSL

package «coda_foc» where
  version := v!"3.2.1"

-- Reconstruction FOC algebra (mathlib).
require mathlib from git "https://github.com/leanprover-community/mathlib4" @ "de5ce8a9a66a4aa68a9bdbb35b63a06d34d9ca11"

@[default_target]
lean_lib «coda_foc» where
  srcDir := "."
  roots := #[
    `Foundations,
    `FOC,
    `AxiomAudit,
    `PrimitiveDifference,
    `L20AKernel,
    `TerminalCompleteness,
    `EpkPrimitiveDifference,
    `Algebra,
    `Core
  ]

