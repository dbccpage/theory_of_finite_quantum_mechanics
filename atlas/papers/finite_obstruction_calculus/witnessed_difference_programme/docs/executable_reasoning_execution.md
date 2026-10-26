# WDP executable refinement: execution and remaining obligations

Edition 2.4.5, 2026-10-16. Starting base:
`accd20100a3c7e40a8c770a281f14abf22c29e12`. AuthorityEffect: None.

## Delivered result

[The derivation](derivations/executable_reasoning_refinement.md) and manuscript
§20.15 close the concrete Lean certificate-checker boundary left by §20.14.
Accepted indexed traces refine the abstract inference calculus; accepted Boolean
countermodels exclude derivability. Both judgments bind the current theory and
query. An independent directed-reachability definition has a general equivalence
with the graph Horn theory, so accepted certificates answer that original graph
question directly.

Python and native Rust export actual certificates as explicit Lean data and
closed theorem obligations. Lean reduces its own proved checker using `decide`.
The foreign searcher supplies data, not a trusted proof judgment. Source/query
substitution, forward references, malformed rules and invalid countermodels
remain refusals. Resource failure supplies no entailment judgment.

## Verification

The [input-bound receipt](../manifests/executable_reasoning_refinement.json)
records the exact source hashes, runtime identities, commands, expected refusals
and output hashes for this increment. Its executable harness is
`scripts/verify_reasoning_refinement.py`; generated modules and logs are retained
in the output directory named by each command. Reproduce it with Python 3.12,
explicit installed `--lake` and `--rustc` paths, and a fresh `--output` directory.

- The root `WdpReasoning` target builds. All 17 new declarations are audited;
  their dependencies are limited to `propext` and `Quot.sound`, with no custom
  axioms or admitted proofs. The 15 previous abstract declarations are retained.
- All 2,048 two-atom Horn tasks agree with independent Boolean valuations and
  yield kernel-checked theorem obligations. All 64 two-vertex directed graph
  tasks yield original-question reachability or non-reachability theorems.
- Ten malformed Python obligations fail kernel checking. The live Python
  adapter also succeeds on an actual valid obligation; timeout/tool-error unit
  tests require the absence of a logical judgment.
- Fresh selected Rust modules pass four tests across the existing checker and
  new exporter. A freshly compiled native example emits eleven obligations:
  four kernel acceptances and seven expected refusals. Repeated premises,
  empty-premise rules, Unicode and stale-source controls are included.
- Targeted Python 3.12 verification covers the 62 paper-contract tests, 16
  existing reasoning tests and 11 new refinement tests. The planner adds a
  regression that prevents these completed components from closing the open
  foreign-semantics obligation.

Lean elaboration uses installed 4.34.1; the repository's 4.34.0 pin is unchanged.
The native checks compile the selected real modules afresh; they do not attest
the whole crate, historical Mathlib package or all repository suites. The old
2.4.4 receipt remains byte-for-byte historical at source commit
`117435fd0a0c12acfe6f846ca8bfd501403c7710`.

The broader source-route validator cannot execute on this checkout because the
`omega_symbol_game` host binary is absent. Its generated owner view is unchanged
and matches the current registry; the planner checks the eleven source/owner
correspondences. This does not substitute for a fresh host-route execution.

The canonical paper builder regenerates Markdown-derived TeX and PDF. The new
section begins on PDF page 124; the document has 286 pages and no overfull-box
warnings. The package checksums bind the current paper artifacts, receipt,
source and documentation. No new Zenodo deposit or release archive is claimed.

## Status reconciliation

The planner records 410 goals: 281 done, 119 open, four blocked and six deferred.
This increment adds three completed scoped records:

| Record | Completed scope |
| --- | --- |
| `WDP-REASONING-EXECUTABLE-KERNEL` | General soundness and trace refinement of the concrete Lean checkers |
| `WDP-REASONING-GRAPH-TRANSPORT` | General equivalence and certificate transport to directed reachability |
| `WDP-REASONING-CERTIFICATE-REPLAY` | Tested foreign exporters and kernel replay of explicit finite tasks |

`WDP-REASONING-FOREIGN-SEMANTICS` remains open. It requires universal
correspondence for the foreign programs and serializers, including a formal
producer saturation/completeness/termination argument. A finite replay corpus
does not supply those proofs. The Lean checker theorems do quantify over
arbitrary finite inputs; their generality is distinct from the bounded tests
of the Python/Rust bridge.

`WDP-REASONING-EXTENSIONS` still requires production integration, observed-world
adequacy, richer update semantics and priced recursive reuse. The completed
subgoals do not close the broader foundational, physical or institutional
programme. Ordinary planner checks pass; strict mode retains the existing
43 unavailable external citations, which are outside this increment's evidence.

The current WDP source-node digest and its affected source correspondences are
refreshed. Main advanced through PRs 1145 and 1146 during this work. PR 1145
changed later finite-QM claims; the joined finite source-packet profile's
8,192-byte source prefix and native owner/oracle remain unchanged. Its current
source-node digest and one join are refreshed after that comparison, with no
new credit for the corrected later QM claims. Historical execution receipts
retain their original bytes and scope; the three stale Woland execution
bindings remain NOT_REPLAYED.
