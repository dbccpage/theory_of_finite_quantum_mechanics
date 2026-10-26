"""Check local teaching links in the four requested foundation estates.

Optional repair changes only moved links whose destination actually exists,
and qualified current documentation paths. It does not establish mathematical
claims, execute notebooks, refresh frozen pins, or check remote URLs/anchors.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ESTATES = (
    "002_s_n",
    "003_minimal_symbol_system_n_mssn",
    "001_genesis",
    "004_oepfp",
    "006_oewdp",
    "007_oelggr",
    "008_oeop",
    "009_oeeis",
    "010_oepciv",
)
MOVED = {
    "0_s_n": "002_s_n",
    "1_minimal_symbol_system_n_mssn": "003_minimal_symbol_system_n_mssn",
    "010_minimal_symbol_system_n_mssn": "003_minimal_symbol_system_n_mssn",
    "2_genesis": "001_genesis",
    "3_the_symbol_game_proposal_fidelity_protocol_pfp": "004_oepfp",
    "030_the_symbol_game_proposal_fidelity_protocol_pfp": "004_oepfp",
    "4_prompt_civilization_and_lamarckian_evolution": "010_oepciv",
    "040_prompt_civilization_and_lamarckian_evolution": "010_oepciv",
    "5_epistemic_immune_system_eis": "009_oeeis",
    "050_epistemic_immune_system_eis": "009_oeeis",
    "6_genesis_ongoing": "005_genesis_ongoing",
    "060_genesis_ongoing": "005_genesis_ongoing",
    "7_witnessed_difference_programme_wdp": "006_oewdp",
    "070_witnessed_difference_programme_wdp": "006_oewdp",
    "8_calculus_of_obstruction_descent_and_authority": "080_calculus_of_obstruction_descent_and_authority",
    "9_workflows_agents_skills_was_multicategories_and_operads": "008_oeop",
    "090_workflows_agents_skills_was_multicategories_and_operads": "008_oeop",
    "10_local_green_global_red": "007_oelggr",
    "100_local_green_global_red": "007_oelggr",
    "14_discrete_deformation_calculus_ddc": "006_oewdp/0_ddc",
    "140_discrete_deformation_calculus_ddc": "006_oewdp/0_ddc",
    "15_normal_forms": "014_normal_forms",
    "13_normal_forms": "014_normal_forms",
    "4_genesis_ongoing": "005_genesis_ongoing",
}
LINK = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")
SN_TOPICS = {
    "sn_real_simplicial.md": "realizations/simplicial",
    "sn_real_logic.md": "realizations/logic",
    "sn_real_category.md": "realizations/category",
    "sn_real_dynamics.md": "realizations/dynamics",
    "sn_real_epistemic.md": "realizations/epistemic",
    "sn_app_metric_simplices.md": "applications/physics/regge_metric.md",
    "sn_app_regge_curvature.md": "applications/physics/discrete_4d_regge.md",
    "sn_s21_topological_query.md": "applications/databases/s21_topological_query.md",
    "sn_s24_session_types.md": "applications/protocols/s24_session_types.md",
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def files(root: Path):
    def fail(error):
        raise error

    for directory, folders, names in os.walk(root, onerror=fail, followlinks=False):
        for name in folders + names:
            path = Path(directory) / name
            status = path.lstat()
            if path.is_symlink() or getattr(status, "st_file_attributes", 0) & 0x400:
                raise ValueError(f"symlink/reparse teaching path refused: {path}")
        folders[:] = [
            name
            for name in folders
            if name not in {"__pycache__", ".lake", "target", ".ipynb_checkpoints"}
        ]
        for name in names:
            path = Path(directory) / name
            if path.suffix in {".md", ".yaml", ".yml", ".ipynb"}:
                yield path


def relocate(text: str) -> str:
    for old, new in MOVED.items():
        text = text.replace(
            f"omega_engine_education/documentation/{old}/",
            f"omega_engine_education/documentation/{new}/",
        )
    return text


def check_text(text: str, source: Path, repo: Path, repair: bool, broken: list, repairs: list):
    def link(match):
        raw = match.group(1).strip()
        destination = raw.strip("<>").split(' "', 1)[0]
        parts = urlsplit(destination)
        if parts.scheme not in {"", "file"} or parts.netloc or not parts.path:
            return match.group(0)
        path = unquote(parts.path).replace("\\", "/")
        if parts.scheme == "file":
            marker = "/the_symbol_game/"
            if marker not in path:
                return match.group(0)
            path = path.split(marker, 1)[1]
            current = repo / path
        else:
            current = (source.parent / path).resolve()
        if current.exists() and parts.scheme != "file":
            return match.group(0)
        candidates = []
        components = path.split("/")
        moved_components = [MOVED.get(component, component) for component in components]
        candidates.append((source.parent / "/".join(moved_components)).resolve())
        for marker in ("omega_engine_education", "omega_engine_atlas", "omega_engine"):
            if marker in moved_components:
                candidates.append(
                    repo.joinpath(*moved_components[moved_components.index(marker) :])
                )
        for name in (*ESTATES, *MOVED.values()):
            if name in moved_components:
                candidates.append(
                    repo
                    / "omega_engine_education"
                    / "documentation"
                    / Path(*moved_components[moved_components.index(name) :])
                )
        # References copied into nested curriculum pages still name the same
        # estate-local primitive/image directories, but with the wrong depth.
        estate = next((parent for parent in source.parents if parent.name in ESTATES), None)
        if estate is not None:
            for marker in (
                "primitives",
                "_images",
                "core",
                "levels",
                "realizations",
                "normal_forms",
                "applications",
            ):
                if marker in moved_components:
                    candidates.append(
                        estate.joinpath(*moved_components[moved_components.index(marker) :])
                    )
            if moved_components[-1] in {"genesis.md", "sn.md", "0_mssn.md"}:
                candidates.append(estate / moved_components[-1])
            # Former curriculum topic locators now point at their indexed
            # canonical page. Require one page and its matching level field.
            topic = re.fullmatch(r"(mssn|gen)_(\d{2,3})_[a-z0-9_]+\.md", moved_components[-1])
            if topic and (
                (topic[1] == "mssn" and estate.name == ESTATES[1])
                or (topic[1] == "gen" and estate.name == ESTATES[2])
            ):
                level = int(topic[2])
                pages = list((estate / "levels").glob(f"level_{level:02d}_*.md"))
                if len(pages) == 1 and re.search(
                    rf"^level:\s*{level}\s*$", pages[0].read_text(encoding="utf-8"), re.M
                ):
                    candidates.append(pages[0])
            core = re.fullmatch(r"sn_s(0[0-6])_[a-z0-9_]+\.md", moved_components[-1])
            if core and estate.name == ESTATES[0]:
                pages = list((estate / "core").glob(f"s{core[1]}_*.md"))
                if len(pages) == 1:
                    candidates.append(pages[0])
            if estate.name == ESTATES[0] and "lesson_520_" in moved_components[-1]:
                candidates.append(
                    source.parent.parent
                    / "notebooks"
                    / moved_components[-1].replace("lesson_520_", "lesson_020_")
                )
            if estate.name == ESTATES[0] and moved_components[-1] in SN_TOPICS:
                candidates.append(estate / SN_TOPICS[moved_components[-1]])
        for candidate in candidates:
            if candidate.exists() and candidate.is_relative_to(repo):
                relative = os.path.relpath(candidate, source.parent).replace("\\", "/")
                if parts.fragment:
                    relative += "#" + parts.fragment
                if repair:
                    repairs.append(
                        {
                            "source": source.relative_to(repo).as_posix(),
                            "old": destination,
                            "new": relative,
                        }
                    )
                    return match.group(0).replace(match.group(1), relative)
        broken.append({"source": source.relative_to(repo).as_posix(), "target": destination})
        return match.group(0)

    # Leave examples inside fenced code untouched; those are not live links.
    blocks = re.split(r"(```[^\n]*\n.*?\n```)", text, flags=re.S)
    for i in range(0, len(blocks), 2):
        blocks[i] = LINK.sub(link, blocks[i])
    return "".join(blocks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--repair-moved-links", action="store_true")
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    repo = args.repo.resolve(strict=True)
    broken, repairs, bindings = [], [], []
    for estate in ESTATES:
        for source in sorted(files(repo / "omega_engine_education" / "documentation" / estate)):
            before = source.read_bytes()
            text = before.decode("utf-8")
            if text.startswith("\ufeff"):
                raise ValueError(f"BOM refused: {source}")
            if source.suffix == ".ipynb":
                notebook = json.loads(text)
                changed = False
                for cell in notebook["cells"]:
                    if cell["cell_type"] == "markdown":
                        body = "".join(cell["source"])
                        revised = check_text(
                            body, source, repo, args.repair_moved_links, broken, repairs
                        )
                        if revised != body:
                            cell["source"] = revised.splitlines(keepends=True)
                            changed = True
                if changed:
                    text = json.dumps(notebook, ensure_ascii=False, indent=1) + "\n"
            else:
                if args.repair_moved_links:
                    text = relocate(text)
                if source.suffix == ".md":
                    text = check_text(text, source, repo, args.repair_moved_links, broken, repairs)
            after = text.encode("utf-8")
            if args.repair_moved_links and after != before:
                source.write_bytes(after)
            bindings.append(
                {
                    "path": source.relative_to(repo).as_posix(),
                    "sha256_before": digest(before),
                    "sha256_after": digest(source.read_bytes()),
                }
            )
    report = {
        "authority_effect": "None",
        "estates": ESTATES,
        "files": bindings,
        "repairs": repairs,
        "broken_local_links": broken,
        "scope": "Local file/directory link targets only; excludes remote URLs, anchors, code cells and mathematical/learning claims.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"{len(bindings)} files; {len(repairs)} link repairs; {len(broken)} unresolved local links"
    )
    raise SystemExit(bool(broken))


if __name__ == "__main__":
    main()
