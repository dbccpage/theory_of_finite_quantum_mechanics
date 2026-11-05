import Lake
open Lake DSL

package «gs001» where
  version := v!"0.1.0"

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "56a005855ea17e0b0958f73ec801ae140b0a1679"

@[default_target]
lean_lib «GS001» where
  srcDir := "."
  roots := #[
    `gs001_core,
    `gs001_l002_01_direction_independence,
    `gs001_l002_02_gauge_proportional,
    `gs001_l002_03_weighted_edge_sum,
    `gs001_l002_04_uniform_weights,
    `gs001_l002_05_counterexamples,
    `gs001_l002_06_maximal_symmetry,
    `gs001_l002_07_norming_functional_core,
    `gs001_l002_07_norming_functional_alias,
    `gs001_l002_08_weighted_to_unweighted_transition,
    `gs001_l002_09_hahn_banach_discharge,
    `gs001_axiom_audit
  ]

