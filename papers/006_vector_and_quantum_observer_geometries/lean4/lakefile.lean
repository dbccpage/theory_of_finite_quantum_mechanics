import Lake
open Lake DSL

package «po000» where
  version := v!"0.1.0"

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "56a005855ea17e0b0958f73ec801ae140b0a1679"

@[default_target]
lean_lib «PaperPO000» where
  srcDir := "."
  roots := #[
    `po000_core,
    `projection_transfer,
    `replica_hierarchy,
    `affine_obstruction,
    `double_commutator_rate,
    `schatten_orthogonal,
    `su2_curvature,
    `cptp_monotonicity,
    `mixed_vector_duality,
    `strong_vector_duality,
    `quantum_trace_duality,
    `po000_axiom_audit
  ]
