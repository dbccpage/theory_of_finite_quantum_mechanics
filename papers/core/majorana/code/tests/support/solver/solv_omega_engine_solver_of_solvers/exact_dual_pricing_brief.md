# Operator brief — SoS exact dual pricing (FW-8 rail)

**Date:** 2026-08-10
**AuthorityEffect:** None
**48h gate:** Exact-origin inputs can emit dual zero-gap receipts (`arithmetic_mode=Q`); float-origin inputs remain diagnostic

---

## Five-line math spine (PO-000 → residual DeWitt)

1. **PO-000** — Product retraction residual \(n_e\); \(\Phi_1=\inf\|\omega-d_0\alpha\|_1\); short-time \(D_e(t)\ge\nu_e t-24g^2 t^2\).
2. **PO-016** — \(\mathcal{O}_{p,F}=\{(x,x'):p(x)=p(x'),F(x)\ne F(x')\}\); descent iff \(F=\bar F\circ p\).
3. **Gate-11 + DDA** — EXACT / CLOSED_NONEXACT / NONCLOSED; float multi-cycle is diagnostic only.
4. **FW-8 / this adapter** — \(\Phi_k\) exact primal/dual with gap \(0\) over \(\mathbb{Q}\); declaration required.
5. **PO-021 / MS-T11** — Residual-form Wheeler–DeWitt: \(\hat\Omega\Psi=\mathfrak{r}\); exact sector is special case after declared repairs. Quotient \(\not\Rightarrow\) section (indefinite supermetric). Continuum \(\Psi[g_{ij}]\) **refused** as solved.

---

## What landed in code

| Piece | Path |
|---|---|
| Adapter | `solv_exact_dual_pricing.py` |
| Cascade wiring | `solv_oesos.py` → stage `ExactDualPricing`; fields `arithmetic_mode`, `exact_phi_k`, `exact_gap`, `is_exact_dual_certified()` |
| Exact rail (reuse) | `omega_engine/crates/functional/degree_k_phi.py` (`solve_degree_k_phi_exact`) |
| Tests | `omega_engine/_tests_unit/test_sos_exact_dual_pricing.py` |

**Certification honesty**

- `is_certified=True` only when rational dual gap is 0 (`dual_witness_status=certified_exact`).
- Public exact adapters reject Python binary floats. Integers, `Fraction`,
  `Decimal`, strings, and SymPy rationals preserve exact scalar provenance.
- Float `solve_phi1_dual_witness` may still run as fallback; status is `float_diagnostic_*` and **never** sets `is_certified` (kill path: forced exact-rail failure → `float_diagnostic_certified` still keeps `is_certified=False` / `arithmetic_mode=diagnostic_float`).
- `diagnostic_residual_mass` is the float cascade mass; `exact_phi_k` is present
  only when the exact scalar representation reaches the exact adapter intact.
- An edge residual mathematically admits Φ₁ pricing independent of
  `degree_window`, but a float-valued cascade does not recover exact provenance
  by converting decimal renderings to `Fraction`; it remains diagnostic.
- `SolverCascadeReceipt.as_evidence_dict()` serializes Q dual fields plus a residual spine fence (`float_as_exact` REFUSED; continuum WDW REFUSED; Pontryagin/π OPEN; `coda_cs=coda_q` pricing language only; `estate_wide_phi_k_theorem` / `normhood_from_attainment_alone` REFUSED).
- Live receipt attributes (via `_dual_fields_for_receipt` / adapter `as_cascade_fields`) also stamp `estate_wide_phi_k_theorem=REFUSED` and `normhood_from_attainment_alone=REFUSED` even when `dual_witness_status=certified_exact` — not spine-fence-only.
- `ExactDualPricingReceipt` itself carries the same refuse fields as live frozen attrs (not only via `as_cascade_fields`), so direct adapter consumers cannot miss the fence.

---

## Commands

```text
cd <anomalonpy repo root>
set PYTHONPATH=.
python -m pytest omega_engine/_tests_unit/test_sos_exact_dual_pricing.py -q
python -m omega_engine.crates.solver.solv_omega_engine_solver_of_solvers.solv_oesos
```

Demo `__main__` prints `arithmetic_mode`, `dual_witness_status`, and a spine-fence
line (`float_as_exact` / `estate_wide_phi_k` REFUSED; `pontryagin_pi` OPEN; continuum
WDW REFUSED) so operator demos cannot be mistaken for estate-wide dual discharge.

Golden expectations (same as FW-8):

| Fixture | Result |
|---|---|
| Tetra faces \(\omega=(2,4,4,6)\) | \(\Phi_2=4\), gap 0 |
| Tetra faces \(\omega=(3,3,5,5)\) | \(\Phi_2=0\), gap 0 (exact cochain negative control) |
| Triangle gradient | \(\Phi_1=0\), gap 0 |
| 4-simplex boundary fundamental | \(\Phi_3=5\), gap 0 |
| Multi-degree battery (Φ₁+Φ₂±+Φ₃) | all `certified_exact` (listed fixtures only; includes Φ₂=0) |

---

## Explicit OPEN (do not sell as Gate-11 / SoS output)

1. **Finite residual period → unbounded \(\mathbb{Z}\) → Pontryagin dual \(U(1)\) → \(\pi\)**
   Shared residual character under scale is a research programme. Finite exact dual certificates do **not** discharge continuum duals or Haar measure.
2. **`coda_cs = coda_q` object identity** — refused. Shared residual **pricing language** only.
3. **Continuum DeWitt / QG** — residual form only; Regge discrete toy is the next falsifiable experiment (PO-021).
4. **Estate-wide quotient-norm / \(\Phi_k\) theorem** — dual zero-gap is **certificate attainment** on declared finite carriers only. Normhood needs genuine \(J_k\) (+ closed \(\mathrm{im}\,d\)); do not claim “norm because the inf is attained.” Kill: `ATTAINMENT_AS_ESTATE_QUOTIENT_NORM`.
   - **Scoped progress (2026-08-10):** `solv_finite_quotient_norm.verify_finite_declared_quotient_norm` → `COMPUTATIONALLY_VERIFIED_SCOPED` on declared carriers; spine `finite_declared_quotient_norm=AVAILABLE`; **estate-wide still REFUSED**.
5. **Lean** — ignored this sprint; PCC/WGOC/CGOC remain ORPHAN until lake rewired.

---

## Non-claims

- No GlobalGreen, ActionLicense, or AuthorityEffect ≠ None.
- No estate-wide \(\Phi_k\) theorem for all carriers.
- No LS surrogate as canonical (kill test `LS_AS_CANONICAL`).
- No float sold as exact (kill test `FLOAT_AS_EXACT`).
- No normhood-from-attainment alone / estate quotient-norm seal (kill `ATTAINMENT_AS_ESTATE_QUOTIENT_NORM`).
