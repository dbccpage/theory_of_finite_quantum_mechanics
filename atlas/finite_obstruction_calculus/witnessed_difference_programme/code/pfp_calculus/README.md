# PFP calculus candidate: live evaluation and archived replay

**AuthorityEffect: None.** This is paper-scoped evaluation evidence. Ordinary
replays make no provider calls; `live_run.py run` performs one explicitly
configured call, with no retry or paid fallback.

The original seed is retained byte-for-byte in `source/seed.txt`:

> Integrate the function f(x) = x from integer 0 to integer 10.
> Provide the single exact numerical result.

The admitted profile is the ordinary real Riemann integral on `[0,10]`, encoded
using rational polynomial coefficients. The words “integer 0” and “integer 10”
describe its endpoints. The polynomial witness establishes the derivative
identity on all real inputs, followed by exact endpoint evaluation; this is
not numerical quadrature.

`source/model_result.json` and `source/model_receipt.json` retain the actual
archived round-04 response and its declared Gemini 2.5 Flash generation metadata.
Those metadata were not re-queried from the provider. Source files were staged
additions in the primary checkout at HEAD `952f5a56d862eec6ba7ba38210aade008a642931`;
the individual byte hashes in `source_provenance.json` bind them, rather than
misidentifying them as committed content at that HEAD. The original checker is
retained unchanged in `source/calculus_reference_check.py`. The live runner,
which implicitly loads environment files and implements only rounds 3 and 4,
is not imported or executed.

The new adapter records a host audit and extraction of those exact candidate
bytes, then executes the supplied Stage 5 obligation through that source
checker. Candidate identity, seed, profile, audit routing and parent artifacts
are bound and checked before mathematical evaluation. Its audit covers source
fidelity and routing only. It does not pretend to establish arbitrary prose
claims around the witness.

The archived antiderivative `F(x)=x^2/2` is accepted with exact result `50`.
A separately labelled host adversarial control `F(x)=5x` has the same endpoint
difference `50` but is rejected because its derivative `5` differs from `x`.
The model candidate is never replaced with that control, or with a computed
solution. Both retain `AuthorityEffect: None`.

From the paper's `code` directory:

```powershell
python -B -m pfp_calculus.replay
```

`replay_receipt.json` stores the result. `unit_tests/test_pfp_calculus.py` checks
the two outcomes, candidate preservation and ten boundary mutations, including
wrong candidate IDs, invented source quotes, stale parents, changed inputs and
authority escalation. The scoped run passed 14 tests.

The numbered model Stages 1–4 and 6–8 were **not executed** for the archive episode.
The archived prompt explicitly describes a standalone probe. Host-generated
audit and extraction records cannot retroactively turn it into the prepared
rounds 13–20 model sequence. The general SG staged runner still requires an
actual calculus adapter and meaningful injected-checker integration. These
remain outside this bounded archived-model-to-host replay.

## Fresh single-example evaluation, 2026-10-04

`live_20261004/` contains a fresh typed two-level PFP request to
`stealth/space-bunny-alpha`, generation
`gen-1791160037-Fc3JtoY58i7oHmvXqMWI`. The shared system rules, original seed,
explicit real profile, different worked example and required witness schema
were saved as one YAML packet and dispatched in separate system/user roles.
The worked example integrates the constant function 2 on `[0,3]`; the answer
to the requested integral is not supplied in the model-visible packet.

The existing `omega_engine_providers.infrastructure.openrouter_transport`
performed exactly one request, with maximum 2048 output tokens and provider
fallbacks disabled. Before dispatch the runner recorded OpenRouter's endpoint
metadata and required all active endpoint prices to be zero. An explicitly
provided configuration path supplied credentials; neither credentials nor
environment-file contents appear in the artifacts. No new call follows this
round. The raw provider usage reports cost **0 USD**; this is a returned cost
field, not an estimate or an independently reconciled account balance.

The fresh model candidate passed the host's identity/source audit and unchanged
extraction, then Stage 5 independently accepted its derivative witness and
result `50`. The separately labelled host control `F(x)=5x` failed the derivative
obligation despite its endpoint result `50`. The audit and extraction are
explicitly **host-owned**. The completed scope is one actual model-proposal to
host-evaluation example; it does not require or imply a full eight-stage model
campaign, a Rust implementation, or execution authority.

Replay the retained provider bytes without a network call from `code`:

```powershell
python -B -m pfp_calculus.live_run replay --run-dir pfp_calculus/live_20261004
```

The final scoped test file has **21 passing tests**, including replay of the
retained live receipt while network access is disabled, exact response binding,
and refusal of unknown or nonzero endpoint pricing.
