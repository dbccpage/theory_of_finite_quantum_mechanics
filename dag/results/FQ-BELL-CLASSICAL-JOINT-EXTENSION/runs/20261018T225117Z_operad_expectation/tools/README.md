# Bell joint extension: staged expectation and operad run

Status: **stopped for user review after P5**. The common-positive-joint-law
implication is checked. The full historical target, including Fine's converse,
remains open. AuthorityEffect: None. Only this target was executed.

This is a local execution of the file-based PFP stage protocol by Codex, with
separate native checker processes. There were no external provider calls. This
does not measure the active chat's cost, and there was no separate human reviewer
or isolated adversarial model. `execution.json` records those limits.

## Stage receipts

| Stage | Work and retained evidence |
| --- | --- |
| P0 | `p0/request.json`, immutable `inputs/`, four narrowed missions, source review and independently pinned checker. |
| P1 | Exact certificates for 22 public rational laws; Rust/Python APIs and Lean constructions. Original candidate bytes, construction snapshots, full stage response and operad delta retained. |
| P2 | Independent stdlib certificate recomputation, Rust/Python exact agreement, 12 Python tests, 10 Rust tests, and Lean 4.33.1 compilation. Raw stdout/stderr and command receipts retained. |
| P3 | Not invoked: no mathematical candidate defect was observed. A real disk-full Rust infrastructure failure and unchanged-candidate retry remain in P2. |
| P4 | False slack, correlator, sign and binding mutations rejected; valid control accepted. Wrong-colour insertion rejected. Lean rejected the deliberately false sign equality. Missing-premise examples retained. |
| P5 | Supported operations and relations merged into the target's cumulative operad collection. Source snapshots, remaining obligations, and next mathematical step recorded. |

Each executed stage has an `operad_delta.yaml`. Checkpoint `raw_response.txt`
contains serialized local artifact bytes, not a fabricated remote API transcript.
P1 also has `response.json` for the construction and delta surrounding its domain
certificate. P2's status comes from the executed checks listed in its receipt;
it is not inferred from a model's assertion.

## Mathematical content collected

For Omega = {-1,+1}^4, in A0,A1,B0,B1 bit order, collect these typed generators:

- `response_products : () -> ResponseMap4`, returning the table
  omega |-> (a0*b0,a0*b1,a1*b0,a1*b1).
- `joint_expectation : (JointLaw, ResponseMap4) -> CorrelatorTuple`, using a single
  nonnegative normalized rational law and coordinate order 00,01,10,11.
- `chsh_linear : CorrelatorTuple -> Scalar`, taking e00+e01+e10-e11.
- The existing score-partition and slack-certificate route, now checked by
  consumers which independently recompute every component.

The graft `CHSH(expectation(p,response_products()))` has one JointLaw input.
The Lean numerator model proves generic integral-table linearity, identifies this
graft with the Bell numerator, and obtains the bound by nonnegative weighted
summation. A positive common denominator D gives -2D <= numerator <= 2D. Dividing
by D yields the exact rational interpretation. The formal Lean theorem about
arbitrary response tables is integral; a general Q-table transport theorem and a
probability-subtype packaging are still open.

`lean4/BellOperad.lean` also constructs heterogeneous function operations
`Op I A B = ((i:I) -> A(i)) -> B` and simultaneous substitution

    substitute f g x = f (i |-> g(i) (j |-> x(i,j))).

Sigma indexing makes block flattening and reassociation explicit. Units and
associativity are kernel-checked without axioms; semantic equality is stable
under substitution. Restriction to finite ordered input families gives the
nonsymmetric endomorphism semantics used here, including nullary and unary
operations. Actual Bell operations and their graft are included. This run does
not supply a named Mathlib Operad class instance, a symmetric action, or a
completeness theorem for a syntactic quotient presentation. The axiom report is
in `p2/logs/lean_3.stdout.log`; the other theorems use only the reported standard
Lean axioms, with no `sorry` or added axioms.

Generic expectation linearity does **not** imply a Bell bound for an arbitrary
response table. A constant table (2,2,2,2) gives CHSH=4. The binary-product table
is an essential hypothesis. Similarly, four positive pair laws with uniform
matching one-party marginals can yield (1,1,1,-1) and CHSH=4. They are not a
common joint law. The saved PR-box example exposes the invalid weakened premise;
it is not a counterexample satisfying the actual theorem's premises.

## Scope and next step

Supports: exact supplied-law Bell certificates; reusable native expectation and
certificate-consumer APIs; typed substitution units, associativity, semantic
congruence, generic integral-table linearity and the Bell composition in Lean.

Does not support: Fine equivalence, a reconstruction of arbitrary pair data,
physical locality or setting independence, full symmetric operad structure, or
completeness of a syntactic presentation. The arbitrary-law score-mass/slack
identities have native checks but no separate general Lean partition theorem.

The narrowest claim is the supplied nonnegative normalized rational joint-law
CHSH implication and the explicitly checked composition semantics.

After review, the next test is to define compatible binary 2x2 pair-marginal
inputs, state the complete relevant inequality family, and construct an exact
extension certificate. This run stops before that work.

## Reproduction and custody

`sources/` preserves the executed implementation and build configuration.
`inputs/` preserves P0 source bytes. `source_manifest.json` binds the complete run
inventory and current working-source hashes. The original pilot artifacts above
this run remain unchanged, apart from a navigation link in their README.

Run `py -3.9 -X utf8 replay.py --working-sources` from this directory to replay
byte custody, stage bindings, exact certificates, Rust/Python output agreement
and four mutation rejections. This writes no evidence and does not rerun
compilers. Use the recorded argv/cwd in P2 for a fresh native check; send new
stdout/stderr to a new folder rather than overwriting this run.

The `tools/` scripts and source fragments retain the actual local construction
procedure and its original absolute worktree path. They are provenance, not a
safe rerun entry point: several write initial checkpoints. Use `replay.py` for
non-mutating replay.
