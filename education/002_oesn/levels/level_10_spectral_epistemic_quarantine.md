---
documentation_contract: symbol-game-documentation/v1
title: "Example E10: Minimum Observation Refinement"
kind: mathematical-reference
level: 10
status: active
maturity: research
claim_status: review_required
authority_effect: "None"
source_paths:
  - omega_engine_education/documentation/002_s_n/sn.md
  - omega_engine_education/documentation/002_s_n/_images/sn_10_spectral_epistemic_quarantine.svg
---

# Example E10: Minimum Observation Refinement

**AuthorityEffect:** None.
**GenesisEffect:** None (example level must never extend Genesis core merely by being constructed).
**Layer:** Example Specification
**ExampleId:** E10 (Candidate Example Level; not a normative Genesis core stage)
**Description:** Minimum observation refinement resolving multi-mark collapse via tag alphabets and binary coordinates.

---

## 1. Schematic & Conceptual Architecture

> [!NOTE]
> **Epistemic Provenance Boundary:** S(0)–S(6) are this strand’s presentation labels; see the [source correspondence](../source_correspondence.md). Example $E10$ replaces broad subject headings with a finite problem whose witnesses, obstructions, and extension costs are displayed completely.

This level formalizes minimum observation refinement when an existing observation collapses multiple admitted marks:
1. **Finite Seed Configuration:**
   - Admit carrier $A = \{a, b, c\}$.
   - Supplied observation $q$ takes the same value on all three marks: $q(a) = q(b) = q(c)$.
   - Supply pair-separation demands for all three unordered pairs: $\{a,b\}, \{b,c\}, \{a,c\}$.
   - No mark is silently identified with another in the metatheory.
2. **Admissible Response Class:**
   - Refine observation $q$ to $q'(x) = (q(x), t(x))$, where the only new data are tag values $t(x) \in T$.
   - Old observations are recovered exactly by first projection: $\operatorname{pr}_1 \circ q' = q$.

---

## 2. Mathematical Presentation & Transition Rules

1. **Cost & Minimality Proof:**
   - For a tag alphabet $T$, resolving all three pairwise demands requires three distinct tag values: $|T| \ge 3$.
   - Tags $t(a)=0, t(b)=1, t(c)=2$ attain the minimum bound $|T| = 3$.
   - If the response uses $k$ fixed binary coordinates $t(x) \in \{0, 1\}^k$, the tag space has $2^k$ available values: $2^k \ge 3 \implies k \ge 2$.
   - Binary coordinate assignments $t(a)=(0,0), t(b)=(0,1), t(c)=(1,0)$ attain the exact bound $k=2$.
2. **General Demand Graph Equivalence:**
   - For a finite demand graph $G = (V, E)$, where edges represent pairs collapsed by $q$ that require separation, admissible tag assignments correspond to proper vertex colorings of $G$.
   - Minimum tag alphabet size is the chromatic number $\chi(G)$.
   - Minimum fixed binary coordinate count is $k = \lceil \log_2 \chi(G) \rceil$.
3. **Adapter Cost:**
   - Finite tag alphabet $T$, tag assignment function $t: A \to T$, and declared set of conflicts $E(G)$.
   - *Epistemic Precision:* Binary endpoint support ($\Delta_{\mathrm{support}} = 2$) does not imply a universal 1-bit repair for multiple conflicting pairs. Chromatic tag cost is kept distinct from new carrier element count.

---

## 3. Verifier Obligation & Counterexamples

- **Negative Counterexample:** Any single binary tag ($k=1$) assigns the same value to at least two of $\{a, b, c\}$, leaving at least one separation demand unresolved.
- **Build Obligation:** Exhibit the successful tag table, demonstrate a collided pair for every 1-bit assignment, and verify old-observation recovery via first projection.

---

## 4. Claim Hygiene Quadrant

1. **What this supports:**
   - Machine-checked proof that separating three mutually collapsed marks requires $|T| \ge 3$ tag values or $k \ge 2$ fixed binary coordinates.
   - Proof that old observations are preserved via first projection.
2. **What this does not support:**
   - Does not claim that computing $\chi(G)$ is computationally tractable for arbitrary graphs.
   - Does not establish a normative Genesis core stage succession.
3. **The narrowest defensible claim:**
   - On carrier $\{a, b, c\}$ under constant observation $q$, refining $q$ to resolve all three pair-separation demands requires at least 3 tag values or 2 binary coordinates.
4. **Next test needed:**
   - Verify tag table evaluator rejects 1-bit binary assignments on $K_3$ conflict graphs.

