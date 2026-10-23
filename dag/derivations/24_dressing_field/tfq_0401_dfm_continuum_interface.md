# [TFQ-0401] Dressing-field continuum and physical interpretation obligations

**Stage:** `DRESSING_FIELD` | **Status:** `GAP` | **AuthorityEffect:** None.

**Parent:** [TFQ-0400](../24_dressing_field/tfq_0400_dfm_hierarchical_borel.md)
**DAG node:** `DFM-CONTINUUM-INTERFACE`
**Required DAG inputs:** `DFM-HIERARCHICAL-BOREL`, `FQ-GAP-CONTINUUM-HILBERT-LIFT`

## Statement and derivation

A continuum extension needs an explicit family of finite graphs or complexes,
compatible connection and observable maps, a topology, and a limit theorem.
Smooth patchwise dressings require gluing and regularity statements. A spanning
tree that depends on the whole graph does not establish locality of a continuum
field. Nontrivial holonomy on a punctured finite graph does not by itself classify
a physical symmetry as substantial.

The finite electroweak doublet construction is a specialization on its admitted
rational carrier, with nonzero radial norm and residual symmetry hypotheses.
Neither that control nor TFQ-0398 derives a continuum Standard Model. Keep these
interfaces explicit when linking the existing QED, electroweak and QCD papers.

## Finite non-locality witness

On the supplied rooted tree with vertices `{root, p, a, b}`, tree edges
`root → p`, `p → a` and `root → b`, and chord `a → b`, the rooted dressing
`u(v) = T(v)^{-1}` gives the dressed chord

`U(root → b)^{-1} U(a → b) U(p → a) U(root → p)`,

with the later path factor on the left. The edge `root → p` does not meet
`{a, b}`. Connections that differ only there have the same labels on the closed
star of the chord and unequal dressed chords. With the other three labels
trivial, outer labels `2` and `5` give dressed chords `2` and `5`. This does
not supply a refinement family, a topology, or a convergence theorem.

## Evidence and next obligation

- [dag/research/electroweak_dfm_weinberg_finite_map.md](../../../dag/research/electroweak_dfm_weinberg_finite_map.md)
- [papers/ravera_dfm_dossier.md](../../../papers/ravera_dfm_dossier.md)
- [lean4/CampaignDfmContinuumInterface.lean](../../../lean4/CampaignDfmContinuumInterface.lean)
- [checks/independent/dfm-continuum-interface.py](../../../checks/independent/dfm-continuum-interface.py)

The finite witness is proved. A refinement family, compatibility maps and a convergence theorem are still required before transporting finite identities to smooth gauge theory.
