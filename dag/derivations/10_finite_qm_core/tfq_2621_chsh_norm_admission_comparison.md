# [TFQ-2621] CHSH as a test of the admitted norm geometry

> **Stage**: `FINITE_QM_CORE` | **Status**: `PROVED_LEAN`  
> **DAG node**: `FQ-CHSH-NORM-ADMISSION-COMPARISON`  
> **Parent record**: `TFQ-0260` (comparison context, not a derivation prerequisite)

**AuthorityEffect:** None. This slice compares explicitly supplied mathematical models. It does not derive the geometric premises from primitive difference or close the Genesis-to-Hilbert gap.

## 1. The common task and its price

Let $V$ be a real normed vector space, let $y_0,y_1\in V$ satisfy $\|y_j\|\le1$, and let $f_0,f_1:V\to\mathbb R$ be linear effects satisfying $|f_i(v)|\le\|v\|$ for every $v$. Define

\[
 E_{ij}=f_i(y_j),\qquad
 S=E_{00}+E_{01}+E_{10}-E_{11}.
\]

This interface supplies the vector space, norm, effects, and response rule. It does not obtain them from an inscription. It also does not assume a common positive distribution of all four counterfactual outcomes. The intended examples are two-dimensional; the following upper bounds do not require finite dimension. The real scalar field and normed carrier are admissions. Even the two-dimensional real example has an infinite underlying set; finite dimension does not make this a finite-carrier reconstruction.

Linearity and the effect bounds give

\[
 |S|\le\|y_0+y_1\|+\|y_0-y_1\|\le4.
\]

This is a general upper bound. No claim that every normed space attains it is made. In the examples below the effects and vectors are explicitly exhibited.

For outcomes $a,b\in\{-1,1\}$, the shared readout is

\[
 p(a,b\mid i,j)=\frac{1+abE_{ij}}4.
\]

Since $|E_{ij}|\le1$, these tables are nonnegative and normalized, with both marginals $1/2$. They therefore provide a precise no-signalling comparison. Table validity does not construct sequential instruments or arbitrary composites.

## 2. Where the square root enters

Assume the parallelogram law for the norm. Then

\[
 \|y_0+y_1\|^2+\|y_0-y_1\|^2
 =2\|y_0\|^2+2\|y_1\|^2\le4.
\]

The scalar inequality $(r+s)^2\le2(r^2+s^2)$ therefore yields $S^2\le8$, hence $|S|\le2\sqrt2$. This exposes the quadratic geometric premise used at the bound.

The real polarization formula

\[
 \langle u,v\rangle=\frac{\|u+v\|^2-\|u-v\|^2}{4}
\]

reconstructs a compatible inner product from a norm satisfying the parallelogram law, through Mathlib's existing norm-to-inner-product construction. Conversely an inner-product norm satisfies that law. Replacing the word “inner product” by the parallelogram premise is thus an equivalent geometric formulation; it does not eliminate the admission. This equivalence concerns norms and inner products, not an assertion that a CHSH ceiling alone characterizes Hilbert spaces.

## 3. Exact controls in the same interface

| Geometry | Vectors $y_0,y_1$ | Effects $f_0,f_1$ | CHSH value |
|---|---|---|---|
| $\ell_1^2$ | $(1,0),(0,1)$ | $v_1+v_2,\ v_1-v_2$ | $4$ |
| $\ell_\infty^2$ | $(1,1),(1,-1)$ | $v_1,\ v_2$ | $4$ |
| $\ell_2^2$ | $(1,0),(0,1)$ | $(v_1+v_2)/\sqrt2,\ (v_1-v_2)/\sqrt2$ | $2\sqrt2$ |

The first two rows yield the same PR correlators $(1,1,1,-1)$. The Euclidean row yields $(1,1,1,-1)/\sqrt2$. The $\ell_1$ example violates the parallelogram identity, so the quadratic proof cannot be reused there.

A separate classical control assumes a single nonnegative mixture of deterministic four-sign assignments. Every assignment has CHSH value $\pm2$, and every such mixture obeys $|S|\le2$. This local bound is a positive-global-joint property, not a theorem that every model labelled $\ell_1$ has CHSH bound $2$.

Different positive Gram matrices on the same coordinate module do not by themselves defeat the quantum bound. They remain inner-product geometries when states and effects are transported consistently. An operational distinction requires specifying what is held fixed under that change.

## 4. Evidence and unfinished questions

The formal interface and inequalities live in `lean4/CHSHNormAdmission.lean`, namespace `CHSHNormAdmission`. Independent exact arithmetic controls live in `code/python/src/qm/chsh_norm_admission.py`. Fresh compilation, theorem/axiom results, hashes and negative controls are recorded in `evidence/chsh_norm_admission/verification.json`; the DAG-validation comparison is separate. The new Lean module compiled successfully without warnings. Its 28 theorem anchors report only `propext`, `Classical.choice` and `Quot.sound`; the general inequalities need no finite-dimension hypothesis. The replay driver is `evidence/chsh_norm_admission/verify.py`. `PROVED_LEAN` refers to its explicitly conditional statements and coordinate witnesses; the admitted premises remain visible.

The existing sector-form uniqueness theorem remains conditional on quadratic readout shape, sector additivity and transitive sector symmetry. The new comparison does not derive these premises, tensor composition or the Born readout from upstream assumptions. It also leaves `L1-R-INNER-PRODUCT-GAP` and `DS-QM073-BELL-THEOREM-OBSTRUCTED` open.

The incoming `RECORD_PARENT` route records the shared Bell comparison question. It is not an implication from a classical positive joint distribution to the PR or Euclidean examples. The remaining question is which additional, explicitly supplied upstream assumptions imply the geometric premises, and which alternatives remain when each assumption is removed.

## 5. Sources and credit

- The existing [Bell.Quantum.sum_difference_bound](C:/Users/a343o/source/repos/cognitive_warfare_and_institutional_and_actor_governance/papers/003_bell_positive_extensions_and_projection_residuals/lean4/Bell/Quantum.lean:37) uses the sum/difference argument and calls the parallelogram law. It is a read-only source for this slice, not a newly compiled dependency.
- Mathlib `Analysis.InnerProductSpace.OfNorm` supplies `InnerProductSpace.ofNorm`; the local reconstruction theorem applies this existing result and records the real polarization formula.
- Craig, Dowker, Henson, Major, Rideout and Sorkin, [A Bell Inequality Analog in Quantum Measure Theory](https://arxiv.org/abs/quant-ph/0605008), derive the corresponding bound through a Hilbert-space construction from a strongly positive quantal measure. Strong positivity is an alternative structural premise to audit; this slice does not formalize that paper or derive that premise.
