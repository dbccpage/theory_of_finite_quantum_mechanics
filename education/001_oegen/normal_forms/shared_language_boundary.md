# A shared contract language: normal forms before new syntax

AuthorityEffect: None. One selected existing normal-form contract now lowers
through AutoP/PTIR to checked SQL reconstruction. The broader shared mathematics
language remains an implementation programme with additional domain obligations.

The useful common language is a language of declared carriers, protected
questions, maps, admissible changes, certificates and refusals. WDP supplies the
witness discipline; mathematical crates supply operations; CODA, LGGR, Prime
and DDC supply distinct evaluation and continuation profiles. Their common
interface need not erase the differences among those profiles.

## Reuse the compiler and contract estate

The [AutoP grammar](../../../../omega_simplex_autop/grammar/atp_grammar.ebnf) already declares structures,
transformations, witnesses and obligations and labels future constructs.
Its proof bodies are opaque. The [compiler root](../../../../omega_engine/crates_rs/auto_p/lib.rs)
also labels several deleted-subsystem stubs. The
[Proof-Carrying Topological IR](../../../../omega_engine/crates_rs/auto_p/compiler/ptir.rs)
already carries nodes, proof hashes and dual-witness flags. Those fields refer
to evidence; a hash authenticates supplied bytes, and a conjunction of supplied
flags is not independent mathematical verification. A production profile needs
an explicit binding to the checker, original problem, result and toolchain.

Extend that existing lowering path after selecting a concrete profile. Do not
infer parser support, soundness, actual engine execution or proof checking from
an EBNF production alone. The [normal-form standard](../../014_normal_forms/contracts_nf_standards/standard.yaml)
already distinguishes reconstruction targets and decision subjects; use its
IDs and version semantics instead of assigning new meanings to APNF or IRNF.

## The semantic contract

| Declaration | Why the checker needs it |
| --- | --- |
| Stable form ID, version and profile | A SQL schema normal form, a quotient representative and a trace normalization have different decision problems. |
| Carrier, coefficient domain and equality/equivalence | A rational matrix, finite relation and SQL bag are different carriers. State their exact or approximate semantics. |
| Protected queries/invariants and admissible edits | A canonical representation may preserve current reports while losing data needed for future source edits. |
| Forward map, reconstruction target and retained data | Declare whether recovery means the original value, an equivalence class, a representative, an invariant or a replayed artifact. Preserve transport/fibers/history when needed. |
| Dependencies and preservation/loss evidence | Local checks need not imply all global dependencies. List preserved queries and explicit losses for every transport. |
| Certificate, checker and source binding | Replay evidence against the original problem; neither an asserted flag nor a digest supplies a missing proof. |
| Decision mode, budget and refusal | A complete decision procedure, certificate checker and bounded search have different ceilings. Exhaustion remains unknown. |
| Policy and authority boundary | Evaluation and admissible mathematical proposals do not supply operational authorization. |

## SQL is a good first target

Choose one existing relational normal-form/decomposition contract and a named
SQL dialect. Specify set versus bag semantics, keys, NULL behavior, supported
dependency language and exact numeric encodings before making preservation
claims. A missing dependency annotation must not become an inferred theorem.

For example, under set semantics and the declared dependency `A -> B`, split
`R(A,B,C)` into `R1(A,B)` and `R2(A,C)`. The contract should bind the projection
and join maps and check reconstruction on every legal relation under that
dependency. A current instance round-trip alone is only an instance check.
If SQL uses NULLs, bags or a wider dependency theory, provide the corresponding
semantics and evidence instead of silently borrowing the set-relational result.
SQL constraints and generated queries implement a profile; they are not a
general proof backend for HoTT or arbitrary mathematical statements.

The first complete milestone is: one versioned contract through AutoP/PTIR,
SQL storage and queries, an actual native certificate check, independent replay,
and rejection of altered data or an incompatible reconstruction claim. The selected milestone is now delivered by the
[native/SQL presentation](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/sql_normal_form_presentation.md) and its
[normal form standards](../../014_normal_forms/contracts_nf_standards/normal_forms_schema.sql). Eight native and
twenty-two actual compiler/SQLite checks pass. It admits immutable text sets,
FDs and binary splits, separately reporting BCNF, lossless join and dependency
loss. It does not certify arbitrary future component edits or every normal form.

## Where the three mathematical tools belong

HoTT can describe identities and transport, sheaves can describe compatible
local reports and their global extensions, and cohomology can record a specified
obstruction under declared coefficients. These roles fit the current owners;
they do not require reimplementing all three foundations before useful work.

Start with actual finite restriction maps, their identity/composition laws,
declared covers and checked extension fibers. For cochains, check shapes,
`d1*d0=0`, the original defect, exact primal/dual certificates and the meaning
of the chosen obstruction. Zero in an incomplete detector is not global green.
Full univalence, higher coherence and general infinite constructions remain
separately declared obligations and backend profiles.

This division has established precedents. Spivak's
[Functorial Data Migration](https://arxiv.org/abs/1009.1166) gives categorical
schema/instance and migration semantics. The
[HoTT book](https://homotopytypetheory.org/book/) develops the type-theoretic
foundation; its results require the stated foundational assumptions.
Abramsky and Brandenburger's
[sheaf treatment](https://arxiv.org/abs/1102.0264) gives a precise global-section
obstruction for their empirical-model setting. The related
[cohomology paper](https://arxiv.org/abs/1111.3620) makes nonvanishing sufficient
but not necessary for contextuality in its construction. Its zero class is
therefore not an automatic global-section certificate. Transporting any of
these results to another carrier requires an actual map and a preservation
argument.

## Spend time on semantic preservation

The first selected lowering and replay path now works. The next useful work
is a second actual domain using the same interface with preservation evidence. Further keywords, a new foundational
kernel or a universal claim about twenty disciplines should wait until those
paths show which abstractions are actually shared. The
[Genesis/WDP crosswalk](../wdp_integration.md) and
[native owner map](../../../../omega_engine_atlas/coda_atlas/F004_papers/001_finite_obstruction_calculus/000_witnessed_difference_programme/docs/native_owner_decomposition.md) keep the central reference connected
to its current implementations.
