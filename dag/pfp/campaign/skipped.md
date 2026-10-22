# Derivation Campaign: Skipped Coordination and Custody Records

AuthorityEffect: None.

Per `dag/pfp/campaign/README.md`, targets in `dag/pfp/campaign/derivation_queue.json` are taken in strict rank order. A node is skipped only if it is an administrative, coordination, or boundary custody record rather than a single self-contained mathematical claim.

The following 5 nodes are recorded as skipped in accordance with the campaign instructions:

| Rank | Node ID | Stage | Status | Downstream | Score | Reason for Skip |
|:---:|:---|:---|:---:|:---:|:---:|:---|
| 1 | `TFQ-0006` | `L1_TO_L2` | `OPEN` | 183 | 549 | Summary record of all L1→L2 imports; addressed through its constituent component nodes rather than a single proof target. |
| 3 | `TFQ-0008` | `FINITE_QM_DYNAMICS` | `OPEN` | 80 | 240 | Stage coordination record separating finite instruments, path sums, and channels from continuum generators rather than an isolated theorem. |
| 4 | `TFQ-0009` | `FINITE_GAUGE` | `OPEN` | 57 | 57 | Stage summary record for finite gauge connection, holonomy, and curvature definitions across three languages. |
| 5 | `TFQ-0012` | `FINITE_QCD` | `OPEN` | 54 | 54 | Custody and boundary obligation separating the Q8 quaternion gauge shadow from missing Hopf gauge data. |
| 9 | `TFQ-0014` | `FINITE_QCD` | `OPEN` | 28 | 28 | Boundary obligation preventing citation of groupoid convolution and qubit packet complexes as the color connection. |
