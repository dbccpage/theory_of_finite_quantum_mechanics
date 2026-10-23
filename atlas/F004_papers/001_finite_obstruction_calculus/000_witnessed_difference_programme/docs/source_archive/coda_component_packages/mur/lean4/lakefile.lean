import Lake
open Lake DSL

package «coda_mur» where
  version := v!"3.1.1"

@[default_target]
lean_lib «coda_mur» where
  srcDir := "."
  roots := #[
    `D01D02D03Records,
    `L01FiniteCoreAction,
    `L02TerminalNonBypass,
    `L03P01T06Soundness,
    `T01CertificatePasting,
    `T02T07Kernel,
    `T03T04T05LossNoCreation,
    `T04LossAlgebra,
    `Algebra,
    `Core
  ]
