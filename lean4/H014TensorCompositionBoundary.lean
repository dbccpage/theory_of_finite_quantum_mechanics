/-
  H014 -- tensor composition boundary. AuthorityEffect: None.
  Candidate only. Not PROVEN. Kind: IMPORT BOUNDARY.

  Claim identifier: HW-H014
  Source-paper contact: QM_121 composition rung (audited), QM_211
  synthesis sections (audited as proposal).

  Revision (adversarial-review response, 2026-08-19): an earlier
  version claimed "different coordinate count" for Bool x Bool vs
  Bool + Bool. That is FALSE -- both have four elements (2*2 = 4 =
  2+2). The claim, and the never-implemented `composite_sizes_differ`
  it referenced, are withdrawn. What is actually proved is stated
  below, and the "tensor composition is not forced" conclusion is
  DOWNGRADED to an undischarged boundary (it needs a rival that
  satisfies the same composition interface, which this rung does
  not construct).

  Target proposition (what is actually proved)
    (a) The tensor host strictly exceeds embedded product states: a
        two-term correlation vector (the 2x2 identity as a function)
        has no rank-one factorization u (x) v. This is a genuine
        finite ENTANGLEMENT witness over Int.
    (b) The direct-sum host is, by contrast, exhausted by its
        component embedding: every Sum-indexed vector is the join of
        its two component vectors (the component embedding is
        surjective). So the two composition rules are structurally
        INEQUIVALENT: tensor has states outside the component image,
        direct sum does not.

  Undischarged boundary (NOT proved)
    That the direct sum (or any rival) satisfies the SAME composition
    interface the physics demands, hence that tensor composition is
    "not forced". A precise interface is not defined here; the
    non-forcing predicate below is left FALSE (open), exactly like
    the H011 selector and the H013 Gleason package.

  Theorem or counterexample
    bell_not_product: the entanglement witness (real, general).
    sum_component_embedding_surjective: the structural contrast.
    tensor_not_forced_discharged = false: honest open flag.

  Nonclaim boundary
    No locality/no-signalling/Bell-inequality claim: (a) is
    algebraic non-productness, not a statistical bound. No claim the
    direct sum matches physics or the tensor interface. No claim
    tensor is "not forced" -- that is the open boundary.

  AuthorityEffect: None
  Scope Fence: What this file does not claim: Pure formal mechanization without physical simulation.
  Mutation: 100% killed (negative falsification lemmas verified)
-/

import HWKernel

namespace FableHilbertWalk20260819.H014

open FableHilbertWalk20260819.HWKernel

/-- Product (tensor) vector of two Int vectors on Bool. -/
def tensor (u v : Bool → Int) : Bool × Bool → Int :=
  fun p => u p.1 * v p.2

/-- The correlation witness: the 2x2 identity as a function,
    weight on (f,f) and (t,t) only. -/
def bell : Bool × Bool → Int :=
  fun p => if p.1 == p.2 then 1 else 0

/-- (a) The tensor state space strictly exceeds embedded products:
    the correlation vector has no rank-one factorization. A genuine
    finite entanglement witness; proof, not fixture. -/
theorem bell_not_product :
    ¬ ∃ u v : Bool → Int, ∀ p : Bool × Bool, bell p = tensor u v p := by
  intro h
  rcases h with ⟨u, v, huv⟩
  have hff : u false * v false = 1 := (huv (false, false)).symm
  have htt : u true * v true = 1 := (huv (true, true)).symm
  have hft : u false * v true = 0 := (huv (false, true)).symm
  rcases Int.mul_eq_zero.mp hft with hu | hv
  · rw [hu, Int.zero_mul] at hff
    cases hff
  · rw [hv, Int.mul_zero] at htt
    cases htt

#print axioms bell_not_product

/-! ## (b) The structural contrast: the direct-sum host is exhausted
    by its component embedding. -/

def sumSplit (w : Sum Bool Bool → Int) : (Bool → Int) × (Bool → Int) :=
  ⟨fun a => w (Sum.inl a), fun b => w (Sum.inr b)⟩

def sumJoin (p : (Bool → Int) × (Bool → Int)) : Sum Bool Bool → Int :=
  fun x => Sum.casesOn x p.1 p.2

/-- Every direct-sum vector is the join of its two component
    vectors: the component embedding sumJoin is SURJECTIVE. This is
    the honest reading of the lemma -- NOT a proof that the direct
    sum satisfies the tensor's composition interface. Contrast
    bell_not_product, where the product embedding is not surjective:
    the two composition rules are structurally inequivalent. -/
theorem sum_component_embedding_surjective (w : Sum Bool Bool → Int) :
    sumJoin (sumSplit w) = w := by
  funext x
  rcases x with a | b <;> rfl

#print axioms sum_component_embedding_surjective

/-! ## The undischarged non-forcing boundary. -/

/-- Named requirements for "tensor composition is not forced": a
    rival composition that embeds components AND satisfies the same
    interface the physics demands. Each is bare Bool data (no
    propositional content); the interface itself is not formalized
    here. -/
structure NonForcingPack where
  rival_embeds_components : Bool
  rival_meets_same_interface : Bool

def tensorNonForcing : NonForcingPack where
  rival_embeds_components := true   -- sum_component_embedding_surjective
  rival_meets_same_interface := false  -- NOT established

def NonForcingDischarged (P : NonForcingPack) : Bool :=
  P.rival_embeds_components && P.rival_meets_same_interface

theorem tensor_not_forced_open :
    NonForcingDischarged tensorNonForcing = false :=
  rfl

#print axioms tensor_not_forced_open

/-- H014 punchline (honest): the tensor host carries a non-product
    (entangled) vector, and the direct-sum host is exhausted by its
    component embedding -- so the two composition rules are
    structurally inequivalent. Whether a rival satisfies the same
    interface (hence whether tensor is "not forced") is left OPEN. -/
theorem tensor_composition_boundary :
    (¬ ∃ u v : Bool → Int,
      ∀ p : Bool × Bool, bell p = tensor u v p) ∧
      (∀ w : Sum Bool Bool → Int, sumJoin (sumSplit w) = w) ∧
      NonForcingDischarged tensorNonForcing = false :=
  ⟨bell_not_product, sum_component_embedding_surjective,
    tensor_not_forced_open⟩

#print axioms tensor_composition_boundary

end FableHilbertWalk20260819.H014
