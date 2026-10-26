# MSS-N and Mode 01: long-horizon mathematical derivation prompt

You are a mathematical researcher with enough execution time to derive, challenge,
formalize and test a family of minimal glyph languages. Work in
`dbccpage/the_symbol_game`. The deliverable is a mathematically compressed,
domain-agnostic foundation for `mssn.ebnf` and Mode 01, accompanied by executable
examples and evidence. Develop the mathematics before implementing its machinery.

## The creator's requirement

MSS-N does not require every inscription to be enclosed in `<...>`.

```text
a>b>c>a
a0>b2>c1>a0
```

Both are legitimate glyph prompts. With a declared graph interpretation, the
first can be a directed cycle. With a declared suffix-annotation convention,
the second can add vertex annotations. Those annotations might later represent
age, cash balance, or something entirely different. Their meaning is not in the
digits themselves. Bytecode is a possible downstream encoding; it is not the
primitive starting assumption.

Mode 01 is strictly about glyph inscription and manipulation. Do not reduce it
to DDC, packetization, JSON envelopes, application architecture, product advice,
or a prescribed ontology. DDC and boundary packets may be particular profiles.
Profile declarations may live beside the prompt. Do not force the entire
metalanguage, codebook or verification protocol into every glyph inscription.

Treat “all possible variants” as a research obligation: derive a finite set of
constructors for a precisely stated class; enumerate all instances under explicit
finite bounds; identify remaining classes and the first unresolved cases. Do not
replace that obligation with either a hand-picked list or an unbounded
completeness claim. Continue until the available budget is used productively,
leaving a precise checkpoint and the next mathematical obstruction.

## Read the current estate first

Read current contents and applicable repository instructions. Record the commit.
Start with:

- `omega_engine_education/documentation/003_minimal_symbol_system_n_mssn/grammar/mssn.ebnf`
- `omega_engine_education/documentation/030_the_symbol_game_proposal_fidelity_protocol_pfp/grammar/grammars_readme.md`
- `omega_engine_education/documentation/030_the_symbol_game_proposal_fidelity_protocol_pfp/grammar/check_grammars.py`
- `omega_engine_education/documentation/003_minimal_symbol_system_n_mssn/code/check_mssn.py`
- `omega_engine_education/documentation/003_minimal_symbol_system_n_mssn/grammar/mssn_conformance_cases.json`
- `omega_engine_education/documentation/030_the_symbol_game_proposal_fidelity_protocol_pfp/modes/mode_01_hieroglyphics_and_glyph_alphabets/contract.yaml`
- The same mode directory's `wire_representations.md` and `examples.md`
- `omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md`
- The MSS-N README and [From Pre-Genesis to MSS-N](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_pre_genesis_to_mssn/paper.md), especially the distinction between an atlas
  row, a presentation and a licensed Genesis lift.
- `omega_engine_education/documentation/030_the_symbol_game_proposal_fidelity_protocol_pfp/grammar/pfp.ebnf` and the other registered
  grammar profiles; inspect their checkers before changing compatibility.
- `omega_engine_education/documentation/030_the_symbol_game_proposal_fidelity_protocol_pfp/modes/mode_types.yaml` and `mode_models.yaml` before
  changing the structure of a mode contract.

The current 22 new profiles are a starting hypothesis, not a sacred inventory.
Keep useful derivations; correct defects. Do not treat file existence, a passing
fixture or the word “canonical” as a mathematical argument.

## 1. Derive the smallest useful mathematical description

Distinguish an occurrence, a glyph identity, its displayed spelling, a token,
a sequence, an interpretation, and an allowed manipulation. Declare the host
mathematics you use. No sets, order, counting, relation, equality test, numeric
domain or evaluation rule may be described as internally earned without its
actual derivation. A raw presentation over marks is still useful when that
internal derivation is absent.

Separate empty input ε, absent input, the two literal marks `<>`, and a declared
ground symbol. State exactly when any of them are identified. Distinguish an
unrecognized spelling, an ambiguous parse, an undecided side condition, a known
invalid transformation, and an exhausted search bound.

Construct a compact definition of a presentation and its admissible moves.
Candidate ingredients are a finite alphabet, spelling/segmentation map, grammar,
start rule, observation/equality policy, partial interpretation and witnessed
relation. Retain an ingredient only when you can exhibit the failure caused by
omitting it. Do not inflate this into a business workflow.

Derive the path rules from explicit roles and concatenation. Derive suffix
attachment from a disjoint letter/digit partition. List every premise used in
getting from marks to `a>b>c>a` and then to `a0>b2>c1>a0`. State which additions
are definitions, which are optional conventions, and which conclusions follow.
Do not call a convenient choice the unique forced successor.

## 2. Construct and classify the grammar families

Develop a parameterized EBNF family with fully defined productions. Each concrete
instance must declare its terminal inventory, spelling policy, public start,
layout, empty-input convention, tokenization and ambiguity policy.

Investigate at least these independent axes:

- Raw marks, words, explicit token boundaries, fixed-width tokens, prefix codes,
  escaping, quotation, separators, and length-prefixed encodings.
- Bare paths, path lists, edge lists, adjacency lists, parallel edges, self-loops,
  repeated vertices, isolated vertices, cycles and branching presentations.
- Prefix, infix, postfix, unary/binary/n-ary forms; grouping; named and anonymous
  trees; nesting; streams; applications and incidence/hyperedge presentations.
- Vertex, edge, occurrence, relation and whole-expression annotations; untyped
  suffixes, exact integers/rationals/decimals, vectors, tuples and named fields.
- Distinct finite alphabets: ASCII, digits alone, binary, mathematical signs,
  Egyptian glyphs, emoji, and mixtures with precise token boundaries.
- `<`/`>` as ordinary data, directional operators, delimiters or separator pieces.
  Resolve collisions by declared profiles or actual disambiguation; do not guess.
- Source notation versus token sequence versus byte encoding versus executable
  bytecode. Supply machine semantics only for a separately selected bytecode task.

For each new family, give its smallest motivating example, productions, parse
structure, assumptions, positive and negative examples, collision cases, and its
relation to an existing family. Group cosmetic renamings by proved transport
instead of counting them as new mathematical capability.

Use ambiguity productively. For `a0`, `ab12`, `a12`, `a0>a1`, `01`, `a>b<c`,
`a<>b`, `<a>b`, `a>b>`, and `a>0>b`, exhibit competing readings where they exist.
Keep lexical annotation distinct from entity identity and numeric decoding.
Specify attachment position. Preserve leading zeros and absent-versus-zero data.

Give the EBNF/side-condition boundary precisely. Equal field lengths, symbol-table
references, unique labels, nonzero denominators, value agreement, graph identities
and arbitrary dependent obligations must not be smuggled into grammar comments
as if an ordinary context-free parser checked them. Make the checker obligation
explicit. Identify limitations of the existing development recognizer, including
left recursion, nullable repetition and loss of parse multiplicity.

## 3. Derive the calculus of glyph manipulation

Study at least identity, concatenation, insertion, deletion, substitution,
duplication, permutation, renaming, reversal, direction inversion, composition,
path splitting/splicing, cycle rotation, annotation attachment/erasure, grouping,
ungrouping, escaping/unescaping, encoding/decoding and contextual rewriting.

For every operation, specify source/target profiles, relation or partial function,
domain of definition, required witness, exact information retained/lost/added,
and closure or counterexample. Distinguish manipulation of raw strings from
manipulation of parsed structures. Decide when positions, occurrences, labels or
quotient classes are the objects being moved.

Prove the useful laws, with hypotheses:

1. Concatenation and contextual substitution laws, including empty words.
2. Injective token renaming extends to an isomorphism of transported presentations.
3. Variable-length token codes need unique decodability; injective codewords alone
    are insufficient. Give the `a↦0,b↦00` collision and investigate beyond prefix codes.
4. Parser/renderer retractions; exact source round trips versus AST round trips
    versus equality only after a declared quotient.
5. Prefix/postfix/nested codecs preserve an explicitly defined structure.
6. Reversal and direction inversion: determine which preserve a directed graph,
    which change it, and what happens to walk order, root, weights and multiplicity.
7. Quotients and forgetful maps: identify fibers and the data needed for a lift.
    Prove when a total inverse cannot exist; retain ties where lifts are nonunique.
8. Composition of partial transformations and compatibility of their declarations.
    Supply the commutative diagram or a smallest counterexample for each claimed
    preservation result.
9. Termination/confluence only for declared rewrite systems. A normalization name,
    selected normal form or bounded successful search is not a proof of either.
10. Conservative grammar extension: old inputs retain their specified behavior
    under the old profile, with any cross-profile ambiguity exposed separately.

Prefer a small common theorem covering many cases to repetitive notation.
Classify transformations as reversible encodings, embeddings, quotients,
information-adding constructions, or other precisely defined relations. Do not
ban legitimate lossy manipulation; describe and test its loss honestly.

## 4. Make exhaustive claims finite and reproducible

Define a finite constructor signature and an explicit bound tuple. Include the
alphabet bound, production count, right-hand-side syntax-tree size, literal
length, recursion restrictions, inscription length, parse depth and rewrite
length where relevant. State the unit of every length.

Give an enumerator and a coverage argument for exactly this bounded class.
Retain syntactically distinct candidates until a proved equivalence permits a
quotient. Do not assume general grammar equivalence is decidable. Bounded language
agreement is one computed relation, not a proof of equality at every length.
Supply a separating word whenever you find one; leave global equivalence open
when its proof is absent.

Track separate coverage: constructor combinations, instantiated grammars,
accepted/rejected words, ambiguous parses, transformations, counterexamples and
proved laws. Use a fair schedule/checkpoint for unbounded continuation. A larger
alphabet or atlas index must not be counted as a derived semantic capability.

If claiming minimality or compression, define the cost. Report glyph count,
serialized bytes, grammar/codebook overhead and any model-token measurement
separately. Include amortization assumptions and retain tied minima. Do not
claim lower LLM token cost without actual tokenizer evidence.

## 5. Tests that could falsify the claims

Use explicit examples plus bounded exhaustive enumeration and independent
reference algorithms. Cover at least:

- Both creator examples under raw, whole-label and suffix profiles.
- All short strings over a declared alphabet; malformed prefixes/suffixes,
  unmatched/grouping marks, multiple roots, layout, empty inputs and duplicates.
- AST/lexeme preservation, repeated/parallel edges, self-loops and no inferred
  filled faces. Under different explicit identity policies, show the difference
  between four occurrences and three named vertices in `a>b>c>a`.
- Multi-digit suffixes, ambiguous labels, zero, leading zeros, negative/rational
  lexemes, zero denominators and static-versus-occurrence annotation conflicts.
- Exact Unicode spellings, multi-codepoint glyphs, normalization, confusables,
  delimiter-as-data, encoding truncation and variable-length code collisions.
- Metamorphic renaming, inverse operations, operation composition, noncommuting
  operations, quotient collisions and inverse failures.
- Uniqueness claims challenged by explicit parse forests or independent readers.
  A recognizer's boolean acceptance is insufficient evidence of unambiguity.
- Existing boundary/historical/K0/quiz/DDC profile regressions. Do not broaden the
  boundary parser or change receipt-bound grammar bytes to make a new example pass.
- Mode contract validation through both the declared schema and existing model.

Report the actual command, scope, result and missing coverage. Never fabricate
runs or promote bounded computations to unbounded theorems. Avoid tests that only
compare a generator with its own unexamined assumptions.

## 6. Deliver the mathematics and update the estate

Produce:

1. A compact mathematical specification with explicit premises, definitions,
   derivations, counterexamples, and unresolved obligations.
2. A refined canonical `grammar/mssn.ebnf` with explicitly selected family starts
   or a justified generator of concrete EBNF instances. No undefined productions,
   implicit parser fallback or silent universal wrapper.
3. An example atlas and machine-readable corpus with broad constructor coverage.
   Include exact parses where relevant, not just accepted strings.
4. Focused updates to Mode 01's contract and documentation, with its scope limited
   to glyph manipulation and optional declared interpretations.
5. A bounded enumerator, independent checks and a reproducible coverage report.
6. A claim ledger separating proved, computed, declared, conditional, conjectured,
   open and refuted claims. Each proved claim needs its proof; each computed claim
   needs its run; each added primitive needs its stated reason.
7. A migration note preserving existing profile contracts, plus the next ten
   mathematical targets ordered by dependency and the obstruction each removes.

Do the work, rather than returning only a plan. Keep the foundation domain
agnostic and as compressed as the derivations allow. The end result should let
another researcher inspect every step from literal glyphs to structured,
transformable inscriptions, and reproduce exactly what has and has not been
established. AuthorityEffect: None.
