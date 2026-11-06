import Lake

open Lake DSL

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "56a005855ea17e0b0958f73ec801ae140b0a1679"

package witnessed_difference where
  version := v!"0.1.0"
  keywords := #["finite", "witness", "observer", "measurement"]
  buildDir := "b"

@[default_target]
lean_lib WitnessedDifference where
  roots := #[
    `WitnessedDifference,
    `WitnessedDifference.AxiomReport,
    `WitnessedDifference.FiniteDistinction,
    `WitnessedDifference.WdpBatch2,
    `WitnessedDifference.WdpBatch2Rep,
    `WitnessedDifference.WdpBatch3,
    `WitnessedDifference.WdpBatch3Rep,
    `WitnessedDifference.WdpBatch4,
    `WitnessedDifference.WdpBatch4Rep,
    `WitnessedDifference.WdpBatch5,
    `WitnessedDifference.WdpBatch5Rep,
    `WitnessedDifference.WdpBatch6,
    `WitnessedDifference.WdpBatch6Rep,
    `WitnessedDifference.WdpBatch7,
    `WitnessedDifference.WdpBatch7Rep,
    `WitnessedDifference.WdpBatch8,
    `WitnessedDifference.WdpBatch8Rep,
    `WitnessedDifference.WdpBatch9,
    `WitnessedDifference.WdpBatch9Rep,
    `WitnessedDifference.WdpBatch10,
    `WitnessedDifference.WdpBatch10Rep,
    `WitnessedDifference.WdpBatch11,
    `WitnessedDifference.WdpBatch11Rep,
    `WitnessedDifference.WdpBatch12,
    `WitnessedDifference.WdpBatch12Rep
  ]


