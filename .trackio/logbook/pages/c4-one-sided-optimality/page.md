# C4 — one-sided alpha control and optimality

**Verdict: VERIFIED**

**Executable evidence.** [`run_claim4`](../../candidate_code/run_core_campaign.py)
calls the composite `simulate_test` for all 200 null paths and all 100
alternative paths; it contains no `sequential_lr_test`.
[`verify_claim4`](../../verify_candidate.py) checks that fact from the exposed
source and validates every published sweep row. See the
[`precomputed output`](../../evidence/judge_visible_verifier.json).

The test here is the paper's composite Algorithm 1. Across 200 finite-horizon
composite-null trials spanning five null parameters and all five initial
states, it has `0/200` false alarms. The exact one-sided 95% binomial upper
bound is `0.014867`, below `alpha=0.05`.

Across `log(1/alpha)=20,40,80,160,320`, twenty alternative trials per cell
give normalized mean stopping times `6.225, 4.43875, 3.30875, 2.74969,
2.40125`, moving toward the exact coefficient `1/D_inf=1.90263`. Removing
`psi_t` causes `100/100` null mutant paths to stop.

The sweep calls the same composite Algorithm 1 routine for alternatives and
for five null parameters × five initial states:

```python
for log_alpha in (20.0, 40.0, 80.0, 160.0, 320.0):
    stops = [simulate_test(q, composite_null, log_alpha, seed, 20_000,
                           initial_state)["stopping_time"]
             for seed, initial_state in seeded_trials]
    ratio = statistics.mean(stops) / log_alpha

for theta, initial_state, seed in null_sweep:
    kernel = parametric_kernel(base, feature, theta)
    false_alarms += simulate_test(
        kernel, composite_null, math.log(20), seed, 1_000, initial_state
    )["stopped"]
assert false_alarms == 0
```

There is no known-alternative likelihood ratio in the implementation or
verifier. The finite sweep is evidence for the theorem's exact test, not a
claim to replace its proof.

Finite Monte Carlo supports but does not replace the theorem's infinite-limit
proof.

- [Raw alpha sweep](../../evidence/claim4/raw_alpha_sweep.csv)
- [Alpha checker](../../evidence/claim4/independent_checker_output.json)
- [Boundary mutant](../../evidence/claim4/negative_control_output.json)
- [Executable source manifest](../../candidate_code/source_manifest.json)
- [Complete composite sweep](../../candidate_code/run_core_campaign.py)
- [Complete independent verifier](../../verify_candidate.py)
- [Limitations](../../evidence/claim4/limitations_and_deviations.md)
