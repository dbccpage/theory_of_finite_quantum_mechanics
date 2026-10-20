# CC-31 through CC-35: proof-to-kernel targets

The general written arguments for CC-26..30 are saved in proof_notes.md. These targets request full formal statements/proofs or kernel transport, not more finite fixtures. They do not replace the pending BR, RS, GF or HL requests.

CC-31. Formalize the d^2 normalized probe-state inversion for arbitrary positive d over Q(i). Prove that trace normalization on this set implies trace preservation for every matrix. Keep K-linearity and the Choi/Hermitian-PSD admission hypotheses explicit. Include d=1.

CC-32. Prove the rectangular classical-kernel composition obstruction and its dual diagonal-effect criterion with exact input/intermediate/output dimensions. Distinguish sufficient no-creation/no-detection conditions from the exact pairwise condition. Give the retained inverse-rotation failure and disjoint-coherence success as corollaries.

CC-33. Construct the category of dephased objects (M_d,Delta_d), identify its morphisms with rational column-stochastic matrices, and verify identity Delta_d and composition. Contrast its declared identity with the ordinary identity in the full CPTP category. Include typed zero CP maps without calling them TP.

CC-34. Derive the general Choi link contraction and tensor-leg permutation in input-first coordinates, explicitly stating every transpose, conjugation and index order. Prove composition, tensor and dual transport descend to operational map equality. State the symmetric monoidal category and its non-vector-space hom-sets.

CC-35. Prove the Householder-like Gaussian-rational unitary formula and inductive isometry completion, with nonzero denominator, e1, square, scalar phase and empty-column recursion branches. Separate assumed unit norm from any norm-equation solving. Transport the proof to Lean rather than extrapolating from the replay list.
