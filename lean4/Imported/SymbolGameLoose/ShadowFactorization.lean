/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.
   Original path : the_symbol_game/lean4/ShadowFactorization.lean
   Original sha256: 4e81ebd53f41c8e55668ce29917a78e16e4ecc9242b52c5f80852350271e608e (bytes as found)
   Imported on    : 2026-10-23
   Module         : Imported.SymbolGameLoose.ShadowFactorization
   Reason         : S(n)
   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;
                    no declaration, proof or comment of the original was edited.
                    Port notes (version drift): none.
   AuthorityEffect: None. -/
import Imported.SymbolGameLoose.ShadowBoundary
/-!
# Paper 043, T1: finite-shadow factorization facade

This module gives Paper 043 stable names for the existing generic shadow
boundary. Every theorem below is a wrapper around an exact theorem from
SnSymbolGameAndPackets.ShadowBoundary; no proof is duplicated and no new
mathematical strength is claimed.
-/

namespace PaperER007

open SnSymbolGameAndPackets

/--
Paper-owned wrapper for
SnSymbolGameAndPackets.no_factor_through_shadow_of_collision.

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
SnSymbolGameAndPackets.bridge_factorization_implies_fiber_invariant.

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
SnSymbolGameAndPackets.shadow_value_descends_iff_fiber_invariant.

The quotient is the existing PrimitiveDifference quotient induced by equality
of shadow values. This wrapper inherits the upstream Quot.sound dependency.
-/
theorem shadow_quotient_descent_iff_fiber_invariance
    {Source Shadow Value : Type}
    (shadow : Source → Shadow) (value : Source → Value) :
    (∃ decode : (shadowPrimitiveDifference shadow).ResidualQuotient → Value,
        ∀ source : Source,
          decode (OmegaCore.PrimitiveDifference.classOf
              (shadowPrimitiveDifference shadow) source) = value source)
      ↔ ShadowFiberInvariant shadow value :=
  shadow_value_descends_iff_fiber_invariant shadow value

#print axioms PaperER007.shadow_collision_blocks_total_decoder
#print axioms PaperER007.shadow_factorization_implies_fiber_invariance
#print axioms PaperER007.shadow_quotient_descent_iff_fiber_invariance

/--
Paper-owned wrapper for
SnSymbolGameAndPackets.coarsening_cannot_repair_shadow_collision.

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
  SnSymbolGameAndPackets.coarsening_cannot_repair_shadow_collision
    fineShadow coarsen value a b hFineCollision hValue

/--
Paper-owned wrapper for
SnSymbolGameAndPackets.augmentation_must_separate_target_collision.

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
  SnSymbolGameAndPackets.augmentation_must_separate_target_collision
    shadow extra value a b hShadow hValue decode hDecode

/--
Paper-owned wrapper for
SnSymbolGameAndPackets.shadow_derived_augmentation_cannot_repair_collision.

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
  SnSymbolGameAndPackets.shadow_derived_augmentation_cannot_repair_collision
    shadow deriveExtra value a b hShadow hValue

/-!
No PaperER007 wrapper is exported for
`target_augmented_shadow_carries_value`: that theorem is the tautological
projection from `(shadow source, value source)`, not a constructive repair
result.
-/

#print axioms PaperER007.shadow_coarsening_cannot_repair_collision
#print axioms PaperER007.shadow_augmentation_must_separate_collision
#print axioms PaperER007.shadow_derived_augmentation_cannot_repair_collision

end PaperER007
