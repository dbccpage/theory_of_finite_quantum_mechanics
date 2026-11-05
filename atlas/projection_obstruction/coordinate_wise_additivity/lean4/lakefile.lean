import Lake
open Lake DSL

package «coordinate_wise_additivity» where
  version := v!"0.1.0"
  buildDir := "b"
  packagesDir := "p"

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "56a005855ea17e0b0958f73ec801ae140b0a1679"

@[default_target]
lean_lib «PaperGS003» where
  srcDir := "."
  roots := #[
    `primitive_difference,
    `gs003_core,
    `gs003_coordinate_l1,
    `gs003_su2_curvature,
    `gs003_schatten_orthogonal
  ]
