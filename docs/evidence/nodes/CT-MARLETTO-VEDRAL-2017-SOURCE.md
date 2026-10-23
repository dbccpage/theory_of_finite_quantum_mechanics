# CT-MARLETTO-VEDRAL-2017-SOURCE

Stage: [CONSTRUCTOR_THEORY](../stages/CONSTRUCTOR_THEORY.md). Status: `SOURCE_RECORD`. Evidence grade: **E1**. [Evidence map overview](../README.md). AuthorityEffect: None.

## Statement

> Marletto and Vedral (2017, arXiv:1707.06036, pp. 1-4, Fig. 1) argue within constructor theory that if a mediator M locally couples two quantum systems Q1 and Q2 (via Q1 \<-\> M \<-\> Q2 with no direct Q1-Q2 coupling) and generates entanglement from a product state, then M must carry at least two incompatible observables (a superinformation medium), and propose testing gravitationally induced phases between two interferometric masses; Bose et al. (2017, arXiv:1707.06050, pp. 1-5, eqs. (1)-(8)) independently propose a spin-correlation entanglement witness W = |(sigma_x^(1) tensor sigma_z^(2)) + (sigma_y^(1) tensor sigma_y^(2))| \> 1 (eq. (8) p. 4) for two Stern-Gerlach interferometers interacting through Newtonian gravity phases delta phi_+- and delta phi_-+ (eqs. (2)-(4) p. 2). This node records both papers; no experiment is claimed to have been performed.

## Grade

Evidence grade **E1** (rules in the [overview](../README.md#evidence-grades)). The grade rates the evidence this checkout holds; it is separate from the status.

- counted in-repo evidence files: 2
- cited Lean, Rust or Python symbols found in their in-repo files: 0
- cited Lean declarations covered by a current replay receipt: 0
- counted in-repo runnable tests: 0
- counted in-repo Rust or Python files that are not tests: 0
- recorded statement-match reviews that qualify: 0
- next step to raise the grade: cite a Lean, Rust or Python symbol that exists in an in-repo file

## Flags

- `receipt_not_current`: lean4/DualWitness.lean: replay failed against 1 receipt(s). A replay receipt exists for a cited Lean file, but its sha256 no longer matches the file, it records a failure, or it records no passed axiom audit.

## Imported structure

None recorded.

## Bottleneck

Record only. Audited against arXiv:1707.06036 and arXiv:1707.06050; the repository makes no physical claim about gravity.

## Source status

Audited against the full texts of arXiv:1707.06036 (pp. 1-4) and arXiv:1707.06050 (pp. 1-5, eqs. (1)-(8)) on 2026-10-22; recorded as an external source record.

## Review

No recorded statement-match review.

## Evidence items

Items are grouped by file. "Counts" means the item counts toward the grade: the file is in this checkout, the citation is the node's own (or an exclusive record's), and the file is not a generated view. To list the axioms of a cited Lean declaration, build its module and run `#print axioms <name>` in a scratch file that imports it.

### Lean: `lean4/DualWitness.lean`

- file: [lean4/DualWitness.lean](../../../lean4/DualWitness.lean)
- sha256 (`bytes`): `b69a5a5b0f7e69541787915ccd48e7b29b687e04a54d838b556936e034e7f7f7`
- cited in: node.source
- replay: `failed`
  - receipt [dag/research/lean_replay_campaign_finite_qm_structure.json](../../../dag/research/lean_replay_campaign_finite_qm_structure.json) (module `DualWitness`): recorded sha256 `b69a5a5b0f7e69541787915ccd48e7b29b687e04a54d838b556936e034e7f7f7` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: no; axioms recorded: propext; only standard axioms: yes
- check: `cd lean4 && lake build DualWitness`
- counts toward the grade: yes

### Lean: `lean4/Entanglement.lean`

- file: [lean4/Entanglement.lean](../../../lean4/Entanglement.lean)
- sha256 (`bytes`): `bccd871b9f8db03c35b564c1a3e41d10d51095a936f2ff4c8980a4bc1195f79d`
- cited in: node.source
- replay: `verified`
  - receipt [dag/research/lean_replay_campaign_constructor_theory.json](../../../dag/research/lean_replay_campaign_constructor_theory.json) (module `Entanglement`): recorded sha256 `bccd871b9f8db03c35b564c1a3e41d10d51095a936f2ff4c8980a4bc1195f79d` matches the current file; exit code 0; Lean 4.35.0; Mathlib `56a005855ea1`; axiom audit passed: yes; axioms recorded: Quot.sound, propext; only standard axioms: yes
- check: `cd lean4 && lake build Entanglement`
- counts toward the grade: yes

### Documents and data: `dag/derivations/30_constructor_theory/tfq_2012_ct_marletto_vedral_2017_source.md`

- file: [dag/derivations/30_constructor_theory/tfq_2012_ct_marletto_vedral_2017_source.md](../../../dag/derivations/30_constructor_theory/tfq_2012_ct_marletto_vedral_2017_source.md)
- sha256 (`lf-normalised`): `b88fbfa6f703df3e0c5a54508772238065aa04fb4c4572ef682f08b2597de87c`
- generated view: listed, not counted
- cited in: node.source, record TFQ-2012
- counts toward the grade: no

### External sources

Named by the node; not in this repository and not checked here.

- `external:arXiv:1707.06036`
- `external:arXiv:1707.06050`

## Routes

Incoming (1):

- `FRO-R-CT-MARLETTO-VEDRAL-2017-SOURCE` `RECORD_PARENT`: [DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS](DS-QM071-ENTANGLEMENT-WITNESS-SOUNDNESS.md) (PROVED_LEAN)

Outgoing (1):

- `FRO-R-CT-LOCAL-MEDIATOR-ENTANGLEMENT-IMPORT` `CONDITIONAL_ON_IMPORT`: [CT-LOCAL-MEDIATOR-ENTANGLEMENT-IMPORT](CT-LOCAL-MEDIATOR-ENTANGLEMENT-IMPORT.md) (IMPORTED_ASSUMPTION)
