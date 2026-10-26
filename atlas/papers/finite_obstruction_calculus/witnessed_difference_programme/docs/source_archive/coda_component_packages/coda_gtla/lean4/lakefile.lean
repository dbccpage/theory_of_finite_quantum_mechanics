import Lake
open Lake DSL

package «coda_gtla» where
  version := v!"3.2.1"

@[default_target]
lean_lib «coda_gtla» where
  srcDir := "."
  roots := #[
    `Foundations,
    `A,
    `D01D02Records,
    `T01SpanPullback,
    `T02MasterNormalForm,
    `T03AuthorityFirewall,
    `Algebra,
    `Core
  ]
