/-
  WitnessedDifference/WdpBatch13Rep.lean

  Representative theorems re-exported for Batch 13 derivations (final 5 nodes):
  1. PGW-WDP-BRIDGE-O05-AUTHORIZATION-FIREWALL (WDP, TFQ-0570)
  2. PGW-WDP-MERON-M1-CORRELATION-ESTIMATES (WDP, TFQ-0582)
  3. PGW-WDP-MERON-M2-CUMULANT-BOUNDS (WDP, TFQ-0583)
  4. PGW-WDP-MERON-M3-SPECTRAL-GAP-BYPASS (WDP, TFQ-0584)
  5. PGW-WDP-MERON-SPACETIME-LIMIT (WDP, TFQ-0587)
-/
import WitnessedDifference.WdpBatch13

namespace WitnessedDifference.WdpBatch13Rep

open WitnessedDifference.WdpBatch9
open WitnessedDifference.WdpBatch10
open WitnessedDifference.WdpBatch11
open WitnessedDifference.WdpBatch12
open WitnessedDifference.WdpBatch13

export WitnessedDifference.WdpBatch13 (
  o05_authorization_firewall_and_policy_enforcement_separation
  wdp_meron_m1_scoped_finite_correlation_and_scaling_obstruction
  wdp_meron_m2_scoped_fourth_cumulant_nonselection
  wdp_meron_m3_gate_e_obstruction_and_margin_bypass
  wdp_meron_spacetime_finite_history_trace_and_sign_discrepancy
)

end WitnessedDifference.WdpBatch13Rep
