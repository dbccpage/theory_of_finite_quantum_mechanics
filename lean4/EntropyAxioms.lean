

import EntropyDefs
import EntropyPurity

namespace FiniteQm.C750.B01.AxiomCensus

open FiniteQm.C750.B01

theorem general_d_purity (d : Nat) (hd : 0 < d) :
    (pureOne d hd).is_pure ∧ mixedHalf.is_mixed :=
  ⟨pureOne_is_pure d hd, mixedHalf_is_mixed⟩

theorem pure_term_gamma_vanishes (D b : Nat) :
    gamma_numerator D b [(D, b)] = 0 :=
  gamma_num_of_pure (IsPureTermList.single D b)

theorem zero_weight_entropy_term (log_val : RatFrac) :
    (removable_singularity_term 0 log_val).isZero :=
  removable_singularity_is_zero log_val

#print axioms general_d_purity
#print axioms pure_term_gamma_vanishes
#print axioms zero_weight_entropy_term

end FiniteQm.C750.B01.AxiomCensus

private def l5aProvenance : String :=
  "Origin: lean4/EntropyAxioms.lean Claim: general_d_purity AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
