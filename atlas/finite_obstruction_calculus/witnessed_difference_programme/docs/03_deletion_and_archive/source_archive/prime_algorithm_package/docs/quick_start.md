# Quick start

AuthorityEffect: None. Every command runs from the package directory.

```bash
python -m pytest -q                       # the whole suite; fractions only
python -m pytest -q --cov=oe_prime_algorithms  # implementation coverage (≥95%)
python scripts/mutation_audit.py          # law mutations; all must be killed
python scripts/lean_census.py --check     # lake build + axiom census (needs elan, Lean v4.34.0)
python verify_deposit.py                  # the whole deposit gate
python verify_deposit.py --extracted      # from the ZIP's unpacked directory
```

Install `.[dev]` first for pytest and pytest-cov. The default gate checks the
ZIP payload as well as both checksum lists. The explicit `--extracted` mode
uses the archive's internal manifest, without requiring the external ZIP or
`SHA256SUMS`; it retains all payload, claim, link, test and coverage checks.

After a content change, run `python scripts/regen_sha256sums.py` to regenerate
the internal manifest, deterministic archive and external checksums together,
then run the default gate. Run the gate again with `--extracted` on a fresh
unpacked copy before distributing the archive.

Read the core implementation first (`code/oe_prime_algorithms.py`), then the
theorems (`lean4/Prime/Theorems.lean`), then the test suite (`code/test_oe_prime_algorithms.py`).
The two notebooks in `jupyter_notebooks/` walk through the same material: one enters
the triad, one falsifies the laws.
