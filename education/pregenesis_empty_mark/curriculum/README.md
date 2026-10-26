# Curriculum & Learning Plan: 000 Pre-Genesis

**AuthorityEffect:** None.  
**Prerequisites:** None.  
**Next Strand:** [`genesis_primitives`](../../genesis_primitives/README.md).

---

## 1. Strand Overview & Learning Goals

This strand examines an empirical and foundational question: **What does a modern language model do when presented with a minimal, uncarved mark (`<>`) under no declared rules or external containers?**

Before the Genesis engine admitted its first mark, empirical trials were conducted across three recorded runs:
- **Trial 1:** Prompted inside Markdown code fences.
- **Trial 2:** Prompted raw without code fences.
- **Full Replay:** Step-by-step history replay testing attribution and memory stability.

### Core Learning Objectives
By completing this curriculum and learning plan, you will be able to:
1. Explain the foundational discipline: **"Constrain epistemology, not mathematics"**—refusing to smuggle set theory, string monoids, clocks, or memory containers into an empty regime.
2. Distinguish the four primordial mathematical states: absent input (`None`), the empty word ($\varepsilon$), the literal wire token (`<>`), and the admitted base carrier ($V_0 = \varnothing$).
3. Identify how presentation formatting (such as code fences) acts as a confounding variable in prompt evaluation.
4. Prove the separation and history-view results from explicit hypotheses; use the transcripts to examine where those hypotheses apply.
5. Execute the automated grammar checker [`check_pre_genesis.py`](../code/check_pre_genesis.py) to verify inscription validity.

---

## 2. Four-Phase Learning Progression & Study Schedule

Total study time is approximately four hours (including the ~35-minute video).

```text
Phase 1: Question & Design ──> Phase 2: Empirical Trials ──> Phase 3: Formal Results ──> Phase 4: Failure Modes & Code
(Epistemic Refusal)             (Fences & Transcripts)        (Separation & Replay)       (Audit Lessons & Checker)
```

| Phase / Hour | Focus | Core Readings | Key Practical Task |
| :--- | :--- | :--- | :--- |
| **Phase 1 (Hour 1)** | Foundations & Design | [`../01_experiment_design.md`](../01_experiment_design.md), [`../sources/design_derivation_v0.md`](../sources/design_derivation_v0.md) | Outline the four branches of model response (Lessons 1 & 2). |
| **Phase 2 (Hour 2)** | Transcripts & Controls | [`../02_trial_record.md`](../02_trial_record.md), [`atlas/papers/finite_obstruction_calculus/genesis/docs/sources/pre_genesis/sources/trial_1_transcript.txt`](/atlas/papers/finite_obstruction_calculus/genesis/docs/sources/pre_genesis/sources/trial_1_transcript.txt), [`atlas/papers/finite_obstruction_calculus/genesis/docs/sources/pre_genesis/sources/trial_2_transcript.txt`](/atlas/papers/finite_obstruction_calculus/genesis/docs/sources/pre_genesis/sources/trial_2_transcript.txt) | Compare Prompt 11 replies across all 3 trials; identify the code-fence confound (Lessons 3 & 4). |
| **Phase 3 (Hour 3)** | Proofs & Arguments | [`../03_results_and_arguments.md`](../03_results_and_arguments.md), [`../sources/analysis_derivation_v1.md`](../sources/analysis_derivation_v1.md) | Work through forced separation, quiescence, and replay necessity proofs (Lessons 5, 6 & 7). |
| **Phase 4 (Hour 4)** | Failure Modes & Code | [`../04_named_failure_modes.md`](../04_named_failure_modes.md), [`../05_method_lessons.md`](../05_method_lessons.md), [`../code/`](../code/) | Run `check_pre_genesis.py` and analyze admission before distinction (Lesson 8). |

---

## 3. The Eight Guided Lessons

Read the primary sources, not only the chapters: the point of this strand is learning to check a claim against its empirical record.

### Lesson 1. The question and the design

**After this lesson you can** state the research question, explain "constrain epistemology, not mathematics", and say why "no move" is a success.

**Read:**
- [`../01_experiment_design.md`](../01_experiment_design.md)
- [`../sources/design_derivation_v0.md`](../sources/design_derivation_v0.md) lines 1 to 20, 173 to 207, 393 to 426.

**Exercises & Answers:**
1. Name three things the model was deliberately not told.  
   *Answer:* any three of: that `<>` means Primitive Difference; that an obstruction should be removed; that structure should be added; that a lift, quotient, tower, DDC trace, Prime algorithm, graph, cochain or homology should appear; that `<a>` is the intended next state; that two kinds of moves are expected (v0 lines 7 to 16).
2. Why does the design count "no continuation is forced" as a success?  
   *Answer:* because with no declared rules nothing is forced; a model that says so is reporting the regime correctly. A supplied `<a>` is then marked as a caller intervention, not a model derivation (branch D).
3. What metadata did the design ask for that the record lacks, and why does it matter?  
   *Answer:* model identifier, settings, date, tool access (v0 line 414). Without them the runs cannot be reproduced or attributed to a model version.

---

### Lesson 2. Bare controls and the code-fence confound

**After this lesson you can** describe how the model read bare marks and why Trial 1 and Trial 2 differ.

**Read:**
- [`../02_trial_record.md`](../02_trial_record.md) "Prompts 1 to 10"
- [`atlas/papers/finite_obstruction_calculus/genesis/docs/sources/pre_genesis/sources/trial_1_transcript.txt`](/atlas/papers/finite_obstruction_calculus/genesis/docs/sources/pre_genesis/sources/trial_1_transcript.txt) lines 1 to 210
- [`atlas/papers/finite_obstruction_calculus/genesis/docs/sources/pre_genesis/sources/trial_2_transcript.txt`](/atlas/papers/finite_obstruction_calculus/genesis/docs/sources/pre_genesis/sources/trial_2_transcript.txt) lines 1 to 185

**Exercises & Answers:**
1. Quote the first sentence of each run's reply to `<>`.  
   *Answer:* Trial 1: "It looks like you've sent the symbol <> inside a code block." Trial 2: "It looks like your message came through as just <>."
2. Why can't the two runs be compared directly?  
   *Answer:* Trial 1 sent the controls inside code fences and Trial 2 sent them raw; the fence is a second variable.
3. A slide says "the model hallucinated in 96% of trials". What do you check?  
   *Answer:* the record has three runs and no rates; the claim has no source.

---

### Lesson 3. The fenced prompt and quiescence

**After this lesson you can** explain no-transition quiescence, compare proposed continuation rules, and say why repetition is not free.

**Read:**
- [`../02_trial_record.md`](../02_trial_record.md) "Prompt 11"
- [`../03_results_and_arguments.md`](../03_results_and_arguments.md) results 1, 3, 4

**Exercises & Answers:**
1. List the three replies to Prompt 11.  
   *Answer:* "None." (Trial 1); "Next inscription: <>" assuming a repetition rule (Trial 2); "`<> <>`" (replay).
2. Is quiescence an experimental finding?  
   *Answer:* no. An empty transition relation has no successors by definition; the trials show the model reporting that.
3. What must a regime have before "`<>` again" differs from "`<>` still"?  
   *Answer:* two positions or stages, an identity criterion across them, a copy or persistence rule, and a stable alphabet.

---

### Lesson 4. Presentation versus internal capacity

**After this lesson you can** state the two conventions for `<a>` and show that the question is undecidable without one.

**Read:**
- [`../02_trial_record.md`](../02_trial_record.md) "Prompt 12"
- [`../03_results_and_arguments.md`](../03_results_and_arguments.md) result 2
- [`../sources/analysis_derivation_v1.md`](../sources/analysis_derivation_v1.md) lines 93 to 135 and 731 to 737

**Exercises & Answers:**
1. Under the opaque convention, is `<a>` a new state after `<>`?  
   *Answer:* no; with no observations nothing distinguishes them.
2. Under the exact-inscription convention?  
   *Answer:* yes; the inscriptions differ.
3. Which run used which?  
   *Answer:* Trials 1 and 2 used the opaque convention ("a new costume for the old emptiness"); the replay used the exact convention ("a new state").

---

### Lesson 5. The collision and forced separation

**After this lesson you can** define regime-relative equivalence, prove that a successful answer must preserve a distinction lost by the current representation, and show that the new observation is not unique.

**Read:**
- [`../03_results_and_arguments.md`](../03_results_and_arguments.md) result 5
- [`../sources/analysis_derivation_v1.md`](../sources/analysis_derivation_v1.md) lines 140 to 303

**Exercises & Answers:**
1. With $O$ empty, is `<>` $\approx$ `<abc>`?  
   *Answer:* yes, vacuously.
2. Prove: if $f$ is defined on the classes of $\approx$, then $f$ cannot separate `<a>` and `<ab>`.  
   *Answer:* they are in one class $c$, so both values are $f(c)$.
3. Give two predicates that separate `<a>` from `<ab>` but disagree on `<aa>`.  
   *Answer:* "contains b" gives `<aa>` the value of `<a>`; "more than one position" gives it the value of `<ab>`.
4. Trial 1 said the regime "identifies them". What is wrong?  
   *Answer:* with no identity rule the regime neither identifies nor distinguishes them; vacuous equivalence is not a declared identification.

---

### Lesson 6. Auditing the auditor

**After this lesson you can** separate licensed metalanguage from imports and explain why a one-turn audit passed a stale reply.

**Read:**
- [`../02_trial_record.md`](../02_trial_record.md) "Prompt 13" and "Prompt 16"
- [`atlas/papers/finite_obstruction_calculus/genesis/docs/sources/pre_genesis/sources/trial_2_transcript.txt`](/atlas/papers/finite_obstruction_calculus/genesis/docs/sources/pre_genesis/sources/trial_2_transcript.txt) lines 571 to 693

**Exercises & Answers:**
1. Why was flagging "We" wrong?  
   *Answer:* the prompt licensed ordinary metalanguage; "We" says nothing about the regime's internal capacities.
2. The two-level auditor answered "None." on Result 15. Was it wrong given what it saw?  
   *Answer:* no; nothing in the single turn attributes undeclared structure to LEVEL S. The error was in the history.

---

### Lesson 7. Provenance and replay

**After this lesson you can** prove the history-view obstruction and check whether the Trial 2 and replay inputs satisfy its premises.

**Read:**
- [`../03_results_and_arguments.md`](../03_results_and_arguments.md) results 6 and 7
- [`atlas/papers/finite_obstruction_calculus/genesis/docs/sources/pre_genesis/sources/trial_2_transcript.txt`](/atlas/papers/finite_obstruction_calculus/genesis/docs/sources/pre_genesis/sources/trial_2_transcript.txt) lines 890 to 1033
- [`atlas/papers/finite_obstruction_calculus/genesis/docs/sources/pre_genesis/sources/full_replay_transcript.txt`](/atlas/papers/finite_obstruction_calculus/genesis/docs/sources/pre_genesis/sources/full_replay_transcript.txt) lines 1 to 30 and 252 to 316

**Exercises & Answers:**
1. State and prove replay necessity.  
   *Answer:* see chapter 03, result 6.
2. Construct a two-history example with equal reports and different protected answers. Does the Prompt 17 comparison establish these premises?
   *Answer:* take $H=\{h_1,h_2\}$, a constant report $\pi$, and $\sigma(h_1)=0$, $\sigma(h_2)=1$. No decoder of $\pi$ recovers both answers. The trials received different contexts, so repeating the same question does not establish equality of the complete auditor inputs.
3. How did the two runs handle Prompt 14's false attribution?  
   *Answer:* Trial 2 answered status 4 without objecting; the replay said "I did not make that claim".

---

### Lesson 8. Admission before distinction, and where this leads

**After this lesson you can** explain why `<ab>` must be admitted before it can be distinguished, why admission alone distinguishes nothing, and how PFP inherits these lessons.

**Read:**
- [`../02_trial_record.md`](../02_trial_record.md) "Prompts 18 and 19"
- [`../04_named_failure_modes.md`](../04_named_failure_modes.md)
- [`../05_method_lessons.md`](../05_method_lessons.md)

**Exercises & Answers:**
1. Why were none of the four extensions one-step?  
   *Answer:* each needed several undeclared capabilities (branching, matching, rewriting).
2. What were the two equally minimal first additions?  
   *Answer:* supply `<ab>` as data, or write `<ab>` into a rule pattern.
3. After `<ab>` is admitted with no rules, are `<a>` and `<ab>` distinguishable?  
   *Answer:* no; nothing in the regime reacts to them differently.
4. Order the spine.  
   *Answer:* mention, supply, designation, admission, retention, internal operation.
5. Name the PFP rule that answers stale certification and false provenance.  
   *Answer:* a candidate never certifies itself; only the host's receipt, computed from the kept history, carries an authoritative status.

---

## 4. Verification Check

To verify inscription validity and conformance against the formal EBNF grammar:

```powershell
py -3.12 education/pregenesis_empty_mark/code/check_pre_genesis.py
```

Then rewrite one claim from an old version of this strand (for example the "Prompt 14 ... Yes, that is correct" quote in git history before 2026-10-06) and find the line in `../sources/` that refutes it.

---

## 5. Next Step in the Curriculum

Once you have completed this curriculum and validated the local checker:
$$\text{000 Pre-Genesis} \quad\longrightarrow\quad \textbf{001 Genesis}$$
Proceed to [`education/genesis_primitives/README.md`](../../genesis_primitives/README.md) to study the sealed 19L57G1 derivation engine and the Two Boxed Laws.
