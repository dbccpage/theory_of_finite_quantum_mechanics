# Documentation Navigation Matrix: The Four-Quadrant Architecture

The documentation for the Witnessed Difference Programme is partitioned into **four typed quadrants**, establishing an immediate, unambiguous separation between verified assets, open derivation targets, archived historical transcripts, and long-term roadmap obligations.

```text
docs/
├── README.md                   <-- You are here: Master Documentation Navigation Matrix
├── 01_substantiated/           <-- Quadrant 1: Exists / Substantiated (Verified proofs, core notes)
├── 02_requiring_derivation/    <-- Quadrant 2: Requires Derivation (Open proofs, active conjectures)
└── 04_roadmap_and_gaps/        <-- Quadrant 4: Remains to be Derived (Bridge register, continuum limits)
```

---

## The Four Quadrants at a Glance

| Quadrant | Focus & Epistemic Status | Primary Contents | Guide |
|---|---|---|---|
| **`01_substantiated/`** | **Exists / Grounded**<br>Formally verified proofs, completed derivations, and confirmed claim ledgers. | Verified proofs (`guarded_schedule_topology.md`, `sparse_guarded_chain_transport.md`, etc.), 20 completed derivation notes in `derivations/`, execution receipts, and absorbed WD2 classical Moore machine package. | [Quadrant 1 Guide](01_substantiated/README.md) |
| **`02_requiring_derivation/`** | **Requires Derivation**<br>Open conjectures, partial formulations, and active targets. | The 5 Outstanding Derivations (`five_outstanding_derivations.md`), Meron field limit derivations (`meron_field_limit_derivations/`), affine thickening conjecture (`affine_thickening_conjecture.md`), and WD2 open Lean targets (`wd2_open_targets.md`). | [Quadrant 2 Guide](02_requiring_derivation/README.md) |
| *(third quadrant)* | **Deleted**<br>Superseded swarms, historical snapshots and deletion candidates. | The 14 withdrawn swarm transcripts, the historical code snapshots and the informal essays were deleted from the tree; git history keeps them. | none |
| **`04_roadmap_and_gaps/`** | **Remains to be Derived**<br>Unclosed bridge obligations and physical limits. | Genesis bridge obligations (`genesis_bridge_register.md` for `GEN-WDP-O01`..`O05`), DAG alignment (`PG-WDP-GENESIS-BRIDGE-OBLIGATIONS`), and long-term continuum limits. | [Quadrant 4 Guide](04_roadmap_and_gaps/README.md) |

---

## Instructions for Researchers & Automated Agents

1. **When verifying mathematical correctness or running replay suites:**
   - Consult `01_substantiated/` and the master monograph `witnessed_difference_programme.md`.
   - Never treat files in `02_requiring_derivation/` or `04_roadmap_and_gaps/` as established theorems.
2. **When identifying open research problems or generating derivation targets:**
   - Consult `02_requiring_derivation/` and `04_roadmap_and_gaps/`.
   - Check `dag/derivation_dag.json` for corresponding node IDs (`TFQ-0559` through `TFQ-0580`).
3. **When indexing code or building symbol trees:**
   - The historical snapshots that once sat in a third quadrant are no longer in the tree.
