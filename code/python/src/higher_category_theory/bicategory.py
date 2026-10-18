"""Weak 2-categories (Bicategories) and coherence isomorphisms.

Mac Lane pentagon and triangle coherence verification for finite bicategories.
AuthorityEffect: None.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set


class HigherCategoryError(Exception):
    """Base error for higher category operations."""
    pass


class PentagonCoherenceViolation(HigherCategoryError):
    def __init__(self, step: str, path_a: str, path_b: str):
        super().__init__(f"Pentagon coherence failed for {step}: {path_a} != {path_b}")
        self.step = step
        self.path_a = path_a
        self.path_b = path_b


class TriangleCoherenceViolation(HigherCategoryError):
    def __init__(self, details: str, left: str, right: str):
        super().__init__(f"Triangle coherence violation: {details} ({left} != {right})")
        self.details = details
        self.left = left
        self.right = right


@dataclass(frozen=True)
class Invertible2Cell:
    """An invertible 2-cell (2-isomorphism) witnessing weak equivalence."""
    forward: str
    inverse: str


@dataclass
class Strict2Category:
    """Finite strict 2-category with categorical identity laws."""
    objects: Set[str] = field(default_factory=set)
    # 1-cells: id -> (src, tgt)
    one_cells: Dict[str, Tuple[str, str]] = field(default_factory=dict)
    # 2-cells: id -> (src_1cell, tgt_1cell)
    two_cells: Dict[str, Tuple[str, str]] = field(default_factory=dict)
    # Composition tables
    comp_1: Dict[Tuple[str, str], str] = field(default_factory=dict)
    comp_2_v: Dict[Tuple[str, str], str] = field(default_factory=dict)
    comp_2_h: Dict[Tuple[str, str], str] = field(default_factory=dict)

    def add_object(self, obj: str):
        self.objects.add(obj)

    def add_1cell(self, name: str, src: str, tgt: str):
        if src not in self.objects or tgt not in self.objects:
            raise HigherCategoryError(f"Endpoints {src}, {tgt} not in objects")
        self.one_cells[name] = (src, tgt)

    def add_2cell(self, name: str, src_1: str, tgt_1: str):
        if src_1 not in self.one_cells or tgt_1 not in self.one_cells:
            raise HigherCategoryError(f"1-cell endpoints {src_1}, {tgt_1} not registered")
        s_src, s_tgt = self.one_cells[src_1]
        t_src, t_tgt = self.one_cells[tgt_1]
        if s_src != t_src or s_tgt != t_tgt:
            raise HigherCategoryError("2-cell parallel boundary mismatch")
        self.two_cells[name] = (src_1, tgt_1)

    def id_1(self, obj: str) -> str:
        name = f"id_{obj}"
        if name not in self.one_cells:
            self.add_1cell(name, obj, obj)
            self.comp_1[(name, name)] = name
        return name

    def id_2(self, one_cell: str) -> str:
        name = f"id_{one_cell}"
        if name not in self.two_cells:
            self.add_2cell(name, one_cell, one_cell)
            self.comp_2_v[(name, name)] = name
        return name

    def is_id_1(self, one_cell: str) -> bool:
        return one_cell.startswith("id_") and one_cell[3:] in self.objects

    def is_id_2(self, two_cell: str) -> bool:
        return two_cell.startswith("id_") and two_cell[3:] in self.one_cells

    def compose_1(self, f: str, g: str) -> str:
        if (f, g) in self.comp_1:
            return self.comp_1[(f, g)]
        s_f, t_f = self.one_cells[f]
        s_g, t_g = self.one_cells[g]
        if t_f != s_g:
            raise HigherCategoryError(f"Cannot compose 1-cells: target({f})={t_f} != source({g})={s_g}")
        # Unital laws
        if self.is_id_1(f):
            return g
        if self.is_id_1(g):
            return f

        # Canonical associativity normalization
        parts_f = f.split("_circ_")
        parts_g = g.split("_circ_")
        comp = "_circ_".join(parts_g + parts_f)
        if comp not in self.one_cells:
            self.add_1cell(comp, s_f, t_g)
        self.comp_1[(f, g)] = comp
        return comp

    def compose_2_vertical(self, alpha: str, beta: str) -> str:
        if (alpha, beta) in self.comp_2_v:
            return self.comp_2_v[(alpha, beta)]
        s_a, t_a = self.two_cells[alpha]
        s_b, t_b = self.two_cells[beta]
        if t_a != s_b:
            raise HigherCategoryError(f"Cannot compose 2-cells vertically: target({alpha})={t_a} != source({beta})={s_b}")

        # Vertical identity laws
        if self.is_id_2(alpha):
            return beta
        if self.is_id_2(beta):
            return alpha

        comp = f"{beta}_o_{alpha}"
        if comp not in self.two_cells:
            self.add_2cell(comp, s_a, t_b)
        self.comp_2_v[(alpha, beta)] = comp
        return comp

    def compose_2_horizontal(self, alpha: str, beta: str) -> str:
        """Horizontal composition: beta *_h alpha where alpha: f => f' (A -> B), beta: g => g' (B -> C)."""
        if (alpha, beta) in self.comp_2_h:
            return self.comp_2_h[(alpha, beta)]
        s_a, t_a = self.two_cells[alpha]
        s_b, t_b = self.two_cells[beta]
        src_1 = self.compose_1(s_a, s_b)
        tgt_1 = self.compose_1(t_a, t_b)

        # Functoriality of identity 2-cell: 1_g *_h 1_f = 1_{g circ f}
        if self.is_id_2(alpha) and self.is_id_2(beta):
            id_comp = self.id_2(src_1)
            self.comp_2_h[(alpha, beta)] = id_comp
            return id_comp

        comp = f"{beta}_star_{alpha}"
        if comp not in self.two_cells:
            self.add_2cell(comp, src_1, tgt_1)
        self.comp_2_h[(alpha, beta)] = comp
        return comp


@dataclass
class CoherenceReport:
    pentagons_verified: int
    triangles_verified: int


class FiniteBicategory:
    """Finite bicategory with explicit associators and unitors."""

    def __init__(self, base_strict: Strict2Category):
        self.base_strict = base_strict
        self.associator_table: Dict[Tuple[str, str, str], Invertible2Cell] = {}
        self.left_unitor_table: Dict[str, Invertible2Cell] = {}
        self.right_unitor_table: Dict[str, Invertible2Cell] = {}

    def set_associator(self, f: str, g: str, h: str, forward: str, inverse: str):
        hg = self.base_strict.compose_1(g, h)
        hgf_left = self.base_strict.compose_1(f, hg)
        gf = self.base_strict.compose_1(f, g)
        hgf_right = self.base_strict.compose_1(gf, h)

        if forward not in self.base_strict.two_cells:
            self.base_strict.add_2cell(forward, hgf_left, hgf_right)
        if inverse not in self.base_strict.two_cells:
            self.base_strict.add_2cell(inverse, hgf_right, hgf_left)

        self.associator_table[(f, g, h)] = Invertible2Cell(forward, inverse)

    def set_left_unitor(self, f: str, forward: str, inverse: str):
        _, tgt = self.base_strict.one_cells[f]
        id_b = self.base_strict.id_1(tgt)
        id_b_f = self.base_strict.compose_1(f, id_b)

        if forward not in self.base_strict.two_cells:
            self.base_strict.add_2cell(forward, id_b_f, f)
        if inverse not in self.base_strict.two_cells:
            self.base_strict.add_2cell(inverse, f, id_b_f)

        self.left_unitor_table[f] = Invertible2Cell(forward, inverse)

    def set_right_unitor(self, f: str, forward: str, inverse: str):
        src, _ = self.base_strict.one_cells[f]
        id_a = self.base_strict.id_1(src)
        f_id_a = self.base_strict.compose_1(id_a, f)

        if forward not in self.base_strict.two_cells:
            self.base_strict.add_2cell(forward, f_id_a, f)
        if inverse not in self.base_strict.two_cells:
            self.base_strict.add_2cell(inverse, f, f_id_a)

        self.right_unitor_table[f] = Invertible2Cell(forward, inverse)

    def associator(self, f: str, g: str, h: str) -> Invertible2Cell:
        if (f, g, h) in self.associator_table:
            return self.associator_table[(f, g, h)]
        # Default identity associator if strict
        hg = self.base_strict.compose_1(g, h)
        left = self.base_strict.compose_1(f, hg)
        id2 = self.base_strict.id_2(left)
        return Invertible2Cell(id2, id2)

    def left_unitor(self, f: str) -> Invertible2Cell:
        if f in self.left_unitor_table:
            return self.left_unitor_table[f]
        id2 = self.base_strict.id_2(f)
        return Invertible2Cell(id2, id2)

    def right_unitor(self, f: str) -> Invertible2Cell:
        if f in self.right_unitor_table:
            return self.right_unitor_table[f]
        id2 = self.base_strict.id_2(f)
        return Invertible2Cell(id2, id2)


def check_pentagon_coherence(
    bicat: FiniteBicategory,
    f: str,
    g: str,
    h: str,
    k: str,
) -> bool:
    """Evaluates the Mac Lane pentagon diagram for 4 composable 1-cells: f, g, h, k."""
    bs = bicat.base_strict
    id_f_2 = bs.id_2(f)
    id_k_2 = bs.id_2(k)

    alpha_k_h_g = bicat.associator(g, h, k).forward
    alpha_h_g_f = bicat.associator(f, g, h).forward

    h_circ_g = bs.compose_1(g, h)
    g_circ_f = bs.compose_1(f, g)
    k_circ_h = bs.compose_1(h, k)

    alpha_k_hg_f = bicat.associator(f, h_circ_g, k).forward
    alpha_kh_g_f = bicat.associator(f, g, k_circ_h).forward
    alpha_k_h_gf = bicat.associator(g_circ_f, h, k).forward

    # Path A (3 steps)
    step_a1 = bs.compose_2_horizontal(id_f_2, alpha_k_h_g)
    step_a2 = alpha_k_hg_f
    step_a3 = bs.compose_2_horizontal(alpha_h_g_f, id_k_2)

    path_a_12 = bs.compose_2_vertical(step_a1, step_a2)
    path_a = bs.compose_2_vertical(path_a_12, step_a3)

    # Path B (2 steps)
    step_b1 = alpha_kh_g_f
    step_b2 = alpha_k_h_gf
    path_b = bs.compose_2_vertical(step_b1, step_b2)

    if path_a == path_b:
        return True
    else:
        raise PentagonCoherenceViolation(
            f"({f}, {g}, {h}, {k})", path_a, path_b
        )


def check_triangle_coherence(
    bicat: FiniteBicategory,
    f: str,
    g: str,
) -> bool:
    """Evaluates the triangle coherence diagram for two composable 1-cells: f, g."""
    bs = bicat.base_strict
    _, tgt_f = bs.one_cells[f]
    id_b_1 = bs.id_1(tgt_f)
    id_g_2 = bs.id_2(g)
    id_f_2 = bs.id_2(f)

    assoc = bicat.associator(f, id_b_1, g).forward
    l_f = bicat.left_unitor(f).forward
    r_g = bicat.right_unitor(g).forward

    # LHS: (1_g * l_f) circ_v alpha
    id_g_star_l_f = bs.compose_2_horizontal(l_f, id_g_2)
    lhs = bs.compose_2_vertical(assoc, id_g_star_l_f)

    # RHS: r_g * 1_f
    rhs = bs.compose_2_horizontal(id_f_2, r_g)

    if lhs == rhs:
        return True
    else:
        raise TriangleCoherenceViolation(
            f"Pair ({f}, {g})", lhs, rhs
        )
