# Finite dynamics, Hamiltonian generators and Noether conservation

AuthorityEffect: None. Replaces the repeated narrative of the teaching drafts.

Three constructions must be kept separate: finite weighted transport,
continuous classical Hamiltonian flow, and an algebraic quantum generator.

## Finite transport

Matrix multiplication composes finite weighted transitions; a path sum expands
the entries of that product. A stochastic kernel preserves the sum of
probabilities under its normalization convention. A unitary matrix preserves
the supplied inner product. Neither property chooses a physical time variable.
A discrete unitary step does not specify a unique continuous generator.
See `FQ-DISCRETE-TIME-STONE-AMBIGUITY` and the conditional
`FQ-GAP-STONE-CONTINUOUS-TIME`.

## Classical Hamilton and Noether

Supply coordinates (q,p), the area form ω=dq∧dp, a C¹ vector field X=(u,v)
and its local flow. If that flow preserves ω, then ∂q u+∂p v=0.
Consequently α=ιXω=u dp−v dq is closed. On a simply connected plane domain,
α=dH, giving q̇=Hₚ and ṗ=−Hq. The potential H is unique up to a constant
on a connected domain. The topology and regularity are hypotheses.

For H=p²/2 the flow is (q,p)↦(q+tp,p). Translation in q preserves both H
and ω. Its Hamiltonian charge is p, and along the trajectory
dp/dt=−∂qH=0. More generally, with the chosen Poisson sign convention,
the charge F of a Hamiltonian symmetry is conserved when {F,H}=0 and F
has no explicit time dependence. This is a stated Hamiltonian form of
Noether conservation, not a derivation of energy or momentum from marks.

## Algebraic Hamiltonian

Supply the full algebra M_d(Q(i)), its adjoint, and a Q(i)-linear derivation
δ satisfying δ(A†)=δ(A)†. For matrix units Eᵢⱼ, set
S=Σⱼδ(Eⱼ₁)E₁ⱼ. Applying Leibniz to EₐᵦEⱼ₁=δᵦⱼEₐ₁ gives
[S,Eₐᵦ]=δ(Eₐᵦ), hence δ=[S,·]. Adjoint preservation implies
[S+S†,A]=0 for all A. Replacing S by (S−S†)/2 leaves δ unchanged.
Then H=iS is Hermitian and δ=−i[H,·]. Any two such Hermitian H differ
by a rational scalar identity. This constructs an algebraic generator;
exponentiation, continuity, a clock and physical energy are additional matters.

Sources: [finite transport](sources/qm_030_finite_weighted_transport_calculus.md),
[path sums](sources/qm_031_finite_path_sum_as_graded_transport.md),
[core dynamics proofs](../10_finite_qm_core/sources/finite_quantum_mechanics_proofs.md#4-dynamics),
[reviewed mathematical sheet](../../../education/hamilton_noether_sources/math_sheet_v5.md).
The [review history and drawings](../../../education/hamilton_noether_sources/start_here.md)
remain available as teaching evidence; reader comprehension is untested.
