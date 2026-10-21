#!/usr/bin/env python3
"""Generate the Unified DAG back-links of the corpus papers.

Reads ``dag/fragments/unified_dag.json`` (audited domain records and trunk
aliases) and ``dag/derivation_dag.json`` (trunk nodes) and writes, for the FSP,
MUB6, Majorana, Dressing Field Method (DFM) corpora and the two sign-problem
companion packages that back FSP records:

* a "Unified DAG" table (source id, NEW or ALIAS, TFQ record, DAG node, source
  claimed status, audited status, reconciliation) into each README and claim
  ledger (md and yaml where present);
* a dated 2026-10-21 change-log entry with the audit errata;
* a ``*_audit.jsonl`` sibling file for the FSP and MUB6 JSONL registers;
* a pointer to that file in the corpus ``.md`` index.

Every generated region sits between stable markers, so a rerun replaces it in
place and never duplicates it::

    <!-- BEGIN UNIFIED-DAG-BACKLINKS --> ... <!-- END UNIFIED-DAG-BACKLINKS -->
    # BEGIN UNIFIED-DAG-BACKLINKS ... # END UNIFIED-DAG-BACKLINKS      (yaml)

Original ledger and register text is never edited or removed; regions are
appended (or, for change logs, inserted above the newest entry).

``--refresh-manifests`` then brings the integrity manifests of the touched
packages up to date. Entries for edited files are re-hashed and a new file is
added in sorted position; entries for files that were already missing from the
checkout are left alone. The Majorana package uses its own
``verify_deposit.py --update-sums``.

Usage (from anywhere inside the repository)::

    python -I -X utf8 papers/core/tools/build_corpus_dag_backlinks.py
    python -I -X utf8 papers/core/tools/build_corpus_dag_backlinks.py --check
    python -I -X utf8 papers/core/tools/build_corpus_dag_backlinks.py --refresh-manifests

AuthorityEffect: None. Hash matches certify byte identity, not mathematics.
"""

from __future__ import annotations

import argparse
import bisect
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

AUDIT_DATE = "2026-10-21"
TOOL = "papers/core/tools/build_corpus_dag_backlinks.py"
UNIFIED = "dag/fragments/unified_dag.json"
DAG = "dag/derivation_dag.json"

REPO = Path(__file__).resolve().parents[3]

FSP_J = "papers/core/fsp/theory_of_finite_fsp.jsonl"
MUB_J = "papers/core/mub6/theory_of_finite_mub6.jsonl"
MAJ_M = "papers/core/majorana/the_majorana_problem.md"
DFM_M = "papers/ravera_dfm_dossier.md"

# Strength order used only to word the reconciliation column.
RANK = {
    "PROVED_LEAN": 6,
    "PROVED_PROSE": 5,
    "COMPUTATIONALLY_CHECKED": 4,
    "CONDITIONAL": 3,
    "IMPORTED_ASSUMPTION": 2,
    "OPEN": 1,
    "REFUTED": 0,
}

# --------------------------------------------------------------------------
# Errata found by the audit. One dated line per error; the original text is
# kept in place and corrected here, in the ledger/README and in the change log.
# --------------------------------------------------------------------------
ERRATA = {
    "fsp": [
        ("FSP-DERIV-033", "TFQ-1197",
         "The register says the Wilson Dirac operator has a non-negative determinant. "
         "gamma5-hermiticity only makes det D_W real; non-negativity holds for the "
         "two-degenerate-flavor product (det D_W)^2 >= 0, and a single-flavor det D_W can be "
         "negative. The cited `NonAbelianGaugeSigns.lean::wilson_dirac_gamma5_hermiticity_positivity` "
         "does not exist (that file has no Dirac operator). Audited status IMPORTED_ASSUMPTION."),
        ("FSP-DERIV-039", "TFQ-1203",
         "The register derives det D(i mu_I) >= 0 from gamma5 D(i mu_I) gamma5 = D(i mu_I)^dagger. "
         "That identity gives reality of the determinant, not positivity for a single Wilson flavor, "
         "and analytic continuation from imaginary to real mu is an extrapolation, not a sign-free "
         "route to real mu. The cited Lean name and `roberge_weiss_analytic_continuation` "
         "(su3_polyakov_loop.py) do not exist. Audited status IMPORTED_ASSUMPTION."),
        ("FSP-DERIV-045", "TFQ-1209",
         "The register calls d_tau = (1 + sqrt 5)/2 an 'exact rational quantum dimension'; d_tau is "
         "irrational, and the conclusion that braiding avoids sign degradation has no content in this "
         "package. The cited `FibonacciAnyonBraiding.lean::fibonacci_anyon_fusion_pentagon_solution` "
         "does not exist (`fibonacci_leakage_is_positive` is `decide` on 618 > 0). Exact ribbon data "
         "are pinned in trunk TFQ-0050. Audited status IMPORTED_ASSUMPTION."),
        ("FSP-DERIV-056", "TFQ-1220",
         "The Master Theorem (every finite system either admits a certified involution eliminating all "
         "negative weights in polynomial time or is NP-hard under Troyer-Wiese) is REFUTED as stated: "
         "involution pairing is sufficient, not necessary (`unequal_three_term_cancellation`, [2,-1,-1] "
         "sums to 0), and disjoint spectra (`disjoint_spectra_obstructs_involution`, triangle fixture) "
         "block equal-weight pairing without establishing hardness. The cited "
         "`FermionSignAll.lean::master_finite_fermion_sign_problem_theorem` does not exist; that file "
         "holds only `package_mechanization_total`, `rfl` on a String."),
        ("FSP-LEAN-CENSUS", "-",
         "Of the 56 `lean4_witness` names in the register, 1 (FSP-DERIV-005, "
         "`GenesisFspBridge.lean::swap_invariant_blind`) resolves to a declaration in this checkout. "
         "The Nicolai-map and Witten-index lemmas (FSP-DERIV-041, FSP-DERIV-042) are `rfl` placeholders "
         "(`t = t`, `idx = idx`) in `regge_wdw_core.lean`, which is not a lakefile root and is never built."),
    ],
    "mub6": [
        ("MUB6-DERIV-062", "TFQ-1231",
         "REFUTED. The register claims that no affine family through F_2 (x) F_3 contains a third basis "
         "unbiased to both the identity and the base matrix. The product triple I_6, F_2 (x) F_3 / sqrt 6, "
         "A_2 (x) C_2 (itself row-phase equivalent to F_2 (x) F_3) is pairwise unbiased (exact check "
         "`verify_three_bases`, squared overlaps 1/6; Jaming et al., arXiv:0902.0882, give an infinite "
         "family of such triplets from the Fourier family)."),
        ("MUB6-DERIV-064/065", "TFQ-1233/TFQ-1234",
         "The total of 180 real constraints in 72 coordinates is correct, but the split '36 normalization, "
         "36 against I_6, 108 against F_6 and B_3' is not the one in Lean. The Lean indexing "
         "(`total_equation_count`, `mu_equation_count`, `coordinate_count`) is 108 MU residuals (36 per "
         "basis of the fixed triple) plus 72 real and imaginary components of U*U - I. The count is not an "
         "independence, rank or overdetermination statement."),
        ("MUB6-DERIV-053", "TFQ-1223",
         "With X|j> = |j+1 mod 6> and Z|j> = w^j|j> one has Z X = w X Z, equivalently X Z = w^{-1} Z X. "
         "The register writes X Z = w Z X, which holds only under the opposite clock convention. There is "
         "no d = 6 Lean declaration for it, and no MUB count follows from the relation."),
        ("MUB6-DERIV-076", "TFQ-1253",
         "The register calls the quantity an l1 operator norm ||P S_6 P||_1 = 9. The computed (and Lean) "
         "quantity is |sum_j prod_r S_rj^{g_r}|^2 = 9 for each of the 20 balanced sign vectors g "
         "(`tao_all_balanced_masks`, `tao_all_balanced_laurent`). This is a finite evaluation for one "
         "matrix and gives no nonextension statement without Conjecture 2."),
        ("MUB6-DERIV-085/086", "TFQ-1254/TFQ-1255",
         "Both records carry PROVED_LEAN. DERIV-085 (no quartet in dimension six) and DERIV-086 "
         "(max MUB(6) = 3) are OPEN: no such declaration exists under `lean4/`, and the package itself "
         "states that N(6) = 3 remains open."),
        ("MUB6-LEAN-CENSUS", "-",
         "None of the 86 Lean names in the register's `languages.lean4` fields exists. The Lean that "
         "actually backs the audited records lives in the repository-root `lean4/` "
         "(ConcreteMub*, Szollosi*, MubTaoLaurent, Conjecture2GeneralMechanization, ...)."),
    ],
    "majorana": [
        ("MAJ-ISING-BRAID-CHECK", "TFQ-1171",
         "Monograph section 7.2 and ledger row MAJ-C7 present the Q(zeta_16) Ising braid identities as "
         "exact. The paper's Python check is floating point: `verify_yang_baxter_braid` builds complex "
         "numpy arrays with 1/sqrt 2 and tests `np.allclose(..., atol=1e-12)`, and "
         "`verify_quantum_dimensions` compares a float sqrt(2). F^2 = I and the hexagon are not checked "
         "in the paper code. Audited status OPEN for the exactness claim; the exact Majorana braid "
         "Yang-Baxter check is the crate twin MAJ-MAJORANA-BRAID-YB (TFQ-1172)."),
        ("README-CLAIM-RANGE", "-",
         "The README described the claim ledger as 'MAJ-C1 through MAJ-C17'; the ledger and "
         "`claim_ledger.yaml` run MAJ-C1 through MAJ-C20. Corrected in the README."),
        ("MAJ-LEAN-COVERAGE", "TFQ-1146/1154/1158/1161/1177-1179",
         "Ledger rows MAJ-C11, C13, C15, C17, C18, C19 and C20 carry [VERIFIED] but their Lean "
         "declarations are definitional restatements, `rfl`, or Nat positivity facts "
         "(for C20 `multiterminal_crosstalk_channels_pos` gives M(M-1)/2 > 0 for M >= 4, not >= 6). "
         "The original labels are kept; the audited statuses are in the table."),
    ],
    "dfm": [
        ("DFM-LEAN-NAMES", "TFQ-1119/1120/1121",
         "Three Lean names cited in section 3.6 and the section 4 table do not exist in "
         "`lean4/RaveraDfmFiniteToContinuum.lean`: `electroweak_su2_dressing_unitary_and_reduces_doublet` "
         "(closest: `ew_dfm_goldstone_elimination_on_sphere`, `ew_gaussian_4d_goldstone_elimination`), "
         "`weinberg_rational_projectors_and_custodial_rho_one` (actual: "
         "`weinberg_projectors_complete_orthogonal_idempotent`, `ew_custodial_rho_eq_one`) and "
         "`sm_anomaly_polynomials_vanish_iff_nc_eq_three` (actual: "
         "`sm_all_four_anomalies_cancel_at_nc3_and_fail_at_nc1` and the iff clauses of "
         "`sm_anomaly_polynomials_general_nc`)."),
        ("DFM-CODE-PATHS", "TFQ-1100..1137",
         "`code/ravera_dfm_dossier_replay.py` and `rust/ravera_dfm_finite_to_continuum.rs` do not exist "
         "in this checkout. The replay is `code/python/src/qm/ravera_dfm.py` (`verify_pillar1_*` to "
         "`verify_pillar9_*`, `evaluate_ravera_dfm_dossier`) with tests in "
         "`code/python/tests/test_ravera_dfm.py`; the Rust twin is "
         "`code/rust/src/qm/campaigns/ravera_dfm.rs`, which calls `evaluate_*_control` functions in the "
         "external `omega_quantum_physics` crate; the Lean file is `lean4/RaveraDfmFiniteToContinuum.lean`."),
        ("DFM-ANOMALY-COEFFICIENT", "TFQ-1121",
         "Theorem 3.6 item 3 prints the cubic hypercharge trace as (3/4)(3 - N_c). The retained Lean "
         "statement `sm_anomaly_polynomials_general_nc` gives (3 - N_c)/4 (value 1/2 at N_c = 1). The "
         "[SU(2)_L]^2 U(1)_Y coefficient (N_c - 3)/6 agrees. The companion change log "
         "`dag/research/ravera_dfm_changes.md` ('6 A_grav = 6(N_c - 3)') is also inconsistent: the "
         "gravitational coefficient vanishes identically."),
        ("DFM-QEM-CONVENTION", "TFQ-1118/1119",
         "The dossier uses Q = T_3 + Y with Y_Phi = 1/2, so Q_EM = diag(1, 0) on the doublet and the "
         "anomaly table uses Y_Q = 1/6, Y_L = -1/2; the companion `dag/research/ravera_dfm_docs.md` "
         "uses Q = T_3 + Y/2. The dossier convention is the one tied to the Lean anomaly table and is "
         "retained; the two normalizations must not be mixed."),
        ("DFM-ROOT-CONJUGATION", "TFQ-0399",
         "Definition 2.2 states that an unanchored shift acts as U^{dress} -> g(v_0)^{-1} U^{dress} g(v_0). "
         "With the stated u_T(v)^g = g(v) u_T(v) g(v_0)^{-1} and U^{dress} = u_T(v)^{-1} U u_T(u), the "
         "action is g(v_0) U^{dress} g(v_0)^{-1}, as in TFQ-0399."),
        ("DFM-CLOCK-IDENTITY", "TFQ-1116",
         "`dag/research/ravera_dfm_docs.md` writes the Page-Wootters identity as (I_C - S_C) (x) I_S, "
         "which disagrees with the dossier (D^dagger W D = S_C (x) I_S) and the code."),
        ("DFM-BIANCHI-GRIBOV-LEAN", "TFQ-1106/1130/1131/1136",
         "Lean names cited for the Bianchi identity (sections 3.2, 3.9) and for Gribov-copy elimination "
         "(section 3.8) prove weaker statements than the prose: "
         "`spanning_tree_nonabelian_mat2_factorization` is one fixed triangle with Mat2Rat links, not "
         "B_2(Q), N or T_2(Q); `su3_diagonal_klein_four_landau_gribov_copies` is rational arithmetic on "
         "diagonal entries (its Landau term is (d1-d1)+(d2-d2)+(d3-d3) = 0) and "
         "`spanning_tree_dfm_eliminates_gribov_copies` works in the commutative group of nonzero "
         "rationals, not SU(3); `bianchi_loop` is h1 h2 h2^{-1} h1^{-1} = I in the 2x2 boost plane. "
         "The Python replay is the substantive check for sections 3.2 and 3.8; the DFM audited "
         "statuses reflect this."),
    ],
    "meron": [],
    "hubbard": [],
}

# --------------------------------------------------------------------------
# Targets
# --------------------------------------------------------------------------
TARGETS = [
    dict(
        key="fsp", corpus=[FSP_J], only=None,
        label="FSP (papers/core/fsp)",
        register=FSP_J, register_idcol="id",
        audit_jsonl="papers/core/fsp/theory_of_finite_fsp_audit.jsonl",
        blocks=[
            ("papers/core/fsp/README.md", "readme"),
            ("papers/core/fsp/the_problem_of_the_fermion_sign_claim_ledger.md", "ledger"),
            ("papers/core/fsp/theory_of_finite_fsp.md", "pointer"),
            ("papers/core/fsp/the_problem_of_the_fermion_sign_change_log.md", "changelog_top"),
        ],
        manifests=None,
    ),
    dict(
        key="mub6", corpus=[MUB_J], only=None,
        label="MUB6 (papers/core/mub6)",
        register=MUB_J, register_idcol="derivation_id",
        audit_jsonl="papers/core/mub6/theory_of_finite_mub6_audit.jsonl",
        blocks=[
            ("papers/core/mub6/README.md", "readme"),
            ("papers/core/mub6/mub6_claim_ledger.md", "ledger"),
            ("papers/core/mub6/mub6_claim_ledger.yaml", "yaml"),
            ("papers/core/mub6/theory_of_finite_mub6.md", "pointer"),
            ("papers/core/mub6/mub6_change_log.md", "changelog_top"),
        ],
        manifests=("papers/core/mub6", ["manifest.sha256", "sha256sums"]),
    ),
    dict(
        key="majorana", corpus=[MAJ_M], only=None,
        label="Majorana (papers/core/majorana)",
        register=None, register_idcol=None, audit_jsonl=None,
        blocks=[
            ("papers/core/majorana/README.md", "readme"),
            ("papers/core/majorana/the_majorana_problem_claim_ledger.md", "ledger"),
            ("papers/core/majorana/claim_ledger.yaml", "yaml"),
            ("papers/core/majorana/the_majorana_problem_change_log.md", "changelog_end"),
        ],
        manifests=("papers/core/majorana", "own-tool"),
    ),
    dict(
        key="dfm", corpus=[DFM_M], only=None,
        label="Dressing Field Method dossier (papers/ravera_dfm_dossier.md)",
        register=None, register_idcol=None, audit_jsonl=None,
        blocks=[
            ("papers/ravera_dfm_dossier.md", "ledger"),
            ("papers/ravera_dfm_dossier_change_log.md", "changelog_file"),
        ],
        manifests=None,
    ),
    dict(
        key="meron", corpus=[FSP_J], only={"FSP-DERIV-028"},
        label="000_meron_sign_problem (backs FSP-DERIV-028)",
        register=None, register_idcol=None, audit_jsonl=None,
        blocks=[
            ("papers/core/000_meron_sign_problem/README.md", "readme"),
            ("papers/core/000_meron_sign_problem/paper_claim_ledger.md", "ledger"),
        ],
        manifests=("papers/core/000_meron_sign_problem", ["manifest.sha256", "sha256sums"]),
    ),
    dict(
        key="hubbard", corpus=[FSP_J], only={"FSP-DERIV-031"},
        label="001_hubbard_sign_problem (backs FSP-DERIV-031)",
        register=None, register_idcol=None, audit_jsonl=None,
        blocks=[
            ("papers/core/001_hubbard_sign_problem/README.md", "readme"),
            ("papers/core/001_hubbard_sign_problem/paper_claim_ledger.md", "ledger"),
        ],
        manifests=("papers/core/001_hubbard_sign_problem", ["sha256sums"]),
    ),
]

MD_BEGIN = "<!-- BEGIN UNIFIED-DAG-BACKLINKS -->"
MD_END = "<!-- END UNIFIED-DAG-BACKLINKS -->"
YML_BEGIN = "# BEGIN UNIFIED-DAG-BACKLINKS"
YML_END = "# END UNIFIED-DAG-BACKLINKS"


# --------------------------------------------------------------------------
# Data
# --------------------------------------------------------------------------
def load_json(rel: str):
    return json.loads((REPO / rel).read_text(encoding="utf-8"))


def read_jsonl(rel: str) -> list[dict]:
    return [json.loads(x) for x in (REPO / rel).read_text(encoding="utf-8").splitlines() if x.strip()]


class Data:
    def __init__(self) -> None:
        self.uni = load_json(UNIFIED)
        self.nodes = {n["id"]: n for n in load_json(DAG)["nodes"]}
        self.fsp = {r["id"]: r for r in read_jsonl(FSP_J)}
        self.mub = {r["derivation_id"]: r for r in read_jsonl(MUB_J)}
        self.maj_ledger = self._maj_ledger_labels()
        self._paper_cache: dict[str, str | None] = {}

    def _maj_ledger_labels(self) -> dict[str, str]:
        out: dict[str, str] = {}
        p = REPO / "papers/core/majorana/the_majorana_problem_claim_ledger.md"
        for line in p.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\|\s*\*\*(MAJ-[A-Z0-9-]+)\*\*.*\|\s*(\[[A-Z ]+\])\s*\|\s*$", line)
            if m:
                out[m.group(1)] = m.group(2).strip("[]")
        return out

    def paper_path(self, tfq: str) -> str | None:
        if tfq in self._paper_cache:
            return self._paper_cache[tfq]
        num = tfq.split("-")[-1]
        hits = sorted(glob.glob(str(REPO / "dag/derivations" / "*" / f"tfq_{num}_*.md")))
        rel = Path(hits[0]).relative_to(REPO).as_posix() if len(hits) == 1 else None
        self._paper_cache[tfq] = rel
        return rel

    def trunk_tfq(self, node_id: str) -> str | None:
        node = self.nodes.get(node_id)
        if not node:
            return None
        if re.fullmatch(r"TFQ-\d{4}", node_id):
            return node_id
        for t in node.get("tags", []):
            if re.fullmatch(r"TFQ-\d{4}", t):
                return t
        return None


def reconcile(claimed: str | None, audited: str) -> str:
    if claimed is None or claimed == "-":
        return "n/a"
    if claimed == audited:
        return "same"
    if "DEFINITION" in (claimed, audited):
        return "reclassified"
    rc, ra = RANK.get(claimed), RANK.get(audited)
    if rc is None or ra is None:
        return "changed"
    if ra < rc:
        return "lowered"
    if ra > rc:
        return "raised"
    return "reclassified"


def corpus_rows(d: Data, t: dict) -> list[dict]:
    rows: list[dict] = []
    for rec in d.uni["domain_records"]:
        if rec["corpus"] not in t["corpus"]:
            continue
        if t["only"] is not None and rec["source_id"] not in t["only"]:
            continue
        rows.append(dict(
            source_id=rec["source_id"], kind="NEW", tfq=rec["record_id"], node=rec["node_id"],
            claimed=rec["source_claimed_status"], audited=rec["status"],
            reconciliation=reconcile(rec["source_claimed_status"], rec["status"]),
            note=(rec["audit"].strip() or rec["obligation"].strip()),
            obligation=rec["obligation"].strip(),
        ))
    for al in d.uni["domain_aliases"]:
        if al["corpus"] not in t["corpus"]:
            continue
        if t["only"] is not None and al["source_id"] not in t["only"]:
            continue
        node = d.nodes[al["alias_of"]]
        sid = al["source_id"]
        if al["corpus"] == FSP_J:
            claimed = d.fsp.get(sid, {}).get("status")
        elif al["corpus"] == MUB_J:
            claimed = "PROVED_LEAN" if d.mub.get(sid, {}).get("languages", {}).get("lean4") else None
        elif al["corpus"] == MAJ_M:
            claimed = d.maj_ledger.get(sid)
        else:
            claimed = None
        rows.append(dict(
            source_id=sid, kind="ALIAS", tfq=d.trunk_tfq(al["alias_of"]) or "-", node=al["alias_of"],
            claimed=claimed or "-", audited=node["status"], reconciliation="restated in trunk",
            note=al["alias_note"].strip(), obligation="",
        ))
    rows.sort(key=lambda r: natural_key(r["source_id"]))
    return rows


def natural_key(s: str):
    return [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", s)]


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------
def rel_link(from_file: str, target: str) -> str:
    return os.path.relpath(REPO / target, (REPO / from_file).parent).replace(os.sep, "/")


def md_table(d: Data, rows: list[dict], file_rel: str) -> str:
    out = ["| Source id | Kind | TFQ record | DAG node | Source claimed | Audited | Reconciliation |",
           "|---|---|---|---|---|---|---|"]
    for r in rows:
        tfq = r["tfq"]
        cell = tfq
        if tfq != "-" and "/" not in tfq:
            p = d.paper_path(tfq)
            if p:
                cell = f"[{tfq}]({rel_link(file_rel, p)})"
        out.append(f"| `{r['source_id']}` | {r['kind']} | {cell} | `{r['node']}` | "
                   f"{r['claimed']} | **{r['audited']}** | {r['reconciliation']} |")
    return "\n".join(out)


def summary(rows: list[dict]) -> str:
    new = [r for r in rows if r["kind"] == "NEW"]
    ali = [r for r in rows if r["kind"] == "ALIAS"]
    c = Counter(r["reconciliation"] for r in new)
    parts = [f"{len(new)} NEW records and {len(ali)} ALIAS rows"]
    if new:
        parts.append(", ".join(f"{c[k]} {k}" for k in
                               ("same", "lowered", "raised", "reclassified", "changed", "n/a") if c.get(k)))
    text = "; ".join(parts) + "."
    refuted = [r["source_id"] for r in new if r["audited"] == "REFUTED"]
    if refuted:
        text += " REFUTED: " + ", ".join(f"`{x}`" for x in refuted) + "."
    return text


def intro(t: dict, rows: list[dict], kind: str) -> str:
    base = (
        f"Audit of {AUDIT_DATE}. The unified derivation DAG (`{UNIFIED}`) folds the records of this "
        "corpus into one graph: a record with no trunk counterpart is a NEW application-branch node "
        "with its own TFQ record; a restatement of a trunk step is an ALIAS row that points to the "
        "trunk node. *Source claimed* is the status the source asserted; *Audited* is the status the "
        "audit assigned against what is actually in this checkout (Lean declarations resolved, "
        "replays rerun, statements compared). The original claims, labels and text of this document are kept "
        "unchanged. A status below the source claim means the claim is not established as stated; it "
        "does not mean the underlying mathematics is false (only REFUTED means that). "
        "For an ALIAS row the audited column is the status of the trunk node, which is the authority "
        "for the restated step. "
        f"Regenerate with `python -I -X utf8 {TOOL}`."
    )
    if t["key"] == "mub6":
        base += (" The MUB6 register has no status field; the claimed status of its records is "
                 "PROVED_LEAN because each cites a Lean name. Rows whose id is not a `MUB6-DERIV-*` "
                 "id come from the claim ledger, the paper or the atlas.")
    if t["only"]:
        base += (f" This package backs the FSP register record(s) {', '.join(sorted(t['only']))}; "
                 "only those rows are listed here, the full table is in `papers/core/fsp/`.")
    return base + "\n\n" + summary(rows)


def errata_md(t: dict) -> str:
    items = ERRATA.get(t["key"], [])
    if not items:
        return ""
    out = [f"### Audit errata ({AUDIT_DATE})", ""]
    for sid, tfq, text in items:
        ref = sid if tfq == "-" else f"{sid}, {tfq}"
        out.append(f"- {AUDIT_DATE} ERRATUM ({ref}): {text}")
    return "\n".join(out)


def block_md(d: Data, t: dict, rows: list[dict], file_rel: str, kind: str) -> str:
    parts = [MD_BEGIN, f"<!-- Generated by {TOOL}; edit the tool, not this region. -->", "",
             "## Unified DAG", "", intro(t, rows, kind), "", md_table(d, rows, file_rel)]
    if kind == "ledger" and ERRATA.get(t["key"]):
        parts += ["", errata_md(t)]
    parts += ["", MD_END]
    return "\n".join(parts)


def block_pointer(t: dict, rows: list[dict]) -> str:
    name = Path(t["audit_jsonl"]).name
    return "\n".join([
        MD_BEGIN, f"<!-- Generated by {TOOL}; edit the tool, not this region. -->", "",
        "## Unified DAG audit", "",
        f"Audit of {AUDIT_DATE}. The records of this register are left exactly as written. Their audited "
        f"status, DAG node and TFQ record are in the sibling file [`{name}`]({name}), one row per "
        f"record ({summary(rows)}). The same mapping is tabulated in the README and the claim ledger "
        "under the heading \"Unified DAG\".", "", MD_END])


def block_changelog(t: dict, rows: list[dict], with_heading: bool = True) -> str:
    items = ERRATA.get(t["key"], [])
    lines = [MD_BEGIN, f"<!-- Generated by {TOOL}; edit the tool, not this region. -->", ""]
    if with_heading:
        lines += [f"## {AUDIT_DATE}: unified-DAG audit and ledger reconciliation", ""]
    lines += [
        f"- Audited every record of {t['label']} against the unified derivation DAG "
        f"(`{UNIFIED}`): {summary(rows)}",
        "- Added a \"Unified DAG\" section (source id, TFQ record, DAG node, source-claimed and audited "
        "status, reconciliation; ALIAS rows point to the trunk node) to "
        + ("the dossier itself, which has no separate README or ledger" if t["key"] == "dfm"
           else "the README and the claim ledger")
        + ", generated by `" + TOOL + "`. No original claim text, label or record was edited or "
        "deleted; claims stronger than their audited status keep their text and gain the audited "
        "column.",
    ]
    if t.get("audit_jsonl"):
        lines.append(f"- Added the sibling `{Path(t['audit_jsonl']).name}` (one row per record: source id, "
                     "audited status, DAG node, TFQ id, audit note) and a pointer in the corpus index. "
                     "The original register is unchanged.")
    if t["manifests"]:
        lines.append("- Integrity manifests were refreshed for the files edited here "
                     "(see the commit that carries this entry).")
    if items:
        lines += ["", "Errata:"]
        for sid, tfq, text in items:
            ref = sid if tfq == "-" else f"{sid}, {tfq}"
            lines.append(f"- {AUDIT_DATE} ERRATUM ({ref}): {text}")
    lines += ["", MD_END]
    return "\n".join(lines)


def yaml_q(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def block_yaml(t: dict, rows: list[dict]) -> str:
    out = [YML_BEGIN, f"# Generated by {TOOL}; edit the tool, not this region.",
           "unified_dag_audit:", f"  audited_on: {yaml_q(AUDIT_DATE)}", f"  source: {yaml_q(UNIFIED)}",
           f"  summary: {yaml_q(re.sub('`', '', summary(rows)))}", "  records:"]
    for r in rows:
        out += [f"    - source_id: {yaml_q(r['source_id'])}", f"      kind: {yaml_q(r['kind'])}",
                f"      tfq: {yaml_q(r['tfq'])}", f"      dag_node: {yaml_q(r['node'])}",
                f"      source_claimed_status: {yaml_q(r['claimed'])}",
                f"      audited_status: {yaml_q(r['audited'])}",
                f"      reconciliation: {yaml_q(r['reconciliation'])}"]
    items = ERRATA.get(t["key"], [])
    if items:
        out.append("  errata:")
        for sid, tfq, text in items:
            out += [f"    - id: {yaml_q(sid)}", f"      tfq: {yaml_q(tfq)}", f"      date: {yaml_q(AUDIT_DATE)}",
                    f"      text: {yaml_q(text)}"]
    out.append(YML_END)
    return "\n".join(out)


# --------------------------------------------------------------------------
# File editing with stable markers
# --------------------------------------------------------------------------
def apply_block(text: str, block: str, begin: str, end: str, where: str) -> str:
    """Replace the marked region, or insert it ('end', or 'top' before the first '## ')."""
    i = text.find(begin)
    if i != -1:
        j = text.find(end, i)
        if j == -1:
            raise SystemExit(f"unterminated marker {begin!r}")
        return text[:i] + block + text[j + len(end):]
    if where == "top":
        m = re.search(r"^## ", text, re.M)
        if not m:
            raise SystemExit("no '## ' heading to insert above")
        return text[:m.start()] + block + "\n\n" + text[m.start():]
    return text.rstrip("\n") + "\n\n" + block + "\n"


def write_if_changed(rel: str, new: str) -> bool:
    p = REPO / rel
    old = p.read_text(encoding="utf-8") if p.exists() else None
    if old == new:
        return False
    with p.open("w", encoding="utf-8", newline="\n") as f:
        f.write(new)
    return True


def audit_jsonl(d: Data, t: dict, rows: list[dict]) -> str:
    by_id = {r["source_id"]: r for r in rows}
    register = read_jsonl(t["register"])
    order = [r[t["register_idcol"]] for r in register]
    extra = [r["source_id"] for r in rows if r["source_id"] not in set(order)]
    out = []
    for sid in order + extra:
        r = by_id.get(sid)
        if r is None:
            raise SystemExit(f"register record {sid} has no unified-DAG row")
        row = {
            "source_id": sid,
            "record_kind": "register_record" if sid in set(order) else "ledger_or_paper_claim",
            "kind": r["kind"],
            "audited_status": r["audited"],
            "source_claimed_status": r["claimed"],
            "reconciliation": r["reconciliation"],
            "dag_node": r["node"],
            "tfq_id": None if r["tfq"] == "-" else r["tfq"],
            "audit_note": r["note"],
        }
        if r["obligation"]:
            row["open_obligation"] = r["obligation"]
        row["audited_on"] = AUDIT_DATE
        row["dag_source"] = UNIFIED
        out.append(json.dumps(row, ensure_ascii=False))
    return "\n".join(out) + "\n"


def changelog_file_text(t: dict, rows: list[dict]) -> str:
    return ("# Change log: The Dressing Field Method on Finite Graphs and Simplicial Complexes "
            "(papers/ravera_dfm_dossier.md)\n\nAuthorityEffect: None.\n\n"
            "The dossier itself carries no change log in `papers/`; earlier versions are recorded in "
            "`dag/research/ravera_dfm_changes.md`.\n\n" + block_changelog(t, rows) + "\n")


def run_target(d: Data, t: dict, check: bool) -> list[str]:
    rows = corpus_rows(d, t)
    changed: list[str] = []
    touched: list[str] = []
    for rel, kind in t["blocks"]:
        p = REPO / rel
        if kind == "changelog_file":
            new = changelog_file_text(t, rows) if not p.exists() else apply_block(
                p.read_text(encoding="utf-8"), block_changelog(t, rows), MD_BEGIN, MD_END, "end")
        else:
            text = p.read_text(encoding="utf-8")
            if kind in ("readme", "ledger"):
                new = apply_block(text, block_md(d, t, rows, rel, kind), MD_BEGIN, MD_END, "end")
            elif kind == "pointer":
                new = apply_block(text, block_pointer(t, rows), MD_BEGIN, MD_END, "end")
            elif kind == "yaml":
                new = apply_block(text, block_yaml(t, rows), YML_BEGIN, YML_END, "end")
            elif kind == "changelog_top":
                new = apply_block(text, block_changelog(t, rows), MD_BEGIN, MD_END, "top")
            elif kind == "changelog_end":
                new = apply_block(text, block_changelog(t, rows), MD_BEGIN, MD_END, "end")
            else:
                raise SystemExit(kind)
        touched.append(rel)
        if check:
            old = p.read_text(encoding="utf-8") if p.exists() else None
            if old != new:
                changed.append(rel)
        elif write_if_changed(rel, new):
            changed.append(rel)
    if t["audit_jsonl"]:
        new = audit_jsonl(d, t, rows)
        touched.append(t["audit_jsonl"])
        p = REPO / t["audit_jsonl"]
        old = p.read_text(encoding="utf-8") if p.exists() else None
        if check:
            if old != new:
                changed.append(t["audit_jsonl"])
        elif write_if_changed(t["audit_jsonl"], new):
            changed.append(t["audit_jsonl"])
    t["_touched"] = touched
    return changed


# --------------------------------------------------------------------------
# Manifests
# --------------------------------------------------------------------------
def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def refresh_one(root: Path, manifest: str, files: list[str]) -> list[str]:
    mp = root / manifest
    if not mp.exists():
        return []
    lines = mp.read_text(encoding="utf-8").splitlines()
    paths = [ln[66:] for ln in lines]
    is_sorted = paths == sorted(paths)
    msgs: list[str] = []
    for rel in files:
        f = root / rel
        if not f.is_file():
            continue
        digest = sha256_file(f)
        entry = f"{digest}  {rel}"
        if rel in paths:
            i = paths.index(rel)
            if lines[i] != entry:
                lines[i] = entry
                msgs.append(f"{manifest}: updated {rel}")
        else:
            i = bisect.bisect_left(paths, rel) if is_sorted else len(paths)
            lines.insert(i, entry)
            paths.insert(i, rel)
            msgs.append(f"{manifest}: added {rel}")
    if msgs:
        with mp.open("w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines) + "\n")
    return msgs


def refresh_manifests(targets: list[dict]) -> list[str]:
    msgs: list[str] = []
    for t in targets:
        if not t["manifests"]:
            continue
        pkg, names = t["manifests"]
        root = REPO / pkg
        if names == "own-tool":
            r = subprocess.run([sys.executable, "-I", "-X", "utf8", "verify_deposit.py", "--update-sums"],
                               cwd=root, capture_output=True, text=True, encoding="utf-8")
            msgs.append(f"{pkg}: verify_deposit.py --update-sums -> {r.stdout.strip() or r.stderr.strip()}")
            if r.returncode:
                raise SystemExit(f"manifest tool failed in {pkg}")
            continue
        files = [Path(x).relative_to(pkg).as_posix() for x in t["_touched"] if x.startswith(pkg + "/")]
        for name in names:
            msgs += [f"{pkg}/{m}" for m in refresh_one(root, name, files)]
        # sha256sums may list the manifest itself (mub6: manifest.sha256; 000: MANIFEST.sha256).
        sums = root / "sha256sums"
        if "manifest.sha256" in names and sums.exists():
            lines = sums.read_text(encoding="utf-8").splitlines()
            digest = sha256_file(root / "manifest.sha256")
            dirty = False
            for i, ln in enumerate(lines):
                if ln[66:].lower() == "manifest.sha256" and ln[:64] != digest:
                    lines[i] = f"{digest}  {ln[66:]}"
                    msgs.append(f"{pkg}/sha256sums: updated {ln[66:]}")
                    dirty = True
            if dirty:
                with sums.open("w", encoding="utf-8", newline="\n") as fh:
                    fh.write("\n".join(lines) + "\n")
    return msgs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true", help="exit 1 if any generated region is stale")
    ap.add_argument("--refresh-manifests", action="store_true",
                    help="update integrity manifests of the touched packages")
    ap.add_argument("--only", action="append", help="target key (fsp, mub6, majorana, dfm, meron, hubbard)")
    args = ap.parse_args()
    d = Data()
    targets = [t for t in TARGETS if not args.only or t["key"] in args.only]
    stale: list[str] = []
    for t in targets:
        changed = run_target(d, t, args.check)
        for rel in changed:
            print(("STALE " if args.check else "wrote ") + rel)
        stale += changed
    if args.refresh_manifests and not args.check:
        for m in refresh_manifests(targets):
            print("manifest " + m)
    if args.check:
        if stale:
            print(f"{len(stale)} generated region(s) are stale; rerun without --check")
            return 1
        print("all generated regions are current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
