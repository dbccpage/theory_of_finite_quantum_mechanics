# Symanzik finite-graph checker review

AuthorityEffect: None.

The repaired application and independent suite receive retention label 5 and
completed L4B assessments in adjacent source-bound contracts. Previous raw
history is preserved. Label 5 does not mean perfection.

The original fixed calculation gave the correct sums, but its public helpers
silently ignored mask bits outside the five-edge carrier and accepted incomplete
weight lists. The archived source and executable witnesses show run(32)=run(0)=4
and prod(0,(2,3))=6 instead of an input refusal.

CotreeGraph now owns an indexed multigraph with 1–16 vertices and 0–12 edges.
Endpoints and masks are admitted exactly, excluding bool and foreign values.
Parallel edges, loops and opposite edge orientations remain distinct edge
positions. Connected subsets with V-1 edges are enumerated in mask order.
Components, tree masks, cotree products and sums return Railway outcomes.
The singleton empty tree has product 1; a disconnected graph has sum 0.

Every weight is admitted before enumeration or multiplication, including
selected edges and graphs with no spanning trees. Signed and zero integer
weights are supported as an explicit finite polynomial extension. Inputs,
product prefixes and sum prefixes are bounded to 4096 bits. These conservative
limits can refuse an intermediate even when a later zero or cancellation would
make the final value fit. Expected input/resource/check failures have typed
outcomes and nonzero executable exits; cancellation and programming errors
propagate.

Component-label merging replaces the original fixed-depth union-find. Matrix
libraries are not used in production. Independent tests instead use BFS for
connectivity and an exact reduced weighted-incidence Laplacian determinant for
cotree sums with nonzero positive weights. Fixed cases separately test signs,
zeros, loops and empty products. The 12 groups include 80 deterministic examples
per property, every supplied mask, full size limits, immutable snapshots,
preflight ordering and executable failures. Strict typing and this suite plus
24 integration groups pass in normal and optimized Python. Both sources have
one class and CCN7/cognitive6/nesting2.

All 36 retained mutation candidates are detected. The initial selected-test
run missed a polarity inversion in the refusal assertion because that oracle
group still rejected the fake success through a different assertion. The
existing negative-input group detects the inversion directly. The follow-up
changes only test selection, with unchanged source, suite and manifest hashes;
the original 35 detections and one survivor remain in the raw receipt.

The default executable records 22 obligations: the three-edge mask list, ten
component decisions, the spanning-tree list, eight individual omitted-edge
products and two sums. It preserves sums 247 and 8. The complete Lean origin
and derivation note were reviewed. Runtime support for other bounded graphs
does not generalize the fixed-graph Lean theorem. QED loop coefficients, the
fine-structure constant and continuum integrals remain open; no scientific DAG
status, new Lean build or hosted-CI result is claimed.
