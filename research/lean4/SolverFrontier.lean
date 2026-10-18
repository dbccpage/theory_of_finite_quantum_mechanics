/-!
# Finite all-co-minima plan frontier

This module formalizes only the selection law used by the Python reference
router.  A caller supplies one explicit finite batch, a verifier bit for each
plan, and a declared strict cost comparison.  The selector retains every
verified plan that is not strictly dominated inside that batch.

It does not prove that the batch exhausts a grammar, that verifier bits are
sound, that costs are physically complete, or that a selected plan has
authority.
  Origin: papers/core/finite_quantum_mechanics.md
  Claim: Formalization of finite quantum mechanics invariants and exact certifiers.
  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

namespace OmegaCore.SolverFrontier

/-- One inert plan and its already-declared verification and cost data. -/
structure Candidate (Plan Cost : Type) where
  plan : Plan
  cost : Cost
  verified : Bool

/-- Batch-relative co-minimality under a caller-declared strict comparison. -/
def onFrontier {Plan Cost : Type}
    (strictlyBetter : Cost → Cost → Bool)
    (batch : List (Candidate Plan Cost))
    (candidate : Candidate Plan Cost) : Bool :=
  candidate.verified &&
    !(batch.any fun other =>
      other.verified && strictlyBetter other.cost candidate.cost)

/-- Executable finite selector. No representative is chosen among ties. -/
def selectFrontier {Plan Cost : Type}
    (strictlyBetter : Cost → Cost → Bool)
    (batch : List (Candidate Plan Cost)) : List (Candidate Plan Cost) :=
  batch.filter (onFrontier strictlyBetter batch)

theorem mem_selectFrontier_iff {Plan Cost : Type}
    (strictlyBetter : Cost → Cost → Bool)
    (batch : List (Candidate Plan Cost))
    (candidate : Candidate Plan Cost) :
    candidate ∈ selectFrontier strictlyBetter batch ↔
      candidate ∈ batch ∧ onFrontier strictlyBetter batch candidate = true := by
  simp [selectFrontier]

theorem verified_of_mem_selectFrontier {Plan Cost : Type}
    (strictlyBetter : Cost → Cost → Bool)
    (batch : List (Candidate Plan Cost))
    (candidate : Candidate Plan Cost)
    (h : candidate ∈ selectFrontier strictlyBetter batch) :
    candidate.verified = true := by
  have hf := (mem_selectFrontier_iff strictlyBetter batch candidate).mp h |>.2
  simp [onFrontier] at hf
  exact hf.1

theorem no_strict_dominator_of_mem_selectFrontier {Plan Cost : Type}
    (strictlyBetter : Cost → Cost → Bool)
    (batch : List (Candidate Plan Cost))
    (candidate : Candidate Plan Cost)
    (h : candidate ∈ selectFrontier strictlyBetter batch) :
    ¬ ∃ other ∈ batch,
      other.verified = true ∧
      strictlyBetter other.cost candidate.cost = true := by
  have hf := (mem_selectFrontier_iff strictlyBetter batch candidate).mp h |>.2
  simp [onFrontier] at hf
  rintro ⟨other, otherInBatch, otherVerified, otherBetter⟩
  have notBetter := hf.2 other otherInBatch otherVerified
  rw [notBetter] at otherBetter
  contradiction

theorem all_verified_coMinima_retained {Plan Cost : Type}
    (strictlyBetter : Cost → Cost → Bool)
    (batch : List (Candidate Plan Cost))
    (candidate : Candidate Plan Cost)
    (inBatch : candidate ∈ batch)
    (verified : candidate.verified = true)
    (minimal : ∀ other ∈ batch,
      other.verified = true →
      strictlyBetter other.cost candidate.cost = false) :
    candidate ∈ selectFrontier strictlyBetter batch := by
  apply (mem_selectFrontier_iff strictlyBetter batch candidate).mpr
  constructor
  · exact inBatch
  · simp [onFrontier, verified]
    intro other otherInBatch otherVerified
    exact minimal other otherInBatch otherVerified

/-- Two separately witnessed co-minimal plans are both retained. Cost equality
is not needed: under a partial order, incomparable costs may also be
co-minimal. -/
theorem coMinima_pair_retained {Plan Cost : Type}
    (strictlyBetter : Cost → Cost → Bool)
    (batch : List (Candidate Plan Cost))
    (left right : Candidate Plan Cost)
    (leftIn : left ∈ batch)
    (rightIn : right ∈ batch)
    (leftVerified : left.verified = true)
    (rightVerified : right.verified = true)
    (leftMinimal : ∀ other ∈ batch,
      other.verified = true →
      strictlyBetter other.cost left.cost = false)
    (rightMinimal : ∀ other ∈ batch,
      other.verified = true →
      strictlyBetter other.cost right.cost = false) :
    left ∈ selectFrontier strictlyBetter batch ∧
      right ∈ selectFrontier strictlyBetter batch := by
  constructor
  · exact all_verified_coMinima_retained strictlyBetter batch left
      leftIn leftVerified leftMinimal
  · exact all_verified_coMinima_retained strictlyBetter batch right
      rightIn rightVerified rightMinimal

#print axioms mem_selectFrontier_iff
#print axioms verified_of_mem_selectFrontier
#print axioms no_strict_dominator_of_mem_selectFrontier
#print axioms all_verified_coMinima_retained
#print axioms coMinima_pair_retained

end OmegaCore.SolverFrontier
