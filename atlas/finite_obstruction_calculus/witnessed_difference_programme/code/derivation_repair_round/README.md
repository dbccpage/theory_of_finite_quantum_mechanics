# One derivation repair round

**AuthorityEffect: None.** The approved single request used the configured
OpenRouter model `stealth/space-bunny-alpha` (Space Bunny Alpha). No separate
“Super Bunny” endpoint was invented. The combined two-level mathematics packet
is retained as `packet.yaml` and `packet.json`, with the exact dispatched copy
under `live_20261004/`. It contains the frozen eight-state observation table,
the two-state unsafe antibody example, ten correction requests, a different
worked example and the required response structure.

The actual generation `gen-1791161698-N4QnW72SRMmTIBU3saic` hit its 4096-token
output limit. OpenRouter returned `finish_reason: length` with no complete
candidate. The host saved **REFUSED_INCOMPLETE_PROVIDER_RESPONSE** and
**NO_ACCEPTED_CANDIDATE**. It did not salvage an incomplete answer, manufacture
a repaired witness, retry, or use a paid fallback. No revised mathematical
statement receives evidence credit from this generation.

Raw usage reports 1783 prompt tokens, 4096 completion tokens and a cost of
**0 USD**. `endpoint_metadata.json` retains the pricing check made immediately
before the request. Cost is provider-reported, not an account reconciliation.
`provider_response.json` retains the original response bytes; `usage_receipt.json`
and `host_receipt.json` bind their hashes.

`check.py` independently checks submitted fixed suites, an uncovered pair for
every cheaper subset, adaptive tree branches and leaves, exact path cost, and
a forcing-pair lower bound. It uses `finite_observation.solver` carriers and
`antibody_transfer.checker.transfer`; it never calls `solve()` to replace a
candidate. Every proposed antibody must itself be admitted. A safe accumulator
that filters out an unsafe proposed rule does not certify that proposal.

The original negative controls remain explicit:

- Observation states `1` and `5` have equal readings under the full printed
  shelf and unequal query values. Neither a fixed nor adaptive exact decoder
  exists for that table.
- The original identity adapter transfers the source-sound rule `D={1}` onto
  a valid target `1`. Its rule-admission claim is rejected.

The **11 passing local tests** use clearly labelled host fixtures to check a
repaired observation suite/tree, both permissible antibody repair styles,
mutated witnesses, the original controls and the actual truncated response.
These successful host-fixture tests are separate from the failed model round.
`offline_verification.json` records their scope and checker hashes.

From the paper's `code` directory, replay the saved response without a model:

```powershell
python -B -m derivation_repair_round.check derivation_repair_round/live_20261004 --write
```

The command saves the structured refusal and exits **1**, as expected. There is
no accepted model repair to integrate. A later request would be a new round,
requiring its own explicit dispatch authorization and evidence.
