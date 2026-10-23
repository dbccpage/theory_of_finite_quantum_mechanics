import Lake
open Lake DSL

package «gs002» where
  version := v!"0.1.0"
  buildDir := "b"
  packagesDir := "p"

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "56a005855ea17e0b0958f73ec801ae140b0a1679"

@[default_target]
lean_lib «GS002» where
  srcDir := "."
  roots := #[
    `gs002_core,
    `gs002_l003_01_triangle_separation,
    `gs002_l003_02_s_ok_local_gauge,
    `gs002_l003_03_weighted_cycle_quotient,
    `gs002_l003_04_edge_decomposition,
    `gs002_l003_05_mixed_closure_bound,
    `gs002_l003_06_mixed_duality_weak,
    `gs002_l003_07_cycle_exactness
  ]
