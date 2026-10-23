# Executive Summary & Quick-Start Card — CODA-MUR

**CODA-MUR: Certified Representation Transport, Composition, and Irreversible Forgetting**  
**Layer 2 of the CODA Tower ($\Omega\chi$)**  
**Version:** `v3.1.1` (2026-09-28)  

---

## 1. Core Principle & Firewall

CODA-MUR governs **certified representation transport**. Changing the representation of an authority-bearing object via a morphism $F: A \to B$ preserves operational standing if and only if $F$ carries a verified descent-compatibility certificate $\chi_F: D_B F \Rightarrow \bar{F} D_A$, declares an exact loss ledger $L_F$ (for lossy maps), and achieves explicit target terminalization $\tau_B$ under $\mathsf{IsAuth}_B$:

$$\chi_F \text{ is necessary for authority transport; } \chi_F \text{ is NOT sufficient for target standing.}$$

A commuting square certifies compatibility with observation. It is not, by itself, target standing.

---

## 2. Representation Morphisms & Loss Ledgers

1. **Exact / Embedding:** Declared loss-free kinds; the runtime verifies the finite square, not an isometry theorem.
2. **Quotient / Approximation / Unmeasured:** Lossy maps dropping degrees of freedom; require an explicit loss ledger $L_F = (e, i, a, u, \text{loss\_mass})$ matching the declared loss dimension.
3. **5×5 Kind Monoid:** Associative total-order monoid $\mathsf{EXACT} < \mathsf{EMBEDDING} < \mathsf{QUOTIENT} < \mathsf{APPROXIMATION} < \mathsf{UNMEASURED}$.
4. **Per-Leg Receipts:** Pasting preserves per-leg ledger receipts in `leg_ledgers`, preventing loss laundering across composite legs.

---

## 3. Quick-Start Commands

```powershell
# From the detached package root:
python -m pip install ".[test,notebooks]"
# 1. Run the static and runtime tests
python -m pytest code/tests -v

# 2. Replay all 3 companion Jupyter notebooks
python verification/replay_notebooks.py --write

# 3. Generate publication figure (discrete policy bars)
python code/generate_figures.py

# 4. Build Lean 4 formalization (pinned toolchain; record actual build result)
cd lean4
lake build
```

The Lean loss ledger proves the four Boolean fields only. Rational mass addition belongs to the paper/Python extension. A finite certificate requires a nonempty carrier and all four maps; flags alone do not suffice.
