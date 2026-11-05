# Repair log: an outside review of the markup board

Date: 2026-11-05. Board: [markup_board.html](../05_boards/markup_board.html) (published as "What You Owe Me"). The reviewer marked the original 11 cards **2 Right, 6 Wrong, 3 Unsure**. For each mark, the table records what failed, whether the objection holds, the repair, and whether the card's conclusion still follows. Where the first reviewer overreached, that is recorded too.

Objection types: **premise** (a premise is false), **inference** (a step does not follow), **fact** (a fact is wrong), **conclusion** (the conclusion goes further than the steps).

| # | Card | Reviewer | Type | Does the objection hold? | Repair | Does the conclusion still follow? |
|---|---|---|---|---|---|---|
| 1 | The tree | Right | premise | Yes. Comparing R1 with R2 already uses a declared way of reading the records. | Picture 1 now admits assumptions one at a time. Step 1, "R1 and R2 differ", is witnessed only under a supplied reading. | Yes: observed difference ≠ a uniquely established history. |
| 2 | Yesterday | Wrong | conclusion | Yes. "Yesterday is a row" confused the evidence with the event. | Became "the row is evidence about yesterday, read now". The card was later dropped from the board. | Narrowed: the claim is about access to yesterday, not about whether yesterday happened. |
| 3 | Observation | Wrong | premise | Yes. The five steps are the WDP certification ladder, not a law of physics. | Labelled as WDP's. Step 2 (a record) can happen with nobody hearing. | Yes, for certified observation. |
| 4 | Observer | Right | — | Accepted: label it as the proposed model. | Labelled as the WDP model. | Yes. |
| 5 | Unreported | Wrong | inference | **Partly.** For two fixed worlds and a deterministic report $D = q(\cdot)$, $P(D\mid A) = [q(A)=D] = [q(B)=D] = P(D\mid B)$, so the Bayes factor is 1 by the card's own setup. The first reviewer is right that this fails for hypotheses that are distributions over states, or for noisy channels that do not factor through $q$. The card did not state those conditions. | The equal-likelihood condition is now written out, "on this channel". The card now keeps claims (a), (b) and (c) apart (below). | Yes, on the stated channel. Not for every channel. |
| 6 | Every observer | Wrong | conclusion | **Partly.** The card's formula already had the condition $\lvert P\rvert < \lvert X\rvert$. Only its title and line dropped it. | Title is now "when states outnumber reports". The line says the condition is supplied for a tree, the air or a brain. | Yes, under the condition. The card was later folded into Picture 2. |
| 7 | Video game | Wrong | fact | Yes. Games do not all keep simulating offscreen. | Drawing, simulating and keeping state are three jobs. Her analogy must say which one the universe skips. | Changed: the analogy no longer counts *against* her. It is simply underspecified. |
| 8 | What she owes | Unsure | conclusion | Yes. "claim − {…} = a story" was rhetoric. | Now "owed before the claim can be checked". A claim can have content without a test. | Narrowed to checkability. |
| 9 | Paper's mathematics | Wrong | fact | **Partly.** The paper states 2.5 PB and 30 TB. Our 2.6 PB and 31 TB are recomputed from its own inputs: $4(1.3)(2\,\text{mm})/(500\,\text{nm})^3 = 8.32\times10^{10}$ bit/mm², and $250\times10^{12}$ bits = 31.25 TB. The paper rounds. Labelling our numbers as "derived" without saying so was the error. | The card shows the paper's numbers, and the repair note gives the source of the difference. Simulation output is labelled as not a biological measurement. | Yes. |
| 10 | Paper vs rendering | Unsure | conclusion | Yes. "Argues the reverse of her post" overreached: the paper assumes an outside world but does not establish one. | Became "does not support her post". Picture 3 now separates model → brain → universe. | Narrowed. |
| 11 | Replies | Unsure | conclusion | Yes. Also the owner's own note on the board: post 1 "starts too early". | Cut to two replies, both under 500 characters. Neither says the paper "measures" anything. | — |

## The discipline added to every card

- **(a)** This observer cannot tell the two states apart with what it has.
- **(b)** No possible observation can tell them apart.
- **(c)** The two states are physically the same.

(a) does not give (b). (b) does not give (c). Failing to show (c) does not show the states differ. Picture 2 on the board demonstrates the first gap: moving the viewport, or adding an object count, separates worlds that one channel reports identically.

## What changed in how the board works

- A **Wrong** mark now asks for the objection type, which is stored with the mark.
- Each card declares which cards it rests on. A wrong mark upstream shows "Needs reassessment" on every card downstream. An unsure mark shows "Check again".
- Repaired cards show what they used to say and why they changed.

## Knock-on repairs in the ledger

[claims_ledger.md](../03_critique/claims_ledger.md) made the same jumps, and those are repaired too:

- §1b had "no observer, conscious or not, can tell the two worlds apart". That is (a) → (b).
- §1b had "every finite observer has an offscreen". The condition was missing.
- The offscreen row said the game analogy is "against B".
- §3 said the paper's outside world counts "against B4".
- The capacity row did not say the paper rounds.
