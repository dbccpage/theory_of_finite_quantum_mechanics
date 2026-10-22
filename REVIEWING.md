# Reviewing

**AuthorityEffect:** None. A review is one reader's recorded opinion. It does not change a node's status by itself.

This project says in public which of its steps are derived, which are conditional, which are imported and which are open. That only means something if people outside the project check it. This page explains what a reviewer looks at, how a verdict is written, how a review is recorded and how reviewers are credited. A call for reviewers, dated, is at the end.

## What a reviewer checks

A review covers any of the five items below. You do not have to cover all of them; say which you assessed.

1. **Statement fidelity.** Does the node's statement say what its source says? Does the Lean declaration (or the paper proof) state what the node says, no more and no less? Are quantifiers, carriers (for example the rational or Gaussian-rational field), hypotheses and the direction of implications the same in all three places?
2. **Proof correctness.** Is the proof valid? For Lean: does the cited declaration prove the statement it appears to prove, with the hypotheses it needs and only the axioms `propext`, `Classical.choice` and `Quot.sound`? Is there a definition that makes the claim trivial, or an instance that is too small to carry the claim? For a paper proof: is every step justified?
3. **Prose clarity.** Can a mathematician or physicist follow the derivation note without Lean? Is it clear what is assumed, what is proved and what is open? Is notation defined before use?
4. **Code correctness.** Does the independent check (SymPy or plain Python) or the Rust or Python certifier compute what the node says it computes? Is the arithmetic exact? Does it share code with the thing it checks (it should not)?
5. **Overclaiming.** Anywhere that the node, the note, the README or a commit message says more than the evidence supports: a status label too high for its evidence, a general word for a fixed instance, a name that suggests a famous theorem the statement does not reach.

The project has lowered its own labels before when review found them too strong, and a reviewer who finds another case is doing exactly what this page asks. Examples are in the README section "How claims are kept honest".

## Rubric

Give one verdict for each item you assessed.

| Verdict | Meaning |
|---|---|
| **A: agree** | I read it and found no error or gap. State what you read and at which commit. |
| **B: agree with remarks** | The substance holds. There are minor issues: unclear wording, a missing hypothesis in the prose, a weak but valid argument. List each one. |
| **C: disagree** | I found an error, a gap or an overstatement. Say where, and say what you think the correct statement or status is. |
| **N: not assessed** | I did not assess this item, or it is outside my competence. This is a normal answer. |

Then give one recommendation about the node's label:

| Recommendation | Meaning |
|---|---|
| **Label supported** | The status label matches the evidence. |
| **Label too strong** | The evidence supports a narrower statement or a lower status. Propose it. |
| **Label too weak** | The evidence supports more than the label claims. Say why. |
| **Cannot say** | I could not assess enough to recommend. |

For overclaiming, read the scale as: A, nothing overstated that I found; B, minor overstatement; C, material overstatement; N, not assessed.

A verdict of A on proof correctness for a Lean node means "the declaration proves what the statement says". It does not mean "the physics is right". If you have a view on the physics or the interpretation, say so under *other remarks*, separately.

## How to review a node

Pick a node (issues carrying the label `review-needed` and the [example prompts](docs/contribute/example_prompts.md) are starting points, and the call below lists areas). Then read, in this order:

1. **The node.** Print it from the DAG. The command below uses the node L1-IMP-HILBERT-INNER-PRODUCT; **replace that id with the node you chose** (do not type angle brackets into a shell, where < is redirection):
   ```
   python -I -X utf8 -c "import json,sys; n={x['id']:x for x in json.load(open('dag/derivation_dag.json',encoding='utf-8'))['nodes']}[sys.argv[1]]; print(json.dumps(n,indent=1,ensure_ascii=False))" L1-IMP-HILBERT-INNER-PRODUCT
   ```
   Note `status`, `statement`, `bottleneck`, `lean`, `rust`, `source` and `pfp_review` (the latter holds the narrowest claim from the earlier host review, if there is one). Status labels are defined in `status_legend` in the same file.
2. **The evidence page** for the node. Per-node evidence pages are proposed in [pull request #181](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/pull/181) (planned location `docs/evidence/nodes/`, one file per node id) and are not on `main` yet. Until your node has a page, use steps 3 to 6 directly.
3. **The Lean file.** The `lean` field names `path::declaration` pairs. Open the declaration and read its statement and the lines that follow it. Then compare it with the node statement, claim by claim. You can do this on GitHub without building. If you want to elaborate it, see the Lean setup in [`CONTRIBUTING.md`](CONTRIBUTING.md); the `#print axioms` lines at the end of a campaign module show what it depends on. A node with no `lean` entry has no Lean proof, and that is part of its label.
4. **The independent check**, if there is one. Under the [campaign protocol](dag/pfp/campaign/README.md) each attempted target gets a script `checks/independent/<node id in lower case>.py`, a SymPy or plain-Python script that recomputes the claim without importing repository code; run it with `python -I -X utf8` and the script path. None exists on `main` yet. Nodes may have a Rust or Python certifier under `code/`, named in the `rust` field.
5. **The derivation note.** Every node has a paper under `dag/derivations/` (its path is the first `source` entry of most nodes). Attempted campaign targets also have `dag/derivations/independent/<node id in lower case>.md`, whose first line says whether a human has reviewed it. Only a named human reviewer may change that line; an AI-drafted note stays marked as such until one does.
6. **The history.** `git log --follow` on the file, and the earlier review records under `dag/results/<node id>/reviews/`, show what was already narrowed and why.

Then open a [*Derivation review* issue](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/issues/new?template=derivation_review.yml). Give the node id, the commit you reviewed (`git rev-parse HEAD`), your background in one line, your verdict for each item, and your specific issues. Be specific: a line, a declaration name, a quantifier. A review that says "looks fine" is welcome if it says what you looked at.

Reviewing the tooling instead? Code correctness of scripts such as `dag/validate_derivation_dag.py`, `dag/pfp/llm_ladder/verify.py` and `scripts/build_status.py` is a valid review too. Open the same issue form and give the file in place of a node id.

## How reviews are recorded

1. **A review issue.** You open the *Derivation review* issue. It is public, and it is the record. You may use a pseudonym.
2. **The maintainer records it.** The maintainer reads it, replies, asks for clarification if needed, and adds a row to [`docs/reviewers.md`](docs/reviewers.md): date, node or file, reviewer (as you wish to be named), verdict, commit reviewed and a link to the issue. Where the review finds an error, the maintainer opens a fix or a label change in a separate pull request that links to the issue. Reviewers do not edit DAG data directly.
3. **Credit.** Your row stays in the table. If a node's evidence page lists its reviews, yours appears there with the same link. A review that leads to a change is named in that change's pull request.
4. **Disagreement.** If you and the maintainer disagree, both positions stay in the issue. A node is not relabelled upward because a review is favourable, and not left unchanged because one is unwelcome.

A recorded review is the opinion of one reader on stated files at a stated commit. It is not a certification. The status of a node changes only through a pull request that meets the rules in [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Call for reviewers

*Dated 22 October 2026.*

I am looking for professional mathematicians and physicists who are willing to read one part of this project critically and tell me where it is wrong or overstated. I would rather hear it from a specialist now than later.

**What the project is.** A public derivation graph (node counts are on the generated status page, <https://dbccpage.github.io/theory_of_finite_quantum_mechanics/status/>) that asks how much of quantum mechanics follows from a finite, exact substrate, starting from a single inert mark, and records which steps are derived, conditional, imported, refuted or open. It does not claim to derive quantum mechanics. Many of its nodes are small finite statements checked in Lean 4 against Mathlib. Several are conditional on structure that is supplied, and that is stated in each node.

**What I would like checked.** Whether the statements say what their proofs prove; whether the proofs are valid; whether the derivation notes can be followed by a specialist; whether the labels are honest. Corrections of mathematics, of terminology and of attribution are all in scope.

**Areas that most need a specialist reader**

| Area | Where to start | Stage in the DAG |
|---|---|---|
| Finite quantum-mechanics foundations (inner product, complex field, dynamics, tensor composition) | `L1-IMP-HILBERT-INNER-PRODUCT`, `L1-IMP-COMPLEX-FIELD`, `L1-IMP-LINEAR-ISOMETRIC-DYNAMICS` | `L1_TO_L2`, `FINITE_QM_CORE`, `FINITE_QM_DYNAMICS`, `TENSOR_COMPOSITION` |
| Gleason-type results and the Born rule | `FQ-GAP-BORN-UNIQUENESS-GLEASON` (the Born rule from effect-additive valuations on rational matrices, conditional on a supplied matrix carrier) | `FINITE_QM_CORE` |
| Mutually unbiased bases | `MUB6-PRODUCT-TRIPLE-LOWER-BOUND`, `MUB6-MAX-MUB-SIX-EQUALS-THREE` (open in the literature; nothing here closes it) | `MUTUALLY_UNBIASED_BASES` |
| Lattice fermions, sign problem and Majorana systems | `FSP-MASTER-DICHOTOMY-REFUTED`, `FSP-JORDAN-WIGNER-HOP-SIGN`, `MAJ-PARITY-SECTOR-SPLIT-EXACT` | `FERMION_SIGN`, `MAJORANA`, `DRESSING_FIELD` |
| Constructor theory | `CT-QUBIT-NO-CLONING-FINITE-TARGET`, `CT-TASK-CONSTRUCTOR-POSSIBILITY` | `CONSTRUCTOR_THEORY` |
| Causal sets and algebraic QFT | `CQFT-MYRHEIM-MEYER-ORDERING-FRACTION-TARGET`, `CQFT-FINITE-CAUSET-IDENTIFICATION` | `CAUSAL_QFT` |
| Loop quantum gravity and spin networks | `LQG-6J-EXACT-AND-PENTAGON-TARGET`, `LQG-AREA-SPECTRUM-EXACT-TARGET` | `LOOP_QUANTUM_GRAVITY` |
| Lean 4 and Mathlib (idiom, vacuity, axioms, statement-versus-theorem) | `QCV-VIABILITY-NEEDS-ALL-REQUIREMENTS`, any module in [`lean4/`](lean4) | all |

The frontier nodes (constructor theory, causal QFT, AdS/CFT, loop quantum gravity) were narrowed to what their Lean modules prove, 3 in full and 11 narrowed. They have had no review by a specialist in those fields, and this is where an expert's reading is most valuable.

**Time.** One node, with its Lean declaration and note: one to three hours. A single Lean module, for idiom and vacuity: one to two hours. There is no standing commitment. One review is a useful contribution, and no follow-up is expected.

**Credit.** You are named in [`docs/reviewers.md`](docs/reviewers.md) with the nodes you reviewed, the commit, the date and a link to your review, using the name and affiliation you choose, or none. Where a review changes the repository, the pull request says so. If the work is written up, reviewers who wish to be acknowledged will be. There is no payment: the project is independently funded and has no budget for it. Authorship is not offered in exchange for a review.

**How to start.** Open a [*Derivation review* issue](https://github.com/dbccpage/theory_of_finite_quantum_mechanics/issues/new?template=derivation_review.yml), or, if you want to ask a question first, open a blank issue titled "Reviewer question: <area>". The statement of what the project claims and does not claim is in the [README](README.md) and on the generated status page, <https://dbccpage.github.io/theory_of_finite_quantum_mechanics/status/> (published by the daily workflow once Pages is enabled).

**What I will not do.** I will not argue a node's label upward in response to a review, quote a review as an endorsement of the project, or treat silence as agreement.
