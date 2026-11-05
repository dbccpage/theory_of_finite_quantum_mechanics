# Historical build reports and unavailable logs

The older consolidation reported the following six log outcomes. The log
files are absent from this package and were ignored in the pinned Git source.
The table preserves the earlier report; it is not a byte-verified log transcript
or a current build result.

| Source log | Survey record | What the recorded output supports |
|---|---|---|
| `build_coda_foc.log` | FOC log | Several targets built, but GT000 failed and the overall build ended with failure. Not a successful full FOC build. |
| `build_gtla.log` | GTLA log | Reports a successful 17-job scratch build and per-declaration messages. |
| `build_gtmur.log` | MUR log | Reports some built modules and failures in certificate-pasting/loss modules; overall build failed. |
| `build_gtta14.log` | GTTA14 log | Component outputs include successful elaboration and disclosed dependencies; final GT005 import-order error has exit=1. Not a single blanket pass. |
| `build_gttcqbridge.log` | Bridge log | Empty (0 bytes); supplies no compiler-output evidence for the claimed bridge build. |
| `build_paper_q.log` | Q log | Reports a successful eight-job scratch build of the displayed slice, not the entire historical Q estate. |

The source manifest deliberately excludes these unavailable logs. The pinned
recovery note and scanner are external historical sources. Current local Lean
builds and axiom reports concern the twenty-declaration package only and cannot
recertify the old scratch builds.
