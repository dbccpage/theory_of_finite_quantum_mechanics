# Minimum cost of sufficient finite observation

AuthorityEffect: None. This corrects the submitted derivation retained verbatim
in [submitted_derivation.md](../code/finite_observation/submitted_derivation.md).
The local identifiers `COST-*` do not reuse the canonical Chapter 14 registry.
The mathematics is finite set cover and deterministic decision-tree optimization
applied to the paper's realized-image factorization criterion. Prices, permitted
instruments and the protected question are supplied, not derived or authorized.

## COST-D01. The instance and its two prices

Let X be finite, with existing report p:X->P, protected question q:X->A and
a finite shelf of total deterministic measurements m_i:X->M_i, each with
positive rational price c_i. All outcome equality is literal equality. No
probability, noise distribution, physical sensor or purchasing authority is
added. For X empty, both optimum values are zero.

A fixed suite S is chosen before seeing which report p(x) occurs; its cost
is the sum of its instrument prices. It is sufficient exactly when q is
constant on every fiber of r_S=(p,(m_i)_(i in S)). Equivalently there is a
unique decoder q_bar on the actual image of r_S with q=q_bar composed with
r_S. The decoder need not be defined on unrealized report labels.

Adaptive observation first receives p(x) freely and may then choose its next
measurement from the observed history. The objective is worst-case total
price, not an expected cost. Define infeasible optima to be +infinity; finite
prices are never substituted for infeasibility. The reference encoding uses
null for +infinity, accompanied by an explicit conflicting state pair.

## COST-P01. Coverage and the correctly typed transversal

Put U={{x,y}:p(x)=p(y),q(x)!=q(y)} and
D_i={u={x,y} in U:m_i(x)!=m_i(y)}. Then S is sufficient iff
the union of D_i over i in S is U. Indeed, an uncovered pair is exactly a
failure of fiber constancy, in both directions.

For the equivalent hitting-set description, the hyperedge associated with
u is E_u={i:u in D_i}, a subset of the instrument index set I. Thus S is
a transversal of (I,{E_u:u in U}). The sets D_i are subsets of U and are
not hyperedges on I. Sufficiency is upward closed; an inclusion-minimal
sufficient suite need not be cheapest. Positive prices imply every cheapest
suite is inclusion-minimal, but do not imply uniqueness.

Every finite set-cover instance is realizable here: use states {*} disjoint
union U, constant p, q(*)=0 and q(u)=1; set m_i(*)=0 and
m_i(u)=1 iff u lies in the supplied D_i. Its only unresolved pairs are
{*,u}. This supplies both directions of the connection with set cover.

## COST-P02. Information order, feasibility and exact fixed optimum

If p'=h composed with p is a coarsening, then equality under p implies
equality under p', and U(p) is contained in U(p'). Every p'-sufficient suite
is therefore p-sufficient; optimum fixed price cannot decrease on
coarsening. Refinement reverses these inclusions. A difference of finite
optimum prices can price a declared extra report; infinity-minus-infinity
is undefined.

A sufficient suite exists iff the whole shelf covers U. Otherwise some
u={x,y} in U has E_u empty, exhibiting equal p and all measurement outcomes
but unequal q. A decision tree must send these two states down the same
path, so adaptivity cannot restore feasibility. Conversely asking every
instrument succeeds whenever the whole shelf covers U.

When feasible, the minimum over the finite set of sufficient subsets is an
attained nonnegative rational. Without feasibility the optimum is +infinity.
An exact optimality certificate can list all 2^|I| subsets, each subset's
actual summed cost and coverage truth value, and a sufficient selected suite
whose price is no larger than every sufficient row. The checker recomputes
every row from the supplied instance. Exhaustion proves a global lower bound;
the selected sufficient suite supplies its matching upper bound.

This is exponential, deliberately complete evidence. A shorter branch-and-bound
certificate could replace it only if its tree covers all alternatives and
every pruned subtree has a checked valid lower bound. A collection of local
prune numbers is insufficient. A cover map alone proves an upper bound.

## COST-P03. LP and disjoint packing bounds

Let A_(u,i)=1 iff u in D_i. Every integer cover gives a feasible nonnegative
vector for Az>=1, so the fractional covering LP is a lower bound on the
integer optimum. A supplied feasible primal z and dual y satisfying
A^T y<=c, y>=0 and c.z=1.y prove the fractional optimum by weak duality.
That value proves the integer optimum only when a sufficient integer suite
attains it. No randomized rounding argument is needed.

For pairwise disjoint nonempty hyperedges E_(u_j), every cover must choose
distinct instruments, giving the lower bound sum_j min_(i in E_(u_j)) c_i.
This packing bound is dominated by the LP bound: assign dual mass
min_(i in E_(u_j)) c_i to u_j and zero elsewhere. Every instrument meets at
most one selected hyperedge and therefore respects its dual inequality.

The concrete Fano fixture has seven points and seven three-point lines:
012, 034, 056, 135, 146, 236, 245, each of price one. No two lines cover
seven points; the three through point zero do. Thus the integer optimum
is three. Every point belongs to three lines, so z_i=y_u=1/3 gives matching
fractional value 7/3. Every two points share a line, making the disjoint
packing bound only one. These are exact table facts, checked by the replay.

The submitted star counterexample was false: the two leaf obligations force
its two instruments and already give a tight disjoint packing. The claim
that packing and LP bounds are incomparable is withdrawn. A single LP-tight
instance also cannot refute the existential assertion that a gap is possible.

## COST-P04. Exact adaptive recursion and its complete certificate

For a candidate subset C, let V(C)=0 if q is constant on C, including the
empty subset. Otherwise let J(C) contain instruments with at least two
outcomes on C and write C_(i,a)={x in C:m_i(x)=a}. Define

    V(C) = min_(i in J(C)) [c_i + max_(a in m_i(C)) V(C_(i,a))].

The minimum of an empty family is +infinity; any alternative with an
infeasible child has value +infinity. Every branch is a proper subset of C,
so induction on |C| defines V. A non-splitting measurement can be deleted
without changing information and, because its price is positive, lowers
each affected path cost. Repeating a previous measurement is non-splitting.
Finite correct reduced trees consequently have depth at most
min(|C|-1,|I|), and the recurrence attains the minimum when finite.

For soundness, every tree's first useful measurement i has worst-case
remaining price at least max_a V(C_(i,a)); this gives the lower bound.
For attainment, choose an optimal first measurement and attach optimal
child trees, supplied inductively. An arbitrary optimal tree need not have
every child optimal: a non-worst-case branch can have slack. Only existence
of an optimal tree with optimal children is required.

For nonconstant q on C inside one p-fiber, J(C) equals the proposed J*(C)
of instruments separating a q-different pair. If a measurement agrees on
every cross-q pair, it also agrees on a same-q pair by comparison with a
third state having another q value; hence it is constant throughout C.
There is no strictly stronger J* pruning condition in this setting.

The initial report must be used:

    C_adaptive = max_(z in p(X)) V(p^-1(z)),

with maximum zero for empty X. In general this is not V(X). Every fixed
sufficient suite can be asked in sequence on each initial fiber, stopping
early on constant q, so C_adaptive<=C_fixed, including the extended values.
Restricting a correct tree to a subset cannot raise worst-case cost.

The reference certificate lists V(C) and one chosen optimal instrument for
every subset C. The verifier checks each terminal value and every competing
Bellman option from the already checked proper-subset rows. Missing rows,
non-splitting choices, incorrect infinities and cheaper omitted alternatives
are rejected. Induction proves all table values; the chosen instrument and
its measured branches give an actual strategy. This checks the submitted
table and never substitutes a fresh solution after a failed replay.

## COST-E01. A repaired adaptive example and retained failures

Use states 1 through 8, constant p, q=(1,1,2,2,3,3,4,4), and

| Instrument | Outcomes on states 1 through 8 | Price |
|---|---|---:|
| A | 0,0,0,0,1,1,1,1 | 1 |
| B | 0,0,1,1,0,0,0,0 | 3 |
| C | 0,0,0,0,0,0,1,1 | 3 |

Pairs {1,3}, {1,5}, {5,7} force B,A,C respectively, so the fixed minimum
is seven. Asking A and then B on outcome zero or C on outcome one costs
four. Any correct path for state 1 must ask both A and B to distinguish
states 5 and 3, proving adaptive minimum four.

The submitted row A=(0,1,0,1,0,0,1,1) instead leaves states 1 and 5 with
identical complete reports and different answers: its optimum is infinite.
It is preserved as a separate negative fixture, not silently corrected in
the retained submission. The supplied three-state miniature also had two
unresolved pairs, {1,2} and {2,3}; its measurements cover the latter. Its
{1,2} infeasibility witness remains valid.

## COST-P05. Approximate decoding has a separate obligation

For a declared pseudometric on answers and an actual decoder with error at
most epsilon, two states with the same augmented report have answer
distance at most 2 epsilon, by the triangle inequality through the decoded
value. A pair farther apart refutes that error claim. The pairwise condition
is necessary and need not supply a center of radius epsilon in the declared
answer space. Failure of exact cover alone supplies no approximate decoder
or numerical error guarantee. At zero error, literal answer equality further
requires metric separation. Prices provide none of these metric premises.

## Executable scope and reproduction

The [standalone reference](../code/finite_observation/solver.py) admits at most
ten states and twelve instruments, with positive exact Fraction prices of
at most 256 numerator/denominator bits. Reports and outcomes are explicit
string tables. It emits complete subset and Bellman tables, binds all input
fields by SHA-256, rechecks every submitted row, and returns a structured
verification failure. These finite caps are resource refusals, not a claim
of a polynomial algorithm. No native Rust or Lean verification is asserted.

With the paper's code directory on PYTHONPATH, run from the paper root:

    python -B -m finite_observation.replay_examples --write observation_certificates.json
    python -B -m finite_observation.replay_examples --check observation_certificates.json
    python -B -m pytest code/unit_tests/test_finite_observation.py -o addopts= -q

The examples include the corrected 4-versus-7 gap, the submitted infeasible
table, the Fano 7/3-versus-3 LP gap, the corrected miniature and a free
visible report already resolving q. Corruption tests exercise omitted table
rows, wrong task/prices/outcomes, false optimal values, invalid choices,
inexact data and forged authority effects. This source-bound finite result
does not close an infinite carrier, a general mathematical language or an
institutional authorization process.
