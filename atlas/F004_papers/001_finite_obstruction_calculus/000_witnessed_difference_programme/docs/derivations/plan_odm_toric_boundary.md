# Toric model boundary

**Status.** Boundary derivation for `PLAN-ODM-TORIC`. The statement is the
boundary. Theorems A and B are not proved here, and Gates D, F, and G are
not closed.

**Witness.** `plan-odm-toric-boundary`,
`problem_sha256` `51971b55aa04fb879116e1ed4784b9801bef3c24b6782110a505458e8bf2206b`,
receipt
[`evidence/plan_odm_toric_boundary_receipt.json`](../../evidence/plan_odm_toric_boundary_receipt.json).
The checker is
[`code/witnessed_difference/plan_odm_toric_boundary.py`](../../code/witnessed_difference/plan_odm_toric_boundary.py).
It reads the historical Gate E receipt and does not rewrite it.

## 1. The admitted boundary

The source anchor is the sentence in
[`outstanding_derivations_master.md`](../../../plans/outstanding_derivations_master.md)
that begins "Theorems A and B and Gates D, F, and G stay open as model".
Appendix W.8 of the manuscript states the same cut: the checked point is
\(L=4\), \(M=1\), \(r=1/10\), the quadratic value is \(-1/88305\), and one
finite point is not a universal finite-\(M\) claim.

The current dossier names the proposals that stay unproved: Theorem A is a
continuous-time Gaussian field, Theorem B is a joint discrete volume/time
limit, and Gate D is the complex winding-sector estimate. The inventory
keeps Gate F as the spacetime Ursell bound and Gate G as mode extinction.
Those five items stay model proposals. This note does not supply their
missing estimates.

## 2. The single Gate E point

The frozen receipt
[`gate_e_exact_counterexample_receipt.json`](../meron_field_limit_derivations/code/gate_e_exact_counterexample_receipt.json)
records \(r=1/10\), eigenvalue \(-1/706440\), test vector
\((-1,-1,-1,-1,+1,+1,+1,+1)\), quadratic value \(-1/88305\), and
`is_positive_semidefinite` false. Its bytes are
`564c2f668339eac0b2b34c35628bf77d5f5c64f15422e6ff1c642b0ea569fe49`.
The receipt does not store \(L\), \(M\), or a scaling formula. \(L=4\) and
\(M=1\) are the point named by W.8 and by the checker docstring.

The eight coordinates of the recorded vector have squared length 8, and
\[
8\cdot\Bigl(-\frac{1}{706440}\Bigr)=-\frac{1}{88305}.
\]
The recorded spectrum has total multiplicity 8, which matches two layers of
length \(L=4\) and does not identify any other carrier. The radius
\(r=1/10\) lies outside the declared region \(r\le 1/192\). The receipt text
does not contain the asymptotic formula \(\lambda_{\min}\sim-(1/9)(r/M)^4\).

## 3. What stays unproved

Theorem A, Theorem B, Gate D, Gate F, and Gate G stay open. The one Gate E
point is not an all-\(M\) theorem, not a spacetime topology, not a covariance
kernel, and not a joint \((L,M)\) schedule. The historical writer is not run.
