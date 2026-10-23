# Faithful finite representations: offline reference and replay

AuthorityEffect: None. This package realizes the finite constraint profile
of GEN-WDP-49–51. Its mathematical specification is the
[full derivation](../../docs/faithful_representation_and_relative_completeness.md).
It uses Python's standard library. It does not contact a model.

From the paper's `code` directory:

```powershell
python -B -m faithful_representation verify
python -B -m faithful_representation replay --directory faithful_representation/evidence/resumed_exhaustion
```

`verify` independently recomputes the eight retained runs and all 4,096
Boolean triangle instances, compares original-assignment and local-family
solutions, and verifies the source-bound summary. `examples` deliberately
regenerates retained artifacts after an intentional implementation change.

The public Python interface is:

```python
from faithful_representation import encode, search, check, replay

encoded = encode(problem, changes=())
partial = search(encoded, fuel=2, proposals=[[999]])
receipt = check(problem, partial)
continued = search(encoded, fuel=20, checkpoint=partial)
```

Input version 1 has exactly `schema_version`, `goal`, `variables`, `relations`,
`assumptions`, and `authorization`. The goal is `exists_global_assignment`.
Variables contain unique names and lists of distinct text values. Relations
contain unique names, scopes of distinct declared variables, and lists of
distinct permitted rows. Domains and relation tables may be empty. A nullary
true relation has rows `[[]]`; a nullary false relation has rows `[]`.

Transport specifications use `rename`, `join`, `split`, or `auxiliary`.
The [four-operation fixture](evidence/four_transports/certificate.json) gives
their actual wire form. Renaming requires complete bijections; split admission
computes the projection/join equality; auxiliary admission checks a total
function on the declared domain product. Every target is recomputed.

`fuel` is the cumulative search-unit ceiling, not a fresh allowance on resume.
Increasing it explicitly appends a grant at the retained cursor. Each transport
and candidate check spends one unit. `max_steps` permits interruption before
the ceiling is reached. A checkpoint is the entire preceding certificate;
the verifier reconstructs its counters, scheduling phase and parent chain.
Preparatory encoding and replay-verifier computation are outside this unit
search-cost model. No wall-clock, memory, API billing or empirical speed claim
is made.

`check` returns `accepted: true` only when the supplied trace supports its
stated status. A checked `Undetermined` is not a solved problem. `Proved`
includes a decoded original assignment; `Refuted` requires complete canonical
coverage. Malformed evidence returns `accepted: false` with no mathematical
status. Hashes bind data; rehashed false witnesses still fail semantic replay.

The authorization list records the original declared requirements; this
reference profile does not authenticate or execute external permissions.
Changed assumptions or authorization requirements require a new original
problem. Existing receipts cannot be reused as unconditional answers to it.

The tests include every Boolean triangle relation triple, every pair of
Boolean binary tables for joins, all Boolean binary tables for lossless
splitting, transport inverses, witness mutations, and interruption/resumption.
The Lean modules prove the mathematical models; concrete Python program
correctness is supported by these separate checks.
