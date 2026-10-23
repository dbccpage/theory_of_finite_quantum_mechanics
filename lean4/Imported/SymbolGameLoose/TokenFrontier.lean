/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/TokenFrontier.lean
   Original sha256: fb1a9de7271ee6d134d2a0e42d6b39bf606ff33e045ff8fd0f189f84799fd0cb (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.SymbolGameLoose.TokenFrontier
   Reason         : MSS-N
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
/-!
# Token Frontier Arithmetic Fragments

This file proves a cross-product identity, projects a supplied zero-numerator
hypothesis, and counts the complement of a bounded support width. It does not
define a probability distribution, connect retained mass to a finite sum, prove
normalization, or verify a runtime refusal or logit-masking implementation.

AuthorityEffect: None.
-/

namespace MSSN.TokenFrontier

/-- Token identifier within a discrete vocabulary. -/
structure Token where
  id : Nat
  deriving DecidableEq, Repr

/-- Discrete candidate with exact rational base and constrained probabilities. -/
structure Candidate where
  token : Token
  baseNum : Nat
  baseDen : Nat
  constNum : Nat
  constDen : Nat
  den_pos : baseDen > 0 ∧ constDen > 0
  deriving Repr

/-- Retained probability mass as an exact fraction. -/
structure RetainedMass where
  num : Nat
  den : Nat
  den_pos : den > 0
  deriving Repr

/-- A zero numerator in the supplied fraction record. -/
def isZeroMass (m : RetainedMass) : Prop :=
  m.num = 0

/-- Equality of the two cross-products by multiplication commutativity;
    no candidate list or conditioned probability is defined here. -/
theorem single_token_deterministic_collapse
    (t : Token) (num den : Nat) (h_pos : den > 0) (h_num_pos : num > 0) :
    let base_mass := RetainedMass.mk num den h_pos
    let p_const_num := num * den
    let p_const_den := den * num
    p_const_num = p_const_den := by
  intro base_mass p_const_num p_const_den
  dsimp [p_const_num, p_const_den]
  rw [Nat.mul_comm]

/-- Projection of the zero-numerator hypothesis; no runtime refusal is modeled. -/
theorem zero_retained_mass_triggers_refusal
    (m : RetainedMass) (h_zero : isZeroMass m) :
    m.num = 0 := h_zero

/-- Support width and masked count conservation:
    For vocabulary size V and support width |S| ≤ V,
    support_width + masked_count = vocabulary_size. -/
theorem support_partition_conservation
    (V support_width : Nat) (h_le : support_width ≤ V) :
    let masked_count := V - support_width
    support_width + masked_count = V := by
  intro masked_count
  dsimp [masked_count]
  exact Nat.add_sub_of_le h_le

end MSSN.TokenFrontier
