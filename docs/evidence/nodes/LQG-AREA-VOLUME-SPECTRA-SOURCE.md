# LQG-AREA-VOLUME-SPECTRA-SOURCE

Stage: [LOOP_QUANTUM_GRAVITY](../stages/LOOP_QUANTUM_GRAVITY.md). Status: `SOURCE_RECORD`. Evidence grade: **E0**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Rovelli and Smolin (1995, arXiv:gr-qc/9411005, Section 1 eqs. (1)-(2) p. 4 and Section 4 eqs. (47)-(48) p. 28) and Ashtekar and Lewandowski (1997, arXiv:gr-qc/9602046, Section 3.3 eq. (3.20) p. 16 and Section 4.1 eqs. (4.7)-(4.9), (4.12) pp. 18-19) compute discrete spectra for loop-quantum-gravity area (and volume) operators. In the convention {A_a^i(x), E_j^b(y)} = G delta_a^b delta_j^i delta^3(x,y) used in both papers, the general area eigenvalue is (l_P^2 / 2) sum_v sqrt(2 j_v^(d)(j_v^(d)+1) + 2 j_v^(u)(j_v^(u)+1) - j_v^(d+u)(j_v^(d+u)+1)) (eq. (4.9) of gr-qc/9602046), which for simple transverse punctures without tangential edges (j^(d)=j^(u)=j_i, j^(d+u)=0) equals l_P^2 sum_i sqrt(j_i(j_i+1)) = (l_P^2 / 2) sum_i sqrt(p_i(p_i+2)) with p_i = 2 j_i (eq. (2) and eq. (47) of gr-qc/9411005; eq. (4.12) of gr-qc/9602046); as Ashtekar and Lewandowski note in Section 3.3 footnote 6 (p. 16) and Engle et al. write in arXiv:0711.0146 Section V eq. (36) (p. 11), restoring the 8 pi G gamma factor from the gravitational action and Barbero-Immirzi parameter gamma multiplies this spectrum by 8 pi gamma, giving 8 pi gamma l_P^2 sum_i sqrt(j_i(j_i+1)). (The nonzero trivalent volume formula in eq. (1) and eq. (37) of gr-qc/9411005 was corrected in the erratum Nucl. Phys. B 456 (1995) 753, where trivalent vertices have zero volume.) This node records both papers and their normalization conventions.

## Grade

Evidence grade **E0** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 0
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- distinct cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite at least one in-repo file that bears on the statement

## Flags

None. Status and evidence are consistent under the rules in the overview.

## Imported structure

None recorded.

## Bottleneck

Record only. Both normalization conventions (l_P^2 vs 8 pi gamma l_P^2, per Ashtekar-Lewandowski Section 3.3 footnote 6 p. 16) and the general vertex-puncture formula (eq. (4.9) p. 18) were audited against the papers on 2026-10-22.

## Source status

Audited against the full texts of arXiv:gr-qc/9411005 (Section 1 eqs. (1)-(2) p. 4, Section 3 eq. (37) p. 22, Section 4 eqs. (47)-(48) p. 28) and arXiv:gr-qc/9602046 (Section 3.3 eq. (3.20) and footnote 6 p. 16, Section 4.1 eqs. (4.7)-(4.9), (4.12) pp. 18-19) on 2026-10-22; recorded as an external source record.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Documents and data: `dag/derivations/33_loop_quantum_gravity/tfq_2303_lqg_area_volume_spectra_source.md`

- file: [dag/derivations/33_loop_quantum_gravity/tfq_2303_lqg_area_volume_spectra_source.md](../../../dag/derivations/33_loop_quantum_gravity/tfq_2303_lqg_area_volume_spectra_source.md)
- sha256 (`lf-normalised`): `e01790567327f0718426a758c88ce7678aef864de09784566f6af0be379fea6f`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2303
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:gr-qc/9411005`
- `external:arXiv:gr-qc/9602046`

## Routes

Incoming (1):

- `FRO-R-LQG-AREA-VOLUME-SPECTRA-SOURCE` `RECORD_PARENT`: [LQG-SPIN-NETWORK-KINEMATICS-SOURCE](LQG-SPIN-NETWORK-KINEMATICS-SOURCE.md) (SOURCE_RECORD)

Outgoing (1):

- `FRO-R-LQG-AREA-SPECTRUM-EXACT-TARGET` `DERIVED_LEAN`: [LQG-AREA-SPECTRUM-EXACT-TARGET](LQG-AREA-SPECTRUM-EXACT-TARGET.md) (PROVED_LEAN)
