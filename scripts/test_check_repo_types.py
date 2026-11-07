"""Origin: scripts/test_check_repo_types.py
Claim: scripts/check_repo_types.py applies block meta of governance/types/repository.type.yaml as written: ownership by
longest claimed folder, first-match order, the glob grammar, the catch-all rule, every finding kind, the naming
report and the public-text normalisation
AuthorityEffect: None
Scope Fence: a synthetic tree in tmp_path; the real tree is only read for the smoke test at the end
Level: L5
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_repo_types as crt  # noqa: E402


def leaf(name: str, **over) -> dict:
    base = {"name": name, "format": "md", "naming": "lower", "schema": "none", "companions": "none", "authored": "hand"}
    base.update(over)
    return base


def member(name: str, match: str, leaf_name: str, **over) -> dict:
    base = {"name": name, "match": match, "leaf": leaf_name, "now": 0, "target": 0}
    base.update(over)
    return base


def write_types(tmp_path: Path, root_doc: dict, others: dict[str, dict]) -> Path:
    types_dir = tmp_path / "governance" / "types"
    types_dir.mkdir(parents=True)
    (types_dir / "repository.type.yaml").write_text(yaml.safe_dump(root_doc, sort_keys=False), encoding="utf-8")
    for name, doc in others.items():
        (types_dir / f"{name}.type.yaml").write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    return types_dir


def base_root(**over) -> dict:
    doc = {
        "schema": "repo-type/1",
        "file_for": ".",
        "naming_rules": {
            "lower": {"pattern": "^[._]*[a-z0-9][a-z0-9_.+-]*$"},
            "readme": {"pattern": "^README([._-][A-Za-z0-9_.-]+)?$"},
            "toolchain": {"pattern": "^(Cargo\\.toml|Cargo\\.lock|lean-toolchain)$"},
            "deposit_boilerplate": {"pattern": "^(MANIFEST\\.sha256|SHA256SUMS)$"},
            "lean_namespace_folder": {"pattern": "^[A-Z][A-Za-z0-9_]*$"},
            "dag_id": {"pattern": "^[A-Z0-9][A-Z0-9_-]*(\\.md)?$"},
            "utc_stamp": {"pattern": "^[0-9]{8}T[0-9]{6}Z.*$"},
            "imported": {"pattern": ".*"},
            "exception": {"paths": ["docs/UPPER.md"]},
        },
        "public_text": {"allow": [], "term_sha256": {}},
        "classes": [
            {
                "class": "Repository",
                "path": ".",
                "summary": "root",
                "role": "source",
                "counts": {"now": 0, "target": 0},
                "attributes": [
                    {"name": "alpha", "class": "AlphaFolder", "required": True},
                    {"name": "beta", "class": "BetaFolders", "required": True},
                    {"name": "dots", "class": "DotFolders", "required": True},
                    member("readme", "README.md", "FrontPage", required=True),
                ],
                "collections": [member("root_notes", "*.md", "Note")],
            },
            {
                "class": "DotFolders",
                "path_glob": ".*",
                "summary": "dot folders",
                "role": "tooling",
                "counts": {"now": 0, "target": 0},
                "collections": [member("workflows", "workflows/*.yml", "Workflow")],
            },
        ],
        "leaf_types": [leaf("FrontPage", naming="readme"), leaf("Note"), leaf("Workflow", format="yaml")],
    }
    doc.update(over)
    return doc


def alpha_doc() -> dict:
    return {
        "schema": "repo-type/1",
        "file_for": "alpha",
        "classes": [
            {
                "class": "AlphaFolder",
                "path": "alpha",
                "summary": "alpha",
                "role": "document",
                "counts": {"now": 0, "target": 0},
                "attributes": [
                    member("readme", "README.md", "FrontPage", required=True),
                    {"name": "inner", "class": "AlphaInner", "required": False},
                ],
                "collections": [
                    member("first", "notes/*.md", "Note"),
                    member("shadowed", "notes/a.md", "Note"),
                    member("deep", "deep/**/*.md", "Note"),
                    member("sets", "set/[abc]?.txt", "Text"),
                    member("choice", "{x,y}/*.{json,yaml}", "Data"),
                ],
            },
            {
                "class": "AlphaInner",
                "path": "alpha/inner",
                "summary": "inner",
                "role": "document",
                "counts": {"now": 0, "target": 0},
                "collections": [member("all", "**", "Blob", catch_all=True, authored="imported:alpha/ledger.json")],
            },
        ],
        "leaf_types": [leaf("Text", format="text"), leaf("Data", format="json"), leaf("Blob", format="any", naming="imported", authored="imported:alpha/ledger.json")],
    }


def beta_doc() -> dict:
    return {
        "schema": "repo-type/1",
        "file_for": "beta",
        "classes": [
            {
                "class": "BetaFolders",
                "paths": ["beta_one", "beta_two"],
                "summary": "beta",
                "role": "record",
                "counts": {"now": 0, "target": 0},
                "collections": [member("records", "*.json", "Data")],
                "relations": [{"kind": "derives_from", "to": "AlphaFolder", "via": "copies"}],
            }
        ],
        "leaf_types": [],
    }


FILES = [
    "README.md",
    "notes.md",
    ".github/workflows/ci.yml",
    "alpha/README.md",
    "alpha/notes/a.md",
    "alpha/notes/b.md",
    "alpha/deep/x/y/z.md",
    "alpha/deep/top.md",
    "alpha/set/a1.txt",
    "alpha/set/d1.txt",
    "alpha/x/one.json",
    "alpha/y/two.yaml",
    "alpha/inner/anything.bin",
    "alpha/inner/sub/more.bin",
    "beta_one/r.json",
    "beta_two/s.json",
    "beta_two/loose.txt",
]


def test_ownership_matching_and_findings(tmp_path):
    types = crt.Types(write_types(tmp_path, base_root(), {"alpha": alpha_doc(), "beta": beta_doc()}))
    assert types.findings["FORM"] == []
    result = crt.evaluate(types, FILES)
    # ownership: longest claimed folder wins; path_glob claims the dot folder; the root owns the rest
    assert result.match["alpha/inner/sub/more.bin"] == ("AlphaInner", "all", "Blob")
    assert result.match[".github/workflows/ci.yml"] == ("DotFolders", "workflows", "Workflow")
    assert result.match["notes.md"] == ("Repository", "root_notes", "Note")
    assert result.match["beta_two/s.json"] == ("BetaFolders", "records", "Data")
    # first match wins, so the later exact member is shadowed and DEAD
    assert result.match["alpha/notes/a.md"] == ("AlphaFolder", "first", "Note")
    assert "member AlphaFolder.shadowed" in result.findings["DEAD"]
    # ** as a whole segment matches zero or more segments
    assert result.match["alpha/deep/x/y/z.md"][1] == "deep"
    assert result.match["alpha/deep/top.md"][1] == "deep"
    # [...] and ? and {a,b}
    assert result.match["alpha/set/a1.txt"][1] == "sets"
    assert "alpha/set/d1.txt" in result.findings["UNTYPED"]
    assert result.match["alpha/x/one.json"][1] == "choice"
    assert result.match["alpha/y/two.yaml"][1] == "choice"
    # UNTYPED: a file in a claimed folder that no member matches
    assert "beta_two/loose.txt" in result.findings["UNTYPED"]
    assert result.findings["MISSING"] == []
    assert result.findings["UNKNOWN"] == []
    assert result.findings["CLAIM"] == []


def test_missing_unknown_claim_and_form(tmp_path):
    root = base_root()
    root["classes"][0]["attributes"].append(member("licence", "LICENSE", "Note", required=True))
    root["classes"][0]["attributes"].append({"name": "gamma", "class": "GammaFolder", "required": True})
    root["classes"][0]["collections"].append(member("ghost", "*.ghost", "NoSuchLeaf"))
    root["classes"][0]["relations"] = [{"kind": "cites", "to": "Nowhere", "via": "x"}]
    alpha = alpha_doc()
    alpha["classes"].append({"class": "GammaFolder", "path": "gamma", "summary": "g", "role": "record", "counts": {"now": 0, "target": 0}, "collections": [member("any", "*", "Data")]})
    beta = beta_doc()
    beta["classes"][0]["paths"].append("alpha")  # claims a folder AlphaFolder already claims
    beta["classes"].append({"class": "AlphaInner", "path": "elsewhere", "summary": "dup", "role": "record", "counts": {"now": 0, "target": 0}})
    beta["leaf_types"].append(leaf("Note"))  # a leaf name defined twice
    types = crt.Types(write_types(tmp_path, root, {"alpha": alpha, "beta": beta}))
    result = crt.evaluate(types, FILES)
    assert "Repository.licence" in result.findings["MISSING"]
    assert "Repository.gamma" in result.findings["MISSING"]
    assert any("NoSuchLeaf" in x for x in result.findings["UNKNOWN"])
    assert any("Nowhere" in x for x in result.findings["UNKNOWN"])
    assert any("folder alpha" in x for x in result.findings["CLAIM"])
    assert any("class AlphaInner" in x for x in result.findings["CLAIM"])
    assert any("leaf Note" in x for x in result.findings["CLAIM"])


def test_form_errors(tmp_path):
    root = base_root()
    root["classes"][0]["role"] = "whatever"
    alpha = alpha_doc()
    alpha["classes"][0]["collections"].append({"name": "no_counts", "match": "q/*", "leaf": "Note"})
    alpha["classes"][0]["collections"].append(member("bad_catch_all", "**", "Note"))
    alpha["classes"][0]["collections"].append(member("flag_without", "z/*", "Note", catch_all=True))
    alpha["classes"][0]["collections"].append(member("authored", "w/*", "Note", authored="derived from x"))
    alpha["classes"][0]["invariants"] = [{"id": "a.b", "statement": "s", "holds_now": "maybe", "checked_by": "unchecked"}]
    alpha["leaf_types"].append({"name": "Half", "format": "md", "naming": "nosuchrule", "schema": "none", "companions": "sometimes", "authored": "hand"})
    alpha["classes"].append({"class": "TwoHomes", "path": "p", "paths": ["q"], "summary": "s", "role": "record", "counts": {"now": 0, "target": 0}})
    types = crt.Types(write_types(tmp_path, root, {"alpha": alpha, "beta": beta_doc()}))
    form = "\n".join(types.findings["FORM"])
    for needle in ("role 'whatever'", "no_counts: now missing", "bad_catch_all: a catch-all needs", "flag_without: catch_all on", "authored 'derived from x'",
                   "holds_now 'maybe'", "naming rule 'nosuchrule'", "companions 'sometimes'", "TwoHomes: exactly one of"):
        assert needle in form, needle


def test_catch_all_and_shadowing_order(tmp_path):
    alpha = alpha_doc()
    # attributes with match are tried before collections, in order
    alpha["classes"][0]["attributes"].insert(0, member("early", "notes/b.md", "Text", required=True))
    types = crt.Types(write_types(tmp_path, base_root(), {"alpha": alpha, "beta": beta_doc()}))
    result = crt.evaluate(types, FILES)
    assert result.match["alpha/notes/b.md"][1] == "early"
    assert result.match["alpha/notes/a.md"][1] == "first"
    assert result.match["alpha/inner/anything.bin"][1] == "all"


def test_naming_report(tmp_path):
    files = FILES + ["alpha/Upper.md", "alpha/inner/Imported.bin", "alpha/Cargo.toml", "docs/UPPER.md", "alpha/archive/old.md", "alpha/Bad-Name/x.md"]
    types = crt.Types(write_types(tmp_path, base_root(), {"alpha": alpha_doc(), "beta": beta_doc()}))
    alpha_cls = types.classes["AlphaFolder"][1]
    alpha_cls["collections"].append(member("rest", "*", "Note"))
    alpha_cls["collections"].append(member("camel", "Bad-Name/*", "Note"))
    alpha_cls["collections"].append(member("archive", "archive/*", "Note"))
    result = crt.evaluate(types, files)
    rows = {(category, path) for category, path, _detail in crt.naming_report(types, files, result)}
    assert ("violation", "alpha/Upper.md") in rows
    assert ("imported", "alpha/inner/Imported.bin") in rows
    assert ("exception", "docs/UPPER.md") in rows
    assert ("archive", "alpha/archive/") in rows
    assert ("folder", "alpha/Bad-Name/") in rows
    assert not any(path == "alpha/Cargo.toml" for _c, path in rows)  # the universal toolchain rule
    assert not any(path == "alpha/README.md" for _c, path in rows)


def sha(word: str) -> str:
    return hashlib.sha256(word.encode()).hexdigest()


def test_public_text_normalisation(tmp_path):
    block = {
        "allow": [{"match": "allowed/*", "reason": "test"}],
        "term_sha256": {"brand": [sha("zorbletron"), sha("quux corp")], "vendor": [sha("flombic")]},
    }
    rule = crt.PublicText(block)
    assert rule.scan(b"nothing here") == set()
    assert rule.scan(b"the zorbletron engine") == {"brand"}
    assert rule.scan(b"Zorbletrons everywhere") == {"brand"}  # one trailing s removed
    assert rule.scan(b"MyZorbletronTool") == {"brand"}  # CamelCase split
    assert rule.scan(b"quux-corp, said") == {"brand"}  # non-letters become one space; pairs are tried
    assert rule.scan(b"quux and corp") == set()  # not adjacent
    assert rule.scan(b"Flombic/zorbletron") == {"brand", "vendor"}
    assert rule.scan(b"zorbletronic") == set()  # whole words only
    repo = tmp_path / "repo"
    (repo / "allowed").mkdir(parents=True)
    (repo / "plain").mkdir()
    (repo / "allowed" / "a.txt").write_bytes(b"zorbletron")
    (repo / "plain" / "b.txt").write_bytes(b"flombic")
    (repo / "plain" / "c.bin").write_bytes(b"flombic\0binary")
    (repo / "plain" / "zorbletron.txt").write_bytes(b"clean content")
    files = ["allowed/a.txt", "plain/b.txt", "plain/c.bin", "plain/zorbletron.txt"]
    types = crt.Types(write_types(tmp_path, base_root(public_text=block), {"alpha": alpha_doc(), "beta": beta_doc()}))
    hits, allowed = crt.public_text_report(types, repo, files)
    assert allowed == ["allowed/a.txt"]
    assert [(p, c, by_path) for p, c, by_path in hits] == [("plain/b.txt", "vendor", False), ("plain/zorbletron.txt", "brand", True)]


def test_duplicates_report(tmp_path):
    types = crt.Types(write_types(tmp_path, base_root(), {"alpha": alpha_doc(), "beta": beta_doc()}))
    tree = {f: f"blob{i}" for i, f in enumerate(FILES)}
    tree["beta_one/r.json"] = tree["alpha/x/one.json"]  # BetaFolders derives_from AlphaFolder: declared
    tree["alpha/notes/b.md"] = tree["alpha/notes/a.md"]  # same class, no relation: undeclared
    result = crt.evaluate(types, FILES)
    groups = crt.duplicates_report(types, tree, result)
    assert groups == [["alpha/notes/a.md", "alpha/notes/b.md"]]
    types.classes["AlphaFolder"][1]["allow"] = [{"match": "notes/*", "reason": "test"}]
    assert crt.duplicates_report(types, tree, result) == []


def test_plan_parsing():
    epic = "intro\n```text\nS05  a/b/ -> c/d/\nS09  blob abc123 -> z/run.md\n```\n\n```text\nS03  rules/\nS04  lean4/qm*.md  (3 files)\nKEEP lean4/qm_keep.md\nS05  one.txt\n```\n"
    plan = crt.Plan(epic)
    assert plan.unparsed == []
    tree = {"rules/r.yaml": "b1", "lean4/qm_a.md": "b2", "lean4/qm_b.md": "b3", "lean4/qm_c.md": "b4", "lean4/qm_keep.md": "b5", "a/b/f.txt": "b6", "one.txt": "b7", "z/old_name.md": "abc123ffff"}
    removed, lines, moved, problems = plan.story("S04", tree)
    assert removed == ["lean4/qm_a.md", "lean4/qm_b.md", "lean4/qm_c.md"] and problems == []
    removed, lines, moved, problems = plan.story("S05", tree)
    assert moved == [("a/b/f.txt", "c/d/f.txt")] and removed == ["one.txt"]
    removed, lines, moved, problems = plan.story("S09", tree)
    assert moved == [("z/old_name.md", "z/run.md")]
    plan2 = crt.Plan("```text\nS04  lean4/qm*.md  (2 files)\n```")
    assert plan2.story("S04", tree)[3]


def test_glob_grammar_edge_cases():
    assert crt.glob_regex("**").match("a/b/c")
    assert crt.glob_regex("a/**").match("a/b/c") and not crt.glob_regex("a/**").match("ab/c")
    assert crt.glob_regex("**/README.md").match("README.md") and crt.glob_regex("**/README.md").match("x/y/README.md")
    assert crt.glob_regex("*.md").match(".hidden.md") and not crt.glob_regex("*.md").match("x/y.md")
    assert crt.glob_regex("a?c").match("abc") and not crt.glob_regex("a?c").match("a/c")
    assert crt.glob_regex("exact.path").match("exact.path") and not crt.glob_regex("exact.path").match("exactXpath")
    assert crt.glob_regex("{a,b}/{c,d}.md").match("b/c.md")


def test_real_tree_smoke():
    """The real type files load without FORM, UNKNOWN or CLAIM findings."""
    types = crt.Types(crt.ROOT / crt.TYPES_DIR)
    assert types.findings["FORM"] == []
    assert types.findings["UNKNOWN"] == []
    assert types.findings["CLAIM"] == []
