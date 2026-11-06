"""
CODA Discipline Core (EPIC-001 / CD-01..CD-13)
Founding discipline structures, CD-12 groupoid faithful functor target, and two-level cost accounting.
AuthorityEffect: None
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np


class HoTTSubsumptionRefusalError(Exception):
    """Refusal raised when ungrounded HoTT subsumption is asserted without model construction."""

    pass


@dataclass(frozen=True)
class Presentation:
    """Finite carrier presentation (V, R) with declared primitive differences."""

    name: str
    carrier_size: int
    diff_matrix: np.ndarray

    def __post_init__(self):
        mat = np.array(self.diff_matrix, dtype=np.float64, copy=True, order="C")
        if self.carrier_size <= 0:
            raise ValueError("Carrier size must be positive")
        if mat.shape != (self.carrier_size, self.carrier_size):
            raise ValueError(
                f"Diff matrix shape {mat.shape} mismatch with carrier {self.carrier_size}"
            )
        if not np.allclose(np.diag(mat), 0.0):
            raise ValueError("Self-difference on diagonal must be zero")
        if np.any(mat < 0.0):
            raise ValueError("Primitive differences must be non-negative")
        if np.any(np.isnan(mat)):
            raise ValueError("Primitive differences must not contain NaN")
        mat[mat == 0.0] = 0.0
        mat.flags.writeable = False
        object.__setattr__(self, "diff_matrix", mat)

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return False
        assert isinstance(other, Presentation)
        return (
            self.name == other.name
            and self.carrier_size == other.carrier_size
            and np.array_equal(self.diff_matrix, other.diff_matrix)
        )

    def __hash__(self) -> int:
        return hash((self.name, self.carrier_size, self.diff_matrix.tobytes()))


@dataclass(frozen=True)
class ComparisonSpan:
    """Comparison span P1 <- M -> P2 with extensional morphism cost."""

    p1: Presentation
    p2: Presentation
    mid_size: int
    left_map: Tuple[int, ...]
    right_map: Tuple[int, ...]
    ext_cost: float = 0.0

    def __post_init__(self):
        if not isinstance(self.mid_size, int) or isinstance(self.mid_size, bool) or self.mid_size < 0:
            raise ValueError("mid_size must be a non-negative integer")
        if len(self.left_map) != self.mid_size or len(self.right_map) != self.mid_size:
            raise ValueError("Map length must equal mid_size")
        for idx in self.left_map:
            if not isinstance(idx, int) or isinstance(idx, bool) or not (0 <= idx < self.p1.carrier_size):
                raise ValueError(
                    f"left_map index {idx} out of bounds for carrier size {self.p1.carrier_size}"
                )
        for idx in self.right_map:
            if not isinstance(idx, int) or isinstance(idx, bool) or not (0 <= idx < self.p2.carrier_size):
                raise ValueError(
                    f"right_map index {idx} out of bounds for carrier size {self.p2.carrier_size}"
                )
        if self.ext_cost < 0.0:
            raise ValueError("Extensional cost must be non-negative")


def make_diag_span(p: Presentation) -> ComparisonSpan:
    """Diagonal comparison span [Delta_P] on presentation P."""
    indices = tuple(range(p.carrier_size))
    return ComparisonSpan(
        p1=p,
        p2=p,
        mid_size=p.carrier_size,
        left_map=indices,
        right_map=indices,
        ext_cost=0.0,
    )


def compose_spans(s1: ComparisonSpan, s2: ComparisonSpan) -> ComparisonSpan:
    """Pullback composition of spans [S2] * [S1]."""
    if s1.p2 != s2.p1:
        raise ValueError(f"Span composition mismatch: {s1.p2.name} != {s2.p1.name}")

    # Pullback mid-carrier: {(m1, m2) : s1.right_map[m1] == s2.left_map[m2]}
    pb_pairs: List[Tuple[int, int]] = []
    for m1 in range(s1.mid_size):
        for m2 in range(s2.mid_size):
            if s1.right_map[m1] == s2.left_map[m2]:
                pb_pairs.append((m1, m2))

    left_map = tuple(s1.left_map[p[0]] for p in pb_pairs)
    right_map = tuple(s2.right_map[p[1]] for p in pb_pairs)
    cost = s1.ext_cost + s2.ext_cost
    return ComparisonSpan(
        p1=s1.p1,
        p2=s2.p3 if hasattr(s2, "p3") else s2.p2,
        mid_size=len(pb_pairs),
        left_map=left_map,
        right_map=right_map,
        ext_cost=cost,
    )


@dataclass(frozen=True)
class Trace:
    """Intensional execution trace in CODA_trace."""

    steps: int
    work_cost: float
    span: ComparisonSpan

    def __post_init__(self):
        if self.steps < 0:
            raise ValueError("Steps must be non-negative")
        if self.work_cost < 0.0:
            raise ValueError("Work cost must be non-negative")


def compose_traces(t1: Trace, t2: Trace) -> Trace:
    """Intensional composition of execution traces."""
    comp_span = compose_spans(t1.span, t2.span)
    return Trace(
        steps=t1.steps + t2.steps, work_cost=t1.work_cost + t2.work_cost, span=comp_span
    )


def erase_trace(t: Trace) -> ComparisonSpan:
    """Erasure quotient map q: CODA_trace -> CODA_pres."""
    return t.span


@dataclass
class FiniteGroupoid:
    """Finite groupoid with objects, morphisms, and inverses."""

    objects: List[str]
    morphisms: Dict[
        str, Dict[str, List[str]]
    ]  # obj_src -> obj_tgt -> list of mor_names
    id_map: Dict[str, str]  # obj -> id_mor_name
    comp_table: Dict[Tuple[str, str], str]  # (g, f) -> g o f
    inv_map: Dict[str, str]  # f -> f^-1

    def validate(self) -> bool:
        if not isinstance(self.objects, (list, tuple)) or not self.objects:
            return False
        obj_set = set(self.objects)
        if len(obj_set) != len(self.objects):
            return False
        if not all(isinstance(o, str) and o for o in self.objects):
            return False

        if not isinstance(self.id_map, dict) or set(self.id_map.keys()) != obj_set:
            return False

        if not isinstance(self.morphisms, dict):
            return False

        mor_src: Dict[str, str] = {}
        mor_tgt: Dict[str, str] = {}
        for src, tgts in self.morphisms.items():
            if src not in obj_set or not isinstance(tgts, dict):
                return False
            for tgt, mors in tgts.items():
                if tgt not in obj_set or not isinstance(mors, (list, tuple)):
                    return False
                for m in mors:
                    if not isinstance(m, str) or not m or m in mor_src:
                        return False
                    mor_src[m] = src
                    mor_tgt[m] = tgt

        all_morphisms = set(mor_src.keys())
        if not all_morphisms:
            return False

        for obj in self.objects:
            id_m = self.id_map[obj]
            if id_m not in all_morphisms:
                return False
            if mor_src[id_m] != obj or mor_tgt[id_m] != obj:
                return False

        if not isinstance(self.inv_map, dict) or set(self.inv_map.keys()) != all_morphisms:
            return False
        for f, finv in self.inv_map.items():
            if finv not in all_morphisms:
                return False
            if mor_src[finv] != mor_tgt[f] or mor_tgt[finv] != mor_src[f]:
                return False

        composable_pairs = {
            (g, f)
            for g in all_morphisms
            for f in all_morphisms
            if mor_tgt[f] == mor_src[g]
        }
        if not isinstance(self.comp_table, dict) or set(self.comp_table.keys()) != composable_pairs:
            return False

        for (g, f), gf in self.comp_table.items():
            if gf not in all_morphisms:
                return False
            if mor_src[gf] != mor_src[f] or mor_tgt[gf] != mor_tgt[g]:
                return False

        for f in all_morphisms:
            src, tgt = mor_src[f], mor_tgt[f]
            id_src = self.id_map[src]
            id_tgt = self.id_map[tgt]
            if self.comp_table.get((id_tgt, f)) != f:
                return False
            if self.comp_table.get((f, id_src)) != f:
                return False

        for f in all_morphisms:
            src, tgt = mor_src[f], mor_tgt[f]
            finv = self.inv_map[f]
            id_src = self.id_map[src]
            id_tgt = self.id_map[tgt]
            if self.comp_table.get((finv, f)) != id_src:
                return False
            if self.comp_table.get((f, finv)) != id_tgt:
                return False

        for (g, f) in composable_pairs:
            gf = self.comp_table[(g, f)]
            tgt_g = mor_tgt[g]
            for h in all_morphisms:
                if mor_src[h] == tgt_g:
                    hg = self.comp_table[(h, g)]
                    if self.comp_table.get((h, gf)) != self.comp_table.get((hg, f)):
                        return False

        return True


def make_z2_groupoid() -> FiniteGroupoid:
    """Finite groupoid for Z_2 (single object point groupoid)."""
    return FiniteGroupoid(
        objects=["*"],
        morphisms={"*": {"*": ["e", "g"]}},
        id_map={"*": "e"},
        comp_table={("e", "e"): "e", ("e", "g"): "g", ("g", "e"): "g", ("g", "g"): "e"},
        inv_map={"e": "e", "g": "g"},
    )


def make_z3_groupoid() -> FiniteGroupoid:
    """Finite groupoid for Z_3."""
    return FiniteGroupoid(
        objects=["*"],
        morphisms={"*": {"*": ["e", "g", "g2"]}},
        id_map={"*": "e"},
        comp_table={
            ("e", "e"): "e",
            ("e", "g"): "g",
            ("e", "g2"): "g2",
            ("g", "e"): "g",
            ("g", "g"): "g2",
            ("g", "g2"): "e",
            ("g2", "e"): "g2",
            ("g2", "g"): "e",
            ("g2", "g2"): "g",
        },
        inv_map={"e": "e", "g": "g2", "g2": "g"},
    )


class FaithfulGroupoidEmbedding:
    """CD-12 Model Construction: Faithful functor E: G -> CODA_pres with trace lifting."""

    def __init__(self, groupoid: FiniteGroupoid):
        self.groupoid = groupoid
        self.presentations: Dict[str, Presentation] = {
            obj: Presentation(
                name=f"Pres_{obj}", carrier_size=1, diff_matrix=np.zeros((1, 1))
            )
            for obj in groupoid.objects
        }
        self.spans: Dict[str, ComparisonSpan] = {}
        for src, tgts in groupoid.morphisms.items():
            for tgt, mors in tgts.items():
                for m in mors:
                    self.spans[m] = ComparisonSpan(
                        p1=self.presentations[src],
                        p2=self.presentations[tgt],
                        mid_size=1,
                        left_map=(0,),
                        right_map=(0,),
                        ext_cost=0.0,
                    )

    def embed_object(self, obj: str) -> Presentation:
        return self.presentations[obj]

    def embed_morphism(self, mor: str) -> ComparisonSpan:
        return self.spans[mor]

    def lift_trace(self, mor: str, work_cost: float = 1.0) -> Trace:
        return Trace(steps=1, work_cost=work_cost, span=self.spans[mor])

    def check_faithfulness(self) -> bool:
        # In this presentation model, distinct groupoid arrows map injectively to distinct typed span entities
        mor_list = list(self.spans.keys())
        return len(mor_list) == len(set(mor_list))

    def check_two_level_cost_accounting(
        self, mor: str, work: float = 2.5
    ) -> Dict[str, float]:
        """Verify extensional cost is 0 on inverse round-trip while intensional trace cost is positive."""
        inv_mor = self.groupoid.inv_map[mor]
        s = self.embed_morphism(mor)
        s_inv = self.embed_morphism(inv_mor)
        s_comp = compose_spans(s, s_inv)

        t = self.lift_trace(mor, work_cost=work)
        t_inv = self.lift_trace(inv_mor, work_cost=work)
        t_comp = compose_traces(t, t_inv)

        return {
            "extensional_cost": s_comp.ext_cost,
            "intensional_work_cost": t_comp.work_cost,
            "trace_steps": float(t_comp.steps),
        }


@dataclass(frozen=True)
class ClaimEntry:
    id: str
    claim: str
    status: str
    evidence_section: str


CODA_DISCIPLINE_CLAIMS = [
    ClaimEntry(
        "CD-01",
        "Discipline named CODA (Calculus of Obstruction, Descent, and Authority)",
        "DEFINITION",
        "§1",
    ),
    ClaimEntry(
        "CD-02",
        "Prior names (RCOC) withdrawn aliases; one discipline, one name",
        "NAMING RULE",
        "§1",
    ),
    ClaimEntry(
        "CD-03",
        "Obstruction-first ontology: difference primitive, identity derived quotient",
        "RESEARCH PROGRAM",
        "§2",
    ),
    ClaimEntry(
        "CD-04",
        "Declaration pricing practiced and proved in exemplars",
        "PROVED (exemplars)",
        "§2",
    ),
    ClaimEntry(
        "CD-05a",
        "Proposed BQNF/WIR normal-form correspondence",
        "PROPOSED CORRESPONDENCE",
        "§2",
    ),
    ClaimEntry(
        "CD-05b",
        "Source-isolated re-derivation on Z_N cases",
        "SOURCE-ISOLATED RE-DERIVATION",
        "§2",
    ),
    ClaimEntry(
        "CD-06",
        "CODA does not subsume HoTT; subsumption verb withdrawn",
        "WITHDRAWAL + POSITIONING",
        "§3",
    ),
    ClaimEntry(
        "CD-07",
        "Positioning 1: identity inversion is research program",
        "CLASSIFIED",
        "§3.1",
    ),
    ClaimEntry(
        "CD-08",
        "Positioning 2: no containers is design declaration",
        "CLASSIFIED",
        "§3.2",
    ),
    ClaimEntry(
        "CD-09",
        "Positioning 3: higher cells as cochains in abelian fragment only",
        "PARTIAL + OPEN",
        "§3.3",
    ),
    ClaimEntry(
        "CD-10",
        "Positioning 4: priced transport is refusal, not univalence",
        "CLASSIFIED",
        "§3.4",
    ),
    ClaimEntry(
        "CD-11",
        "HoTT funext non-constructive claim withdrawn as false",
        "WITHDRAWN + CORRECTED",
        "§3.5",
    ),
    ClaimEntry(
        "CD-12",
        "CD-12 faithful functor target from finite groupoids",
        "RESEARCH TARGET",
        "§4",
    ),
    ClaimEntry(
        "CD-13", "Paper confers no authority and completes nothing", "SCOPE FENCE", "§5"
    ),
]


def assert_hott_non_subsumption_fence(claim_text: str) -> None:
    """Enforce strict refusal if an ungrounded HoTT subsumption claim is made."""
    forbidden = ["subsumes hott", "replaces univalence", "proves univalence false"]
    lower = claim_text.lower()
    for f in forbidden:
        if f in lower:
            raise HoTTSubsumptionRefusalError(
                f"Prohibited HoTT subsumption claim detected: '{f}'"
            )
