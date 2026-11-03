"""Regression witnesses for PR #497's three measurement-boundary corrections.

Run directly with Python (unittest; NumPy required). Visibility and record
examples are numerical finite checks. The dilation checks use exact Fractions.
These checks establish neither a collapse model nor a general Lean theorem.
"""
from fractions import Fraction as F
import unittest

import numpy as np


def reduced_state(psi):
    """Trace the environment out of a two-path pure state, system index first."""
    amplitudes = psi.reshape(2, -1)
    return amplitudes @ amplitudes.conj().T


def trace_environment(rho, env_dim):
    return np.trace(rho.reshape(2, env_dim, 2, env_dim), axis1=1, axis2=3)


def record_permutation(n, mask):
    """Controlled NOTs from the path qubit to the selected record qubits."""
    dim = 2**n
    return [s * dim + (e ^ mask if s else e) for s in range(2) for e in range(dim)]


class VisibilityTests(unittest.TestCase):
    def test_visibility_and_distinguishability_include_path_priors(self):
        # Compute actual fringes by projecting the joint state onto the plus
        # output, and distinguishability from a weighted operator's spectrum.
        for w1 in (0.0, 0.1, 0.5, 0.9, 1.0):
            w2 = 1 - w1
            for overlap in (0.0, 0.3, 0.6, 1.0):
                for marker_phase in (0.0, 0.7):
                    with self.subTest(w1=w1, overlap=overlap, phase=marker_phase):
                        e1 = np.array([1, 0], complex)
                        e2 = np.array([overlap * np.exp(1j * marker_phase),
                                       np.sqrt(1 - overlap**2)])
                        probabilities = []
                        # Align the grid to include both extrema even for a
                        # complex overlap; do not assume its phase is zero.
                        for theta in np.linspace(0, 2*np.pi, 65) - marker_phase:
                            psi = np.concatenate((np.sqrt(w1) * e1,
                                                  np.sqrt(w2) * np.exp(1j*theta) * e2))
                            output = np.array([1, 1]) @ psi.reshape(2, 2) / np.sqrt(2)
                            probabilities.append(np.vdot(output, output).real)
                        pmax, pmin = max(probabilities), min(probabilities)
                        visibility = (pmax - pmin) / (pmax + pmin)
                        weighted_difference = (w1 * np.outer(e1, e1.conj())
                                               - w2 * np.outer(e2, e2.conj()))
                        distinguishability = sum(abs(np.linalg.eigvalsh(weighted_difference)))
                        self.assertAlmostEqual(visibility, 2*np.sqrt(w1*w2)*overlap)
                        self.assertAlmostEqual(distinguishability, np.sqrt(1-4*w1*w2*overlap**2))
                        self.assertAlmostEqual(visibility**2 + distinguishability**2, 1)

    def test_identical_records_do_not_imply_full_visibility(self):
        # Exact probabilities from amplitudes 3/sqrt(10) and 1/sqrt(10).
        pmax, pmin = F((3 + 1)**2, 2 * 10), F((3 - 1)**2, 2 * 10)
        visibility = (pmax - pmin) / (pmax + pmin)
        self.assertEqual(visibility, F(3, 5))
        self.assertNotEqual(visibility, 1)  # rejects the old V = |gamma| claim
        self.assertEqual(abs(F(9, 10) - F(1, 10)), F(4, 5))


class UnitaryDilationTests(unittest.TestCase):
    def setUp(self):
        # Basis |system, environment>; controlled rational rotation.
        self.unitary = np.array([[1, 0, 0, 0], [0, 1, 0, 0],
                                 [0, 0, F(3, 5), F(-4, 5)],
                                 [0, 0, F(4, 5), F(3, 5)]], dtype=object)
        self.ready = np.array([[1, 0], [0, 0]], dtype=object)
        self.kraus = [np.diag([F(1), F(3, 5)]), np.diag([F(0), F(4, 5)])]

    def dilated(self, rho):
        joint = self.unitary @ np.kron(rho, self.ready) @ self.unitary.T
        return trace_environment(joint, 2)

    def test_exact_unitary_dilation_on_a_matrix_basis(self):
        np.testing.assert_array_equal(self.unitary.T @ self.unitary, np.eye(4, dtype=int))
        for e, kraus in enumerate(self.kraus):
            np.testing.assert_array_equal(self.unitary[e::2, ::2], kraus)
        # Agreement on all four matrix units implies agreement for every
        # qubit operator by complex linearity, including imaginary coherences.
        for i in range(2):
            for j in range(2):
                rho = np.zeros((2, 2), dtype=object)
                rho[i, j] = F(1)
                expected = sum(k @ rho @ k.T for k in self.kraus)
                np.testing.assert_array_equal(self.dilated(rho), expected)

    def test_exact_three_step_decay_from_fresh_unitary_environments(self):
        rho = np.full((2, 2), F(1, 2), dtype=object)
        for coherence in (F(3, 10), F(9, 50), F(27, 250)):
            # Reattach |0><0| at each step; no fundamental collapse assumed.
            rho = self.dilated(rho)
            self.assertEqual(rho[0, 1], coherence)
            self.assertEqual(np.trace(rho), 1)
            self.assertEqual(sum(rho.flat) / 2, F(1, 2) + coherence)
            self.assertLess(np.trace(rho @ rho), 1)


class RecordReversalTests(unittest.TestCase):
    def test_reversing_all_records_restores_coherence(self):
        for n in (1, 3, 5):
            with self.subTest(record_qubits=n):
                ready = np.zeros(2**n)
                ready[0] = 1
                initial = np.kron(np.array([3/5, 4j/5]), ready)
                permutation = record_permutation(n, 2**n - 1)
                recorded = initial[permutation]
                np.testing.assert_allclose(reduced_state(recorded), np.diag([9/25, 16/25]))
                # Undo all but one record: the remaining path tag still
                # removes local coherence. Undoing the last restores it.
                partial = recorded[record_permutation(n, 2**n - 2)]
                self.assertAlmostEqual(abs(reduced_state(partial)[0, 1]), 0)
                restored = partial[record_permutation(n, 1)]
                np.testing.assert_allclose(restored, initial)
                np.testing.assert_allclose(reduced_state(restored), reduced_state(initial))
                self.assertGreater(abs(reduced_state(restored)[0, 1]), 0)

    def test_discarding_and_resetting_records_is_not_coherent_reversal(self):
        n = 3
        ready = np.zeros(2**n)
        ready[0] = 1
        initial = np.kron(np.array([3/5, 4j/5]), ready)
        permutation = record_permutation(n, 2**n - 1)
        recorded = initial[permutation]
        # Discard the old records and prepare new blank ones, losing the
        # joint correlations needed to reverse the recording interaction.
        reset = np.kron(reduced_state(recorded), np.outer(ready, ready))
        after_inverse = reset[np.ix_(permutation, permutation)]
        self.assertAlmostEqual(abs(trace_environment(after_inverse, 2**n)[0, 1]), 0)
        self.assertGreater(abs(reduced_state(initial)[0, 1]), 0)

    def test_many_partial_records_need_not_give_exactly_zero_overlap(self):
        for n in (1, 3, 5):
            e1, e2 = np.array([1.0]), np.array([1.0])
            for _ in range(n):
                e1 = np.kron(e1, [1, 0])
                e2 = np.kron(e2, [3/5, 4/5])
            overlap = np.vdot(e1, e2)
            self.assertGreater(overlap, 0)
            self.assertAlmostEqual(overlap, (3/5)**n)
            psi = np.concatenate((e1, e2)) / np.sqrt(2)
            self.assertAlmostEqual(2*abs(reduced_state(psi)[0, 1]), overlap)


if __name__ == '__main__':
    unittest.main(verbosity=2)
