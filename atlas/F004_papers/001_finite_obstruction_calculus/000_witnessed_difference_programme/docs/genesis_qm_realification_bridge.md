# Genesis and the declared quantum realification bridge

AuthorityEffect: None. This is a finite representation theorem, not a derivation
of complex scalars, Hilbert geometry, quantum probability, or Born selection
from `<>`, difference, or GenesisOngoing. It does not extend Genesis or grant
admission. The proposal/evaluation/admission factorization and ongoing quotient
are owned separately. Existing WDP scopes are CH19-O02, CH19-O03, CH19-O04 and
the nonselection statements CH18-O01 and CH19-N01/N02.

## Declared host and algebra theorem

Declare finite-dimensional complex Hilbert carriers with chosen orthonormal
bases. For any complex m-by-n matrix A=P+iQ, with P,Q real, define

`R(A) = [[P,-Q],[Q,P]] : R^(2n) -> R^(2m)`.

For a vector z=x+iy, its coordinates are `(x,y)`. This ordering is essential.
The fixed real complex structure is
`J_n=[[0,-I_n],[I_n,0]]`, so `J_n^2=-I_(2n)`.

**Theorem 1.** R is injective, real-linear, multiplicative on composable
matrices, preserves identity, and satisfies `R(A*)=R(A)^T` and
`J_m R(A)=R(A) J_n`. For a square matrix,
`Tr_R R(A)=2 Re Tr_C A`.

**Proof.** For A=P+iQ and B=S+iT, AB has real part PS-QT and imaginary
part PT+QS. Block multiplication of R(A)R(B) gives precisely these blocks.
Transposing R(A) gives the block matrix of P^T-iQ^T, which is A*.
The other algebraic assertions follow immediately from the same blocks.
The two diagonal blocks both equal P, proving the trace identity. In
particular the trace formula does **not** say twice the complex trace for
an arbitrary non-Hermitian matrix: A=(1+i) gives real trace2, not 2+2i.
R is not complex-linear with ordinary real scalar multiplication;
`R(iA)=J_m R(A)=R(A)J_n`. These are declarations of complex structure,
not a theorem that an unstructured real carrier selects J. Square matrices
and arbitrary rectangular operators are covered, including non-Hermitian
Kraus operators. No infinite-dimensional trace/exponential assertion is made.

**Theorem 2 (exact image).** A real m-by-n doubled matrix M, meaning size
2m-by-2n, is R(A) for exactly one complex A iff `J_m M=M J_n`.
In particular the square image is exactly the real matrices commuting
with J_n.

**Proof.** Write M in equal-sized blocks `[[U,V],[W,Z]]`. Intertwining with
the two J matrices says `W=-V` and `Z=U`. Thus M=R(U-iV), uniquely.
The rectangular assertion is important for operators between different
carriers; “commutes with J” is appropriate only on a common carrier.

If A is Hermitian, R(A) is real symmetric. Conversely a real symmetric M
commuting with J corresponds to a complex Hermitian A. Positivity is
preserved and reflected: for z=x+iy,
`z*Az=(x,y)^T R(A)(x,y)`, a real scalar when A is Hermitian; all real
vectors occur in this way. These assertions use the declared positive
inner product and selected complex involution. They do not construct them
from a difference relation.

## States, effects, instruments and trace pairing

Declare a complex density state rho, rho>=0 and Tr_C rho=1, and effects
`0<=E<=I`. Set `sigma=R(rho)/2` and `E_R=R(E)`.
Then sigma is a real density state and E_R is a real effect. The factor 1/2
belongs to states, **not** to effects or Kraus operators. For Hermitian E,rho,
`Tr_C(E rho)` is real: its conjugate is `Tr_C(rho E)=Tr_C(E rho)`.
Consequently

`Tr_R(E_R sigma)=Tr_C(E rho)`.

The state map is a bijection between complex density matrices and real
density matrices commuting with J: invert R on a commuting sigma and
multiply the result by2. Its trace is then one by Theorem1. The effect
map is a bijection between complex effects and commuting real effects,
without scaling. Positivity, order, convex mixtures and normalization are
preserved. Complex pure states generally become real rank2 states; this
is an operational density-state equivalence with a restricted real host,
not an identification with unrestricted real pure-state ontology.

**Theorem 3 (finite instrument equivalence).** Let declared outcome maps be
`M_o(rho)=sum_a K_oa rho K_oa*`, where K_oa are finite rectangular operators
and `sum_oa K_oa* K_oa=I`. Put `L_oa=R(K_oa)`.
Then `sum_oa L_oa^T L_oa=I_(2n)`, and on realified states

`M_o^R(sigma)=sum_a L_oa sigma L_oa^T = R(M_o(rho))/2`.

The real outcome effect is `sum_a L_oa^T L_oa=R(E_o)`, where
`E_o=sum_a K_oa* K_oa`. Therefore outcome probabilities agree, are
nonnegative, and sum to one. If their common probability p_o>0, conditional
post-states obey

`M_o^R(sigma)/p_o = R(M_o(rho)/p_o)/2`.

If p_o=0, positivity and trace0 make the unnormalized operator zero;
neither side declares a normalized conditional state. This is an explicit
zero-probability boundary, not an arbitrary choice of post-state.

**Proof.** Apply Theorem1 to every finite sum and product, and apply the
trace identity to the Hermitian unnormalized output. At zero probability,
all eigenvalues of a positive finite operator are nonnegative and sum to0,
so the operator is zero. The assertion needs no square-root normalization.
Nonnegative real Kraus weights can also be retained directly on both sides:
`sum_a w_a K_a rho K_a*` maps to `sum_a w_a R(K_a) sigma R(K_a)^T`.
This includes rational weights whose square roots are irrational.

These are consequences of an already declared CP instrument and trace
pairing. The pairing is the Born operational rule in this model; the proof
preserves it, not derives or uniquely selects it.

## Channel and sequential composition

For finite channels Phi and Psi with Kraus K_a and H_b, the Kraus operators
of Psi after Phi are H_b K_a. Theorem1 gives
`R(H_b K_a)=R(H_b)R(K_a)`, hence

`(Psi after Phi)^R = Psi^R after Phi^R`

on the declared state correspondence. Outcome-resolved sequential
instruments satisfy the same equality with both outcome indices retained.
Marginalizing outcomes is a finite sum and therefore also commutes with R.
The Heisenberg adjoint obeys
`Phi_R*(R(E))=R(Phi*(E))`, so effect transport and Schrödinger state
transport give the same probabilities. This covers arbitrary finite
sequential channel composition, not merely equality of one calibration table.

Realifying a complex mn-dimensional composite gives real dimension 2mn,
whereas the ordinary real tensor of the two doubled carriers has dimension 4mn.
The [local-composition supplement](complex_tensor_balancing.md) now supplies
the explicit balance T, projector P and conditional tensor transport proof.
Operators compress as T(R(A) tensor R(B))T^t/2; products of separately
normalized realified states compress without that extra factor. Arbitrary
complex composite states, including entangled states, have a normalized
balanced lift. The supplied complex structure and tensor product remain
premises. This does not reconstruct tensor ontology from Genesis.

## Why unrestricted real extensions are excluded

The image restriction is substantive. On a doubled qubit carrier,
`diag(1,0,0,0)` is a positive real trace-one state but does not commute
with J_2, hence is not the image of any complex density state. An ordinary
real orthogonal reflection `diag(-1,1,1,1)` likewise does not commute
with J_2. Applied to the realification of a state with nonzero imaginary
coherence, it can produce a state outside the image.

Even preservation of the commuting **state set** is weaker than being
a realified complex CP channel. The real orthogonal matrix
`C=diag(I_n,-I_n)` anticommutes with J_n and implements complex conjugation
on real coordinates. Its real conjugation channel sends R(rho)/2 to
R(conjugate(rho))/2, staying inside the commuting state set. Restricted
to complex Hermitian states this is transposition, which is positive but
not complex completely positive for n>=2: its Choi operator is the swap
operator, with eigenvalue-1 on an antisymmetric vector. Thus valid unrestricted
real dynamics do not automatically recover complex CP dynamics. The
declared Kraus intertwining in Theorem3 pays that additional structure.

Conversely the claim is not that every real Kraus presentation of a channel
with a complex realization must intertwine J term by term. Kraus presentations
can be redundant; this theorem supplies one concrete intertwining presentation
and checks that presentation. It does not state a classification theorem
for all representations of arbitrary real channels.

## Difference countermodels and representation boundary

Two opaque distinguishable reports can be modeled by a classical two-state
carrier, by basis states in a real Hilbert space, or by basis states in a
complex Hilbert space. The difference relation alone distinguishes none of
these choices. A signed normalized report valuation can fail positivity;
declaring a quotient does not exclude it. Even after complex amplitudes and
phase invariance are supplied, amplitudes(1,2) admit quadratic normalized
readout(1/5,4/5) and quartic normalized readout(1/17,16/17).
Existing `phase_readout.rs` verifies that nonselection exactly.

Accordingly the permitted dependency is
`declared WDP realization + complex/Hilbert/instrument/readout hypotheses
 -> operationally equivalent restricted real realization`.
No theorem here replaces those hypotheses by Genesis. Returning a theorem
about the realization to the Genesis core would require the separately
proved faithful reflection/admission bridge; an attractive mathematical
realization cannot itself authorize an extension.

## Production evidence and executable domain

The original native test file is
`omega_engine/crates_rs/tests/omega_quantum_physics/genesis_realification_bridge.rs`.
It reuses `exact_hermitian::realify`, which publicly accepts Hermitian
operators only. To test arbitrary rectangular Kraus operators without
editing native implementation, it forms the Hermitian dilation
`[[0,K],[K*,0]]`, invokes that existing realification, and extracts the
appropriate blocks. All matrix products, positivity, states, channels and
instruments use the existing production owners. There is no floating-point
surrogate or independently duplicated matrix arithmetic engine.

The written theorems cover arbitrary finite complex coefficients. The
executed fixtures use exact Q(i) coefficients and rational Kraus weights;
they verify imaginary density coherences, genuinely complex nontrivial
effects, normalized probabilities and conditional states, rectangular
algebra, the real-part trace qualification, weighted sequential composition,
Heisenberg transport, and refusal of unrestricted real-image extensions.
They do not prove a full analytic scalar-host implementation or unrestricted
real/complex quantum equivalence. The original sequential bridge added no
Python, Lean, native implementation, central manuscript or ledger changes.
The later [tensor supplement](complex_tensor_balancing.md) adds reusable
native balancing, quantum and WDP adapters, selected integer Lean coefficient
proofs and manuscript/teaching updates at their separate scopes.

Production receipt (2026-10-01):

`cargo test -p omega_quantum_physics --test genesis_realification_bridge -j2 --locked --offline`

Result: **4 passed, 0 failed**, using the integration workspace and shared
`CARGO_TARGET_DIR=/workspace/the_symbol_game/omega_engine/crates_rs/target`.
The actual production dependencies compiled normally; existing contract and
upstream compiler warnings were emitted. No gate was bypassed, hash rewritten,
mock mathematics substituted, or network dependency resolution performed.
The test file was individually formatted with the installed rustfmt.
