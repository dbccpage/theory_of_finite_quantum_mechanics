import Lake
open Lake DSL

package «coda_q» where
  version := v!"3.1.1"

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "de5ce8a9a66a4aa68a9bdbb35b63a06d34d9ca11"

@[default_target]
lean_lib «coda_q» where
  srcDir := "."
  roots := #[
    `D01D02Records,
    `T01ModeDescentFirewall,
    `T02AdmissionDebt,
    `T03ProfileCollision,
    `Algebra,
    `Core
  ]
