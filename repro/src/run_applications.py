from __future__ import annotations

import json
import math
import time
from dataclasses import dataclass

import cvxpy as cp
import gymnasium as gym
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, minimize

from markov_core import boundary, empirical_log_likelihood, stationary
from run_core_campaign import (
    ARTIFACTS,
    SEED,
    common_files,
    csv_rows,
    dump,
    text,
)


TARGET = np.array([0.1, 0.1, 0.2, 0.2, 0.4])
Q_BAD = np.array(
    [
        [0.1, 0.5, 0.1, 0.1, 0.2],
        [0.2, 0.1, 0.4, 0.2, 0.1],
        [0.1, 0.1, 0.1, 0.6, 0.1],
        [0.3, 0.2, 0.1, 0.1, 0.3],
        [0.1, 0.1, 0.1, 0.1, 0.6],
    ]
)
Q_GOOD = np.array(
    [
        [0.50, 0.20, 0.00, 0.00, 0.30],
        [0.20, 0.50, 0.30, 0.00, 0.00],
        [0.00, 0.15, 0.50, 0.35, 0.00],
        [0.00, 0.00, 0.35, 0.50, 0.15],
        [0.075, 0.00, 0.00, 0.075, 0.85],
    ]
)


class StationaryNullProjector:
    def __init__(self, target: np.ndarray, solver: str = "CLARABEL") -> None:
        m = len(target)
        self.counts = cp.Parameter((m, m), nonneg=True)
        self.kernel = cp.Variable((m, m))
        constraints = [
            self.kernel >= 1e-10,
            cp.sum(self.kernel, axis=1) == 1,
            target @ self.kernel == target,
        ]
        self.problem = cp.Problem(
            cp.Maximize(cp.sum(cp.multiply(self.counts, cp.log(self.kernel)))),
            constraints,
        )
        self.solver = solver

    def statistic(self, counts: np.ndarray) -> float:
        self.counts.value = counts
        self.problem.solve(solver=self.solver, warm_start=True, verbose=False)
        if self.problem.status not in {"optimal", "optimal_inaccurate"}:
            raise RuntimeError(f"MCMC projection failed: {self.problem.status}")
        return max(0.0, empirical_log_likelihood(counts) - float(self.problem.value))


def simulate_mcmc(
    kernel: np.ndarray,
    projector: StationaryNullProjector,
    seed: int,
    horizon: int,
    check_interval: int,
    alpha: float,
) -> dict:
    rng = np.random.default_rng(seed)
    state = seed % 5
    counts = np.zeros((5, 5), dtype=np.int64)
    trace = []
    stop = None
    for step in range(1, horizon + 1):
        next_state = int(rng.choice(5, p=kernel[state]))
        counts[state, next_state] += 1
        state = next_state
        if step % check_interval == 0:
            statistic = projector.statistic(counts)
            beta = boundary(counts.sum(axis=1), math.log(1 / alpha))
            trace.append({"time": step, "L_t": statistic, "beta_t": beta})
            if statistic >= beta:
                stop = step
                break
    return {"stopping_time": stop, "trace": trace, "counts": counts.tolist()}


def run_mcmc() -> dict:
    alpha = 0.05
    primary = StationaryNullProjector(TARGET)
    bad_runs = [
        simulate_mcmc(Q_BAD, primary, SEED + 100000 + i, 10000, 50, alpha)
        for i in range(100)
    ]
    good_runs = [
        simulate_mcmc(Q_GOOD, primary, SEED + 110000 + i, 10000, 250, alpha)
        for i in range(100)
    ]
    bad_stops = [run["stopping_time"] for run in bad_runs]
    good_stops = [run["stopping_time"] for run in good_runs]
    assert all(value is not None for value in bad_stops)
    assert all(value is None for value in good_stops)
    independent = StationaryNullProjector(TARGET, solver="SCS")
    sample_counts = np.asarray(bad_runs[0]["counts"])
    primary_value = primary.statistic(sample_counts)
    independent_value = independent.statistic(sample_counts)
    agreement = abs(primary_value - independent_value) / (1 + primary_value)
    assert agreement < 2e-3
    return {
        "paper_target": TARGET.tolist(),
        "stationary_bad": stationary(Q_BAD).tolist(),
        "stationary_good": stationary(Q_GOOD).tolist(),
        "bad_detection_rate": 1.0,
        "good_false_rejections": 0,
        "trials_each": 100,
        "mean_bad_stop": float(np.mean(bad_stops)),
        "sd_bad_stop": float(np.std(bad_stops, ddof=1)),
        "check_interval_bad": 50,
        "check_interval_good": 250,
        "horizon": 10000,
        "independent_primary_L": primary_value,
        "independent_scs_L": independent_value,
        "independent_relative_gap": agreement,
        "bad_runs": bad_runs,
        "good_runs": good_runs,
    }


def rbf_features(dimension: int, sigma: float = 32.0) -> np.ndarray:
    indices = np.arange(192, dtype=float)
    centers = np.linspace(0, 191, dimension - 1)
    values = [np.ones(192)]
    values.extend(np.exp(-((indices - center) ** 2) / (2 * sigma**2)) for center in centers)
    features = np.stack(values, axis=1)
    return features / features.sum(axis=1, keepdims=True)


class LinearMDPProjector:
    def __init__(self, features: np.ndarray, solver: str = "CLARABEL") -> None:
        d = features.shape[1]
        self.counts = cp.Parameter((192, 64), nonneg=True)
        self.weights = cp.Variable((d, 64))
        transition = features @ self.weights
        constraints = [
            self.weights >= 1e-10,
            cp.sum(self.weights, axis=1) == 1,
        ]
        self.problem = cp.Problem(
            cp.Maximize(cp.sum(cp.multiply(self.counts, cp.log(transition)))),
            constraints,
        )
        self.solver = solver
        self.fallback_count = 0

    def statistic(self, full_counts: np.ndarray) -> float:
        collapsed = full_counts.reshape(192, 64, 3).sum(axis=2)
        total = int(full_counts.sum())
        self.counts.value = collapsed / total
        try:
            self.problem.solve(solver=self.solver, warm_start=True, verbose=False)
        except cp.error.SolverError:
            if self.solver == "SCS":
                raise
            self.fallback_count += 1
            self.problem.solve(
                solver="SCS",
                warm_start=False,
                verbose=False,
                eps=1e-5,
                max_iters=50000,
            )
        if self.problem.status not in {"optimal", "optimal_inaccurate"}:
            raise RuntimeError(f"linear-MDP projection failed: {self.problem.status}")
        null_log_likelihood = total * float(self.problem.value) - total * math.log(3)
        return max(0.0, empirical_log_likelihood(full_counts) - null_log_likelihood)


def independent_linear_mdp_statistic(
    features: np.ndarray, full_counts: np.ndarray
) -> tuple[float, dict]:
    """Solve the same concave projection with SciPy, independently of CVXPY."""
    collapsed = full_counts.reshape(192, 64, 3).sum(axis=2)
    total = int(full_counts.sum())
    normalized = collapsed / total
    dimension = features.shape[1]

    def objective(flat_weights: np.ndarray) -> tuple[float, np.ndarray]:
        weights = flat_weights.reshape(dimension, 64)
        transition = np.maximum(features @ weights, 1e-300)
        value = -float(np.sum(normalized * np.log(transition)))
        gradient = -(features.T @ (normalized / transition))
        return value, gradient.ravel()

    row_sum_matrix = np.zeros((dimension, dimension * 64))
    for row in range(dimension):
        row_sum_matrix[row, row * 64 : (row + 1) * 64] = 1.0
    result = minimize(
        objective,
        np.full(dimension * 64, 1 / 64),
        jac=True,
        method="SLSQP",
        bounds=Bounds(1e-10, 1.0),
        constraints=LinearConstraint(row_sum_matrix, 1.0, 1.0),
        options={"ftol": 1e-11, "maxiter": 3000, "disp": False},
    )
    if not result.success:
        raise RuntimeError(f"independent SciPy projection failed: {result.message}")
    null_log_likelihood = -total * float(result.fun) - total * math.log(3)
    statistic = max(
        0.0, empirical_log_likelihood(full_counts) - null_log_likelihood
    )
    diagnostics = {
        "solver": "scipy.optimize.SLSQP",
        "success": bool(result.success),
        "iterations": int(result.nit),
        "row_sum_error": float(
            np.max(
                np.abs(
                    result.x.reshape(dimension, 64).sum(axis=1)
                    - 1
                )
            )
        ),
        "minimum_weight": float(np.min(result.x)),
    }
    return statistic, diagnostics


def discretize(observation: np.ndarray) -> int:
    position = min(7, max(0, int((observation[0] + 1.2) / 1.8 * 8)))
    velocity = min(7, max(0, int((observation[1] + 0.07) / 0.14 * 8)))
    return position * 8 + velocity


def mountaincar_counts(seed: int, horizon: int, checkpoints: set[int]) -> tuple[np.ndarray, dict[int, np.ndarray]]:
    rng = np.random.default_rng(seed)
    env = gym.make("MountainCar-v0", max_episode_steps=horizon + 1)
    observation, _ = env.reset(seed=seed)
    state, action = discretize(observation), int(rng.integers(3))
    counts = np.zeros((192, 192), dtype=np.int64)
    snapshots = {}
    for step in range(1, horizon + 1):
        next_observation, _, terminated, truncated, _ = env.step(action)
        next_state = discretize(next_observation)
        next_action = int(rng.integers(3))
        counts[state * 3 + action, next_state * 3 + next_action] += 1
        state, action = next_state, next_action
        if step in checkpoints:
            snapshots[step] = counts.copy()
        if terminated or truncated:
            observation, _ = env.reset(seed=seed + step)
            state, action = discretize(observation), int(rng.integers(3))
    env.close()
    return counts, snapshots


def linear_null_counts(features: np.ndarray, seed: int, horizon: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    d = features.shape[1]
    weights = rng.dirichlet(np.ones(64), size=d)
    transition = features @ weights
    state, action = 0, 0
    counts = np.zeros((192, 192), dtype=np.int64)
    for _ in range(horizon):
        next_state = int(rng.choice(64, p=transition[state * 3 + action]))
        next_action = int(rng.integers(3))
        counts[state * 3 + action, next_state * 3 + next_action] += 1
        state, action = next_state, next_action
    return counts


def run_mdp() -> dict:
    horizon = 100000
    checkpoint_values = (1000, 5000, 10000, 25000, 50000, 100000)
    paths = []
    representative = {}
    for trial in range(20):
        counts, snapshots = mountaincar_counts(
            SEED + 120000 + trial,
            horizon,
            set(checkpoint_values) if trial == 0 else set(),
        )
        paths.append(counts)
        if trial == 0:
            representative = snapshots
    rows = []
    controls = []
    solver_checks = []
    primary_solver_fallbacks = 0
    for dimension in (3, 5, 7):
        features = rbf_features(dimension)
        projector = LinearMDPProjector(features)
        final_values = []
        for trial, counts in enumerate(paths):
            statistic = projector.statistic(counts)
            beta = boundary(counts.sum(axis=1), math.log(100))
            final_values.append(statistic)
            rows.append(
                {
                    "kind": "trial_final",
                    "dimension": dimension,
                    "trial": trial,
                    "time": horizon,
                    "L_t": statistic,
                    "beta_t": beta,
                    "rejected": statistic >= beta,
                }
            )
        for checkpoint, counts in representative.items():
            checkpoint_statistic = projector.statistic(counts)
            checkpoint_beta = boundary(counts.sum(axis=1), math.log(100))
            rows.append(
                {
                    "kind": "checkpoint",
                    "dimension": dimension,
                    "trial": 0,
                    "time": checkpoint,
                    "L_t": checkpoint_statistic,
                    "beta_t": checkpoint_beta,
                    "rejected": checkpoint_statistic >= checkpoint_beta,
                }
            )
        null_counts = linear_null_counts(features, SEED + 130000 + dimension, horizon)
        null_statistic = projector.statistic(null_counts)
        null_beta = boundary(null_counts.sum(axis=1), math.log(100))
        controls.append(
            {
                "dimension": dimension,
                "L_t": null_statistic,
                "beta_t": null_beta,
                "rejected": null_statistic >= null_beta,
            }
        )
        if dimension == 5:
            primary_value = final_values[0]
            independent_value, independent_diagnostics = (
                independent_linear_mdp_statistic(features, paths[0])
            )
            solver_checks.append(
                {
                    "dimension": dimension,
                    "primary_L": primary_value,
                    "independent_scipy_L": independent_value,
                    "relative_gap": abs(primary_value - independent_value)
                    / (1 + primary_value),
                    "diagnostics": independent_diagnostics,
                }
            )
        primary_solver_fallbacks += projector.fallback_count
    final_rows = [row for row in rows if row["kind"] == "trial_final"]
    assert len(final_rows) == 20 * 3
    means = {
        dimension: float(np.mean([row["L_t"] for row in final_rows if row["dimension"] == dimension]))
        for dimension in (3, 5, 7)
    }
    detection_rates = {
        dimension: float(np.mean([row["rejected"] for row in final_rows if row["dimension"] == dimension]))
        for dimension in (3, 5, 7)
    }
    print(
        "APPLICATION_MDP_PREASSERT "
        + json.dumps(
            {
                "mean_final_statistic": means,
                "detection_rates": detection_rates,
                "linear_null_controls": controls,
                "independent_solver_checks": solver_checks,
                "primary_solver_fallbacks": primary_solver_fallbacks,
                "final_rows_by_dimension": {
                    dimension: sum(
                        row["dimension"] == dimension for row in final_rows
                    )
                    for dimension in (3, 5, 7)
                },
            }
        ),
        flush=True,
    )
    assert means[3] > means[5] > means[7]
    assert all(not row["rejected"] for row in controls)
    assert solver_checks[0]["relative_gap"] < 5e-3
    return {
        "rows": rows,
        "linear_null_controls": controls,
        "independent_solver_checks": solver_checks,
        "mean_final_statistic": means,
        "detection_rates": detection_rates,
        "trials": 20,
        "horizon": horizon,
        "state_grid": "8x8",
        "actions": 3,
        "dimensions": [3, 5, 7],
        "alpha": 0.01,
        "rbf_sigma_substitution": 32.0,
        "reported_check_interval": 100,
        "evaluated_checkpoints": list(checkpoint_values),
        "primary_solver_fallbacks": primary_solver_fallbacks,
        "final_rows_by_dimension": {
            dimension: sum(row["dimension"] == dimension for row in final_rows)
            for dimension in (3, 5, 7)
        },
    }


def main() -> None:
    started = time.perf_counter()
    print("APPLICATION_PHASE mcmc_start")
    mcmc = run_mcmc()
    print(
        "APPLICATION_MCMC_SUMMARY",
        json.dumps(
            {
                key: value
                for key, value in mcmc.items()
                if key not in {"bad_runs", "good_runs"}
            }
        ),
    )
    print("APPLICATION_PHASE mdp_start")
    mdp = run_mdp()
    print(
        "APPLICATION_MDP_SUMMARY",
        json.dumps({key: value for key, value in mdp.items() if key != "rows"}),
    )
    folder = common_files(
        "claim6",
        {
            "verdict": "VERIFIED",
            "statement": "Section 5 applies Algorithm 1 to MCMC stationary-kernel misspecification and linear-transition validation in MDPs.",
            "acceptance": "Use both paper applications and composite nulls at the reported state/action dimensions, trial counts, and horizons; require valid-null controls and independent solver agreement.",
        },
        "# Source audit\n\nAnchors `body.tex:cor:applications_mcmc` / ar5iv `#S5.Thmtheorem1` and `body.tex:cor:applications_mdp` / ar5iv `#S5.Thmtheorem3`. Appendix G supplies the exact MCMC matrices and the MountainCar dimensions, policy, ranks, horizon, and trial count.",
        "# Method\n\nMCMC uses the published target and exact good/bad 5×5 kernels with a convex stationary-distribution null. MDP uses Gymnasium MountainCar-v0, an 8×8 discretization, three actions, a uniform policy, ranks 3/5/7, 100,000 transitions, and 20 seeds. Each GLR is a constrained maximum-likelihood projection and the boundary is Algorithm 1's beta_t.",
        "# Limitations\n\nThe source omits the RBF bandwidth and random seeds; sigma=32 and all seeds are pinned here. MountainCar statistics are evaluated at six durable checkpoints rather than every reported 100 steps, although all 100,000 transitions and all 20 trials are generated. MCMC stopping times are interval-censored at 50 steps under the alternative and null checks use 250-step intervals.",
    )
    dump(folder / "raw_mcmc.json", mcmc)
    csv_rows(folder / "raw_mdp.csv", mdp["rows"])
    dump(
        folder / "independent_checker_output.json",
        {
            "mcmc_solver_relative_gap": mcmc["independent_relative_gap"],
            "mdp_solver_checks": mdp["independent_solver_checks"],
            "stationary_good_max_error": float(
                np.max(np.abs(np.asarray(mcmc["stationary_good"]) - TARGET))
            ),
        },
    )
    negative = {
        "mcmc_valid_null_false_rejections": mcmc["good_false_rejections"],
        "linear_mdp_null_controls": mdp["linear_null_controls"],
        "negative_controls_passed": mcmc["good_false_rejections"] == 0
        and all(not row["rejected"] for row in mdp["linear_null_controls"]),
    }
    assert negative["negative_controls_passed"]
    dump(folder / "negative_control_output.json", negative)
    result = {
        "verdict": "VERIFIED",
        "mcmc_bad_detection_rate": mcmc["bad_detection_rate"],
        "mcmc_good_false_rejections": mcmc["good_false_rejections"],
        "mcmc_mean_bad_stop": mcmc["mean_bad_stop"],
        "mdp_detection_rates": mdp["detection_rates"],
        "mdp_mean_final_statistic": mdp["mean_final_statistic"],
        "runtime_seconds": time.perf_counter() - started,
    }
    dump(folder / "verifier_output.json", result)
    text(
        folder / "EVAL.md",
        "# Claim 6 — VERIFIED\n\nBoth applications were executed with their actual composite null classes. "
        f"MCMC detected `{mcmc['bad_detection_rate']:.3f}` of 100 bad-kernel runs and rejected 0/100 valid-kernel runs. "
        f"MountainCar final rejection rates were `{mdp['detection_rates']}`; all generated linear-null controls stayed below beta_t.",
    )
    dump(ARTIFACTS / "application_summary.json", result)
    print("APPLICATION_CAMPAIGN_SUMMARY")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
