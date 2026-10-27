-- COMP-C7-ENCODED-INSTANCE-REDUCTION. Not a default target.
-- The conditional reduction already stated by reach_problem_not_computable.
-- startWord_computable stays a hypothesis.
import GenesisCompUniv

namespace ComputationC7EncodedInstanceReduction

open GenesisComputation
open GenesisComputation.Universal
open GenesisComputation.TMEncoding
open Turing

theorem encoded_instance_reduction
    [Primcodable (Sym G1 (TM1to0.Λ' M1))] (hc : Computable startWord) :
    ¬ ComputablePred (fun w : List (Sym G1 (TM1to0.Λ' M1)) =>
      ∃ w', Reach (Rules M0) w w' ∧ Irreducible (Rules M0) w') :=
  reach_problem_not_computable hc

#print axioms encoded_instance_reduction
#print axioms reach_problem_not_computable

end ComputationC7EncodedInstanceReduction
