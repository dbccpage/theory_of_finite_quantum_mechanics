import Lake
open Lake DSL

package «coda_a» where
  version := v!"0.1.0"

@[default_target]
lean_lib «coda_a» where
  srcDir := "."
  roots := #[
    `Foundations,
    `A,
    `D01D02Records,
    `T01AnomalonTerminal,
    `T02ResidualNonCreation,
    `T03ToyAnomalonWitness,
    `Algebra,
    `Core
  ]
