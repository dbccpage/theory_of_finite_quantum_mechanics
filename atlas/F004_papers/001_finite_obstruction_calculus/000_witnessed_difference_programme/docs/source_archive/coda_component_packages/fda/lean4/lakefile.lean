import Lake
open Lake DSL

package «coda_fda» where
  version := v!"0.1.1"

@[default_target]
lean_lib «coda_fda» where
  srcDir := "."
  roots := #[
    `GtfdaAuthorityCore,
    `GtfdaAuthorityCoreAudit,
    `Foundations,
    `FDA,
    `Algebra,
    `Core
  ]
