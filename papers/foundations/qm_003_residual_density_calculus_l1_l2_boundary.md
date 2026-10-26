# QM_003 — Redirect Stub (Absorbed into QM_004 / GOMC Part I)

**AuthorityEffect:** None.  
**Status:** ABSORBED_REDIRECT (2026-07-31 packaging merge; verified 2026-10-17).

## Live Destinations

Residual Density Calculus is retired as a standalone paper; its mathematical content was absorbed into:

- **Canonical Monograph:** [`../finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md#chapter-04`](../finite_obstruction_calculus/witnessed_difference_programme/witnessed_difference_programme.md#chapter-04) (Chapter 4, §4.2.2).
- **Companion Paper:** [`qm_004_general_obstruction_management_calculus.md`](qm_004_general_obstruction_management_calculus.md).
- **Encyclopedia Entry:** [`omega_engine_library/coda_library/encyclopedia/entries/quantum/enc-1111-residual-density-representation-bridge.md`](../../../../omega_engine_library/coda_library/encyclopedia/entries/quantum/enc-1111-residual-density-representation-bridge.md) (ENC-1111: Residual Density Representation Bridge).
- **Source Notes:** [`../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md#114-residual-density-across-the-l1l2-boundary`](../finite_quantum_mechanics/finite_quantum_mechanics_source_notes.md#114-residual-density-across-the-l1l2-boundary) (§11.4).
- **Rust Implementation:** `sources/atlas/papers/finite_quantum_mechanics/native/src/campaigns/residual_density_calculus.rs`.
- **Integration Tests:** `sources/atlas/papers/finite_quantum_mechanics/native/tests/residual_density_boundary.rs`.
- **Consolidated Claims:** [`../finite_quantum_mechanics/claims/claim_ledger.yaml`](../finite_quantum_mechanics/claims/claim_ledger.yaml) (IDs `003:QM-003-C1` through `003:QM-003-C18` / `RDB-01` through `RDB-13b`).

## Substantive Mathematical Content

1. **Mass Normalization to Probabilities:**  
   Finite nonnegative residual masses $\mu_s \ge 0$ with total mass $M = \sum_s \mu_s > 0$ normalize to sector probabilities $p_s = \mu_s / M$.
2. **Diagonal Density Matrix Embedding:**  
   The probability vector $p$ embeds as a diagonal density matrix $\rho_{\mathrm{diag}} = \operatorname{diag}(p)$. This matrix is positive semidefinite, has $\operatorname{Tr}(\rho_{\mathrm{diag}}) = 1$, and declared basis measurement recovers $p$.
3. **Distinction from QM-000 Pure-State Amplitudes:**  
   The diagonal density $\rho_{\mathrm{diag}} = \operatorname{diag}(p)$ and the pure-state projector $\rho_{\mathrm{pure}} = |\psi\rangle\langle\psi|$ (with $\psi_j = \sqrt{p_j}e^{i\phi_j}$) agree on basis probabilities but contain different coherence information. For $p = (3/4, 1/4, 0)$, $\operatorname{Tr}(\rho_{\mathrm{diag}}^2) = 5/8$, whereas the pure-state projector has purity $1$.
4. **Information Discarded by Normalization & Modulus:**  
   Passing from a signed cochain residual $x$ to coordinatewise absolute values $|x|$ and normalizing discards total scale, edge signs, and spatial orientation (orientation blindness).
5. **Phase Insensitivity:**  
   Sector probabilities $p$ do not determine coherent phase predictions; phase-sensitive mixing distinguishes states that share identical probability weights.
6. **Observer Nonfaithfulness & Hidden Readouts:**  
   Coarse observations can merge sectors while a hidden readout separates states; local diagnostic greenness does not imply the absence of global obstruction.
7. **Stochastic Transport:**  
   Finite row-stochastic transport preserves total mass and nonnegativity under the stated finite pushforward law.
8. **Diagnostic Validity vs. Terminal Authority:**  
   Channel and density diagnostics carry `AuthorityEffect::None`; diagnostic validity does not decide acceptance, reward, or terminal authority.
9. **Quotient-to-Density Representative Boundary:**  
   A quotient class $[x] \in C^1/\operatorname{im}(d_0)$ does not automatically descend to a coordinatewise absolute-value density. For $M = \operatorname{span}\{(1, -1)\} \subset \mathbb{R}^2$, the vectors $x = (1, 0)$ and $y = (0, 1)$ satisfy $x - y \in M$, hence $[x] = [y]$, and both attain the minimal $\ell^1$ norm $1$ in their class. Yet their normalized absolute-value densities $\rho_x = \operatorname{diag}(1, 0)$ and $\rho_y = \operatorname{diag}(0, 1)$ are orthogonal. Therefore, residual density is a diagnostic of a declared representative, not a quotient class invariant.

## What This Folder Retains

- Historical claim ledger mappings (`003:QM-003-*` / `RDB-*`) for bijection packaging.
- No standalone paper or new claims may be minted here.
