"""Fresh, offline Lean compatibility audit. Default checks; --write explicit only."""

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERMITTED = {"propext", "Quot.sound"}


def code_only(text):
    """Erase strings and line/nested block comments, preserving line boundaries."""
    out, i, depth = [], 0, 0
    while i < len(text):
        if depth:
            if text.startswith("/-", i):
                depth += 1
                i += 2
            elif text.startswith("-/", i):
                depth -= 1
                i += 2
            else:
                out.append("\n" if text[i] == "\n" else " ")
                i += 1
        elif text.startswith("/-", i):
            depth = 1
            out.append(" ")
            i += 2
        elif text.startswith("--", i):
            end = text.find("\n", i)
            i = len(text) if end < 0 else end
        elif text[i] == '"':
            out.append(" ")
            i += 1
            while i < len(text):
                if text[i] == "\\":
                    i += 2
                elif text[i] == '"':
                    i += 1
                    break
                else:
                    out.append("\n" if text[i] == "\n" else " ")
                    i += 1
        else:
            out.append(text[i])
            i += 1
    if depth:
        raise ValueError("unclosed block comment")
    return "".join(out)


def declarations(text):
    stack, names = [], []
    for line in code_only(text).splitlines():
        match = re.match(r"\s*namespace\s+([\w.]+)", line)
        if match:
            stack.append(match[1])
        elif re.match(r"\s*end\b", line):
            if stack:
                stack.pop()
        match = re.match(
            r"\s*(?:@[\[\]\w ,]+\s*)?(?:private\s+|protected\s+)?(?:theorem|lemma)\s+(\w+)", line
        )
        if match:
            names.append(".".join((*stack, match[1])))
    return names


def scan(sources):
    expected = {}
    for group, files in sources.items():
        decls, audits = [], []
        for path, text in files.items():
            code = code_only(text)
            if re.search(r"\b(sorry|sorryAx|admit|axiom|unsafe|partial)\b", code):
                raise ValueError(f"forbidden escape in {path}")
            decls.extend(declarations(text))
            for name in re.findall(r"#print\s+axioms\s+([\w.]+)", code):
                candidates = [
                    decl for decl in declarations(text) if decl == name or decl.endswith("." + name)
                ]
                audits.append(candidates[0] if len(candidates) == 1 else name)
        if len(decls) != len(set(decls)) or sorted(decls) != sorted(audits):
            raise ValueError(f"incomplete or duplicate axiom audit: {group}")
        count = 9 if group == "education" else 5
        if len(decls) != count:
            raise ValueError(f"unexpected declaration count: {group}")
        expected[group] = sorted(decls)
    return expected


def reports(output):
    found = {}
    pattern = r"'([^']+)' (does not depend on any axioms|depends on axioms: \[([^\]]*)\])"
    for match in re.finditer(pattern, output):
        name = match[1]
        axioms = sorted(x.strip() for x in (match[3] or "").split(",") if x.strip())
        if name in found or not set(axioms) <= PERMITTED:
            raise ValueError(f"duplicate or forbidden axiom report: {name}")
        found[name] = axioms
    return found


def validate_receipt(receipt, hashes, expected):
    if receipt.get("schema") != 1 or receipt.get("sources") != hashes:
        raise ValueError("stale source hashes or receipt schema")
    if (
        receipt.get("verification_kind")
        != "fresh_compatibility_build_not_pinned_toolchain_verification"
    ):
        raise ValueError("missing compatibility qualification")
    actual = receipt.get("axiom_reports", {})
    names = sorted(n for group in expected.values() for n in group)
    if sorted(actual) != names or any(not set(a) <= PERMITTED for a in actual.values()):
        raise ValueError("missing report or forbidden axiom")
    commands = receipt.get("commands", [])
    if len(commands) != 21 or any(c.get("returncode") != 0 for c in commands):
        raise ValueError("missing or failed fresh compile")


def generate(lean_bin, root=ROOT):
    package = root.parent / "primitives" / "lean4"
    sources = {
        "education": {
            p.name: p.read_text(encoding="utf-8")
            for p in sorted(package.glob("*.lean"))
            if p.name != "lakefile.lean"
        },
        "choice": {
            "ChoiceAudit.lean": (root / "lean4/ChoiceAudit.lean").read_text(encoding="utf-8")
        },
    }
    expected = scan(sources)
    paths = list(sorted(package.glob("*.lean"))) + [
        package / "lean-toolchain",
        package / "lake-manifest.json",
        root / "lean4/ChoiceAudit.lean",
        Path(__file__),
    ]
    hashes = {
        p.relative_to(root.parent).as_posix()
        if p.is_relative_to(root.parent)
        else str(p): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in paths
    }
    lean_bin = Path(lean_bin).resolve(strict=True)
    version = subprocess.run(
        [str(lean_bin), "--version"], check=True, capture_output=True, text=True
    ).stdout.strip()
    commands, printed = [], {}
    with tempfile.TemporaryDirectory(prefix="genesis-lean-fresh-") as temporary:
        work = Path(temporary)
        for group in sources.values():
            for name, text in group.items():
                (work / name).write_text(text, encoding="utf-8")
        pending, built = dict(sources["education"]), set()
        order = []
        while pending:
            ready = [
                name
                for name, text in pending.items()
                if all(
                    imp + ".lean" not in pending
                    for imp in re.findall(r"^import\s+(\w+)", code_only(text), re.M)
                )
            ]
            if not ready:
                raise ValueError("local import cycle")
            for name in ready:
                order.append(name)
                built.add(name)
                del pending[name]
        order.append("ChoiceAudit.lean")
        environment = dict(os.environ, LEAN_PATH=str(work))
        for name in order:
            command = [str(lean_bin), "-o", name.removesuffix(".lean") + ".olean", name]
            run = subprocess.run(
                command, cwd=work, env=environment, capture_output=True, text=True, timeout=120
            )
            if run.returncode or "warning:" in run.stdout or "warning:" in run.stderr:
                raise ValueError(f"compile rejected {name}: {run.stdout}{run.stderr}")
            printed.update(reports(run.stdout + run.stderr))
            commands.append(
                {
                    "command": ["<explicit-lean-bin>", *command[1:]],
                    "returncode": run.returncode,
                    "stdout": run.stdout,
                    "stderr": run.stderr,
                }
            )
    receipt = {
        "schema": 1,
        "verification_kind": "fresh_compatibility_build_not_pinned_toolchain_verification",
        "declared_toolchain": (package / "lean-toolchain").read_text(encoding="utf-8").strip(),
        "actual_lean_version": version,
        "sources": hashes,
        "declarations": expected,
        "axiom_reports": printed,
        "commands": commands,
    }
    validate_receipt(receipt, hashes, expected)
    return receipt


def receipts_match(saved, fresh):
    """Compare fresh evidence while allowing the same Lean build on another host."""
    validate_receipt(saved, fresh["sources"], fresh["declarations"])
    normalized = []
    for receipt in (saved, fresh):
        value = dict(receipt)
        version = re.fullmatch(
            r"Lean \(version ([^,]+), [^,]+, commit ([0-9a-f]+), ([^)]+)\)",
            value["actual_lean_version"],
        )
        if version is None:
            return False
        value["actual_lean_version"] = version.groups()
        normalized.append(value)
    return json.dumps(normalized[0], sort_keys=True) == json.dumps(normalized[1], sort_keys=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean-bin", required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    receipt = generate(args.lean_bin)
    path = ROOT / "manifests/lean_receipt.json"
    if args.write:
        path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    else:
        saved = json.loads(path.read_text(encoding="utf-8"))
        if not receipts_match(saved, receipt):
            raise ValueError("receipt differs from fresh replay")
    print(
        "verified: 21 fresh compilations, 9 education + 5 choice theorem reports; compatibility only"
    )


if __name__ == "__main__":
    main()
