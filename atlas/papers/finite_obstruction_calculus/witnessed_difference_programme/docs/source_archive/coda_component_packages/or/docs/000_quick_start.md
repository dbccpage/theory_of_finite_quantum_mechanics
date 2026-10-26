# Quick Start: CODA-OR (Comparison Envelope)

## Overview
CODA-OR formalizes the **Comparison Envelope** $\Omega_\mathfrak{O} := \operatorname{Comp}_W(\mathbf{Reg}_\chi)$ over certified representation regimes under declared weight class $W$.

## Core Claims
- **GTOR-01:** Enriched comparison object / envelope definition.
- **GTOR-02 (Non-Creation Firewall):** Limits, colimits, or consensus envelopes organize diagrams but never manufacture authority ($X \in \Omega_\mathfrak{O} \not\Rightarrow \mathsf{Auth}(X)$).
- **GTOR-03 / GTOR-04 / GTOR-16 (Support Sieve Necessity):** Empty support sieve $\operatorname{Supp}_{\mathsf{Auth}}(X) = \emptyset$ forces hard refusal `R_empty_support`.
- **GTOR-05 / GTOR-10 / GTOR-14 (Four-Case Square Defect Classification):** Defects $\delta_\square = D_D HF - D_D KG$ are typed into $\mathsf{StrictCommute}$, $\mathsf{WeakCommuteCertified}$ (exact repair $d_0 \alpha = \delta$), $\mathsf{H1DiagramTear}$ (closed residual), and $\mathsf{OpenDiagramObstruction}$ ($d_1 \delta \neq 0$).
- **GTOR-06:** Limit authority necessity (requires component descent and local terminalization).
- **GTOR-08:** Weak 2-terminal candidate non-assumption.

## Quick Execution
```console
# Run test suite across 8 workers
python -m pytest -n 8 coda_atlas/F005_coda/or/code/tests -v

# Generate pedagogy figure
python coda_atlas/F005_coda/or/code/generate_figures.py

# Build Lean 4 formalization
cd coda_atlas/F005_coda/or/lean4
lake build
```
