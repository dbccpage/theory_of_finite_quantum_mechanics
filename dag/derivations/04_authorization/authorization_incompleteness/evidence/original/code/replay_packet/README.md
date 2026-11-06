# Bounded finite replay packet

**Status:** executable finite packet for AIT-G3 and AIT-G4.

**AuthorityEffect:** None.

This directory is a concrete replay packet for the four-configuration
transition table in formal/tape_transition_invariant_models.lean. It
does not authorize a paper, a deployment, or a general computation. It
recomputes one declared finite contract and keeps the terminal result
open.

## Bound carrier

packet_manifest.json binds SHA-256 digests for:

- the source-controlled transition proposal;
- the separately declared contract and terminal policy;
- the PowerShell evaluator and entrypoint;
- the Lean finite model and its direct formal dependency; and
- the Lean toolchain pin.

The evaluator rejects an artifact substitution before it reads the
proposal. It enumerates the transition table, checks the
clean-terminal invariant, finds marked-cell countertraces, and compares
two report interfaces. Full configuration is adequate for the
marked-cell contract. The control-only stay report is not adequate, so
its route is open_due_to_inadequate_report.

The proposal's source_claimed_pass Boolean is recorded but not used by
the evaluator.

## Replay

From the repository root:

<!-- markdownlint-disable MD013 -->
~~~powershell
pwsh -NoProfile -File coda_university/coda_research/authorization_an_incompleteness_theory/code/replay_packet/verify_transition_packet.ps1 -RepositoryRoot (Get-Location).Path -RunFormalReplay
~~~
<!-- markdownlint-enable MD013 -->

The optional RunFormalReplay switch compiles the bound transition model
and its bound direct dependency with the exact toolchain after the byte
bindings pass. It does not invoke the shared Lake target.

## Tests

<!-- markdownlint-disable MD013 -->
~~~powershell
pwsh -NoProfile -File coda_university/coda_research/authorization_an_incompleteness_theory/code/tests/test_replay_packet.ps1 -RepositoryRoot (Get-Location).Path

pwsh -NoProfile -File coda_university/coda_research/authorization_an_incompleteness_theory/code/integration_tests/test_transition_packet_integration.ps1 -RepositoryRoot (Get-Location).Path
~~~
<!-- markdownlint-enable MD013 -->

The unit corpus checks the good packet, proves the source pass flag has
no effect, and rejects twenty-one mutations: proposal bytes, path escape,
every bound artifact role, extra proposal field, proposal schema,
contract outcome, terminal policy, parser profile, and command profile.
The integration replay runs the evaluator and target-local two-source
Lean closure.

## Trust boundary and ceiling

The manifest is a trust-root input. It must be fixed outside the
proposal bytes by a commit, review, or independently retained receipt;
the manifest does not authenticate itself. SHA-256 collision resistance,
the evaluator's correspondence to Lean, runtime integrity, and custody
are explicit assumptions, not results of this packet.

The producer, evaluator, and manifest currently share a local working
tree. That is useful for demonstrating logical separation and replay
binding, but it is not evidence of independent organizational custody.
Changing the proposal, contract, checker, manifest, or terminal policy
together is a new trust-root event, not a replay of this packet.

The current manifest is `AIT-G3-FINITE-TRANSITION-REPLAY-V4`. It binds
only the finite model, its direct dependency, and the exact Lean
toolchain needed for its target-local replay. This avoids treating an
unrelated shared Lake-root edit as a change to this finite packet. The
finite transition proposal, contract, evaluator, and terminal policy
remain the bounded object under test; the packet neither imports nor
makes a claim about unrelated research roots.

**AuthorityEffect:** None.
