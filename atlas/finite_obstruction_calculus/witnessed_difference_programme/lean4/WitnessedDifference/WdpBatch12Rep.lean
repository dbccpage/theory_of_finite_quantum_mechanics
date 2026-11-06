/-
  WitnessedDifference/WdpBatch12Rep.lean

  Representative theorems re-exported for Batch 12 derivations:
  1. PGW-C1-ENGINE-CLASS-144 (GENESIS, TFQ-0474)
  2. PG-WDP-GENESIS-BRIDGE-OBLIGATIONS (WDP, TFQ-0343)
  3. TFQ-0385 (GENESIS, TFQ-0385)
  4. PGW-WDP-BRIDGE-O02-OBSERVER-REPAIR (WDP, TFQ-0567)
  5. PGW-WDP-BRIDGE-O04-TENSOR-RECONSTRUCTION (WDP, TFQ-0569)
-/
import WitnessedDifference.WdpBatch12

namespace WitnessedDifference.WdpBatch12Rep

open WitnessedDifference.WdpBatch9
open WitnessedDifference.WdpBatch10
open WitnessedDifference.WdpBatch11
open WitnessedDifference.WdpBatch12

export WitnessedDifference.WdpBatch12 (
  c1_engine_class_144_and_no_initial
  pg_wdp_genesis_bridge_scoped_finite_slice
  tfq_0385_uniform_rule_erases_separation_and_no_return
  wdp_bridge_o02_scoped_preservation_reflection_characterization
  wdp_bridge_o04_scoped_operational_readout_and_countermodel
)

end WitnessedDifference.WdpBatch12Rep
