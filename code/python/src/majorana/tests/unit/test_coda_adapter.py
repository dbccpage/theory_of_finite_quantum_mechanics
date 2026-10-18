from __future__ import annotations

from dataclasses import replace
from itertools import islice

import pytest

pytest.importorskip("numpy")
pytest.importorskip("scipy")

from omega_engine.crates.carrier.cochain_carrier import (
    CochainCarrier,
    MAX_PROJECTION_EDGES,
)
from omega_engine.crates.carrier.rust_oesos import (
    RustOesosFreshSolveReplayRequestV1,
    rust_replay_request,
)
from omega_engine.crates.engine.eng_symbol_game import OesosLab
from omega_engine.crates.projection_obstruction.cochain_projector import (
    CochainProjector,
)
from omega_engine.crates.solver.solv_coda_cascade_proposal import (
    CodaCascadeProposalSolver,
)
from omega_engine_pfp.use_cases.problem_builders.coda_problem import (
    build_coda_problem,
)


def _oversized_edge_pairs() -> tuple[tuple[int, int], ...]:
    return tuple(
        islice(
            ((tail, head) for tail in range(92) for head in range(tail + 1, 92)),
            MAX_PROJECTION_EDGES + 1,
        )
    )


def test_existing_coda_solver_is_only_a_proposer_then_reprojected() -> None:
    problem = build_coda_problem()
    run = OesosLab((CodaCascadeProposalSolver(),)).solve(problem)

    assert run.locally_resolved
    assert len(run.attempts) == 1
    assert run.attempts[0].accepted
    assert run.final_projection is not None
    assert run.final_projection.phi1 == pytest.approx(0.0)
    assert run.final_projection.gamma2 == pytest.approx(0.0)


def test_rust_replay_request_transports_inputs_not_a_verified_receipt() -> None:
    request = rust_replay_request(
        build_coda_problem(),
        expected_carrier_hash_blake3="a" * 64,
        solver_registry_hash="b" * 64,
        source_revision="deadbeef",
    )

    assert request.replay_required
    assert request.authority_effect == "None"
    assert len(request.request_id) == 64
    assert request.solve_args()["omega"] == (3, 2, 2, 1, 1)
    assert "omega" not in request.solve_args()["carrier"]
    assert replace(request, omega=(3, 2, 2, 1, 0)).request_id != request.request_id


def test_cochain_carrier_refuses_more_edges_than_exact_l1_accepts() -> None:
    edges = _oversized_edge_pairs()

    with pytest.raises(ValueError, match="exact-L1 edge resource fence"):
        CochainCarrier(
            nodes=tuple(range(92)),
            edges=edges,
            faces=(),
            weights=(1,) * len(edges),
        )


def test_rust_request_refuses_more_edges_than_exact_l1_accepts() -> None:
    edge_pairs = _oversized_edge_pairs()
    edges = tuple((tail, head, 1) for tail, head in edge_pairs)

    with pytest.raises(ValueError, match="exact-L1 edge resource fence"):
        RustOesosFreshSolveReplayRequestV1(
            packet_id="a" * 64,
            num_vertices=92,
            edges=edges,
            faces=(),
            omega=(0,) * len(edges),
            expected_carrier_hash_blake3="b" * 64,
            solver_registry_hash="c" * 64,
            source_revision="deadbeef",
        )


def test_cochain_projector_preserves_legacy_third_positional_projector_id() -> None:
    problem = build_coda_problem()
    projector = CochainProjector(
        problem.projector.carrier,
        1.0e-7,
        "legacy-custom-projector-id",
    )

    assert projector.projector_id == "legacy-custom-projector-id"
    assert projector.research_parent_event_id is None


