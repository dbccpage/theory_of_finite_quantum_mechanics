# Vectors unbiased to I and a Szöllősi matrix: exact computations (2026-10-15)

**AuthorityEffect:** None.

Step 1 of the rank 1 plan in the 2026-10-15 next-derivation report: compute exactly the
set M(S) of unit vectors unbiased to both I and S, for Szöllősi matrices S. Then decide
the orthogonality and unbiasedness relations between those vectors. Any quartet
{I, S/√6, K, L} of mutually unbiased bases (MUBs) needs two orthonormal bases inside
M(S) that are mutually unbiased (Jaming et al., arXiv:0902.0882).

## Setup

- S = [[A, B], [B*, −A*]], where A and B are circulant with first rows (1, x, xy) and
  (1, u, uv). The point (x, y, u, v) lies on the unit torus with
  φ(x, y) + φ(u, v) = 0, where φ(x, y) = x + y + conj(xy). This is the
  parametrization in `SzollosiTwoCirculant.lean`.
- A vector is v = (1, v₁, …, v₅) with v_j = a_j + i·b_j and a_j² + b_j² = 1.
- Each column h_k of S gives the condition |⟨h_k, v⟩|² = 6. Columns 1 to 5 are used;
  column 6 is implied by the other five.
- This gives a real polynomial system over ℚ in a₁…a₅, b₁…b₅. Its real solutions are
  exactly the rays of M(S).

## Method

1. `msolve` computes a rational parametrization of the complex solutions:
   one eliminating polynomial ELIM(t) and x_i = −NUM_i(t) / (c_i · ELIM′(t))
   (`scripts/gen.py`, `scripts/gen_pt2.py`).
2. Exact checks on that parametrization (`scripts/exactcheck.py`, python-flint):
   - every equation, homogenized to its degree, vanishes modulo ELIM, so every root of
     ELIM gives a solution;
   - ELIM is squarefree and prime to ELIM′, so its roots are distinct solutions;
   - ELIM is factored over ℚ.
3. Independent count of the complex solutions: Singular `modStd(i, 1)` over ℚ (with
   its exactness test) and `std` modulo two primes (`scripts/mksing.py`).
4. Certified real solutions (`scripts/roots.gp`, `scripts/certroots.py`):
   - PARI's Sturm count gives the number of real roots of each factor;
   - each approximate root is refined by Newton's method in arb and enclosed in an
     interval of width 2^-2999 on which the factor changes sign, tested in exact
     rational arithmetic;
   - the intervals are disjoint and their number equals the Sturm count;
   - the coordinates are arb balls obtained by evaluating the parametrization on the
     interval.
5. Relations between rays (`scripts/certgraph.py`): for each pair of rays (same S),
   ⟨v, v′⟩ is enclosed in a ball. A pair is certified non-orthogonal when the ball
   excludes 0, and certified not unbiased when |⟨v, v′⟩|² − 6 excludes 0. The true
   orthogonality graph is therefore a subgraph of the candidate graph of pairs not
   excluded.
6. Every 6-clique of the candidate graph is tested exactly
   (`scripts/clique_prep.py`, `scripts/clique_exact.gp`): for each pair in the clique,
   PARI forms the compositum of the two number fields, matches the real embedding to
   the two certified roots, and evaluates ⟨v, v′⟩ as an element of the compositum.

msolve also prints isolating boxes for the real solutions. At the second point they
were wrong in the 17th digit while claiming a width near 10⁻³⁸, so they are not used.

## Result at (x, y, u, v) = (1, −1, 1, i)

Files are in `special_1_m1_1_i/`.

| Quantity | Value |
| --- | ---: |
| Complex solutions (msolve; Singular `modStd` over ℚ: dim 0, vdim 192) | 192 |
| Irreducible factors of ELIM over ℚ | 76 of degree 2, 10 of degree 4 |
| Exact substitution check; ELIM squarefree | pass; yes |
| Real solutions = rays of M(S) | 120 |
| Orthogonal pairs | 600 |
| Unbiased pairs of rays | **0** |
| Orthonormal bases (6-cliques) | 10 |
| Mutually unbiased pairs of bases | 0 |

No two rays of M(S) are unbiased to each other. So no quartet of MUBs contains I and
S(1, −1, 1, i). This point has y = −x, so it lies on a special stratum of the family.
The first pipeline (`scripts/graph.gp`, exact compositum test on every pair) and the
certified-interval pipeline give the same graph.

## Result at a generic point

Files are in `generic_point/`. The point is x = (−8 − 15i)/17, y = (56 − 33i)/65,
u = (3 + 4i)/5. Here v and w = 1/(uv) are the two roots of the quadratic left after
dividing t³ − d t² + conj(d) t − 1 (d = −φ(x, y)) by (t − 1/u); the system carries w as
an unknown, so both matrices S (one per choice of v) are computed together and told
apart by the value of w. The point was found by `scripts/search6.py`.

| Quantity | Value |
| --- | ---: |
| Complex solutions (msolve; both choices of v) | 504 |
| Irreducible factors of ELIM over ℚ | 37 of degree 4, 1 of degree 8, 1 of degree 348 |
| Exact substitution check; ELIM squarefree | pass; yes |
| Real solutions (Sturm: 4 + 8 + 156 summed over the factors) | 168 |
| Rays of M(S), for each of the two matrices S | 84 |
| Candidate orthogonal pairs, for each S | 132 |
| Unbiased pairs of rays, for each S | **0** (all excluded by interval) |
| 6-cliques of the candidate graph, for each S | 1 |
| Of these, exactly orthonormal | 1 of 1 |

For each of the two matrices, M(S) has 84 rays, no two of which are unbiased, and
exactly one orthonormal basis. So no quartet of MUBs contains I and either matrix at
this point.

**Status.** The certified-interval and exact steps decide every relation used above for
the solutions found. Completeness, meaning no complex solution is missing, rests on
msolve's count of 504. Singular `std` gives vdim 504 modulo 32003 and modulo
2147483629; the exact `modStd` run over ℚ did not finish within 2 hours. At the
special point, the count of 192 is confirmed over ℚ by `modStd`.

## Controls

- Exact clique test, negative control: six rays at the special point that do not form
  an orthonormal basis (`special_1_m1_1_i/control_fake_clique.gp`) are rejected
  (`control_fake_clique.txt`: 0).
- Exact clique test, positive cases: the 10 bases at the special point and the one basis
  per S at the generic point are accepted (`clique_check.txt` in each folder).

## Reproduce

Tools: msolve 0.6.5, PARI/GP 2.15.4, Singular 4.3.2, Python 3.13 with sympy 1.14.0,
python-flint 0.9.0 and networkx 3.7. Run from `scripts/` (the generic point uses
`gen_pt2.py` and `pt2` in place of `special`). msolve's output for the generic point is
34 MB and is not committed; msolve regenerates it in about 5 minutes (sha256
`c3b479aa…25cf` here).

```
python3 gen_pt2.py pt2.ms
msolve -f pt2.ms -o pt2.par -P 1 -t 4
python3 exactcheck.py pt2.ms pt2.par            # writes pt2.par.check.json, pt2.par.factors.gp
head -1 pt2.par.factors.gp > pt2_fac_only.gp
printf 'FACF="pt2_fac_only.gp"; OUTF="pt2_approx.txt";\n' | cat - roots.gp > run_roots.gp
gp -q run_roots.gp < /dev/null
python3 certroots.py pt2.par pt2_approx.txt pt2_cert.json
python3 certgraph.py pt2_cert.json pt2_certgraph.json
python3 clique_prep.py pt2.par pt2_cert.json pt2_certgraph.json pt2_clq.gp
printf 'CF="pt2_clq.gp";\n' | cat - clique_exact.gp > run_clq.gp
gp -q run_clq.gp < /dev/null
```

## Envelope

- **Supports:** at (1, −1, 1, i) and at one generic point (both choices of S), every
  ray of M(S) found is exact; no two rays are unbiased; at the generic point each S has
  exactly one orthonormal basis inside M(S). Hence no MUB quartet contains I and any of
  these three matrices, given completeness of the solution sets.
- **Does not support:** any statement about other points of the family, Conjecture 3,
  or N(6). Completeness at the generic point rests on msolve, with modular agreement
  from Singular.
- **Narrowest claim:** for S at these three parameter values, the solution sets
  computed contain no unbiased pair of rays.
- **Next test:** lemma L2 of the plan. Show the incidence variety over the domain is
  irreducible (or compute its monodromy) for the generic count 504, then compute the
  locus where an unbiased pair or a second basis could appear, by elimination.
- **Correction to the 2026-10-15 report:** the float probes suggested "60 rays at
  generic points". The number of real solutions changes from one region of the
  parameter domain to another: 84 at this generic point. Lemma L2 must be stated for
  the complex solutions and for each region of real-root count, not as one count of
  rays.
