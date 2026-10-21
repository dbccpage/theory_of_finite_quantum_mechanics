"""Comprehensive unit tests for omega_engine core contract subsystems."""

import pytest
from omega_engine.crates.kernel.higher_operad.result import Err
from omega_engine.crates.carrier import Carrier
from omega_engine.crates.boundary import Boundary, CrossingType, verify_boundary_contract
from omega_engine.crates.replay import ReplayKernel, ReplayStatus, verify_replay_contract
from omega_engine.crates.observer import Observer
from omega_engine.crates.observable import Observable
from omega_engine.crates.evaluator import Evaluator, EvaluationInput, EvaluationPolicy
from omega_engine.crates.engine import Engine, LicensedEngine
from omega_engine.crates.type.engine_io import EngineInput, LicensedTransitionInput, RefusedEngineOutput
from omega_engine.crates.pipeline import Pipeline, PipelineStep
from omega_engine.crates.functional import evaluate_phi1, evaluate_gamma2, evaluate_xi, curvature_defect
from omega_engine.crates.solver import (
    BaseSolver,
    SolverKernel,
    SolverResult,
    verify_solver_contract,
)
from omega_engine.crates.lift import LiftBoundary, LiftRequest, verify_lift_contract
from omega_engine.crates.measurement import MeasurementKernel, MeasurementValue, MeasurementValueKind, verify_measurement_contract
from omega_engine.crates.type import TypeRegistry, KindDefinition, verify_type_contract


def test_observer_subsystem():
    proj = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    obs = Observer(observer_id="obs_001", num_channels=3, projection_matrix=proj)

    omega = obs.observe([0.5, 1.0, -0.5])
    assert omega == [0.5, 1.0, -0.5]

    artifact = obs.to_artifact()
    assert artifact.authority_effect == "None"

    checked = obs.check_contract()
    assert checked.authority_effect == "EvidenceOnly"


def test_observable_subsystem():
    observable = Observable(observable_id="observable_001")
    output = observable.extract(source_ref="state:001", raw_data=[1.0, 2.0, 3.0])

    assert output.authority_effect == "EvidenceOnly"
    assert output.raw_values == [1.0, 2.0, 3.0]

    checked = observable.check_output(output)
    assert checked.authority_effect == "FactOnly"


def test_evaluator_subsystem():
    evaluator = Evaluator(evaluator_id="eval_001")
    policy = EvaluationPolicy(policy_id="strict_policy", max_phi1_tol=1e-3, max_gamma2_tol=1e-3)

    good_input = EvaluationInput(candidate_id="cand_good", fact_envelopes={"phi1_mass": 0.0, "gamma2_mass": 0.0})
    good_res = evaluator.evaluate(good_input, policy)
    assert good_res.is_admissible is True
    assert good_res.verdict == "ACCEPT"

    bad_input = EvaluationInput(candidate_id="cand_bad", fact_envelopes={"phi1_mass": 0.5, "gamma2_mass": 0.0})
    bad_res = evaluator.evaluate(bad_input, policy)
    assert bad_res.is_admissible is False
    assert bad_res.verdict == "REJECT"


def test_engine_subsystem():
    with pytest.raises(TypeError):
        Engine(engine_id="eng_001")


def test_pipeline_subsystem():
    carrier = Carrier(
        c0_dim=2,
        c1_dim=3,
        c2_dim=1,
        d0=[[-1.0, 0.0], [1.0, -1.0], [0.0, 1.0]],
        d1=[[1.0, 1.0, 1.0]],
    )

    steps = [
        PipelineStep(step_id="s1", step_kind="extract"),
        PipelineStep(step_id="s2", step_kind="engine_step"),
        PipelineStep(step_id="s3", step_kind="evaluate"),
    ]

    pipeline = Pipeline(pipeline_id="pipe_001", steps=steps)
    res = pipeline.run(run_id="run_001", carrier=carrier, cochain_vec=[0.0, 0.0, 0.0])

    assert res.is_success is True
    assert res.status == "ACCEPT"
    assert len(res.steps_executed) == 3


def test_gamma2_functional_update():
    res = evaluate_gamma2([0.0, 0.0, 0.0])
    assert res.is_closed is True
    assert res.gamma2_mass == 0.0

    defect = curvature_defect([1.0, 2.0], [1.0, 1.0])
    assert defect == 1.0


def test_solver_subsystem():
    class StructuralSolver:
        def solve(self, problem: dict[str, float]) -> SolverResult[dict[str, float]]:
            value = float(problem["value"])
            return SolverResult(
                payload={"value": value},
                residual=0.0,
                diagnostics={"verification_status": "Unverified"},
            )

    solver = StructuralSolver()
    result = solver.solve({"value": 7.0})

    assert verify_solver_contract(solver) is True
    assert isinstance(solver, SolverKernel)
    assert isinstance(result, SolverResult)
    assert result.payload == {"value": 7.0}
    assert result.evidence_class == "EvidenceOnly"
    assert result.authority_effect == "None"
    assert result.diagnostics == {"verification_status": "Unverified"}

    class BaseOnlySolver(BaseSolver):
        pass

    assert verify_solver_contract(StructuralSolver) is False
    assert verify_solver_contract(BaseSolver) is False
    assert verify_solver_contract(BaseOnlySolver) is False
    with pytest.raises(TypeError):
        BaseOnlySolver()



def test_lift_subsystem():
    boundary = LiftBoundary(boundary_id="lift_001")
    assert verify_lift_contract(boundary) is True

    req = LiftRequest(request_id="req_001", source_level="L1", target_level="L2", carrier_ref="c1", proposed_delta={})
    lic = boundary.issue_license(
        request=req,
        checked_obstruction_ref="obs_01",
        context_witness_ref="wit_01",
        repair_exhaustion_ref="rep_01",
        replay_manifest_ref="man_01",
    )
    assert lic.authority_effect == "AuthorizesTransition"
    assert len(lic.license_hash) == 64

    checked = boundary.check_license(lic)
    assert checked.authority_effect == "FactOnly"


def test_measurement_subsystem():
    kernel = MeasurementKernel(kernel_id="meas_001")
    assert verify_measurement_contract(kernel) is True

    val = MeasurementValue(kind=MeasurementValueKind.EXACT_RATIONAL, val_repr="1/2")
    env = kernel.create_envelope(measurement_id="m001", source_ref="src1", method_ref="meth1", value=val)
    assert env.authority_effect == "EvidenceOnly"

    result = kernel.verify_measurement(env)
    assert type(result) is Err
    assert result.error.code == "MEASUREMENT_CHECKER_UNAVAILABLE"
    assert dict(result.error.details) == {"authority_effect": "None", "checks_performed": "none"}



def test_type_subsystem():
    registry = TypeRegistry(registry_id="reg_001")
    kind = KindDefinition(kind_name="CarrierState", category="state", field_schema={"dim": "int"})
    registry.register_kind(kind)

    b_type = registry.create_type(type_id="t001", kind_name="CarrierState", payload={"dim": 3})
    assert verify_type_contract(b_type) is True
    assert b_type.authority_effect == "None"



def test_boundary_subsystem():
    b = Boundary(
        boundary_id="b001",
        local_space="space_local",
        global_space="space_global",
        crossing_type=CrossingType.GLOBAL_TO_LOCAL_PROJECTION,
    )
    assert verify_boundary_contract(b)["admissible"] is True

    spec = b.to_spec()
    assert spec.authority_effect == "EvidenceOnly"
    assert spec.boundary_id == "b001"

    checked = b.check_boundary()
    assert checked.authority_effect == "FactOnly"
    assert checked.is_checked is True


def test_replay_subsystem():
    r_kernel = ReplayKernel(kernel_id="rep_001", verifier_ref="verifier:local")
    assert verify_replay_contract(r_kernel)["admissible"] is True

    rep = r_kernel.execute_replay(
        replay_id="r001",
        trace_refs=["trace_01"],
        manifest_ref="man_01",
        execution_output={"val": 42},
    )
    assert rep.status == ReplayStatus.UNVERIFIED
    assert rep.authority_effect == "EvidenceOnly"

    verified = r_kernel.verify_report(rep)
    assert verified.authority_effect == "FactOnly"
    assert verified.verifier_ref == "verifier:local"





