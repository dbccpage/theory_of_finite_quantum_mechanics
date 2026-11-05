"""Bounded local calculus reconstruction from retained PFP operations.

Retrieve the actual retained proposal, run its unchanged supplied task checker,
and record its checked result. This is not an execution of missing PFP stages or
a native Woland binding. Optional propose transitions are declared adversarial
outcomes, not evidence that any provider was called. Prices are operation units.
"""

import hashlib
import json
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from .checker import check_certificate
from .model import compile_model, digest, graph_model
from .replay import regular, sources, strict_json
from .structural import check_quotient, check_refinement

SOURCE = Path(__file__).resolve().parents[1] / "pfp_calculus" / "source"


def task_checker():
    regular(SOURCE / "calculus_reference_check.py")
    spec = spec_from_file_location(
        "supplied_calculus_reference", SOURCE / "calculus_reference_check.py"
    )
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def inputs():
    checker = task_checker()
    original = checker.problems()["real"]
    good = checker.strict_json(regular(SOURCE / "model_result.json").decode("utf-8"))
    bad = dict(good, antiderivative_coefficients=["0", "5"])
    return original, good, bad


def bound_model(*, allow_archive=True, shortcut=False):
    problem, good, bad = inputs()
    check = task_checker().check
    if (
        check(problem, good)["status"] != "checked_accept"
        or check(problem, bad)["status"] != "invalid_witness"
    ):
        raise ValueError("retained task or checker behavior changed")
    graph = {
        "ready": [("propose", "1", ["ready", "good", "bad"])],
        "good": [("check", "1", ["verified"])],
        "bad": [("check", "1", ["refused"])],
        "verified": [("record_resolution", "1", ["resolved"])],
        "refused": [],
    }
    if allow_archive:
        for s in ("ready", "refused"):
            graph[s].append(("retrieve_archived", "1", ["good"]))
    if shortcut:
        graph["ready"].append(("checked_shortcut", "1/2", ["resolved"]))
    model = graph_model(
        graph,
        initial="ready",
        targets=("resolved",),
        emissions={
            "record_resolution": "answer-50",
            **({"checked_shortcut": "answer-50"} if shortcut else {}),
        },
        valid_resolutions={s: ["answer-50"] for s in ("ready", "verified", "resolved")},
        task_id=digest(problem),
    )
    model["authorization"] = {"effect": "None", "external_authorization": "independently supplied"}
    return model


def bindings():
    original, good, _ = inputs()
    return {
        "task": digest(original),
        "candidate": digest(good),
        "checker_sha256": hashlib.sha256(
            regular(SOURCE / "calculus_reference_check.py")
        ).hexdigest(),
        "proposal_sha256": hashlib.sha256(regular(SOURCE / "model_result.json")).hexdigest(),
    }


def local_episode():
    """Execute actual retrieve -> independent check -> local record operations."""
    original, submitted, _ = inputs()
    receipt = task_checker().check(original, submitted)
    if receipt["status"] != "checked_accept":
        raise ValueError("submitted archive proposal failed")
    return {
        "bindings": bindings(),
        "submitted": submitted,
        "task_receipt": receipt,
        "operations": ["retrieve_archived", "check", "record_resolution"],
        "cost": "3",
        "value": receipt["value"],
        "authority_effect": "None",
    }


def check_bound_progress(model, certificate, episode):
    """Bind terminal truth to the original checker, independently of game search."""
    try:
        if (
            type(certificate) is not dict
            or certificate.get("kind") != "WIN_OPTIMAL"
            or certificate.get("optimality_requested") is not True
        ):
            return False
        original, good, _ = inputs()
        if episode.get("bindings") != bindings() or episode.get("submitted") != good:
            return False
        receipt = task_checker().check(original, episode["submitted"])
        if receipt != episode.get("task_receipt") or receipt["status"] != "checked_accept":
            return False
        if episode.get("value") != "50" or episode.get("authority_effect") != "None":
            return False
        if (
            episode.get("operations") != ["retrieve_archived", "check", "record_resolution"]
            or episode.get("cost") != "3"
        ):
            return False
        # Admit only the supplied reconstruction, including all prices and outcomes.
        if model != bound_model():
            return False
        game_receipt = check_certificate(model, certificate)
        if not game_receipt["accepted"] or game_receipt.get("initial_value") != "3":
            return False
        arena = compile_model(model)
        if any("answer-50" not in arena.valid_resolutions(b) for b in arena.targets):
            return False
        return check_progress_with_resolutions(
            model,
            certificate,
            original,
            {"answer-50": good},
            lambda problem, _state, payload: (
                task_checker().check(problem, payload)["status"] == "checked_accept"
            ),
        )
    except (ValueError, TypeError, KeyError):
        return False


def check_progress_with_resolutions(model, certificate, original, payloads, task_check):
    """Generic finite binding to an independently supplied state-aware checker.

    task_check(original, concrete_state, submitted_payload) must terminate and
    return an actual bool. Its source-task soundness is a separate hypothesis.
    Declared valid IDs must be sound; every target needs a common checked ID.
    Missing advertised IDs do not prove source-negative completeness.
    """
    try:
        arena = compile_model(model)
        if arena.task_id != digest(original) or set(payloads) != set(model["resolutions"]):
            return False
        for state in arena.states:
            for r in model["valid_resolutions"][state]:
                if task_check(original, state, payloads[r]) is not True:
                    return False
        if any(not arena.valid_resolutions(b) for b in arena.targets):
            return False
        return check_certificate(model, certificate)["accepted"]
    except (ValueError, TypeError, KeyError):
        return False


def replay_bound(data):
    if data.get("bindings") != bindings() or data.get("sources") != sources():
        raise ValueError("calculus or progress source binding changed")
    if not check_bound_progress(data["model"], data["certificate"], data["episode"]):
        raise ValueError("submitted strategy or actual task witness failed")
    exact = data["exact_quotient"]
    arena = compile_model(data["model"])
    seed = [[list(b) for b in arena.reachable]]
    if (
        not check_refinement(data["model"], seed, exact["refinement"])
        or not check_quotient(data["model"], exact["blocks"], exact["table"])
        or exact["blocks"] != exact["refinement"]["rounds"][-1]
    ):
        raise ValueError("quotient or coarseness receipt failed")
    for row, original, claim, value in (
        (data["proposal_only"], bound_model(allow_archive=False), "LOSS", None),
        (data["optional_shortcut"], bound_model(shortcut=True), "WIN_OPTIMAL", "1/2"),
    ):
        receipt = check_certificate(original, row["certificate"])
        if (
            row["model"] != original
            or not receipt["accepted"]
            or receipt.get("claim") != claim
            or receipt.get("initial_value") != value
        ):
            raise ValueError("changed operation menu or witness")
    if data["sources"] != sources() or data["bindings"] != bindings():
        raise ValueError("source changed during bound replay")
    return {
        "status": "PASS",
        "actual_task_answer": "50",
        "operating_optimum": "3",
        "proposal_only": "LOSS",
        "optional_shortcut_optimum": "1/2",
        "provider_calls": 0,
        "authority_effect": "None",
    }


def main():
    path = Path(__file__).parent / "evidence" / "bound_calculus.json"
    if sys.argv[1:] == ["--write"]:
        from .observation import refine_operation_presentation
        from .producer import solve_progress

        model = bound_model()
        arena = compile_model(model)
        data = {
            "bindings": bindings(),
            "sources": sources(),
            "model": model,
            "certificate": solve_progress(model)["certificate"],
            "episode": local_episode(),
            "exact_quotient": refine_operation_presentation(
                model, [[list(b) for b in arena.reachable]]
            ),
        }
        for key, original in (
            ("proposal_only", bound_model(allow_archive=False)),
            ("optional_shortcut", bound_model(shortcut=True)),
        ):
            data[key] = {"model": original, "certificate": solve_progress(original)["certificate"]}
        replay_bound(data)
        path.write_text(
            json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n"
        )
    elif sys.argv[1:]:
        raise SystemExit("usage: python -m certified_progress.calculus [--write]")
    raw = regular(path)
    print(json.dumps(replay_bound(strict_json(raw)), sort_keys=True))
    if regular(path) != raw:
        raise ValueError("retained witness changed during replay")


if __name__ == "__main__":
    main()
