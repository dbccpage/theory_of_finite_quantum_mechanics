# Curriculum: 010 MSS-N

**AuthorityEffect:** None.

Eight lessons, about five hours of study including the video. MSS-N is an
externally designed atlas of glyph grammars and declared verification targets.
It is a side branch, not the next Genesis stage: "MSS-2 ≠ S(2)". The checkable
core is one grammar file, a codec, and a short paper whose proofs you can do by
hand. The 101-level atlas around it is a list of targets, not of results.

**Prerequisite:** [`002_s_n`](../002_s_n/curriculum.md).
**Main reading:** [From Pre-Genesis to MSS-N](../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md),
[`grammar/mssn.ebnf`](grammar/mssn.ebnf), [`reading_guide.md`](reading_guide.md),
and the [publication review](publication_review.md).

---

## Lesson 1. An atlas, not a derivation

**After this lesson you can** say what MSS-N is, and separate coverage from depth.

- The README calls MSS-N "an externally designed atlas of finite representations
  and verifier obligations", "not constrained to blind derivation".
- Every atlas row is a specification target, not evidence that the target was met.
- Coverage C(N) counts specified rows; depth D(k) is the length of a chain of
  licensed lift records. "Having an atlas of 100 rows provides C(100) coverage; it
  does not demonstrate that row 0 generated row 100." No licensed lift exists, so
  D = 0.
- A declared successor is a research obligation; a candidate lift is a proposed pair
  of maps with repair witnesses; a licensed lift has exhausted repairs, a minimised
  extension, a verified retraction and a passing host replay.

**Exercise.** The canonical tower grades levels 0, 1, 23, 35, 36 and 48 COMPUTED.
Does that give depth 6? *Answer:* no. The grades are shape checks assigned by level
membership; depth counts licensed lifts, of which there are none.

## Lesson 2. The alphabet and the eight things to declare

**After this lesson you can** name the alphabet and the eight dimensions every model
must declare.

- Γ38: 26 lowercase letters, 10 digits, and the two marks `<` and `>`. The grammar's
  `word` uses Σ36, the letters and digits.
- Declare separately: terminal spellings, tokenization, grammar, public start,
  layout, identity policy, annotation decoding, and manipulation rules.
- Keep apart three relations that share notation: an encoded relation E ⊆ V × V, a
  rewrite relation, and an observation map q : V → O.

**Exercise.** Why does `<` need to be named in the alphabet when `raw_glyphs` treats
it as an ordinary mark? *Answer:* because balanced pairing is not an axiom there;
it is a glyph until a grammar gives it a role.

## Lesson 3. One string, many readings

**After this lesson you can** parse a string under several public starts and explain
why there is no default.

| Text | `raw_glyphs` | `label_path` | `suffix_path` | `glyph_path` |
| --- | --- | --- | --- | --- |
| `a>b>c>a` | accept | accept | refuse | accept |
| `a0>b2>c1>a0` | accept | accept | accept | refuse |

- `label_path` reads `a0` as one identifier; `suffix_path` as label `a` with
  annotation `0`; `glyph_path` as two adjacent vertices with no direction, so it
  refuses the second string.
- Run `py -3.12 omega_engine_education/documentation/003_minimal_symbol_system_n_mssn/code/check_mssn.py`:
  39 cases over 22 starts.

**Exercise.** Why does `suffix_path` refuse `a>b>c>a`? *Answer:* its vertices must
carry a digit annotation.

## Lesson 4. Syntax is not decoding

**After this lesson you can** say which side conditions a grammar can enforce.

- `a:1/0` parses in `scalar_path`; division by zero is a later numeric refusal.
- Zero denominators can be excluded lexically, bracket matching is context-free, and
  acyclicity or triangle inequalities are semantic obligations.
- `a>2<b` is refused in `edge_weight_path`: both marks on a step must agree.

**Exercise.** Classify "every denominator is non-zero", "brackets balance", "the graph
has no cycle". *Answer:* lexical (if written that way), context-free, semantic.

## Lesson 5. More keys do not give more meaning

**After this lesson you can** prove that free monoids on 2 and 10 generators are not
isomorphic, and test a renaming.

- Capability changes need declared formation and decoding rules. One glyph with
  repetition gives a⁺, and with the decoder dec(w) = |w| it models (ℤ⁺, +). Two glyphs
  give a non-commutative free monoid, ab ≠ ba.
- $\{0,1\}^{\ast}\not\cong\{0,\ldots,9\}^{\ast}$: in a free monoid the indecomposable elements are exactly the
  generators, an isomorphism preserves them, and 2 ≠ 10. A fixed-width binary code
  embeds one into the other, but not onto.
- A renaming ρ : Σ → Σ′ is invertible if and only if it is a bijection. ρ(c) = d,
  ρ(d) = d sends `ac` and `ad` to `ad`. The code a ↦ 0, b ↦ 00 sends `aa` and `b` to `00`.

**Exercise.** Find another collision for a ↦ 0, b ↦ 00. *Answer:* `ab` and `ba` both
give `000`.

## Lesson 6. Retraction at the level of languages

**After this lesson you can** distinguish a language-level retraction from erasure and
state the old-image law.

- For A ⊆ B, ℓ(L) = L and r(M) = M ∩ $A^{\ast}$, so r(ℓ(L)) = L. This is about languages, not
  words. Erasure h : $B^{\ast}$ → $A^{\ast}$ loses information: h(a₁ b a₂) = a₁ a₂.
- "The identity rℓ = id confirms that prior expressions can be recovered. It does not
  imply that the larger system gained nothing."
- Old-image law with typed refusal: r(u(x)) = x and r(z) = NON_DESCENT for a new z.
  That does not give an inverse on z, or permission to add z. Write r_N, not d_N.

**Exercise.** Why is r(M) = M ∩ $A^{\ast}$ not a word map? *Answer:* it discards words outside
$A^{\ast}$ rather than sending each word somewhere.

## Lesson 7. Cycles, boundaries, and filling a hole

**After this lesson you can** compute the triangle cycle and prove that filling it
blocks a chain-map retraction.

- ∂₁(e) = t(e) − s(e). For `a>b>c>a`, z = e_ab + e_bc + e_ca and
  ∂₁z = (b − a) + (c − b) + (a − c) = 0. With no 2-cells, H₁ ≅ ℤ·[z].
- The inscription supplies only the 1-skeleton; it does not supply a 2-cell f with
  ∂₂f = z. Homology is not reachability, and vanishing homology is not
  null-homotopy.
- **Proposition.** An extension that kills a nonzero class cannot have a chain-map
  retraction fixing the original complex. Proof: if r∘i = id and i(z) = ∂b, then
  z = r(∂b) = ∂(r b), so [z] = 0.
- Smallest example: two points a, b with no edges, so [b − a] ≠ 0 in reduced H₀; add
  an edge e with ∂e = b − a. Any chain map fixing C₀ has r₁ = 0 (C₁ was 0), forcing
  b − a = 0, a contradiction.

**Exercise.** Add a second edge parallel to an existing one in a connected graph. Is
there a retraction? *Answer:* yes: no class is killed, and the new edge can map to
the old one.

## Lesson 8. Three packet languages, and what the tower checks

**After this lesson you can** tell the three packet grammars apart and read a tower
stage check honestly.

| Input | boundary | tower wire | `glyph_path` |
| --- | --- | --- | --- |
| `<>` | accept | accept | refuse |
| `<ab>` | accept | accept (atom `ab`) | refuse |
| `<<ab><>>` | accept | refuse | refuse |
| `op<<10010><1><11><10>>` | refuse | accept (−3/2) | refuse |
| `a>b>c>a` | refuse | refuse | accept |

- `<ab>` is an atom whose word is `ab` in both packet grammars; reading it as an edge
  from a to b is a declared decoder.
- The tower's stage checks return `STRUCTURAL_ONLY`, never mathematical
  certification. MSS-0 admits only `<>`; MSS-1 refuses `<a>` and accepts `<01>`.
- PFP keeps MSS-N as a separate object from the protocol. A packet is checked by the
  host; it does not certify itself.

**Exercise.** The tower decodes `op<<10010><1><11><10>>` to −3/2. What do the four
atoms mean? *Answer:* opcode 10010, then sign, numerator 11 (three) and denominator
10 (two) in binary; the sign atom 1 gives the minus.

---

## What this strand does not claim

- That MSS levels are Genesis stages, or that the atlas is verified, sealed or
  computed as a whole.
- That `Evaluator::*` names or `ERR_*` codes in the level tables are running software.
- That `MssnSyntax.lean` proves parser correspondence: it contains unrestricted
  syntax sketches. Other Lean files contain the scoped algebraic results listed
  in [the Lean inventory](lean4/README.md). The codec now refuses non-ASCII digits
  and undeclared Unicode tokens; finite differential tests are not an all-input proof.
- That compiling syntax or fixture modules mechanizes every theorem in the combined paper.
- That MSS-N has zero opcodes, or that its four-state terminal sets are the canonical
  routing terminals.
- Anything physical on the strength of the domain Lean files or tests.
