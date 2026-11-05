# Self-audit: the replies, the board, the adversary record and the Lean file

Date: 2026-11-05. This file covers what [self_review.md](self_review.md) does not: the final reply set, the board cards and their equations, [adversary_of_chatgpt.md](../03_critique/adversary_of_chatgpt.md), [lean4/ThreadsReply.lean](../lean4/ThreadsReply.lean), and the lines in [claims_ledger.md](../03_critique/claims_ledger.md) and [analysis.md](../03_critique/analysis.md). For [adversarial_review.md](../03_critique/adversarial_review.md) and its checks, see `self_review.md` §A.

Each entry runs the same steps: **claim → break → repair → retest → status**.

A claim survives only when it rests on something checkable. That means a quote from the paper ([ijms-25-02399.md](../02_paper/ijms-25-02399.md), by section), a recomputation (check ids S1–S5 in [code/self_audit_checks.py](../code/self_audit_checks.py)), or a Lean proof. Agreement between Claude passes, or between Claude and ChatGPT, is not on that list. Where two passes disagree, both readings are kept below.

Status words:
- **KEPT**: it survived the attack.
- **REPAIRED**: it was wrong as written, and the text is now changed.
- **WITHDRAWN**: it is dropped.
- **OPEN**: it is not settled here.

Repairs are applied to the files still in use: `replies.md`, the board, the ledger and the analysis. Records of earlier rounds, such as `adversary_of_chatgpt.md`, `adversarial_review.md` and `board_repair_log.md`, are left as written so the trail stays readable. Each gets a pointer here instead.

---

## A. Replies, every version

The first version is in commit a76b21f, the second in 1fdd076 and the third in 9a21f26. The rhymed drafts were in the thread. The final set is in `replies.md`.

| # | As written | Break | Repair | Status |
|---|---|---|---|---|
| A1 | "A falling tree produces pressure waves whether anyone hears them or not, according to ordinary physics." | It opens by supplying air, waves and a fall, which are the very imports the argument is about. It starts too early. | Opens on the two records instead (A9). | WITHDRAWN |
| A2 | "quantum measurement doesn't require consciousness. A detector can record which-path information without anyone looking." | It depends on interpretation: von Neumann–Wigner readings give consciousness a role. As written, it is a claim about all of quantum mechanics. | Dropped. The final set asks what "looking" is instead of asserting what measurement needs (post 4: "a detector, a record, or a feeling in the chest?"). | WITHDRAWN |
| A3 | "Without one, it's a metaphor, not an explanation." | A claim can explain without a new test. What it cannot do without one is be checked. | "Until then it's a gorgeous story, not yet a test." | REPAIRED |
| A4 | "Its carriers are water and light, and it measures bits and field density." | The paper measures nothing. It estimates capacity (eq. 4) and simulates density (Figs. 5–6). | "estimates capacity and simulates field density" (v2). The final set says "one simulation shown". | REPAIRED |
| A5 | "It never says the universe doesn't render offscreen." | Retest: "render" occurs 0 times in the paper. | Kept as "Not one line about rendering the universe." The only "universe" is a reference title (Hameroff and Penrose). | KEPT |
| A6 | "the observer, is the one part nobody supplied." | "Nobody" covers every reader of the thread. The paper also flags the gap itself: "yet another mystery altogether". | "Your source ... honestly left the observer open." | REPAIRED |
| A7 | v1 post 4: "A hologram can't be read without a reference beam. In your version, who supplies it?" | Reading a hologram needs a reconstruction wave, which need not be the original beam (white-light reflection holograms). | v2: "Appendix B proposes a reference wave and reconstruction. What evidence connects...". It was later dropped as too categorical (`board_repair_log.md`). | WITHDRAWN |
| A8 | v3 post 1: "do you mean it stops existing, stops evolving, or simply isn't experienced? Those are three different claims." | **The two passes disagree.** This audit and `adversary_of_chatgpt.md` round 1 say option 3 is a free exit. `self_review.md` C1 says taking it is itself a result: the claim shrinks to ordinary limited observation. Both are right about different things. The exit costs her nothing in the thread unless the post says that it shrinks the claim. | The game post names option 3 as ordinary ("Number 3 is just Tuesday"). Taking it is then visibly the shrinkage `self_review.md` describes. | REPAIRED |
| A9 | Tree: "Something happening in between? That's a story, not a view." | It calls an inference a "story". Inferring a history from two records is legitimate. The point is only that the history is inferred. | "Inferred, not in view." | REPAIRED |
| A10 | Tree: "I'm saying none of it was witnessed." | Overreach. The two poses are witnessed. The fall, identity and order are not. | "Saying it came in on the side." | REPAIRED |
| A11 | Tree: "who checked? Who decided?" | The past tense asks about one act. The question is about the standing rule. | "who checks? Who decides?" | REPAIRED |
| A12 | Tree: "And what record would show it, if we pulled the curtain wide?" | A curtain is a screen with a world behind it. That is the picture we said "offscreen" smuggles in. | "And what record would show it, and what test would it provide?" | REPAIRED |
| A13 | Tree: "two trees standing" | It calls the lines trees, which supplies something. | Kept for the reply: a post may name the picture. The board keeps bare lines and pose labels (B1). | KEPT |
| A14 | Game: "skip the drawing, sometimes skip the physics, fake it when you turn around." | "Fake" implies deception. Games rebuild state from storage or from the seed. | "...the rest get generated from the seed when you arrive." | REPAIRED |
| A15 | Game: "Minecraft stops ticking far-off chunks, but the save file still knows where the diamonds are." | **Fact error.** Unvisited chunks are never generated or saved. The seed fixes them, and they are generated on arrival. `self_review.md` C7 found the same error independently; that is noted, not counted as proof. | "same diamonds every time". This holds for the same seed and game version; ore placement changed between versions. | REPAIRED |
| A16 | Game: "(1) nothing's there, (2) nothing moves, (3) nobody kept a receipt", and "which does the universe skip?" | "Which" reads as "pick one", but the readings are not exclusive: a game can skip several chores at once. They are also not ordered. A paused, saved Minecraft chunk has (2) without (3): nothing moves, yet its state is kept. | Kept. She may name one reading or several. The post claims no order among them, and "Number 3 is just Tuesday" says only that (3) is ordinary. An earlier version of this entry claimed (2) implies (3) and ranked the readings strongest to weakest; both are withdrawn (R5). | KEPT (reading stated) |
| A17 | "Number 3 is true of every observer." | This needs more states than reports, which is not given. Lean `small_domain_all_reported` is a counterexample. | "Number 3 is just Tuesday." This makes no universal claim. | REPAIRED |
| A18 | "If none, they cannot be told apart from 3." | It jumps from "no test proposed" to "no test exists". "Nothing changes" could show up when looking resumes. | "For 1 or 2: what comes out different when you peek?" | REPAIRED |
| A19 | Paper: "But it assumes 'the outside world of the observable phenomena,' the very thing you say isn't rendered" | **Fact error.** §6: "Vision is perhaps the most important link between the outside world of the observable phenomena and the inner life of our mind." Observable phenomena are the part that *is* seen. | "It calls vision ... the link between 'the outside world of the observable phenomena' and the mind: world first, brain images it." | REPAIRED |
| A20 | Paper: "It calls vision the link between ..." (the A19 repair) | It drops the paper's hedge, "perhaps the most important". | "It calls vision perhaps the most important link between ..." | REPAIRED |
| A21 | Paper: "It just forgot to bring the observer." | "Forgot" says oversight, but the paper flags the gap itself. | "Your source brought the world and honestly left the observer open." | REPAIRED |
| A22 | Paper: "one simulation run" | The paper shows one configuration (N = 4, Figs. 4–6). It may have run others (`self_review.md` C6). | "one simulation shown" | REPAIRED |
| A23 | Paper: "world first, brain images it" | The paper frames this as a question ("where is the image of the outside world formed inside the brain?") and weighs Sheldrake against Pribram. | Kept. The order (world, then its image) is the paper's framing, whichever answer it prefers. | KEPT |
| A24 | Paper (rhymed): "A memory trick inside a skull, even if it works, tells us nothing about the moon nobody's watching." | "Nothing" is a universal negative. | Not in the final set. `replies_alternates.md` has "doesn't reach". | REPAIRED |
| A25 | Opener (rhymed): "Berkeley said God keeps watching the quad." | **Attribution.** The quad is from the limerick usually credited to Ronald Knox, not from Berkeley. | Not in the final set. The alternates credit Knox. | REPAIRED |
| A26 | "Dr. Johnson kicked a stone to refute Berkeley." | Retest: Boswell, *Life of Johnson*, 6 August 1763: "I refute it thus." | — | KEPT |
| A27 | "Einstein asked Pais whether the moon is there only when someone looks." | Pais, *Rev. Mod. Phys.* 51 (1979) 863: Einstein asked "whether I really believed that the moon exists only when I look at it." Here "someone" stands in for Pais. That is the usual paraphrase. | — | KEPT |
| A28 | Thales (in the thread): "Everything we know about him comes through Aristotle and later writers." | Herodotus writes about Thales before Aristotle (*Histories* 1.74–75, 1.170). | "only what Herodotus, Aristotle and later writers kept." | REPAIRED |

Retest: S5 checks the lengths in `replies.md` (434, 429, 489, 438 and 168 characters).

---

## B. Board cards and equations

These are applied to the live board and saved as [markup_board.html](../05_boards/markup_board.html).

| # | Card: as written | Break | Repair | Status |
|---|---|---|---|---|
| B1 | Tree: $R_1=\{L_1,L_2\}\neq R_2=\{L_1',L_2'\}$ | As label sets, these differ only because the labels differ. They would differ for identical pictures. The witnessed difference is in the poses. | $R_1=(\text{up},\text{up})\neq R_2=(\text{up},\text{flat})$. Supplied: which line is which ($L_2'\equiv L_2$), a between, and the reading of up and flat. Lean: `records_do_not_fix_identity`. | REPAIRED |
| B2 | Tree stepper: "The records carry no clock." | Too general: photos carry timestamps, and trees have rings. | "These two records carry no clock." This repair is the same as `self_review.md` B4. | REPAIRED |
| B3 | Rendering: $q_1(A)=q_1(B)\Rightarrow E(q_1(A))=E(q_1(B))$ | Retest: true for any $E$ that reads only the report. Lean: `same_report_same_verdict`. | — | KEPT |
| B4 | Rendering: $q_1(A)=q_1(B)\not\Rightarrow q_2(A)=q_2(B)$ | Retest: Lean `one_channel_not_every_channel`. | — | KEPT |
| B5 | Earlier rendering card: Bayes factor 1 from equal reports | Equal reports are not equal likelihoods. Lean `same_report_not_same_likelihood` gives normalized weights 9/10 and 5/10, so the Bayes factor is 1.8 (S4a). | The Bayes factor is 1 under equal weights on every report, if the reports are sampled independently and the shared likelihood is nonzero: Lean `same_weights_same_likelihood` (S4b). Without independence, equal single-report weights can still give a Bayes factor of 2: Lean `same_marginals_not_same_joint` (S4c, R2). This was removed from the board in an earlier round. | REPAIRED |
| B6 | Ladder: "owed first: (carrier, gauge, evaluator)" | The evaluator acts at step 5, so what is owed before step 1 is its declaration. | "declared first: (carrier, gauge, evaluator)" | REPAIRED |
| B7 | Observer: $\mathcal O=(\mathsf{Pres},\mathsf{Mem},\mathsf{Eval},\mathsf{Policy})$ | Four layers is the WDP text (Ch. 10). The Lean `ObserverPacket` has three: presentation, memory and evaluator, with no policy. $\mathsf{Accept}\not\Rightarrow\mathsf{Authorized}$ is a Lean theorem (`acceptance_does_not_entail_authority`). | The card now says so. | REPAIRED (disclosed) |
| B8 | Paper chain, stage 2: "not tested" | The paper cites infrared work on coherence in water (ref. 73). That is evidence about water, not memory, but "not tested" can read as "nothing cited". | "not tested here" | REPAIRED |
| B9 | Paper chain: "paper, on 3: 'the outside world of the observable phenomena'" | Same fact error as A19. The quote is about the observed world, not stage 3. | "paper, on the world: ..." | REPAIRED |
| B10 | Paper chain: "one year at 310 K needs about 1.2 eV" | This assumes a record held by one barrier, and the attempt time $\tau_0$ is supplied: $\Delta E = k_BT\ln(1\,\text{yr}/\tau_0)$. With $\tau_0 = 1$ ps that gives 1.199 eV. With $\tau_0 = 1$ s it gives 0.461 eV (S3e, S3e2). A collective order parameter can also have an extensive barrier (`self_review.md` A9). | "a record held by one barrier, with a supplied attempt time of 1 ps, needs about 1.2 eV; with 1 s it would need 0.46 eV". The first repair left out $\tau_0$ (R4). | REPAIRED |
| B11 | Paper chain: "Gauss's law ... broken exactly through the added M², γ and v terms" | The algebra is exact. The size along the run is numerical, from `retest_checks.py` (1.1–2.3 times the charge change, with stencil error about 1e-7). | The note now says which part is exact and which is numerical. | REPAIRED |
| B12 | Paper inputs: $E_3=\frac{g\Omega^2N}{4\pi}\mathrm{sech}\frac{x^0-\tau_0}{\tau_R}$, with $\tau_R=\frac{2\pi}{g^2\Omega N}$ | Retest from (A36)–(A46): the energy law, the $Z^2+R^2$ law, (A44) solving (A43), and the sech form all check (S1a–d). | — | KEPT |
| B13 | Paper inputs: "loss term 𝒜/L₃ (added by hand)" | The term comes with a one-line reason before (A42): "Setting the length $L_3$ for release of radiation". | "loss term 𝒜/L₃ (added for release of radiation)" | REPAIRED |
| B14 | Paper inputs: "every tissue layer = same field" | §4 uses one set of equations and one set of parameters for all four layers. "Same field" says more than that. | "same equations, same parameters, every layer" | REPAIRED |
| B15 | Paper inputs: "object wave o: no source" | "No source" could mean "no physical origin". What (A51) lacks is an equation for $o$. | "object wave o: given, no equation" | REPAIRED |
| B16 | Paper inputs: "2.5 PB, 30 TB" | Retest: these are the paper's own figures. Unrounded, they are 2.6 PB and 31.25 TB (S3f–h). | — | KEPT |
| B17 | Draft-replies card | It held the v3 posts that A8 and A19 broke. | It now holds the four repaired posts. | REPAIRED |

---

## C. Adversary record and analysis files

| # | As written | Break | Repair | Status |
|---|---|---|---|---|
| C1 | `adversary_of_chatgpt.md`: with $A^0=0$ and $\nabla\cdot\mathbf A=0$, $\partial^\nu F_{\nu0}=-\partial_0(\nabla\cdot\mathbf A)=0$; with (A7), $0=-e\lvert\varphi\rvert^2$ | Retest: S2a (sympy). Sign convention: $\partial^iA_i=\nabla\cdot\mathbf A$ in $(+,-,-,-)$. | — | KEPT |
| C2 | Same file: "A static density kills super-radiance" | Round 2 already narrowed this to the modelled emitter. Retest of that step: a frozen $\lvert\varphi\rvert^2$ forces the cross term $2\,\mathrm{Re}(b_0^*b_1\varphi_0^*\varphi_1)$ to vanish, and that term oscillates at $\Omega$. So $R=0$, and the source in (A38) is gone. This holds wherever $\varphi_0^*\varphi_1\neq0$, which (A16)–(A17) need anyway. `self_review.md` A1 goes further: the slow population term breaks it too. | The condition is stated. | KEPT |
| C3 | Same file: "≈ 4×10⁹ molecules per cubic wavelength, so the dropped term is not small" | A count is not an interaction strength (ChatGPT, round 2). | The count stays as a number (S3a: 4.18e9). The size claim is dropped. This was done in round 2. | WITHDRAWN |
| C4 | Same file: $e^{-2.4\text{ eV}/26.7\text{ meV}}\approx e^{-90}$, "so thermal photons will not write at that frequency" | The number holds: 89.8 with the paper's 2.4 eV, and 92.8 with the correct 2.48 eV (S3c–d). The relevance is narrower. In tissue, the noise that matters is absorption and chemistry, not thermal photons (`self_review.md` A7). | Both numbers are stated. "No thermal photons compete" is kept; "the write is clean" does not follow. | REPAIRED |
| C5 | Same file, "Not attacked here: Landauer ... correct" | `self_review.md` A8 objects that recording over a medium in use must erase. That is true only under conditions. Landauer's bound is $k_BT\ln2$ per bit of information that is logically discarded into a bath at temperature $T$. Overwriting a cell costs at least that only when its prior content is unknown, carries a full bit of entropy, and is not correlated with anything kept. If the content is known, or an identical copy is retained, the overwrite can be done reversibly, with no minimum (Bennett's reversible erasure with a retained copy). The paper says neither what is erased nor under which assumptions. The first version of this entry said "overwriting an occupied medium does cost at least $k_BT\ln2$ per bit". Occupancy alone does not establish that (R3). | Pointer added to the file, with the conditions. What survives either way: Landauer says nothing about retention. | REPAIRED |
| C6 | Same file: "4.7 bits per synapse gives about 147 TB" | Retest S3i: 146.9 TB. | — | KEPT |
| C7 | `claims_ledger.md`: "Correction to `analysis.md`: its six slots put authority inside the observer." | **The correction is itself wrong.** `analysis.md` lists Authority and Observer as separate rows. It never puts authority inside the observer. | The line now says the six slots are consistent with authority outside the observer, then gives the same mapping. | REPAIRED |
| C8 | Ledger: "This assumes a world that exists offscreen." | Same fact error as A19. | "This assumes a world outside the brain that vision links to the mind. It says nothing about the unobserved part of that world." | REPAIRED |
| C9 | Ledger: "Section 4 says the input maximum is 'approximately 3', then computes the factor as 3.9." | The sentence reads "approximately 3 due to the factor ... = 3.9". The factor is a prefactor, not the computed maximum. | Reworded. The prefactor is 3.906 (S3j). The realized maximum is not printed. The rerun's recursion gives 2.13 (`self_review.md` A6, open). | REPAIRED |
| C10 | `analysis.md` scope: "Remaining reading scope: Conclusions, Appendices A and C, references." | Out of date. The whole paper has since been converted and read. | Scope line updated. | REPAIRED |

---

## D. Lean (`lean4/ThreadsReply.lean`)

| # | As written | Break | Repair | Status |
|---|---|---|---|---|
| D1 | `records_do_not_fix_identity` proved a list of side facts: swap is injective, a value of R2, and 1 ≠ 0. | It never stated the claim, which is that two matchings give two different histories. | It now defines `fallenUnder σ`, the line that lies flat after matching, and proves there are injective σ and τ with `fallenUnder σ ≠ fallenUnder τ`. | REPAIRED |
| D2 | `same_report_not_same_likelihood` with weights 9, 1 and 5, 5 | Without normalization, rescaling can hide or create the difference. | It adds that both totals are 10. | REPAIRED |
| D3 | `same_weights_same_likelihood` was proved as `h d` | A tautology: it restated its hypothesis. The first repair used a product of weights as "the likelihood", which holds only for independent reports (R2). | `iidLikelihood` is now named and documented as the independent-sampling likelihood. The theorem proves equality and a nonzero denominator (`iidLikelihood_pos`). `same_marginals_not_same_joint` shows the product rule failing without independence. | REPAIRED |
| D4 | `small_domain_all_reported` used `id : Fin n → Fin n` | That covers only equal sizes. | Any `n ≤ m`, via `Fin.castLE`. | REPAIRED |
| D5 | `pigeonhole`, `same_report_same_verdict`, `one_channel_not_every_channel` | Retest: they compile. | — | KEPT |

Check: `lean lean4/ThreadsReply.lean` exits 0 on Lean 4.35.0, core only, with no Mathlib. Axioms used:

```
records_do_not_fix_identity      [propext]
same_report_same_verdict         none
one_channel_not_every_channel    none
same_report_not_same_likelihood  none
iidLikelihood_pos                [propext]
same_weights_same_likelihood     [propext, Quot.sound]
same_marginals_not_same_joint    none
pigeonhole                       [propext, Classical.choice, Quot.sound]
small_domain_all_reported        none
```

---

## F. Review round: Jeremy on commit 1eea606 (2026-11-05)

Five findings, all accepted. Each one broke a repair made earlier in this file.

| # | Finding | Break, reproduced | Repair | Status |
|---|---|---|---|---|
| R1 | The checker reports failure but exits 0, and a missing `replies.md` skips S5 and prints ALL PASS. | Reproduced: a 501-character reply printed FAIL with exit 0. | The checker now exits 1 on any failure. The replies file is required (`--replies PATH`), and the number of reply blocks must match (`--expect-blocks`, default 5). Regression tests in `code/test_self_audit_checks.py` cover the 501-character reply, the missing file and the passing case. | REPAIRED |
| R2 | The Bayes reading of `same_weights_same_likelihood` needs independence, and a Bayes factor needs a nonzero denominator. | Counterexample: two independent fair bits against one fair bit read twice. The single-report weights are the same, but P(TT) is 1/4 against 1/2, a Bayes factor of 2. | `iidLikelihood` is named and documented as the independent-sampling likelihood. The theorem adds a nonzero denominator (`iidLikelihood_pos`). The counterexample is proved as `same_marginals_not_same_joint` and checked as S4c. Entries B5 and D3 are updated. | REPAIRED |
| R3 | The Landauer repair in C5 was too categorical. | Occupancy alone does not show that a bit is discarded. Known or correlated content allows a reversible overwrite (Bennett, with a retained copy). | C5 now states the conditions: unknown prior content, a full bit of entropy, no correlation with anything kept, and a bath at $T$. It also says the paper specifies none of them. | REPAIRED |
| R4 | The board kept "one barrier" but dropped the 1 ps attempt time. | $\Delta E = k_BT\ln(1\,\text{yr}/\tau_0)$, and one barrier does not fix $\tau_0$. With $\tau_0 = 1$ s the barrier is 0.461 eV, not 1.199 eV. | The board note now gives the formula, says $\tau_0$ is supplied, and gives both values. S3e2 checks 0.461 eV, and S6 fails if any board sentence with 1.2 eV omits 1 ps. B10 is updated. | REPAIRED |
| R5 | A16 claimed "nothing moves" implies "nobody kept a receipt", and ranked the readings. | A paused, saved Minecraft chunk is a counterexample: nothing moves, and its state is kept. | The implication and the ranking are withdrawn. The readings are neither exclusive nor ordered. | REPAIRED |

The review compiled nothing in Lean. Here, `lean lean4/ThreadsReply.lean` exits 0 on Lean 4.35.0 after these changes, with the axioms listed in §D.

---

## G. Learning boards (`05_boards/learning_boards.html`, 2026-11-05)

Jeremy asked for about five boards in plain logic, with no poetry, that answer the post and the paper and teach a reusable move. Six boards and a method page were drafted, then attacked line by line before the first publish. G15 came after the assumptions audit merged. Each board's backing is listed in `05_boards/learning_boards_references.md`.

| # | Draft line | Break | Repair | Status |
|---|---|---|---|---|
| G1 | Board 1 result: "No part of the sentence points to a record yet." | The post linked a paper, and a paper is a record. | "No part of the sentence points to a record of rendering yet ... The paper it linked is checked on board 5." | REPAIRED |
| G2 | Board 2 step 4: "Each reading either predicts something you could see, or is built so that it predicts nothing." | Not a true either/or: a reading can predict a difference nobody can see in practice. | "...either predicts some record that would come out differently, or predicts the same records as a world that does every job." Now exhaustive. | REPAIRED |
| G3 | Board 2 step 5: "Not run predicts that things stop changing while nobody looks. They do not." | A universal negative tagged Witnessed. Records are finite. | "The records say otherwise", followed by the clock, the ice and the rock layers. | REPAIRED |
| G4 | Board 3 step 2: "Every channel in use reports A and B the same way. That is what 'nobody looks there' means." Tagged Derived. | This is our reading of her word, not a derivation. | Tagged Supplied: "Read 'nobody looks there' as ... This is our reading of the post's word." | REPAIRED |
| G5 | Board 3 step 5: "anything that reports with a limited set of reports has blind spots." | "Limited" is not "fewer than the states". A small domain can be fully reported (A17; Lean `small_domain_all_reported`). | "anything with fewer possible reports than the states it looks at has blind spots." | REPAIRED |
| G6 | Board 3 step 6: "the fringes go away, whether or not a person ever reads the record." | Fine on the reader, loose on the device: "a device" could read as one special device. | "When any device records which slit ... Whether a person ever reads the record makes no difference." | REPAIRED |
| G7 | Board 4 step 1: "Evidence is a ratio." | Stated as a definition. The Bayes factor is one measure of evidence. | "Measure evidence by a ratio". | REPAIRED |
| G8 | Board 4 result: "A story built to match every record can never be favoured by a record." | Favoured over what? A story can match every record and still be favoured over a story that fails one. | "A story built to match the ordinary account on every record can never be favored over it by a record". | REPAIRED |
| G9 | Board 6 capacity: "2.6 petabytes before rounding". | The paper's 2.5 comes from rounding 8.32e10 to 8e10 in the middle. "Before rounding" hides where. | "without its intermediate rounding". | REPAIRED |
| G10 | Board 6 retention: "20 meV, the least energy needed to erase one bit". | Too categorical, the same fault as review finding 3: the bound is on heat released, under conditions. And a reader can take the 2.4 eV photon as the barrier, since 2.4 eV is larger than 1.2 eV. | "the least heat released in erasing one bit ..., under conditions given on the back page ... and the photon's energy is not a barrier." The back page states the three conditions, Bennett's kept-copy case, and why the photon's energy does not enter. | REPAIRED |
| G11 | Board 6 back page: "Everything else cancels exactly." | True only for the $e^2\lvert\varphi\rvert^2/m$ form. The printed $e\lvert\varphi\rvert^2/m$ in (A76) and (A78) breaks Gauss's law by itself. | The back page now says which form, and calls the printed one a probable typo. | REPAIRED |
| G12 | All boards: sections marked `hidden` but styled `display:grid`. | First screenshot: all six boards and every back page showed at once, so the "one board at a time" and "back page" design did nothing. | `[hidden]{display:none!important}` added to the page's own CSS. | REPAIRED |
| G13 | Phone layout. | First screenshot at 390 px: the page scrolled sideways to 638 px. Grid children kept the pictures' 480 px minimum width. | `min-width:0` on the board's children. The pictures scroll inside their own frame. | REPAIRED |
| G14 | Spelling: "favour", "favours", "favoured". | The folder uses American spelling, for example "favoring" in the thread and "color" throughout. | Changed to "favor", "favors" and "favored". | REPAIRED |
| G15 | Board 6, written before the assumptions audit merged (#523). Capacity: "the inputs are supplied". Appendix A: "A version that keeps the scalar potential might avoid this. The paper does not give one." | Both lines undersell what is now derived. The audit's row Y1 shows that the 2.6 PB rests on the thickness: a surface hologram over the same area holds 0.5 TB. Rows D1 and E1 show the repair: the Coulomb gauge fixes only $\nabla\cdot\mathbf A = 0$, and with $A^0$ from Poisson's equation the pulse returns, at the price of a Coulomb term. | Board 6 and its back page now state both. The arithmetic is rechecked by S7b. | REPAIRED |

## E. Tally and what is still open

- **This file:** 80 entries: 62 repaired, 4 withdrawn, 14 kept. Section F holds the five review findings on 1eea606; each one broke an earlier repair here. Section G holds the fifteen repairs to the learning boards.
- **Fact errors found in Claude's own text:** the Minecraft save file (A15), the vision quote read as being about the unobserved world (A19, B9, C8), the misplaced correction about authority in `analysis.md` (C7), and the Knox limerick credited to Berkeley (A25).
- **Open:**
  - The input amplitude, about 3 against the rerun's 2.13 (`self_review.md` A6).
  - Whether any barrier protects the proposed record.
  - The size of the dropped near-field term in Appendix A.
  - Nobody has compared the Appendix C rerun with the authors' code.
- **Who reviewed this:** Claude reviewed Claude, with ChatGPT and a second Claude pass as adversaries. None of that is independent. Jeremy's review is the next gate, and so is Fable's full review of the paper.
