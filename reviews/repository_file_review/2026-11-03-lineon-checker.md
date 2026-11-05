# Hinge-lineon checker repair and assessment

AuthorityEffect: None.

The entire TFQ-1219 checker, its companion, formal path/scalar declarations and
consumer references were reviewed. The repaired source, adjacent companion,
new contract suite, its companion and mutation manifest receive file label 5.
Both Python artifacts have completed L4B assessments for their stated finite
interfaces. Label 5 is a retention decision, not a perfection claim.

## Repairs

- Hop validation discarded its snapshot and then iterated the caller's mutable
  collection. The frozen `LineonPath` now owns validated nested tuple snapshots
  and computes order from exact relative distance. Trajectory validation also
  returns a detached tuple, which the witness finder actually uses. Tests clear
  caller lists immediately after snapshot admission to expose the old defect.
- Positions admitted arbitrarily large integers. They now have a 4096-bit
  boundary, checked before collection processing. Both hop and trajectory
  collections retain the 4096-entry budget. Unit moves and malformed descriptions
  are validated before a mathematical false result for unordered paths.
- Projection, defect-mass and routing helpers accepted floats or truthy flags.
  They now admit exact rational values and exact booleans; both routing flags are
  checked before short circuiting. Squaring directly replaces duplicated `abs`.
- Invalid commutator operands could raise `AttributeError`. Both exact matrix
  types are validated before inversion; singular/resource failures use the shared
  Railway boundary and are tested on each operand.
- Callbacks, orchestration handoffs, return values and CLI status are typed.
  The routing result has a closed two-label type. Redundant separator blocks are
  removed while meaningful fixture comments remain.
- Symbolic curvature now simplifies only the five integral traces and constructs
  other rational angles with `evaluate=False`, avoiding an implicit symbolic
  simplification job. It remains exact, rejects traces outside [-2,2], and does
  not claim SU(2) membership or a numeric error model.
- The header now distinguishes commuting and Pauli examples from the positive
  noncommuting SU(2) counterexample. Phi1 is labelled a sign indicator. The
  legacy collision witness explicitly prefers a site meeting, then an edge
  crossing; it is not an earliest-event finder or a general collision query.

The previous shared Gaussian value-object repairs, unitarity control, unique
case IDs, undefined-parity refusal and removal of numeric angle clamping remain.
No shared matrix implementation is presented as an independent confirmation.

## Verification

Strict pinned mypy, 15 new contract groups and all 24 first-25 regression groups
pass in normal and optimized Python. Properties use 80 deterministic examples:
site/edge collision references, translation, generated swap witnesses, separate
SymPy matrix multiplication/inversion, rational projection/mass/routing rules,
symbolic-angle structure and named receipt accounting. The original suite
retains the independent 8,200-path enumeration. Negative controls exercise
malformed domains, bit/length extremes, snapshots, singular/invalid matrices,
short-circuit flags, exact angle endpoints, failed CLI results, resource errors,
cancellation and subsequent clean invocation. The refusal assertion helper is
itself challenged with a successful operation.

All 48 retained critical-path mutations are detected. The original selected-test
campaign recorded 46 kills and two survivors: its 80-example path property alone
missed a site-collision boundary and a wrong distance update. The existing fixed
positive/negative fixture suite detects both. Their selectors now include that
suite; source and test bytes did not change for this closure. The original
manifest, raw outcomes, added selectors and reruns are retained. No equivalence,
invalid candidate, timeout or omission is hidden in the 48/48 denominator.

## Actual claim and cost

The unchanged default receipt has 77 unique obligations: 52 path, 14 matrix,
9 projection/routing and 2 Y-junction cases. A conjunction is one obligation.
The legacy witness pair remains `(found,index)` with -1 for no exchange. Site
witnesses take priority even over an earlier edge crossing.

The Lean `TwoLineonConfig` stores ordered endpoints; its site-IVT theorem assumes
a relative-coordinate step bound of at most one. This Python interface admits
simultaneous unit hops, hence also reports an edge crossing. Neither interface
establishes a physical sign-free Hamiltonian. Projection is a defined scalar
toy map, routing a two-label fixture, and the Y-junction exchange sign a supplied
convention. DAG/formal statuses are unchanged; no Lean build or hosted CI run
is claimed.

Paths and trajectories use linear work in at most 4096 entries, positions begin
with at most 4096 bits, and updated coordinates require at most 4097 bits.
Holonomy is a fixed 2x2 computation under the shared Gaussian component budget.
Curvature constructs one bounded symbolic expression or returns a known
constant. The sole production class owns its immutable path data; each checker
invocation owns its Cases. Reproduce using the pinned requirements/workflow and
the mutation snapshot protocol in `checks/tests/README.md`. Adjacent contracts
bind every declaration, origin, consumer audit and evidence receipt while
preserving historical entries.
