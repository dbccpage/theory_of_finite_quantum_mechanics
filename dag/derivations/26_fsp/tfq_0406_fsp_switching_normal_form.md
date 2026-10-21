# [TFQ-0406] Signed-graph switching normal form and class count

**Stage:** `FERMION_SIGN` | **Status:** `PROVED_LEAN` | **AuthorityEffect:** None.

**Parent:** [TFQ-0003](../03_finite_obstruction/tfq_0003_finite_obstruction_calculus_on_a_declared_carrier.md)
**DAG node:** `FSP-SWITCHING-NORMAL-FORM`
**Required DAG inputs:** `IMPL-FSP-SWITCHING-NORMAL-FORM-NF002`

## Statement and derivation

Write an edge-sign assignment as σ∈F₂^E. Vertex switching adds the coboundary
d₀g, where g∈F₂^V and (d₀g)_e=g(s(e))+g(t(e)). Fix a rooted spanning forest.
Starting at its roots, choose g so that every tree edge has transformed sign zero.
The remaining chord coordinates determine the switching class and a canonical
representative. On c connected components there are |V|-c forest edges, leaving
numChord=|E|-|V|+c coordinates and 2^numChord representatives.

The pinned NF-002 Lean source contains `normal_sound`, `same_class_iff`,
`numChord_identity`, `normalForms_length`, `normalForms_nodup` and
`mem_normalForms_iff`. In particular, enumeration length is no longer a residual
counting obligation. The supplied forest and graph-label convention remain premises.

This is the F₂ sign-switching specialization related to graph dressing. It
does not cover graph relabelling, arbitrary basis changes, or construct a fast
sampler for a fermionic partition function.

## Evidence and next obligation

- [dag/results/IMPL-FSP-SWITCHING-NORMAL-FORM-NF002/runs/20261019T215447Z_staged/inputs/the_symbol_game/omega_engine_atlas/coda_atlas/proposals/008_fsp_switching_normal_form/SwitchingNormalForm.lean](../../../dag/results/IMPL-FSP-SWITCHING-NORMAL-FORM-NF002/runs/20261019T215447Z_staged/inputs/the_symbol_game/omega_engine_atlas/coda_atlas/proposals/008_fsp_switching_normal_form/SwitchingNormalForm.lean)
- [dag/results/IMPL-FSP-SWITCHING-NORMAL-FORM-NF002/runs/20261019T215447Z_staged/inputs/the_symbol_game/omega_engine_atlas/coda_atlas/proposals/008_fsp_switching_normal_form/SwitchingNormalForm.lean::normalForms_length](../../../dag/results/IMPL-FSP-SWITCHING-NORMAL-FORM-NF002/runs/20261019T215447Z_staged/inputs/the_symbol_game/omega_engine_atlas/coda_atlas/proposals/008_fsp_switching_normal_form/SwitchingNormalForm.lean)
- [dag/results/IMPL-FSP-SWITCHING-NORMAL-FORM-NF002/runs/20261019T215447Z_staged/inputs/the_symbol_game/omega_engine_atlas/coda_atlas/proposals/008_fsp_switching_normal_form/SwitchingNormalForm.lean::normalForms_nodup](../../../dag/results/IMPL-FSP-SWITCHING-NORMAL-FORM-NF002/runs/20261019T215447Z_staged/inputs/the_symbol_game/omega_engine_atlas/coda_atlas/proposals/008_fsp_switching_normal_form/SwitchingNormalForm.lean)
- [dag/results/IMPL-FSP-SWITCHING-NORMAL-FORM-NF002/runs/20261019T215447Z_staged/inputs/the_symbol_game/omega_engine_atlas/coda_atlas/proposals/008_fsp_switching_normal_form/SwitchingNormalForm.lean::mem_normalForms_iff](../../../dag/results/IMPL-FSP-SWITCHING-NORMAL-FORM-NF002/runs/20261019T215447Z_staged/inputs/the_symbol_game/omega_engine_atlas/coda_atlas/proposals/008_fsp_switching_normal_form/SwitchingNormalForm.lean)

Retain fixed labels and vertex-switching equivalence; this canonicalizer is not a normal form under arbitrary many-body basis transformations.

## Current Lean replay

The [local compatibility port](../../../lean4/SwitchingNormalForm.lean) retains the sealed theorem statements and proof text except for 19 obsolete conditional-elimination lemma spellings. Its source hash and precise transformation are checked by [the branch integration test](../../test_application_branches.py). The original sealed source remains unchanged. Lean 4.33.1 checks the port, and the counting, uniqueness, membership and chord-count theorems use only `propext` and `Quot.sound`.
