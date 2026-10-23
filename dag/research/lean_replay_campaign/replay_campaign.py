"""Lean replay campaign driver.

AuthorityEffect: None. Builds Lean modules of lean4/ one `lake build <Module>` at a time, in dependency
order (independent modules of one dependency level may run side by side; --workers sets how many), then runs
the library's own axiom collector (`Lean.collectAxioms`, the function behind `#print axioms`) over every
declaration the DAG cites in that module, in a scratch file that imports the module (no sealed source is
edited). One JSON file per module is kept in --work so that an interrupted run resumes; `assemble` turns those
into dag/research/lean_replay_campaign_<group>.json in the schema of pfp_batch01_lean_replay.json.

    python -I -X utf8 replay_campaign.py run --repo R --plan plan.json --work W [--workers 4] [--only M ...]
    python -I -X utf8 replay_campaign.py assemble --repo R --plan plan.json --work W

plan.json maps a repository-relative Lean path to {"nodes": [[id, status, stage]...], "decls": {symbol: [ids]}}.
No LLM or provider call, no cargo build.
"""
from __future__ import annotations

import argparse
import collections
import concurrent.futures
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import threading
import time
from pathlib import Path

ALLOWED = ("propext", "Classical.choice", "Quot.sound")
SOURCE_BASE = "10be79e94"  # origin/main when the campaign started
AUDIT_VERSION = 4  # 4: exact matching only; whole-file audit never sets the pass flag
EXTPKG = ("Mathlib", "Std", "Lean", "Init", "Batteries", "Aesop", "Qq", "ProofWidgets", "Plausible",
          "LeanSearchClient", "Cli", "ImportGraph")
IMPORT = re.compile(r"^\s*import\s+(.+)$", re.M)


_IDENT = re.compile(r"[\w.'!?]")
_CHAR = re.compile(r"'(?:\\(?:x[0-9a-fA-F]{2}|u[0-9a-fA-F]{4}|.)|[^\\'\n])'")
_RAW = re.compile(r'r(#*)"')


def strip_comments(text: str) -> str:
    """The Lean source with comments and string/char literals blanked, in one pass.

    Line comments (`--`), nested block comments (`/- ... -/`, doc comments included), string literals with
    escapes, raw strings (`r"..."`, `r#"..."#`), character literals and `«...»` quoted names are recognised
    in the order they occur, so `-- /-`, `"/-"` and `'"'` cannot open or close anything they should not.
    Newlines are kept so that line anchors in later regexes still work; a string becomes `""`.
    """
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        raw = _RAW.match(text, i) if c == "r" and (i == 0 or not _IDENT.match(text[i - 1])) else None
        if text.startswith("--", i):
            j = text.find("\n", i)
            i = n if j < 0 else j
        elif text.startswith("/-", i):
            depth, i = 1, i + 2
            while i < n and depth:
                if text.startswith("/-", i):
                    depth, i = depth + 1, i + 2
                elif text.startswith("-/", i):
                    depth, i = depth - 1, i + 2
                else:
                    if text[i] == "\n":
                        out.append("\n")
                    i += 1
            out.append(" ")
        elif raw:
            close = '"' + raw.group(1)
            j = text.find(close, raw.end())
            end = n if j < 0 else j + len(close)
            out.append('""' + "\n" * text.count("\n", i, end))
            i = end
        elif c == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == "\\" else 1
            end = min(j + 1, n)
            out.append('""' + "\n" * text.count("\n", i, end))
            i = end
        elif c == "'" and (i == 0 or not _IDENT.match(text[i - 1])) and _CHAR.match(text, i):
            i = _CHAR.match(text, i).end()
            out.append("''")
        elif c == "«":
            j = text.find("»", i)
            end = n if j < 0 else j + 1
            out.append(text[i:end])
            i = end
        else:
            out.append(c)
            i += 1
    return "".join(out)


def module_of(path: str) -> str | None:
    if path.startswith("lean4/") and path.endswith(".lean"):
        return path[len("lean4/"):-len(".lean")].replace("/", ".")
    return None


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Graph:
    def __init__(self, repo: Path):
        self.repo = repo
        self.path_of: dict[str, str] = {}
        for p in (repo / "lean4").rglob("*.lean"):
            rel = p.relative_to(repo).as_posix()
            parts = rel.split("/")
            if parts[1] in ("b", ".lake") or parts[1].startswith("zz_"):
                continue
            if parts[-1] in ("lakefile.lean",):
                continue
            self.path_of[module_of(rel)] = rel
        self.deps: dict[str, list[str]] = {}
        for mod, rel in self.path_of.items():
            code = strip_comments((repo / rel).read_text(encoding="utf-8", errors="replace"))
            ds = []
            for m in IMPORT.finditer(code):
                for tok in m.group(1).split():
                    tok = tok.strip("«»")
                    if tok.split(".")[0] in EXTPKG:
                        continue
                    if tok in self.path_of:
                        ds.append(tok)
            self.deps[mod] = ds

    def closure(self, roots):
        seen, stack = set(), list(roots)
        while stack:
            m = stack.pop()
            if m in seen:
                continue
            seen.add(m)
            stack.extend(self.deps.get(m, []))
        return seen

    def levels(self, mods):
        mods = set(mods)
        level: dict[str, int] = {}

        def lv(m):
            if m not in level:
                level[m] = 1 + max([lv(d) for d in self.deps[m] if d in mods] or [-1])
            return level[m]
        sys.setrecursionlimit(10000)
        for m in mods:
            lv(m)
        out = collections.defaultdict(list)
        for m, l in level.items():
            out[l].append(m)
        return [sorted(out[k]) for k in sorted(out)]


def lean_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def axiom_script(module: str, symbols: list[str]) -> str:
    cited = ", ".join('"' + lean_escape(s) + '"' for s in symbols)
    return f'''import Lean
import {module if re.fullmatch(r"[A-Za-z_][\w.]*", module) else "«" + module + "»"}
open Lean Elab Command in
#eval show CommandElabM Unit from do
  let env ← getEnv
  match env.getModuleIdx? "{lean_escape(module)}".toName with
  | none => IO.println "MODULE-NOT-FOUND"
  | some idx =>
    let cited : Array String := #[{cited}]
    let names := env.header.moduleData[idx.toNat]!.constNames
    let mut anyMiss := false
    for s in cited do
      -- a cited symbol resolves to a constant whose full name is the symbol or ends in "." ++ symbol (the
      -- evidence map's rule). All matches are printed; the driver treats a leaf with several matches and no
      -- exact one as ambiguous, and a symbol with no match as unresolved. No other fallback.
      let mut hit := false
      for n in names do
        let ns := n.toString
        if !n.isInternal && (ns == s || ns.endsWith ("." ++ s)) then
          hit := true
          let axs ← collectAxioms n
          IO.println s!"AX\\t{{s}}\\t{{ns}}\\t{{axs.toList.map toString}}"
      if !hit then
        anyMiss := true
        IO.println s!"UNRESOLVED\\t{{s}}"
    if cited.isEmpty || anyMiss then
      -- extra information only: every user-facing theorem the file declares. It never sets the pass flag of
      -- a row whose cited symbols include one that did not resolve.
      for n in names do
        if !n.isInternal then
          match env.find? n with
          | some (.thmInfo _) =>
            let axs ← collectAxioms n
            IO.println s!"AX\\t*\\t{{n.toString}}\\t{{axs.toList.map toString}}"
          | _ => pure ()
'''


ADMISSION = [
    re.compile(r"(?<![\w.'])sorry(?![\w'])"),
    re.compile(r"(?m)^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+)?axiom\s"),
    re.compile(r"(?<![\w.'])native_decide(?![\w'])"),
    re.compile(r"(?<![\w.'])unsafe(?![\w'])"),
    re.compile(r"(?m)^\s*admit\s*$|\bby\s+admit\b|<;>\s*admit\b|;\s*admit\b"),
]


def admission_scan(text: str) -> list[str]:
    code = strip_comments(text)
    return [p.pattern for p in ADMISSION if p.search(code)]


def _axiom_list(raw: str) -> list[str]:
    return sorted(a.strip() for a in raw.strip().strip("[]").split(",") if a.strip())


def parse_audit(output: str, cited: list[str]) -> dict:
    """Turn the audit script's output into a resolution of the cited symbols.

    A cited symbol is resolved only through the printed `AX` lines for that symbol: exactly one constant, or
    several of which one is spelled exactly like the symbol. Several suffix matches and no exact one is
    ambiguous, no match is unresolved; both count as not resolved. `AXLC` lines (the retired last-component
    fallback of an earlier version) are ignored. `AX\t*` lines are the whole-file theorem audit, kept apart.
    """
    hits: dict[str, list[tuple[str, list[str]]]] = collections.defaultdict(list)
    file_wide: dict[str, list[str]] = {}
    seen: set[str] = set()
    for line in output.splitlines():
        if line.startswith("AX\t"):
            _, sym, fq, ax = line.split("\t", 3)
            if sym == "*":
                file_wide[fq] = _axiom_list(ax)
            else:
                hits[sym].append((fq, _axiom_list(ax)))
                seen.add(sym)
        elif line.startswith("UNRESOLVED\t"):
            seen.add(line.split("\t", 1)[1])
    axioms: dict[str, list[str]] = {}
    resolution: dict[str, list[str]] = {}
    unresolved: list[str] = []
    ambiguous: dict[str, list[str]] = {}
    for sym in cited:
        found = hits.get(sym, [])
        exact = [h for h in found if h[0] == sym]
        chosen = exact[:1] or (found if len(found) == 1 else [])
        if chosen:
            axioms[chosen[0][0]] = chosen[0][1]
            resolution[sym] = [chosen[0][0]]
        else:
            unresolved.append(sym)
            if len(found) > 1:
                ambiguous[sym] = sorted(h[0] for h in found)
    return {"axioms": axioms, "cited_resolution": resolution, "unresolved_cited_symbols": sorted(unresolved),
            "ambiguous_cited_symbols": ambiguous, "file_wide_axioms": file_wide,
            "all_cited_audited": all(s in seen for s in cited)}


def audit_decision(parsed: dict, cited: list[str], audit_done: bool) -> tuple[bool, dict]:
    """(axiom_audit_passed, the axioms to print in the row).

    With cited symbols: passed only if the audit ran, every cited symbol resolved, and the axioms of the
    resolved constants are all standard. The whole-file audit never sets the flag. With no cited symbol the
    file-wide theorem audit is the audit (there is nothing cited that could fail to resolve).
    """
    if cited:
        axioms = parsed["axioms"]
        ok = bool(audit_done and parsed["all_cited_audited"] and not parsed["unresolved_cited_symbols"] and axioms)
    else:
        axioms = parsed["file_wide_axioms"]
        ok = bool(audit_done and axioms)
    standard = all(set(v) <= set(ALLOWED) for v in axioms.values())
    return ok and standard, axioms


class Runner:
    def __init__(self, repo: Path, work: Path, plan: dict, workers: int):
        self.repo, self.work, self.plan, self.workers = repo, work, plan, workers
        self.lean4 = repo / "lean4"
        self.graph = Graph(repo)
        (work / "results").mkdir(parents=True, exist_ok=True)
        (work / "scratch").mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock()
        self._sha_cache: dict[str, str] = {}

    def res_file(self, module: str) -> Path:
        return self.work / "results" / (module + ".json")

    def lake(self, module: str):
        for target in (module, "+" + module):
            t0 = time.time()
            p = subprocess.run(["lake", "build", target], cwd=self.lean4, capture_output=True,
                               encoding="utf-8", errors="replace")
            secs = time.time() - t0
            out = p.stdout + p.stderr
            if p.returncode != 0 and "unknown target" in out.lower() and target == module:
                continue
            return p.returncode, secs, out, target
        return p.returncode, secs, out, target

    def dep_shas(self, module: str) -> dict[str, str]:
        """sha256 of every lake module this one imports, directly or not."""
        out = {}
        for m in sorted(self.graph.closure([module]) - {module}):
            with self.lock:
                if m not in self._sha_cache:
                    self._sha_cache[m] = sha256_file(self.repo / self.graph.path_of[m])
            out[m] = self._sha_cache[m]
        return out

    @staticmethod
    def keys(sha0: str, deps: dict[str, str], symbols: list[str] | None) -> tuple[str, str]:
        """(build key, audit key). The build depends on the file and its transitive local imports; the audit
        also on the set of cited symbols and on the audit procedure."""
        build = hashlib.sha256(json.dumps([sha0, deps], sort_keys=True).encode()).hexdigest()
        audit = hashlib.sha256(json.dumps([build, symbols, AUDIT_VERSION]).encode()).hexdigest()
        return build, audit

    def process(self, module: str, cited: dict | None):
        rel = self.graph.path_of[module]
        path = self.repo / rel
        cache = self.res_file(module)
        sha0 = sha256_file(path)
        symbols = sorted(cited["decls"]) if cited is not None else None
        build_key, audit_key = self.keys(sha0, self.dep_shas(module), symbols)
        reuse = None
        if cache.exists():
            old = json.loads(cache.read_text(encoding="utf-8"))
            if old.get("build_key") == build_key and old.get("exit_code") == 0:
                if cited is None or (old.get("audit_key") == audit_key and old.get("audit_done")):
                    return old
                reuse = old
        if reuse:
            rc, secs, out, target = 0, reuse["seconds"], reuse["build_output"], reuse["build_target"]
        else:
            rc, secs, out, target = self.lake(module)
        sha1 = sha256_file(path)
        row = {"module": module, "source": rel, "sha256": sha0, "sha256_after_build": sha1,
               "source_unchanged_during_build": sha0 == sha1, "exit_code": rc, "seconds": round(secs, 2),
               "build_target": target, "build_output": out, "checked_at": datetime.datetime.now(
                   datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               "admission_hits": admission_scan(path.read_text(encoding="utf-8", errors="replace")),
               "audit_done": False, "build_key": build_key, "audit_key": audit_key, "audit_version": AUDIT_VERSION}
        if reuse:
            row["checked_at"] = reuse["checked_at"]
        if rc == 0 and cited is not None:
            script = self.work / "scratch" / (module + ".lean")
            script.write_text(axiom_script(module, symbols), encoding="utf-8", newline="\n")
            t0 = time.time()
            p = subprocess.run(["lake", "env", "lean", str(script)], cwd=self.lean4, capture_output=True,
                               encoding="utf-8", errors="replace")
            aout = p.stdout + p.stderr
            row["audit_exit_code"] = p.returncode
            row["audit_seconds"] = round(time.time() - t0, 2)
            row["audit_output"] = aout
            row["cited_symbols_audited"] = symbols
            row["audit_done"] = p.returncode == 0 and "MODULE-NOT-FOUND" not in aout
        cache.write_text(json.dumps(row, indent=1, ensure_ascii=False), encoding="utf-8", newline="\n")
        return row

    def standalone_key(self, rel: str) -> str:
        return "standalone_" + re.sub(r"[^A-Za-z0-9_]+", "_", rel)

    def lake_lean_path(self) -> str:
        if not hasattr(self, "_lean_path"):
            p = subprocess.run(["lake", "env", sys.executable, "-c", "import os;print(os.environ['LEAN_PATH'])"],
                               cwd=self.lean4, capture_output=True, encoding="utf-8")
            self._lean_path = p.stdout.strip()
        return self._lean_path

    def lean_file(self, path: Path, out_olean: Path | None = None):
        """Run `lean` on one file with the lake LEAN_PATH plus the folder of compiled sibling modules."""
        olean_dir = self.work / "olean"
        olean_dir.mkdir(exist_ok=True)
        env = dict(os.environ)
        env["LEAN_PATH"] = self.lake_lean_path() + os.pathsep + str(olean_dir)
        args = ["lean"] + ([f"--root={path.parent}", "-o", str(out_olean)] if out_olean else []) + [str(path)]
        return subprocess.run(args, cwd=self.lean4, capture_output=True, encoding="utf-8", errors="replace", env=env)

    def sibling_files(self, path: Path, seen: set | None = None) -> list[Path]:
        """The files of the same folder that `path` imports, transitively (paper-local modules)."""
        seen = seen if seen is not None else set()
        found: list[Path] = []
        code = strip_comments(path.read_text(encoding="utf-8", errors="replace"))
        for m in IMPORT.finditer(code):
            for tok in m.group(1).split():
                tok = tok.strip("«»")
                sib = path.parent / (tok + ".lean")
                if tok.split(".")[0] in EXTPKG or tok in seen or not sib.is_file():
                    continue
                seen.add(tok)
                found.append(sib)
                found.extend(self.sibling_files(sib, seen))
        return found

    def compile_siblings(self, path: Path, seen: set | None = None) -> None:
        """Compile, in dependency order, the files of the same folder that `path` imports (paper-local modules)."""
        seen = seen if seen is not None else set()
        code = strip_comments(path.read_text(encoding="utf-8", errors="replace"))
        for m in IMPORT.finditer(code):
            for tok in m.group(1).split():
                tok = tok.strip("«»")
                sib = path.parent / (tok + ".lean")
                if tok.split(".")[0] in EXTPKG or tok in seen or not sib.is_file():
                    continue
                seen.add(tok)
                self.compile_siblings(sib, seen)
                self.lean_file(sib, self.work / "olean" / (tok + ".olean"))

    def process_standalone(self, rel: str, cited: dict):
        """A Lean file that is not a module of the lake graph (a paper-local copy): compile it with `lake env lean`
        and audit the constants it declares, in a scratch copy that appends the audit command."""
        key = self.standalone_key(rel)
        path = self.repo / rel
        cache = self.res_file(key)
        sha0 = sha256_file(path)
        symbols = sorted(cited["decls"])
        siblings = {s.name: sha256_file(s) for s in self.sibling_files(path)}
        build_key, audit_key = self.keys(sha0, siblings, symbols)
        if cache.exists():
            old = json.loads(cache.read_text(encoding="utf-8"))
            if old.get("audit_key") == audit_key and old.get("audit_done"):
                return old
        self.compile_siblings(path)
        t0 = time.time()
        p = self.lean_file(path)
        secs = time.time() - t0
        out = p.stdout + p.stderr
        sha1 = sha256_file(path)
        row = {"module": key, "standalone": True, "source": rel, "sha256": sha0, "sha256_after_build": sha1,
               "source_unchanged_during_build": sha0 == sha1, "exit_code": p.returncode, "seconds": round(secs, 2),
               "build_target": "lean " + rel + "   # LEAN_PATH from `lake env`; sibling modules compiled first", "build_output": out,
               "checked_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               "admission_hits": admission_scan(path.read_text(encoding="utf-8", errors="replace")),
               "audit_done": False, "build_key": build_key, "audit_key": audit_key, "audit_version": AUDIT_VERSION}
        if p.returncode == 0:
            cited_lit = ", ".join('"' + lean_escape(x) + '"' for x in symbols)
            snippet = f'''
open Lean Elab Command in
#eval show CommandElabM Unit from do
  let env ← getEnv
  let cited : Array String := #[{cited_lit}]
  for s in cited do
    let mut hit := false
    for (n, _) in env.constants.map₂.toList do
      let ns := n.toString
      if ns == s || ns.endsWith ("." ++ s) then
        hit := true
        let axs ← collectAxioms n
        IO.println s!"AX\\t{{s}}\\t{{ns}}\\t{{axs.toList.map toString}}"
    if !hit then
      IO.println s!"UNRESOLVED\\t{{s}}"
'''
            script = self.work / "scratch" / (key + ".lean")
            script.write_text("import Lean\n" + path.read_text(encoding="utf-8") + "\n" + snippet,
                              encoding="utf-8", newline="\n")
            t1 = time.time()
            q = self.lean_file(script)
            aout = q.stdout + q.stderr
            row.update(audit_exit_code=q.returncode, audit_seconds=round(time.time() - t1, 2), audit_output=aout,
                       cited_symbols_audited=symbols, audit_done=q.returncode == 0)
        cache.write_text(json.dumps(row, indent=1, ensure_ascii=False), encoding="utf-8", newline="\n")
        return row

    def normalise_only(self, only):
        """--only takes repository paths (lean4/X.lean, papers/.../X.lean) or module names (X, Imported.A.B).
        Returns (set of plan paths, set of lake modules); an unknown token is an error."""
        if not only:
            return None, None
        paths, mods = set(), set()
        for tok in only:
            if tok in self.plan:
                paths.add(tok)
                if module_of(tok) in self.graph.path_of:
                    mods.add(module_of(tok))
            elif tok in self.graph.path_of:
                mods.add(tok)
                paths.add(self.graph.path_of[tok])
            else:
                raise SystemExit(f"--only {tok!r} is neither a path of the plan nor a lake module")
        return paths, mods

    def run(self, only=None):
        only_paths, only_mods = self.normalise_only(only)
        for rel, ent in sorted(self.plan.items()):
            if module_of(rel) is None and ent["decls"] and (only_paths is None or rel in only_paths):
                r = self.process_standalone(rel, ent)
                print(f"[standalone] {rel}: {'ok' if r['exit_code'] == 0 else 'FAIL'} {r['seconds']}s "
                      f"audit={'ok' if r.get('audit_done') else '-'}", flush=True)
        cited_mods = {}
        for path, ent in self.plan.items():
            m = module_of(path)
            if m and m in self.graph.path_of:
                cited_mods[m] = ent
        todo = set(only_mods) if only_mods is not None else set(cited_mods)
        closure = self.graph.closure(todo)
        levels = self.graph.levels(closure)
        print(f"{len(todo)} receipt modules, {len(closure)} modules in the dependency closure, "
              f"{len(levels)} levels", flush=True)
        # dependency-driven schedule: a module starts as soon as every module it imports is finished;
        # modules on the longest remaining chain go first
        deps = {m: {d for d in self.graph.deps[m] if d in closure} for m in closure}
        users: dict[str, list[str]] = collections.defaultdict(list)
        for m, ds in deps.items():
            for d in ds:
                users[d].append(m)
        height: dict[str, int] = {}

        def h(m):
            if m not in height:
                height[m] = 1 + max([h(u) for u in users[m]] or [0])
            return height[m]
        sys.setrecursionlimit(10000)
        for m in closure:
            h(m)
        waiting = {m: set(ds) for m, ds in deps.items()}
        ready = sorted([m for m, ds in waiting.items() if not ds], key=lambda m: -height[m])
        running: dict = {}
        done = 0
        with concurrent.futures.ThreadPoolExecutor(self.workers) as ex:
            while ready or running:
                while ready and len(running) < self.workers:
                    m = ready.pop(0)
                    running[ex.submit(self.process, m, cited_mods.get(m) if m in todo else None)] = m
                finished, _ = concurrent.futures.wait(running, return_when=concurrent.futures.FIRST_COMPLETED)
                for f in finished:
                    m = running.pop(f)
                    try:
                        r = f.result()
                        status = "ok" if r["exit_code"] == 0 else "FAIL"
                        note = f" audit={'ok' if r.get('audit_done') else '-'}" if m in todo else ""
                        print(f"[h{height[m]}] {m}: {status} {r['seconds']}s{note}", flush=True)
                    except Exception as e:  # noqa: BLE001
                        print(f"[h{height[m]}] {m}: ERROR {e!r}", flush=True)
                    done += 1
                    for u in users[m]:
                        waiting[u].discard(m)
                        if not waiting[u] and u not in ready and u not in running.values():
                            ready.append(u)
                    ready.sort(key=lambda x: -height[x])
        print("done", done, flush=True)


def tool_versions(lean4: Path):
    def run(args):
        return subprocess.run(args, cwd=lean4, capture_output=True, encoding="utf-8").stdout.strip()
    return run(["lean", "--version"]), run(["lake", "--version"])


def trunc(s: str, n: int) -> str:
    return s if len(s) <= n else s[: n // 2] + "\n...[truncated " + str(len(s) - n) + " chars]...\n" + s[-n // 2:]


def assemble(repo: Path, work: Path, plan: dict, groups_out: Path):
    lean_v, lake_v = tool_versions(repo / "lean4")
    mathlib = json.loads((repo / "lean4/lake-manifest.json").read_text(encoding="utf-8"))
    msha = next(p["rev"] for p in mathlib["packages"] if p["name"] == "mathlib")
    lakefile_sha = sha256_file(repo / "lean4/lakefile.lean")
    by_group: dict[str, list] = collections.defaultdict(list)
    deps_built: dict[str, list] = collections.defaultdict(list)
    rows_by_module = {}
    for f in sorted((work / "results").glob("*.json")):
        rows_by_module[f.stem] = json.loads(f.read_text(encoding="utf-8"))
    runner_key = lambda rel: "standalone_" + re.sub(r"[^A-Za-z0-9_]+", "_", rel)  # noqa: E731
    for path, ent in sorted(plan.items()):
        m = module_of(path) or runner_key(path)
        if m not in rows_by_module:
            continue
        r = rows_by_module[m]
        stage_count = collections.Counter(n[2] for n in ent["nodes"])
        group = sorted(stage_count.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]
        if sha256_file(repo / r["source"]) != r["sha256"]:
            raise SystemExit(f"{r['source']} changed since it was replayed; run the campaign again before assembling")
        cited = sorted(ent["decls"])
        parsed = parse_audit(r.get("audit_output", ""), cited)
        audit_ok, axioms = audit_decision(parsed, cited, bool(r.get("audit_done")))
        admission_ok = not r.get("admission_hits") and "declaration uses 'sorry'" not in r["build_output"]
        row = {
            "module": m if not rows_by_module[m].get("standalone") else path[:-len(".lean")].replace("/", "."),
            "standalone_file": bool(rows_by_module[m].get("standalone")),
            "dag_nodes": sorted({n[0] for n in ent["nodes"]}),
            "dag_node_statuses": {n[0]: n[1] for n in ent["nodes"]},
            "source": r["source"],
            "sha256": r["sha256"],
            "sha256_after_build": r["sha256_after_build"],
            "source_unchanged_during_build": r["source_unchanged_during_build"],
            "exit_code": r["exit_code"],
            "built_successfully": r["exit_code"] == 0,
            "seconds": r["seconds"],
            "admission_scan_passed": admission_ok,
            "axiom_audit_passed": audit_ok,
            "cited_symbols": sorted(ent["decls"]),
            "cited_resolution": parsed["cited_resolution"],
            "unresolved_cited_symbols": parsed["unresolved_cited_symbols"],
            "ambiguous_cited_symbols": parsed["ambiguous_cited_symbols"],
            "axiom_audit_basis": "cited declarations" if cited else "every theorem of the file (no declaration cited)",
            "axioms": axioms,
            **({"axioms_whole_file_extra": parsed["file_wide_axioms"]}
               if cited and parsed["file_wide_axioms"] else {}),
            "output": trunc(r["build_output"], 3000 if r["exit_code"] == 0 else 12000),
            "axiom_audit_output": trunc(r.get("audit_output", ""), 6000),
            "build_command": (f"cd lean4 && {r['build_target']}" if r.get("standalone")
                              else f"cd lean4 && lake build {r.get('build_target', m)}"),
            "audit_command": "cd lean4 && lake env lean <scratch>.lean   # imports Lean and the module; "
                             "Lean.collectAxioms over each constant named by a cited symbol",
            "checked_at": r["checked_at"],
        }
        by_group[group].append(row)
    summary = {}
    for group, rows in sorted(by_group.items()):
        ok = sum(1 for r in rows if r["exit_code"] == 0 and r["axiom_audit_passed"] and r["admission_scan_passed"])
        doc = {
            "schema_version": "lean_replay_campaign.v1",
            "authority_effect": "None",
            "checked_at": datetime.date.today().isoformat(),
            "group": group,
            "result": (f"{len(rows)} Lean module(s) cited by DAG nodes of stage {group}; {ok} built with exit code 0, "
                       "passed the admission scan and the axiom audit (every printed axiom list a subset of "
                       "propext, Classical.choice, Quot.sound); the rest are listed with their failure."),
            "source_base": SOURCE_BASE,
            "proof_boundary": "This receipt records that the file with the stated sha256 type-checks and which axioms "
                              "the cited declarations depend on. It changes no DAG node status and does not say the "
                              "declaration states the node's claim.",
            "lean_replay": {
                "lean_version": lean_v,
                "lake_version": lake_v,
                "mathlib_source_sha": msha,
                "lakefile_sha256": lakefile_sha,
                "build_directory": "lean4/b (lakefile buildDir; removed after the run)",
                "dependency_packages": "read-only junction lean4/.lake/packages to the shared Mathlib v4.35.0 cache (removed after the run)",
                "command": "cd lean4 && lake build <Module>   (one invocation per module, dependencies first)",
                "parallelism": "modules of one dependency level were built side by side; seconds are wall-clock "
                               "and include contention",
                "allowed_axioms": list(ALLOWED),
                "results": sorted(rows, key=lambda r: r["module"]),
            },
            "reproduction": [
                "ln -s <shared Mathlib v4.35.0 package cache> lean4/.lake/packages   # Mathlib rev 56a005855ea17e0b0958f73ec801ae140b0a1679",
                "cd lean4 && lake build <module>   # modules of lean4/Imported are in the ImportedAtlas library",
                "cd lean4 && lake env lean <scratch.lean>   # import Lean + the module; Lean.collectAxioms over the constants "
                "whose names end in a cited symbol (every theorem of the module when the DAG cites the file only)",
                "python -I -X utf8 dag/research/lean_replay_campaign/replay_campaign.py run|assemble --repo . --plan plan.json --work <dir>",
            ],
            "limits": [
                "A receipt covers a file, not a statement: it shows that the file type-checks and which axioms the named "
                "declarations use. Whether a declaration states a node's claim is the job of the PFP reviews.",
                "Axiom lists come from Lean.collectAxioms (the function behind #print axioms) run in a scratch file; the "
                "sources were not edited. A cited symbol resolves only to a constant whose full name is the symbol or "
                "ends in '.' + the symbol; a symbol with no such constant, or only several suffix matches and no exact "
                "one, is listed under unresolved_cited_symbols / ambiguous_cited_symbols and is not audited. "
                "axiom_audit_passed is true only if every cited symbol resolved and every audited axiom is standard; "
                "the whole-file theorem audit (axioms_whole_file_extra) is information and never sets it. When the DAG "
                "cites a file without naming a declaration, the audit is of every theorem of the file.",
                "seconds is wall-clock for one `lake build` invocation while up to four independent modules were built "
                "side by side; it includes contention and, for a module whose dependencies were built just before, only "
                "that module's own compile.",
            ],
        }
        out = groups_out / f"lean_replay_campaign_{group.lower()}.json"
        out.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        summary[group] = {"modules": len(rows), "passed": ok,
                          "failed": [r["module"] for r in rows if not (r["exit_code"] == 0 and r["axiom_audit_passed"]
                                                                      and r["admission_scan_passed"])]}
    deps = [{"module": m, "source": r["source"], "sha256": r["sha256"], "exit_code": r["exit_code"],
             "seconds": r["seconds"]} for m, r in sorted(rows_by_module.items())
            if not any((module_of(p) or runner_key(p)) == m for p in plan)]
    dep_dir = groups_out / "lean_replay_campaign"
    dep_dir.mkdir(parents=True, exist_ok=True)
    (dep_dir / "dependency_builds.json").write_text(json.dumps({
        "schema_version": "lean_replay_dependency_builds.v1", "authority_effect": "None",
        "note": "Modules built only because a cited module imports them. Not receipts: no cited declaration is audited.",
        "dependency_builds": deps}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    (work / "assemble_summary.json").write_text(json.dumps({"groups": summary, "dependency_builds": deps},
                                                           indent=1), encoding="utf-8", newline="\n")
    return summary, deps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "assemble"])
    ap.add_argument("--repo", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    repo, work = Path(a.repo), Path(a.work)
    plan = json.loads(Path(a.plan).read_text(encoding="utf-8"))
    if a.cmd == "run":
        Runner(repo, work, plan, a.workers).run(a.only)
    else:
        s, d = assemble(repo, work, plan, repo / "dag/research")
        print(json.dumps(s, indent=1))
        print(len(d), "dependency-only builds")


if __name__ == "__main__":
    main()
