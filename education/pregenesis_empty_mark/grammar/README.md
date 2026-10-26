# Grammar

**AuthorityEffect:** None.

`pre_genesis.ebnf` is later host notation for the recorded inscriptions and lists of them.
It was not a grammar tested by the original trials. It is written in the EBNF subset of
[`check_grammars.py`](../../004_oepfp/grammar/check_grammars.py):
`=`, `;`, `,`, `|`, `{ }`, `[ ]`, `( )`, `(* *)` comments and double-quoted
terminals; lowercase rule names; exact full-length matching with no whitespace
skipping; no nullable repetition.

## Alphabet

The inscription alphabet is { `<`, `>`, `a`, `b` }. The list notation additionally
uses `{`, `}` and `,`. The delimiters and payload glyphs occur in
the trial transcripts in [`../sources/`](../sources/README.md); `<b>` never occurs in them, and `b` occurs only inside `<ab>`.
The Sigma36 glyphs, the directed cut `<a->b>` and the admission events belong
to [`genesis.ebnf`](../../genesis_primitives/grammar/genesis.ebnf) and
[`sn.ebnf`](../../symmetric_group_presentations/grammar/sn.ebnf).

## Four states kept apart

| State | In this grammar | Why it matters |
| --- | --- | --- |
| Absent input | Not a word; no start matches it | A missing document is not an empty one. |
| Empty word `""` | Refused by every public start | The recognizer has no empty production, so this is a conformance fact (`PG_002`, `PG_011`, `PG_025`). |
| `<>` | `ground_token` | A literal host word; its shape does not admit a native container. |
| `{}` | `pre_genesis_regime` with zero inscriptions | An empty host list; the grammar specifies no transition semantics. |

## Public starts

| Start | Accepts | Refuses |
| --- | --- | --- |
| `ground_token` | `<>` | `""`, `<a>`, `<><>` |
| `inscription` | `<>`, `<a>`, `<b>`, `<ab>`, `<aab>` | `<`, `>`, `a`, `<c>`, `<<>>`, `<a><b>`, `< >`, `[]`, `<a->b>` |
| `pre_genesis_regime` | `{}`, `{<>}`, `{<>,<a>}` | `""`, `<>`, `{<>,}`, `{`, `{ <> }`, `{supply(<>)}` |

The cases live in `pre_genesis_conformance_cases.json` and are replayed by
[`../code/check_pre_genesis.py`](../code/check_pre_genesis.py) and
[`../code/tests/test_pre_genesis_grammar.py`](../code/tests/test_pre_genesis_grammar.py).

```bash
py -3.12 education/pregenesis_empty_mark/code/check_pre_genesis.py
```

This grammar describes inscriptions. It does not assert that any model
produced them, that `<>` forces a carrier, or that a transition exists; the
absence of transitions must be a premise of a declared transition system.
