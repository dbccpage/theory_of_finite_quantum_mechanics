"""Render docs/maintenance/atlas_dependency_inventory.md from the inventory JSON, the import manifest and the DAG.

AuthorityEffect: None. Reads only files of this checkout.

    python -I -X utf8 atlas_inventory_md.py --repo R
"""
from __future__ import annotations

import argparse
import collections
import importlib.util
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("atlas_inventory", HERE / "atlas_inventory.py")
inv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inv)
_rspec = importlib.util.spec_from_file_location("replay_campaign", HERE / "replay_campaign.py")
replay = importlib.util.module_from_spec(_rspec)
_rspec.loader.exec_module(replay)

NODE_FIELDS = ("lean", "rust", "source")
RECORD_FIELDS = ("lean4", "rust", "python")
PROVENANCE_FIELDS = ("f004_refs", "coda_atlas_paths")


def human(n: float) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def cell(s: object) -> str:
    return str(s).replace("|", "\\|")


def dag_citations(repo: Path, existing: dict[str, dict]):
    """node id -> (status, set of atlas paths it cites in node fields), likewise for records."""
    dag = json.loads((repo / "dag/derivation_dag.json").read_bytes())
    node_cites: dict[str, tuple[str, set[str]]] = {}
    for n in dag["nodes"]:
        s: set[str] = set()
        for f in NODE_FIELDS:
            for ref in n.get(f, []):
                p = inv.clean(ref.split("::")[0])
                for m in inv.PATH_SIMPLE.finditer(p):
                    s.add(inv.clean(m.group(1)))
        if s:
            node_cites[n["id"]] = (n["status"], s)
    prov = 0
    rec_cites = 0
    for r in dag["records"]:
        for f in RECORD_FIELDS:
            for ref in r.get(f, []):
                if inv.PATH_SIMPLE.search(ref):
                    rec_cites += 1
        for f in PROVENANCE_FIELDS:
            prov += sum(1 for ref in r.get(f, []) if inv.PATH_SIMPLE.search(ref))
    return node_cites, rec_cites, prov


def _dependency_paths(doc: dict):
    """(dependency name, path) for every dependency table of a parsed Cargo.toml: dependencies,
    dev-dependencies, build-dependencies, workspace.dependencies, target.*.dependencies and patch/replace
    tables. `path =` under [lib], [[bin]], [[test]] and so on is a source file, not a dependency, and is skipped."""
    tables = []
    for key in ("dependencies", "dev-dependencies", "build-dependencies"):
        tables.append(doc.get(key, {}))
        for target in doc.get("target", {}).values():
            tables.append(target.get(key, {}))
    tables.append(doc.get("workspace", {}).get("dependencies", {}))
    for patched in doc.get("patch", {}).values():
        tables.append(patched)
    for table in tables:
        for name, spec in table.items():
            if isinstance(spec, dict) and isinstance(spec.get("path"), str):
                yield name, spec["path"]


def structured_atlas_lean_refs(repo: Path) -> list[tuple[str, str]]:
    """(id, reference) for every node `lean` and record `lean4` reference that still names an atlas Lean file."""
    dag = json.loads((repo / "dag/derivation_dag.json").read_bytes())
    found = []
    for kind, field in (("nodes", "lean"), ("records", "lean4")):
        for item in dag[kind]:
            for ref in item.get(field, []):
                if ref.startswith(("absent", "external:")):
                    continue
                path = ref.split("::")[0].split(":")[0]
                if path.endswith(".lean") and inv.PATH_SIMPLE.search(path):
                    found.append((item["id"], ref))
    return found


def replay_exit_codes(repo: Path) -> dict[str, int]:
    """repo-relative Lean path -> exit code of its build, from the receipts and the dependency build record."""
    out: dict[str, int] = {}
    for f in sorted((repo / "dag/research").glob("lean_replay_campaign_*.json")):
        for r in json.loads(f.read_text(encoding="utf-8")).get("lean_replay", {}).get("results", []):
            out[r["source"]] = r["exit_code"]
    for deps in sorted((repo / "dag/research/lean_replay_campaign").glob("dependency_builds*.json")):
        for r in json.loads(deps.read_text(encoding="utf-8"))["dependency_builds"]:
            out.setdefault(r["source"], r["exit_code"])
    return out


def cargo_leaks(repo: Path):
    """Path dependencies of Cargo.toml files (outside dag/results, which holds sealed copies) that point out of
    the repository. Both sides are resolved and compared with is_relative_to, case-insensitively on Windows."""
    import os
    import tomllib
    root = repo.resolve()

    def inside(p: Path) -> bool:
        return Path(os.path.normcase(p)).is_relative_to(Path(os.path.normcase(root)))

    leaks, n = [], 0
    for dp, dn, fns in os.walk(repo):
        rel = Path(dp).relative_to(repo).as_posix()
        dn[:] = [d for d in dn if d not in (".git", "target", "b", ".lake", "node_modules")
                 and not (Path(rel) / d).as_posix().startswith("dag/results")]
        if "Cargo.toml" not in fns:
            continue
        manifest = Path(dp) / "Cargo.toml"
        try:
            doc = tomllib.loads(manifest.read_text(encoding="utf-8", errors="replace"))
        except tomllib.TOMLDecodeError:
            continue
        for name, dep_path in _dependency_paths(doc):
            n += 1
            if not inside((manifest.parent / dep_path).resolve()):
                leaks.append((manifest.relative_to(repo).as_posix(), name, dep_path))
    return leaks, n


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    a = ap.parse_args()
    repo = Path(a.repo)
    out_dir = repo / "docs/maintenance"
    doc = json.loads((out_dir / "atlas_dependency_inventory.json").read_text(encoding="utf-8"))
    manifest = json.loads((repo / "lean4/Imported/import_manifest.json").read_text(encoding="utf-8"))
    paths = doc["paths"]
    for p in paths:
        p["group"] = inv.group_of(p["path"])
    by_path = {p["path"]: p for p in paths}
    node_cites, rec_cites, prov = dag_citations(repo, by_path)

    # ---- per group
    groups: dict[str, dict] = collections.defaultdict(lambda: {
        "paths": 0, "exist": 0, "missing": 0, "live": 0, "generated": 0, "sealed": 0,
        "kinds": collections.Counter(), "live_kinds": collections.Counter(), "live_bytes": 0,
        "gone_kinds": collections.Counter(), "gone_bytes": 0, "gone_files": 0,
        "nodes": set(), "top": 0})
    for p in paths:
        g = groups[p["group"]]
        g["paths"] += 1
        g["exist"] += p["exists_in_atlas"]
        gone_file = bool(p.get("removed_in_commit")) and not p.get("removed_dir")
        g["missing"] += not p["exists_in_atlas"] and not gone_file
        g["removed"] = g.get("removed", 0) + gone_file
        live = sum(n for loc, n in p["referenced_from"].items() if loc in inv.LIVE)
        gen = sum(n for loc, n in p["referenced_from"].items() if loc in inv.GENERATED)
        sealed = sum(n for loc, n in p["referenced_from"].items() if loc in inv.SEALED)
        g["live"] += live
        g["generated"] += gen
        g["sealed"] += sealed
        g["kinds"][p["kind"]] += 1
        if live and p["exists_in_atlas"] and not p.get("is_dir"):
            g["live_kinds"][p["kind"]] += 1
            g["live_bytes"] += p.get("size_bytes", 0)
        if live and gone_file:
            g["gone_kinds"][p["kind"]] += 1
            g["gone_bytes"] += p.get("size_bytes_before_removal", 0)
            g["gone_files"] += 1
    for nid, (status, cites) in node_cites.items():
        for c in cites:
            if c in by_path:
                groups[by_path[c]["group"]]["nodes"].add((nid, status))

    def verdict(g: dict) -> tuple[str, str]:
        existing_live = sum(g["live_kinds"].values())
        if g["live"] == 0:
            return "SAFE TO DELETE", "no live reference (only sealed run artifacts or generated views, if any)"
        if existing_live:
            kinds = ", ".join(f"{n} {k}" for k, n in g["live_kinds"].most_common())
            extra = f"; a further {g['gone_files']} cited file(s) are already gone from the working tree" if g["gone_files"] else ""
            return "NOT YET SAFE", f"{existing_live} existing file(s) are cited by live files of this repo ({kinds}; {human(g['live_bytes'])}){extra}"
        if g["gone_files"]:
            kinds = ", ".join(f"{n} {k}" for k, n in g["gone_kinds"].most_common())
            return "ALREADY REMOVED", (f"{g['gone_files']} cited file(s) ({kinds}; {human(g['gone_bytes'])}) were deleted by sibling commit "
                                       f"{inv.REMOVAL_COMMIT}; this repo's references to them no longer resolve and the content is only in the sibling's git history")
        return "SAFE TO DELETE", ("every live reference names a path that is not in the atlas (already broken); "
                                  "nothing is lost")

    top_level = collections.defaultdict(list)
    for name in sorted(groups):
        top_level[name.split("/")[0]].append(name)

    total_exist = sum(1 for p in paths if p["exists_in_atlas"])
    gone = [p for p in paths if p.get("removed_in_commit") and not p.get("removed_dir")]
    gone_paths = {p["path"] for p in gone}
    gone_cited = [p for p in gone if sum(n for loc, n in p["referenced_from"].items() if loc in inv.LIVE)]
    gone_families = sorted({"/".join(p["path"].split("/")[3:4]) for p in gone})
    lines: list[str] = []
    w = lines.append
    w("# Atlas dependency inventory")
    w("")
    w("**AuthorityEffect:** None. This page is a report. It changes no node status and copies no file out of the sibling tree.")
    w("")
    w(f"Generated {doc['generated']} by [`dag/research/lean_replay_campaign/atlas_inventory.py`](../../dag/research/lean_replay_campaign/atlas_inventory.py) "
      "and `atlas_inventory_md.py` from this checkout, read-only against the sibling checkout `the_symbol_game` "
      "(the tree that holds `omega_engine*` and the atlas folders). The machine-readable list is "
      "[`atlas_dependency_inventory.json`](atlas_dependency_inventory.json): one entry per distinct path, with whether it "
      "exists in the atlas, its size, its kind and which kinds of file here cite it.")
    w("")
    w("## What was scanned")
    w("")
    w(f"- {doc['files_scanned']} text files of this checkout (`.py .rs .toml .md .json .jsonl .yaml .lean .txt ...`), "
      f"{doc['files_mentioning_atlas']} of which name a sibling-tree path. `lean4/Imported/` (provenance headers), the campaign tools and this page are not scanned.")
    w(f"- {doc['distinct_paths']} distinct paths: {total_exist} exist in the sibling working tree, {len(gone)} existed until sibling commit "
      f"`{inv.REMOVAL_COMMIT}` removed them (see the next section), and {doc['distinct_paths'] - total_exist - len(gone) - sum(1 for p in paths if p.get('removed_dir'))} "
      "are not files of the sibling tree at any commit examined (historical names, moved files, directories, or prose fragments that look like paths).")
    w("- Reference classes: node fields (`source`, `rust`, `lean`) and record fields (`lean4`, `rust`, `python`) of "
      "`dag/derivation_dag.json`; the fragments that generate them; generated derivation papers and views; "
      "`dag/results/**` (sealed run artifacts that quote the paths of their inputs); `code/**`; `papers/**`; `scripts/**`; `lean4/**`; `docs/**`.")
    w(f"- Records also carry {prov} provenance strings (`f004_refs`, `coda_atlas_paths`) that name atlas files as the origin of a record. "
      "They are left as they are; they are history, not a dependency a tool resolves.")
    w("")
    w("## The sibling tree changed while this was being done")
    w("")
    w(f"Sibling commit `{inv.REMOVAL_COMMIT}` (\"Remove seven F004 paper families from the atlas tree\", 2026-10-22 17:52 -0400, on the sibling branch `chore/remove-woland-digests`) "
      f"deleted `{'`, `'.join(gone_families)}` under `omega_engine_atlas/coda_atlas/F004_papers/` from the working tree. "
      f"{len(gone)} files that this checkout names existed there; {len(gone_cited)} of them are cited by live files "
      f"({human(sum(p.get('size_bytes_before_removal', 0) for p in gone_cited))}). They are still in the sibling's git history "
      f"(`git -C the_symbol_game show {inv.REMOVAL_COMMIT}^:<path>`). The Lean files this change imported all come from families that were not removed, "
      "so the import and the replay are unaffected; the references that now dangle are the `source`, `rust` and `python` citations of nodes and records "
      "that quote the removed families. The inventory below counts those as *removed*, not as missing.")
    w("")
    w("## Where the references are")
    w("")
    w("| Reference class | references | distinct paths |")
    w("|---|---|---|")
    cls = collections.Counter(); cls_paths = collections.Counter()
    for p in paths:
        for loc, n in p["referenced_from"].items():
            cls[loc] += n
            cls_paths[loc] += 1
    for loc, n in cls.most_common():
        w(f"| {cell(loc)} | {n} | {cls_paths[loc]} |")
    w("")
    w(f"*{inv.PROVENANCE_LOC}* are the `f004_refs`, `coda_atlas_paths` and `coda_atlas_ids` values of records and fragments. They say where a record "
      "came from and are excluded from every *live* count below.")
    w("")
    w("A reference in a generated paper or view, or in a sealed run artifact, follows from a reference in `dag/derivation_dag.json`, "
      "its fragments or a sealed input and is not a separate dependency.")
    w("")
    w("## What was imported")
    w("")
    files = manifest["files"]
    ported = [f for f in files if f.get("ports")]
    by_slug = collections.Counter(f["slug"] for f in files)
    mathlib_rev = next((p["rev"] for p in json.loads((repo / "lean4/lake-manifest.json").read_text(encoding="utf-8"))["packages"]
                        if p["name"] == "mathlib"), "?")
    builds = replay_exit_codes(repo)
    imported_paths = [f["repo_path"] for f in files]
    built_ok = sum(1 for rp_ in imported_paths if builds.get(rp_) == 0)
    built_bad = [rp_ for rp_ in imported_paths if rp_ in builds and builds[rp_] != 0]
    not_built = [rp_ for rp_ in imported_paths if rp_ not in builds]
    admission = sorted(rp_ for rp_ in imported_paths
                       if replay.admission_scan((repo / rp_).read_text(encoding="utf-8", errors="replace")))
    w(f"{len(files)} Lean files that DAG nodes and records cited outside this repository, together with their local (non-Mathlib) imports, "
      f"were copied to `lean4/Imported/<package>/<path under the package root>.lean` and registered as the non-default library `ImportedAtlas` "
      f"in `lean4/lakefile.lean`. {sum(1 for f in files if f['cited_directly'])} are cited directly; the others are dependencies. "
      "The package folder disambiguates files that share a stem in different atlas papers. "
      "Every file carries a header with its original path, original sha256 and the import date. "
      f"Build record (receipts and `dag/research/lean_replay_campaign/dependency_builds*.json`, Mathlib `{mathlib_rev}`): "
      f"{built_ok} of {len(files)} built with exit code 0, {len(built_bad)} failed, {len(not_built)} have no build record. "
      f"{len(ported)} needed a port for version drift ({', '.join('`' + f['repo_path'][len('lean4/'):] + '`' for f in ported) or 'none'}), "
      "recorded in its header and in [`lean4/Imported/import_manifest.json`](../../lean4/Imported/import_manifest.json). "
      f"The admission scan (`sorry`, `admit`, `axiom`, `native_decide`, `unsafe` outside comments and strings) flags {len(admission)} of them"
      + (f": {', '.join('`' + a + '`' for a in admission)}." if admission else "."))
    w("")
    w("| Package (atlas path of the Lean root) | files |")
    w("|---|---|")
    for slug, n in sorted(by_slug.items()):
        sample = next(f for f in files if f["slug"] == slug)
        rel = sample["repo_path"][len(f"lean4/Imported/{slug}/"):]
        orig = sample["original_path"]
        root = orig[: len(orig) - len(rel)].rstrip("/")
        w(f"| `{root}` -> `lean4/Imported/{slug}/` | {n} |")
    w("")
    rp = manifest["repointed_instead_of_imported"]
    w(f"{len(rp)} cited path(s) were not imported because this repository already holds a file with that role (see the import manifest); "
      "the references now name the in-repo file:")
    w("")
    for k, v in rp.items():
        w(f"- `{k}` -> `{v}`")
    w("")
    w("Files under `dag/results/**` are sealed run snapshots; their references were not touched and their Lean files are not replayed.")
    w("")
    prog_path = repo / "lean4/Imported/import_manifest_programmes.json"
    if prog_path.exists():
        prog = json.loads(prog_path.read_text(encoding="utf-8"))
        prog_files = prog["files"]
        w("### Programme folders (`lean4/research_programs/*`, `lean4/quantum_mechanics`, loose `lean4/*.lean`)")
        w("")
        w("A second import took Lean files from the sibling `lean4/` tree only where they are not already here "
          "(identical sha256, newline-equivalent, or same module name) and a DAG node cites them, a file being imported imports them, "
          "or they belong to the genesis / S(n) / MSS-N / pre-genesis / WDP / MUB6 / HCT programmes. "
          "`dag/research/lean_replay_campaign/import_programmes.py` makes the decision for every file and "
          "[`lean4/Imported/import_manifest_programmes.json`](../../lean4/Imported/import_manifest_programmes.json) records the imports.")
        w("")
        w("| Sibling folder | decision counts |")
        w("|---|---|")
        for slug, c in sorted(prog["decisions_summary"].items()):
            w(f"| `{slug}` | " + ", ".join(f"{k} {v}" for k, v in sorted(c.items())) + " |")
        w("")
        codes = replay_exit_codes(repo)
        ok = [f for f in prog_files if codes.get(f["repo_path"]) == 0]
        bad = [f for f in prog_files if f["repo_path"] in codes and codes[f["repo_path"]] != 0]
        missing_rec = [f for f in prog_files if f["repo_path"] not in codes]
        roots = (repo / "lean4/lakefile.lean").read_text(encoding="utf-8")
        in_lib = [f for f in prog_files if re.search("`" + re.escape(f["module"]) + r"(?![\w.])", roots)]
        w(f"{len(prog_files)} files were imported; {len(ok)} built with exit code 0 and {len(in_lib)} of them are roots of `ImportedAtlas`; "
          f"{len(bad)} did not build and are kept out of the library; {len(missing_rec)} have no build record.")
        w("")
        if bad:
            w("Files that did not build (receipt rows with `exit_code` 1):")
            w("")
            for f in bad:
                w(f"- `{f['repo_path']}` (from `{f['original_path']}`)")
            w("")
    w("## What this repository would lose")
    w("")
    w("The table lists each group of sibling-tree paths that this checkout cites. *live* counts references from files that are inputs of "
      "the DAG, code, papers, scripts, `lean4/` and docs; *gen.* from generated papers and views; *sealed* from `dag/results/**`. "
      "*nodes* is the number of DAG nodes that cite a file of the group in their `source`, `rust` or `lean` field (node count only; "
      "a node can cite several).")
    w("")
    w("| Group | paths (exist/removed/missing) | live | gen. | sealed | nodes | files cited live (present; removed) |")
    w("|---|---|---|---|---|---|---|")
    for top, names in sorted(top_level.items()):
        for name in names:
            g = groups[name]
            if g["live"] == 0 and g["generated"] == 0 and g["sealed"] == 0:
                continue
            kinds = ", ".join(f"{n} {k}" for k, n in g["live_kinds"].most_common(4)) or "-"
            if g["gone_files"]:
                kinds += "; removed: " + ", ".join(f"{n} {k}" for k, n in g["gone_kinds"].most_common(4))
            w(f"| `{name}` | {g['paths']} ({g['exist']}/{g.get('removed', 0)}/{g['missing']}) | {g['live']} | {g['generated']} | {g['sealed']} | {len(g['nodes'])} | {cell(kinds)} |")
    w("")
    w("### Nodes that depend on the atlas, by status")
    w("")
    status_count = collections.Counter()
    for nid, (status, cites) in node_cites.items():
        if any(c in by_path and (by_path[c]["exists_in_atlas"] or by_path[c].get("removed_in_commit")) for c in cites):
            status_count[status] += 1
    w("Counting nodes whose `source`, `rust` or `lean` field names an atlas file that exists, or existed until the removal commit (the provenance strings are not counted):")
    w("")
    w("| Status | nodes |")
    w("|---|---|")
    for s, n in status_count.most_common():
        w(f"| `{s}` | {n} |")
    w("")
    lean_live = [p for p in paths if p["kind"] == "Lean" and (p["exists_in_atlas"] or p["path"] in gone_paths)
                 and not p.get("is_dir") and any(l in inv.LIVE for l in p["referenced_from"])]
    dag_only = [p for p in lean_live if all(l not in inv.LIVE or l.startswith("dag") for l in p["referenced_from"])]
    code_pin = [p for p in lean_live if "code/**" in p["referenced_from"] or "papers/**" in p["referenced_from"]]
    structured_outside = structured_atlas_lean_refs(repo)
    w(f"Lean: {len(structured_outside)} node `lean` fields and record `lean4` fields still name an atlas Lean file "
      f"(not counting `absent:` notes). {len(lean_live)} atlas Lean files are named by live files in some way: {len(dag_only)} only inside "
      f"`dag/derivation_dag.json` or its fragments (notes, statements, summaries), {len(code_pin)} by `code/**` or `papers/**`. "
      "A file named only in free text or in a hash pin backs no replay receipt and was not imported.")
    w("")

    # ---- non-Lean cited files
    def size_of(p):
        return p.get("size_bytes", p.get("size_bytes_before_removal", 0))

    cited_files = [p for p in paths if (p["exists_in_atlas"] and not p.get("is_dir") or p["path"] in gone_paths)
                   and sum(n for loc, n in p["referenced_from"].items() if loc in inv.LIVE)]
    w("## Files cited by live files, by kind")
    w("")
    w("| Kind | files | size | of which removed from the working tree |")
    w("|---|---|---|---|")
    kind_n = collections.Counter(); kind_b = collections.Counter(); kind_g = collections.Counter()
    for p in cited_files:
        kind_n[p["kind"]] += 1; kind_b[p["kind"]] += size_of(p); kind_g[p["kind"]] += p["path"] in gone_paths
    for k, n in kind_n.most_common():
        w(f"| {k} | {n} | {human(kind_b[k])} | {kind_g[k]} |")
    w("")
    dag_locs = ("dag nodes/records/routes (derivation_dag.json)", "dag fragments (sync inputs)")
    docs = [p for p in cited_files if p["kind"] in ("paper / document", "yaml claim register", "yaml (other)", "data (json/jsonl/csv)")
            and any(l in p["referenced_from"] for l in dag_locs)]
    docs_bytes = sum(size_of(p) for p in docs)
    w("## Recommended copy list (not copied in this change)")
    w("")
    w(f"The papers, claim registers and data files that DAG nodes and records cite as `source` come to {len(docs)} files, {human(docs_bytes)}. "
      f"{sum(1 for p in docs if p['path'] in gone_paths)} of them ({human(sum(size_of(p) for p in docs if p['path'] in gone_paths))}) are no longer in the sibling working tree and would be restored from its git history. "
      + ("That is over the 5 MB this change allows for non-Lean files, so **none of them was copied**. " if docs_bytes > 5 * 1024 * 1024 else "None of them was copied (this change copies Lean only). ")
      +
      "Recommended: copy them verbatim, keeping their atlas-relative path, to `sources/atlas/<atlas-relative path>` in one follow-up change, "
      "then rewrite the `source` fields with `dag/research/lean_replay_campaign/rewrite_refs.py` (extend its table; the files are byte-identical, so `:line` references stay valid). "
      "The complete list with sizes is in the JSON file (entries whose `kind` is a document, yaml or data file and that are cited from the DAG classes). The largest:")
    w("")
    w("| File | size | references |")
    w("|---|---|---|")
    for p in sorted(docs, key=lambda p: -size_of(p))[:25]:
        w(f"| `{p['path']}`{' (removed)' if p['path'] in gone_paths else ''} | {human(size_of(p))} | {p['reference_count']} |")
    w("")
    code = [p for p in cited_files if p["kind"] in ("Rust", "Python") and any(l in p["referenced_from"] for l in dag_locs)]
    w(f"Rust and Python files cited from node `rust` fields and record fields: {len(code)} files, "
      f"{human(sum(size_of(p) for p in code))} ({sum(1 for p in code if p['kind'] == 'Rust')} Rust, {sum(1 for p in code if p['kind'] == 'Python')} Python). "
      f"{sum(1 for p in code if p['path'].startswith('omega_engine/'))} of them are under `omega_engine/`. "
      "These were not copied; whether to cite an in-repo twin or record the citation as external is a decision for a reviewer.")
    w("")
    w("## Code that imports sibling packages")
    w("")
    imps = doc["python_imports_of_atlas_packages"]
    if imps:
        w("Python files here that `import` or `from ... import` a package of the sibling tree (not a path citation; the code would fail to import without the package):")
        w("")
        w("| Package | files | import statements |")
        w("|---|---|---|")
        for pkg, files_ in sorted(imps.items()):
            w(f"| `{pkg}` | {len(files_)} | {sum(files_.values())} |")
        w("")
        by_dir = collections.Counter("/".join(f.split("/")[:3]) for files_ in imps.values() for f in files_)
        w("Where they are (first three path components): "
          + ", ".join(f"`{d}` {n}" for d, n in by_dir.most_common(8)) + ".")
        w("")
    leaks, total_paths = cargo_leaks(repo)
    if leaks:
        w(f"`Cargo.toml` path dependencies (excluding sealed copies under `dag/results/**`): {total_paths} entries, {len(leaks)} leave the repository:")
        w("")
        for manifest_path, name, dep in leaks:
            w(f"- `{manifest_path}`: dependency `{name}`, `path = \"{dep}\"`")
        w("")
    else:
        w(f"No `Cargo.toml` outside `dag/results/**` has a `path =` dependency that leaves the repository ({total_paths} entries checked).")
    w("")
    w(f"{len(doc['absolute_path_mentions_files'])} files name an absolute `...\\the_symbol_game\\...` path in prose, scripts or receipts; they are listed in the JSON.")
    w("")

    # ---- verdicts
    w("## Verdict per atlas folder")
    w("")
    w("*SAFE TO DELETE* means: no live file of this repository cites an existing file of the folder, so deleting it changes nothing the DAG checks, the replay or the tests read. "
      "*ALREADY REMOVED* means the folder is gone from the sibling working tree and this repository still cites files that were in it. "
      "*NOT YET SAFE* names what would break. Sealed run artifacts under `dag/results/**` quote paths of their inputs; they carry their own copies of those inputs and are not a dependency.")
    w("")
    w("By top-level folder of the sibling tree (the answer to \"can this whole folder go\"):")
    w("")
    w("| Top-level folder | verdict | reason |")
    w("|---|---|---|")
    for top, names in sorted(top_level.items()):
        agg = {"live": 0, "live_kinds": collections.Counter(), "live_bytes": 0, "gone_kinds": collections.Counter(),
               "gone_bytes": 0, "gone_files": 0}
        for name in names:
            g = groups[name]
            agg["live"] += g["live"]
            agg["live_kinds"].update(g["live_kinds"])
            agg["live_bytes"] += g["live_bytes"]
            agg["gone_kinds"].update(g["gone_kinds"])
            agg["gone_bytes"] += g["gone_bytes"]
            agg["gone_files"] += g["gone_files"]
        v, why = verdict(agg)
        w(f"| `{top}` | **{v}** | {cell(why)} |")
    w("")
    w("Per paper or sub-folder (only folders with at least one path that resolves now or resolved before the removal commit; "
      "folders whose every cited path never resolved are left out, they hold nothing to lose):")
    w("")
    w("| Folder | verdict | reason |")
    w("|---|---|---|")
    for top, names in sorted(top_level.items()):
        for name in names:
            g = groups[name]
            if g["exist"] == 0 and g.get("removed", 0) == 0:
                continue
            v, why = verdict(g)
            w(f"| `{name}` | **{v}** | {cell(why)} |")
    w("")
    w("Folders of the sibling tree that no file here cites are not listed; nothing in this repository depends on them.")
    w("")
    w("### The QM and other papers (`omega_engine_atlas/coda_atlas/F004_papers/**`)")
    w("")
    fam = [n for n in groups if n.startswith("omega_engine_atlas/coda_atlas/F004_papers")]
    blocked = [n for n in fam if verdict(groups[n])[0] == "NOT YET SAFE"]
    removed_fam = [n for n in fam if verdict(groups[n])[0] == "ALREADY REMOVED"]
    blocker_kinds = collections.Counter()
    for n in blocked:
        blocker_kinds.update(groups[n]["live_kinds"])
    w(f"{len(removed_fam)} of the {len(fam)} paper folders listed above are ALREADY REMOVED (their cited files are in the sibling's git history only) and "
      f"{len(blocked)} are NOT YET SAFE. The files that block them: "
      + (", ".join(f"{n} {k}" for k, n in blocker_kinds.most_common()) or "none")
      + ". Deleting a blocked folder makes `validate_derivation_dag.py` (with file resolution) report the cited paths as missing.")
    w("")
    text = "\n".join(lines) + "\n"
    (out_dir / "atlas_dependency_inventory.md").write_text(text, encoding="utf-8", newline="\n")
    print("wrote", len(lines), "lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
