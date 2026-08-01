# Conclusion

The candidate resolves all six selected claims as **VERIFIED** under explicit,
source-pinned contracts. Claims 1–2 combine exact witnesses with audits of the
universal proof dependencies; Claim 3 exhaustively checks Algorithm 1's
components; Claims 4–5 combine executable martingale/proof certificates with
finite-sample confidence gates; and Claim 6 reruns both named applications.
Every negative control is required to fail, all evidence regenerates from the
single fixed command, and no GPU was used.

This is not a predicted score. The live result remains 7/12 until the candidate
is published to the existing Space and independently judged.

## Reproducibility notes

- Fixed command: `uv sync --frozen && uv run python repro/src/run_publication_gate.py`
- Deterministic seed: `260217587`
- Primary paper-source SHA-256: `2561f5fe38413c0fe8455d1f3e9e30ba24e75eb2837c96375e34bd98880bb8e8`
- Compute: Hugging Face `cpu-upgrade`, CPU only
- Current evidence map: [judge response](#/judge-response), [campaign report](#/candidate-report), [negative controls](#/negative-controls), and [release gate](#/tests-and-gate)

## Preserved archive

The exact judged files remain present and reachable: [overview](#/overview),
[old Claim 1](#/claim-1-lower-bound), [old Claim 4](#/claim-4-alpha-correct-optimal),
[old Claim 5](#/claim-5-two-sided), [methods](#/methods), [claims](#/claims),
[evidence](#/evidence), [verification run](#/verification-run), and the
[historical conclusion](#/conclusion). These archived pages are retained as
provenance and are not the candidate verdicts.
