from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / ".openresearch" / "artifacts"
IMAGES = Path(__file__).resolve().parent / "images"
IMAGES.mkdir(parents=True, exist_ok=True)

NAVY = "#172554"
BLUE = "#2563eb"
CYAN = "#0891b2"
GREEN = "#15803d"
AMBER = "#d97706"
RED = "#b91c1c"
GRAY = "#64748b"
PALE = "#e2e8f0"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.titleweight": "bold",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
    }
)


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(IMAGES / name, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def claim_overview() -> None:
    labels = [
        "C1 full lower bound",
        "C2 Poisson bound",
        "C3 Algorithm 1",
        "C4 one-sided",
        "C5 two-sided",
        "C6 applications",
    ]
    judged_credit = np.array([1, 0, 1, 1, 1, 1], dtype=float)
    contract_pass = np.array([1, 1, 1, 1, 1, 1], dtype=float)
    y = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(10.5, 4.8))
    ax.barh(y + 0.18, judged_credit / 2, height=0.3, color=PALE, label="Live judged credit (5/12)")
    ax.barh(y - 0.18, contract_pass, height=0.3, color=GREEN, label="Candidate claim contract passed")
    ax.set_yticks(y, labels)
    ax.set_xlim(0, 1.03)
    ax.set_xticks([0, 0.5, 1], ["0", "partial", "complete"])
    ax.invert_yaxis()
    ax.set_title("The 5/12 revision omitted the executable evidence behind all six contracts")
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.14),
        ncol=2,
        frameon=False,
    )
    ax.grid(axis="x", alpha=0.2)
    fig.text(0.98, 0.02, "Executable repair published; awaiting a new live verdict", color=RED, fontsize=9, ha="right")
    fig.subplots_adjust(bottom=0.24)
    save(fig, "headline_claim_status.png")


def algorithm_trace() -> None:
    raw = json.loads((ARTIFACTS / "claim3" / "raw_trace.json").read_text())
    trace = raw["trace"]
    time = np.array([row["time"] for row in trace])
    statistic = np.array([row["L_t"] for row in trace])
    boundary = np.array([row["beta_t"] for row in trace])
    fig, ax = plt.subplots(figsize=(10.5, 4.8))
    ax.plot(time, statistic, color=BLUE, lw=2.2, label=r"Composite GLR $L_t$")
    ax.plot(time, boundary, color=AMBER, lw=2.2, label=r"Adaptive boundary $\beta_t$")
    stop = int(raw["stopping_time"])
    ax.axvline(stop, color=GREEN, ls="--", lw=1.5)
    ax.scatter([stop], [statistic[-1]], color=GREEN, zorder=5)
    ax.annotate(
        f"stop at t={stop}",
        (stop, statistic[-1]),
        xytext=(-120, -38),
        textcoords="offset points",
        arrowprops={"arrowstyle": "->", "color": GREEN},
        color=GREEN,
        weight="bold",
    )
    ax.set_xlabel("Transitions")
    ax.set_ylabel("Statistic")
    ax.set_title("Algorithm 1 stops only when the composite GLR crosses its adaptive boundary")
    ax.legend(frameon=False)
    ax.grid(alpha=0.2)
    save(fig, "algorithm1_boundary.png")


def asymptotic_trend() -> None:
    with (ARTIFACTS / "claim4" / "raw_alpha_sweep.csv").open() as handle:
        rows = list(csv.DictReader(handle))
    x = np.array([float(row["log_inverse_alpha"]) for row in rows])
    ratio = np.array([float(row["mean_tau_over_log"]) for row in rows])
    target = float(rows[0]["target_inverse_D"])
    se_ratio = np.array([float(row["se_tau"]) / float(row["log_inverse_alpha"]) for row in rows])
    fig, ax = plt.subplots(figsize=(10.5, 4.8))
    ax.errorbar(x, ratio, yerr=1.96 * se_ratio, marker="o", color=BLUE, capsize=4, lw=2)
    ax.axhline(target, color=GREEN, ls="--", lw=2, label=rf"$1/D^\inf_M={target:.3f}$")
    ax.set_xscale("log", base=2)
    ax.set_xticks(x, [f"{value:g}" for value in x])
    ax.set_xlabel(r"$\log(1/\alpha)$")
    ax.set_ylabel(r"$E[\tau_\alpha]/\log(1/\alpha)$")
    ax.set_title("Algorithm 1's normalized stopping time moves toward the theorem coefficient")
    ax.legend(frameon=False)
    ax.grid(alpha=0.2)
    save(fig, "one_sided_optimality.png")


def applications() -> None:
    mcmc = json.loads((ARTIFACTS / "claim6" / "raw_mcmc.json").read_text())
    with (ARTIFACTS / "claim6" / "raw_mdp.csv").open() as handle:
        mdp_rows = list(csv.DictReader(handle))
    finals = [row for row in mdp_rows if row["kind"] == "trial_final"]
    dimensions = [3, 5, 7]
    means = [
        np.mean([float(row["L_t"]) for row in finals if int(row["dimension"]) == dimension])
        for dimension in dimensions
    ]
    rates = [
        np.mean([row["rejected"] == "True" for row in finals if int(row["dimension"]) == dimension])
        for dimension in dimensions
    ]
    fig, (left, right) = plt.subplots(1, 2, figsize=(11.2, 4.8))
    left.bar(["Misspecified", "Correct null"], [mcmc["bad_detection_rate"], mcmc["good_false_rejections"] / 100], color=[GREEN, PALE])
    left.set_ylim(0, 1.08)
    left.set_ylabel("Rejection rate")
    left.set_title("MCMC kernel check (100 trials each)")
    left.text(0, 1.02, "100/100", ha="center", weight="bold", color=GREEN)
    left.text(1, 0.03, "0/100", ha="center", weight="bold", color=NAVY)
    left.grid(axis="y", alpha=0.2)

    bars = right.bar([str(d) for d in dimensions], means, color=[BLUE, CYAN, GREEN])
    right.set_xlabel("Feature dimension d")
    right.set_ylabel(r"Mean final $L_t$")
    right.set_title("MountainCar 8×8, 20 trials, 100k steps")
    right.grid(axis="y", alpha=0.2)
    for bar, rate in zip(bars, rates, strict=True):
        right.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 3500,
            f"{rate:.0%} reject",
            ha="center",
            fontsize=9,
            weight="bold",
        )
    fig.suptitle("Both named paper applications are exercised at their reported dimensions", weight="bold", y=1.03)
    fig.tight_layout()
    save(fig, "applications.png")


def diagnostics() -> None:
    checker = json.loads((ARTIFACTS / "claim6" / "independent_checker_output.json").read_text())
    negative = json.loads((ARTIFACTS / "claim6" / "negative_control_output.json").read_text())
    mdp_controls = negative["linear_mdp_null_controls"]
    margins = [
        1 - float(row["L_t"]) / float(row["beta_t"])
        for row in mdp_controls
    ]
    solver = checker["mdp_solver_checks"][0]
    fig, (left, right) = plt.subplots(1, 2, figsize=(11.2, 4.6))
    left.bar(["d=3", "d=5", "d=7"], margins, color=[BLUE, CYAN, GREEN])
    left.axhline(0, color=RED, lw=1)
    left.set_ylabel(r"Null margin $1-L_t/\beta_t$")
    left.set_title("Exact linear-null controls remain below boundary")
    left.grid(axis="y", alpha=0.2)
    right.bar(
        ["CLARABEL", "SciPy SLSQP"],
        [float(solver["primary_L"]), float(solver["independent_scipy_L"])],
        color=[BLUE, AMBER],
    )
    right.set_ylabel(r"$L_t$")
    right.set_title(f"Independent projection gap: {float(solver['relative_gap']):.2e}")
    right.ticklabel_format(axis="y", style="plain", useOffset=False)
    right.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    save(fig, "controls_and_solver.png")


if __name__ == "__main__":
    claim_overview()
    algorithm_trace()
    asymptotic_trend()
    applications()
    diagnostics()
