/- Imported so that this repository carries its own Lean evidence.
   Original sha256: 4e81ebd53f41c8e55668ce29917a78e16e4ecc9242b52c5f80852350271e608e (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.LegacyTopLevel.ShadowFactorization
   Reason         : S(n)
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   Renamed        : 2026-10-27, directory and namespace names only (lean4/RENAMES.json).
   AuthorityEffect: None. -/
import Imported.LegacyTopLevel.ShadowBoundary
/-!
# Paper 043, T1: finite-shadow factorization facade

This module gives Paper 043 stable names for the existing generic shadow
boundary. Every theorem below is a wrapper around an exact theorem from
SnPacketGame.ShadowBoundary; no proof is duplicated and no new
mathematical strength is claimed.
-/

namespace LggrFiniteConsequences

open SnPacketGame

/--
Paper-owned wrapper for
SnPacketGame.no_factor_through_shadow_of_collision.

This is an alias of the existing finite collision obstruction, not a new proof.
-/
theorem shadow_collision_blocks_total_decoder
    {Source Shadow Value : Type}
    (shadow : Source → Shadow) (value : Source → Value)
    (a b : Source)
    (hShadow : shadow a = shadow b)
    (hValue : value a ≠ value b) :
    ¬ ∃ decode : Shadow → Value,
        ∀ source : Source, decode (shadow source) = value source :=
  no_factor_through_shadow_of_collision
    shadow value a b hShadow hValue

/--
Paper-owned wrapper for
SnPacketGame.bridge_factorization_implies_fiber_invariant.

It only unpacks the consequence of an already-supplied decoder.
-/
theorem shadow_factorization_implies_fiber_invariance
    {Source Shadow Value : Type}
    (shadow : Source → Shadow) (value : Source → Value)
    (hFactor : ∃ decode : Shadow → Value,
      ∀ source : Source, decode (shadow source) = value source) :
    ShadowFiberInvariant shadow value :=
  bridge_factorization_implies_fiber_invariant shadow value hFactor

/--
Paper-owned wrapper for
SnPacketGame.shadow_value_descends_iff_fiber_invariant.

The quotient is the existing PrimitiveDifference quotient induced by equality
of shadow values. This wrapper inherits the upstream Quot.sound dependency.
-/
theorem shadow_quotient_descent_iff_fiber_invariance
    {Source Shadow Value : Type}
    (shadow : Source → Shadow) (value : Source → Value) :
    (∃ decode : (shadowPrimitiveDifference shadow).ResidualQuotient → Value,
        ∀ source : Source,
          decode (ObstructionCore.PrimitiveDifference.classOf
              (shadowPrimitiveDifference shadow) source) = value source)
      ↔ ShadowFiberInvariant shadow value :=
  shadow_value_descends_iff_fiber_invariant shadow value

#print axioms LggrFiniteConsequences.shadow_collision_blocks_total_decoder
#print axioms LggrFiniteConsequences.shadow_factorization_implies_fiber_invariance
#print axioms LggrFiniteConsequences.shadow_quotient_descent_iff_fiber_invariance

/--
Paper-owned wrapper for
SnPacketGame.coarsening_cannot_repair_shadow_collision.

Post-composing an already-colliding shadow cannot recover the separated target.
-/
theorem shadow_coarsening_cannot_repair_collision
    {Source FineShadow CoarseShadow Value : Type}
    (fineShadow : Source → FineShadow)
    (coarsen : FineShadow → CoarseShadow)
    (value : Source → Value)
    (a b : Source)
    (hFineCollision : fineShadow a = fineShadow b)
    (hValue : value a ≠ value b) :
    ¬ ∃ decode : CoarseShadow → Value,
        ∀ source : Source,
          decode (coarsen (fineShadow source)) = value source :=
  SnPacketGame.coarsening_cannot_repair_shadow_collision
    fineShadow coarsen value a b hFineCollision hValue

/--
Paper-owned wrapper for
SnPacketGame.augmentation_must_separate_target_collision.

Any successful augmentation must separate the displayed colliding pair.
-/
theorem shadow_augmentation_must_separate_collision
    {Source Shadow Extra Value : Type}
    (shadow : Source → Shadow)
    (extra : Source → Extra)
    (value : Source → Value)
    (a b : Source)
    (hShadow : shadow a = shadow b)
    (hValue : value a ≠ value b)
    (decode : Shadow × Extra → Value)
    (hDecode : ∀ source : Source,
      decode (shadow source, extra source) = value source) :
    extra a ≠ extra b :=
  SnPacketGame.augmentation_must_separate_target_collision
    shadow extra value a b hShadow hValue decode hDecode

/--
Paper-owned wrapper for
SnPacketGame.shadow_derived_augmentation_cannot_repair_collision.

An extra coordinate computed only from the colliding shadow remains unable to
separate the target values.
-/
theorem shadow_derived_augmentation_cannot_repair_collision
    {Source Shadow Extra Value : Type}
    (shadow : Source → Shadow)
    (deriveExtra : Shadow → Extra)
    (value : Source → Value)
    (a b : Source)
    (hShadow : shadow a = shadow b)
    (hValue : value a ≠ value b) :
    ¬ ∃ decode : Shadow × Extra → Value,
        ∀ source : Source,
          decode (shadow source, deriveExtra (shadow source)) = value source :=
  SnPacketGame.shadow_derived_augmentation_cannot_repair_collision
    shadow deriveExtra value a b hShadow hValue

/-!
No LggrFiniteConsequences wrapper is exported for
`target_augmented_shadow_carries_value`: that theorem is the tautological
projection from `(shadow source, value source)`, not a constructive repair
result.
-/

#print axioms LggrFiniteConsequences.shadow_coarsening_cannot_repair_collision
#print axioms LggrFiniteConsequences.shadow_augmentation_must_separate_collision
#print axioms LggrFiniteConsequences.shadow_derived_augmentation_cannot_repair_collision

end LggrFiniteConsequences
