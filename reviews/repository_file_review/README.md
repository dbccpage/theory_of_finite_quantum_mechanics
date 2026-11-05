# Systematic repository file review

AuthorityEffect: None.

## Active systematic pass

The current pass follows the user's required order: finish `checks`, then
continue through `code`. The [current file ledger](current_file_scores.json)
distinguishes completed labels from files still awaiting their current review.
The [November 3 infrastructure review](2026-11-03-checker-infrastructure.md)
records 12 completed L4B sources and five helper files composed and removed.
The [November 3 AdS review](2026-11-03-ads-checkers.md) adds six completed L4B
sources, including the repaired original regression harness. All old contract
histories are retained. The [authority review](2026-11-03-authority-checkers.md)
adds four completed L4B sources for framing, finite semantics and source-record
verification. The [Wilson review](2026-11-03-wilson-checker.md) adds two completed
L4B sources, preserving the finite 110-case boundary. The [strong-coupling
review](2026-11-03-strong-coupling-checker.md) adds two completed L4B sources with
exact threshold matching and bounded power evaluation. The [hinge-lineon
review](2026-11-03-lineon-checker.md) adds two completed L4B sources with owned
path snapshots and exact trace boundaries. The [computation review](2026-11-03-computation-checkers.md)
composes six literal checkers into one bounded verification application, adds
its independent test suite, and reassesses the migrated regression harness.
The [causal-QFT review](2026-11-03-cqft-checkers.md) adds the three repaired
applications, their bounded matrix value and independent suite. The
[constructor-theory review](2026-11-03-constructor-theory-checkers.md) adds two
repaired applications and their independent suite, and corrects the Gaussian
norm cost in its existing assessment. The [BPHZ review](2026-11-03-bphz-checker.md)
adds its repaired application and independent suite. The [CKM review](2026-11-03-ckm-checker.md)
adds its owned Gaussian-table application and independent suite. There are now
42 distinct completed L4B sources before the
[continuum-interface review](2026-11-03-continuum-interface-checker.md), which adds
its bounded SL2 application and independent suite for 44 completed sources.
The [refinement-limit review](2026-11-03-refinement-limit-checker.md) adds its
dyadic-cell application and independent suite for 46 completed sources.
The [electroweak review](2026-11-03-electroweak-checker.md) adds its doublet
application and independent suite for 48 completed sources.
The [Gribov review](2026-11-03-gribov-checker.md) adds its weighted-trace
application and independent suite for 50 completed sources.
The [hierarchical Borel review](2026-11-03-hierarchical-borel-checker.md) adds
its bounded tree application and independent suite for 52 completed sources.
The [Regge review](2026-11-03-regge-checker.md) adds its bounded formula/block
application and independent suite for 54 completed sources.
The [relational-time review](2026-11-03-relational-time-checker.md) adds its
owned schedule application and independent suite for 56 completed sources.
The [Symanzik review](2026-11-03-symanzik-checker.md) adds its owned graph
application and independent suite for 58 completed sources.
The [counterterm review](2026-11-03-counterterm-checker.md) adds its owned
Dirac-kernel application and independent suite for 60 completed sources.
The [continuous-time review](2026-11-03-continuous-time-checker.md) adds its
owned finite-map application and independent suite for 62 completed sources.
The [positive-form review](2026-11-03-positive-forms-checkers.md) composes
two scalar applications into an owned Gram-form application and suite, for
64 completed L4B sources. Exact retired sources remain archived.
The [discrete-dynamics review](2026-11-03-discrete-dynamics-checker.md)
composes the residue-only source into the existing finite-dynamics application
and reassesses its two current sources;64 distinct L4B sources remain completed.
The [Born-boundary composition](2026-11-03-born-controls-checker.md) adds explicit
scalar shares and rotations to the Gram-form application and reassesses its two
current sources;64 distinct L4B sources remain completed.
The [observer-presheaf review](2026-11-03-observer-presheaf-checker.md) adds its
repaired application, six owned components and four independent suites, for
75 distinct completed L4B sources.
The [Gaussian modulo-two review](2026-11-03-mod2-checker.md) adds its owned
frame application, shared inverse component and independent suite, for
78 distinct completed L4B sources.
The [rational-ray review](2026-11-03-rational-rays-checker.md) adds its owned
ray application and independent suite, for80 distinct completed L4B sources.
The [Gaussian extension review](2026-11-03-extension-checker.md) adds three
completed L4B sources, for83 distinct completed sources.
The [binary-colouring review](2026-11-03-colouring-checker.md) adds three
completed L4B sources, for86 distinct completed sources.
The [tomography review](2026-11-03-tomography-checker.md) adds nine
completed L4B sources, for95 distinct completed sources.
The [numeral retirement review](2026-11-03-numeral-retirement.md) removes two
redundant executables after exact archival;95 completed L4B sources remain.
The [integer obstruction review](2026-11-03-integer-obstructions-requirements.json)
brings the total to 98 assessed L4B sources. The Hilbert, Stone and U1 checks
share one exact polynomial model and one census application. The original
sources and companion histories are archived. The final suite detected all
53 [injected faults](2026-11-03-integer-obstructions-mutations-final.json).
The next file is `fq-gap-tensor-uniqueness.py`.

The review starts at `checks/independent` in the requested source checkout and
continues in path order, considering a source and its existing companion
together. Tracked source, data, documentation and existing companion files are
in scope; generated caches and Git internals are inventoried separately, not
silently treated as reviewed. Existing user changes are preserved. Each file
score is the user's 1–5 retention/action label, distinct from the independent
SCORING.md capability/engineering assessment. Missing evidence remains
unassessed and does not satisfy the requested L4B floor.

| Batch | Files reviewed | Record | Next file |
|---|---:|---|---|
| 1 | 4 Python sources and 4 newly created companions | [AdS/CFT independent checkers](2026-11-02-checks-ads.md), [companion assessment](2026-11-02-checks-auth.md#newly-created-adscft-companion-files) | Authorization fixtures |
| 2 | 3 Python sources and 2 existing companions | [Authorization fixtures](2026-11-02-checks-auth.md) | `checks/independent/check_tfq_1050_fqcd_wilson_dirac_gamma5_hermiticity.contract.score.yaml` and its Python source |
| 3 | 1 Python source, 1 existing companion and 1 newly created companion | [FQCD Wilson–Dirac](2026-11-02-checks-fqcd-1050.md) | `checks/independent/check_tfq_1052_fqcd_strong_coupling_area_law.contract.score.yaml` and its Python source |
| 4 | 1 Python source and 1 existing companion | [FQCD strong coupling](2026-11-02-checks-fqcd-1052.md) | `checks/independent/check_tfq_1219_fsp_hinge_lineon_sign_claim.contract.score.yaml` and its Python source |
| 5 | 1 Python source and 1 existing companion | [Hinge-lineon checker](2026-11-02-checks-fsp-1219.md) | `checks/independent/comp-c2-step3-not-word-step.contract.score.yaml` and its Python source |
| 6 | 6 Python sources and 6 existing companions | [Computation fixtures](2026-11-02-checks-comp.md) | `checks/independent/cqft-causal-factorization-import.py` |
| 7 | 3 Python sources and 3 newly created companions | [Causal-QFT checkers](2026-11-02-checks-cqft.md) | `checks/independent/ct-information-media-interoperability.contract.score.yaml` and its Python source |
| 8 | 2 Python sources, 1 existing companion and 1 newly created companion | [Constructor-theory checkers](2026-11-02-checks-ct.md) | `checks/independent/dfm-bphz-continuum-fence.contract.score.yaml` and its Python source |
| 9 | 1 Python source and 1 existing companion | [BPHZ fence checker](2026-11-02-checks-dfm-bphz.md) | `checks/independent/dfm-ckm-physics-fence.contract.score.yaml` and its Python source |
| 10 | 1 Python source and 1 existing companion | [CKM fence checker](2026-11-02-checks-dfm-ckm.md) | `checks/independent/dfm-continuum-interface.contract.score.yaml` and its Python source |
| 11 | 1 Python source and 1 existing companion | [Continuum-interface checker](2026-11-02-checks-dfm-continuum.md) | `checks/independent/dfm-continuum-refinement-limit.contract.score.yaml` and its Python source |
| 12 | 1 Python source and 1 existing companion | [Refinement-limit checker](2026-11-02-checks-dfm-refinement.md) | `checks/independent/dfm-electroweak-continuum-fence.contract.score.yaml` and its Python source |

At the starting snapshot, `checks/` had 258 tracked files: 171 Python sources,
85 contract companions, one requirements file and one JSON data file; 86 of
the Python sources lacked a matching contract. Four
ignored `.pyc` cache files also existed in the requested checkout. These counts
do not mean the remaining files have been reviewed. Companion records created
for the first batch are assessed as review metadata when verified, and their
source scores remain incomplete unless their evidence supports a complete one.

## Repair follow-up

The errors identified in batches 1-12 were repaired and retested in
[the repair report](2026-11-02-checks-repairs.md). The new
[source-bound receipt](2026-11-02-checks-repair-retest.json) records 24 passing
regression groups in both normal and optimized Python, including all 25
checker CLIs per mode. Contracts were appended without rewriting historical
records. The requested L4B floor remains unestablished; see the report's
explicit scoring limits. The review cursor above has not advanced.
