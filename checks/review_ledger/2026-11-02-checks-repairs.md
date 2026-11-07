# Repairs and retest of the first 25 reviewed checkers

AuthorityEffect: None.

The executable defects and misleading checker descriptions recorded in the
first twelve review batches have been repaired. This report supplements the
original reviews; their bytes and the historical contract/score entries are
preserved. No physics target, DAG status, theorem, or authority ceiling is
promoted by these changes. The original review cursor remains at
`dfm-electroweak-continuum-fence.contract.score.yaml`.

## Repairs by source

| Source in `checks/independent` | Correction and regression coverage |
|---|---|
| `ads-cft-duality-import.py` | Replaced optimization-stripped assertions with active guards. The constant-mass mutant is rejected. Exact rational boundaries reject floats/bools. Corrected the unmultiplied ribbon-weight factorization; limited the BF/discriminant description to what the checker executes. Corrected the source checkout's derivation-note count from 963 to 829. |
| `ads-happy-toy-not-duality-gap.py` | Validates qubit regions, generator domain, interval bounds, disjointness and Renyi orders. Split census, Renyi and mutual-information checks. The model is explicitly hand-encoded; independent network identification is not claimed. |
| `ads-regge-area-rt-gap.py` | Requires positive integer subdivision counts; retains exact Fraction division. States that geometry/triangulation counts are supplied. Shares the tested finite mincut model. |
| `ads-rt-formula-import.py` | Replaced float/log/round examples with exact symbolic logs and a reduced-rational square certificate. Enforces positive Newton constant and valid interval/radius/area domains. General Baker-dependent transcendence is not inferred from samples. |
| `auth-dtm2-input-request-planned.py` | Import-safe, per-run closed fixture; active failures propagate through the Railway/CLI boundary. Does not claim an encoder/decoder or an infinite-machine theorem. |
| `auth-rice-theorem-import.py` | Immutable behavior table and explicit code/index validation, including boolean rejection. |
| `authf-carrier-admission-gate.py` | Import-safe, per-run closed status fixture. Does not claim live candidate-record validation or carrier admission. |
| `check_tfq_1050_fqcd_wilson_dirac_gamma5_hermiticity.py` | Whole rational parameters appear in case IDs; duplicate IDs are rejected. Exact determinant inputs reject floats/bools. Clifford matrices, links, operator assembly and gamma-five checks are named components. The 2D description now says chiral-sign checks. |
| `check_tfq_1052_fqcd_strong_coupling_area_law.py` | Split the CCN-89 runner into 24 named domain checks with explicit dependencies. Fixed the reversed inequality description. Exact unit-phase powers handle charges -4096..4096, including +/-4. Added exact/domain/resource boundaries and unique case IDs. Character tables are declared supplied data; the two omitted 2I cancellation groups are each 24 elements, giving total 120. Uniqueness is limited to displayed comparisons. |
| `check_tfq_1219_fsp_hinge_lineon_sign_claim.py` | Validates integer unit hops and trajectories. Invalid/colliding trajectories cannot masquerade as odd permutation parity. Gaussian values and matrices are separate immutable value objects. Curvature is exact symbolic acos on [-2,2], with no clamping. Adds an SU(2) unitarity check, unique IDs, and explicit toy-map/two-label/sign-convention descriptions. |
| `comp-c2-step3-not-word-step.py` | Import-safe fixture; shared exact one-hole replacement refuses an invalid split instead of returning a fabricated word. |
| `comp-c3-no-fixed-bound.py` | Retains the bounded no-rule fixture and explicit exit status; compressed repeated length comparisons. |
| `comp-c6-tm0-output-form-open.py` | Import-safe, per-run fixture with active failure propagation; retains the toy-writer scope. |
| `comp-c7-encoded-instance-reduction.py` | Import-safe, per-run two-code fixture; no general computable reduction is claimed. |
| `comp-c7-fixed-target-open.py` | Import-safe fixture using the same independently tested split validation as C2. |
| `comp-c8-minimality-fence.py` | Import-safe, per-run tape fixture with explicit failures. |
| `cqft-causal-factorization-import.py` | Unimodular inverse and matrix shapes are checked in both interpreter modes. Counterterm range corrected to 0..6. |
| `cqft-local-net-axioms-import.py` | Rejects malformed matrices and points outside the four-point carrier. Split order axioms, pair counts, single-site and tensor-product checks. |
| `cqft-reeh-schlieder-theorem-import.py` | Explicit nonempty rectangular shape and multiplication checks, coefficient length/site validation, and an unnormalized-representative convention. Split the census by subsystem. |
| `ct-information-media-interoperability.py` | Import-safe and optimization-safe; the identity-for-controlled-flip mutant fails. Classical assignment cloning remains a finite functional fixture. |
| `ct-local-mediator-entanglement-import.py` | Active symbolic checks reject the simplifier mutant. General concurrence divides by the squared state norm: u=0 gives 4/9. The zero-determinant M00=0 charts are also checked. |
| `dfm-bphz-continuum-fence.py` | Import-safe; validates projector shape and distinct known forest names before computation. Durable regression checks the joint-kernel converse on 1,925 finite cases. |
| `dfm-ckm-physics-fence.py` | Immutable Gaussian-rational labels; positive non-boolean table dimensions and a six-cell enumeration budget. Retains nonzero rescaling versus physical unit-phase distinctions. |
| `dfm-continuum-interface.py` | Every transport validates and freezes all SL(2,Z) labels. Unknown edges, invalid signs, noncomposable tree paths, singular, float and determinant-2 matrices are refused. One-vertex loop words remain distinct from general typed Lean walks. |
| `dfm-continuum-refinement-limit.py` | Per-invocation counter, strict binary words, bounded nonnegative integer depths, and validated S3 permutations. Two runs both report 14,642; a failed run does not contaminate the next. |

## Architecture and independence

`checks/checker_support` owns the independent checking bounded context:
immutable `Failure`/`Outcome`, invocation-owned `Cases`/`RunCounter`, exact input
validators, and Gaussian value objects. Each class has its own file. Public
`evaluate(operation, ...)` returns a Railway outcome; internal helpers signal
declared refusals through `Violation`, and the CLI reports failures nonzero.

The duplicated one-hole replacement, Wilson determinant, Gaussian arithmetic
and hand-encoded stabilizer model are shared. Agreement between consumers of
these helpers is not independent confirmation. The durable test suite instead
uses separately constructed determinant, span, cut, collision and kernel
oracles. Production code is never imported as the reference oracle.

The regression asserts that each of the 25 checkers and 13 support modules has
no executable `assert`, no more than one class, and maximum Radon CCN <= 15.
The measured maximum is 14. This measurement alone does not certify cognitive
complexity, static typing, full branch coverage, or the other SCORING gates.

## Retest evidence

The machine-readable [retest receipt](2026-11-02-checks-repair-retest.json)
records the exact hashes of all 39 Python files (25 checkers, 13 support modules,
one regression suite), Python version, test output and exit codes.

- Normal Python: 24 test groups passed, including all 25 checker subprocesses.
- Optimized Python: the same 24 groups and 25 checker subprocesses passed.
- Independent comparisons: 8,200 lineon paths; 1,925 joint-kernel cases;
  380 interval cuts against all 64 internal-vertex assignments; 160 GF(2)
  spans; 16 Wilson determinants against SymPy Bareiss elimination.
- Four specified semantic mutants were killed in both interpreter modes:
  constant GKPW mass, identity controlled flip, constant symbolic simplifier,
  and all-positive gamma-five signs. This is a bounded campaign, not an
  exhaustive mutation or coverage claim.
- Development failures introduced during refactoring were retained in the
  receipt and corrected before the final successful runs.

`.github/workflows/reviewed-checkers.yml` schedules both interpreter modes on
Python 3.12 and 3.14. It has not been pushed or executed on hosted CI. Local
execution used the installed Python 3.14 environment. No Lean rebuild or full
repository test run is claimed.

## Contracts, labels and remaining scoring work

Every changed/new Python source has an adjacent source-bound contract. Current
assessments cite this report, the retest receipt, regression source and rubric;
the old histories remain unchanged. Known repaired E findings are recorded as
resolved for the new bytes rather than erased from history. The former
numerical angle boundary is now exact symbolic arithmetic.

The original 1-5 labels are retained as review/action labels. Newly introduced
support/test code and companions are labeled 4 pending the complete scoring
assessment. No file is called perfect. The requested **L4B floor remains
unmet**: the finite fixtures and small utilities retain their actual capability
levels; the complete five-gate/B-level evidence is not supplied by this bounded
repair suite. Current score tokens remain null, and no governance exception or
false capability promotion was added. The existing repository governance
population still excludes `checks/`.

Unimplemented broad mathematical/physical targets remain outside these repairs:
network identification, general continuum results, full BQNF classification,
categorical projection, physical statistics, live candidate validation and
general machine/reduction constructions are not established by fixed fixtures.
