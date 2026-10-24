# [TFQ-0409] Efficient sampling and general FSP obligations

**Stage:** `FERMION_SIGN` | **Status:** `OPEN_OBLIGATION` | **AuthorityEffect:** None.

**Parent:** [TFQ-0408](../26_fsp/tfq_0408_fsp_hubbard_protected_representations.md)
**DAG node:** `FSP-EFFICIENT-SAMPLING-OBLIGATIONS`
**Required DAG inputs:** `FSP-HUBBARD-PROTECTED-REPRESENTATIONS`, `FSP-MERON-CHARACTER-CANCELLATION`

## Statement and derivation

A computational claim needs an explicit model family and input encoding.
Price the representation change, evaluation of each weight, partition-function
normalization, precision and sampling cost. Nonnegative weights alone leave
mixing and variance unresolved. Exhaustive enumeration of a finite SQL orbit is
not a polynomial-time algorithm for growing instances.

The branch must distinguish an exact finite identity, a protected sign-free
representation, an efficient sampler for a stated family, and a general FSP
solution. Only the first two have starting evidence in the cited package. This
node leaves algorithmic complexity and unrestricted model coverage open.

## Evidence and next obligation

- [papers/core/fsp/README.md](../../../papers/core/fsp/README.md)
- [lean4/CampaignFspEfficientSamplingObligations.lean](../../../lean4/CampaignFspEfficientSamplingObligations.lean)
- [checks/independent/fsp-efficient-sampling-obligations.py](../../../checks/independent/fsp-efficient-sampling-obligations.py)
- [dag/derivations/independent/fsp-efficient-sampling-obligations.md](../independent/fsp-efficient-sampling-obligations.md)

Define input size, transformation cost, estimator variance, normalization and mixing or sampling bounds for the chosen model family.
