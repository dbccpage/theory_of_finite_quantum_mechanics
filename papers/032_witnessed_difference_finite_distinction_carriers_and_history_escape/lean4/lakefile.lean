import Lake
open Lake DSL

package «wd2_finite_distinction» where
  version := v!"0.1.0"

@[default_target]
lean_lib «FiniteDistinction» where
  srcDir := "."
  roots := #[`FiniteDistinction]
