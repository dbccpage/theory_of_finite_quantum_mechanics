# Review verdict: arithmetic accepted; original import signature rejected

The original attachment compiles as received under the project-pinned core Lean 4.33.1, without Mathlib, and reproduces the four reported axiom receipts. No trailing-exact repair was needed. That verifies the actual Lean terms and their dependencies. It does not verify the meanings assigned to the encoded datatypes or the truth of new axioms.

## A kernel-checked inconsistency in the local import interface

`ReconstructionUnsafeDiagnostic.lean` includes the original source and constructs a one-state `System` with a singleton frame, trivial reversible action, `hull=True`, rank 1 and dim 2. Its `Spectral` and `StronglySymmetric` witnesses use no axioms. These values are legal because `System.dim` is an arbitrary natural number and the file does not encode convex geometry or semantic dimension.

The unrestricted `jordan_of_spectral_strongSym` applies to this object and supplies an encoded EJA of rank 1 and dimension 2. Existing arithmetic lemmas prove every well-formed encoded rank-one EJA has dimension 1. Lean therefore checks `unrestricted_bridge_derives_false : False`. Its custom dependencies are exactly `JordanIso` and `jordan_of_spectral_strongSym`, with standard `propext` and `Quot.sound`.

This is a counterexample to the LOCAL AXIOM SIGNATURE over the given `System`, not to Barnum-Hilgert's theorem. The original bridge declaration must not be accepted as a sound import merely because it carries a citation. The diagnostic is audit evidence, not a production theorem or a physical countermodel.

## What the verified arithmetic actually establishes

`SimpleEJA` is a tag datatype; `EJA` is a nonempty list of such tags with validity conditions. No Jordan multiplication, ordered vector space, Hilbert structure, cone, trace pairing or actual algebra isomorphism is constructed.

- `no_simple_dim4m_rank2m` is a valid rank/dimension exclusion over the encoded list.
- `qubit_algebra` validly selects `complexHerm 2` or `spin 3` at rank 2 and dimension 4. It does not construct Herm_2(C) isomorphic to V_3, nor establish the classification itself.
- `real_not_multiplicative` and `quat_not_multiplicative` prove the displayed natural-number inequalities.
- The original `rebit_is_disk` and `quabit_is_5ball` prove dimensions 3 and 6, not disk/ball geometry. The arithmetic extraction renames them accordingly.
- The spin/Albert statements exclude those individual tags as rank-at-least-four hosts. They do not construct or classify an operational composite.
- `composite_rank_mul` is a numerical capacity equation conditional on the reconstruction imports. It does not exhibit a tensor-product isomorphism or monoidal coherence.

`ReconstructionArithmetic.lean` isolates these useful results with no custom axioms. Nineteen printed arithmetic receipts are retained.

## Operational content missing from the original structures

`System` lacks a real vector space, convex subset, compactness, an order unit/effects, actual affine dimension, group laws, affine action laws and a relation between frames and distinguishability. `Composite` lacks bilinearity/affinity and joint product effects; `rank_mul` is an assumed bound rather than a derived product-frame theorem. Its marginal section equations alone do not encode operational no-signalling. `Theory.localTomo` is a dimension equality, not injectivity of joint local statistics. `Theory.comp` has no unit, associator or symmetry data.

The Barnum-Hilgert primary result concerns actual finite-dimensional compact convex sets and affine symmetries; its statement already includes the simple-Jordan-or-simplex dichotomy. Those hypotheses are absent from the bare interface. [Primary abstract](https://arxiv.org/abs/1904.03753).

Barnum-Wilce's cited route also has structured composite hypotheses, including factorizable self-duality (or conditions proving it), yielding the Hanche-Olsen product identities. A numerical dimension equation is not those identities. [Primary paper, Section 1.4 and Proposition 1](https://arxiv.org/html/1202.4513).

The rank-2/dim-4 A4 can be used as a weaker numerical selector AFTER a valid geometric Jordan bridge. It is not by itself a derivation of a physical qubit or a theorem about polarization. Interpreting dim 4 as three normalized real parameters requires the missing affine/order-unit semantics. The Stokes reference remains motivation, not a formal derivation here.

## Dynamics and global equivalence remain open

`JordanIso` and `DynamicsEquivalence` are declared with `axiom`, not defined geometric/dynamical predicates. Lean reports both in the original dependency list along with the five theorem axioms. No effect set, process hom-set, CP extension test, ancillary availability or time topology occurs in `System`. Thus the dynamics bridge assumes the entire advertised missing content.

Classifying affine automorphisms does not establish which processes physically exist. In particular, affine antiunitary symmetries and locally composable CP dynamics need separate treatment. The quoted proper-subgroup dimension argument is not formalized, and `Rev` is not even specified as a closed topological group. It cannot discharge the process bridge in this interface.

Even a genuine theorem that every available object has complex quantum state space does not show that all finite dimensions are available, or identify the full morphism theory. The previously reviewed powers-of-two subtheory distinction remains relevant.

## Repaired conditional file and the classical-exclusion route

`ReconstructionConditional.lean` puts the predicates into explicit parameters and all five bridges into a per-theory `ReconstructionImports` hypothesis, restricted to registered objects. It contains no global custom axioms. The conditional assembly and capacity theorem compile with only standard Lean axioms, but ALL FIVE BRIDGE FIELDS REMAIN ASSUMPTIONS and no instance is constructed. This is a checked implication, not a completed reconstruction or a consistency proof for an intended physical model.

For the elementary classical-exclusion branch, a cleaner argument avoids presuming pure products are pure: an affine surjective image of a finite polytope is a finite polytope. A composite marginal is surjective if a fixed first-system state and the product/marginal section equation exist. A qubit ball is not a finite polytope, so such a composite cannot be a finite simplex. Affinity and the concrete geometry must still be supplied.

The repaired file proves `finite_hull_image` and `no_finite_hull_composite_with_nonpolytope_marginal` with no axioms. Their hull relation, transport law, finite-hull premise and nonpolytope premise are EXPLICIT PARAMETERS. This proves the general interface implication; it does not yet instantiate real convex geometry or replace the original elementary axiom unconditionally.

All originals and prior seals remain intact. No native library was edited, no provider was invoked and no Git publication was performed. Stop for review.
