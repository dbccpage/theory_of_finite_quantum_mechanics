# [TFQ-0505] alpha-license-binding-m1-m8

> **Stage**: `AUTHORIZATION` | **Status**: `SOURCE_RECORD`  
> **UUID**: `09cd8a3d-d387-50cf-9527-f8f22a0c33f4`  
> **Parent Derivation**: [TFQ-0331](tfq_0331_attach_a_replay_packet_to_a_named_terminal_without_letting_the_packet.md)

---

## 1. Abstract & Formal Statement

The Alpha reference slice is READY_WITHIN_DECLARED_SCOPE: after one repair pass (commit b698cf7f) the eight mandatory conditions hold within the §7 trust boundary. M1 authorized admission executes only a member freshly recomputed from the sealed kernel; M2 a parent Node whose history does not replay to its regime is refused; M3 a License is bound to the source history digest, the target, the measure and the bounds, and reuse with any field changed is refused; M4 uniqueness is not authorization; M5 every retained class receives one disposition (explored, pruned or open); M6 proposal and evaluation are inert and OPEN, bound or guard outcomes are typed stops, never admitted successes; M7 the slice replays offline with no model provider; M8 one local command (python verify.py) passed nine of nine steps with 0 skipped checks, including 169 tests and the sealed kernel's 66. The audit reproduced B1, B2 and B3 through the real path, and each repair fired and recovered under live injection.

### Governing Obligation
Admit only through apply_licensed or explore with a host-built License bound to source, target, measure and bounds, recompute the evaluation from the sealed kernel, and refuse every mismatch by name.

---

## 2. Derivation Context & Mathematical Grounding

In accordance with strict constructive principles:
- **Zero Floating-Point Cheating**: All quantities must be evaluated using exact integer combinatorial logic, discrete fractions, or exact field extensions (e.g. cyclotomic / Gaussian integer arithmetic).
- **Explicit Valuation**: No continuum limits, Hilbert topologies, or measure spaces may be assumed prior to their explicit constructive descent.

### Admitted Structural Imports
- **Admitted**: `Trust boundary of closeout §7: trusted sealed runtime modules, harness code and host; excluded process compromise, kernel or harness tampering, SHA-256 collisions, concurrent use and any authentication (assumption)`
- **Admitted**: `The one-command receipt is a local receipt in dbccpage/19L57G1, not hosted CI and not re-run in this checkout (assumption)`

### Further Prerequisites
- [TFQ-0492](../02_genesis/tfq_0492_candidate_extension_generator.md) candidate-extension-generator

### Epistemic Bottlenecks & Falsification Fences
> [!WARNING]
> Within the declared scope only: a License is checked for consistency with the call, not for provenance, so the host's call is the authorization; the refinement to Lean is NOT_PROVED, demand generation is OPEN and consumer bridges are OPEN.

---

## 3. Multi-Tier Code & Proof Witnesses

### Lean 4 Theorems
- `missing obligation: research/alpha_engine/lean/Harness.lean (dbccpage/19L57G1 only) is about harness datatypes and does not model the License binding; python_driver_refinement NOT_PROVED`

### Sovereign Rust Certifiers (Exact Rational Arithmetic)
- `missing obligation: no Rust port of the Alpha harness`

### Python Oracles & Numerical Evaluators
- [`github:dbccpage/19L57G1@85a83ae7c/research/alpha_engine/driver_a.py::apply_licensed`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/alpha_engine/driver_a.py)
- [`github:dbccpage/19L57G1@85a83ae7c/research/alpha_engine/harness.py::check_license_binding`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/alpha_engine/harness.py)
- [`github:dbccpage/19L57G1@85a83ae7c/research/alpha_engine/tests/test_admission_boundary.py::B3LicenseBinding`](https://github.com/dbccpage/19L57G1/blob/85a83ae7ce64dc2123ff218568a4ecd37e566d33/research/alpha_engine/tests/test_admission_boundary.py)

---

## 4. Downstream Derivations (Outgoing DAG Links)

- [TFQ-0506](tfq_0506_pfp_tripartite_law.md)

---

## 5. Audit Trail & Primary Source Lineage

- **Cited Source Lines**:
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt:270-288`
  - `atlas/papers/finite_obstruction_calculus/genesis/docs/sources/closeout.txt:587`
  - `github:dbccpage/19L57G1@85a83ae7c/docs/ALPHA_HANDOFF.md:130-133`
