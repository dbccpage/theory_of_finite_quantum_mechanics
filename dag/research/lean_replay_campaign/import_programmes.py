"""Import the Lean files of five sibling-tree programme folders into lean4/Imported, only where needed.

AuthorityEffect: None. Reads the sibling `the_symbol_game/lean4` (read-only), writes lean4/Imported/<Slug>/...,
lean4/Imported/import_manifest_programmes.json and prints the lake roots. Extends the ImportedAtlas machinery of
the first import; nothing in the sibling tree is changed.

    python -I -X utf8 import_programmes.py <repo> <sibling lean4 dir> <YYYY-MM-DD> [--write]

Decision rule for every sibling file considered:
  1. present: an identical file (sha256), a newline-equivalent file, or a file with the same module name is
     already a module of this repository (lean4/**, lean4/Imported/**) or a paper-local copy
     (papers/core/mub6/lean4/**). It is not imported; a module-name match with different content is recorded
     as an edition difference.
  2. import only if not present AND (a) a DAG node or record cites it, (b) a file being imported imports it,
     or (c) it belongs to the genesis / S(n) / MSS-N / pre-genesis / WDP / MUB6 / HCT programmes.
  3. Build output, .lake, .olean and vendored packages are never read.
Imports of an imported file resolve inside the sibling tree first; a target that is byte-identical to a module
already in this repository keeps naming that module, any other target is imported too.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path

SKIP_DIRS = {".lake", "build", ".git", "b", "lake-packages", "packages", "__pycache__", ".cache"}
EXTPKG = ("Mathlib", "Std", "Lean", "Init", "Batteries", "Aesop", "Qq", "ProofWidgets", "Plausible",
          "LeanSearchClient", "Cli", "ImportGraph")
IMP = re.compile(r"^(\s*import\s+)(.+)$")

# slug -> directory (relative to the sibling lean4 dir) that is the module root of the files in it
ROOTS = {
    "HigherCategoryTheory": "research_programs/higher_category_theory",
    "WdpReasoning": "research_programs/wdp_reasoning",
    "Mub6": "research_programs/mub6",
    "LevelEngine": "research_programs/level_engine",
    "QuantumMechanics": "quantum_mechanics",
    "SymbolGameLoose": "",
}
FOLDER_PROGRAMMES = {"higher_category_theory": "HCT", "mub6": "MUB6", "wdp_reasoning": "WDP",
                     "level_engine": None, "quantum_mechanics": None}

# loose files of lean4/ selected for the named programmes, with the reason
LOOSE_SELECTED = {
    "S(n)": ["SLevel", "SnTower", "SnSymbolGameAndPackets", "ShadowBoundary", "TowerZeta", "RuntimeLimits", "Sweeper",
             "ShadowFactorization", "TypedPacketShadow", "TriggerNotLicense", "LggrNonFactorization", "LGGR", "LGGR1",
             "LGGR2", "LGGR3", "Stage0LiftNecessity", "Stage1LiftNecessity", "LiftPatchSemantics", "FidelityAdequacy",
             "OperationTreeFold", "TerminalizerPolicy", "GrammarDepthCeiling", "FiniteConsequences", "LpWeakDuality",
             "Expressivity", "Family", "GrammarCeiling", "SymbolGame", "Lib"],
    "MSS-N": ["AntimorphicInvolution", "Level15AuthorityCalculus", "Level16IndObject", "Level17HodgeDecomposition",
              "Level18ZeroFloatLaw", "Level19IharaZetaQuarantine", "Level20AutopoieticCohomology", "Level21DiscreteRegge",
              "Level22FibredDependentContexts", "Level23SheafDescent", "Level80ScopedAuthorization", "TowerLadder",
              "TokenFrontier", "Demo3ProtocolInvariants"],
    "genesis": ["GenesisBellCertificate", "GenesisContinuation", "GenesisJoint", "GenesisJointOperations",
                "GenesisSimulation", "GenesisTrace", "NormalFormsCore"],
    "WDP": ["ReportRepair"],
}
LOOSE_REASON = {stem: prog for prog, stems in LOOSE_SELECTED.items() for stem in stems}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def norm(b: bytes) -> bytes:
    return b.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def lean_files(base: Path):
    for dp, dn, fns in os.walk(base):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fns:
            if f.endswith(".lean"):
                yield Path(dp) / f


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("sibling")
    ap.add_argument("date")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--decisions", default=None, help="write the per-file decision table here")
    a = ap.parse_args()
    repo, sg = Path(a.repo), Path(a.sibling)

    # ---- what the repository already has
    have: dict[str, tuple[str, str, str]] = {}
    for base in ("lean4", "papers/core/mub6/lean4"):
        for p in lean_files(repo / base):
            rel = p.relative_to(repo).as_posix()
            b = p.read_bytes()
            have[rel] = (sha(b), sha(norm(b)), p.stem)
    by_sha: dict[str, list[str]] = {}
    by_nsha: dict[str, list[str]] = {}
    by_stem: dict[str, list[str]] = {}
    for rel, (h, nh, stem) in have.items():
        by_sha.setdefault(h, []).append(rel)
        by_nsha.setdefault(nh, []).append(rel)
        by_stem.setdefault(stem, []).append(rel)

    def lake_module(rel: str) -> str | None:
        """module name of a repo file that is a module of the lake package"""
        if rel.startswith("lean4/") and rel.count("/") >= 1 and not rel.startswith("lean4/b/"):
            return rel[len("lean4/"):-len(".lean")].replace("/", ".")
        return None

    # ---- every sibling file of the folders considered
    files: dict[str, dict] = {}
    for slug, rel in ROOTS.items():
        base = sg / rel if rel else sg
        walker = lean_files(base) if rel else (p for p in sg.glob("*.lean"))
        for p in walker:
            key = p.relative_to(sg).as_posix()
            if not rel and "/" in key:
                continue
            b = p.read_bytes()
            files[key] = {"slug": slug, "root": rel, "path": key, "sha": sha(b), "nsha": sha(norm(b)), "bytes": b,
                          "stem": p.stem}
    for f in files.values():
        f["identical"] = by_sha.get(f["sha"], [])
        f["newline_equiv"] = [x for x in by_nsha.get(f["nsha"], []) if x not in f["identical"]]
        f["same_module_name"] = [x for x in by_stem.get(f["stem"], []) if x not in f["identical"] + f["newline_equiv"]]
        f["present"] = bool(f["identical"] or f["newline_equiv"])

    def resolve(f: dict, token: str) -> dict | None:
        """the sibling file that `import token` in file f names"""
        tail = Path(*token.split(".")).as_posix() + ".lean"
        order = [f["slug"]] + [s for s in ROOTS if s != f["slug"]]
        for slug in order:
            rel = ROOTS[slug]
            key = f"{rel}/{tail}" if rel else tail
            if key in files:
                return files[key]
        return None

    # ---- seeds
    seeds: dict[str, str] = {}
    for key, f in files.items():
        if f["present"]:
            continue
        folder = f["root"].split("/")[-1] if f["root"] else ""
        if f["slug"] in ("HigherCategoryTheory", "WdpReasoning", "Mub6"):
            if key.endswith("/lakefile.lean") or "/cli/" in key:
                continue
            if f["same_module_name"] and f["slug"] == "Mub6":
                continue  # an edition of a module already in lean4/
            seeds[key] = FOLDER_PROGRAMMES[folder]
        elif f["slug"] == "SymbolGameLoose" and f["stem"] in LOOSE_REASON:
            seeds[key] = LOOSE_REASON[f["stem"]]

    # ---- closure over imports
    chosen: dict[str, str] = dict(seeds)
    edges: dict[str, list[str]] = {}
    queue = list(seeds)
    unresolved: list[tuple[str, str]] = []
    keep_in_repo: dict[str, str] = {}
    while queue:
        key = queue.pop()
        f = files[key]
        text = f["bytes"].decode("utf-8", "replace")
        es = []
        for line in text.splitlines():
            m = IMP.match(line)
            if not m:
                continue
            for tok in m.group(2).split():
                tok = tok.strip("«»")
                if tok.split(".")[0] in EXTPKG:
                    continue
                g = resolve(f, tok)
                if g is None:
                    # a module of this repository?
                    cand = [x for x in have if lake_module(x) == tok]
                    if cand:
                        keep_in_repo[f"{key}:{tok}"] = cand[0]
                        continue
                    unresolved.append((key, tok))
                    continue
                twin = [x for x in g["identical"] + g["newline_equiv"] if lake_module(x)]
                if twin:
                    keep_in_repo[f"{key}:{tok}"] = twin[0]
                    es.append(g["path"])
                    continue
                es.append(g["path"])
                if g["path"] not in chosen:
                    chosen[g["path"]] = "import of " + key
                    queue.append(g["path"])
        edges[key] = es

    # ---- decision table
    decisions = []
    for key, f in sorted(files.items()):
        if key in chosen:
            d, why = "import", chosen[key] if key in seeds else chosen[key]
        elif f["present"]:
            d, why = "present", f"identical to {f['identical'][:1] or f['newline_equiv'][:1]}"
        elif f["same_module_name"] and f["slug"] == "Mub6":
            d, why = "present-by-module-name", f"module name already in repo as {f['same_module_name'][:1]}; content differs"
        else:
            d, why = "skip", "not cited, not imported by an imported file, not in a named programme"
        decisions.append({"path": key, "slug": f["slug"], "decision": d, "reason": why,
                          "same_module_name": f["same_module_name"][:2]})
    if a.decisions:
        Path(a.decisions).write_text(json.dumps(decisions, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    counts: dict[str, dict[str, int]] = {}
    for d in decisions:
        counts.setdefault(d["slug"], {}).setdefault(d["decision"], 0)
        counts[d["slug"]][d["decision"]] += 1
    print(json.dumps(counts, indent=1))
    print("unresolved imports:", unresolved[:10], len(unresolved))
    if not a.write:
        return 0

    manifest, roots = [], []
    for key in sorted(chosen):
        f = files[key]
        slug = f["slug"]
        base = f["root"]
        relmod = key[len(base) + 1:] if base else key
        relmod = relmod[:-len(".lean")]
        mod = f"Imported.{slug}.{relmod.replace('/', '.')}"
        newrel = f"lean4/Imported/{slug}/{relmod}.lean"
        text = f["bytes"].decode("utf-8").replace("\r\n", "\n")
        out, changes = [], []
        for line in text.split("\n"):
            m = IMP.match(line)
            if m:
                new = []
                for tok in m.group(2).split():
                    c = tok.strip("«»")
                    if c.split(".")[0] in EXTPKG:
                        new.append(tok)
                        continue
                    g = resolve(f, c)
                    twin = [x for x in (g["identical"] + g["newline_equiv"]) if lake_module(x)] if g else []
                    if g is None or twin:
                        target = lake_module(twin[0]) if twin else c
                        new.append(target)
                        if target != c:
                            changes.append(f"import {c} -> {target}")
                        continue
                    gslug, gbase = g["slug"], g["root"]
                    grel = (g["path"][len(gbase) + 1:] if gbase else g["path"])[:-len(".lean")]
                    target = f"Imported.{gslug}.{grel.replace('/', '.')}"
                    new.append(target)
                    changes.append(f"import {c} -> {target}")
                line = m.group(1) + " ".join(new)
            out.append(line)
        header = ("/- Imported from the sibling the_symbol_game lean4/ tree so that this repository carries its own Lean.\n"
                  f"   Original path : the_symbol_game/lean4/{key}\n"
                  f"   Original sha256: {f['sha']} (bytes as found)\n"
                  f"   Imported on    : {a.date}\n"
                  f"   Module         : {mod}\n"
                  f"   Reason         : {chosen[key]}\n"
                  "   Changes        : local import lines rewritten to the Imported namespace; line endings normalised to LF;\n"
                  "                    no declaration, proof or comment of the original was edited.\n"
                  "                    Port notes (version drift): none.\n"
                  "   AuthorityEffect: None. -/\n")
        data = (header + "\n".join(out)).encode("utf-8")
        dest = repo / newrel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        manifest.append({"original_path": f"lean4/{key}", "original_sha256": f["sha"], "original_size": len(f["bytes"]),
                         "repo_path": newrel, "repo_sha256": sha(data), "module": mod, "slug": slug,
                         "reason": chosen[key], "imports": sorted(edges.get(key, [])), "import_rewrites": changes,
                         "ports": []})
        roots.append(mod)
    (repo / "lean4/Imported/import_manifest_programmes.json").write_text(
        json.dumps({"schema_version": "imported_programmes_manifest.v1", "imported_on": a.date, "sibling": "the_symbol_game/lean4",
                    "decisions_summary": counts, "files": manifest}, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8", newline="\n")
    (repo / "lean4/Imported/roots_programmes.txt").write_text("\n".join(roots) + "\n", encoding="utf-8", newline="\n")
    print(len(manifest), "files written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
