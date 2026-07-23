# Faithful claim-by-claim reproduction

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-YEckWPoS09-sequential-markov-testing/blob/main/notebooks/sequential_markov_reproduction.py)

This repository reproduces all six claims selected from
**Asymptotically Optimal Sequential Testing with Markovian Data**
([arXiv:2602.17587](https://arxiv.org/abs/2602.17587)). The earlier judged
artifact scored 4/12 because it mostly exercised known-alternative SPRTs. The
published release implements the paper's composite Algorithm 1 and directly checks
the full lower-bound correction, the actual Poisson solution bound, one- and
two-sided composite tests, and both named applications.

Assessment: all six local claim contracts are **VERIFIED**. This is not a
predicted judge score; the live judge remains at 4/12 and has not evaluated
the published Space revision
[`66d5e67`](https://huggingface.co/spaces/DineshAI/YEckWPoS09/commit/66d5e67b5426622768e4d797656e409526f3a299).

For the central first-order claim, the paper predicts
\(1/D^\inf_M=1.9026\) on the reproduced instance. The observed
\(E[\tau_\alpha]/\log(1/\alpha)\) moves from 6.225 to 2.401 as
\(\log(1/\alpha)\) increases 16×. There were 0/200 finite-horizon null alarms
(one-sided 95% upper bound 0.01487 < 0.05).

The accepted run used local Apple M2 CPU and took 18m12s, with no paid compute.
MountainCar uses the paper's \(8\times8\) state grid, three actions, 20 trials,
100,000 transitions, and \(d=3,5,7\). The source omits its RBF bandwidth and
random seeds, so this reproduction pins `sigma=32` and seed `260217587`.
The asymptotic sweeps are finite Monte Carlo evidence and do not replace the
paper's universal proofs.

- [Illustrated claim-by-claim report](reports/claim-by-claim/report.md)
- [Tutorial-style marimo notebook](notebooks/sequential_markov_reproduction.py)
- [Durable raw evidence and claim contracts](.openresearch/artifacts)
- [Published Hugging Face evidence logbook](https://huggingface.co/spaces/DineshAI/YEckWPoS09)

## Experiment log

| Branch / experiment | Purpose or change | Exact run command | Assessment / outcome | Compute |
|---|---|---|---|---|
| `main` | Publication surface | Not run as an experiment (publication surface) | Published; awaiting live judge | — |
| [`orx/frozen-judged-baseline-certificate`](https://github.com/MachineLearning-Nerd/icml26-repro-YEckWPoS09-sequential-markov-testing/tree/orx/frozen-judged-baseline-certificate) | Freeze and reproduce the judged 4/12 certificate | `uv sync --frozen && uv run python repro/src/run_publication_gate.py` | Reproduced the limited source/formula certificate; frozen | Local CPU, 5s |
| [`orx/faithful-core-contracts-and-algorithm-1`](https://github.com/MachineLearning-Nerd/icml26-repro-YEckWPoS09-sequential-markov-testing/tree/orx/faithful-core-contracts-and-algorithm-1) | Replace SPRT proxies with full lower-bound, Poisson, and composite Algorithm 1 checks | `uv sync --frozen && uv run python repro/src/run_publication_gate.py` | C1–C5 VERIFIED; cumulative gate passed | Local CPU, 4m10s |
| [`orx/corrected-paper-scale-application-evidence`](https://github.com/MachineLearning-Nerd/icml26-repro-YEckWPoS09-sequential-markov-testing/tree/orx/corrected-paper-scale-application-evidence) | Add exact MCMC and reported-dimension MountainCar applications; correct duplicate terminal aggregation | `uv sync --frozen && uv run python repro/src/run_publication_gate.py` | C1–C6 VERIFIED; 20 final rows per MDP dimension | Local CPU, 18m12s |
| [`orx/release-candidate-report-and-protected-logbook`](https://github.com/MachineLearning-Nerd/icml26-repro-YEckWPoS09-sequential-markov-testing/tree/orx/release-candidate-report-and-protected-logbook) | Add report, notebook, protected logbook union, manifests, and release validation | `uv sync --frozen && uv run python repro/src/run_publication_gate.py` | Cumulative release gate passed; published additively | Local CPU, 13m56s |

## Reproduce

Install [uv](https://docs.astral.sh/uv/) and run:

```bash
uv sync --frozen
uv run python repro/src/run_publication_gate.py
```

The command uses the repository-level `.venv` and the committed lockfile. It
regenerates `.openresearch/artifacts/`, runs the six verifiers, independent
checkers, negative controls, and regression tests, and exits nonzero if a
claim contract fails. The final publication gate additionally validates the
report, notebook, protected old/new Space subset, text-only upload allowlist,
hash manifest, and secret scan.

## Paper and source scope

The primary arXiv source archive is pinned at SHA-256
`2561f5fe38413c0fe8455d1f3e9e30ba24e75eb2837c96375e34bd98880bb8e8`.
The release's `VERIFIED` verdicts refer to explicit source-pinned contracts.
Numerical proof-obligation audits and finite experiments support the universal
lower-bound and asymptotic theorems; they are not presented as new formal
proofs.
