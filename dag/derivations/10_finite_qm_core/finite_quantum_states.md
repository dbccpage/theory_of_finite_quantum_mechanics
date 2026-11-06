# Finite quantum states, readout and composition

AuthorityEffect: None. Combined reading of the core and foundations manuscripts.

Fix a scalar carrier with conjugation and an appropriate positivity notion.
In standard finite-dimensional complex QM, states are positive matrices ρ
with Tr ρ=1; effects satisfy 0≤E≤I; a POVM has effects summing to I; and the
declared probability is Tr(ρE). These definitions use the matrix algebra,
positive cone and state-effect pairing. They are not consequences of a
two-mark alphabet. Exact subfields require separate closure checks for each
normalization, spectral decomposition and purification.

Several meanings of finite must remain separate: finite dimension, finite
state cardinality, finite field, finite algorithmic description, and an exact
number-field carrier. A finite-dimensional complex state space is generally
uncountable. An exact algebraic representation can have infinitely many states.
The [guide map](sources/finite_qm_guide_map.md) distinguishes these cases.

The population counterexample in [the Hilbert chapter](../08_l1_to_l2/repair_to_hilbert.md)
shows a failure of descent. Power-rule tests restrict a chosen family of
readouts. Gleason-type results require their frame and dimension hypotheses.
None of these three statements can substitute for the other two.

For two systems, product tables, nonfactorizing tables, nonseparable density
matrices and Bell violations answer different questions. A Bell state and a
classical mixture can share one measurement table. A common joint law bounds
CHSH by 2. A supplied quantum model can violate that bound, while a general
no-signalling table need not satisfy the quantum bound. Contextuality records
an obstruction to a common assignment under specified measurement contexts.

Composition is conditional in `FQ-GAP-TENSOR-UNIQUENESS`. The tomography,
controlled-shift and effect-cone records supply stronger results under their
named local-state, local-effect, dynamical and availability hypotheses.
They should not be replaced by the older bare statement that tensor structure
is missing, nor promoted into selection from primitive difference.

Detailed proofs: [core proofs](sources/finite_quantum_mechanics_proofs.md),
[structure proofs](../12_finite_qm_structure/sources/finite_quantum_foundations_proofs.md),
[tensor proofs](../27_tensor_composition/sources/tensor_composition_proofs.md).
The [core manuscript](sources/finite_quantum_mechanics.md),
[claim ledger](sources/finite_quantum_mechanics_claim_ledger.md) and
[source notes](sources/finite_quantum_mechanics_source_notes.md) preserve the
full derivation history. The DAG status and stated premises govern this reading.
