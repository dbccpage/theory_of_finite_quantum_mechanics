# Quantum information: what follows from the admitted quantum model

AuthorityEffect: None. Combines state/effect, channel, entropy and repair material.

Fix finite-dimensional complex Hilbert systems, tensor composition, density
matrices and the Born state-effect pairing. Quantum information then studies
how preparations, channels and measurements retain or lose distinguishability.
These are added structures after the primitive/report route, not consequences
of the definition of NP or of a machine that interprets programs.

Classical distributions embed as diagonal matrices. A stochastic matrix K
has a measure-and-prepare quantum lift with Kraus operators
√K(j|i)|j⟩⟨i|. This demonstrates existence of one lift under the quantum
model. It does not recover a unique coherence-sensitive channel from K.
General channels are completely positive and trace preserving; complete
positivity concerns arbitrary admitted ancillas, not just positivity on the
single system. These distinctions are explicit in QM-080/081/082.

Trace distance D(ρ,σ)=½‖ρ−σ‖₁ reduces to total variation distance on
diagonal states. A trace-distance contraction statement is conditional on the
channel class. It cannot be used backwards to derive that class uniquely.

The no-cloning argument uses inner-product preservation: a single unitary
cloning ψ and φ with the same blank would require z=z² for
z=⟨ψ,φ⟩. Distinct nonorthogonal rays violate the resulting modulus equation.
Orthogonal classical basis labels can still be copied; this is why reversible
Boolean computation is compatible with the no-cloning boundary.

For standard spectral states, S(ρ)=−Tr(ρ log ρ). State the logarithm base:
natural-log entropy and entropy in bits have different exact arithmetic
properties. Integer Rényi power sums stay in a declared algebraic field;
generic logarithmic entropies need a separate evaluation interface. The
source-coding and channel-capacity theorems require families of codes, error
criteria and asymptotic limits. A finite entropy calculation alone supplies none
of those operational theorems.

Distance d of a code supplies correction through floor((d−1)/2) errors under
the stated error model. A fault-tolerance theorem additionally needs a noise
class, gadgets, recovery, scheduling and bounds uniform in computation size.
The finite queue and recurrence results in `QCV-*` are useful pieces with
their own premises, not an unconditional hardware threshold.

Sources: [trace norm and dual witnesses](sources/qm_080_cptp_trace_norm_geometry_and_quantum_dual_witnesses.md),
[classical shadows and channel lifts](sources/qm_082_channels_as_stochastic_kernels_and_the_cptp_lift.md),
[repair capacity](sources/qm_102_fault_tolerance_repair_capacity.md),
and the [core proofs](../10_finite_qm_core/sources/finite_quantum_mechanics_proofs.md).
For the standard external theory, see [Watrous's book](https://cs.uwaterloo.ca/~watrous/TQI/)
and [course](https://arxiv.org/abs/2507.11536). The repository's remaining
operational and asymptotic obligations are recorded separately in the DAG.
