"""Adversarial source-contract tests; no mathematical truth is inferred."""
from __future__ import annotations

import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest
from pydantic import ValidationError

from paper_contract.audit import PaperBaseline, compare, fingerprint, integrity_issues
from paper_contract.inventory import (
    BASELINE,
    LEDGER,
    MANUSCRIPT,
    from_git_tree,
    git_blob,
    worktree_snapshot,
)
from paper_contract.models import PaperDocument, ResearchPaper
from paper_contract.parser import parse_document, parse_ledger, table_cells

TEXT = "# Theory\n\n**Version:** 1.0\n\n<a id=\"chapter-01\"></a>\n\n## 1. Questions\n\n`WDP-CH01-O01` is resolved. $x=y$ and \\(a+b\\).\n\n$$\nx=1 \\tag{A}\n$$\n\n### 1.1 Details\n\n| a | b |\n|---|---|\n| $x|y$ | `a|b` |\n\n## 1. Questions\n\nLiteral end.\n"
CLAIMS = "# Ledger\n\n<!-- CANONICAL-CLAIM-TABLE:BEGIN -->\n\n| ID | Status | Canonical location | Bound evidence | Canonical statement |\n|---|---|---|---|---|\n| WDP-CH01-O01 | FINITE_PROPOSITION | [#chapter-01](witnessed_difference_programme.md#chapter-01) | P | $x=y$ under the declared condition. |\n\n<!-- CANONICAL-CLAIM-TABLE:END -->\n"


def tree(text=TEXT, ledger=CLAIMS):
    files = {MANUSCRIPT: text.encode(), LEDGER: ledger.encode(), "code/tests/test_example.py": b"pass\n",
             "docs/proof.md": b"proof\n", "lean4/Proof.lean": b"-- scoped\n", "scripts/check.py": b"pass\n"}
    entries = [{"path": p, "type": "tree", "mode": "040000"} for p in ["code", "code/tests", "docs", "lean4", "scripts"]]
    entries.extend({"path": p, "type": "blob", "mode": "100644", "sha": git_blob(data), "size": len(data)} for p, data in files.items())
    return {"commit": "a" * 40, "root": "atlas/paper", "entries": entries}, files


def paper(text=TEXT, ledger=CLAIMS):
    inventory, _ = tree(text, ledger)
    return from_git_tree(text, ledger, inventory, repository="owner/repo")


def test_literal_roundtrip_and_indexes():
    doc = parse_document(TEXT, MANUSCRIPT)
    assert doc.literal() == TEXT
    assert len(doc.sections) == 4
    assert len({s.id for s in doc.sections}) == 4
    assert doc.sections[-1].id.endswith("~2")
    assert len(doc.equations) == 4
    assert doc.equations[2].display and doc.equations[2].labels == ("A",)
    assert doc.sections[2].parent_id == doc.sections[1].id
    assert doc.metadata_fields[0].value_literal == "1.0"
    assert PaperDocument.model_validate_json(doc.model_dump_json()) == doc


@pytest.mark.parametrize("text", ["", "plain", "α\r\nβ\r\n", "# A\n# B\n", "# A\n\ntext"])
def test_all_bytes_retained(text):
    assert parse_document(text, "paper.md").literal() == text


def test_math_code_escaping_and_balanced_pipes():
    raw = "# Test\n\n`$not_math$` \\$money $a+b$ \\(x\\).\n\n```python\n# fake\n$fake$ WDP-CH99-P01\n```\n"
    doc = parse_document(raw, "paper.md")
    assert [e.latex for e in doc.equations] == ["a+b", "x"]
    assert len(doc.sections) == 1
    assert not doc.claim_occurrences
    assert table_cells("| $x|y$ | `a|b` | \\| |\n") == ("$x|y$", "`a|b`", "\\|")
    assert table_cells("| a | b\n") == ("a", "b")


@pytest.mark.parametrize("raw,code", [("# A\n\n$$unclosed", "unclosed_math"), ("```text\nraw", "unclosed_code_fence")])
def test_unclosed_syntax_is_preserved_and_reported(raw, code):
    doc = parse_document(raw, "paper.md")
    assert doc.literal() == raw
    assert doc.diagnostics[0].code == code


@pytest.mark.parametrize("mutation", ["extra", "hash", "span", "line", "heading", "equation", "drop_equation", "drop_claim", "claim_id", "duplicate_section", "metadata", "table"])
def test_forged_document_indexes_fail(mutation):
    payload = json.loads(parse_document(TEXT, MANUSCRIPT).model_dump_json())
    if mutation == "extra":
        payload["made_up"] = 1
    elif mutation == "hash":
        payload["source_sha256"] = "0" * 64
    elif mutation == "span":
        payload["blocks"][1]["span"]["start"] += 1
    elif mutation == "line":
        payload["equations"][0]["span"]["start_line"] += 1
    elif mutation == "heading":
        payload["blocks"][0]["title"] = "Something else"
    elif mutation == "equation":
        payload["equations"][0]["latex"] = "false"
    elif mutation == "drop_equation":
        payload["equations"].pop()
    elif mutation == "drop_claim":
        payload["claim_occurrences"].pop()
    elif mutation == "claim_id":
        payload["claim_occurrences"][0]["claim_id"] = "WDP-CH01-P99"
    elif mutation == "duplicate_section":
        payload["sections"].append(payload["sections"][0])
    elif mutation == "metadata":
        payload["metadata_fields"][0]["value_literal"] = "100.0"
    else:
        next(b for b in payload["blocks"] if b["kind"] == "table")["rows"].pop()
    with pytest.raises(ValidationError):
        PaperDocument.model_validate_json(json.dumps(payload))


def test_status_comes_from_ledger_not_claim_id():
    p = paper()
    assert p.claim_ledger.records[0].claim_id.endswith("O01")
    assert p.claim_ledger.records[0].status == "FINITE_PROPOSITION"
    assert not integrity_issues(p)


@pytest.mark.parametrize("field,value", [("status", "OPEN_CLAIM"), ("statement_literal", "An enlarged theorem"), ("evidence_literal", "L:exact(fake)")])
def test_forged_ledger_semantics_fail(field, value):
    payload = json.loads(paper().model_dump_json())
    payload["claim_ledger"]["records"][0][field] = value
    with pytest.raises(ValidationError):
        ResearchPaper.model_validate_json(json.dumps(payload))


def test_authoritative_claim_index_cannot_omit_rows():
    payload = json.loads(paper().model_dump_json())
    payload["claim_ledger"]["records"] = []
    with pytest.raises(ValidationError):
        ResearchPaper.model_validate_json(json.dumps(payload))


@pytest.mark.parametrize("field", ["section_owner", "section_extent", "block_membership", "table_cell"])
def test_indexes_cannot_change_structure_while_preserving_raw_text(field):
    payload = json.loads(parse_document(TEXT, MANUSCRIPT).model_dump_json())
    if field == "section_owner":
        payload["equations"][0]["section_id"] = payload["sections"][0]["id"]
    elif field == "section_extent":
        payload["sections"][0]["span"]["end"] -= 1
    elif field == "block_membership":
        payload["sections"][1]["block_ids"].pop()
    else:
        next(b for b in payload["blocks"] if b["kind"] == "table")["rows"][0]["cells"][0] = "forged"
    with pytest.raises(ValidationError):
        PaperDocument.model_validate_json(json.dumps(payload))


@pytest.mark.parametrize("raw", [CLAIMS.replace("<!-- CANONICAL-CLAIM-TABLE:END -->", ""), CLAIMS.replace("FINITE_PROPOSITION", "UNKNOWN_STATUS"), CLAIMS.replace("WDP-CH01-O01", "not-a-claim")])
def test_malformed_ledger_fails(raw):
    with pytest.raises(ValueError):
        parse_ledger(raw, LEDGER)


@pytest.mark.parametrize("folder", ["code", "code/tests", "docs", "lean4", "scripts"])
def test_required_folders_cannot_disappear(folder):
    inventory, _ = tree()
    inventory["entries"] = [e for e in inventory["entries"] if e["path"] != folder and not e["path"].startswith(folder + "/")]
    with pytest.raises(ValueError):
        from_git_tree(TEXT, CLAIMS, inventory, repository="owner/repo")


@pytest.mark.parametrize("mutation", ["duplicate", "escape", "backslash", "absolute", "symlink", "submodule", "truncated", "wrong_blob", "wrong_bytes", "orphan"])
def test_bad_inventory_fails(mutation):
    inventory, _ = tree()
    if mutation == "duplicate":
        inventory["entries"].append(deepcopy(inventory["entries"][0]))
    elif mutation in {"escape", "backslash", "absolute"}:
        inventory["entries"][0]["path"] = {"escape": "../code", "backslash": "code\\tests", "absolute": "/code"}[mutation]
    elif mutation == "symlink":
        inventory["entries"][-1]["mode"] = "120000"
    elif mutation == "submodule":
        inventory["entries"][-1]["type"] = "commit"
    elif mutation == "truncated":
        inventory["truncated"] = True
    elif mutation in {"wrong_blob", "wrong_bytes"}:
        entry = next(e for e in inventory["entries"] if e["path"] == MANUSCRIPT)
        entry["sha" if mutation == "wrong_blob" else "size"] = "0" * 40 if mutation == "wrong_blob" else 1
    else:
        inventory["entries"] = [e for e in inventory["entries"] if e["path"] != "code/tests"]
    with pytest.raises(ValueError):
        from_git_tree(TEXT, CLAIMS, inventory, repository="owner/repo")


def test_case_colliding_inventory_fails():
    inventory, _ = tree()
    entry = next(e for e in inventory["entries"] if e["path"] == "docs/proof.md")
    inventory["entries"].append({**entry, "path": "docs/Proof.md"})
    with pytest.raises(ValueError, match="case-colliding"):
        from_git_tree(TEXT, CLAIMS, inventory, repository="owner/repo")


def test_optional_and_additional_folder_types():
    inventory, _ = tree()
    for name in ["evidence", "jupyter_notebooks", "images", "manifests", "future_folder"]:
        inventory["entries"].append({"path": name, "type": "tree", "mode": "040000"})
    p = from_git_tree(TEXT, CLAIMS, inventory, repository="owner/repo")
    assert p.evidence.path == "evidence" and p.jupyter_notebooks.path == "jupyter_notebooks"
    assert p.additional_folders[0].path == "future_folder"
    assert ResearchPaper.model_validate_json(p.model_dump_json()) == p
    with pytest.raises(ValidationError):
        p.authority_effect = "yes"


def test_baseline_detects_prose_equation_renumbering_status_and_evidence_changes():
    baseline = fingerprint(paper())
    assert compare(baseline, paper()).matches_baseline
    for replacement in [("Literal end.", "Silently altered."), ("x=1", "x=2"), ("WDP-CH01-O01", "WDP-CH01-O02")]:
        report = compare(baseline, paper(TEXT.replace(*replacement)))
        assert not report.matches_baseline
        assert "document" in {c.category for c in report.changes}
    changed = paper(ledger=CLAIMS.replace("FINITE_PROPOSITION", "OPEN_CLAIM").replace("| P |", "| L:exact(fake) |"))
    assert any(c.category == "claim" for c in compare(baseline, changed).changes)
    assert PaperBaseline.model_validate_json(baseline.model_dump_json()) == baseline


def test_worktree_includes_untracked_and_dirty_files_and_detects_deletion(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    root = tmp_path / "atlas" / "paper"
    _, files = tree()
    for path, data in files.items():
        dest = root / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    subprocess.run(["git", "-C", str(tmp_path), "add", "."], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "-c", "user.name=Contract test", "-c", "user.email=test@example.invalid", "commit", "-qm", "fixture"], check=True)
    first = worktree_snapshot(root, repository="owner/repo")
    baseline = fingerprint(first)
    assert compare(baseline, first).matches_baseline
    (root / "docs" / "new.md").write_text("new\n")
    report = compare(baseline, worktree_snapshot(root, repository="owner/repo"))
    assert any(c.key == "docs/new.md" and c.operation == "added" for c in report.changes)
    (root / MANUSCRIPT).write_text(TEXT.replace("x=1", "x=0"))
    report = compare(baseline, worktree_snapshot(root, repository="owner/repo"))
    assert any(c.category == "equation" for c in report.changes)
    (root / BASELINE).parent.mkdir(exist_ok=True)
    (root / BASELINE).write_text("self-reference is excluded\n")
    assert not any(f.path == BASELINE for f in worktree_snapshot(root, repository="owner/repo").artifacts())
    (root / "lean4" / "Proof.lean").unlink()
    with pytest.raises(ValueError, match="missing/nonregular"):
        worktree_snapshot(root, repository="owner/repo")


def test_live_full_manuscript_roundtrip_and_claim_census():
    root = Path(__file__).resolve().parents[4]
    if not (root / MANUSCRIPT).is_file():
        pytest.skip("full manuscript available in the repository checkout")
    raw = (root / MANUSCRIPT).read_bytes().decode("utf-8")
    doc = parse_document(raw, MANUSCRIPT)
    ledger = parse_ledger((root / LEDGER).read_bytes().decode("utf-8"), LEDGER)
    assert doc.literal() == raw and not doc.diagnostics
    assert len([r for r in ledger.records if r.register_kind == "canonical"]) == 154
    assert len([r for r in ledger.records if r.register_kind == "preserver_generator_supplement"]) == 9
    # October 16 source includes the mechanism inventory and witnessed reasoning.
    assert len(doc.sections) == 440
    assert "### 20.14 From an admitted distinction to witnessed reasoning" in raw
    assert "### 20.15 Executable refinement and kernel replay" in raw
    assert all(r.claim_id in {c.claim_id for c in doc.claim_occurrences} for r in ledger.records)


def test_cli_explicit_trusted_baseline_and_drift_exit_codes(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    root = tmp_path / "atlas" / "paper"
    _, files = tree()
    for path, data in files.items():
        dest = root / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    subprocess.run(["git", "-C", str(tmp_path), "add", "."], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "-c", "user.name=Contract test", "-c", "user.email=test@example.invalid", "commit", "-qm", "fixture"], check=True)
    script = Path(__file__).resolve().parents[4] / "scripts/check_paper_contract.py"

    def run(command, *args):
        return subprocess.run([sys.executable, str(script), command, "--paper-root", str(root), "--repository", "owner/repo", *map(str, args)],
                              capture_output=True, text=True, check=False)

    assert run("inspect").returncode == 0
    schema = tmp_path / "schema.json"
    assert run("schema", "--output", schema).returncode == 0
    assert "ResearchPaper" in schema.read_text()
    trusted = tmp_path / "trusted.json"
    assert run("baseline", "--output", trusted).returncode == 0
    assert run("check").returncode == 2
    assert run("check", "--trusted-baseline", trusted).returncode == 1  # candidate baseline absent
    candidate = root / BASELINE
    candidate.parent.mkdir(exist_ok=True)
    candidate.write_bytes(trusted.read_bytes())
    assert run("check", "--trusted-baseline", trusted).returncode == 0
    candidate.write_text("{}\n")
    assert run("check", "--trusted-baseline", trusted).returncode == 1
    candidate.write_bytes(trusted.read_bytes())
    (root / MANUSCRIPT).write_text(TEXT.replace("x=1", "x=2"))
    result = run("check", "--trusted-baseline", trusted)
    assert result.returncode == 1 and '"category": "equation"' in result.stdout
    (root / "docs/proof.md").unlink()
    assert run("check", "--trusted-baseline", trusted).returncode == 2


@pytest.mark.parametrize("mutation", ["drop_reference", "alter_target", "drop_metadata", "drop_parent"])
def test_complete_literal_indexes_cannot_be_forged(mutation):
    payload = json.loads(parse_document(TEXT, MANUSCRIPT).model_dump_json())
    if mutation == "drop_reference":
        payload["references"].pop()
    elif mutation == "alter_target":
        payload["references"][0]["target"] = "invented-anchor"
    elif mutation == "drop_metadata":
        payload["metadata_fields"] = []
    else:
        for section in payload["sections"]:
            section["parent_id"] = None
            section["children"] = []
    with pytest.raises(ValidationError):
        PaperDocument.model_validate_json(json.dumps(payload))


def test_inventory_rejects_linked_ancestors(tmp_path):
    from paper_contract.inventory import regular_path
    real = tmp_path / "real"
    real.mkdir()
    (real / "paper.md").write_text("source")
    link = tmp_path / "alias"
    link.symlink_to(real, target_is_directory=True)
    with pytest.raises(ValueError, match="nonregular"):
        regular_path(link / "paper.md")
    with pytest.raises(ValueError, match="nonregular"):
        worktree_snapshot(link, repository="owner/repo")


@pytest.mark.parametrize("mutation", ["omit_heading", "fake_fence", "omit_ledger_table"])
def test_literal_block_types_cannot_hide_source_indexes(mutation):
    raw = CLAIMS if mutation == "omit_ledger_table" else "# Original\n\nText WDP-CH01-D01\n"
    doc = parse_document(raw, "paper.md")
    payload = json.loads(doc.model_dump_json())
    for block in payload["blocks"]:
        if mutation == "omit_heading" and block["kind"] == "heading":
            for key in ("level", "title", "number"):
                block.pop(key)
            block["kind"] = "prose"
        elif mutation == "omit_ledger_table" and block["kind"] == "table":
            block.pop("rows")
            block["kind"] = "prose"
        elif mutation == "fake_fence" and block["kind"] == "prose":
            block["kind"] = "code"
            block["language"] = "python"
    if mutation == "omit_heading":
        payload["sections"] = []
        for claim in payload["claim_occurrences"]:
            claim["section_id"] = None
    if mutation == "fake_fence":
        payload["claim_occurrences"] = []
    with pytest.raises(ValidationError, match="block classification"):
        PaperDocument.model_validate_json(json.dumps(payload))
