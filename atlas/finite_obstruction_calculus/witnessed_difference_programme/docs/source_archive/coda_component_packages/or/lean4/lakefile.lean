import Lake
open Lake DSL

package «coda_or» where
  version := v!"1.0.1"

@[default_target]
lean_lib «coda_or» where
  srcDir := "."
  roots := #[
    `D01D02Records,
    `L01NonCreation,
    `L02SupportSieve,
    `T01SquareClassification,
    `T02LimitAuthority,
    `Algebra,
    `Core
  ]
