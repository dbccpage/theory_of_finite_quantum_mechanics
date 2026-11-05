# Causal-QFT finite checker review

AuthorityEffect: None.

The three `cqft-*-import.py` files, the new shared `rational_matrix.py` and
`test_cqft_checkers.py` receive retention label **5** and completed **L4B**
assessments bound to their exact source bytes. Their adjacent companions and
the executed mutation manifest receive **5**. Earlier companion entries remain
unchanged. A label is a retention decision, not a perfection claim.

## Repairs and composition

The matrix helpers validated immutable snapshots but then indexed the original
caller data. Their integer components also lacked a bit budget. The new frozen
`RationalMatrix` owns detached rational rows, admits dimensions 1..64 and
components up to 4096 bits, and bounds every dot-product intermediate. Tensor
dimensions are checked before constructing output. Expected shape, domain,
singularity and resource failures use the shared Railway boundary.

Matrix addition, multiplication, transpose, tensor products and small inverses
now share that one implementation. The independent tests use SymPy expressions
and separate bit-insertion formulas; shared production helpers are dependencies,
not independent confirmations. Integer-only boundaries remain integer-only;
the local-net flat2 API retains its prior exact rational inputs. Integer exports
refuse nonintegral values. Each code file has at most one class.

The causal ordered-product helper now snapshots and validates its assignment
and factor list, including unused assigned matrices, bounds both to 64 entries,
and rejects missing/invalid point identifiers before multiplication. Unimodular
inversion explicitly admits determinant +1 or -1. The Reeh checker snapshots
all eight coefficients and validates all three full-system input states before
indexing. Its bit-placement map no longer applies a redundant modulo operation
after validating the bit domains.

Duplicated manual counters now use `Cases`, with exact bool admission and
per-invocation ownership. Causal/Reeh section interfaces retain their
`(executed, failed)` summaries; the local-net application now emits a structured
JSON receipt with failure names. The constant identity-cell sentinel was
replaced by full left/right identity-product checks. Nested scans were composed
with finite Cartesian products, and the N-order extension predicate was reduced
to its pairwise condition, bringing every reviewed function within B thresholds.

The causal header claimed a cocycle check for both matrix families, but only
one was checked directly. The second now contributes 112 direct cocycle
obligations. All 16 diamond-order point pairs are independently checked against
its height-order description, covering orientation and diagonal/spacelike
behavior. The total is now **923 = 484 + 32 + 407**, compared with the historical
795. Local-net reports **84 = 71 + 8 + 5** executed obligations. Reeh retains
**252 = 227 + 24 + 1**. Conjunctions count as one executed obligation.

## Claim and consumer boundaries

All three Lean origins were read in full. The causal Python file checks two
supplied integer matrix families and fixed finite orders; its general group
theorems stay in Lean. Local-net constructs one four-point order and two-site
integer operators, without a continuum region index. Reeh checks unnormalized
integer state representatives, recorded kernels and supplied left inverses;
the abstract cyclicity/separation proof and translation-aliasing theorem remain
in Lean. Finite translation invariance is not continuum analyticity.

The three executable paths and regression-tested matrix/site interfaces remain
available. Internal local-net fixture functions were composed after a caller
audit. Historical DAG/evidence files keep their original source hashes, counts
and scientific statuses; current execution receipts do not rewrite them. The
requirements map binds all origins, current consumers and nested-declaration
ownership. No continuum AQFT result, Lean rebuild or hosted CI run is claimed.

## Verification

Strict pinned mypy passes on all five files. Fifteen CQFT test groups and all
24 integration groups pass under normal and optimized Python; every generated
property runs 80 deterministic cases. Separate symbolic matrix and bit-insertion
oracles cover rectangular products, inverses, tensors and unfoldings. Tests
also cover direct-constructor and factory ownership, exact scalar domains,
resource thresholds and preflight, integer export, missing keys, full carrier
pairs, false mathematical controls, CLI failures and cancellation.

The initial 69-candidate mutation campaign killed 64 and retained five
survivors. Three exposed missing challenges: direct-constructor aliasing,
Boolean factor indices whose coerced key is present, and an untested diamond
edge. Tests and the full finite-order cross-check were strengthened. The entire
69-candidate campaign was rerun: **67 killed, two equivalent**. One bypasses an
initial column screen while the complete row-admission screen still refuses
the same inputs. The other removes the explicit unimodular screen, while
integer export of the inverse still refuses every nonsingular nonunimodular
integer matrix. Exact equivalence arguments, both manifests, initial source
bytes and all raw outcomes are retained; the eligible detection rate is 67/67.

A local type annotation was added after the rerun snapshot because strict mypy
could not infer the mixed rational/integer nested list. Removing that exact
annotation reproduces the complete test bytes used in the mutation campaign;
it has no runtime evaluation. The initial passing quality run, intervening
typing failure, final passing run and annotation amendment are separate records.
Source-checkout postflight is recorded separately after guarded synchronization.
