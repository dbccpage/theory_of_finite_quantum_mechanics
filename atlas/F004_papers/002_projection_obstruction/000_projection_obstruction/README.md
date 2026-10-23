# Projection Obstruction Anchor (PO-000)

[The mechanism inventory](projection_obstruction.md#mechanism-inventory) defines the
core structural mechanisms within this single unified 69-page publication. The current adversarial pass
corrects confirmed claim and implementation defects; it does not certify every
statement or replace the explicitly scoped reproduction records below.

**Title:** Projection Obstruction for Factorized States: Nonlinear Dynamics, Conditional $\ell^1$ Diagnostics, and Exact Short-Time Defect Bounds
**Author:** Jeremy H. Carroll
**Status:** Author-review revision (v6.9.18); not a new external deposit

*(Rewritten 2026-08-31 for the v6.3 Zenodo republication: the previous README
said v6.1 and described a `src/po000/` production package, a root `tests/`
directory, numbered notebook names, a `docs/zenodo_v6_preflight_checklist.md`,
a `code/`-as-mirror doctrine, and an `omega_engine` Lean lake home with a
`PaperPO000` target — none of which exist in this tree. That migration was
never applied to this deposit; `code/` is and always was the production source
here. The relics of the migration under `scripts/` are marked historical in
place. Everything below is stated against the actual package contents.)*

---

## Release identity and verification profiles

[`release_identity.json`](release_identity.json) declares manuscript/release
**6.9.18**, Python code **6.9.6**, and release date **2026-10-14**. These are
separate version identities. The archive and PDF title use the release version;
`pyproject.toml` declares the code version.

```bash
pip install .[jets]
python scripts/regen_sha256sums.py
python scripts/build_release_zip.py --output dist/ --check
python verify_deposit.py --profile standalone --archive dist/projection_obstruction_v6.9.18.zip
# Optional partial custody check, explicitly without tests or replay:
python verify_deposit.py --integrity-only --lean-source-scan --archive dist/projection_obstruction_v6.9.18.zip
```

Standalone verification disables ambient native imports and deliberately
**deselects 11 native integration cases**. Selected tests must pass without
skips. Native measurement records retain explicit capability refusals and do
not count as verified measurements. In a full repository with the native host,
`--profile native` opts in, includes native tests and requires all measurement
records to be verified; unavailable capabilities fail this profile. Direct
integration commands require `PO000_NATIVE_INTEGRATION=1`.

`--lean-source-scan` is only a lexical `sorry`/`admit` token scan. It neither
elaborates Lean nor audits axioms; the old ambiguous `--lean` flag is rejected.
For the scoped Lean 4.34.0/Mathlib 4.34.0 E.1/E.6 target, use the exact build recipe
and pin in [`lean4/README.md`](lean4/README.md). Historical sources retain their
separate statuses. The current scoped target includes the canonical trace-form proof; historical sources are not revalidated by that target.

The verifier compares the **selected ZIP's complete bytes**, canonical metadata,
member order and external sidecar against the current tree. It refuses missing
or altered archives, links/reparse points, and tree/control changes after mutable
subprocesses. A partial integrity check is not a full standalone profile pass.
See [`docs/publication_revision.md`](docs/publication_revision.md) for the
earlier revisions' execution scopes and publication limitations. Those
historical checks do not certify the current editorial revision.

## New in v6.9.16

Section 7.10 connects protected native futures and joint report refinement to
quantum observer sufficiency, distinguishing report collisions, support gluing
and positive Bell extension. A classical correlated state illustrates the
corrected partial-trace adapter. Reconstruction premises and the central-sector carrier test
are referenced in sibling package 006_finite_qm (§13.8, formerly Appendix E).
The exact quantum CHSH 14/5 example and setting-dependent native CHSH 12/5
example retain distinct assumptions. External Rust and Lean sources are
referenced with their scopes; this editorial bridge adds no mechanization or
operational quantum reconstruction. Python code remains version 6.9.5.

## New in v6.9.15

Written proofs of the Edge-Decomposed TDVP Duhamel Master Theorem (Theorem 5.10.A / §5.10.2)
and the Cut-Edge Pythagorean Cluster Rate Law (Theorem 5.10.B / §5.10.3), the Quantum Partial-Trace
Poset Cochain Adapter (Theorem 4.3.A / §4.3.2), and the Higher-Degree Graph-State Minimax Theorem
(Theorem 7.12 / §7.8) with the algebraic root master equation $r_d^{d+1}+r_d-1=0$. Repair of the
factor-of-2 scaling in §5.10.1, jump-operator support definition in §5.4.1, formal references
[32]--[35], and measurement setting symbol collision disambiguation ($M_{\mathrm{settings}}$).
The integration fixture is a floating-point comparison on an eight-site
hexagon-plus-square graph, with sampled Duhamel estimates. It is neither a
honeycomb example nor a certified integration enclosure; these theorems have
no bundled general Lean formalization.

## New in v6.9.14

Proposition E.6 (now in 006_finite_qm §13.8) constructs a positive invariant trace form from explicit real
spectral data and Jordan--Lie identities, with a scoped Lean proof and scalar
inhabitant retained in PO-000. Proposition E.7 gives sharp central-weight bounds on extension
purity and distance to a pure-composite marginal. Real quantum theory admits
purification; the corrected fixture exhibits it and separately witnesses failure
of local tomography. Quaternionic multiplication is associative. Finite Albert
checks and dimension counts do not certify whole operational axiom tables.
Python code 6.9.5 rejects inexact inputs to these exact fixtures.

## New in v6.9.5 through v6.9.13

Lemmas 3.4 through 3.14 are omitted from the 69-page edition; their proofs
are preserved in archived monograph revision 90e6231546 and verified by
symbolic tests in code/retraction_geometry.py. The Python runner refuses
claims C4d through C4l and does not certify those proofs. The executable chart
check remains Example 3.5, and those revisions retained Python package version 6.9.4.

## New in v6.9.4

Lemma 3.5 computes the coordinate field of a constant shear onto a \(C^2\)
graph. With \(g(e,n)=e+L(n-f(e))\) and \(\Pi=m\circ g\),
\(b(u)=Q(u)\alpha(u)+L\beta(u)\) where \(Q(u)=I_E-L\circ Df(u)\).
The case \(L=0\) is Lemma 3.4. Example 3.5 takes the parabola, the generator
\(A(x,y)=(-x,0)\), and unit shear, and obtains \(Db(0)=-1\), \(Db(1)=3\).
The vertical retraction on the same data has constant \(Db\). The exact
checks are in `code/retraction_geometry.py`. They are not a proof of the
Banach-space lemma. S1 remains open for a nonlinear fiber displacement and
for a submanifold that is not presented as a graph.

## New in v6.9.3

Lemma 3.4 computes the coordinate derivative of a vertical retraction onto a
\(C^2\) graph. With \(\Pi(e+n)=e+f(e)\) and chart coordinate \(u\),
\(b(u)=P_E A m(u)\) and
\(Db(u_1)-Db(u_0)=P_E A(Df(u_1)-Df(u_0))\).
If \(P_E A\) vanishes on \(F\), the chart derivative is independent of \(f\);
that is the case of Proposition 3.C. Example 3.4 takes \(f(s)=s^2\) and
\(A(x,y)=(-x-y,-y)\), a Euclidean contraction generator, and obtains
\(Db(0)=-1\), \(Db(1)=-3\). The exact checks are in
`code/retraction_geometry.py`. They are not a proof of the Banach-space
lemma. S1 remains open for a retraction that moves the chart coordinate and
for a submanifold that is not presented as a graph.

## New in v6.9.2

Lemma 3.3 transfers nonconstancy of the tangent-restricted ambient derivative
to the coordinate derivative when the manifold is relatively open in a closed
affine subspace and the chart comes from an ambient affine isomorphism.
Proposition 3.C refutes the claim that ambient nonconstancy or projection
curvature alone forces chart nonlinearity: the graph retraction onto
\(y=x^2\) with generator \(A(x,y)=(-x,0)\) has chart field \(b(s)=-s\).
S1 remains open when the second fundamental form is nonzero. The exact
checks are in `code/retraction_geometry.py`. They do not prove the
Banach-space lemma and they are not a proof of a curved-embedding transfer.

## New in v6.9.1

Aggregate schema `po000.mechanization_run.v4` adds separate finite certificates
for three measurement contracts and two boundary-checked local-zero models.
The independent checker replays their mathematics against declared inputs.
General theorem refusals remain separate. Measurement quotients and lower
bounds are evaluated by the native `omega_functional` implementation; no
Python fallback supplies an engine certificate. Without the repository native
host, those records explicitly refuse. Local-zero records require the `jets`
extra (SymPy).

The [active claim/dependency inventory](docs/claim_dependencies.json) gives
individual hypotheses, dependencies, proofs, examples and formalization scope
for the onset/physical results and E.1–E.5. Historical ledgers are preserved.
The two new E.1 Lean modules check associativity, the involution, the faithful
left representation, its closed finite-dimensional C*-image, and equality
of the positive cone with finite sums of self-adjoint Jordan squares. Their
input is the displayed identities after complexification; the construction
of that input from a real B1 system and E.2–E.5 remain written proofs.
See [the Lean source notes](lean4/README.md) for the pinned build and axiom scope.

Finite measurement assumptions include simultaneous moment-error coverage;
the checker does not verify experimental coverage. A separable correlated
state has a positive product-distance certificate and is included as a control.

## New in v6.9

Appendix E now contains a conditional reconstruction with written proofs.
The explicit base B1–B4 assumes positive real Jordan–Lie observables,
locally tomographic and dynamically compatible composition, exact corner
compression, and full process availability. It is not derived from the
finite-obstruction framework.

Within that base, the three surviving theory families are classical
probability, complex quantum theory, and finite complex quantum theory with
arbitrary superselection sectors. Pure-state purification selects the
sector-free complex quantum theory. Continuous reversible pure-state
transitivity is equivalent in this model class. The result includes all
density operators, effects, Born probabilities, tensor products, and quantum
channels, not just isolated state-space dimensions. The base is strong and
is not claimed to be a minimal operational axiom package.

Run the new exact identity and counterexample checks with:

```bash
python -m pytest -q code/tests/test_quantum_selector.py
```

The general classification is a written proof, not new Lean mechanization.
The aggregate replay explicitly refuses to certify the new general claims.

## New in v6.8

Section 7.8 derives a physical obstruction certificate for Ising rings:
an explicit local Pauli adapter, cycle-gradient repairs, a quotient with
conditioning constant one, and a noisy distance-from-product lower bound.
At most four product measurement settings suffice. The graph-state example
has zero pair defects but a nonzero measured quotient.

Section 5.17 derives finite-family onset/cancellation strata, constructs
sharp onset on every incidence-qubit tree, and gives a boundary-checked
local persistent-zero criterion and a leading-coefficient measurement protocol.
It does not claim generic sharpness for all qubit Hamiltonians.

At v6.8 Appendix E was a specification-only sketch. The v6.9 section above
supersedes that status with a reconstruction under the explicit added axioms.

The retained companion claim ledgers are legacy indexes. The current E.6/E.7
rows in the Markdown ledger support explicit replay refusals; the YAML index
is not complete. The active inventory, manuscript theorem statements,
S11--S12 entries and Appendix E specify the current scope.

These are written proofs plus exact finite checks, not new general Lean
formalizations or experimental results. Run the added checks with:

```bash
python -m pytest -q code/tests/test_physical_obstruction.py code/tests/test_sharp_onset.py
```

## New in v6.7

The v6.7 revision resolves the optional-dependency test collection in
`code/tests/test_polynomial_onset.py` (`pytest.importorskip("sympy")`),
positions Theorem 5.16 against established polynomial lifting literature
(Brunton et al., *PLOS ONE* 2016), provides an explicit non-claim of priority
for the generic lifting mechanism, and articulates the minimal observer
rank-nullity formulation ($\dim\ker Q - \dim(\ker Q \cap N)$) for uniform
prediction over the full lifted linear carrier. On a restricted admitted set
$Z$, the criterion is $(Z-Z)\cap\ker Q\subseteq N$; the ambient count need
not be minimal. This is a written argument, with no new formal-proof receipt.

## New in v6.6

The v6.6 addition in §5.16 gives a model-specific finite onset-or-invariance
certificate for polynomial defects. Run its exact examples and adversarial
checks with `python -m pytest code/tests/test_polynomial_onset.py`. The new
general result is a written proof; no new Lean build or external deposit is
claimed. The rational replay refuses lifts above 256 coordinates.

The v6.5 additions retained here give nearest-product metric certificates, pure excitation-sector
rate identities, exact phase prediction and completed-observer minimax results,
connected-cumulant onset and density bounds, and two counterexamples to an
unrestricted global/edge norm equivalence. Conditional extension results
(formerly Appendix D) are preserved in archived revision 90e6231546. These are
written mathematical proofs; the new tests replay exact finite examples and do
not formalize the general analytic arguments in Lean.

## Reproduce the new finite examples

Use Python ≥ 3.11 with NumPy, SciPy, pytest and SymPy (`pip install .[jets]`). From
this package root, run the focused files in small batches:

```bash
python -m pytest -q code/tests/test_metric_phase_derivations.py code/tests/test_connected_cumulants.py
python -m pytest -q code/tests/test_short_time_jets.py code/tests/test_polynomial_onset.py
python code/derivation_replays.py
python scripts/build_paper_artifacts.py --check
python scripts/regen_sha256sums.py --check
```

The first two files cover mixed primal/dual certificates, overlapping pure
sectors, the rational five-cycle state, finite-sign and full-phase distinctions,
nonoptimal dephasing, second-order phase ambiguity, connected/disconnected
cumulants, and coefficient locality. SymPy is required for these exact replays;
without it the exact test modules are explicitly skipped. The v6.5 metric,
phase and cumulant helpers reject floating-point inputs and malformed tensor
block data; supply exact rational or algebraic values. Earlier certificate
and replay tests retain their original scope and can be run by individual
file. Rendering additionally requires Pandoc and XeLaTeX; the `--check` rebuild compares the TeX against one Pandoc writer version, so a different Pandoc reports a mismatch rather than a content defect.

Optional notebooks use `pip install .[notebooks]`. No external deposit is
created by rebuilding the local artifacts.

---

## Three-Tier Pedagogical Ladder

| Tier | Latency | Surface & Description |
| --- | --- | --- |
| **Tier 1: Quick start** | ~3s | Executive summary in [`docs/quick_start.md`](docs/quick_start.md). |
| **Tier 2: Interactive front door** | ~60s | **Primary:** [`jupyter_notebooks/00_enter_po000.ipynb`](jupyter_notebooks/00_enter_po000.ipynb) — single place to demo, refute, and navigate claims (projection / retraction / obstruction widgets). Wings: [Reviewer walkthrough](jupyter_notebooks/reviewer_projection_obstruction.ipynb) · [Falsification](jupyter_notebooks/falsification_sandbox.ipynb). |
| **Tier 3: Monograph** | Deep | Primary manuscript [`projection_obstruction.md`](projection_obstruction.md), claim ledger [`projection_obstruction_claim_ledger.md`](projection_obstruction_claim_ledger.md) (+ machine-readable [`.yaml`](projection_obstruction_claim_ledger.yaml)), change log [`projection_obstruction_change_log.md`](projection_obstruction_change_log.md), and Lean 4 sources under [`lean4/`](lean4/) (see Lean honesty below). |

---

## Layout (what is actually in the box)

```text
Paper claim (ledger row, typed status)
        │
        ├─► Python (flat modules)  code/   ── pytest code/tests/
        ├─► Replay certificate     evidence/000_mechanization_run.json
        ├─► Jupyter front door     jupyter_notebooks/00_enter_po000.ipynb  (+ reviewer / falsify wings)
        ├─► Historical Lean cores lean4/po000_*.lean  (per-file historical scope)
        └─► E.1/E.6 scoped Lake build lean4/Po000JordanLie*.lean + Po000JordanTrace.lean
```

| Surface | Path | Notes |
| --- | --- | --- |
| **Python source** | [`code/`](code/) | Flat modules; the only Python layout in this deposit; notebooks and tests use `sys.path`/`pythonpath` = `code` |
| **Tests** | [`code/tests/`](code/tests/) | `python -m pytest code/tests` from the package root |
| **Replay evidence** | [`evidence/`](evidence/) | Retained historical certificate; generate a fresh v4 receipt as below. Verified finite supplements require the native host/adapter and SymPy for independent replay. |
| **Monograph** | [`projection_obstruction.md`](projection_obstruction.md) | v6.9.18 |
| **Reader formats** | [`projection_obstruction.tex`](projection_obstruction.tex), [`projection_obstruction.pdf`](projection_obstruction.pdf) | Generated with the toolchain reported by `scripts/build_paper_artifacts.py`; tracked so the release archive rebuilds from a clean checkout |
| **Legacy claim index** | [`projection_obstruction_claim_ledger.md`](projection_obstruction_claim_ledger.md) | Retained earlier rows (+ `.yaml`); not the new v6.9 theorem inventory |
| **Change log** | [`projection_obstruction_change_log.md`](projection_obstruction_change_log.md) | Newest first |
| **Lean 4 sources** | [`lean4/`](lean4/) | Scoped three-module E.1/E.6 Lake target with Lean/Mathlib 4.34.0; historical standalone files retain their separate build statuses. See `lean4/README.md`. |
| **Quick start** | [`docs/quick_start.md`](docs/quick_start.md) | Tier-1 card |
| **Notebooks** | [`jupyter_notebooks/`](jupyter_notebooks/) | `00_enter_po000.ipynb` is the front door |

---

## Environment

Dependencies are declared in `pyproject.toml` as minimum versions, not
exact pins (stdlib + numpy + scipy + pytest; SymPy for the optional exact-jet
suite; notebooks are a separate extra). From the package root:

```bash

# Test suite
python -m pytest code/tests

# Checksum manifest (stdlib only)
python scripts/regen_sha256sums.py --check
```

`MANIFEST.sha256` covers the admitted payload, excluding both root checksum
controls. `SHA256SUMS` covers that payload plus `MANIFEST.sha256`. Both are
regenerated in this order by `scripts/regen_sha256sums.py` as the final assembly
step. Verification checks both layers independently; rehashing a stale inner
manifest does not make it current.

**Release archive.** The obsolete v6.1-era archives were deleted because
their contents contradicted the tree they sat in: they packaged the retired
sympy v6.1.1 code. This tree does not commit the release archive: the builder
writes it and its external checksum sidecar under `dist/`, which the manifest
excludes. They are derived release objects,
not independent evidence, and must be regenerated after any covered payload
changes. `scripts/build_release_zip.py` regenerates both manifests first, packs
only files that manifest covers, and normalises timestamps, line endings and
the ZIP creator byte. The reader-facing `.md`, `.tex`, and `.pdf` paper
formats are members of the archive. Build with:

```bash
python scripts/build_release_zip.py --output dist/
```

**Which checksum file is which.** The payload manifests and archive sidecar
have different scopes:

| File | Hashes | Use |
| --- | --- | --- |
| archive member `MANIFEST.sha256` | admitted payload files, excluding both checksum controls | shipped *inside* the archive; checked independently |
| archive member `SHA256SUMS` | payload plus `MANIFEST.sha256`, as stored in the archive (LF-normalised) | shipped *inside* the archive; verifies an extraction |
| `dist/projection_obstruction_v6.9.18.zip.sha256` | the archive itself | the external sidecar for the `.zip` |

The root `SHA256SUMS` describes the working-tree bytes and does not hash the
archive. The builder derives the archive member with hashes of the
LF-normalised member bytes, then writes the archive sidecar after the tree is
final.

**Reproducibility, exactly.** From the committed payload bytes, the `.zip` is
byte-reproducible across machines: members are stored rather than deflated and
every platform-dependent field is pinned. Regeneration of the `.tex` and
`.pdf` is **not** toolchain-independent — Pandoc's LaTeX writer changes
between releases, and the same `.tex` gives 271,208 bytes at PDF 1.7 under
MiKTeX against 271,122 at PDF 1.5 under TeX Live. Their regeneration is
reproducible only within the named toolchain, which
`scripts/build_paper_artifacts.py` prints on every run.

The deletions and reasons for the old archives are recorded in
`projection_obstruction_change_log.md`.

## Replay and independent verification

The committed `evidence/000_mechanization_run.json` is historical v6.3
evidence, not a receipt for the revised v6.9.1 tree. Preserve it; write a
fresh replay separately. The aggregate replay retains the legacy numbered
claim checks and explicitly refuses the general theorem groups; it does not verify the new written proof of Proposition 4.7 or the
general analytic additions in §§5.8–5.17, §§7.5–7.8 or Appendices D–E.
The new physical and onset examples use the two targeted files above;
Appendix E has written proofs and exact examples in the quantum-selector
test file; neither a passing example nor this replay certifies its general
theorems. For v4 finite records marked verified, the independent checker
requires the repository native host/adapter for measurements and the `jets`
extra (SymPy) for local-zero records. Explicit capability refusals do not
count as mathematical verification. The legacy envelope checks use the
standard library.

```bash
# generate a current deterministic run without replacing historical evidence
PYTHONPATH=code python code/replay.py --output build/verification/current_run.json
PYTHONPATH=code python code/artifact_bundle.py --certificate build/verification/current_run.json --manifest build/verification/SHA256SUMS

# independently verify, with the capabilities required by each verified record
python code/verify_certificate.py build/verification/current_run.json
```

## Lean honesty

Lean 4 sources live under [`lean4/`](lean4/) (they are not built by this
deposit's Python test suite). The historical mirrored files certify the algebraic RE
hierarchy, abstract defect transfer, the Theorem 4.2 weighted/orbit singleton
cores, and the §7.4 observer-visibility layer
(`po000_l004_observer_visibility.lean`, `po000_l005_weighted_hierarchy.lean`);
the short-time quantum bound is paper-proved with Python finite replays —
**not** a Lean quantum theorem. The `l002` / `l003_double_commutator_rate`
files are **LEAN_TOY** residuals, not Theorem 5.1; two files are
package-context-only with no current green receipt; one is a labelled broken
parked draft (`lean4/README.md` names them).

The package-local `po000_short_time_jets.lean` compiles with Lean 4.34.1
and `Std` only. Its ten arithmetic declarations cover the rising support
factors and Taylor-normalization constants, not the quantum norm
inequalities, infinite-volume dynamics or spatial averaging proof.
Sections 5.8--5.10 give those written arguments. In particular, the
all-time local dynamics requires a fixed locally finite graph, compatible
bounded interactions and finite-dimensional local spaces; the spatial
defect-density limit additionally assumes translation invariance on a
nearest-neighbor lattice and cubic exhaustion.

## Scope fences and nonclaims

These are the package's literal scope fences; `code/replay.py` audits this
section and the monograph for them and reports FAIL if any is missing.

- This monograph assigns no authorization and changes no jurisdiction. It
  carries no operational authority or institutional standing. Nothing in this
  package mints authority; a positive residual tally is an evaluation, never
  an authorization.
- The Python package is finite instance evidence and is **not a proof** of
  the paper's universally quantified theorems.
- The **withdrawn five-way** RE1–RE5 independence claim stays withdrawn;
  only the RE3-drop and RE5-drop countermodels survive, and their
  arithmetic is what is mechanized.
- **Global trace norm** comparison theorems and the **nonlinear smooth**
  Banach-manifold semigroup material remain imported analytic results.
- **Lieb--Robinson** bounds are not used in the mechanized route; the
  short-time bound is the exact finite-system double-commutator estimate,
  valid only under the stated finite **host assumptions**.
- Higher-cell data ($C^2$, $d_1$) belongs to the companion papers
  **PO-004** and **PO-005** and is refused, not synthesized, here.

## Supplementary numerical diagnostics (PR #673)

`code/entanglement_production.py` and `code/krylov_scaling_benchmark.py` are
finite floating-point diagnostics, outside the manuscript's numbered theorem
inventory. Proposition 5.13 continues to concern reference-support decomposition.
Source-hash registration records custody; it does not certify new propositions.
No new Theorem 5.13--5.13.4 or Physical Review A readiness is asserted.

Sampled trapezoidal integration is exposed as `compute_cumulative_duhamel_estimate`
and can underestimate the integral. `compute_cumulative_duhamel_bound` instead
returns the conservative ideal-flow envelope
`min(2, 2*t*sum_e(|Jxx|+|Jyy|+|Jzz_e|))`, using the bond operator-norm bound.
It makes no tightness claim. Numerical ODE and matrix-exponential errors are
not enclosed; result flags only compare sampled values, and
`numerical_error_certified` is false.

The entropy coefficients come from fourth-order sparse Taylor jets, followed
by reduced-density convolution and purity expansion. They are floating-point
coefficients, without a Taylor remainder enclosure. `compute_entropy_expansion`
returns `c2`, `c3`, `c4`, `quartic_crossover_time` and `quartic_status`.
`sqrt(c2/abs(c4))` compares the quadratic and quartic terms only: it does not
control cubic or higher terms, their cancellations, or bulk transport.
When a term is zero or unresolved by the documented roundoff heuristic,
the crossover is `None`, with status `quartic_unresolved` or
`quadratic_unresolved`. This heuristic does not establish exact vanishing.
The legacy tuple API returns `NaN` for an unavailable ratio. An unavailable
ratio does not mean an infinite validity interval. Both evolution paths use
the same normalized product state. SciPy is a declared dependency.

The boundary coefficient examples assume a globally pure site-product initial
state and aggregated interactions on distinct unordered edges. They do not
extend that identity to arbitrary mixed states or correlated subsystems.
The three geometry comparisons describe their chosen inputs, without a
general coordination monotonicity or bulk-penetration claim.

Local dissipators have zero normal projection at a product state, but can
change concurrence growth. The local raising-noise regression for `H=J XX`
has right slope `2*max(0, abs(J)-gamma)`. The reduced unitary three-qubit
example is a different model from Markovian local noise.

The review repair has focused regressions, including aliased two- and five-point
meshes, an analytic two-qubit XX example, and a vanishing-quartic counterexample
across Hamiltonian scales. Full
package/deposit verification and release archive rebuilding must be repeated
before a release claim; earlier totals apply only to their earlier revisions.

## License

- **Text and Figures:** [Creative Commons Attribution 4.0 International (CC-BY-4.0)](LICENSE)
- **Code and Notebooks:** [Apache License 2.0](LICENSE)
