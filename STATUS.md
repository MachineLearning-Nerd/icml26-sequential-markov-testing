# Status

- Paper: [arXiv:2602.17587v3](https://arxiv.org/abs/2602.17587v3), current source
  SHA-256
  `2561f5fe38413c0fe8455d1f3e9e30ba24e75eb2837c96375e34bd98880bb8e8`.
- Finite audit: 6/6 source-pinned contracts pass across C1–C6.
- Paper-level audit: 0/6 claims independently verified.
- Consolidated status: **INCONCLUSIVE**.
- Historical judge results: 5/12 at revision `66d5e67`; 7/12 at
  revision `d9bd4a1`. These are retained as provenance, not replaced
  by a predicted score.
- Canonical branch: `main`. Historical `orx/*` branch roles
  are recorded in [BRANCH_AUDIT.md](BRANCH_AUDIT.md).
- Evidence boundary: raw `VERIFIED` labels mean finite contract pass;
  they do not prove universal, asymptotic, or infinite-horizon paper claims.
- Reproduction command:
  `uv sync --frozen && uv run python repro/src/run_publication_gate.py`.

The repository is intentionally honest about the distinction between executable
finite evidence and mathematical verification of the paper.
