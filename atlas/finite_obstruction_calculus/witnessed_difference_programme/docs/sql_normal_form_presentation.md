# An executable finite normal-form presentation

AuthorityEffect: None. This closes one selected AutoP/PTIR-to-SQL path for
`nf.classical.bcnf` version `v0`. The general shared mathematics language,
all five enlarged Genesis obligations and the physical continuum remain open.
The finite mathematical arguments below are written; no additional Lean
formalization or whole-compiler soundness theorem is claimed.

## The protected question and admitted carrier

Let U be a finite heading, F a supplied finite set of functional dependencies,
and R a set of tuples with that heading. Equality of attribute values is exact.
The schema question concerns every relation satisfying F; the instance question
concerns the supplied R. They are separate even when R is empty or a singleton.

The native profile admits 1–8 attributes, at most 128 input FDs and 128 tuples,
with an explicit decision budget. SQL values are UTF-8 text atoms of at most
1024 bytes, without NUL or NULL. Duplicate input tuples are refused. Heading
identifiers contain only uppercase ASCII letters. The reconstruction target is
the original set of tuples, with its heading, rather than source-file order or
JSON formatting. It is not a bag, numeric normalization or Unicode quotient.

For two nonempty subheadings U1,U2 covering U, the forward map is
P(R)=(projection_U1(R),projection_U2(R)). The proposed recovery map J is the
natural join in original heading order. The contract protects all original
rows; it separately reports projected normal forms and dependency loss.

## Closure has a certificate and a countermodel

Start C at X and repeatedly add Y whenever an input FD A→Y has A contained in
C. The ascending chain terminates on finite U. Each effective application is
recorded with its input-FD index. The independent closure verifier replays
those applications and checks that the final C is closed under every FD.
An application adds only attributes implied by X; every closed superset of X
contains the constructed C. Thus the replayed C is the least closed superset.

For completeness, if b is outside C, take two tuples agreeing with value 0 on
C, with values 0 and 1 respectively outside C. Each admitted FD holds: either
its determinant includes an attribute outside C, so the tuples disagree there,
or the determinant is inside C and closure puts its dependent inside C too.
But X→b fails. This proves the usual FD implication criterion by a concrete
two-tuple countermodel. It uses the declared FD-only theory with unrestricted
text domains, not additional singleton-domain or application constraints.

For each component V and every X contained in V, compute C_F(X) intersected
with V. Its nontrivial part gives X→(C_F(X)∩V)−X. These enumerate a cover of
the projected FD theory, including implications not listed directly in F.
The component is BCNF exactly when every nontrivial such closure is all of V:
the determinant is then a superkey. Empty determinants are included.

## Binary lossless recovery is a universal schema property

Put S=U1∩U2. The binary split is lossless for every F-legal relation exactly
when C_F(S) contains U1 or U2. Suppose it contains U1. A joined tuple comes
from original tuples t1,t2 agreeing on S. They must agree on U1, so that
joined tuple is t2 itself. Projection puts every original tuple in the join;
therefore J(P(R))=R for every legal R. The other case is symmetric.

Conversely, if neither component is contained in C_F(S), use the two legal
tuples from the preceding closure construction. There is an attribute outside
the closure in each component, and every such attribute is outside S. Joining
the first tuple's U1 projection with the second tuple's U2 projection gives a
tuple different from both originals. It agrees on S but is spurious. Thus the
criterion is also necessary in the stated FD-only theory.

For a lossless split satisfying the stated FD criterion, P is injective on legal relations, J is its left inverse, and
P∘J is the identity on the actual image of P. This is a concrete finite
presentation closure. Arbitrary pairs of component relations are outside that
image unless independently checked; they are not silently admitted updates.

## Dependency preservation is a separate decision

Let G be the union of the two complete projected FD covers. Every FD in G is
implied by F. The converse holds exactly when G implies each original FD;
closure under G decides that question. Together these inclusions give
G+ = F+ when preservation succeeds. A missing implication is retained as a
lost input dependency, rather than concealed by a successful join.

For R(A,B,C), F={A→B}, the split (A,B),(A,C) is lossless, both components
are BCNF, and the dependency is preserved. For the existing contract's
(S,J,T) counterexample, F={SJ→T,T→J}, the split (J,T),(S,T) is lossless and
BCNF but loses SJ→T. The locally legal component relations
{(j,t0),(j,t1)} and {(s,t0),(s,t1)} join to a global SJ→T violation.
Reconstructing an originally legal snapshot therefore does not license later
independent component edits. These are standard distinctions in relational
normalization; see [Toman's normalization notes](https://cs.uwaterloo.ca/~david/cs348/handout-FD.pdf).

## Existing AutoP, actual PTIR and an executable SQL profile

The [working example](../../../../../../omega_engine_projects/wdp_sql_normal_form/fixtures/heath.atp)
uses the existing `contract` and `obligation` productions. The selected
compiler profile requires exact identity, version, SQL semantics, protected
query, recovery target, headings, FDs, components and budget. It refuses
opaque proof bodies, unknown fields and duplicate obligations. This adds a
typed profile to the existing compiler without introducing a second grammar.

The native checker computes the decisions above and checks the actual rows.
It constructs real PTIR object/morphism nodes and a projection/join diagram,
binding their evidence references to the actual schema, report and inputs.
The SQL backend consumes those PTIR object/morphism roles, requires both
projection and reconstruction, and checks their evidence and endpoint binding
before lowering. Unsupported or incomplete operation plans are refused.
The generic PTIR hashes and Betti field remain custody/structure fields;
the FD theorem is supplied by the relational checker and the written proof.

The artifact retains actual contract/source/instance/checker-input hashes,
both projected relations, the decision report, PTIR fingerprints and emitted
SQL. Native verification recompiles from the original source and rows and
compares the entire typed artifact. It does not accept a supplied PASS flag.
The CLI also binds its executing binary and rechecks its inputs after checking.

The SQL profile uses SQLite 3.37 or newer, `STRICT, WITHOUT ROWID` tables,
all-column primary keys, explicit `NOT NULL` and `COLLATE BINARY`, parameter
binding and `SELECT DISTINCT`. [SQLite's STRICT documentation](https://www.sqlite.org/stricttables.html)
still permits type coercion; native admission therefore rejects nonstring
JSON values before SQL insertion. [BINARY collation](https://www.sqlite.org/datatype3.html)
compares actual text bytes; composed/decomposed Unicode and case variants are
retained as distinct atoms. Numeric-looking text is not parsed as a number.

The [independent replay](../../../../../../omega_engine_projects/wdp_sql_normal_form/code/replay.py)
executes the generated schema and projections, compares them with the native
sets, executes the join, removes the original table, and reconstructs again.
It records the actual SQLite version/source ID and binary/input SHA-256s,
then rehashes the retained files even after a failed subprocess. Generated
SQL supplies the set/text storage profile; it is not a general SQL constraint
enforcer for arbitrary later edits.

## Ownership and evidence ceiling

`omega_category_theory::finite_functional_dependencies` owns closure,
projection, BCNF, binary lossless/dependency-preservation decisions and finite
instance operations. AutoP owns profile admission, actual PTIR construction,
SQL emission and native artifact replay. WDP retains declared data and recovery
targets in a thin adapter; it does not implement another FD algorithm.

Focused verification has eight new native checks and twenty-two actual
native/SQLite Python checks, including text exactness, the loss counterexample,
empty instances, altered transports/certificates, incompatible targets,
budget refusal and retained-input mutation during SQL execution. The exhaustive
Boolean relation test is bounded evidence; the universal schema argument is
the separate written proof above. The complete normal-form contract is not
reclassified as fully verified from this one profile. A second domain, richer
dependencies, mutable migrations, general proof checking and full source
refinement remain separate work.
