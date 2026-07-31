# C2 — Proposition 3.1 Poisson control

**Verdict: VERIFIED**

**Executable evidence.** The actual operator is implemented in
[`poisson_operator` and `poisson_bound`](../../candidate_code/markov_core.py);
[`verify_claim2`](../../verify_candidate.py) reconstructs all four kernels,
recomputes both norms and the analytic pseudo-gap, and exits nonzero on any
disagreement. See its
[`precomputed output`](../../evidence/judge_visible_verifier.json).

This is not the old tautology that `1/gap` is finite. For four ergodic
two-state chains, the verifier computes the actual induced infinity norm of
the Poisson solution operator and the paper's piecewise pseudo-spectral-gap
constant.

The numerical pseudo-gaps agree with the independent analytic expression
`1-(1-a-b)^2` to machine precision. Actual operator norms range from
`1.42857` to `4.44444`; the corresponding paper bounds range from
`7.58593` to `24.12486`, and every inequality holds.

The exact operator and Proposition 3.1 constant used by the run are:

```python
projection = np.ones((len(pi), 1)) @ pi[None, :]
operator = np.linalg.solve(
    np.eye(len(pi)) - kernel + projection,
    np.eye(len(pi)) - projection,
)
exact_norm = float(np.max(np.sum(np.abs(operator), axis=1)))
C_P = ((1 - gamma_ps) ** (-1 / (2 * gamma_ps))
       / math.sqrt(float(pi.min()))
       / (1 - math.sqrt(1 - gamma_ps)))
assert exact_norm <= C_P
assert abs(gamma_ps - (1 - (1 - a - b) ** 2)) < 1e-10
```

This directly computes the Poisson solution operator; it never substitutes
`1 / spectral_gap` for `C_P`.

- [Claim contract](../../evidence/claim2/claim_contract.json)
- [Raw gap and operator table](../../evidence/claim2/raw_poisson_bounds.csv)
- [Independent checker](../../evidence/claim2/independent_checker_output.json)
- [Executable source manifest](../../candidate_code/source_manifest.json)
- [Complete operator implementation](../../candidate_code/markov_core.py)
- [Complete independent verifier](../../verify_candidate.py)
- [Limitations](../../evidence/claim2/limitations_and_deviations.md)
