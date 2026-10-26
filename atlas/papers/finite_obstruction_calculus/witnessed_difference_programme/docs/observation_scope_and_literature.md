# Observation scope, finite encodings, and comparison boundaries

Date: 2026-10-08. Evidence: written finite arguments and scoped native fixtures.
No new Lean formalization or external theorem import is claimed.

## 1. Which repair-class question?

Appendix T.8 proves **WDP-DIM-R** for finite rational linear data. With
realizable candidates $R$, repairs $B$, existing report kernel $K$, and
arbitrary additional rational linear rows, the repair-class question on
actual reports of candidates in $R$ needs exactly

$$
\dim(R\cap K)-\dim(R\cap K\cap B)
$$

rows. The global question on all of $V$ instead needs
$\dim K-\dim(K\cap B)$, as already proved in WDP-DIM-1.
The proof and examples in T.8 distinguish actual reports, the restricted
quotient by $A(R\cap B)$, and the potentially coarser quotient by $A(B)$.
Restricting the candidate set changes the question; it does not refute the
global theorem.

## 2. Standard auxiliary-bit corollary of the fiber criterion

**OBS-BITS.** Let $X$ be finite, $p:X\to P$ an existing report and $q:X\to Z$
a protected answer. An additional encoder $e:X\to\{0,1\}^b$ is unrestricted,
and the decoder sees both $p(x)$ and $e(x)$. Define

$$
M=\max_{a\in p(X)}|q(p^{-1}(a))|
$$

when $X$ is nonempty, and set $M=1$ for $X=\varnothing$.
A decoder on the realized image of $(p,e)$ exists for some encoder $e$
exactly when $2^b\ge M$. Consequently the minimum fixed bit length is
$\lceil\log_2 M\rceil$.

*Proof.* In any one $p$-fiber, candidates with different protected answers
must receive different auxiliary strings. Pigeonhole counting gives the
lower bound. Conversely, in each realized $p$-fiber assign a distinct
$b$-bit string to each distinct protected answer, and give every candidate
with that answer the assigned string. Codes may be reused in different
$p$-fibers because the decoder also receives $p$. The answer is then constant
on every $(p,e)$-fiber, so the report-fiber criterion supplies the decoder.
The empty domain admits the empty decoder with zero bits. $\square$

Taking $q=\operatorname{id}_X$ recovers the identity-recovery fiber count.
A coarser protected answer can need fewer bits. This is a standard counting
consequence, not a novelty or priority claim. It does not price a fixed
instrument shelf, constrain encoder computation, prove faithful retention
under future updates, or bind a report to an external source. Those contracts
must be stated separately. In particular, the encoder is allowed to depend
on the very answer it is intended to preserve; this is an existence theorem,
not an algorithm for discovering that answer cheaply.

## 3. Pairwise non-derivability does not give matroid bases

Let $X=\{a,b,c,d\}$ and let the protected question be identity. The available
binary queries are:

| State | $A$ | $B$ | $C$ | $D$ | $E$ |
| --- | --- | --- | --- | --- | --- |
| $a$ | 0 | 0 | 1 | 0 | 0 |
| $b$ | 0 | 1 | 0 | 1 | 0 |
| $c$ | 1 | 0 | 0 | 0 | 1 |
| $d$ | 1 | 1 | 0 | 0 | 0 |

**OBS-MENU.** No one of these queries determines another, yet their
inclusion-minimal separating subsets cannot be the bases of a matroid.

*Proof.* All five queries are nonconstant. A nonconstant binary query can be
a function of another nonconstant binary query only if the two columns are
equal or complementary. No two columns in this table are equal or
complementary, which establishes all 20 ordered non-derivability claims.
The pair $\{A,B\}$ separates all four states, and neither singleton does.
The triple $\{C,D,E\}$ also separates them: its reports are $100$, $010$,
$001$, $000$. Removing any one column merges its marked state with $d$.
Thus these are inclusion-minimal separating sets of cardinalities two and
three. All bases of a matroid have the same cardinality (by the augmentation
axiom), so this family of minimal separating sets is not a matroid basis
family. $\square$

This refutes the sufficiency of **pairwise non-derivability** for that basis
claim. It does not refute a theorem with additional hypotheses, nor does it
attribute this hypothesis as the complete statement of an unread paper.
Section 14.6's hitting-set formulation remains valid. Chapter 23 and Appendix
U require a separate proof that sufficiency equals full rank before using
matroid greedy selection.

## 4. Noise and quantum selection remain separate obligations

A necessary noise limitation can already be stated. Fix finitely many
calibrated rational linear report rows $\ell_i$, with adversarial additive
error bounds $\varepsilon_i>0$ in their declared units. Let the domain be the
whole rational subspace $R$, with $R\not\subseteq B$, and require exact
recovery of $r+B$. Choose $v\in R\setminus B$. There is a positive rational
$t$ so small that $|t\ell_i(v)|\le2\varepsilon_i$ for every row. The report
boxes of zero and $tv$ then overlap: their midpoint is within the allowed
error of either report. Their protected answers differ, so no decoder can
always recover the class from that noisy report. Rows vanishing on $v$
already agree and impose no restriction on $t$.

This argument assumes every row is noisy, finitely many fixed rows and
scale-closed $R$; it does not rule out noiseless separating rows, a separated
finite domain, or a weaker approximate question. A useful noise/quantization
extension must declare its domain or margin, row calibration, observation
model and shelf. No noisy-observation implementation is claimed here.

Similarly, WDP's positive-$\lambda$ depolarized readout family preserves
state separation while changing the readout. State separation alone is not
a full composite local-tomography model. A quantum-selection theorem must
state the composite and operational axioms and show which axiom excludes
the surviving family; it is not derived here.

## 5. Native controls and evidence scope

The monorepo fixture
`omega_engine/crates_rs/tests/omega_wdp/observation_scope.rs` calls
`omega_category_theory::finite_report_query::ReportQueryProblem` for admission,
decision and certificate replay. It does not implement another fiber solver
or evaluate Phi, Gamma2 or Xi outside `omega_functional`.

Run from `omega_engine/crates_rs`:

```bash
cargo test -p omega_wdp --test observation_scope --locked -- --nocapture
```

The tests inspect all 32 shelf subsets and all 20 ordered query pairs, all
16 one-bit encodings for four identities in one existing-report fiber, a
two-bit attaining encoding, answer coarsening and code reuse across existing
fibers, and finite controls for T.8's domain and quotient distinctions.
These verify the explicit tables and canonical checker behavior. The
rank-nullity argument and finite counting arguments establish the general
claims at their declared scope; bounded table tests are not substitutes for
those proofs. No physical or execution authority follows from a decision.

## 6. Primary-source comparison queue

The supplied text is a synthesis of a GLM review and selected SciSpace
results. The original full review, ranked search results and primary papers
were not supplied. All five primary texts below remain **UNCONSULTED**:
arXiv and Springer requests were denied by the environment proxy. No PDF
copy was obtained. The [acquisition inventory](../manifests/literature_access.json)
records the probes and candidate PDF URLs for later retrieval. The source
metadata below is supplied, not independently verified.

| Registry lead | Proposed comparison after primary-text acquisition | Current boundary |
| --- | --- | --- |
| [REF-SCI-001: Simas](references.md#ref-sci-001--semantic-identity-compression) | Match representation-fiber identity and bit-budget statements against OBS-BITS, then inspect the exact orthogonal-core/matroid hypotheses. | OBS-MENU addresses a hypothesis, not the unread paper's full theorem. |
| [REF-SCI-002: Castello, Redmond and Kuper](references.md#ref-sci-002--inductive-diagrams-for-causal-reasoning) | Compare causal path witnesses and Agda semantics with guarded legal swaps, retained events and WDP's local 3-witnesses. | No semantic equivalence is asserted without an explicit adapter and preservation proof. |
| [REF-SCI-003: Ayyam and Sammler](references.md#ref-sci-003--higher-order-interaction-trees) | Inspect effectful and concurrent Lean semantics as a possible execution-model comparison. | This is not evidence for WDP's finite observation theorem. |
| [REF-SCI-004: Bungert and Stinson](references.md#ref-sci-004--nonlocal-perimeter-limit) | Record topology, compactness, liminf and recovery-sequence hypotheses before any graph-to-continuum method comparison. | A classifier perimeter theorem does not transfer to WDP by analogy. |
| [REF-SCI-005: Song et al.](references.md#ref-sci-005--llm-reasoning-failures) | Extract task categories and failure controls that could guide a future evaluated corpus. | A deterministic fixture is not an LLM evaluation; this supplies no mathematical proof. |

The focused next source review is Simas followed by the causal-diagram paper.
Unidentified or duplicate search hits are not promoted to bibliographic
records. Future acquisition should retain the actual version, bytes and hash,
and record the precise definitions and theorem passages read before changing
the consultation status. The source access limitation supplies no conclusion
about the validity of any external theorem.
