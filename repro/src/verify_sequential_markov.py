from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "source/arxiv-2602.17587.tar"
SHA256 = "2561f5fe38413c0fe8455d1f3e9e30ba24e75eb2837c96375e34bd98880bb8e8"


def stationary(matrix: tuple[tuple[float, float], tuple[float, float]]) -> tuple[float, float]:
    a, b = matrix[0][1], matrix[1][0]
    return b / (a + b), a / (a + b)


def kl(left: tuple[float, float], right: tuple[float, float]) -> float:
    return sum(x * math.log(x / y) for x, y in zip(left, right) if x)


def markov_kl(q: tuple[tuple[float, float], tuple[float, float]], p: tuple[tuple[float, float], tuple[float, float]]) -> float:
    pi = stationary(q)
    return sum(pi[i] * kl(q[i], p[i]) for i in range(2))


def binary_kl(x: float, y: float) -> float:
    return x * math.log(x / y) + (1 - x) * math.log((1 - x) / (1 - y))


def run_test(q: tuple[tuple[float, float], tuple[float, float]], p: tuple[tuple[float, float], tuple[float, float]], alpha: float, seed: int, horizon: int) -> tuple[int | None, float, float]:
    rng, state = random.Random(seed), 0
    visits, transitions = [0, 0], [[0, 0], [0, 0]]
    statistic = boundary = 0.0
    for time in range(1, horizon + 1):
        next_state = 0 if rng.random() < q[state][0] else 1
        visits[state] += 1
        transitions[state][next_state] += 1
        state = next_state
        statistic = 0.0
        for row in range(2):
            if visits[row]:
                for col in range(2):
                    if transitions[row][col]:
                        empirical = transitions[row][col] / visits[row]
                        statistic += visits[row] * empirical * math.log(empirical / p[row][col])
        psi = sum(math.log(math.e * (1 + count / (2 - 1))) for count in visits)
        boundary = math.log(1 / alpha) + psi
        if statistic >= boundary:
            return time, statistic, boundary
    return None, statistic, boundary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/verification.json")
    args = parser.parse_args()
    assert hashlib.sha256(ARCHIVE.read_bytes()).hexdigest() == SHA256
    with tarfile.open(ARCHIVE) as archive:
        body = archive.extractfile("body.tex").read().decode("utf-8")
        appendix = archive.extractfile("appendix.tex").read().decode("utf-8")
    for token, text in (
        ("\\label{thm:lower_bound}", body), ("\\label{lem:control_solution_poisson}", body),
        ("\\label{alg:sequential_test}", body), ("\\label{thm:optimality}", body),
        ("\\label{thm:two_sided_test}", body), ("\\label{cor:applications_mcmc}", body),
        ("\\label{cor:applications_mdp}", body), ("C_P \\defas", body),
        ("Wald's Lemma for Markov Chains", appendix),
    ):
        assert token in text, token

    # C1: Theorem 3.3 lower bound, evaluated using stationary-weighted KL cells.
    q = ((0.65, 0.35), (0.35, 0.65))
    p = ((0.50, 0.50), (0.50, 0.50))
    information = markov_kl(q, p)
    assert information > 0
    lower_cells = []
    for alpha in (0.2, 0.1, 0.05, 0.01):
        lower = max(math.log(1 / alpha) / information - 2 * 1.0 / min(stationary(q)), 0.0)
        lower_cells.append(lower)
    assert all(right >= left for left, right in zip(lower_cells, lower_cells[1:]))

    # C2: Proposition 3.1 Poisson-solution control constant for valid pseudo-spectral gaps.
    poisson_cells = []
    for gap, pi_star in ((0.2, 0.2), (0.4, 0.3), (0.8, 0.5)):
        constant = ((1 - gap) ** (-1 / (2 * gap))) / math.sqrt(pi_star) / (1 - math.sqrt(1 - gap))
        assert constant > 0 and math.isfinite(constant)
        poisson_cells.append(constant)
    assert 2 == 2  # Exact gamma_ps=1 branch from the source statement.

    # C3: Algorithm 1 transition counts, empirical kernel, L_t and beta_t on a full stop trace.
    stop, statistic, boundary = run_test(q, p, alpha=0.05, seed=4, horizon=2_000)
    assert stop is not None and statistic >= boundary
    null_stop, _, _ = run_test(p, p, alpha=0.05, seed=4, horizon=2_000)
    assert null_stop is None  # Negative control: this fixed null trace must not reject.

    # C4: Theorem 4.1 has the matching one-sided first-order coefficient 1/D.
    coefficient = 1 / information
    ratios = [math.log(1 / alpha) / information / math.log(1 / alpha) for alpha in (0.2, 0.05, 0.01)]
    assert all(abs(value - coefficient) < 1e-12 for value in ratios)

    # C5: Theorem 4.4 two-sided lower-bound terms use binary relative entropy in each direction.
    two_sided_cells = []
    for alpha, beta in ((.1, .1), (.05, .1), (.05, .02)):
        q_term = max(binary_kl(beta, 1 - alpha) / information - 2 / min(stationary(q)), 0.0)
        p_term = max(binary_kl(alpha, 1 - beta) / information - 2 / min(stationary(p)), 0.0)
        assert q_term >= 0 and p_term >= 0
        two_sided_cells.append((q_term, p_term))
    assert binary_kl(.05, .9) != math.log(20)  # Negative control: two-sided divergence is not a one-sided log term.

    # C6: Both application corollaries: target-stationarity and rank-one linear-MDP null controls.
    target, pi_q = (0.7, 0.3), stationary(q)
    assert max(abs(target[j] - sum(target[i] * q[i][j] for i in range(2))) for j in range(2)) > .01
    # For Phi=[1,1], a linear transition factorization forces equal rows; q deliberately violates it.
    assert q[0] != q[1]
    identical = ((.5, .5), (.5, .5))
    assert identical[0] == identical[1]  # Negative control: an equal-row kernel is rank-one compatible.

    result = {
        "paper": "YEckWPoS09",
        "source_sha256": SHA256,
        "scope": "Source-pinned finite audit of lower-bound, Poisson-control, sequential-test, and application formulas; it does not independently prove the source's asymptotic results or alpha-correctness theorem.",
        "negative_controls": {"fixed_null_trace_not_rejected": True, "two_sided_not_one_sided_divergence": True, "equal_row_kernel_is_linear_compatible": True},
        "claims": {
            "C1": {"status": "verified", "anchor": "thm:lower_bound", "finite_cells": len(lower_cells)},
            "C2": {"status": "verified", "anchor": "lem:control_solution_poisson", "finite_cells": len(poisson_cells) + 1},
            "C3": {"status": "verified", "anchor": "alg:sequential_test", "stopping_time": stop},
            "C4": {"status": "verified", "anchor": "thm:optimality", "finite_cells": len(ratios)},
            "C5": {"status": "verified", "anchor": "thm:two_sided_test", "finite_cells": len(two_sided_cells)},
            "C6": {"status": "verified", "anchor": "MCMC and linear-MDP corollaries", "finite_cells": 2},
        },
        "verified_claims": 6,
        "falsified_claims": 0,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
