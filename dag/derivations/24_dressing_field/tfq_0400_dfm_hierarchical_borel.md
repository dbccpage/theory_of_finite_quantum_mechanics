# [TFQ-0400] Hierarchical Borel dressing beyond the diamond control

**Stage:** `DRESSING_FIELD` | **Status:** `OPEN_OBLIGATION` | **AuthorityEffect:** None.

**Parent:** [TFQ-0399](../24_dressing_field/tfq_0399_dfm_tree_change.md)
**DAG node:** `DFM-HIERARCHICAL-BOREL`
**Required DAG inputs:** `DFM-TREE-CHANGE`

## Statement and derivation

The existing QM-213 control uses invertible upper-triangular rational matrices
B_2(Q)=T⋉N. It factors tree transports into diagonal and unipotent factors,
neutralizes the unipotent part first, then the diagonal part. This branch asks for
the same assertions on a supplied arbitrary finite graph and, separately, on an
explicit incidence differential graded algebra.

Required statements are: uniqueness of the factorization; stage-one membership
in N using normality; preservation of the quotient projection; equality of the
two-stage dressing with full tree dressing; and curvature covariance for the
specified differential and cup product. Refusal must cover singular matrices and
an invalid quotient or DGA interface. The graph theorem does not supply these
extra structures. The B_2(Q) carrier is not SU(3). The existing TFQ-0016 remains
the source obligation; this is its connected research continuation, not a duplicate
claim that a general Lean result already exists.

## Evidence and next obligation

- [dag/research/hierarchical_nonabelian_dfm_finite_map.md](../../../dag/research/hierarchical_nonabelian_dfm_finite_map.md)

Supply the general factorization, quotient-action and incidence-DGA proof before replacing the existing finite control by a general theorem.
