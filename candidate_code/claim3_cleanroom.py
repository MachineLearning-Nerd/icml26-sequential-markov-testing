from __future__ import annotations

import math

import numpy as np
from scipy.optimize import minimize_scalar


def perron_kernel(base: np.ndarray, feature: np.ndarray, theta: float) -> np.ndarray:
    """Construct the paper's tilted kernel with a power-method Perron solver."""
    tilted = base * np.exp(theta * feature)[None, :]
    vector = np.full(len(base), 1.0 / len(base))
    for _ in range(10000):
        next_vector = tilted @ vector
        next_vector /= next_vector.sum()
        if np.max(np.abs(next_vector - vector)) < 1e-14:
            vector = next_vector
            break
        vector = next_vector
    else:
        raise RuntimeError("clean-room Perron iteration did not converge")
    rho = float((tilted @ vector).sum())
    kernel = tilted * vector[None, :] / (rho * vector[:, None])
    return kernel / kernel.sum(axis=1, keepdims=True)


def counts_from_path(path: tuple[int, ...], states: int) -> np.ndarray:
    counts = np.zeros((states, states), dtype=np.int64)
    for left, right in zip(path, path[1:]):
        counts[left, right] += 1
    return counts


def empirical_kernel(counts: np.ndarray) -> np.ndarray:
    states = len(counts)
    visits = counts.sum(axis=1)
    empirical = np.full((states, states), 1.0 / states)
    active = visits > 0
    empirical[active] = counts[active] / visits[active, None]
    return empirical


def rowwise_glr(
    counts: np.ndarray,
    base: np.ndarray,
    feature: np.ndarray,
    low: float,
    high: float,
) -> tuple[float, float, list[float]]:
    visits = counts.sum(axis=1)
    empirical = empirical_kernel(counts)

    def objective(theta: float) -> float:
        kernel = perron_kernel(base, feature, theta)
        rows = []
        for row in range(len(counts)):
            if visits[row] == 0:
                rows.append(0.0)
                continue
            positive = empirical[row] > 0
            divergence = float(
                np.sum(
                    empirical[row, positive]
                    * np.log(empirical[row, positive] / kernel[row, positive])
                )
            )
            rows.append(float(visits[row]) * divergence)
        return float(sum(rows))

    result = minimize_scalar(
        objective,
        bounds=(low, high),
        method="bounded",
        options={"xatol": 1e-11},
    )
    candidates = [
        (objective(low), low),
        (objective(high), high),
        (float(result.fun), float(result.x)),
    ]
    statistic, theta = min(candidates)
    kernel = perron_kernel(base, feature, theta)
    contributions = []
    for row in range(len(counts)):
        if visits[row] == 0:
            contributions.append(0.0)
            continue
        positive = empirical[row] > 0
        divergence = float(
            np.sum(
                empirical[row, positive]
                * np.log(empirical[row, positive] / kernel[row, positive])
            )
        )
        contributions.append(float(visits[row]) * divergence)
    return statistic, theta, contributions


def adaptive_boundary(visits: np.ndarray, log_inverse_error: float) -> float:
    states = len(visits)
    psi = sum(
        math.log(math.e * (1.0 + float(count) / (states - 1)))
        for count in visits
    )
    return log_inverse_error + (states - 1) * psi
