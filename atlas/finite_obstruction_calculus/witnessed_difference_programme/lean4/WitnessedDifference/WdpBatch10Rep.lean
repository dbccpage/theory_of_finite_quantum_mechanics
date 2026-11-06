/-
  WitnessedDifference/WdpBatch10Rep.lean

  Representative-theorem companion module for `WitnessedDifference.WdpBatch10`.
-/
import WitnessedDifference.WdpBatch10

namespace WitnessedDifference.WdpBatch10Rep

open WitnessedDifference.WdpBatch10

abbrev rep_l1_imp_complex_field :=
  @l1_imp_complex_field_selection_and_gaussian_standin

abbrev rep_rung2a_stake_declared_label :=
  @rung2a_stake_declared_label_and_growth_cases

abbrev rep_rung3_first_demand_index :=
  @rung3_first_demand_index_uniqueness_and_countermodels

abbrev rep_rung4_index_up_to_isomorphism :=
  @rung4_uniform_transport_and_nonuniform_escape

abbrev rep_rung5_symmetry_along_history :=
  @rung5_symmetry_step_law_and_both_ways_witness

end WitnessedDifference.WdpBatch10Rep

#print axioms WitnessedDifference.WdpBatch10Rep.rep_l1_imp_complex_field
#print axioms WitnessedDifference.WdpBatch10Rep.rep_rung2a_stake_declared_label
#print axioms WitnessedDifference.WdpBatch10Rep.rep_rung3_first_demand_index
#print axioms WitnessedDifference.WdpBatch10Rep.rep_rung4_index_up_to_isomorphism
#print axioms WitnessedDifference.WdpBatch10Rep.rep_rung5_symmetry_along_history

