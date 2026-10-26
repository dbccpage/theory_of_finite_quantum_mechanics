---
documentation_contract: education-documentation/v1
title: "Finite alphabet growth, word encodings, and countable unions"
kind: grammar-reference
status: active
maturity: research
atlas_status: specified
source_provenance: external_mss_atlas
authority_effect: "None"
genesis_effect: "None"
---

# Finite alphabet growth, word encodings, and countable unions

The 38-glyph inventory is a chosen presentation alphabet:

\[
\Gamma_{38}=\{a,\ldots,z,0,\ldots,9,<,>\}.
\]

The [grammar](../grammar/mssn.ebnf) declares how its marks may be combined.
The alphabet index counts available glyphs; a Genesis stage records admitted
structure; an MSS row names a proposed capability. These indices are independent.
The active mathematical account is [From Pre-Genesis to MSS-N](/atlas/papers/finite_obstruction_calculus/pregenesis_to_minimal_symbol_systems/paper.md).

This note replaces the former claims that particular alphabet keys force
relations, counting, homology or transfinite reflection. The useful construction
is explicit: specify an alphabet, then a grammar, then its interpretation and
preservation obligations. A parser can check the first two without deciding the
last two.

## 1. From the supplied inscription to a chosen alphabet

In the canonical Genesis primitive reading, supplying `<>` records an inscription
without admitting a datum, a relation, a form, or an instance. A later datum
admission is a separate event. The literal spelling does not itself provide an
empty set, a point space, a terminal category, or an empty word.

Once a finite alphabet \(\Sigma\) has been declared, the mathematical presentation
\(\Sigma^*\) is the free monoid of finite words, with concatenation and empty word
\(\varepsilon\). This is an explicit mathematical construction over the admitted
alphabet. It does not identify pre-genesis with the empty set or claim that an
unadmitted ambient container belongs to the object language.

For the public start `raw_glyphs`, both angle marks are ordinary glyphs and the
empty word is allowed. Thus `<>`, `><`, and `<<<` all parse there. The separate
boundary-packet grammar has different rules. The chosen public start matters.

## 2. What changes when one glyph is added

Fix the display order `a` through `z`, then `0` through `9`, then `<`, `>`.
Let \(\Sigma_k\) contain the first \(k\) glyphs. This order is a convention:

| Alphabet index | Inventory change | Additional declaration needed for the suggested use |
| --- | --- | --- |
| 0 | No glyphs | A word grammar still contains its chosen empty word. |
| 1–26 | Latin glyphs | A datum interpretation must distinguish glyph spelling from admitted identity. |
| 27–36 | Digit glyphs | Numeral value needs a base, concatenation syntax and a decoder. |
| 37–38 | Angle glyphs | Direction, enclosure and reversal are separate interpretations. |

For every \(k\), inclusion \(\Sigma_k\hookrightarrow\Sigma_{k+1}\) extends
letterwise to an injective monoid homomorphism
\(u_k:\Sigma_k^*\hookrightarrow\Sigma_{k+1}^*\).
A partial decoder that copies old words and returns `NON_DESCENT` on a word
containing the new glyph satisfies \(r_k(u_k(w))=w\). This proves preservation
of old words. Preserving a protected answer requires, in addition, a compatible
interpretation of those words.

Admitting a second glyph does not force a protected-pair demand. Declaring
concatenation over one glyph already gives infinitely many finite words
\(\varepsilon,a,aa,\ldots\); the 28th inventory entry is not the origin of
counting. A decimal digit is not a number until a decoder is specified.

## 3. Free monoids of different finite ranks are not isomorphic

**Proposition.** If finite alphabets \(A\) and \(B\) have different cardinalities,
then \(A^*\) and \(B^*\) are not isomorphic as monoids.

**Proof.** The nonidentity elements that cannot be written as a product of two
nonidentity elements are exactly the one-letter words. A monoid isomorphism
preserves the identity and this property, so it restricts to a bijection
\(A\to B\). Different cardinalities exclude such a bijection. \(\square\)

Consequently \(\{0,1\}^*\not\cong\{0,\ldots,9\}^*\) as monoids.
Both underlying word sets are countably infinite, so they admit a set bijection;
that is a weaker assertion. Converting `111111` in base two to `63` in base ten
preserves a numeric value, not concatenation: the image of `1` concatenated with
itself is `11`, whereas the numeric conversion of binary `11` is decimal `3`.

Similarly, discrete categories with \(k\) and \(k+1\) objects are not equivalent:
an equivalence of discrete categories is a bijection on objects. Replacing names
on a fixed carrier is different from adjoining an object.

## 4. A correct encoding of countably many generators

**Proposition.** For a declared countable alphabet
\(A=\{x_0,x_1,\ldots\}\), the code

\[
c(x_k)=1^k0
\]

extends by concatenation to an injective monoid homomorphism
\(C:A^*\to\{0,1\}^*\). Its image is the empty word together with binary words
ending in `0`, and its inverse on that image is explicit.

**Proof.** Each codeword consists of a run of ones terminated by a zero. No
codeword is a proper prefix of another. Split an encoded word after each zero;
the length of each preceding run of ones gives exactly one index \(k\). This
recovers every input word and proves injectivity. Splitting a concatenation
recovers the concatenation of the decoded lists. Every nonempty binary word
ending in zero has precisely this decomposition. \(\square\)

Words ending in `1` are outside the image and the partial decoder must refuse
them. Plain binary representations of integers are not prefix-free: for example
`1` prefixes `10`. Adding an undeclared separator `#` would change the target
alphabet. The unary-terminated code above avoids both errors.

For a question \(q:A^*\to Q\), define \(\widehat q=q\circ C^{-1}\) on the
image. Then \(\widehat q(C(w))=q(w)\). An executable checker still requires an
explicit representation of the question and its implementation. This is
question preservation by decoding, not an unrestricted theorem of logical
conservativity, computational efficiency, or equality of grammar classes.

## 5. Retractions can erase distinctions

The [extended codec](../code/mssn_extended_codec.py) fixes every old
\(\Gamma_{38}\)-word and substitutes old words for 62 new glyphs. It satisfies
\(r\circ u=\mathrm{id}\) on the old language. It is not injective on the new one:

\[
r(\texttt{α})=\texttt{alpha}=r(\texttt{alpha}).
\]

An observer receiving only this result cannot answer whether the original
contained the Greek glyph. This is the WDP report-fiber criterion: a protected
question descends exactly when it is constant on the report's fibers. Use the
prefix-free construction above when the new glyph distinctions must survive.

The ideal information per uniformly distributed glyph is \(\log_2|\Sigma|\).
The ratio \(\log_2(100)/\log_2(38)\approx1.266\) compares ideal symbol counts
for equal information. It is not measured compression. The corresponding ideal
reduction is \(1-\log_2(38)/\log_2(100)\approx21\%\), not 26.6%; UTF-8 byte
lengths and the nonuniform source distribution require separate accounting.

## 6. Countable unions and mathematical interpretations

For a nested family of alphabets \(\Sigma_0\subseteq\Sigma_1\subseteq\cdots\),

\[
\left(\bigcup_{k<\omega}\Sigma_k\right)^*
=\bigcup_{k<\omega}\Sigma_k^*.
\]

Every word uses finitely many glyphs, all contained in some finite stage; this
proves the nontrivial inclusion. The equality concerns finite words over a
countable alphabet. It does not admit infinite words, prove an ordinal notation
system, or select a reflection principle at \(\omega+1\).

If an explicitly chosen realization interprets \(k>0\) distinct admitted data
as a discrete space, then \(\widetilde H_0\cong\mathbb Z^{k-1}\). Admitting an
edge between two components reduces their component count by one. If instead
it joins vertices in the same component, the component count is unchanged and
a graph cycle is created. Attaching a two-cell along a cycle is a further
operation. These are useful mathematical constructions once the realization
and allowed operations have been declared; none follows merely from adding an
angle mark to the alphabet.

## 7. Current executable scope

[`check_mssn.py`](../code/check_mssn.py) replays 39 grammar cases over 22 starts.
[`mssn_codec.py`](../code/mssn_codec.py) implements those starts, including raw
glyphs and the explicitly enumerated Unicode tokens. Targeted codec tests compare
accepted and refused strings with the grammar and exercise the extended
retraction. They do not mechanize every proposition in this note.

The [Lean inventory](../lean4/README.md) distinguishes syntax sketches, supplied
fixture checks and actual algebraic theorems. The executable construction from
the canonical primitive history is described in the
[WDP Genesis construction supplement](/atlas/papers/finite_obstruction_calculus/witnessed_difference_programme/docs/derivations/genesis_construction.md).
