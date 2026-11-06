# Grammar

**AuthorityEffect:** None.

`genesis.ebnf` is written in the EBNF subset of
[`check_grammars.py`](../../004_oepfp/grammar/check_grammars.py):
`=`, `;`, `,`, `|`, `{ }`, `[ ]`, `( )`, `(* *)` comments and double-quoted
terminals; lowercase rule names; exact full-length matching with no whitespace
skipping; no nullable repetition. Its master start is `genesis_statement`; the
cases in `genesis_conformance_cases.json` name their start, and
[`../code/check_genesis.py`](../code/check_genesis.py) replays them.

The regime before the first admission event is described by
[`../../1_pregenesis_empty_mark/grammar/pre_genesis.ebnf`](../../1_pregenesis_empty_mark/grammar/pre_genesis.ebnf).

```bash
py -3.12 education/4_genesis_primitives/code/check_genesis.py
```
