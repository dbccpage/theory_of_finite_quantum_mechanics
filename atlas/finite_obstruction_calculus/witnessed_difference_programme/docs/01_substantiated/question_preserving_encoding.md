# Question-preserving encoding and a checked finite experiment

**Date:** 2026-10-08. **Evidence:** written conditional proofs and a bounded
native experiment. **AuthorityEffect:** None.

This bridge applies WDP's existing report-fiber criterion (Appendix P.1 and
GEN-WDP-03). It does not infer semantic correctness from a cochain invariant.
The interface is an explicit encoding, partial parser and sound checker
for one declared question. Its acceptance argument is a special case of
WDP's [faithful-representation soundness](faithful_representation_and_relative_completeness.md)
(GEN-WDP-49, §20.6); the new contribution is this explicit bounded encoding
profile and controlled comparison. The experiment tests that interface on integer
quadratics and retains a direct checker as the correctness boundary.

## QPE-1. What a report-only verifier cannot decide

Fix a task $t$, a candidate set $C_t$, an encoded report $E_t:C_t\to R_t$,
and a protected answer $q_t:C_t\to A_t$. A decoder on the realized report
image exists exactly when $q_t$ is constant on every $E_t$-fiber.
In particular, if $E_t(c)=E_t(c')$ but $q_t(c)\ne q_t(c')$, every
deterministic procedure seeing only that report returns the same result on
the pair and therefore cannot correctly decide both answers. The proof is
$D(E_t(c))=D(E_t(c'))$, followed by the supposed decoder equations.

This is a decision obstruction, not a prohibition on sound refusal. For a
Boolean question, a checker may reject both candidates without accepting a
false answer. Randomization with no additional candidate-dependent input
gives the same output distribution on both reports and cannot decide both
with certainty. A witness that differs between the two cases is additional
information: the fiber criterion then applies to the joint report and witness.

The criterion concerns actual maps, not metadata asserting that a report is
faithful. Its set-theoretic decoder need not be an executable or efficient
parser. Task parameters must be retained or supplied independently: the same
polynomial can answer two different derivative questions differently.

## QPE-2. The positive parser/checker bridge

For a fixed admitted task, declare semantic candidates $C$, parsed objects
$Z$, reports $R$, Boolean questions $q_C,q_Z$, an encoder $E:C\to R$ and
a partial parser $P:R\rightharpoonup Z$. Require **question fidelity**:
for every $c\in C$, $P(E(c))$ is defined and

$$q_Z(P(E(c)))=q_C(c).$$

Let $K:Z\times W\to\{\mathrm{accept},\mathrm{reject}\}$ be a checker
with the stated one-sided soundness law
$K(z,w)=\mathrm{accept}\Rightarrow q_Z(z)=\mathrm{true}$.
Define $V(r,w)$ to accept exactly when parsing succeeds and $K(P(r),w)$
accepts. Then, for every original candidate and witness,

$$V(E(c),w)=\mathrm{accept}\quad\Longrightarrow\quad q_C(c)=\mathrm{true}.$$

**Proof.** Acceptance supplies a parsed object and a successful checker
result. Checker soundness gives $q_Z(P(E(c)))=\mathrm{true}$; question
fidelity gives the required original answer. No cochain premise enters this
composition argument. Exact round trip $P(E(c))=c$ is a sufficient stronger
condition when $Z=C$, but question preservation does not require injectivity.

The theorem supplies no checker soundness premise, witness completeness,
search termination or efficiency. For an arbitrary received report $r$,
acceptance concerns its parsed object. Applying the conclusion to a claimed
external candidate $c$ still requires the binding $r=E(c)$ or a checked
question-preserving relation between them. Source authenticity, suitability
of the chosen task, and a relation to a physical or external software system
are separate obligations. A self-reported digest does not discharge them.

## QPE-3. An explicit symbolic-math instance

Let $C=\{-2,-1,0,1,2\}^3$ represent
$f_c(x)=c_0+c_1x+c_2x^2\in\mathbb Z[x]$. Tasks are all
$(v,b_0,b_1)\in\{-2,\ldots,2\}^2\times\{-4,\ldots,4\}$, asking
whether $f_c(0)=v$ and $f_c'=b_0+b_1x$ as polynomial identities.
The direct checker evaluates all three equalities

$$c_0=v,\qquad c_1=b_0,\qquad 2c_2=b_1.$$

These are necessary and sufficient by differentiation and uniqueness of
polynomial coefficients over $\mathbb Z$. This establishes the written
soundness and completeness argument for this checker and domain, without
replacing it with agreement of two encodings. There are 225 tasks and 125
candidates; 125 tasks have one solution and the 100 odd-$b_1$ tasks have none.

On the declared filled triangle with orientations $01,12,20$, encode
$c$ by the edge cochain
$u=(c_1-c_0,c_2-c_1,c_0-c_2)$. The candidates $(0,0,0)$ and $(1,1,1)$
both report $(0,0,0)$, although only the former answers task $(0,0,0)$.
Even the full unanchored cochain loses this question. Its closure scalar
also vanishes for every encoded candidate, including wrong answers.

The **anchored report** adds $a=c_0$. Its parser checks the fixed schema,
the independently supplied task, $a\in[-2,2]$, each edge in $[-4,4]$,
and zero triangle closure. It reconstructs

$$P(a,u)=(a,\ a+u_{01},\ a+u_{01}+u_{12})$$

and refuses reconstructed coefficients outside $C$. Closure identifies the
last edge with the required return edge, so this is an exact inverse on
admitted reports. Inserting the encoded differences telescopes to $c$,
establishing question fidelity. The native parser rejects missing, duplicate,
unknown or mistyped JSON fields; its input size is bounded. Task and candidate
bounds precede arithmetic. A valid but wrong candidate reaches the direct
checker and is rejected there.

On the unrestricted linear coefficient carrier, the edge-map kernel is the
one-dimensional constant direction; the anchor removes exactly that blind
direction. This is a small instance of sharp observation (§10.6). It does
not assert that every individual Boolean task needs the anchor: some task
answers are already constant on the unanchored fibers.

## QPE-4. Exhaustive comparison and what it measures

The native experiment audits all 28,125 task/candidate pairs and runs three
strategies over the same declared task list. Enumeration checks candidates
in lexicographic coefficient order and stops at the first success. Direct
reconstruction solves the three coefficient equations and checks its proposed
answer. Cochain reconstruction solves those equations in anchored edge
coordinates, parses the report and submits the decoded answer to the same
checker. Both reconstruction strategies retain the odd-slope failures and
are compared against exhaustive search, including absence of a solution.

| Strategy | Checker calls | Checker coefficient comparisons | Report parses | Candidate integer fields sent | Closure evaluations |
| --- | ---: | ---: | ---: | ---: | ---: |
| Enumerate, then check | 20,375 | 61,125 | 0 | 0 | 0 |
| Direct reconstruction, then check | 125 | 375 | 125 | 375 | 0 |
| Cochain reconstruction, then check | 125 | 375 | 125 | 500 | 125 |

These are counts for the declared strategy executions, not wall-clock
speedups or a common weighted cost. Exhaustive auditing and additional
round-trip assertions are separate work. Shared task headers, proposal
arithmetic and JSON byte costs are not hidden in a claim of total savings;
they are outside this partial count. Every checker call evaluates all three
coefficient equalities. The reconstruction gain over enumeration comes from
the supplied linear equations. **The cochain route shows no checker-call
advantage over direct reconstruction**, and adds a scalar and a closure test
per successful proposal. No net efficiency improvement is established.

Canonical finite report-table replay finds unanchored collisions on 101
tasks and closure-only collisions on 125 tasks. There are 28,000 wrong
task/candidate pairs with closed encoded cochains. All 225 anchored report
tables preserve their protected answers. A corrupted return edge is refused
as inconsistent representation; a coherent constant shift parses but fails
the semantic checker. This distinction locates a wire diagnostic, not a
demonstrated diagnostic cost advantage over a direct checker.

The implementation is
`omega_wdp::question_preserving_encoding`; finite fiber decisions delegate
to `omega_category_theory::finite_report_query`, and closure evaluations to
`omega_functional::Gamma2Functional`. No functional is recomputed in Python.
The [replay adapter](../code/question_encoding/README.md) and
[deposited result](../manifests/question_encoding_experiment.json) bind the
native source bytes. Embedded build hashes detect a stale trusted local build;
they are not cryptographic authentication of an arbitrary executable.
The new theorems have written proofs; no fresh Lean result is claimed.

A next experiment would need a declared multi-constraint workload, a strong
direct solver/diagnostic baseline, and full preprocessing, checking and
repair costs before attributing any advantage to a cochain layer. That is an
experimental obligation, not a correctness consequence of the representation.
