# Signed triangle switching review

AuthorityEffect is None.

The original script and its declared Boolean Lean model agree on the fixed
three-cycle switching calculation. The old matrix helper accepts bool and
float entries; the initial review records both probes. Its source and full
contract history are archived before repair.

SignedTriangle now owns the three exact edge signs, their adjacency matrix,
cycle product and constructive normalizing gauge. Switching returns an owned
triangle through Outcome. The application owns all eight triangles and keeps
full matrix conjugation through the existing bounded RationalMatrix backend.
Each of its 64 switchings is compared against the edge-switching API.

The original CLI output is preserved. The result API records 145 guard calls,
including 64 full-matrix comparisons, 64 cycle controls, 8 chosen-normal-form
controls, 8 classifications and one population control. A recorder checks the
actual calls across repeated runs.

The independent suite exhausts all 64 graph/gauge cases using SymPy diagonal
conjugation and Boolean parity, and all 512 pairs of gauge actions. It verifies
four-element orbits and positive reachability. 80 deterministic generated
matrix pairs compare both legacy and Outcome queries with symbolic products.
Shape, scalar, sign, resource, ownership, preflight, CLI, import and
cancellation cases exercise the component boundaries. Product and prefix
overflow are tested even when a later sum would fit.

Strict typing and 10 new groups plus 24 prior integration groups pass normally
and optimized. All 38 critical faults are detected. They include matrix order,
unadmitted rational inputs, three-dimensional shape budgets, stale counters,
disabled guards, shared matrix product/prefix budgets, a disabled refusal-test
helper and corrupted Boolean/matrix oracles. The earlier passing test stage is
retained before the additional intermediate-product cancellation case.

The source review reads SignedTriangleSwitching.lean and its exact hypotheses.
This phase records Python verification and source correspondence. A fresh
Lean build and hosted CI have separate receipts. The claim covers vertex-sign
switching on the declared triangle; a bordism or fermionic sign argument
requires its own model and representation class.

The helper, application and suite have retention 5 and completed L4B records.
The next file is fsp-discrete-wdw-constraint.py.
