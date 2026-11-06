# Independent recheck of v2 and narrow source verification

**Verdict on v2:** the substantive mathematical drawing errors identified in v1 are corrected. I found no new mathematical error in the conditional classical construction. Three presentation issues remain, listed below. This review does not establish that v2 derives from the supplied paper.

I inspected `render_sheets_v2.py`, `picture_sheet_v2.png`, and `math_sheet_v2.png`. I separately checked the requested passages in `primitive_axiomatics.md`. I modified nothing.

## Status of the ten v1 findings

| Finding | Status in v2 |
|---|---|
| 1. Inconsistent rate magnitudes | **Resolved.** At \((2.1,1.2)\), orange lengths are now \(1.2\) and \(2.1\), as required. |
| 2. Changed starting state and invisible rotation | **Resolved.** The same state and scale are retained; three endpoint vectors share an origin. |
| 3. Undefined component meanings | **Resolved.** The companion identifies black/green with \(q/p\), signs, and the represented endpoint. |
| 4. Ambiguous commuting operations | **Resolved mathematically.** Both orders now have explicit, correct intermediate states and the same final state. A color convention remains ambiguous. |
| 5. Apparent successive finite kicks | **Resolved.** Simultaneous captions and removal of the intervening operation arrow address this. |
| 6. Unannounced alteration in strip 1 | **Resolved.** The caption announces turning, and the renderer now preserves length. |
| 7. Unexplained mathematical vocabulary | **Partly resolved.** Rates and partial derivatives receive useful explanations; several other essential terms remain undefined. |
| 8. Missing variational boundary conditions | **Resolved.** Independent variations and fixed endpoint conditions are stated; constant translations are correctly distinguished from those variations. |
| 9. Misleading “geometric phase” terminology | **Resolved.** “Angular phase” is used with an explicit distinction. |
| 10. Arrowhead and ghost-count defects | **Resolved.** Arrowheads are capped relative to segment length; the stated count is three. |

The oscillator samples at times \(0,0.5,1\) are approximately
\[
(2.1,1.2),\quad(2.418234,0.046305),\quad(2.144400,-1.118726).
\]
Each has \(q^2+p^2=5.85\), up to floating-point rounding.

The two translation histories are correctly
\[
2\longrightarrow3.5\longrightarrow4.15,
\qquad
2\longrightarrow2.65\longrightarrow4.15.
\]

## Remaining v2 findings

### V2-A — Medium: operation colors change meaning in strip 7

In the middle panel, the gray overhead arrow represents the shift of \(1.5\), and orange represents the dynamical slide of \(0.65\). In the right panel, gray represents the slide of \(0.65\), and orange represents the shift of \(1.5\).

Thus the colors encode first/second operation, whereas the left panel has already associated orange with the slide. The numerical comparison is correct, but the color assignment makes the operations harder to track when their order reverses.

**Remedy:** give the shift one consistent color and the slide another across both panels. Alternatively, explicitly state that these overhead colors mean first and second operation.

### V2-B — Low: the second rate panel obscures the green component

The vertical orange arrow is drawn directly over the green segment. In the PNG, most of green’s shaft disappears beneath orange, leaving its tip as the main visible evidence of the component.

This is not a sign or magnitude error, but it makes the “same state” comparison less legible.

**Remedy:** offset the orange rate arrow slightly sideways while retaining its correct direction and length.

### V2-C — Medium: the companion remains a proof sketch requiring mathematical prerequisites

The revised explanation substantially improves accessibility. However, “autonomous,” “C¹,” “closed,” “simply connected,” and “canonical” remain unexplained. These terms carry assumptions or justification needed for the conclusion.

**Remedy:** add short glosses: time-independent rule; continuously differentiable; locally path-independent integral; a patch without holes; preservation of the specified oriented area. Explicitly describe the page as a proof sketch if complete novice derivation is not its intended function.

These remaining findings concern presentation and learning. They do not overturn the conditional Hamiltonian or Noether calculations.

## Narrow verification of the supplied paper

### S1 — Confirmed: the proposed detector identity establishes gauge invariance

The paper defines the finite pairing and adjoint in §1.6, particularly lines 811–829. For a **fixed** detector \(\phi\) satisfying \(d_0^*\phi=0\),
\[
\begin{aligned}
\langle\phi,\delta+d_0f\rangle
&=\langle\phi,\delta\rangle+\langle\phi,d_0f\rangle\\
&=\langle\phi,\delta\rangle+\langle d_0^*\phi,f\rangle\\
&=\langle\phi,\delta\rangle.
\end{aligned}
\]

This is a valid consequence of the declared linear pairing and adjoint. The norm bound \(\|\phi\|_\infty\le1\) is needed for the paper’s normalized dual optimization, but not for this invariance identity alone.

The result says that the detector cannot distinguish representatives differing by an exact repair. It supplies neither a time evolution nor an action principle. The paper’s phrase “flow conservation at every node” describes the static divergence constraint on the detector; it does not by itself establish a conserved dynamical Noether charge.

**Scope remedy:** label this “invariance under exact repair” or “gauge-invariant detector response.” Any later connection to dynamical conservation needs its own stated evolution and symmetry assumptions.

### S2 — Confirmed, with qualification: Theorem 003-A’s listed assumptions admit the proposed counterexample under their weak reading

The title at line 648 explicitly names **arbitrary disjoint-component additivity**, and the preceding discussion intends a strong decomposability condition. But the theorem’s numbered assumptions instead describe:

- “Edge decomposability” as dependence only on local stalk magnitudes;
- additivity over disjoint **replicas**.

Its proof then uses arbitrary disjoint additivity to split a heterogeneous collection into singletons.

For nonnegative magnitudes \(a=(a_1,\dots,a_n)\), define
\[
J_n(a)=\sqrt{n\sum_{i=1}^{n}a_i^2}.
\]
For each fixed \(n\), this is continuous, convex, positively homogeneous, permutation-invariant, faithful, and dependent only on the listed magnitudes. It is singleton-normalized:
\[
J_1(a)=a.
\]
For \(N\) identical replicas,
\[
J_{Nn}(a^{\sqcup N})
=\sqrt{Nn\,N\sum_i a_i^2}
=N J_n(a).
\]
Nevertheless,
\[
J_2(1,2)=\sqrt{10}\ne3=J_1(1)+J_1(2).
\]

Thus the proposed counterexample is valid against the **weak parenthetical reading**. It does not refute a theorem that explicitly assumes arbitrary component additivity or a stronger decomposition law excluding this aggregation.

Theorem F and the S5 statement, particularly lines 684–693 and 1277, already acknowledge the missing independence bridge. That acknowledgement should be propagated into the exact hypothesis list of Theorem 003-A.

**Remedy:** state
\[
A(a\sqcup b)=A(a)+A(b)
\]
for arbitrary finite heterogeneous components as an explicit assumption, or formally define and prove a stronger decomposition condition that entails it. Identical-replica extensivity alone cannot supply the singleton-splitting step.

### S3 — Confirmed: subtraction is an instance, not the unique consequence of the listed properties

At line 1201, the summary attributes \(D(x,y)=y-x\) to antisymmetry, “linearity,” and faithfulness. Line 204 defines that “linearity” as path additivity:
\[
D(x,y)+D(y,z)=D(x,z).
\]

The counterexample
\[
D(x,y)=2(y-x)
\]
satisfies all three properties. More generally, path additivity gives
\[
D(x,y)=g(y)-g(x),\qquad g(x)=D(0,x),
\]
and faithfulness requires \(g\) to be injective. Even \(g(x)=x^3\) satisfies those stated properties.

The body at lines 214–223 correctly chooses ordinary scalar subtraction and verifies that it is an instance. The overbroad “recovered when the following restrictions are imposed” wording also appears at lines 201–206, so the issue is not confined to the summary.

**Remedy:** describe ordinary subtraction as the supplied scalar specialization, as the actual proof does. A uniqueness claim would require additional hypotheses and normalization; the three listed properties do not establish it.

These are scoped checks of the cited passages and proposed bridge. They are not a full audit of the paper, its companion results, or its formalization.
