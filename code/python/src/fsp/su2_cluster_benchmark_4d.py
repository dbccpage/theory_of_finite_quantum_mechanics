"""su2_cluster_benchmark_4d.py — Multi-Turn PFP Cluster Sweeps on L=8 (V=4096) 4D SU(2) Lattice.

AuthorityEffect: None.
Reference: sealed-derivation-v1 (3100c4e), Paper 011, gemini_000.md.

Mechanizes:
1. Scalable 4D Torus T^4 Gauge Architecture:
   - Configurable lattice size L x L x L x L (L=8 yields V = 4096 sites and 16,384 gauge links).
   - Exact rational SU(2) link variables via unit quaternions under Zero-Float Law.
2. Multi-Turn Cluster Sweep Proposals:
   - Identifies connected multi-site clusters C subset T^4.
   - Proposes coordinated cluster link updates via exact Pythagorean quadruples.
   - Evaluates exact rational action changes Delta S in Q.
   - Applies rational Metropolis acceptance filter alpha = min(1, 1 / (1 + Delta S)).
3. Orientation-Reversing Involution tau Verification:
   - Verifies action invariance S[tau(U)] == S[U] and positive determinant product across sweeps.
4. Cryptographic Receipt Emission:
   - Emits L8ClusterBenchmarkReceipt certified with SHA-256 under AuthorityEffect: None.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

from su2_link_holonomy_4d import ExactRationalSU2, Lattice4DCoord, Lattice4DSU2
from pfp_fsp_bridge import FspLinkProposal, FspPfpProposalPacket, FspPfpReferee


@dataclass(frozen=True)
class L8ClusterBenchmarkReceipt:
    """Receipt certifying multi-turn PFP cluster sweep results on large 4D lattices."""

    benchmark_id: str
    lattice_dims: Tuple[int, int, int, int]
    total_sites: int
    total_links: int
    num_rounds: int
    num_proposals: int
    num_accepted: int
    acceptance_rate: Fraction
    initial_action: Fraction
    final_action: Fraction
    action_descent: Fraction
    involution_pairing_certified: bool
    unitarity_certified: bool
    authority_effect: str = "None"

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return False
        return (
            self.benchmark_id == other.benchmark_id
            and self.lattice_dims == other.lattice_dims
            and self.total_sites == other.total_sites
            and self.total_links == other.total_links
            and self.num_rounds == other.num_rounds
            and self.num_proposals == other.num_proposals
            and self.num_accepted == other.num_accepted
            and self.acceptance_rate == other.acceptance_rate
            and self.initial_action == other.initial_action
            and self.final_action == other.final_action
            and self.action_descent == other.action_descent
            and self.involution_pairing_certified == other.involution_pairing_certified
            and self.unitarity_certified == other.unitarity_certified
            and self.authority_effect == other.authority_effect
        )

    def canonical_digest(self) -> str:
        """Deterministic SHA-256 digest of benchmark receipt."""
        payload = {
            "benchmark_id": self.benchmark_id,
            "lattice_dims": list(self.lattice_dims),
            "total_sites": self.total_sites,
            "total_links": self.total_links,
            "num_rounds": self.num_rounds,
            "num_proposals": self.num_proposals,
            "num_accepted": self.num_accepted,
            "acceptance_rate": str(self.acceptance_rate),
            "initial_action": str(self.initial_action),
            "final_action": str(self.final_action),
            "action_descent": str(self.action_descent),
            "involution_pairing_certified": self.involution_pairing_certified,
            "unitarity_certified": self.unitarity_certified,
            "authority_effect": self.authority_effect,
        }
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


class SU2ClusterBenchmarkRunner:
    """Orchestrates multi-turn PFP cluster sweep benchmarks on 4D SU(2) lattices."""

    def __init__(self, lattice_dim: int = 8) -> None:
        if not isinstance(lattice_dim, int) or isinstance(lattice_dim, bool) or lattice_dim < 2:
            raise ValueError(f"lattice_dim must be an integer >= 2, got {lattice_dim}")
        self.dims: Tuple[int, int, int, int] = (lattice_dim, lattice_dim, lattice_dim, lattice_dim)
        self.lattice = Lattice4DSU2(self.dims)
        self.referee = FspPfpReferee(self.lattice)

    def generate_cluster_sites(self, base_coord: Lattice4DCoord, cluster_size: int = 2) -> List[Lattice4DCoord]:
        """Generates a localized connected hypercubic cluster of sites on T^4."""
        sites = []
        for d0 in range(cluster_size):
            for d1 in range(cluster_size):
                for d2 in range(cluster_size):
                    for d3 in range(cluster_size):
                        x0 = (base_coord.x0 + d0) % self.dims[0]
                        x1 = (base_coord.x1 + d1) % self.dims[1]
                        x2 = (base_coord.x2 + d2) % self.dims[2]
                        x3 = (base_coord.x3 + d3) % self.dims[3]
                        sites.append(Lattice4DCoord(x0, x1, x2, x3, self.dims))
        return sites

    def run_benchmark(
        self,
        num_rounds: int = 10,
        cluster_size: int = 2,
        random_threshold: Fraction = Fraction(1, 2),
    ) -> L8ClusterBenchmarkReceipt:
        """Executes a multi-turn PFP benchmark on the lattice."""
        if num_rounds <= 0:
            raise ValueError(f"num_rounds must be positive, got {num_rounds}")
        if not (Fraction(0, 1) <= random_threshold <= Fraction(1, 1)):
            raise ValueError("random_threshold must be in [0, 1]")

        initial_action = self.lattice.total_wilson_action()
        total_proposals = 0
        accepted_count = 0

        candidate_palette = [
            ExactRationalSU2.from_pythagorean_quadruple(1, 2, 2, 0),
            ExactRationalSU2.from_pythagorean_quadruple(2, 1, 0, 2),
            ExactRationalSU2.from_pythagorean_quadruple(0, 3, 0, 4),
            ExactRationalSU2.identity(),
        ]

        for rnd in range(num_rounds):
            base_site = Lattice4DCoord(
                rnd % self.dims[0],
                (rnd * 2) % self.dims[1],
                (rnd * 3) % self.dims[2],
                (rnd * 4) % self.dims[3],
                self.dims,
            )
            cluster = self.generate_cluster_sites(base_site, cluster_size=cluster_size)

            proposals = []
            cand = candidate_palette[rnd % len(candidate_palette)]
            for site in cluster[:4]:
                for mu in range(2):
                    proposals.append(FspLinkProposal(site.x0, site.x1, site.x2, site.x3, mu, cand))

            total_proposals += len(proposals)
            packet = FspPfpProposalPacket(
                round_id=f"l8_round_{rnd:03d}",
                proposer_id="agent_pfp_cluster_proposer",
                lattice_dims=self.dims,
                proposals=tuple(proposals),
                declared_initial_action=self.lattice.total_wilson_action(),
                declared_delta_action=Fraction(0, 1),
            )

            receipt = self.referee.evaluate_proposal(packet, random_threshold=random_threshold)
            if receipt.is_accepted:
                accepted_count += 1

        final_action = self.lattice.total_wilson_action()
        action_descent = initial_action - final_action
        inv_check = self.lattice.verify_involution_sign_balance()

        acc_rate = (
            Fraction(accepted_count, num_rounds)
            if num_rounds > 0
            else Fraction(0, 1)
        )

        return L8ClusterBenchmarkReceipt(
            benchmark_id=f"bm_l8_{self.dims[0]}x{self.dims[1]}x{self.dims[2]}x{self.dims[3]}",
            lattice_dims=self.dims,
            total_sites=self.lattice.volume,
            total_links=self.lattice.num_links,
            num_rounds=num_rounds,
            num_proposals=total_proposals,
            num_accepted=accepted_count,
            acceptance_rate=acc_rate,
            initial_action=initial_action,
            final_action=final_action,
            action_descent=action_descent,
            involution_pairing_certified=bool(inv_check["sign_cancellation_certified"]),
            unitarity_certified=bool(inv_check["all_links_unitary"]),
        )
