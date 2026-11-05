## 2026-10-08 — Graph qualifications

Qualified the edge-addition H0 claim and allowed self-loops in the maximal-component formula. The central chain-retraction theorem is unchanged.

# Change Log for Minimal Symbol System - N (MSS-N) Foundational Monograph Package

AuthorityEffect: None. GenesisEffect: None.

## [0.2.0] - 2026-10-05

### Substantive Mathematical Amendments (Codex Sol6.1 Review)
- **Separation of Declared Data:** Explicitly separated terminal spellings, tokenization policy, grammar, public start, layout policy, identity policy, annotation decoding, and manipulation rules.
- **De-overloaded Relation Symbols:** Replaced the conflated symbol $R$ with distinct mathematical relations: encoded graph relation $E \subseteq V \times V$, string rewrite relation $ o_{\text{rewrite}}$, and observation map $q: V \to O$.
- **Conditional Capability Results:** Replaced unconditional keyboard ladder assumptions with conditional results: 1 glyph with repetition yields unary counting via length decoders; 2 glyphs introduce noncommutativity ($ab\neq ba$) and binary encoding; relations do not strictly require arrow glyphs.
- **Proof of Free Monoid Non-Isomorphism:** Disproved the false isomorphism $\{0,1\}^* \cong \{0,\dots,9\}^*$ with a rigorous proof via indecomposable elements (generators), and proved discrete categories $\mathbf{C}_2$ and $\mathbf{C}_{26}$ are neither isomorphic nor equivalent.
- **Absence vs. Empty Word:** Formalized four distinct states: absent input (typed `None`), empty word $\varepsilon$, literal boundary ground $\langle\rangle$, and declared ground carrier. Corrected meta-grammar to explicitly typed metalanguage options.
- **Language Retraction vs. Word Maps:** Rigorously typed the language-level retraction $r\ell = \operatorname{id}$ on $\mathcal{P}(A^*)$, distinguished it from word-level maps, defined the total erasure homomorphism $h: B^* \to A^*$, and removed the unsupported abelian short exact sequence and $\operatorname{Ext}$ calculation.
- **Graph Homology Corrections:** Corrected $H_0 \cong \mathbb{Z}^c$ and $\tilde{H}_0 \cong \mathbb{Z}^{c-1}$ for $c$ connected components, noted that adding an edge does not prove observational discrimination ($q(a) = q(b)$ unchanged), and clarified that ordinary graph homology does not encode directed reachability.
- **Central Homological Obstruction Theorem:** Proved the fundamental proposition that an extension killing a non-zero homology class cannot admit a chain-map retraction fixing the original complex, demonstrated on the minimal 2-point, 1-edge complex and cycle filling.
- **Chains vs. Cochains in Triangle Cycle:** Derived `a>b>c>a` 1-cycle $z$ without conflating homology with cohomology, keeping chain boundaries $\partial_k$ distinct from cochain coboundaries $d^k$, and distinguishing homological vanishing from homotopy path contraction.
- **Creator Examples Across Four Profiles:** Formalized `a>b>c>a` and `a0>b2>c1>a0` across four profile readings (`raw_glyphs`, `label_path`, `suffix_path`, `glyph_path`), correcting DeepSeek's claim regarding suffix necessity.
- **Explicit Manipulation Collisions & Traversal Inversions:** Documented valid collisions under non-injective codes ($aa \mapsto 00, b \mapsto 00$ and $ab \mapsto 000, ba \mapsto 000$) and tabulated the 3 elementary transformations of `a>b` and multi-edge paths.
- **Mode 01 & Implementation Reality:** Clarified that Tier H and Tier D use extended alphabets beyond $\Gamma_{38}$, distinguished AST recovery from exact source-byte recovery in codebooks/legends, phrased the prose restriction operationally, and added `check_mssn.py` and `mssn_conformance_cases.json`.
- **Authoritative Monograph Claim:** Replaced the monograph's concluding claim with Codex Sol6.1's exact formulation on structural preservation and homological retraction obstructions.

## [0.1.0] - 2026-10-05

### Added
- Integrated Part 9 on Epistemic Architecture into `paper.md`, absorbing all operational mechanics from `0_mssn.md` and `mssn_ebnf_grammar.md`: the Ascent Triad (declared successor vs. candidate lift vs. licensed lift), dual accounting (coverage $C(N)$ vs. licensed depth $D(k)$), the Proposer-Host Oracle pipeline and terminal states, the Repair-Before-Ascent protocol, and historical binary rational codecs.
- Initial canonical deposit package for *Minimal Symbol System - N (MSS-N): Conservative Grammar Growth, Simplicial Cycle Repair, and Obstruction Cohomology* as a v0.1 Pre-Print monograph (`paper.md`).
- Exhaustive documentation of the production grammar architecture: the 22 formal starts of `mssn.ebnf` and the 6 runtime profiles of `check_grammars.py`.
- Formulated the Rent Rule (diagonal avoidance $R \cap \Delta = \varnothing$ and irreflexivity) and the split extension retraction invariant ($r_N \circ \ell_N = \operatorname{id}$).
- Algebraic topology of simplicial cycle repair in the pinned $K_0$ complex (4 vertices, 5 edges, 1 face) under boundary operators $d_1$ and $d_2$, external repair $d_{2,\text{ext}}$, and exact solver receipts `qed<exact>`.
- Articulation of the Syntactic Firewall Invariant ($\text{Parse}
eq \text{Model}$).
