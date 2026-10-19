# Test Infrastructure Specification: Theory of Finite Quantum Mechanics

## 1. Test Philosophy
The test infrastructure for the Theory of Finite Quantum Mechanics repository enforces an **opaque-box, requirement-driven verification methodology** derived directly from `original_request.md` and `PROJECT.md`.
- **Opaque-Box Contract**: Tests interact strictly via public, published module interfaces (`code/python/src/mub`, `code/python/src/fsp`, `code/python/src/majorana`, and root test runners) without coupling to internal private state.
- **Tri-Language Alignment**: Python test suites mirror the exact algebraic invariants, exact rational certifiers, and boundary gates implemented in Rust (`code/rust/src/`) and formal Lean 4 theorems (`lean4/`).
- **Claim Hygiene**: Test suites maintain strict claim discipline. Test verifications are documented with scoped, defensible claims (e.g., "checked by this test under the declared discrete parameters" rather than ungrounded claims).

---

## 2. Feature Inventory
The E2E test suite validates core capabilities across the three foundational domains:

| Feature ID | Domain | Module / Area | Description |
|---|---|---|---|
| **FEAT-MUB-01** | MUB6 | `src.mub` / `mub_verify` | Crate invariants, authority fences (`AuthorityEffect: None`), and SSOT package metadata. |
| **FEAT-MUB-02** | MUB6 | `cyclotomic.Cyc24` | Exact cyclotomic field arithmetic in $\mathbb{Q}(\zeta_{24})$, root-of-unity relations, and zero-defect checks. |
| **FEAT-MUB-03** | MUB6 | `interval.RationalInterval` & `SqrtBox` | Interval enclosure arithmetic, inclusion checks, boundary width, and volume bounding. |
| **FEAT-MUB-04** | MUB6 | `mub_triples` | Dita seed triples, Tao S6 blocks, and pairwise mutual unbiasedness verification in dimension $d=6$. |
| **FEAT-MUB-05** | MUB6 | `target_a4_gram_certifier` | Gramian matrix structure computation, exact rational LDLT pivots, and dual SDP obstruction certificates. |
| **FEAT-MUB-06** | MUB6 | `cover` & `verifier` | Regional covering trees, torus boundary cell subdivision, and full coverage certificates. |
| **FEAT-FSP-01** | FSP | `src.fsp.witness` | Exact canonical CAR hop product ($-1$), parity sum ($3$), and $k=1$ orbit witness generation. |
| **FEAT-FSP-02** | FSP | `refuse_removed_holonomy` | Refusal gate rejecting non-CAR cycle products and asserting holonomy preservation. |
| **FEAT-FSP-03** | FSP | `refuse_foreign_fixture` | Refusal gate restricting orbit scalars to valid orbit outputs and rejecting foreign fixtures. |
| **FEAT-FSP-04** | FSP | `bqnf_sign_evaluator` | 5-fold BQNF `TerminalRoute` classification, RREF cochain quotients, and sign-switching normal forms. |
| **FEAT-FSP-05** | FSP | `fermionic_hamiltonian` | Discrete lattice creation, Fock state representations, and exact Fermi-Hubbard Hamiltonian evaluations. |
| **FEAT-MAJ-01** | Majorana | `FockCarrier` | Jordan-Wigner mode algebra, creation/annihilation operators, and exact anticommutation relations. |
| **FEAT-MAJ-02** | Majorana | `sparse_kitaev` | 1D topological superconductor chain parameterization and isolated zero-mode detection at boundaries. |
| **FEAT-MAJ-03** | Majorana | `tetron` & `complexes` | Tetron surface carrier construction, Betti number $H_1$ derivation, and code distance calculations. |
| **FEAT-MAJ-04** | Majorana | `braid_action` | Elementary Majorana braiding operations, permutation parities, and multi-qubit compilation. |
| **FEAT-MAJ-05** | Majorana | `dual_observer` & `packet_wall`| Dual observer syndrome agreements, $L_1$ harmonic projections, and packet repair capacity bounds. |
| **FEAT-MAJ-06** | Majorana | `hard_invariants` | 10-invariant structural regression battery mirroring Rust `hard_invariants.rs`. |

---

## 3. Test Architecture

### 3.1 Directory Layout
```
tests/e2e/
├── __init__.py                                 # Package marker
├── conftest.py                                 # Sys.path shims and shared fixtures
├── test_tier1_feature_coverage.py             # Tier 1: Core feature verification (>= 5 per domain)
├── test_tier2_boundary_corner_cases.py         # Tier 2: Boundary value analysis & corner cases (>= 5 per domain)
├── test_tier3_pairwise_combinations.py         # Tier 3: Pairwise cross-feature interactions
└── test_tier4_real_world_scenarios.py         # Tier 4: Realistic physics workflows and end-to-end protocols
```

### 3.2 Test Runner Invocation
Tests are executed using `pytest` via the configured Python environment:
```powershell
# Run the complete E2E test suite
python -m pytest tests/e2e -v

# Run an individual tier
python -m pytest tests/e2e/test_tier1_feature_coverage.py -v
python -m pytest tests/e2e/test_tier2_boundary_corner_cases.py -v
python -m pytest tests/e2e/test_tier3_pairwise_combinations.py -v
python -m pytest tests/e2e/test_tier4_real_world_scenarios.py -v
```

### 3.3 Pass / Fail Semantics
- **Zero Tolerance for Silent Failures**: All assertions compare exact algebraic quantities (`Fraction`, integer parity, bitmask equivalence, exact enum types).
- **Exact Exception Raising**: Error gates (`refuse_foreign_fixture`, `refuse_removed_holonomy`, dimension mismatches) must raise the declared exception classes with expected message patterns.
- **Timeout and Determinism**: Tests are completely deterministic with zero network dependencies and sub-second execution per file.

---

## 4. 4-Tier Methodology

| Tier | Methodology | Scope & Objective | Threshold |
|---|---|---|---|
| **Tier 1** | **Category-Partition & Feature Coverage** | Partitions inputs by valid functional categories across MUB6, FSP, and Majorana to verify each primary feature path. | $\ge 5$ test cases per feature domain (MUB6: 6, FSP: 6, Majorana: 6; Total: 18) |
| **Tier 2** | **Boundary Value Analysis & Corner Cases** | Exercises boundary limits, degenerate inputs, zero-dimensional objects, particle vacuum states, out-of-range scalars, and refusal walls. | $\ge 5$ test cases per feature domain (MUB6: 5, FSP: 5, Majorana: 5; Total: 15) |
| **Tier 3** | **Pairwise Combinatorial Testing** | Validates joint invariants and algebraic interactions between distinct domains (MUB ↔ Majorana, MUB ↔ FSP, Majorana ↔ FSP, and tri-paper integration). | $\ge 4$ cross-feature combinations (Total: 5) |
| **Tier 4** | **Real-World Application Scenarios** | Simulates complete physical protocols (fault-tolerant braiding, meron quench simulation, 6D state tomography, topological phase transition, quantum teleportation). | $\ge 5$ application scenarios (Total: 5) |

---

## 5. Coverage Thresholds & Target Counts
- **Total Test Cases**: $\ge 40$ test cases across 4 tiers.
- **Suite Total**: 45 test cases.
- **Pass Rate**: 100% passing tests (45/45) with zero skips and zero expected failures.
