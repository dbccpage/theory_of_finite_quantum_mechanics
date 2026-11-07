# File review: the first four AdS/CFT independent checkers

AuthorityEffect: None.

## Scope and method

Reviewed on 2026-11-02. The requested source checkout is
`C:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics`, at Git HEAD
`e45ed2e133920aa3790af8c5e072ee9829898490`; other parts of that checkout have
unrelated changes. The four files below were clean in that checkout and their
bytes matched the isolated review worktree at
`b72fad2cb34e183ef0c58aba4f252424cd3c18c9`. Searches of the source checkout
found references in the associated derivation notes, DAG, and evidence pages.
The source checkout's DAG is modified, so its references are observations of
the working tree, not claims about that HEAD's committed DAG.

All lines of these four scripts were read. Their matching contract companions
were absent at the start. The 1–5 scores below use the user's meanings; a 4
means the file is currently referenced and needs repair or stronger tests. It
does not certify perfection. The separate rubric assessment is deliberately
incomplete: a capability level does not become L4 merely by request, and
unassessed gates are not filled with invented grades. The requested floor is
L4B, stricter than the repository's L4D default. None of these files is shown
to meet L4B. No claim follows about a system-wide score.

All commands below ran in the isolated worktree with Python 3.14.7,
SymPy 1.14.0 and `-I -B -X utf8`. These executions are finite evidence about
the exact scripts and environment, not proofs of the imported physics.

## 1. `checks/independent/ads-cft-duality-import.py`

- **File score: 4.** Referenced by `dag/derivations/32_ads_cft/tfq_2202_ads_cft_duality_import.md`,
  the independent derivation note and the ADS_CFT evidence page. It checks a
  distinct scalar, ribbon-weight and finite-isometry bundle. A shared
  reporting or exact-matrix library could reduce repetition, but moving its
  checker logic into the implementation being checked would destroy the stated
  independence. Retain a standalone oracle or independently verified fixtures.
- **Bytes:** SHA-256 `33a8f4e4f820bf0c0f84f21af5602d80b0f89877e880abc0d8220f1d3db40ef7`.
- **SCORING.md:** assessed capability L3, exact profile; G3 **E** is
  demonstrated below, G1 is at most D because of the claim/evidence mismatch;
  remaining gates are unassessed. Composite/token are null, assessment
  incomplete, and the L4B target is not met.
- **Critical – optimized mode reports success with checks removed.** Lines
  66–229 put all substantive checks in `assert`, while the counters and success
  report survive `python -O`. A mutation replacing `gkpw_mass_sq` with the
  constant 12345 raises `AssertionError` normally but under `-O` returns
  `checks=803` as if the GKPW checks succeeded. Replace assertions in this
  executable verification boundary with explicit comparisons and structured
  failures, or fail closed when `__debug__` is false. Add subprocess regression
  tests in both normal and optimized mode that inject a wrong result.
- **Claim mapping and independent evidence.** Lines 14–16 describe absence of
  rational roots below the bound and a non-square discriminant; the script
  checks a finite rational grid and `4² < 20 < 5²`. The latter excludes an
  integer square, but this program does not itself implement the additional
  rational-square argument. Lines 145–155 verify an equality after multiplying
  the original ribbon weight by an additional power of N; this is true but
  does not itself establish the general unmultiplied genus-scaling formula.
  State the narrower checks or add an exact, independently justified argument
  for each claim and explicitly retain its hypotheses. The Lean theorem is a
  separate evidence source; this finding does not assert its proof is false.
- **Stale evidence and count.** The historical receipt
  `dag/research/campaign_ads-cft-duality-import_independent.json` binds
  `68c5c189…`, not the current hash above. The derivation note says 963 checks;
  the current program reports 829. Keep the old receipt as history and create a
  new byte-bound replay receipt; correct the current note's count and scope.
- **Observed execution:** `checks=829 gkpw=803 thooft=13 isometry_fence=13 failures=0`.

## 2. `checks/independent/ads-happy-toy-not-duality-gap.py`

- **File score: 4.** Referenced by the TFQ-2212 derivation and evidence
  pages. This checker contains a stabilizer entropy census and mutual
  information witnesses not supplied by the other three scripts.
- **Bytes:** SHA-256 `d123071557f5014d5e2fb57f88969974a8c68ff84a8595dffa0981c2c8f76e2a`.
- **SCORING.md:** assessed capability L3, exact profile; the five gates and
  composite remain unassessed pending a complete evidence and boundary audit.
  L4B has not been established.
- **Boundary handling.** The command uses fixed valid regions, but the exposed
  helpers accept invalid states: `region_entropy(gens, [20]) == -1`,
  `region_entropy(gens, [0, 0, 0]) == -1`, and
  `interval_entropy(gens, 0, -1) == 1`. `region_mutual_information(gens,
  [0], [0])` silently accepts overlapping regions. Model a validated qubit
  region and interval, reject duplicates, out-of-range indices, invalid
  lengths and overlap through explicit typed results, and test those cases.
  These observations do not invalidate the fixed valid inputs in `main`.
- **Claim boundary.** The computed census is for the hand-encoded generators
  and cut graph. Their identity with an independently specified contracted
  six-tensor HaPPY network needs its own construction/transport evidence;
  pairwise commutation and rank alone do not establish that identification.
  Maintain the finite-model qualifier until the mapping is independently
  checked.
- **Compression.** The 20-qubit encoding and cut routines overlap substantially
  with `ads-rt-formula-import.py`. A named, tested model and one small runner
  per claim could remove duplication, but preserve an independent alternative
  implementation or oracle and update the no-repository-import boundary if
  sharing changes it. Do not merge merely because text is similar.
- **Observed execution:** `checks=499 renyi=82 mincut=410 mi_codim=7 failures=0`.
  Its historical checker receipt matches the current bytes.

## 3. `checks/independent/ads-regge-area-rt-gap.py`

- **File score: 4.** Referenced by TFQ-2211 and its evidence page; its
  subdivision and weighting checks are distinct from the other scripts.
- **Bytes:** SHA-256 `30504d898a8d40d9825d3c6cd38bd99248db18ef9f4b29e970e11a725d93e5b1`.
- **SCORING.md:** assessed capability L3 for the finite domain computation;
  G1 is at most D, other gates and composite unassessed. L4B has not been
  established.
- **Claim mapping.** The header names 6 right and 4 equilateral hinges and
  240 Kuhn pentatopes. Lines 72–84 check binomial counts and `10 * 4! = 240`,
  while lines 105–114 insert 6 and 4 into an arithmetic sum. They do not
  construct those simplices, classify their hinges, or independently establish
  the stated boundary triangulation. Either construct and check the actual
  incidence/geometry from an independently specified carrier or narrow the
  Python check to arithmetic conditional on those supplied counts.
- **Input boundary.** The subdivision helpers divide by `m` without validating
  that it is a positive integer; `m = 0` raises and fractional/negative `m`
  silently enters a subdivision model. The CLI uses valid fixed examples.
  Introduce an explicit validated subdivision count and typed error result,
  with zero, negative and fractional rejection tests.
- **Stale evidence.** The historical receipt's `checker_sha256` is
  `bc37f3b8…`, not the current hash above. Retain the historical record and
  append a new execution bound to the reviewed bytes.
- **Observed execution:** `checks=463 carrier=387 subdiv=45 decoupling=31 failures=0`.

## 4. `checks/independent/ads-rt-formula-import.py`

- **File score: 4.** Referenced by TFQ-2204 and its evidence page; it includes
  RT/Brown–Henneaux algebra, hinge geometry and finite entropy comparisons.
- **Bytes:** SHA-256 `62970038b1b56f5446d2a78bbba6b70812b51065abeb02bacaee6a211f323015`.
- **SCORING.md:** assessed capability L3; the advertised exact profile has a
  demonstrated G2 **E** under the rubric's prohibition on unadmitted floats
  in an exact claim path. Other gates are unassessed; composite/token null,
  assessment incomplete, L4B not met.
- **Exactness and scope.** Lines 211–234 use binary `float` and `math.log` for
  four sample spectra and rounded conversions, without an error bound. They do
  not independently verify the general algebraic-spectrum transcendence or
  the rational-equality fence described in the header. Lines 276–282 search
  only `0 ≤ p ≤ 40, 1 ≤ q ≤ 40`; that is not a proof that no rational square
  root exists. The associated Lean result is a separate conditional/formal
  evidence source. Replace the bounded search with an exact integer/rational
  certificate or label it bounded; separate numerical demonstrations from
  exact claims and retain the Baker assumption where it is used.
- **Boundary handling and shared implementation.** `rt_leading_entropy`
  raises on zero Newton constant and accepts negative values; region helpers
  likewise do not validate interval bounds. Fixed `main` examples stay inside
  their intended domains. Validate domain value objects and return explicit
  errors. The duplicated HaPPY code merits the independence-preserving
  composition described under file 2.
- **Stale evidence.** The historical independent receipt binds `cb22ab06…`,
  not the current bytes. Preserve it and append a current, source-bound replay.
- **Observed execution:** `checks=545 rt_bh=82 dichotomy=24 regge_happy=439 failures=0`.

## Cross-checks and limits

An independent, deterministic review harness used seed `20261102` and compared
both GF(2) rank implementations on 160 random lists of at most 13 rows against
the cardinality of their explicitly enumerated vector span. It compared all
380 interval cuts in the three checkers against all 64 assignments of the
six graph-internal vertices, and compared both entropy implementations for all
380 intervals. All comparisons passed. These checks validate the stated
finite computations; the two entropy implementations still share the same
hand-entered generators, so agreement does not independently establish the
physical network identification.

The optimized-mode mutation witness was run using `importlib` to load the
first checker and replace `gkpw_mass_sq` in memory. Normal Python detected the
mutation; optimized Python returned the 803 count without detecting it. No
source file was modified by the witness. No comprehensive mutation campaign,
full gate audit, continuous integration run, or L4B certification was made.
