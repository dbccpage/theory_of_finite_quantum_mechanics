# [TFQ-0403] Prime-power MUB construction and exact field obligations

**Stage:** `MUTUALLY_UNBIASED_BASES` | **Status:** `OPEN_OBLIGATION` | **AuthorityEffect:** None.

**Parent:** [TFQ-0402](../25_mub/tfq_0402_mub_exact_projectors.md)
**DAG node:** `MUB-PRIME-POWER-CONSTRUCTION`
**Required DAG inputs:** `MUB-EXACT-PROJECTORS`

## Statement and derivation

The target is a parameterized construction at d=p^n, not a list of numerical
matrices. State the finite field, additive character, Weyl relations, commuting
classes and exact scalar field, then derive each projector resolution and every
cross-class trace pairing. Characteristic two must have its own valid construction
and phase convention rather than silently dividing by two.

Existing dimension-three and dimension-four source records are starting witnesses,
not a mechanized theorem for every prime power. Record their hypotheses and replay
their exact certificates before generalization. A composite dimension outside the
proved construction stays outside its conclusion.

## Evidence and next obligation

- [papers/core/mub6/README.md](../../../papers/core/mub6/README.md)

Provide the construction and all pairwise trace identities for the admitted dimension; do not infer a dimension-six family from smaller dimensions.
