import math
import sys
import unittest
from pathlib import Path

import numpy as np

try:
    from repro.src.markov_core import (
        ThetaFamily,
        boundary,
        parametric_kernel,
        poisson_bound,
        poisson_solution,
        pseudo_spectral_gap,
        simulate_parallel_thresholds,
        simulate_test,
        simulate_thresholds,
        stationary,
    )
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from markov_core import (
        ThetaFamily,
        boundary,
        parametric_kernel,
        poisson_bound,
        poisson_solution,
        pseudo_spectral_gap,
        simulate_parallel_thresholds,
        simulate_test,
        simulate_thresholds,
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

    def test_shared_path_thresholds_match_separate_runs(self):
        base = np.array(
            [[0.7, 0.2, 0.1], [0.1, 0.7, 0.2], [0.2, 0.1, 0.7]]
        )
        feature = np.array([1.0, 0.0, -1.0])
        family = ThetaFamily(base, feature, 0.4, 0.8, 101)
        kernel = parametric_kernel(base, feature, -0.6)
        levels = (10.0, 20.0)
        shared = simulate_thresholds(kernel, family, levels, 1234, 5000)
        for level in levels:
            separate = simulate_test(kernel, family, level, 1234, 5000)
            self.assertEqual(shared[level], separate["stopping_time"])

    def test_parallel_thresholds_match_both_separate_runs(self):
        base = np.array(
            [[0.7, 0.2, 0.1], [0.1, 0.7, 0.2], [0.2, 0.1, 0.7]]
        )
        feature = np.array([1.0, 0.0, -1.0])
        p_family = ThetaFamily(base, feature, 0.4, 0.8, 101)
        q_family = ThetaFamily(base, feature, -0.8, -0.4, 101)
        kernel = parametric_kernel(base, feature, -0.6)
        level = 10.0
        shared = simulate_parallel_thresholds(
            kernel,
            p_family,
            (level,),
            q_family,
            (level,),
            4321,
            5000,
            "p",
        )
        p_run = simulate_test(kernel, p_family, level, 4321, 5000)
        q_run = simulate_test(kernel, q_family, level, 4321, 5000)
        self.assertEqual(shared["p"][level], p_run["stopping_time"])
        if q_run["stopping_time"] is not None and q_run["stopping_time"] <= p_run["stopping_time"]:
            self.assertEqual(shared["q"][level], q_run["stopping_time"])


if __name__ == "__main__":
    unittest.main()
