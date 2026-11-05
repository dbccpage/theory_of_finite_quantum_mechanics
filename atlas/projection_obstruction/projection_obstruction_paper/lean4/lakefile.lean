import Lake
open Lake DSL

package po000_bridge where
  version := v!"6.9.15"

-- Override every transitive package with the existing local cache. Merely
-- making Mathlib local would still let Lake clone its transitive dependencies.
def mathlibCache : System.FilePath :=
  System.FilePath.mk ((get_config? mathlib).getD ".lake/vendor/mathlib")

require batteries from mathlibCache / ".lake/packages/batteries"
require Qq from mathlibCache / ".lake/packages/Qq"
require aesop from mathlibCache / ".lake/packages/aesop"
require proofwidgets from mathlibCache / ".lake/packages/proofwidgets"
require importGraph from mathlibCache / ".lake/packages/importGraph"
require LeanSearchClient from mathlibCache / ".lake/packages/LeanSearchClient"
require plausible from mathlibCache / ".lake/packages/plausible"
require Cli from mathlibCache / ".lake/packages/Cli"
require mathlib from mathlibCache

@[default_target]
lean_lib Po000Bridge where
  roots := #[`Po000JordanLie, `Po000JordanLieImage, `Po000JordanTrace]
