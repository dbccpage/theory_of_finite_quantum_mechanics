# Relocated CODA application

The maintained source package is `coda_application` inside WDP. From the WDP
`code` directory, run `python -m coda_application.presentation.cli --help`,
or install both local packages from the WDP root with
`python -m pip install . ./code/coda_application`. The CODA wheel depends on
WDP 2.2.2; WDP includes its Python native transport and observer support.
Build the Rust executables from the full repository as described in the
[WDP guide](../../README.md), and set `WDP_FUNCTIONALS_BIN` to the absolute
path of `evaluate_wdp_functionals`. The Python wheels do not contain that
binary or the sibling Omega Engine crates needed to build it.

# CODA finite application

This Python package evaluates declared finite instances with exact rational
arithmetic and routes the resulting evidence through a local authority
firewall. The [consolidated CODA paper](../../docs/source_archive/coda_component_packages/coda/coda.md) is the
retained research source. Its shared mathematics is integrated in
[WDP Appendix P](../../witnessed_difference_programme.md)
and the [CODA decomposition](../../docs/coda_mathematical_decomposition.md).
This application exercises selected finite cases and
does not prove every result in that paper or in its companion monographs.

CODA means **Calculus of Obstruction, Descent, and Authority**. The research
programme names eight components under GTLA's overarching authority
architecture. The application has nine runtime stages because it represents
GTLA terminal routing as its final stage.

| Runtime stage | Paper | Implemented finite behavior | Boundary |
| --- | --- | --- | --- |
| 1 FOC | [Finite Obstruction Calculus](../../docs/source_archive/coda_component_packages/foc/coda_foc.md) | Exact rational, unweighted coordinate L1 distance to the full image of a supplied repair map, with checked primal and dual certificates; next-defect norm for a supplied map. | The paper's weighted real-space and second repair-quotient theorems are broader. |
| 2 MUR | [Meta & Universal Re-Presentation](../../docs/source_archive/coda_component_packages/mur/coda_mur.md) | Checks declared finite section overlaps and coordinate loss. | No general commutation-square, comparison-span, or holonomy certificate. |
| 3 CS | [Continuum Shadow](../../docs/source_archive/coda_component_packages/cs/coda_cs.md) | Checks supplied coarse and fine profile consistency. | No continuum descent theorem follows from the check. |
| 4 CS_Q | [Continuum Shadow to Continuum Bridge](../../docs/source_archive/coda_component_packages/cs_q/coda_cs_q_bridge.md) | Finds equal supplied section vectors and a minimum nonzero coordinate distance. | No general image-factor construction or decoder collision bound is implemented. |
| 5 Q | [The Continuum](../../docs/source_archive/coda_component_packages/q/coda_q.md) | Checks rational interval order and diameter. | No metric completion is constructed; the check does not establish that an unknown point is enclosed. |
| 6 A | [Anomalon](../../docs/source_archive/coda_component_packages/a/coda_a.md) | Records a positive finite quotient residual in a JSONL register. | The file is persistent but can be deleted by its owner; no universal residual ontology is established. |
| 7 OR | [Omniversal Re-Presentation](../../docs/source_archive/coda_component_packages/or/coda_or.md) | Refuses declared incompatible overlaps and empty candidate sieves. | No general gluing or transport theorem is implemented. |
| 8 FDA | [Finite Descent Authority](../../docs/source_archive/coda_component_packages/fda/coda_fda.md) | Applies seven application firewall checks to sealed finite evidence and a caller supplied signed grant. | These checks differ from FDA's seven evidence-derived guards g1–g7 and do not construct standing for a five-field FDA packet. |
| 9 GTLA | [General Theory of Layered Authority](../../docs/source_archive/coda_component_packages/coda_gtla/coda_gtla_monograph.md.txt) | Emits one of the local authorized, residual, or refusal record variants. | This is an application routing contract, not a proof of general Kleisli factorization or Master Normal Form. |

The application begins with supplied cochain data. It does not construct the
witnessed irreflexive difference that starts the consolidated paper.
The papers' open targets remain open when a finite application check passes.

## Authority scope

An AUTHORIZED application outcome requires zero checked quotient defect and
a one-use HMAC grant accepted by the caller configured keyring, bound to the
problem and computed evidence. A Boolean license field cannot supply this
grant. The keyring does not establish that its operator has institutional or
normative standing. AUTHORIZED therefore names this local contract outcome;
it is not FDA standing, a Zenodo publication decision, or external permission.

The seven firewall checks in domain/firewall_engine.py concern role
separation, exact arithmetic, dual witness validation, cocycle consistency,
the grant gap, the nonterminal budget, and verification limits. They must not
be relabelled as FDA's accepted, deterministic, zero residual mass, skeleton
preserving, exhaustive, no pending lift, and no refusal guards.

The Rust bridge executes the native proposal solver and verifies its certificate
through `omega_functional`. Phi_1 and Gamma_2 are evaluated only by that owner.
A missing executable produces a refusal; there is no Python functional fallback.

## Run and verify

From the WDP root after installing the packages and configuring the executable:

    python -m coda_application.presentation.cli --help
    python -m pytest -o addopts= code/coda_application/tests/test_pipeline_flow.py -q

Run additional test files individually. The
[test catalog](docs/test_catalog_and_failure_modes.md) describes finite
examples and failure modes; passing tests do not promote the paper's open
claims.
