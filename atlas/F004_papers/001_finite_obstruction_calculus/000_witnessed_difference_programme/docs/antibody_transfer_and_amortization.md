# Antibody transfer and amortization: checked finite scope

**Statement version: 1, 2026-10-04. AuthorityEffect: None.** Local `ANT-*`
identifiers below are supplemental identifiers, not additions to the canonical
154-row claim registry. The [submitted derivation](../code/antibody_transfer/submitted_derivation.md)
is retained byte-for-byte as a proposal. This note supplies corrected statements
and proofs; the [finite checker](../code/antibody_transfer/checker.py) and
[replay](../code/antibody_transfer/replay_examples.py) check their declared inputs.

## ANT-D01: tasks, predicates and applicability

A task supplies a candidate carrier and a validity predicate. Write its accepted
subset as `G_S ⊆ X` or `G_T ⊆ Y`. Acceptance is relative to that mathematical
profile: repair *potentials* lie in their own carrier `U`, with admissible set
`A ⊆ U`; for the exact-repair task, accepted defects are `d0(A) ⊆ V`. In general
the repair domain is not the candidate carrier. Profile data include the actual
operators, coefficient domain, admissible repairs, comparison question, weights,
tolerance and evaluator semantics needed to determine the predicate.

The executable finite-set checker treats an explicitly supplied acceptance
table as its declared predicate. It checks table membership and every adapter
image exhaustively. It does **not** certify that a caller's table faithfully
implements a different external evaluator. The polynomial and circulation
examples additionally compute their mathematical predicates from exact inputs.
Recorded profile fields bind the question; equality or presence of seven fields
does not prove a semantic transfer law.

An antibody is a rejection set `D ⊆ X` with independent evidence that
`D ∩ G_S = ∅`. A checked failing candidate only justifies its singleton rejection;
enlarging that singleton requires a proof for the enlarged predicate. Such a
proof can be finite exhaustion, an algebraic invariant, a separating functional,
or another sound argument. A dual functional is not a compulsory witness type.
Guard survival means only “this rule did not reject”; target evaluation and
authorization remain separate.

## ANT-P01: one rule versus every rule

Let `α:H → X`, where `H ⊆ Y` is the declared adapter domain. The transferred
rejection of a source set `D` is `{y ∈ H : α(y) ∈ D}`. Then

\[
 \bigl[\forall D\subseteq X\setminus G_S:
       \alpha^{-1}(D)\cap G_T=\varnothing\bigr]
 \quad\Longleftrightarrow\quad
 \alpha(G_T\cap H)\subseteq G_S.
\]

**Proof.** Inclusion implies that any valid target input in the adapter domain
maps to a source-valid input, outside every sound source rejection. Conversely,
if valid `y ∈ H` maps to invalid `x`, the sound source singleton `{x}` rejects
`y`. These arguments do not require finiteness. Finiteness makes the supplied
table check executable.

For **one fixed** source-sound `D`, the exact weaker condition is simply
`α⁻¹(D) ∩ G_T = ∅`. Multiple independently checked per-rule conditions can be
conjoined and safely accumulated. The submission's claim that per-rule evidence
“composes with nothing” is false. The universal adapter certificate amortizes
the transfer premise over arbitrary future source-sound rules; it is not the
only reusable evidence.

Image inclusion here is one-way preservation of validity. It does not assert
reflection of validity, factorization of every observable, or fiber constancy
of the target predicate. For example, a constant map to a source-valid point
can send both a valid and an invalid target point to that point and satisfy
ANT-P01, while the target validity predicate is not constant on its fiber.

**ANT-X01: the quantifiers differ.** On the triangle use

\[
 d_0=\begin{pmatrix}-1&1&0\\0&-1&1\\-1&0&1\end{pmatrix},
 \quad y=(1,1,-1),\quad b=(1,-1,0)=d_0(0,1,0).
\]

The source allows only zero repair and has `G_S={0}`. The target allows all
potentials and has `G_T=im d0`. With `α=id`, the circulation rule
`D={δ:y·δ≠0}` is safe on both tasks, although the universal audit fails because
`b ∈ G_T \ G_S`. The source-sound point rule `{b}` is unsafe after transfer.
The original `(0,1,0)=d0(0,1,0)` was an incorrect matrix calculation; `(0,1,0)`
is not exact. The finite replay restricts to the three named candidates
`0`, `b` and `(1,1,0)`, which suffices to exhibit both quantifiers.

## ANT-P02: partial adapters and task parameters

Safety on `H` needs no totality. An everywhere-defined guard can return
`NOT_APPLICABLE` outside `H` and send those inputs to the ordinary target
evaluator. This is a declared handling policy, not evidence of their validity.
Covering only `G_T` does not define a guard on all of `Y`. Conversely, choosing
to reject every out-of-domain candidate is safe only if `G_T ⊆ H` **as well as**
the inside-domain rejection being safe. Coverage, typing, safety and cost are
distinct obligations.

For validation maps `f_S:X→D_S`, `f_T:Y→D_T` and data adapter
`β:D_T→D_S`, fix target datum `e`. Let
`G_T(e)=f_T⁻¹(e)` and `G_S(β(e))=f_S⁻¹(β(e))`. Then ANT-P01 becomes

\[
 \alpha(G_T(e)\cap H)\subseteq G_S(\beta(e))
 \iff
 \forall z\in H\cap G_T(e),\quad f_S(\alpha z)=\beta(f_Tz).
\]

**Proof.** Substitute `f_T(z)=e` in the two definitions. A commuting square on
all of `H` is sufficient simultaneously for every datum. Conversely, the
pointwise condition for every datum realized by `f_T(H)` gives that square.
Additional task constraints must be included in the validity predicate;
commutation of one diagnostic alone need not preserve their acceptance.

**ANT-X02: the calculus case.** On rational polynomials, `F=5x` fails the source
task `F'=x` and satisfies the target task `F'=5`. Transferring either the point
rejection `{5x}` or the frozen predicate `F'≠x` by the identity is unsafe. The
parameterized predicate `F'≠g`, evaluated with the current target integrand,
correctly retains `5x` at `g=5`. Here both data spaces are polynomial spaces;
the identity data adapter is not an identity on the scalar field alone.

For `α=π_{≤k}`, `k≥0`, and identity data adapter,

\[
 \partial(\pi_{\le k}F)=\pi_{\le k-1}(\partial F).
\]

For `k=0` the right side is zero. Commutation holds exactly when the derivative
has no nonzero coefficient in degrees `≥k`, equivalently `deg F≤k`, including
constant and zero polynomials. At `F=x^{k+1}` and `g=(k+1)x^k`, projection sends
the candidate to zero and the transferred derivative guard wrongly rejects it.
Restricting the pool to degree `≤k+1` does **not** repair that failure; degree
`≤k` suffices. A source point rule may or may not survive this projection; its
preimage must be checked. There is no universal strict increase of coverage or
fragility on generalizing a rule.

## ANT-P03: safe accumulation and audit reuse

If each admitted rule is source-sound **and** satisfies its target transfer
condition, then their transferred union is disjoint from `G_T`. The transfer
conditions may come from one universal adapter audit or separate per-rule
checks. **Proof:** a member of the union lies in one constituent rejection,
contradicting its disjointness from `G_T`.

Source soundness alone does not imply this result; that premise was missing
from submitted Q-P06. The finite checker records a failed adapter audit, still
admits an individually safe rule when its per-rule check passes, and refuses
an unsafe rule without changing the already admitted rejection union. Every
new rule is checked against the full declared source and target valid sets,
not validity after earlier filtering.

This implementation choice is not a prohibition on certified incremental
reasoning. If a checked invariant establishes `G_T ⊆ R`, then a new proof
`D ∩ R = ∅` soundly entails `D ∩ G_T = ∅`. The unsafe operation is treating an
uncertified survivor set as if that invariant had already been proved.

For a finite pool of distinct target candidates `P`,

\[
 |P\cap\bigcup_j\alpha^{-1}(D_j)|
 \le \min\left(|P\setminus G_T|,
           \sum_j|P\cap\alpha^{-1}(D_j)|\right).
\]

This is the ordinary union bound. For an occurrence list with duplicates, count
occurrences on both sides instead. A singleton source rule has at most one hit
only when its preimage meets the distinct target pool in at most one point
(for example, identity transfer on a distinct pool). Noninjective adapters or
repeated candidate occurrences can yield several hits.

An existing adapter audit is preserved under restricting `G_T` or enlarging
`G_S`, with the adapter and applicable domain fixed. Enlarging `G_S`, however,
can invalidate existing source-sound antibodies. Example: initially `G_S={a}`,
`D={b}`; enlarge to `{a,b}`. The adapter inclusion can still hold, but `D` is
now unsound. Reusing the adapter audit therefore does not discharge the new
source-soundness checks. Other task changes can also preserve an audit through
a new proof; these sufficient monotone directions are not a classification of
all permissible changes.

## ANT-P04: circulation rules and their boundary

For a rational matrix `D`, exact dual vector `y` with `Dᵀy=0`, and any declared
repair set `A`, the rule `y·δ≠0` is sound for exact repair `δ∈D(A)`.
**Proof:** if `δ=Df`, then `y·δ=(Dᵀy)·f=0`. No `d1` or norm is needed for this
zero-versus-nonzero statement. Capacity bounds `|y_i|≤w_i` with positive weights
give the stronger numerical certificate

\[
 |y\cdot\delta|\le\|\delta-Df\|_{1,w}\quad(f\in A).
\]

For acceptance at tolerance `ε≥0`, reject only when `|y·δ|>ε` under these
capacity bounds; nonzero alone is insufficient at positive tolerance. The
checker recomputes annihilation, capacities and every supplied query score.
This certifies exact lower bounds, not a measured runtime advantage over an LP.

For `δ=(1,1,0)` on the triangle, the rule has score `2`. Orthogonal projection
to `(1/3,1/3,2/3)` changes its quotient class and yields an exact vector, so
`Φ` changes from `2` to `0`. It is not an admissible repair in the original
class. The projected vector is nevertheless a perfectly valid member of the
cochain carrier; the error is substituting a different candidate/problem,
not producing a “non-element”.

## ANT-P05: exact amortization under a declared cost model

Let `N≥0` be the number of pool occurrences, `0≤h≤N` the verified sound early
rejection count, and exact costs `C0,g,v≥0` in the same declared units. Assume a
guard is paid once for every occurrence and saves one evaluation of cost `v`
per rejection. Then

\[
 T_0=Nv,\qquad T_1=C_0+Ng+(N-h)v,\qquad T_0-T_1=hv-Ng-C_0.
\]

The formula is valid at `N=0` and `v=0`. Only for `v>0` may it be written
`h>(Ng+C0)/v`; only for `N>0,v>0` may it be written
`h/N>g/v+C0/(Nv)`. Positive saving requires `g<v`; if `g≥v`, saving is
nonpositive, and may be exactly zero when `C0=0`. The term `C0/(Nv)` tends to
zero for fixed costs and `v>0`; it strictly decreases only when `C0>0`.

For `N=10000,v=1,g=1/1000,C0=2`, the strict threshold is `h>12`. This is an
arithmetic example, not a measured hit rate. A distinct identity-mapped point
rule with `h≤1` loses at least `11` cost units in that example, but point rules
can be profitable with other costs or repeated occurrences. No density such
as `1/3` is defined on `Q³` without a specified finite pool or probability law.
Source frequencies do not determine target frequencies, even under safe
transfer. No “random-ish” pool or `g≪v` claim is admitted without measurements.

A certified lower bound `h≥L` guarantees profit if `Lv>Ng+C0`. An upper bound
`h≤U` proves no profit if `Uv≤Ng+C0`; otherwise it cannot guarantee profit.
An upper hit bound gives an upper saving bound, not an upper loss bound.
For a partial guard, the actual applicability and invocation costs must match
the declared model; the finite checker uses pass-through outside its domain
and explicitly charges every pool occurrence.

## ANT-P06: two-stage audit cost

For the same declared obligations, let `Cα,c,c'≥0` be costs of one reusable
adapter audit, one source-rule check, and one combined per-rule check. Their
values are accounting inputs; logical inclusion does not imply `c'≥c` for
different algorithms. For `k≥0` rules the reusable plan is no more expensive
exactly when

\[
 C_\alpha+kc\le kc' \iff C_\alpha\le k(c'-c).
\]

If `c'>c`, this is `k≥Cα/(c'-c)`. If `c'=c`, it holds exactly when `Cα=0`.
If `c'<c`, it holds only in the degenerate `k=0,Cα=0` case. Strict saving
always requires `Cα<k(c'-c)`. No threshold expression divides by zero.

## Evidence and nonclaims

Five distinct obligations are retained: source soundness, adapter safety,
parameter/validator binding, admitted accumulation, and cost accounting. Their
receipts cannot substitute for one another. The checker supplies bounded
finite exhaustion, exact rational polynomial/matrix arithmetic, and arithmetic
cost receipts. Candidate/profile/adaptation identities are bound to the
external input digest; edited receipts are rejected without changing them.
The retained [input](../code/antibody_transfer/input.json),
[submitted receipt](../code/antibody_transfer/submitted_receipt.json) and
[replay receipt](../code/antibody_transfer/replay_receipt.json) support literal
replay with `replay_examples.py --input input.json --receipt submitted_receipt.json`
from their directory. The scoped test file has **32 passing tests**, including
864 finite profiles for the two quantifiers; replay rejects 11 receipt mutations.
The [source provenance](../code/antibody_transfer/source_provenance.json) records
the original submission bytes, corrected sources, test scope and exact results.
No result establishes general audit decidability, global antibody usefulness,
search speed, implementation-port correctness, Lean formalization or authority.
