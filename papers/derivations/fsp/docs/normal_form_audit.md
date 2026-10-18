# Actual normal forms and the limits of the contract atlas

AuthorityEffect: None. Audit and extension, 2026-09-22.

The directory initially contained **28 contracts**, not the 23 claimed in the
old evaluator header. They were accepted by a linter that checked seven keys,
four identity fields, and a nonempty route list. It did not implement its
companion schema, let alone prove normal-form laws. Several files used enums
absent from that schema, omitted required sections, and supplied
predicate-to-local-route maps where local-to-system-route maps were required.

The revised directory contains 30 contracts: **two executable canonicalizers,
12 relational admissibility predicates, and 16 operational contracts**.
Relational normal forms retain their established predicate usage: a relation
schema can satisfy BCNF, for example, without there being a unique canonical
BCNF decomposition. The physics and routing contracts do not acquire a unique
representative merely by excluding an anomaly or reaching a terminal status.
Their metadata now says this explicitly. A schema pass certifies structure
only; declarations of laws must be assessed against their evidence.

## 1. Required meaning of a canonical normal form

Fix a domain X, an equivalence relation ~, and an actual function N:X -> X.
The obligations used here are:

1. Soundness: x ~ N(x).
2. Idempotence: N(N(x)) = N(x).
3. Completeness for the declared equivalence: N(x)=N(y) iff x~y.
4. Determinism: the declared carrier order and algorithm determine the output.

The equivalence and carrier are part of the input contract. Changing a basis,
vertex labels, edge order, discretization, or model class is not silently
included in either equivalence below. In particular, completeness of a quotient
section is not completeness of a solution method for arbitrary physical models.

## 2. Rational quotient section: a genuine normal form

Let D be an exact rational m-by-n matrix and W=im(D) inside Q^m. Fix the ambient
coordinate order. Take the nonzero rows v_1,...,v_r of RREF(D^T), with pivot
coordinates p_1,...,p_r. They satisfy v_j[p_i]=delta_ij. Define

    N_D(c) = c - sum_j c[p_j] v_j.

`BQNFSignEvaluator.normalize_cochain` implements this map and returns alpha
with c-N_D(c)=D alpha. The row operations retain their transformations on the
original columns of D, so the witness is replayable even when D has redundant
generators. The normal representatives are precisely vectors whose pivot
coordinates are zero.

**Proof of all four laws.** Each v_j belongs to W, proving soundness. Subtraction
sets every pivot coordinate to zero, so a second application subtracts zero:
idempotence. If c-d belongs to W, write c-d=sum_j t_j v_j; its pivot coordinates
are t_j, hence N_D(c-d)=0 and N_D(c)=N_D(d). Conversely, equality of the outputs
gives c-d=D(alpha_c-alpha_d), proving equivalence completeness. RREF is uniquely
determined by its row space and the ordered ambient coordinates, establishing
determinism and independence from a change of generating basis for W. The gauge
witness itself need not be invariant under such a generator change.

Equivalently, if B has columns v_j and E selects the pivot coordinates, EB=I
and N=I-BE. Thus N^2=N and ker(N)=W. Gaussian elimination gives a finite exact
algorithm; every sum is folded in `Fraction`, which reduces rational numerator
and denominator by their GCD. The rational space is not called a Banach space:
Q with its ordinary metric is not complete.

**Representative norm is not quotient norm.** With D=(1,2)^T and c=(1,0), the
normal representative is (0,-2), with L1 norm 2. The exact quotient L1 distance
is 1, attained already at alpha=0. A deterministic section and an optimization
problem must not be conflated.

## 3. Exact L1 distance and its explicit cost

For the same rational D, the companion reference solver computes

    Phi(c) = min_z ||c - Bz||_1,

where B has independent columns spanning im(D). It enumerates r-subsets of the
m residual hyperplanes c_i-(Bz)_i=0, solves each independent set exactly, and
compares rational objective values. The cost is bounded by binomial(m,r)
candidate sets; the default refuses more than 100,000. A refusal is reported
as `budget_unknown`, with no fabricated residual. Exact quotient membership
and the normal representative remain available independently of this budget.

**Why vertex enumeration attains the optimum.** Since B is injective,
||c-Bz||_1 is coercive and has a minimizer. Among minimizers, choose one with
the largest rank of active zero-residual hyperplanes. If this rank is less
than r, move along a nonzero vector annihilated by their normals. On the
current sign cell, the objective is affine; its slope in this direction is
zero because the starting point is a minimizer and both directions are locally
feasible. Move until a new hyperplane becomes active. Coercivity prevents this
constant-objective line from continuing indefinitely. The new hyperplane's
normal is independent of the old active normals, a contradiction. Thus an
optimum occurs among the enumerated full-rank intersections. For r=0 the sole
candidate is the original residual.

All constraints and candidate values are rational, so an optimal rational
witness exists for these rational data. A lexicographic tie break chooses one
of the enumerated residuals; no uniqueness of L1 minimizers is asserted. This
enumerative implementation is a bounded reference solver, not a polynomial
complexity claim. Legacy finite float inputs are converted to their exact
binary rational values; use `Fraction` or rational strings for intended exact
decimal values. NaN, infinity, and booleans are rejected.

## 4. Binary graph switching: an FSP-specific normal form

Let G=(V,E) be a fixed ordered labelled undirected multigraph. Loops, parallel
edges, disconnected components, and isolated vertices are allowed. An edge
cochain s belongs to F2^E. Vertex switching acts by

    (delta a)(uv) = a(u) xor a(v),
    s ~ t iff t = s xor delta a.

Scan the declared edge order to select a spanning forest T. Root each component
at its least vertex. Set a(root)=0 and a(v) equal to the parity of the unique
forest path from its root to v. Then

    N_T(s)(uv) = s(uv) xor a(u) xor a(v).

`normalize_sign_cochain` returns this representative, its vertex gauge, the
forest indices, and an odd fundamental cycle for every nonzero chord.

**Soundness and idempotence.** The displayed equation is the gauge witness.
Every forest edge becomes zero. Applying the algorithm to an already normalized
cochain yields a=0 in every component, so the output is fixed.

**Gauge invariance and completeness.** If t=s xor delta b, telescoping along
forest paths gives a_t(v)=a_s(v) xor b(v) xor b(root(v)). Each edge joins vertices
in one component, so both root terms cancel and N_T(t)=N_T(s). Conversely,
equality of representatives gives t=s xor delta(a_s xor a_t). Thus the normal
form is complete for precisely this switching equivalence. Edge order and the
root convention fix the result deterministically.

For a chord e=uv, N_T(s)(e) is the parity around the cycle formed by e and its
forest path. These cycle parities are independent switching obstructions.
There are |E|-|V|+components coordinates, so there are exactly
2^(|E|-|V|+components) switching classes, including the loop coordinates. The
obstruction is zero iff a vertex sign gauge can make every edge positive.
The algorithm is polynomial in the size of the explicitly supplied graph;
the configuration graph of a succinct many-body model can be exponentially
larger than the model description.

**Physical scope.** For a fixed real Hamiltonian basis, put an edge between
states with a nonzero off-diagonal H_uv and define s_uv=1 iff H_uv>0. A diagonal
basis change |v> -> (-1)^a(v)|v> acts by the switching law. The normal form
therefore decides whether this restricted gauge family can make all
off-diagonal entries nonpositive. An odd cycle proves an obstruction within
this family, not within arbitrary basis changes, fermion-bag regroupings,
particle-hole transformations, auxiliary-field choices, or meron resummations.
The graph normalizer does not by itself discover any of those transformations.

## 5. Repairs and explicit counterexamples

- The old summary router returned `ExactRepair` for `{}` and for any positive
  residual below 1e-7. It accepted `has_meron_pairing=True` without a witness.
  It now requires the actual complex, cochain, and path signs and recomputes them.
- The old quotient routine performed fixed-step floating subgradient descent
  while its header called the result exact. Exact rational normalization and
  guarded exact optimization replace that implementation.
- For the existing SU(3)-labelled Y-junction fixture, the former value 2.6 is
  replaced by the certified optimum 5/2. For c=(1,1/2,-3/2,0,0,0), the vertex
  gauge alpha=(0,1/2,1/2,1/2) gives residual (1/2,0,-2,0,0,0), of norm 5/2.
  The dual vector y=(1,0,-1,1,1,0) satisfies D^T y=0, ||y||_infinity=1 and
  c dot y=5/2, proving the matching lower bound. The regression test replays
  both certificates. The value 2.6 was an iterative artifact, not evidence of
  a larger obstruction. This calculation concerns the chosen cochain fixture;
  it establishes no intrinsic SU(3) sign-hardness theorem.
- Matrices are dimension-checked and d1*d0 must equal zero exactly. A nonzero
  rational product as small as 1/10^30 is still nonzero.
- The old pairing search accepted approximately equal weights and ignored
  sufficiently small active rows. The revised routine pairs only exactly equal
  positive magnitudes with opposite signs, covers every nonzero row, and rejects
  malformed signs and negative magnitudes. It does not discover physical clusters.
- Signed rows +2,-1,-1 have zero total but no equal-weight opposite-sign
  involution. Such an involution is sufficient for cancellation, not necessary.
- An arbitrary rational quotient distance does not bound average sign. With
  D=I, c=(1,1), and signs (+1,-1), Phi=0 while average sign is 0. The former
  claim average_sign >= 1-Phi/||c|| would give 0>=1. It is withdrawn in the
  CDT-FSIGN contract. A physical bridge must prove that the admitted gauge action
  preserves the relevant partition sum and observable estimators.
- Closed but non-boundary cochains are exact algebraic evidence for a nonzero
  quotient class. `StabilizedSurvivor` is retained as a compatibility route name;
  it proves no stability, sampling efficiency, or average-sign lower bound.
- Generic complex determinants carry a phase. `sign(Re(det(D)))` cannot replace
  that phase without an independently justified real-determinant restriction.

Physics contracts still contain proposed model identities and numerical
diagnostic predicates. The present audit does not prove those identities or
turn their tolerance-based diagnostics into exact physical certificates. In
particular, SUSY pairing or an asserted Nicolai map does not establish that a
generic thermal ensemble has nonnegative weights. Their prior `verified`
normal-form label is withdrawn; they are explicitly scoped operational forms.

## 6. Evidence and its limits

`code/tests/test_normal_form_laws.py` exhausts all 81 two-by-two matrices with
entries in {-1,0,1} over specified finite cochain/gauge samples; it also checks
an independent codimension-one invariant and a closed-form L1 dual value.
Binary tests enumerate every edge-sign vector and every vertex gauge on the
declared graph fixtures, including K4, a triangle, parallel edges, a loop,
disconnected graphs and empty carriers. Counterexample tests cover the former
false exactness routes, malformed inputs and budget refusal. These finite tests
support the implementation and are distinct from the general proofs above.

`lean4/NormalFormLaws.lean` proves actual soundness, idempotence and equivalence
completeness for the integral quotient by span_Z(1,2), and for the F2 triangle
switching normalizer; it also proves triangle-cycle invariance and the odd-cycle
obstruction. The five triangle results use no axioms. The three integral results
use only `propext` and/or `Quot.sound`. They do not mechanically verify the general
Python RREF or graph traversal. The existing `BqnfSignPacket.lean` formalizes a
different route vocabulary and supplied scalar/Boolean assumptions; it is not
a verification of the revised evaluator or these normal-form algorithms.

Validation performed with eight pytest workers: the new law/schema/e2e tests
and existing cochain/fermion-engine tests passed, **125 tests total**. The Lean
file elaborated successfully with all eight axiom reports. The repository
exact-arithmetic skill check is a small Fraction sanity check, not a substitute
for these algorithmic tests. The five SU(3) integration tests additionally passed
after replacing the iterative residual expectation with the exact primal/dual
certificate above.
