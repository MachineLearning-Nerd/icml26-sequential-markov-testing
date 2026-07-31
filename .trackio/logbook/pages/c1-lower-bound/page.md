# C1 — full Theorem 3.3 lower bound

**Verdict: VERIFIED**

**Executable evidence.** [`run_claim1`](../../candidate_code/run_core_campaign.py)
computes the projection, stationary law, Poisson solution, `C_Q`, and the full
correction. [`verify_claim1`](../../verify_candidate.py) recomputes them from
scratch and checks the published CSV; its precomputed output is
[`judge_visible_verifier.json`](../../evidence/judge_visible_verifier.json).

This check retains the term omitted by the old reproduction:

\[
\mathbb E_Q[\tau_\alpha]\geq
\left(\frac{\log(1/\alpha)}{D^\inf_M(Q,\mathcal P)}
-\frac{2C_Q}{\min_i\pi_i}\right)^+.
\]

On the source-matched five-state composite-null instance,
`D_inf=0.5255872657`, `C_Q=16.39753751`, and
`pi_min=0.1020932807`, so the full correction is `321.2265763`.
At `log(1/alpha)=337.6652`, the leading term is `642.4532` and the
full non-vacuous bound is `321.2266`.

The checker recomputes the stationary law, information projection, actual
Poisson solution and residual, Proposition 3.1 constant, and each inequality
used in the published derivation. A mutant that drops the correction is
rejected.

The producing and independent-checking operations are visible here, not only
linked from an external repository:

```python
information, theta_star = family.information_projection(q)
p_star = parametric_kernel(family.base, family.feature, theta_star)
pi = stationary(q)
paper_c, exact_norm, gamma_ps, best_k = poisson_bound(q)
omega = poisson_solution(q, row_kl(q, p_star))
penalty = 2.0 * paper_c / float(pi.min())
full_lower_bound = max(log_inverse_alpha / information - penalty, 0.0)
assert exact_norm <= paper_c * (1 + 1e-10)
assert np.max(np.abs((np.eye(5) - q) @ omega - (row_kl(q, p_star) - pi @ row_kl(q, p_star)))) < 1e-9
```

The separate `verify_claim1` reloads the CSV, recomputes `information`,
`theta_star`, `pi`, `C_Q`, the actual Poisson norm, `gamma_ps`, and every full
bound cell, then executes `assert all(checks.values())`.

- [Claim contract](../../evidence/claim1/claim_contract.json)
- [Raw bound cells](../../evidence/claim1/raw_lower_bound.csv)
- [Independent checker](../../evidence/claim1/independent_checker_output.json)
- [Executable source manifest](../../candidate_code/source_manifest.json)
- [Complete producer](../../candidate_code/run_core_campaign.py)
- [Complete independent verifier](../../verify_candidate.py)
- [Limitations](../../evidence/claim1/limitations_and_deviations.md)
