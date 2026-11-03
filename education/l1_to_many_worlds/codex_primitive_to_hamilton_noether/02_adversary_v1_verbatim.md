# Independent adversarial review of v1

**Verdict: revise before presenting this as a visual explanation for novices.** The conditional Hamiltonian construction and the explicit Noether example are mathematically sound. The principal problems are inaccurate rate lengths, an unannounced change of example state, and drawings whose operation order does not clearly express their accompanying claims.

I inspected `01_draft_for_review.md`, `render_sheets.py`, `picture_sheet_v1.png`, and `math_sheet_v1.png`. I made no changes.

Severity below concerns the intended teaching task. A high-severity visual defect does not imply that the accompanying theorem is false.

## 1. High — Strip 6 gives the two rates incompatible magnitudes

**Type: mathematical mismatch between drawing and stated rule.**

The first two panels use the same state, \(q=2.8,\ p=1.7\), but both orange arrows have length \(1.2\) (`render_sheets.py`, lines 89–90).

For the stated rule
\[
\dot q=p,\qquad \dot p=-q,
\]
their magnitudes should have ratio \(1.7:2.8\). The drawn ratio is \(1:1\). Interpreting them as small increments over a shared time interval does not fix this: the implied intervals would be \(1.2/1.7\approx0.706\) and \(1.2/2.8\approx0.429\).

If orange indicates direction only, the picture does not establish the proportional coupling required for this particular oscillator. That convention is currently unstated.

**Remedy:** draw orange arrows with a common scale factor, giving lengths \(c\,p\) and \(c\,q\). State that they depict two simultaneous rates. Alternatively, explicitly declare that these arrows show signs only, and supply the magnitude rule separately.

## 2. High — Strip 6 silently changes its starting state and does not visibly show rotation

**Type: continuity error and pedagogical omission; the rotation formula itself is correct.**

The rate panels use \((2.8,1.7)\). The last panel instead starts from \((2.1,1.2)\), drawn with another scale factor, \(0.9\). This is not a uniform rescaling of the earlier state.

The last panel contains these correct oscillator samples:

| Time | \(q\) | \(p\) |
|---|---:|---:|
| 0 | 2.100000 | 1.200000 |
| 0.3 | 2.360831 | 0.525811 |
| 0.6 | 2.410776 | −0.195346 |

However, their origins are moved horizontally to three different locations. The visible result is three upright component pairs with a shrinking green part, then a tiny negative green part. No segment representing the total state visibly turns around a persistent origin.

The caption “Together, the pair turns” therefore requires a construction that the picture does not supply: identify the green tip as the state point and compare its displacement from the pair’s own origin.

**Remedy:** keep the initial state and drawing scale consistent. Make the shared reference origin and moving endpoint apparent through ghosted configurations, or add a straight origin-to-endpoint segment. If retaining separately positioned snapshots, explain that their placement on the page is layout, and that the endpoint relative to each black tail is what rotates. Use a wider angular interval if the purpose is to make turning recognizable.

## 3. High — The printed sheets do not adequately define the new glyph meanings

**Type: pedagogical omission and hidden role change.**

In strips 1–4, arrows behave as freely placed geometric vectors. In strips 6–8, the black and green strokes encode two signed scalar coordinates, with green attached to black’s tip.

The draft explains this more clearly than the delivered sheets. The printed math sheet introduces \(q,p\), but does not explicitly identify black with \(q\), green with \(p\), their sign directions, or the green endpoint with the represented state. “Colours distinguish marks” does not supply that mapping.

This matters especially when green becomes negative in strip 6. The reader has not been taught that a downward green stroke means negative momentum rather than a different physical direction.

**Remedy:** add a compact decoding statement to the companion sheet: black measures \(q\), green measures \(p\); right/up are positive; left/down are negative; the green tip identifies the state relative to the black tail. Explicitly announce that these are now state coordinates. The requested absence of axes and formula labels on the picture page makes this explanation more necessary.

## 4. Medium — Strip 7 does not unambiguously depict the stated commuting operations

**Type: diagram/claim mismatch, not a counterexample to translation symmetry.**

The renderer uses:

- First panel: \(q=2,\ 3.5\), both with \(p=0.65\).
- Second panel: both receive a translation of \(+1\).
- Third panel: both translated states advance by \(0.65\), corresponding to time \(1\).

There are therefore two different horizontal differences: the \(1.5\) separation between the stacked examples, and the \(+1\) translation between the first and second panels. “The same shift survives the move” does not identify which difference is meant.

The third panel does not show the evolved unshifted states alongside their translated counterparts, despite the draft describing advancement of “the shifted and unshifted pairs.” The data are compatible with translation covariance, but the roles of the two histories are ambiguous.

**Remedy:** choose one shift and one time interval. Either show two initial states separated by that shift, evolve both, and visibly retain their separation; or show “slide then move” and “move then slide” reaching the same result. Remove the extra simultaneous translation unless it serves a clearly stated purpose.

## 5. Medium — Sequential captions and arrows invite the finite-kick reading the math sheet rejects

**Type: pedagogical contradiction between presentation and explanation.**

Strip 6 reads left-to-right as:

1. Green determines black’s “next change.”
2. Black determines green’s “opposite change.”
3. The pair turns.

The linking arrows make this look like a sequence of updates. The math sheet correctly says that the first two panels are not consecutive finite kicks, but this correction arrives after the visual has suggested precisely that interpretation.

The two identical starting states in the first panels could communicate simultaneous rate rules, but their sameness is not identified.

**Remedy:** use captions such as “At this instant: black changes this way” and “At the same instant: green changes this way.” Make the third caption explicitly introduce evolution under both rules. The distinction should be readable on the picture page itself.

## 6. Medium — Strip 1 creates a difference by an unannounced operation

**Type: missing operation in the visual argument.**

The second panel contains matching vectors. In the third, green has changed from displacement \((1.4,2)\) to \((2.7,1.1)\): both direction and length change. Translation alone cannot do this.

“Now there is a difference” reports the result without saying what produced it. For an explanation beginning with comparison and primitive difference, this is a significant missing step.

**Remedy:** use a caption such as “Change one; compare again,” or make a specific change visible with a ghosted previous arrow. If only direction matters at this stage, preserve its length and explicitly introduce turning.

## 7. Medium — The companion sheet assumes much of the mathematical vocabulary it is meant to explain

**Type: novice-learning gap, not incorrect mathematics.**

The crucial passage moves through a vector field, area form, contraction, closed one-form, simply connected patch, and Hamiltonian potential without explaining those terms. A novice can read the claimed result but cannot follow why it holds.

The first genuinely explanatory transition is especially compressed:
\[
u_q+v_p=0\quad\Longrightarrow\quad u\,dp-v\,dq=dH.
\]
The symbols are correct. Their meaning and the reason for introducing \(H\) remain inaccessible.

**Remedy:** reserve a few sentences for the actual mechanism:

- The two components specify rates of change.
- Preserving every small area forces their local expansion rates to cancel.
- This cancellation allows one scalar function to generate both rates through its two slopes.
- Hamilton’s equations name that relationship.

Define dots and partial derivatives. A scalar line-integral construction can accompany the differential-form statement if space permits. Spell the translation generator as \(\partial/\partial q\), rather than the visually ambiguous `∂q`.

## 8. Medium — The action argument leaves its variational assumptions unspecified

**Type: incomplete mathematical contract, not a wrong Noether conclusion.**

For this example, the direct proof
\[
\dot p=-H_q=0
\]
is correct. The alternative action explanation says that stationarity supplies the equations, but does not state the allowed variations or endpoint conditions.

A constant translation changes fixed \(q\) endpoints, so it should not silently be treated as an admissible variation within one fixed-endpoint variational problem. Noether’s theorem handles this distinction; the sheet currently leaves it implicit.

**Remedy:** specify independent interior variations of \(q,p\), with \(\delta q\) vanishing at the time endpoints when deriving the equations. Explain that constant translations express a symmetry of the action and map endpoint data to translated endpoint data. The conserved charge then follows along stationary trajectories. One compact sentence can prevent the boundary issue from becoming a hidden assumption.

## 9. Medium — “Geometric phase” introduces unnecessary technical ambiguity

**Type: terminology risk.**

Strip 4 demonstrates an angular position relative to a reference and return after a full rotation. Calling this “geometric phase” can suggest the more specialized concept associated with transport and holonomy. No such transport rule or comparison with dynamical phase has been constructed here.

The explicit rejection of a quantum-amplitude interpretation is helpful, but does not resolve this separate ambiguity.

**Remedy:** call it “relative angle,” “cyclic position,” or “angular phase.” Reserve “geometric phase” for a later construction that defines exactly what is transported and how its phase is compared.

## 10. Low — Two rendering details undermine exact visual reading

**Type: implementation and draft/output fidelity.**

First, the final green segment in strip 6 has rendered length approximately \(0.1758\), shorter than the fixed arrowhead length \(0.2\). The renderer consequently places the head’s base beyond the segment’s start and draws a short shaft in the opposite direction.

**Remedy:** cap arrowhead length as a fraction of the segment length.

Second, the draft says strip 4 has “four ghosted intermediate directions,” while `rotor()` draws three: up, left, and down. Those dashed strokes have no arrowheads and resemble a small coordinate cross; their temporal order is also invisible.

**Remedy:** correct the count and use directional ghost arrows or a caption identifying successive turns in the same direction.

## What survives the review

I found no sign error in the conditional Hamiltonian derivation:
\[
\iota_X(dq\wedge dp)=u\,dp-v\,dq,\qquad
d(\iota_X\omega)=(u_q+v_p)\,dq\wedge dp.
\]
The local exactness conclusion is valid under the stated hypotheses.

The oscillator update, its conservation of \(H\), and the stated Euler area/energy factor \(1+h^2\) are correct. The shear drawings preserve their positively oriented area. The free-particle flow, its translation symmetry, and the charge \(J=p\) are correct.

The draft also explicitly distinguishes supplied structure from derived consequences and does not claim a derivation of quantum mechanics. Preserve those limits. The necessary revision is to make the pictures accurately and intelligibly express this bounded classical construction.
