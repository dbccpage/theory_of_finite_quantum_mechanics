# Grammar

**AuthorityEffect:** None.

`mssn.ebnf` is written in the EBNF subset of
[`check_grammars.py`](../../004_oepfp/grammar/check_grammars.py):
`=`, `;`, `,`, `|`, `{ }`, `[ ]`, `( )`, `(* *)` comments and double-quoted
terminals; lowercase rule names; exact full-length matching with no whitespace
skipping; no nullable repetition.

There is no default start. Each case in `mssn_conformance_cases.json` names its
public start, and [`../code/check_mssn.py`](../code/check_mssn.py) replays the
cases across the 22 public starts.

```bash
py -3.12 omega_engine_education/documentation/003_oemssn/code/check_mssn.py
```
