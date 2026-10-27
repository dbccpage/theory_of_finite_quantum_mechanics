# S(n) Grammar and Mathematical Reading Guide

**AuthorityEffect:** None. Status: Active.\
**Genesis & WDP Alignment:** Standardizes wire tokens and mathematical invariants for the binary germ, the Witnessed Irreflexive Relation (WIR) endpoint support ($`\Delta_{\mathrm{support}} = 2`$), and later presentation constructions related to Genesis through the [source correspondence](../source_correspondence.md).

> **Math rendering.** Inline math uses GitHub's $`\ldots`$ form and display math
> uses fenced `math` blocks, so Markdown never reads `_` or `\_` inside a formula
> as emphasis or an escape. Wire tokens such as `NON_DESCENT` are written as code,
> not as math.

---

## 1. The Binary Germ & $`\Delta_{\mathrm{support}} = 2`$

For an irreflexive relation $`R`$,

```math
R(a,b) \implies a \neq b
```

Otherwise $`R(a,b)`$ would become $`R(a,a)`$, contradicting irreflexivity. Consequently, every admitted primitive cut has **exactly two distinct endpoints**:

```math
\Delta_{\mathrm{support}}(a,b) := \lvert\{a,b\}\rvert = 2
```

This provides the mathematically defensible meaning for the constant $`\Delta_w = 2`$. It applies wherever an inhabited primitive cut exists (the ground and singleton stages contain no such cut).

### Separation of Quantities

| Quantity | What Follows from an Inhabited Irreflexive Cut | Verification / Lean 4 Source |
| :--- | :--- | :--- |
| **Distinct endpoints of that cut** | **Exactly 2** ($`\Delta_{\mathrm{support}} = 2`$) | `PrimDiff.irrefl_witness_ne` |
| **Minimum carrier size supporting it** | **2** | `PrimDiff.no_witness_on_subsingleton` |
| **Witness occurrences or certificates** | **May be 1, 2, or more** | `PrimDiff.single_oriented_witness_consistent` (1 witness fwd, 0 rev) |
| **Newly supplied carrier elements** | **May be 0** (when both endpoints already exist) | Already admitted endpoints; no new datum is needed |
| **Operator count or description cost** | Depends on the declared accounting model ($`\mu_1, \mu_2`$) | `cost1_insufficient_general` |
| **Total carrier size** | Can grow arbitrarily while each primitive cut remains binary | Carrier growth across stages |

`PrimDiff.lean` makes this distinction concrete: `irrefl_witness_ne` establishes distinct endpoints ($`a \neq b`$), while `single_oriented_witness_consistent` constructs an explicit model with one witness occurrence from false to true and none in the reverse direction. Thus, **two endpoints** is established; "two witness occurrences everywhere" is contradicted by explicit models.

### Universal Binary Germ ($`D_2`$)

Let $`D_2`$ have carrier $`\{0, 1\}`$ and the single directed edge $`0 \to 1`$. Given any admitted pair $`R(a,b)`$, there is exactly one point-preserving function

```math
f \colon D_2 \longrightarrow (A, R), \qquad f(0) = a, \quad f(1) = b
```

and it preserves the edge. Irreflexivity makes its two endpoint images distinct. At the level of relation-preserving functions, this constitutes the universal binary germ (`D2_initial_pointed`).

### Tagging Collision Resolution

Suppose an observation $`q \colon A \to O`$ collapses an admitted distinction: $`q(a) = q(b)`$. Supply a binary tag $`t \colon A \to \{0, 1\}`$ with $`t(a) = 0`$ and $`t(b) = 1`$, and define

```math
q'(x) = \bigl(q(x),\, t(x)\bigr)
```

Then

```math
q'(a) \neq q'(b), \qquad \mathrm{pr}_O \circ q' = q
```

The lifted presentation resolves that collision while retaining the previous observation. Two tag values suffice for one conflicting pair; multiple conflicting pairs generalize to a graph-coloring problem whose primitive constraints remain binary.

---

## 2. Inscription vs. Admission

- **Ground Inscription `<>`:** One opaque presentation lexeme, two ASCII bytes (`len = 2` bytes, 1 token), with **zero admitted carrier elements** ($`\lvert V_0 \rvert = 0`$, proved inertia under `CL-0-INERTIA` and `supply_no_op`).
- **Supplied Mark `<a>`:** Records a single mark. `<a>` alone does not force admission or $`\lvert V_1 \rvert = 1`$. Under quiescent equilibrium, admission requires an explicit consumer or retention receipt.
- **Pair syntax `<ab>`:** This grammar parses two glyphs. The source Genesis token `<ab>` is instead one opaque whole. Parsing this local pair does not admit either glyph or a relation.

---

## 3. Section and Retraction Dynamics

For presentation stages $`P_n`$ and $`P_{n+1}`$, write $`\bot_{\mathrm{ND}}`$ for the refusal value that the wire profile spells `NON_DESCENT`.

- **Section Lift:** $`u_n \colon P_n \hookrightarrow P_{n+1}`$.
- **Typed Retraction Down-Map:** $`\widehat{r}_n \colon P_{n+1} \to P_n \sqcup \{\bot_{\mathrm{ND}}\}`$.
- **Exact Typed Retraction Law:**

  ```math
  \widehat{r}_n \circ u_n = \mathrm{inl}
  ```

  On the image $`\mathrm{im}(u_n)`$, $`\widehat{r}_n(u_n(x)) = \mathrm{inl}(x)`$, recovering the lower stage exactly.
- **Descent Refusal:** For novel terms $`y \notin \mathrm{im}(u_n)`$, $`\widehat{r}_n(y) = \mathrm{inr}(\bot_{\mathrm{ND}})`$, that is, the wire token `NON_DESCENT`. This defines exact recovery from the image, kept separate from a total forgetful projection or Postnikov down-map.

### Homotopy Truncation ($`j`$) vs. Construction Stage ($`n`$)

Calling $`S(n)`$ a Postnikov tower adds mathematical requirements:

- $`n`$ = construction stage
- $`j`$ = homotopy truncation depth

For a fixed space $`X`$, its Postnikov stages $`P_j X = \tau_{\le j} X`$ preserve homotopy groups through degree $`j`$ and remove higher ones. Downward maps are total; upward sections are additional structure and need not exist. Successive truncations preserve $`\pi_0`$. Therefore, an empty-space stage followed by a point cannot be successive truncations of the same space $`X`$.

After supplying an explicit realization $`\rho(S(n))`$, $`P_j(\rho(S(n)))`$ is the candidate Postnikov tower at fixed $`n`$. Growth across construction stages $`n`$ remains a separate construction requiring its own preservation proofs.

---

## 4. Wire Profiles & Conformance Testing

The flat grammar `sn.ebnf` uses **50 distinct characters**: the 26 lowercase letters and 10 digits of $`\Sigma_{36}`$, the seven punctuation marks `<`, `>`, `[`, `]`, `,`, `-` and `_`, and the seven capitals `N`, `O`, `D`, `E`, `S`, `C`, `T` that occur only in the literal `NON_DESCENT`. The lift and retraction prefixes `u_` and `r_` use the ordinary letters `u` and `r` with an ordinary underscore.

1. **Version 1 Flat Profile (`sn-wire-v1`):**
   - Ground: `<>`
   - Mark: `<a>`
   - Pair: `<ab>`
   - Cut: `<a->b>`, `[a,b]`
   - Section/Retraction: `u_6<a->b>`, `r_6<ab>`
2. **Recursive Profile (`sn-wire-v2`):**
   - Permits complete presentations inside lift/retraction enclosures:
     - `u_0<<>>` (stage 0 lift enclosing ground token)
     - `r_6<u_6<<ab>>>` (nested retraction of lift)

### Automated Conformance & Auditing

Run from the repository root:

```sh
# Standalone CLI checker
py -3.12 education/symmetric_group_presentations/code/check_sn.py

# Grammar conformance test suite (syntax cases SN_001–SN_085)
py -3.12 -m pytest education/symmetric_group_presentations/code/tests/test_sn_grammar.py

# Comprehensive audit & WIR verification test suite
py -3.12 -m pytest education/symmetric_group_presentations/code/tests/test_sn_audit.py
```

The recursive profile is implemented by `sn_audit.py`; it is not a production
in `sn.ebnf`. `sn_codec.py` normalizes stage numerals such as `u_006<a>` to
`u_6<a>`; use the audit codec when exact source spelling must be retained.
