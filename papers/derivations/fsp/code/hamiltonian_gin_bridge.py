"""Exact cancellation audit for explicitly enumerated finite Euler paths.
AuthorityEffect: None.

Fractions and the retained path records are the arithmetic authority. Legacy
SQLite REAL views are displays only. Equal-weight matching constructs an
involution on its paired subset; it is not a discovered physical symmetry,
does not preserve general observables or spectators, and has no implicit
polynomial bound in lattice size.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
import sqlite3
import sys
from typing import Any, Dict, List, Optional, Set, Tuple

code_dir = Path(__file__).resolve().parent
if str(code_dir) not in sys.path:
    sys.path.insert(0, str(code_dir))

from fermionic_hamiltonian import (
    DiscreteFermionicHamiltonian,
    FermionicLattice,
    FockState,
    exact_fraction,
)
from fermion_gin_index import (
    InvolutionCancellationReceipt,
    MajoranaZeroModeReceipt,
)


@dataclass(frozen=True)
class HamiltonianPathRecord:
    path_id: int
    model_name: str
    path_indices: Tuple[int, ...]
    occupied_modes: frozenset[int]
    weight: Fraction
    jw_sign: int
    is_cancelling: bool
    ensemble_id: int


@dataclass(frozen=True)
class ExactHamiltonianCancellationReceipt(InvolutionCancellationReceipt):
    """Legacy float fields are displays; these fractions certify the finite sum."""
    exact_signed_sum: Fraction
    exact_unsigned_mass: Fraction
    exact_max_weight_defect: Fraction
    exact_unpaired_negative_mass: Fraction
    exact_residual_mass: Fraction
    integrity_errors: Tuple[str, ...]


class HamiltonianGinBridge:
    """Indexes finite Euler ensembles and audits exact, disjoint cancellation."""

    def __init__(self, in_memory: bool = True):
        self.conn = sqlite3.connect(":memory:" if in_memory else "hamiltonian_gin.db")
        self.conn.row_factory = sqlite3.Row
        self.posting_index: Dict[int, Set[int]] = defaultdict(set)
        self.cfg_modes: Dict[int, Set[int]] = {}
        self.paths: Dict[int, HamiltonianPathRecord] = {}
        self._next_ensemble_id = 1
        self._init_schema()

    def _init_schema(self) -> None:
        schema_path = Path(__file__).resolve().parent.parent / "databases" / "fermion_gin_index_schema.sql"
        if not schema_path.exists():
            schema_path = Path(__file__).resolve().parent / "fermion_gin_index_schema.sql"
        if schema_path.exists():
            self.conn.executescript(schema_path.read_text(encoding="utf-8"))
        self.conn.execute("""CREATE TABLE IF NOT EXISTS ExactHamiltonianPathWeights (
            cfg_id INTEGER PRIMARY KEY,
            numerator TEXT NOT NULL,
            denominator TEXT NOT NULL,
            ensemble_id INTEGER NOT NULL
        )""")
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()


    def index_hamiltonian_paths(
        self,
        hamiltonian: DiscreteFermionicHamiltonian,
        beta: int | float | Fraction = 1.5,
        trotter_steps: int = 4,
        model_name: str = "FermionicHamiltonian",
    ) -> Dict[str, Any]:
        """Retain every nonzero exact path; pair equal weights within this batch."""
        raw_paths = hamiltonian.generate_sample_paths(beta=beta, trotter_steps=trotter_steps)
        ensemble_id = self._next_ensemble_id
        self._next_ensemble_id += 1
        num_sites = hamiltonian.lattice.num_sites
        total_modes = 2 * num_sites

        c = self.conn.cursor()
        c.execute("SELECT COALESCE(MAX(cfg_id), 0) FROM FermionConfigurations;")
        max_cfg_db = c.fetchone()[0]
        cfg_id = max(max_cfg_db, max(self.paths.keys(), default=0)) + 1

        indexed_records = []
        pos_by_weight: Dict[Fraction, List[int]] = defaultdict(list)
        neg_by_weight: Dict[Fraction, List[int]] = defaultdict(list)

        for p in raw_paths:
            weight = exact_fraction(p["abs_weight"], "path weight")
            sign = int(p["parity"])
            if weight <= 0 or sign not in (-1, 1):
                raise ValueError("Indexed paths must have positive magnitude and sign +/-1")
            if exact_fraction(p["signed_amplitude"], "signed amplitude") != sign * weight:
                raise ValueError("Path amplitude disagrees with its sign and magnitude")
            path_indices = tuple(p["path_indices"])

            occupied_modes: Set[int] = set()
            for idx in path_indices:
                fock = hamiltonian.basis[idx]
                for s in range(num_sites):
                    if fock.is_occupied(s, "up"):
                        occupied_modes.add(s + 1)
                    if fock.is_occupied(s, "down"):
                        occupied_modes.add(num_sites + s + 1)

            c.execute(
                """INSERT INTO FermionConfigurations
                   (cfg_id, model_name, num_particles, total_modes, weight, jw_sign, parity_sector)
                   VALUES (?, ?, ?, ?, ?, ?, ?);""",
                (cfg_id, model_name, hamiltonian.num_up + hamiltonian.num_down,
                 total_modes, float(weight), sign, 1),
            )
            c.execute("INSERT INTO ExactHamiltonianPathWeights VALUES (?, ?, ?, ?)",
                      (cfg_id, str(weight.numerator), str(weight.denominator), ensemble_id))

            self.cfg_modes[cfg_id] = set(occupied_modes)
            for m in range(1, total_modes + 1):
                is_occ = 1 if m in occupied_modes else 0
                c.execute(
                    "INSERT INTO GinModePostingList (mode_id, cfg_id, is_occupied) VALUES (?, ?, ?);",
                    (m, cfg_id, is_occ),
                )
                if is_occ:
                    self.posting_index[m].add(cfg_id)

            record = HamiltonianPathRecord(
                path_id=cfg_id,
                model_name=model_name,
                path_indices=path_indices,
                occupied_modes=frozenset(occupied_modes),
                weight=weight,
                jw_sign=sign,
                is_cancelling=(sign < 0),
                ensemble_id=ensemble_id,
            )
            self.paths[cfg_id] = record
            indexed_records.append(record)

            if sign > 0:
                pos_by_weight[weight].append(cfg_id)
            elif sign < 0:
                neg_by_weight[weight].append(cfg_id)

            cfg_id += 1

        self.conn.commit()

        c.execute("SELECT COALESCE(MAX(pair_id), 0) FROM GinInvolutionPairs;")
        pair_id = c.fetchone()[0] + 1
        matched_pos: Set[int] = set()
        matched_neg: Set[int] = set()
        total_pairs = 0

        for weight, neg_list in neg_by_weight.items():
            for partner_cid, neg_cid in zip(pos_by_weight.get(weight, []), neg_list):
                matched_pos.add(partner_cid)
                matched_neg.add(neg_cid)
                c.execute(
                    """INSERT INTO GinInvolutionPairs
                       (pair_id, cfg_pos_id, cfg_neg_id, involution_type, is_exact_partner)
                       VALUES (?, ?, ?, 'ExactEnumeratedWeightMatching', 1);""",
                    (pair_id, partner_cid, neg_cid),
                )
                pair_id += 1
                total_pairs += 1

        self.conn.commit()

        total_negatives = sum(len(lst) for lst in neg_by_weight.values())
        unpartnered_negatives = total_negatives - len(matched_neg)

        return {
            "model_name": model_name,
            "total_paths": len(indexed_records),
            "positive_paths": sum(len(lst) for lst in pos_by_weight.values()),
            "negative_paths": total_negatives,
            "matched_pairs": total_pairs,
            "unpartnered_negatives": unpartnered_negatives,
            "is_completely_paired": (unpartnered_negatives == 0),
            "ensemble_id": ensemble_id,
            "pairing_scope": "enumerated partition weights only",
            "preserves_general_observables": False,
            "arithmetic": "Fraction; finite floats retain exact binary value",
        }


    def audit_sign_resolution(self, model_name: str) -> ExactHamiltonianCancellationReceipt:
        """Independently check the proposed involution and its exact residual.

        Both endpoints, opposite signs, equal rational weights, same batch,
        unique use, and correspondence to retained records are mandatory.
        SQL rows without retained exact provenance may report a defect but
        cannot receive a certificate. A zero quotient is not a probability
        ensemble and never receives average sign one.
        """
        configurations = {r["cfg_id"]: r for r in self.conn.execute(
            "SELECT * FROM FermionConfigurations")}
        exact_rows = {r["cfg_id"]: r for r in self.conn.execute(
            "SELECT * FROM ExactHamiltonianPathWeights")}
        records = {cid: r for cid, r in self.paths.items() if r.model_name == model_name}
        model_ids = set(records) | {cid for cid, r in configurations.items()
                                    if r["model_name"] == model_name}
        errors: Set[str] = set()
        magnitudes: Dict[int, Fraction] = {}
        signs: Dict[int, int] = {}
        for cid in model_ids:
            rec, row, exact_row = records.get(cid), configurations.get(cid), exact_rows.get(cid)
            if rec is None:
                errors.add(f"configuration {cid}: missing retained exact record")
                if row is not None:
                    try:
                        magnitudes[cid] = exact_fraction(row["weight"], "SQL weight")
                        signs[cid] = row["jw_sign"]
                    except (ValueError, TypeError):
                        errors.add(f"configuration {cid}: invalid display weight")
                continue
            magnitudes[cid], signs[cid] = rec.weight, rec.jw_sign
            if row is None:
                errors.add(f"configuration {cid}: missing SQL row")
            elif (row["model_name"] != rec.model_name or row["jw_sign"] != rec.jw_sign
                  or row["weight"] != float(rec.weight)):
                errors.add(f"configuration {cid}: SQL row differs from exact record")
            if exact_row is None or (
                exact_row["numerator"], exact_row["denominator"], exact_row["ensemble_id"]
            ) != (str(rec.weight.numerator), str(rec.weight.denominator), rec.ensemble_id):
                errors.add(f"configuration {cid}: rational provenance differs")
            if rec.weight <= 0 or rec.jw_sign not in (-1, 1):
                errors.add(f"configuration {cid}: invalid exact weight or sign")

        pair_rows = [r for r in self.conn.execute("SELECT * FROM GinInvolutionPairs")
                     if r["cfg_pos_id"] in model_ids or r["cfg_neg_id"] in model_ids]
        endpoint_counts = Counter(cid for r in pair_rows
                                  for cid in (r["cfg_pos_id"], r["cfg_neg_id"]))
        paired: Set[int] = set()
        involution: Dict[int, int] = {}
        max_defect = Fraction(0)
        for pair in pair_rows:
            p, n = pair["cfg_pos_id"], pair["cfg_neg_id"]
            pos, neg = records.get(p), records.get(n)
            if p in magnitudes and n in magnitudes:
                max_defect = max(max_defect, abs(magnitudes[p] - magnitudes[n]))
            valid = (
                p != n and endpoint_counts[p] == endpoint_counts[n] == 1
                and pos is not None and neg is not None
                and pos.ensemble_id == neg.ensemble_id
                and pos.jw_sign == 1 and neg.jw_sign == -1
                and pos.weight == neg.weight and pair["is_exact_partner"] == 1
            )
            if not valid:
                errors.add(f"pair {pair['pair_id']}: invalid disjoint exact same-batch pairing")
                continue
            paired.update((p, n))
            involution[p], involution[n] = n, p

        if any(involution.get(partner) != cid or partner == cid
               for cid, partner in involution.items()):
            errors.add("pair map is not a fixed-point-free involution")
        signed_sum = sum((w * signs[cid] for cid, w in magnitudes.items()), Fraction(0))
        unsigned_mass = sum(magnitudes.values(), Fraction(0))
        residual_mass = sum((w for cid, w in magnitudes.items() if cid not in paired), Fraction(0))
        residual_signed = sum((w * signs[cid] for cid, w in magnitudes.items()
                               if cid not in paired), Fraction(0))
        unpaired_negative = sum((w for cid, w in magnitudes.items()
                                 if cid not in paired and signs[cid] == -1), Fraction(0))
        if signed_sum != residual_signed:
            errors.add("pair deletion changed the signed sum")

        raw_average = signed_sum / unsigned_mass if unsigned_mass > 0 else Fraction(0)
        quotient_average = residual_signed / residual_mass if residual_mass > 0 else Fraction(0)
        if errors:
            route = "SplitBrainRefusal"
        elif not model_ids or unsigned_mass <= 0:
            route = "EmptyEnsembleRefusal"
        elif residual_mass == 0:
            route = "ZeroResidualRefusal"
        elif unpaired_negative == 0:
            route = "Repair"
        else:
            route = "SplitBrainRefusal"

        return ExactHamiltonianCancellationReceipt(
            model_name=model_name,
            pairs_audited=len(pair_rows),
            all_exact_cancellations=route == "Repair",
            max_weight_defect=float(max_defect),
            total_uncancelled_mass=float(unpaired_negative),
            raw_average_sign=float(raw_average),
            gin_quotiented_average_sign=float(quotient_average),
            terminal_route=route,
            exact_signed_sum=signed_sum,
            exact_unsigned_mass=unsigned_mass,
            exact_max_weight_defect=max_defect,
            exact_unpaired_negative_mass=unpaired_negative,
            exact_residual_mass=residual_mass,
            integrity_errors=tuple(sorted(errors)),
        )


    def index_kitaev_chain_majorana(self, L: int = 4, model_name: str = "KitaevChain") -> MajoranaZeroModeReceipt:
        """Indexes sweet-spot Kitaev chain bulk bonds and audits topological boundary isolation."""
        c = self.conn.cursor()
        c.execute(
            """INSERT INTO FermionConfigurations
               (cfg_id, model_name, num_particles, total_modes, weight, jw_sign, parity_sector)
               VALUES (9999, ?, ?, ?, 1.0, 1, 1);""",
            (model_name, L, 2 * L),
        )

        bond_id = 1
        for j in range(1, L):
            u = 2 * j
            v = 2 * j + 1
            c.execute(
                "INSERT INTO GinMajoranaBonds (bond_id, cfg_id, u, v, is_bulk_bond) VALUES (?, 9999, ?, ?, 1);",
                (bond_id, u, v),
            )
            bond_id += 1

        c.execute(
            "INSERT INTO GinMajoranaBonds (bond_id, cfg_id, u, v, is_bulk_bond) VALUES (?, 9999, 1, ?, 0);",
            (bond_id, 2 * L),
        )
        self.conn.commit()

        c.execute("SELECT * FROM ViewMajoranaZeroModeAudit ORDER BY mode_idx;")
        rows = c.fetchall()

        unpaired = [r["mode_idx"] for r in rows if r["is_unpaired_zero_mode"] == 1]
        bulk = [r["mode_idx"] for r in rows if r["is_unpaired_zero_mode"] == 0]

        is_boundary_isolated = (set(unpaired) == {1, 2 * L})
        status = "MZM_TOPOLOGICALLY_PROTECTED" if is_boundary_isolated else "MZM_BULK_POLLUTION"

        return MajoranaZeroModeReceipt(
            total_modes_audited=len(rows),
            unpaired_zero_modes=unpaired,
            bulk_bonded_modes=bulk,
            is_boundary_isolated=is_boundary_isolated,
            mzm_status=status,
        )


__all__ = [
    "HamiltonianGinBridge",
    "HamiltonianPathRecord",
    "ExactHamiltonianCancellationReceipt",
]
