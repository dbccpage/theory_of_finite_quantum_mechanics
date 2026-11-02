---
title: "From Marbles to Everett in Five Moves"
subtitle: "A classroom route to the double slit, what a detector does, and what \"many worlds\" actually claims. No bra-kets. Arithmetic only."
author: "Jeremy H. Carroll"
date: "2026-11-02"
---

**The one idea.** Keep a scoreboard. When the scoreboard fails to predict what happens next, find the smallest pair of cases that the scoreboard scores the same but the world treats differently. That pair is a *witness*. Add to the scoreboard exactly what the witness shows is missing, and nothing more. Repeat. Stop when no witness forces anything further. Everett is where this ladder stops. The step after it, calling the lines of the ledger "worlds", is the one step no witness forces.

## Move 1. Marbles: scores add

Drop marbles through two holes in a board onto the floor. Left hole open: a pile under it. Right hole open: a pile under it. Both open: both piles, and the count on any floor tile is the left count plus the right count.

The scoreboard is a count per tile. Counts can only add. Students write the row for a tile between the piles: **left 1, right 1, both 2.**

> **Teacher box.** This is the phase-blind report, a pair of non-negative weights $(w_1,w_2)$. "Both equals left plus right" is the entire content of classical probability for this setup.

## Move 2. The witness: same scores, opposite outcome

Two speakers, one tone, the same volume on each. Stand at the midpoint: loud. Now swap the two wires on one speaker. Both volume meters still read exactly what they read before. At the midpoint: near silence. (Noise-cancelling headphones are the same trick: they add a flipped copy of the noise. Two sounds, each just as loud as before, and the sum is quiet.)

Write it as arithmetic. Each speaker contributes a push that can be $+$ or $-$.

<figure><svg viewBox="0 0 540 205" width="100%" role="img" aria-label="Two speaker setups with identical scoreboards and opposite loudness" style="max-width:540px;display:block;margin:0 auto;font-family:inherit"><g transform="translate(0,0)"><text x="130" y="22" text-anchor="middle" font-size="14" font-weight="600">both wires normal</text><line x1="70" y1="110" x2="70" y2="60" stroke="currentColor" stroke-width="3"/><polygon points="64,54 76,54 70,60" fill="currentColor"/><text x="70" y="126" text-anchor="middle" font-size="13">left +1</text><line x1="190" y1="110" x2="190" y2="60" stroke="currentColor" stroke-width="3"/><polygon points="184,54 196,54 190,60" fill="currentColor"/><text x="190" y="126" text-anchor="middle" font-size="13">right +1</text><rect x="20" y="130" width="220" height="64" rx="6" fill="var(--card, #f1f1ec)" stroke="var(--rule, #999)"/><text x="130" y="152" text-anchor="middle" font-size="13">scoreboard: 1² + 1² = 2</text><text x="130" y="172" text-anchor="middle" font-size="13">total push +2, loudness 2² = 4</text></g><g transform="translate(280,0)"><text x="130" y="22" text-anchor="middle" font-size="14" font-weight="600">one wire swapped</text><line x1="70" y1="110" x2="70" y2="60" stroke="currentColor" stroke-width="3"/><polygon points="64,54 76,54 70,60" fill="currentColor"/><text x="70" y="126" text-anchor="middle" font-size="13">left +1</text><line x1="190" y1="60" x2="190" y2="110" stroke="currentColor" stroke-width="3"/><polygon points="184,116 196,116 190,110" fill="currentColor"/><text x="190" y="52" text-anchor="middle" font-size="13">right −1</text><rect x="20" y="130" width="220" height="64" rx="6" fill="var(--card, #f1f1ec)" stroke="var(--rule, #999)"/><text x="130" y="152" text-anchor="middle" font-size="13">scoreboard: 1² + 1² = 2</text><text x="130" y="172" text-anchor="middle" font-size="13">total push 0, loudness 0² = 0</text></g></svg><figcaption>Same meters, opposite outcome. The scoreboard (1, 1) cannot tell the two apart; the next step can.</figcaption></figure>

$$(1+1)^2=4,\qquad (1-1)^2=0,\qquad \text{scoreboard } 1^2+1^2=2 \text{ in both cases.}$$

That is a witness: two situations with an identical scoreboard and opposite outcomes. It proves the scoreboard is missing something, and it says exactly what: a **direction**. Marbles do not have one. Sounds do. The striped double-slit pattern says that whatever passes through the slits has one too.

The smallest repair: each path contributes a push with a size and a direction, and the pile height is the square of the total push. In words,

$$\text{height}=(\text{push}_1)^2+(\text{push}_2)^2+2\,(\text{push}_1)(\text{push}_2)\,(\text{alignment}).$$

The last term is the only new thing. "Alignment" runs from $+1$ (same direction) through $0$ to $-1$ (opposite). It can make a pile taller than the sum of the two, or make it vanish. That is the whole of interference.

> **Teacher box.** $P=w_1+w_2+2\sqrt{w_1w_2}\cos\theta$, equation (E1) of the math note. The two-row witness $(1,1)$ versus $(1,-1)$ with readouts $(4,0)$ versus $(0,4)$ is kernel-checked: `InterferenceNonDescent.mix_psi1` and `mix_psi2` compute the two readouts, and `InterferenceNonDescent.no_descent_through_fiber` shows that no function of the scoreboard reproduces both. "Direction" is the relative phase. With three paths you never need anything beyond pairs (Sorkin, $I_3=0$).

## Move 3. One marble at a time

The speaker demo uses two sources. The fact that makes this physics rather than acoustics: send electrons or photons **one at a time**, and the dots still build the stripes, with dark bands where either slit alone would land hits. So the two pushes with directions belong to a single marble. One marble's two options add like pushes, not like counts.

Do not explain this. Record it. It is the experimental fact on which the rest of the lesson stands.

> **Teacher box.** This is where "superposition" earns its name: one particle carries one direction assignment, and the scoreboard only says which set of assignments (the fiber over a weight point) it lies in. The scoreboard cannot tell points of the fiber apart; mixing can.

## Move 4. The tag: what a detector does

Put a detector at the slits that tags each marble: "went left" or "went right". Students expect the story "looking disturbs it". The arithmetic says something cleaner.

Back to the speakers. Give them slightly different pitches. Now you can tell which speaker any sound came from: the pitch is a tag. Stand at the midpoint. No silence any more; the two loudnesses simply add. Cancellation requires the two contributions to be the same kind of thing. A tag makes them different kinds of things.

Make the pitches nearly equal and you hear beats: the cancellation comes and goes. Listen for a short window and you catch the cancellation; listen for a long one and it averages away. How alike the two sounds are over your listening window is the tag overlap, and it is one dial, from full stripes (tags identical, so no information about the path) to plain piles (tags fully distinguishable).

<figure><svg viewBox="0 0 540 125" width="100%" role="img" aria-label="Stripe visibility falling as tags become distinguishable" style="max-width:540px;display:block;margin:0 auto;font-family:inherit"><g><polyline points="10.0,25.0 10.9,25.1 11.9,25.4 12.8,26.0 13.8,26.7 14.7,27.7 15.6,28.8 16.6,30.2 17.5,31.7 18.4,33.4 19.4,35.3 20.3,37.3 21.2,39.4 22.2,41.7 23.1,44.1 24.1,46.6 25.0,49.2 25.9,51.8 26.9,54.5 27.8,57.3 28.8,60.0 29.7,62.7 30.6,65.5 31.6,68.2 32.5,70.8 33.4,73.4 34.4,75.9 35.3,78.3 36.2,80.6 37.2,82.7 38.1,84.7 39.1,86.6 40.0,88.3 40.9,89.8 41.9,91.2 42.8,92.3 43.8,93.3 44.7,94.0 45.6,94.6 46.6,94.9 47.5,95.0 48.4,94.9 49.4,94.6 50.3,94.0 51.2,93.3 52.2,92.3 53.1,91.2 54.1,89.8 55.0,88.3 55.9,86.6 56.9,84.7 57.8,82.7 58.8,80.6 59.7,78.3 60.6,75.9 61.6,73.4 62.5,70.8 63.4,68.2 64.4,65.5 65.3,62.7 66.2,60.0 67.2,57.3 68.1,54.5 69.1,51.8 70.0,49.2 70.9,46.6 71.9,44.1 72.8,41.7 73.8,39.4 74.7,37.3 75.6,35.3 76.6,33.4 77.5,31.7 78.4,30.2 79.4,28.8 80.3,27.7 81.2,26.7 82.2,26.0 83.1,25.4 84.1,25.1 85.0,25.0 85.9,25.1 86.9,25.4 87.8,26.0 88.8,26.7 89.7,27.7 90.6,28.8 91.6,30.2 92.5,31.7 93.4,33.4 94.4,35.3 95.3,37.3 96.2,39.4 97.2,41.7 98.1,44.1 99.1,46.6 100.0,49.2 100.9,51.8 101.9,54.5 102.8,57.3 103.8,60.0 104.7,62.7 105.6,65.5 106.6,68.2 107.5,70.8 108.4,73.4 109.4,75.9 110.3,78.3 111.2,80.6 112.2,82.7 113.1,84.7 114.1,86.6 115.0,88.3 115.9,89.8 116.9,91.2 117.8,92.3 118.8,93.3 119.7,94.0 120.6,94.6 121.6,94.9 122.5,95.0 123.4,94.9 124.4,94.6 125.3,94.0 126.2,93.3 127.2,92.3 128.1,91.2 129.1,89.8 130.0,88.3 130.9,86.6 131.9,84.7 132.8,82.7 133.8,80.6 134.7,78.3 135.6,75.9 136.6,73.4 137.5,70.8 138.4,68.2 139.4,65.5 140.3,62.7 141.2,60.0 142.2,57.3 143.1,54.5 144.1,51.8 145.0,49.2 145.9,46.6 146.9,44.1 147.8,41.7 148.8,39.4 149.7,37.3 150.6,35.3 151.6,33.4 152.5,31.7 153.4,30.2 154.4,28.8 155.3,27.7 156.2,26.7 157.2,26.0 158.1,25.4 159.1,25.1 160.0,25.0" fill="none" stroke="var(--accent, #1f6f54)" stroke-width="2.5"/><line x1="10" y1="95" x2="160" y2="95" stroke="currentColor" stroke-width="1" opacity=".5"/><text x="85" y="118" text-anchor="middle" font-size="12">tags identical: full stripes</text></g><g><polyline points="190.0,42.5 190.9,42.6 191.9,42.7 192.8,43.0 193.8,43.4 194.7,43.8 195.6,44.4 196.6,45.1 197.5,45.8 198.4,46.7 199.4,47.6 200.3,48.6 201.2,49.7 202.2,50.9 203.1,52.1 204.1,53.3 205.0,54.6 205.9,55.9 206.9,57.3 207.8,58.6 208.8,60.0 209.7,61.4 210.6,62.7 211.6,64.1 212.5,65.4 213.4,66.7 214.4,67.9 215.3,69.1 216.2,70.3 217.2,71.4 218.1,72.4 219.1,73.3 220.0,74.2 220.9,74.9 221.9,75.6 222.8,76.2 223.8,76.6 224.7,77.0 225.6,77.3 226.6,77.4 227.5,77.5 228.4,77.4 229.4,77.3 230.3,77.0 231.2,76.6 232.2,76.2 233.1,75.6 234.1,74.9 235.0,74.2 235.9,73.3 236.9,72.4 237.8,71.4 238.8,70.3 239.7,69.1 240.6,67.9 241.6,66.7 242.5,65.4 243.4,64.1 244.4,62.7 245.3,61.4 246.2,60.0 247.2,58.6 248.1,57.3 249.1,55.9 250.0,54.6 250.9,53.3 251.9,52.1 252.8,50.9 253.8,49.7 254.7,48.6 255.6,47.6 256.6,46.7 257.5,45.8 258.4,45.1 259.4,44.4 260.3,43.8 261.2,43.4 262.2,43.0 263.1,42.7 264.1,42.6 265.0,42.5 265.9,42.6 266.9,42.7 267.8,43.0 268.8,43.4 269.7,43.8 270.6,44.4 271.6,45.1 272.5,45.8 273.4,46.7 274.4,47.6 275.3,48.6 276.2,49.7 277.2,50.9 278.1,52.1 279.1,53.3 280.0,54.6 280.9,55.9 281.9,57.3 282.8,58.6 283.8,60.0 284.7,61.4 285.6,62.7 286.6,64.1 287.5,65.4 288.4,66.7 289.4,67.9 290.3,69.1 291.2,70.3 292.2,71.4 293.1,72.4 294.1,73.3 295.0,74.2 295.9,74.9 296.9,75.6 297.8,76.2 298.8,76.6 299.7,77.0 300.6,77.3 301.6,77.4 302.5,77.5 303.4,77.4 304.4,77.3 305.3,77.0 306.2,76.6 307.2,76.2 308.1,75.6 309.1,74.9 310.0,74.2 310.9,73.3 311.9,72.4 312.8,71.4 313.8,70.3 314.7,69.1 315.6,67.9 316.6,66.7 317.5,65.4 318.4,64.1 319.4,62.7 320.3,61.4 321.2,60.0 322.2,58.6 323.1,57.3 324.1,55.9 325.0,54.6 325.9,53.3 326.9,52.1 327.8,50.9 328.8,49.7 329.7,48.6 330.6,47.6 331.6,46.7 332.5,45.8 333.4,45.1 334.4,44.4 335.3,43.8 336.2,43.4 337.2,43.0 338.1,42.7 339.1,42.6 340.0,42.5" fill="none" stroke="var(--accent, #1f6f54)" stroke-width="2.5"/><line x1="190" y1="95" x2="340" y2="95" stroke="currentColor" stroke-width="1" opacity=".5"/><text x="265" y="118" text-anchor="middle" font-size="12">tags partly tellable: faint</text></g><g><polyline points="370.0,60.0 370.9,60.0 371.9,60.0 372.8,60.0 373.8,60.0 374.7,60.0 375.6,60.0 376.6,60.0 377.5,60.0 378.4,60.0 379.4,60.0 380.3,60.0 381.2,60.0 382.2,60.0 383.1,60.0 384.1,60.0 385.0,60.0 385.9,60.0 386.9,60.0 387.8,60.0 388.8,60.0 389.7,60.0 390.6,60.0 391.6,60.0 392.5,60.0 393.4,60.0 394.4,60.0 395.3,60.0 396.2,60.0 397.2,60.0 398.1,60.0 399.1,60.0 400.0,60.0 400.9,60.0 401.9,60.0 402.8,60.0 403.8,60.0 404.7,60.0 405.6,60.0 406.6,60.0 407.5,60.0 408.4,60.0 409.4,60.0 410.3,60.0 411.2,60.0 412.2,60.0 413.1,60.0 414.1,60.0 415.0,60.0 415.9,60.0 416.9,60.0 417.8,60.0 418.8,60.0 419.7,60.0 420.6,60.0 421.6,60.0 422.5,60.0 423.4,60.0 424.4,60.0 425.3,60.0 426.2,60.0 427.2,60.0 428.1,60.0 429.1,60.0 430.0,60.0 430.9,60.0 431.9,60.0 432.8,60.0 433.8,60.0 434.7,60.0 435.6,60.0 436.6,60.0 437.5,60.0 438.4,60.0 439.4,60.0 440.3,60.0 441.2,60.0 442.2,60.0 443.1,60.0 444.1,60.0 445.0,60.0 445.9,60.0 446.9,60.0 447.8,60.0 448.8,60.0 449.7,60.0 450.6,60.0 451.6,60.0 452.5,60.0 453.4,60.0 454.4,60.0 455.3,60.0 456.2,60.0 457.2,60.0 458.1,60.0 459.1,60.0 460.0,60.0 460.9,60.0 461.9,60.0 462.8,60.0 463.8,60.0 464.7,60.0 465.6,60.0 466.6,60.0 467.5,60.0 468.4,60.0 469.4,60.0 470.3,60.0 471.2,60.0 472.2,60.0 473.1,60.0 474.1,60.0 475.0,60.0 475.9,60.0 476.9,60.0 477.8,60.0 478.8,60.0 479.7,60.0 480.6,60.0 481.6,60.0 482.5,60.0 483.4,60.0 484.4,60.0 485.3,60.0 486.2,60.0 487.2,60.0 488.1,60.0 489.1,60.0 490.0,60.0 490.9,60.0 491.9,60.0 492.8,60.0 493.8,60.0 494.7,60.0 495.6,60.0 496.6,60.0 497.5,60.0 498.4,60.0 499.4,60.0 500.3,60.0 501.2,60.0 502.2,60.0 503.1,60.0 504.1,60.0 505.0,60.0 505.9,60.0 506.9,60.0 507.8,60.0 508.8,60.0 509.7,60.0 510.6,60.0 511.6,60.0 512.5,60.0 513.4,60.0 514.4,60.0 515.3,60.0 516.2,60.0 517.2,60.0 518.1,60.0 519.1,60.0 520.0,60.0" fill="none" stroke="var(--accent, #1f6f54)" stroke-width="2.5"/><line x1="370" y1="95" x2="520" y2="95" stroke="currentColor" stroke-width="1" opacity=".5"/><text x="445" y="118" text-anchor="middle" font-size="12">tags fully tellable: piles</text></g></svg><figcaption>One dial. Height = sum of the two piles plus the cross term times the tag overlap (1 → ½ → 0).</figcaption></figure>

Nothing was deleted. The pushes still have directions. They are married to different tags, and pushes with different tags do not cancel.

$$\text{height}=(\text{push}_1)^2+(\text{push}_2)^2+2\,(\text{push}_1)(\text{push}_2)\,(\text{alignment})\,(\text{tag overlap}).$$

Tag overlap $1$: Move 2. Tag overlap $0$: Move 1. A measurement is the tag overlap going to zero, whatever the tag is made of: a detector, a stray air molecule, a scattered photon, a student's eye. No mind is required, and no disturbance story is required either.

The twist students love: sort the dots by what the tag later says, and each sorted subset shows stripes, shifted so that the two subsets add up to no stripes. Sorting does not change the full pile, and nothing travels backward in time. A different operation, coherently undoing the tagging interactions before the dots land, can restore interference in the full pile. That becomes impractical once tags have spread into air, light and heat; it is not forbidden by unitary evolution.

> **Teacher box.** The cross term is multiplied by the overlap $\gamma=\langle E_1|E_2\rangle$ of the two tag states, equation (E2); visibility and distinguishability obey $V^2+D^2=1$. The speaker analogy is exact in this sense: the two tags are the two time profiles, and the overlap is their correlation over the listening window. Decoherence is not collapse: the directions still exist in the marble-plus-tag system, and a joint test recovers them (the recoherence witness $(1+\cos\varphi)/2$ in the math note). Eraser: $|x+y|^2+|x-y|^2=2(|x|^2+|y|^2)$.

## Move 5. The ledger: Everett without bra-kets

Write the full ledger after the tag:

$$[\text{marble left and tag says left}]\;+\;[\text{marble right and tag says right}]$$

Add the student who reads the tag:

$$[\text{left, tag left, student saw left}]\;+\;[\text{right, tag right, student saw right}]$$

Each line holds one definite record. No line says "both". And the rules of Moves 2 to 4 never delete a line; they only attach tags to lines. That is the core of Everett's 1957 proposal: read the ledger literally. Both lines are there, each with its own reader who sees one result. "Many worlds" is a name for the lines.

What it buys: no extra deletion rule. What it costs, honestly:

- **The weights are not a count of lines.** A one-third / two-thirds split is not "two lines", and some splits match no whole-number count at all: the weights $(5\pm\sqrt5)/10$ cannot be reproduced by any equal-weight subdivision (the arithmetic is kernel-checked in the repository; the last step is the standard rational root theorem). Everettians agree that weights are not counts. So "why these weights" has to be supplied or argued for separately: Deutsch and Wallace argue for it from rules of rational choice, and those rules then become the input.
- **Which lines are "the" lines** depends on the tags being perfectly distinguishable, which is only ever approximately true. Everettians reply that approximate is good enough; the point is that the choice is not written in the ledger.

And the test nobody can run: the pile heights are computed from the ledger the same way whether or not you call its lines "worlds". The word adds no prediction and removes none. So Everett is not needed to predict anything, and nothing predicted excludes it.

What **would** exclude it: directions fading on their own, with no tag anywhere, not even an air molecule. Then the ledger rule itself is wrong, and so is every theory that keeps it (Everett, Bohm, and textbook quantum mechanics between measurements). Experiments keep raising the size at which this has been checked. So far, directions fade only when something tags.

> **Teacher box.** Equation (E3), $\Psi=\sum_i c_i\,|i\rangle|E_i\rangle|O_i\rangle$. The predicate "the terms are worlds" is not an argument of $\mathrm{Tr}(\rho F)$, so it changes no prediction. The reduced-system decay $\rho_{01}\mapsto(3/5)^k\rho_{01}$ (kernel-checked phase damping) also arises from unitary coupling to fresh environment qubits. It is not by itself evidence for fundamental collapse: that would require a specified closed-system model and exclusion of environmental and technical explanations. Branch count versus weight: `RationalSector.lean`.

## The ladder, as witnesses

| Scoreboard | Witness that breaks it | What gets added |
|---|---|---|
| counts per tile | two speakers, one wire flipped: same meters, loudness 4 versus 0 | a direction per path |
| sizes and directions | tag the paths: stripes fade exactly as the tags become distinguishable | a tag per path (a record) |
| the tagged ledger | none: the ledger predicts every pile | nothing is forced; "worlds" is a reading of the ledger, not a line in it |

**What a witness is, in one sentence:** a pair of cases that your description calls the same but the next step tells apart. It proves the description is incomplete and shows the minimum you must add.

## For the student

The stripes are what two options do when nothing can tell them apart. A measurement is anything that can tell them apart, and the stripes fade exactly as fast as the telling-apart gets good. Everett is the refusal to erase from the ledger the option you did not see. Whether that refusal is a fact about the world is open and sharp, and it is yours to think about. Nobody has a proof either way, and anyone who tells you otherwise is skipping a step.

### Pocket version (fits one post)

> Marbles through two holes make two piles: counts only add. Light and electrons make stripes, with dark bands where either hole alone would land hits. So each path carries a size and a direction, and opposite directions cancel. A detector needn't disturb anything: it tags the paths, and tagged pushes can't cancel. The stripes fade exactly as fast as the tags become tellable-apart. Everett just refuses to erase the line you didn't see from the ledger. Whether that's reality is still open.
>
> (491 characters, counted by `count_threads_safe.py`.)

## Classroom kit, ten minutes

1. Two small speakers (or two phones with a tone app on the same note). Stand at the midpoint, then swap one speaker's wires, or use the app's "invert" switch. Reflections blur it, so stay close.
2. Detune one speaker by a few hertz (beats, partial tags), then by a lot (no cancellation, plain addition).
3. Scoreboard sheet, three columns: meters, total push, loudness. Rows $(+1,+1)$ and $(+1,-1)$.
4. Ledger sheet: students write the two lines of Move 5 and add themselves as readers.
