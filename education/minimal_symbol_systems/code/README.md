# MSS-N Code & Verification

**AuthorityEffect:** None.

| File | Purpose |
| :--- | :--- |
| [`check_mssn.py`](check_mssn.py) | Replays [`../grammar/mssn_conformance_cases.json`](../grammar/mssn_conformance_cases.json) against [`../grammar/mssn.ebnf`](../grammar/mssn.ebnf) across its 22 public starts; exit 0 on PASS. `verify-strand 010` runs it. |
| [`mssn_codec.py`](mssn_codec.py) | Parse all 22 grammar starts and serialize checked ASTs; `verify-strand 010` round-trips a word through it. |
| [`mssn_extended_codec.py`](mssn_extended_codec.py) | Explicit old-alphabet inclusion and a noninjective substitution retraction, with ideal information-rate calculations. |
| [`tests/test_mssn_codec.py`](tests/test_mssn_codec.py) | Codec and conformance tests. |

The shared S(n) Python models and the curriculum runner live once, in
[`../../symmetric_group_presentations/code/`](../../symmetric_group_presentations/code/README.md). The byte-identical copies
that used to sit here were removed on 2026-10-06.

```bash
py -3.12 education/minimal_symbol_systems/code/check_mssn.py
py -3.12 -m pytest education/minimal_symbol_systems/code/tests/test_mssn_codec.py
```

`serialize_mssn` checks the public-profile AST by reparsing its exact output.
Individual `to_wire` methods only render fields. The finite Unicode profile
accepts its eight declared tokens, including the exact ZWJ sequence in `👩‍💻`;
ASCII digit productions reject Unicode digit lookalikes. Numeric decoding,
resource limits and semantic interpretation remain separate from this codec.
