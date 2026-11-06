# Conditional selection of the complex carrier

AuthorityEffect: None. Proposed node status: **CONDITIONAL**. The canonical DAG is unchanged.
Base: `lean-v4-35`, commit `5c6887bf881af025540653b95c5ba345df73b0a4`;
Lean `v4.35.0`, Mathlib `56a005855ea17e0b0958f73ec801ae140b0a1679`.

## Result and necessary corrections to the request

Write K_d(n) = n + d binom(n,2). Over natural d the exact universal result is

    [for every n,m >= 2, K_d(nm) = K_d(n) K_d(m)] iff [d = 0 or d = 2].

The requested iff with only d=2 was false at d=0. With d>0, and hence for the
supplied matrix families d in {1,2,4}, the iff with d=2 is proved. At (2,2),
4+6d=(2+d)^2 gives d(d-2)=0. Conversely K_2(n)=n^2 for every natural n,
so multiplication follows for all n,m. This converse is a universal Lean proof;
the bounded census does not replace it. A single failing nontrivial pair refutes
the universal premise. A passing (2,2) pair plus the proved algebraic bridge is
sufficient here; the invalid P4 proposal substitutes a bare instance check for
that proof. Every d passes when either factor has one level.

Product **spanning alone** supplies only a dimension upper bound. Independent
product preparations and factorized nondegenerate tests supply the lower bound:
choose local bases and dual tests; testing a relation among product preparations
extracts each coefficient, proving independence. Local tomography then identifies
a joint vector by its product-test coordinates. Together these give dimension
multiplication. The new Lean conditional theorem consumes this dimension premise;
it does not derive operational tomography from primitive difference. The existing
TensorCoordinates.TomographicData factor/tomography assumptions explain the bridge.
In particular, the projected quaternionic example below shows why merely spanning
is insufficient.

## Real witness, exactly over Q

Y = [[0,-1],[1,0]], and, in ordered basis (00,01,10,11),

    D = Y tensor Y = [[0,0,0,1], [0,0,-1,0], [0,-1,0,0], [1,0,0,0]].
    rho+ = (I+D)/4,    rho- = (I-D)/4.

D is symmetric and nonzero. For symmetric A,B, trace(Y A)=0 and
trace(D (A tensor B))=trace(Y A) trace(Y B)=0. The two rho matrices
are distinct, symmetric, trace one, and positive semidefinite. Lean proves their
quadratic forms, for arbitrary rational x, equal respectively

    ((x00+x11)^2 + (x01-x10)^2)/4,
    ((x00-x11)^2 + (x01+x10)^2)/4.

Thus all local product tests give identical statistics, while pairing with D gives
+1 and -1. The exact Python and Rust checks verify all principal minors and all
local symmetric basis products. The universal quantification over rational
symmetric A,B and over rational x is kernel-checked; no sampling argument is used.
The real 2 tensor 2 product span has dimension 9 in the 10-dimensional symmetric
joint space.

## Gaussian-rational valid control

The existing TensorTomography.product_span is over R and C, not Q and Q(i).
The new gaussian_product_span uses the repository's BornFable.GaussRat field and
proves, for all finite index types n,m, that every self-adjoint joint matrix lies
in the Q-linear span of local self-adjoint Kronecker products. The proof uses
matrix units and the exact identity

    ReH(A tensor B) = ReH(A) tensor ReH(B) - ImH(A) tensor ImH(B),
    ReH(A)=(A+A*)/2,    ImH(A)=(-i)(A-A*)/2.

For 2 tensor 2 the exact replay obtains 16 independent product directions in
Herm_4(Q(i)). This proof concerns the exact algebraic field, not completeness.

## Two quaternionic product definitions

The rational Hamilton algebra uses i^2=j^2=k^2=ijk=-1. Its local Hermitian
2-by-2 dimension is 6; the proposed same-family Herm_4 dimension is 28, whereas
independent products require 36. The count obstruction is kernel-checked.

For the ordered entrywise Kronecker rule, multiplication is Q-bilinear but the
Hermitian codomain fails: take A=[[0,i],[-i,0]], B=[[0,j],[-j,0]]. The (00,11)
and (11,00) entries of A tensor B both equal k, whose conjugate is -k. Of the
36 local basis products, six are non-Hermitian. Their span in **all** quaternionic
4-by-4 matrices has rational dimension 31; this is not a rank in Herm_4.

The alternative product (A tensor B + (A tensor B)*)/2 is Q-bilinear and
Hermitian-valued. It spans all 28 joint directions but has an 8-dimensional kernel
on the 36-dimensional tensor domain. The displayed nonzero basis tensor maps to
zero. Consequently this rule cannot preserve independent preparation and
factorized nondegenerate testing. It is not excluded by spanning alone. These
explicit quaternion calculations and ranks are finite exact Python/Rust evidence;
only the dimension obstruction is claimed as a Lean quaternion result. No claim
excludes every possible quaternionic composite in other categories.

## P4 semantic boundaries

* Added J: for J=[[0,-I],[I,0]], J^2=-I. Symmetric real matrices commuting with J
  have blocks [[A,-B],[B,A]], with A symmetric and B skew; their dimension is
  n(n+1)/2+n(n-1)/2=n^2. The map A+iB to this block matrix is the exact Q(i)
  realification. Rational scalar action (a+ib)v=av+bJv explicitly reinstates i.
  Complex-balanced composition supplies the n*m complex carrier; an ordinary
  real tensor product of the underlying 2n and 2m spaces has 4nm real dimensions,
  not 2nm. The checker computes J^2, commutants and realification at n=1..4 and
  refuses claims of a purely real scalar structure or ordinary real composition.
  Adding J without the observable restriction and composition rule is insufficient.
* Spin factors: use V_k=R plus R^k, dimension k+1. Counts alone allow an apparent
  joint V_l with l=(k+1)(h+1)-1, and therefore do not exclude these alternatives.
  No admissible product/cone is constructed by this arithmetic. Exclusion of
  additional spin factors is OPEN and supplied in the carrier restriction.
  V_2,V_3,V_5 already coincide with the real, complex, quaternionic 2-level matrix
  Jordan algebras: excluding every spin-factor presentation would also exclude
  the complex qubit. The restriction concerns additional alternatives, direct
  sums/superselection sectors, and the exceptional algebra, not those overlaps.
* n=1 gives K_d(1)=1 for every d and cannot select a field.
* An instance-only evidence label is refused as the universal theorem, while a
  valid (2,2) premise with the universal proof remains accepted.

The Jordan-von Neumann-Wigner classification and Koecher-Vinberg correspondence
are contextual imported results, not proofs here that only three carriers occur.
They require their own hypotheses and do not by themselves remove spin factors,
exceptional possibilities or direct sums. Related stronger reconstruction results
have additional assumptions, including a qubit and conditions on composites:
[Barnum and Wilce](https://arxiv.org/abs/1202.4513). Other composite frameworks
are outside the same-family selection claim:
[Barnum, Graydon and Wilce](https://quantum-journal.org/papers/q-2020-11-08-359/).
Neither literature nor network experiments are verification receipts for this run.

## Evidence and custody

`p1/candidate.json` is the literal checked candidate. `p2/source_pins.json` binds
construction/checker bytes and imported local source files. `p2/` retains failed
build/test attempts as well as final command output. `p4/challenges.json` records
every coordinate/semantic mutant and a passing control using the same checker.
`p5/proposed_node_delta.json` is a proposal; it grants no DAG authority.

The starting worktree contained an unfinished draft and earlier failed logs in
`20261021T161932Z_complex_selection`. Those files were left untouched and were not
accepted as verification. The present record is a local continuation: one researcher
prepared/reviewed the missions and implemented the checkers; the Lean kernel and
separate Python/Rust executables performed verification. There was no independent
human/model review panel or external provider dispatch. P0 review metadata is a
transparent local reconstruction of the reviewed obligations, not a claim of an
earlier sealed provider exchange. Paid provider calls: 0.

## Claim boundary

**Supported:** the exact positive-natural dimension-selection iff, unrestricted
0-or-2 theorem, failing-pair refutation, rational real-state witness, general
Gaussian-rational product span, and conditional selection among the three tags;
finite exact quaternionic product/rank controls and 1..6 dimension census.

**Not supported:** derivation from primitive difference, WDP or <>; a classification
proof; elimination of all spin factors or other composite rules; a continuum
field construction; global physical uniqueness or experimental validation.

**Narrowest defensible claim:** for the supplied R/C/H matrix families with
same-family n*m composites, independent products and local tomography (consumed
as dimension multiplicativity), only d=2 remains. The finite stand-in is Q(i).

**Remaining imports:** the matrix-carrier classification/restriction (including
additional spin-factor, exceptional and direct-sum exclusions), same-family
composition, independent preparations/factorized tests, local tomography, and
real/complex completeness. The sqrt-field and real-embedding choices remain open
under their existing scopes.

**Next test:** establish a field-neutral product-preparation/testing interface
from the repository's operational primitives and prove its injectivity and
state separation, without assuming complex local QM. Alternatively, supply
explicit extra hypotheses excluding the remaining spin-factor alternatives.

GP-IMPORT-COMPLEX-FIELD retains IMPORTED_ASSUMPTION in the proposal because its original claim includes completeness; only its selection subclaim receives the conditional annotation.

Git-byte custody repair: p3/normalization.json records CRLF-to-LF normalization only. The original source pins and accepted receipts remain in p2/source_pins.json and p2/verified/. Final committed-byte source pins are p2/commit_source_pins.json; use p2/replay_commit.py with a new --output directory to replay them.
