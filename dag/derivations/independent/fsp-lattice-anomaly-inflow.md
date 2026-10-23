Status: AI-drafted, awaiting human review.

# Finite Wilson slabs: a fixed-basis obstruction, not anomaly inflow

AuthorityEffect: None. Target: FSP-LATTICE-ANOMALY-INFLOW, still OPEN.
Provisional campaign class: **Narrowed**; the reviewer decides. The finite
construction below fails to realize the requested chiral cancellation. It is
not a counterexample to the existence of a different lattice regulator.

## Geometry, field and fermions

Use a three-dimensional Euclidean box
`{0,...,w-1} x {0,...,w-1} x {0,...,h-1}`, with open boundaries in every
direction. The explicit cases are `(w,h)=(2,3),(2,4),(3,3)`. The end surfaces
`z=0,h-1` are two-dimensional; lateral faces are retained in the chain boundary.
There are two spin components per site. Site order is lexicographic `(x,y,z)`;
spin order is up, down. No thermodynamic limit, periodic identification, or
claim of isolated chiral zero modes is made.

Take lattice spacing and Wilson parameter equal to one. Put
`m(z)=-1` when `2*z<h`, and `m(z)=+1` otherwise. For positive nearest-neighbor
edges `v -> v+e_mu`, let `U_v,mu = i^n_v,mu`, where the integer `n` specifies
the rational lift `a=n/4`. Use Pauli matrices

```
sigma_x = [[0,1],[1,0]]
sigma_y = [[0,-i],[i,0]]
sigma_z = [[1,0],[0,-1]].
```

The Wilson operator is specified entrywise, not by prescribing its determinant:

```
D_vv       = (m(z)+3) I
D_v,v+e_mu = -(I-sigma_mu) U_v,mu / 2
D_v+e_mu,v = -(I+sigma_mu) conjugate(U_v,mu) / 2.
```

All omitted entries, including exterior hops, vanish. These matrices lie in
Q(i); the links have unit norm. This is a Wilson regulator with a mass sign
jump, not a proof that a finite box carries the continuum chiral spectrum.

For vertex lifts `alpha=q/4`, let `g_v=i^q_v`. Transform the links by
`a'_vw=a_vw+alpha_w-alpha_v`, hence `U'_vw=g_v^-1 U_vw g_w`.
The spin-independent diagonal matrix `G` then gives `D'=G^-1 D G`.
`hopping_covariant` establishes the corresponding entry identity for arbitrary
fixed hopping coefficients; `transport_mul` and `det_transport` establish
matrix composition and determinant invariance over any commutative ring.
This is a background U(1) gauge change acting on a candidate chiral block.
It is not an axial field rotation with a separately specified Grassmann Jacobian.

## Boundary and bulk determinants

Let B contain both spin components on both end surfaces, and I the intermediate
layers. In block notation set `A=D_BB`, `B0=D_BI`, `C0=D_IB`, `C=D_II`.
The independent checker refuses a singular C; otherwise it verifies both
inverse identities and forms `S=A-B0 C^-1 C0`. The exact determinant
factorization `det D = det C det S` is checked from separately computed
determinants. Here det C is the actual interior determinant and det S the
boundary effective determinant obtained by eliminating the interior.
Both have gauge variation zero. Their product is gauge invariant, but this
zero-plus-zero result is not evidence of anomalous inflow or an induced CS term.

To attempt a Weyl boundary determinant, choose one source and one target spin
at each end site: source up and target down on the bottom, source down and
target up on the top. Denote the corresponding square submatrix of S by K.
This is a fixed-basis chiral truncation; it is not identified with a regulated
Weyl determinant line. The checker also verifies that S does not anticommute
with the sitewise sigma_z matrix. In particular, exact chiral symmetry is not
being silently attributed to this Wilson regulator.

Row and column bases of K have identical gauge charge at each site, so
`K'=G_B^-1 K G_B` in these bases and `det K'=det K`.
`chiral_fixed_basis_det` states this obstruction for arbitrary finite fixed
bases with the same site charges. `transport_inverse` and `schur_covariant`
show that elimination preserves covariance whenever the inverse certificate
exists. The Lean development does not construct or kernel-evaluate the
explicit Wilson determinants; those are independently checked in SymPy.

## A specified lattice CS candidate and its exact variation

Triangulate every elementary cube by its six monotone coordinate paths,
oriented with the sign of the coordinate permutation. Vertices use the same
lexicographic order. Extend the axial link lifts to each diagonal edge by
the x-then-y-then-z path. This extension commutes with addition of `d alpha`.
Define `F_ijk=a_jk-a_ik+a_ij` and the *lifted level-one cup-product candidate*

```
S_CS(a) = (1/2) sum_[0123] orientation * a_01 F_123.
```

The normalization is a definition. Identification with the effective action
of the Wilson interior is not assumed or derived. It is deliberately tested
as a candidate, and it fails below. In particular this is not a complete
compact U(1) lattice CS theory with its integer-cochain data and counterterms.

`curvature_gauge` gives `F'=F`; `bianchi` gives `dF=0`. On a tetrahedron,

```
Delta S_CS = (alpha_1-alpha_0) F_123 / 2
           = (alpha_1 F_123-alpha_0 F_023
              +alpha_0 F_013-alpha_0 F_012) / 2.
```

The latter is the signed boundary pairing. `cs_cell_variation` and
`cs_chain_variation` prove the formula for arbitrary rational cochains and
finite signed tetrahedral chains. The checker constructs all triangular
faces and cancels interior faces independently. Lateral faces are included.

For the two width-two boxes, the only nonzero axial lift is `1/4` on
`(0,0,1)->(0,1,1)`; alpha is `1/4` at `(0,0,0)` and zero elsewhere.
For the width-three box, the active link is `(1,1,0)->(1,2,0)` and alpha
is `1/4` at `(1,1,0)`. The latter transformation is zero on every lateral
face, so missing side inflow cannot explain that witness.

In each case `S_CS(a)=0` and `S_CS(a')=1/32`.
`slab_three_cs` and `slab_four_cs` compute the width-two actions from the
coordinate construction in Lean; the width-three value is SymPy evidence.
No signed charge pair was inserted to make the result cancel.

Use the named cyclotomic field Q(zeta_32) for phases, containing Q(i) through
`i=zeta_32^8`. The cyclotomic polynomial is `X^16+1`. The phase ratio is
`zeta_32`, whereas every nonzero fermion determinant ratio is one.
The combined ratio is therefore `zeta_32`, not one. The independent checker
reduces the residual to `X-1` modulo `X^16+1`; `phase_obstruction` and
`phase_times_det_ne` give the corresponding field-theoretic obstruction.
No branch of a logarithm or floating-point exponential is used.

There is a second failure: change the nonzero alpha from `1/4` to one.
All U(1) links, D, S and K are then unchanged, but the lifted action changes
by `1/8`. This is an exact witness that this bare candidate depends on the
choice of lift. It must not be advertised as a well-defined compact action.

## Exact determinant witnesses and replay

The full output is in
`dag/research/campaign_fsp-lattice-anomaly-inflow_independent.json`.
For the width-two boxes the determinants before and after gauge change are:

| height | det D | det C | det S | det K |
|---|---|---|---|---|
| 3 | 21364883442765/4096 | 4097/16 | 21364883442765/1048832 | 54749/65552 |
| 4 | 22705577808916543965/65536 | 4423167197/256 | 22705577808916543965/1132330802432 | 14320719405/70770675152 |

The script recomputes every entry in this table using exact domain
elimination, checks covariance before taking determinants, and checks
the determinant factorization. It imports no repository module. It also
rejects malformed shapes, Boolean integer impostors, out-of-envelope inputs,
nonmonotone paths and singular interior blocks, and detects the recorded
reverse-link, orientation and zero-variation semantic mutations. Replay
both normally and with Python optimization enabled. Strict mypy checks the
local API; SymPy's untyped symbolic API is explicitly outside static typing.

Build only `lake build CampaignFspLatticeAnomalyInflow` under the pinned
toolchain. The replay receipt records committed LF source blobs, output,
and every printed axiom set. The default Lean library and historical
`ChiralAnomalyInflow.lean` are not rebuilt by this campaign.

For context only, [Fukaya et al., arXiv:2001.03318](https://arxiv.org/abs/2001.03318)
discuss the bulk/edge anomaly and their correlations. This literature is an
import, not an inference from this calculation.

## What is proved

General gauge-transport, inverse-certificate, fixed-basis determinant and
Schur-covariance identities; general rational cochain variation; the two
width-two CS values; and the algebraic cyclotomic obstruction are Lean results.
Exact finite Wilson matrix determinants and the width-three control are
independent computational witnesses. For this specified candidate pair,
cancellation fails exactly, with no claimed lattice-spacing error bound.

## What is assumed

The chosen finite geometry, Wilson stencil, mass profile, fixed boundary
bases, cochain branching, lifts and CS coefficient define the model.
The determinant split requires an invertible interior block, checked in
each witness. The mathematical ring/field hypotheses are explicit in Lean.

## What is open

The node's full anomalous chiral determinant cancellation, a regulator and
measure defining that determinant, matching the induced bulk action to it,
a compact lattice CS completion, and controlled continuum or large-slab
limits remain open here. The continuum Callan-Harvey mechanism stays an
import. Neither a full derivation nor a general impossibility result follows
from this failed fixed-basis construction. No DAG status is raised.
