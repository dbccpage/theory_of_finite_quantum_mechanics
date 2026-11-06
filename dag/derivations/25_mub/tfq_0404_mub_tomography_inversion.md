# [TFQ-0404] Tomography from a supplied complete MUB family

**Stage:** `MUTUALLY_UNBIASED_BASES` | **Status:** `PROVED_PROSE` | **AuthorityEffect:** None.

**Parent:** [TFQ-0402](../25_mub/tfq_0402_mub_exact_projectors.md)
**DAG node:** `MUB-TOMOGRAPHY-INVERSION`
**Required DAG inputs:** `MUB-EXACT-PROJECTORS`

## Statement and derivation

Assume the exact projector contract and a supplied family of d+1 MUBs. Put
Q_{b,j}=P_{b,j}-I/d. Then ∑_j Q_{b,j}=0, and

    tr(Q_{b,j} Q_{c,k}) = δ_{bc}(δ_{jk}-1/d).

For each b this Gram matrix has rank d-1; different b subspaces are orthogonal.
Together their dimensions are (d+1)(d-1)=d²-1, the real dimension of traceless
Hermitian matrices. They span that space. For trace-one Hermitian ρ with
p_{b,j}=tr(ρP_{b,j}), define A=∑_{b,j}p_{b,j}P_{b,j}-I. Its trace is one.
For a fixed P_{c,k}, the same-basis contribution is p_{c,k}, the other d bases
contribute d/d=1, and subtracting I contributes -1. Thus
tr(AP_{c,k})=p_{c,k}=tr(ρP_{c,k}). The traceless difference A-ρ is orthogonal to
the spanning Q family, so A=ρ.

This is a finite-dimensional prose proof under the supplied complete-family
hypothesis. Its general Lean/Rust/Python reconstruction obligation remains open.
It supplies no existence proof for d+1 MUBs in dimension six.

## Evidence and next obligation

- [papers/core/mub6/README.md](../../../papers/core/mub6/README.md)

Mechanize the trace-inner-product dimension and reconstruction argument; constructing a complete MUB family is a separate existence obligation.
