# Finite orbit witness protocol

This companion evaluates complete witnesses on four orbits from the existing
four-site, two-repetition exact model at q = 5/2. It does not rerun the
historical discovery pilot and does not establish a general sign-problem
solution or an attention mechanism.

The fixed orbit selectors are 63, 3, 255 and 15. Public case labels a, b, c
and d are assigned independently of their answers. Each input supplies every
graph edge as a bare arrow, a rational weight, and the complete sign table in
orientation-mask order. It supplies no component partition, reversing-bit
list, cancelling-pair list, orbit total, aggregate partition value, average
sign or correction string. Providing the full raw inputs makes each task
solvable; they are not hidden-oracle questions.

The response must give the connected components in the declared order,
every sign-reversing coordinate, a complete disjoint opposite-sign pairing
when such a coordinate exists, and a canonical exact rational signed sum.
The scorer checks those objects against the existing model's SQL construction
and verifies each submitted pair against the supplied sign table. Merely
stating a keyword, a truthy flag, or the correct scalar total cannot pass.
Weights are constant within each supplied orbit; unequal-weight cancellation
is outside this task.

The analysis is fixed before requests: one request per available named
model, four cases per request, temperature 0, and an explicit output-token
cap. The primary reported result is whether all four finite witness checks
pass. Report each failed check, provider error, unavailable model, and
truncation separately. One request per model supports no statistical model
comparison. Serving provider, exact request, complete raw response, usage and
client duration are retained when supplied by the service. No seed is
requested and deterministic provider output is not assumed.

Run the host positive control, with zero provider calls:

```text
py -3.12 code/run_witness_benchmark.py --output-dir <new-directory>
py -3.12 -m pytest code/tests/test_witness_benchmark.py -q
```

Live mode requires named models, a positive explicit spend ceiling, and an
absolute deadline with timezone. Credentials must be inherited or come from
the explicitly supplied env file. It never discovers credentials, never
overwrites an existing receipt directory, and never retries a paid request.
The current public model catalogue supplies rates; provider routing uses
those rates as price caps. Conservative byte-based input reservations and the
output cap are retained for every dispatched request, including failed ones.
Reservations are estimated upper bounds under the stated price and token
assumptions; provider usage.cost is reported separately and is not an
independently audited account bill. Existing historical pilot files and their
prompt strings remain unchanged.

Duplicate model IDs are refused before execution. A provider-reported cost
above its reserved bound or the cumulative ceiling halts further requests;
missing cost stays unknown and its reservation is retained. The launcher must
also enforce a process deadline: a socket inactivity timeout alone cannot bound
the wall-clock duration of a streamed or slowly delivered response.

Protocol and source hashes are saved before any generation request. Keep
run outputs outside the release package during execution. The host positive
control is labeled as such and reports neither fabricated provider usage nor
model success.
All package-local executable modules, including the explicit credential
loader, and the SQL schema are bound. A source change before or after a call
halts subsequent requests and is reported as a failed source-custody check.

# Why a boundary shift is not a Meron transport proof

The established operational definition is a cluster flip that reverses the
permutation sign in a model with independent flips. Cancellation applies when
at least one such cluster occurs under the stated weight assumptions.
See [Chandrasekharan and Wiese, version 2](https://arxiv.org/abs/cond-mat/9902128v2).

A proposed identification with simplicial boundaries requires a separate,
typed transport map that preserves model weights and the observable being
computed. A cluster pairing is an involution on configurations; no such
chain-complex map is implemented or proved by this package.

Let C be a chain complex over Z2, z a 1-cycle, alpha a 1-cocycle, and b a
2-chain. Then

```text
alpha(z + boundary(b))
  = alpha(z) + alpha(boundary(b))
  = alpha(z) + coboundary(alpha)(b)
  = alpha(z).
```

Consequently, adding a boundary cannot remove nonzero evaluation by a
cocycle. A cochain alpha lives in C^1; boundary(b) lives in C_1. Adding them
also requires a declared identification, and even that does not supply a
weight-preserving, sign-reversing configuration map. These are deductions
from the chain/cochain pairing, whose definitions are given in
[Hatcher, Algebraic Topology, Section 3.1](https://pi.math.cornell.edu/~hatcher/AT/AT.pdf#page=199).
They explain an unfulfilled bridge obligation rather than a new physical
no-go theorem.
