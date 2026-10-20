"""Verify source-pinned provider changes against preserved public/caller boundaries.

This checks custody and declared composition, not a generic Rust refinement proof.
The accompanying source review supplies the mathematical preservation argument.
"""
import hashlib
import re


def closing_brace(text, opening):
    depth = 0
    for pos in range(opening, len(text)):
        if text[pos] == "{":
            depth += 1
        elif text[pos] == "}":
            depth -= 1
            if depth == 0:
                return pos + 1
    raise ValueError("Unclosed reviewed declaration")


def public_api(text):
    """Exact public signatures with impl owner, and complete type/constant bodies.

    The reviewed source uses balanced brace pairs in its format literals. This
    small inventory is not a general Rust parser or an expansion/type checker.
    """
    production = text.split("#[cfg(test)]", 1)[0]
    owners = []
    for item in re.finditer(r"(?m)^impl\b", production):
        brace = production.index("{", item.start())
        owners.append((item.start(), closing_brace(production, brace), production[item.start():brace].strip()))
    functions = []
    for item in re.finditer(r"(?m)^[ \t]*pub fn\s+\w+", production):
        brace = production.index("{", item.start())
        owner = next((header for start, end, header in owners if start < item.start() < end), "module")
        functions.append({"owner": owner, "signature": production[item.start():brace].strip()})
    types = []
    for item in re.finditer(r"(?m)^pub (?:struct|enum)\s+\w+", production):
        brace = production.index("{", item.start())
        types.append(production[item.start():closing_brace(production, brace)])
    constants = []
    for item in re.finditer(r"(?m)^pub const\s+\w+", production):
        end = production.index(";", item.start()) + 1
        constants.append(production[item.start():end])
    return {"functions": functions, "types": types, "constants": constants}


def verify_provider_context(reference, artifact, root, load, sha, verify_run, verify_dependencies):
    bridge = load(reference)
    if bridge.get("AuthorityEffect") != "None" or not bridge.get("providers"):
        raise ValueError("Provider context scope is missing")
    canonical = load(bridge["canonical"])
    flags = ("baseline_ok", "source_unchanged", "dependencies_unchanged", "copied_sources_unchanged", "build_outputs_removed")
    if not all(canonical.get(key) for key in flags):
        raise ValueError("Provider composition did not pass")
    sources = load(bridge["canonical_sources"])
    for path, value in sources.items():
        if sha(root / path) != value:
            raise ValueError("Provider composition source drift")
    copies = load(bridge["canonical_copies"])
    if any(sha(root / path) != value for path, value in copies.items()):
        raise ValueError("Provider composition copy drift")
    dependencies = load(bridge["canonical_dependencies"])
    if not dependencies:
        raise ValueError("Provider composition dependencies missing")
    verify_dependencies((root / bridge["canonical"]["path"]).parent, {
        "dependencies_unchanged": True,
        "dependency_receipt_sha256": bridge["canonical_dependencies"]["sha256"]})
    verify_run(canonical["build"], successful=True)
    runs = canonical["runs"]
    if len(runs) != 2 or len(bridge["canonical_tests"]) != 2:
        raise ValueError("Both provider crate roots are required")
    for run, expected in zip(runs, bridge["canonical_tests"]):
        text = verify_run(run, successful=True)
        found = re.search(r"test result: ok\. ([1-9][0-9]*) passed; 0 failed;", text)
        if found is None or int(found[1]) != expected:
            raise ValueError("Provider composition test declaration mismatch")
    for provider in bridge["providers"]:
        texts = []
        for key in ("previous", "current"):
            item = provider[key]
            if sha(root / item["path"]) != item["sha256"]:
                raise ValueError("Provider boundary source drift")
            texts.append((root / item["path"]).read_text(encoding="utf-8"))
        if any(public_api(text) != provider["public_api"] for text in texts):
            raise ValueError("Provider public boundary changed")
        marker = "#[cfg(test)]"
        tests = [text[text.index(marker):] for text in texts]
        if not provider["tests_unchanged"] or tests[0] != tests[1]:
            raise ValueError("Provider original tests changed")
        if hashlib.sha256(tests[1].encode()).hexdigest() != provider["normalized_tests_sha256"]:
            raise ValueError("Provider test declaration mismatch")
        current = provider["current"]
        if sources.get(current["path"]) != current["sha256"]:
            raise ValueError("Provider was not in the current canonical composition")
        review = load(provider["source_review"])
        if (review["artifact"]["path"] != current["path"]
                or review["artifact"]["sha256"] != current["sha256"]
                or review.get("status") != "complete_source_review"
                or review.get("open_findings") or not provider.get("semantic_preservation_argument")):
            raise ValueError("Provider lacks its exact semantic source review")
    consumers = bridge["consumers"]
    for consumer in consumers:
        previous, current = consumer["previous"], consumer["current"]
        if previous["sha256"] != current["sha256"]:
            raise ValueError("Consumer source is not unchanged")
        if any(sha(root / item["path"]) != item["sha256"] for item in (previous, current)):
            raise ValueError("Consumer source drift")
        if sources.get(current["path"]) != current["sha256"]:
            raise ValueError("Consumer was not compiled in the current composition")
    expected = {"path": artifact["path"], "sha256": artifact["sha256"]}
    if expected not in [item["current"] for item in consumers]:
        raise ValueError("This assessment is not covered by the provider bridge")
