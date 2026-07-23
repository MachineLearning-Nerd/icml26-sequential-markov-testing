# C2 — Proposition 3.1 Poisson control

**Verdict: VERIFIED**

This is not the old tautology that `1/gap` is finite. For four ergodic
two-state chains, the verifier computes the actual induced infinity norm of
the Poisson solution operator and the paper's piecewise pseudo-spectral-gap
constant.

The numerical pseudo-gaps agree with the independent analytic expression
`1-(1-a-b)^2` to machine precision. Actual operator norms range from
`1.42857` to `4.44444`; the corresponding paper bounds range from
`7.58593` to `24.12486`, and every inequality holds.

- [Claim contract](../../evidence/claim2/claim_contract.json)
- [Raw gap and operator table](../../evidence/claim2/raw_poisson_bounds.csv)
- [Independent checker](../../evidence/claim2/independent_checker_output.json)
- [Limitations](../../evidence/claim2/limitations_and_deviations.md)
