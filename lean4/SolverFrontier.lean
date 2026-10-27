


namespace ObstructionCore.SolverFrontier

structure Candidate (Plan Cost : Type) where
  plan : Plan
  cost : Cost
  verified : Bool

def onFrontier {Plan Cost : Type}
    (strictlyBetter : Cost → Cost → Bool)
    (batch : List (Candidate Plan Cost))
    (candidate : Candidate Plan Cost) : Bool :=
  candidate.verified &&
    !(batch.any fun other =>
      other.verified && strictlyBetter other.cost candidate.cost)

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

end ObstructionCore.SolverFrontier

private def l5aProvenance : String :=
  "Origin: lean4/SolverFrontier.lean Claim: mem_selectFrontier_iff AuthorityEffect: None Scope Fence: this file does not claim unproved continuum physics and does not inherit authority beyond its proved statements Level: L5"
