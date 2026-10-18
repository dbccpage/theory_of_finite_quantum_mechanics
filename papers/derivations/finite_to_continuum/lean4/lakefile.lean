import Lake
open Lake DSL

package «finite_to_continuum» where
  version := v!"0.1.0"

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "de5ce8a9a66a4aa68a9bdbb35b63a06d34d9ca11"

@[default_target]
lean_lib «CharacterOrthogonality» where
  srcDir := "."
  roots := #[`CharacterOrthogonality, `circle_haar, `finite_presentation, `axiom_audit]
