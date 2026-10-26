# Genesis Code & Verification

**AuthorityEffect:** None.

| File | Purpose |
| :--- | :--- |
| [`check_genesis.py`](check_genesis.py) | Replays [`../grammar/genesis_conformance_cases.json`](../grammar/genesis_conformance_cases.json) against [`../grammar/genesis.ebnf`](../grammar/genesis.ebnf); exit 0 on PASS. `verify-strand 001` runs it. |
| [`tests/test_genesis_grammar.py`](tests/test_genesis_grammar.py) | Pytest replay of the same cases. |

The shared S(n) Python models and the curriculum runner live once, in
[`../../symmetric_group_presentations/code/`](../../symmetric_group_presentations/code/README.md). The byte-identical copies
that used to sit here were removed on 2026-10-06.

```bash
py -3.12 education/genesis_primitives/code/check_genesis.py
py -3.12 -m pytest education/genesis_primitives/code/tests/test_genesis_grammar.py
```
