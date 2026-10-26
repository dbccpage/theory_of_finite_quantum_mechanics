# Finite Vocabulary Fence — CODA-CS–Q Bridge

**Date:** 2026-07-31
**Rule:** Never infer one FINITE_* sense from another.

| Stable ID | Meaning | Not the same as |
|---|---|---|
| `FINITE_CARRIER` | Finite set of states / discrete support | Finite-dim Hilbert; continuum space is finite |
| `FINITE_DIMENSION` | Finite-dim vector/Hilbert rank | Finite carrier of continuum $X$; finite certificate |
| `FINITE_CERTIFICATE` | Finite evidence/receipt/audit artifact | Finite-dim Hilbert; finite presentation |
| `FINITE_PRESENTATION` | Finitely many generators + relations | Finite carrier or ambient dimension |
| `FINITE_DIM_CONTINUUM_SCALARS` | Finite-dim system with continuum scalars (e.g. $M_n(\mathbb{C})$) | Finite certificate; continuum object is finite as a set |

**Non-inference (mandatory):** continuum scalars ⇏ finite certificate; finite certificate ⇏ finite-dim Hilbert; finite carrier ⇏ continuum object is finite.

Related: `../coda_cs_q_bridge.md` §7–§8; `../lean4/Algebra.lean` and `../lean4/D01D02Records.lean`. The finite runtime domain is the explicit sample list D; it is not the arbitrary type X of the Lean factorization theorem.
