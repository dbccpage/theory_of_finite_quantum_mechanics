import Lake
open Lake DSL
package projection_bounds
require rsi_mathlib_vendor from "projection_vendor"
@[default_target]
lean_lib ProjectionBounds where
  roots := #[`ProjectionBounds]
