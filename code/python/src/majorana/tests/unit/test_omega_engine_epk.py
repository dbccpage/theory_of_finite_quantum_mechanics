import pytest
import numpy as np
from omega_engine.crates.engine.eng_obstruction_runtime import ObstructionRuntime
from omega_engine.crates.type.engine_invariants import (
    EscalationRoute,
    EvaluationVerdict,
    EngineDecision,
    EngineTraceStep,
)
from omega_engine.crates.invariant.inv_engine import (
    assert_meta_escalation_resolution,
    TerminationViolation,
)
from omega_engine.crates.engine.eng_prompt_intake import PromptIntakeEngine
from omega_engine.crates.engine.eng_operator_algebra import (
    MatrixCStarAlgebra,
    AlgebraicState,
    GnsConstruction,
    FiniteVonNeumannAlgebra,
)
from omega_engine.crates.operator.generator.gen_everett import ManyWorldsDAG
from omega_engine.crates.type.obstruction_runtime import (
    ObstructionMetrics,
    ObstructionThresholds,
    Candidate,
)
from omega_engine.crates.evaluator.eval_obstruction import DefaultObstructionEvaluator
from omega_engine.crates.type.cycle_aware import (
    CycleAwareConfig,
    XiDiagnostic,
)
from omega_engine.crates.operator.generator.gen_cycle_aware import CycleAwareGenerator
from omega_engine.crates.functional.fn_xi_witness import try_compute_xi_witness


def test_engine_invariants_meta_escalation():
    # Test valid meta escalation resolution
    step0 = EngineTraceStep(
        evaluator_verdict=EvaluationVerdict.Escalate(EscalationRoute.MetaAnalysis),
        decision=EngineDecision.Continue,
        phi=0.5,
        gamma2=0.1,
    )
    step1 = EngineTraceStep(
        evaluator_verdict=None, decision=EngineDecision.Lift, phi=0.4, gamma2=0.1
    )
    assert_meta_escalation_resolution([step0, step1])  # passes

    # Test invalid meta escalation resolution (escalated but followed by continue)
    step2 = EngineTraceStep(
        evaluator_verdict=None, decision=EngineDecision.Continue, phi=0.4, gamma2=0.1
    )
    with pytest.raises(TerminationViolation):
        assert_meta_escalation_resolution([step0, step2])


def test_prompt_intake_engine():
    # JSONL
    line = '{"id":"test_01","prompt":"hello world","solution":"ok"}'
    record = PromptIntakeEngine.parse_jsonl_record(line)
    assert record.id == "test_01"
    assert record.raw_prompt == "hello world"
    assert record.expected_answer == "ok"

    # CSV
    csv_line = 'row_1,"What, exactly, is this?","answer, here"'
    record_csv = PromptIntakeEngine.parse_csv_record(csv_line)
    assert record_csv.id == "row_1"
    assert record_csv.raw_prompt == "What, exactly, is this?"
    assert record_csv.expected_answer == "answer, here"


def test_operator_algebra_engine():
    # Pauli Z
    pauli_z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    pauli_x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)

    algebra = MatrixCStarAlgebra.new(2)
    defect = algebra.cstar_identity_defect(pauli_x)
    assert defect < 1e-10

    # Create state
    psi = np.array([1.0, 0.0], dtype=complex)
    state = AlgebraicState.vector_state(psi)
    exp_z = state.expectation(pauli_z)
    assert abs(exp_z - 1.0) < 1e-10

    # GNS
    gns = GnsConstruction.from_state(state)
    assert gns.quotient_dimension() == 2

    # Finite Von Neumann Algebra
    vna = FiniteVonNeumannAlgebra.generated_by(2, [pauli_x, pauli_z])
    diag = vna.double_commutant_diagnostic()
    assert diag.generated_dimension == 4
    assert diag.commutant_dimension == 1
    assert diag.is_double_commutant_closed is True
    assert vna.is_factor() is True


def test_everett_dag():
    dag = ManyWorldsDAG.new_root("root", 1.0, [1, -1])
    assert dag.root_index == 0
    assert dag.arena.nodes[0].id.val == "root"
    assert dag.arena.nodes[0].amplitude == 1.0
    assert dag.arena.nodes[0].configuration_sign_field == [1, -1]


def test_obstruction_runtime():
    # Mock classes
    class MockFunctional:
        def compute(self, state):
            return state.metrics

    class MockState:
        def __init__(self, label, metrics):
            self.label = label
            self.metrics = metrics

    class MockGenerator:
        def generate(self, state):
            return [
                Candidate.new(
                    MockState("child1", ObstructionMetrics(0.5, 0.1, 0.9)),
                    "op1",
                    "prov1",
                ),
                Candidate.new(
                    MockState("child2", ObstructionMetrics(1.2, 0.1, 0.9)),
                    "op2",
                    "prov2",
                ),
            ]

    seed = MockState("root", ObstructionMetrics(1.0, 0.1, 0.9))
    evaluator = DefaultObstructionEvaluator.try_new(ObstructionThresholds())

    runtime = ObstructionRuntime(
        seed_state=seed,
        functional=MockFunctional(),
        evaluator=evaluator,
        generator=MockGenerator(),
    )

    step = runtime.step()
    assert len(step.evaluated) == 2
    # child1 has phi_1 = 0.5 (descent from 1.0), should be accepted
    # child2 has phi_1 = 1.2, should be rejected
    assert step.evaluated[0].verdict == "Accept"
    assert step.evaluated[1].verdict == "Reject"
    assert step.selected is not None
    assert step.selected.candidate.state.label == "child1"
    assert runtime.current_state.label == "child1"


def test_cycle_aware_generator():
    class GraphState:
        def __init__(self, edges, values, num_nodes=3):
            self._edges = edges
            self._values = values
            self._num_nodes = num_nodes

        def edge_values(self):
            return self._values

        def edges(self):
            return self._edges

        def node_count(self):
            return self._num_nodes

        def with_corrected_edges(self, corrected):
            return GraphState(self._edges, corrected, self._num_nodes)

        def validate_cycle_correctable(self):
            return len(self._values) == len(self._edges)

    class MockDiagnosticFunctional:
        def diagnose(self, state):
            witness = try_compute_xi_witness(
                state.edge_values(), [2.0, 2.0, 2.0], 0.3, 2
            )
            return XiDiagnostic([2.0, 2.0, 2.0], 0.3, witness)

    state = GraphState([(0, 1), (1, 2), (2, 0)], [3.0, 1.0, 2.0])
    config = CycleAwareConfig(xi_activation_threshold=0.5, top_k_edges=2)
    gen = CycleAwareGenerator(config, MockDiagnosticFunctional())

    candidates = gen.generate(state)
    # should generate 1 bulk + 2 single-edge = 3 candidates
    assert len(candidates) == 3
    assert candidates[0].operator_id.val == "cycle_aware.bulk_correction"
