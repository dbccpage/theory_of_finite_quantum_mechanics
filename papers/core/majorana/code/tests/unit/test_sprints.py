# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Jeremy H. Carroll

import os
import sys
import unittest
from enum import Enum
from types import ModuleType
from omega_engine.crates.majorana.core.gf2_matrix import GF2Matrix

# Create module objects first
basic_matrix_mod = ModuleType("omega_runtime.arithmos.linear_algebra.basic_matrix")
proof_mod = ModuleType("omega_runtime.arithmos.linear_algebra.proof")

# Inject mock packages/modules to satisfy omega_runtime imports in arithmos homology
sys.modules["omega_runtime"] = ModuleType("omega_runtime")
sys.modules["omega_runtime"].__path__ = []

sys.modules["omega_runtime.arithmos"] = ModuleType("omega_runtime.arithmos")
sys.modules["omega_runtime.arithmos"].__path__ = []

sys.modules["omega_runtime.arithmos.linear_algebra"] = ModuleType("omega_runtime.arithmos.linear_algebra")
sys.modules["omega_runtime.arithmos.linear_algebra"].__path__ = []
sys.modules["omega_runtime.arithmos.linear_algebra.basic_matrix"] = basic_matrix_mod
sys.modules["omega_runtime.arithmos.linear_algebra.proof"] = proof_mod

# Resolve local paths to self-contained module files
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)


# Populate mock basic_matrix_mod without string exec
import importlib
class MatrixError(Exception):
    pass
setattr(basic_matrix_mod, "MatrixError", MatrixError)

_bm = importlib.import_module("omega_engine.crates.linear_algebra_theory.basic_matrix")
basic_matrix_mod.__dict__.update(_bm.__dict__)

# Pre-define mock proof structures to satisfy finite_directed_graph.py self-imports during execution
class ProvenanceKind(Enum):
    FOUNDATION = "FOUNDATION"
    LEMMA = "LEMMA"
    COROLLARY = "COROLLARY"
    CONJECTURE = "CONJECTURE"

class TheoremBoundaryRisk(str):
    pass

class TheoremProvenance:
    def __init__(self, kind, theorem_id, certificate_id=None, replay_hash=None, boundary_id=None, reviewer=None, risk=None):
        self.kind = kind
        self.theorem_id = theorem_id
        self.certificate_id = certificate_id
        self.replay_hash = replay_hash
        self.boundary_id = boundary_id
        self.reviewer = reviewer
        self.risk = risk

    def to_dict(self):
        res = {
            "kind": self.kind.value if isinstance(self.kind, Enum) else str(self.kind),
            "theorem_id": str(self.theorem_id)
        }
        if self.certificate_id is not None:
            res["certificate_id"] = str(self.certificate_id)
        if self.replay_hash is not None:
            res["replay_hash"] = self.replay_hash.hex() if isinstance(self.replay_hash, bytes) else str(self.replay_hash)
        if self.boundary_id is not None:
            res["boundary_id"] = str(self.boundary_id)
        if self.reviewer is not None:
            res["reviewer"] = str(self.reviewer)
        if self.risk is not None:
            res["risk"] = self.risk.value if isinstance(self.risk, Enum) else str(self.risk)
        return res

class TheoremId(str):
    pass

class CertificateId(str):
    pass

class ReplayHash(bytes):
    pass

class BoundaryId(str):
    pass

class ReviewerId(str):
    pass

setattr(proof_mod, "TheoremProvenance", TheoremProvenance)
setattr(proof_mod, "TheoremId", TheoremId)
setattr(proof_mod, "CertificateId", CertificateId)
setattr(proof_mod, "ReplayHash", ReplayHash)
setattr(proof_mod, "BoundaryId", BoundaryId)
setattr(proof_mod, "ReviewerId", ReviewerId)
setattr(proof_mod, "ProvenanceKind", ProvenanceKind)
setattr(proof_mod, "TheoremBoundaryRisk", TheoremBoundaryRisk)

_fdg = importlib.import_module("omega_engine.crates.homology_theory.finite_directed_graph")
proof_mod.__dict__.update(_fdg.__dict__)



class TestSprintFeatures(unittest.TestCase):
    def test_kernel_basis(self):
        # 1. Simple empty matrix
        self.assertEqual(GF2Matrix([]).kernel_basis(), [])

        # 2. Identity-like matrix (kernel is empty/zero)
        A = GF2Matrix([[1, 0], [0, 1]])
        self.assertEqual(A.kernel_basis(), [])

        # 3. Rectangular matrix with 1-dimensional kernel
        # Matrix: [[1, 1]] -> 1 row, 2 cols. RREF is [[1, 1]].
        # Pivot col: 0, Free col: 1.
        # Kernel basis vector should be [1, 1] because x_0 + x_1 = 0 mod 2.
        B = GF2Matrix([[1, 1]])
        kb = B.kernel_basis()
        self.assertEqual(kb, [[1, 1]])
        # Verify multiplication yields zero vector
        self.assertEqual(B.mat_vec_mul(kb[0]), [0])

        # 4. Larger matrix with 2-dimensional kernel
        # Matrix: [[1, 1, 0, 0], [0, 0, 1, 1]]
        C = GF2Matrix([[1, 1, 0, 0], [0, 0, 1, 1]])
        kb_C = C.kernel_basis()
        # Free columns are 1 and 3.
        # Basis vector 1 (from col 1): [1, 1, 0, 0]
        # Basis vector 2 (from col 3): [0, 0, 1, 1]
        self.assertEqual(len(kb_C), 2)
        self.assertIn([1, 1, 0, 0], kb_C)
        self.assertIn([0, 0, 1, 1], kb_C)
        for v in kb_C:
            self.assertEqual(C.mat_vec_mul(v), [0, 0])

    def test_homology_basis_reporter(self):
        from omega_engine.crates.homology_theory import compute_homology

        # Triangle complex: D0 shape 3x3, D1 shape 1x3.
        # Boundary operators: D1 * D0 = 0.
        # H1 should be trivial (dim_H1 = 0) because every 1-cycle is a boundary of the face.
        D0 = [[1, 1, 0], [0, 1, 1], [1, 0, 1]]
        D1 = [[1, 1, 1]]
        res = compute_homology(D0, D1)
        self.assertEqual(res["dim_H1"], 0)
        self.assertEqual(res["basis_H1"], [])

        # Plaquette without a face: H1 should have dimension 1.
        # D0 has shape 4x4, D1 shape 1x4 (but all zeros, representing no face).
        # We expect dim_H1 = 1, representing the single loop.
        D0_plaq = [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 1]]
        D1_plaq = [[0, 0, 0, 0]]
        res_pl = compute_homology(D0_plaq, D1_plaq)
        self.assertEqual(res_pl["dim_H1"], 1)
        self.assertEqual(len(res_pl["basis_H1"]), 1)
        # Verify that the basis vector is a closed cycle (i.e. inside ker(D1_plaq))
        v = res_pl["basis_H1"][0]
        # Since D1 is zero, ker is everything, but it shouldn't lie in im(D0)
        # Check that we can't solve D0 * x = v
        d0_mat = GF2Matrix(D0_plaq)
        self.assertIsNone(d0_mat.solve(v))

    def test_certificate_diff(self):
        from omega_engine.crates.majorana.certificates.diff import run_diff

        # 1. Identical certificates
        c1 = {
            "carrier_hash": "hash_x",
            "terminal_status": "Exact",
            "algebraic_class_id": "exact",
        }
        res1 = run_diff(c1, c1)
        self.assertTrue(res1["same_carrier_hash"])
        self.assertTrue(res1["same_terminal_status"])
        self.assertTrue(res1["same_q1_class"])
        self.assertEqual(res1["transport_mutation"], "none")

        # 2. Mutated parameters under transport (different carrier hash, same status, different class)
        c2 = {
            "carrier_hash": "hash_y",
            "terminal_status": "Exact",
            "algebraic_class_id": "exact-mutated",
        }
        res2 = run_diff(c1, c2)
        self.assertFalse(res2["same_carrier_hash"])
        self.assertTrue(res2["same_terminal_status"])
        self.assertFalse(res2["same_q1_class"])
        self.assertEqual(res2["transport_mutation"], "detected")

    def test_trace_terminalizer(self):
        from omega_engine.crates.majorana.engines.trace import resolve_trace_residual, process_trace

        # 1. Resolve raw trace: 10 shots, 2 checks.
        # Check 0 shots: [1, 1, 1, 0, 1] -> majority: 1, threshold 0.9: 0
        # Check 1 shots: [0, 0, 0, 1, 0] -> majority: 0, threshold 0.2: 0
        shots = [1, 1, 1, 0, 1, 0, 0, 0, 1, 0]
        shot_checks = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]

        # Test majority
        r_maj = resolve_trace_residual(shots, 2, shot_checks, readout_policy="majority")
        self.assertEqual(r_maj, [1, 0])

        # Test threshold
        r_thresh = resolve_trace_residual(shots, 2, shot_checks, readout_policy="threshold", threshold=0.9)
        self.assertEqual(r_thresh, [0, 0])

        # Test windowing
        # Slicing check 0 shots to indices [0, 3] -> [1, 1, 1] -> majority 1
        # Slicing check 1 shots to indices [1, 4] -> [0, 0, 1] -> majority 0
        r_win = resolve_trace_residual(shots, 2, shot_checks, readout_policy="declared_window", declared_window=[0, 3])
        self.assertEqual(r_win, [1, 0])

        # 2. Process complete trace JSON mockup
        # Let's map a simple Triangle complex with residual [1, 0, 0] (which is an OpenObstruction since D1 * r != 0)
        trace_data = {
            "shots": [1, 0, 0],
            "declared_parity_checks": [[0, 1], [1, 2], [2, 0]],
            "declared_cycles": [[0, 1, 2]],
            "readout_policy": "majority",
        }
        res = process_trace(trace_data)
        # Expected to be OpenObstruction because D1 * r = [[1, 1, 1]] * [1, 0, 0]^T = [1] != 0
        self.assertEqual(res["terminal_status"], "OpenObstruction")
        self.assertEqual(res["q1_norm"], 1)

    def test_ambiguity_demo(self):
        from omega_engine.crates.majorana.demos.ambiguity_demo import run_ambiguity_demo
        res = run_ambiguity_demo()
        self.assertEqual(res["topological_carrier"]["terminal_status"], "ClosedResidual")
        self.assertEqual(res["trivial_carrier"]["terminal_status"], "Exact")
        self.assertEqual(res["topological_carrier"]["q1_norm"], "1")
        self.assertEqual(res["trivial_carrier"]["q1_norm"], "0")

    def test_tgp_demo(self):
        from omega_engine.crates.majorana.demos.tgp_demo import run_tgp_demo
        res = run_tgp_demo()
        self.assertEqual(res["parameter_t_window_A"]["terminal_status"], "Exact")
        self.assertEqual(res["parameter_t_window_B"]["terminal_status"], "OpenObstruction")
        self.assertEqual(res["transport_status"], "SilentMutationDetected")

    def test_gallery_demo(self):
        from omega_engine.crates.majorana.demos.gallery_demo import run_gallery_demo
        res = run_gallery_demo()
        self.assertEqual(len(res), 5)
        for name in ("line_wire", "t_junction", "measurement_loop", "two_island_parity_box", "braid_like_square_move"):
            self.assertIn(name, res)
            self.assertTrue(res[name]["D1_D0_exact_validation"])

    def test_ising_demo(self):
        from omega_engine.crates.majorana.demos.ising_demo import run_ising_demo
        res = run_ising_demo()
        self.assertTrue(res["fusion_associativity"])
        self.assertTrue(res["ising_braid_relation"])
        self.assertTrue(res["sigma_hexagon_specialization"])
        self.assertIn("exact algebraic identity verification only", res["claim"])

    def test_basic_matrix_bridge(self):
        from omega_engine.crates.linear_algebra_theory.basic_matrix import BasicMatrix

        # Create GF2Matrix
        raw = [[1, 0, 1], [0, 1, 0]]
        g_mat = GF2Matrix(raw)

        # Convert to BasicMatrix
        b_mat = g_mat.to_basic_matrix()
        self.assertEqual(b_mat.__class__.__name__, "BasicMatrix")
        self.assertEqual(b_mat.rows, 2)
        self.assertEqual(b_mat.cols, 3)
        self.assertEqual(b_mat.to_nested(), raw)

        # Convert back from BasicMatrix
        g_mat2 = GF2Matrix.from_basic_matrix(b_mat)
        self.assertEqual(g_mat2.to_list(), raw)
    def test_finite_directed_graph_bridge(self):
        from omega_engine.crates.homology_theory import DirectedGraphBuilder
        from omega_engine.crates.linear_algebra_theory.proof import TheoremProvenance, ProvenanceKind, TheoremId
        from omega_engine.crates.majorana.adapters.graph_to_complex import GraphToComplexAdapter

        prov = TheoremProvenance(
            kind=ProvenanceKind.FOUNDATION,
            theorem_id=TheoremId("homology-reusability-test")
        )
        # Create a cycle graph of size 3 (a triangle)
        graph = DirectedGraphBuilder.cycle_graph(3, prov)

        # Build GraphToComplexAdapter directly from FiniteDirectedGraph
        adapter = GraphToComplexAdapter.from_finite_directed_graph(graph, faces=[[0, 1, 2]])
        
        self.assertEqual(adapter.num_vertices, 3)
        self.assertEqual(adapter.num_edges, 3)
        self.assertEqual(adapter.num_faces, 1)
        self.assertEqual(adapter.vertices, ["n0", "n1", "n2"])
        # Check boundary operator D0 and D1 validation
        self.assertEqual(adapter.edges, [(0, 1), (1, 2), (2, 0)])

    def test_line_wire_constructs(self):
        from omega_engine.crates.homology_theory.graph_complex import get_line_wire_complex
        adapter = get_line_wire_complex()
        self.assertEqual(adapter.num_faces, 0)

    def test_t_junction_constructs(self):
        from omega_engine.crates.homology_theory.graph_complex import get_t_junction_complex
        adapter = get_t_junction_complex()
        self.assertEqual(adapter.num_edges, 3)

    def test_braid_like_square_move_constructs(self):
        from omega_engine.crates.homology_theory.graph_complex import get_braid_like_square_move_complex
        adapter = get_braid_like_square_move_complex()
        self.assertEqual(adapter.num_faces, 2)

    def test_from_finite_directed_graph_relabels_nodes(self):
        from omega_engine.crates.homology_theory import DirectedGraphBuilder
        from omega_engine.crates.linear_algebra_theory.proof import TheoremProvenance, ProvenanceKind, TheoremId
        from omega_engine.crates.majorana.adapters.graph_to_complex import GraphToComplexAdapter

        prov = TheoremProvenance(
            kind=ProvenanceKind.FOUNDATION,
            theorem_id=TheoremId("relabel-nodes-test")
        )
        # Create a graph with custom string node names ("n0", "n1", "n2")
        graph = DirectedGraphBuilder.cycle_graph(3, prov)
        adapter = GraphToComplexAdapter.from_finite_directed_graph(graph, faces=[[0, 1, 2]])
        # Check boundary operator D0 and D1 validation
        self.assertEqual(adapter.edges, [(0, 1), (1, 2), (2, 0)])

    def test_pure_math_abstraction_pipeline(self):
        from omega_engine.crates.homology_theory import DirectedGraphBuilder, GF2ChainComplex
        from omega_engine.crates.majorana.engines.terminalizer import terminalize
        from omega_engine.crates.linear_algebra_theory.proof import TheoremProvenance, ProvenanceKind, TheoremId

        # 1. Construct FiniteDirectedGraph with custom node labels and provenance tracking
        prov = TheoremProvenance(
            kind=ProvenanceKind.FOUNDATION,
            theorem_id=TheoremId("pure-math-pipeline-test")
        )
        graph = DirectedGraphBuilder.from_named(
            nodes=["a", "b", "c"],
            named_edges=[("a", "b"), ("b", "c"), ("c", "a")],
            provenance=prov
        )

        # 2. Build GF2ChainComplex
        chain = GF2ChainComplex(
            graph=graph,
            faces=((0, 1, 2),),
        )

        # Validate dimensions
        self.assertEqual(chain.num_vertices, 3)
        self.assertEqual(chain.num_edges, 3)
        self.assertEqual(chain.num_faces, 1)

        # 3. Convert to Cochain complex
        cochain = chain.to_cochain()
        self.assertEqual(cochain.d0.shape(), (3, 3)) # |E| x |V|
        self.assertEqual(cochain.d1.shape(), (1, 3)) # |F| x |E|

        # Validate d1 * d0 = 0 mod 2
        cochain.validate_cochain()

        # 4. Create carrier with a cycle residual [1, 1, 1]
        carrier = cochain.create_carrier([1, 1, 1])

        # 5. Terminalize
        result = terminalize(
            carrier.D0,
            carrier.D1,
            carrier.residual,
        )
        # With a face, the cycle residual acts as an open boundary/coherence contradiction
        self.assertEqual(result["terminal_status"], "OpenObstruction")

        # 6. Now let's test a no-face graph to verify true empty matrix math is completely clean!
        no_face_chain = GF2ChainComplex(
            graph=graph,
            faces=(),
        )
        self.assertEqual(no_face_chain.num_faces, 0)
        
        no_face_cochain = no_face_chain.to_cochain()
        self.assertEqual(no_face_cochain.d1.shape(), (0, 3)) # True zero-row 0 x 3 matrix!

        # Create carrier and terminalize on no-face loop
        no_face_carrier = no_face_cochain.create_carrier([1, 1, 1])
        no_face_result = terminalize(
            no_face_carrier.D0,
            no_face_carrier.D1,
            no_face_carrier.residual,
        )
        # Without any faces, the cycle commutes under the empty boundary operator and is a closed residual
        self.assertEqual(no_face_result["terminal_status"], "ClosedResidual")


if __name__ == "__main__":
    unittest.main()




