# [TFQ-0403] Prime-power MUB construction and exact field obligations

**Stage:** `MUTUALLY_UNBIASED_BASES` | **Status:** `OPEN_OBLIGATION` | **AuthorityEffect:** None.

**Parent:** [TFQ-0402](../25_mub/tfq_0402_mub_exact_projectors.md)
**DAG node:** `MUB-PRIME-POWER-CONSTRUCTION`
**Required DAG inputs:** `MUB-EXACT-PROJECTORS`

## Statement and derivation

Narrowed boundary, status left OPEN. In dimension 2, the bases
Z = ((1, 0), (0, 1)), X = ((1, 1), (1, -1)) and Y = ((1, i), (1, -i))
are unnormalized Gaussian-integer representatives of mutually unbiased bases of C^2 after normalization. Squared norms are 1, 1, 2, 2, 2 and 2.
Vectors in one basis have inner product 0. For a vector from one basis and a vector from
another, twice the squared modulus of the inner product equals the product of the squared
norms. The square of i is -1. The additive character of the two-element field sends 0 to 1
and 1 to -1, and it sends 1+1 to 1.

The original target remains a parameterized construction at d=p^n. Characteristic two is
recorded here by the Pauli bases above, without dividing by two. Odd characteristic, every
larger prime power, and dimension six stay outside this conclusion.

## Evidence and next obligation

- [papers/core/mub6/README.md](../../../papers/core/mub6/README.md)

Provide the construction and all pairwise trace identities for the admitted dimension; do not infer a dimension-six family from smaller dimensions.
