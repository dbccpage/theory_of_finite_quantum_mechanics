# Concrete transport and gauge syzygies

AuthorityEffect: None. Continuation from local commit
`180271c6e4450acefb532aa946c5af3bae726e02` on the isolated
`codex/mub6-derivation` branch. The earlier checkpoint receipt describes the
bytes at that commit; it is not a receipt for later versions of its files.

Current validation is bound in the
[continuation receipt](../artifacts/mub6_transport_semantics_20261011_receipt.json).
The [derivation DAG](derivation_dag_20261011.json) records 25 nodes across
branches A-F and six routes, distinguishing required premises from subset
progress. Its references and acyclicity were checked; both decisive outcomes
remain open.

## Concrete transport

`MubMonomialTransport.lean` uses actual complex square matrices. For index set
of cardinality n, `RawHadamard H` requires entrywise squared modulus one and
H* H = nI. `RawMU H U` requires every entry of H* U to have squared modulus n.
`HasRawQuartet H` requires H and two further raw Hadamard matrices with all
three pairwise raw MU conditions.

For row permutation sigma, column permutations tau and upsilon, and unit row
phases r, the common row action satisfies the exact identity

\[
 (T_{\sigma,\tau,r,c}H)^*
 T_{\sigma,\upsilon,r,d}U
 =\bigl(\overline{c_i}(H^*U)_{\tau(i),\upsilon(j)}d_j\bigr)_{ij},
 \qquad (TH)_{ij}=r_i H_{\sigma(i),\tau(j)}c_j.
\]

Unit column phases preserve every entry norm. Transporting both further
bases by the same left action therefore preserves quartet completion.
The inverse permutations and conjugate phases give the reverse implication.
This derives preservation from matrix arithmetic; preservation is not a field
assumed in a transformation record.

`MubQuartetTransportBridge.lean` connects this statement to
`ConcreteSemantics.IsCH6`, `HadamardEquivalent`,
`SzollosiQuadraticSystem.RawCandidates`, and
`SzollosiQuartetSystem.Quartet`. Its validation is recorded separately in the
continuation receipt. The bridge also normalizes an arbitrary actual quartet
by multiplying all bases by the adjoint of its first basis and rescaling the
remaining three by sqrt(6).

The final reduction still takes two explicit mathematical inputs: complete
representative coverage and nonextension for **every** representative. It
does not manufacture either input.

## Exact balance identities

`MubGaugeSyzygy.lean` works over an arbitrary commutative star ring. For
six-by-six A and B, write

\[
 g_{A,j}=A_{0j}-1,\qquad
 R_{B,m}=\sum_k B_{mk}\overline{B_{0k}}-6\delta_{m0}.
\]

The kernel-checked row identity is

\[
 \sum_k(A^*B)_{jk}-6
 =\sum_m\overline{A_{mj}}R_{B,m}
 -\sum_{m,k}\overline{A_{mj}}B_{mk}\overline{g_{B,k}}
 +6\overline{g_{A,j}}.
\]

The column identity is its conjugate with A and B interchanged:

\[
 \sum_j(A^*B)_{jk}-6
 =\sum_m\overline{R_{A,m}}B_{mk}
 -\sum_{m,j}g_{A,j}\overline{A_{mj}}B_{mk}+6g_{B,k}.
\]

Both identities hold before any equations are imposed. Separate Lean
corollaries put each residual in any ideal containing its displayed
generators. Consequently the balances are exact ideal consequences, including
in a polynomial star ring. No Jacobian rank or independence conclusion is
drawn from counting the displayed equations.

## Tao semantic bridge and nonextension source

`MubTaoLaurent.lean` defines the recorded matrix over the actual complex
numbers using omega = -1/2 + i sqrt(3)/2. Integer-pair addition, multiplication,
conjugation, and norm are connected to this interpretation. The checked
conclusion is the squared norm of the sum of column products with integer
exponents given by each balanced mask: it equals nine. The eight displayed
endpoints passed, and the integer-pair comparison uses no axioms. Source hashes
and the 23-module replay scope belong to the continuation receipt.

[Brierley and Weigert, arXiv:0901.4051v2](https://arxiv.org/html/0901.4051v2),
Section 4.1 and Table 1, report 90 vectors unbiased to the identity and the
spectral matrix, with no orthogonal sextuple. Their Equation (33) gives the
phase table used here. Section 3.4 describes error-controlled root
approximations; Section 4.3 separately warns about replacing coefficients
in non-affine-family calculations. A local Tao nonextension replay would
need the elimination certificate, exhaustive real-root isolation, and the
orthogonality obstruction. The Laurent calculation alone supplies none of
those three certificates.

## Pinned classification audit

External source:
[Hadamard6 at 57b03025](https://github.com/mateocardeneswuttig/all_hadamard_matrices_in_dimension_six/tree/57b03025ecbe259e474281f49e201ea7cb474e34).
The downloaded archive has SHA-256
`90b202d4da34649d9a9f3b2c1f7c218b3febbf543e105c18e583e25243a31d5e`.
Its Lean pin is 4.33.0-rc2 and its Mathlib pin is
`51e6992efd06126df61a496bebf8f49482a4e129`, distinct from this project's pins.

The inspected public theorem takes only `IsHadamard H` and returns an actual
finite-corner witness. `IsHadamard` means unit entry norms and HH* = 6I;
equivalence means explicit row/column permutations and unit phases. Finite
corners require nonempty finite sets of invertible adjacent blocks, and the
remaining block is reconstructed as -C E* (B inverse)*. The retained-output
predicate additionally requires unit entry norms for that block.

The reviewed source scanner passed on all 136 project modules. All are
reachable from the public root. The additional option scan found resource
limits, linter settings, and a tactic macro expanding ordinary proofs; it
found no kernel-check bypass setting. These source checks are not a substitute
for replay. The first public-theorem build encountered an out-of-memory
failure in `KarlssonResidualCayley`; its successful predecessors do not verify
the public endpoint. That module subsequently passed a single-worker retry.
The public target is being resumed with one worker; no complete endpoint
replay is claimed at this checkpoint.

The shared Git object pool used when preparing the isolated dependencies
became unavailable. Exact pinned objects were fetched into a scratch pool
owned by this worktree, without changing dependency source files. All eighteen
dependency trees across the two environments then matched their pinned Git
commits with clean status. All 215 extracted external archive files also
matched the pinned archive bytes.

The source explicitly leaves construction comparison, generic reconstruction
geometry, and several seed-domain results outside Lean. A finite fibre for
each fixed four-phase seed is not a finite list of all matrices.

## Remaining decisive obligation

If the classification replay and semantic integration are admitted, the
classification route still needs

\[
 \forall p,B,C,\quad
 \operatorname{Retained}(E(p),B,C)\Longrightarrow
 \neg\operatorname{HasRawQuartet}(\operatorname{completion}(E(p),B,C)).
\]

This ranges over the continuous seed domain and every retained block pair.
Excluding Fourier, Tao, or selected Karlsson/Szollosi subfamilies does not
discharge it. An exact quartet is the competing decisive outcome.

**Supports:** concrete simultaneous-equivalence transport, explicit gauge
residual ideal identities, and the complex Tao Laurent calculation, with the
theorem-specific replay receipt.
**Does not support:** an unconditional quartet exclusion, N(6)=3, or complete
external classification replay from a partial build.
**Narrowest claim:** the recorded matrix identities supply previously missing
links in the reduction; the universal exclusion premise remains open.
**Next test:** finish the external classification replay and integration, then
address a quantified nonextension obligation on the retained-output domain.
