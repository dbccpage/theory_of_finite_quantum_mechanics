/-
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

-- AxiomCensus.lean — purity certificate for the finite entropy carrier
-- Campaign: C750 Block 01 (Target C750-T571)
-- AuthorityEffect: None. Citation: sealed-derivation-v1 (3100c4e).
-- The finite purity statement below is the whole claim. No transcendence axiom is added.

import EntropyDefs
import EntropyPurity

namespace FiniteQm.C750.B01.AxiomCensus

open FiniteQm.C750.B01

/-- General dimension is certified by a spectrum, not by a boolean flag:
    the one-hot state in every positive dimension is pure, and the
    equal two-point state is mixed. -/
theorem general_d_purity (d : Nat) (hd : 0 < d) :
    (pureOne d hd).is_pure ∧ mixedHalf.is_mixed :=
  ⟨pureOne_is_pure d hd, mixedHalf_is_mixed⟩

/-- A pure prime-reduction term has vanishing numerator `G_i = D * b - D * b`. -/
theorem pure_term_gamma_vanishes (D b : Nat) :
    gamma_numerator D b [(D, b)] = 0 :=
  gamma_num_of_pure (IsPureTermList.single D b)

/-- The zero-weight convention contributes nothing to a logarithmic form. -/
theorem zero_weight_entropy_term (log_val : RatFrac) :
    (removable_singularity_term 0 log_val).isZero :=
  removable_singularity_is_zero log_val

#print axioms general_d_purity
#print axioms pure_term_gamma_vanishes
#print axioms zero_weight_entropy_term

end FiniteQm.C750.B01.AxiomCensus
