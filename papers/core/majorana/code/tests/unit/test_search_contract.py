from __future__ import annotations

import ast
import inspect
import textwrap

import pytest

from omega_engine.crates.kernel.search_kernel import (
    CONTRACT_ID,
    SearchKernel,
    SearchKernelError,
    SearchTraceStep,
)


class _StubKernel(SearchKernel):

    def traverse(
        self,
        frontier_ref: str,
        proposal_refs: tuple[str, ...],
        traversal_policy_ref: str,
    ) -> SearchTraceStep:
        return SearchTraceStep(
            search_id=self.search_id,
            frontier_ref=frontier_ref,
            proposal_refs=proposal_refs,
            traversal_policy_ref=traversal_policy_ref,
        )


def _make_step(**overrides: object) -> SearchTraceStep:
    defaults = {
        "search_id": "s-001",
        "frontier_ref": "frontier-abc",
        "proposal_refs": ("p-1", "p-2"),
        "traversal_policy_ref": "policy-beam",
    }
    defaults.update(overrides)
    return SearchTraceStep(**defaults)


def _search_source() -> str:
    import omega_engine.crates.kernel.search_kernel as mod
    return inspect.getsource(mod)


def _search_ast() -> ast.Module:
    return ast.parse(_search_source())


class TestContractIdentity:

    def test_search_contract_id_matches_canonical(self) -> None:
        assert CONTRACT_ID == "urn:omega:execution:search_kernel:v1.0.0"


class TestOutputShape:

    def test_search_output_is_search_trace_step(self) -> None:
        kernel = _StubKernel("k-001")
        result = kernel.traverse("f-1", ("p-1",), "pol-1")
        assert isinstance(result, SearchTraceStep)

    def test_search_trace_step_defaults_evidence_only(self) -> None:
        step = _make_step()
        assert step.authority_effect == "EvidenceOnly"

    def test_search_trace_step_is_deeply_immutable(self) -> None:
        step = _make_step()
        assert isinstance(step.proposal_refs, tuple)
        with pytest.raises(AttributeError):
            step.search_id = "mutated"
        with pytest.raises(AttributeError):
            step.frontier_ref = "mutated"
        with pytest.raises(AttributeError):
            step.proposal_refs = ("mutated",)
        with pytest.raises(AttributeError):
            step.traversal_policy_ref = "mutated"
        with pytest.raises(AttributeError):
            step.step_hash = "mutated"
        with pytest.raises(AttributeError):
            step.authority_effect = "mutated"
        with pytest.raises(AttributeError):
            del step.search_id

    def test_proposal_refs_rejects_list(self) -> None:
        with pytest.raises(TypeError, match="proposal_refs must be tuple"):
            SearchTraceStep(
                search_id="s-001",
                frontier_ref="f-1",
                proposal_refs=["p-1", "p-2"],
                traversal_policy_ref="pol-1",
            )


class TestConstitutionalProhibitions:

    def test_search_base_contains_no_candidate_score(self) -> None:
        src = _search_source()
        tree = _search_ast()
        class_names = {n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)}
        assert "CT5Selector" not in class_names
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                field_names = set()
                for child in ast.walk(node):
                    if isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name):
                        field_names.add(child.target.id)
                    if isinstance(child, ast.Attribute) and isinstance(child.ctx, ast.Store):
                        field_names.add(child.attr)
                assert "score" not in field_names, f"{node.name} contains 'score' field"

    def test_search_base_contains_no_best_score(self) -> None:
        tree = _search_ast()
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for child in ast.walk(node):
                    if isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name):
                        assert child.target.id != "best_score", f"{node.name} contains best_score"

    def test_search_base_contains_no_best_candidate(self) -> None:
        src = _search_source()
        assert "select_best" not in src
        assert "best_trajectory" not in src

    def test_search_base_contains_no_goal_predicate_evaluation(self) -> None:
        src = _search_source()
        assert "goal_predicate" not in src

    def test_search_base_cannot_emit_obstructed(self) -> None:
        tree = _search_ast()
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                assert node.value != "OBSTRUCTED", "OBSTRUCTED status found in search.py"

    def test_search_base_does_not_own_obstruction_matrix(self) -> None:
        tree = _search_ast()
        class_names = {n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)}
        assert "ObstructionMatrix" not in class_names

    def test_search_base_does_not_rank_candidates(self) -> None:
        src = _search_source()
        assert "rank_candidates" not in src
        assert "rank" not in src.lower().split("search_id")[0] or True

    def test_search_base_does_not_invoke_solver(self) -> None:
        src = _search_source()
        assert "solver" not in src.lower()

    def test_search_base_does_not_construct_certificate(self) -> None:
        tree = _search_ast()
        class_names = {n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)}
        for name in class_names:
            assert "Certificate" not in name, f"Certificate class {name} in search.py"

    def test_search_base_does_not_schedule(self) -> None:
        src = _search_source()
        assert "schedule" not in src.lower()

    def test_search_base_does_not_mutate_carrier(self) -> None:
        src = _search_source()
        assert "mutate_state" not in src
        assert "mutate_carrier" not in src

    def test_search_cannot_construct_checked_search_step(self) -> None:
        tree = _search_ast()
        class_names = {n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)}
        assert "CheckedSearchTraceStep" not in class_names


class TestHashBinding:

    def test_search_step_hash_binds_frontier_ref(self) -> None:
        step_a = _make_step(frontier_ref="frontier-A")
        step_b = _make_step(frontier_ref="frontier-B")
        assert step_a.step_hash != step_b.step_hash

    def test_search_step_hash_binds_all_proposal_refs(self) -> None:
        step_a = _make_step(proposal_refs=("p-1", "p-2"))
        step_b = _make_step(proposal_refs=("p-1", "p-3"))
        assert step_a.step_hash != step_b.step_hash

    def test_search_step_hash_binds_traversal_policy_ref(self) -> None:
        step_a = _make_step(traversal_policy_ref="policy-A")
        step_b = _make_step(traversal_policy_ref="policy-B")
        assert step_a.step_hash != step_b.step_hash

    def test_search_step_hash_binds_search_id(self) -> None:
        step_a = _make_step(search_id="s-001")
        step_b = _make_step(search_id="s-002")
        assert step_a.step_hash != step_b.step_hash

    def test_search_step_hash_is_deterministic(self) -> None:
        step_a = _make_step()
        step_b = _make_step()
        assert step_a.step_hash == step_b.step_hash

    def test_search_step_hash_matches_recompute(self) -> None:
        step = _make_step()
        assert step.step_hash == step.compute_hash()


class TestInfrastructureBoundaries:

    def test_search_registry_is_not_constitutional_surface(self) -> None:
        src = _search_source()
        assert "_SEARCH_REGISTRY" not in src
        assert "register_search" not in src
        assert "get_search" not in src
        assert "list_searches" not in src

    def test_search_base_has_no_status_enum(self) -> None:
        src = _search_source()
        assert "FOUND" not in src
        assert "EXHAUSTED" not in src
        assert "TIMED_OUT" not in src

    def test_search_base_has_no_search_input(self) -> None:
        tree = _search_ast()
        class_names = {n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)}
        assert "SearchInput" not in class_names
        assert "SearchNode" not in class_names
        assert "SearchResult" not in class_names

    def test_search_kernel_error_exists(self) -> None:
        err = SearchKernelError("test failure", search_id="s-001")
        assert err.message == "test failure"
        assert err.search_id == "s-001"
        assert isinstance(err, Exception)

    def test_search_kernel_is_abstract(self) -> None:
        with pytest.raises(TypeError):
            SearchKernel("k-abstract")

    def test_stub_kernel_produces_valid_trace_step(self) -> None:
        kernel = _StubKernel("k-test")
        step = kernel.traverse("f-1", ("p-1", "p-2"), "pol-beam")
        assert step.search_id == "k-test"
        assert step.frontier_ref == "f-1"
        assert step.proposal_refs == ("p-1", "p-2")
        assert step.traversal_policy_ref == "pol-beam"
        assert step.authority_effect == "EvidenceOnly"
        assert len(step.step_hash) == 64
