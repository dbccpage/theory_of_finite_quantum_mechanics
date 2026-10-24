# Review of the Majorana campaign proposal

AuthorityEffect: None. AI review, awaiting human review.

Scope: `FSP-MAJORANA-CLIFFORD-PARITY`, against base
`637ed588908dd2848ea4c71af8f9c86480a90aeb`. Generated source metadata for the
previous imaginary-fugacity contribution is also refreshed by the required
pipeline; that source, its exception, and its mathematical claim are unchanged.

Method: read the full retained target statement and obligation, the new Lean
module and its imports, the independent checker, replay receipts, and the
derivation note. The scoped Lake build was run outside the overclaim-hunter
skill, before this review. This review uses that receipt; the skill itself
does not build Lean. The full repository Lean library and Rust application
workspace were not rebuilt. This is not independent human review.

Result: **0 FULL, 1 NARROWED, 0 OVERCLAIM** for the changed target. No node
status, original statement, imported structure, or pre-existing scope fence
is changed. The campaign classification remains provisional.

## Per-node claim table

All Lean line references below are in
`lean4/CampaignMajoranaCliffordParity.lean`.

| Atomic source claim | Declaration and actual scope | Verdict |
|---|---|---|
| CAR modes decompose into self-adjoint Majoranas | `gamma_star` at line 70, with `CARFamily` inputs at line 48 | NARROWED to the declared complex star-algebra model |
| Anticommutators are twice the Kronecker delta | `gamma_ac` at line 74, arbitrary index type; index count at line 205 | NARROWED to the declared CAR hypotheses |
| Majoranas generate the Clifford algebra on the stated number of generators | `recover_c` at line 84, `recover_star_c` at line 90, `generated_algebra` at line 98 give equality of concrete complex generated subalgebras | Abstract Clifford identification NOT PROVED; finite matrix span ranks are computational witnesses only |
| The signed Majorana-pair product is fermion parity | `localParity_pair` at line 150 and `parity_product` at line 177 give the ordered product identity | NARROWED; no unordered-product or basis-completeness theorem |
| That product equals the particle-number parity operator | `parity_action` at line 191 gives its sign on a supplied common occupation eigenvector | Full operator/Fock identification NOT PROVED |
| The historical manuscript infers physical superselection | `oneCAR` at line 213, `oneRho_posSemidef` at line 249, and `parity_superselection_not_forced` at line 266 provide an unrestricted-state countermodel | No physical superselection theorem; the existing postulate fence is retained |

The precise narrower statement is: in the declared complex star-algebra CAR
model, the Majorana formulas are self-adjoint, satisfy the Clifford relations,
generate the same complex subalgebra as annihilators and creators, and give
the local parity factors and their ordered eigenaction. A one-mode positive
trace-one density matrix does not commute with the declared parity. The
target's original broader statement is retained, not replaced by this statement.

The original bottleneck remains as a prefix. Its added scope names the
unproved all-mode abstract Clifford identification, source CAR/Fock refinement,
and occupation-basis completeness. Parity superselection remains a physical
postulate. These are not discharged by the bounded Jordan-Wigner rank checks.

## Corrections to the proposal's own text

The development distinguishes generated-subalgebra equality from an abstract
Clifford isomorphism, and ordered eigenaction from a total-number operator
theorem. The countermodel concerns unrestricted density matrices, not a
refutation of a theory with a separately imposed state/observable restriction.
The derivation note at `dag/derivations/independent/fsp-majorana-clifford-parity.md`
keeps those distinctions in its calculation and its final scope sections.

During development the axiom-output parser initially missed the axiom-free
`ac_comm` output format. The saved successful build was reparsed to include
that declaration. No source change, admission, or extra axiom was needed.
The replay also now supplies the evidence mapper's required per-result
`axiom_audit_passed` flag, in addition to the detailed top-level audit. This
avoids treating a successful scoped replay as an unaudited receipt.

## Numbers recomputed

| Claim | Exact route | Result |
|---|---|---|
| Matrix dimensions for mode counts from zero through four | Independent `audit`, `dimension = 2**modes` | 1, 2, 4, 8, 16 |
| Majorana counts in those cases | Actual constructed list lengths | 0, 2, 4, 6, 8 |
| Monomial span ranks through three modes | Exact SymPy matrix rank over Gaussian-rational entries | 1, 4, 16, 64; no rank assertion at four modes |
| Density entries, trace and commutator entry | Lean matrix declarations at lines 228–268; independent `counterexamples` | Entries 1/2, trace 1, commutator entry (0,1) equal to 1 |
| Mutation and invalid-bound checks | Independent runtime checks under normal and optimized Python | Three designated mutations detected; five invalid bounds refused |
| Printed declaration audits | Compare every terminal `#print axioms` command with captured build output | 32 matched; each uses a subset of propext, Classical.choice, Quot.sound |
| README and manuscript census | Required readme-facts and results-audit generators, checked after sync | Counts regenerated from repository data; statuses unchanged |

Identifiers, source line coordinates, toolchain versions, hashes, and the
queue rank are custody metadata rather than new numerical physics claims.

## Scanner and remaining limits

The mechanical scan and the evidence map are recorded with the campaign
checks. The scan reported HIGH=0, MEDIUM=0, LOW=3. Findings require semantic
reading; a quiet scan does not establish
the full node statement. The existing baseline is not widened by this review.
The LOW findings are historical: R10 for five tensor modules without replay
receipts, R5 for the date-like token `20261019` in the tensor-uniqueness note,
and R5 for `1/2` and `1/4` in the older tensor-countermodel note. Those modules
were not rebuilt and those older matrix values were not independently
recomputed in this review. Required tensor receipt repinning exposes these
records to the diff scan; this proposal does not certify their full claims.
Exact-source acceptance exceptions, if separately approved, concern only
code governance and confer no mathematical status.

Acceptance update: the human explicitly approved the three new exact-source
exceptions. The two governed sources received CLI-generated FLOOR entries;
all 8155 original entries and every existing support pin were retained.
The independent checker's exception is bound in the separate authorization
receipt. The proof/checker remain L3D and the build configuration L1D; the
global L4/D floor and all mathematical scope fences remain unchanged. This
permission is not a human mathematical review.

The scanner cannot decide whether the imported CAR representation is the
intended finite source model, whether a real rather than complex Clifford
algebra was intended, or whether a physical superselection postulate is
appropriate. Those questions remain open to human review.
