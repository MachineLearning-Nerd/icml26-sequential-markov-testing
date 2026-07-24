# C3 — composite Algorithm 1

**Verdict: VERIFIED**

**Executable evidence.** [`ThetaFamily.glr`, `boundary`, and
`simulate_test`](../../candidate_code/markov_core.py) implement the empirical
kernel, row-wise composite likelihood projection, and adaptive boundary.
[`verify_claim3`](../../verify_candidate.py) independently rebuilds every
recorded empirical row, the 4,001-point GLR, and `beta_t`; see its
[`precomputed output`](../../evidence/judge_visible_verifier.json).

The implementation follows Algorithm 1 rather than a known-alternative SPRT:
transition counts, empirical row kernels, a continuous composite-null
information projection, row-wise KL accumulation, `psi_t`, and
`beta_t=(m-1)psi_t+log(1/alpha)`.

The accepted five-state trace stops at transition `93`. Counts sum exactly to
time, the refined GLR agrees with an independent 4,001-point dense grid, the
boundary is recomputed independently, and the projected parameter lies in the
null interval. Dropping the `(m-1)` multiplier changes the stop to `7`, so the
boundary mutant is detected.

- [Claim contract](../../evidence/claim3/claim_contract.json)
- [Raw trace](../../evidence/claim3/raw_trace.json)
- [Independent checker](../../evidence/claim3/independent_checker_output.json)
- [Negative control](../../evidence/claim3/negative_control_output.json)
- [Executable source manifest](../../candidate_code/source_manifest.json)
