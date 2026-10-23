# Certified finite progress

This reference implementation checks finite belief-game certificates against the
original declared model. It is the executable repair for the Appendix S review
counterexamples. The corrected Appendix S is integrated into the main WDP
manuscript, and its mathematical modules are registered in the aggregate Lean
harness. Formal and executable evidence remain separately scoped.

## Interfaces

- `compile_model(model)` reconstructs reachable beliefs, enabled actions, targets,
  exact positive rational costs, and supplied resolution tables from the input.
- `solve_progress(model, max_horizon=None)` proposes a losing trap or an optimal
  winning strategy. A declared horizon limit produces `Undetermined` when the
  required finite minimax horizon exceeds that limit.
- `check_certificate(model, certificate)` independently replays the submitted
  witness. It never invokes the producer or substitutes another strategy.
- `refine_observation(model, blocks)` refines a partition of reachable beliefs
  until target, action, price, and successor-class signatures agree.
- `report_termination(model, certificate, budget)` distinguishes a checked
  optimal budget lower bound from a merely feasible strategy's upper bound.

Certificates bind the model digest, task, assumptions, authorization metadata,
initial belief, submitted strategy, rank, values, and losing closure witnesses.
Authorization metadata records the declared context; this package does not grant
institutional authority. Supplied resolution truth tables remain assumptions.

## Local replay

With the paper's `code` directory on `PYTHONPATH`, an example is:

```python
from certified_progress import check_certificate, solve_progress
from certified_progress.fixtures import cheaper_route

model = cheaper_route()
submitted = solve_progress(model)["certificate"]
receipt = check_certificate(model, submitted)
assert receipt["accepted"] and receipt["initial_value"] == "2"
```

The direct route costs five; the two-step route costs two. A forged stalled
classification hiding the cheaper route is refused.

Run the three focused test modules from the paper root, with `code` on `PYTHONPATH`:

```text
python -B -m pytest code/tests/unit_tests/test_certified_progress.py code/tests/unit_tests/test_progress_observation.py code/tests/unit_tests/test_progress_replay.py -q -o addopts=
```

The scoped run has 58 tests across three modules, including
`code/tests/unit_tests/test_progress_replay.py`. One independently enumerates every policy in each
of 4,096 small finite games and compares its outcome and exact cost with the
producer, then checks the submitted certificate. Other tests cover false stalls,
terminal value shifts, omitted initial beliefs, terminal-as-loss claims, missing
model targets, dead ends, observer partitions, and changed witness bindings.
Replay makes no model calls.

## Formal evidence and remaining work

From `lean4`, compile `WitnessedDifference/CertifiedProgress.lean` with Lean
4.33.1. Its 23 printed declarations prove reachability, losing-trap soundness and
existence, ranked certificate soundness, and exact rational optimality from the
stated upper and lower certificate laws. Its axiom union is `propext`,
`Classical.choice`, and `Quot.sound`; it contains no `sorry` or custom axioms.

`BeliefGameQuotient.lean` adds 16 audited declarations proving two-sided game
transport, achievable-budget equality, optional-action monotonicity, and a
constructive greatest finite stable relation which remains an equivalence for
an equivalence seed. The aggregate spine has 33 modules and 493 declarations.

This is mechanization of a mathematical game model. It does not verify the
Python implementation or concrete producer's horizon construction. The sharper
partition block-round bound is a written proof and an executable check;
the Lean relation algorithm uses its finite seed-pair count as the bound.

Run `python -B -m certified_progress.replay` with `code` on `PYTHONPATH` to
replay the retained eight accepted certificates and seven rejected mutations.
Replay requires no model calls. `--write` generates fresh proposals and saves
their independently checked witnesses; it is distinct from replay.

A game loss alone does not establish that an external source problem has no
solution. That interpretation also requires solution coverage and sound target
transport from the faithful-representation theorem.
