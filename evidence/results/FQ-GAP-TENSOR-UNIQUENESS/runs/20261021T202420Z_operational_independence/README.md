# Operational independence of local tomography

This package constructs two complete finite operational theories satisfying the same explicit causal, convex and compositional laws. The ordinary classical theory is locally tomographic. The finite involutive theory is not: two normalized joint states agree on **every** product of allowed local effects, while an allowed joint effect distinguishes them with probabilities 1 and 0.

The Lean theorem is `OperationalIndependence.operational_independence`. Its scope is the declared operational package below. It does not derive the real carrier, the symmetry restriction, or quantum theory from primitive difference. `AuthorityEffect: None`; this run proposes no canonical DAG mutation.

## Construction and assumptions

A system is a finite nonempty set X with an involutive permutation s. Its real carrier consists of functions v with v(s(x)) = v(x). A state is a nonnegative invariant function whose coordinates sum to one; an effect is an invariant function valued in [0,1]. Probabilities are the ordinary finite pairing sum_x e(x)p(x).

A process X -> Y is a nonnegative matrix T satisfying T(s_Y(y),s_X(x)) = T(y,x). A physical event has column sums at most one; a channel has column sums one. A finite instrument is a family of such processes whose total column sum is one. Unbounded positive processes are useful algebraic objects; they are not all physical events.

Sequential composition is matrix multiplication. Tensor products use Cartesian products of point sets, Kronecker products of matrices, and the **diagonal** involution (s_X,s_Y). The unit is a singleton. Classical registers have trivial involution. Rebracketing, swapping, and unit removal are equivariant permutations.

| Construction choice retained explicitly | What is proved from that choice |
| --- | --- |
| Finite nonempty real carriers with a specified involution | Orbit preparations exist; the positive cone generates the invariant carrier; normalization is faithful; normalized preparations span |
| Nonnegative equivariant matrices; column bounds for events | Positive and invariant action, probability bounds, state preservation, complete ancillary positivity by tensor closure |
| All matrices and instruments satisfying these definitions are admitted | Sequential/parallel closure, finite convex randomization, reset availability, adaptive instruments, coarse-graining, and completion of every event |
| Diagonal composite symmetry | Unit, associative and symmetric tensor laws; naturality, pentagon, triangle, hexagon and interchange for actual process matrices |
| All invariant effects in [0,1] | Global separation of invariant vectors; no restriction to a sampled effect basis in the Lean theorem |
| Equality of transformations retains ancillary distinctions | A normalized diagonal correlation probes every matrix entry; complete operational indistinguishability implies matrix equality |

`OperationalLaws` records 53 proved laws. `operational_laws` supplies every field by a theorem. `Theory` selects systems closed under the unit, all finite nonempty classical registers, tensor products and reversible wiring; it admits every ambient event and instrument between selected systems. `OperationalModel` adds the proved law certificate. This is a concrete class of complete models, not an axiomatization of every conceivable operational theory. Two models within this class suffice to demonstrate independence of local tomography from the listed requirements.

There is no assumption of purification, local complex quantum state spaces, continuous transitivity, a fundamental difference primitive, or a proof that these construction choices follow from the reconstruction programme. Stronger assumptions may exclude this countermodel. No claim is made that a weakest sufficient extra principle has been identified.

## Why tomography fails

An atom has points (a,b) in Bool x Bool. The visible bit is a; the unreferenced flag b is flipped by the involution. Local invariant effects cannot distinguish b from its complement. A composite flips both flags together, so their parity is observable.

With both visible bits fixed to zero, define:

- rho: probability 1/2 on each of the flag pairs (0,0) and (1,1).
- sigma: probability 1/2 on each of the flag pairs (0,1) and (1,0).

Both are positive, invariant and normalized. Every product e x f of local invariant effects has the same value on rho and sigma. The invariant joint effect indicating equal flags has probability 1 on rho and 0 on sigma. `normalized_hidden_witness` proves all these assertions together, with universal quantification over allowed local effects.

The classical subtheory consists of systems with trivial involution. Point-indicator effects are allowed there, and their products read every joint coordinate. `classical_tomography` proves separation on the entire real carrier. The two theories therefore witness both directions of independence; the laws neither force nor forbid local tomography.

## The compositional issue resolved

It is essential to retain processes as equivariant matrices, not quotient them by their action on isolated invariant states. On one atom, identity and flag flip agree on every local state. On an invariant correlated state with an ancilla, they give different joint states. Quotienting these processes locally would make tensor composition ill-defined.

For every finite system A, the normalized diagonal state c(x,z) = delta(x,z)/|A| is invariant. Applying T to its first leg yields T(y,z)/|A|. Since allowed global effects separate invariant output vectors, equality of all such experiment probabilities implies equality of every matrix entry (`ancillary_process_separation`). Thus the distinction is operational, and all wiring equalities are equalities of actual admitted transformations.

The universal no-signalling theorem applies to arbitrary joint vectors and arbitrary allowed local channels, not just product preparations. Every event has an explicit failure branch: prepare a normalized orbit state with weight 1 minus the event's column sum. Finite instruments can be recorded in a classical output register and subsequent channels controlled by that register.

## Relationship to the preceding derivations

PR147 established conditional reset-family, irreducibility and pullback/descent results. A hidden-coordinate pair by itself did not establish a complete theory on all composite systems. This construction supplies that missing model, with a coherent tensor product at arbitrary finite arity and complete instruments.

The new model has globally separating effects, faithful normalization, a generating cone, normalized preparation span, and admitted preparation-after-test resets. These facts are proved directly here; they are not new physical assumptions. Their coexistence with the normalized hidden witness explains why global operational richness does not force product-effect separation. This run does not assert a new formal transport theorem into every interface of `OperationalFilterFamily` or close `FQ-GAP-TENSOR-UNIQUENESS` for the full quantum reconstruction.

## Checks and reproducibility

The three Lean modules separate the carrier/process algebra, coherence/control laws, and the two-model independence result. The replay rebuilds them and the preceding filter/selection/hidden modules, then freshly checks `OperationalIndependence.lean` and audits 61 declarations. Only `propext`, `Classical.choice`, and `Quot.sound` are allowed in the reported axiom dependencies; proof holes and custom axioms are rejected by the audit.

Python uses exact fractions and Gaussian elimination. Rust independently checks orbit partitions and disjoint-support Gram matrices using exact rationals. `construction.py` imports neither checker and reconstructs `candidate.json` byte for byte. Numerical coverage is finite:

| Atoms | Invariant state dimension | Product coordinates | Hidden dimension |
| ---: | ---: | ---: | ---: |
| 0 | 1 | 1 | 0 |
| 1 | 2 | 2 | 0 |
| 2 | 8 | 4 | 4 |
| 3 | 32 | 8 | 24 |
| 4 | 128 | 16 | 112 |

These rows supplement the unrestricted finite-system Lean laws; they do not establish those laws by extrapolation. The negative witness at two atoms already disproves local tomography. Mutation controls test omitted scope premises, wrong primitive types, nested duplicate fields, coordinate changes, malformed orbit coverage, and altered witnesses. The pin guard rejects missing, extra and corrupt source entries.

Run from the repository root with the configured Lean and Rust toolchains, Python with pytest/PyYAML, and cached dependencies:

```text
python -X utf8 dag/results/FQ-GAP-TENSOR-UNIQUENESS/runs/20261021T202420Z_operational_independence/replay.py --output <new-directory>
```

The output directory must not already exist. `source_pins.json` binds all new sources, companions and run inputs plus the 86-source PR147 review chain. Our integration edits among inherited files are limited to the Lake roots and Rust test-module registration. The base advanced during this task when Wigner PR150 merged. The branch was updated to `0364c3c9744e72f05ec6a7ebd14f971f1ddd1c2c`; `upstream_changes.json` records inherited source changes. Historical evidence and canonical DAG files are unchanged relative to that refreshed base. Explicit upstream exceptions must match the corresponding Git blobs at that base. Every command records its arguments, exit status, duration and output digest; failed development attempts remain under `attempts/`.

The accepted results belong to `verified/receipt.json`, with a separate index/blob audit before commit. Checks cover 49 focused Python tests, the full 347-test finite-probability Rust library, Lean and axiom audits, DAG validation and three sync checks, contract histories, candidate reconstruction and mutation controls. This is not a claim that the entire repository test suite was run.

Related background: reference-frame restrictions and relational encodings are discussed by [Bartlett, Rudolph and Spekkens](https://arxiv.org/abs/quant-ph/0610030). A separate study of nonlocally tomographic classical-like theories is [Soltani, Erba, Schmid and Selby](https://arxiv.org/abs/2511.19266). These links provide context; the formal evidence for this particular construction is the source and receipts in this repository. No identification with another paper's exact theory or novelty claim is required.
