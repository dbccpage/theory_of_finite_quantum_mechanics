<div align="center">

# Minimal Symbol System - N (MSS-N): Conservative Grammar Growth, Homological Obstructions, and Invariant-Preserving Lifts

### A Foundational Monograph on Minimal Glyph Languages, Retraction Invariants, and Topological Obstruction Ledgers

**The Symbol Game & Omega Engine Architecture Group**
*Version 0.2.0 · Research Monograph Pre-Print · 2026-10-05*
*Tracked Reference Baseline: `mssn.ebnf` (22 Starts) & `check_grammars.py` (6 Retained Profiles)*

</div>

> **Academic Nonclaim Standard:**
> This monograph assigns no operational authority, institutional standing, or sweeping claims. The structural transformations, homological obstructions, and retracting chain maps documented herein reflect finite mathematical models, explicit grammar declarations, and exact symbolic checkers within scoped test settings.

---

## Abstract

This monograph formalizes the mathematical and grammatical foundations of the **Minimal Symbol System - N (MSS-N)**, a parameterized family of minimal glyph languages defined over an alphabet of up to 38 characters: 26 lowercase Latin letters (`a`–`z`), 10 decimal digits (`0`–`9`), and 2 directional relation symbols (`<`, `>`). We analyze the algebraic, grammatical, and topological consequences of incremental alphabet expansion and vocabulary manipulation.

We show that expressive capability does not advance through raw key counts alone; rather, new capabilities depend on explicitly declared formation, identity, decoding, and manipulation rules:
1. **One glyph with repetition** already generates arbitrarily long words in a free monoid; a declared length decoder supplies unary counting.
2. **Two glyphs** introduce noncommutativity in the free concatenation monoid ($ab \neq ba$) and support binary numeral encoding without requiring literal names `0` and `1`.
3. **Relations** can be encoded by position, pairing, or external codebooks without awaiting explicit arrow glyphs; the arrival of `<` and `>` supplies dedicated relational syntax.

We disprove the false monoid and category isomorphisms that often arise in informal treatments. Specifically, we prove that free monoids on distinct numbers of generators are not isomorphic ($\{0,1\}^* \not\cong \{0,\dots,9\}^*$) by analyzing indecomposable elements, and show that discrete categories with 2 and 26 objects are neither isomorphic nor equivalent.

At the core of the lift discussion, we establish the fundamental obstruction theorem:
$$\textbf{Proposition.}\text{ An extension that kills a nonzero homology class cannot have a chain-map retraction preserving the original complex.}$$
We demonstrate this obstruction in the minimal setting of two disconnected points bridged by an edge, and apply it to cycle filling in the pinned $K_0$ simplicial complex.

Finally, we document the operational architecture: the 22 explicit starts of `mssn.ebnf`, the four distinct profile readings of unwrapped inscriptions (e.g. `a>b>c>a` and `a0>b2>c1>a0`), the six retained runtime profiles of `check_grammars.py`, and the strict operational demarcation between syntax verification and semantic evaluation.

---

## Read This First: The Whole Story in Seven Sentences

Picture a keyboard with 38 keys: letters `a` to `z`, digits `0` to `9`, and arrows `<` and `>`.

Switch the keys on one at a time and ask: *what can be expressed now under declared formation and decoding rules that could not be expressed before?*

Adding a glyph does not automatically introduce a number system, relation, sentence, type, or category; each requires explicit formation and interpretation rules.

One glyph with repetition already allows unary counting; two glyphs introduce noncommutativity ($ab \neq ba$) and binary encoding; arrow glyphs supply dedicated relational syntax.

At the level of formal languages, alphabet expansion yields a retraction ($r\ell = \operatorname{id}$) that recovers prior expressions, but does not bound what new structures the larger system can express.

When an extension is constrained to kill a topological gap or fill a cycle, an exact mathematical obstruction arises: no chain-map retraction can both kill a non-zero homology class and preserve the original complex.

Tracking these obstructions and pairing them with explicit witnesses is the domain of homology and cohomology.

---

## Part 0: The Discipline of Absence: Distinguishing Four Mathematical States

To construct a formal symbol system without unearned assumptions, one must avoid smuggling ambient containers into the object theory before the first rule is admitted. In particular, four distinct mathematical conditions must remain strictly distinguished:

$$\boxed{\text{absent input} \quad\neq\quad \varepsilon \quad\neq\quad \text{literal } \langle\rangle \quad\neq\quad \text{declared ground}}$$

1. **Absent Input:** The condition where no string or expression is supplied to the evaluator. At the metalanguage level, this is an explicitly typed option: $\operatorname{Option}\langle\text{InscribedString}\rangle = \operatorname{None}$. It does not exist as an element of the object alphabet or as a node in an object AST.
2. **The Empty Word ($\varepsilon$):** The unique identity element of a string monoid $\Sigma^*$, having length zero ($|\varepsilon| = 0$). Removing an $\varepsilon$ production from a grammar excludes the empty word from the accepted language; it does not eliminate the mathematical framework in which the grammar and strings are defined.
3. **The Literal Token $\langle\rangle$:** A concrete, two-character terminal string in the `mss-boundary-v1` dialect. It is not "nothing"; it is a positive syntactic mark denoting a nullary container or ground packet.
4. **Declared Ground:** An explicitly admitted mathematical base state in a derivation or protocol (such as the initial carrier $R_0 = \{a\}$ in Genesis, or the terminal category $\mathbf{1}$).

### Meta-Grammar vs. Object-Level Derivations

An object grammar derives strings within a declared formal system; it cannot derive the non-existence of its own derivation. Attempting to express "no grammar" via an object-level production such as:
```ebnf
Grammar ::= ∅ | Mark
```
does not establish the absence of a framework. If an evaluator must handle the absence of a grammar or input, that option must be represented at the metalanguage level in the host environment (e.g. `Option<Grammar>` in Rust or `Optional[Grammar]` in Python). Host mathematics must always be explicitly declared.

---

## Part 1: Meet the 38 Keys & Separation of Declared Data

The baseline alphabet $\Gamma_{38}$ consists of 38 discrete glyphs:
- **26 Lowercase Latin Letters:** `a, b, c, ..., z`
- **10 Decimal Digits:** `0, 1, 2, ..., 9`
- **2 Relation Marks:** `<`, `>`

### 1.1 Eight Dimensions of Declared Data

To prevent conceptual conflation, every symbol-manipulation model must explicitly separate eight distinct dimensions of data:

1. **Terminal Spellings:** The exact character inventory (e.g. ASCII bytes vs. Unicode code points).
2. **Tokenization Policy:** How character streams partition into tokens. Maximal-munch is one possible declared policy, not a global invariant.
3. **Grammar:** The formal formation rules (productions) defining well-formedness.
4. **Public Start Symbol:** The explicit entry point for parsing (selected from declared starts; never guessed).
5. **Layout Policy:** Rules governing whitespace, line breaks, and indentation.
6. **Identity Policy:** How tokens are equated (e.g. identity by literal label spelling vs. identity by occurrence/position).
7. **Annotation Decoding:** How parsed substrings map to semantic values (e.g. string digits to integers, rationals, or labels).
8. **Manipulation Rules:** Permitted transformations, rewrites, and operations over inscriptions.

### 1.2 Decoupling the Three Overloaded Relations

Informal descriptions frequently use a single relation symbol $R$ to mean three completely different concepts. This monograph decouples them:

1. **Encoded Relation ($E \subseteq V \times V$):** The relation represented *inside* an inscription (e.g. directed edges in a graph).
2. **Rewrite Relation ($\to_{\text{rewrite}} \subseteq \Sigma^* \times \Sigma^*$):** The operational relation *between* inscriptions defining permitted transformations.
3. **Observation Map ($q: V \to O$):** A comparison or quotient map used to distinguish or collapse decoded objects under an observer's lens.

### 1.3 Unicode Tokenization and Normalization

When expanding beyond ASCII to Unicode glyphs (as in `unicode_path`):
- Distinguish bytes, Unicode scalar values (code points), grapheme clusters, and declared grammar tokens.
- For example, the token `👩‍💻` ("technologist") consists of three code points joined by a Zero-Width Joiner: `U+1F469` (Woman), `U+200D` (ZWJ), `U+1F4BB` (Laptop).
- The grammar treats this sequence as a single atomic token only under an explicit tokenization and normalization policy (e.g. NFC vs NFD, exact byte matching).

---

## Part 2: The Three Master Lenses: Genesis, HoTT, and Category Theory

We analyze glyph systems through three formal perspectives, replacing informal metaphors with explicit constructions:

### 2.1 Genesis Lens: Builders, Admissions, and Obstructions

In the Genesis metatheory:
- **Presentation vs. Admission:** External presentation ($\operatorname{Supply}$) places data outside the carrier. A datum enters the object system only when admitted into the active carrier registry ($\operatorname{AdmitDatum}$).
- **Quiescence:** A carrier with admitted data but no non-trivial relations or transitions is quiescent (${\longrightarrow}_0 = \varnothing$).
- **Active Obstructions:** Imposing distinction ($\operatorname{Impose}(a, b)$) triggers an active obstruction detector ($\operatorname{obstP}$) whenever an observation profile $q$ collapses them ($q(a) = q(b)$).
- **Rule 2 Forcing:** An unresolved obstruction forces carrier expansion, licensing minimal witnessed transitions.

### 2.2 Homotopy Type Theory (HoTT) Lens: Types, Paths, and Directions

In HoTT:
- **Types as Spaces:** A type is an $\infty$-groupoid. A single named glyph `a` does not automatically denote a contractible type; a type with one designated basepoint may possess non-trivial higher loops ($\pi_1(X, a) \neq 0$).
- **Identity Paths are Reversible:** In standard HoTT, every path $p : x = y$ has a canonical symmetric inverse $p^{-1} : y = x$, and reflexivity $\operatorname{refl}_x : x = x$ witnesses self-identity.
- **The Interval $\mathbb{I}$:** The standard interval has endpoints $0, 1$ and a path $\operatorname{seg} : 0 = 1$. Because $\mathbb{I}$ is contractible, it cannot directly model an irreflexive, irreversible relation between propositionally unequal points without directed type theory (dHoTT).
- **Directed HoTT:** In dHoTT, directed paths are not invertible; the arrow `<` serves as a primitive directed 1-cell.

### 2.3 Category Theory Lens: Objects, Morphisms, and Functors

In Category Theory:
- **0-Cells and 1-Cells:** Points are objects; directed relations are morphisms.
- **Free Categories:** A directed graph generates a free category only after identity morphisms $\operatorname{id}_v$ and associative composition are explicitly added. A directed cycle in a graph yields an endomorphism in the free category, which need not equal the identity.
- **Arrows and Duals:** Introducing a reverse arrow `>` does not automatically create an opposite category or isomorphisms unless an explicit contravariant functor or inverse law is declared.
- **Retractions vs. Adjunctions:** A retraction equation $r \circ \ell = \operatorname{id}$ on sets or categories does not constitute an adjunction or homotopy equivalence. An adjunction $F \dashv U$ requires:
  - Natural bijections $\operatorname{Hom}(F(A), B) \cong \operatorname{Hom}(A, U(B))$,
  - A unit natural transformation $\eta : \operatorname{Id} \Rightarrow UF$,
  - A counit natural transformation $\varepsilon : FU \Rightarrow \operatorname{Id}$,
  - Satisfaction of the triangle identities: $(U\varepsilon) \circ (\eta U) = \operatorname{id}_U$ and $(\varepsilon F) \circ (F\eta) = \operatorname{id}_F$.

---

## Part 3: Vocabulary Expansion: Conditional Capability & Proof of False Isomorphisms

Informal narratives often assert that a fixed keyboard sequence produces "unconditional jumps" at specific keys (e.g. keys 2, 28, and 37). Rigorous analysis reveals that capability changes are strictly conditional on declared formation and decoding rules.

### 3.1 Four Distinct Measures of Expressive Power

To avoid ambiguity, four distinct questions must be evaluated separately:
1. **New Spellings:** Cardinality and characters of terminal inventory $|\Sigma|$.
2. **New Accepted Syntax:** The formal language $L(G) \subseteq \Sigma^*$ generated by the grammar.
3. **New Decoded Structures:** The mathematical carrier (e.g. set, monoid, graph, category) produced by the semantic decoder.
4. **Changes to a Specified Invariant:** Modification of a concrete metric, invariant, or homology group.

Distinct indices must be maintained: alphabet size $k = |\Sigma|$, grammar profile $P$, Genesis stage $S(n)$, and homological degree $H_q$.

### 3.2 Capability Milestones Under Declared Rules

- **Level 1 ($\{a\}$):**
  - Without repetition: $L = \{a\}$ (a single isolated term).
  - With repetition allowed ($S ::= a \mid a S$): $L = \{a, aa, aaa, \dots\} = a^+$. A declared length decoder $\operatorname{dec}(w) = |w|$ supplies unary counting and models the positive integers $(\mathbb{Z}^+, +)$ with a single glyph!
- **Level 2 ($\{a, b\}$):**
  - Noncommutativity: The free monoid $\{a, b\}^*$ is non-abelian ($ab \neq ba$).
  - Binary Representation: Two glyphs can encode any binary numeral system; their printed shapes need not be `0` and `1`.
  - Identity by Occurrence: Multiple occurrences of a single glyph (`a...a`) can be distinguished by position or occurrence index without adding new letters.
- **Relational Encoding:**
  - A relation does not require an arrow symbol `<`. Relations can be encoded by juxtaposition ($ab$), explicit pairing ($[a, b]$), or an external table. Dedicated arrow glyphs provide specialized, readable syntax, not an ontological prerequisite for relations.

### 3.3 Theorem: Non-Isomorphism of Free Monoids on Different Generator Sets

Informal discussions sometimes claim that all multi-digit numeral systems are "isomorphic" as free monoids. We prove this is false:

$$\boxed{\{0, 1\}^* \not\cong \{0, \dots, 9\}^*}$$

**Proof:**
Let $M$ be a monoid with identity $e$. An element $x \in M \setminus \{e\}$ is called **indecomposable** if:
$$x = yz \implies y = e \text{ or } z = e.$$
In a free monoid $X^* = \operatorname{FreeMonoid}(X)$, the indecomposable elements are precisely the words of length 1—that is, the elements of the generating alphabet $X$.

Let $\phi : X^* \to Y^*$ be an isomorphism of monoids. An isomorphism maps the identity to the identity and preserves factorizations:
$$\phi(x) = \phi(y)\phi(z).$$
Consequently, $x$ is indecomposable in $X^*$ if and only if $\phi(x)$ is indecomposable in $Y^*$. Thus $\phi$ induces a bijection between the sets of indecomposable elements of $X^*$ and $Y^*$:
$$X \cong Y \implies |X| = |Y|.$$
For $\{0, 1\}^*$, the generating set has size 2. For $\{0, \dots, 9\}^*$, the generating set has size 10. Since $2 \neq 10$, no monoid isomorphism can exist. $\blacksquare$

> [!NOTE]
> **Numeral Decoders vs. String Monoids:**
> A binary numeral decoder $\operatorname{dec}_2 : \{0, 1\}^* \to \mathbb{N}$ and a decimal numeral decoder $\operatorname{dec}_{10} : \{0, \dots, 9\}^* \to \mathbb{N}$ can have the same semantic image ($\mathbb{N}$). This shared semantic target does not make their string monoids isomorphic. A fixed-width binary encoding of decimal digits defines an injective homomorphism $\{0, \dots, 9\}^* \hookrightarrow \{0, 1\}^*$, but this map is strictly not surjective.

### 3.4 Discrete Categories on Different Object Inventories

Similarly, discrete categories $\mathbf{C}_2$ (2 objects) and $\mathbf{C}_{26}$ (26 objects) are neither isomorphic nor equivalent:
- An isomorphism of categories requires a bijection on objects ($2 \neq 26$).
- An equivalence of categories requires an essentially surjective functor; since all morphisms in a discrete category are identities, isomorphism classes of objects are singletons, so equivalence also requires $|V_1| = |V_2|$.

### 3.5 Renaming Bijectivity and Identity Collapse

A terminal renaming map $\rho : \Sigma \to \Sigma'$ is invertible if and only if $\rho$ is a bijection. Replacing a letter `c` with an already-used letter `d` defines a non-injective map that collapses identities:
$$\rho(c) = d, \quad \rho(d) = d \implies \rho(ac) = \rho(ad) = ad.$$
Such a collapse destroys the retraction.

---

## Part 4: Syntactic Lift, Language Retraction, and the Homological Obstruction

Let $A \subseteq B$ be terminal alphabets. We analyze how formal languages and expressions lift and restrict.

### 4.1 Language-Level Retraction vs. Word-Level Homomorphisms

At the level of formal languages (sets of words), define the inclusion lift $\ell$ and restriction $r$:
$$\ell(L) = L \subseteq B^*, \qquad r(M) = M \cap A^*.$$
Then for any language $L \subseteq A^*$:
$$r(\ell(L)) = L \cap A^* = L.$$
This identity $r \circ \ell = \operatorname{id}_{\mathcal{P}(A^*)}$ is a **language-level retraction**.

- **Not a Word-Level Map:** The restriction $r$ acts on languages by filtering out words containing symbols in $B \setminus A$. It is *not* a total function $B^* \to A^*$ on individual words, because words containing new terminals have no preimage under an identity-preserving word map.
- **Erasure Homomorphism:** A total word map can be constructed via the projection homomorphism:
  $$h : B^* \to A^*, \qquad h(x) = \begin{cases} x & \text{if } x \in A, \\ \varepsilon & \text{if } x \in B \setminus A. \end{cases}$$
  This map is total, but it causes information loss: $h(a_1 b a_2) = a_1 a_2$, obliterating the position and presence of $b$.
- **What Retraction Means:** The identity $r\ell = \operatorname{id}$ confirms that prior expressions can be recovered. It does *not* imply that the larger system gained nothing: the complement $B^* \setminus A^*$ may support entirely new structures and languages.

### 4.2 Removal of the Unsupported Abelian Ext Calculation

Earlier informal notes attempted to construct a short exact sequence of formal languages and assert $\operatorname{Ext}(\mathsf{Lang}_N, \ker r_N) = 0$. This calculation is mathematically unsupported:
1. The collection of formal languages under set union and intersection does not form an abelian category (there are no additive inverses or abelian group structures on hom-sets).
2. Even in a valid abelian category, a split extension represents the zero extension class in $\operatorname{Ext}^1$; it does not imply that the entire bifunctor $\operatorname{Ext}^1(A, B)$ vanishes for all possible extensions.
We retain the verified language-level retraction $r\ell = \operatorname{id}$ and dispense with the unsupported Ext construction.

### 4.3 The Conditional Rent Rule: Six-Step Minimal Extension Protocol

Irreflexivity and diagonal avoidance ($R \cap \Delta = \varnothing$) are explicitly selected policy constraints; they are not mandatory axioms. Self-loops, repeated glyphs, and aliases remain valid in general syntax.

When an extension is claimed to be *necessary* or *minimal* under a declared constraint, the claim must satisfy the **Six-Step Proof Protocol**:
1. **State the Obligation:** Define the exact predicate $P$ that the current system fails to satisfy.
2. **Specify Admissible Internal Witnesses:** Define the set $W_{\text{int}}$ of candidate expressions within the existing alphabet and formation rules.
3. **Prove No Internal Witness Suffices:** Prove that $\forall w \in W_{\text{int}}, \neg P(w)$.
4. **Specify Admissible Extensions & Cost:** Define the class of allowed extensions $\mathcal{E}$ and a cost metric $\mu : \mathcal{E} \to \mathbb{R}$.
5. **Identify Minimizing Extensions:** Determine $\arg\min_{E \in \mathcal{E}} \mu(E)$, explicitly preserving tied minima.
6. **Prove the Selected Extension Satisfies the Obligation:** Verify that the chosen extension formally discharges $P$.

---

## Part 5: Graph Homology, Simplicial Complexes, and the Central Obstruction Theorem

We ground topological claims in finite simplicial and graph chain complexes.

### 5.1 Finite Graph Homology Model

Let $G = (V, E)$ be a declared finite directed graph with source map $s : E \to V$ and target map $t : E \to V$. The integral chain complex is:
$$C_1 = \mathbb{Z}^E \xrightarrow{\;\;\partial_1\;\;} C_0 = \mathbb{Z}^V \xrightarrow{\;\;\partial_0\;\;} 0,$$
where the boundary operator is defined on basis edges $e \in E$ by:
$$\partial_1(e) = t(e) - s(e).$$

- **Connected Components ($H_0$ and $\tilde{H}_0$):**
  If the underlying undirected graph of $G$ is nonempty and has $c$ connected components, then:
  $$H_0(G; \mathbb{Z}) \cong \mathbb{Z}^c, \qquad \tilde{H}_0(G; \mathbb{Z}) \cong \mathbb{Z}^{c-1}.$$
  The formula $\tilde{H}_0 \cong \mathbb{Z}^{|V|-1}$ holds when no edge joins distinct vertices; in the loop-free case this is equivalent to $E = \varnothing$. Self-loops do not change the component count.
- **Edge Addition and Observation:**
  Adding an edge $e$ from $a$ to $b$ sets $\partial_1(e) = b - a$, making $b - a$ a boundary. This reduces the rank of $\tilde{H}_0$ only when $a$ and $b$ previously belonged to different connected components. However, this algebraic boundary does *not* prove observational discrimination between $a$ and $b$. If an observation map satisfies $q(a) = q(b)$, adding an edge leaves that collision unchanged unless the observation mechanism itself is modified.
- **Algebraic Coefficients vs. Directed Reachability:**
  Ordinary integer homology does not encode directed reachability. A formal chain $-e$ has boundary $s(e) - t(e)$; this is an algebraic formal inverse, not physical permission to traverse a one-way edge backwards.
- **Self-Loops:**
  In a CW graph, a self-loop $e$ at vertex $v$ satisfies $\partial_1(e) = v - v = 0$. With one vertex and one loop, $\ker \partial_1 = \mathbb{Z}e$ and $C_2 = 0$, so $H_1 \cong \mathbb{Z}$. Whether a loop is degenerate depends on the chosen model.

---

### 5.2 The Central Obstruction Theorem

The precise mathematical obstruction governing vocabulary ascent and cycle filling is stated as follows:

$$\boxed{\textbf{Proposition.}\text{ An extension that kills a nonzero homology class cannot have a chain-map retraction preserving the original complex.}}$$

**Proof:**
Let $C = (C_\bullet, \partial^C)$ and $D = (D_\bullet, \partial^D)$ be chain complexes over $\mathbb{Z}$. Let:
$$i : C \to D \quad\text{and}\quad r : D \to C$$
be chain maps satisfying the retraction identity:
$$r \circ i = \operatorname{id}_C.$$
Since $r$ is a chain map, it satisfies the commutation relation:
$$r \circ \partial^D = \partial^C \circ r.$$

Suppose $z \in C_k$ is a cycle in $C$ ($\partial^C z = 0$) whose homology class is non-trivial:
$$[z] \neq 0 \in H_k(C).$$
Now suppose that in the extended complex $D$, the cycle $i(z)$ becomes a boundary (i.e. its homology class is killed):
$$i(z) = \partial^D b \quad\text{for some } b \in D_{k+1}.$$
Applying the retraction chain map $r$ to both sides yields:
$$z = \operatorname{id}_C(z) = (r \circ i)(z) = r(i(z)) = r(\partial^D b) = \partial^C(r(b)).$$
Because $r(b) \in C_{k+1}$, this shows that $z$ is a boundary in $C$, which implies:
$$[z] = 0 \in H_k(C).$$
This contradicts the hypothesis $[z] \neq 0$. Therefore, no such chain-map retraction $r$ can exist. $\blacksquare$

#### Smallest Concrete Example: Bridging Two Points

Consider the minimal complex of two isolated points:
$$C_0 = \mathbb{Z}a \oplus \mathbb{Z}b, \qquad C_1 = 0.$$
Here, $b - a$ is a cycle with non-trivial reduced homology class $[b - a] \neq 0 \in \tilde{H}_0(C)$.

Extend $C$ by adding an edge $e$ from $a$ to $b$:
$$D_0 = C_0 = \mathbb{Z}a \oplus \mathbb{Z}b, \qquad D_1 = \mathbb{Z}e, \qquad \partial^D_1(e) = b - a.$$
In $D$, the class $[b - a]$ is killed: $i(b - a) = \partial^D_1(e)$.

Suppose there exists a retraction chain map $r : D \to C$ fixing the original vertices ($r_0 = \operatorname{id}_{C_0}$). Since $C_1 = 0$, the map $r_1 : D_1 \to C_1$ must be the zero map ($r_1(e) = 0$). The chain map condition requires:
$$b - a = r_0(\partial^D_1 e) = \partial^C_1(r_1(e)) = \partial^C_1(0) = 0.$$
This requires $b - a = 0$ in $C_0$, which cannot hold because $a$ and $b$ are linearly independent basis elements.

> **Significance:** This theorem shows that killing a topological gap (in $\tilde{H}_0$) or filling a cycle (in $H_1$) is structurally incompatible with a chain-map retraction that fixes the original chain groups. Moving to a connected or filled space requires accepting that the original chain complex cannot be retracted without losing the boundary witness.

---

### 5.3 The Triangle Cycle: Derivation Without Conflation

Consider the inscription `a>b>c>a`. Under identity by label spelling, this decodes to three vertices $V = \{a, b, c\}$ and three directed edges $E = \{e_{ab}, e_{bc}, e_{ca}\}$:
$$\partial_1 e_{ab} = b - a, \qquad \partial_1 e_{bc} = c - b, \qquad \partial_1 e_{ca} = a - c.$$
Form the 1-chain:
$$z = e_{ab} + e_{bc} + e_{ca}.$$
Computing its boundary:
$$\partial_1 z = (b - a) + (c - b) + (a - c) = 0.$$
Thus $z \in \ker \partial_1 = Z_1$ is a 1-cycle. If $C_2 = 0$, every cycle is an integer multiple of $z$, yielding:
$$H_1(G; \mathbb{Z}) \cong \mathbb{Z} \cdot [z].$$

#### Adding a 2-Cell
If an external 2-cell $f$ is added with boundary $\partial_2 f = z$, we verify:
$$\partial_1(\partial_2 f) = \partial_1 z = 0.$$
In the extended complex $D$ with $D_2 = \mathbb{Z}f$, the cycle becomes a boundary, so $[z] = 0 \in H_1(D)$. The inscription `a>b>c>a` itself supplies only the 1-skeleton; it does *not* contain or supply the 2-cell $f$.

#### Chains vs. Cochains
We maintain a strict boundary between chains and cochains:
- **Chains:** $C_k$ are free abelian groups on simplices, with boundary maps $\partial_k : C_k \to C_{k-1}$.
- **Cochains:** $C^k = \operatorname{Hom}(C_k, \mathbb{Z})$ are functional groups, with coboundary maps $d^k : C^k \to C^{k+1}$ defined by:
  $$d^k(\phi) = \phi \circ \partial_{k+1}.$$
Filling a chain is a boundary equation ($\partial_2 f = z$); it must not be conflated with a coboundary equation ($d^1 \phi = \psi$).

#### Homology vs. Homotopy
Homological vanishing does not imply null-homotopy:
- In the wedge of two circles $S^1 \vee S^1$ (the figure-8 space with generators $x, y$), the commutator loop $[x, y] = xyx^{-1}y^{-1}$ maps to zero in the abelianized homology group $H_1 \cong \mathbb{Z}^2$.
- However, $[x, y]$ is non-trivial in the fundamental group $\pi_1(S^1 \vee S^1) \cong \mathbb{Z} * \mathbb{Z}$; it cannot be continuously shrunk to a point.
Homological calculations alone do not construct HoTT paths between paths.

---

## Part 6: The MSS-N Family Architecture: 22 Explicit Starts & Profile Readings

MSS-N is not a monolithic single-start grammar. It is a family of **22 explicit starts** defined in [`mssn.ebnf`](../../../../../../../omega_engine_education/documentation/003_minimal_symbol_system_n_mssn/grammar/mssn.ebnf) and **6 retained runtime profiles** governing production intake in [`check_grammars.py`](../../../../../../../omega_engine_education/documentation/030_the_symbol_game_proposal_fidelity_protocol_pfp/grammar/check_grammars.py).

### 6.1 The Creator Examples Across Four Profile Readings

MSS-N does not impose a mandatory outer enclosure `<...>` as an axiom. Both creator examples remain fully valid:
```text
a>b>c>a
a0>b2>c1>a0
```
Their syntactic acceptance and semantic decoding depend entirely on the selected grammar profile:

1. **In `raw_glyphs`:** Both expressions parse as valid unconstrained character sequences over $\Gamma_{38}$. They carry no inferred vertices, directed edges, weights, or annotations.
2. **In `label_path`:** Both expressions parse as paths between multi-character alphanumeric identifiers:
   - `a>b>c>a` connects vertices `a`, `b`, `c`, `a`.
   - `a0>b2>c1>a0` connects vertices `a0`, `b2`, `c1`, `a0`. Here `a0` is a single identifier atom, not an annotated pair.
3. **In `suffix_path`:**
   - `a0>b2>c1>a0` parses as a sequence of structured `suffix_vertex` tokens, where `a` is the label and `0` is the numeric annotation.
   - `a>b>c>a` **fails** in `suffix_path` because vertices lack the required digit suffix.
4. **In `glyph_path`:**
   - `a>b>c>a` parses as alternating single glyphs and directions.
   - `a0>b2>c1>a0` **fails** in `glyph_path` because `a` and `0` are adjacent vertex glyphs without an intervening direction separator.

> [!IMPORTANT]
> **Correction to DeepSeek:**
> Suffix binding is necessary for the *suffix annotation reading*, but is NOT required for the inscription `a0>b2>c1>a0` to be syntactically legitimate. Under `raw_glyphs` and `label_path`, `a0>b2>c1>a0` is already well-formed without suffix mechanics.

---

### 6.2 The 22 Explicit Starts of `mssn.ebnf`

| # | Start Symbol | EBNF Production | Canonical Input | Lexical & Structural Contract |
|---|---|---|---|---|
| **01** | `raw_glyphs` | `{ glyph \| "<" \| ">" }` | `a><b0<<` | Raw strings over $\Gamma_{38}$, including $\varepsilon$. No balancing required. |
| **02** | `word` | `glyph, { glyph }` | `alpha01` | Nonempty sequence over $\Sigma_{36}$. No delimiters. |
| **03** | `glyph_path` | `glyph, { direction, glyph }` | `a>b<c>a` | Alternating single glyphs and directions. |
| **04** | `label_path` | `word, { direction, word }` | `a0>b2>c1` | Directed paths between multi-glyph identifiers. |
| **05** | `suffix_path` | `suffix_vertex, { direction, suffix_vertex }` | `a0>b12<c3` | Vertex structured as `lower_latin` followed by `digits`. |
| **06** | `path_list` | `glyph_path, { ";", glyph_path }` | `a>b;c<d` | Semicolon-delimited sequence of independent paths. |
| **07** | `suffix_list` | `suffix_path, { ";", suffix_path }` | `a0>b1;c2<d3` | Semicolon-delimited sequence of suffix paths. |
| **08** | `scalar_path` | `scalar_vertex, { direction, scalar_vertex }` | `a:1.5>b:-2/3` | Paths with colon-separated scalar weights. `a:1/0` parses syntactically. |
| **09** | `vector_path` | `vector_vertex, { direction, vector_vertex }` | `a[1,2]>b[3,4]` | Bracketed vector-annotated vertices. |
| **10** | `edge_weight_path` | `lower_latin, { weighted_link, lower_latin }` | `a>2.5>b<1<c` | Arrow-flanked edge weights (`>w>` or `<w<`). Opposing marks (`>w<`) rejected. |
| **11** | `labelled_path` | `lower_latin, { "-", word, ">", lower_latin }` | `a-step>b` | Named relation links (`-label>`). |
| **12** | `prefix_tree` | `glyph \| direction, prefix_tree, prefix_tree` | `>ab` | Polish prefix notation for binary syntax trees. |
| **13** | `postfix_tree` | `glyph, { postfix_tree, direction }` | `ab>` | Reverse Polish notation for binary syntax trees. |
| **14** | `sequence` | `glyph, { ",", glyph }` | `a,b,c` | Comma-delimited list of single glyphs. |
| **15** | `nested_tree` | `glyph \| "(", [ nested_tree, { ",", nested_tree } ], ")"` | `(a,(b,c))` | Parenthesized nested trees. |
| **16** | `head_term` | `word, [ "(", [ head_term, { ",", head_term } ], ")" ]` | `f(x,g(y))` | Functional terms with head words and argument lists. |
| **17** | `incidence` | `incidence_item, { ";", incidence_item }` | `[a,b]>[c,d]` | Hypergraph directed incidence lists. |
| **18** | `unicode_path` | `unicode_glyph, { unicode_direction, unicode_glyph }` | `α→β←γ` | Directed paths over Greek/symbolic Unicode alphabets. |
| **19** | `arrow_path` | `glyph, { unicode_direction, glyph }` | `a→b←c` | ASCII glyphs joined by Unicode arrows (`→`, `←`). |
| **20** | `bitstream` | `bit, { bit }` | `10011010` | Nonempty binary digit strings (`0` and `1`). |
| **21** | `octets` | `hex_digit, hex_digit, { hex_digit, hex_digit }` | `deadbeef` | Lowercase hexadecimal byte strings (even length required). |
| **22** | `rewrite_rule` | `{ glyph }, "=>", { glyph }` | `a=>b` | String rewrite rules with optional empty sides. |

---

### 6.3 Syntax Checks vs. Decoder Checks

Side conditions must be categorized by the formal mechanism that evaluates them:
- **Regular Lexical Restrictions:** Excluding zero denominators can be enforced lexically at the grammar level:
  $$\text{NonzeroDenominator} ::= [1-9][0-9]^*$$
- **Context-Free Restrictions:** Matching opening and closing parentheses, or equal unary lengths ($a^n b^n$), are context-free.
- **Semantic Decoder Obligations:** Verifying that a graph is acyclic, that edge weights satisfy triangle inequalities, or that variable names are bound in an environment are semantic evaluation obligations evaluated by external checkers, not syntax checkers.

---

### 6.4 Implementation Reality: Parsers vs. Recognizers

The repository maintains an explicit inventory:
- **28 Total Registered Profiles:** Comprises 6 retained profiles in production plus 22 new starts in `mssn.ebnf`.
- **Runtime Parser Execution:** The existing runtime engine exercises three specific application parsers:
  1. `parse_boundary` in `rewrite.py` (`mss-boundary-v1`),
  2. The historical operational packet parser (`historical-packet-v1`),
  3. The K0 cycle repair transcoder (`pkt00-k0-v1`).
- **Recognizers vs. Round-Trip Parsers:** Grammar recognition fixtures in `conformance_cases.json` and `mssn_conformance_cases.json` test language membership; they are distinct from AST-reconstructing production parsers.
- **Resource Limits:** Budget ceilings (64 KB input, 4,096 nodes, 32 recursion levels) apply to the boundary parser; they do not automatically govern external profiles. Whitespace rejection is strict: `1>2` parses in `glyph_path`, whereas `1 > 2` is rejected due to undeclared space characters.

---

## Part 7: Manipulation Laws, Inverses, and Collisions

Transformations over glyph sequences must declare their exact domain, result, retained information, and inverse conditions.

### 7.1 Collisions Under Non-Injective Encodings

Consider the non-prefix binary code:
$$a \mapsto 0, \qquad b \mapsto 00.$$
The valid collision examples over this alphabet are:
$$\begin{aligned}
aa &\mapsto 00, &\quad b &\mapsto 00 &\quad\text{(Collision on output } 00\text{)} \\
ab &\mapsto 000, &\quad ba &\mapsto 000 &\quad\text{(Collision on output } 000\text{)}
\end{aligned}$$
*(Note: A string like `b0` is undefined unless `0` is explicitly included in the source alphabet).*

### 7.2 Inversion and Traversal of Directed Edges

Let `>` denote a directed edge pointing from the preceding vertex to the following vertex ($s \to t$), and `<` denote an edge pointing from following to preceding ($t \leftarrow s$).

Applying elementary syntactic manipulations to the inscription `a>b` yields:

| Manipulation | Result | Directed Edge Represented | Orientation Relative to Original |
|---|:---:|:---:|:---:|
| **Original Inscription** | `a>b` | $a \to b$ | Baseline |
| **Reverse Traversal Only** | `b>a` | $b \to a$ | **Reversed** |
| **Invert Direction Only** | `a<b` | $b \to a$ | **Reversed** |
| **Reverse Traversal & Invert Direction** | `b<a` | $a \to b$ | **Preserved** |

For multi-edge paths (e.g. `a>b>c`):
- Reversing traversal order and inverting all arrows yields `c<b<a`.
- This operation preserves the underlying directed edge multiset while reversing the linear sequence of traversal.
- Preservation of vertex occurrence order, annotations, and multiplicities must be evaluated independently.

---

## Part 8: Epistemic Architecture: Ascent Engine, Proposer-Host Oracle, and Dual Accounting

To complete the foundational architecture of MSS-N, we formalize the operational and epistemic mechanics governing how presentations are verified, repaired, and lifted across levels.

### 8.1 Three Distinct Ontological Objects

The architecture strictly distinguishes three separate objects across documentation, tests, and runtime:

| Object | Origin | What Numbering Means | Can its Next Stage be "Derived"? |
|---|---|---|---|
| **Genesis $S(n)$** | Blind/internal 19L57G1 derivation | Actual provenance-bearing derivation stage | Only if Genesis itself forces and licenses it |
| **MSS-N** | Externally designed research/verification atlas | Numbered specification row and capability target | Only if a separate MSS lift record certifies the transition |
| **Symbol Game (PFP)** | Host/proposer verification protocol | Runtime and evaluation machinery | No; it verifies candidate claims on declared carriers |

> [!IMPORTANT]
> **The Index Non-Identity Invariant:**
> The atlas row index does not equal the Genesis derivation index:
> $$\boxed{\mathrm{MSS}\text{-}2 \neq S(2)}$$
> Genesis $S(2)$ consists of retained inscriptions under observational collapse without directed cuts, whereas $\mathrm{MSS}\text{-}2$ specifies directed and obstructed relations (crosswalking post-hoc to Genesis $S(3)$).

### 8.2 The Ascent Triad: Declared Successor vs. Candidate Lift vs. Licensed Lift

To prevent semantic inflation, vocabulary ascent is governed by a strict tripartite distinction:

$$\boxed{\text{declared successor} \neq \text{candidate lift} \neq \text{licensed lift}}$$

1. **Declared Successor:** A stated research obligation in a curriculum or specification row. It defines an evaluation target, not evidence that the obligation has been met.
2. **Candidate Lift:** A proposed pair of extension maps accompanied by candidate repair witnesses submitted to an evaluator.
3. **Licensed Lift:** A transition whose local repairs have been formally exhausted, whose extension class is minimized, whose retraction is verified, and whose host replay passes.

### 8.3 Dual Accounting: Specification Coverage vs. Machine-Checked Depth

Evaluation enforces strict dual accounting:
- **Specification Coverage $C(N)$:** Counts how many rows at or below $N$ possess specified carriers, positive fixtures, negative fixtures, and local host checkers.
- **Licensed Depth $D(k)$:** The length of a contiguous chain of licensed lift records from the declared seed.

Having an atlas of 100 rows provides $C(100)$ coverage; it does not demonstrate that row 0 generated row 100 or that all intermediate transitions are licensed.

### 8.4 Proposer-Host Runtime Oracle Architecture

The Symbol Game operates as an external, deterministic oracle and validator stack evaluating candidate proposal streams:

```
[Candidate Proposal Stream]
       │
       ▼
 [PacketParser] ──────── (Syntax Error) ─────────► [Refusal: Syntax Malformed]
       │
       ▼
[LocalValidator] ─────── (Constraint Defect) ───► [Repair: Defect Cochain x]
       │                                                    │
       ▼                                                    ▼
[BoundaryValidator] ──── (Boundary Violation) ──► [ℓ¹ Exact Repair LP (Φ₁)]
       │                                                    │
       ▼                                                    ▼
 [Terminalizer] ◄────────────────────────────── [Sparse Landing r*]
       │
       ├─► Certificate: Valid & Clean Replay Witness
       ├─► Refusal: Typed Refusal (Explicit Non-admissibility)
       ├─► Repair: Sparse Landing Repair Vector (Excess Mass = 0)
       └─► OracleNeeded: External Solver / Decision Procedure Required
```

Every evaluation over presentation $P_N$ terminates in one of four mutually exclusive states:
1. **Saturation:** All local constraints satisfied; zero defect cochain.
2. **Blocked Extension:** Search exhausted without a viable extension candidate.
3. **Budget Stop:** Computational resource bound reached; status is returned as typed `UNKNOWN` (non-exhaustion).
4. **Licensed Finite Lift:** An auditable up-lift to $P_{N+1}$ with verified retraction.

### 8.5 The Repair-Before-Ascent Protocol (The Workshop Analogy)

Before any level ascent is licensed:
1. **Exhaust Allowed Repairs:** Within declared computational budget, apply all permitted local repairs on the current presentation carrier.
2. **Obstruction vs. Search Defect:** If a defect survives, determine whether it represents an unresolvable obstruction or an incomplete search under finite budget. A budget stop returns typed `UNKNOWN`, never proof of obstruction or exhaustion.
3. **Enumerate Extension Class:** Only upon witnessed obstruction is an extension class enumerated.
4. **Retain Tied Minima:** Equally cheap, non-equivalent candidate solutions are preserved under declared selection metrics.

### 8.6 Historical Codecs and Visual Shorthands

- **Historical Rational Representation:** Uses binary payloads under prefix opcodes. Under that codec, `op<<10010><1><11><10>>` represents the rational number $-3/2$. Decimal `-3/2` is not a primitive boundary atom.
- **Visual Shorthand Compilation:** In early notes, infix notation was used before boundary grammar was mechanized:
  - `a > b` compiles to atom $\langle ab \rangle$.
  - `a <>> b` (walk interrupted by the void $\langle\rangle$) compiles to obstructed cut $\langle\langle ab \rangle\langle\rangle\rangle$.

---

## Part 9: Summary & Authoritative Monograph Claim

We conclude by stating the authoritative foundation of the MSS-N framework:

> **Core Monograph Finding:**
> MSS-N admits families of finite glyph presentations whose structure depends on declared formation, identity, decoding, and manipulation rules. Alphabet extension can preserve old inscriptions while adding new possibilities. Structural preservation and obstruction removal require separate proofs; an extension that kills a nonzero homology class cannot simultaneously retract the original chain complex by a chain map fixing it.

---

### Claim Hygiene Assessment

1. **What it supports:** This monograph demonstrates in this formal model how finite glyph alphabets expand under declared grammar profiles, establishes the non-isomorphism of free monoids on different generator sets ($\{0,1\}^* \not\cong \{0,\dots,9\}^*$), and derives the homological retraction obstruction proposition for complexes killing non-zero classes.
2. **What it does not support:** It does not demonstrate empirical properties of natural languages, neural representations, or unverified downstream dialects; nor does it claim that formal syntax validation replaces semantic domain verification.
3. **The narrowest defensible claim:** Expressive power and homological invariants depend strictly on declared formation, decoding, and boundary rules; language-level retraction $r\ell = \operatorname{id}$ holds for terminal inclusions, but killing a non-zero homology class precludes a chain-map retraction fixing the original complex.
4. **Next test needed:** Execute `check_mssn.py` and `check_grammars.py --runtime` against extended conformance suites to verify multi-profile parse boundaries and refusal semantics across all 22 declared start symbols.
