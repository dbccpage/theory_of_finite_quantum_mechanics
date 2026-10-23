# Study guide — Discrete Deformation Calculus v1.0.3

Read the [manuscript](../discrete_deformation_calculus.md), then use this guide
to compute examples and challenge their interpretation.

## Learning route

| Stage | Reading | What you should be able to do |
|---|---|---|
| 1. Declare the model | Spine §§1–3 | Specify vertices, ordered oriented edges, signed faces, positive weights and a detector; check $d_1d_0=0$. |
| 2. Measure | Spine §3; Chapter 2 | Separate exactness, closure and representative norm; check both sides of a primal/dual certificate. |
| 3. Admit steps | Spine §§7, 10; Chapters 1–8 | Check the letter law and control law separately; explain every witness assumption. |
| 4. Compose and challenge | Spine §11; both notebooks | Prove no free diagnostic decrease and CREDIT necessity; supply a failing converse. |
| 5. Bound the evidence | Spine §§5, 9, 13, 16 | Distinguish measured replay, abstract policy checks, anchored history and authorization; locate open claims. |

Prerequisites are exact rational arithmetic, directed graphs and elementary
linear algebra. Keep all edge orders explicit: changing an orientation
changes signs in both the cochain and its operators.

## Three diagnostic classes

For positive edge weights,

$$\Phi_1(x)=\min_\varphi\sum_e w_e|x_e-(d_0\varphi)_e|,
\qquad \Gamma_2(x)=\|d_1x\|_1.$$

| Class | Diagnostic condition | What follows |
|---|---|---|
| ExactRepair | $\Phi_1=\Gamma_2=0$ | $x=d_0\varphi$; a gauge repair can remove the defect. |
| ClosedResidual | $\Phi_1>0$, $\Gamma_2=0$ | The cochain is closed but not exact. An unchanged T routes to Residual. |
| ActiveClosureFailure | $\Gamma_2>0$ | Closure fails; an unchanged T is refused. |

For genuinely measured states, $\Phi_1=0$ implies $\Gamma_2=0$ by the chain
law. The abstract `State` type permits inconsistent supplied pairs; its
classification gives positive $\Gamma_2$ priority. Carrier-bound replay rejects
such pairs when they disagree with measurement.

## Worked example 1: a closed survivor and a certified minimum

Take the hollow oriented triangle $a\to b\to c\to a$, weights $(2,3,5)$,
and $x=(1,0,0)$. There are no faces, so $\Gamma_2=0$. Its circulation is 1,
so it is not exact. The zero potential has objective 2. The flow
$y=(2,2,2)$ has zero divergence, obeys $|y_e|\le w_e$, and gives
$\langle y,x\rangle=2$. Primal upper and dual lower bounds agree:
$\Phi_1=2$ and the class is ClosedResidual.

Adding the signed triangle face gives $d_1x=1$, hence $\Gamma_2=1$ and
ActiveClosureFailure. The same $d_0$, weights and cochain give the same
$\Phi_1$. Adding a face changes closure; it does not make the circulation exact.

The dual certificate is independently checkable: for every feasible $y$,
zero divergence removes the potential term and

$$\langle y,x\rangle=\langle y,x-d_0\varphi\rangle
\le\sum_e w_e|x_e-(d_0\varphi)_e|.$$

This inequality needs no appeal to a solver's assertion of optimality.

## Worked example 2: representative norm versus quotient distance

Use vertices $a<b<c<d$ and edges $(ab,ac,ad,bc,bd,cd)$, oriented increasingly,
with unit weights, no faces and $x=(-1,-1,-1,-1,-1,-1)$.
The forest $(ab,ac,ad)$ fixes potential $(0,-1,-1,-1)$ and leaves
representative $(0,0,0,-1,-1,-1)$, with recorded norm 3.

The potential $(0,-1,-1,-2)$ instead leaves $(0,0,1,-1,0,0)$, with norm 2.
The dual flow $(-1,0,1,-1,0,-1)$ is divergence-free, lies in the unit box,
and pairs with $x$ to give 2. Therefore $\Phi_1=2$, including after the
forest projection. Its register has three coordinates, the graph's cycle
rank; this is not necessarily the first Betti number after faces are attached.

Both representatives differ from $x$ by an exact cochain. Quotient
preservation does not require the chosen representative to minimize its norm.
`ResidualProjectionReceipt.residual_norm` is an unweighted vector norm;
use `cochain.phi1_certificate` for a certified quotient minimum.

## Worked example 3: repair can reduce raw norm without diagnostic progress

On a two-edge path $a\to b\to c$, let $x=(2,-3)$. Potential $(0,2,-1)$
has $d_0\varphi=x$. The raw norm is 5, but $\Phi_1=\Gamma_2=0$ already.
E sends $x$ to zero and reduces its raw norm to zero. It lowers neither
diagnostic, so the no-free-decrease theorem is respected. Do not read that
theorem as saying that E never repairs anything.

## Eight letters, two admission checks

| Letter | Principal step guard | Evidence boundary |
|---|---|---|
| E | Same carrier, exact starting class, zero final defect, adequate initial detector | Abstract exactness is supplied; measured replay recomputes it. |
| R | Same carrier and equal diagnostics, adequate initial detector | Equal diagnostics alone do not preserve quotient class; measured replay checks exact difference. |
| C | Changed carrier; neither diagnostic decreases | A read-only exposure is not automatically an admitted C step. |
| I | Unchanged state; receipt flag true | A presence flag does not authenticate a receipt. |
| Λ | Changed carrier; licence flag and closed-residual or inadequate-detector trigger | A trigger does not establish a licence. |
| D | Changed carrier; loss-ledger flag true | The abstract law does not check the numerical loss ledger. |
| M | Unchanged state; named in-trace refusal reason | An intake refusal stays outside the tape. |
| T | Unchanged state; zero closure defect and adequate detector | Routing and authority are separate axes. |

The control check is additional: Open admits any letter subject to its law;
Refused admits only C, Λ or T; Terminalized admits none. M changes control to
Refused; it does not itself seal the tape. A failed proposal is not committed.

The auxiliary `FiniteLambdaLedger` is a consistency checker over declared
Boolean flags. It checks exact nonnegative diagnostics, frozen row storage,
adjacency and endpoints. It neither measures diagnostics nor executes the
external Rust certificate methods. A nonempty ledger can have an unresolved
endpoint under this local gate; a resolution policy must check that separately.

## Worked example 4: a lawful CREDIT needs more than its two necessities

On a hollow triangle, $(1,2,-3)$ has zero circulation and is exact.
C can expose this exact defect from an empty declared carrier without lowering
either diagnostic; R can retain the state; E can set it to zero; a booked D
can move that zero to a smaller carrier; I with a receipt and T can then finish.
All six laws hold.

Now retain the exact start and booked D but set the I receipt flag to false.
The proposal is refused at I. Exact start and booked descent are necessary,
and their conjunction is insufficient. Conversely, a closed survivor can
reach an exact endpoint through a booked D because the abstract law permits
that change. An extending lift with commuting restriction cannot exactify
the old survivor; the stronger restriction theorem applies only under its
stated map hypotheses.

## Receipts and formal proof

`run_tape` without a carrier map checks supplied states and witness flags.
With `carriers=...`, it recomputes diagnostics and R's exact-difference
condition and binds topology and weights into genesis. Neither mode verifies
licence authenticity or general detector adequacy.

Internal hash consistency can survive a completely rehashed replacement or
truncation. Retain `tape.checkpoint()` independently and pass it to
`verify_integrity(checkpoint)` to compare genesis, head and length. The
security interpretation still assumes SHA-256 collision resistance.

The 61 Lean theorem sources establish typed statements in an abstract model:
natural-number diagnostics, integer residual lists and Boolean witness
assumptions. The graph optimizer and rational Hodge decomposition have written
proofs and exact Python checks, rather than full Lean mechanizations. The
retained axiom report and a fresh kernel run are different evidence.

## Practice and verification

Predict results before running either notebook. For each claim, name its setting,
its hypotheses, its evidence type and one interpretation it does not support.

```bash
python -m pytest -q code/tests/test_publication_regressions.py
python scripts/replay_notebooks.py --check
python verify_deposit.py --full
```
