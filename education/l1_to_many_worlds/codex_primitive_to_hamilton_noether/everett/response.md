# Response to the independent review

The [review](review.md) refers to the first commit on this PR. Its eight findings appear there in the reviewer's words.

| Finding | Repair |
|---|---|
| 1. The sign entered twice | The speaker calculation uses signed pushes on one line. The angle formula uses nonnegative lengths. The tag formula uses the overlap magnitude and includes its phase once. |
| 2. The fringe tradeoff and beats | The classroom example gives visibility 0.8 for distinguishability 0.6 under the ideal balanced assumptions. The speaker demo distinguishes instantaneous beats from the average over a beat period. |
| 3. What the witness proves | The two-meter witness rules out that scoreboard. The revised lesson introduces one model that fits the data and restricts the comparison of interpretations to the same preparation, dynamics and readout. |
| 4. Which record the reader copies | The text identifies the detector and copying interaction that select a record basis and allows other correlated decompositions of the balanced state. |
| 5. Arrow lengths | Both panels now use the same arrow length on the same scale. The cancellation panel omits the grey tick, and the caption describes cancellation at the exit. |
| 6. Counting launches | The math page gives probabilities per launch and per transmitted particle. The marble experiment specifies equal run times and fixed incoming flux through each open hole. |
| 7. Speaker figure | Each arrowhead now points along its shaft. The figure and worksheet label the squared quantities as relative intensity. |
| 8. Reversal and the three posts | The README places reversal before testing the exit and introduces the tweets as a sequence. |

The checks reproduce the balanced input, recorded state and reversal probabilities. A classroom trial with first-time readers remains open.

## Independent recheck, verbatim

**Recheck at `7344f2f7ad43a5f38eddaf4522a3f3bf709084ba`.** I checked all eight repairs and inspected the committed PNG and both PDF pages. The interference signs, visibility example, counting denominators, arrow lengths and directions, and reversal timing check out. The packet’s exit probabilities agree with the corrected diagrams.

One clarification remains in finding 4. “The balanced state also has perfectly correlated pairs when written in rotated bases” holds for the route–detector pair **before the reader copies the mark**. The immediately preceding example includes the reader. After that copy, measuring the route and detector alone in their respective \(+\)/\(−\) bases gives all four pairs with probability \(1/4\) each. Start the sentence with “Before the student reads the tag, the balanced route–detector state…” to make clear which experiment supports the claim. This clarification leaves the packet’s calculation intact. [Classroom draft, lines 66–79](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/blob/7344f2f7ad43a5f38eddaf4522a3f3bf709084ba/atlas/papers/everett_mw/marbles_to_everett.md#L66-L79)

## Repair after recheck

The classroom draft now places the rotated-basis example before the reader copies the mark. After copying, ignoring the reader leaves an equal mixture of matching route and detector records in the original basis.
