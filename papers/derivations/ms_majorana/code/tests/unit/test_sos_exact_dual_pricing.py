"""SoS exact dual pricing (FW-8 rail) — golden fixtures + kill tests.

AuthorityEffect: None.
"""

from __future__ import annotations

import unittest
from decimal import Decimal
from fractions import Fraction
from itertools import combinations

from sympy import Matrix, Rational

from omega_engine.crates.functional.degree_k_phi import DegreeKPricingDeclaration
from omega_engine.crates.functional.higher_simplex_assembly import (
    SimplexComplex,
    assemble_from_network,
    rational_boundary_matrix,
)
from omega_engine.crates.residuals.network_residual import Network
from omega_engine.crates.solver.solv_omega_engine_solver_of_solvers.solv_exact_dual_pricing import (
    ExactDualPricingError,
    price_degree_k_with_optional_nilpotency,
    price_exact_degree_k,
    price_network_phi1_exact,
    refuse_attainment_as_estate_quotient_norm,
    refuse_float_as_exact,
    refuse_ls_as_canonical,
    refuse_phi1_sold_as_phi2,
)
from omega_engine.crates.solver.solv_omega_engine_solver_of_solvers.solv_oesos import (
    CascadeSolver,
)


class TestSoSExactDualPricingGoldens(unittest.TestCase):
    def test_fw8_tetra_phi2_equals_4(self):
        """Boundary of a tetrahedron, omega=(2,4,4,6) => Phi_2=4, gap 0."""
        nodes = [0, 1, 2, 3]
        edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
        faces = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
        net = Network(nodes=nodes, edges=edges, faces=faces)
        cx = assemble_from_network(net, max_dim=3)
        from omega_engine.crates.functional.degree_k_phi import phi_k_on_complex_exact

        dec = DegreeKPricingDeclaration.exact_l1(2)
        receipt = phi_k_on_complex_exact(cx, 2, [2, 4, 4, 6], dec)
        self.assertEqual(receipt.primal_value, Rational(4))
        self.assertEqual(receipt.exact_gap, Rational(0))
        self.assertTrue(receipt.is_certified)

        cells_k = list(cx.cells[2])
        cells_km1 = list(cx.cells[1])
        from omega_engine.crates.functional.higher_simplex_assembly import (
            rational_boundary_matrix,
        )

        d_lower = rational_boundary_matrix(cells_k, cells_km1).T
        sos = price_exact_degree_k(d_lower, [2, 4, 4, 6], dec, degree=2)
        self.assertTrue(sos.is_certified)
        self.assertEqual(sos.phi_k, Rational(4))
        self.assertEqual(sos.exact_gap, Rational(0))
        self.assertEqual(sos.arithmetic_mode, "Q")
        self.assertEqual(sos.dual_witness_status, "certified_exact")

    def test_fw8_tetra_exact_cochain_phi2_zero(self):
        """Same carrier, omega=(3,3,5,5) => Phi_2=0, gap 0."""
        nodes = [0, 1, 2, 3]
        edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
        faces = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
        net = Network(nodes=nodes, edges=edges, faces=faces)
        cx = assemble_from_network(net, max_dim=3)
        from omega_engine.crates.functional.degree_k_phi import phi_k_on_complex_exact

        dec = DegreeKPricingDeclaration.exact_l1(2)
        receipt = phi_k_on_complex_exact(cx, 2, [3, 3, 5, 5], dec)
        self.assertEqual(receipt.primal_value, Rational(0))
        self.assertEqual(receipt.exact_gap, Rational(0))
        self.assertTrue(receipt.is_certified)

    def test_multi_degree_phi1_phi2_phi3_exact_battery(self):
        """Listed multi-degree fixtures: Φ₁/Φ₂/Φ₃ all Q zero-gap via SoS adapter.

        Finite-scope only — does not mint an estate-wide degree-n theorem.
        """
        net = Network(nodes=[0, 1, 2], edges=[(0, 1), (1, 2), (0, 2)])
        r1 = price_network_phi1_exact(net, {(0, 1): 2, (1, 2): 3, (0, 2): 5})
        self.assertEqual(r1.degree, 1)
        self.assertEqual(r1.phi_k, Rational(0))
        self.assertEqual(r1.exact_gap, Rational(0))
        self.assertEqual(r1.arithmetic_mode, "Q")
        self.assertEqual(r1.dual_witness_status, "certified_exact")

        verts4 = list(range(4))
        cx2 = SimplexComplex(
            vertices=verts4,
            cells={d: list(combinations(verts4, d + 1)) for d in range(3)},
            max_dim=2,
        )
        d1 = rational_boundary_matrix(list(cx2.cells[2]), list(cx2.cells[1])).T
        r2 = price_exact_degree_k(
            d1, [2, 4, 4, 6], DegreeKPricingDeclaration.exact_l1(2), degree=2
        )
        self.assertEqual(r2.degree, 2)
        self.assertEqual(r2.phi_k, Rational(4))
        self.assertEqual(r2.exact_gap, Rational(0))
        self.assertEqual(r2.dual_witness_status, "certified_exact")

        r2z = price_exact_degree_k(
            d1, [3, 3, 5, 5], DegreeKPricingDeclaration.exact_l1(2), degree=2
        )
        self.assertEqual(r2z.degree, 2)
        self.assertEqual(r2z.phi_k, Rational(0))
        self.assertEqual(r2z.exact_gap, Rational(0))
        self.assertEqual(r2z.dual_witness_status, "certified_exact")
        self.assertEqual(
            r2z.as_cascade_fields()["estate_wide_phi_k_theorem"], "REFUSED"
        )

        verts5 = list(range(5))
        cx3 = SimplexComplex(
            vertices=verts5,
            cells={d: list(combinations(verts5, d + 1)) for d in range(4)},
            max_dim=3,
        )
        d2 = rational_boundary_matrix(list(cx3.cells[3]), list(cx3.cells[2])).T
        r3 = price_exact_degree_k(
            d2,
            [1, -1, 1, -1, 1],
            DegreeKPricingDeclaration.exact_l1(3),
            degree=3,
        )
        self.assertEqual(r3.degree, 3)
        self.assertEqual(r3.phi_k, Rational(5))
        self.assertEqual(r3.exact_gap, Rational(0))
        self.assertEqual(r3.dual_witness_status, "certified_exact")
        self.assertEqual(r3.y_star, ("1", "-1", "1", "-1", "1"))

        with self.assertRaises(ExactDualPricingError) as ctx:
            refuse_phi1_sold_as_phi2(declared_degree=2, computed_degree=r1.degree)
        self.assertEqual(ctx.exception.code, "DEGREE_MISMATCH")

    def test_network_phi1_gradient_exact_zero(self):
        """Exact gradient cochain on triangle: Phi_1=0, dual certified."""
        net = Network(nodes=[0, 1, 2], edges=[(0, 1), (1, 2), (0, 2)])
        residual = {
            (0, 1): 2,
            (1, 2): Fraction(3, 1),
            (0, 2): Decimal("5"),
        }
        receipt = price_network_phi1_exact(net, residual)
        self.assertTrue(receipt.is_certified)
        self.assertEqual(receipt.phi_k, Rational(0))
        self.assertEqual(receipt.exact_gap, Rational(0))
        self.assertEqual(receipt.degree, 1)
        self.assertEqual(receipt.estate_wide_phi_k_theorem, "REFUSED")
        self.assertEqual(receipt.normhood_from_attainment_alone, "REFUSED")
        self.assertEqual(receipt.authority_effect, "None")
        casc = receipt.as_cascade_fields()
        self.assertEqual(casc["estate_wide_phi_k_theorem"], "REFUSED")
        self.assertEqual(casc["normhood_from_attainment_alone"], "REFUSED")

    def test_network_phi1_cycle_positive(self):
        """Oriented cycle residual has positive Phi_1 with zero dual gap."""
        net = Network(nodes=[0, 1, 2], edges=[(0, 1), (1, 2), (0, 2)])
        residual = {(0, 1): 1, (1, 2): 1, (0, 2): 0}
        receipt = price_network_phi1_exact(net, residual)
        self.assertTrue(receipt.is_certified)
        self.assertGreater(receipt.phi_k, Rational(0))
        self.assertEqual(receipt.exact_gap, Rational(0))

    def test_cascade_solve_emits_exact_dual_fields(self):
        """A float cascade remains diagnostic even when its dual gap vanishes."""
        net = Network(
            nodes=[0, 1, 2],
            edges=[(0, 1), (1, 2), (0, 2)],
            faces=[(0, 1, 2)],
        )
        omega = {(0, 1): 2.0, (1, 2): 3.0, (0, 2): 5.0}
        solver = CascadeSolver(net)
        receipt = solver.solve(omega)
        self.assertIn("ExactDualPricing", receipt.stages_executed)
        self.assertEqual(receipt.arithmetic_mode, "diagnostic_float")
        self.assertTrue(receipt.dual_witness_status.startswith("float_diagnostic_"))
        self.assertFalse(receipt.is_certified)
        self.assertFalse(receipt.is_exact_dual_certified())
        self.assertIsNone(receipt.exact_phi_k)
        self.assertIsNotNone(receipt.diagnostic_residual_mass)

    def test_exact_dual_survives_elevated_degree_window(self):
        """A lifted float residual cannot acquire exact-Q status."""
        net = Network(
            nodes=[0, 1, 2],
            edges=[(0, 1), (1, 2), (0, 2)],
            faces=[(0, 1, 2)],
        )
        solver = CascadeSolver(net)
        solver.dda_engine.degree_window = 3
        cochain = {(0, 1): 1.0, (1, 2): 1.0, (0, 2): 0.0}
        ok, gap, status, exact_rcpt = solver._get_exact_dual_cert(cochain)
        self.assertFalse(ok)
        self.assertTrue(status.startswith("float_diagnostic_"))
        self.assertIsNone(exact_rcpt)
        self.assertIsNotNone(gap)
        dual_kw = solver._dual_fields_for_receipt(cochain, diagnostic_mass=2.0)
        self.assertEqual(dual_kw["arithmetic_mode"], "diagnostic_float")
        self.assertTrue(
            dual_kw["dual_witness_status"].startswith("float_diagnostic_")
        )
        self.assertFalse(dual_kw["is_certified"])

    def test_cascade_as_evidence_dict_spine_fence(self):
        """Float evidence stays diagnostic and keeps the residual fence.

        Live receipt attrs also refuse estate-wide / normhood-from-attainment
        on the diagnostic path (not spine-fence-only).
        """
        net = Network(
            nodes=[0, 1, 2],
            edges=[(0, 1), (1, 2), (0, 2)],
            faces=[(0, 1, 2)],
        )
        omega = {(0, 1): 2.0, (1, 2): 3.0, (0, 2): 5.0}
        receipt = CascadeSolver(net).solve(omega)
        self.assertEqual(receipt.estate_wide_phi_k_theorem, "REFUSED")
        self.assertEqual(receipt.normhood_from_attainment_alone, "REFUSED")
        dual_kw = CascadeSolver(net)._dual_fields_for_receipt(omega, 0.0)
        self.assertEqual(dual_kw["estate_wide_phi_k_theorem"], "REFUSED")
        self.assertEqual(dual_kw["normhood_from_attainment_alone"], "REFUSED")
        self.assertTrue(
            dual_kw["dual_witness_status"].startswith("float_diagnostic_")
        )
        ev = receipt.as_evidence_dict()
        self.assertEqual(ev["arithmetic_mode"], "diagnostic_float")
        self.assertTrue(ev["dual_witness_status"].startswith("float_diagnostic_"))
        self.assertFalse(ev["is_exact_dual_certified"])
        self.assertEqual(ev["authority_effect"], "None")
        self.assertEqual(ev["estate_wide_phi_k_theorem"], "REFUSED")
        self.assertEqual(ev["normhood_from_attainment_alone"], "REFUSED")
        fence = ev["spine_fence"]
        self.assertEqual(fence["continuum_superspace_wdw"], "REFUSED")
        self.assertEqual(fence["pontryagin_dual_pi_programme"], "STAGED_HOST")
        self.assertEqual(fence["finite_declared_quotient_norm"], "AVAILABLE")
        self.assertEqual(fence["float_as_exact"], "REFUSED")
        self.assertEqual(fence["holy_land_rec_full"], "REFUSED_WITHOUT_EVIDENCE")
        self.assertEqual(fence["estate_wide_phi_k_theorem"], "REFUSED")
        self.assertEqual(fence["normhood_from_attainment_alone"], "REFUSED")
        self.assertIn("pricing language", fence["coda_cs_coda_q"])
        self.assertIn("ExactDualPricing", ev["stages_executed"])

    def test_nilpotency_gate_refuses_bad_pair(self):
        """Phi_k refused when supplied upper/lower maps fail nilpotency."""
        d_lower = Matrix([[1, 0], [0, 1], [1, 1]])
        d_upper = Matrix([[1, 0, 0], [0, 1, 0]])
        dec = DegreeKPricingDeclaration.exact_l1(1)
        with self.assertRaises(ExactDualPricingError) as ctx:
            price_degree_k_with_optional_nilpotency(
                d_lower, [1, 0, 0], dec, d_upper=d_upper
            )
        self.assertEqual(ctx.exception.code, "NILPOTENCY_FAILED")

    def test_float_fallback_never_sets_is_certified(self):
        """When exact rail fails, float dual may report gaps but never is_certified."""
        import omega_engine.crates.solver.solv_omega_engine_solver_of_solvers.solv_oesos as oesos

        net = Network(
            nodes=[0, 1, 2],
            edges=[(0, 1), (1, 2), (0, 2)],
            faces=[(0, 1, 2)],
        )
        cochain = {(0, 1): 1.0, (1, 2): 1.0, (0, 2): 0.0}
        solver = CascadeSolver(net)

        def _exact_raises(*_a, **_k):
            raise RuntimeError("forced exact-rail failure for float path")

        def _float_claims_certified(nodes, edges, vec):
            return {"is_certified": True, "duality_gap": 0.0}

        saved_exact = oesos.price_network_phi1_exact
        saved_float = oesos.solve_phi1_dual_witness
        try:
            oesos.price_network_phi1_exact = _exact_raises
            oesos.solve_phi1_dual_witness = _float_claims_certified
            ok, gap, status, exact_rcpt = solver._get_exact_dual_cert(cochain)
            self.assertFalse(ok)
            self.assertIsNone(exact_rcpt)
            self.assertEqual(status, "float_diagnostic_certified")
            self.assertEqual(gap, 0.0)
            dual_kw = solver._dual_fields_for_receipt(cochain, diagnostic_mass=2.0)
            self.assertFalse(dual_kw["is_certified"])
            self.assertEqual(dual_kw["arithmetic_mode"], "diagnostic_float")
            self.assertIsNone(dual_kw["exact_phi_k"])
            self.assertEqual(dual_kw["dual_witness_status"], "float_diagnostic_certified")
            self.assertEqual(dual_kw["estate_wide_phi_k_theorem"], "REFUSED")
            self.assertEqual(dual_kw["normhood_from_attainment_alone"], "REFUSED")
            with self.assertRaises(ExactDualPricingError) as ctx:
                refuse_float_as_exact(True, dual_kw["arithmetic_mode"])
            self.assertEqual(ctx.exception.code, "FLOAT_AS_EXACT")
            refuse_float_as_exact(False, dual_kw["arithmetic_mode"])
        finally:
            oesos.price_network_phi1_exact = saved_exact
            oesos.solve_phi1_dual_witness = saved_float


class TestSoSExactDualPricingKills(unittest.TestCase):
    def test_refuse_float_as_exact(self):
        net = Network(nodes=[0, 1], edges=[(0, 1)])
        with self.assertRaises(ExactDualPricingError) as exact_ctx:
            price_network_phi1_exact(net, {(0, 1): 0.5})
        self.assertEqual(exact_ctx.exception.code, "FLOAT_SCALAR")

        with self.assertRaises(ExactDualPricingError) as ctx:
            refuse_float_as_exact(True, "float_lp_dual_certificate_PROTO")
        self.assertEqual(ctx.exception.code, "FLOAT_AS_EXACT")
        with self.assertRaises(ExactDualPricingError) as q_ctx:
            refuse_float_as_exact(True, "Q")
        self.assertEqual(q_ctx.exception.code, "FLOAT_AS_EXACT")
        refuse_float_as_exact(False, "Q")

    def test_refuse_ls_as_canonical(self):
        with self.assertRaises(ExactDualPricingError) as ctx:
            refuse_ls_as_canonical("CANONICAL")
        self.assertEqual(ctx.exception.code, "LS_AS_CANONICAL")
        refuse_ls_as_canonical("SURROGATE_ONLY")

    def test_refuse_phi1_sold_as_phi2(self):
        with self.assertRaises(ExactDualPricingError) as ctx:
            refuse_phi1_sold_as_phi2(2, 1)
        self.assertEqual(ctx.exception.code, "DEGREE_MISMATCH")

    def test_refuse_attainment_as_estate_quotient_norm(self):
        """Finite dual gap-0 does not mint estate-wide quotient-norm theorem."""
        with self.assertRaises(ExactDualPricingError) as ctx:
            refuse_attainment_as_estate_quotient_norm(
                claim_estate_wide_quotient_norm=True
            )
        self.assertEqual(ctx.exception.code, "ATTAINMENT_AS_ESTATE_QUOTIENT_NORM")
        with self.assertRaises(ExactDualPricingError) as ctx2:
            refuse_attainment_as_estate_quotient_norm(
                claim_estate_wide_quotient_norm=False,
                claim_normhood_from_attainment_alone=True,
            )
        self.assertEqual(ctx2.exception.code, "ATTAINMENT_AS_ESTATE_QUOTIENT_NORM")
        refuse_attainment_as_estate_quotient_norm(
            claim_estate_wide_quotient_norm=False,
            claim_normhood_from_attainment_alone=False,
        )
        net = Network(nodes=[0, 1, 2], edges=[(0, 1), (1, 2), (0, 2)])
        r = price_network_phi1_exact(net, {(0, 1): 2, (1, 2): 3, (0, 2): 5})
        fields = r.as_cascade_fields()
        self.assertEqual(fields["estate_wide_phi_k_theorem"], "REFUSED")
        self.assertEqual(fields["normhood_from_attainment_alone"], "REFUSED")
        self.assertEqual(r.dual_witness_status, "certified_exact")

    def test_missing_declaration_refused(self):
        from omega_engine.crates.functional.degree_k_phi import (
            DegreeKPricingRefused,
            solve_degree_k_phi_exact,
        )

        d = Matrix([[1], [-1]])
        w = Matrix([1, 0])
        with self.assertRaises(DegreeKPricingRefused):
            solve_degree_k_phi_exact(d, w, None)


if __name__ == "__main__":
    unittest.main()
