# [TFQ-0413] Countermodels and the interaction assumption boundary

**Stage:** `TENSOR_COMPOSITION` | **Status:** `PROVED_LEAN` | **AuthorityEffect:** None.

**Parent:** [TFQ-0412](tfq_0412_tensor_controlled_shift_reconstruction.md)
**DAG node:** `TENSOR-ASSUMPTION-COUNTERMODELS`
**Required DAG inputs:** `TENSOR-TOMOGRAPHIC-COORDINATES`, `TENSOR-CONTROLLED-SHIFT-RECONSTRUCTION`, `TENSOR-BINARY-EFFECT-INTERVAL`

The verified result is a collection of explicit countermodels to weakened
hypothesis packages. It does not derive local complex quantum mechanics,
classify arbitrary operational theories, or prove that every reconstruction
premise is logically minimal. Effect saturation and finite-test saturation
remain separate premises of TFQ-0415 and TFQ-0416; no countermodel here removes them.

## Tomography and local reversibility do not select the state cone

On the supplied real space `Herm(n × m)` of complex Hermitian matrices, define
`sep` as the full conic hull of positive product matrices and `BlockPositive H`
by nonnegative trace pairing with **every** pair of local positive matrices.
`blockPositive_iff_dual_sep` proves that BP is exactly the trace dual of SEP.
`sep_positive`, `sep_ppt`, and `positive_blockPositive` establish the inclusions
used below. These definitions quantify over full cones, without a finite test
sample or an assumed SEP/BP-to-PSD equality.

`sep_local`, `bp_local`, and `twisted_local` prove preservation by local matrix
conjugations, and therefore by local unitaries. `conjMap_inverse` and
`conjMap_trace` supply reversibility and trace normalization for unitaries.
`binary_product_statistics_separate` proves local tomography on the underlying
joint carrier using actual binary local effects; its proof decomposes Hermitian
probes into positive parts and scales positive probes into the binary interval.
This is matrix-level separation, not a claim that arbitrary operational effect
sets are saturated. The inherited trace-product factorization is
`TensorTomography.pairing_product`.

For two qubits let

    B = (1/2) |00+11><00+11|,   W = Gamma(B),

where Gamma transposes the first tensor factor. Lean proves B is positive and
not separable, W is block-positive, and

    <01-10| W |01-10> = -1.

Thus W is not positive. `cone_separations_all_dimensions` embeds these witnesses
into every pair of finite local dimensions n,m >= 2, retaining positivity,
nonseparability, block positivity, and failure of matrix positivity.

The interaction failures use the exact two-qubit controlled shift C from
TFQ-0412. `sep_fails_controlled_shift` maps the separable normalized preparation
`seed = |+><+| tensor |0><0|` to B. `bp_fails_inverse_controlled_shift` tests
C-dagger W C against the positive product projector on the unnormalized vector
`|-,1>` and obtains -1. SEP fails forward closure; BP fails inverse closure.
These are the preservation directions in the cone theorem, without assuming
state-cone self-duality. The general-dimensional theorem concerns cone
separation; the explicit calibration and preservation failures are two-qubit
counterexamples, which suffice to refute the corresponding universal claim.

## A reversible interaction does not determine the fixed coordinate convention

`TensorPartialTranspose.gamma` is a real linear involution preserving trace and
the trace pairing. Define `twisted = {H | Positive (gamma H)}`. The proved
`twisted_eq_image` identifies it with Gamma(PSD), and `twisted_self_dual` proves
self-duality in the trace pairing. It contains all positive product matrices
and lies in BP. The covariance theorem is

    Gamma(Ad_(U tensor V)(H)) = Ad_(conj(U) tensor V)(Gamma(H)).

The map `twist R = Gamma Ad_R Gamma` preserves this cone. For supplied unitary R,
`twist_reversible` and `twist_trace` give an inverse and trace preservation.
`twist_path_continuous` proves continuity whenever a continuous matrix path is
supplied; unitarity at each time is a separate premise for reversibility.
No path's existence or physical availability is derived from primitive data.

This cone differs from PSD in the fixed coordinates because it contains W.
It is order-isomorphic to PSD by Gamma, so this is not a classification of an
inequivalent abstract theory. `twisted_fails_ordinary_calibration` shows that
the twisted controlled shift is available on this cone while the ordinary
controlled shift sends `seed` outside it.

`twisted_same_classical_table` proves agreement on every computational-basis
input. For the local binary effect P = |+i><+i|, the coherent product test P
tensor P instead gives **0** for Ad_C(seed) and **1/2** for the twisted output
(`imaginary_effect_binary`, `coherent_calibration_separates`). Classical truth
tables therefore do not supply the complete calibration required in TFQ-0412.

Dephasing after Ad_C is positive and trace preserving and also passes every
classical-basis input. The product test |+><+| tensor |+><+| gives **1/2** before
dephasing and **1/4** after it. `dephased_controlled_shift_not_injective` proves
that the composed operation is not reversible. These are exact scalar and
matrix identities checked by Lean, not floating-point comparisons.

## Removing tomography admits hidden joint coordinates

`TensorHiddenCoordinates` constructs `Doubled d = Herm d × Herm d`, with cone
PSD × PSD and unit Tr(X)+Tr(Y). Product preparations place half of A tensor B
in each summand. Product tests pair E tensor F with X+Y. The curried linear
maps `prepare` and `test` are bilinear in the local arguments, and
`independent_probabilities` proves factorization. Positive preparations,
nonnegative product tests and the deterministic trace unit are checked.

Componentwise unitary conjugation preserves positivity, has the stated
inverse, and gives the ordinary product statistics on split preparations.
For any positive trace-one rho, `hidden_normalized_states` gives two distinct
normalized positive states (rho,0) and (0,rho) agreeing on every product test.
The first-summand trace separates them. `basis_state_normalized` supplies such
a rho from any basis index, making nonemptiness explicit. `no_local_tomography`
and `dimension_doubled` certify failure of separation and twice the real
dimension of the Hermitian carrier. Hence this example fails exactly the
separation condition used to identify joint operational coordinates.

## Proof boundaries

| Claim | Verified scope and remaining premise |
|---|---|
| SEP/BP and twisted cones | Arbitrary finite complex local matrix carriers; full positive-test quantifiers, local preservation, duality and binary-test separation. |
| Cone separation | All finite n,m >= 2, by explicit isometric embeddings of the two-qubit witnesses. |
| Gate calibration failures | Exact two-qubit controlled shift; coherent binary product tests distinguish operations with the same classical table. |
| Reversible twisted dynamics | A supplied unitary, or a supplied continuous path with unitary values; physical availability is not derived. |
| Hidden-coordinate states | Any finite joint index type with a positive trace-one state; an index supplies a concrete basis state. |
| Effect availability | No operational saturation is inferred from positivity or matrix-level binary bounds. |
| Other commentary | Topological closedness of SEP, a full operational-model packaging, and logical minimality of the full reconstruction package are not new Lean results here. |

The published identical-qubit reconstruction of de la Torre, Masanes, Short
and Mueller, [Deriving quantum theory from its local structure and reversibility](https://arxiv.org/abs/1110.5482),
remains an **external theorem**. Its larger-family composition assumptions are
not a theorem about an isolated arbitrary-dimensional pair and are not included
in this Lean verification. `FQ-GAP-TENSOR-UNIQUENESS` remains `CONDITIONAL`.

## Verified sources and replay

- [Partial transpose and conjugation](../../../lean4/TensorPartialTranspose.lean)
- [Full cones, duality, tomography and twisted dynamics](../../../lean4/TensorCountermodelCones.lean)
- [Exact calibration and preservation witnesses](../../../lean4/TensorCountermodelWitnesses.lean)
- [Embeddings into all larger local dimensions](../../../lean4/TensorCountermodelEmbeddings.lean)
- [Hidden-coordinate countermodel](../../../lean4/TensorHiddenCoordinates.lean)
- [Fresh replay and source hashes](../../research/tensor_countermodel_validation.json)
- [Replay script](../../research/replay_tensor_countermodels.py)

The receipt records the precise Lean/Mathlib versions, source hashes, compiler
outputs and axiom audits. Only standard Lean logical axioms are accepted;
there are no admitted proofs or custom axioms in this dependency replay.
