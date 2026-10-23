"""Origin: scripts/auto/obstruction_scan.py (adapted from the_symbol_game auto-obstruction-hunter/scripts/ast_cochain_obstruction_scanner.py; the networkx cochain complex is replaced by a standard-library import graph, and the OE-specific ten-level scanner is not ported)
Claim: finds three structural non-fits: an independent check that imports repository code or edits sys.path (O1), a cycle of module-level imports among repository Python files (O2), and a derived DAG route that requires an OPEN or REFUTED input (O3)
AuthorityEffect: None
Scope Fence: a finding is a place where two records do not fit; it does not say which record is wrong, it changes no status, and an empty scan does not show that the DAG or the code is coherent
Level: L4

Usage (from the repository root):
    python -I -X utf8 scripts/auto/obstruction_scan.py
    python -I -X utf8 scripts/auto/obstruction_scan.py --changed-since origin/main
    python -I -X utf8 scripts/auto/obstruction_scan.py --only O3
Exit status: 0 ok; 1 a finding at or above --fail-on (default HIGH); 2 usage or environment error.
"""

from __future__ import annotations

import ast
import json
import sys
import warnings
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:  # python -I does not put the script directory on sys.path
    sys.path.insert(0, str(HERE))

from auto_common import AuditError, Finding, base_parser, changed_files, emit, in_scope, merge_base, read_text, run_main, show_at, tracked_files  # noqa: E402

TOOL = "obstruction_scan"
RULES = ("O1", "O2", "O3")
INDEPENDENT = "checks/independent/"
PY_SCOPES = ("scripts", "dag", "checks", "code/python")
IMPORT_ROOTS = (".", "scripts", "dag", "code/python", "code/python/src")
DAG = "dag/derivation_dag.json"
DERIVED_ROUTES = ("DERIVED_LEAN", "DERIVED_PROSE", "COMPUTED")
UNHELD_INPUTS = ("OPEN", "REFUTED")
SYS_PATH_EDITS = ("insert", "append", "extend")


# --------------------------------------------------------------------------------------------
# Module index shared by O1 and O2


def module_index(root: Path, files: list[str]) -> dict[str, str]:
    """Dotted module name -> repository-relative file, for every import root a file sits under."""
    index: dict[str, str] = {}
    for rel in files:
        parts = rel[:-3].split("/")
        for base in IMPORT_ROOTS:
            prefix = [] if base == "." else base.split("/")
            if parts[: len(prefix)] != prefix or len(parts) == len(prefix):
                continue
            dotted = parts[len(prefix) :]
            if dotted[-1] == "__init__":
                dotted = dotted[:-1]
            if dotted and all(piece.isidentifier() for piece in dotted):
                index.setdefault(".".join(dotted), rel)
    return index


def repository_top_names(index: dict[str, str]) -> set[str]:
    stdlib = set(getattr(sys, "stdlib_module_names", ()))
    return {name.split(".")[0] for name in index} - stdlib


def parse_python(root: Path, rel: str) -> ast.Module | None:
    text = read_text(root, rel)
    if text is None:
        return None
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)  # invalid escapes in scanned files are not findings here
            return ast.parse(text)
    except SyntaxError:
        return None


# --------------------------------------------------------------------------------------------
# O1: an independent check must not import repository code


def rule_o1(root: Path, rel: str, tree: ast.Module, top_names: set[str]) -> list[Finding]:
    found: list[Finding] = []
    for node in ast.walk(tree):
        for name in _imported_names(node) if isinstance(node, (ast.Import, ast.ImportFrom)) else []:
            if name.split(".")[0] in top_names:
                found.append(Finding("O1", "HIGH", rel, getattr(node, "lineno", 0), f"independent check imports repository module `{name}`"))
        if isinstance(node, ast.ImportFrom) and node.level:
            found.append(Finding("O1", "HIGH", rel, node.lineno, "independent check uses a relative import"))
        if isinstance(node, ast.Call) and _edits_sys_path(node.func):
            found.append(Finding("O1", "MEDIUM", rel, node.lineno, "independent check edits sys.path"))
    return found


def _imported_names(node: ast.AST) -> list[str]:
    if isinstance(node, ast.Import):
        return [alias.name for alias in node.names]
    if isinstance(node, ast.ImportFrom) and not node.level and node.module:
        return [node.module]
    return []


def _edits_sys_path(func: ast.AST) -> bool:
    if not (isinstance(func, ast.Attribute) and func.attr in SYS_PATH_EDITS):
        return False
    target = func.value
    return (isinstance(target, ast.Attribute) and target.attr == "path"
            and isinstance(target.value, ast.Name) and target.value.id == "sys")


# --------------------------------------------------------------------------------------------
# O2: cycles of module-level imports


def module_level_imports(tree: ast.Module) -> list[ast.Import | ast.ImportFrom]:
    """Import statements that run at import time: not inside a function or lambda body."""
    out: list[ast.Import | ast.ImportFrom] = []
    stack: list[ast.AST] = list(tree.body)
    while stack:
        node = stack.pop()
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            continue
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            out.append(node)
        stack.extend(ast.iter_child_nodes(node))
    return out


def resolve_targets(rel: str, node: ast.Import | ast.ImportFrom, index: dict[str, str], files: set[str]) -> set[str]:
    if isinstance(node, ast.Import):
        return {hit for alias in node.names if (hit := _longest(alias.name, index))}
    if node.level:
        return _resolve_relative(rel, node, files)
    module = node.module or ""
    hits = {hit for alias in node.names if (hit := index.get(f"{module}.{alias.name}"))}
    base = _longest(module, index)
    return hits | ({base} if base else set())


def _longest(dotted: str, index: dict[str, str]) -> str | None:
    pieces = dotted.split(".")
    for size in range(len(pieces), 0, -1):
        hit = index.get(".".join(pieces[:size]))
        if hit:
            return hit
    return None


def _resolve_relative(rel: str, node: ast.ImportFrom, files: set[str]) -> set[str]:
    folder = rel.split("/")[:-1]
    if node.level - 1 > len(folder):
        return set()
    base = folder[: len(folder) - (node.level - 1)]
    stems = [base + (node.module or "").split(".") if node.module else base]
    stems += [stems[0] + [alias.name] for alias in node.names]
    hits: set[str] = set()
    for stem in stems:
        joined = "/".join(piece for piece in stem if piece)
        for candidate in (f"{joined}.py", f"{joined}/__init__.py"):
            if candidate in files:
                hits.add(candidate)
    return hits


def strongly_connected(graph: dict[str, set[str]]) -> list[list[str]]:
    """Tarjan's algorithm without recursion; returns the components with two or more files."""
    order: dict[str, int] = {}
    low: dict[str, int] = {}
    on_stack: set[str] = set()
    stack: list[str] = []
    result: list[list[str]] = []
    for start in sorted(graph):
        if start in order:
            continue
        work = [(start, iter(sorted(graph[start])))]
        order[start] = low[start] = len(order)
        stack.append(start)
        on_stack.add(start)
        while work:
            node, children = work[-1]
            child = next(children, None)
            if child is None:
                work.pop()
                if work:
                    low[work[-1][0]] = min(low[work[-1][0]], low[node])
                if low[node] == order[node]:
                    result.append(_pop_component(node, stack, on_stack))
            elif child not in order:
                order[child] = low[child] = len(order)
                stack.append(child)
                on_stack.add(child)
                work.append((child, iter(sorted(graph.get(child, ())))))
            elif child in on_stack:
                low[node] = min(low[node], order[child])
    return sorted((c for c in result if len(c) > 1), key=lambda c: c[0])


def _pop_component(node: str, stack: list[str], on_stack: set[str]) -> list[str]:
    component: list[str] = []
    while True:
        item = stack.pop()
        on_stack.discard(item)
        component.append(item)
        if item == node:
            return sorted(component)


def rule_o2(graph: dict[str, set[str]], focus: set[str] | None) -> list[Finding]:
    found: list[Finding] = []
    for component in strongly_connected(graph):
        if focus is not None and not focus.intersection(component):
            continue
        shown = ", ".join(component[:6]) + (f" and {len(component) - 6} more" if len(component) > 6 else "")
        found.append(Finding("O2", "MEDIUM", component[0], 0, f"module-level import cycle of {len(component)} files", shown))
    return found


# --------------------------------------------------------------------------------------------
# O3: a derived route needs every input; an OPEN or REFUTED input means the route as recorded does not hold


def load_dag(text: str | None, label: str) -> dict[str, Any]:
    if text is None:
        raise AuditError(f"{label} is missing")
    try:
        doc = json.loads(text)
    except json.JSONDecodeError as error:
        raise AuditError(f"{label} is not valid JSON: {error}") from error
    if not isinstance(doc, dict) or not isinstance(doc.get("nodes"), list) or not isinstance(doc.get("routes"), list):
        raise AuditError(f"{label} has no nodes and routes lists")
    return doc


def id_lines(text: str) -> dict[str, int]:
    lines: dict[str, int] = {}
    for number, line in enumerate(text.splitlines(), 1):
        start = line.find('"id": "')
        if start >= 0:
            lines.setdefault(line[start + 7 :].split('"', 1)[0], number)
    return lines


def changed_dag_ids(current: dict[str, Any], base: dict[str, Any]) -> set[str]:
    """Ids of nodes and routes whose record differs from the base (new ones included)."""
    old = {item.get("id"): item for item in base["nodes"] + base["routes"]}
    return {item.get("id") for item in current["nodes"] + current["routes"] if old.get(item.get("id")) != item}


def rule_o3(doc: dict[str, Any], lines: dict[str, int], changed: set[str] | None) -> list[Finding]:
    status = {node.get("id"): node.get("status") for node in doc["nodes"]}
    incoming: dict[str, list[dict[str, Any]]] = {}
    for route in doc["routes"]:
        if route.get("status") != "RECORD_PARENT":
            incoming.setdefault(route.get("output"), []).append(route)
    found: list[Finding] = []
    for route in doc["routes"]:
        bad = _unheld_inputs(route, status)
        if not bad:
            continue
        rid, output = route.get("id"), route.get("output")
        if changed is not None and not changed.intersection({rid, output, *route.get("inputs", [])}):
            continue
        clean = [r for r in incoming.get(output, []) if r.get("status") in DERIVED_ROUTES and not _unheld_inputs(r, status)]
        note = "no other derived route into the output has only held inputs" if not clean else f"{len(clean)} other derived route(s) have held inputs"
        inputs = ", ".join(f"{item} [{status.get(item)}]" for item in bad)
        found.append(Finding("O3", "MEDIUM", DAG, lines.get(rid, 0),
                             f"route {rid} ({route.get('status')}) into {output} [{status.get(output)}] requires {inputs}", note))
    return found


def _unheld_inputs(route: dict[str, Any], status: dict[str, Any]) -> list[str]:
    if route.get("status") not in DERIVED_ROUTES:
        return []
    return [item for item in route.get("inputs", []) if status.get(item) in UNHELD_INPUTS]


# --------------------------------------------------------------------------------------------


class ImportGraph:
    """Module-level import edges between repository files, parsed on first use."""

    def __init__(self, root: Path, files: list[str]) -> None:
        self.root, self.known = root, set(files)
        self.index = module_index(root, files)
        self._edges: dict[str, set[str]] = {}
        self.unparsed: set[str] = set()

    def successors(self, rel: str) -> set[str]:
        if rel not in self._edges:
            tree = parse_python(self.root, rel)
            if tree is None:
                self.unparsed.add(rel)
            targets: set[str] = set()
            for node in module_level_imports(tree) if tree is not None else []:
                targets.update(resolve_targets(rel, node, self.index, self.known))
            self._edges[rel] = targets - {rel}
        return self._edges[rel]

    def subgraph(self, starts: set[str]) -> dict[str, set[str]]:
        """Every file reachable from starts, with its edges; a cycle through a start lies inside it."""
        graph: dict[str, set[str]] = {}
        pending = [rel for rel in sorted(starts) if rel in self.known]
        while pending:
            rel = pending.pop()
            if rel not in graph:
                graph[rel] = self.successors(rel)
                pending.extend(graph[rel] - graph.keys())
        return graph


def python_files(root: Path, focus: set[str] | None) -> list[str]:
    files = set(tracked_files(root, tuple(f"{scope}/*.py" for scope in PY_SCOPES)))
    if focus:
        files.update(rel for rel in focus if rel.endswith(".py") and rel.startswith(tuple(f"{s}/" for s in PY_SCOPES)))
    return sorted(rel for rel in files if rel.endswith(".py") and in_scope(rel))


def python_findings(root: Path, rules: set[str], focus: set[str] | None) -> list[Finding]:
    graph = ImportGraph(root, python_files(root, focus))
    found: list[Finding] = []
    if "O1" in rules:
        top = repository_top_names(graph.index)
        for rel in sorted(graph.known):
            if rel.startswith(INDEPENDENT) and (focus is None or rel in focus):
                tree = parse_python(root, rel)
                if tree is None:
                    graph.unparsed.add(rel)
                else:
                    found.extend(rule_o1(root, rel, tree, top))
    if "O2" in rules:
        found.extend(rule_o2(graph.subgraph(graph.known if focus is None else focus), focus))
    found.extend(Finding("UNPARSEABLE", "LOW", rel, 0, "Python file not read or not parsed; its imports are unknown to O1/O2")
                 for rel in sorted(graph.unparsed))
    return found


def dag_findings(root: Path, ref: str | None) -> list[Finding]:
    """O3 over the whole DAG, or (with ref) over routes touching a node or route changed since the merge base."""
    text = read_text(root, DAG)
    doc = load_dag(text, DAG)
    changed = None
    if ref:
        base_text = show_at(root, merge_base(root, ref), DAG)
        if base_text is not None:
            changed = changed_dag_ids(doc, load_dag(base_text, f"{DAG} at {ref}"))
    return rule_o3(doc, id_lines(text or ""), changed)


def scan(root: Path, ref: str | None, rules: set[str]) -> tuple[list[Finding], str]:
    focus = set(changed_files(root, ref)) if ref else None
    found = python_findings(root, rules, focus) if rules & {"O1", "O2"} else []
    if "O3" in rules:
        found.extend(dag_findings(root, ref))
    scope = f"changes since {ref}" if ref else "whole checkout"
    return found, f"{scope}; rules {', '.join(sorted(rules))}"


def main(argv: list[str] | None = None) -> int:
    parser = base_parser(__doc__.splitlines()[1])
    parser.add_argument("--only", choices=RULES, action="append", help="run only these rules (repeatable)")
    args = parser.parse_args(argv)

    def body() -> int:
        root = args.repo_root.resolve()
        if not (root / ".git").exists():
            raise AuditError(f"{root} is not a git checkout")
        findings, scope = scan(root, args.changed_since, set(args.only or RULES))
        return emit(TOOL, "Obstruction scan", findings, args, scope)

    return run_main(TOOL, body)


if __name__ == "__main__":
    sys.exit(main())
