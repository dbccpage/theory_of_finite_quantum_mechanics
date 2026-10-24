# Pre-Commit Claim Hygiene & Scope Review: `CT-INFORMATION-MEDIA-INTEROPERABILITY` (`TFQ-2006`)

- **Date**: 2026-10-24
- **Branch**: `campaign/ct-information-media-interoperability`
- **Target Node**: `CT-INFORMATION-MEDIA-INTEROPERABILITY` (`TFQ-2006`, `CONSTRUCTOR_THEORY`)
- **Status**: `IMPORTED_ASSUMPTION` (narrowed to exact finite/algebraic components and non-selection scope fences, `E0 -> E3`)

## 1. What It Supports
- Formalizes in [`lean4/CampaignCtInformationMediaInteroperability.lean`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/lean4/CampaignCtInformationMediaInteroperability.lean) (`L4D`, 11 theorems, 0 `sorry`, standard axioms only, 6/6 semantic mutations killed) and [`checks/independent/ct-information-media-interoperability.py`](file:///c:/Users/a343o/source/repos/theory_of_finite_quantum_mechanics/checks/independent/ct-information-media-interoperability.py) (`checks=4408`, `failures=0`) the finite deterministic core of Constructor Theory Principle III (Deutsch & Marletto 2015, `arXiv:1405.5563`, Sections 3–6 pp. 9–12):
  1. Reversible CNOT / modular addition cloning on $\mathbb{Z}_n \times \mathbb{Z}_n$ with blank attribute $0$, two-sided inverse $\mathrm{cnotUnclone}_n$, and $\mathbb{Z}_2$ involutivity.
  2. Computation variable cardinality threshold ($|\mathrm{Fin}\ 1| = 1$ has trivial permutation group of size $1$, whereas $\mathrm{Fin}(n+2)$ admits distinct attributes $0 \neq 1$ swapped by $\mathrm{Equiv.swap}\ 0\ 1$) and distinguishability via injective cloning.
  3. Principle III composite Cartesian cloning on $\mathbb{Z}_{n_1} \times \mathbb{Z}_{n_2}$ with composite blank $(0, 0)$, composite attribute cardinality $d_1 d_2$, and cross-medium copy/permutation recoding.
  4. Explicit mathematical fences showing why Principle III does not discharge `FQ-GAP-TENSOR-UNIQUENESS` (`TFQ-2007`): off-diagonal entanglement under 2-qubit CNOT on $(|0\rangle + |1\rangle) \otimes |0\rangle$, the four-way state-space dimension trichotomy ($3 < 9 < 10 < 16$ at $d_1 = d_2 = 2$), real vs complex local tomography holism excess, and PSD vs Partially-Transposed (PT) cone agreement on all classical diagonal states alongside separation by the Bell witness on the singlet vector.

## 2. What It Does Not Support
- Does not claim that Constructor Theory Principle III derives the complex Hilbert-space tensor product $\mathcal{H}_1 \otimes_{\mathbb{C}} \mathcal{H}_2$ or selects the bipartite PSD cone (`FQ-GAP-TENSOR-UNIQUENESS` remains an explicit open gap).

## 3. Narrowest Defensible Claim
- On finite deterministic substrates, Principle III induces the Cartesian composite attribute set $S_1 \times S_2$ of size $d_1 d_2$ with componentwise reversible cloning $\mathrm{compositeClone}_{n_1, n_2}$, which is shared by classical simplex, real quantum, complex quantum, and partially-transposed bipartite state spaces and therefore leaves `FQ-GAP-TENSOR-UNIQUENESS` open.

## 4. Next Test Needed
- Narrow `FSP-BF-2GROUP-SIGN-CLAIM` (`TFQ-1210`) and `FSP-COBORDISM-INTRINSIC-SIGN` (`TFQ-1211`) in the fermion-sign frontier queue.
