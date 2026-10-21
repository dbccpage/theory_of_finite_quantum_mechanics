
import os
import sys
import unittest
from enum import Enum
from types import ModuleType
from omega_engine.crates.majorana.core.gf2_matrix import GF2Matrix

basic_matrix_mod = ModuleType("omega_runtime.arithmos.linear_algebra.basic_matrix")
proof_mod = ModuleType("omega_runtime.arithmos.linear_algebra.proof")

sys.modules["omega_runtime"] = ModuleType("omega_runtime")
sys.modules["omega_runtime"].__path__ = []

sys.modules["omega_runtime.arithmos"] = ModuleType("omega_runtime.arithmos")
sys.modules["omega_runtime.arithmos"].__path__ = []

sys.modules["omega_runtime.arithmos.linear_algebra"] = ModuleType("omega_runtime.arithmos.linear_algebra")
sys.modules["omega_runtime.arithmos.linear_algebra"].__path__ = []
sys.modules["omega_runtime.arithmos.linear_algebra.basic_matrix"] = basic_matrix_mod
sys.modules["omega_runtime.arithmos.linear_algebra.proof"] = proof_mod

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)


import importlib
class MatrixError(Exception):
    pass
setattr(basic_matrix_mod, "MatrixError", MatrixError)

_bm = importlib.import_module("omega_engine.crates.linear_algebra_theory.basic_matrix")
basic_matrix_mod.__dict__.update(_bm.__dict__)

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
        self.assertEqual(GF2Matrix([]).kernel_basis(), [])

        A = GF2Matrix([[1, 0], [0, 1]])
        self.assertEqual(A.kernel_basis(), [])

        B = GF2Matrix([[1, 1]])
        kb = B.kernel_basis()
        self.assertEqual(kb, [[1, 1]])
        self.assertEqual(B.mat_vec_mul(kb[0]), [0])

        C = GF2Matrix([[1, 1, 0, 0], [0, 0, 1, 1]])
        kb_C = C.kernel_basis()
        self.assertEqual(len(kb_C), 2)
        self.assertIn([1, 1, 0, 0], kb_C)
        self.assertIn([0, 0, 1, 1], kb_C)
        for v in kb_C:
            self.assertEqual(C.mat_vec_mul(v), [0, 0])

    def test_homology_basis_reporter(self):
        from omega_engine.crates.homology_theory import compute_homology

        D0 = [[1, 1, 0], [0, 1, 1], [1, 0, 1]]
        D1 = [[1, 1, 1]]
        res = compute_homology(D0, D1)
        self.assertEqual(res["dim_H1"], 0)
        self.assertEqual(res["basis_H1"], [])

        D0_plaq = [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 1]]
        D1_plaq = [[0, 0, 0, 0]]
        res_pl = compute_homology(D0_plaq, D1_plaq)
        self.assertEqual(res_pl["dim_H1"], 1)
        self.assertEqual(len(res_pl["basis_H1"]), 1)
        v = res_pl["basis_H1"][0]
        d0_mat = GF2Matrix(D0_plaq)
        self.assertIsNone(d0_mat.solve(v))

    def test_certificate_diff(self):
        from omega_engine.crates.majorana.certificates.diff import run_diff

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

        shots = [1, 1, 1, 0, 1, 0, 0, 0, 1, 0]
        shot_checks = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]

        r_maj = resolve_trace_residual(shots, 2, shot_checks, readout_policy="majority")
        self.assertEqual(r_maj, [1, 0])

        r_thresh = resolve_trace_residual(shots, 2, shot_checks, readout_policy="threshold", threshold=0.9)
        self.assertEqual(r_thresh, [0, 0])

        r_win = resolve_trace_residual(shots, 2, shot_checks, readout_policy="declared_window", declared_window=[0, 3])
        self.assertEqual(r_win, [1, 0])

        trace_data = {
            "shots": [1, 0, 0],
            "declared_parity_checks": [[0, 1], [1, 2], [2, 0]],
            "declared_cycles": [[0, 1, 2]],
            "readout_policy": "majority",
        }
        res = process_trace(trace_data)
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

        raw = [[1, 0, 1], [0, 1, 0]]
        g_mat = GF2Matrix(raw)

        b_mat = g_mat.to_basic_matrix()
        self.assertEqual(b_mat.__class__.__name__, "BasicMatrix")
        self.assertEqual(b_mat.rows, 2)
        self.assertEqual(b_mat.cols, 3)
        self.assertEqual(b_mat.to_nested(), raw)

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
        graph = DirectedGraphBuilder.cycle_graph(3, prov)

        adapter = GraphToComplexAdapter.from_finite_directed_graph(graph, faces=[[0, 1, 2]])

        self.assertEqual(adapter.num_vertices, 3)
        self.assertEqual(adapter.num_edges, 3)
        self.assertEqual(adapter.num_faces, 1)
        self.assertEqual(adapter.vertices, ["n0", "n1", "n2"])
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
        graph = DirectedGraphBuilder.cycle_graph(3, prov)
        adapter = GraphToComplexAdapter.from_finite_directed_graph(graph, faces=[[0, 1, 2]])
        self.assertEqual(adapter.edges, [(0, 1), (1, 2), (2, 0)])

    def test_pure_math_abstraction_pipeline(self):
        from omega_engine.crates.homology_theory import DirectedGraphBuilder, GF2ChainComplex
        from omega_engine.crates.majorana.engines.terminalizer import terminalize
        from omega_engine.crates.linear_algebra_theory.proof import TheoremProvenance, ProvenanceKind, TheoremId

        prov = TheoremProvenance(
            kind=ProvenanceKind.FOUNDATION,
            theorem_id=TheoremId("pure-math-pipeline-test")
        )
        graph = DirectedGraphBuilder.from_named(
            nodes=["a", "b", "c"],
            named_edges=[("a", "b"), ("b", "c"), ("c", "a")],
            provenance=prov
        )

        chain = GF2ChainComplex(
            graph=graph,
            faces=((0, 1, 2),),
        )

        self.assertEqual(chain.num_vertices, 3)
        self.assertEqual(chain.num_edges, 3)
        self.assertEqual(chain.num_faces, 1)

        cochain = chain.to_cochain()
        self.assertEqual(cochain.d0.shape(), (3, 3))
        self.assertEqual(cochain.d1.shape(), (1, 3))

        cochain.validate_cochain()

        carrier = cochain.create_carrier([1, 1, 1])

        result = terminalize(
            carrier.D0,
            carrier.D1,
            carrier.residual,
        )
        self.assertEqual(result["terminal_status"], "OpenObstruction")

        no_face_chain = GF2ChainComplex(
            graph=graph,
            faces=(),
        )
        self.assertEqual(no_face_chain.num_faces, 0)

        no_face_cochain = no_face_chain.to_cochain()
        self.assertEqual(no_face_cochain.d1.shape(), (0, 3))

        no_face_carrier = no_face_cochain.create_carrier([1, 1, 1])
        no_face_result = terminalize(
            no_face_carrier.D0,
            no_face_carrier.D1,
            no_face_carrier.residual,
        )
        self.assertEqual(no_face_result["terminal_status"], "ClosedResidual")


if __name__ == "__main__":
    unittest.main()




