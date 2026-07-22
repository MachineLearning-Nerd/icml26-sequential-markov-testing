# Asymptotically Optimal Sequential Testing with Markovian Data

CPU-only, source-pinned finite certificate for ICML 2026 OpenReview `YEckWPoS09`
and arXiv:2602.17587.

## Reproduce

```bash
python3 -m venv .venv
.venv/bin/python repro/src/run_publication_gate.py
```

Only the Python standard library is required. The fail-closed gate hashes the
archived primary source, verifies six source anchors, executes a deterministic
two-state Algorithm-1 trace, runs independent tests, and only then writes
`outputs/publication_gate.json`.

1. Theorem `thm:lower_bound` stationary-weighted-KL lower-bound formula.
2. Proposition `lem:control_solution_poisson` and its pseudo-spectral-gap constant.
3. Algorithm `alg:sequential_test`: transition counts, empirical rows, statistic, and boundary.
4. Theorem `thm:optimality` one-sided first-order coefficient.
5. Theorem `thm:two_sided_test` binary-relative-entropy terms.
6. The MCMC-misspecification and linear-MDP application corollaries.

## Scope

The primary source is pinned at SHA-256
`2561f5fe38413c0fe8455d1f3e9e30ba24e75eb2837c96375e34bd98880bb8e8`.
This bundle is a finite source-formula and algorithm audit. It does not replace
the paper's asymptotic proofs or independently establish alpha-correctness.
It is CPU-only: no Hugging Face job, GPU, T4, or L4 is used.
