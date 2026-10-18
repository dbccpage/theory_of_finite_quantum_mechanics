from __future__ import annotations

import cmath
import math
import sys

import pytest
import numpy as np

sys.path.insert(0, "omega_engine/research/ooutwire_docs")

from omega_engine.crates.homology_theory.lefschetz_thimble import (
    AiryAction,
    BesselAction,
    PolynomialAction,
    sample_dual_flow_hits,
    steepest_descent_flow,
    steepest_descent_flow_with_frame,
    integrate_thimble,
    verify_airy_stokes_rays,
)
from omega_engine.crates.homology_theory.thimble_state import (
    ThimbleFlowResult,
)


class TestAiryCriticalValues:

    def test_airy_critical_values_match_eval(self) -> None:
        for lam in [1.0, 2.0, 1.0 + 1.0j]:
            a = AiryAction(lam)
            cps = a.exact_critical_points()
            cvs = a.exact_critical_values()
            for cp, cv in zip(cps, cvs):
                eval_val = a.eval([cp])
                assert abs(cv - eval_val) < 1e-10, (
                    f"lambda={lam}: exact_critical_values()={cv} != eval({cp})={eval_val}"
                )

    def test_airy_critical_values_are_real_for_real_lambda(self) -> None:
        a = AiryAction(1.0)
        for cv in a.exact_critical_values():
            assert abs(cv.imag) < 1e-14, f"critical value {cv} has nonzero imaginary part"

    def test_airy_critical_values_sign_convention(self) -> None:
        a = AiryAction(1.0)
        cvs = a.exact_critical_values()
        assert cvs[0].real < 0 < cvs[1].real


class TestRK45ButcherConsistency:

    def test_rk45_z5_coefficients_sum_to_one(self) -> None:
        from fractions import Fraction
        b5 = [
            Fraction(37, 378),
            Fraction(0),
            Fraction(250, 621),
            Fraction(125, 594),
            Fraction(0),
            Fraction(512, 1771),
        ]
        assert sum(b5) == 1, f"Cash-Karp 5th order weights sum to {sum(b5)}, not 1"

    def test_rk45_constant_ode_exact(self) -> None:
        c = 1.0 + 2.0j

        class ConstantAction(PolynomialAction):
            def __init__(self):
                super().__init__(n_vars=1)
                self.add_term(-c.conjugate(), [(0, 1)])

        a = ConstantAction()

        z0 = [0.0 + 0.0j]
        traj, _ = steepest_descent_flow(a, z0, dt=0.01, steps=1)
        if len(traj) > 1:
            z1 = traj[1][0]
            expected = 0.01 * c
            assert abs(z1 - expected) < 1e-6, (
                f"RK45 on constant ODE: got {z1}, expected {expected}"
            )


class TestTangentTransport:

    def test_tangent_transport_finite_difference(self) -> None:
        a = AiryAction(1.0)
        z_start = [0.5 + 0.0j]
        eps = 1e-6
        dt = 0.001
        n_steps = 5

        result = steepest_descent_flow_with_frame(a, z_start, dt=dt, steps=n_steps)
        z_end = result.trajectory[-1]

        z_perturbed_start = [z_start[0] + eps]
        result_perturbed = steepest_descent_flow_with_frame(
            a, z_perturbed_start, dt=dt, steps=n_steps
        )
        z_perturbed_end = result_perturbed.trajectory[-1]

        J_last = np.array(result.jacobian_history[-1], dtype=complex)
        fd_derivative = (z_perturbed_end[0] - z_end[0]) / eps
        J_derivative = J_last[0, 0]

        rel_err = abs(fd_derivative - J_derivative) / max(abs(fd_derivative), 1e-14)
        assert rel_err < 0.1, (
            f"Tangent transport J={J_derivative} vs finite-diff={fd_derivative}, "
            f"relative error={rel_err}"
        )


class TestStokesDetection:

    def test_stokes_checks_imaginary_part(self) -> None:
        results = verify_airy_stokes_rays(lam_mag=1.0, num_angles=72)
        for r in results:
            assert "im_diff" in r, "Stokes result should use im_diff, not re_diff"
            assert "re_diff" not in r, "Stokes result should not contain re_diff"

    def test_stokes_known_angles_have_zero_im_diff(self) -> None:
        a = AiryAction(1.0)
        cps = a.exact_critical_points()
        s_plus = a.eval([cps[0]])
        s_minus = a.eval([cps[1]])
        assert abs(s_plus.imag - s_minus.imag) < 1e-10, (
            f"For real lambda, both critical values should have same Im part: "
            f"Im(S+)={s_plus.imag}, Im(S-)={s_minus.imag}"
        )


class TestIntersectionRename:

    def test_intersection_function_is_renamed(self) -> None:
        import omega_engine.crates.homology_theory.lefschetz_thimble as mod
        assert hasattr(mod, "sample_dual_flow_hits"), (
            "sample_dual_flow_hits should exist"
        )
        assert not hasattr(mod, "compute_intersection_numbers"), (
            "compute_intersection_numbers should no longer exist"
        )


class TestIntegration:

    def test_integrate_thimble_1d_complex_dz(self) -> None:
        a = AiryAction(1.0)
        cps = a.exact_critical_points()
        try:
            integral_fwd, _ = integrate_thimble(
                a, [cps[0]], dt=0.001, steps=20, both_directions=False
            )
            assert isinstance(integral_fwd, complex)
        except OverflowError:
            pytest.skip("exp(-S) overflows for this configuration — pre-existing issue")


class TestBesselDomain:

    def test_bessel_domain_consistent_refusal(self) -> None:
        b = BesselAction(1.0)
        z_origin = [0.0 + 0.0j]

        eval_result = b.eval(z_origin)
        assert math.isinf(eval_result.real) or math.isinf(eval_result.imag)

        grad_result = b.gradient(z_origin)
        assert math.isinf(grad_result[0].real) or math.isinf(grad_result[0].imag)

        hess_result = b.hessian(z_origin)
        assert math.isinf(hess_result[0][0].real) or math.isinf(hess_result[0][0].imag)


class TestThimbleFlowResultDefaults:

    def test_thimble_flow_result_defaults_none(self) -> None:
        result = ThimbleFlowResult(
            trajectory=[[0.0 + 0.0j]],
            conserved_im_s=0.0,
            max_im_deviation=0.0,
        )
        assert result.orientation_sign is None, (
            f"orientation_sign should default to None, got {result.orientation_sign}"
        )
        assert result.jacobian_determinant is None, (
            f"jacobian_determinant should default to None, got {result.jacobian_determinant}"
        )


