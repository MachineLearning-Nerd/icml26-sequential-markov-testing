from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize_scalar


def stationary(kernel: np.ndarray) -> np.ndarray:
    """Return the unique stationary distribution of an ergodic kernel."""
    m = kernel.shape[0]
    system = np.vstack((kernel.T - np.eye(m), np.ones(m)))
    rhs = np.r_[np.zeros(m), 1.0]
    value, *_ = np.linalg.lstsq(system, rhs, rcond=None)
    value = np.maximum(value, 0.0)
    return value / value.sum()


def row_kl(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    if np.any((left > 0) & (right <= 0)):
        return np.full(left.shape[0], np.inf)
    terms = np.zeros_like(left, dtype=float)
    mask = left > 0
    terms[mask] = left[mask] * np.log(left[mask] / right[mask])
    return terms.sum(axis=1)


def markov_kl(left: np.ndarray, right: np.ndarray) -> float:
    return float(stationary(left) @ row_kl(left, right))


def pseudo_spectral_gap(kernel: np.ndarray) -> tuple[float, int, list[dict[str, float]]]:
    """Compute gamma_ps with a finite stopping certificate.

    Once k > 1 / best, the universal bound gap(A_k)/k <= 1/k proves that
    no untested k can improve the incumbent.
    """
    pi = stationary(kernel)
    reverse = kernel.T * pi[None, :] / pi[:, None]
    p_power = np.eye(len(pi))
    r_power = np.eye(len(pi))
    best, best_k, rows, k = 0.0, 0, [], 0
    while True:
        k += 1
        p_power = p_power @ kernel
        r_power = reverse @ r_power
        multiplicative = r_power @ p_power
        similarity = np.sqrt(pi)[:, None] * multiplicative / np.sqrt(pi)[None, :]
        eigenvalues = np.linalg.eigvalsh((similarity + similarity.T) / 2)
        gap = max(0.0, 1.0 - float(np.sort(eigenvalues)[-2]))
        candidate = gap / k
        rows.append({"k": k, "gap": gap, "gap_over_k": candidate})
        if candidate > best:
            best, best_k = candidate, k
        if best > 0 and k > 1.0 / best:
            break
        if k >= 10000:
            raise RuntimeError("pseudo-spectral-gap certificate did not terminate")
    return best, best_k, rows


def poisson_operator(kernel: np.ndarray) -> np.ndarray:
    pi = stationary(kernel)
    projection = np.ones((len(pi), 1)) @ pi[None, :]
    return np.linalg.solve(np.eye(len(pi)) - kernel + projection, np.eye(len(pi)) - projection)


def poisson_solution(kernel: np.ndarray, function: np.ndarray) -> np.ndarray:
    return poisson_operator(kernel) @ function


def poisson_bound(kernel: np.ndarray) -> tuple[float, float, float, int]:
    pi = stationary(kernel)
    gap, best_k, _ = pseudo_spectral_gap(kernel)
    if math.isclose(gap, 1.0, abs_tol=1e-12):
        paper_constant = 2.0
    else:
        paper_constant = (
            (1.0 - gap) ** (-1.0 / (2.0 * gap))
            / math.sqrt(float(pi.min()))
            / (1.0 - math.sqrt(1.0 - gap))
        )
    exact_operator_norm = float(np.max(np.sum(np.abs(poisson_operator(kernel)), axis=1)))
    return paper_constant, exact_operator_norm, gap, best_k


def empirical_log_likelihood(counts: np.ndarray) -> float:
    visits = counts.sum(axis=1)
    value = 0.0
    for i in range(len(visits)):
        if visits[i] <= 0:
            continue
        mask = counts[i] > 0
        value += float(
            np.sum(counts[i, mask] * np.log(counts[i, mask] / visits[i]))
        )
    return value


def parametric_kernel(base: np.ndarray, feature: np.ndarray, theta: float) -> np.ndarray:
    tilted = base * np.exp(theta * feature)[None, :]
    values, vectors = np.linalg.eig(tilted)
    index = int(np.argmax(values.real))
    rho = float(values[index].real)
    vector = np.abs(vectors[:, index].real)
    vector /= vector.sum()
    kernel = tilted * vector[None, :] / (rho * vector[:, None])
    kernel = np.maximum(kernel.real, 1e-300)
    return kernel / kernel.sum(axis=1, keepdims=True)


@dataclass
class ThetaFamily:
    base: np.ndarray
    feature: np.ndarray
    low: float
    high: float
    grid_size: int = 401

    def __post_init__(self) -> None:
        self.grid = np.linspace(self.low, self.high, self.grid_size)
        self.kernels = np.stack(
            [parametric_kernel(self.base, self.feature, float(x)) for x in self.grid]
        )
        self.log_kernels = np.log(self.kernels)

    def glr(self, counts: np.ndarray, refine: bool = True) -> tuple[float, float]:
        empirical = empirical_log_likelihood(counts)
        likelihoods = np.einsum("gij,ij->g", self.log_kernels, counts)
        index = int(np.argmax(likelihoods))
        theta = float(self.grid[index])
        null_log_likelihood = float(likelihoods[index])
        if refine:
            left = float(self.grid[max(0, index - 1)])
            right = float(self.grid[min(self.grid_size - 1, index + 1)])

            def objective(value: float) -> float:
                return -float(np.sum(counts * np.log(parametric_kernel(self.base, self.feature, value))))

            result = minimize_scalar(
                objective,
                bounds=(left, right),
                method="bounded",
                options={"xatol": 1e-11},
            )
            if result.success and -float(result.fun) >= null_log_likelihood:
                theta = float(result.x)
                null_log_likelihood = -float(result.fun)
        return max(0.0, empirical - null_log_likelihood), theta

    def information_projection(self, alternative: np.ndarray) -> tuple[float, float]:
        result = minimize_scalar(
            lambda theta: markov_kl(
                alternative, parametric_kernel(self.base, self.feature, theta)
            ),
            bounds=(self.low, self.high),
            method="bounded",
            options={"xatol": 1e-12},
        )
        if not result.success:
            raise RuntimeError(result.message)
        return float(result.fun), float(result.x)


def boundary(visits: np.ndarray, log_inverse_error: float, multiplier: float | None = None) -> float:
    m = len(visits)
    psi = float(np.log(math.e * (1.0 + visits / (m - 1))).sum())
    return log_inverse_error + (m - 1 if multiplier is None else multiplier) * psi


def simulate_test(
    kernel: np.ndarray,
    family: ThetaFamily,
    log_inverse_error: float,
    seed: int,
    horizon: int,
    initial_state: int = 0,
    boundary_multiplier: float | None = None,
    trace: bool = False,
) -> dict:
    rng = np.random.default_rng(seed)
    state, m = initial_state, len(kernel)
    counts = np.zeros((m, m), dtype=np.int64)
    trace_rows = []
    last_statistic = last_boundary = last_theta = 0.0
    for time in range(1, horizon + 1):
        next_state = int(rng.choice(m, p=kernel[state]))
        counts[state, next_state] += 1
        state = next_state
        visits = counts.sum(axis=1)
        last_boundary = boundary(visits, log_inverse_error, boundary_multiplier)
        # A grid gives an upper bound on the true GLR (the continuous null
        # likelihood is at least the grid maximum). Refine whenever that bound
        # is near the boundary; otherwise it already certifies "continue".
        last_statistic, last_theta = family.glr(counts, refine=False)
        if last_statistic >= last_boundary - 2.0:
            last_statistic, last_theta = family.glr(counts, refine=True)
        if trace and (time <= 10 or time % 50 == 0 or last_statistic >= last_boundary):
            empirical = np.full((m, m), 1.0 / m)
            active = visits > 0
            empirical[active] = counts[active] / visits[active, None]
            trace_rows.append(
                {
                    "time": time,
                    "counts": counts.tolist(),
                    "empirical_kernel": empirical.tolist(),
                    "visits": visits.tolist(),
                    "L_t": last_statistic,
                    "beta_t": last_boundary,
                    "theta_hat": last_theta,
                }
            )
        if last_statistic >= last_boundary:
            return {
                "stopped": True,
                "stopping_time": time,
                "L_t": last_statistic,
                "beta_t": last_boundary,
                "theta_hat": last_theta,
                "counts": counts.tolist(),
                "trace": trace_rows,
            }
    return {
        "stopped": False,
        "stopping_time": None,
        "L_t": last_statistic,
        "beta_t": last_boundary,
        "theta_hat": last_theta,
        "counts": counts.tolist(),
        "trace": trace_rows,
    }
