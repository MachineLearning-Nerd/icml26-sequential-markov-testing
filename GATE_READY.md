# Publication gate

This repository is gate-ready as a finite evidence audit, not as a paper-proof
claim.

- Finite contracts: 6/6 pass.
- Paper-level claims independently verified: 0/6.
- Overall status: **INCONCLUSIVE**.
- Gate output: [publication_gate.json](publication_gate.json).
- Raw contract output: [outputs/verification.json](outputs/verification.json).

The full command is:

```bash
uv sync --frozen && uv run python repro/src/run_publication_gate.py
```

The gate checks the declared finite inputs, generated evidence, negative
controls, and release files. It does not establish universal quantifiers,
infinite-horizon alpha control, or asymptotic optimality.
