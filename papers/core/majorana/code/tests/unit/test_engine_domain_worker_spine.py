"""Contract-true Engine v1 + DomainWorker spine (path-scoped)."""

from __future__ import annotations

import ast
import hashlib
import inspect
import json
from pathlib import Path

from omega_engine.crates.runtime.rt_domain_worker import CONTRACT_ID as DW_ID
from omega_engine.crates.engine.base.eng_base import (
    CONTRACT_ID as ENGINE_ID,
    Engine,
    EngineRefusal,
    LicensedTransitionInput,
    VerifiedActionLicense,
    verify_engine_contract,
)
from omega_engine.crates.evaluator.eval_engine_output import check_engine_output_hash
from omega_engine.crates.runtime.rt_linear_algebra_domain_worker import (
    LinearAlgebraDomainWorker,
)
from omega_engine.crates.type.engine_io import (
    CheckedEngineOutput,
    DomainWorkerInput,
    EngineOutput,
    RefusedEngineOutput,
)


class DummyStore:
    def __init__(self):
        self.db = {"state-001": {"version": "1", "state": {"val": 1}}}
        self.traces = []

    def load(self, ref):
        if ref not in self.db:
            raise KeyError(ref)
        d = self.db[ref]
        from omega_engine.crates.engine.base.eng_base import CarrierSnapshot

        return CarrierSnapshot(
            state_ref=ref, version=d["version"], carrier_state=d["state"]
        )

    def commit_transition(
        self, *, target_state_ref, expected_version, post_state, trace_event, action_id
    ):
        from omega_engine.crates.engine.base.eng_base import (
            CommittedCarrier,
            TransitionCommitReceipt,
        )

        self.db[target_state_ref] = {
            "version": str(int(expected_version) + 1),
            "state": post_state,
        }
        self.traces.append(trace_event)
        return TransitionCommitReceipt(
            committed_carrier=CommittedCarrier(
                state_ref=target_state_ref, version="2", carrier_state=post_state
            ),
            trace_ref=f"trace_{action_id[:8]}",
        )


class DummyHasher:
    def hash_state(self, state):
        return f"sha256:{hashlib.sha256(str(state).encode()).hexdigest()}"


class DummyVerifier:
    def __init__(self):
        self.licenses = {}

    def register(self, lic):
        self.licenses[lic.license_ref] = lic

    def verify(self, req):
        if req.license_ref not in self.licenses:
            from omega_engine.crates.engine.base.eng_base import LicenseRefusal

            return LicenseRefusal("InvalidActionLicense")
        return self.licenses[req.license_ref]


def test_engine_contract_id_is_base_v1() -> None:
    assert ENGINE_ID == "urn:omega:execution:engine:v1.0.0"
    store = DummyStore()
    hasher = DummyHasher()
    verifier = DummyVerifier()
    eng = Engine(
        engine_id="eng-001",
        engine_version="v1.0.0",
        license_verifier=verifier,
        state_hasher=hasher,
        trace_sink=store,
        carrier_store=store,
    )
    rep = verify_engine_contract(eng)
    assert rep["contract_id"] == ENGINE_ID


def test_engine_requires_action_license() -> None:
    store = DummyStore()
    hasher = DummyHasher()
    verifier = DummyVerifier()
    eng = Engine(
        engine_id="eng-001",
        engine_version="v1.0.0",
        license_verifier=verifier,
        state_hasher=hasher,
        trace_sink=store,
        carrier_store=store,
    )
    out = eng.execute(
        LicensedTransitionInput(
            license_ref="",
            decision_ref="d1",
            target_state_ref="s1",
            expected_state_version="1",
            expected_pre_state_hash="sha256:pre",
            operator_ref="op1",
            proposed_state_ref="s1_prop",
            expected_post_state_hash="sha256:post",
        )
    )
    assert isinstance(out, EngineRefusal)
    assert out.refusal_reason == "MissingActionLicense"


def test_engine_registered_transition_is_fenced_without_mutation() -> None:
    store = DummyStore()
    hasher = DummyHasher()
    verifier = DummyVerifier()
    store.db["state-001"] = {"version": "1", "state": {"a": 1}}
    store.db["artifact:s_proposed"] = {"version": "1", "state": {"a": 2}}

    pre_hash = hasher.hash_state({"a": 1})
    post_hash = hasher.hash_state({"a": 2})

    lic = VerifiedActionLicense(
        license_ref="lic-001",
        decision_ref="dec-001",
        target_state_ref="state-001",
        expected_state_version="1",
        expected_pre_state_hash=pre_hash,
        operator_ref="op_add",
        proposed_state_ref="artifact:s_proposed",
        expected_post_state_hash=post_hash,
    )
    verifier.register(lic)

    eng = Engine(
        engine_id="eng-001",
        engine_version="v1.0.0",
        license_verifier=verifier,
        state_hasher=hasher,
        trace_sink=store,
        carrier_store=store,
    )
    before = dict(store.db["state-001"])
    result = eng.execute(
        LicensedTransitionInput(
            license_ref="lic-001",
            decision_ref="dec-001",
            target_state_ref="state-001",
            expected_state_version="1",
            expected_pre_state_hash=pre_hash,
            operator_ref="op_add",
            proposed_state_ref="artifact:s_proposed",
            expected_post_state_hash=post_hash,
        )
    )
    assert isinstance(result, EngineRefusal)
    assert result.refusal_reason == "EngineAdmittedTransitionFenced"
    assert store.db["state-001"] == before
    assert store.traces == []


def test_engine_output_hash_check_is_owned_by_evaluator() -> None:
    body = {"vec": [1.0], "status": "candidate", "task_id": "task-1"}
    output_hash = hashlib.sha256(
        json.dumps(body, sort_keys=True).encode("utf-8")
    ).hexdigest()
    output = EngineOutput(
        task_id="task-1",
        status="candidate",
        residual_vector=[1.0],
        phi1_mass=1.0,
        output_hash=output_hash,
    )
    assert isinstance(check_engine_output_hash(output), CheckedEngineOutput)

    bad_output = EngineOutput(
        task_id=output.task_id,
        status=output.status,
        residual_vector=output.residual_vector,
        phi1_mass=output.phi1_mass,
        output_hash="wrong",
    )
    assert isinstance(check_engine_output_hash(bad_output), RefusedEngineOutput)


def test_engine_module_source_has_no_diy_phi1_sum_abs() -> None:
    """Gate sketch: eng_base.py must not reimplement residual mass as sum(abs)."""
    src_path = Path(inspect.getfile(Engine))
    tree = ast.parse(src_path.read_text(encoding="utf-8"))
    text = src_path.read_text(encoding="utf-8")
    assert "sum(abs" not in text
    # No Call to residual_l1/phi1 inside engine module (Engine must not compute Φ)
    assert "residual_l1" not in text
    assert "from omega_engine.crates.functional" not in text
    assert isinstance(tree, ast.Module)


def test_domain_worker_contract_id() -> None:
    assert DW_ID == "urn:omega:execution:domain_worker:v1.0.0"


def test_linear_algebra_matmul() -> None:
    worker = LinearAlgebraDomainWorker()
    a = {"rows": 2, "cols": 2, "data": [1.0, 2.0, 3.0, 4.0]}
    b = {"rows": 2, "cols": 2, "data": [5.0, 6.0, 7.0, 8.0]}
    expected = {"rows": 2, "cols": 2, "data": [19.0, 22.0, 43.0, 50.0]}
    out = worker.run(
        DomainWorkerInput(
            task_id="mm1",
            task_kind="matmul",
            payload={"a": a, "b": b, "expected": expected},
        )
    )
    assert out.authority_effect == "EvidenceOnly"
    assert out.status == "SOLVED"
    assert out.residual_l1 == 0.0
    assert out.result["product"]["data"] == [19.0, 22.0, 43.0, 50.0]
    assert any("basic_matrix" in p for p in out.math_path)
    assert any("residual_l1" in p for p in out.math_path)
    assert DW_ID in out.implements


def test_linear_algebra_gram_schmidt() -> None:
    worker = LinearAlgebraDomainWorker()
    columns = [[1.0, 1.0], [1.0, 0.0]]
    out = worker.run(
        DomainWorkerInput(
            task_id="gs1",
            task_kind="gram_schmidt",
            payload={"columns": columns},
        )
    )
    assert out.authority_effect == "EvidenceOnly"
    assert out.status == "SOLVED"
    assert out.residual_l1 < 1e-9
    assert len(out.result["q_columns"]) == 2
    assert any("gram_schmidt_proto" in p for p in out.math_path)
    assert any("residual_l1" in p for p in out.math_path)
    assert any("PROD_TODO:omega" in p for p in out.math_path)
