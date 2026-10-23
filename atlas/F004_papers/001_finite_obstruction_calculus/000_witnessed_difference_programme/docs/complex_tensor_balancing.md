# Local composition in the declared quantum realification

This note assigns no authorization and changes no jurisdiction. GEN-WDP-19 is a conditional finite representation
theorem. Complex scalars, Hilbert positivity, density admission, trace pairing
and the complex tensor product are premises. This closes the explicit tensor
transport gap in [the earlier realification bridge](genesis_qm_realification_bridge.md)
under those premises; GEN-WDP-O04 remains open as a reconstruction obligation.

## Carrier, coordinates and balance

Let V=C^m and W=C^n have declared orthonormal bases. Their underlying real
carriers have coordinates `(real, imaginary)`. On their ordinary real tensor,
index `(a*m+i)*(2*n)+b*n+j` has a,b in {0,1}, i<m and j<n. For each (i,j),
write its four coefficients as `(rr,ri,ir,ii)`. Define

`T(rr,ri,ir,ii)=(rr-ii,ri+ir)`.

The target orders all mn real coordinates before all mn imaginary coordinates.
Thus T has shape 2mn by 4mn. It is the real coordinate map of
`v tensor_R w -> v tensor_C w`; expanding `(x+iy)(u+iv)` gives its formula.
For m=n=1 its two rows are `(1,0,0,-1)` and `(0,1,1,0)`.

Put L=J_m tensor I_(2n), H=I_(2m) tensor J_n, with J(x,y)=(-y,x).
On four coefficients L=(-ir,-ii,rr,ri), H=(-ri,rr,-ii,ir). Direct substitution
gives `TL=TH=J_(mn)T`, `L^2=H^2=-I` and LH=HL. Consequently T kills
the balancing relation `(J_m v) tensor w - v tensor (J_n w)`.

**Theorem 1 (exact quotient).** The kernel of T is precisely the span of those
relations. T is surjective and `TT^t=2I_(2mn)`. Over the declared real field,

`P=T^t T/2=(I-LH)/2`

is a symmetric idempotent of rank 2mn. Its image is the balanced subspace,
where L=H, and its kernel is the unbalanced subspace, where L=-H.

**Proof.** On each basis pair, Tv=0 iff rr=ii and ri=-ir. Every such vector
`(a,b,-b,a)` equals `(L-H)(0,0,-a,-b)`. Pure tensors span the ordinary tensor,
so these are exactly the imposed relations. The two rows of each coefficient
block are orthogonal with squared length two; blocks for distinct pairs
have disjoint supports. This proves TT^t=2I, surjectivity and the rank.
Applying T^tT to (rr,ri,ir,ii) gives
`(rr-ii,ri+ir,ri+ir,ii-rr)`, which is `(I-LH)v`. Since (LH)^2=I,
P^2=P. The equations for its two eigenspaces follow from L^2=-I and LH=HL.
The argument also covers empty algebraic carriers, without admitting an
empty density state. The quotient coefficient identities work over any
commutative ring; normalized P requires an invertible two. Positivity
statements below require the real ordered Hilbert host.

## Operators and coherence

For complex rectangular A:C^c->C^a and B:C^d->C^b, write R for the block
realification in the earlier bridge. Multiplying a pure tensor gives

`T_(a,b) (R(A) tensor_R R(B)) = R(A tensor_C B) T_(c,d)`.

**Theorem 2 (operator transport).** Multiplication by T_(c,d)^t and Theorem 1
give the exact normalized compression

`R(A tensor_C B)=T_(a,b)(R(A) tensor_R R(B))T_(c,d)^t/2`.

No positivity or square-matrix assumption is needed. Ordinary products of
the local realified operators preserve the balanced subspace and its
complement. Their restriction to that subspace represents the complex
tensor operator. Adjoint and sequential composition commute with transport,
by the earlier R identities and this intertwining equation.

Balancing is associative with the ordinary tensor associator understood:

`T_(mn,k)(T_(m,n) tensor I_(2k)) = T_(m,nk)(I_(2m) tensor T_(n,k))`.

**Proof.** On the eight real/imaginary coefficient types, in order
`rrr,rri,rir,rii,irr,iri,iir,iii`, both sides return
`(rrr-rii-iri-iir, rri+rir+irr-iii)`. Each basis triple has these same
coefficients. Bilinearity then proves equality for every finite tensor.
Swapping local factors likewise gives the declared complex tensor swap
after swapping the corresponding basis indices. These are coherence laws
of this supplied representation; they do not force a tensor ontology from
an inscription or classify all real quantum models.

## Product states and entangled composites

For admitted local complex densities rho_A and rho_B set sigma_A=R(rho_A)/2
and sigma_B=R(rho_B)/2. Their ordinary real product has trace one. Theorem 2
and its two local factors of 1/2 give

`T(sigma_A tensor_R sigma_B)T^t = R(rho_A tensor_C rho_B)/2`.

There is **no additional 1/2** in this product-state equation. Using the
operator compression factor here would produce trace 1/2.

For any admitted complex composite rho, including entangled rho, put
sigma=R(rho)/2 and define its balanced lift

`X=T^t sigma T/2=T^t R(rho)T/4`.

**Theorem 3 (state and effect transport).** X is positive, trace one,
supported on P, and commutes with the restriction of L. Its inverse view is
`sigma=T X T^t/2`. Conversely a positive trace-one real X supported on P
and commuting with L yields exactly one complex density by that inverse
view and the inverse of R. For declared complex local effects E,F,

`Tr_R((R(E) tensor_R R(F)) X)=Tr_C((E tensor_C F)rho)`.

**Proof.** Congruence preserves positivity. Cyclic trace and TT^t=2I give
Tr(X)=Tr(sigma)=1, and P T^t=T^t proves support. Intertwining proves the
complex-structure condition. Compression followed by lift is PXP=X;
lift followed by compression is sigma. Trace, positivity and the J condition
are preserved in both directions. The earlier inverse realification theorem
then gives the complex density. For effects, cyclic trace turns the left
pairing into
`Tr_R([T(R(E) tensor R(F))T^t/2] sigma)`.
Theorem 2 and the earlier trace-pairing theorem give the claimed probability.
General composite effects use `T^t R(E)T/2` as their representative with
relative identity P. Balanced support alone does not supply the J condition.

A raw product is generally not supported on P. In fact
`Tr(P(sigma_A tensor sigma_B)P)=1/2`: expand P=(I-LH)/2 and use
`Tr(J R(rho))=2 Re Tr(i rho)=0`. Its normalized balanced lift is therefore
`X=2P(sigma_A tensor sigma_B)P`, consistently with the formula above.
Projecting and leaving the result unnormalized loses half the mass.

## Local instruments

Let two admitted complex instruments have finite Kraus families K_oa and
H_pb. Their complex product instrument has Kraus K_oa tensor_C H_pb.
Its compressed real Kraus operators are given by Theorem 2. The inherited
R multiplicativity and adjoint equations prove completeness and, for each
outcome pair, preserve the unnormalized post-state and its trace. Positive
outcome probabilities admit the same normalized conditional state; zero
probability admits none.

Alternatively act on X with the ordinary local real Kraus products
R(K_oa) tensor_R R(H_pb). Their intertwiners preserve balanced support and
the declared complex structure. The adjoint intertwining gives
`(R(K) tensor R(H))T_in^t=T_out^t R(K tensor H)`, so the output is precisely
the balanced lift of the complex output. Finite outcome sums and sequential
composition retain these equalities. CP, locality, allowed effects and
Born pairing remain supplied premises.

## Proof and production owners

[ComplexTensorBalancing.lean](../lean4/WitnessedDifference/ComplexTensorBalancing.lean)
proves fourteen selected integer coefficient laws: the double section,
projector numerator, exact relation kernel, both J intertwiners, local
scalar actions and the eight-coefficient associativity equation. Its
[source-bound receipt](../lean4/complex_tensor_balancing_axioms.txt) lists
only propext and Quot.sound, with no admitted proofs. It does not formalize
the full arbitrary-size matrix, real positivity or trace arguments above.

The reusable exact-field implementation lives in
`omega_engine/crates_rs/omega_linear_algebra/src/exact_field/complex_tensor.rs`.
It checks actual local intertwiners and refuses malformed shapes, overflow,
missing or false inverses of two and exhausted budgets. Characteristic two
is refused for normalized constructions. Whole-function allocation and
scalar-call bounds are checked before scalar work; coefficient bit lengths
and scalar-internal allocation are outside that matrix budget.

The Q(i) quantum adapter owns admitted-density normalization and conversions
in `omega_quantum_physics/src/complex_realification.rs`. Its conversion and
balancing costs share one aggregate preflight. WDP's
`genesis_realification_adapter.rs` retains declared local dimensions, the
view and balanced state. It delegates the
mathematical algorithms rather than selecting a model or extending Genesis.

Focused native evidence comprises six math-owner cases, five quantum cases
and one WDP case. These independently compare rectangular complex tensors,
local Kraus completeness and outputs, an imaginary-coherence Bell density,
local effect probabilities, normalized round trips, half-mass projection
and inclusive resource/refusal boundaries. The earlier four realification
cases are retained as a separate regression surface. Finite Q(i) execution
does not implement arbitrary analytic scalars or prove physical reconstruction.

The [focused native receipt](../evidence/complex_tensor_receipt.json) binds
the actual selected source bytes and executed commands. The full local
spine has 28 modules and 393 selected declarations; the historical
202-declaration Mathlib census is retained at its earlier scope.
