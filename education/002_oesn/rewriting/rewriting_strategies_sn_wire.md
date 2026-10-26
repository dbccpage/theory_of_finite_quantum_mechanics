# Rewriting S(n) presentations

AuthorityEffect: None. This is a declared extension specification.

The [flat grammar](../grammar/sn.ebnf) parses ground, supplied mark, pair,
cut, lift, retraction and refusal syntax. It does not define a rewrite system.
In particular, its lift body cannot contain another complete presentation.
The recursive `sn-wire-v2` profile in [sn_audit.py](../code/sn_audit.py) handles
nested presentations; selecting that profile is an explicit grammar choice.

## A typed reduction that is justified

For an injection u:A→B and its partial inverse r̂:B→A+{NON_DESCENT}, the rule

\[
\widehat r(u(x))\rightsquigarrow\mathrm{inl}(x)
\]

is justified by the old-image law. In the flat Lean example, A is exactly
`BasePresentation`, not all nested syntax. Composition of partial inverses
uses the actual composable source and target types and propagates refusal.
There is no general rule r_j(r_k(x))=r_min(j,k)(x): its terms may not even have
matching types. Nor is an undefined boundary ∂_k a descent test.

## Paths need their own constructors

A relation a→b and b→c supplies a composable path only after a path category
or equivalent construction is declared. It does not imply an existing primitive
edge a→c. A free category adds identity paths; irreflexive generating edges
remain distinct from identities. The earlier loop reduction to the lone byte
`<` was malformed and is withdrawn.

A polygraph additionally needs typed source and target maps, composition and
higher cells. Merely listing terms, rules and joins does not supply that data.
For a concrete finite confluence calculation use
[Example E11](../levels/level_11_polygraph_confluence_peaks.md).
The local `Polygraph2` class only normalizes repeated `<>` strings by a chosen
length-decreasing rule. It does not alter source opaque-token semantics.

## Transport to packet syntax

A packet encoding must preserve constructor tags, admit a parser and satisfy
round-trip laws on its stated image. [Example E17](../levels/level_17_per_lift_dialects.md)
and `sn_audit.py` demonstrate the tagged boundary encoding. A codec changes
representation; source execution, authorization and semantic preservation
remain separate checks.

---

## Retraction Down-Map Reductions & Pilot Grounding (Rewrite 09)

In the empirical benchmark harness [`omega_engine_pfp/tests/pilot_0000000`](../../../../omega_engine_pfp/tests/pilot_0000000), the S(n) Stage Wire & Retraction Down-Map Form is evaluated as Ingress Dialect `rewrite_09` (`seed_rewrite_09.yaml` and `p_star_rewrite_09.yaml`):

```text
r_1<x->y>
```

### Formal Specification of Rewrite 09
- **Governing Strategy:** S(n) Section-Retraction Reduction Laws & Directed Cut Composition.
- **Dialect Tier:** S(n) Stage Wire (`sn-presentation-v1`).
- **Semantic Carrier:** `LinearSystem(dimension=2, field=Rational)` mapped into a directed transition cut $x \to y$ evaluated under the retraction down-map $r_1$.
- **Reduction Rule:**
  \[
  r_1(\langle x \to y \rangle) \rightsquigarrow \begin{cases}
  \operatorname{inl}(x + y) & \text{if } (x, y) \text{ is in the pre-image of the linear system embedding } u_1, \\
  \operatorname{inr}(\mathrm{NON\_DESCENT}) & \text{otherwise.}
  \end{cases}
  \]
- **Trace Diagnostic:** Without an explicit schema channel for scalar answers, raw scratchpad evaluations exhibit antiskill `antiskill_schema_displacement`. Under $P^*$ compilation, the SPK-001 policy envelope guides the reduction to scalar evaluation while preserving the fail-closed refusal boundary if arithmetic licenses are omitted.

---

## Claim Hygiene Quadrant

1. **What this document supports:**
   - Formalizes the typed retraction down-map reduction rules for S(n) presentations.
   - Grounded directly in `sn.ebnf` and verified by `sn_audit.py`.
   - Links the theoretical retraction law to empirical test dialect `rewrite_09` in `pilot_0000000`.

2. **What this document does not support:**
   - Does not assert that higher boundaries $\partial_k$ or arbitrary retraction compositions are generally confluent without explicit polygraph syzygies.
   - Does not mint authority or self-certify correctness (`AuthorityEffect: None`).

3. **Narrowest defensible claim:**
   - Under the declared assumptions of `sn.ebnf` and the old-image law, retraction down-maps define typed partial inverses that deterministically propagate refusal outside the admitted pre-image.

4. **Next test needed:**
   - Execute formal Lake elaboration of the retraction down-map in `omega_engine_education/documentation/002_oesn/lean4/` to ensure zero axiom injection.

