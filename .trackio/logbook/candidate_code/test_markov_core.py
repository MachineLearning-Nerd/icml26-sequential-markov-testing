import math
import sys
import unittest
from pathlib import Path

import numpy as np

try:
    from repro.src.markov_core import (
        boundary,
        poisson_bound,
        poisson_solution,
        pseudo_spectral_gap,
        stationary,
    )
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from markov_core import (
        boundary,
        poisson_bound,
        poisson_solution,
        pseudo_spectral_gap,
        stationary,
    )


class TestMarkovCore(unittest.TestCase):
    def test_two_state_pseudo_gap_and_poisson_bound(self):
        kernel = np.array([[0.8, 0.2], [0.3, 0.7]])
        gap, best_k, _ = pseudo_spectral_gap(kernel)
        self.assertAlmostEqual(gap, 1 - (1 - 0.2 - 0.3) ** 2, places=10)
        self.assertEqual(best_k, 1)
        constant, actual, _, _ = poisson_bound(kernel)
        self.assertLessEqual(actual, constant)
        function = np.array([1.0, -0.5])
        omega = poisson_solution(kernel, function)
        pi = stationary(kernel)
        residual = (np.eye(2) - kernel) @ omega - (function - pi @ function)
        self.assertLess(np.max(np.abs(residual)), 1e-10)

    def test_algorithm_boundary(self):
        visits = np.array([3, 0, 2, 1, 0])
        psi = np.log(math.e * (1 + visits / 4)).sum()
        self.assertAlmostEqual(boundary(visits, math.log(20)), math.log(20) + 4 * psi)


if __name__ == "__main__":
    unittest.main()
