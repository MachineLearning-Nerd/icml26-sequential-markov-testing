# C4 — one-sided alpha control and optimality

**Verdict: VERIFIED**

The test here is the paper's composite Algorithm 1. Across 200 finite-horizon
composite-null trials spanning five null parameters and all five initial
states, it has `0/200` false alarms. The exact one-sided 95% binomial upper
bound is `0.014867`, below `alpha=0.05`.

Across `log(1/alpha)=20,40,80,160,320`, twenty alternative trials per cell
give normalized mean stopping times `6.225, 4.43875, 3.30875, 2.74969,
2.40125`, moving toward the exact coefficient `1/D_inf=1.90263`. Removing
`psi_t` causes `100/100` null mutant paths to stop.

Finite Monte Carlo supports but does not replace the theorem's infinite-limit
proof.

- [Raw alpha sweep](../../evidence/claim4/raw_alpha_sweep.csv)
- [Alpha checker](../../evidence/claim4/independent_checker_output.json)
- [Boundary mutant](../../evidence/claim4/negative_control_output.json)
- [Limitations](../../evidence/claim4/limitations_and_deviations.md)
