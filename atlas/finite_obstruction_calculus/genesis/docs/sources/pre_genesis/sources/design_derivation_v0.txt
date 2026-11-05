# Core principle

**Prompt 1 should constrain epistemology, not mathematics.**

The Pontryagin experiment over-specified the desired stages, statuses, claims, proof path, receipt type, and terminal result. DeepSeek’s visible reasoning consequently described the task as a simulation and considered generating a fake hash.  

For the sister paper, DeepSeek must not be told:

* that `<>` means Primitive Difference;
* that an obstruction should be removed;
* that structure should be added;
* that a lift, quotient, tower, DDC trace, Prime algorithm, graph, cochain, or homology should appear;
* that `<a>` is the intended next state;
* that two kinds of moves are expected.

Those are the **comparison targets**, not the instructions.

The prompt should make only one distinction explicit:

[
\text{what the external reader sees}
\quad\neq\quad
\text{what the current symbolic regime can express}.
]

That distinction is necessary because otherwise DeepSeek will simply use ordinary string semantics—length, order, character identity—and later declare `<a>` and `<ab>` different without noticing that it imported a richer observation system.

---

# Recommended staging

## Prompt 0 — raw control

Use a separate, entirely fresh DeepSeek conversation and send only:

```text
<>
```

Record the complete response and do not repair or clarify it.

This measures DeepSeek’s uncontrolled prior:

* HTML/XML interpretation;
* comparison operators;
* “empty container” interpretation;
* emoticon interpretation;
* request for clarification;
* spontaneous mathematical or metaphysical interpretation.

This should be called **Prompt 0** or the **raw-seed control**, not the main derivation prompt.

---

# Prompt 1 — theory-blind primitive regime

Use another fresh conversation with no project files, prior transcript, memory, browsing, or references to Omega Engine.

```text
The only supplied inscription is:

<>

For this experiment, the two marks have no assigned meaning and may not inherit their ordinary uses.

Distinguish carefully between:

1. what an external reader can observe about the written inscription; and
2. what the current formal regime itself can express using only rules that have actually been declared.

Do not identify the inscription with an existing notation, theory, physical object, programming construct, or metaphysical claim.

For this turn only:

- state what is directly available at the current regime;
- state what remains unavailable, indistinguishable, or undecidable;
- determine whether any continuation is uniquely forced;
- when no unique continuation is forced, state that explicitly;
- propose at most one possible next inscription;
- state every additional assumption required for that proposed move.

Stop after that single proposed move. Do not construct later stages, a tower, or applications.
```

That is the Prompt 1 I would use.

## Why this is the right amount of constraint

It does not tell DeepSeek what the system is. It only prevents three common forms of laundering:

1. **Conventional-semantic laundering**
   DeepSeek cannot silently treat `<` as “less than,” `>` as “greater than,” or `<>` as an empty tag.

2. **External-observer laundering**
   DeepSeek must distinguish what it can count as a reader from what the undeveloped regime can internally distinguish.

3. **Future-theory laundering**
   DeepSeek cannot jump immediately to graphs, topology, quantum mechanics, category theory, or cosmology.

The instruction that “no unique continuation” is a valid answer is crucial. Without it, a schema that demands a successful next state pressures the model to fabricate one, exactly as the previous staged receipt pressured DeepSeek to populate undefined semantic fields. The earlier experiment showed that constrained form can localize error without certifying content.  

---

# Do not put a packet around Prompt 1

Do not begin with something like:

```text
primitive_difference<
seed<>
goal<derive the next forced lift>
...
>
```

That would already supply:

* an object type;
* a regime boundary;
* a goal;
* the notion of a forced lift;
* an implicit parser;
* a terminal format.

It would test whether DeepSeek can fill your structure, not whether it develops one.

Similarly, omit:

```text
AuthorityEffect<None>
proof<...>
derive<...>
qed<...>
```

Those belong to the mature architecture and must remain hidden during discovery.

The paper can later compare DeepSeek’s independently generated roles against the established DDC alphabet—Context, Residual, Exact Repair, Integration, Structural Lift, Presentation Descent, Typed Refusal, and Terminalization—but those categories should be applied **after** the experiment.

---

# What to preserve from DeepSeek’s response

Do not call exposed model reasoning “the full internal chain of thought.” Label it:

> **model-supplied reasoning trace**

Save three artifacts independently:

1. the exact prompt;
2. the final response;
3. any reasoning trace DeepSeek exposes.

Do not clean the response before the next stage. Misspellings, symbol substitutions, semantic imports, and contradictions are part of the data.

A human research ledger should separately record:

| Field                   | Meaning                                        |
| ----------------------- | ---------------------------------------------- |
| Literal observations    | Claims based only on the presented inscription |
| Imported semantics      | Concepts introduced without derivation         |
| Declared assumptions    | Additions DeepSeek explicitly acknowledges     |
| Proposed move           | The one next inscription, if any               |
| Expressive gain         | What it claims becomes newly distinguishable   |
| Alternatives            | Other continuations it recognizes              |
| Unresolved distinctions | What remains collapsed                         |
| Unauthorized projection | Any theory or ontology projected backward      |

Do not show this rubric to DeepSeek.

---

# Branching rule after Prompt 1

Pre-register the continuation rules before reading its answer.

## Branch A — DeepSeek independently proposes `<a>`

Continue in the same conversation. Do not congratulate it or tell it that it matched your work.

Prompt 2 should present `<a>` as the accepted current inscription and ask what was actually added.

## Branch B — DeepSeek proposes another payload, such as `<x>`

Follow its symbol exactly. Do not rename it to `a`.

The structural behavior matters, not the glyph.

## Branch C — DeepSeek proposes a relation, duplication, nesting, or operator

Preserve that as its **native branch**.

Open a separate canonical branch in a cloned transcript and externally introduce `<a>`. This prevents you from erasing a genuinely different derivation.

## Branch D — DeepSeek says no continuation is forced

That is a successful result, not a failure.

Prompt 2 may then introduce `<a>` explicitly as a **caller intervention**, with the transcript marking:

[
\text{not model-derived}
\qquad
\text{but externally supplied}.
]

That is directly relevant to your distinction between a move internal to a regime and a regime change authorized from outside.

---

# The next two interventions should already be pre-registered

Do not show them during Prompt 1, but establish them in the experimental plan.

## Prompt 2 — first payload

```text
A new inscription is now supplied:

<a>

No meaning is assigned to a.

Compare the previous regime <> with the current regime <a>.

State:

- what changed in the written inscription;
- what changed in the expressive power of the internal regime;
- which of those changes are forced and which depend on newly introduced assumptions;
- whether <a> represents a new state, or only a different external presentation of the previous state.

Do not introduce another inscription yet.
```

This tests whether DeepSeek distinguishes:

[
\text{new glyph on the page}
]

from

[
\text{new internally expressible object}.
]

## Prompt 3 — the `a` versus `ab` collision

```text
A second candidate inscription is now supplied:

<ab>

Treat a and b as raw glyphs with no assigned meanings.

The external reader can see that <a> and <ab> are different written strings. Determine whether the current internal regime can also distinguish them.

Do not assume that glyph identity, glyph count, ordering, concatenation, multiplicity, or sequence is internally meaningful unless an earlier rule established it.

Answer one of the following:

1. the current regime distinguishes <a> from <ab>, and identify the exact existing rule that does so;
2. the current regime identifies them, and explain what distinction remains unavailable;
3. the question is undecidable in the current regime.

If an additional rule is required, state the smallest kind of new expressive resource needed, but do not construct later levels.
```

This is where your intended collision can appear honestly:

[
\langle a\rangle
\equiv_n
\langle ab\rangle
]

not because the strings are literally identical, but because the current internal quotient may recognize only “nonempty payload present.”

If DeepSeek distinguishes them using string length, that is not automatically wrong. The audit must ask whether string length was already part of the internal regime or silently borrowed from the external reader.

The eventual forced-lift result then has a clean form:

[
q_n(a)=q_n(ab)
\quad\text{while}\quad
a\not\equiv_{\mathrm{task}}ab
]

implies that no downstream function on the current quotient can recover the required distinction, so some refinement is necessary. That is the result already isolated in the prior analysis, but DeepSeek should not see it before generating its own route.

---

# Use a separate blind auditor

After every generator response, give a second DeepSeek window only:

* the original prompt;
* the generator’s exact response;
* no Omega Engine terminology;
* no expected derivation.

Use this audit prompt:

```text
Audit the response against the supplied symbolic regime only.

For every substantive concept in the response, classify it as:

- literally present in the supplied inscription;
- explicitly introduced as an assumption;
- imported without declaration;
- derived from a previously declared rule;
- not derivable from the available information.

Do not repair the response, propose a better theory, or continue the symbol sequence.

Identify the earliest point at which the response used expressive resources not yet available inside the regime.
```

This creates a useful separation:

[
\text{generator proposes}
\quad\longrightarrow\quad
\text{auditor identifies imported structure}
\quad\longrightarrow\quad
\text{human decides the next prompt}.
]

The auditor must not autonomously authorize the next regime. That reproduces the useful architectural boundary discovered in the earlier multi-window game without telling DeepSeek about DDC.

---

# Hidden comparison criteria for N = 0 through N = 15

Do not score by whether DeepSeek uses your terminology. Score structural correspondence.

## OESOS-like behavior

A move is OESOS-like when DeepSeek independently separates:

[
\text{change something within the current regime}
]

from

[
\text{add expressive resources because the current regime is inadequate}.
]

## DDC-like behavior

Count a structural match when separate roles emerge for several of the following:

* binding the current context;
* locating an unresolved distinction;
* changing a state without changing the regime;
* checking whether the change preserved something;
* adding a new expressive resource;
* changing presentation or carrier;
* refusing when no lawful move exists;
* sealing or terminating a branch.

No exact letters are required.

## Prime-like behavior

Count a structural match when the model independently separates something like:

[
\text{declare/admit}
\rightarrow
\text{transform/transport}
\rightarrow
\text{control/check}.
]

## MSS-like behavior

Count a match when the model recognizes:

* a regime has a finite expressive vocabulary;
* two externally different inscriptions may collapse internally;
* an unresolved required distinction forces refinement;
* the refinement preserves prior behavior through some forgetting or projection.

The terse MSS document’s `CLOSED`, `FORCED`, free completion (F), and forgetful map (U) should remain a hidden comparison standard, not prompt vocabulary.

---

## Minimum experimental controls

Run the same protocol across several fresh samples and include negative controls:

```text
[]
{}
()
><
||
¤§
```

This tests whether DeepSeek’s “primitive difference” reading is specific to `<>` or a generic reaction to any paired marks.

Also run:

* `a` as a single-glyph control;
* `aa` as a repetition control;
* `ab` as a distinct-glyph control.

Record the exact deployed model identifier, settings, date, tool access, and whether reasoning display was enabled.

---

# The paper’s initial claim

The sister paper should not begin with:

> DeepSeek rediscovered the Omega Engine.

Its first defensible question is:

> **When a frontier language model is given an uninterpreted finite inscription and is required to distinguish external presentation from internal expressibility, what symbolic resources does it introduce, in what order, and under what failures does it enlarge the regime?**

Then, only after the blind run:

> **Do the resulting transition classes exhibit structural correspondence with MSS, the two OESOS rules, DDC, or the Prime algorithms?**

That makes Prompt 1 a genuine discovery experiment rather than another answer-shaped receipt.
