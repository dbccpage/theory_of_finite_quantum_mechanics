from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import json
from pathlib import Path
import sys
import tempfile

from omega_engine.crates.prompt_civilization.cli import main


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "_ooutwire"
    / "2026-08-13-132939-local-command-caveatcaveat-the-messages-below.txt"
)
ESTATE = ROOT / ".agents" / "anti_skills"


def _run(*arguments: str) -> tuple[int, str, str]:
    original = list(sys.argv)
    stdout = StringIO()
    stderr = StringIO()
    try:
        sys.argv = ["omega-prompt", *arguments]
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = main()
    finally:
        sys.argv = original
    return code, stdout.getvalue(), stderr.getvalue()


def test_all_public_cli_commands_round_trip_without_send_or_admit() -> None:
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        episodes = root / "episodes.json"
        candidates = root / "candidates.json"
        registry = root / "registry.json"
        bundle = root / "bundle.json"
        approved = root / "approved.json"
        packet = root / "packet.json"
        evaluation = root / "evaluation.json"

        code, _, error = _run(
            "segment-dialogue",
            "--source",
            str(SOURCE),
            "--start-line",
            "12693",
            "--end-line",
            "13354",
            "--output",
            str(episodes),
        )
        assert code == 0 and not error
        assert len(json.loads(episodes.read_text(encoding="utf-8"))["episodes"]) == 5

        code, _, error = _run(
            "mine-candidates",
            "--episodes",
            str(episodes),
            "--output",
            str(candidates),
        )
        assert code == 0 and not error
        assert json.loads(candidates.read_text(encoding="utf-8"))["candidates"] == []

        code, _, error = _run(
            "validate-registry",
            "--registry",
            str(ESTATE / "admitted" / "registry.json"),
            "--output",
            str(registry),
        )
        assert code == 0 and not error

        code, _, error = _run(
            "review",
            "--original",
            str(ESTATE / "fixtures" / "original_prompt.txt"),
            "--proposal",
            str(ESTATE / "fixtures" / "valid_prompt_proposal.json"),
            "--registry",
            str(registry),
            "--output",
            str(bundle),
        )
        assert code == 0 and not error

        code, _, error = _run(
            "approve",
            "--bundle",
            str(bundle),
            "--operator",
            "jeremy",
            "--output",
            str(approved),
        )
        assert code == 0 and not error

        code, _, error = _run(
            "packetize",
            "--approved",
            str(approved),
            "--output",
            str(packet),
        )
        assert code == 0 and not error
        assert json.loads(packet.read_text(encoding="utf-8"))["authority_effect"] == "None"

        code, _, error = _run(
            "evaluate-fixtures",
            "--cases",
            str(ESTATE / "fixtures" / "eval_cases.json"),
            "--proposal",
            str(ESTATE / "fixtures" / "valid_prompt_proposal.json"),
            "--registry",
            str(registry),
            "--output",
            str(evaluation),
        )
        assert code == 0 and not error
        assert json.loads(evaluation.read_text(encoding="utf-8"))["outcome"] == "COMPUTED_PASS"


def test_cli_converts_malformed_wire_into_typed_refusal() -> None:
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        malformed = root / "proposal.json"
        malformed.write_text('{"objective":"a","objective":"b"}', encoding="utf-8")
        code, _, error = _run(
            "review",
            "--original",
            str(ESTATE / "fixtures" / "original_prompt.txt"),
            "--proposal",
            str(malformed),
            "--registry",
            str(ESTATE / "admitted" / "registry.json"),
        )
        assert code == 2
        assert "duplicate JSON key" in error
