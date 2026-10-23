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


def cargo_leaks(repo: Path):
    import os
    root = str(repo.resolve())
    leaks, n = [], 0
    for dp, dn, fns in os.walk(repo):
        rel = os.path.relpath(dp, repo).replace("\\", "/")
        dn[:] = [d for d in dn if d not in (".git", "target", "b", ".lake", "node_modules") and not (rel + "/" + d).lstrip("./").startswith("dag/results")]
        if "Cargo.toml" in fns:
            text = (Path(dp) / "Cargo.toml").read_text(encoding="utf-8", errors="replace")
            for m in re.finditer(r'path\s*=\s*"([^"]+)"', text):
                n += 1
                target = os.path.normpath(os.path.join(dp, m.group(1)))
                if not target.startswith(root):
                    leaks.append(((Path(dp) / "Cargo.toml").relative_to(repo).as_posix(), m.group(1)))
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
    w("## What Part 1 imported")
    w("")
    files = manifest["files"]
    ported = [f for f in files if f.get("ports")]
    by_slug = collections.Counter(f["slug"] for f in files)
    w(f"All {len(files)} Lean files that DAG nodes and records cite outside this repository, together with their local (non-Mathlib) imports, "
      f"were copied to `lean4/Imported/<package>/<path under the package root>.lean` and registered as the non-default library `ImportedAtlas` "
      f"in `lean4/lakefile.lean`. {sum(1 for f in files if f['cited_directly'])} are cited directly; the others are dependencies. "
      "The package folder disambiguates files that share a stem in different atlas papers (`Paper.lean`, `Same.lean`, `SnTheorems.lean`, `Core.lean`). "
      "Every file carries a header with its original path, original sha256 and the import date. "
      f"All {len(files)} compile under Lean 4.35.0 with Mathlib `56a005855ea17e0b0958f73ec801ae140b0a1679`; "
      f"{len(ported)} needed a port for version drift ({', '.join('`' + f['repo_path'][len('lean4/'):] + '`' for f in ported) or 'none'}), recorded in its header and in "
      "[`lean4/Imported/import_manifest.json`](../../lean4/Imported/import_manifest.json). None contains `sorry`, `admit`, `axiom`, `native_decide` or `unsafe`.")
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
    w("Three cited paths were not imported because this repository already holds a file whose cited declarations have the same statements; "
      "the references now name the in-repo file:")
    w("")
    for k, v in rp.items():
        w(f"- `{k}` -> `{v}`")
    w("")
    w("The two cited `omega_engine_education/.../inputs/the_symbol_game/...` copies under `dag/results/` are sealed run inputs and were not touched.")
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
    lean_live = [p for p in paths if p["kind"] == "Lean" and (p["exists_in_atlas"] or p in gone) and not p.get("is_dir")
                 and any(l in p["referenced_from"] for l in inv.LIVE)]
    dag_only = [p for p in lean_live if all(l not in inv.LIVE or l.startswith("dag") for l in p["referenced_from"])]
    code_pin = [p for p in lean_live if "code/**" in p["referenced_from"] or "papers/**" in p["referenced_from"]]
    w(f"Lean: the Lean files that a node `lean` field or a record `lean4` field cites are all in `lean4/` now. {len(lean_live)} further atlas Lean files "
      f"are still named by live files, but not as a citation the evidence map resolves: {len(dag_only)} appear only inside `dag/derivation_dag.json` "
      "in free text (`absent: no local lean twin located for ...` notes, statements, summaries), and "
      f"{len(code_pin)} are named by `code/**` or `papers/**` (the `source_pin.json` hash pins of the QM code and two MUB6 test files). "
      "None of them backs a replay receipt, so they were not imported; the DAG already records them as absent twins.")
    w("")

    # ---- non-Lean cited files
    def size_of(p):
        return p.get("size_bytes", p.get("size_bytes_before_removal", 0))

    cited_files = [p for p in paths if (p["exists_in_atlas"] and not p.get("is_dir") or p in gone)
                   and sum(n for loc, n in p["referenced_from"].items() if loc in inv.LIVE)]
    w("## Files cited by live files, by kind")
    w("")
    w("| Kind | files | size | of which removed from the working tree |")
    w("|---|---|---|---|")
    kind_n = collections.Counter(); kind_b = collections.Counter(); kind_g = collections.Counter()
    for p in cited_files:
        kind_n[p["kind"]] += 1; kind_b[p["kind"]] += size_of(p); kind_g[p["kind"]] += p in gone
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
      f"{sum(1 for p in docs if p in gone)} of them ({human(sum(size_of(p) for p in docs if p in gone))}) are no longer in the sibling working tree and would be restored from its git history. "
      + ("That is over the 5 MB this change allows for non-Lean files, so **none of them was copied**. " if docs_bytes > 5 * 1024 * 1024 else "None of them was copied (this change copies Lean only). ")
      +
      "Recommended: copy them verbatim, keeping their atlas-relative path, to `sources/atlas/<atlas-relative path>` in one follow-up change, "
      "then rewrite the `source` fields with `dag/research/lean_replay_campaign/rewrite_refs.py` (extend its table; the files are byte-identical, so `:line` references stay valid). "
      "The complete list with sizes is in the JSON file (entries whose `kind` is a document, yaml or data file and that are cited from the DAG classes). The largest:")
    w("")
    w("| File | size | references |")
    w("|---|---|---|")
    for p in sorted(docs, key=lambda p: -size_of(p))[:25]:
        w(f"| `{p['path']}`{' (removed)' if p in gone else ''} | {human(size_of(p))} | {p['reference_count']} |")
    w("")
    code = [p for p in cited_files if p["kind"] in ("Rust", "Python") and any(l in p["referenced_from"] for l in dag_locs)]
    w(f"Rust and Python files cited from node `rust` fields and record fields: {len(code)} files, "
      f"{human(sum(size_of(p) for p in code))} ({sum(1 for p in code if p['kind'] == 'Rust')} Rust, {sum(1 for p in code if p['kind'] == 'Python')} Python). "
      "Most live in `omega_engine/` (the Rust crates); this repository has its own `code/rust` and `code/python`, and the in-repo twins are what the evidence map counts. "
      "Copying a sibling-crate file in would not make it build here; the honest options are to cite the in-repo twin or to record the citation as external. "
      "These were not copied.")
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
        w("These are in vendored governance contracts and test support (`code/python/governance/**`, `papers/core/**/tests/support/**`) and in tests; none is on the path that builds the DAG, the evidence map or the Lean replay.")
        w("")
    leaks, total_paths = cargo_leaks(repo)
    if leaks:
        w(f"`Cargo.toml` path dependencies (excluding sealed copies under `dag/results/**`): {total_paths} entries, {len(leaks)} leave the repository:")
        w("")
        for manifest_path, dep in leaks:
            w(f"- `{manifest_path}`: `path = \"{dep}\"`")
        w("")
        w("Every other path dependency points inside `code/rust`. The sealed copies of crates under `dag/results/**` carry absolute `the_symbol_game` paths in their `Cargo.toml`; they are archives, not built.")
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
    w(f"{len(removed_fam)} of the {len(fam)} paper folders listed above are ALREADY REMOVED (their cited files are in the sibling's git history only) and "
      f"{len(blocked)} are NOT YET SAFE; the blockers are documents, claim registers and data files "
      "that nodes cite as `source` (and the Rust and Python files the atlas holds), not Lean. After the follow-up copy to `sources/atlas/` and the matching `source` rewrite, "
      "the paper folders can be deleted. Until then, deleting them leaves the DAG internally consistent but makes `validate_derivation_dag.py` (with files) and the evidence map's "
      "document links report the sources as missing.")
    w("")
    text = "\n".join(lines) + "\n"
    (out_dir / "atlas_dependency_inventory.md").write_text(text, encoding="utf-8", newline="\n")
    print("wrote", len(lines), "lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
