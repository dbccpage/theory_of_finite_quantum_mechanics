# Guarded schedule classification: proof and verification

Date: 2026-10-09. AuthorityEffect: None.

[Appendix P.22](../witnessed_difference_programme.md#p22-exact-topology-and-coherence-thresholds-for-paired-count-guards)
and the [complete derivation](guarded_schedule_topology.md) classify the full
legal schedule complex for distinct paired removals/additions on one count
key. For `n >= 2` and `1 <= c < n`, it has the homotopy type of the real
no-`(c+1)`-equal arrangement complement. The result uses supplied task tags
and pair precedence, the stated count guard, and every legal permutohedral
cell. It is not a classification of all guarded WDP presentations.

## Evidence by claim

| Claim | Evidence | Scope |
| --- | --- | --- |
| General homotopy equivalence, exact connectivity and maximal-capacity sphere | Complete written proof; [independent mathematical audit](../manifests/guarded_schedule_topology_math_audit.json) | Includes a proof of all-dimensional linear-extension contractibility. Imports the cited nerve theorems. Not a Lean topology formalization. |
| Prefix replay, block refinements, endpoints and order constraints | [Lean source](../lean4/WitnessedDifference/GuardedScheduleTopology.lean), [fresh build receipt](../manifests/guarded_schedule_topology_lean.json), [build output](guarded_schedule_topology_lean_build.txt) | Lean 4.33.1; 37 theorems, six definitions and one inductive declaration. All 44 declarations have printed axiom dependencies; their union is `propext`, `Quot.sound`. No custom axiom or admitted proof. |
| Finite cells, signed boundaries and free integral homology | [Retained certificate](../code/guarded_schedule_topology/evidence/certificate.json), [validation receipt](../manifests/guarded_schedule_topology_validation.json) | All 14 cases `n = 1..4`, `c = 0..n`. Integer unit-pivot certificates have zero residuals in these cases. An unresolved nonunit residual is reported as unclassified. |
| Native transition correspondence | Validation receipt and [source-bound Rust build receipt](../code/guarded_schedule_topology/evidence/native_build_receipt.json) | All 12,980 causal schedules in the finite range, including refusals and intermediate counts. Native count semantics do not supply task tags or precedence. |
| Independent implementation review | [Code audit](../manifests/guarded_schedule_topology_code_audit.json) | Independent cell enumeration, 37,481 boundary-orientation comparisons, 1,500 integer-matrix controls and another 12,980 native calls. The two native runs cover the same schedule population. |
| Non-exact cellular cochains | Certificate and [focused tests](../code/unit_tests/test_guarded_schedule_topology.py) | Explicit cycles pair by `-1` with closed top cochains on `T(3,2)` and `T(4,3)`. The differential is the signed cellular boundary dual. |

The 52 focused Python tests passed. They include altered boundaries, invalid
certificates, unsafe mixed blocks, unresolved integer residuals and explicit
cycle/cochain mutations. The full complex matters: the two-skeleton of
`K(4,3)` has second Betti number 1883, while the full complex has rank one.

The source hashes in the audit records identify the reviewed bytes. Absolute
`/tmp` and `/workspace` paths record the original runs, not portable installation
requirements. The mathematical audit also hashes the exact P.22 passage;
the passage is retained verbatim in the manuscript. The Lean build output is
copied without alteration from the path named in its receipt.

The [PR review follow-up](../manifests/guarded_schedule_topology_review_followup.json)
records a later reference addition: Panov–Tril's Construction 4.5 and Theorem
4.6 give the task complex and its arrangement-complement interpretation
directly. Only §11 of the derivation changed; the previously audited proof in
§§1–10 and the manuscript passage remain byte-identical. The earlier audit
retains its original source hash.

The follow-up also corrects a missed integration test: adding P.22 raises the
exact manuscript section census from 426 to 427. The full contract suite then
passes all 62 tests, with the canonical claim count still 154. This was a new
PR regression, separate from the older publication-rule failures. The trusted
baseline comparison is another check: the current base commit already differs
from its stored contract baseline by 932 entries, with no structural integrity
issues. The candidate also differs from that baseline. Its check therefore
still refuses; passing the census test does not approve the baseline changes.

## Reproduce the executable checks

From the paper root with Python 3.12 and pytest installed:

```sh
python -m pytest -q -o addopts= --confcutdir=code/unit_tests \
  code/unit_tests/test_guarded_schedule_topology.py
python scripts/verify_guarded_schedule_topology.py check \
  --certificate code/guarded_schedule_topology/evidence/certificate.json \
  --receipt /tmp/guarded-topology-recheck.json
```

The second command checks the retained finite certificate without native
replay. [Package instructions](../code/guarded_schedule_topology/README.md)
give the explicit Rust build and source-custody arguments needed to repeat
native replay. Missing native arguments are recorded as an unrequested check,
not a successful native run.

For the isolated formal build, put the pinned Lean 4.33.1 `bin` directory on
`PATH`, then run this from the paper root. It copies only the three sources
named in the retained receipt, checks their hashes, and builds them with the
receipt's minimal Lake configuration. No Mathlib installation is required.

```python
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

receipt = json.loads(Path("manifests/guarded_schedule_topology_lean.json").read_text())
build = Path(tempfile.mkdtemp(prefix="wdp-guarded-lean-"))
for source, expected in receipt["source_sha256_after"].items():
    raw = Path(source).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == expected, source
    target = build / Path(source).relative_to("lean4")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
(build / "lakefile.lean").write_text(receipt["lakefile"])
(build / "lean-toolchain").write_text("leanprover/lean4:v4.33.1\n")
subprocess.run([shutil.which("lake"), "build"], cwd=build, check=True)
```

## Limits and remaining work

The task complex is a smaller homotopy model. The reduction from 15,170 event
cells to 74 task cells at `(n,c) = (4,3)` preserves topology; it does not
establish a quotient preserving every execution answer, cost or continuation.
An explicit chain map is still needed to transport numerical task-cell
witnesses to native event-cell coordinates.

The new formal record is separate from the earlier 50-module, 691-declaration
audit. No full Mathlib build, physical reconstruction, authorization guarantee
or general guarded-coherence closure is claimed. Finite enumeration tests the
implementation and examples; the unbounded theorem rests on its written proof.

The pre-existing package-wide publication gate was not green before this
increment. This evidence supports review of the derivation and its code; it
does not declare the whole WDP deposit ready for republication.
