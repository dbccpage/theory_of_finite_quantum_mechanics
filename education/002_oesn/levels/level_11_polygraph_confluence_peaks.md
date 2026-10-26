---
documentation_contract: symbol-game-documentation/v1
title: "Example E11: Priced Joins of Divergent Reductions"
kind: mathematical-reference
level: 11
status: active
maturity: research
claim_status: review_required
authority_effect: "None"
source_paths:
  - omega_engine_education/documentation/002_s_n/sn.md
  - omega_engine_education/documentation/002_s_n/_images/sn_11_polygraph_confluence_peaks.svg
---

# Example E11: Priced Joins of Divergent Reductions

**AuthorityEffect:** None.
**GenesisEffect:** None (example level must never extend Genesis core merely by being constructed).
**Layer:** Example Specification
**ExampleId:** E11 (Candidate Example Level; not a normative Genesis core stage)
**Description:** Priced joins of divergent reductions comparing asymmetric rule additions against symmetric diamond terms.

---

## 1. Schematic & Conceptual Architecture

> [!NOTE]
> **Epistemic Provenance Boundary:** S(0)–S(6) are this strand’s presentation labels; see the [source correspondence](../source_correspondence.md). Example $E11$ replaces broad subject headings with a finite problem whose witnesses, obstructions, and extension costs are displayed completely.

This level formalizes priced joins for divergent rewrite reductions:
1. **Finite Seed Configuration:**
   - Closed finite rewrite carrier with terms $u, v, w$ and rules $u \to v$, $u \to w$.
   - Terms $v$ and $w$ are irreducible.
   - Demand: Unique normal forms on this carrier and on any admitted new terms.

---

## 2. Admissible Response Classes & Cost Comparison

1. **Response Class A (Asymmetric Rule Addition):**
   - Add a rewrite arrow while retaining old arrows.
   - Price by number of new rules.
   - Zero new rules leave two normal forms for $u$.
   - One rule $v \to w$ suffices; symmetric choice $w \to v$ also suffices. Both cost-1 responses are minimal.
   - For $v \to w$, term ranks $\rho(u)=2, \rho(v)=1, \rho(w)=0$ decrease strictly on every arrow, and every term reduces uniquely to $w$.
2. **Response Class B (Symmetric Diamond Join):**
   - Require a fresh common normal form $j$ while keeping $v$ and $w$ incomparable by direct reduction.
   - The diamond adds one new term $j$ and two rules $v \to j, w \to j$. Ranks are $\rho(u)=2, \rho(v)=1, \rho(w)=1, \rho(j)=0$.
   - Cost: 1 new term + 2 new rules, rather than the cost-1 minimum of Class A.

---

## 3. Verifier Obligation & Counterexamples

- **Counterexamples:** Omitting either arm of the diamond leaves a non-joinable fork. Adding a fuel counter to the evaluator ensures a bounded run returns; it does not prove termination of the underlying rules.
- **Adapter Cost:** Finite term carrier, rewrite relation, response restrictions, and reduction order. Context closure or variable-bearing rules enlarge the quantified carrier and require a new argument.
- **Build Obligation:** Enumerate normal forms and reachable joins in the declared finite carrier, supply rank inequalities, and retain both tied Class-A minima. Tested peaks provide scoped evidence; universal confluence requires covering all relevant branchings.

---

## 4. Claim Hygiene Quadrant

1. **What this supports:**
   - Proof that Class A minimum cost is 1 rule ($v \to w$ or $w \to v$), while Class B diamond join costs 1 new term + 2 rules.
   - Exact rank inequality proof of termination for the joined rewrite system.
2. **What this does not support:**
   - Does not prove termination of arbitrary unfuelled relations without a well-founded reduction order.
   - Does not establish a normative Genesis core stage succession.
3. **The narrowest defensible claim:**
   - On the finite fork $u \to v, u \to w$, resolving divergence under Class A costs 1 rule, while Class B diamond join costs 1 term and 2 rules.
4. **Next test needed:**
   - Verify confluence checker confirms unique normal form $w$ for $v \to w$ and rejects incomplete diamond arms.

