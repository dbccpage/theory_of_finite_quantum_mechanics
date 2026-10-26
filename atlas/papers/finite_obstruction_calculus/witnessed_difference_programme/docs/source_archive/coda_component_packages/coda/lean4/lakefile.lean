import Lake
open Lake DSL

package «coda_paper» where
  version := v!"2.0.1"

@[default_target]
lean_lib «Coda» where
  srcDir := "."
  roots := #[
    `Foundations,
    `Boundaries,
    `Coda
  ]
