# C1 — full Theorem 3.3 lower bound

**Verdict: VERIFIED**

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

- [Claim contract](../../evidence/claim1/claim_contract.json)
- [Raw bound cells](../../evidence/claim1/raw_lower_bound.csv)
- [Independent checker](../../evidence/claim1/independent_checker_output.json)
- [Limitations](../../evidence/claim1/limitations_and_deviations.md)
