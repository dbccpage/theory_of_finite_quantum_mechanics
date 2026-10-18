"""Build a DDA trajectory DAG without conflating refusal with repair."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from omega_engine_governance.contracts.dda_packets import (
    DDATapeDFA,
    DDATapeValidationError,
)
from omega_engine.crates.discrete_deformation_algebra.dda_trace_logger import _find_repo_root
from omega_engine.crates.discrete_deformation_algebra.trajectory_recorder import (
    verify_trajectory_chain,
)


def _get_default_trace_dir() -> Path:
    trace_dir = (
        _find_repo_root(Path(__file__).resolve().parent) / "_intelligence" / "dda_traces"
    )
    trace_dir.mkdir(parents=True, exist_ok=True)
    return trace_dir


def _grammar_result(records: List[Dict[str, Any]]) -> tuple[bool, str, str]:
    dialect = str(records[0].get("dda_dialect", DDATapeDFA.LEGACY_V1))
    tape = ".".join(str(record.get("letter", "")) for record in records)
    try:
        DDATapeDFA.validate(tape, dialect=dialect)
    except DDATapeValidationError as exc:
        return False, str(exc), tape
    return True, f"valid {dialect} tape", tape


def build_dda_dag(
    trace_dir: Optional[Path] = None,
    trace_paths: Optional[Iterable[str | Path]] = None,
) -> Dict[str, Any]:
    target_dir = Path(trace_dir) if trace_dir else _get_default_trace_dir()
    target_dir.mkdir(parents=True, exist_ok=True)

    runs: Dict[str, List[Dict[str, Any]]] = {}
    load_errors: List[Dict[str, str]] = []
    jsonl_files = (
        sorted(target_dir.glob("*.jsonl"))
        if trace_paths is None
        else sorted(Path(path) for path in trace_paths)
    )
    for jsonl_file in jsonl_files:
        try:
            lines = [
                line
                for line in jsonl_file.read_text("utf-8").splitlines()
                if line.strip()
            ]
            records = [json.loads(line) for line in lines]
        except (OSError, json.JSONDecodeError) as exc:
            load_errors.append({"file": jsonl_file.name, "error": str(exc)})
            continue
        if records:
            run_id = str(records[0].get("run_id") or jsonl_file.stem)
            runs[f"{run_id}:{jsonl_file.name}"] = records

    dag_nodes: List[Dict[str, Any]] = []
    dag_edges: List[Dict[str, Any]] = []
    run_validations: List[Dict[str, Any]] = []
    structure_built_count = 0
    obstructions_removed_count = 0
    residual_carried_count = 0
    refusal_count = 0
    terminal_count = 0
    within_run_residual_reductions: Dict[str, float] = {}

    for run_key, records in runs.items():
        chain_ok, chain_detail = verify_trajectory_chain(records)
        grammar_ok, grammar_detail, tape = _grammar_result(records)
        run_id = str(records[0].get("run_id", run_key))
        runner_id = str(records[0].get("runner_id", "unknown"))
        dialect = str(records[0].get("dda_dialect", DDATapeDFA.LEGACY_V1))
        run_residual_reduction = 0.0
        run_is_valid = chain_ok and grammar_ok
        run_validations.append(
            {
                "runner_id": runner_id,
                "run_id": run_id,
                "dialect": dialect,
                "tape": tape,
                "chain_valid": chain_ok,
                "chain_detail": chain_detail,
                "grammar_valid": grammar_ok,
                "grammar_detail": grammar_detail,
            }
        )

        for index, step in enumerate(records):
            letter = str(step.get("letter", ""))
            effect = str(step.get("effect") or "")
            step_id = str(step.get("step_id", f"STEP_{index}"))
            node_id = f"{runner_id}_{run_id}_{step_id}"
            residual_delta = step.get("residual_delta")

            legacy_structure = dialect == DDATapeDFA.LEGACY_V1 and letter in {
                "C",
                "I",
                "Λ",
                "L",
                "D",
            }
            is_refusal = effect == "refusal" or letter in {"M", "Z"}
            if run_is_valid:
                if effect == "structure_added" or legacy_structure:
                    structure_built_count += 1
                if not is_refusal and (
                    effect == "obstruction_eliminated" or (not effect and letter == "E")
                ):
                    if (
                        step.get("obstruction_id")
                        and residual_delta is not None
                        and float(residual_delta) < 0.0
                    ):
                        obstructions_removed_count += 1
                if effect == "residual_carried" or letter == "R":
                    residual_carried_count += 1
                if is_refusal:
                    refusal_count += 1
                if letter == "T":
                    terminal_count += 1
                if residual_delta is not None and float(residual_delta) < 0.0:
                    run_residual_reduction += -float(residual_delta)

            dag_nodes.append(
                {
                    "node_id": node_id,
                    "runner_id": runner_id,
                    "run_id": run_id,
                    "dialect": dialect,
                    "letter": letter,
                    "effect": effect,
                    "action_name": step.get("action_name", ""),
                    "input_state": step.get("input_state", ""),
                    "output_state": step.get("output_state", ""),
                    "witness": step.get("witness", ""),
                    "obstruction_id": step.get("obstruction_id"),
                    "residual_before": step.get("residual_before"),
                    "residual_after": step.get("residual_after"),
                    "residual_delta": residual_delta,
                    "structure_delta": step.get("structure_delta", {}),
                    "refusal_reason": step.get("refusal_reason"),
                    "evidence": step.get("evidence", {}),
                    "chain_valid": chain_ok,
                    "grammar_valid": grammar_ok,
                }
            )

            if index > 0:
                previous = records[index - 1]
                previous_id = f"{runner_id}_{run_id}_{previous.get('step_id', f'STEP_{index - 1}')}"
                dag_edges.append(
                    {
                        "from_node": previous_id,
                        "to_node": node_id,
                        "transition_letter": letter,
                        "effect": effect,
                        "action_name": step.get("action_name", ""),
                    }
                )

        if run_is_valid:
            within_run_residual_reductions[f"{runner_id}:{run_id}"] = (
                run_residual_reduction
            )

    valid_runs = sum(
        1
        for validation in run_validations
        if validation["chain_valid"] and validation["grammar_valid"]
    )
    summary_data: Dict[str, Any] = {
        "schema_version": "omega.dda.dag.v2",
        "total_runs": len(runs),
        "valid_runs": valid_runs,
        "invalid_runs": len(runs) - valid_runs,
        "load_errors": load_errors,
        "total_steps": len(dag_nodes),
        "structure_built_steps": structure_built_count,
        "obstructions_removed_steps": obstructions_removed_count,
        "residual_carried_steps": residual_carried_count,
        "refusal_steps": refusal_count,
        "terminal_steps": terminal_count,
        "measured_residual_reduction": (
            next(iter(within_run_residual_reductions.values()))
            if len(within_run_residual_reductions) == 1
            else None
        ),
        "residual_reduction_comparison": (
            "WITHIN_SINGLE_RUN"
            if len(within_run_residual_reductions) == 1
            else "NOT_COMPARABLE_ACROSS_CARRIERS"
        ),
        "within_run_residual_reductions": within_run_residual_reductions,
        "run_validations": run_validations,
        "nodes": dag_nodes,
        "edges": dag_edges,
    }

    (target_dir / "dda_dag.json").write_text(
        json.dumps(summary_data, indent=2, sort_keys=True, default=str),
        encoding="utf-8",
    )

    markdown: List[str] = [
        "# DDA Trajectory DAG Summary",
        "",
        f"- Executed runs: {len(runs)}",
        f"- Hash-chain + grammar valid runs: {valid_runs}",
        f"- DDA steps: {len(dag_nodes)}",
        f"- Explicit structure additions: {structure_built_count}",
        f"- Explicit obstruction eliminations: {obstructions_removed_count}",
        f"- Residual-carry steps: {residual_carried_count}",
        f"- Refusals / unresolved targets (M or Z): {refusal_count}",
        "- Cross-run residual reduction: not comparable across distinct carriers",
        "",
        "A refusal is retained as an obstruction and is never included in the removal count.",
        "",
        "## Run tapes",
        "",
        "| Runner | Dialect | Tape | Chain | Grammar |",
        "|---|---|---|---:|---:|",
    ]
    for validation in run_validations:
        markdown.append(
            "| {runner_id} | {dialect} | `{tape}` | {chain_valid} | {grammar_valid} |".format(
                **validation
            )
        )

    markdown.extend(["", "## Within-run residual reductions", ""])
    for run_name, reduction in within_run_residual_reductions.items():
        markdown.append(f"- `{run_name}`: {reduction:.12g}")

    markdown.extend(["", "## Sequence DAG", "", "```mermaid", "graph TD"])
    for edge in dag_edges:
        source = edge["from_node"].replace("-", "_").replace(".", "_")
        target = edge["to_node"].replace("-", "_").replace(".", "_")
        label = f"{edge['transition_letter']}: {edge['action_name']}".replace('"', "'")
        markdown.append(f'  {source} -->|"{label}"| {target}')
    markdown.extend(["```", ""])
    (target_dir / "dda_dag_summary.md").write_text(
        "\n".join(markdown), encoding="utf-8"
    )

    return summary_data


