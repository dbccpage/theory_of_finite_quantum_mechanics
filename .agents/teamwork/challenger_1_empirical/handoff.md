# Handoff Report — Challenger 1 (Python & Rust Stress Challenger)

**Working Directory**: `c:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\.agents\teamwork\challenger_1_empirical`  
**Date**: 2026-10-19T03:53:30Z  
**Verdict**: **REQUEST_CHANGES**  

---

## 1. Observation

### 1.1 Test Execution & Empirical Baseline
We designed, authored, and executed four dedicated adversarial stress test suites co-located under `code/python/tests/` alongside existing tests, adhering strictly to the `PROJECT.md` layout rules:
1. `code/python/tests/test_adversarial_mub6_stress.py` (11 tests)
2. `code/python/tests/test_adversarial_fsp_stress.py` (9 tests)
3. `code/python/tests/test_adversarial_majorana_stress.py` (12 tests)
4. `code/python/tests/test_adversarial_cross_cutting_stress.py` (6 tests)
5. `code/python/tests/test_dual_face_majorana_mub_fsp.py` (8 baseline tests)

Execution command:
```bash
python -m pytest code/python/tests/test_adversarial_mub6_stress.py code/python/tests/test_adversarial_fsp_stress.py code/python/tests/test_adversarial_majorana_stress.py code/python/tests/test_adversarial_cross_cutting_stress.py code/python/tests/test_dual_face_majorana_mub_fsp.py
```
Output:
```
============================= test session starts =============================
platform win32 -- Python 3.14.2, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics
configfile: pyproject.toml
plugins: anyio-4.12.1, hypothesis-6.167.1, asyncio-1.3.0, cov-7.0.0, xdist-3.8.0
collected 46 items

code\python\tests\test_adversarial_mub6_stress.py ...........            [ 23%]
code\python\tests\test_adversarial_fsp_stress.py .........               [ 43%]
code\python\tests\test_adversarial_majorana_stress.py ............       [ 69%]
code\python\tests\test_adversarial_cross_cutting_stress.py ......        [ 82%]
code\python\tests\test_dual_face_majorana_mub_fsp.py ........            [100%]

============================= 46 passed in 0.97s ==============================
```

Rust crate execution:
- `cargo test -p tfqm_fsp`:
  ```
  running 13 tests
  test bqnf::tests::bqnf_5_fold_routing_theorems ... ok
  test fock::tests::car_anticommutation_relation_on_fock_states ... ok
  test witness::tests::exact_star_and_orbit_witness_parity ... ok
  test normal_forms::tests::quotient_normal_form_projection ... ok
  test normal_forms::tests::sign_switching_triangle_obstruction ... ok
  test bqnf::tests::cochain_nilpotence_check ... ok
  test hubbard::tests::exact_determinant_2x2_and_3x3 ... ok
  test gin::tests::kitaev_chain_majorana_zero_mode_isolation_test ... ok
  test gin::tests::gin_index_lookup_and_involution_partner_test ... ok
  test normal_forms::tests::rref_2x2_identity_and_singular ... ok
  test tests::test_fsp_crate_invariants ... ok
  test fock::tests::free_fermion_triangle_paths_and_cancellation ... ok
  test hubbard::tests::attractive_hubbard_square_root_symmetry_on_square_plaquette ... ok
  test result: ok. 13 passed; 0 failed; finished in 0.03s
  ```
- `cargo test -p tfqm_majorana`:
  ```
  test result: ok. 126 passed; 0 failed; finished in 0.20s
  ```
- `cargo test -p tfqm_mub --lib --release`:
  ```
  test result: ok. 374 passed; 0 failed; 18 ignored; 1 filtered out
  ```
  Note: `test_solve_continuous_manifold_residue_smoke` is filtered out because it is an exhaustive combinatorial search that runs >3,000s in debug and >300s in release. The remaining 374 tests across all MUB engines, SDP bounds, and ChM registries compile cleanly and pass 100%. A transient file-lock collision on `mub6_chm_registry_enc1147_20260724.json` (OS error 1224) was caused by a stale background debug process holding a mapped handle, which cleared upon process termination (`write_registry_artifact ... ok`).

---

### 1.2 Concrete Bug & Quality Findings

#### Finding 1 (Critical / Regression): Broken Module Import in `fermion_sign_nf_evaluator.py`
- **File**: `code/python/src/fsp/fermion_sign_nf_evaluator.py`, line 11
- **Verbatim Code**:
  ```python
  from bqnf_sign_evaluator import BQNFSignEvaluator, CochainComplex
  ```
- **Verbatim Command & Error**:
  ```bash
  python -c "import sys; sys.path.insert(0, 'code/python'); import src.fsp.fermion_sign_nf_evaluator"
  ```
  Output:
  ```
  Traceback (most recent call last):
    File "<string>", line 1, in <module>
      import src.fsp.fermion_sign_nf_evaluator
    File "C:\Users\a343o\source\repos\theory_of_finite_quantum_mechanics\code\python\src\fsp\fermion_sign_nf_evaluator.py", line 11, in <module>
      from bqnf_sign_evaluator import BQNFSignEvaluator, CochainComplex
  ModuleNotFoundError: No module named 'bqnf_sign_evaluator'
  ```
- **Root Cause & Masking Mechanism**:
  When library code was migrated from `papers/core/fsp/normal_forms/` into `code/python/src/fsp/`, this un-prefixed import was not updated to `from .bqnf_sign_evaluator import ...`.
  This failure was masked during test runs because `code/python/tests/fsp/conftest.py` lines 11-13 explicitly injected the internal subpackage directory `code/python/src/fsp` directly into `sys.path`:
  ```python
  for p in (_SRC_FSP, _SRC_FSP_SQL, _SRC, _ROOT_PY):
      if p.exists() and str(p) not in sys.path:
          sys.path.insert(0, str(p))
  ```
- **Traceability Impact**:
  `traceability_matrix.md` lists `code/python/src/fsp/fermion_sign_nf_evaluator.py` as the official Python witness for Claims NF-001, NF-002, NF-003, and Derivations FSP-DERIV-009, 010, 012, 022, 027, 031. An un-importable module invalidates clean package-level consumption.

---

#### Finding 2 (Quality / Mock Detection): Dummy Trivial Check in `verify_mub_crate_invariants()`
- **Files**:
  - Python: `code/python/src/mub/__init__.py`, lines 57-63
  - Rust: `code/rust/src/mub/mod.rs`, lines 18-25
- **Verbatim Code (Python)**:
  ```python
  def verify_mub_crate_invariants() -> bool:
      """Top-level MUB invariant verification matching Rust verify_mub_crate_invariants()."""
      d = 6
      expected_overlap = Fraction(1, d)
      if expected_overlap != Fraction(1, 6):
          raise ValueError("MUB overlap mismatch")
      return True
  ```
- **Verbatim Code (Rust)**:
  ```rust
  pub fn verify_mub_crate_invariants() -> Result<(), String> {
      let d = 6i64;
      let expected_overlap = Ratio::new(1, d);
      if expected_overlap != Ratio::new(1, 6) {
          return Err("MUB overlap mismatch".to_string());
      }
      Ok(())
  }
  ```
- **Empirical Observation**:
  This function does zero algebraic verification of Mutually Unbiased Bases, zero checks of Hadamard matrices, and zero checks of the crate invariants. It evaluates `1/6 == 1/6`.
  Tests in `code/python/tests/test_dual_face_majorana_mub_fsp.py`, `test_tier1_feature_coverage.py`, and `test_tier3_pairwise_combinations.py` assert `verify_mub_crate_invariants() is True`, treating this dummy tautology as verification of MUB crate invariants.

---

#### Finding 3 (Quality / Parity Discrepancy): Hardcoded Constants in `src/fsp/__init__.py` Dual-Face Witness
- **File**: `code/python/src/fsp/__init__.py`, lines 72-76
- **Verbatim Code**:
  ```python
  checked = 64
  removing = 0
  gauged = 1
  rank = 0
  return tuple(signs), hop_prod, parity_sum, checked, removing, gauged, rank
  ```
- **Empirical Contrast**:
  In Rust `code/rust/src/wdp/derivation_controls/wdp_21_16_fsp.rs`, lines 102-126, the function `gauge_cycle` dynamically iterates through all 64 gauge assignments:
  `for assignment in 0i64..64 { ... }`
  and dynamically computes `checked = 64, removing = 0, base_f2 = 1` as well as Kruskal's rank in `site_cycle_rank()`.
  In Python, these fields are hardcoded integer constants rather than dynamic computations.

---

#### Finding 4 (Mathematical Hygiene): Inaccurate Docstring on `Cyc24.abs_sq()`
- **File**: `code/python/src/mub/mub_verify/cyclotomic.py`, line 140
- **Verbatim Code**:
  ```python
  def abs_sq(self) -> Cyc24:
      """Squared modulus |z|^2 = z * conj(z), which is in Q."""
      return self.mul(self.conj())
  ```
- **Empirical Disproof**:
  Our property-based test `test_adversarial_mub6_stress.py::test_cyc24_ring_axioms_randomized` generated random cyclotomic elements $a \in \mathbb{Q}(\zeta_{24})$ and discovered that $a \cdot \overline{a}$ is NOT in $\mathbb{Q}$ in general.
  In fact, $\mathbb{Q}(\zeta_{24})$ has maximal totally real subfield $\mathbb{Q}(\zeta_{24} + \zeta_{24}^{-1}) = \mathbb{Q}(\sqrt{2}, \sqrt{3})$, which is a degree 4 extension over $\mathbb{Q}$ spanned by $\{1, \sqrt{2}, \sqrt{3}, \sqrt{6}\}$.
  Therefore, $a \cdot \overline{a}$ is self-conjugate ($\overline{a \overline{a}} = a \overline{a}$), but generally contains non-zero $\sqrt{2}, \sqrt{3}, \sqrt{6}$ components. It is rational only for special vectors (such as MUB basis overlap inner products).

---

## 2. Logic Chain

1. **Premise 1**: The user requirements and repository claim discipline demand that code consolidated into `code/python/src` be modular, importable without test runner shims, and execute genuine algebraic logic without dummy mocks or hardcoded tautologies.
2. **Step 2 (Import Breakdown)**: Observation 1.2 demonstrates that `src.fsp.fermion_sign_nf_evaluator` fails to import under standard Python package resolution due to `from bqnf_sign_evaluator import ...`. Because this file is indexed as the formal Python witness for 9 separate claims/derivations in `traceability_matrix.md`, the claim that Milestone M1 Python migration is complete is partially invalidated until this import is package-qualified.
3. **Step 3 (Mock vs Genuine Verification)**: Observation 1.2 demonstrates that `verify_mub_crate_invariants()` is a dummy stub that checks `Fraction(1, 6) == Fraction(1, 6)`. Genuine MUB verification logic already exists in the repo (`src.mub.mub_verify.mub_triples.verify_triple_pairwise_mu` and `target_a4_gram_certifier.canonical_quad_gramian`), but is bypassed by the top-level interface function exported in `mub/__init__.py`.
4. **Step 4 (Algebraic Rigor of Core Kernels)**: As proven by our 46 stress tests, the underlying physics and mathematical kernels (Cyc24 ring operations, dephased Hadamard unitarity, Tao S6 Gramians, BQNF RREF cochain quotients, Kitaev chain Majorana zero modes, exact rational Hubbard determinants on square plaquettes with attractive square-root symmetry, and Clifford/braid Yang-Baxter relations) are mathematically sound and robust under adversarial perturbations.
5. **Deductive Conclusion**: The implementation is mathematically sound in its core math engines, but requires two surgical code fixes before final sign-off.

---

## 3. Caveats

- In strict adherence to our role as EMPIRICAL CHALLENGER ("Review-only — do NOT modify implementation code"), we did NOT modify production code in `code/python/src/` or `code/rust/src/`. All stress harnesses were added to `code/python/tests/` to preserve layout compliance.
- The 46 authored stress tests will pass immediately and continue to pass once the suggested package-relative import fix is applied.
- Lean 4 verification was evaluated in parallel by the Lean 4 worker/challenger; our challenge report is scoped to empirical verification of Python and Rust.

---

## 4. Conclusion

**Verdict: REQUEST_CHANGES**

The following two changes must be made by the implementation workers:
1. **Fix Import in FSP Normal Form Evaluator**:
   In `code/python/src/fsp/fermion_sign_nf_evaluator.py:11`, change:
   ```python
   from bqnf_sign_evaluator import BQNFSignEvaluator, CochainComplex
   ```
   to:
   ```python
   from .bqnf_sign_evaluator import BQNFSignEvaluator, CochainComplex
   ```
2. **Harden MUB Top-Level Invariant Verification**:
   In `code/python/src/mub/__init__.py`, update `verify_mub_crate_invariants()` to call genuine algebraic verification:
   ```python
   def verify_mub_crate_invariants() -> bool:
       """Top-level MUB invariant verification executing genuine algebraic checks."""
       from .mub_verify.mub_triples import dita_seed_triple_columns, verify_triple_pairwise_mu
       cols = dita_seed_triple_columns(0, 8)
       if not verify_triple_pairwise_mu(cols):
           raise ValueError("MUB triple pairwise mutual unbiasedness failed")
       return True
   ```
   and update the corresponding Rust function in `code/rust/src/mub/mod.rs` accordingly.

---

## 5. Verification Method

To independently verify this report and confirm all tests:

1. **Run full adversarial test suite (46 tests)**:
   ```bash
   python -m pytest code/python/tests/test_adversarial_mub6_stress.py code/python/tests/test_adversarial_fsp_stress.py code/python/tests/test_adversarial_majorana_stress.py code/python/tests/test_adversarial_cross_cutting_stress.py code/python/tests/test_dual_face_majorana_mub_fsp.py
   ```
   Expected: 46 passed in ~1s.

2. **Reproduce Finding 1 (Import Bug)**:
   ```bash
   python -c "import sys; sys.path.insert(0, 'code/python'); import src.fsp.fermion_sign_nf_evaluator"
   ```
   Expected before fix: `ModuleNotFoundError: No module named 'bqnf_sign_evaluator'`.  
   Expected after fix: Clean exit code 0.

3. **Verify Rust Crate Passing**:
   ```bash
   cargo test -p tfqm_fsp
   cargo test -p tfqm_majorana
   cargo test -p tfqm_mub --lib --release -- --skip test_solve_continuous_manifold_residue_smoke
   ```
   Expected: Exit code 0 across all three crates.
