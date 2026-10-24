import Lake
open Lake DSL

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "v4.35.0"

package «CampaignMajorana» where
  buildDir := "b/campaign-majorana"

-- Separate, non-default target: preserve the exact-source pin of lakefile.lean.
lean_lib CampaignMajoranaCliffordParity where
  roots := #[`CampaignMajoranaCliffordParity]
