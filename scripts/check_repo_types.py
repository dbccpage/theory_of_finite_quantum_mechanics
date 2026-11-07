#!/usr/bin/env python3
"""Check the tracked tree against the repository types in governance/types.

Every tracked file must be an instance of exactly one member of exactly one class (block `meta` of
governance/types/repository.type.yaml says how files are owned and matched). This script applies that
meta-schema to `git ls-files` and prints, per class, the files it owns and, per member, the matched count
beside the recorded `now` and `target`, followed by the findings:

    UNTYPED  a tracked file that no member of its owning class matches
    DEAD     a member that matches no file, or a leaf type that types no file
    MISSING  a required attribute with no instance
    UNKNOWN  a member, attribute or relation naming a leaf type or class no type file defines
    CLAIM    two classes claiming one folder, or one class or leaf name defined twice
    FORM     a field missing or outside the grammar of block `meta`

Options:
    --strict                 exit 1 on any of the six findings
    --report naming          files and folders whose names break their naming rule
    --report public-text     files that hit the public_text rule (paths and categories only)
    --report duplicates      groups of tracked files sharing one blob that no relation or allow entry declares
    --report library         paths of library.yaml that do not exist
    --plan Snn               the files the epic's appendix removes, keeps or moves in story Snn
    --summary FILE           append a Markdown summary (for the CI step summary)

AuthorityEffect: None. This script changes nothing and is not evidence for any claim.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TYPES_DIR = "governance/types"
ROOT_TYPE_FILE = "repository.type.yaml"
EPIC_FILE = "repository_typing_epic.md"
FINDING_KINDS = ("UNTYPED", "DEAD", "MISSING", "UNKNOWN", "CLAIM", "FORM")
ROLES = ("source", "proof", "check", "evidence", "record", "document", "tooling", "config", "vendored", "generated")
COMPANIONS = ("none", "policy", "review_ledger", "convention")
RELATION_KINDS = ("cites", "imports", "builds", "checks", "generates", "renders", "consumes", "derives_from")
UNIVERSAL_FILE_RULES = ("readme", "toolchain", "deposit_boilerplate")
FOLDER_RULES = ("lower", "lean_namespace_folder", "dag_id", "utc_stamp")
REPORTED_RULES = ("imported", "exception")
ARCHIVE_FOLDER = re.compile(r"^(archive|archives|old|legacy|superseded|backup|source_archive|retired.*)$")
STORY_ID = re.compile(r"^S\d\d$")


# ---------------------------------------------------------------------------------------------------------------
# glob grammar of block meta
# ---------------------------------------------------------------------------------------------------------------

def _expand_braces(pattern: str) -> list[str]:
    m = re.search(r"\{([^{}]*)\}", pattern)
    if not m:
        return [pattern]
    out = []
    for choice in m.group(1).split(","):
        out.extend(_expand_braces(pattern[: m.start()] + choice + pattern[m.end():]))
    return out


_GLOB_CACHE: dict[str, re.Pattern[str]] = {}


def glob_regex(pattern: str) -> re.Pattern[str]:
    """Compile one meta glob: `*`, `?`, `[...]`, `**` as a whole segment, `{a,b}`; case-sensitive."""
    cached = _GLOB_CACHE.get(pattern)
    if cached is not None:
        return cached
    alternatives = []
    for alt in _expand_braces(pattern):
        segments = alt.split("/")
        parts = []
        for index, segment in enumerate(segments):
            last = index == len(segments) - 1
            if segment == "**":
                parts.append(".*" if last else "(?:[^/]+/)*")
                continue
            regex = ""
            j = 0
            while j < len(segment):
                ch = segment[j]
                if ch == "*":
                    regex += "[^/]*"
                elif ch == "?":
                    regex += "[^/]"
                elif ch == "[":
                    k = segment.find("]", j + 1)
                    if k < 0:
                        regex += re.escape(ch)
                    else:
                        regex += "[" + segment[j + 1 : k].replace("\\", "\\\\") + "]"
                        j = k
                else:
                    regex += re.escape(ch)
                j += 1
            parts.append(regex + ("" if last else "/"))
        alternatives.append("".join(parts))
    compiled = re.compile("^(?:" + "|".join(alternatives) + ")$")
    _GLOB_CACHE[pattern] = compiled
    return compiled


def is_glob(pattern: str) -> bool:
    return bool(re.search(r"[*?\[{]", pattern))


# ---------------------------------------------------------------------------------------------------------------
# loading
# ---------------------------------------------------------------------------------------------------------------

class Types:
    """The parsed type files: classes, leaf types, the root blocks and the FORM, UNKNOWN and CLAIM findings."""

    def __init__(self, types_dir: Path):
        self.dir = types_dir
        self.docs: dict[str, dict] = {}
        self.classes: dict[str, tuple[str, dict]] = {}
        self.leaves: dict[str, tuple[str, dict]] = {}
        self.findings: dict[str, list[str]] = {k: [] for k in FINDING_KINDS}
        for name in sorted(os.listdir(types_dir)):
            if not name.endswith(".type.yaml"):
                continue
            with open(types_dir / name, encoding="utf-8") as handle:
                doc = yaml.safe_load(handle) or {}
            self.docs[name] = doc
            for cls in doc.get("classes") or []:
                cname = cls.get("class")
                if cname in self.classes:
                    self.findings["CLAIM"].append(f"class {cname} defined in {self.classes[cname][0]} and {name}")
                    continue
                self.classes[cname] = (name, cls)
            for leaf in doc.get("leaf_types") or []:
                lname = leaf.get("name")
                if lname in self.leaves:
                    self.findings["CLAIM"].append(f"leaf {lname} defined in {self.leaves[lname][0]} and {name}")
                    continue
                self.leaves[lname] = (name, leaf)
        self.root = self.docs.get(ROOT_TYPE_FILE) or {}
        self.naming_rules = dict(self.root.get("naming_rules") or {})
        self.public_text = dict(self.root.get("public_text") or {})
        self._check_form()

    # -- grammar ------------------------------------------------------------------------------------------------
    def form(self, message: str) -> None:
        self.findings["FORM"].append(message)

    def _check_form(self) -> None:
        if ROOT_TYPE_FILE not in self.docs:
            self.form(f"{ROOT_TYPE_FILE} is missing")
        for name, doc in self.docs.items():
            if doc.get("schema") != "repo-type/1":
                self.form(f"{name}: schema must be repo-type/1")
            if "file_for" not in doc:
                self.form(f"{name}: file_for missing")
            elif name != ROOT_TYPE_FILE and doc["file_for"] != name[: -len(".type.yaml")]:
                self.form(f"{name}: file_for {doc['file_for']!r} does not name the file")
            for key in doc:
                if key not in ("schema", "file_for", "classes", "leaf_types", "meta", "sources_of_truth", "naming_rules", "public_text"):
                    self.form(f"{name}: unknown top-level field {key}")
        for rule, spec in self.naming_rules.items():
            if not isinstance(spec, dict) or not ("pattern" in spec or "paths" in spec):
                self.form(f"naming rule {rule}: needs pattern or paths")
        roots_seen = 0
        for cname, (fname, cls) in self.classes.items():
            where = f"{fname} class {cname}"
            keys = [k for k in ("path", "paths", "path_glob") if k in cls]
            if len(keys) != 1:
                self.form(f"{where}: exactly one of path, paths, path_glob")
            if cls.get("path") == ".":
                roots_seen += 1
            for field in ("summary", "role", "counts"):
                if field not in cls:
                    self.form(f"{where}: {field} missing")
            if cls.get("role") not in ROLES:
                self.form(f"{where}: role {cls.get('role')!r} outside roles")
            counts = cls.get("counts") or {}
            if not (isinstance(counts, dict) and isinstance(counts.get("now"), int) and isinstance(counts.get("target"), int)):
                self.form(f"{where}: counts needs integer now and target")
            if "totals" in cls and cls.get("path") != ".":
                self.form(f"{where}: totals is for the root class only")
            for key in cls:
                if key not in ("class", "path", "paths", "path_glob", "summary", "role", "counts", "attributes", "collections", "invariants", "relations", "totals", "allow"):
                    self.form(f"{where}: unknown field {key}")
            names_seen: set[str] = set()
            for group in ("attributes", "collections"):
                for member in cls.get(group) or []:
                    mname = member.get("name")
                    mwhere = f"{where}.{mname}"
                    if not mname:
                        self.form(f"{where}: a member without name in {group}")
                    elif mname in names_seen:
                        self.form(f"{mwhere}: name used twice")
                    names_seen.add(mname)
                    for key in member:
                        if key not in ("name", "match", "leaf", "now", "target", "authored", "required", "catch_all", "note", "class"):
                            self.form(f"{mwhere}: unknown field {key}")
                    if "class" in member:
                        if group != "attributes":
                            self.form(f"{mwhere}: a class attribute belongs in attributes")
                        if any(k in member for k in ("match", "path", "paths", "path_glob", "leaf")):
                            self.form(f"{mwhere}: a class attribute carries no match, path or leaf")
                        if member["class"] not in self.classes:
                            self.findings["UNKNOWN"].append(f"{mwhere}: class {member['class']}")
                        continue
                    if "match" not in member:
                        self.form(f"{mwhere}: match missing")
                    if member.get("leaf") not in self.leaves:
                        self.findings["UNKNOWN"].append(f"{mwhere}: leaf {member.get('leaf')}")
                    for key in ("now", "target"):
                        if not isinstance(member.get(key), int):
                            self.form(f"{mwhere}: {key} missing or not an integer")
                    if "required" in member and group != "attributes":
                        self.form(f"{mwhere}: required is for attributes only")
                    authored = member.get("authored", "hand")
                    if not re.match(r"^(hand\b|generated:|imported:)", str(authored)):
                        self.form(f"{mwhere}: authored {authored!r} outside the grammar")
                    leaf = self.leaves.get(member.get("leaf"), (None, {}))[1]
                    is_catch_all = member.get("match") == "**" or leaf.get("format") == "any"
                    if is_catch_all and not (member.get("catch_all") is True and str(authored).startswith("imported:")):
                        self.form(f"{mwhere}: a catch-all needs catch_all: true and authored imported:")
                    if member.get("catch_all") and not is_catch_all:
                        self.form(f"{mwhere}: catch_all on a member that is no catch-all")
            for relation in cls.get("relations") or []:
                if relation.get("kind") not in RELATION_KINDS:
                    self.form(f"{where}: relation kind {relation.get('kind')!r} outside relation_kinds")
                if relation.get("to") not in self.classes:
                    self.findings["UNKNOWN"].append(f"{where}: relation to class {relation.get('to')}")
            for inv in cls.get("invariants") or []:
                for field in ("id", "statement", "holds_now", "checked_by"):
                    if field not in inv:
                        self.form(f"{where}: invariant {inv.get('id')} lacks {field}")
                if inv.get("holds_now") not in (True, False, "unknown"):
                    self.form(f"{where}: invariant {inv.get('id')} holds_now {inv.get('holds_now')!r}")
            for entry in cls.get("allow") or []:
                if not (isinstance(entry, dict) and "match" in entry and "reason" in entry):
                    self.form(f"{where}: allow entries need match and reason")
        if roots_seen != 1:
            self.form(f"exactly one class must have path '.', found {roots_seen}")
        for lname, (fname, leaf) in self.leaves.items():
            where = f"{fname} leaf {lname}"
            for field in ("format", "naming", "schema", "companions", "authored"):
                if field not in leaf:
                    self.form(f"{where}: {field} missing")
            for rule in str(leaf.get("naming", "")).split(" or "):
                if rule not in self.naming_rules:
                    self.form(f"{where}: naming rule {rule!r} is not defined")
            if leaf.get("companions") not in COMPANIONS:
                self.form(f"{where}: companions {leaf.get('companions')!r} outside the grammar")
            if not re.match(r"^(hand\b|generated:|imported:)", str(leaf.get("authored", ""))):
                self.form(f"{where}: authored {leaf.get('authored')!r} outside the grammar")

    # -- helpers ------------------------------------------------------------------------------------------------
    def members(self, cls: dict) -> list[dict]:
        attrs = [m for m in (cls.get("attributes") or []) if "match" in m]
        return attrs + list(cls.get("collections") or [])

    def rule_regex(self, rule: str) -> re.Pattern[str] | None:
        spec = self.naming_rules.get(rule) or {}
        pattern = spec.get("pattern")
        return re.compile(pattern) if pattern else None


# ---------------------------------------------------------------------------------------------------------------
# the tree
# ---------------------------------------------------------------------------------------------------------------

def git_tracked(repo_root: Path) -> dict[str, str]:
    """Tracked files from the index: path -> blob id."""
    out = subprocess.run(["git", "-C", str(repo_root), "ls-files", "-s", "-z"], capture_output=True, check=True).stdout
    tree: dict[str, str] = {}
    for record in out.decode("utf-8").split("\0"):
        if not record:
            continue
        meta, path = record.split("\t", 1)
        mode, blob, _stage = meta.split()
        if mode == "160000":
            continue
        tree[path] = blob
    return tree


def top_folder(path: str) -> str | None:
    return path.split("/", 1)[0] if "/" in path else None


# ---------------------------------------------------------------------------------------------------------------
# evaluation
# ---------------------------------------------------------------------------------------------------------------

class Result:
    def __init__(self) -> None:
        self.owned: dict[str, list[tuple[str, str]]] = collections.defaultdict(list)
        self.match: dict[str, tuple[str, str, str]] = {}
        self.member_counts: collections.Counter = collections.Counter()
        self.findings: dict[str, list[str]] = {k: [] for k in FINDING_KINDS}
        self.claimed: dict[str, str] = {}
        self.unclaimed_top: list[str] = []


def evaluate(types: Types, files: list[str]) -> Result:
    result = Result()
    for kind in FINDING_KINDS:
        result.findings[kind].extend(types.findings[kind])
    roots: list[tuple[str, str]] = []
    claimed: dict[str, str] = {}
    root_class = None
    for cname, (_fname, cls) in types.classes.items():
        if cls.get("path") == ".":
            root_class = cname
            continue
        for folder in ([cls["path"]] if "path" in cls else []) + list(cls.get("paths") or []):
            folder = folder.rstrip("/")
            if folder in claimed:
                result.findings["CLAIM"].append(f"folder {folder} claimed by {claimed[folder]} and {cname}")
                continue
            claimed[folder] = cname
            roots.append((folder, cname))
    tops = sorted({top_folder(f) for f in files if top_folder(f)})
    for cname, (_fname, cls) in types.classes.items():
        if "path_glob" in cls:
            regex = glob_regex(cls["path_glob"])
            for top in tops:
                if regex.match(top) and top not in claimed:
                    claimed[top] = cname
                    roots.append((top, cname))
    result.claimed = claimed
    if root_class is None:
        result.findings["FORM"].append("no root class (path '.')")
        return result
    roots.sort(key=lambda item: -item[0].count("/"))
    for path in files:
        owner, rel = root_class, path
        for folder, cname in roots:
            if path.startswith(folder + "/"):
                owner, rel = cname, path[len(folder) + 1 :]
                break
        result.owned[owner].append((path, rel))
    result.unclaimed_top = [t for t in tops if t not in claimed]
    for cname, (_fname, cls) in types.classes.items():
        members = types.members(cls)
        compiled = [(m, glob_regex(str(m.get("match", "")))) for m in members]
        for path, rel in result.owned.get(cname, []):
            for member, regex in compiled:
                if regex.match(rel):
                    result.match[path] = (cname, member["name"], member.get("leaf"))
                    result.member_counts[(cname, member["name"])] += 1
                    break
            else:
                result.findings["UNTYPED"].append(path)
    leaf_use = collections.Counter(leaf for _c, _m, leaf in result.match.values())
    for cname, (_fname, cls) in types.classes.items():
        for member in types.members(cls):
            if result.member_counts[(cname, member["name"])] == 0:
                result.findings["DEAD"].append(f"member {cname}.{member['name']}")
        for attr in cls.get("attributes") or []:
            if not attr.get("required"):
                continue
            if "match" in attr and result.member_counts[(cname, attr["name"])] == 0:
                result.findings["MISSING"].append(f"{cname}.{attr['name']}")
            if "class" in attr and not result.owned.get(attr["class"]):
                result.findings["MISSING"].append(f"{cname}.{attr['name']}")
    for lname in types.leaves:
        if leaf_use[lname] == 0:
            result.findings["DEAD"].append(f"leaf {lname}")
    return result


# ---------------------------------------------------------------------------------------------------------------
# reports
# ---------------------------------------------------------------------------------------------------------------

def naming_report(types: Types, files: list[str], result: Result) -> list[tuple[str, str, str]]:
    """(category, path, detail): category is violation, imported, exception, folder or archive."""
    universal = [types.rule_regex(r) for r in UNIVERSAL_FILE_RULES]
    exception_paths = set((types.naming_rules.get("exception") or {}).get("paths") or [])
    rows: list[tuple[str, str, str]] = []
    imported_files: set[str] = set()
    for path in files:
        base = path.rsplit("/", 1)[-1]
        typed = result.match.get(path)
        leaf = types.leaves.get(typed[2], (None, {}))[1] if typed else {}
        rules = str(leaf.get("naming", "lower")).split(" or ")
        if any(r in rules for r in ("imported",)):
            imported_files.add(path)
        enforced = [types.rule_regex(r) for r in rules if r not in REPORTED_RULES]
        if any(rx and rx.match(base) for rx in enforced + universal):
            continue
        if path in exception_paths:
            rows.append(("exception", path, "listed by naming rule exception"))
        elif "imported" in rules:
            rows.append(("imported", path, f"leaf {typed[2]} (imported bytes)"))
        else:
            rows.append(("violation", path, f"leaf {typed[2] if typed else '-'} allows {' or '.join(rules)}"))
    folder_rules = [types.rule_regex(r) for r in FOLDER_RULES]
    folders: dict[str, list[str]] = collections.defaultdict(list)
    for path in files:
        parts = path.split("/")
        for index in range(len(parts) - 1):
            folders["/".join(parts[: index + 1])].append(path)
    for folder in sorted(folders):
        segment = folder.rsplit("/", 1)[-1]
        if ARCHIVE_FOLDER.match(segment):
            rows.append(("archive", folder + "/", f"{len(folders[folder])} files"))
        if any(rx and rx.match(segment) for rx in folder_rules):
            continue
        if all(p in imported_files for p in folders[folder]):
            rows.append(("imported", folder + "/", "folder of imported bytes"))
        else:
            rows.append(("folder", folder + "/", "folder name outside lower, lean_namespace_folder, dag_id and utc_stamp"))
    return rows


_CAMEL = re.compile(rb"(?<=[a-z0-9])(?=[A-Z])")
_WORDS = re.compile(rb"[A-Za-z]+")


class PublicText:
    """The public_text rule: hashed words and word pairs after the stated normalisation."""

    def __init__(self, block: dict):
        self.want: dict[str, str] = {}
        for category, hashes in (block.get("term_sha256") or {}).items():
            for digest in hashes or []:
                self.want[str(digest)] = category
        self.allow = [(glob_regex(e["match"]), e.get("reason", "")) for e in (block.get("allow") or []) if isinstance(e, dict) and "match" in e]
        self._cache: dict[bytes, str] = {}

    def _hit(self, token: bytes) -> str:
        found = self._cache.get(token)
        if found is None:
            found = self.want.get(hashlib.sha256(token).hexdigest(), "")
            if not found and token.endswith(b"s"):
                found = self.want.get(hashlib.sha256(token[:-1]).hexdigest(), "")
            self._cache[token] = found
        return found

    @staticmethod
    def normalise(data: bytes) -> list[bytes]:
        return [w.lower() for w in _WORDS.findall(_CAMEL.sub(b" ", data))]

    def scan(self, data: bytes) -> set[str]:
        categories: set[str] = set()
        previous = None
        for word in self.normalise(data):
            category = self._hit(word)
            if category:
                categories.add(category)
            if previous is not None:
                category = self._hit(previous + b" " + word)
                if category:
                    categories.add(category)
            previous = word
        return categories

    def scan_file(self, repo_root: Path, path: str) -> tuple[set[str], bool]:
        """Categories hit by the path and the content; the flag says whether the path itself hits."""
        path_hits = self.scan(path.encode("utf-8"))
        categories = set(path_hits)
        try:
            with open(repo_root / path, "rb") as handle:
                data = handle.read()
        except OSError:
            return categories, bool(path_hits)
        if b"\0" not in data[:8000]:
            categories |= self.scan(data)
        return categories, bool(path_hits)

    def allowed(self, path: str) -> str | None:
        for regex, reason in self.allow:
            if regex.match(path):
                return reason
        return None


def public_text_report(types: Types, repo_root: Path, files: list[str]) -> tuple[list[tuple[str, str, bool]], list[str]]:
    rule = PublicText(types.public_text)
    hits: list[tuple[str, str, bool]] = []
    allowed: list[str] = []
    for path in files:
        categories, by_path = rule.scan_file(repo_root, path)
        if not categories:
            continue
        if rule.allowed(path) is not None:
            allowed.append(path)
            continue
        hits.append((path, ",".join(sorted(categories)), by_path))
    return hits, allowed


def duplicates_report(types: Types, tree: dict[str, str], result: Result) -> list[list[str]]:
    """Blob groups of two or more files that no derives_from relation or allow entry declares."""
    derives: set[tuple[str, str]] = set()
    allow: dict[str, list[re.Pattern[str]]] = {}
    for cname, (_fname, cls) in types.classes.items():
        for relation in cls.get("relations") or []:
            if relation.get("kind") == "derives_from":
                derives.add((cname, relation.get("to")))
        allow[cname] = [glob_regex(e["match"]) for e in (cls.get("allow") or []) if isinstance(e, dict) and "match" in e]
    groups: dict[str, list[str]] = collections.defaultdict(list)
    for path, blob in tree.items():
        groups[blob].append(path)
    undeclared: list[list[str]] = []
    for blob, paths in groups.items():
        if len(paths) < 2:
            continue
        paths.sort()
        owners = [result.match.get(p, (None, None, None))[0] for p in paths]
        declared = True
        for index, path in enumerate(paths):
            owner = owners[index]
            rel = path
            if owner and owner in types.classes:
                cls = types.classes[owner][1]
                for folder in ([cls["path"]] if "path" in cls and cls["path"] != "." else []) + list(cls.get("paths") or []):
                    if path.startswith(folder.rstrip("/") + "/"):
                        rel = path[len(folder.rstrip("/")) + 1 :]
                        break
            if owner and any(rx.match(rel) for rx in allow.get(owner, [])):
                continue
            if owner and any((owner, other) in derives or (other, owner) in derives for other in owners if other != owner):
                continue
            declared = False
            break
        if not declared:
            undeclared.append(paths)
    undeclared.sort()
    return undeclared


def library_report(repo_root: Path, files: list[str]) -> list[str]:
    """Paths and entry points of library.yaml that no tracked file or folder provides."""
    catalog = repo_root / "library.yaml"
    if not catalog.exists():
        return ["library.yaml"]
    with open(catalog, encoding="utf-8") as handle:
        doc = yaml.safe_load(handle) or {}
    tracked = set(files)
    folders = {"/".join(f.split("/")[:i]) for f in files for i in range(1, f.count("/") + 1)}
    missing: list[str] = []
    for shelf in doc.get("shelves") or []:
        for book in shelf.get("books") or []:
            for key in ("path",):
                value = book.get(key)
                if value and value not in tracked and value.rstrip("/") not in folders:
                    missing.append(f"{shelf.get('key')}/{book.get('key')}: {key} {value}")
            for entry in book.get("entry_points") or []:
                if entry not in tracked and entry.rstrip("/") not in folders:
                    missing.append(f"{shelf.get('key')}/{book.get('key')}: entry point {entry}")
    return missing


# ---------------------------------------------------------------------------------------------------------------
# the epic's appendix (--plan)
# ---------------------------------------------------------------------------------------------------------------

class Plan:
    def __init__(self, epic_text: str):
        self.removes: list[tuple[str, str, int]] = []
        self.keeps: set[str] = set()
        self.moves: list[tuple[str, str, str]] = []
        self.unparsed: list[str] = []
        blocks = re.findall(r"```text\n(.*?)```", epic_text, re.S)
        for block in blocks:
            for line in block.splitlines():
                if not line.strip():
                    continue
                m = re.match(r"^(S\d\d)\s+(.+?)\s+->\s+(\S+)\s*$", line)
                if m:
                    self.moves.append(m.groups())
                    continue
                m = re.match(r"^KEEP\s+(\S+)\s*$", line)
                if m:
                    self.keeps.add(m.group(1))
                    continue
                m = re.match(r"^(S\d\d)\s+(\S+)(?:\s+\((\d+) files?\))?\s*$", line)
                if m:
                    self.removes.append((m.group(1), m.group(2), int(m.group(3)) if m.group(3) else 1))
                    continue
                self.unparsed.append(line)

    @staticmethod
    def resolve_source(source: str, tree: dict[str, str]) -> str | None:
        m = re.search(r"blob ([0-9a-f]{6,})", source)
        if not m:
            return source
        hits = [path for path, blob in tree.items() if blob.startswith(m.group(1))]
        return hits[0] if len(hits) == 1 else None

    @staticmethod
    def matches(pattern: str, tree: dict[str, str]) -> set[str]:
        if pattern.endswith("/"):
            return {f for f in tree if f.startswith(pattern)}
        if is_glob(pattern):
            regex = glob_regex(pattern)
            return {f for f in tree if regex.match(f)}
        return {pattern} & set(tree)

    def story(self, story: str, tree: dict[str, str]) -> tuple[list[str], list[str], list[tuple[str, str]], list[str]]:
        """(removed files, lines, moved pairs, problems) for one story against the tree."""
        removed: list[str] = []
        lines: list[str] = []
        problems: list[str] = []
        for st, pattern, count in self.removes:
            if st != story:
                continue
            hit = self.matches(pattern, tree) - self.keeps
            lines.append(f"remove  {pattern}  ({len(hit)} files, appendix says {count})")
            if len(hit) != count:
                problems.append(f"{pattern}: appendix says {count} files, the tree has {len(hit)}")
            removed.extend(sorted(hit))
        moved: list[tuple[str, str]] = []
        for st, source, dest in self.moves:
            if st != story:
                continue
            resolved = self.resolve_source(source, tree)
            if resolved is None:
                problems.append(f"move source {source!r} does not resolve to one tracked file")
                continue
            if resolved.endswith("/"):
                pairs = [(f, dest + f[len(resolved) :]) for f in sorted(tree) if f.startswith(resolved) and f not in removed]
            else:
                pairs = [(resolved, dest)] if resolved in tree else []
            if not pairs:
                problems.append(f"move source {resolved} matches no tracked file")
            lines.append(f"move    {resolved} -> {dest}  ({len(pairs)} files)")
            moved.extend(pairs)
        return removed, lines, moved, problems


# ---------------------------------------------------------------------------------------------------------------
# output
# ---------------------------------------------------------------------------------------------------------------

def class_lines(types: Types, result: Result) -> list[str]:
    lines: list[str] = []
    for cname, (fname, cls) in types.classes.items():
        where = cls.get("path") or cls.get("path_glob") or ", ".join(cls.get("paths") or [])
        counts = cls.get("counts") or {}
        owned = len(result.owned.get(cname, []))
        lines.append(f"{cname} ({where}): owns {owned} files  now={counts.get('now')} target={counts.get('target')}  [{fname}]")
        for member in types.members(cls):
            got = result.member_counts[(cname, member["name"])]
            flag = "" if got == member.get("target") else "  *"
            lines.append(f"    {member['name']:<32} matched={got:<6} now={member.get('now'):<6} target={member.get('target'):<6} leaf={member.get('leaf')}{flag}")
    return lines


def finding_lines(result: Result) -> list[str]:
    lines = []
    for kind in FINDING_KINDS:
        items = result.findings[kind]
        lines.append(f"{kind} {len(items)}")
        lines.extend(f"    {item}" for item in items)
    return lines


def summary_markdown(types: Types, result: Result, files: list[str]) -> str:
    out = ["## Repository types", "", f"Tracked files: {len(files)}", "", "| Finding | Count |", "|---|---:|"]
    for kind in FINDING_KINDS:
        out.append(f"| {kind} | {len(result.findings[kind])} |")
    out += ["", "| Class | Owns | now | target |", "|---|---:|---:|---:|"]
    for cname, (_fname, cls) in types.classes.items():
        counts = cls.get("counts") or {}
        out.append(f"| {cname} | {len(result.owned.get(cname, []))} | {counts.get('now')} | {counts.get('target')} |")
    examples = result.findings["UNTYPED"][:40]
    if examples:
        out += ["", "<details><summary>UNTYPED examples</summary>", ""]
        out += [f"- `{p}`" for p in examples]
        out += ["", "</details>"]
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--repo-root", default=str(ROOT))
    parser.add_argument("--strict", action="store_true", help="exit 1 on any UNTYPED, DEAD, MISSING, UNKNOWN, CLAIM or FORM finding")
    parser.add_argument("--report", choices=["naming", "public-text", "duplicates", "library"])
    parser.add_argument("--plan", metavar="Snn", help="list the files the epic's appendix removes, keeps or moves in one story")
    parser.add_argument("--summary", metavar="FILE", help="append a Markdown summary to FILE")
    args = parser.parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    types = Types(repo_root / TYPES_DIR)
    tree = git_tracked(repo_root)
    files = sorted(tree)

    if args.plan:
        if not STORY_ID.match(args.plan):
            print(f"--plan expects a story id like S05, got {args.plan!r}")
            return 2
        with open(repo_root / TYPES_DIR / EPIC_FILE, encoding="utf-8") as handle:
            plan = Plan(handle.read())
        for line in plan.unparsed:
            print(f"appendix line not parsed: {line!r}")
        removed, lines, moved, problems = plan.story(args.plan, tree)
        for line in lines:
            print(line)
        for path in removed:
            print(f"  - {path}")
        for source, dest in moved:
            print(f"  > {source} -> {dest}")
        kept = sorted(k for k in plan.keeps if any(k in plan.matches(p, tree) for st, p, _n in plan.removes if st == args.plan))
        for path in kept:
            print(f"  = KEEP {path}")
        print(f"{args.plan}: {len(removed)} files removed, {len(moved)} files moved, {len(kept)} kept by KEEP lines")
        for problem in problems:
            print(f"COUNT {problem}")
        return 1 if problems or plan.unparsed else 0

    result = evaluate(types, files)

    if args.report == "naming":
        rows = naming_report(types, files, result)
        counts = collections.Counter(category for category, _p, _d in rows)
        for category, path, detail in rows:
            print(f"{category:<10} {path}  ({detail})")
        print("naming: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) if rows else "naming: every name satisfies its rule")
        return 0
    if args.report == "public-text":
        hits, allowed = public_text_report(types, repo_root, files)
        by_category: collections.Counter = collections.Counter()
        by_path = 0
        for path, categories, path_hit in hits:
            print(f"{path}  [{categories}]{'  (path)' if path_hit else ''}")
            for category in categories.split(","):
                by_category[category] += 1
            by_path += path_hit
        print(f"public-text: {len(hits)} of {len(files)} files hit ({', '.join(f'{k} {v}' for k, v in sorted(by_category.items()))}; {by_path} by path); {len(allowed)} allowed")
        return 0
    if args.report == "duplicates":
        groups = duplicates_report(types, tree, result)
        for group in groups:
            print(f"{len(group)} files share one blob:")
            for path in group:
                print(f"    {path}")
        print(f"duplicates: {len(groups)} undeclared blob groups, {sum(len(g) for g in groups)} files")
        return 0
    if args.report == "library":
        missing = library_report(repo_root, files)
        for item in missing:
            print(f"missing  {item}")
        print(f"library: {len(missing)} paths of library.yaml do not exist")
        return 0

    for line in class_lines(types, result):
        print(line)
    if result.unclaimed_top:
        print("top-level folders no class claims: " + ", ".join(result.unclaimed_top))
    for line in finding_lines(result):
        print(line)
    total = sum(len(v) for v in result.findings.values())
    print(f"check_repo_types: {len(files)} tracked files, {total} findings (" + ", ".join(f"{k} {len(result.findings[k])}" for k in FINDING_KINDS) + ")")
    if args.summary:
        with open(args.summary, "a", encoding="utf-8") as handle:
            handle.write(summary_markdown(types, result, files))
    return 1 if args.strict and total else 0


if __name__ == "__main__":
    sys.exit(main())
