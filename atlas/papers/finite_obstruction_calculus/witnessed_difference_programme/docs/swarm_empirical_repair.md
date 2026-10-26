# Arbitrary-cover empirical repair and sampling tolerance

CH19-O01, declared finite/statistical scope. AuthorityEffect: None.

## Exact compatible-polytope distance

Fix a finite measurement set, common finite outcome set, and a nonempty indexed
list of nonempty contexts. Repeated contexts are permitted: they are independent
recorded experiment slots and must agree after repair. List all outcome sections
on each context, including zero-frequency sections. The input is one rational
probability vector f_i per context, obtained from actual nonempty run counts.
The compatible polytope K consists of normalized nonnegative p_i with equal
marginals on every pairwise overlap. It is nonempty: the marginals of the uniform
global distribution belong to K. It is compact and defined by rational data.
Compatibility does not require a global hidden-variable distribution.

The desired radius is

    rho(f) = min_{p in K} max_i ||p_i - f_i||_1.

For every section coordinate introduce p>=0 and an envelope d>=0, and introduce
t>=0. Impose normalization, overlap equalities, p-f<=d, f-p<=d, and
sum_{s in E(C_i)} d_{i,s}<=t, where E(C_i) is the full set of outcome sections on C_i. Minimize t. The native formulation adds nonnegative
slacks to make these inequalities equalities; it retains p>=0. This positivity
is why an unrestricted weighted-L1 projection solver cannot replace this LP.

**Reduction proof.** Every feasible LP gives p in K and |p-f|<=d, hence
max_i ||p_i-f_i||_1<=t. Conversely every p in K extends to a feasible LP with
d=|p-f|, t=max_i ||p_i-f_i||_1 and the corresponding nonnegative slacks. Thus
the optima coincide. Uniform p gives a feasible radius at most 2. Existence of
a rational optimum follows from rational finite LP theory, or by finite Bland
simplex with phase-I artificial variables and exact arithmetic. An explicit
pivot budget may return BudgetExhausted; it is never interpreted as infeasible.

The exact standard-form solver proposes x,y,v and an independent verifier
checks x>=0, Ax=b, A^T y<=c, and c.x=b.y=v. For any feasible z,

    b.y = (Az).y = z.(A^T y) <= z.c,

so equality with the candidate's objective proves global minimality. The replay
uses actual problem data and no solver call. WDP reconstructs the LP from the
actual cover and run table, checks the candidate certificate, recovers p, checks
compatibility, and verifies its actual maximum L1 distance equals v. Changing
the table, cover, repaired vectors, dual, or claimed radius fails replay.
Hashes are not a proof premise. All accepted receipts carry no authority effect.

For two contexts the existing half-marginal-defect theorem agrees with this
general construction. For three copies of a three-outcome context with inputs
e_1,e_2,e_3, compatibility requires one common p. Its distances are 2(1-p_i),
so their maximum is 2(1-min_i p_i)>=4/3, with equality at uniform p. Every pair
has distance 2: half the maximum pair defect is only 1. Thus the pairwise lower
bound does not solve the arbitrary-context problem. Four-context PR data have
rho=0 but no nonnegative global joint model; zero repair does not imply W7.

## Deriving tolerance from a trial protocol

For context i declare n_i independent identically distributed categorical
trials with true distribution p_i on m_i full sections. Let f_i be empirical
frequency. The iid premise gives

    E ||f_i-p_i||_2^2 = (1-sum_s p_i(s)^2)/n_i
                        <= (m_i-1)/(m_i n_i).

The equality follows by summing the variances of the individual frequencies;
cross-category covariances do not enter that sum. The inequality follows from
sum p_i(s)^2>=1/m_i by Cauchy-Schwarz. Applying Cauchy-Schwarz to the error
vector gives E||f_i-p_i||_1^2<=(m_i-1)/n_i. For a declared rational r_i>0,
Markov bounds

    P(||f_i-p_i||_1 > r_i) <= min(1,(m_i-1)/(n_i r_i^2)).

If r_i>=2 the event is empty, so failure is exactly zero. If m_i=1 every
frequency equals its population and the bound is also zero. No independence
between context experiments is needed: the union bound gives simultaneous
failure at most min(1,sum_i failure_i).

Suppose additionally the true context distributions p_i are compatible.
Marginalization contracts L1: group each signed error coordinate by its overlap
section and apply triangle inequality. On the simultaneous good event,

    ||marg(f_i)-marg(f_j)||_1 <= r_i+r_j.

The adapter therefore gives the pair tolerances r_i+r_j and their maximum as a
uniform tolerance, using the actual run counts and full section cardinalities.
These are finite-sample conservative bounds; no asymptotic approximation or
assumed cross-context independence is hidden. Also rho(f)<=max_i r_i on this
event because the true compatible population family is a feasible repair.
The table cannot itself establish iid, population compatibility, physical
calibration, or confidence in an undeclared population model. Re-access,
acceptance and calibration remain the original packet admission conditions;
the empirical image preserves only the recorded outcomes as in CH19-P03.

## Ownership and verification

- `omega_finite_probability::marginal_compatibility` owns finite section
  enumeration, compatibility, the repair LP reduction and checked sampling bounds.
- `omega_solvers::standard_rational_lp` owns exact two-phase Bland proposal and
  independent standard-form primal/dual verification.
- `omega_wdp::empirical_repair` translates actual tables, binds replay and emits
  the conditional protocol result. The direct solver dependency is acyclic.
- Python `witnessed_difference.empirical_repair` delegates to the existing
  generic obstruction solver. Its checked verifier rejects floats and booleans
  substituted for exact Fraction witness data. The generic solver now counts
  artificial-basis cleanup pivots against its budget and replays its candidate.
- Core-only Lean `EmpiricalRepair.lean` proves finite integer transpose pairing,
  weak duality and matching-certificate optimality in nine declarations. This is
  partial coverage of the rational LP argument. It does not formalize simplex
  termination, the minimax reduction or iid probability theory. Rational weak
  duality uses the same ordered-field calculation above; native exact replay
  is not presented as a Lean proof of that full theorem.

Production checks: 3 standard-LP tests, 2 probability-owner tests and 4 WDP
tests pass. Python: 3 new focused tests pass; 102 existing obstruction/vector/
pipeline regression tests pass after the generic-solver change. Fixtures check
global minimality, substituted actual data and false duals, incompatible
three-context radius, PR compatibility, and exact enumeration of a small iid
trial experiment. The Lean module compiles with Lean 4.33.1; its printed axioms
are limited to propext and Quot.sound, with no admitted proofs.
