# 006 Vector And Quantum Observer Geometries — Quick-Start Card

Actionable reproduction and verification instructions for paper GS-003: *Vector and Quantum Observer Geometries: Gauge Relativity and Trace Metric Bounds*.

---

## 1. Quick Verification (All Gates)

Run the root deposit verification suite to check envelope purity, cryptographic checksums, metadata schema, Lean 4 axiom normalization, and the full pytest suite:

```bash
python verify_deposit.py
```

Expected output:
```text
=== Vector and Quantum Observer Geometries Deposit Verifier ===
[5/5] Verifying deposit envelope purity...
  OK: envelope purity verified.
[1/5] Verifying SHA256SUMS manifest...
  OK: all 65 declared manifest entries verified byte-for-byte.
[2/5] Verifying zenodo_metadata.json...
  OK: metadata schema and required fields present.
[3/5] Verifying Lean 4 formalization and axiom report...
  OK: Lean 4 axiom report exists and is platform-normalized.
[4/5] Executing pytest test suite...
  OK: test suite passed cleanly.
=== All deposit verification gates passed cleanly! ===
```

---

## 2. Python Test Suite

Run the isolated, hermetic pytest suite with coverage:

```bash
python -m pytest code/tests -q -p no:debugging --cov=code --cov-report=term-missing
```

---

## 3. Lean 4 Formalization

To inspect or verify the Lean 4 formal proof kernels:

```bash
cd lean4
lake build
lake exe census  # or inspect axiom_report.txt
```

The formalization verifies without custom axioms, depending strictly on standard Lean 4 kernel axioms (`propext`, `Quot.sound`, `Classical.choice`).

---

## 4. Interactive Companion Notebooks

Launch the companion notebooks using `uv`:

```bash
# Intuitive exploration
./public_export/run_notebook.sh   # Linux / macOS
public_export\run_notebook.bat    # Windows

# Rigorous cochain calculations
./public_export/run_rigorous.sh   # Linux / macOS
public_export\run_rigorous.bat    # Windows

# Reproduction checks
./public_export/run_reviewer.sh   # Linux / macOS
public_export\run_reviewer.bat    # Windows
```
